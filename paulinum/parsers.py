# -*- coding: utf-8 -*-
"""
parsers.py — analizadores de los formatos de origen.

Cada analizador devuelve una lista de «partes» (una por documento resultante) con la estructura
    {"part": <n o ''>, "title": <str>, "tokens": [Token, ...]}
donde Token es un dict con las claves: form (forma tal como aparece), lemma (o ''), pos (o ''),
person ('1', '2', '3' o ''), ref (referencia de capítulo y versículo o de sección, como cadena).

Formatos (A.1): MorphGNT (tabla morfológica), Open Apostolic Fathers (texto por referencia),
TEI de Perseus y First1KGreek, PROIEL (XML), MACULA (TSV), Diorisis (XML; solo para el lexicón)
y textos locales (data/local, formato «ref\ttexto» o texto corrido).

El filtro «solo tokens griegos» (§ 0.1 del informe de la campaña 03) se aplica en corpus.py,
al normalizar; aquí se conservan todos los tokens con su forma cruda.
"""
from __future__ import annotations

import csv
import io
import re
from typing import Iterator

from lxml import etree

from .text import tokenize, beta_to_unicode, is_greek

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"


def _tok(form: str, lemma: str = "", pos: str = "", person: str = "", ref: str = "", mood: str = "") -> dict:
    return {"form": form, "lemma": lemma, "pos": pos, "person": person, "ref": ref, "mood": mood}


# ---------------------------------------------------------------------------------------------
# MorphGNT / SBLGNT
# ---------------------------------------------------------------------------------------------
def parse_morphgnt(path: str) -> list[dict]:
    """
    Columnas: bcv, pos, parse, text, word, normalized, lemma.
    parse = persona, tiempo, voz, modo, caso, número, género, grado (8 posiciones).
    Se usa la columna `normalized` (forma sin puntuación ni signos críticos).
    """
    tokens = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(" ")
            if len(parts) < 7:
                continue
            bcv, pos, parse, _text, _word, normalized, lemma = parts[:7]
            ch, vs = int(bcv[2:4]), int(bcv[4:6])
            person = parse[0] if parse and parse[0] in "123" else ""
            mood = parse[3] if len(parse) > 3 and parse[3] in "ISOPDN" else ""  # D = imperativo
            tokens.append(_tok(normalized, lemma, pos.strip("-"), person, f"{ch}:{vs}", mood))
    return [{"part": "", "title": "", "tokens": tokens}]


# ---------------------------------------------------------------------------------------------
# Open Apostolic Fathers (texto de Lake): «ref texto» por línea
# ---------------------------------------------------------------------------------------------
def parse_af(path: str) -> list[dict]:
    tokens = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^([\d\.]+)\s+(.*)$", line)
            if not m:
                continue
            ref, text = m.group(1), m.group(2)
            # 1.1.1 (Hermas: visión.capítulo.versículo) → capítulo:versículo uniforme
            bits = ref.split(".")
            ref_norm = ":".join(bits[-2:]) if len(bits) >= 2 else ref
            if len(bits) == 3:
                ref_norm = f"{bits[0]}.{bits[1]}:{bits[2]}"
            for w in tokenize(text):
                tokens.append(_tok(w, ref=ref_norm))
    return [{"part": "", "title": "", "tokens": tokens}]


# ---------------------------------------------------------------------------------------------
# Textos locales (data/local): «ref\ttexto» o texto corrido
# ---------------------------------------------------------------------------------------------
def parse_local(path: str) -> list[dict]:
    tokens = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "\t" in line:
                ref, text = line.split("\t", 1)
            else:
                ref, text = str(i), line
            for w in tokenize(text):
                tokens.append(_tok(w, ref=ref))
    return [{"part": "", "title": "", "tokens": tokens}]


# ---------------------------------------------------------------------------------------------
# TEI (Perseus canonical-greekLit, First1KGreek)
# ---------------------------------------------------------------------------------------------
_SKIP_TAGS = {"note", "bibl", "head", "del", "gap", "rdg", "label", "speaker", "figDesc", "ref", "milestone",
              "pb", "lb", "cb", "fw", "teiHeader", "front", "back", "witDetail", "app_rdg"}
_TEXTPART_TAGS = {"div", "div1", "div2", "div3"}


def _local(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.split("}")[-1]


def _iter_text(el, ref_chain: list[str]) -> Iterator[tuple[str, str]]:
    """Recorre el árbol produciendo (texto, ref) sin entrar en aparato, notas ni títulos."""
    for child in el:
        tag = _local(child.tag)
        if tag in _SKIP_TAGS or child.tag is etree.Comment:
            if child.tail:
                yield child.tail, ".".join(ref_chain)
            continue
        if tag == "app":  # aparato crítico: solo el lema
            for lem in child:
                if _local(lem.tag) == "lem":
                    yield from _iter_text(lem, ref_chain)
                    if lem.text:
                        yield lem.text, ".".join(ref_chain)
            if child.tail:
                yield child.tail, ".".join(ref_chain)
            continue
        new_chain = ref_chain
        if tag in _TEXTPART_TAGS or tag in ("l", "p", "seg", "said", "q", "quote", "sp"):
            n = child.get("n")
            if n and tag in _TEXTPART_TAGS:
                new_chain = ref_chain + [n]
        if child.text:
            yield child.text, ".".join(new_chain)
        yield from _iter_text(child, new_chain)
        if child.tail:
            yield child.tail, ".".join(ref_chain)


def _tokens_from(el, ref_chain) -> list[dict]:
    toks = []
    if el.text:
        for w in tokenize(el.text):
            toks.append(_tok(w, ref=".".join(ref_chain)))
    for text, ref in _iter_text(el, ref_chain):
        for w in tokenize(text):
            toks.append(_tok(w, ref=ref))
    return toks


def _textparts(body, subtypes: set[str]) -> list:
    """Divisiones textuales del subtipo pedido (cualquier profundidad, sin anidar unas en otras)."""
    found = []
    for el in body.iter():
        if _local(el.tag) in _TEXTPART_TAGS and (el.get("subtype") or "").lower() in subtypes:
            # no incluir descendientes de otro hallazgo
            anc = el.getparent()
            nested = False
            while anc is not None:
                if anc in found:
                    nested = True
                    break
                anc = anc.getparent()
            if not nested:
                found.append(el)
    return found


def parse_tei(path: str, split: str = "", min_tokens: int = 0, max_docs: int = 0,
              group_min_tokens: int = 0) -> list[dict]:
    """
    split = '' → un documento; 'books' → un documento por libro; 'letters' → uno por carta;
    'chapters' → capítulos agrupados hasta alcanzar `min_tokens` (Justino, Diálogo).
    """
    parser = etree.XMLParser(recover=True, huge_tree=True, remove_blank_text=False)
    tree = etree.parse(path, parser)
    root = tree.getroot()
    body = None
    for el in root.iter():
        if _local(el.tag) == "body":
            body = el
            break
    if body is None:
        body = root
    if not split:
        return [{"part": "", "title": "", "tokens": _tokens_from(body, [])}]
    subtypes = {"books": {"book", "liber", "libro"}, "letters": {"letter", "epistle", "epistula", "epist", "ep"},
                "chapters": {"chapter", "section", "caput", "capitulum"}}[split]
    parts = _textparts(body, subtypes)
    if not parts:  # respaldo: primer nivel de textparts
        parts = [el for el in body.iter() if _local(el.tag) in _TEXTPART_TAGS and el.get("type") == "textpart"
                 and not any(_local(a.tag) in _TEXTPART_TAGS and a.get("type") == "textpart"
                             for a in el.iterancestors())]
    out = []
    for el in parts:
        n = el.get("n") or str(len(out) + 1)
        toks = _tokens_from(el, [n])
        toks = [t for t in toks if is_greek(t["form"])]
        out.append({"part": n, "title": n, "tokens": toks})
    if split == "letters":
        # las colecciones de cartas numeran las cartas; se descartan fragmentos y piezas no numeradas
        numeric = [p for p in out if str(p["part"]).isdigit()]
        if len(numeric) >= len(out) / 2:
            out = numeric
    if split == "chapters":
        # agrupar capítulos consecutivos hasta ≥ min_tokens
        grouped, acc, first = [], [], None
        for p in out:
            if first is None:
                first = p["part"]
            acc.extend(p["tokens"])
            if len(acc) >= max(min_tokens, 1):
                grouped.append({"part": f"{first}-{p['part']}" if first != p["part"] else first,
                                "title": first, "tokens": acc})
                acc, first = [], None
        if acc and grouped:
            grouped[-1]["tokens"].extend(acc)
            grouped[-1]["part"] = grouped[-1]["part"].split("-")[0] + f"-{out[-1]['part']}"
        out = grouped
    if min_tokens and split != "chapters":
        out = [p for p in out if len(p["tokens"]) >= min_tokens]
    if max_docs:
        out = out[:max_docs]
    return out


# ---------------------------------------------------------------------------------------------
# PROIEL greek-nt.xml (Tischendorf)
# ---------------------------------------------------------------------------------------------
PROIEL_BOOKS = {
    "MATT": "Mt", "MARK": "Mc", "LUKE": "Lc", "JOHN": "Jn", "ACTS": "Hch", "ROM": "Rom", "1COR": "1Cor",
    "2COR": "2Cor", "GAL": "Gal", "EPH": "Ef", "PHIL": "Flp", "COL": "Col", "1THESS": "1Tes", "2THESS": "2Tes",
    "1TIM": "1Tim", "2TIM": "2Tim", "TIT": "Tit", "PHILEM": "Flm", "HEB": "Heb", "JAS": "Sant", "1PET": "1Pe",
    "2PET": "2Pe", "1JOHN": "1Jn", "2JOHN": "2Jn", "3JOHN": "3Jn", "JUDE": "Jud", "REV": "Ap",
}


def parse_proiel(path: str) -> dict[str, list[dict]]:
    """Devuelve {id_libro: tokens} para los 27 libros del NT (edición de Tischendorf)."""
    books: dict[str, list[dict]] = {}
    for _, el in etree.iterparse(path, events=("end",), tag="token", huge_tree=True):
        form = el.get("form")
        cit = el.get("citation-part") or ""
        if form and cit:
            book_code, _, ref = cit.partition(" ")
            book = PROIEL_BOOKS.get(book_code.upper())
            if book:
                morph = el.get("morphology") or ""
                person = morph[0] if morph and morph[0] in "123" else ""
                mood = {"m": "D", "i": "I", "s": "S", "o": "O", "n": "N", "p": "P"}.get(morph[3], "") if len(morph) > 3 else ""
                books.setdefault(book, []).append(
                    _tok(form, el.get("lemma") or "", el.get("part-of-speech") or "", person, ref.replace(".", ":"), mood))
        el.clear()
        while el.getprevious() is not None:
            del el.getparent()[0]
    return books


# ---------------------------------------------------------------------------------------------
# MACULA (Nestle 1904 / SBLGNT), TSV
# ---------------------------------------------------------------------------------------------
MACULA_BOOKS = {
    "MAT": "Mt", "MRK": "Mc", "LUK": "Lc", "JHN": "Jn", "ACT": "Hch", "ROM": "Rom", "1CO": "1Cor", "2CO": "2Cor",
    "GAL": "Gal", "EPH": "Ef", "PHP": "Flp", "COL": "Col", "1TH": "1Tes", "2TH": "2Tes", "1TI": "1Tim", "2TI": "2Tim",
    "TIT": "Tit", "PHM": "Flm", "HEB": "Heb", "JAS": "Sant", "1PE": "1Pe", "2PE": "2Pe", "1JN": "1Jn", "2JN": "2Jn",
    "3JN": "3Jn", "JUD": "Jud", "REV": "Ap",
}


def parse_macula(path: str) -> dict[str, list[dict]]:
    books: dict[str, list[dict]] = {}
    with open(path, encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in rd:
            ref = row.get("ref") or ""
            m = re.match(r"^(\w+) (\d+):(\d+)", ref)
            if not m:
                continue
            book = MACULA_BOOKS.get(m.group(1))
            if not book:
                continue
            form = (row.get("normalized") or row.get("text") or "").strip()
            if not form:
                continue
            person = {"first": "1", "second": "2", "third": "3"}.get((row.get("person") or "").strip(), "")
            mood = {"imperative": "D", "indicative": "I", "subjunctive": "S", "optative": "O", "infinitive": "N",
                    "participle": "P"}.get((row.get("mood") or "").strip(), "")
            books.setdefault(book, []).append(
                _tok(form, (row.get("lemma") or "").strip(), (row.get("class") or "").strip(), person,
                     f"{m.group(2)}:{m.group(3)}", mood))
    return books


# ---------------------------------------------------------------------------------------------
# Diorisis (Vatri y McGillivray): pares forma → lema para el diccionario uniforme
# ---------------------------------------------------------------------------------------------
def iter_diorisis_pairs(xml_bytes: bytes) -> Iterator[tuple[str, str]]:
    """Itera (forma, lema) en Unicode a partir de un archivo XML de Diorisis (formas en Beta Code)."""
    for _, el in etree.iterparse(io.BytesIO(xml_bytes), events=("end",), tag="word", huge_tree=True, recover=True):
        form = el.get("form")
        if form:
            lemma = ""
            for ch in el:
                if _local(ch.tag) == "lemma":
                    lemma = ch.get("entry") or ""
                    break
            if lemma:
                yield beta_to_unicode(form), beta_to_unicode(lemma)
        el.clear()


PARSERS = {"morphgnt": parse_morphgnt, "af": parse_af, "tei": parse_tei, "local": parse_local}

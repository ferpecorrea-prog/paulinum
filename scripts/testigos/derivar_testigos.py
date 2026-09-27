#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derivar_testigos.py — derivados normalizados de los testigos manuscritos (docs/testigos_manuscritos.md, D-013).

Entradas (data/local/testigos/, no versionadas):
  sinaiticus_project_v105.xml   transcripción del proyecto Codex Sinaiticus v1.05 (principal para 01)
  sinaiticus_ntvmr_20001.xml    transcripción NTVMR de 01 (control de transcripción)
  p46_ntvmr_10046.xml           transcripción NTVMR de P46
y la edición SBLGNT (data/raw/morphgnt, vía paulinum.corpus.build_corpus).

Salidas (data/local/testigos/derivados/):
  <testigo>_<carta>_bruto.txt         ref<TAB>texto: mano primera, palabras íntegramente atestiguadas, nomina sacra expandidos,
                                      minúsculas, sin diacríticos, ϲ→σ (no se versiona; huella en provenance)
  <testigo>_<carta>_reg.txt           ídem con la regularización ortográfica guiada por alineación (tabla T)
  <testigo>_<carta>_sblgnt_recortado.txt  SBLGNT (sin diacríticos) recortado a las palabras alineadas con texto atestiguado
  <testigo>_cobertura.csv             por carta y versículo: estado y recuentos
  <testigo>_intervenciones.tsv        cada transformación (expansión, exclusión, regularización), con posición y regla
  acuerdo_ediciones.csv               acuerdo de tokens de cada testigo con SBLGNT por carta, bruto y regularizado
  acuerdo_transcripciones_01.csv      acuerdo entre las dos transcripciones del Sinaítico por carta
  p46_contenido_y_orden.csv           libros contenidos en P46 y su orden en el códice (canal de transmisión)
  RESUMEN.json                        recuentos globales y huellas SHA-256 de todos los derivados

Reglas fijas: mano primera (NTVMR: rdg type="orig"; proyecto: rdg type="main-corr"); palabras con <supplied> o <gap>
excluidas (no se imputan lagunas); <unclear> incluido y contado; nomina sacra expandidos por la tabla NOMINA_SACRA;
regularización: una forma del testigo se sustituye por la de SBLGNT alineada solo si difiere de ella exclusivamente por
las sustituciones de la tabla T (canonización CANON); todo lo demás se conserva.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

from lxml import etree

sys.path.insert(0, os.getcwd())
from paulinum.text import normalize_form, strip_diacritics  # noqa: E402

TEI = "{http://www.tei-c.org/ns/1.0}"
TESTIGOS_DIR = os.path.join("data", "local", "testigos")
OUT_DIR = os.path.join(TESTIGOS_DIR, "derivados")

# Libros: código NTVMR y número del proyecto Sinaiticus → identificador paulinum
NTVMR_BOOKS = {"B06": "Rom", "B07": "1Cor", "B08": "2Cor", "B09": "Gal", "B10": "Ef", "B11": "Flp", "B12": "Col",
               "B13": "1Tes", "B14": "2Tes", "B15": "1Tim", "B16": "2Tim", "B17": "Tit", "B18": "Flm", "B19": "Heb"}
PROJECT_BOOKS = {"37": "Rom", "38": "1Cor", "39": "2Cor", "40": "Gal", "41": "Ef", "42": "Flp", "43": "Col",
                 "44": "1Tes", "45": "2Tes", "46": "Heb", "47": "1Tim", "48": "2Tim", "49": "Tit", "50": "Flm"}
LETTERS = ["Rom", "1Cor", "2Cor", "Gal", "Ef", "Flp", "Col", "1Tes", "2Tes", "1Tim", "2Tim", "Tit", "Flm", "Heb"]

# Tabla cerrada de nomina sacra (forma abreviada sin diacríticos, minúscula → forma plena). Se completa con las
# terminaciones regulares; una abreviatura ausente se conserva tal cual y se registra como «abreviatura no expandida».
_NS_BASE = {
    "θ": ("θε", {"ς": "ος", "υ": "ου", "ω": "ω", "ν": "ον", "ε": "ε"}),           # θεός
    "κ": ("κυρι", {"ς": "ος", "υ": "ου", "ω": "ω", "ν": "ον", "ε": "ε"}),          # κύριος
    "χ": ("χριστ", {"ς": "ος", "υ": "ου", "ω": "ω", "ν": "ον", "ε": "ε"}),         # Χριστός
    "ι": ("ιησου", {"ς": "ς", "υ": "", "ν": "ν"}),                                  # Ἰησοῦς
    "υ": ("υι", {"ς": "ος", "υ": "ου", "ω": "ω", "ν": "ον", "ε": "ε", "οι": "οι", "ων": "ων", "ους": "ους", "οις": "οις"}),  # υἱός
}
NOMINA_SACRA = {}
for _k, (_stem, _ends) in _NS_BASE.items():
    for _ab, _full in _ends.items():
        NOMINA_SACRA[_k + _ab] = _stem + _full
NOMINA_SACRA.update({
    "ιης": "ιησους", "ιη": "ιησου", "ιηυ": "ιησου", "ιην": "ιησουν", "υις": "υιος", "υιυ": "υιου", "υιν": "υιον", "χρς": "χριστος", "χρυ": "χριστου", "χρω": "χριστω", "χρν": "χριστον",
    "πνα": "πνευμα", "πνς": "πνευματος", "πνι": "πνευματι", "πνατος": "πνευματος", "πνατι": "πνευματι", "πνατα": "πνευματα",
    "πνατων": "πνευματων", "πνασι": "πνευμασι", "πνασιν": "πνευμασιν", "πνικος": "πνευματικος", "πνικον": "πνευματικον",
    "πνικοι": "πνευματικοι", "πνικων": "πνευματικων", "πνικα": "πνευματικα", "πνικη": "πνευματικη", "πνικης": "πνευματικης",
    "πνικοις": "πνευματικοις", "πνικας": "πνευματικας", "πνικως": "πνευματικως", "πνικου": "πνευματικου",
    "πηρ": "πατηρ", "πρς": "πατρος", "πρι": "πατρι", "πρα": "πατερα", "περ": "πατερ", "πρες": "πατερες", "πρων": "πατερων",
    "πρσι": "πατρασι", "πρσιν": "πατρασιν", "πρας": "πατερας", "πατρς": "πατρος",
    "ανος": "ανθρωπος", "ανου": "ανθρωπου", "ανω": "ανθρωπω", "ανον": "ανθρωπον", "ανε": "ανθρωπε", "ανοι": "ανθρωποι",
    "ανων": "ανθρωπων", "ανοις": "ανθρωποις", "ανους": "ανθρωπους", "ανινος": "ανθρωπινος", "ανινη": "ανθρωπινη",
    "ανινης": "ανθρωπινης", "ανινον": "ανθρωπινον", "ανινων": "ανθρωπινων",
    "ουνος": "ουρανος", "ουνου": "ουρανου", "ουνω": "ουρανω", "ουνον": "ουρανον", "ουνοι": "ουρανοι", "ουνων": "ουρανων",
    "ουνοις": "ουρανοις", "ουνους": "ουρανους", "ουνιος": "ουρανιος", "ουνιου": "ουρανιου", "ουνιω": "ουρανιω",
    "ουνιον": "ουρανιον", "ουνιοι": "ουρανιοι", "ουνιων": "ουρανιων", "ουνιοις": "ουρανιοις", "ουνιους": "ουρανιους",
    "ουνιας": "ουρανιας",
    "ιηλ": "ισραηλ", "ισλ": "ισραηλ", "ιλημ": "ιερουσαλημ", "ιερλμ": "ιερουσαλημ", "ιηλμ": "ιερουσαλημ", "δαδ": "δαυιδ",
    "στρς": "σταυρος", "στρου": "σταυρου", "στρω": "σταυρω", "στρν": "σταυρον", "στρος": "σταυρος",
    "εστρωθη": "εσταυρωθη", "εστραι": "εσταυρωται", "στρωθη": "σταυρωθη", "στρωσαι": "σταυρωσαι", "συνεστρωθην": "συνεσταυρωθην",
    "σηρ": "σωτηρ", "σωρ": "σωτηρ", "σρς": "σωτηρος", "σρι": "σωτηρι", "σρα": "σωτηρα", "σωρς": "σωτηρος", "σωρι": "σωτηρι", "σωρα": "σωτηρα",
    "μηρ": "μητηρ", "μρς": "μητρος", "μρι": "μητρι", "μρα": "μητερα", "μητρς": "μητρος",
})

NOMINA_SACRA = {k.replace("ς", "σ"): v.replace("ς", "σ") for k, v in NOMINA_SACRA.items()}  # sigma unificada como en norm()

# Tabla T (regularización guiada): canonización que iguala solo las sustituciones admitidas
def canon(s: str) -> str:
    s = s.replace("ει", "ι").replace("η", "ι").replace("οι", "υ").replace("αι", "ε").replace("ω", "ο")
    s = re.sub(r"(.)\1", r"\1", s)          # geminadas
    s = re.sub(r"ν$", "", s)                 # ν efelcística / final
    return s


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def norm(tok: str) -> str:
    """ϲ→σ, minúsculas, sin diacríticos (incluida la diéresis), sigma unificada como en el corpus."""
    tok = tok.replace("ϲ", "σ").replace("Ϲ", "σ")
    tok = re.sub(r"[’ʼ᾽᾿'´‘`]", "", tok)   # apóstrofos y diástoles del copista (no son elisiones del texto)
    tok = normalize_form(tok, keep_diacritics=True)
    return strip_diacritics(tok)


# ---------------------------------------------------------------------------------------------
# Lectura de los XML → {carta: {(c, v): [token, ...]}} con token = dict(text, supplied, gap, unclear, nomsac, abbr)
# ---------------------------------------------------------------------------------------------
def _local(tag) -> str:
    return tag.split("}")[-1] if isinstance(tag, str) else ""


def _w_text(w, first_hand_rdg: str) -> dict:
    """Texto de una <w>, ignorando saltos de línea y marcas; señala supplied/gap/unclear/abbr."""
    parts = []
    flags = {"supplied": False, "gap": False, "unclear": False, "nomsac": False, "abbr": False, "raya": False}

    def walk(el, inside_supplied=False, inside_unclear=False):
        tag = _local(el.tag)
        if tag in ("note", "margin", "pc"):
            return
        if tag == "app":  # aparato dentro de una palabra: tomar la mano primera
            for r in el:
                if _local(r.tag) == "rdg" and r.get("type") == first_hand_rdg:
                    walk(r, inside_supplied, inside_unclear)
                    if r.tail:
                        pass
            return
        if tag == "gap":
            flags["gap"] = True
        if tag == "supplied":
            inside_supplied = True
            flags["supplied"] = True
        if tag == "unclear":
            inside_unclear = True
            flags["unclear"] = True
        if tag == "abbr":
            flags["abbr"] = True
            if (el.get("type") or "") == "nomSac":
                flags["nomsac"] = True
        if tag == "hi" and (el.get("rend") or "") == "ol2":   # proyecto Sinaiticus: raya = nomen sacrum o ν suspendida
            flags["raya"] = True
        # rend="ol" (raya simple sobre υ/ι inicial) no es abreviatura: se ignora
        if el.text and tag not in ("lb", "cb", "pb"):
            parts.append(el.text)
        for ch in el:
            walk(ch, inside_supplied, inside_unclear)
            if ch.tail:
                parts.append(ch.tail)

    walk(w)
    text = "".join(parts)
    text = re.sub(r"\s+", "", text)
    flags["text"] = text
    return flags


def _iter_tokens(ab, first_hand_rdg: str) -> list[dict]:
    """Tokens de un versículo (<ab>), mano primera; los <gap> sueltos se registran como huecos."""
    out = []

    def walk(el):
        for ch in el:
            tag = _local(ch.tag)
            if tag == "w":
                out.append(_w_text(ch, first_hand_rdg))
            elif tag == "app":
                chosen = None
                for r in ch:
                    if _local(r.tag) == "rdg" and r.get("type") == first_hand_rdg:
                        chosen = r
                        break
                if chosen is not None:
                    walk(chosen)
                else:  # sin lectura de la mano primera (p. ej. solo correctores): hueco
                    out.append({"text": "", "gap": True, "supplied": False, "unclear": False, "nomsac": False, "abbr": False, "raya": False})
            elif tag == "gap":
                out.append({"text": "", "gap": True, "supplied": False, "unclear": False, "nomsac": False, "abbr": False, "raya": False})
            elif tag in ("note", "margin", "pc", "lb", "cb", "pb", "hi", "ptr", "g"):
                continue
            else:
                walk(ch)

    walk(ab)
    return out


def read_ntvmr(path: str) -> tuple[dict, list[str]]:
    tree = etree.parse(path, etree.XMLParser(huge_tree=True, recover=True))
    root = tree.getroot()
    letters: dict = defaultdict(dict)
    order = []
    for div in root.iter(TEI + "div"):
        if div.get("type") != "book":
            continue
        book = NTVMR_BOOKS.get(div.get("n") or "")
        if not book:
            continue
        if book not in order:
            order.append(book)
        for ab in div.iter(TEI + "ab"):
            n = ab.get("n") or ""
            m = re.match(r"B\d+K(\d+)V(\d+)", n)
            if not m:
                continue
            key = (int(m.group(1)), int(m.group(2)))
            letters[book].setdefault(key, []).extend(_iter_tokens(ab, "orig"))
    return letters, order


def read_project(path: str) -> tuple[dict, list[str]]:
    tree = etree.parse(path, etree.XMLParser(huge_tree=True, recover=True))
    root = tree.getroot()
    letters: dict = defaultdict(dict)
    order = []
    for div in root.iter():
        if _local(div.tag) != "div" or div.get("type") != "book":
            continue
        book = PROJECT_BOOKS.get(div.get("n") or "")
        if not book:
            continue
        if book not in order:
            order.append(book)
        for ab in div.iter():
            if _local(ab.tag) != "ab":
                continue
            m = re.match(r"V-B\d+K(\d+)V(\d+)-", ab.get("id") or "")
            if not m:
                continue
            key = (int(m.group(1)), int(m.group(2)))
            letters[book].setdefault(key, []).extend(_iter_tokens(ab, "main-corr"))
    return letters, order


# ---------------------------------------------------------------------------------------------
# Derivación
# ---------------------------------------------------------------------------------------------
def sblgnt_by_verse(letter_docs: dict, letter: str) -> dict:
    d = letter_docs[letter]
    out: dict = defaultdict(list)
    for f, ref in zip(d.forms_nodia, d.refs):
        m = re.match(r"(\d+):(\d+)", ref)
        if m:
            out[(int(m.group(1)), int(m.group(2)))].append(f)
    return out


def align(a: list[str], b: list[str]) -> list[tuple[int | None, int | None]]:
    """Alineación de dos listas de formas: pares (i, j); i o j = None si no hay pareja."""
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    pairs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            pairs.extend((i, j) for i, j in zip(range(i1, i2), range(j1, j2)))
        elif tag == "replace":
            la, lb = i2 - i1, j2 - j1
            # segundo nivel: emparejar por canonización T dentro del bloque
            ca = [canon(x) for x in a[i1:i2]]
            cb = [canon(x) for x in b[j1:j2]]
            sm2 = difflib.SequenceMatcher(a=ca, b=cb, autojunk=False)
            for t2, p1, p2, q1, q2 in sm2.get_opcodes():
                if t2 == "equal":
                    pairs.extend((i1 + i, j1 + j) for i, j in zip(range(p1, p2), range(q1, q2)))
                else:
                    n = min(p2 - p1, q2 - q1)
                    for k in range(n):  # emparejamiento posicional (variantes reales): no se regulariza
                        pairs.append((i1 + p1 + k, j1 + q1 + k))
                    for k in range(n, p2 - p1):
                        pairs.append((i1 + p1 + k, None))
                    for k in range(n, q2 - q1):
                        pairs.append((None, j1 + q1 + k))
        elif tag == "delete":
            pairs.extend((i, None) for i in range(i1, i2))
        elif tag == "insert":
            pairs.extend((None, j) for j in range(j1, j2))
    return pairs


def _resolve_raya(form: str, sbl_forms: set) -> str | None:
    """Raya simple (proyecto Sinaiticus): ν omitida. Se restituye solo si con ella la forma coincide (bajo T) con una
    forma de SBLGNT del mismo versículo: al final o, si no, en cualquier posición interior."""
    cands = [form + "ν"] + [form[:i] + "ν" + form[i:] for i in range(1, len(form))]
    canon_sbl = {canon(x): x for x in sbl_forms}
    for c in cands:
        if canon(c) in canon_sbl:
            return c
    return None


def derive(name: str, letters: dict, sbl_all: dict, out_dir: str, log: list, cov_rows: list, agree_rows: list,
           write: bool = True) -> dict:
    stats = Counter()
    hashes = {}
    bruto_by_verse: dict = {}
    for letter in LETTERS:
        if letter not in letters:
            continue
        verses = letters[letter]
        sbl = sbl_all.get(letter, {})
        bruto_lines, reg_lines, sbl_lines = [], [], []
        agree_b = agree_r = aligned = 0
        n_wit_tokens = n_sbl_tokens = 0
        for key in sorted(verses):
            toks = verses[key]
            ref = f"{key[0]}:{key[1]}"
            sbl_v = sbl.get(key, [])
            sbl_set = set(sbl_v)
            n_total = 0
            kept = []
            for pos, t in enumerate(toks):
                if not t["text"] and not (t["gap"] or t["supplied"]):
                    stats["omisiones_mano_primera"] += 1   # <w/> vacía: la mano primera no escribió nada aquí
                    continue
                if t["text"] and not norm(t["text"]):
                    stats["signos_de_puntuacion"] += 1     # <w>·</w>
                    continue
                n_total += 1
                stats["tokens_total"] += 1
                if t["gap"] or t["supplied"]:
                    reason = "hueco" if t["gap"] else "supplied"
                    log.append([name, letter, ref, pos, t["text"], "", f"exclusión ({reason})"])
                    stats["excluidos_" + reason] += 1
                    continue
                form = norm(t["text"])
                if t["nomsac"] or t["abbr"] or t.get("raya"):
                    full = NOMINA_SACRA.get(form)
                    if full:
                        log.append([name, letter, ref, pos, form, full, "expansión de nomen sacrum"])
                        stats["nomina_sacra_expandidos"] += 1
                        form = full
                    else:
                        r = _resolve_raya(form, sbl_set)
                        if r:
                            log.append([name, letter, ref, pos, form, r, "ν suspendida restituida (raya, guiada por SBLGNT)"])
                            stats["nu_restituidas"] += 1
                            form = r
                        elif form and form[-1] in "αεηιουω":
                            log.append([name, letter, ref, pos, form, form + "ν", "ν final restituida (raya sobre vocal final, convención)"])
                            stats["nu_restituidas_convencion"] += 1
                            form = form + "ν"
                        else:
                            log.append([name, letter, ref, pos, form, form, "raya sin expansión (ni nomen sacrum de tabla ni ν)"])
                            stats["rayas_sin_expansion"] += 1
                if t["unclear"]:
                    stats["unclear_incluidos"] += 1
                kept.append(form)
            bruto_by_verse.setdefault(letter, {})[key] = list(kept)
            n_wit_tokens += len(kept)
            n_sbl_tokens += len(sbl_v)
            estado = "no_contenido" if n_total == 0 else ("laguna" if not kept else ("parcial" if len(kept) < n_total else "conservado"))
            if not sbl_v and kept:
                estado = "sin_correspondencia_sblgnt"
            cov_rows.append([name, letter, key[0], key[1], estado, n_total, len(kept), len(sbl_v)])
            if not kept:
                continue
            pairs = align(kept, sbl_v)
            reg = list(kept)
            sbl_cut = []
            for i, j in pairs:
                if i is None or j is None:
                    continue
                aligned += 1
                w, s_ = kept[i], sbl_v[j]
                if w == s_:
                    agree_b += 1
                    agree_r += 1
                elif canon(w) == canon(s_):
                    reg[i] = s_
                    agree_r += 1
                    log.append([name, letter, ref, i, w, s_, "regularización (tabla T)"])
                    stats["regularizados"] += 1
                else:
                    stats["variantes_conservadas"] += 1
                sbl_cut.append(s_)
            bruto_lines.append(f"{ref}\t{' '.join(kept)}")
            reg_lines.append(f"{ref}\t{' '.join(reg)}")
            if sbl_cut:
                sbl_lines.append(f"{ref}\t{' '.join(sbl_cut)}")
        if not bruto_lines or not write:
            continue
        for suffix, lines in (("bruto", bruto_lines), ("reg", reg_lines), ("sblgnt_recortado", sbl_lines)):
            p = os.path.join(out_dir, f"{name}_{letter}_{suffix}.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            hashes[os.path.basename(p)] = sha256(p)
        agree_rows.append([name, letter, n_wit_tokens, n_sbl_tokens, aligned,
                           round(agree_b / aligned, 4) if aligned else "", round(agree_r / aligned, 4) if aligned else ""])
    return {"stats": dict(stats), "hashes": hashes, "bruto": bruto_by_verse}


def compare_transcriptions(a: dict, b: dict) -> tuple[list, list]:
    """Acuerdo entre dos transcripciones del mismo testigo sobre los versículos presentes en ambas, comparando el
    texto bruto derivado con las mismas reglas; devuelve también una muestra de discrepancias."""
    rows, sample = [], []
    for letter in LETTERS:
        if letter not in a or letter not in b:
            continue
        na = nb = eq = 0
        common = set(a[letter]) & set(b[letter])
        for key in sorted(common):
            ta, tb = a[letter][key], b[letter][key]
            na += len(ta)
            nb += len(tb)
            sm = difflib.SequenceMatcher(a=ta, b=tb, autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    eq += i2 - i1
                elif len(sample) < 400:
                    sample.append([letter, f"{key[0]}:{key[1]}", tag, " ".join(ta[i1:i2]), " ".join(tb[j1:j2])])
        rows.append([letter, len(common), len(set(a[letter]) - common), len(set(b[letter]) - common), na, nb, eq,
                     round(2 * eq / (na + nb), 4) if na + nb else ""])
    return rows, sample


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=TESTIGOS_DIR)
    a = ap.parse_args()
    out_dir = os.path.join(a.dir, "derivados")
    os.makedirs(out_dir, exist_ok=True)

    from paulinum.corpus import build_corpus
    docs = build_corpus(tier=1, verbose=False, only_ids=set(LETTERS))
    letter_docs = {d.id: d for d in docs}
    sbl = {L: sblgnt_by_verse(letter_docs, L) for L in LETTERS}

    sources = {
        "sinaiticus": (os.path.join(a.dir, "sinaiticus_project_v105.xml"), read_project),
        "sinaiticus_ntvmr": (os.path.join(a.dir, "sinaiticus_ntvmr_20001.xml"), read_ntvmr),
        "p46": (os.path.join(a.dir, "p46_ntvmr_10046.xml"), read_ntvmr),
    }
    log: list = []
    cov_rows: list = []
    agree_rows: list = []
    resumen = {"fuentes": {}, "derivados": {}, "orden_en_el_codice": {}}
    parsed = {}
    bruto: dict = {}
    for name, (path, reader) in sources.items():
        if not os.path.exists(path):
            print(f"[ausente] {name}: {path}")
            continue
        letters, order = reader(path)
        parsed[name] = letters
        resumen["fuentes"][name] = {"archivo": os.path.basename(path), "sha256": sha256(path),
                                    "cartas": {L: len(letters[L]) for L in LETTERS if L in letters}}
        resumen["orden_en_el_codice"][name] = order
        print(f"{name}: {len(letters)} cartas; versículos: " + ", ".join(f"{L} {len(letters[L])}" for L in LETTERS if L in letters))
        # la copia NTVMR del Sinaítico se procesa con las mismas reglas pero solo como control (sin derivados)
        r = derive(name, letters, sbl, out_dir, log if name != "sinaiticus_ntvmr" else [], cov_rows if name != "sinaiticus_ntvmr" else [],
                   agree_rows if name != "sinaiticus_ntvmr" else [], write=(name != "sinaiticus_ntvmr"))
        bruto[name] = r.pop("bruto")
        resumen["derivados"][name] = r
        print(f"  {name}: {r['stats']}")

    with open(os.path.join(out_dir, "cobertura.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["testigo", "carta", "capitulo", "versiculo", "estado", "tokens_transcritos", "tokens_atestiguados", "tokens_sblgnt"])
        w.writerows(cov_rows)
    with open(os.path.join(out_dir, "intervenciones.tsv"), "w", encoding="utf-8") as f:
        f.write("testigo\tcarta\tref\tposicion\tforma_original\tforma_resultante\tregla\n")
        for row in log:
            f.write("\t".join(str(x) for x in row) + "\n")
    with open(os.path.join(out_dir, "acuerdo_ediciones.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["testigo", "carta", "tokens_testigo", "tokens_sblgnt", "pares_alineados", "acuerdo_bruto", "acuerdo_regularizado"])
        w.writerows(agree_rows)
    if "sinaiticus" in bruto and "sinaiticus_ntvmr" in bruto:
        rows, sample = compare_transcriptions(bruto["sinaiticus"], bruto["sinaiticus_ntvmr"])
        with open(os.path.join(out_dir, "acuerdo_transcripciones_01.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["carta", "versiculos_comunes", "solo_proyecto", "solo_ntvmr", "tokens_proyecto", "tokens_ntvmr", "coincidentes", "acuerdo"])
            w.writerows(rows)
        with open(os.path.join(out_dir, "discrepancias_transcripciones_01_muestra.tsv"), "w", encoding="utf-8") as f:
            f.write("carta\tref\ttipo\tproyecto\tntvmr\n")
            for row in sample:
                f.write("\t".join(row) + "\n")
        resumen["acuerdo_transcripciones_01"] = rows
    if "p46" in parsed:
        with open(os.path.join(out_dir, "p46_contenido_y_orden.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["posicion", "carta", "versiculos_transcritos", "versiculos_con_texto_atestiguado"])
            for i, L in enumerate(resumen["orden_en_el_codice"]["p46"], 1):
                vs = parsed["p46"][L]
                att = sum(1 for k, toks in vs.items() if any(t["text"] and not (t["gap"] or t["supplied"]) for t in toks))
                w.writerow([i, L, len(vs), att])
    # huellas de todos los derivados
    resumen["huellas"] = {fn: sha256(os.path.join(out_dir, fn)) for fn in sorted(os.listdir(out_dir)) if fn != "RESUMEN.json"}
    resumen["tabla_T"] = "ει~ι, η~ι, οι~υ, αι~ε, ω~ο, geminadas, ν final"
    resumen["reglas"] = ["mano primera (NTVMR rdg orig; proyecto rdg main-corr)", "supplied y gap excluidos",
                         "unclear incluido", "nomina sacra: tabla cerrada (proyecto: hi rend=ol2; NTVMR: abbr nomSac)",
                         "raya (ol2) que no es nomen sacrum de tabla: ν restituida donde así coincide bajo T con una forma SBLGNT del versículo; si no hay coincidencia y la raya cae sobre vocal final, ν final por convención; rend=ol (υ/ι inicial) se ignora",
                         "apóstrofos y diástoles del copista eliminados",
                         "<w/> vacía en la mano primera = omisión (nada que excluir); signos de puntuación no cuentan",
                         "regularización: sustitución por la forma SBLGNT alineada solo si difiere únicamente por T"]
    resumen["nomina_sacra_tabla"] = len(NOMINA_SACRA)
    with open(os.path.join(out_dir, "RESUMEN.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    print("→", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

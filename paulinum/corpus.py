# -*- coding: utf-8 -*-
"""
corpus.py — construcción de los documentos con sus capas, división en obras y partes,
máscaras por referencia (fórmulas epistolares, material preformado, citas del AT) y por índice
(pasajes paralelos, metadata/reuse_ranges.csv).

Un Document lleva: id, author, work, work_group, status, tradition, genre, subgenre, addressee,
edition_key, forms (normalizadas, con diacríticos), forms_nodia, lemmas, pos, person, refs y
masks {nombre: [bool]} (True = token excluido por esa máscara).

Los corpus construidos se guardan en data/cache/corpus_<edición>.jsonl (una línea por documento).
"""
from __future__ import annotations

import csv
import json
import os
import re
from dataclasses import dataclass, field, asdict

from . import parsers
from .fetch import raw_path, DATA_DIR
from .sources import ALL_SOURCES, NT, EDITION_SOURCES, Source, by_tier
from .text import normalize_form, strip_diacritics

METADATA_DIR = os.environ.get("PAULINUM_METADATA", "metadata")


@dataclass
class Document:
    id: str
    author: str
    work: str
    status: str
    tradition: str
    edition_key: str
    forms: list[str]
    forms_nodia: list[str] = field(default_factory=list)
    lemmas: list[str] = field(default_factory=list)
    pos: list[str] = field(default_factory=list)
    person: list[str] = field(default_factory=list)
    mood: list[str] = field(default_factory=list)
    refs: list[str] = field(default_factory=list)
    masks: dict = field(default_factory=dict)
    work_group: str = ""
    genre: str = ""
    subgenre: str = ""
    addressee: str = ""
    source_id: str = ""
    part: str = ""

    @property
    def n_tokens(self) -> int:
        return len(self.forms)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @staticmethod
    def from_json(line: str) -> "Document":
        d = json.loads(line)
        return Document(**d)


# ---------------------------------------------------------------------------------------------
# Referencias «capítulo:versículo» y máscaras por referencia
# ---------------------------------------------------------------------------------------------
def _ref_key(ref: str) -> tuple[int, int]:
    m = re.match(r"^(?:[\w\.]+\.)?(\d+):(\d+)", ref or "")
    if not m:
        return (0, 0)
    return int(m.group(1)), int(m.group(2))


def load_mask_table(path: str | None = None) -> dict[str, list[tuple[str, tuple, tuple, str]]]:
    """metadata/masks.csv → {id: [(mask, (c,v)_ini, (c,v)_fin, descripción)]}"""
    path = path or os.path.join(METADATA_DIR, "masks.csv")
    out: dict[str, list] = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("id") or row["id"].startswith("#"):
                continue
            out.setdefault(row["id"], []).append(
                (row["mask"].strip(), _ref_key(row["ref_start"]), _ref_key(row["ref_end"]), row.get("description", "")))
    return out


def load_reuse_table(path: str | None = None) -> dict[str, list[tuple[int, int]]]:
    """metadata/reuse_ranges.csv → {id: [(start, end)]} (posiciones de palabra, fin exclusivo)."""
    path = path or os.path.join(METADATA_DIR, "reuse_ranges.csv")
    out: dict[str, list] = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("id"):
                continue
            out.setdefault(row["id"], []).append((int(row["start"]), int(row["end"])))
    return out


def apply_masks(doc: Document, mask_table: dict, reuse_table: dict) -> None:
    n = doc.n_tokens
    names = {"formulae", "preformed", "otq", "reuse"}
    for name in names:
        doc.masks[name] = [False] * n
    for mask, (c1, v1), (c2, v2), _ in mask_table.get(doc.id, []):
        if mask not in doc.masks:
            doc.masks[mask] = [False] * n
        for i, ref in enumerate(doc.refs):
            c, v = _ref_key(ref)
            if (c1, v1) <= (c, v) <= (c2, v2) and c:
                doc.masks[mask][i] = True
    for start, end in reuse_table.get(doc.id, []):
        for i in range(max(0, start), min(n, end)):
            doc.masks["reuse"][i] = True


def mask_vector(doc: Document, mask_spec: str) -> list[bool]:
    """
    mask_spec: 'none' | 'reuse' | 'all' (= formulae+preformed+otq) | 'formulae+preformed+otq' | combinación con '+'.
    Devuelve la lista de tokens EXCLUIDOS.
    """
    if not mask_spec or mask_spec == "none":
        return [False] * doc.n_tokens
    parts = ["formulae", "preformed", "otq"] if mask_spec == "all" else mask_spec.split("+")
    out = [False] * doc.n_tokens
    for p in parts:
        m = doc.masks.get(p)
        if m:
            out = [a or b for a, b in zip(out, m)]
    return out


def masked_tokens(doc: Document, mask_spec: str, nodia: bool = False, layer: str = "forms") -> list[str]:
    seq = getattr(doc, layer)
    if layer == "forms" and nodia:
        seq = doc.forms_nodia
    excl = mask_vector(doc, mask_spec)
    return [t for t, e in zip(seq, excl) if not e]


# ---------------------------------------------------------------------------------------------
# Construcción
# ---------------------------------------------------------------------------------------------
def _make_document(src: Source, part: dict, edition_key: str) -> Document | None:
    forms, forms_nodia, lemmas, pos, person, mood, refs = [], [], [], [], [], [], []
    for t in part["tokens"]:
        f = normalize_form(t["form"], keep_diacritics=True)
        if not f:
            continue  # filtro «solo tokens griegos»
        forms.append(f)
        forms_nodia.append(strip_diacritics(f))
        lemmas.append(normalize_form(t.get("lemma", ""), True) if t.get("lemma") else "")
        pos.append(t.get("pos", ""))
        person.append(t.get("person", ""))
        mood.append(t.get("mood", ""))
        refs.append(t.get("ref", ""))
    if not forms:
        return None
    pn = part.get("part", "")
    doc_id = f"{src.id}#{pn}" if pn else src.id
    status = src.part_status.get(str(pn), src.status) if pn else src.status
    author = src.part_author.get(str(pn), src.author) if pn else src.author
    if author == "Galo César":
        status = "other"
    return Document(id=doc_id, author=author, work=f"{src.work} {pn}".strip(), status=status,
                    tradition=src.tradition, edition_key=edition_key, forms=forms, forms_nodia=forms_nodia,
                    lemmas=lemmas, pos=pos, person=person, mood=mood, refs=refs, work_group=src.work_group or "",
                    genre=src.genre, subgenre=src.subgenre, addressee=src.addressee, source_id=src.id, part=str(pn))


def build_corpus(tier: int = 1, edition_key: str = "sblgnt", data_dir: str = DATA_DIR,
                 mask_path: str | None = None, reuse_path: str | None = None, verbose: bool = True,
                 only_ids: set[str] | None = None) -> list[Document]:
    mask_table = load_mask_table(mask_path)
    reuse_table = load_reuse_table(reuse_path)
    docs: list[Document] = []
    nt_ids = {s.id: s for s in NT}
    for src in by_tier(tier):
        if only_ids and src.id not in only_ids:
            continue
        path = raw_path(src, data_dir)
        if src.parser == "morphgnt" and edition_key != "sblgnt":
            continue  # el NT se toma de la edición alternativa (abajo)
        if not os.path.exists(path):
            if verbose:
                print(f"  [ausente] {src.id}: {path}")
            continue
        try:
            if src.parser == "tei":
                parts = parsers.parse_tei(path, split=src.split, min_tokens=src.min_tokens, max_docs=src.max_docs)
            else:
                parts = parsers.PARSERS[src.parser](path)
        except Exception as e:  # pragma: no cover
            print(f"  [error de análisis] {src.id}: {e}")
            continue
        made = []
        for p in parts:
            d = _make_document(src, p, edition_key if src.parser == "morphgnt" else src.edition_key)
            if d is not None and (not src.min_tokens or d.n_tokens >= src.min_tokens or src.split == "chapters"):
                made.append(d)
        if src.max_docs and len(made) > src.max_docs:
            made = made[: src.max_docs]
        docs.extend(made)
    if edition_key != "sblgnt":
        alt = EDITION_SOURCES[edition_key]
        path = raw_path(alt, data_dir)
        if os.path.exists(path):
            books = parsers.parse_proiel(path) if alt.parser == "proiel" else parsers.parse_macula(path)
            for bid, toks in books.items():
                src = nt_ids[bid]
                d = _make_document(src, {"part": "", "tokens": toks}, edition_key)
                if d:
                    docs.append(d)
        elif verbose:
            print(f"  [ausente] edición {edition_key}: {path}")
    for d in docs:
        apply_masks(d, mask_table, reuse_table)
    if verbose:
        print(f"build: {len(docs)} documentos, {sum(d.n_tokens for d in docs)} tokens (edición {edition_key})")
    return docs


def cache_path(edition_key: str, data_dir: str = DATA_DIR) -> str:
    return os.path.join(data_dir, "cache", f"corpus_{edition_key}.jsonl")


def save_corpus(docs: list[Document], edition_key: str, data_dir: str = DATA_DIR) -> str:
    p = cache_path(edition_key, data_dir)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(d.to_json() + "\n")
    return p


def load_corpus(edition_key: str = "sblgnt", data_dir: str = DATA_DIR) -> list[Document]:
    p = cache_path(edition_key, data_dir)
    with open(p, encoding="utf-8") as f:
        return [Document.from_json(line) for line in f if line.strip()]


def inventory_rows(docs: list[Document]) -> list[dict]:
    return [{"id": d.id, "author": d.author, "work": d.work, "status": d.status, "tradition": d.tradition,
             "genre": d.genre, "subgenre": d.subgenre, "addressee": d.addressee, "work_group": d.work_group,
             "edition": d.edition_key, "tokens": d.n_tokens, "types": len(set(d.forms)),
             "ttr": round(len(set(d.forms)) / max(1, d.n_tokens), 4),
             "masked_all": sum(mask_vector(d, "all")), "masked_reuse": sum(mask_vector(d, "reuse"))}
            for d in docs]

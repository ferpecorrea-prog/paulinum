#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
onomastica_extraer.py — candidatos a nombre propio (PROTOCOLO § 9.2; docs/canales/codigos_onomastica.md § 1).

Vuelve a leer las fuentes crudas (con mayúsculas) de los documentos pedidos con los mismos analizadores del paquete
sellado y saca, por documento, los tokens que empiezan por mayúscula griega. En el NT (MorphGNT) el nombre propio se
reconoce por el lema con mayúscula; en el resto, por la mayúscula del token, descontando las formas que también
aparecen en minúscula en cualquier fuente del corpus (mayúsculas de comienzo de frase); `dudoso` = 1-2 minúsculas en el corpus. La lista resultante es de CANDIDATOS:
la clasificación (persona / lugar / pueblo / divinidad / otro) se hace a mano en onomastica_inventario.csv.

Uso: python herramientas/onomastica_extraer.py --salida results/canales/onomastica_candidatos.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.sources import by_tier  # noqa: E402
from paulinum.fetch import raw_path  # noqa: E402
from paulinum import parsers  # noqa: E402
from paulinum.text import normalize_form, GREEK_LETTER_RE  # noqa: E402

LETTERS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb"]
BASILIO = [1, 3, 6, 14, 18, 20, 22, 23, 25, 28, 32, 34, 37, 51, 53, 55, 65, 68, 70, 73, 84, 89, 90, 91, 92, 93, 96, 105,
           114, 116, 124, 125, 135, 136, 138, 148, 150, 155, 160, 162, 165, 172, 191, 212, 213, 219, 222, 224, 235, 237,
           238, 243, 244, 245, 248, 250, 262, 271, 272, 294]
LIBANIO = [25, 37, 70, 81, 97, 101, 113, 114, 119, 150, 163, 173, 175, 192, 195, 208, 219, 224, 238, 245, 256, 267, 281,
           282, 298, 309, 315, 316, 319, 326, 330, 340, 359, 362, 369, 374, 375, 379, 405, 432, 438, 493, 495, 497, 503,
           516, 557, 560, 580, 620, 673, 731, 791, 793, 796, 802, 810, 811, 819, 833]
JUL_GENUINE_EP = [4, 8, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
                  67, 68, 69, 70, 71, 72, 73]  # se filtra después por lo que exista en el corpus


def coleccion(doc_id: str, author: str, status: str) -> str | None:
    sid, _, part = doc_id.partition("#")
    if doc_id in LETTERS:
        return "paulinas"
    if sid in ("IgnEf", "IgnMagn", "IgnTral", "IgnRom", "IgnFil", "IgnEsm", "IgnPol"):
        return "Ignacio"
    if sid == "IgnLong":
        return "Ps-Ignacio"
    if sid == "1Clem":
        return "1Clem"
    if author == "Ps-Clemente":
        return "Ps-Clemente"
    if sid in ("Jul_Ep", "Jul_EpAth", "Jul_EpThem") and author == "Juliano":
        return "Juliano"
    if author == "Ps-Juliano":
        return "Ps-Juliano"
    if sid == "Bas_Ep" and author == "Basilio de Cesarea" and part.isdigit() and int(part) in BASILIO:
        return "Basilio"
    if author == "Ps-Basilio":
        return "Ps-Basilio"
    if sid == "Liban_Ep10" and part.isdigit() and int(part) in LIBANIO:
        return "Libanio"
    if sid == "3Cor":
        return "3Cor"
    if author.startswith("Ps-") and author not in ("Ps-Plutarco", "Ps-Bernabé") and sid.startswith("Ps"):
        return "Hercher"
    return None


def is_upper_greek(tok: str) -> bool:
    for ch in tok:
        if GREEK_LETTER_RE.match(ch):
            return ch.isupper()
        if unicodedata.combining(ch):
            continue
        return False
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join("results", "canales", "onomastica_candidatos.csv"))
    a = ap.parse_args()
    from paulinum.corpus import load_corpus
    corpus = {d.id: d for d in load_corpus("sblgnt")}
    targets = {}
    for d in corpus.values():
        c = coleccion(d.id, d.author, d.status)
        if c:
            targets[d.id] = c
    print(f"documentos objetivo: {len(targets)}", Counter(targets.values()))
    rows = []
    lower_by_col: dict[str, Counter] = defaultdict(Counter)
    upper_by_col: dict[str, dict] = defaultdict(dict)
    src_needed = {i.partition("#")[0] for i in targets}
    lower_global: Counter = Counter()
    for src in by_tier(4):
        path = raw_path(src)
        if not os.path.exists(path):
            print("  [ausente]", src.id, path)
            continue
        if src.parser == "tei":
            parts = parsers.parse_tei(path, split=src.split, min_tokens=src.min_tokens, max_docs=src.max_docs,
                                      group_min_tokens=src.group_tokens)
        else:
            parts = parsers.PARSERS[src.parser](path)
        for p in parts:
            pn = p.get("part", "")
            doc_id = f"{src.id}#{pn}" if pn else src.id
            if src.parser != "morphgnt":
                for t in p["tokens"]:
                    if not is_upper_greek(t["form"]):
                        nf0 = normalize_form(t["form"])
                        if nf0:
                            lower_global[nf0] += 1
            if doc_id not in targets:
                continue
            col = targets[doc_id]
            d = corpus[doc_id]
            for t in p["tokens"]:
                form = t["form"]
                if src.parser == "morphgnt":
                    lem = t.get("lemma", "")
                    if lem and is_upper_greek(lem) and t.get("pos", "").startswith("N"):
                        key = (doc_id, lem)
                        e = upper_by_col[col].setdefault(key, {"n": 0, "refs": [], "forms": set()})
                        e["n"] += 1; e["refs"].append(t.get("ref", "")); e["forms"].add(form)
                else:
                    nf = normalize_form(form)
                    if not nf:
                        continue
                    if is_upper_greek(form):
                        key = (doc_id, nf)
                        e = upper_by_col[col].setdefault(key, {"n": 0, "refs": [], "forms": set()})
                        e["n"] += 1; e["refs"].append(t.get("ref", "")); e["forms"].add(form)
                    else:
                        lower_by_col[col][nf] += 1
    for col, d in upper_by_col.items():
        for (doc_id, key), e in d.items():
            low = lower_by_col[col].get(key, 0)
            lowg = lower_global.get(key, 0)
            rows.append({"coleccion": col, "documento": doc_id, "estado": corpus[doc_id].status, "autor": corpus[doc_id].author,
                         "clave": key, "formas": "|".join(sorted(e["forms"])), "n_menciones": e["n"],
                         "n_minusculas_en_coleccion": low, "n_minusculas_en_corpus": lowg,
                         "refs": "|".join(dict.fromkeys(e["refs"]))[:200],
                         "candidato": "sí" if (col == "paulinas" or lowg == 0) else ("dudoso" if lowg <= 2 else "no")})
    rows.sort(key=lambda r: (r["coleccion"], r["documento"], r["clave"]))
    os.makedirs(os.path.dirname(a.salida), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\r\n")
        w.writeheader(); w.writerows(rows)
    print(f"{a.salida}: {len(rows)} filas;", Counter((r['coleccion'], r['candidato']) for r in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

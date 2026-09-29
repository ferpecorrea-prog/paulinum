#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
institucional_extraer.py — apariciones del léxico cerrado de organización y culto (PROTOCOLO § 9.3;
docs/canales/codigos_institucional.md § 1) en las catorce cartas y en el corpus de comparación (Hechos, 1 Clemente,
Didajé, Ignacio, Policarpo, Hermas), con contexto, para su codificación manual en institucional_datos.py.

Salida: results/canales/institucional_apariciones.csv (documento, termino, ref, forma, contexto).
"""
from __future__ import annotations

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb",
        "Hch", "1Clem", "Did", "IgnEf", "IgnMagn", "IgnTral", "IgnRom", "IgnFil", "IgnEsm", "IgnPol", "PolFil", "Herm"]
# término → prefijos de forma normalizada (minúsculas, σ final unificada, acentos incluidos)
LEX = {
    "ἐπίσκοπος": ["ἐπίσκοπ", "ἐπισκόπ", "ἐπισκοπ"],
    "πρεσβύτερος": ["πρεσβύτερ", "πρεσβυτέρ", "πρεσβυτερ"],
    "διάκονος": ["διάκον", "διακόν", "διακον"],
    "προϊστάμενος": ["προϊστ", "προΐστ", "προεστ", "προστ"],
    "ἡγούμενος": ["ἡγούμεν", "ἡγουμέν"],
    "χήρα": ["χήρ", "χῆρ", "χηρ"],
    "νεώτερος": ["νεώτερ", "νεωτέρ"],
    "ἐκκλησία": ["ἐκκλησί"],
    "οἶκος": ["οἶκ", "οἴκ", "οἰκ"],
    "χειροτονία": ["χειροτον"],
    "ἐπίθεσις χειρῶν": ["ἐπίθεσ"],
}
OIKOS_OK = {"οἶκοσ", "οἴκου", "οἴκῳ", "οἶκον", "οἶκοι", "οἴκων", "οἴκοισ", "οἴκουσ"}  # solo el sustantivo οἶκος
CHEIR = re.compile(r"^(χεῖρ|χειρ|χεῖρα|χερ)")
EPITITH = re.compile(r"^(ἐπιτίθ|ἐπετίθ|ἐπέθ|ἐπιθ|ἐπίθ|ἐπιτεθ)")


def main() -> int:
    corpus = {d.id: d for d in load_corpus("sblgnt")}
    rows = []
    for doc_id in DOCS:
        d = corpus[doc_id]
        forms = d.forms
        for i, f in enumerate(forms):
            hits = []
            for term, prefs in LEX.items():
                if term == "οἶκος":
                    if f in OIKOS_OK:
                        hits.append(term)
                elif any(f.startswith(p) for p in prefs):
                    hits.append(term)
            # imposición de manos: verbo ἐπιτίθημι + χείρ a ≤ 4 tokens
            if EPITITH.match(f) and any(CHEIR.match(forms[j]) for j in range(max(0, i - 4), min(len(forms), i + 5)) if j != i):
                hits.append("ἐπίθεσις χειρῶν")
            for term in dict.fromkeys(hits):
                ctx = " ".join(forms[max(0, i - 9):i] + ["[" + f + "]"] + forms[i + 1:i + 10])
                rows.append({"documento": doc_id, "termino": term, "ref": d.refs[i] if d.refs else "", "forma": f,
                             "lema": d.lemmas[i] if d.lemmas and i < len(d.lemmas) else "", "contexto": ctx})
    out = os.path.join(ROOT, "results", "canales", "institucional_apariciones.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\r\n"); w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(out, len(rows)); print(Counter(r["termino"] for r in rows)); print(Counter(r["documento"] for r in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

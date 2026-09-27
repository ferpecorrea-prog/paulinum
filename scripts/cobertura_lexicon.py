#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cobertura_lexicon.py — cobertura del diccionario uniforme de lemas por documento y por tradición
(lectura posterior al sellado; solo lee el corpus y el lexicón).

Salida: results/<run>/cobertura_lexicon.csv (por documento) y resumen por tradición en pantalla
(documentos, mediana, mín, máx), como en el Apéndice A.2.
Uso: python scripts/cobertura_lexicon.py --run campana_03
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.features import load_lexicon  # noqa: E402
from paulinum.pipeline import _write_csv  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--edicion", default="sblgnt")
    a = ap.parse_args()
    lex = load_lexicon()
    if not lex:
        print("no hay data/cache/lexicon_uniforme.tsv: ejecute scripts/construir_lexicon.py")
        return 1
    rows = []
    for d in load_corpus(a.edicion):
        n = d.n_tokens
        cov = sum(1 for f in d.forms_nodia if f in lex) / max(n, 1)
        rows.append({"id": d.id, "author": d.author, "tradition": d.tradition, "status": d.status, "tokens": n, "cobertura": round(cov, 4)})
    run_dir = os.path.join("results", a.run)
    os.makedirs(run_dir, exist_ok=True)
    _write_csv(os.path.join(run_dir, "cobertura_lexicon.csv"), rows)
    print("tradición            documentos  mediana  mín    máx")
    for t in sorted({r["tradition"] for r in rows}):
        v = np.array([r["cobertura"] for r in rows if r["tradition"] == t])
        print(f"{t:20s} {len(v):10d}  {np.median(v):.3f}  {v.min():.3f}  {v.max():.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

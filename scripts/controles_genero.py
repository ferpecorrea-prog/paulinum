#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controles_genero.py — controles de género (lectura posterior al sellado; solo lee resultados).

Para cada clase de subgénero (apologia, circular, consolatoria, exhortacion, mandato, parenetica,
testamentaria, otra) toma (a) los problemas positivos intra-autor cuya diana pertenece a esa clase y
(b) los negativos frente a Pablo de esa clase, y calcula la puntuación media (mediana entre especificaciones),
la de las demás clases y la fracción por debajo / por encima de 0,5, como en controles_genero_resumen.csv.
Uso: python scripts/controles_genero.py --run campana_03
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.pipeline import _write_csv  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--edicion", default="sblgnt")
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    docs = {d.id: d for d in load_corpus(a.edicion)}
    rows = list(csv.DictReader(open(os.path.join(run_dir, "gi_results_all_specs.csv"), encoding="utf-8")))
    # mediana por problema entre especificaciones
    per = defaultdict(list)
    for r in rows:
        if r["score"] and r["kind"] in ("pos_pairs", "neg_target"):
            per[(r["kind"], r["target"])].append(float(r["score"]))
    med = {k: float(np.median(v)) for k, v in per.items()}
    classes = sorted({docs[t].subgenre for (_, t) in med if t in docs} | {"otra"})
    out, detail = [], []
    for cl in classes:
        pos = [m for (k, t), m in med.items() if k == "pos_pairs" and docs[t].subgenre == cl]
        pos_o = [m for (k, t), m in med.items() if k == "pos_pairs" and docs[t].subgenre != cl]
        neg = [m for (k, t), m in med.items() if k == "neg_target" and docs[t].subgenre == cl]
        neg_o = [m for (k, t), m in med.items() if k == "neg_target" and docs[t].subgenre != cl]
        neg_letters_o = [m for (k, t), m in med.items() if k == "neg_target" and docs[t].genre == "carta" and docs[t].subgenre != cl]
        out.append({"clase": cl, "n_pos": len(pos), "pos_media": np.mean(pos) if pos else "", "pos_otros": np.mean(pos_o) if pos_o else "",
                    "pos_frac_menor_05": np.mean([p < 0.5 for p in pos]) if pos else "", "n_neg": len(neg),
                    "neg_media": np.mean(neg) if neg else "", "neg_otros": np.mean(neg_o) if neg_o else "",
                    "neg_cartas_otras": np.mean(neg_letters_o) if neg_letters_o else "",
                    "neg_frac_mayor_05": np.mean([n >= 0.5 for n in neg]) if neg else ""})
        for (k, t), m in med.items():
            if docs[t].subgenre == cl:
                detail.append({"clase": cl, "kind": k, "id": t, "author": docs[t].author, "mediana_gi": m})
    _write_csv(os.path.join(run_dir, "controles_genero_resumen.csv"), out)
    _write_csv(os.path.join(run_dir, "controles_genero_detalle.csv"), detail)
    for r in out:
        print(f"  {r['clase']:14s} pos n={r['n_pos']:3d} media={r['pos_media'] if r['pos_media']=='' else round(r['pos_media'],3)}  "
              f"neg n={r['n_neg']:3d} media={r['neg_media'] if r['neg_media']=='' else round(r['neg_media'],3)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

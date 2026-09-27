#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lectura_modelo_svm.py — lectura del segundo modelo junto al GI (posterior al sellado; solo lee resultados).

Cruza modelo_svm_percentiles.csv con summary_by_letter.csv y gi_targets_por_especificacion.csv para
informar, carta a carta, la concordancia o discordancia entre el segundo modelo y el método de los
impostores (regla preregistrada: se informa la concordancia, no se elige el modelo mejor).
Salida: results/<run>/lectura_modelo_svm.md
Uso: python scripts/lectura_modelo_svm.py --run campana_03
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.pipeline import LETTERS_13  # noqa: E402


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) and os.path.getsize(p) else []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    pct = rd(os.path.join(run_dir, "modelo_svm_percentiles.csv"))
    summ = {r["id"]: r for r in rd(os.path.join(run_dir, "summary_by_letter.csv"))}
    lines = [f"# Lectura del segundo modelo · {a.run}", "",
             "| carta | GI mediana | P(Pablo) por familia (logística) | pct negativos (mediana) | pct núcleo (mediana) | concordancia |",
             "|---|---|---|---|---|---|"]
    for L in LETTERS_13:
        rs = [r for r in pct if r["id"] == L]
        if not rs:
            continue
        gi = float(summ[L]["score_median"]) if L in summ else float("nan")
        fam = "; ".join(f"{r['features']} {float(r['p_media']):.2f}" for r in rs if r["model"] == "logistic")
        pn = np.median([float(r["pct_neg"]) for r in rs if r["pct_neg"]])
        pc = np.median([float(r["pct_nucleo"]) for r in rs if r["pct_nucleo"]])
        pmed = np.median([float(r["p_media"]) for r in rs if r["p_media"]])
        conc = "concuerda" if (gi >= 0.5) == (pmed >= 0.5) else "discuerda"
        lines.append(f"| {L} | {gi:.3f} | {fam} | {pn:.3f} | {pc:.3f} | {conc} |")
    out = os.path.join(run_dir, "lectura_modelo_svm.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())

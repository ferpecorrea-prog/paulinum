#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2 — réplica de la capa de trece lemas sobre MorphGNT/SBLGNT 6.12 (y, si se ha construido el corpus
de Tischendorf, sobre PROIEL) — Investigación 1, § 4.5 «Primero».

Valores publicados para el cotejo (MorphGNT): cada indiscutida dejada fuera y medida contra las otras
seis: 2 Cor 0,55; 0,88; 1,22; 1,24; 1,38; Rom 1,67; Flm 2,06. Colosenses 2,32 (2,34 en Diorisis);
correlación de rangos con Perseus 0,99; 2 Tim y 2 Tes por debajo de todo control no paulino;
2 Pe el control más próximo.

Uso (desde la raíz de paulinum_lab, con el corpus construido): python investigacion_1/segunda_campana/p2_replica_morphgnt.py
"""
from __future__ import annotations

import os
import sys

import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylolib import ROOT, LEMAS_13, NUCLEO_6, NUCLEO_7, matriz_13_lemas, distancia_13, loo_13, load_corpus  # noqa: E402

TEXTOS = ["Rom", "1Cor", "2Cor", "Gal", "Ef", "Flp", "Col", "1Tes", "2Tes", "1Tim", "2Tim", "Tit", "Flm", "Heb",
          "Sant", "1Pe", "2Pe", "1Jn", "Jud"]
PERSEUS = os.path.join(ROOT, "investigacion_1", "capa_13_lemas", "data", "matriz_19x13.csv")


def main() -> int:
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    for edition in ("sblgnt", "tischendorf"):
        try:
            docs = [d for d in load_corpus(edition, os.path.join(ROOT, "data")) if d.id in TEXTOS]
        except FileNotFoundError:
            print(f"[{edition}] corpus no construido (python -m paulinum build --config config/campana_02b_ediciones.yaml)")
            continue
        m = matriz_13_lemas(docs).loc[TEXTOS]
        m.to_csv(os.path.join(out_dir, f"p2_matriz_19x13_{edition}.csv"))
        d6 = distancia_13(m, NUCLEO_6)
        loo = loo_13(m, NUCLEO_7)
        loo_nuc = pd.Series({c: float(loo.loc[c, c]) for c in NUCLEO_7}).sort_values()
        print(f"\n== {edition}: distancia de 13 lemas (núcleo 6), ordenada ==")
        print(d6.sort_values().round(3).to_string())
        print(f"\n== {edition}: cada indiscutida dejada fuera frente a las otras seis ==")
        print(loo_nuc.round(3).to_string())
        pd.DataFrame({"D_13_nucleo6": d6}).join(pd.DataFrame({"loo_nucleo7": loo_nuc})).to_csv(
            os.path.join(out_dir, f"p2_distancias_{edition}.csv"), float_format="%.4f")
        if os.path.exists(PERSEUS):
            per = pd.read_csv(PERSEUS, index_col="id")
            dP = distancia_13(per, NUCLEO_6).loc[TEXTOS]
            rho = spearmanr(dP.values, d6.loc[TEXTOS].values).correlation
            print(f"\ncorrelación de rangos con Perseus: {rho:.3f} (publicado: 0,99)")
            print("Col:", round(float(d6["Col"]), 3), "(publicado MorphGNT 2,32) · Flm:", round(float(d6["Flm"]), 3), "(publicado 2,06)")
            print("2Tim y 2Tes por debajo de todo control no paulino:",
                  bool(max(d6["2Tim"], d6["2Tes"]) < min(d6[["Sant", "1Pe", "2Pe", "1Jn", "Jud"]])),
                  "· control más próximo:", d6[["Sant", "1Pe", "2Pe", "1Jn", "Jud"]].idxmin())
    return 0


if __name__ == "__main__":
    sys.exit(main())

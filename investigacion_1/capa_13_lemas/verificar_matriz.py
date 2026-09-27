#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar_matriz.py — exige identidad exacta entre una matriz reconstruida y la depositada
(Investigación 1, nota 44) e imprime la huella SHA-256 de la matriz depositada.

La huella publicada de la matriz primaria original era 729a77b5…abbc78e9 (el libro la imprime
truncada); la de data/matriz_19x13.csv (misma matriz, formato CSV de esta reconstrucción) es la que
imprime este guion.

Uso: python verificar_matriz.py [--otra data/matriz_19x13_reconstruida.csv]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
DEP = os.path.join(AQUI, "data", "matriz_19x13.csv")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--otra", default=None)
    a = ap.parse_args()
    h = hashlib.sha256(open(DEP, "rb").read()).hexdigest()
    print(f"SHA-256 de {os.path.relpath(DEP)}: {h}")
    dep = pd.read_csv(DEP, index_col="id")
    print(f"{dep.shape[0]} escritos × {dep.shape[1] - 4} lemas; suma de recuentos = {int(dep.iloc[:, 4:].values.sum())}")
    if a.otra:
        otra = pd.read_csv(a.otra, index_col="id")
        cols = [c for c in dep.columns if c in otra.columns]
        same = dep[cols].astype(int).equals(otra.loc[dep.index, cols].astype(int))
        print("identidad exacta:", same)
        if not same:
            diff = (dep[cols].astype(int) != otra.loc[dep.index, cols].astype(int))
            print(diff[diff.any(axis=1)].to_string())
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

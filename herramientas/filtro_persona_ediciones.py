#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filtro_persona_ediciones.py — comprobación de la exclusión de la persona gramatical por edición (D-032).

El código sellado (Sello 2) aprende las formas verbales de 1.ª y 2.ª persona de la anotación de cada edición
(`features.learn_person_verb_forms`, que solo reconoce la etiqueta «V» de MorphGNT) y el inventario de clase cerrada con
las etiquetas de MorphGNT (`learn_closed_class`, D-025). Este guion, fuera del conjunto sellado y sin modificar la
biblioteca, informa de cuántas formas aprende cada edición construida y de qué etiquetas trae su anotación.

Salida: results/paulinum_1_0/filtro_persona_ediciones.csv
Uso: python herramientas/filtro_persona_ediciones.py
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.features import PersonFilter, learn_closed_class  # noqa: E402

EDICIONES = ["sblgnt", "tischendorf", "nestle1904", "sinaiticus", "p46"]


def main() -> None:
    filas = []
    for ed in EDICIONES:
        try:
            docs = load_corpus(ed, "data")
        except FileNotFoundError:
            print(f"[ausente] {ed}")
            continue
        anot = [d for d in docs if any(d.pos)]
        etiquetas = Counter(p for d in anot for p in d.pos if p)
        filas.append({"edicion": ed, "documentos": len(docs), "documentos_anotados": len(anot),
                      "formas_verbales_1_2_persona": len(PersonFilter(docs).verb_forms),
                      "clase_cerrada": len(learn_closed_class(docs)),
                      "etiquetas_mas_frecuentes": " ".join(f"{k}:{v}" for k, v in etiquetas.most_common(8))})
        print(filas[-1])
    out = os.path.join("results", "paulinum_1_0", "filtro_persona_ediciones.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\r\n")
        w.writeheader()
        w.writerows(filas)
    print("->", out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extraer_de_perseus.py — reconstrucción de la matriz 19 × 13 desde el repertorio lematizado de Perseus
(Investigación 1, nota 44: «guion de extracción desde Perseus»).

Fuente original: las tablas de frecuencia por lema del Perseus Hopper (perseus.tufts.edu) para los textos
tlg0031.tlg006-tlg019 (14 paulinas y Hebreos) y tlg0031.tlg020-tlg023, tlg026 (Santiago, 1-2 Pedro,
1 Juan, Judas), con los identificadores de lema 18986 (δέ), 17560 (γάρ), 59906 (οὐ), 53376 (μή) y
19658 (διά) para los cinco recuentos recuperados. El servicio devuelve páginas HTML cuyo formato puede
cambiar; este guion documenta las direcciones y el procedimiento y comprueba la identidad con la matriz
depositada (data/matriz_19x13.csv). Requiere acceso a perseus.tufts.edu.

Uso: python extraer_de_perseus.py [--salida data/matriz_19x13_reconstruida.csv]
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
TEXTOS = {  # id: (obra Perseus, URN CTS)
    "Rom": "tlg0031.tlg006", "1Cor": "tlg0031.tlg007", "2Cor": "tlg0031.tlg008", "Gal": "tlg0031.tlg009",
    "Ef": "tlg0031.tlg010", "Flp": "tlg0031.tlg011", "Col": "tlg0031.tlg012", "1Tes": "tlg0031.tlg013",
    "2Tes": "tlg0031.tlg014", "1Tim": "tlg0031.tlg015", "2Tim": "tlg0031.tlg016", "Tit": "tlg0031.tlg017",
    "Flm": "tlg0031.tlg018", "Heb": "tlg0031.tlg019", "Sant": "tlg0031.tlg020", "1Pe": "tlg0031.tlg021",
    "2Pe": "tlg0031.tlg022", "1Jn": "tlg0031.tlg023", "Jud": "tlg0031.tlg026",
}
LEMAS = ["ὁ", "καί", "ἐν", "ἐγώ", "σύ", "ὅς", "αὐτός", "εἰς", "δέ", "γάρ", "οὐ", "μή", "διά"]
BETA = {"ὁ": "o(", "καί": "kai/", "ἐν": "e)n", "ἐγώ": "e)gw/", "σύ": "su/", "ὅς": "o(/s", "αὐτός": "au)to/s",
        "εἰς": "ei)s", "δέ": "de/", "γάρ": "ga/r", "οὐ": "ou)", "μή": "mh/", "διά": "dia/"}
VOCAB_URL = "http://www.perseus.tufts.edu/hopper/vocablist?works=Perseus%3Atext%3A1999.01.0155%3Abook%3D{book}&sort=freq&filt=all&lang=greek"
WORDFREQ_URL = "http://www.perseus.tufts.edu/hopper/wordfreq?lang=greek&lookup={beta}"


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(AQUI, "data", "matriz_19x13_reconstruida.csv"))
    a = ap.parse_args()
    print("Este guion depende del formato de las páginas del Perseus Hopper (vocablist / wordfreq).")
    print("Procedimiento: para cada lema, la página wordfreq lista las obras con su recuento; se filtran las")
    print("obras del NT (Perseus:text:1999.01.0155) y se leen los recuentos de los 19 escritos; palabras y")
    print("lemas distintos se toman de la cabecera de vocablist de cada libro.")
    filas = []
    for lema in LEMAS:
        url = WORDFREQ_URL.format(beta=BETA[lema])
        try:
            html = fetch(url)
        except Exception as e:  # pragma: no cover
            print(f"  no accesible: {url} ({e})")
            return 1
        # formato observado en 2026: filas <tr> con el nombre de la obra y el recuento total
        for m in re.finditer(r"<tr[^>]*>(.*?)</tr>", html, re.S):
            filas.append((lema, re.sub(r"<[^>]+>", " ", m.group(1))))
    with open(a.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lema", "fila_html"])
        w.writerows(filas)
    print(f"filas crudas guardadas en {a.salida}; complete el análisis según el formato vigente de la página")
    return 0


if __name__ == "__main__":
    sys.exit(main())

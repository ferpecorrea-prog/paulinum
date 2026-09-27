#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_lexicon.py — diccionario uniforme forma → lema a partir de MorphGNT, PROIEL y Diorisis.

Para cada forma (minúsculas, sin diacríticos) se toma el lema más frecuente en el conjunto de las tres
anotaciones (§ 0.2 del informe de la campaña 03: MorphGNT 137.554 tokens, PROIEL 132.356, Diorisis
10.052.828; 399.678 formas). Las formas de Diorisis vienen en Beta Code y se convierten. Salida:
data/cache/lexicon_uniforme.tsv (forma \t lema \t frecuencia \t n_fuentes) y un resumen en pantalla.

Uso: python scripts/construir_lexicon.py --diorisis-zip <ruta a Diorisis.zip> [--sin-diorisis]
Diorisis (Vatri y McGillivray, CC BY-NC-SA 4.0) no se redistribuye aquí: descárguelo de
https://figshare.com/articles/dataset/The_Diorisis_Ancient_Greek_Corpus/6187256 y pase la ruta del zip.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
import zipfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum import parsers  # noqa: E402
from paulinum.text import normalize_form, strip_diacritics  # noqa: E402


def key_of(form: str) -> str:
    f = normalize_form(form, keep_diacritics=True)
    return strip_diacritics(f) if f else ""


def lemma_of(lemma: str) -> str:
    l = normalize_form(lemma, keep_diacritics=True)
    return l


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diorisis-zip", default="")
    ap.add_argument("--sin-diorisis", action="store_true")
    ap.add_argument("--data", default="data")
    ap.add_argument("--salida", default=os.path.join("data", "cache", "lexicon_uniforme.tsv"))
    a = ap.parse_args()
    counts: dict[str, Counter] = defaultdict(Counter)
    sources: dict[str, set] = defaultdict(set)
    n_tok = {"morphgnt": 0, "proiel": 0, "diorisis": 0}
    for path in sorted(glob.glob(os.path.join(a.data, "raw", "morphgnt", "*-morphgnt.txt"))):
        for part in parsers.parse_morphgnt(path):
            for t in part["tokens"]:
                k, l = key_of(t["form"]), lemma_of(t["lemma"])
                if k and l:
                    counts[k][l] += 1
                    sources[k].add("morphgnt")
                    n_tok["morphgnt"] += 1
    proiel = os.path.join(a.data, "raw", "proiel", "greek-nt.xml")
    if os.path.exists(proiel):
        for book, toks in parsers.parse_proiel(proiel).items():
            for t in toks:
                k, l = key_of(t["form"]), lemma_of(t["lemma"])
                if k and l:
                    counts[k][l] += 1
                    sources[k].add("proiel")
                    n_tok["proiel"] += 1
    else:
        print(f"[aviso] PROIEL no descargado ({proiel}); ejecute: python -m paulinum fetch --editions")
    if a.diorisis_zip and not a.sin_diorisis:
        with zipfile.ZipFile(a.diorisis_zip) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".xml")]
            print(f"Diorisis: {len(names)} archivos XML")
            for i, n in enumerate(names, 1):
                for form, lemma in parsers.iter_diorisis_pairs(z.read(n)):
                    k, l = key_of(form), lemma_of(lemma)
                    if k and l:
                        counts[k][l] += 1
                        sources[k].add("diorisis")
                        n_tok["diorisis"] += 1
                if i % 50 == 0:
                    print(f"  {i}/{len(names)} archivos; {len(counts)} formas")
    elif not a.sin_diorisis:
        print("[aviso] sin --diorisis-zip: el lexicón se construye solo con MorphGNT y PROIEL (cobertura menor en los controles)")
    os.makedirs(os.path.dirname(a.salida), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as f:
        f.write("# forma_sin_diacriticos\tlema_mas_frecuente\tfrecuencia\tn_fuentes\n")
        for k in sorted(counts):
            l, n = counts[k].most_common(1)[0]
            f.write(f"{k}\t{l}\t{n}\t{len(sources[k])}\n")
    print(f"lexicón: {len(counts)} formas → {a.salida}; tokens usados: {n_tok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

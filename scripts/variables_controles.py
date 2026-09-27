#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
variables_controles.py — anotación de las variables de situación de los controles y PERMANOVA por autor.

(1) Anota los documentos de autoría segura (y las 13 paulinas como referencia) con destinatario
    (individuo / comunidad / publico / si_mismo), género, polémica (0/1/2) y clase de longitud
    (corta < 1.500; media 1.500-5.000; larga > 5.000 palabras), a partir del manifiesto (sources.py) y
    de metadata/letter_variables.csv, y escribe metadata/control_variables.csv (corregible a mano; si el
    archivo ya existe se leen de él las anotaciones y no se sobrescribe salvo --reescribir).
(2) Dentro de cada autor con ≥ 8 ventanas de 400 palabras, calcula la PERMANOVA de cada variable con
    ≥ 2 niveles sobre la matriz Delta (mfw:200), más un R² submuestreado a 76 ventanas (el n de Pablo),
    promedio de 20 submuestras. Salida: results/<run>/permanova_controles.csv.

Uso: python scripts/variables_controles.py --run campana_03 [--reescribir] [--permutaciones 299]
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter, learn_closed_class  # noqa: E402
from paulinum.pipeline import _write_csv, LETTERS_13, load_letter_variables  # noqa: E402
from paulinum.variables import DistanceMatrixBuilder, fixed_windows, permanova  # noqa: E402
from paulinum.verify import Spec  # noqa: E402

POLEMIC_SUBGENRES = {"polemica": 2, "apologia": 2, "satira": 2, "deliberativo": 1, "exhortacion": 1, "mandato": 1}


def length_class(n: int) -> str:
    return "corta" if n < 1500 else ("media" if n <= 5000 else "larga")


def annotate(docs, letter_vars) -> list[dict]:
    rows = []
    for d in docs:
        if d.author in ("Pablo", "Pablo?") and d.id in LETTERS_13:
            lv = letter_vars.get(d.id, {})
            rows.append({"id": d.id, "author": "Pablo (13 cartas)", "work": d.work, "status": d.status,
                         "addressee_type": lv.get("addressee_type", d.addressee), "genre": "carta",
                         "polemic": lv.get("polemic_level", "0"), "length_class": length_class(d.n_tokens),
                         "work_group": d.work_group or d.id, "tokens": d.n_tokens})
        elif d.status == "genuine":
            rows.append({"id": d.id, "author": d.author, "work": d.work, "status": d.status,
                         "addressee_type": d.addressee, "genre": d.genre,
                         "polemic": POLEMIC_SUBGENRES.get(d.subgenre, 0), "length_class": length_class(d.n_tokens),
                         "work_group": d.work_group or d.id, "tokens": d.n_tokens})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--edicion", default="sblgnt")
    ap.add_argument("--reescribir", action="store_true")
    ap.add_argument("--permutaciones", type=int, default=299)
    ap.add_argument("--ventana", type=int, default=400)
    ap.add_argument("--min-ventanas", type=int, default=8)
    a = ap.parse_args()
    docs = load_corpus(a.edicion)
    meta = os.path.join("metadata", "control_variables.csv")
    if os.path.exists(meta) and not a.reescribir:
        rows = list(csv.DictReader(open(meta, encoding="utf-8")))
        print(f"anotaciones leídas de {meta} ({len(rows)} documentos)")
    else:
        rows = annotate(docs, load_letter_variables())
        _write_csv(meta, rows)
        print(f"anotaciones escritas en {meta} ({len(rows)} documentos)")
    ann = {r["id"]: r for r in rows}
    pf, closed = PersonFilter(docs), learn_closed_class(docs)
    fs = FeatureSpace("mfw:200", docs, person_filter=pf, closed_set=closed)
    b = DistanceMatrixBuilder(docs, fs, "delta", window=None, draws=1)
    by_id = {d.id: d for d in docs}
    by_author: dict[str, list[str]] = {}
    for r in rows:
        by_author.setdefault(r["author"], []).append(r["id"])
    out = []
    rng = np.random.default_rng(76)
    for author, ids in sorted(by_author.items()):
        wins = []
        for i in ids:
            wins.extend(fixed_windows(by_id[i], fs, window=a.ventana))
        if len(wins) < a.min_ventanas:
            continue
        D = b.window_matrix(wins)
        variables = {"addressee_type": [ann[d]["addressee_type"] for d, _, _ in wins],
                     "genre": [ann[d]["genre"] for d, _, _ in wins],
                     "polemic": [str(ann[d]["polemic"]) for d, _, _ in wins],
                     "length_class": [ann[d]["length_class"] for d, _, _ in wins],
                     "work": [ann[d]["work_group"] for d, _, _ in wins]}
        for var, g in variables.items():
            if len(set(g)) < 2:
                continue
            r = permanova(D, g, permutations=a.permutaciones)
            r2s = []
            if len(wins) > 76:
                for _ in range(20):
                    idx = np.sort(rng.choice(len(wins), size=76, replace=False))
                    gg = [g[i] for i in idx]
                    if len(set(gg)) < 2:
                        continue
                    r2s.append(permanova(D[np.ix_(idx, idx)], gg, permutations=0)["R2"])
            out.append({"author": author, "variable": var, "n_windows": len(wins), "k": r["k"], "R2": r["R2"],
                        "R2_sub76": float(np.mean(r2s)) if r2s else r["R2"], "pseudo_F": r["pseudo_F"], "p": r["p"]})
            print(f"  {author:26s} {var:15s} n={len(wins):4d} k={r['k']:2d} R2={r['R2']:.3f} sub76={out[-1]['R2_sub76']:.3f} p={r['p']:.3f}")
    run_dir = os.path.join("results", a.run)
    os.makedirs(run_dir, exist_ok=True)
    _write_csv(os.path.join(run_dir, "permanova_controles.csv"), out)
    print(f"→ {run_dir}/permanova_controles.csv ({len(out)} filas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P6 y P7 — métodos de la disciplina (Delta coseno sobre 200 formas frecuentes y verificación por
impostores) y controles de falsificación (3 Corintios; recensión larga de Ignacio) — Investigación 1,
§ 4.5 «Segundo» y «Tercero».

Diseño reconstruido a partir del libro:
  * verificación por impostores: 50 % de los rasgos en cada iteración; dos bancos de impostores:
    (a) banco amplio preregistrado: todos los documentos de control de longitud suficiente (NT, Padres
        Apostólicos, 3 Cor), 100 iteraciones; (b) banco epistolar añadido tras el resultado: las cinco
        epístolas católicas, los Padres Apostólicos y 3 Cor, 200 iteraciones. Se imprimen los dos.
  * núcleo paulino = siete indiscutidas; cada carta del núcleo se evalúa dejándola fuera; dianas: las seis
    discutidas, Hebreos, Filemón (control), 3 Cor (falsificación cierta), Santiago, 1-2 Pedro, 1 Juan, Judas.
  * Ignacio: siete cartas auténticas frente a las seis espurias (y las siete interpoladas) de la recensión
    larga, con banco propio (los 19 escritos neotestamentarios y de control, 1 Clem, Policarpo, Didajé,
    Bernabé y 3 Cor).
Valores publicados para el cotejo: 2 Tes 0,955/0,99; 1 Pe 0,960/0,98; Col 0,790/0,89; Sant 0,765/0,78;
Ef 0,690/0,61; Heb 0,625/0,58; 3 Cor 0,595/0,29; Flm 0,540/0,79; 2 Tim 0,400/0,39; 1 Jn 0,045/0,11;
2 Pe 0,035/0,08; Tit 0,025/0,17; 1 Tim 0,025/0,14; Jud 0,015/0,23 (banco epistolar / banco amplio).
Ignacio: auténticas 0,59-1,00; espurias 0,005-0,205 (una 0,515); interpoladas 1,000.

Uso: python investigacion_1/segunda_campana/p6_p7_impostores_falsificacion.py [--iters-amplio 100] [--iters-epistolar 200]
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylolib import ROOT, asegurar_fuente  # noqa: E402
from paulinum.corpus import load_corpus, build_corpus  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter, learn_closed_class  # noqa: E402
from paulinum.verify import GIEngine, Spec, Problem  # noqa: E402

NUCLEO = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm"]
DIANAS = ["2Tes", "1Pe", "Col", "Sant", "Ef", "Heb", "3Cor", "Flm", "2Tim", "1Jn", "2Pe", "Tit", "1Tim", "Jud"]
CATOLICAS = ["Sant", "1Pe", "2Pe", "1Jn", "Jud"]
AF = ["1Clem", "2Clem", "IgnEf", "IgnMagn", "IgnTral", "IgnRom", "IgnFil", "IgnEsm", "IgnPol", "PolFil", "Did", "Bern",
      "Herm", "MartPol", "Diogn"]


def score(engine, target, cands, bank, rng, iters):
    engine.spec.iters = iters
    pr = Problem(f"p6:{target}", "p6", target, cands, exclude=[d for d in engine.by_id if d not in bank], label=None)
    # el banco se impone excluyendo todo lo que no esté en él
    pool = [b for b in bank if b != target and b not in cands and b in engine.by_id]
    engine_pool = engine.impostor_pool

    def forced_pool(problem):
        return [p for p in pool if engine.length[p] >= engine.min_tokens]
    engine.impostor_pool = forced_pool
    try:
        return engine.score(pr, rng)["score"]
    finally:
        engine.impostor_pool = engine_pool


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters-amplio", type=int, default=100)
    ap.add_argument("--iters-epistolar", type=int, default=200)
    ap.add_argument("--semilla", type=int, default=20260903)
    a = ap.parse_args()
    data = os.path.join(ROOT, "data")
    docs = load_corpus("sblgnt", data)
    ids = {d.id for d in docs}
    # recensión larga de Ignacio (First1KGreek), si está descargada
    asegurar_fuente("IgnLong")  # recensión larga de Ignacio (First1KGreek), si no está descargada
    extra = build_corpus(tier=2, edition_key="sblgnt", data_dir=data, only_ids={"IgnLong"}, verbose=False,
                         mask_path=os.path.join(ROOT, "metadata", "masks.csv"),
                         reuse_path=os.path.join(ROOT, "metadata", "reuse_ranges.csv"))
    docs = docs + [d for d in extra if d.id not in ids]
    by_id = {d.id: d for d in docs}
    pf, closed = PersonFilter(docs), learn_closed_class(docs)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for metric, feat in (("minmax", "mfw:200"), ("cosine", "mfw:200")):
        fs = FeatureSpace(feat, docs, person_filter=pf, closed_set=closed)
        spec = Spec(features=feat, metric=metric, window=None, iters=100, n_impostors=30, seed=a.semilla)
        eng = GIEngine(docs, spec, fs, min_tokens=300)
        rng = np.random.default_rng(a.semilla)
        banco_amplio = [d.id for d in docs if d.author not in ("Pablo", "Pablo?") and d.n_tokens >= 300 and d.status != "mixed"
                        and not d.id.startswith("IgnLong")]
        banco_epist = [x for x in CATOLICAS + AF + ["3Cor"] if x in by_id and by_id[x].n_tokens >= 300]
        for t in NUCLEO + DIANAS:
            if t not in by_id:
                continue
            cands = [c for c in NUCLEO if c != t]
            s_amp = score(eng, t, cands, [b for b in banco_amplio if b != t], rng, a.iters_amplio)
            s_epi = score(eng, t, cands, [b for b in banco_epist if b != t], rng, a.iters_epistolar)
            rows.append({"metric": metric, "texto": t, "palabras": by_id[t].n_tokens, "banco_epistolar": s_epi,
                         "banco_amplio": s_amp, "condicion": by_id[t].status})
            print(f"  [{metric}] {t:5s} {by_id[t].n_tokens:5d}  epistolar {s_epi:.3f}  amplio {s_amp:.3f}")
        # Ignacio: banco = NT (19 escritos de la matriz) + 1Clem, PolFil, Did, Bern, 3Cor
        ign = [x for x in ["IgnEf", "IgnMagn", "IgnTral", "IgnRom", "IgnFil", "IgnEsm", "IgnPol"] if x in by_id]
        banco_ign = [x for x in ["Rom", "1Cor", "2Cor", "Gal", "Ef", "Flp", "Col", "1Tes", "2Tes", "1Tim", "2Tim", "Tit", "Flm",
                                 "Heb", "Sant", "1Pe", "2Pe", "1Jn", "Jud", "1Clem", "PolFil", "Did", "Bern", "3Cor"] if x in by_id]
        for t in ign:
            s = score(eng, t, [c for c in ign if c != t], banco_ign, rng, a.iters_amplio)
            rows.append({"metric": metric, "texto": t, "palabras": by_id[t].n_tokens, "banco_epistolar": None,
                         "banco_amplio": s, "condicion": "Ignacio auténtica (LOO)"})
            print(f"  [{metric}] Ignacio {t:8s} {s:.3f}")
        for d in sorted((x for x in docs if x.id.startswith("IgnLong")), key=lambda x: x.id):
            s = score(eng, d.id, ign, banco_ign, rng, a.iters_amplio)
            rows.append({"metric": metric, "texto": d.id, "palabras": d.n_tokens, "banco_epistolar": None,
                         "banco_amplio": s, "condicion": f"recensión larga ({d.status})"})
            print(f"  [{metric}] {d.id:10s} {d.status:8s} {s:.3f}")
    pd.DataFrame(rows).to_csv(os.path.join(out_dir, "p6_p7_impostores.csv"), index=False, float_format="%.3f")
    print(f"→ {out_dir}/p6_p7_impostores.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())

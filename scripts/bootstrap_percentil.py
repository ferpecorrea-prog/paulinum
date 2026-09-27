#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap_percentil.py — intervalos de confianza del percentil intra-autor (mismo rasero).

A partir de results/<run>/pair_distances_<metric>.csv (envolvente) y double_standard_ledger_<metric>.csv:
  (a) IC 95 % por bootstrap de AUTORES: se remuestrean con reemplazo los autores de la envolvente
      (2.000 remuestreos) y se recalcula el percentil de cada carta;
  (b) leave-one-author-out: percentil sin cada autor y autor más influyente (mayor desplazamiento);
  (c) IC 95 % por bootstrap de VENTANAS: 100 réplicas de la matriz de distancias, cada una media de 20
      sorteos de ventanas con semilla distinta (requiere recomputar distancias: es la parte lenta).
Salidas: bootstrap_percentil_<metric>.csv y loo_autor_percentil_<metric>.csv.
Regla preregistrada (campaña 03): si el IC cruza 90, la carta se declara «indeterminada», no «anómala».

Uso: python scripts/bootstrap_percentil.py --run campana_03 --metric minmax [--replicas-ventanas 100] [--sin-ventanas]
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
from paulinum.pipeline import _write_csv, load_config, LETTERS_13  # noqa: E402
from paulinum.sources import CORE_SETS, SISTERS  # noqa: E402
from paulinum.variables import DistanceMatrixBuilder, intra_author_pairs, percentile_of, same_standard_ledger  # noqa: E402
from paulinum.verify import Spec  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--metric", default="minmax")
    ap.add_argument("--config", default=None)
    ap.add_argument("--remuestreos", type=int, default=2000)
    ap.add_argument("--replicas-ventanas", type=int, default=100)
    ap.add_argument("--sin-ventanas", action="store_true")
    ap.add_argument("--edicion", default="sblgnt")
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    env = list(csv.DictReader(open(os.path.join(run_dir, f"pair_distances_{a.metric}.csv"), encoding="utf-8")))
    led = list(csv.DictReader(open(os.path.join(run_dir, f"double_standard_ledger_{a.metric}.csv"), encoding="utf-8")))
    authors = sorted({r["author"] for r in env})
    by_author = {au: np.array([float(r["distance"]) for r in env if r["author"] == au]) for au in authors}
    allv = np.concatenate(list(by_author.values()))
    rng = np.random.default_rng(2026)
    rows, loo_rows = [], []
    for L in led:
        d = float(L["d_mean"])
        pct = percentile_of(d, allv)
        # (a) bootstrap de autores
        boots = []
        for _ in range(a.remuestreos):
            pick = rng.choice(len(authors), size=len(authors), replace=True)
            sample = np.concatenate([by_author[authors[i]] for i in pick])
            boots.append(percentile_of(d, sample))
        lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
        # (b) leave-one-author-out
        shifts = {}
        for au in authors:
            sample = np.concatenate([v for k, v in by_author.items() if k != au])
            shifts[au] = percentile_of(d, sample)
            loo_rows.append({"id": L["id"], "author_out": au, "percentile_without": shifts[au]})
        infl = max(shifts, key=lambda k: abs(shifts[k] - pct))
        rows.append({"id": L["id"], "kind": L["kind"], "d_mean": d, "percentile": pct, "ic_autores_inf": lo,
                     "ic_autores_sup": hi, "autor_influyente": infl, "percentil_sin_ese_autor": shifts[infl],
                     "cruza_90_autores": bool(lo <= 0.90 <= hi),
                     "veredicto": "indeterminado" if lo <= 0.90 <= hi else ("anomalo" if lo > 0.90 else "dentro")})
    # (c) bootstrap de ventanas
    if not a.sin_ventanas:
        cfg = load_config(a.config) if a.config else {}
        mr = cfg.get("mismo_rasero", {}) if cfg else {}
        docs = load_corpus(a.edicion)
        pf, closed = PersonFilter(docs), learn_closed_class(docs)
        fs = FeatureSpace(mr.get("rasgos", "mfw:300"), docs, person_filter=pf, closed_set=closed)
        core_name = (cfg.get("rejilla", {}).get("nucleos", ["seven"]) if cfg else ["seven"])[0]
        core = [c for c in CORE_SETS[core_name] if any(d.id == c for d in docs)]
        letters = [L["id"] for L in led]
        pairs = intra_author_pairs(docs, cap_pairs_per_author=int(mr.get("tope_pares_por_autor", 120)))
        pcts = {L: [] for L in letters}
        for rep in range(a.replicas_ventanas):
            b = DistanceMatrixBuilder(docs, fs, a.metric, window=int(mr.get("ventana", 500)),
                                      draws=int(mr.get("sorteos", 20)), seed=1000 + rep)
            res = same_standard_ledger(b, letters, core, pairs, exclude_sisters=SISTERS)
            for L in letters:
                pcts[L].append(res["letters"][L]["percentile"])
            if (rep + 1) % 10 == 0:
                print(f"  réplica de ventanas {rep + 1}/{a.replicas_ventanas}")
        for r in rows:
            v = np.array(pcts[r["id"]])
            r["ic_ventanas_inf"], r["ic_ventanas_sup"] = float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
    _write_csv(os.path.join(run_dir, f"bootstrap_percentil_{a.metric}.csv"), rows)
    _write_csv(os.path.join(run_dir, f"loo_autor_percentil_{a.metric}.csv"), loo_rows)
    for r in rows:
        print(f"  {r['id']:5s} pct {r['percentile']:.3f} IC autores [{r['ic_autores_inf']:.2f}-{r['ic_autores_sup']:.2f}] "
              f"sin {r['autor_influyente']}: {r['percentil_sin_ese_autor']:.3f}"
              + (f" IC ventanas [{r['ic_ventanas_inf']:.2f}-{r['ic_ventanas_sup']:.2f}]" if "ic_ventanas_inf" in r else "")
              + f" → {r['veredicto']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

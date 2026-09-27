#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap_percentil.py — intervalos de confianza de los percentiles del mismo rasero (paulinum 1.0, PROTOCOLO § 7.3-7.4).

A partir de results/<run>/pair_distances_<metric>.csv (E, intra-autor), pair_distances_inter_<metric>.csv (B, inter-autor,
carta frente a carta), pair_distances_genero_<metric>.csv (G, saltos de género intra-autor) y
double_standard_ledger_<metric>.csv (distancia de cada carta al núcleo):
  (a) IC 95 % por bootstrap de AUTORES (2.000 remuestreos con reemplazo de los autores de cada envolvente) del percentil
      de cada carta en E (pct_E), en B (pct_B) y en G (pct_G);
  (b) leave-one-author-out en E: percentil sin cada autor y autor más influyente;
  (c) IC 95 % por bootstrap de VENTANAS: 100 réplicas de las distancias con semillas distintas (la parte lenta), para pct_E,
      pct_B y pct_G.
Regla de equivalencia (PROTOCOLO § 7.3), aplicada por scripts/veredicto.py con estos intervalos:
  dentro del rango intra-autor si el IC de pct_E incluye un valor <= 0,90; fuera solo si el IC de pct_E está entero por
  encima de 0,90 Y el IC de pct_B está entero en >= 0,10; en otro caso, indeterminado. Si «fuera», el percentil en G dice
  si la diferencia es del tamaño de un salto de género (pct_G <= 0,90 con IC) o de un cambio de autor.
Salidas: bootstrap_percentil_<metric>.csv y loo_autor_percentil_<metric>.csv.

Uso: python scripts/bootstrap_percentil.py --run paulinum_1_0 --metric minmax [--replicas-ventanas 100] [--sin-ventanas]
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
from paulinum.pipeline import _write_csv, load_config  # noqa: E402
from paulinum.sources import CORE_SETS, SISTERS  # noqa: E402
from paulinum.variables import (DistanceMatrixBuilder, intra_author_pairs, inter_author_pairs, genre_pairs,  # noqa: E402
                                percentile_of, same_standard_ledger)
from paulinum.verify import Spec  # noqa: E402


def _read(path: str) -> list[dict]:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _by_author(rows: list[dict]) -> dict[str, np.ndarray]:
    out: dict[str, list[float]] = {}
    for r in rows:
        out.setdefault(r["author"].split("~")[0], []).append(float(r["distance"]))
    return {k: np.array(v) for k, v in out.items()}


def _boot(d: float, by_author: dict[str, np.ndarray], rng: np.random.Generator, n: int) -> tuple[float, float, float]:
    """Percentil y su IC 95 % por remuestreo de autores."""
    if not by_author:
        return float("nan"), float("nan"), float("nan")
    authors = sorted(by_author)
    allv = np.concatenate([by_author[a] for a in authors])
    pct = percentile_of(d, allv)
    boots = []
    for _ in range(n):
        pick = rng.choice(len(authors), size=len(authors), replace=True)
        boots.append(percentile_of(d, np.concatenate([by_author[authors[i]] for i in pick])))
    return pct, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


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
    env_e = _by_author(_read(os.path.join(run_dir, f"pair_distances_{a.metric}.csv")))
    env_b = _by_author(_read(os.path.join(run_dir, f"pair_distances_inter_{a.metric}.csv")))
    env_g = _by_author(_read(os.path.join(run_dir, f"pair_distances_genero_{a.metric}.csv")))
    led = _read(os.path.join(run_dir, f"double_standard_ledger_{a.metric}.csv"))
    if not led:
        print("sin cartas en el ledger (¿ejecución sin dianas?): nada que calcular")
        return 0
    rng = np.random.default_rng(2026)
    rows, loo_rows = [], []
    all_e = np.concatenate(list(env_e.values())) if env_e else np.array([])
    for L in led:
        d = float(L["d_mean"])
        pe, pe_lo, pe_hi = _boot(d, env_e, rng, a.remuestreos)
        pb, pb_lo, pb_hi = _boot(d, env_b, rng, a.remuestreos)
        pg, pg_lo, pg_hi = _boot(d, env_g, rng, a.remuestreos)
        shifts = {}
        for au in sorted(env_e):
            sample = np.concatenate([v for k, v in env_e.items() if k != au])
            shifts[au] = percentile_of(d, sample)
            loo_rows.append({"id": L["id"], "author_out": au, "percentile_without": shifts[au]})
        infl = max(shifts, key=lambda k: abs(shifts[k] - pe)) if shifts else ""
        rows.append({"id": L["id"], "kind": L["kind"], "d_mean": d,
                     "pct_E": pe, "ic_autores_E_inf": pe_lo, "ic_autores_E_sup": pe_hi,
                     "pct_B": pb, "ic_autores_B_inf": pb_lo, "ic_autores_B_sup": pb_hi,
                     "pct_G": pg, "ic_autores_G_inf": pg_lo, "ic_autores_G_sup": pg_hi,
                     "autor_influyente": infl, "percentil_E_sin_ese_autor": shifts.get(infl, float("nan"))})
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
        cap = int(mr.get("tope_pares_por_autor", 120))
        pe_pairs = intra_author_pairs(docs, cap_pairs_per_author=cap)
        pb_pairs = inter_author_pairs(docs, cap_pairs_per_author=cap)
        pg_pairs = genre_pairs(docs, cap_pairs_per_author=cap)
        pcts = {L: {"E": [], "B": [], "G": []} for L in letters}
        for rep in range(a.replicas_ventanas):
            b = DistanceMatrixBuilder(docs, fs, a.metric, window=int(mr.get("ventana", 500)),
                                      draws=int(mr.get("sorteos", 20)), seed=1000 + rep)
            res = same_standard_ledger(b, letters, core, pe_pairs, exclude_sisters=SISTERS, pairs_inter=pb_pairs,
                                       pairs_genre=pg_pairs)
            for L in letters:
                pcts[L]["E"].append(res["letters"][L]["percentile"])
                pcts[L]["B"].append(res["letters"][L]["pct_inter"])
                pcts[L]["G"].append(res["letters"][L]["pct_genre"])
            if (rep + 1) % 10 == 0:
                print(f"  réplica de ventanas {rep + 1}/{a.replicas_ventanas}")
        for r in rows:
            for k in ("E", "B", "G"):
                v = np.array([x for x in pcts[r["id"]][k] if not np.isnan(x)])
                r[f"ic_ventanas_{k}_inf"] = float(np.percentile(v, 2.5)) if len(v) else float("nan")
                r[f"ic_ventanas_{k}_sup"] = float(np.percentile(v, 97.5)) if len(v) else float("nan")
    _write_csv(os.path.join(run_dir, f"bootstrap_percentil_{a.metric}.csv"), rows)
    _write_csv(os.path.join(run_dir, f"loo_autor_percentil_{a.metric}.csv"), loo_rows)
    for r in rows:
        print(f"  {r['id']:5s} pct_E {r['pct_E']:.3f} [{r['ic_autores_E_inf']:.2f}-{r['ic_autores_E_sup']:.2f}] "
              f"pct_B {r['pct_B']:.3f} [{r['ic_autores_B_inf']:.2f}-{r['ic_autores_B_sup']:.2f}] "
              f"pct_G {r['pct_G']:.3f} · sin {r['autor_influyente']}: {r['percentil_E_sin_ese_autor']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

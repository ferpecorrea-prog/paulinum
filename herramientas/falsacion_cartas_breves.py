#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
falsacion_cartas_breves.py — comprobación de § 10.1 (tercer punto) del PROTOCOLO de paulinum 1.0:

  «Más del 10 % de las cartas `genuine` de Basilio o de Libanio fuera de su propia envolvente (percentil > 90 con IC
  entero por encima): la envolvente E no representa la variación intra-autor de cartas breves; el nivel 2 se declara
  no concluyente para todas las cartas de menos de 1.000 palabras (Flm, Tit, 2 Tes).»

El código sellado (Sello 2) no escribe ningún archivo con esta comprobación, así que se calcula aquí, fuera del conjunto
sellado, con las mismas piezas y los mismos parámetros que el «mismo rasero» de la campaña (`mismo_rasero` de la
configuración: mfw:300, ventanas de 500 palabras, 20 sorteos, min-max y Delta; `DistanceMatrixBuilder` con su semilla).
Para cada carta genuina de cada autor (≥ min_tokens palabras): distancia media a las demás cartas del autor
(leave-one-out, como la distancia de cada carta paulina al núcleo), percentil de esa media (a) en la envolvente propia del
autor (todos sus pares intra-autor) y (b) en la envolvente E global publicada (`pair_distances_<medida>.csv`), e IC 95 %
del percentil por bootstrap de ventanas (los 20 sorteos). «Fuera» = percentil > 0,90 con el IC entero por encima de 0,90.

Salida: results/<run>/falsacion_cartas_breves_<medida>.csv (una fila por carta) y falsacion_cartas_breves_resumen.csv.
Uso: python herramientas/falsacion_cartas_breves.py --run paulinum_1_0 [--config config/paulinum_1_0.yaml]
"""
from __future__ import annotations

import argparse
import csv
import itertools
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.pipeline import Context, load_config, _write_csv, _read_csv  # noqa: E402
from paulinum.variables import DistanceMatrixBuilder, percentile_of  # noqa: E402
from paulinum.verify import Spec  # noqa: E402

AUTORES = ["Basilio de Cesarea", "Libanio"]
P_INTRA = 0.90


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="paulinum_1_0")
    ap.add_argument("--config", default="config/paulinum_1_0.yaml")
    ap.add_argument("--autores", default=",".join(AUTORES))
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    cfg = load_config(a.config)
    ctx = Context(cfg)
    mr = cfg.get("mismo_rasero", {})
    edition = cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    spec = Spec(features=mr.get("rasgos", "mfw:300"), metric="minmax", window=mr.get("ventana", 500), edition=edition)
    fs = ctx.feature_space(spec)
    resumen = []
    for metric in mr.get("distancias", ["minmax", "delta"]):
        t0 = time.time()
        b = DistanceMatrixBuilder(docs, fs, metric, window=mr.get("ventana", 500), draws=int(mr.get("sorteos", 20)),
                                  min_tokens=ctx.min_tokens)
        env_global = np.array([float(r["distance"]) for r in _read_csv(os.path.join(run_dir, f"pair_distances_{metric}.csv"))])
        rows = []
        for autor in [x.strip() for x in a.autores.split(",") if x.strip()]:
            cartas = [d.id for d in docs if d.author == autor and d.status == "genuine" and (d.genre or "") == "carta"
                      and len(b.ids[d.id]) >= ctx.min_tokens]
            # tensor cartas × cartas × sorteos (simétrico; diagonal 0)
            n = len(cartas)
            T = np.zeros((n, n, b.draws))
            for i, j in itertools.combinations(range(n), 2):
                T[i, j, :] = T[j, i, :] = b.pair_distance_draws(cartas[i], cartas[j])
            env_propia = np.array([T[i, j, :].mean() for i, j in itertools.combinations(range(n), 2)])
            fuera_propia = fuera_global = 0
            for i, L in enumerate(cartas):
                refs = [j for j in range(n) if j != i]
                ds = T[i, refs, :]                       # refs × sorteos
                d_mean = float(ds.mean())
                por_sorteo = ds.mean(axis=0)             # media a las demás cartas en cada sorteo de ventanas
                pct_p = percentile_of(d_mean, env_propia)
                pct_g = percentile_of(d_mean, env_global)
                ic_p = [percentile_of(float(v), env_propia) for v in por_sorteo]
                ic_g = [percentile_of(float(v), env_global) for v in por_sorteo]
                lo_p, hi_p = float(np.percentile(ic_p, 2.5)), float(np.percentile(ic_p, 97.5))
                lo_g, hi_g = float(np.percentile(ic_g, 2.5)), float(np.percentile(ic_g, 97.5))
                fp = pct_p > P_INTRA and lo_p > P_INTRA
                fg = pct_g > P_INTRA and lo_g > P_INTRA
                fuera_propia += int(fp)
                fuera_global += int(fg)
                rows.append({"autor": autor, "id": L, "tokens": len(b.ids[L]), "n_refs": len(refs), "d_mean": d_mean,
                             "pct_envolvente_propia": pct_p, "ic_propia_inf": lo_p, "ic_propia_sup": hi_p,
                             "fuera_propia": fp, "pct_envolvente_E_global": pct_g, "ic_global_inf": lo_g,
                             "ic_global_sup": hi_g, "fuera_E_global": fg})
            resumen.append({"metrica": metric, "autor": autor, "n_cartas": n, "n_pares_propios": len(env_propia),
                            "fuera_propia": fuera_propia, "pct_fuera_propia": round(fuera_propia / n, 4) if n else float("nan"),
                            "fuera_E_global": fuera_global, "pct_fuera_E_global": round(fuera_global / n, 4) if n else float("nan"),
                            "supera_10_pct_propia": bool(n and fuera_propia / n > 0.10),
                            "supera_10_pct_E_global": bool(n and fuera_global / n > 0.10)})
            print(f"  {metric:6s} {autor:20s} cartas {n:3d} · fuera de su envolvente {fuera_propia} ({100 * fuera_propia / n:.1f} %) "
                  f"· fuera de E global {fuera_global} ({100 * fuera_global / n:.1f} %) · {time.time() - t0:.0f} s")
        _write_csv(os.path.join(run_dir, f"falsacion_cartas_breves_{metric}.csv"), rows)
    _write_csv(os.path.join(run_dir, "falsacion_cartas_breves_resumen.csv"), resumen)
    return 0


if __name__ == "__main__":
    sys.exit(main())

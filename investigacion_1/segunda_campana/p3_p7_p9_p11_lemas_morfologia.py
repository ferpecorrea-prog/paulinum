#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P3, P7 (13 lemas), P9 y P11 — Investigación 1, § 4.5 «Cuarto», «Segundo», «Quinto» y «Séptimo».

  P3  morfosintaxis (MorphGNT): distribución de categorías, modos, personas y bigramas de categorías;
      distancia tipificada de cada escrito al núcleo de siete; regla: una carta discutida es divergente si
      queda más lejos que TODOS los controles ajenos en dos de las tres familias.
  P7  Ignacio en trece lemas: cada carta auténtica dejada fuera frente a las otras seis (publicado 0,75-2,97,
      máx. IgnRom); recensión larga frente al núcleo auténtico (interpoladas 0,92-1,66; espurias 1,37-1,66);
      3 Corintios frente al núcleo paulino (publicado 1,075, entre Flp 1,051 y Rom 1,070) si data/local/3Cor.txt existe.
  P9  Dirichlet-multinomial sobre los 13 lemas: log10 LR perfil paulino / perfil no paulino agregado con la
      dispersión intra-autor estimada en los controles (publicado: Flm +7,0; 2Tes +4,9; 2Tim +3,7; Flp +0,4;
      3Cor −1,8; 1Tim −3,2; 1Pe −3,2; Tit −4,8; Col −6,4; Heb −8,4; Ef −8,7; Ignacio auténticas de +7,0 a −6,2).
  P11 afinidad lucana: distancia de cada carta a Lucas-Hechos frente a su distancia al núcleo paulino, en
      13 lemas y en morfología (publicado: Pastorales 1,6-2,6 veces más lejos de Lucas-Hechos que del núcleo).

Uso: python investigacion_1/segunda_campana/p3_p7_p9_p11_lemas_morfologia.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylolib import (ROOT, LEMAS_13, NUCLEO_7, matriz_13_lemas, distancia_13, rasgos_morfologicos,  # noqa: E402
                      estimar_precision, dirichlet_multinomial_lr, asegurar_fuente)
from paulinum.corpus import load_corpus, build_corpus  # noqa: E402

NT19 = ["Rom", "1Cor", "2Cor", "Gal", "Ef", "Flp", "Col", "1Tes", "2Tes", "1Tim", "2Tim", "Tit", "Flm", "Heb", "Sant", "1Pe", "2Pe", "1Jn", "Jud"]
DISC = ["Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb"]
CTRL = ["Sant", "1Pe", "2Pe", "1Jn", "Jud"]
IGN = ["IgnEf", "IgnMagn", "IgnTral", "IgnRom", "IgnFil", "IgnEsm", "IgnPol"]


def z_dist(df: pd.DataFrame, nucleo: list[str]) -> pd.Series:
    mu, sd = df.loc[nucleo].mean(), df.loc[nucleo].std(ddof=1).replace(0, np.nan)
    z = ((df - mu) / sd).fillna(0)
    return np.sqrt((z ** 2).mean(axis=1))


def main() -> int:
    data = os.path.join(ROOT, "data")
    docs = load_corpus("sblgnt", data)
    ids = {d.id for d in docs}
    asegurar_fuente("IgnLong")  # recensión larga de Ignacio (First1KGreek), si no está descargada
    extra = build_corpus(tier=2, edition_key="sblgnt", data_dir=data, only_ids={"IgnLong"}, verbose=False,
                         mask_path=os.path.join(ROOT, "metadata", "masks.csv"), reuse_path=os.path.join(ROOT, "metadata", "reuse_ranges.csv"))
    docs += [d for d in extra if d.id not in ids]
    by_id = {d.id: d for d in docs}
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    m = matriz_13_lemas(docs)

    # ---- P7: Ignacio en 13 lemas
    ign = [i for i in IGN if i in by_id]
    rows = []
    for c in ign:
        d = distancia_13(m, [x for x in ign if x != c])
        rows.append({"texto": c, "condicion": "Ignacio auténtica (LOO)", "d13": float(d[c])})
    d_ign = distancia_13(m, ign)
    for d in sorted((x for x in docs if x.id.startswith("IgnLong")), key=lambda x: int(x.id.split("#")[1])):
        rows.append({"texto": d.id, "condicion": f"recensión larga ({d.status})", "d13": float(d_ign[d.id])})
    if "3Cor" in by_id:
        d7 = distancia_13(m, NUCLEO_7)
        rows.append({"texto": "3Cor", "condicion": "falsificación cierta frente al núcleo paulino de siete", "d13": float(d7["3Cor"])})
        rows.append({"texto": "Flp (LOO)", "condicion": "referencia", "d13": float(distancia_13(m, [x for x in NUCLEO_7 if x != "Flp"])["Flp"])})
        rows.append({"texto": "Rom (LOO)", "condicion": "referencia", "d13": float(distancia_13(m, [x for x in NUCLEO_7 if x != "Rom"])["Rom"])})
    p7 = pd.DataFrame(rows)
    p7.to_csv(os.path.join(out_dir, "p7_ignacio_13_lemas.csv"), index=False, float_format="%.3f")
    print("== P7 · Ignacio, 13 lemas ==")
    print(p7.round(3).to_string(index=False))

    # ---- P3: morfología (MorphGNT) sobre los 19 escritos
    morph = pd.DataFrame([rasgos_morfologicos(by_id[i]) for i in NT19 if i in by_id]).set_index("id").fillna(0.0)
    fam = {"categorias": [c for c in morph.columns if c.startswith("pos_")],
           "modos_personas": [c for c in morph.columns if c.startswith("mood_") or c.startswith("person_")],
           "bigramas": [c for c in morph.columns if c.startswith("bigr_")]}
    p3 = pd.DataFrame({f: z_dist(morph[cols], NUCLEO_7) for f, cols in fam.items()})
    p3["divergente(2 de 3 familias)"] = [
        sum(p3.loc[i, f] > p3.loc[CTRL, f].max() for f in fam) >= 2 if i in DISC else "" for i in p3.index]
    p3.to_csv(os.path.join(out_dir, "p3_morfologia.csv"), float_format="%.3f")
    print("\n== P3 · morfología: distancia tipificada al núcleo de siete ==")
    print(p3.round(3).to_string())

    # ---- P9: Dirichlet-multinomial
    controles = [d.id for d in docs if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and d.n_tokens >= 1000]
    by_author = {}
    for i in controles:
        by_author.setdefault(by_id[i].author, []).append(i)
    precs = {}
    for au, ids_ in by_author.items():
        if len(ids_) >= 2:
            c = m.loc[ids_, LEMAS_13].values.astype(float)
            resto = (m.loc[ids_, "palabras"].values - c.sum(axis=1))[:, None]
            precs[au] = estimar_precision(np.hstack([c, np.maximum(resto, 0)]))
    c = m.loc[NUCLEO_7, LEMAS_13].values.astype(float)
    precs["Pablo (núcleo)"] = estimar_precision(np.hstack([c, np.maximum((m.loc[NUCLEO_7, "palabras"].values - c.sum(axis=1))[:, None], 0)]))
    prec_med = float(np.median([v for k, v in precs.items() if k != "Pablo (núcleo)"])) if len(precs) > 1 else precs["Pablo (núcleo)"]
    negativos = [i for i in CTRL + ["Heb"] if i in by_id] + [i for i in controles if by_id[i].tradition == "cristiano"]
    evaluados = [i for i in NUCLEO_7 + DISC + CTRL + (["3Cor"] if "3Cor" in by_id else []) + ign if i in by_id]
    p9 = dirichlet_multinomial_lr(m, NUCLEO_7, negativos, prec_med, evaluados)
    p9.to_csv(os.path.join(out_dir, "p9_dirichlet_multinomial.csv"), float_format="%.3f")
    print("\n== P9 · precisión (dispersión intra-autor; menor = más disperso):", {k: round(v, 1) for k, v in precs.items()})
    print("   precisión mediana de los controles usada:", round(prec_med, 1))
    print(p9.round(2).to_string())

    # ---- P11: afinidad lucana (misma escala: tipificación con el núcleo paulino de siete)
    if "Lc" in by_id and "Hch" in by_id:
        t = m[LEMAS_13].div(m["palabras"], axis=0) * 1000.0
        mu, sd = t.loc[NUCLEO_7].mean(), t.loc[NUCLEO_7].std(ddof=1)
        z = (t - mu) / sd
        luc = z.loc[["Lc", "Hch"]].mean()
        rows = []
        for i in NT19 + ["Mt", "Mc"]:
            if i not in z.index:
                continue
            core_others = [x for x in NUCLEO_7 if x != i]
            d_core = float(np.sqrt(((z.loc[i] - z.loc[core_others].mean()) ** 2).mean()))
            d_luc = float(np.sqrt(((z.loc[i] - luc) ** 2).mean()))
            rows.append({"id": i, "d13_a_Lucas-Hechos": d_luc, "d13_al_centro_del_nucleo": d_core, "ratio": d_luc / d_core})
        p11 = pd.DataFrame(rows).set_index("id")
        p11.to_csv(os.path.join(out_dir, "p11_afinidad_lucana.csv"), float_format="%.3f")
        print("\n== P11 · afinidad lucana (13 lemas, escala del núcleo paulino) ==")
        print(p11.round(3).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

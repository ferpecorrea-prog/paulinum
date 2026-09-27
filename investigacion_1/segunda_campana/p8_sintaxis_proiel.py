#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P8 — sintaxis sobre el treebank PROIEL (Universal Dependencies / PROIEL nativo), Investigación 1, § 4.5 «Cuarto».

Rasgos por mil palabras, calculados sobre greek-nt.xml (anotación manual del NT; faltan 2 Pe, 1 Jn y, en más
que fragmentos, Judas y 3 Jn; 1 Pe parcial): densidad de modificadores adjetivales (adjetivo con relación
atributiva), de relativas, de participios, de infinitivos, de subordinantes, longitud media de la oración,
proporción de dependientes a la izquierda y distancia media de dependencia. Distancia tipificada al núcleo
de siete (a) completa, (b) sin el rasgo de modificadores adjetivales y (c) con puntuaciones acotadas (|z| ≤ 3).
Regla preregistrada: una discutida es adversa si supera a todos los controles y a Filemón en la distancia
completa. Publicado: Tito 6,2; 1 Pe 4,4; 1 Tim 4,3; Ap 3,3; 2 Tim 2,9; Flm 2,5; Sant 2,3; Ef 2,3; Col 2,1;
Heb 2,1; 2 Tes 1,8; modificadores adjetivales ‰: núcleo 9-13, Flm 15, Heb 20, Sant 28, 2 Tim 29, 1 Pe 45, 1 Tim 47, Tit 64.

Uso: python investigacion_1/segunda_campana/p8_sintaxis_proiel.py
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylolib import ROOT, NUCLEO_7  # noqa: E402
from paulinum.parsers import PROIEL_BOOKS  # noqa: E402

PATH = os.path.join(ROOT, "data", "raw", "proiel", "greek-nt.xml")
CTRL = ["Sant", "1Pe", "2Pe", "1Jn", "Jud", "Ap", "Heb"]


def main() -> int:
    if not os.path.exists(PATH):
        print("falta data/raw/proiel/greek-nt.xml: python -m paulinum fetch --editions")
        return 1
    stats = defaultdict(lambda: defaultdict(float))
    sent_len = defaultdict(list)
    for _, sent in etree.iterparse(PATH, events=("end",), tag="sentence", huge_tree=True):
        toks = [t for t in sent.iter("token") if t.get("form")]
        if not toks:
            sent.clear()
            continue
        cit = toks[0].get("citation-part") or ""
        book = PROIEL_BOOKS.get(cit.split(" ")[0].upper())
        if not book:
            sent.clear()
            continue
        s = stats[book]
        ids = {t.get("id"): i for i, t in enumerate(toks)}
        s["n"] += len(toks)
        sent_len[book].append(len(toks))
        for i, t in enumerate(toks):
            pos = t.get("part-of-speech") or ""
            rel = t.get("relation") or ""
            morph = t.get("morphology") or ""
            head = t.get("head-id")
            if pos.startswith("A") and rel in ("atr", "adnom"):
                s["adj_mod"] += 1
            if pos == "Pr":
                s["relativos"] += 1
            if len(morph) > 3 and morph[3] == "p":
                s["participios"] += 1
            if len(morph) > 3 and morph[3] == "n":
                s["infinitivos"] += 1
            if pos == "G-":
                s["subordinantes"] += 1
            if pos == "C-":
                s["coordinantes"] += 1
            if pos.startswith("R"):
                s["preposiciones"] += 1
            if head and head in ids:
                j = ids[head]
                s["dep_dist"] += abs(j - i)
                s["n_dep"] += 1
                if i < j:
                    s["izquierda"] += 1
        sent.clear()
    rows = []
    for book, s in stats.items():
        n = s["n"]
        rows.append({"id": book, "tokens": int(n), "adj_mod_permil": s["adj_mod"] / n * 1000, "relativos_permil": s["relativos"] / n * 1000,
                     "participios_permil": s["participios"] / n * 1000, "infinitivos_permil": s["infinitivos"] / n * 1000,
                     "subordinantes_permil": s["subordinantes"] / n * 1000, "coordinantes_permil": s["coordinantes"] / n * 1000,
                     "preposiciones_permil": s["preposiciones"] / n * 1000, "long_oracion": float(np.mean(sent_len[book])),
                     "dep_izquierda": s["izquierda"] / max(s["n_dep"], 1), "dist_dependencia": s["dep_dist"] / max(s["n_dep"], 1)})
    df = pd.DataFrame(rows).set_index("id")
    feats = [c for c in df.columns if c != "tokens"]
    core = [c for c in NUCLEO_7 if c in df.index]
    mu, sd = df.loc[core, feats].mean(), df.loc[core, feats].std(ddof=1).replace(0, np.nan)
    z = ((df[feats] - mu) / sd).fillna(0)
    out = pd.DataFrame({"tokens_proiel": df["tokens"], "adj_mod_permil": df["adj_mod_permil"],
                        "d_completa": np.sqrt((z ** 2).mean(axis=1)),
                        "d_sin_adj_mod": np.sqrt((z.drop(columns=["adj_mod_permil"]) ** 2).mean(axis=1)),
                        "d_acotada_3": np.sqrt((z.clip(-3, 3) ** 2).mean(axis=1))})
    order = NUCLEO_7 + ["Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit"] + CTRL
    out = out.loc[[i for i in order if i in out.index]]
    # los controles con menos de 100 tokens anotados (Judas, 3 Jn: «más que fragmentos») no entran en la regla
    ctrl_ok = [c for c in CTRL if c in out.index and out.loc[c, "tokens_proiel"] >= 100] + ["Flm"]
    ctrl_max = out.loc[ctrl_ok, "d_completa"].max()
    out["adversa(regla P8)"] = ["" if i in NUCLEO_7 or i in CTRL else bool(out.loc[i, "d_completa"] > ctrl_max) for i in out.index]
    res_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(res_dir, exist_ok=True)
    df.to_csv(os.path.join(res_dir, "p8_rasgos_sintacticos_proiel.csv"), float_format="%.3f")
    out.to_csv(os.path.join(res_dir, "p8_distancias_sintaxis.csv"), float_format="%.3f")
    print(out.round(2).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

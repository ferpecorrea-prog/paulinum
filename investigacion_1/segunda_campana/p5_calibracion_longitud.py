#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P5 — calibración de la tasa de error por longitud (Investigación 1, § 4.5, tabla de AUC por longitud).

Diseño reconstruido: sobre autores griegos de prosa de autoría segura con varias obras (en el original,
trece: Josefo, Plutarco, Luciano, Epicteto, Dión de Prusa, Arriano, Apiano, Filóstrato, Juliano, Diodoro y
otros; aquí, los autores con ≥ 2 obras del corpus de controles construido), 200 problemas por longitud y
condición: núcleo = seis fragmentos de 2.000 palabras tomados de OTRAS obras del mismo autor; fragmento de
prueba de L palabras (300, 500, 700, 1.000, 1.500, 2.500, 5.000) del mismo autor (positivo) o de otro
(negativo). A cada problema se aplican tres medidas: distancia tipificada de 13 lemas (diccionario
uniforme), Delta coseno sobre 200 formas frecuentes (z frente al núcleo) y verificación por impostores
(GI con 30 impostores de otros autores). Salida: AUC por longitud y medida, tasa de rechazo de auténticos
(13 lemas, umbral = distancia de la carta paulina indicada) y P(auténtico > Tito / 1 Tim / Col).

Requiere el corpus de la campaña 01 o 03 construido (python -m paulinum fetch --tier 2 && build).
Uso: python investigacion_1/segunda_campana/p5_calibracion_longitud.py [--problemas 200] [--edicion sblgnt]
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylolib import ROOT, LEMAS_13, _LEMMA_KEYS, _norm_lemma  # noqa: E402
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter, learn_closed_class, load_lexicon  # noqa: E402
from paulinum.distances import cosine, minmax  # noqa: E402
from paulinum.verify import auc as _auc  # noqa: E402

LONGITUDES = [300, 500, 700, 1000, 1500, 2500, 5000]
NUCLEO_PAULINO = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm"]


def lemma_seq(d, lex):
    if any(d.lemmas):
        return [_norm_lemma(l) for l in d.lemmas]
    return [_norm_lemma(lex.get(f, f)) for f in d.forms_nodia]


def counts13(seq):
    c = Counter(seq)
    return np.array([c.get(_LEMMA_KEYS[l], 0) for l in LEMAS_13], float)


def dist13(frag_counts, frag_len, core_counts, core_lens):
    rates = core_counts / core_lens[:, None] * 1000
    mu, sd = rates.mean(axis=0), rates.std(axis=0, ddof=1)
    sd[sd < 1e-9] = 1e-9
    z = (frag_counts / frag_len * 1000 - mu) / sd
    return float(np.sqrt((z ** 2).mean()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--problemas", type=int, default=200)
    ap.add_argument("--edicion", default="sblgnt")
    ap.add_argument("--semilla", type=int, default=5)
    a = ap.parse_args()
    docs = load_corpus(a.edicion, os.path.join(ROOT, "data"))
    lex = load_lexicon(os.path.join(ROOT, "data", "cache", "lexicon_uniforme.tsv"))
    by_id = {d.id: d for d in docs}
    genuine = [d for d in docs if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and d.n_tokens >= 2500]
    by_author = {}
    for d in genuine:
        by_author.setdefault(d.author, []).append(d)
    authors = [au for au, ds in by_author.items() if len({x.work_group or x.id for x in ds}) >= 2 and sum(x.n_tokens for x in ds) >= 20000]
    if len(authors) < 3:
        print("hacen falta al menos tres autores de control con varias obras largas: construya el corpus de la campaña 01/03")
        return 1
    print("autores de calibración:", ", ".join(authors))
    pf, closed = PersonFilter(docs), learn_closed_class(docs)
    fs = FeatureSpace("mfw:200", docs, person_filter=pf, closed_set=closed)
    ids = {d.id: fs.token_ids(d) for d in docs}
    lem = {d.id: lemma_seq(d, lex) for d in docs}
    rng = np.random.default_rng(a.semilla)
    # distancias paulinas de referencia (13 lemas): Tito, 1 Tim, Col frente al núcleo de siete
    core_c = np.array([counts13(lem[c]) for c in NUCLEO_PAULINO])
    core_n = np.array([by_id[c].n_tokens for c in NUCLEO_PAULINO], float)
    ref = {L: dist13(counts13(lem[L]), by_id[L].n_tokens, core_c, core_n) for L in ("Tit", "1Tim", "Col") if L in by_id}
    print("distancias paulinas de referencia (13 lemas):", {k: round(v, 3) for k, v in ref.items()})

    def fragment(doc, L):
        n = doc.n_tokens
        s = int(rng.integers(0, max(n - L, 0) + 1))
        return s, min(s + L, n)

    def vec_mfw(doc, s, e):
        c = fs.counts_from_ids(ids[doc.id][s:e])
        return c / max(c.sum(), 1e-12)

    rows = []
    for L in LONGITUDES:
        d13_pos, d13_neg, cos_pos, cos_neg, gi_pos, gi_neg = [], [], [], [], [], []
        for k in range(a.problemas):
            au = authors[int(rng.integers(len(authors)))]
            ds = by_author[au]
            test_doc = ds[int(rng.integers(len(ds)))]
            others = [x for x in ds if (x.work_group or x.id) != (test_doc.work_group or test_doc.id)]
            if not others:
                continue
            # núcleo: seis fragmentos de 2.000 palabras de otras obras del autor
            core_frags = [(others[int(rng.integers(len(others)))], 2000) for _ in range(6)]
            core_frags = [(d, *fragment(d, 2000)) for d, _ in core_frags]
            cc = np.array([counts13(lem[d.id][s:e]) for d, s, e in core_frags])
            cn = np.array([e - s for d, s, e in core_frags], float)
            core_mfw = np.array([vec_mfw(d, s, e) for d, s, e in core_frags])
            mu, sd = core_mfw.mean(axis=0), core_mfw.std(axis=0, ddof=1)
            sd[sd < 1e-12] = 1e-12
            for positive in (True, False):
                if positive:
                    d = test_doc
                else:
                    au2 = authors[int(rng.integers(len(authors)))]
                    while au2 == au:
                        au2 = authors[int(rng.integers(len(authors)))]
                    d = by_author[au2][int(rng.integers(len(by_author[au2])))]
                s, e = fragment(d, L)
                if e - s < L:
                    continue
                d13 = dist13(counts13(lem[d.id][s:e]), e - s, cc, cn)
                v = vec_mfw(d, s, e)
                zc = (core_mfw - mu) / sd
                zv = (v - mu) / sd
                dcos = float(cosine(zc, zv[None, :]).min())
                # impostores: 30 fragmentos de L palabras de otros autores (ni au ni el autor del test)
                imps = []
                while len(imps) < 30:
                    au3 = authors[int(rng.integers(len(authors)))]
                    if au3 == au or au3 == d.author:
                        continue
                    di = by_author[au3][int(rng.integers(len(by_author[au3])))]
                    si, ei = fragment(di, L)
                    imps.append(vec_mfw(di, si, ei))
                imps = np.array(imps)
                hits = 0
                for _ in range(20):
                    cols = np.sort(rng.choice(v.shape[0], size=max(2, v.shape[0] // 2), replace=False))
                    dc = minmax(core_mfw[:, cols], v[cols][None, :]).min()
                    di_ = minmax(imps[:, cols], v[cols][None, :]).min()
                    hits += int(dc < di_)
                gi = hits / 20
                (d13_pos if positive else d13_neg).append(d13)
                (cos_pos if positive else cos_neg).append(dcos)
                (gi_pos if positive else gi_neg).append(gi)
        d13_pos, d13_neg = np.array(d13_pos), np.array(d13_neg)
        row = {"longitud": L, "n_pos": len(d13_pos), "n_neg": len(d13_neg),
               "auc_13_lemas": _auc(-d13_pos, -d13_neg), "auc_delta_coseno": _auc(-np.array(cos_pos), -np.array(cos_neg)),
               "auc_impostores": _auc(np.array(gi_pos), np.array(gi_neg))}
        for L_, v in ref.items():
            row[f"P(autentico>{L_})"] = float((d13_pos > v).mean()) if len(d13_pos) else float("nan")
        rows.append(row)
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "p5_calibracion_longitud.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False, float_format="%.3f")
    print("→", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

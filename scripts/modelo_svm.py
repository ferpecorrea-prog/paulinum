#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modelo_svm.py — segundo modelo, independiente del de los impostores: máquina de vectores de soporte
lineal calibrada (sigmoide) y regresión logística sobre ventanas contiguas de 500 palabras.

Diseño preregistrado (§ 0.6 del informe de la campaña 03): ventanas contiguas de 500 tokens, tope de 20
por documento y 120 por autor; positivos = ventanas del núcleo (45), negativos = ventanas de los
documentos de autoría segura de otros autores; z-scores ajustados solo en el entrenamiento de cada
pliegue; class_weight equilibrado; validación GroupKFold de 10 pliegues por autor (el autor de prueba
nunca está en el entrenamiento) y leave-one-letter-out para el núcleo. Para cada carta discutida se
entrena con todo el núcleo y todos los negativos y se informa la P(Pablo) media de sus ventanas y su
percentil entre los negativos (predicciones en validación cruzada) y entre las cartas del núcleo (LOO).
Regla: se informa la concordancia con el GI; no se elige el modelo «mejor».

Salidas: modelo_svm_cv.csv, modelo_svm_percentiles.csv, modelo_svm_percentiles_resumen.csv.
Uso: python scripts/modelo_svm.py --run campana_03 --features mfw:300,closed:150,char3:600,lemma_dict:300
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter, learn_closed_class, load_lexicon  # noqa: E402
from paulinum.pipeline import _write_csv, LETTERS_13  # noqa: E402
from paulinum.sources import CORE_SETS, TARGETS  # noqa: E402
from paulinum.verify import auc as _auc  # noqa: E402


def windows_of(fs: FeatureSpace, doc, W: int, cap: int) -> list[np.ndarray]:
    ids = fs.token_ids(doc)
    n = len(ids)
    out = []
    for s in range(0, n - W + 1, W):
        out.append(fs.counts_from_ids(ids[s:s + W]))
        if len(out) >= cap:
            break
    if not out and n >= 100:
        out.append(fs.counts_from_ids(ids))
    return [c / max(c.sum(), 1e-12) for c in out]


def make_models():
    return {"svm": lambda: CalibratedClassifierCV(LinearSVC(C=1.0, class_weight="balanced", max_iter=5000), method="sigmoid", cv=3),
            "logistic": lambda: LogisticRegression(C=1.0, class_weight="balanced", max_iter=2000)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--features", default="mfw:300,closed:150,char3:600,lemma_dict:300")
    ap.add_argument("--edicion", default="sblgnt")
    ap.add_argument("--ventana", type=int, default=500)
    ap.add_argument("--tope-doc", type=int, default=20)
    ap.add_argument("--tope-autor", type=int, default=120)
    ap.add_argument("--pliegues", type=int, default=10)
    ap.add_argument("--core", default="seven")
    a = ap.parse_args()
    docs = load_corpus(a.edicion)
    by_id = {d.id: d for d in docs}
    core = [c for c in CORE_SETS[a.core] if c in by_id]
    pf, closed, lex = PersonFilter(docs), learn_closed_class(docs), load_lexicon()
    run_dir = os.path.join("results", a.run)
    cv_rows, pct_rows = [], []
    for feat in a.features.split(","):
        fs = FeatureSpace(feat, docs, person_filter=pf, closed_set=closed, lexicon=lex)
        # positivos: ventanas del núcleo; negativos: autores seguros distintos de Pablo
        Xp, gp = [], []
        for c in core:
            for w in windows_of(fs, by_id[c], a.ventana, a.tope_doc):
                Xp.append(w)
                gp.append(c)
        Xn, gn = [], []
        per_author = {}
        for d in docs:
            if d.status != "genuine" or d.author in ("Pablo", "Pablo?"):
                continue
            ws = windows_of(fs, d, a.ventana, a.tope_doc)
            room = a.tope_autor - per_author.get(d.author, 0)
            ws = ws[:max(room, 0)]
            per_author[d.author] = per_author.get(d.author, 0) + len(ws)
            for w in ws:
                Xn.append(w)
                gn.append(d.author)
        Xp, Xn = np.array(Xp), np.array(Xn)
        X = np.vstack([Xp, Xn])
        y = np.concatenate([np.ones(len(Xp)), np.zeros(len(Xn))])
        groups = np.array(gp + gn)
        n_authors = len(set(gn))
        for mname, mk in make_models().items():
            # validación cruzada por autor (negativos) y por carta (núcleo): GroupKFold sobre grupos
            pred = np.full(len(y), np.nan)
            gkf = GroupKFold(n_splits=min(a.pliegues, len(set(groups))))
            for tr, te in gkf.split(X, y, groups):
                if len(set(y[tr])) < 2:
                    continue
                sc = StandardScaler().fit(X[tr])
                m = mk().fit(sc.transform(X[tr]), y[tr])
                pred[te] = m.predict_proba(sc.transform(X[te]))[:, 1]
            ok = ~np.isnan(pred)
            pos_pred, neg_pred = pred[ok & (y == 1)], pred[ok & (y == 0)]
            cv_rows.append({"features": feat, "model": mname, "n_pos": int(len(Xp)), "n_neg": int(len(Xn)),
                            "n_autores_neg": n_authors, "auc_cv_grupo": _auc(pos_pred, neg_pred),
                            "fpr_cv_05": float((neg_pred >= 0.5).mean()), "fnr_cv_05": float((pos_pred < 0.5).mean())})
            # P(Pablo) de cada carta del núcleo en LOO (media de sus ventanas en validación)
            core_p = {c: float(np.nanmean(pred[(groups == c)])) for c in core if (groups == c).any()}
            # modelo final para las discutidas
            sc = StandardScaler().fit(X)
            final = mk().fit(sc.transform(X), y)
            neg_doc_means = neg_pred  # percentil entre ventanas negativas en CV
            for L in LETTERS_13:
                if L not in by_id:
                    continue
                if L in core:
                    p_mean = core_p.get(L, float("nan"))
                    others = [v for k, v in core_p.items() if k != L]
                else:
                    ws = windows_of(fs, by_id[L], a.ventana, a.tope_doc)
                    if not ws:
                        continue
                    p_mean = float(final.predict_proba(sc.transform(np.array(ws)))[:, 1].mean())
                    others = list(core_p.values())
                pct_rows.append({"features": feat, "model": mname, "id": L, "kind": "core_loo" if L in core else "target",
                                 "p_media": p_mean,
                                 "pct_neg": float((neg_doc_means < p_mean).mean()) if len(neg_doc_means) else float("nan"),
                                 "pct_nucleo": float(np.mean([o < p_mean for o in others])) if others else float("nan")})
            print(f"  {feat:15s} {mname:9s} AUC_cv={cv_rows[-1]['auc_cv_grupo']:.3f} FPR={cv_rows[-1]['fpr_cv_05']:.3f} "
                  f"FNR={cv_rows[-1]['fnr_cv_05']:.3f} (n+={len(Xp)}, n-={len(Xn)})")
    _write_csv(os.path.join(run_dir, "modelo_svm_cv.csv"), cv_rows)
    _write_csv(os.path.join(run_dir, "modelo_svm_percentiles.csv"), pct_rows)
    # resumen: mediana entre los modelos
    res = []
    for L in LETTERS_13:
        rs = [r for r in pct_rows if r["id"] == L]
        if not rs:
            continue
        pm = np.array([r["p_media"] for r in rs])
        pn = np.array([r["pct_neg"] for r in rs])
        pc = np.array([r["pct_nucleo"] for r in rs])
        res.append({"id": L, "kind": rs[0]["kind"], "n_modelos": len(rs), "p_media_mediana": float(np.nanmedian(pm)),
                    "pct_neg_mediana": float(np.nanmedian(pn)), "pct_neg_min": float(np.nanmin(pn)),
                    "pct_nucleo_mediana": float(np.nanmedian(pc)), "pct_nucleo_min": float(np.nanmin(pc)),
                    "pct_nucleo_max": float(np.nanmax(pc))})
    _write_csv(os.path.join(run_dir, "modelo_svm_percentiles_resumen.csv"), res)
    for r in res:
        print(f"  {r['id']:5s} P(Pablo) {r['p_media_mediana']:.3f}  pct negativos {r['pct_neg_mediana']:.3f}  pct núcleo {r['pct_nucleo_mediana']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

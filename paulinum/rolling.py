# -*- coding: utf-8 -*-
"""
rolling.py — ventanas deslizantes (heterogeneidad interna, § 7.5 y § 9.5).

Cada carta se recorre con ventanas de `window` palabras y paso `step`; cada ventana se puntúa con
el método de los impostores frente al núcleo (sin la propia carta ni su hermana), con `iters`
iteraciones. Devuelve, por ventana, la posición, la referencia inicial y final y la puntuación GI.
"""
from __future__ import annotations

import numpy as np

from .corpus import Document, mask_vector
from .distances import METRICS
from .features import FeatureSpace
from .sources import SISTERS
from .verify import GIEngine, Spec, Problem


def _refs_for_window(doc: Document, fs: FeatureSpace, start: int, end: int) -> tuple[str, str]:
    """Referencias (capítulo:versículo) del primer y último token de la ventana, sobre la secuencia usada por fs."""
    excl = mask_vector(doc, fs.mask)
    kept = [r for r, e in zip(doc.refs, excl) if not e]
    if not kept:
        return "", ""
    s = min(start, len(kept) - 1)
    e = min(end - 1, len(kept) - 1)
    return kept[s], kept[e]


def rolling_scores(docs: list[Document], engine: GIEngine, letters: list[str], core: list[str],
                   window: int = 400, step: int = 100, iters: int = 60, seed: int = 21) -> list[dict]:
    rng = np.random.default_rng(seed)
    by_id = {d.id: d for d in docs}
    pauline = {d.id for d in docs if d.author in ("Pablo", "Pablo?")}
    rows = []
    fs = engine.fs
    saved_window, saved_iters = engine.spec.window, engine.spec.iters
    engine.spec.iters = iters
    for L in letters:
        doc = by_id[L]
        ids = engine.ids[L]
        n = len(ids)
        cands = [c for c in core if c != L and c not in SISTERS.get(L, [])]
        problem = Problem(f"roll:{L}", "rolling", L, cands, exclude=sorted(pauline))
        pool = engine.impostor_pool(problem)
        if n < window:
            starts = [0]
        else:
            starts = list(range(0, n - window + 1, step))
        k_sel = max(2, int(round(engine.k * engine.spec.feature_frac)))
        n_imp = min(engine.spec.n_impostors, len(pool))
        f = METRICS[engine.spec.metric]
        for s in starts:
            e = min(s + window, n)
            wcounts = fs.counts_from_ids(ids[s:e])
            hits = 0
            for _ in range(iters):
                cols = np.sort(rng.choice(engine.k, size=k_sel, replace=False))
                imps = [pool[i] for i in rng.choice(len(pool), size=n_imp, replace=False)]
                tv = engine._vectors(wcounts, cols)
                cv = engine._vectors(np.array([engine.window_counts(c, rng) for c in cands]), cols)
                iv = engine._vectors(np.array([engine.window_counts(i, rng) for i in imps]), cols)
                hits += int(f(cv, tv).min() < f(iv, tv).min())
            r0, r1 = _refs_for_window(doc, fs, s, e)
            rows.append({"id": L, "start": s, "end": e, "ref_start": r0, "ref_end": r1, "score": hits / iters})
    engine.spec.window, engine.spec.iters = saved_window, saved_iters
    return rows

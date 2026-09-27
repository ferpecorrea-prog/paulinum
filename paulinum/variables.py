# -*- coding: utf-8 -*-
"""
variables.py — variables no autorales: PERMANOVA (Anderson 2001), coordenadas principales (PCoA),
dbRDA (partición de varianza sobre coordenadas principales), envolvente intra-autor y «mismo rasero».

Envolvente intra-autor (§ 9.6): distribución de distancias entre obras distintas de un mismo autor de
control (estado genuine, grupos de obra distintos), calculada con ventanas de W palabras, promediada
sobre `draws` sorteos y con tope de `cap_pairs_per_author` pares por autor. Percentil intra-autor de
una carta: posición de su distancia media al núcleo dentro de esa distribución.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

from .corpus import Document
from .distances import METRICS, Standardizer, Z_BASED, REL_BASED
from .features import FeatureSpace


# ---------------------------------------------------------------------------------------------
# Matrices de distancia entre documentos (ventanas promediadas)
# ---------------------------------------------------------------------------------------------
class DistanceMatrixBuilder:
    def __init__(self, docs: list[Document], fs: FeatureSpace, metric: str, window: int | None = 500,
                 draws: int = 20, seed: int = 7, min_tokens: int = 100):
        self.docs = docs
        self.fs = fs
        self.metric = metric
        self.window = window
        self.draws = draws
        self.rng = np.random.default_rng(seed)
        self.ids = {d.id: fs.token_ids(d) for d in docs}
        self.full = {d.id: fs.counts_from_ids(self.ids[d.id]) for d in docs}
        ref = np.array([self._rel(self.full[d.id]) for d in docs if len(self.ids[d.id]) >= min_tokens])
        self.std = Standardizer(ref)

    @staticmethod
    def _rel(c):
        s = c.sum()
        return c / s if s > 0 else c

    def _vec(self, counts: np.ndarray) -> np.ndarray:
        c = np.atleast_2d(counts)
        if self.metric in Z_BASED:
            return self.std.z(c / np.maximum(c.sum(axis=1, keepdims=True), 1e-12))
        if self.metric in REL_BASED:
            return c / np.maximum(c.sum(axis=1, keepdims=True), 1e-12)
        return c

    def _window(self, doc_id: str) -> np.ndarray:
        ids = self.ids[doc_id]
        W = self.window
        if not W or len(ids) <= W:
            return self.full[doc_id]
        s = int(self.rng.integers(0, len(ids) - W + 1))
        return self.fs.counts_from_ids(ids[s:s + W])

    def pair_distance(self, a: str, b: str) -> float:
        """Distancia media entre a y b sobre `draws` sorteos de ventanas."""
        f = METRICS[self.metric]
        vals = []
        for _ in range(self.draws):
            va = self._vec(self._window(a))
            vb = self._vec(self._window(b))
            vals.append(float(f(va, vb)[0]))
        return float(np.mean(vals))

    def matrix(self, ids: list[str]) -> np.ndarray:
        n = len(ids)
        M = np.zeros((n, n))
        for i, j in itertools.combinations(range(n), 2):
            M[i, j] = M[j, i] = self.pair_distance(ids[i], ids[j])
        return M

    def window_matrix(self, doc_windows: list[tuple[str, int, int]]) -> np.ndarray:
        """Matriz de distancias entre ventanas fijas [(doc, inicio, fin), ...] (para PERMANOVA y rolling)."""
        f = METRICS[self.metric]
        vecs = np.vstack([self._vec(self.fs.counts_from_ids(self.ids[d][s:e])) for d, s, e in doc_windows])
        n = len(vecs)
        M = np.zeros((n, n))
        for i in range(n):
            M[i, :] = f(vecs, vecs[i])
        np.fill_diagonal(M, 0.0)
        return M


def fixed_windows(doc: Document, fs: FeatureSpace, window: int = 400, step: int | None = None) -> list[tuple[str, int, int]]:
    n = fs.sequence_length(doc)
    step = step or window
    if n < window:
        return [(doc.id, 0, n)] if n > 0 else []
    return [(doc.id, s, s + window) for s in range(0, n - window + 1, step)]


# ---------------------------------------------------------------------------------------------
# PERMANOVA y PCoA / dbRDA
# ---------------------------------------------------------------------------------------------
def _gower(D: np.ndarray) -> np.ndarray:
    A = -0.5 * D ** 2
    n = A.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    return J @ A @ J


def permanova(D: np.ndarray, groups: list, permutations: int = 499, seed: int = 11) -> dict:
    """PERMANOVA de un factor (Anderson 2001): pseudo-F, R² y p por permutación."""
    groups = np.asarray(groups)
    n = len(groups)
    labels, inv = np.unique(groups, return_inverse=True)
    k = len(labels)
    if k < 2 or n <= k:
        return {"n": n, "k": k, "R2": float("nan"), "pseudo_F": float("nan"), "p": float("nan")}
    G = _gower(D)
    sst = np.trace(G)

    def ssw(idx):
        H = np.zeros((n, n))
        for g in range(k):
            m = idx == g
            H[np.ix_(m, m)] = 1.0 / m.sum()
        return np.trace(G) - np.trace(H @ G)

    def stat(idx):
        w = ssw(idx)
        a = sst - w
        return (a / (k - 1)) / (w / (n - k)), a / sst

    F, R2 = stat(inv)
    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(permutations):
        Fp, _ = stat(rng.permutation(inv))
        if Fp >= F - 1e-12:
            ge += 1
    return {"n": int(n), "k": int(k), "R2": float(R2), "pseudo_F": float(F), "p": (ge + 1) / (permutations + 1)}


def pcoa(D: np.ndarray, n_axes: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    G = _gower(D)
    vals, vecs = np.linalg.eigh(G)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    keep = vals > 1e-10
    vals, vecs = vals[keep], vecs[:, keep]
    coords = vecs * np.sqrt(vals)
    if n_axes:
        coords, vals = coords[:, :n_axes], vals[:n_axes]
    return coords, vals


def dbrda_partition(D: np.ndarray, variables: dict[str, list]) -> dict:
    """
    Regresión de las coordenadas principales sobre las variables (codificadas como indicadores):
    R² total de cada variable y R² del conjunto, con la parte compartida (RDA basada en distancias).
    """
    coords, vals = pcoa(D)
    Y = coords
    total = (Y ** 2).sum()
    n = Y.shape[0]

    def design(names):
        cols = [np.ones((n, 1))]
        for v in names:
            g = np.asarray(variables[v])
            labs = np.unique(g)
            for lab in labs[1:]:
                cols.append((g == lab).astype(float)[:, None])
        return np.hstack(cols)

    def r2(names):
        X = design(names)
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        fitted = X @ beta
        return float(((fitted - Y.mean(axis=0)) ** 2).sum() / total)

    out = {v: r2([v]) for v in variables}
    out["_conjunto"] = r2(list(variables)) if variables else float("nan")
    return out


# ---------------------------------------------------------------------------------------------
# Envolvente intra-autor y mismo rasero
# ---------------------------------------------------------------------------------------------
def intra_author_pairs(docs: list[Document], cap_pairs_per_author: int = 120, seed: int = 3,
                       exclude_authors: set[str] | None = None) -> list[tuple[str, str, str]]:
    """Pares (autor, id_a, id_b) de obras genuinas del mismo autor con grupo de obra distinto, con tope por autor."""
    rng = np.random.default_rng(seed)
    by_author: dict[str, list[Document]] = {}
    for d in docs:
        if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and (not exclude_authors or d.author not in exclude_authors):
            by_author.setdefault(d.author, []).append(d)
    pairs = []
    for a, ds in sorted(by_author.items()):
        cand = [(a, x.id, y.id) for x, y in itertools.combinations(ds, 2)
                if (x.work_group or x.id) != (y.work_group or y.id)]
        if len(cand) > cap_pairs_per_author:
            idx = rng.choice(len(cand), size=cap_pairs_per_author, replace=False)
            cand = [cand[i] for i in sorted(idx)]
        pairs.extend(cand)
    return pairs


def percentile_of(value: float, distribution: np.ndarray) -> float:
    d = np.asarray(distribution)
    if len(d) == 0 or math.isnan(value):
        return float("nan")
    return float((d < value).mean() + 0.5 * (d == value).mean())


def same_standard_ledger(builder: DistanceMatrixBuilder, letters: list[str], core: list[str],
                         pairs: list[tuple[str, str, str]], exclude_sisters: dict[str, list[str]] | None = None) -> dict:
    """
    Distancia media de cada carta al núcleo (sin la propia carta ni su hermana) y percentil dentro de la
    envolvente intra-autor. Devuelve {'envelope': [...], 'letters': {id: {...}}, 'pairs': [...]}.
    """
    env_vals, env_rows = [], []
    for a, x, y in pairs:
        d = builder.pair_distance(x, y)
        env_vals.append(d)
        env_rows.append({"author": a, "a": x, "b": y, "distance": d})
    env = np.array(env_vals)
    out = {}
    for L in letters:
        refs = [c for c in core if c != L and c not in (exclude_sisters or {}).get(L, [])]
        ds = [builder.pair_distance(L, c) for c in refs]
        mean_d = float(np.mean(ds)) if ds else float("nan")
        out[L] = {"d_mean": mean_d, "percentile": percentile_of(mean_d, env),
                  "d_min": float(np.min(ds)) if ds else float("nan"), "d_max": float(np.max(ds)) if ds else float("nan"),
                  "n_core_refs": len(refs)}
    stats = {"n_pairs": int(len(env)), "min": float(env.min()) if len(env) else float("nan"),
             "q1": float(np.percentile(env, 25)) if len(env) else float("nan"),
             "median": float(np.median(env)) if len(env) else float("nan"),
             "q3": float(np.percentile(env, 75)) if len(env) else float("nan"),
             "max": float(env.max()) if len(env) else float("nan")}
    return {"envelope": env_rows, "envelope_stats": stats, "letters": out}

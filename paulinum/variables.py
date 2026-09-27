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

    def pair_distance_draws(self, a: str, b: str) -> np.ndarray:
        """Las `draws` distancias de cada sorteo de ventanas (para el bootstrap de ventanas)."""
        f = METRICS[self.metric]
        return np.array([float(f(self._vec(self._window(a)), self._vec(self._window(b)))[0]) for _ in range(self.draws)])

    def matrix_rect(self, rows: list[str], cols: list[str], keep_draws: bool = False) -> np.ndarray:
        """Matriz rectangular de distancias medias (draws sorteos) entre dos listas de documentos; con keep_draws,
        tensor (filas, columnas, sorteos)."""
        if keep_draws:
            T = np.zeros((len(rows), len(cols), self.draws))
            for i, a in enumerate(rows):
                for j, b in enumerate(cols):
                    T[i, j, :] = self.pair_distance_draws(a, b) if a != b else 0.0
            return T
        M = np.zeros((len(rows), len(cols)))
        for i, a in enumerate(rows):
            for j, b in enumerate(cols):
                M[i, j] = self.pair_distance(a, b) if a != b else 0.0
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


def inter_author_pairs(docs: list[Document], cap_pairs_per_author: int = 120, seed: int = 5,
                       genre: str = "carta") -> list[tuple[str, str, str]]:
    """Envolvente B (PROTOCOLO § 7.3): pares (autor_a~autor_b, id_a, id_b) de obras genuine de autores DISTINTOS,
    del mismo género (por defecto carta frente a carta), con tope de pares por autor de partida."""
    rng = np.random.default_rng(seed)
    by_author: dict[str, list[Document]] = {}
    for d in docs:
        if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and (d.genre or "") == genre:
            by_author.setdefault(d.author, []).append(d)
    authors = sorted(by_author)
    pairs = []
    for a in authors:
        cand = [(f"{a}~{b}", x.id, y.id) for b in authors if b != a for x in by_author[a] for y in by_author[b]]
        if len(cand) > cap_pairs_per_author:
            idx = rng.choice(len(cand), size=cap_pairs_per_author, replace=False)
            cand = [cand[i] for i in sorted(idx)]
        pairs.extend(cand)
    return pairs


def genre_pairs(docs: list[Document], cap_pairs_per_author: int = 120, seed: int = 9) -> list[tuple[str, str, str]]:
    """Envolvente G (PROTOCOLO § 7.4): pares (autor, id_a, id_b) de obras genuine del mismo autor y de género
    distinto (carta frente a discurso, tratado, etc.), grupo de obra distinto, con tope por autor."""
    rng = np.random.default_rng(seed)
    by_author: dict[str, list[Document]] = {}
    for d in docs:
        if d.status == "genuine" and d.author not in ("Pablo", "Pablo?"):
            by_author.setdefault(d.author, []).append(d)
    pairs = []
    for a, ds in sorted(by_author.items()):
        cand = [(a, x.id, y.id) for x, y in itertools.combinations(ds, 2)
                if x.genre != y.genre and (x.work_group or x.id) != (y.work_group or y.id)]
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


def _stats(env: np.ndarray) -> dict:
    if not len(env):
        return {"n_pairs": 0, "min": float("nan"), "q1": float("nan"), "median": float("nan"), "q3": float("nan"),
                "p90": float("nan"), "max": float("nan")}
    return {"n_pairs": int(len(env)), "min": float(env.min()), "q1": float(np.percentile(env, 25)),
            "median": float(np.median(env)), "q3": float(np.percentile(env, 75)), "p90": float(np.percentile(env, 90)),
            "max": float(env.max())}


def same_standard_ledger(builder: DistanceMatrixBuilder, letters: list[str], core: list[str],
                         pairs: list[tuple[str, str, str]], exclude_sisters: dict[str, list[str]] | None = None,
                         pairs_inter: list[tuple[str, str, str]] | None = None,
                         pairs_genre: list[tuple[str, str, str]] | None = None) -> dict:
    """
    Distancia media de cada carta al núcleo (sin la propia carta ni su hermana) y percentil dentro de la envolvente
    intra-autor E; con `pairs_inter` y `pairs_genre` (paulinum 1.0), también los percentiles en la distribución
    inter-autor B y en la de saltos de género G (PROTOCOLO § 7.3-7.4). Devuelve {'envelope', 'envelope_inter',
    'envelope_genre', '*_stats', 'letters': {id: {...}}, 'overlap_*'}.
    """
    def _env(prs):
        vals, rows = [], []
        for a, x, y in (prs or []):
            d = builder.pair_distance(x, y)
            vals.append(d)
            rows.append({"author": a, "a": x, "b": y, "distance": d})
        return np.array(vals), rows
    env, env_rows = _env(pairs)
    env_b, rows_b = _env(pairs_inter)
    env_g, rows_g = _env(pairs_genre)
    out = {}
    for L in letters:
        refs = [c for c in core if c != L and c not in (exclude_sisters or {}).get(L, [])]
        ds = [builder.pair_distance(L, c) for c in refs]
        mean_d = float(np.mean(ds)) if ds else float("nan")
        out[L] = {"d_mean": mean_d, "percentile": percentile_of(mean_d, env),
                  "pct_inter": percentile_of(mean_d, env_b) if len(env_b) else float("nan"),
                  "pct_genre": percentile_of(mean_d, env_g) if len(env_g) else float("nan"),
                  "d_min": float(np.min(ds)) if ds else float("nan"), "d_max": float(np.max(ds)) if ds else float("nan"),
                  "n_core_refs": len(refs)}
    stats = _stats(env)
    res = {"envelope": env_rows, "envelope_stats": stats, "letters": out,
           "envelope_inter": rows_b, "inter_stats": _stats(env_b), "envelope_genre": rows_g, "genre_stats": _stats(env_g)}
    if len(env) and len(env_g):
        res["overlap_G_E"] = float((env_g <= stats["p90"]).mean())   # fracción de saltos de género dentro del rango intra-autor
    if len(env) and len(env_b):
        res["overlap_B_E"] = float((env_b <= stats["p90"]).mean())   # fracción de pares inter-autor dentro del rango intra-autor
    return res


def nearest_authors(builder: DistanceMatrixBuilder, letters: list[str], core: list[str],
                    exclude_sisters: dict[str, list[str]] | None = None, min_docs: int = 2,
                    precomputed: tuple[np.ndarray, list[str]] | None = None, replicas: int = 200,
                    seed: int = 17) -> list[dict]:
    """Nivel 3 (PROTOCOLO § 8.3): para cada carta, distancia media a cada autor genuine con ≥ min_docs obras y al
    núcleo (sin la carta ni su hermana); posición del núcleo y margen sobre el mejor otro autor, con IC 95 % por
    bootstrap de ventanas (remuestreo de los sorteos de ventana de cada par). `precomputed` = (tensor cartas ×
    documentos × sorteos, ids de columna) evita recalcular las distancias."""
    rng = np.random.default_rng(seed)
    by_id = {d.id: d for d in builder.docs}
    by_author: dict[str, list[str]] = {}
    for d in builder.docs:
        if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and d.id not in letters:
            by_author.setdefault(d.author, []).append(d.id)
    by_author = {a: ids for a, ids in by_author.items() if len(ids) >= min_docs}
    col = {c: j for j, c in enumerate(precomputed[1])} if precomputed else {}
    core_author = by_id[core[0]].author if core and core[0] in by_id else "Pablo"
    core_label = f"{core_author} (núcleo)"
    rows = []
    for L in letters:
        refs = [c for c in core if c != L and c not in (exclude_sisters or {}).get(L, [])]
        core_draws = np.array([builder.pair_distance_draws(L, c) for c in refs]) if refs else np.zeros((0, builder.draws))
        dist = {core_label: float(core_draws.mean()) if refs else float("nan")}
        i = letters.index(L)
        draws = {}
        for a, ids in by_author.items():
            if precomputed and all(x in col for x in ids):
                D = precomputed[0][i, [col[x] for x in ids], :]     # (docs del autor, sorteos)
            else:
                D = np.array([builder.pair_distance_draws(L, x) for x in ids])
            draws[a] = D
            dist[a] = float(D.mean())
        order = sorted(dist.items(), key=lambda kv: kv[1])
        rank = [a for a, _ in order].index(core_label) + 1
        best_other = next((a for a, _ in order if a != core_label), "")
        # IC del margen por bootstrap de ventanas: se remuestrean los sorteos (columnas) de cada par
        margins = []
        if refs and best_other:
            nd = builder.draws
            for _ in range(replicas):
                pick = rng.integers(0, nd, size=nd)
                margins.append(float(core_draws[:, pick].mean() - draws[best_other][:, pick].mean()))
        m_lo = float(np.percentile(margins, 2.5)) if margins else float("nan")
        m_hi = float(np.percentile(margins, 97.5)) if margins else float("nan")
        rows.append({"id": L, "rank_nucleo": rank, "d_nucleo": dist[core_label],
                     "autor_mas_proximo": order[0][0], "d_mas_proximo": order[0][1],
                     "mejor_otro_autor": best_other, "d_mejor_otro": dist.get(best_other, float("nan")),
                     "margen_nucleo_menos_mejor_otro": dist[core_label] - dist.get(best_other, float("nan")),
                     "margen_ic_inf": m_lo, "margen_ic_sup": m_hi, "margen_ic_incluye_0": bool(m_lo <= 0 <= m_hi) if margins else "",
                     "n_autores": len(by_author),
                     "orden": " | ".join(f"{a}:{v:.4f}" for a, v in order[:8])})
    return rows

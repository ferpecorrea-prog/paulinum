# -*- coding: utf-8 -*-
"""
verify.py — verificación de autoría por impostores generales (Koppel y Winter 2014; Kestemont et
al. 2016) con ventanas de igual longitud; construcción de los problemas de calibración de respuesta
conocida; AUC, c@1, banda de indecisión, tasas de error, razón de verosimilitud por densidades y
escala verbal.

Puntuación GI de un problema (diana T, candidatos C, impostores I): en cada iteración se sortean
el 50 % de los rasgos, 30 impostores y una ventana aleatoria de W palabras por documento; acierto si
min_c d(T, c) < min_i d(T, i). GI = fracción de aciertos.

Problemas de respuesta conocida (§ 9.1):
  core_loo     cada carta del núcleo frente a las otras (positivo)
  pos_pairs    obra de un autor de control frente a las demás obras del mismo autor (positivo)
  neg_pairs    obra de un autor frente a las obras de otro autor (negativo)
  pseudo_pairs pseudoepigrafía conocida frente al autor imitado (negativo)
  neg_target   texto no paulino frente al núcleo (negativo)
  target       carta discutida frente al núcleo (respuesta desconocida)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict

import numpy as np
from scipy.stats import gaussian_kde

from .corpus import Document
from .distances import METRICS, Standardizer, Z_BASED, REL_BASED
from .features import FeatureSpace
from .sources import CORE_SETS, TARGETS, SISTERS, IMITATED

VERBAL_SCALE = [(0.3, "no discriminante"), (1.0, "débil"), (2.0, "moderado"), (math.inf, "fuerte")]


def verbal(log10lr: float) -> str:
    a = abs(log10lr)
    for lim, label in VERBAL_SCALE:
        if a < lim:
            if label == "no discriminante":
                return label
            side = "H_mismo-autor" if log10lr > 0 else "H_otro-autor"
            return f"apoyo {label} a {side}"
    return "fuerte"


@dataclass
class Spec:
    features: str = "mfw:300"
    metric: str = "minmax"
    window: int | None = 500
    mask: str = "none"
    nodia: bool = False
    core: str = "seven"
    edition: str = "sblgnt"
    iters: int = 100
    feature_frac: float = 0.5
    n_impostors: int = 30
    seed: int = 20260908
    index: int = 0

    @property
    def label(self) -> str:
        w = f"w{self.window}" if self.window else "wall"
        m = "m" + ("none" if self.mask in ("", "none") else self.mask)
        return f"{'nodia' if self.nodia else 'dia'}|{self.features}|{self.metric}|{w}|{m}|{self.core}|{self.edition}"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Problem:
    pid: str
    kind: str          # core_loo | pos_pairs | neg_pairs | pseudo_pairs | neg_target | target
    target: str
    candidates: list[str]
    exclude: list[str] = field(default_factory=list)   # documentos excluidos del banco de impostores
    label: int | None = None                           # 1 positivo, 0 negativo, None desconocido
    author: str = ""
    cand_author: str = ""
    tradition: str = ""


# ---------------------------------------------------------------------------------------------
# Construcción de problemas
# ---------------------------------------------------------------------------------------------
def build_problems(docs: list[Document], core_name: str = "seven", max_pos_per_author: int = 6,
                   n_neg_pairs: int = 150, seed: int = 1, sisters_as_candidates: bool = False,
                   min_tokens: int = 100) -> list[Problem]:
    by_id = {d.id: d for d in docs}
    core = [c for c in CORE_SETS[core_name] if c in by_id]
    pauline = {d.id for d in docs if d.author in ("Pablo", "Pablo?")}
    usable = [d for d in docs if d.status not in ("disputed", "duplicate") and d.n_tokens >= min_tokens]
    rng = np.random.default_rng(seed)
    problems: list[Problem] = []

    def sisters_excl(t):
        return [] if sisters_as_candidates else SISTERS.get(t, [])

    # core_loo
    for c in core:
        cands = [x for x in core if x != c and x not in sisters_excl(c)]
        problems.append(Problem(f"core_loo:{c}", "core_loo", c, cands, exclude=sorted(pauline), label=1,
                                author="Pablo", cand_author="Pablo", tradition="cristiano"))
    # target
    for t in TARGETS:
        if t not in by_id or t in core:   # con el núcleo «trece» las dianas del núcleo ya tienen su leave-one-out
            continue
        cands = [x for x in core if x != t and x not in sisters_excl(t)]
        problems.append(Problem(f"target:{t}", "target", t, cands, exclude=sorted(pauline), label=None,
                                author="Pablo?", cand_author="Pablo", tradition="cristiano"))
    # autores de control con ≥ 2 obras genuinas de grupos de obra distintos
    genuine = [d for d in usable if d.status == "genuine" and d.author not in ("Pablo", "Pablo?")]
    by_author: dict[str, list[Document]] = {}
    for d in genuine:
        by_author.setdefault(d.author, []).append(d)
    multi = {a: ds for a, ds in by_author.items() if len({(x.work_group or x.id) for x in ds}) >= 2}
    all_author_ids = {a: {x.id for x in docs if x.author == a} for a in by_author}
    # pos_pairs
    for a in sorted(multi):
        ds = multi[a]
        idx = np.linspace(0, len(ds) - 1, min(max_pos_per_author, len(ds))).round().astype(int)
        for i in sorted(set(idx.tolist())):
            t = ds[i]
            cands = [x.id for x in ds if x.id != t.id and (x.work_group or x.id) != (t.work_group or t.id)]
            if not cands:
                continue
            problems.append(Problem(f"pos:{t.id}", "pos_pairs", t.id, cands, exclude=sorted(all_author_ids[a]),
                                    label=1, author=a, cand_author=a, tradition=t.tradition))
    # neg_pairs: obra de A frente a obras de B (B con ≥ 2 obras)
    authors_multi = sorted(multi)
    if len(authors_multi) >= 2 and n_neg_pairs > 0:
        pool = []
        for a in sorted(by_author):
            for b in authors_multi:
                if a != b:
                    pool.append((a, b))
        chosen = [pool[i] for i in rng.choice(len(pool), size=min(n_neg_pairs, len(pool)), replace=False)] \
            if len(pool) > n_neg_pairs else pool
        for a, b in chosen:
            t = by_author[a][int(rng.integers(len(by_author[a])))]
            cands = [x.id for x in multi[b]]
            problems.append(Problem(f"neg:{t.id}~{b}", "neg_pairs", t.id, cands,
                                    exclude=sorted(all_author_ids[a] | all_author_ids[b]), label=0,
                                    author=a, cand_author=b, tradition=t.tradition))
    # pseudo_pairs
    for d in usable:
        if d.status != "spurious":
            continue
        imitated = IMITATED.get(d.author)
        if not imitated:
            continue
        cands = [x.id for x in usable if x.author == imitated and x.status in ("genuine", "core")]
        if imitated == "Pablo":
            cands = list(core)
        if not cands:
            continue
        excl = set(all_author_ids.get(imitated, set())) | {x.id for x in docs if x.author == d.author}
        if imitated == "Pablo":
            excl |= pauline
        problems.append(Problem(f"pseudo:{d.id}", "pseudo_pairs", d.id, cands, exclude=sorted(excl), label=0,
                                author=d.author, cand_author=imitated, tradition=d.tradition))
    # neg_target: todo texto no paulino (genuine, spurious, other, mixed) frente al núcleo
    for d in usable:
        if d.id in pauline:
            continue
        excl = pauline | {x.id for x in docs if x.author == d.author}
        problems.append(Problem(f"negT:{d.id}", "neg_target", d.id, list(core), exclude=sorted(excl), label=0,
                                author=d.author, cand_author="Pablo", tradition=d.tradition))
    return problems


# ---------------------------------------------------------------------------------------------
# Motor de impostores
# ---------------------------------------------------------------------------------------------
class GIEngine:
    def __init__(self, docs: list[Document], spec: Spec, fs: FeatureSpace, min_tokens: int = 100):
        self.docs = docs
        self.spec = spec
        self.fs = fs
        self.by_id = {d.id: d for d in docs}
        self.ids: dict[str, list[list[int]]] = {}
        self.length: dict[str, int] = {}
        self.full: dict[str, np.ndarray] = {}
        for d in docs:
            ids = fs.token_ids(d)
            self.ids[d.id] = ids
            self.length[d.id] = len(ids)
            self.full[d.id] = fs.counts_from_ids(ids)
        # estandarización sobre frecuencias relativas de los documentos completos de referencia
        ref = np.array([self._rel(self.full[d.id]) for d in docs if self.length[d.id] >= min_tokens])
        self.std = Standardizer(ref)
        self.k = len(fs.vocab)
        self.min_tokens = min_tokens

    @staticmethod
    def _rel(c: np.ndarray) -> np.ndarray:
        s = c.sum()
        return c / s if s > 0 else c

    def window_counts(self, doc_id: str, rng: np.random.Generator) -> np.ndarray:
        W = self.spec.window
        ids = self.ids[doc_id]
        n = len(ids)
        if not W or n <= W:
            return self.full[doc_id]
        start = int(rng.integers(0, n - W + 1))
        return self.fs.counts_from_ids(ids[start:start + W])

    def _vectors(self, counts: np.ndarray, cols: np.ndarray) -> np.ndarray:
        """Representación según la métrica: z-scores (delta, eder, cosine), relativas (minmax...) o recuentos (labbe).
        Las frecuencias relativas se calculan sobre el vocabulario completo y después se seleccionan los rasgos
        sorteados, de modo que la estandarización (media y desviación típica de los documentos de referencia,
        también sobre el vocabulario completo) sea la misma base en todas las iteraciones."""
        m = self.spec.metric
        full = np.atleast_2d(counts)
        if m in Z_BASED:
            rel = full / np.maximum(full.sum(axis=1, keepdims=True), 1e-12)
            return self.std.z(rel[:, cols], cols)
        if m in REL_BASED:
            rel = full / np.maximum(full.sum(axis=1, keepdims=True), 1e-12)
            return rel[:, cols]
        return full[:, cols]

    def impostor_pool(self, problem: Problem) -> list[str]:
        excl = set(problem.exclude) | {problem.target} | set(problem.candidates)
        t = self.by_id[problem.target]
        pool = []
        for d in self.docs:
            if d.id in excl or d.status in ("disputed", "duplicate"):
                continue
            if d.author == t.author:
                continue
            if t.work_group and d.work_group == t.work_group:
                continue
            if self.length[d.id] < self.min_tokens:
                continue
            pool.append(d.id)
        return pool

    def score(self, problem: Problem, rng: np.random.Generator, return_detail: bool = False) -> dict:
        spec = self.spec
        pool = self.impostor_pool(problem)
        cands = [c for c in problem.candidates if c in self.by_id]
        if not cands or not pool:
            return {"score": float("nan"), "n_iter": 0, "n_pool": len(pool)}
        k_sel = max(2, int(round(self.k * spec.feature_frac)))
        n_imp = min(spec.n_impostors, len(pool))
        hits = 0
        margins = []
        nearest_imp = []
        for _ in range(spec.iters):
            cols = np.sort(rng.choice(self.k, size=k_sel, replace=False))
            imps = [pool[i] for i in rng.choice(len(pool), size=n_imp, replace=False)]
            tv = self._vectors(self.window_counts(problem.target, rng), cols)
            cv = self._vectors(np.array([self.window_counts(c, rng) for c in cands]), cols)
            iv = self._vectors(np.array([self.window_counts(i, rng) for i in imps]), cols)
            f = METRICS[spec.metric]
            dc = f(cv, tv)
            di = f(iv, tv)
            hit = dc.min() < di.min()
            hits += int(hit)
            if return_detail:
                margins.append(float(di.min() - dc.min()))
                nearest_imp.append(imps[int(di.argmin())])
        out = {"score": hits / spec.iters, "n_iter": spec.iters, "n_pool": len(pool), "n_cand": len(cands)}
        if return_detail:
            out["margin_median"] = float(np.median(margins))
            vals, cnts = np.unique(nearest_imp, return_counts=True)
            out["nearest_impostor"] = str(vals[int(cnts.argmax())])
        return out


# ---------------------------------------------------------------------------------------------
# Calibración
# ---------------------------------------------------------------------------------------------
def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Probabilidad de que un positivo puntúe más que un negativo (empates cuentan ½)."""
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    pos = np.asarray(pos)[:, None]
    neg = np.asarray(neg)[None, :]
    return float(((pos > neg).sum() + 0.5 * (pos == neg).sum()) / (pos.size * neg.size))


def c_at_1(pos: np.ndarray, neg: np.ndarray, lo: float, hi: float) -> float:
    """c@1 (Peñas y Rodrigo 2011): (nc + nu·nc/n)/n, con abstención en la banda (lo, hi)."""
    scores = np.concatenate([pos, neg])
    labels = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    n = len(scores)
    decided = (scores <= lo) | (scores >= hi)
    pred = (scores >= hi).astype(float)
    nc = int(((pred == labels) & decided).sum())
    nu = int((~decided).sum())
    return (nc + nu * nc / n) / n if n else float("nan")


def best_band(pos: np.ndarray, neg: np.ndarray) -> tuple[float, float, float]:
    """Banda de indecisión simétrica en torno a 0,5 que maximiza c@1 (paso 0,025; semianchura ≤ 0,25)."""
    best = (0.5, 0.5, c_at_1(pos, neg, 0.5, 0.5))
    for half in np.arange(0.0, 0.2501, 0.025):
        lo, hi = 0.5 - half, 0.5 + half
        v = c_at_1(pos, neg, lo, hi)
        if v > best[2] + 1e-12:
            best = (round(lo, 3), round(hi, 3), v)
    return best


class LRCalibrator:
    """Razón de verosimilitud por densidades de núcleo de las puntuaciones positivas y negativas."""

    def __init__(self, pos: np.ndarray, neg: np.ndarray, floor: float = 1e-3):
        self.pos = np.clip(np.asarray(pos, float), 0.0, 1.0)
        self.neg = np.clip(np.asarray(neg, float), 0.0, 1.0)
        self.floor = floor
        self.kp = gaussian_kde(self._jitter(self.pos)) if len(self.pos) > 2 else None
        self.kn = gaussian_kde(self._jitter(self.neg)) if len(self.neg) > 2 else None

    @staticmethod
    def _jitter(x: np.ndarray) -> np.ndarray:
        # reflexión en los bordes 0 y 1 para que la densidad no se hunda en los extremos
        return np.concatenate([x, -x, 2 - x])

    def log10lr(self, s: float) -> float:
        if self.kp is None or self.kn is None:
            return float("nan")
        fp = max(float(self.kp(s)[0]) * 3, self.floor)  # ×3 compensa la reflexión
        fn = max(float(self.kn(s)[0]) * 3, self.floor)
        return math.log10(fp / fn)


def calibrate(results: list[dict], auc_min: float = 0.80) -> dict:
    pos = np.array([r["score"] for r in results if r["label"] == 1 and not math.isnan(r["score"])])
    neg = np.array([r["score"] for r in results if r["label"] == 0 and not math.isnan(r["score"])])
    a = auc(pos, neg)
    lo, hi, c1 = best_band(pos, neg)
    return {"n_pos": int(len(pos)), "n_neg": int(len(neg)), "auc": a, "c_at_1": c1, "thr_low": lo, "thr_high": hi,
            "fpr_at_0.5": float((neg >= 0.5).mean()) if len(neg) else float("nan"),
            "fnr_at_0.5": float((pos < 0.5).mean()) if len(pos) else float("nan"),
            "valid": bool(a >= auc_min) if not math.isnan(a) else False}


def attach_lr(results: list[dict], subset_neg=None, key: str = "log10lr") -> None:
    """Añade a cada resultado log10 LR (y su escala verbal) calibrado con los positivos y los negativos
    (opcionalmente restringidos por `subset_neg(r) -> bool`)."""
    pos = np.array([r["score"] for r in results if r["label"] == 1 and not math.isnan(r["score"])])
    neg = np.array([r["score"] for r in results if r["label"] == 0 and not math.isnan(r["score"])
                    and (subset_neg is None or subset_neg(r))])
    cal = LRCalibrator(pos, neg)
    for r in results:
        if math.isnan(r["score"]):
            r[key] = float("nan")
            r[key + "_verbal"] = ""
        else:
            v = cal.log10lr(r["score"])
            r[key] = v
            r[key + "_verbal"] = verbal(v) if not math.isnan(v) else ""

# -*- coding: utf-8 -*-
"""
verify.py — verificación de autoría por impostores generales (Koppel y Winter 2014; Kestemont et
al. 2016) con ventanas de igual longitud; construcción de los problemas de calibración de respuesta
conocida; AUC, c@1, banda de indecisión, tasas de error, razón de verosimilitud por densidades y
escala verbal.

Puntuación GI de un problema (diana T, candidatos C, impostores I): en cada iteración se sortean
el 50 % de los rasgos, 30 impostores y una ventana aleatoria de W palabras por documento; acierto si
min_c d(T, c) < min_i d(T, i). GI = fracción de aciertos.

Problemas de respuesta conocida (§ 9.1; paulinum 1.0, PROTOCOLO § 7.1):
  core_loo       cada carta del núcleo frente a las otras (positivo)
  pos_pairs      obra de un autor de control frente a las demás obras del mismo autor (positivo)
  neg_pairs      obra de un autor frente a las obras de otro autor (negativo)
  pseudo_pairs   pseudoepigrafía conocida frente al autor imitado (negativo)
  neg_target     texto no paulino frente al núcleo (negativo)
  genre_pairs    obra de un género de un autor frente a sus obras de otro género (positivo; paulinum 1.0)
  mediated_pairs texto editado por otro frente al editor: Epicteto/Arriano, Plotino/Porfirio (negativo; paulinum 1.0)
  pos_epist      carta de un autor frente a sus OTRAS CARTAS (positivo epistolar; hasta 12 por autor; paulinum 1.0)
  neg_epist      carta de A frente a las cartas de B (negativo epistolar; 200 pares sorteados; paulinum 1.0)
  target         carta discutida frente al núcleo (respuesta desconocida)
Cada resultado lleva además `epistolar` (diana y candidatos de género carta): la calibración epistolar
(PROTOCOLO § 7.2) usa solo los positivos y negativos epistolares (core_loo, pos_epist, neg_epist y los pos_pairs,
neg_pairs, pseudo_pairs y neg_target cuya diana y candidatos son cartas).

Familias de métodos (PROTOCOLO § 6.4), todas con la misma envoltura de problemas, banco de impostores,
ventanas y calibración: `impostores` (GIEngine, distancias sobre rasgos sorteados), `ncd` (NCDEngine,
distancia de compresión normalizada con LZMA sobre el texto de la ventana) y `dirichlet` (DirichletEngine,
verosimilitud predictiva Dirichlet-multinomial del perfil de autor con hiperparámetro compartido).
"""
from __future__ import annotations

import lzma
import math
from dataclasses import dataclass, field, asdict

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import gammaln
from scipy.stats import gaussian_kde

from .corpus import Document, masked_tokens
from .distances import METRICS, Standardizer, Z_BASED, REL_BASED
from .features import FeatureSpace
from .sources import CORE_SETS, TARGETS, SISTERS, IMITATED

# Composición mediada (PROTOCOLO § 7.4, Hm3): texto de un autor editado por otro → problemas negativos frente al editor
MEDIATED = [("Epicteto(ap. Arriano)", "Arriano"), ("Plotino", "Porfirio")]

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
    family: str = "impostores"   # impostores | ncd | dirichlet (paulinum 1.0)

    @property
    def label(self) -> str:
        w = f"w{self.window}" if self.window else "wall"
        m = "m" + ("none" if self.mask in ("", "none") else self.mask)
        base = f"{'nodia' if self.nodia else 'dia'}|{self.features}|{self.metric}|{w}|{m}|{self.core}|{self.edition}"
        return base if self.family == "impostores" else f"{self.family}|{base}"

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
    epistolar: bool = False   # diana y todos los candidatos de género «carta» (calibración epistolar)


def _is_letter(d: Document) -> bool:
    return (d.genre or "") == "carta"


# ---------------------------------------------------------------------------------------------
# Construcción de problemas
# ---------------------------------------------------------------------------------------------
def build_problems(docs: list[Document], core_name: str = "seven", max_pos_per_author: int = 6,
                   n_neg_pairs: int = 150, seed: int = 1, sisters_as_candidates: bool = False,
                   min_tokens: int = 100, sin_dianas: bool = False, core_ids: list[str] | None = None,
                   target_ids: list[str] | None = None, max_pos_epist_per_author: int = 12,
                   n_neg_epist: int = 200) -> list[Problem]:
    """`sin_dianas=True` (fase de implementación, PROTOCOLO § 3.3): no se construye ningún problema cuya diana sea
    una de las catorce cartas (ni target ni core_loo); solo los de respuesta conocida de los controles.
    `core_ids`/`target_ids` (prueba de veredicto con autores de control): sustituyen al núcleo paulino y a las dianas
    por documentos de un autor de control y de su imitador; el «autor bajo examen» es entonces ese autor."""
    by_id = {d.id: d for d in docs}
    custom = core_ids is not None
    core = [c for c in (core_ids if custom else CORE_SETS[core_name]) if c in by_id]
    targets = [t for t in (target_ids if custom else TARGETS) if t in by_id]
    if custom:
        under_test = {by_id[c].author for c in core} | {by_id[t].author for t in targets}
        pauline = {d.id for d in docs if d.author in under_test} | set(core) | set(targets)
        core_author = by_id[core[0]].author if core else "?"
    else:
        pauline = {d.id for d in docs if d.author in ("Pablo", "Pablo?")}
        core_author = "Pablo"
    usable = [d for d in docs if d.status not in ("disputed", "duplicate") and d.n_tokens >= min_tokens]
    rng = np.random.default_rng(seed)
    problems: list[Problem] = []

    def sisters_excl(t):
        return [] if sisters_as_candidates else SISTERS.get(t, [])

    # core_loo
    for c in ([] if sin_dianas else core):
        cands = [x for x in core if x != c and x not in sisters_excl(c)]
        problems.append(Problem(f"core_loo:{c}", "core_loo", c, cands, exclude=sorted(pauline), label=1,
                                author=core_author, cand_author=core_author, tradition=by_id[c].tradition,
                                epistolar=_is_letter(by_id[c]) and all(_is_letter(by_id[x]) for x in cands)))
    # target
    for t in ([] if sin_dianas else targets):
        if t in core:   # con el núcleo «trece» las dianas del núcleo ya tienen su leave-one-out
            continue
        cands = [x for x in core if x != t and x not in sisters_excl(t)]
        problems.append(Problem(f"target:{t}", "target", t, cands, exclude=sorted(pauline), label=None,
                                author=by_id[t].author if custom else "Pablo?", cand_author=core_author,
                                tradition=by_id[t].tradition,
                                epistolar=_is_letter(by_id[t]) and all(_is_letter(by_id[x]) for x in cands)))
    # autores de control con ≥ 2 obras genuinas de grupos de obra distintos (el autor bajo examen queda fuera)
    genuine = [d for d in usable if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and d.id not in pauline]
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
                                    label=1, author=a, cand_author=a, tradition=t.tradition,
                                    epistolar=_is_letter(t) and all(_is_letter(by_id[c]) for c in cands)))
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
                                    author=a, cand_author=b, tradition=t.tradition,
                                    epistolar=_is_letter(t) and all(_is_letter(by_id[c]) for c in cands)))
    # pseudo_pairs
    for d in usable:
        if d.status != "spurious":
            continue
        imitated = IMITATED.get(d.author)
        if not imitated:
            continue
        if d.id in pauline:
            continue   # en la prueba de veredicto el imitador es la diana, no un control
        cands = [x.id for x in usable if x.author == imitated and x.status in ("genuine", "core")]
        if imitated == "Pablo":
            cands = list(core)
        if not cands:
            continue
        excl = set(all_author_ids.get(imitated, set())) | {x.id for x in docs if x.author == d.author}
        if imitated == "Pablo":
            excl |= pauline
        problems.append(Problem(f"pseudo:{d.id}", "pseudo_pairs", d.id, cands, exclude=sorted(excl), label=0,
                                author=d.author, cand_author=imitated, tradition=d.tradition,
                                epistolar=_is_letter(d) and all(_is_letter(by_id[c]) for c in cands)))
    # neg_target: todo texto no paulino (genuine, spurious, other, mixed) frente al núcleo
    for d in usable:
        if d.id in pauline:
            continue
        excl = pauline | {x.id for x in docs if x.author == d.author}
        problems.append(Problem(f"negT:{d.id}", "neg_target", d.id, list(core), exclude=sorted(excl), label=0,
                                author=d.author, cand_author=core_author, tradition=d.tradition,
                                epistolar=_is_letter(d) and all(_is_letter(by_id[c]) for c in core)))
    # pos_epist / neg_epist (paulinum 1.0, calibración epistolar): cartas frente a cartas
    letters_by_author = {a: [d for d in ds if _is_letter(d)] for a, ds in by_author.items()}
    epist_authors = sorted(a for a, ds in letters_by_author.items()
                           if len({(x.work_group or x.id) for x in ds}) >= 2)
    for a in epist_authors:
        ds = letters_by_author[a]
        idx = np.linspace(0, len(ds) - 1, min(max_pos_epist_per_author, len(ds))).round().astype(int)
        for i in sorted(set(idx.tolist())):
            t = ds[i]
            cands = [x.id for x in ds if x.id != t.id and (x.work_group or x.id) != (t.work_group or t.id)]
            if not cands:
                continue
            problems.append(Problem(f"posE:{t.id}", "pos_epist", t.id, cands, exclude=sorted(all_author_ids[a]),
                                    label=1, author=a, cand_author=a, tradition=t.tradition, epistolar=True))
    letter_authors = sorted(a for a, ds in letters_by_author.items() if ds)
    if len(epist_authors) >= 1 and len(letter_authors) >= 2 and n_neg_epist > 0:
        pool = [(a, b) for a in letter_authors for b in epist_authors if a != b]
        chosen = [pool[i] for i in rng.choice(len(pool), size=min(n_neg_epist, len(pool)), replace=False)] \
            if len(pool) > n_neg_epist else pool
        for a, b in chosen:
            t = letters_by_author[a][int(rng.integers(len(letters_by_author[a])))]
            cands = [x.id for x in letters_by_author[b]]
            problems.append(Problem(f"negE:{t.id}~{b}", "neg_epist", t.id, cands,
                                    exclude=sorted(all_author_ids[a] | all_author_ids[b]), label=0,
                                    author=a, cand_author=b, tradition=t.tradition, epistolar=True))
    # genre_pairs (paulinum 1.0): obra de un género frente a las obras de otro género del mismo autor genuine
    for a in sorted(by_author):
        ds = by_author[a]
        genres = sorted({d.genre for d in ds})
        if len(genres) < 2:
            continue
        for g in genres:
            same = [d for d in ds if d.genre == g]
            other = [d for d in ds if d.genre != g]
            if not other:
                continue
            idx = np.linspace(0, len(same) - 1, min(max_pos_per_author, len(same))).round().astype(int)
            for i in sorted(set(idx.tolist())):
                t = same[i]
                cands = [x.id for x in other if (x.work_group or x.id) != (t.work_group or t.id)]
                if not cands:
                    continue
                problems.append(Problem(f"genre:{t.id}", "genre_pairs", t.id, cands, exclude=sorted(all_author_ids[a]),
                                        label=1, author=a, cand_author=f"{a} ({'/'.join(x for x in genres if x != g)})",
                                        tradition=t.tradition, epistolar=False))
    # mediated_pairs (paulinum 1.0): texto editado frente al editor, y viceversa
    for edited, editor in MEDIATED:
        for a, b in ((edited, editor), (editor, edited)):
            ta = [d for d in usable if d.author == a and d.status == "genuine"]
            cb = [d.id for d in usable if d.author == b and d.status == "genuine"]
            if not ta or not cb:
                continue
            for t in ta:
                problems.append(Problem(f"mediated:{t.id}~{b}", "mediated_pairs", t.id, cb,
                                        exclude=sorted(all_author_ids.get(a, set()) | all_author_ids.get(b, set())),
                                        label=0, author=a, cand_author=b, tradition=t.tradition, epistolar=False))
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
# Familia B: distancia de compresión normalizada (NCD; Cilibrasi y Vitányi 2005)
# ---------------------------------------------------------------------------------------------
class NCDEngine(GIEngine):
    """
    Misma envoltura que GIEngine (problemas, banco de impostores, 30 impostores y ventana aleatoria por iteración),
    sin muestreo de rasgos: la distancia entre dos ventanas es NCD(x, y) = [C(xy) − mín(C(x), C(y))] / máx(C(x), C(y)),
    con C = longitud comprimida con LZMA (preset 6, un solo flujo) de la ventana como cadena de caracteres sin
    diacríticos, con las formas de 1.ª y 2.ª persona sustituidas por el marcador «_» (PROTOCOLO § 6.4 B).
    La secuencia de palabras es la misma sobre la que GIEngine sortea sus ventanas (texto enmascarado).
    """

    def __init__(self, docs: list[Document], spec: Spec, fs: FeatureSpace, min_tokens: int = 100, preset: int = 6):
        self.docs = docs
        self.spec = spec
        self.fs = fs
        self.by_id = {d.id: d for d in docs}
        self.preset = preset
        self.min_tokens = min_tokens
        self.words: dict[str, list[str]] = {}
        self.length: dict[str, int] = {}
        for d in docs:
            toks = masked_tokens(d, spec.mask, nodia=True)
            self.words[d.id] = [t if fs.pf.keep(t, True) else "_" for t in toks]
            self.length[d.id] = len(self.words[d.id])
        self._c: dict[bytes, int] = {}

    def _compress(self, b: bytes) -> int:
        """
        Longitud LZMA2 (preset 6) de b. El diccionario se ajusta a la menor potencia de 2 que cubre toda la entrada
        (mínimo 64 KiB): como ninguna entrada excede el diccionario, la salida es idéntica byte a byte a la del preset 6
        con su diccionario de 8 MiB (verificado en 289 entradas reales de 1 KB a 721 KB, D-020) y se evita reservar 8 MiB
        por llamada, lo que multiplica por ~4,7 la velocidad en ventanas de 500 palabras.
        """
        v = self._c.get(b)
        if v is None:
            dict_size = max(1 << 16, 1 << (len(b) - 1).bit_length())
            v = len(lzma.compress(b, format=lzma.FORMAT_RAW,
                                  filters=[{"id": lzma.FILTER_LZMA2, "preset": self.preset, "dict_size": dict_size}]))
            if len(self._c) < 200000:
                self._c[b] = v
        return v

    def window_text(self, doc_id: str, rng: np.random.Generator) -> bytes:
        W = self.spec.window
        w = self.words[doc_id]
        if not W or len(w) <= W:
            return " ".join(w).encode("utf-8")
        start = int(rng.integers(0, len(w) - W + 1))
        return " ".join(w[start:start + W]).encode("utf-8")

    def ncd(self, x: bytes, y: bytes) -> float:
        cx, cy = self._compress(x), self._compress(y)
        cxy = self._compress(x + b" " + y)
        return (cxy - min(cx, cy)) / max(cx, cy, 1)

    def score(self, problem: Problem, rng: np.random.Generator, return_detail: bool = False) -> dict:
        spec = self.spec
        pool = self.impostor_pool(problem)
        cands = [c for c in problem.candidates if c in self.by_id]
        if not cands or not pool:
            return {"score": float("nan"), "n_iter": 0, "n_pool": len(pool)}
        n_imp = min(spec.n_impostors, len(pool))
        hits = 0
        margins, nearest_imp = [], []
        for _ in range(spec.iters):
            imps = [pool[i] for i in rng.choice(len(pool), size=n_imp, replace=False)]
            tx = self.window_text(problem.target, rng)
            dc = np.array([self.ncd(tx, self.window_text(c, rng)) for c in cands])
            di = np.array([self.ncd(tx, self.window_text(i, rng)) for i in imps])
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
# Familia C: modelo probabilístico jerárquico Dirichlet-multinomial
# ---------------------------------------------------------------------------------------------
def dirmult_log_predictive(x: np.ndarray, alpha_vec: np.ndarray) -> float:
    """log p(x | α) de la Dirichlet-multinomial (sin el coeficiente multinomial, común a todos los candidatos)."""
    A = alpha_vec.sum()
    N = x.sum()
    return float(gammaln(A) - gammaln(A + N) + np.sum(gammaln(alpha_vec + x) - gammaln(alpha_vec)))


class DirichletEngine(GIEngine):
    """
    Perfil de autor con prior Dirichlet(α·m): m = perfil medio del corpus de referencia (frecuencias relativas de los
    documentos completos), α = concentración estimada por máxima verosimilitud marginal en los documentos genuine de
    la envolvente (hiperparámetro compartido: «jerárquico»). Verosimilitud predictiva de las cuentas de la ventana de
    la diana bajo el candidato = Dirichlet-multinomial con parámetro α·m + n_cand (cuentas completas de todos los
    documentos candidatos, es decir, el perfil del AUTOR candidato); bajo un impostor, ídem con las cuentas de todos
    los documentos del AUTOR impostor presentes en el banco (perfil de autor, simétrico con el candidato). En cada
    iteración se sortean 30 autores impostores y una ventana de la diana; acierto si la verosimilitud del candidato
    supera a la del mejor impostor. Sin muestreo de rasgos (PROTOCOLO § 6.4 C).
    """

    def __init__(self, docs: list[Document], spec: Spec, fs: FeatureSpace, min_tokens: int = 100):
        super().__init__(docs, spec, fs, min_tokens)
        ref_ids = [d.id for d in docs if self.length[d.id] >= min_tokens]
        ref = np.array([self.full[i] for i in ref_ids])
        rel = ref / np.maximum(ref.sum(axis=1, keepdims=True), 1e-12)
        self.m = np.maximum(rel.mean(axis=0), 1e-6)
        self.m /= self.m.sum()
        env = np.array([self.full[d.id] for d in docs if d.status == "genuine" and d.author not in ("Pablo", "Pablo?")
                        and self.length[d.id] >= min_tokens])
        self.alpha = self._fit_alpha(env if len(env) else ref)
        self._author_prof: dict[str, np.ndarray] = {}

    def _fit_alpha(self, X: np.ndarray) -> float:
        """α que maximiza la verosimilitud marginal Dirichlet-multinomial de los documentos de la envolvente bajo el
        prior común α·m (búsqueda unidimensional en log α)."""
        def nll(log_a):
            a = math.exp(log_a) * self.m
            A = a.sum()
            N = X.sum(axis=1)
            ll = gammaln(A) - gammaln(A + N) + (gammaln(a[None, :] + X) - gammaln(a)[None, :]).sum(axis=1)
            return -float(ll.sum())
        res = minimize_scalar(nll, bounds=(math.log(1.0), math.log(1e6)), method="bounded",
                              options={"xatol": 1e-3, "maxiter": 200})
        return float(math.exp(res.x))

    def _profile(self, doc_ids: list[str]) -> np.ndarray:
        return self.alpha * self.m + np.sum([self.full[i] for i in doc_ids], axis=0)

    def impostor_authors(self, problem: Problem) -> dict[str, list[str]]:
        """Banco de impostores agrupado por autor (mismas exclusiones que GIEngine.impostor_pool)."""
        pool = self.impostor_pool(problem)
        by_author: dict[str, list[str]] = {}
        for i in pool:
            by_author.setdefault(self.by_id[i].author, []).append(i)
        return by_author

    def score(self, problem: Problem, rng: np.random.Generator, return_detail: bool = False) -> dict:
        spec = self.spec
        cands = [c for c in problem.candidates if c in self.by_id]
        authors = self.impostor_authors(problem)
        names = sorted(authors)
        if not cands or not names:
            return {"score": float("nan"), "n_iter": 0, "n_pool": len(names)}
        n_imp = min(spec.n_impostors, len(names))
        cand_prof = self._profile(cands)
        prof = {}
        for a in names:
            key = (a, tuple(authors[a]))
            if key not in self._author_prof:
                self._author_prof[key] = self._profile(authors[a])
            prof[a] = self._author_prof[key]
        hits = 0
        margins, nearest_imp = [], []
        for _ in range(spec.iters):
            imps = [names[i] for i in rng.choice(len(names), size=n_imp, replace=False)]
            x = self.window_counts(problem.target, rng)
            lc = dirmult_log_predictive(x, cand_prof)
            li = np.array([dirmult_log_predictive(x, prof[a]) for a in imps])
            hit = lc > li.max()
            hits += int(hit)
            if return_detail:
                margins.append(float(lc - li.max()))
                nearest_imp.append(imps[int(li.argmax())])
        out = {"score": hits / spec.iters, "n_iter": spec.iters, "n_pool": len(names), "n_cand": len(cands),
               "alpha": round(self.alpha, 2)}
        if return_detail:
            out["margin_median"] = float(np.median(margins))
            vals, cnts = np.unique(nearest_imp, return_counts=True)
            out["nearest_impostor"] = str(vals[int(cnts.argmax())])
        return out


ENGINES = {"impostores": GIEngine, "ncd": NCDEngine, "dirichlet": DirichletEngine}


def make_engine(docs: list[Document], spec: Spec, fs: FeatureSpace, min_tokens: int = 100, **kw):
    return ENGINES[spec.family](docs, spec, fs, min_tokens=min_tokens, **kw)


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


def calibrate(results: list[dict], auc_min: float = 0.80, subset=None) -> dict:
    """AUC, c@1, banda y tasas de error; `subset(r) -> bool` restringe positivos y negativos (p. ej. epistolares)."""
    pos = np.array([r["score"] for r in results if r["label"] == 1 and not math.isnan(r["score"])
                    and (subset is None or subset(r))])
    neg = np.array([r["score"] for r in results if r["label"] == 0 and not math.isnan(r["score"])
                    and (subset is None or subset(r))])
    a = auc(pos, neg)
    lo, hi, c1 = best_band(pos, neg)
    return {"n_pos": int(len(pos)), "n_neg": int(len(neg)), "auc": a, "c_at_1": c1, "thr_low": lo, "thr_high": hi,
            "fpr_at_0.5": float((neg >= 0.5).mean()) if len(neg) else float("nan"),
            "fnr_at_0.5": float((pos < 0.5).mean()) if len(pos) else float("nan"),
            "valid": bool(a >= auc_min) if not math.isnan(a) else False}


def attach_lr(results: list[dict], subset_neg=None, key: str = "log10lr", subset_pos=None) -> None:
    """Añade a cada resultado log10 LR (y su escala verbal) calibrado con los positivos y los negativos
    (opcionalmente restringidos por `subset_pos(r)` y `subset_neg(r) -> bool`)."""
    pos = np.array([r["score"] for r in results if r["label"] == 1 and not math.isnan(r["score"])
                    and (subset_pos is None or subset_pos(r))])
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

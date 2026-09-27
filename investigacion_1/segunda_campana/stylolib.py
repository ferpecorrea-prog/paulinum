# -*- coding: utf-8 -*-
"""
stylolib — biblioteca de la segunda campaña de la Investigación 1 (reconstrucción).

El libro (nota 46) describe la biblioteca original `stylolib` con: distancia tipificada de trece lemas,
leave-one-out, remuestreo, Delta de Burrows, Delta coseno (Evert et al. 2017), verificación por impostores
(Koppel y Winter 2014), rasgos morfológicos y bigramas de categorías. Esta reimplementación reutiliza el
paquete paulinum (parsers, corpus, distancias, motor de impostores) y añade lo específico de aquella campaña:

  * matriz_13_lemas(docs)      recuentos de los 13 lemas por documento a partir de la capa de lemas
                                (MorphGNT/PROIEL) o, para textos sin anotación, del diccionario uniforme
  * distancia_13(matriz, nucleo) distancia tipificada (media y desviación típica muestral del núcleo)
  * loo_13, bootstrap_13        leave-one-out y remuestreo multinomial (como en la capa B)
  * rasgos_morfologicos(doc)    distribución de categorías, casos, tiempos, modos, voces y bigramas de categorías
  * dirichlet_multinomial       razón de verosimilitud «perfil paulino» / «perfil no paulino» (P9)

Las rutas de datos se toman de la raíz de paulinum_lab (data/cache/corpus_<edición>.jsonl).
"""
from __future__ import annotations

import math
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from paulinum.corpus import Document, load_corpus  # noqa: E402
from paulinum.features import load_lexicon  # noqa: E402
from paulinum.text import strip_diacritics  # noqa: E402

LEMAS_13 = ["ὁ", "καί", "ἐν", "ἐγώ", "σύ", "ὅς", "αὐτός", "εἰς", "δέ", "γάρ", "οὐ", "μή", "διά"]
# formas de la capa de lemas de MorphGNT/PROIEL para cada lema (los lemas se normalizan con sigma medial)
_LEMMA_KEYS = {l: strip_diacritics(l.replace("ς", "σ")) for l in LEMAS_13}
NUCLEO_6 = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes"]
NUCLEO_7 = NUCLEO_6 + ["Flm"]


def _norm_lemma(l: str) -> str:
    return strip_diacritics(l.replace("ς", "σ")) if l else ""


LEXICON_PATH = os.path.join(ROOT, "data", "cache", "lexicon_uniforme.tsv")


def asegurar_lexicon() -> dict:
    """Carga el diccionario uniforme; si no existe, lo construye con MorphGNT (y PROIEL si está descargado)."""
    lex = load_lexicon(LEXICON_PATH)
    if lex:
        return lex
    import subprocess
    print("[stylolib] no existe data/cache/lexicon_uniforme.tsv: se construye con scripts/construir_lexicon.py --sin-diorisis")
    rc = subprocess.call([sys.executable, os.path.join(ROOT, "scripts", "construir_lexicon.py"), "--sin-diorisis"], cwd=ROOT)
    lex = load_lexicon(LEXICON_PATH)
    if rc != 0 or not lex:
        raise SystemExit("no se pudo construir el lexicón (¿falta `python -m paulinum fetch --tier 1`?)")
    return lex


def asegurar_fuente(source_id: str) -> None:
    """Descarga un archivo del manifiesto si falta (p. ej. la recensión larga de Ignacio, IgnLong)."""
    from paulinum.sources import ALL_SOURCES
    from paulinum.fetch import raw_path, download
    src = next(s for s in ALL_SOURCES if s.id == source_id)
    dest = raw_path(src, os.path.join(ROOT, "data"))
    if not os.path.exists(dest):
        ok, err = download(src.url, dest)
        print(f"[stylolib] descarga de {source_id}: {'ok' if ok else err}")


def matriz_13_lemas(docs: list[Document], lexicon: dict | None = None) -> pd.DataFrame:
    """Recuentos brutos de los 13 lemas (más palabras y lemas distintos) por documento."""
    rows = []
    lex = None
    for d in docs:
        if any(d.lemmas):
            lem = [_norm_lemma(l) for l in d.lemmas]
        else:
            if lex is None:
                lex = lexicon if lexicon else asegurar_lexicon()
            lem = [_norm_lemma(lex.get(f, f)) for f in d.forms_nodia]
        c = Counter(lem)
        row = {"id": d.id, "author": d.author, "status": d.status, "palabras": d.n_tokens,
               "lemas_distintos": len(set(l for l in lem if l))}
        for l in LEMAS_13:
            row[l] = c.get(_LEMMA_KEYS[l], 0)
        rows.append(row)
    return pd.DataFrame(rows).set_index("id")


def distancia_13(m: pd.DataFrame, nucleo: list[str], lemas: list[str] | None = None) -> pd.Series:
    lemas = lemas or LEMAS_13
    t = m[lemas].div(m["palabras"], axis=0) * 1000.0
    mu = t.loc[nucleo].mean(axis=0)
    sd = t.loc[nucleo].std(axis=0, ddof=1)
    z = (t - mu) / sd
    return np.sqrt((z ** 2).mean(axis=1))


def loo_13(m: pd.DataFrame, nucleo: list[str]) -> pd.DataFrame:
    out = {}
    for fuera in nucleo:
        out[fuera] = distancia_13(m, [c for c in nucleo if c != fuera])
    return pd.DataFrame(out)


def bootstrap_13(m: pd.DataFrame, nucleo: list[str], replicas: int = 20000, semilla: int = 3) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    t = m[LEMAS_13].div(m["palabras"], axis=0) * 1000.0
    mu, sd = t.loc[nucleo].mean(axis=0).values, t.loc[nucleo].std(axis=0, ddof=1).values
    rows = []
    for idx in m.index:
        n = int(m.loc[idx, "palabras"])
        cuentas = m.loc[idx, LEMAS_13].values.astype(int)
        p = np.append(cuentas, max(n - cuentas.sum(), 0)) / n
        rep = rng.multinomial(n, p, size=replicas)[:, :13]
        d = np.sqrt((((rep / n * 1000.0 - mu) / sd) ** 2).mean(axis=1))
        rows.append({"id": idx, "ic95_inf": float(np.percentile(d, 2.5)), "ic95_sup": float(np.percentile(d, 97.5)),
                     "mediana_boot": float(np.median(d))})
    return pd.DataFrame(rows).set_index("id")


# ---------------------------------------------------------------------------------------------
# Rasgos morfológicos (MorphGNT: pos y parse en Document.pos / person / mood; casos no almacenados →
# se recomputan desde el archivo MorphGNT cuando se necesita la distribución de casos)
# ---------------------------------------------------------------------------------------------
def rasgos_morfologicos(doc: Document) -> dict:
    n = max(doc.n_tokens, 1)
    pos = Counter(doc.pos)
    mood = Counter(m for m in doc.mood if m)
    person = Counter(p for p in doc.person if p)
    bigr = Counter(zip(doc.pos[:-1], doc.pos[1:]))
    out = {"id": doc.id}
    for k, v in pos.items():
        out[f"pos_{k}"] = v / n * 1000
    for k, v in mood.items():
        out[f"mood_{k}"] = v / n * 1000
    for k, v in person.items():
        out[f"person_{k}"] = v / n * 1000
    for (a, b), v in bigr.most_common(60):
        out[f"bigr_{a}_{b}"] = v / n * 1000
    return out


# ---------------------------------------------------------------------------------------------
# P9: modelo Dirichlet-multinomial sobre los 13 lemas
# ---------------------------------------------------------------------------------------------
def _dm_loglik(counts: np.ndarray, alpha: np.ndarray) -> float:
    n = counts.sum()
    a0 = alpha.sum()
    return (math.lgamma(a0) - math.lgamma(n + a0) + sum(math.lgamma(c + a) - math.lgamma(a) for c, a in zip(counts, alpha)))


def ajustar_dm(matriz_counts: np.ndarray, precision: float) -> np.ndarray:
    """alpha = precisión · perfil medio (perfil = frecuencias relativas medias de las filas, con un
    pseudo-recuento de 0,5 por categoría para que ningún alpha sea 0)."""
    m = matriz_counts + 0.5
    p = (m / m.sum(axis=1, keepdims=True)).mean(axis=0)
    return precision * p


def estimar_precision(matriz_counts: np.ndarray) -> float:
    """Precisión (dispersión intra-autor) por máxima verosimilitud sobre una rejilla logarítmica."""
    best, best_ll = 10.0, -math.inf
    for s in np.logspace(0, 5, 101):
        alpha = ajustar_dm(matriz_counts, s)
        ll = sum(_dm_loglik(r, alpha) for r in matriz_counts)
        if ll > best_ll:
            best, best_ll = float(s), ll
    return best


def dirichlet_multinomial_lr(m: pd.DataFrame, nucleo: list[str], negativos: list[str], precision: float,
                             evaluados: list[str]) -> pd.DataFrame:
    """log10 LR (perfil paulino / perfil no paulino agregado) con la misma precisión para ambos perfiles."""
    def counts(ids):
        c = m.loc[ids, LEMAS_13].values.astype(float)
        resto = (m.loc[ids, "palabras"].values - c.sum(axis=1))[:, None]
        return np.hstack([c, np.maximum(resto, 0)])
    rows = []
    for e in evaluados:
        core = [c for c in nucleo if c != e]
        a_pos = ajustar_dm(counts(core), precision)
        a_neg = ajustar_dm(counts([x for x in negativos if x != e]), precision)
        x = counts([e])[0]
        lr = (_dm_loglik(x, a_pos) - _dm_loglik(x, a_neg)) / math.log(10)
        rows.append({"id": e, "log10lr": lr})
    return pd.DataFrame(rows).set_index("id")

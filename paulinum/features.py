# -*- coding: utf-8 -*-
"""
features.py — espacios de rasgos: palabras frecuentes (mfw:N), clase cerrada (closed:N),
trigramas y tetragramas de caracteres (char3:N, char4:N), lemas de la anotación (lemma:N) y
lemas del diccionario uniforme (lemma_dict:N); exclusión de la persona gramatical; descriptivos.

Convenciones:
  * el vocabulario de cada espacio se fija sobre el conjunto de documentos de referencia de la
    especificación (todo el corpus construido), ordenando por frecuencia total;
  * los n-gramas de caracteres se toman dentro de cada forma con marca de límite «_»;
  * la persona gramatical (1.ª y 2.ª) se excluye: pronombres personales y posesivos de 1.ª y 2.ª
    persona (lista cerrada) y toda forma verbal que la anotación de MorphGNT etiquete en 1.ª o 2.ª
    persona (conjunto de formas aprendido del NT, aplicado por igual a todos los documentos).
"""
from __future__ import annotations

import csv
import os
from collections import Counter

import numpy as np

from .corpus import Document, masked_tokens
from .text import strip_diacritics

# Pronombres personales y posesivos de 1.ª y 2.ª persona (formas normalizadas, con diacríticos)
PERSON_FORMS = {
    "ἐγώ", "ἐμοῦ", "μου", "ἐμοί", "μοι", "ἐμέ", "με", "ἡμεῖσ", "ἡμῶν", "ἡμῖν", "ἡμᾶσ",
    "σύ", "σοῦ", "σου", "σοί", "σοι", "σέ", "σε", "ὑμεῖσ", "ὑμῶν", "ὑμῖν", "ὑμᾶσ",
    "ἐμόσ", "ἐμή", "ἐμόν", "ἐμοῦ", "ἐμῆσ", "ἐμῷ", "ἐμῇ", "ἐμήν", "ἐμοί", "ἐμαί", "ἐμά", "ἐμῶν", "ἐμοῖσ", "ἐμαῖσ", "ἐμούσ", "ἐμάσ",
    "σόσ", "σή", "σόν", "σοῦ", "σῆσ", "σῷ", "σῇ", "σήν", "σοί", "σαί", "σά", "σῶν", "σοῖσ", "σαῖσ", "σούσ", "σάσ",
    "ἡμέτεροσ", "ἡμετέρα", "ἡμέτερον", "ἡμετέρου", "ἡμετέρασ", "ἡμετέρῳ", "ἡμετέρᾳ", "ἡμετέραν", "ἡμέτεροι", "ἡμέτεραι",
    "ἡμέτερα", "ἡμετέρων", "ἡμετέροισ", "ἡμετέραισ", "ἡμετέρουσ",
    "ὑμέτεροσ", "ὑμετέρα", "ὑμέτερον", "ὑμετέρου", "ὑμετέρασ", "ὑμετέρῳ", "ὑμετέρᾳ", "ὑμετέραν", "ὑμέτεροι", "ὑμέτεραι",
    "ὑμέτερα", "ὑμετέρων", "ὑμετέροισ", "ὑμετέραισ", "ὑμετέρουσ",
    "ἐμαυτοῦ", "ἐμαυτῷ", "ἐμαυτόν", "σεαυτοῦ", "σεαυτῷ", "σεαυτόν", "σαυτοῦ", "σαυτῷ", "σαυτόν",
    "ἑαυτῶν",  # ambiguo (1.ª/2.ª/3.ª plural): se excluye por prudencia
}
PERSON_LEMMAS = {"ἐγώ", "σύ", "ἐμόσ", "σόσ", "ἡμέτεροσ", "ὑμέτεροσ", "ἐμαυτοῦ", "σεαυτοῦ"}
# Categorías de clase cerrada en MorphGNT: RA artículo, C conjunción, P preposición, RP/RD/RR/RI pronombres, X partícula
CLOSED_POS = {"RA", "C", "P", "RP", "RD", "RR", "RI", "X"}


def learn_person_verb_forms(docs: list[Document]) -> set[str]:
    """Formas verbales etiquetadas en 1.ª o 2.ª persona en los documentos anotados (NT)."""
    out = set()
    for d in docs:
        for f, p, pe in zip(d.forms, d.pos, d.person):
            if p == "V" and pe in ("1", "2"):
                out.add(f)
    return out


def learn_closed_class(docs: list[Document], min_share: float = 0.9) -> set[str]:
    """Formas que en la anotación del NT llevan categoría de clase cerrada en ≥ 90 % de sus apariciones."""
    tot, clo = Counter(), Counter()
    for d in docs:
        for f, p in zip(d.forms, d.pos):
            if not p:
                continue
            tot[f] += 1
            if p in CLOSED_POS:
                clo[f] += 1
    return {f for f, n in tot.items() if clo[f] / n >= min_share}


class PersonFilter:
    def __init__(self, docs: list[Document]):
        self.verb_forms = learn_person_verb_forms(docs)
        self.forms = PERSON_FORMS | self.verb_forms
        self.forms_nodia = {strip_diacritics(f) for f in self.forms}

    def keep(self, form: str, nodia: bool = False) -> bool:
        return form not in (self.forms_nodia if nodia else self.forms)


def load_lexicon(path: str = os.path.join("data", "cache", "lexicon_uniforme.tsv")) -> dict[str, str]:
    lex = {}
    if not os.path.exists(path):
        return lex
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and not row[0].startswith("#"):
                lex[row[0]] = row[1]
    return lex


def parse_feature_spec(spec: str) -> tuple[str, int]:
    kind, _, n = spec.partition(":")
    return kind, int(n or 0)


class FeatureSpace:
    """
    Vocabulario fijo de un espacio de rasgos y proyección de documentos/ventanas a vectores de recuento.
    `token_ids(doc)` devuelve, para cada token del documento (tras máscara), la lista de índices de
    rasgo que aporta (0 o 1 para palabras y lemas; varios para n-gramas de caracteres).
    """

    def __init__(self, spec: str, docs: list[Document], mask: str = "none", nodia: bool = False,
                 person_filter: PersonFilter | None = None, closed_set: set[str] | None = None,
                 lexicon: dict[str, str] | None = None):
        self.spec = spec
        self.kind, self.n = parse_feature_spec(spec)
        self.mask = mask
        self.nodia = nodia
        self.pf = person_filter or PersonFilter(docs)
        self.closed = closed_set if closed_set is not None else learn_closed_class(docs)
        if nodia:
            self.closed = {strip_diacritics(f) for f in self.closed}
        self.lexicon = lexicon or {}
        self._cache: dict[str, np.ndarray] = {}
        counts = Counter()
        for d in docs:
            counts.update(self._units(d))
        self.vocab = [u for u, _ in counts.most_common(self.n)]
        self.index = {u: i for i, u in enumerate(self.vocab)}

    # ---- unidades ----
    def _tokens(self, d: Document) -> list[str]:
        """Tokens tras la máscara; los de persona gramatical se devuelven como '' para conservar la alineación."""
        toks = masked_tokens(d, self.mask, nodia=self.nodia)
        return [t if self.pf.keep(t, self.nodia) else "" for t in toks]

    def _lemmatize(self, d: Document) -> list[str]:
        forms = masked_tokens(d, self.mask, nodia=False)
        if self.kind == "lemma":
            lem = masked_tokens(d, self.mask, layer="lemmas")
            return [l if (l and l not in PERSON_LEMMAS and self.pf.keep(f)) else "" for l, f in zip(lem, forms)]
        out = []
        for f in forms:
            if not self.pf.keep(f):
                out.append("")
                continue
            key = strip_diacritics(f)
            out.append(self.lexicon.get(key, key))
        return out

    def _units(self, d: Document) -> list[str]:
        """Unidades contables del documento (sin alineación): para fijar el vocabulario."""
        if self.kind in ("mfw", "closed"):
            toks = [t for t in self._tokens(d) if t]
            if self.kind == "closed":
                toks = [t for t in toks if t in self.closed]
            return toks
        if self.kind in ("lemma", "lemma_dict"):
            return [l for l in self._lemmatize(d) if l]
        if self.kind in ("char3", "char4"):
            k = 3 if self.kind == "char3" else 4
            out = []
            for t in self._tokens(d):
                if not t:
                    continue
                s = f"_{t}_"
                out.extend(s[i:i + k] for i in range(len(s) - k + 1))
            return out
        raise ValueError(f"espacio de rasgos desconocido: {self.kind}")

    # ---- proyección ----
    def token_ids(self, d: Document) -> list[list[int]]:
        """Índices de rasgo por token (tras máscara), uno por palabra: las ventanas se sortean sobre esta secuencia,
        de modo que «ventana de 500 palabras» son 500 palabras del texto enmascarado."""
        if self.kind in ("mfw", "closed"):
            toks = self._tokens(d)
            if self.kind == "closed":
                return [[self.index[u]] if (u and u in self.closed and u in self.index) else [] for u in toks]
            return [[self.index[u]] if (u and u in self.index) else [] for u in toks]
        if self.kind in ("lemma", "lemma_dict"):
            return [[self.index[u]] if (u and u in self.index) else [] for u in self._lemmatize(d)]
        k = 3 if self.kind == "char3" else 4
        out = []
        for t in self._tokens(d):
            if not t:
                out.append([])
                continue
            s = f"_{t}_"
            out.append([self.index[g] for g in (s[i:i + k] for i in range(len(s) - k + 1)) if g in self.index])
        return out

    def sequence_length(self, d: Document) -> int:
        """Número de palabras (tras la máscara) sobre el que se sortean las ventanas."""
        return len(masked_tokens(d, self.mask))

    def counts_from_ids(self, ids: list[list[int]]) -> np.ndarray:
        flat = [i for sub in ids for i in sub]
        return np.bincount(flat, minlength=len(self.vocab)).astype(float) if flat else np.zeros(len(self.vocab))

    def doc_counts(self, d: Document) -> np.ndarray:
        if d.id not in self._cache:
            self._cache[d.id] = self.counts_from_ids(self.token_ids(d))
        return self._cache[d.id]


def relative(counts: np.ndarray) -> np.ndarray:
    s = counts.sum()
    return counts / s if s > 0 else counts


def descriptives(d: Document) -> dict:
    n = d.n_tokens
    c = Counter(d.forms)
    imper = sum(1 for m in d.mood if m == "D")
    p12 = sum(1 for f in d.forms if f in PERSON_FORMS)
    return {"id": d.id, "tokens": n, "types": len(c), "ttr": round(len(c) / max(n, 1), 4),
            "imperatives_permil": round(1000.0 * imper / max(n, 1), 2) if any(d.mood) else None,
            "hapax_ratio": round(sum(1 for v in c.values() if v == 1) / max(len(c), 1), 4),
            "mean_word_len": round(float(np.mean([len(f) for f in d.forms])) if n else 0.0, 3),
            "person12_pronouns_permil": round(1000.0 * p12 / max(n, 1), 2),
            "ego_permil": round(1000.0 * sum(1 for f in d.forms if f in ("ἐγώ", "ἐμοῦ", "μου", "ἐμοί", "μοι", "ἐμέ", "με")) / max(n, 1), 2),
            "hemeis_permil": round(1000.0 * sum(1 for f in d.forms if f in ("ἡμεῖσ", "ἡμῶν", "ἡμῖν", "ἡμᾶσ")) / max(n, 1), 2),
            "su_permil": round(1000.0 * sum(1 for f in d.forms if f in ("σύ", "σοῦ", "σου", "σοί", "σοι", "σέ", "σε")) / max(n, 1), 2),
            "humeis_permil": round(1000.0 * sum(1 for f in d.forms if f in ("ὑμεῖσ", "ὑμῶν", "ὑμῖν", "ὑμᾶσ")) / max(n, 1), 2)}

# -*- coding: utf-8 -*-
"""pytest: comprobaciones deterministas de las piezas nuevas de paulinum 1.0 (familias, problemas, envolventes,
rejilla, testigos). No tocan la red ni los datos descargados: construyen documentos sintéticos."""
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from paulinum.corpus import Document, apply_masks  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter  # noqa: E402
from paulinum.pipeline import expand_grid, active_families, campaign_sets  # noqa: E402
from paulinum.sources import WITNESS_EDITIONS, TARGETS, CORE_SETS  # noqa: E402
from paulinum.variables import inter_author_pairs, genre_pairs, intra_author_pairs  # noqa: E402
from paulinum.verify import (Spec, build_problems, make_engine, dirmult_log_predictive, NCDEngine,  # noqa: E402
                             DirichletEngine, GIEngine)

RNG = np.random.default_rng(7)
WORDS_A = ["καί", "δέ", "ὁ", "τοῦ", "ἐν", "εἰς", "γάρ", "οὐ", "τό", "μή", "ὅτι", "πρός", "διά", "ἀλλά", "τῆς"]
WORDS_B = ["λόγος", "θεός", "ἄνθρωπος", "πόλις", "ψυχή", "χρόνος", "ἔργον", "νόμος", "πίστις", "ἀγάπη", "σοφία",
           "ἀλήθεια", "δύναμις", "εἰρήνη", "χάρις"]


def _doc(id_, author, n, p_a=0.6, genre="carta", status="genuine", work_group=""):
    forms = []
    for _ in range(n):
        pool = WORDS_A if RNG.random() < p_a else WORDS_B
        forms.append(pool[int(RNG.integers(len(pool)))])
    refs = [f"{1 + i // 50}:{1 + i % 50}" for i in range(n)]
    d = Document(id=id_, author=author, work=id_, status=status, tradition="x", edition_key="t", forms=forms,
                 forms_nodia=forms, lemmas=[""] * n, pos=[""] * n, person=[""] * n, mood=[""] * n, refs=refs,
                 work_group=work_group, genre=genre, subgenre="", addressee="individuo", source_id=id_, part="")
    apply_masks(d, {}, {})
    return d


def _corpus():
    docs = []
    # autor A: 6 cartas (p_a 0,75), autor B: 5 cartas y 2 discursos (p_a 0,45), autor C: 4 tratados (p_a 0,6)
    for i in range(6):
        docs.append(_doc(f"A{i}", "A", 700, 0.75))
    for i in range(5):
        docs.append(_doc(f"B{i}", "B", 700, 0.45))
    for i in range(2):
        docs.append(_doc(f"Bd{i}", "B", 900, 0.45, genre="discurso"))
    for i in range(4):
        docs.append(_doc(f"C{i}", "C", 800, 0.6, genre="tratado"))
    for i in range(3):
        docs.append(_doc(f"D{i}", "D", 700, 0.6))
    docs.append(_doc("PsA", "Ps-A", 600, 0.5, status="spurious"))
    return docs


def test_expand_grid_por_familia():
    cfg = {"rejilla": {"rasgos": ["mfw:300", "closed:150"], "distancias": ["minmax", "delta"], "ventanas": [500],
                       "mascaras": ["none", "all"], "diacriticos": ["dia"]},
           "parametros": {"iters": 10, "semilla": 5},
           "familias": {"impostores": {"activa": True}, "ncd": {"activa": True, "iters": 3},
                        "dirichlet": {"activa": True, "rasgos": ["mfw:300"]}}}
    assert active_families(cfg) == ["impostores", "ncd", "dirichlet"]
    assert len(expand_grid(cfg, "impostores")) == 8
    assert len(expand_grid(cfg, "ncd")) == 2 and expand_grid(cfg, "ncd")[0].iters == 3
    assert len(expand_grid(cfg, "dirichlet")) == 2
    seeds = {s.seed for f in ("impostores", "ncd", "dirichlet") for s in expand_grid(cfg, f)}
    assert len(seeds) == 12   # semillas distintas entre familias y especificaciones


def test_problemas_epistolares_genero_y_mediados():
    docs = _corpus()
    pr = build_problems(docs, core_ids=["A0", "A1", "A2", "A3"], target_ids=["PsA", "A4"], n_neg_pairs=20, n_neg_epist=20)
    kinds = {p.kind for p in pr}
    assert {"core_loo", "target", "pos_pairs", "neg_pairs", "neg_target", "pos_epist", "neg_epist", "genre_pairs"} <= kinds
    assert all(p.epistolar for p in pr if p.kind in ("core_loo", "target", "pos_epist", "neg_epist"))
    assert any(p.kind == "genre_pairs" and p.author == "B" for p in pr)          # B tiene cartas y discursos
    assert not any(p.kind == "pos_pairs" and p.author == "A" for p in pr)        # el autor bajo examen no es control
    assert {p.target for p in pr if p.kind == "target"} == {"PsA", "A4"}
    pr2 = build_problems(docs, core_ids=["A0", "A1", "A2"], target_ids=["A3"], sin_dianas=True)
    assert not any(p.kind in ("core_loo", "target") for p in pr2)


def test_tres_familias_separan_autores():
    docs = _corpus()
    pf = PersonFilter(docs)
    fs = FeatureSpace("mfw:30", docs, person_filter=pf, closed_set=set())
    pr = build_problems(docs, core_ids=["A0", "A1", "A2", "A3"], target_ids=["A4"], n_neg_pairs=5, n_neg_epist=5)
    pos = [p for p in pr if p.kind == "pos_epist" and p.author == "B"][:3]
    neg = [p for p in pr if p.kind == "neg_epist" and p.author == "D"][:3]   # cartas de D frente a las de B
    for fam, iters in (("impostores", 20), ("dirichlet", 20), ("ncd", 4)):
        spec = Spec(features="mfw:30", metric="minmax", window=300, iters=iters, n_impostors=5, family=fam)
        eng = make_engine(docs, spec, fs)
        assert isinstance(eng, {"impostores": GIEngine, "ncd": NCDEngine, "dirichlet": DirichletEngine}[fam])
        rng = np.random.default_rng(1)
        sp = [eng.score(p, rng)["score"] for p in pos]
        sn = [eng.score(p, rng)["score"] for p in neg]
        assert np.mean(sp) > np.mean(sn), (fam, sp, sn)


def test_dirichlet_predictiva_y_alpha():
    x = np.array([5.0, 3.0, 2.0])
    a_close = np.array([50.0, 30.0, 20.0])
    a_far = np.array([20.0, 30.0, 50.0])
    assert dirmult_log_predictive(x, a_close) > dirmult_log_predictive(x, a_far)
    docs = _corpus()
    fs = FeatureSpace("mfw:30", docs, person_filter=PersonFilter(docs), closed_set=set())
    eng = DirichletEngine(docs, Spec(features="mfw:30", metric="dirmult", window=300, family="dirichlet"), fs)
    assert 1.0 <= eng.alpha <= 1e6 and math.isfinite(eng.alpha)


def test_ncd_propiedades():
    docs = _corpus()
    fs = FeatureSpace("mfw:30", docs, person_filter=PersonFilter(docs), closed_set=set())
    eng = NCDEngine(docs, Spec(features="ncd", metric="ncd", window=300, family="ncd"), fs)
    x = " ".join(docs[0].forms[:300]).encode()
    y = " ".join(docs[7].forms[:300]).encode()
    assert eng.ncd(x, x) < 0.2
    assert 0.0 <= eng.ncd(x, y) <= 1.1
    assert abs(eng.ncd(x, y) - eng.ncd(y, x)) < 0.15


def test_envolventes():
    docs = _corpus()
    E, B, G = intra_author_pairs(docs), inter_author_pairs(docs), genre_pairs(docs)
    assert E and B and G
    assert all(a == "B" for a, _, _ in G)                       # solo B tiene dos géneros
    assert all("~" in a for a, _, _ in B)                       # pares inter-autor etiquetados A~B
    assert all(docs_by_id(docs)[x].genre == "carta" and docs_by_id(docs)[y].genre == "carta" for _, x, y in B)


def docs_by_id(docs):
    return {d.id: d for d in docs}


def test_campaign_sets_y_testigos():
    docs = _corpus()
    cfg = {"rejilla": {"nucleos": ["seven"]}, "parametros": {"nucleo_ids": ["A0", "A1"], "dianas_ids": ["PsA"]}}
    core, targets, letters = campaign_sets(cfg, docs)
    assert core == ["A0", "A1"] and targets == ["PsA"] and letters == ["A0", "A1", "PsA"]
    cfg2 = {"rejilla": {"nucleos": ["seven"]}, "parametros": {"sin_dianas": True}}
    assert campaign_sets(cfg2, docs)[2] == []
    assert "Heb" in TARGETS and len(CORE_SETS["trece"]) == 13
    assert set(WITNESS_EDITIONS) == {"sinaiticus", "sblgnt_rec_sinaiticus", "p46", "sblgnt_rec_p46"}


def test_determinismo_por_problema():
    """Cada problema se puntúa con su propia semilla (pipeline.run_spec: semilla de la especificación × 100003 + índice),
    así que el resultado no depende del orden ni del reparto entre procesos: aquí se puntúa el mismo problema solo y
    después de otros, con la misma semilla, y debe dar lo mismo en las tres familias."""
    docs = _corpus()
    fs = FeatureSpace("mfw:30", docs, person_filter=PersonFilter(docs), closed_set=set())
    pr = build_problems(docs, core_ids=["A0", "A1", "A2", "A3"], target_ids=["A4"], n_neg_pairs=5, n_neg_epist=5)
    some = [p for p in pr if p.kind in ("pos_epist", "neg_epist")][:4]
    for fam, iters in (("impostores", 6), ("dirichlet", 6), ("ncd", 3)):
        eng = make_engine(docs, Spec(features="mfw:30", metric="minmax", window=300, iters=iters, n_impostors=5,
                                     family=fam), fs)
        solo = eng.score(some[0], np.random.default_rng(12345), return_detail=True)
        for q in some[1:]:
            eng.score(q, np.random.default_rng(99))
        otra_vez = eng.score(some[0], np.random.default_rng(12345), return_detail=True)
        assert solo == otra_vez, fam

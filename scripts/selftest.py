#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py — pruebas de referencia de paulinum.

Comprueba, con datos sintéticos y deterministas, que la normalización, las distancias, la calibración,
la PERMANOVA y el motor de impostores producen los valores esperados, y que la capa de trece lemas de
la Investigación 1 reproduce dígito a dígito las tablas del libro (313 valores). Al final imprime una
huella SHA-256 del conjunto de resultados numéricos: dos instalaciones con las mismas versiones de las
bibliotecas deben producir la misma huella («resultados idénticos bit a bit en las pruebas de referencia»,
§ 8.3). Devuelve código 0 si todo pasa.

Uso: python scripts/selftest.py  (o python -m paulinum selftest)
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from paulinum.text import normalize_form, strip_diacritics, beta_to_unicode, tokenize  # noqa: E402
from paulinum.distances import delta, minmax, cosine, labbe, Standardizer  # noqa: E402
from paulinum.verify import auc, c_at_1, best_band, LRCalibrator, verbal, GIEngine, Spec, Problem  # noqa: E402
from paulinum.variables import permanova, pcoa, percentile_of  # noqa: E402
from paulinum.corpus import Document  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter  # noqa: E402

RESULTS = {}
FAILS = []
N_CHECKS = 0


def check(name, cond, detail=""):
    global N_CHECKS
    N_CHECKS += 1
    RESULTS[name] = bool(cond)
    if not cond:
        FAILS.append(f"{name} {detail}")
    print(("  ok   " if cond else "  FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))


def main() -> int:
    print("paulinum selftest")
    # 1. normalización
    check("norm.sigma_final", normalize_form("λόγος") == "λόγοσ")
    check("norm.grave_agudo", normalize_form("τὸν") == "τόν")
    check("norm.minusculas", normalize_form("Παῦλος") == "παῦλοσ")
    check("norm.no_griego", normalize_form("Paulus") == "" and normalize_form("123") == "")
    check("norm.nodia", strip_diacritics("ἀγάπη") == "αγαπη")
    check("norm.elision", normalize_form("δι’") == "δι’")
    check("norm.tokenize", tokenize("ὁ λόγος, καὶ· τὸ φῶς.") == ["ὁ", "λόγος", "καὶ", "τὸ", "φῶς"])
    # 2. Beta Code
    check("beta.logos", beta_to_unicode("lo/gos") == "λόγος")
    check("beta.mayuscula", beta_to_unicode("*)ihsou=s") == "Ἰησοῦς")
    check("beta.iota_suscrita", beta_to_unicode("tw=|") == "τῷ")
    # 3. distancias
    a = np.array([[0.2, 0.3, 0.5]])
    b = np.array([[0.1, 0.4, 0.5]])
    check("dist.minmax", abs(minmax(a, b)[0] - (1 - 0.9 / 1.1)) < 1e-9, str(minmax(a, b)[0]))
    ref = np.array([[0.2, 0.3, 0.5], [0.1, 0.4, 0.5], [0.3, 0.3, 0.4]])
    st = Standardizer(ref)
    za, zb = st.z(a), st.z(b)
    check("dist.delta", abs(delta(za, zb)[0] - np.abs(za - zb).mean()) < 1e-12)
    check("dist.cosine_identico", abs(cosine(za, za)[0]) < 1e-9)
    check("dist.labbe_identico", abs(labbe(np.array([[3, 4, 5]]), np.array([[3, 4, 5]]))[0]) < 1e-12)
    RESULTS["dist.values"] = [float(minmax(a, b)[0]), float(delta(za, zb)[0])]
    # 4. calibración
    pos = np.array([0.9, 0.8, 0.7, 0.6, 0.55])
    neg = np.array([0.1, 0.2, 0.3, 0.65, 0.4])
    check("cal.auc", abs(auc(pos, neg) - 0.92) < 1e-12, str(auc(pos, neg)))
    check("cal.c@1_sin_banda", abs(c_at_1(pos, neg, 0.5, 0.5) - 0.9) < 1e-12)
    lo, hi, c1 = best_band(pos, neg)
    check("cal.banda", c1 >= 0.9, f"{lo} {hi} {c1}")
    cal = LRCalibrator(np.concatenate([pos, pos + 0.01]), np.concatenate([neg, neg + 0.01]))
    check("cal.lr_signo", cal.log10lr(0.85) > 0 > cal.log10lr(0.15))
    check("cal.verbal", verbal(0.2) == "no discriminante" and verbal(0.5).startswith("apoyo débil")
          and verbal(-1.5).startswith("apoyo moderado"))
    RESULTS["cal.values"] = [auc(pos, neg), lo, hi, round(cal.log10lr(0.85), 6)]
    # 5. PERMANOVA sobre grupos separables
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal(0, 1, (10, 3)), rng.normal(3, 1, (10, 3))])
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    r = permanova(D, [0] * 10 + [1] * 10, permutations=199, seed=1)
    check("permanova.separable", r["R2"] > 0.5 and r["p"] <= 0.01, str(r))
    r0 = permanova(D, list(range(20)) if False else [0, 1] * 10, permutations=199, seed=1)
    check("permanova.nulo", r0["p"] > 0.05, str(r0))
    coords, vals = pcoa(D)
    check("pcoa.dim", coords.shape[0] == 20 and vals[0] > vals[1])
    check("percentil", abs(percentile_of(2.0, np.array([1.0, 2.0, 3.0, 4.0])) - 0.375) < 1e-12)
    RESULTS["permanova.R2"] = round(r["R2"], 6)
    # 6. motor de impostores sobre un corpus sintético: dos «autores» con vocabulario sesgado
    def synth(doc_id, author, bias, n=1500, seed=0):
        g = np.random.default_rng(seed)
        vocab = [f"τ{i}" for i in range(40)]
        p = np.ones(40)
        p[:20] *= bias
        p /= p.sum()
        forms = [vocab[i] for i in g.choice(40, size=n, p=p)]
        return Document(id=doc_id, author=author, work=doc_id, status="genuine", tradition="x", edition_key="t",
                        forms=forms, forms_nodia=forms, lemmas=[""] * n, pos=[""] * n, person=[""] * n,
                        mood=[""] * n, refs=["1:1"] * n, masks={}, work_group="")
    docs = [synth(f"A{i}", "A", 3.0, seed=i) for i in range(4)] + [synth(f"B{i}", "B", 1 / 3.0, seed=10 + i) for i in range(4)] \
        + [synth(f"C{i}", "C", 1.0, seed=20 + i) for i in range(6)]
    fs = FeatureSpace("mfw:40", docs, person_filter=PersonFilter(docs), closed_set=set())
    spec = Spec(features="mfw:40", metric="minmax", window=500, iters=40, n_impostors=5, seed=5)
    eng = GIEngine(docs, spec, fs, min_tokens=100)
    g = np.random.default_rng(spec.seed)
    same = eng.score(Problem("p", "pos_pairs", "A0", ["A1", "A2", "A3"], exclude=[], label=1, author="A"), g)["score"]
    other = eng.score(Problem("n", "neg_pairs", "B0", ["A1", "A2", "A3"], exclude=[], label=0, author="B"), g)["score"]
    check("gi.separa", same > 0.8 and other < 0.2, f"{same} {other}")
    RESULTS["gi.values"] = [same, other]
    # 7. capa de trece lemas (Investigación 1): cotejo íntegro con el libro
    cot = os.path.join(ROOT, "investigacion_1", "capa_13_lemas", "cotejo_con_el_libro.py")
    if os.path.exists(cot):
        out = subprocess.run([sys.executable, cot], capture_output=True, text=True, cwd=os.path.dirname(cot))
        first = out.stdout.strip().splitlines()[0] if out.stdout.strip() else out.stderr[-200:]
        check("capa13.cotejo_313", first.startswith("313/313"), first)
        RESULTS["capa13"] = first
    h = hashlib.sha256(json.dumps(RESULTS, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    print(f"\n{N_CHECKS - len(FAILS)} comprobaciones superadas, {len(FAILS)} fallidas")
    print(f"huella de referencia: {h}")
    if FAILS:
        for f in FAILS:
            print("  -", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

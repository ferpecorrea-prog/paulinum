# -*- coding: utf-8 -*-
"""pytest: codificación uniforme entre corpus y calibración (versión 1.1.0). Sin red ni datos descargados."""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from paulinum import parsers  # noqa: E402
from paulinum.corpus import Document  # noqa: E402
from paulinum.features import learn_closed_class, learn_person_verb_forms, morphgnt_pos  # noqa: E402
from paulinum.text import normalize_form  # noqa: E402
from paulinum.verify import LRCalibrator  # noqa: E402


def test_elision_uniforme_con_coronis_y_psili():
    # U+2019, U+02BC, U+0027, U+1FBD (koronis) y U+1FBF (psili) dan la misma forma
    for f in ("δ’", "δʼ", "δ'", "δ᾽", "δ᾿"):
        assert normalize_form(f) == "δ’", f
    assert normalize_form("ἀλλ᾿", keep_diacritics=False) == "αλλ’"




def test_morphgnt_columna_word_conserva_la_forma_del_texto(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("060105 P- -------- δι’ δι’ διά διά\n"
                 "060106 D- -------- οὐκ οὐκ οὐ οὐ\n"
                 "060107 V- 3PAI-S-- ἐστιν ἐστιν ἐστίν εἰμί\n", encoding="utf-8")
    assert [t["form"] for t in parsers.parse_morphgnt(str(p))[0]["tokens"]] == ["δι’", "οὐκ", "ἐστιν"]
    assert [t["form"] for t in parsers.parse_morphgnt(str(p), "normalized")[0]["tokens"]] == ["διά", "οὐ", "ἐστίν"]


def _doc(forms, pos, person):
    n = len(forms)
    return Document(id="x", author="a", work="w", status="other", tradition="t", edition_key="e", forms=forms,
                    forms_nodia=forms, lemmas=[""] * n, pos=pos, person=person, mood=[""] * n, refs=[""] * n)


def test_etiquetas_proiel_y_macula_equivalen_a_morphgnt():
    assert morphgnt_pos("V-") == morphgnt_pos("verb") == morphgnt_pos("V") == "V"
    assert morphgnt_pos("S-") == morphgnt_pos("det") == "RA"
    proiel = _doc(["ὁ", "καί", "λέγω", "λέγει"], ["S-", "C-", "V-", "V-"], ["", "", "1", "3"])
    macula = _doc(["ὁ", "καί", "λέγω", "λέγει"], ["det", "conj", "verb", "verb"], ["", "", "1", "3"])
    for d in (proiel, macula):
        assert learn_closed_class([d]) == {"ὁ", "καί"}
        assert learn_person_verb_forms([d]) == {"λέγω"}


def test_lr_ancho_de_banda_sobre_la_muestra_original():
    rng = np.random.default_rng(1)
    pos = np.clip(rng.normal(0.9, 0.05, 300), 0, 1)
    neg = np.clip(rng.normal(0.1, 0.05, 300), 0, 1)
    cal = LRCalibrator(pos, neg)
    bw = cal.kp.factor * pos.std(ddof=1)
    assert bw < 0.05                       # con la muestra reflejada salía ~0,2
    assert cal.log10lr(0.95) > 2 > -2 > cal.log10lr(0.05)   # distribuciones separadas → LR fuertes

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anotacion_diagnostico.py — DIAGNÓSTICO (carpeta diagnostico/, fuera del conjunto sellado: no forma parte del código sellado ni de ninguna etapa del protocolo).

La validación sellada (`scripts/anotacion_uniforme.py`) dio con OdyCy `grc_odycy_joint_sm` un acuerdo con MorphGNT de
0,148 (categoría) y 0,487 (lema), muy por debajo de la exactitud publicada del modelo. Este guion mide el acuerdo de
nuevo separando las causas posibles, sin cambiar ningún resultado sellado:

  V0 · método sellado (texto unido por espacios en lotes de 2000 y alineación por posición);
  V1 · tokenización forzada (`Doc(vocab, words=formas)`), alineación garantizada uno a uno;
  V2 · V1 + sigma final restaurada («σ» final → «ς») antes de anotar, comparación de lemas insensible a σ/ς;
  V3 · V2 + comparación de categorías con una tabla de equivalencias UPOS (CCONJ/SCONJ, PART/ADV, PROPN/NOUN, etc.).

Escribe results/anotacion/diagnostico_<modelo>.json y diagnostico_<modelo>_confusion.csv (matriz de confusión
MorphGNT→UPOS × UPOS del modelo, para la variante V2). Uso:
  python diagnostico/anotacion_diagnostico.py --modelo grc_odycy_joint_sm --edicion sblgnt
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.text import strip_diacritics  # noqa: E402

MORPHGNT_TO_UPOS = {"N-": "NOUN", "V-": "VERB", "A-": "ADJ", "RA": "DET", "C-": "CCONJ", "P-": "ADP", "D-": "ADV",
                    "RP": "PRON", "RD": "PRON", "RR": "PRON", "RI": "PRON", "RE": "PRON", "X-": "PART", "I-": "INTJ",
                    "M-": "NUM"}
# equivalencias admitidas en V3 (diferencias de convención entre tagsets, no errores de análisis)
EQUIV = {("CCONJ", "SCONJ"), ("SCONJ", "CCONJ"), ("PART", "ADV"), ("ADV", "PART"), ("NOUN", "PROPN"), ("PROPN", "NOUN"),
         ("VERB", "AUX"), ("AUX", "VERB"), ("ADJ", "NUM"), ("NUM", "ADJ"), ("DET", "PRON"), ("PRON", "DET"),
         ("ADJ", "DET"), ("DET", "ADJ")}


def sigma_final(f: str) -> str:
    return f[:-1] + "ς" if f.endswith("σ") else f


def lema_norm(s: str) -> str:
    return strip_diacritics(s.lower()).replace("ς", "σ")


def anotar_v0(nlp, forms, batch=2000):
    pos, lem = [], []
    for i in range(0, len(forms), batch):
        chunk = forms[i:i + batch]
        doc = nlp(" ".join(chunk))
        toks = [t for t in doc if not t.is_space]
        got_p, got_l = [t.pos_ for t in toks], [t.lemma_ for t in toks]
        got_p = (got_p + [""] * len(chunk))[:len(chunk)]
        got_l = (got_l + [""] * len(chunk))[:len(chunk)]
        pos.extend(got_p)
        lem.extend(got_l)
    return pos, lem


def anotar_forzado(nlp, forms, batch=2000):
    from spacy.tokens import Doc
    pos, lem = [], []
    for i in range(0, len(forms), batch):
        chunk = forms[i:i + batch]
        doc = Doc(nlp.vocab, words=chunk)
        for _name, proc in nlp.pipeline:
            doc = proc(doc)
        pos.extend(t.pos_ for t in doc)
        lem.extend(t.lemma_ for t in doc)
    return pos, lem


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="grc_odycy_joint_sm")
    ap.add_argument("--edicion", default="sblgnt")
    a = ap.parse_args()
    import spacy
    nlp = spacy.load(a.modelo)
    meta = nlp.meta
    docs = load_corpus(a.edicion)
    nt = [d for d in docs if d.source_id and d.pos and any(d.pos)]
    out_dir = os.path.join("results", "anotacion")
    os.makedirs(out_dir, exist_ok=True)
    res = {"modelo": a.modelo, "version_modelo": meta.get("version"), "spacy": spacy.__version__,
           "pipeline": nlp.pipe_names, "obras_nt": len(nt), "variantes": {}}
    conf = Counter()
    t0 = time.time()
    variantes = {"V0_sellado": ("v0", False, False), "V1_forzado": ("v1", False, False),
                 "V2_forzado_sigma": ("v1", True, False), "V3_forzado_sigma_equiv": ("v1", True, True)}
    por_obra = {k: [] for k in variantes}
    for nombre, (metodo, sigma, equiv) in variantes.items():
        n = okp = okl = 0
        for d in nt:
            forms = [sigma_final(f) for f in d.forms] if sigma else list(d.forms)
            pos, lem = anotar_v0(nlp, forms) if metodo == "v0" else anotar_forzado(nlp, forms)
            n_d = okp_d = okl_d = 0
            for p_manual, l_manual, p_auto, l_auto in zip(d.pos, d.lemmas, pos, lem):
                if not p_manual:
                    continue
                n_d += 1
                pm = MORPHGNT_TO_UPOS.get(p_manual[:2], p_manual)
                ok = pm == p_auto or (equiv and (pm, p_auto) in EQUIV)
                okp_d += int(ok)
                if nombre == "V2_forzado_sigma":
                    conf[(pm, p_auto)] += 1
                if l_manual and l_auto:
                    okl_d += int(lema_norm(l_manual) == lema_norm(l_auto) if sigma else
                                 strip_diacritics(l_manual) == strip_diacritics(l_auto.lower()))
            por_obra[nombre].append({"id": d.id, "tokens": n_d, "acuerdo_pos": okp_d / n_d if n_d else None,
                                     "acuerdo_lema": okl_d / n_d if n_d else None})
            n += n_d
            okp += okp_d
            okl += okl_d
        res["variantes"][nombre] = {"tokens": n, "acuerdo_pos": okp / n if n else None, "acuerdo_lema": okl / n if n else None}
        print(f"{nombre}: categoría {okp / n:.3f} · lema {okl / n:.3f}")
    res["segundos"] = round(time.time() - t0)
    res["por_obra"] = por_obra
    with open(os.path.join(out_dir, f"diagnostico_{a.modelo}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    filas = sorted(conf.items(), key=lambda kv: -kv[1])
    with open(os.path.join(out_dir, f"diagnostico_{a.modelo}_confusion.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["morphgnt_upos", "modelo_upos", "n"])
        for (pm, pa), c in filas:
            w.writerow([pm, pa, c])
    print("diagnóstico →", out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

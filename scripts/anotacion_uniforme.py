#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anotacion_uniforme.py — anotación morfosintáctica UNIFORME de todo el corpus (PROTOCOLO § 5.3) y su validación.

1. Anota las 27 obras del NT con un analizador uniforme (greCy, modelo `grc_proiel_sm` u otro de spaCy para griego
   antiguo; se instala desde Hugging Face solo si el entorno lo alcanza) y mide su acuerdo con la anotación manual de
   MorphGNT (lema y categoría gramatical, token a token). Umbral fijado antes: exactitud de lema >= 0,95 y de categoría
   >= 0,95 sobre el NT. Escribe results/anotacion/acuerdo_nt.csv y acuerdo_nt.json.
2. Si se alcanza el umbral, anota TODOS los documentos del corpus construido (data/cache/corpus_<edición>.jsonl) y
   guarda la capa `pos_uniforme` (una etiqueta por token, alineada con `forms`) en data/cache/pos_uniforme_<edición>.jsonl.
   El espacio `pos3:N` de la sensibilidad la lee de ahí. Si no se alcanza, no escribe la capa y lo dice: el espacio
   pos3 queda descartado y el informe publica el acuerdo obtenido.
La anotación manual de MorphGNT nunca se usa como rasgo (solo el NT la tiene).

Uso: python scripts/anotacion_uniforme.py [--modelo grc_proiel_sm] [--edicion sblgnt] [--solo-validar]
"""
from __future__ import annotations

import argparse
import gzip
import importlib
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.pipeline import _write_csv  # noqa: E402
from paulinum.text import strip_diacritics  # noqa: E402

UMBRAL_LEMA = 0.95
UMBRAL_POS = 0.95
# Correspondencia MorphGNT (categoría de la primera columna) → etiqueta universal (UPOS) que produce spaCy
MORPHGNT_TO_UPOS = {"N-": "NOUN", "V-": "VERB", "A-": "ADJ", "RA": "DET", "C-": "CCONJ", "P-": "ADP", "D-": "ADV",
                    "RP": "PRON", "RD": "PRON", "RR": "PRON", "RI": "PRON", "RE": "PRON", "X-": "PART", "I-": "INTJ",
                    "M-": "NUM"}


def load_model(name: str):
    try:
        spacy = importlib.import_module("spacy")
    except ImportError:
        return None, "spaCy no está instalado (pip install grecy spacy)"
    try:
        return spacy.load(name), ""
    except Exception:
        pass
    # instalación del modelo con greCy (solo alcanza si huggingface.co es accesible)
    try:
        subprocess.run([sys.executable, "-m", "grecy", "install", name], check=True, timeout=1800,
                       capture_output=True, text=True)
        return spacy.load(name), ""
    except Exception as e:  # pragma: no cover
        return None, f"no se pudo instalar/cargar el modelo {name}: {type(e).__name__}: {str(e)[:200]}"


def annotate(nlp, forms: list[str], batch: int = 2000) -> tuple[list[str], list[str]]:
    """Etiqueta (UPOS) y lema de cada forma; el texto se pasa token a token con espacios (sin puntuación)."""
    pos, lem = [], []
    for i in range(0, len(forms), batch):
        chunk = forms[i:i + batch]
        doc = nlp(" ".join(chunk))
        toks = [t for t in doc if not t.is_space]
        if len(toks) != len(chunk):   # el tokenizador dividió o unió: alinear por posición aproximada
            got_p, got_l = [t.pos_ for t in toks], [t.lemma_ for t in toks]
            got_p = (got_p + [""] * len(chunk))[:len(chunk)]
            got_l = (got_l + [""] * len(chunk))[:len(chunk)]
        else:
            got_p, got_l = [t.pos_ for t in toks], [t.lemma_ for t in toks]
        pos.extend(got_p)
        lem.extend(got_l)
    return pos, lem


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="grc_proiel_sm")
    ap.add_argument("--edicion", default="sblgnt")
    ap.add_argument("--solo-validar", action="store_true")
    a = ap.parse_args()
    out_dir = os.path.join("results", "anotacion")
    os.makedirs(out_dir, exist_ok=True)
    nlp, err = load_model(a.modelo)
    if nlp is None:
        res = {"modelo": a.modelo, "disponible": False, "motivo": err, "apto": False}
        json.dump(res, open(os.path.join(out_dir, "acuerdo_nt.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("anotación uniforme NO disponible:", err)
        return 0
    docs = load_corpus(a.edicion)
    nt = [d for d in docs if d.source_id and d.pos and any(d.pos)]
    rows, tot_l = [], [0, 0, 0]
    t0 = time.time()
    for d in nt:
        pos, lem = annotate(nlp, d.forms)
        n = 0
        ok_p = ok_l = 0
        for f, p_manual, l_manual, p_auto, l_auto in zip(d.forms, d.pos, d.lemmas, pos, lem):
            if not p_manual:
                continue
            n += 1
            ok_p += int(MORPHGNT_TO_UPOS.get(p_manual[:2], p_manual) == p_auto)
            ok_l += int(strip_diacritics(l_manual) == strip_diacritics(l_auto.lower()) if l_manual and l_auto else False)
        rows.append({"id": d.id, "tokens": n, "acuerdo_pos": ok_p / n if n else float("nan"),
                     "acuerdo_lema": ok_l / n if n else float("nan")})
        tot_l[0] += n
        tot_l[1] += ok_p
        tot_l[2] += ok_l
    acc_p = tot_l[1] / tot_l[0] if tot_l[0] else float("nan")
    acc_l = tot_l[2] / tot_l[0] if tot_l[0] else float("nan")
    apto = bool(acc_p >= UMBRAL_POS and acc_l >= UMBRAL_LEMA)
    _write_csv(os.path.join(out_dir, "acuerdo_nt.csv"), rows)
    res = {"modelo": a.modelo, "disponible": True, "tokens_nt": tot_l[0], "acuerdo_pos": acc_p, "acuerdo_lema": acc_l,
           "umbral_pos": UMBRAL_POS, "umbral_lema": UMBRAL_LEMA, "apto": apto, "segundos": round(time.time() - t0)}
    json.dump(res, open(os.path.join(out_dir, "acuerdo_nt.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"acuerdo con MorphGNT: categoría {acc_p:.3f}, lema {acc_l:.3f} → {'APTO' if apto else 'NO APTO'}")
    if not apto or a.solo_validar:
        return 0
    out = os.path.join("data", "cache", f"pos_uniforme_{a.edicion}.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        for i, d in enumerate(docs):
            pos, _ = annotate(nlp, d.forms)
            f.write(json.dumps({"id": d.id, "pos_uniforme": pos}, ensure_ascii=False) + "\n")
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{len(docs)} documentos anotados")
    print("capa pos_uniforme →", out)
    # copia comprimida publicable (solo etiquetas, no texto): la lee pipeline.Context.corpus si falta la de data/cache
    pub = os.path.join(out_dir, f"pos_uniforme_{a.edicion}.jsonl.gz")
    with open(out, "rb") as f, gzip.open(pub, "wb") as g:
        shutil.copyfileobj(f, g)
    print("copia comprimida →", pub)
    return 0


if __name__ == "__main__":
    sys.exit(main())

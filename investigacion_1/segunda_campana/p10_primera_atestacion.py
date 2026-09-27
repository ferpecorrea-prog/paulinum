#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P10 — primera atestación datable del léxico exclusivo de cada carta en el corpus Diorisis
(Investigación 1, § 4.5 «Sexto»; apéndice, apartado décimo).

Definición (nota 50): léxico exclusivo de una carta = lemas (MorphGNT) que no aparecen en ninguna otra de
las trece cartas paulinas. Para cada lema se busca en Diorisis la obra más antigua que lo contiene y se toma
la fecha convencional del autor o corpus (floruit) que trae la cabecera de Diorisis; la coincidencia exacta
se intenta primero con diacríticos y, si falla, sin ellos (limitación declarada en la nota 50). Resultado
principal: proporción de lexemas exclusivos con fecha asignada ≤ 50 por carta y por bloque (Pastorales
frente a indiscutidas), con prueba exacta de Fisher; secundario: lexemas con fecha > 100.

Publicado (P10 histórico): Rom 0,83; 1Cor 0,81; 2Tes 0,81; 2Cor 0,77; Col 0,77; 2Tim 0,77; Gal 0,76;
Ef 0,75; Tit 0,71; Flp 0,70; 1Tim 0,66; 1Tes 0,59; Pastorales 176/251 = 0,70 frente a indiscutidas
656/834 = 0,79, p = 0,0064; > 100: 6,4 % frente a 2,5 % (p = 0,005). La validación externa posterior
P10-R(sym-ext) (117 testimonios validados a mano por el autor) no puede reconstruirse desde el código:
sus resultados agregados están en results_publicados/investigacion_1/p10_validacion_externa.csv.

Requiere Diorisis.zip (no redistribuible): python p10_primera_atestacion.py --diorisis-zip <ruta>
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import zipfile
from collections import defaultdict

import pandas as pd
from lxml import etree
from scipy.stats import fisher_exact

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylolib import ROOT  # noqa: E402
from paulinum.corpus import load_corpus  # noqa: E402
from paulinum.text import beta_to_unicode, normalize_form, strip_diacritics  # noqa: E402

LETTERS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit"]
PASTORALES = ["1Tim", "2Tim", "Tit"]
INDISCUTIDAS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm"]


def parse_date(text: str) -> float | None:
    """Fecha convencional de la cabecera de Diorisis (p. ej. '-400', '50', '-20/50' → extremo final)."""
    if not text:
        return None
    nums = re.findall(r"-?\d+", text)
    if not nums:
        return None
    return float(nums[-1])


def diorisis_index(zip_path: str) -> dict[str, float]:
    """lema (Unicode, con diacríticos) → fecha más antigua de una obra que lo contiene."""
    first = {}
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".xml")]
        for k, n in enumerate(names, 1):
            data = z.read(n)
            root = etree.fromstring(data, etree.XMLParser(recover=True, huge_tree=True))
            date = None
            for el in root.iter():
                tag = el.tag.split("}")[-1] if isinstance(el.tag, str) else ""
                if tag == "date":
                    date = parse_date("".join(el.itertext()))
                    break
            if date is None:
                continue
            seen = set()
            for w in root.iter("word"):
                for ch in w:
                    if ch.tag == "lemma" and ch.get("entry"):
                        seen.add(normalize_form(beta_to_unicode(ch.get("entry"))))
            for l in seen:
                if l and (l not in first or date < first[l]):
                    first[l] = date
            if k % 50 == 0:
                print(f"  {k}/{len(names)} obras; {len(first)} lemas fechados")
    return first


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diorisis-zip", required=True)
    ap.add_argument("--umbral", type=float, default=50)
    a = ap.parse_args()
    docs = {d.id: d for d in load_corpus("sblgnt", os.path.join(ROOT, "data"))}
    lemmas_by = {L: set(normalize_form(l) for l in docs[L].lemmas if l) for L in LETTERS}
    exclusive = {L: sorted(lemmas_by[L] - set().union(*[lemmas_by[o] for o in LETTERS if o != L])) for L in LETTERS}
    print("léxico exclusivo:", {L: len(v) for L, v in exclusive.items()})
    idx = diorisis_index(a.diorisis_zip)
    idx_nodia = defaultdict(lambda: float("inf"))
    for l, d in idx.items():
        k = strip_diacritics(l)
        idx_nodia[k] = min(idx_nodia[k], d)
    rows = []
    for L in LETTERS:
        for lem in exclusive[L]:
            d = idx.get(lem)
            modo = "exacta"
            if d is None:
                d2 = idx_nodia.get(strip_diacritics(lem))
                if d2 is not None and d2 != float("inf"):
                    d, modo = d2, "sin_diacriticos"
            rows.append({"carta": L, "lema": lem, "fecha_primera_atestacion": d, "coincidencia": modo if d is not None else "sin_fecha",
                         "le_50": (d is not None and d <= a.umbral), "gt_100": (d is not None and d > 100)})
    df = pd.DataFrame(rows)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, "p10_detalle.csv"), index=False)
    res = df.groupby("carta").agg(n=("lema", "count"), le_50=("le_50", "sum"), gt_100=("gt_100", "sum"))
    res["prop_le_50"] = res["le_50"] / res["n"]
    print(res.loc[LETTERS].round(3).to_string())
    p = df[df.carta.isin(PASTORALES)]
    i = df[df.carta.isin(INDISCUTIDAS)]
    tab = [[int(p.le_50.sum()), int((~p.le_50).sum())], [int(i.le_50.sum()), int((~i.le_50).sum())]]
    print(f"Pastorales {tab[0][0]}/{len(p)} = {tab[0][0] / len(p):.3f}; indiscutidas {tab[1][0]}/{len(i)} = {tab[1][0] / len(i):.3f}; "
          f"Fisher p = {fisher_exact(tab)[1]:.4f}")
    tab2 = [[int(p.gt_100.sum()), len(p) - int(p.gt_100.sum())], [int(i.gt_100.sum()), len(i) - int(i.gt_100.sum())]]
    print(f"> 100: Pastorales {tab2[0][0]}/{len(p)}; indiscutidas {tab2[1][0]}/{len(i)}; Fisher p = {fisher_exact(tab2)[1]:.4f}")
    res.to_csv(os.path.join(out_dir, "p10_resumen.csv"), float_format="%.3f")
    return 0


if __name__ == "__main__":
    sys.exit(main())

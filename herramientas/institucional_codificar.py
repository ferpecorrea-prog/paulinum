#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
institucional_codificar.py — aplica la codificación manual (institucional_datos.py) a las apariciones extraídas
(results/canales/institucional_apariciones.csv), asigna el paralelo externo (§ 4, § 6 del libro de códigos) y escribe:

  results/canales/institucional.csv          una fila por aparición (§ 3 del libro de códigos)
  results/canales/institucional_resumen.csv  una fila por documento (§ 5): n_cargos, n_rasgos, fecha_compatible…
  results/canales/institucional_lectura.csv  las catorce cartas × H1-H5 (§ 6.4)

Toda aparición debe tener código explícito: el guion se detiene si falta alguno (no hay codificación por defecto).
"""
from __future__ import annotations

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from institucional_datos import CODIGOS, PARALELOS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APAR = os.path.join(ROOT, "results", "canales", "institucional_apariciones.csv")
OUT = os.path.join(ROOT, "results", "canales", "institucional.csv")
RES = os.path.join(ROOT, "results", "canales", "institucional_resumen.csv")
LECT = os.path.join(ROOT, "results", "canales", "institucional_lectura.csv")
LETTERS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb"]
COMPARACION = ["Hch", "1Clem", "Did", "IgnEf", "IgnMagn", "IgnTral", "IgnRom", "IgnFil", "IgnEsm", "IgnPol", "PolFil", "Herm"]
DATAN = {"cargo", "categoria", "rito"}
ORDEN = {"s1": 1, "fin_s1": 2, "s2": 3}
ESTADO = {"Rom": "core", "1Cor": "core", "2Cor": "core", "Gal": "core", "Flp": "core", "1Tes": "core", "Flm": "core",
          "Ef": "target", "Col": "target", "2Tes": "target", "1Tim": "target", "2Tim": "target", "Tit": "target", "Heb": "target"}


def paralelo_fila(termino: str, uso: str, rasgos: list[str]):
    """Fase, origen, fuente y cita de una fila que data: la más tardía entre el término y sus rasgos."""
    if uso not in DATAN:
        return "no_aplica", "", "", ""
    key = (termino, uso)
    if key not in PARALELOS:
        return "sin_paralelo", "", "", f"sin entrada en PARALELOS para {key}"
    cands = [PARALELOS[key]] + [PARALELOS[("rasgo", r)] for r in rasgos if r]
    fase, origen, fuente, cita = max(cands, key=lambda c: ORDEN[c[0]])
    # fuente: se listan todas las consultadas (término y rasgos), la que fija la fecha primero
    fuentes = [fuente] + [c[2] for c in cands if c[2] != fuente]
    return fase, origen, " || ".join(dict.fromkeys(fuentes)), cita


def main() -> int:
    rows = list(csv.DictReader(open(APAR, encoding="utf-8")))
    out, faltan = [], []
    for r in rows:
        k4 = (r["documento"], r["ref"], r["termino"], r["forma"])
        k3 = (r["documento"], r["ref"], r["termino"])
        cod = CODIGOS.get(k4) or CODIGOS.get(k3)
        if cod is None:
            faltan.append(k4); continue
        uso, rasgos, juicio, nota = cod
        rl = [x for x in rasgos.split(";") if x]
        fase, origen, fuente, cita = paralelo_fila(r["termino"], uso, rl)
        out.append({"documento": r["documento"], "termino": r["termino"], "pasaje": r["ref"], "forma": r["forma"], "uso": uso,
                    "rasgos": ";".join(rl), "paralelo_epigrafico": fase, "origen_fecha": origen, "fuente": fuente, "cita": cita,
                    "juicio": juicio, "nota": nota, "contexto": r["contexto"]})
    if faltan:
        print("SIN CÓDIGO:", len(faltan)); [print("  ", k) for k in faltan]; return 1
    cols = ["documento", "termino", "pasaje", "forma", "uso", "rasgos", "paralelo_epigrafico", "origen_fecha", "fuente", "cita", "juicio", "nota", "contexto"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\r\n"); w.writeheader(); w.writerows(out)

    # resumen por documento (§ 5, § 6.1-6.2), con todas las filas y sin las filas juicio=sí
    def resumen(doc, filas):
        d = {"documento": doc, "grupo": ESTADO.get(doc, "comparacion"), "n_apariciones": len(filas)}
        for suf, sub in (("", filas), ("_sin_juicio", [x for x in filas if x["juicio"] != "sí"])):
            datan = [x for x in sub if x["uso"] in DATAN]
            cargos = [x for x in sub if x["uso"] == "cargo"]
            rasgos = sorted({r for x in datan for r in x["rasgos"].split(";") if r})
            fases = [x for x in datan if x["paralelo_epigrafico"] in ORDEN]
            top = max(fases, key=lambda x: ORDEN[x["paralelo_epigrafico"]]) if fases else None
            d[f"n_institucional{suf}"] = len(datan)
            d[f"n_cargos{suf}"] = len(cargos)
            d[f"terminos_cargo{suf}"] = ";".join(sorted({x["termino"] for x in cargos}))
            d[f"n_rasgos{suf}"] = len(rasgos)
            d[f"rasgos{suf}"] = ";".join(rasgos)
            d[f"fecha_compatible{suf}"] = top["paralelo_epigrafico"] if top else ""
            d[f"origen_fecha{suf}"] = top["origen_fecha"] if top else ""
            d[f"fija_fecha{suf}"] = ";".join(sorted({f"{x['termino']} {x['pasaje']}" for x in fases if x["paralelo_epigrafico"] == top["paralelo_epigrafico"]})) if top else ""
        return d
    docs = [d for d in LETTERS + COMPARACION]
    res = [resumen(doc, [x for x in out if x["documento"] == doc]) for doc in docs]
    rcols = list(res[0].keys())
    with open(RES, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rcols, lineterminator="\r\n"); w.writeheader(); w.writerows(res)

    # lectura § 6.4
    def lectura(fase, origen):
        if not fase:
            return "no decide", "no decide", "no decide"
        if fase == "s1":
            return "compatible", "compatible", "no decide"
        if fase == "fin_s1":
            return ("no compatible" if origen == "asociaciones" else "no decide"), "compatible", "no decide"
        return "no compatible", "no decide", "compatible"
    lect = []
    for d in res:
        if d["documento"] not in LETTERS:
            continue
        e = {"carta": d["documento"], "kind": d["grupo"], "n_institucional": d["n_institucional"], "n_cargos": d["n_cargos"],
             "n_rasgos": d["n_rasgos"], "fecha_compatible": d["fecha_compatible"], "origen_fecha": d["origen_fecha"], "fija_fecha": d["fija_fecha"]}
        e["H1_H3"], e["H4"], e["H5"] = lectura(d["fecha_compatible"], d["origen_fecha"])
        e["fecha_compatible_sin_juicio"] = d["fecha_compatible_sin_juicio"]
        e["H1_H3_sin_juicio"], e["H4_sin_juicio"], e["H5_sin_juicio"] = lectura(d["fecha_compatible_sin_juicio"], d["origen_fecha_sin_juicio"])
        e["lectura"] = f"H1-H3 {e['H1_H3']}; H4 {e['H4']}; H5 {e['H5']}"
        lect.append(e)
    with open(LECT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lect[0].keys()), lineterminator="\r\n"); w.writeheader(); w.writerows(lect)

    from collections import Counter
    print(OUT, len(out), Counter(x["uso"] for x in out))
    for d in res:
        print(f"{d['documento']:8s} inst={d['n_institucional']:3d} cargos={d['n_cargos']:3d} [{d['terminos_cargo']}] rasgos={d['rasgos']} "
              f"fecha={d['fecha_compatible'] or '—'} ({d['origen_fecha']}) ← {d['fija_fecha']} | sin juicio: {d['fecha_compatible_sin_juicio'] or '—'}")
    for e in lect:
        print(f"{e['carta']:5s} {e['lectura']} | sin juicio: H1-H3 {e['H1_H3_sin_juicio']}; H4 {e['H4_sin_juicio']}; H5 {e['H5_sin_juicio']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

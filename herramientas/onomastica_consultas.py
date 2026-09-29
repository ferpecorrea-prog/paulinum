#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
onomastica_consultas.py — vuelca las consultas externas (PHI Greek Inscriptions, D-028) en el inventario onomástico,
calcula los índices por documento y la lectura de las catorce cartas (docs/canales/codigos_onomastica.md § 2-3).

Entradas: results/canales/onomastica_inventario.csv (de onomastica_inventario.py) y results/canales/onomastica_phi.json
(recuentos de PHI por patrón, anotados a mano desde el navegador el 29-IX-2026).
Salidas: onomastica_inventario.csv (con c_region_periodo, fuente, cita), onomastica_indices.csv, onomastica_lectura.csv.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import statistics as st
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onomastica_datos_paulinas import NOMBRES  # noqa: E402
from onomastica_datos_referencia import R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, "results", "canales", "onomastica_inventario.csv")
PHI = os.path.join(ROOT, "results", "canales", "onomastica_phi.json")
LETTERS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb"]
AUTENTICAS = {"Ignacio", "1Clem", "Juliano", "Basilio", "Libanio"}
FALSAS = {"Ps-Ignacio", "Ps-Clemente", "Ps-Juliano", "Ps-Basilio", "3Cor", "HechosPablo", "Hercher"}
# nombre del remitente (o del autor supuesto) por colección: no cuenta como nombre del documento
REMITENTES = {"Ignacio": {"Ignacio"}, "Ps-Ignacio": {"Ignacio"}, "1Clem": set(), "Ps-Clemente": {"Clemente"}, "Juliano": {"Juliano"},
              "Ps-Juliano": {"Juliano"}, "Basilio": {"Basilio"}, "Ps-Basilio": {"Basilio"}, "Libanio": {"Libanio"}, "3Cor": {"Pablo"},
              "HechosPablo": set(), "paulinas": {"Pablo"},
              "Hercher": {"Fálaris", "Bruto", "Diógenes", "Crates", "Anacarsis", "Antíoco", "Artajerjes", "Temístocles", "Sócrates", "Eurípides",
                          "Quión", "Solón", "Nicias", "Mitrídates", "Aristipo", "Antístenes", "Esquines", "Jenofonte", "Simón", "Platón"}}


def escala(n: int) -> int:
    return 0 if n == 0 else 1 if n <= 5 else 2 if n <= 50 else 3


def main() -> int:
    rows = list(csv.DictReader(open(INV, encoding="utf-8")))
    phi = json.load(open(PHI, encoding="utf-8"))
    # patrón → clave de consulta: paulinas por lema, referencias por prefijo de regla
    es2lemma = {v[0]: k for k, v in NOMBRES.items()}
    for r in rows:
        if r["nuevo"] != "1":
            continue
        key = None
        if r["coleccion"] == "paulinas":
            key = es2lemma.get(r["nombre_es"])
        else:
            best = None
            for pref, es, tipo in R.get(r["coleccion"], []):
                if es == r["nombre_es"] and r["nombre"].startswith(pref) and (best is None or len(pref) > len(best)):
                    best = pref
            if best:
                key = best[0].upper() + best[1:]
                if key in ("Κράτησ", "Καστέλιοσ", "Ἑρμίασ", "Σιμμίασ", "Θάμυρισ"):
                    key = key[:-1] + "ς"
                if key == "Δαμᾶ":
                    key = "Δαμᾶς"
            if r["coleccion"] == "HechosPablo":
                key = {"Castelio": "Καστέλιος", "Falconila": "Φαλκονίλλα", "Hermias": "Ἑρμίας", "Lectra": "Λέκτρα", "Simias": "Σιμμίας",
                       "Tamiris": "Θάμυρις", "Tecla": "Θέκλα", "Teoclía": "Θεοκλεία", "Zenón": "Ζήνων"}.get(r["nombre_es"])
        if key and key in phi:
            n = phi[key]["n"]
            r["c_region_periodo"] = str(escala(n))
            r["fuente"] = "PHI Greek Inscriptions (inscriptions.packhum.org), consulta 29-IX-2026"
            r["cita"] = f"PHI: {n} apariciones del patrón «{phi[key]['patron']}» (todas las regiones, sin fecha)"
            r["juicio"] = "sí"
    cols = list(rows[0].keys())
    with open(INV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\r\n"); w.writeheader(); w.writerows(rows)
    # índices por documento
    docs = defaultdict(list)
    for r in rows:
        docs[(r["coleccion"], r["documento"], r["estado"])].append(r)
    ind = []
    for (col, doc, est), rs in sorted(docs.items()):
        rem = REMITENTES.get(col, set())
        rs2 = [r for r in rs if not (r["nombre_es"].split(" (")[0] in rem or r["funcion"] in ("remitente", "destinatario"))]
        names = {}
        for r in rs2:
            names.setdefault(r["nombre_es"], r)
        rs2 = list(names.values())
        n = len(rs2)
        def props(subset):
            m = len(subset)
            nuevos = [r for r in subset if r["nuevo"] == "1"]
            cons = [r for r in nuevos if r["c_region_periodo"] != ""]
            return {"n_nombres": m,
                    "p_nuevos": round(len(nuevos) / m, 3) if m else "",
                    "n_nuevos_consultados": len(cons),
                    "p_nuevos_documentados": round(sum(1 for r in cons if int(r["c_region_periodo"]) >= 1) / len(cons), 3) if cons else "",
                    "p_incoherencias": round(sum(1 for r in subset if r["e_coherencia"] == "incoherente") / m, 3) if m else "",
                    "p_famosos": round(sum(1 for r in subset if r["d_famoso"] == "1") / m, 3) if m else "",
                    "p_de_otras_fuentes": round(sum(1 for r in subset if r["a_otra_carta"] == "1" or r["b_hechos"] == "1") / m, 3) if m else ""}
        d = {"coleccion": col, "documento": doc, "estado": est, "grupo": "diana" if col == "paulinas" and est == "target" else
             "nucleo" if col == "paulinas" else "autenticidad" if col in AUTENTICAS else "falsificacion"}
        d.update(props(rs2))
        sj = props([r for r in rs2 if r["juicio"] != "sí"])
        d.update({f"{k}_sin_juicio": v for k, v in sj.items()})
        ind.append(d)
    icols = list(ind[0].keys())
    with open(os.path.join(ROOT, "results", "canales", "onomastica_indices.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=icols, lineterminator="\r\n"); w.writeheader(); w.writerows(ind)
    # distribuciones y percentiles
    def pct(v, dist):
        dist = [x for x in dist if x != ""]
        if v == "" or not dist:
            return ""
        return round((sum(1 for x in dist if x < v) + 0.5 * sum(1 for x in dist if x == v)) / len(dist), 3)
    aut = [d for d in ind if d["grupo"] == "autenticidad" and d["n_nombres"] >= 1]
    fal = [d for d in ind if d["grupo"] == "falsificacion" and d["n_nombres"] >= 1]
    lect = []
    for L in LETTERS:
        d = next(x for x in ind if x["coleccion"] == "paulinas" and x["documento"] == L)
        e = {"carta": L, "kind": d["estado"], "n_nombres": d["n_nombres"]}
        for k in ("p_nuevos", "p_nuevos_documentados", "p_incoherencias", "p_famosos", "p_de_otras_fuentes"):
            e[k] = d[k]
            e[f"{k}_pct_autenticidad"] = pct(d[k], [x[k] for x in aut])
            e[f"{k}_pct_falsificacion"] = pct(d[k], [x[k] for x in fal])
        # lectura § 3, por hipótesis (compatible / no compatible / no decide), con el mismo rasero que el núcleo:
        # n_nombres = 0 no es señal de H5 porque 1 Tesalonicenses (núcleo) tampoco lleva nombres fuera del prescripto.
        pn, pnd, pinc, pf = e["p_nuevos_pct_autenticidad"], e["p_nuevos_documentados_pct_autenticidad"], e["p_incoherencias_pct_autenticidad"], e["p_famosos_pct_autenticidad"]
        if d["n_nombres"] == 0:
            e["H1_H3"], e["H4"], e["H5"] = "no decide", "no decide", "no decide"
            e["lectura"] = "no decide (sin nombres fuera del prescripto; también 1 Tes, del núcleo)"
        else:
            en_rango = (pn != "" and 0.1 <= pn <= 0.9) or (pn != "" and pn < 0.1 and e["p_de_otras_fuentes"] != "" and e["p_de_otras_fuentes"] < 0.5)
            inc_ok = pinc == "" or pinc <= 0.9
            h5_senal = (pf != "" and pf > 0.9) or (pinc != "" and pinc > 0.9)
            h4_senal = pn != "" and pn < 0.1 and e["p_de_otras_fuentes"] != "" and e["p_de_otras_fuentes"] >= 0.5
            e["H1_H3"] = "compatible" if (en_rango and inc_ok and not h5_senal) else ("no compatible" if h5_senal else "no decide")
            e["H4"] = "compatible" if h4_senal else ("no decide" if (pn == "" or pn < 0.5) else "no compatible")
            e["H5"] = "compatible" if h5_senal else ("no compatible" if (e["p_nuevos_documentados"] != "" and e["p_nuevos_documentados"] >= 0.5 and inc_ok) else "no decide")
            e["lectura"] = f"H1-H3 {e['H1_H3']}; H4 {e['H4']}; H5 {e['H5']}"
        lect.append(e)
    lcols = list(lect[0].keys())
    with open(os.path.join(ROOT, "results", "canales", "onomastica_lectura.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=lcols, lineterminator="\r\n"); w.writeheader(); w.writerows(lect)
    print(f"autenticidad: {len(aut)} documentos con nombres; falsificación: {len(fal)}")
    for e in lect:
        print(f"{e['carta']:5s} n={e['n_nombres']:3d} nuevos={e['p_nuevos']} (pct aut {e['p_nuevos_pct_autenticidad']}, fal {e['p_nuevos_pct_falsificacion']}) "
              f"doc={e['p_nuevos_documentados']} inc={e['p_incoherencias']} fam={e['p_famosos']} (pct aut {e['p_famosos_pct_autenticidad']}) otras={e['p_de_otras_fuentes']} → {e['lectura']}")
    for g, lst in (("autenticidad", aut), ("falsificacion", fal)):
        pn = [x["p_nuevos"] for x in lst if x["p_nuevos"] != ""]
        print(g, "p_nuevos mediana", round(st.median(pn), 3), "p10", round(sorted(pn)[int(0.1 * len(pn))], 3), "p90", round(sorted(pn)[int(0.9 * len(pn))], 3),
              "| p_famosos mediana", round(st.median([x["p_famosos"] for x in lst if x["p_famosos"] != ""]), 3))
    return 0


if __name__ == "__main__":
    sys.exit(main())

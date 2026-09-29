#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
onomastica_inventario.py — inventario de nombres de persona (PROTOCOLO § 9.2; docs/canales/codigos_onomastica.md).

Entrada: results/canales/onomastica_candidatos.csv (de onomastica_extraer.py), la clasificación manual de
onomastica_datos_paulinas.py y onomastica_datos_referencia.py, y la tabla de los Hechos de Pablo y Tecla (aquí).
Salida: results/canales/onomastica_inventario.csv (una fila por nombre × documento) y onomastica_indices.csv.
Las columnas `c_region_periodo`, `fuente` y `cita` de la consulta externa se rellenan después con
onomastica_consultas.py; aquí quedan vacías.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from onomastica_datos_paulinas import NOMBRES, DETALLE  # noqa: E402
from onomastica_datos_referencia import R  # noqa: E402
from paulinum.text import normalize_form  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(ROOT, "results", "canales", "onomastica_candidatos.csv")
OUT = os.path.join(ROOT, "results", "canales", "onomastica_inventario.csv")
CRISTIANAS = {"paulinas", "Ignacio", "Ps-Ignacio", "1Clem", "Ps-Clemente", "3Cor", "HechosPablo", "Basilio", "Ps-Basilio"}
FAMOSO = {"historico", "literario", "biblico"}
# nombres de persona que aparecen en Hechos (SBLGNT), en forma castellana normalizada de este inventario
HECHOS = {"Pablo", "Timoteo", "Silvano (Silas)", "Apolo", "Cefas (Pedro)", "Pedro", "Santiago (hermano del Señor)", "Santiago", "Juan (apóstol)", "Juan",
          "Bernabé", "Aquila", "Prisca (Priscila)", "Jasón", "Sosípatro", "Gayo", "Erasto", "Sóstenes", "Crispo", "Marcos", "Aristarco", "Tíquico", "Alejandro",
          "Trófimo", "Poncio Pilato", "Poncio", "Simón (Pedro)", "Simón Mago", "Tomás", "Lucas", "Ana (profetisa)", "Herodes", "Pilato"}
# nombres de las catorce cartas (castellano normalizado) para `a_otra_carta` en las colecciones cristianas
PAULINAS_ES = {v[0] for v in NOMBRES.values() if v[1] in ("persona", "historico")}
PAULINAS_ES |= {"Pedro", "Santiago", "Juan", "Onésimo", "Timoteo", "Tito", "Lucas", "Marcos", "Clemente", "Demas", "Hermógenes", "Onesíforo", "Trifena", "Alejandro", "Lino", "Apia"}

# Hechos de Pablo y Tecla (APTh 1-43): nombres según Lipsius-Bonnet 1891 (griego) y M. R. James 1924 (verificado en
# earlychristianwritings.com/text/actspaul.html el 29-IX-2026). Una fila por nombre.
APTH = [
    ("Παῦλος", "Pablo", "historico", "APTh 1", "Iconio", "personaje literario", "protagonista", "coherente", "protagonista de la obra"),
    ("Δημᾶς", "Demas", "persona", "APTh 1", "Iconio", "adversario", "compañero hipócrita", "coherente", "nombre tomado de Col 4,14; Flm 24; 2 Tim 4,10"),
    ("Ἑρμογένης", "Hermógenes", "persona", "APTh 1", "Iconio", "adversario", "calderero", "coherente", "nombre tomado de 2 Tim 1,15 (y «calderero» de Alejandro, 2 Tim 4,14)"),
    ("Ὀνησιφόρος", "Onesíforo", "persona", "APTh 2", "Iconio", "mencionado", "hospedador", "coherente", "nombre tomado de 2 Tim 1,16; 4,19"),
    ("Λέκτρα", "Lectra", "persona", "APTh 2", "Iconio", "mencionado", "esposa de Onesíforo", "no comprobable", ""),
    ("Σιμμίας", "Simias", "persona", "APTh 2", "Iconio", "mencionado", "hijo de Onesíforo", "no comprobable", ""),
    ("Ζήνων", "Zenón", "persona", "APTh 2", "Iconio", "mencionado", "hijo de Onesíforo", "no comprobable", ""),
    ("Τίτος", "Tito", "persona", "APTh 2", "—", "mencionado", "informante", "coherente", "nombre tomado de las cartas"),
    ("Θέκλα", "Tecla", "persona", "APTh 7", "Iconio", "personaje literario", "protagonista", "no comprobable", ""),
    ("Θεοκλεία", "Teoclía", "persona", "APTh 7", "Iconio", "mencionado", "madre de Tecla", "no comprobable", ""),
    ("Θάμυρις", "Tamiris", "persona", "APTh 7", "Iconio", "adversario", "prometido de Tecla", "no comprobable", "nombre del mito (Tamiris)"),
    ("Καστέλιος", "Castelio", "persona", "APTh 14", "Iconio", "mencionado", "gobernador", "no comprobable", ""),
    ("Ἀλέξανδρος", "Alejandro", "persona", "APTh 26", "Antioquía", "adversario", "siriarca", "no comprobable", "nombre común; en 2 Tim 4,14 Alejandro es adversario"),
    ("Τρύφαινα", "Trifena", "persona", "APTh 27", "Antioquía", "mencionado", "reina, protectora", "incoherente", "Rom 16,12 saluda a una Trifena en Roma; la reina Trifena (viuda de Cotis) es personaje histórico de Tracia/Ponto, situado en Antioquía"),
    ("Φαλκονίλλα", "Falconila", "persona", "APTh 28", "Antioquía", "mencionado", "hija difunta de Trifena", "no comprobable", ""),
    ("Ἑρμίας", "Hermias", "persona", "APTh 41", "Mira", "mencionado", "hospedador", "no comprobable", ""),
]


def match(col: str, key: str):
    best = None
    for pref, es, tipo in R.get(col, []):
        if key.startswith(pref) and (best is None or len(pref) > len(best[0])):
            best = (pref, es, tipo)
    return best


def main() -> int:
    rows = list(csv.DictReader(open(CAND, encoding="utf-8")))
    inv = []
    unmatched = defaultdict(int)
    # agregación por (documento, nombre_es)
    agg = {}
    for r in rows:
        col, doc, key = r["coleccion"], r["documento"], r["clave"]
        if col == "paulinas":
            if key not in NOMBRES:
                unmatched[(col, key)] += int(r["n_menciones"]); continue
            es, tipo, b, nota_b = NOMBRES[key]
            if tipo in ("lugar", "pueblo", "divinidad", "otro"):
                continue
            k = (col, doc, es)
            e = agg.setdefault(k, {"nombre": key, "tipo": tipo, "n": 0, "refs": [], "b": b, "nota_b": nota_b, "estado": r["estado"]})
            e["n"] += int(r["n_menciones"]); e["refs"].append(r["refs"])
        else:
            if r["candidato"] == "no":
                continue
            m = match(col, key)
            if not m:
                unmatched[(col, key)] += int(r["n_menciones"]); continue
            pref, es, tipo = m
            k = (col, doc, es)
            e = agg.setdefault(k, {"nombre": key, "tipo": tipo, "n": 0, "refs": [], "b": None, "nota_b": "", "estado": r["estado"]})
            e["n"] += int(r["n_menciones"]); e["refs"].append(r["refs"])
    # a_otra_carta
    docs_by_name = defaultdict(set)
    for (col, doc, es) in agg:
        docs_by_name[(col, es)].add(doc)
    for (col, doc, es), e in sorted(agg.items()):
        tipo = e["tipo"]
        d = 1 if tipo in FAMOSO else 0
        if col == "paulinas":
            a = 1 if len(docs_by_name[(col, es)]) > 1 else 0
            b = e["b"]
        elif col in CRISTIANAS:
            a = 1 if es in PAULINAS_ES or es.split(" (")[0] in PAULINAS_ES else 0
            b = 1 if es in HECHOS or es.split(" (")[0] in HECHOS else 0
        else:
            a = 1 if len(docs_by_name[(col, es)]) > 1 else 0
            b = 0
        det = DETALLE.get((doc, e["nombre"])) if col == "paulinas" else None
        lugar, funcion, relacion, ecoh, nota = det if det else ("—", "mencionado", "—", "no comprobable", "")
        if col == "paulinas" and det is None and tipo == "biblico":
            funcion, ecoh = "personaje literario", "coherente"
        juicio = "sí" if (ecoh != "no comprobable" and col == "paulinas") or "(juicio)" in e["nota_b"] or (col != "paulinas") else "no"
        inv.append({"coleccion": col, "documento": doc, "estado": e["estado"], "nombre": e["nombre"], "nombre_es": es, "tipo": tipo,
                    "pasaje": "|".join(x for x in e["refs"] if x)[:120], "n_menciones": e["n"], "lugar": lugar, "funcion": funcion,
                    "relacion": relacion, "a_otra_carta": a, "b_hechos": b, "c_region_periodo": "", "d_famoso": d, "e_coherencia": ecoh,
                    "nuevo": 1 if (a == 0 and b == 0 and d == 0) else 0, "fuente": "", "cita": "", "juicio": juicio,
                    "nota": "; ".join(x for x in (nota, e["nota_b"]) if x)})
    for (gr, es, tipo, pas, lugar, funcion, rel, ecoh, nota) in APTH:
        d = 1 if tipo in FAMOSO else 0
        a = 1 if es in PAULINAS_ES else 0; b = 1 if es in HECHOS else 0
        inv.append({"coleccion": "HechosPablo", "documento": "APTh", "estado": "spurious", "nombre": normalize_form(gr), "nombre_es": es, "tipo": tipo,
                    "pasaje": pas, "n_menciones": "", "lugar": lugar, "funcion": funcion, "relacion": rel, "a_otra_carta": a, "b_hechos": b,
                    "c_region_periodo": "", "d_famoso": d, "e_coherencia": ecoh, "nuevo": 1 if (a == 0 and b == 0 and d == 0) else 0,
                    "fuente": "Lipsius-Bonnet 1891; James 1924", "cita": "", "juicio": "sí", "nota": nota})
    cols = ["coleccion", "documento", "estado", "nombre", "nombre_es", "tipo", "pasaje", "n_menciones", "lugar", "funcion", "relacion", "a_otra_carta",
            "b_hechos", "c_region_periodo", "d_famoso", "e_coherencia", "nuevo", "fuente", "cita", "juicio", "nota"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\r\n"); w.writeheader(); w.writerows(inv)
    from collections import Counter
    print(OUT, len(inv), Counter(r["coleccion"] for r in inv))
    top = sorted(unmatched.items(), key=lambda x: -x[1])[:60]
    print("sin clasificar (los más frecuentes):", [(c, k, n) for (c, k), n in top])
    return 0


if __name__ == "__main__":
    sys.exit(main())

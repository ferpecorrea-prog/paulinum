#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convergencia.py — tabla de convergencia de PROTOCOLO § 9.4: para cada carta, cuatro canales (estilometría, recepción,
onomástica, institucional) × cinco hipótesis (H1-H5) con tres valores (compatible / no compatible / no decide), y la
regla de lectura del protocolo: sostenida (ningún canal la hace no compatible y al menos dos la hacen compatible);
debilitada (un canal la hace no compatible); descartada (dos o más canales); abierta (el resto).

Entradas (todas ya publicadas):
  results/paulinum_1_0/veredicto.csv        columna `patron_8_5` del veredicto mecánico sellado (§ 8.5)
  results/canales/recepcion_medidas.csv     `lectura_mismo_rasero` (§ 9.1, D-027)
  results/canales/onomastica_lectura.csv    H1_H3 / H4 / H5 (§ 9.2, D-029)
  results/canales/institucional_lectura.csv H1_H3 / H4 / H5 (§ 9.3, D-030)
Salidas:
  results/canales/convergencia.csv           carta × canal × H1-H5 (+ base, nota)
  results/canales/convergencia_veredicto.csv carta × H1-H5 → sostenida / debilitada / descartada / abierta, y § 10 (refutada / debilitada / abierta para H1-H3)

Traducción del veredicto estilométrico (frase sellada `patron_8_5`) a los tres valores, fijada aquí y declarada en
docs/canales/codigos_convergencia.md: «compatible con Hx» → compatible; «no con Hx» y «Hx improbable» → no compatible
(la carta está dentro del rango y § 2.2 predice para H4 y H5 «fuera del rango»); hipótesis no nombrada → no decide;
«se informa sin decidir» → no decide en las cinco.
"""
from __future__ import annotations

import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETTERS = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb"]
H = ["H1", "H2", "H3", "H4", "H5"]
C, NC, ND = "compatible", "no compatible", "no decide"


def rango(s):
    """'H1-H3' → ['H1','H2','H3']; 'H2-H3' → ['H2','H3']; 'H5' → ['H5']."""
    m = re.match(r"H(\d)(?:-H(\d))?", s)
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    return [f"H{i}" for i in range(a, b + 1)]


def estilometria(patron: str):
    v = {h: ND for h in H}
    if "sin decidir" in patron:
        return v, "discordancia entre niveles (nivel 1 en contra, nivel 2 dentro): el veredicto no decide"
    for m in re.finditer(r"compatible con (H\d(?:-H\d)?)", patron):
        for h in rango(m.group(1)):
            v[h] = C
    for m in re.finditer(r"no con (H\d(?:-H\d)?)", patron):
        for h in rango(m.group(1)):
            v[h] = NC
    for m in re.finditer(r"(H\d(?:-H\d)?) improbable", patron):
        for h in rango(m.group(1)):
            v[h] = NC
    return v, ""


def recepcion(lectura: str):
    v = {h: ND for h in H}
    if lectura.startswith("H1, H2, H3, H4 compatibles"):
        for h in ("H1", "H2", "H3", "H4"):
            v[h] = C
        v["H5"] = NC
        return v, "mismo rasero (D-027): dentro del rango del núcleo + 50 años, atribución estable; el canal no separa H1-H4"
    if lectura.startswith("H1-H3 no compatible"):
        for h in ("H1", "H2", "H3"):
            v[h] = NC
        v["H4"] = v["H5"] = C
        return v, "atribución no estable (negada en Occidente: Ireneo según Gobar, Tertuliano → Bernabé, Roma según Eusebio)"
    raise ValueError(lectura)


def tres(h13, h4, h5):
    v = {"H1": h13, "H2": h13, "H3": h13, "H4": h4, "H5": h5}
    return v


def main() -> int:
    ver = {r["carta"]: r for r in csv.DictReader(open(os.path.join(ROOT, "results", "paulinum_1_0", "veredicto.csv"), encoding="utf-8"))}
    rec = {r["carta"]: r for r in csv.DictReader(open(os.path.join(ROOT, "results", "canales", "recepcion_medidas.csv"), encoding="utf-8"))}
    ono = {r["carta"]: r for r in csv.DictReader(open(os.path.join(ROOT, "results", "canales", "onomastica_lectura.csv"), encoding="utf-8"))}
    ins = {r["carta"]: r for r in csv.DictReader(open(os.path.join(ROOT, "results", "canales", "institucional_lectura.csv"), encoding="utf-8"))}
    filas, veredictos = [], []
    for L in LETTERS:
        canales = {}
        v, nota = estilometria(ver[L]["patron_8_5"])
        canales["estilometria"] = (v, f"veredicto § 8.5: nivel 1 «{ver[L]['nivel1']}», nivel 2 «{ver[L]['nivel2']}», nivel 3 «{ver[L]['nivel3']}», nivel 4 {ver[L]['nivel4_mantienen']}/{ver[L]['nivel4_configs']}", nota or ver[L]["patron_8_5"])
        v, nota = recepcion(rec[L]["lectura_mismo_rasero"])
        canales["recepcion"] = (v, f"recepcion_medidas.csv: {rec[L]['lectura_mismo_rasero']}", nota)
        o = ono[L]
        canales["onomastica"] = (tres(o["H1_H3"], o["H4"], o["H5"]), f"onomastica_lectura.csv: n_nombres={o['n_nombres']}, p_nuevos={o['p_nuevos']}, p_famosos={o['p_famosos']}, p_nuevos_documentados={o['p_nuevos_documentados']}", o["lectura"])
        i = ins[L]
        canales["institucional"] = (tres(i["H1_H3"], i["H4"], i["H5"]), f"institucional_lectura.csv: fecha_compatible={i['fecha_compatible'] or '—'} ({i['origen_fecha'] or '—'}); n_cargos={i['n_cargos']}, n_rasgos={i['n_rasgos']}", i["lectura"])
        for canal, (v, base, nota) in canales.items():
            filas.append({"carta": L, "canal": canal, **v, "base": base, "nota": nota})
        est = {"carta": L, "kind": ver[L]["kind"]}
        for h in H:
            vals = [canales[c][0][h] for c in canales]
            n_nc, n_c = vals.count(NC), vals.count(C)
            est[h] = "descartada" if n_nc >= 2 else "debilitada" if n_nc == 1 else "sostenida" if n_c >= 2 else "abierta"
            est[f"{h}_compatibles"] = ";".join(c for c in canales if canales[c][0][h] == C)
            est[f"{h}_no_compatibles"] = ";".join(c for c in canales if canales[c][0][h] == NC)
        # § 10: hipótesis de partida H1-H3 (para las trece; Hebreos sin hipótesis previa)
        fuera = ver[L]["nivel2"] != "dentro"
        lr_contra = "H_otro-autor" in ver[L]["nivel1"]
        otro_canal = any(canales[c][0][h] == NC for c in ("recepcion", "onomastica") for h in ("H1", "H2", "H3"))
        indeterminado = ver[L]["nivel3"].startswith("indeterminado") or "discordante" in ver[L]["nivel1"] or "sin decidir" in ver[L]["patron_8_5"]
        if L == "Heb":
            est["hipotesis_partida_s10"] = "sin hipótesis de partida (Hebreos, D-002): se informa la tabla"
        elif fuera and lr_contra and otro_canal:
            est["hipotesis_partida_s10"] = "refutada"
        elif fuera and lr_contra:
            est["hipotesis_partida_s10"] = "debilitada"
        elif indeterminado:
            est["hipotesis_partida_s10"] = "abierta (resultado indeterminado en la estilometría)"
        else:
            est["hipotesis_partida_s10"] = "no refutada"
        veredictos.append(est)
    with open(os.path.join(ROOT, "results", "canales", "convergencia.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["carta", "canal"] + H + ["base", "nota"], lineterminator="\r\n"); w.writeheader(); w.writerows(filas)
    with open(os.path.join(ROOT, "results", "canales", "convergencia_veredicto.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(veredictos[0].keys()), lineterminator="\r\n"); w.writeheader(); w.writerows(veredictos)
    for e in veredictos:
        print(f"{e['carta']:5s} " + " | ".join(f"{h} {e[h]}" for h in H) + f" | § 10: {e['hipotesis_partida_s10']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

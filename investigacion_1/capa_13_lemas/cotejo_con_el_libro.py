#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cotejo automático entre los valores impresos en el libro (Investigación 1, § 4.4 y notas 42-44)
y los que produce recalcular_capa_13.py sobre la matriz depositada. Escribe COTEJO_CON_EL_LIBRO.md.

Las cifras «publicadas» están transcritas del libro tal como se imprimen (tres decimales).
Se considera coincidencia exacta cuando |publicado − recalculado| < 0,0005 (redondeo a tres decimales);
los intervalos de remuestreo dependen del generador aleatorio y se comparan con tolerancia 0,01.
"""
from __future__ import annotations

import itertools
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recalcular_capa_13 import (AQUI, CONFIGURACIONES, EVALUADOS, LEMAS_13, LEMAS_8, NUCLEO_6,  # noqa: E402
                                NUCLEO_7, bootstrap_multinomial, cargar_matriz, distancias, heaps,
                                pares, pca_y_ward, tasas, tipificar)

PUB_A8 = {"2Cor": 0.638, "Gal": 0.744, "Flp": 0.829, "Jud": 0.875, "1Cor": 0.905, "2Tes": 1.005, "1Tes": 1.049,
          "2Tim": 1.136, "Rom": 1.198, "Sant": 1.281, "2Pe": 1.461, "Tit": 1.520, "1Pe": 1.646, "Heb": 1.762,
          "1Tim": 1.811, "Ef": 2.141, "Col": 2.264, "Flm": 2.817, "1Jn": 3.197}
PUB_B6 = {"2Cor": 0.598, "Gal": 0.629, "1Tes": 0.945, "1Cor": 0.989, "Flp": 1.076, "Rom": 1.104, "2Tim": 1.108,
          "2Tes": 1.190, "2Pe": 1.262, "Sant": 1.452, "Heb": 1.457, "Jud": 1.514, "1Pe": 1.520, "Tit": 1.733,
          "1Tim": 1.754, "Ef": 1.990, "Col": 2.138, "Flm": 2.433, "1Jn": 2.854}
PUB_B7 = {"2Cor": 0.504, "Gal": 0.682, "1Tes": 0.796, "1Cor": 0.989, "Flp": 0.920, "Rom": 1.004, "2Tim": 0.705,
          "2Tes": 0.918, "2Pe": 1.089, "Sant": 1.371, "Heb": 1.348, "Jud": 1.342, "1Pe": 1.182, "Tit": 1.500,
          "1Tim": 1.380, "Ef": 1.782, "Col": 1.960, "1Jn": 2.643}
PUB_SENS = {  # texto: (13, 11 sin ἐγώ/σύ, 10 sin art., 8 conect./prep., 7 sin οὐ)
    "Rom": (1.104, 1.114, 1.018, 0.984, 1.050), "1Cor": (0.989, 1.010, 1.058, 1.074, 1.037),
    "2Cor": (0.598, 0.565, 0.573, 0.604, 0.585), "Gal": (0.629, 0.668, 0.690, 0.675, 0.721),
    "Flp": (1.076, 1.136, 1.138, 1.063, 0.977), "1Tes": (0.945, 0.828, 0.863, 0.964, 1.002),
    "2Tes": (1.190, 1.219, 1.278, 1.322, 1.337), "2Tim": (1.108, 1.175, 1.218, 1.188, 1.194),
    "Heb": (1.457, 1.388, 1.392, 0.970, 1.023), "Tit": (1.733, 1.844, 1.738, 1.627, 1.466),
    "1Tim": (1.754, 1.684, 1.609, 1.361, 1.286), "Ef": (1.990, 2.085, 1.752, 1.628, 1.571),
    "Col": (2.138, 2.270, 2.147, 2.046, 2.066), "Flm": (2.433, 1.833, 1.778, 1.849, 1.687),
    "Sant": (1.452, 1.439, 1.507, 1.495, 1.596), "1Pe": (1.520, 1.309, 1.350, 1.451, 1.452),
    "2Pe": (1.262, 1.268, 1.267, 0.912, 0.909), "1Jn": (2.854, 3.091, 3.037, 1.948, 2.056),
    "Jud": (1.514, 1.558, 1.625, 1.772, 1.737)}
PUB_LOO = {  # mín, mediana, máx, desv. típ.
    "2Tim": (0.640, 0.671, 1.108, 0.183), "2Tes": (0.815, 0.938, 1.190, 0.141), "2Pe": (1.000, 1.096, 1.325, 0.131),
    "1Pe": (1.102, 1.256, 1.520, 0.143), "Heb": (1.248, 1.355, 1.772, 0.179), "Jud": (1.207, 1.414, 1.516, 0.114),
    "Sant": (1.238, 1.416, 1.554, 0.109), "1Tim": (1.264, 1.418, 1.754, 0.162), "Tit": (1.390, 1.475, 1.779, 0.155),
    "Ef": (1.665, 1.764, 2.216, 0.211), "Col": (1.850, 1.973, 2.301, 0.175), "1Jn": (2.430, 2.642, 3.398, 0.330)}
PUB_LOO_NUCLEO = {"2Cor": 0.566, "Gal": 0.841, "1Tes": 1.008, "Flp": 1.251, "1Cor": 1.377, "Rom": 1.397, "Flm": 2.433}
PUB_BOOT13 = {"2Tim": (0.905, 1.768, 6), "2Tes": (1.036, 2.031, 5), "2Pe": (1.015, 1.969, 5), "Heb": (1.267, 1.757, 3),
              "Sant": (1.278, 1.846, 3), "1Pe": (1.350, 1.977, 3), "Jud": (1.414, 2.235, 2), "Tit": (1.474, 2.519, 1),
              "1Tim": (1.557, 2.122, 0), "Ef": (1.753, 2.372, 0), "Col": (1.872, 2.613, 0), "Flm": (2.009, 3.698, 0),
              "1Jn": (2.435, 3.392, 0)}
PUB_BOOT8 = {"2Tes": (0.747, 2.001), "2Tim": (0.742, 1.952), "Tit": (1.213, 2.279), "1Tim": (1.554, 2.226),
             "Heb": (1.495, 2.116), "Ef": (1.781, 2.636), "Col": (1.840, 2.909), "Flm": (2.051, 4.288)}
PUB_HEAPS = {"a": 1.209358, "b": 0.647958, "R2": 0.9929, "cook_Flm": 2.675, "a_sinFlm": 1.630, "b_sinFlm": 0.597}
PUB_HEAPS_IP = {"Ef": (564, 457, 651), "Col": (453, 346, 495), "2Tes": (280, 231, 336), "1Tim": (568, 347, 496),
                "2Tim": (459, 294, 423), "Tit": (314, 190, 281), "Heb": (1072, 715, 1031), "Sant": (580, 366, 522),
                "1Pe": (562, 357, 510), "2Pe": (417, 270, 390), "Jud": (233, 149, 224), "1Jn": (262, 426, 607)}
PUB_HEAPS_RESID = {"1Tim": 0.314, "Tit": 0.305, "2Tim": 0.264, "Heb": 0.222, "Sant": 0.283, "1Pe": 0.276,
                   "2Pe": 0.251, "Jud": 0.244}
PUB_PCA = (0.375, 0.200)
PUB_PARES = {"Ef-Col": 0.678, "Rom-Heb": 0.899, "1Tim-Tit": 1.232, "1Tes-2Tes": 1.406, "1Tim-2Tim": 1.699,
             "2Tim-Tit": 1.870, "Flm-2Tim": 2.095}
# Capa A: diagnósticos del § 4.4
PUB_A_SIN_PRON = {"Flm": 1.978, "Col": 2.527, "Ef": 2.346, "Heb": 1.754, "1Tim": 1.706, "Tit": 1.676}
PUB_A_JUDAS = {"sin_pronombres": 0.713, "sin_pron_ni_articulo": 0.740, "solo_conect_prep": 0.780,
               "suelo_de_ruido_esperado": 1.143, "boot_mediana": 1.357, "boot_ic": (0.819, 2.038),
               "frac_subconjuntos_judas_bajo_4_o_mas": 0.379, "frac_subconjuntos_flm_maxima_de_14": 0.758}


def fmt(v):
    return "—" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"


class Cotejo:
    def __init__(self):
        self.filas = []
        self.exactas = 0
        self.total = 0

    def add(self, seccion, item, pub, rec, tol=0.0005):
        ok = abs(pub - rec) < tol
        self.total += 1
        self.exactas += int(ok)
        self.filas.append((seccion, item, pub, rec, "✓" if ok else "✗ (%.3f)" % (rec - pub)))

    def md(self):
        out = ["| sección | valor | publicado | recalculado | coincide |", "|---|---|---|---|---|"]
        for s, i, p, r, ok in self.filas:
            out.append(f"| {s} | {i} | {fmt(p)} | {fmt(r)} | {ok} |")
        return "\n".join(out)


def main():
    m = cargar_matriz(os.path.join(AQUI, "data", "matriz_19x13.csv"))
    c = Cotejo()
    dA = distancias(m, LEMAS_8, NUCLEO_6)
    for k, v in PUB_A8.items():
        c.add("Capa A (8 rasgos, núcleo 6)", k, v, float(dA[k]))
    dB6 = distancias(m, LEMAS_13, NUCLEO_6)
    for k, v in PUB_B6.items():
        c.add("Capa B (13, núcleo 6)", k, v, float(dB6[k]))
    dB7 = distancias(m, LEMAS_13, NUCLEO_7)
    for k, v in PUB_B7.items():
        c.add("Capa B (13, núcleo 7)", k, v, float(dB7[k]))
    sens = pd.DataFrame({k: distancias(m, v, NUCLEO_6) for k, v in CONFIGURACIONES.items()})
    for k, vals in PUB_SENS.items():
        for col, v in zip(CONFIGURACIONES.keys(), vals):
            c.add("Sensibilidad", f"{k} · {col}", v, float(sens.loc[k, col]))
    loo = {}
    for fuera in NUCLEO_7:
        loo[fuera] = distancias(m, LEMAS_13, [x for x in NUCLEO_7 if x != fuera])
    loo = pd.DataFrame(loo)
    for k, (mn, md, mx, sd) in PUB_LOO.items():
        r = loo.loc[k]
        c.add("LOO", f"{k} mín", mn, float(r.min()))
        c.add("LOO", f"{k} mediana", md, float(r.median()))
        c.add("LOO", f"{k} máx", mx, float(r.max()))
        c.add("LOO", f"{k} desv. típ.", sd, float(r.std(ddof=1)))
    for k, v in PUB_LOO_NUCLEO.items():
        c.add("LOO núcleo (cada indiscutida fuera)", k, v, float(loo.loc[k, k]))
    b13 = bootstrap_multinomial(m, LEMAS_13, NUCLEO_6, 20000, 20260903)
    for k, (lo, hi, n) in PUB_BOOT13.items():
        c.add("Remuestreo 13 (IC 95 %)", f"{k} inf", lo, float(b13.loc[k, "ic95_inf"]), tol=0.01)
        c.add("Remuestreo 13 (IC 95 %)", f"{k} sup", hi, float(b13.loc[k, "ic95_sup"]), tol=0.01)
    b8 = bootstrap_multinomial(m, LEMAS_8, NUCLEO_6, 20000, 20260904)
    for k, (lo, hi) in PUB_BOOT8.items():
        c.add("Remuestreo 8 (IC 95 %)", f"{k} inf", lo, float(b8.loc[k, "ic95_inf"]), tol=0.02)
        c.add("Remuestreo 8 (IC 95 %)", f"{k} sup", hi, float(b8.loc[k, "ic95_sup"]), tol=0.02)
    h7 = heaps(m, NUCLEO_7)
    h6 = heaps(m, NUCLEO_6)
    c.add("Heaps", "a", PUB_HEAPS["a"], h7["a"], tol=5e-7)
    c.add("Heaps", "b", PUB_HEAPS["b"], h7["b"], tol=5e-7)
    c.add("Heaps", "R²", PUB_HEAPS["R2"], h7["R2"], tol=5e-5)
    c.add("Heaps", "Cook (Flm)", PUB_HEAPS["cook_Flm"], h7["cook"]["Flm"])
    c.add("Heaps", "a sin Flm", PUB_HEAPS["a_sinFlm"], h6["a"])
    c.add("Heaps", "b sin Flm", PUB_HEAPS["b_sinFlm"], h6["b"])
    for k, (obs, lo, hi) in PUB_HEAPS_IP.items():
        c.add("Heaps IP95", f"{k} inf", lo, float(h7["tabla"].loc[k, "ip95_inf"]), tol=0.6)
        c.add("Heaps IP95", f"{k} sup", hi, float(h7["tabla"].loc[k, "ip95_sup"]), tol=0.6)
    for k, v in PUB_HEAPS_RESID.items():
        c.add("Heaps residuo log", k, v, float(h7["tabla"].loc[k, "residuo_log"]))
    # Sin Filemón: Tito entra por un solo lema (314 frente a 204-315)
    c.add("Heaps sin Flm IP95", "Tit inf", 204, float(h6["tabla"].loc["Tit", "ip95_inf"]), tol=0.6)
    c.add("Heaps sin Flm IP95", "Tit sup", 315, float(h6["tabla"].loc["Tit", "ip95_sup"]), tol=0.6)
    z6 = tipificar(tasas(m, LEMAS_13), NUCLEO_6)
    pca, dendro = pca_y_ward(z6)
    c.add("PCA", "PC1", PUB_PCA[0], pca["varianza_explicada"][0])
    c.add("PCA", "PC2", PUB_PCA[1], pca["varianza_explicada"][1])
    p = pares(z6, [tuple(k.split("-")) for k in PUB_PARES])
    for k, v in PUB_PARES.items():
        c.add("Pares", k, v, float(p.loc[k, "distancia"]))
    # Capa A: diagnósticos
    sinp = distancias(m, [l for l in LEMAS_8 if l not in ("ἐγώ", "σύ")], NUCLEO_6)
    for k, v in PUB_A_SIN_PRON.items():
        c.add("Capa A sin ἐγώ/σύ", k, v, float(sinp[k]))
    c.add("Capa A Judas", "sin pronombres", PUB_A_JUDAS["sin_pronombres"], float(sinp["Jud"]))
    sinpa = distancias(m, [l for l in LEMAS_8 if l not in ("ἐγώ", "σύ", "ὁ")], NUCLEO_6)
    c.add("Capa A Judas", "sin pron. ni artículo", PUB_A_JUDAS["sin_pron_ni_articulo"], float(sinpa["Jud"]))
    # «solo conectivos y preposiciones» de la capa A: por analogía con la capa B, {καί, ἐν, ὅς, εἰς}
    concp = distancias(m, ["καί", "ἐν", "ὅς", "εἰς"], NUCLEO_6)
    c.add("Capa A Judas", "solo conect./prep. (καί ἐν ὅς εἰς)", PUB_A_JUDAS["solo_conect_prep"], float(concp["Jud"]))
    # Suelo de ruido: distancia esperada de un texto de 478 palabras con las tasas medias del núcleo
    t8 = tasas(m, LEMAS_8)
    mu = t8.loc[NUCLEO_6].mean(axis=0).values
    sd = t8.loc[NUCLEO_6].std(axis=0, ddof=1).values
    n = int(m.loc["Jud", "palabras"])
    p_mu = mu / 1000.0
    var_rate = p_mu * (1 - p_mu) / n * 1e6
    suelo = float(np.sqrt(np.mean(var_rate / sd ** 2)))
    c.add("Capa A Judas", "suelo de ruido multinomial", PUB_A_JUDAS["suelo_de_ruido_esperado"], suelo, tol=0.01)
    c.add("Capa A Judas", "boot mediana", PUB_A_JUDAS["boot_mediana"], float(b8.loc["Jud", "d_mediana_boot"]), tol=0.01)
    c.add("Capa A Judas", "boot IC inf", PUB_A_JUDAS["boot_ic"][0], float(b8.loc["Jud", "ic95_inf"]), tol=0.02)
    c.add("Capa A Judas", "boot IC sup", PUB_A_JUDAS["boot_ic"][1], float(b8.loc["Jud", "ic95_sup"]), tol=0.01)
    # 219 subconjuntos de ≥ 3 de los 8 rasgos
    paulinas14 = NUCLEO_7 + ["Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit", "Heb"]
    n_sub = jud_ok = flm_max = 0
    for k in range(3, 9):
        for sub in itertools.combinations(LEMAS_8, k):
            d = distancias(m, list(sub), NUCLEO_6)
            n_sub += 1
            jud_ok += int(sum(d[c_] > d["Jud"] for c_ in NUCLEO_6) >= 4)
            flm_max += int(d[paulinas14].idxmax() == "Flm")
    c.add("Capa A subconjuntos", "n subconjuntos (=219)", 219, n_sub, tol=0.6)
    c.add("Capa A subconjuntos", "Judas bajo ≥4 del núcleo (fracción)", PUB_A_JUDAS["frac_subconjuntos_judas_bajo_4_o_mas"], jud_ok / n_sub, tol=0.001)
    c.add("Capa A subconjuntos", "Flm máxima de las 14 (fracción)", PUB_A_JUDAS["frac_subconjuntos_flm_maxima_de_14"], flm_max / n_sub, tol=0.001)

    texto = [
        "# Cotejo de la capa de trece lemas con el libro",
        "",
        "Generado por `cotejo_con_el_libro.py` sobre `data/matriz_19x13.csv` (la matriz primaria impresa en la nota 43).",
        "Cada fila compara el valor impreso en Investigación 1 (§ 4.4, notas 42-44) con el recalculado por",
        "`recalcular_capa_13.py`. Tolerancia: 0,0005 (redondeo a tres decimales); 0,01 en los intervalos de",
        "remuestreo de trece lemas y 0,02 en los de ocho (dependen del generador aleatorio); 0,6 lemas en los intervalos de predicción de Heaps (el libro los imprime redondeados a enteros).",
        "",
        f"**Resultado: {c.exactas} de {c.total} valores coinciden.**",
        "",
        "Nota sobre las configuraciones de sensibilidad: el libro rotula la cuarta configuración como «8 conectores y",
        "preposiciones». La búsqueda exhaustiva sobre todos los subconjuntos de 8 y de 7 lemas muestra que las cifras",
        "impresas corresponden, de forma única, a {καί, ἐν, ὅς, εἰς, δέ, γάρ, οὐ, διά} y, sin οὐ, a",
        "{καί, ἐν, ὅς, εἰς, δέ, γάρ, διά}: el depósito original incluía el relativo ὅς y excluía μή en esa configuración.",
        "La reconstrucción adopta esa composición para reproducir las tablas; el rótulo del libro es, en rigor, inexacto.",
        "",
        "Partición de Ward recalculada: `" + str(dendro).replace("'", "") + "`",
        "",
        c.md(),
    ]
    with open(os.path.join(AQUI, "COTEJO_CON_EL_LIBRO.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(texto) + "\n")
    print(f"{c.exactas}/{c.total} coincidencias")
    for s, i, p, r, ok in c.filas:
        if not ok.startswith("✓"):
            print("  DIFIERE:", s, i, p, round(r, 4))
    return 0


if __name__ == "__main__":
    sys.exit(main())

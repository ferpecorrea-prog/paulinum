#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recálculo íntegro de la capa estilométrica de trece lemas (Investigación 1, cap. 2, § 4.4).

Reconstrucción a partir de la especificación publicada en el libro (notas 42-44):
  - Corpus: léxico lematizado de Perseus, tlg0031.tlg006-tlg019 (14 paulinas + Hebreos),
    tlg0031.tlg020-tlg023 y tlg026 (cinco controles no paulinos).
  - Matriz primaria: 19 escritos × 13 lemas (data/matriz_19x13.csv), recuentos brutos.
  - Procedimiento: tasas por mil palabras; tipificación con media y desviación típica
    MUESTRAL del núcleo (seis cartas: Rom, 1Cor, 2Cor, Gal, Flp, 1Tes; o siete con Flm);
    distancia = raíz del promedio de los cuadrados de las puntuaciones tipificadas.
  - Capa A = los ocho primeros lemas (ὁ, καί, ἐν, ἐγώ, σύ, ὅς, αὐτός, εἰς); capa B = los trece.
  - Sensibilidad (5 configuraciones), leave-one-out del núcleo de siete, remuestreo
    multinomial (20.000 réplicas), ley de Heaps, componentes principales, Ward, pares.

Uso:  python recalcular_capa_13.py [--salida results/] [--replicas 20000] [--semilla 20260903]

Todas las tablas se escriben en CSV; la salida por pantalla reproduce las del libro
para cotejo visual. Véase COTEJO_CON_EL_LIBRO.md para el resultado de la comparación.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
LEMAS_8 = ["ὁ", "καί", "ἐν", "ἐγώ", "σύ", "ὅς", "αὐτός", "εἰς"]
LEMAS_13 = LEMAS_8 + ["δέ", "γάρ", "οὐ", "μή", "διά"]
NUCLEO_6 = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes"]
NUCLEO_7 = NUCLEO_6 + ["Flm"]
EVALUADOS = ["2Tim", "2Tes", "2Pe", "1Pe", "Heb", "Jud", "Sant", "1Tim", "Tit", "Ef", "Col", "1Jn"]

CONFIGURACIONES = {
    "13": LEMAS_13,
    "11 sin ἐγώ/σύ": [l for l in LEMAS_13 if l not in ("ἐγώ", "σύ")],
    "10 sin art.": [l for l in LEMAS_13 if l not in ("ἐγώ", "σύ", "ὁ")],
    # Composición exacta de las dos últimas configuraciones, recuperada por búsqueda exhaustiva
    # sobre todos los subconjuntos de 8 y de 7 lemas (coincidencia única con la tabla del libro,
    # error máximo < 0,0005): el conjunto «conectores y preposiciones» del depósito original
    # incluía el relativo ὅς y excluía μή. Véase COTEJO_CON_EL_LIBRO.md.
    "8 conect./prep.": ["καί", "ἐν", "ὅς", "εἰς", "δέ", "γάρ", "οὐ", "διά"],
    "7 sin οὐ": ["καί", "ἐν", "ὅς", "εἰς", "δέ", "γάρ", "διά"],
}


def cargar_matriz(ruta: str) -> pd.DataFrame:
    m = pd.read_csv(ruta, index_col="id")
    for col in ["palabras", "lemas_distintos"] + LEMAS_13:
        m[col] = m[col].astype(int)
    return m


def tasas(m: pd.DataFrame, lemas: list[str]) -> pd.DataFrame:
    return m[lemas].div(m["palabras"], axis=0) * 1000.0


def tipificar(t: pd.DataFrame, nucleo: list[str]) -> pd.DataFrame:
    mu = t.loc[nucleo].mean(axis=0)
    sd = t.loc[nucleo].std(axis=0, ddof=1)  # desviación típica muestral
    return (t - mu) / sd


def distancia(z: pd.DataFrame) -> pd.Series:
    return np.sqrt((z ** 2).mean(axis=1))


def distancias(m: pd.DataFrame, lemas: list[str], nucleo: list[str]) -> pd.Series:
    return distancia(tipificar(tasas(m, lemas), nucleo))


def heaps(m: pd.DataFrame, entrenamiento: list[str]) -> dict:
    """Regresión ordinaria log(lemas) = a + b·log(palabras) con intervalo de predicción al 95 %."""
    from scipy import stats

    x = np.log(m.loc[entrenamiento, "palabras"].values.astype(float))
    y = np.log(m.loc[entrenamiento, "lemas_distintos"].values.astype(float))
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    s2 = float(resid @ resid / (n - 2))
    r2 = 1 - float(resid @ resid) / float(((y - y.mean()) ** 2).sum())
    XtX_inv = np.linalg.inv(X.T @ X)
    tcrit = stats.t.ppf(0.975, n - 2)
    # distancia de Cook
    h = np.einsum("ij,jk,ik->i", X, XtX_inv, X)
    cook = (resid ** 2 / (2 * s2)) * (h / (1 - h) ** 2)
    filas = []
    for idx in m.index:
        xi = np.log(float(m.loc[idx, "palabras"]))
        x0 = np.array([1.0, xi])
        pred = float(x0 @ beta)
        se_pred = np.sqrt(s2 * (1 + x0 @ XtX_inv @ x0))
        lo, hi = pred - tcrit * se_pred, pred + tcrit * se_pred
        obs = int(m.loc[idx, "lemas_distintos"])
        filas.append({
            "id": idx,
            "palabras": int(m.loc[idx, "palabras"]),
            "lemas_observados": obs,
            "lemas_predichos": float(np.exp(pred)),
            "ip95_inf": float(np.exp(lo)),
            "ip95_sup": float(np.exp(hi)),
            "residuo_log": float(np.log(obs) - pred),
            "dentro_del_intervalo": bool(np.exp(lo) <= obs <= np.exp(hi)),
            "entrenamiento": idx in entrenamiento,
        })
    return {
        "a": float(beta[0]), "b": float(beta[1]), "R2": r2, "n": n,
        "cook": dict(zip(entrenamiento, map(float, cook))),
        "tabla": pd.DataFrame(filas).set_index("id"),
    }


def bootstrap_multinomial(m: pd.DataFrame, lemas: list[str], nucleo: list[str],
                          replicas: int, semilla: int) -> pd.DataFrame:
    """Réplicas multinomiales de los recuentos de cada texto; el patrón del núcleo se mantiene fijo."""
    rng = np.random.default_rng(semilla)
    t = tasas(m, lemas)
    mu = t.loc[nucleo].mean(axis=0).values
    sd = t.loc[nucleo].std(axis=0, ddof=1).values
    filas = []
    for idx in m.index:
        n = int(m.loc[idx, "palabras"])
        cuentas = m.loc[idx, lemas].values.astype(int)
        p = np.append(cuentas, n - cuentas.sum()) / n
        rep = rng.multinomial(n, p, size=replicas)[:, : len(lemas)]
        z = (rep / n * 1000.0 - mu) / sd
        d = np.sqrt((z ** 2).mean(axis=1))
        filas.append({
            "id": idx, "d_observada": float(distancia(tipificar(t, nucleo)).loc[idx]),
            "d_mediana_boot": float(np.median(d)),
            "ic95_inf": float(np.percentile(d, 2.5)), "ic95_sup": float(np.percentile(d, 97.5)),
        })
    return pd.DataFrame(filas).set_index("id")


def solapamientos(boot: pd.DataFrame, nucleo: list[str]) -> pd.Series:
    out = {}
    for idx in boot.index:
        lo, hi = boot.loc[idx, "ic95_inf"], boot.loc[idx, "ic95_sup"]
        k = sum(1 for c in nucleo if not (hi < boot.loc[c, "ic95_inf"] or lo > boot.loc[c, "ic95_sup"]))
        out[idx] = k
    return pd.Series(out, name="solapa_con_n_del_nucleo")


def pca_y_ward(z: pd.DataFrame) -> tuple[dict, list]:
    from scipy.cluster.hierarchy import linkage, to_tree

    X = z.values - z.values.mean(axis=0)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    var = S ** 2 / (S ** 2).sum()
    coords = pd.DataFrame(U[:, :2] * S[:2], index=z.index, columns=["PC1", "PC2"])
    L = linkage(z.values, method="ward")
    arbol = to_tree(L)
    etiquetas = list(z.index)

    def dendro(nodo):
        if nodo.is_leaf():
            return etiquetas[nodo.id]
        return [dendro(nodo.get_left()), dendro(nodo.get_right())]

    return {"varianza_explicada": var[:2].tolist(), "coordenadas": coords}, dendro(arbol)


def pares(z: pd.DataFrame, lista: list[tuple[str, str]]) -> pd.DataFrame:
    filas = []
    for a, b in lista:
        d = float(np.sqrt(((z.loc[a] - z.loc[b]) ** 2).mean()))
        filas.append({"par": f"{a}-{b}", "distancia": d})
    return pd.DataFrame(filas).set_index("par")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matriz", default=os.path.join(AQUI, "data", "matriz_19x13.csv"))
    ap.add_argument("--salida", default=os.path.join(AQUI, "results"))
    ap.add_argument("--replicas", type=int, default=20000)
    ap.add_argument("--semilla", type=int, default=20260903)
    a = ap.parse_args()
    os.makedirs(a.salida, exist_ok=True)
    m = cargar_matriz(a.matriz)

    def guardar(df, nombre):
        df.to_csv(os.path.join(a.salida, nombre), float_format="%.6f")

    # 1. Tasas y tipificación
    t13 = tasas(m, LEMAS_13)
    guardar(t13, "tasas_por_mil.csv")
    z6 = tipificar(t13, NUCLEO_6)
    guardar(z6, "z_nucleo6.csv")

    # 2. Capa A (8 lemas) y capa B (13 lemas) sobre núcleo 6 y 7
    dA = distancias(m, LEMAS_8, NUCLEO_6).rename("D_8_nucleo6")
    dB6 = distancias(m, LEMAS_13, NUCLEO_6).rename("D_13_nucleo6")
    dB7 = distancias(m, LEMAS_13, NUCLEO_7).rename("D_13_nucleo7")
    dist = pd.concat([dA, dB6, dB7], axis=1)
    dist.loc["Flm", "D_13_nucleo7"] = np.nan  # Flm está dentro del núcleo de siete; el libro imprime «---»
    dist["condicion"] = m["condicion"]
    guardar(dist, "distancias.csv")
    print("\n== Capa A (8 rasgos, núcleo 6), ordenada ==")
    print(dA.sort_values().round(3).to_string())
    print("\n== Capa B (13 rasgos), núcleo 6 / núcleo 7, ordenada por núcleo 6 ==")
    print(dist.sort_values("D_13_nucleo6")[["D_13_nucleo6", "D_13_nucleo7", "condicion"]].round(3).to_string())

    # 3. Sensibilidad
    sens = pd.DataFrame({k: distancias(m, v, NUCLEO_6) for k, v in CONFIGURACIONES.items()})
    guardar(sens, "sensibilidad.csv")
    print("\n== Sensibilidad (núcleo 6) ==")
    print(sens.round(3).to_string())

    # 4. Leave-one-out sobre el núcleo de siete
    loo_detalle = {}
    for fuera in NUCLEO_7:
        nucleo = [c for c in NUCLEO_7 if c != fuera]
        loo_detalle[fuera] = distancias(m, LEMAS_13, nucleo)
    loo_detalle = pd.DataFrame(loo_detalle)  # filas: texto; columnas: carta omitida
    guardar(loo_detalle, "loo_detalle.csv")
    loo_eval = loo_detalle.loc[EVALUADOS]
    loo_resumen = pd.DataFrame({
        "minimo": loo_eval.min(axis=1), "mediana": loo_eval.median(axis=1),
        "maximo": loo_eval.max(axis=1), "desv_tip": loo_eval.std(axis=1, ddof=1),
    }).sort_values("mediana")
    guardar(loo_resumen, "loo_resumen.csv")
    print("\n== LOO (evaluados): mín / mediana / máx / desv. típ. ==")
    print(loo_resumen.round(3).to_string())
    loo_nucleo = pd.Series({c: float(loo_detalle.loc[c, c]) for c in NUCLEO_7}, name="distancia_a_las_otras_seis").sort_values()
    guardar(loo_nucleo.to_frame(), "loo_nucleo_siete.csv")
    print("\n== Cada indiscutida dejada fuera, frente a las otras seis ==")
    print(loo_nucleo.round(3).to_string())

    # 5. Remuestreo multinomial
    boot13 = bootstrap_multinomial(m, LEMAS_13, NUCLEO_6, a.replicas, a.semilla)
    boot13["solapa_con_n_del_nucleo"] = solapamientos(boot13, NUCLEO_6)
    guardar(boot13, "bootstrap_13.csv")
    boot8 = bootstrap_multinomial(m, LEMAS_8, NUCLEO_6, a.replicas, a.semilla + 1)
    boot8["solapa_con_n_del_nucleo"] = solapamientos(boot8, NUCLEO_6)
    guardar(boot8, "bootstrap_8.csv")
    print("\n== Remuestreo multinomial, 13 rasgos (IC 95 %) ==")
    print(boot13.loc[EVALUADOS + ["Flm"]].round(3).to_string())

    # 6. Ley de Heaps
    h7 = heaps(m, NUCLEO_7)
    guardar(h7["tabla"], "heaps_nucleo7.csv")
    h6 = heaps(m, NUCLEO_6)
    guardar(h6["tabla"], "heaps_sin_filemon.csv")
    resumen_heaps = {
        "nucleo7": {k: h7[k] for k in ("a", "b", "R2", "n", "cook")},
        "sin_filemon": {k: h6[k] for k in ("a", "b", "R2", "n", "cook")},
    }
    with open(os.path.join(a.salida, "heaps_ajuste.json"), "w", encoding="utf-8") as f:
        json.dump(resumen_heaps, f, ensure_ascii=False, indent=2)
    print("\n== Heaps (siete indiscutidas): a=%.6f b=%.6f R2=%.4f; Cook(Flm)=%.3f" %
          (h7["a"], h7["b"], h7["R2"], h7["cook"]["Flm"]))
    print("   Sin Filemón: a=%.3f b=%.3f" % (h6["a"], h6["b"]))
    print(h7["tabla"][["lemas_observados", "ip95_inf", "ip95_sup", "residuo_log", "dentro_del_intervalo"]].round(3).to_string())

    # 7. PCA y Ward sobre la matriz tipificada (19 × 13, núcleo 6)
    pca, dendro = pca_y_ward(z6)
    guardar(pca["coordenadas"], "pca_coordenadas.csv")
    with open(os.path.join(a.salida, "ward_dendrograma.json"), "w", encoding="utf-8") as f:
        json.dump({"varianza_explicada_PC1_PC2": pca["varianza_explicada"], "dendrograma": dendro},
                  f, ensure_ascii=False, indent=1)
    print("\n== PCA: varianza explicada PC1, PC2 = %.3f, %.3f" % tuple(pca["varianza_explicada"]))
    print("== Ward:", json.dumps(dendro, ensure_ascii=False))

    # 8. Distancias entre pares de interés
    p = pares(z6, [("Ef", "Col"), ("Rom", "Heb"), ("1Tim", "Tit"), ("1Tes", "2Tes"),
                   ("1Tim", "2Tim"), ("2Tim", "Tit"), ("Flm", "2Tim")])
    guardar(p, "pares.csv")
    print("\n== Pares ==")
    print(p.round(3).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

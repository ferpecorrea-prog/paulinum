#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
veredicto.py — veredicto mecánico por carta (PROTOCOLO de paulinum 1.0, § 8), calculado solo a partir de los archivos de
resultados, sin intervención manual. El libro reproduce la tabla que produce y la comenta; no la corrige.

Entradas (results/<run>/):
  familias_aptitud.csv, summary_by_letter.csv, concordancia_familias.csv        (nivel 1: posibilidad)
  bootstrap_percentil_{minmax,delta}.csv                                        (nivel 2: plausibilidad, § 7.3-7.4)
  nearest_author_{minmax,delta}.csv                                             (nivel 3: superioridad comparativa)
  sensibilidad/<bloque>/summary_by_letter.csv y bootstrap_percentil_*.csv       (nivel 4: robustez; opcional)
Salida: veredicto.csv y veredicto.md (una fila por carta, sin grado ni adjetivos), y «qué revisaría este juicio».

Reglas (fijadas antes de ejecutar; véase PROTOCOLO § 8):
  Nivel 1  por familia apta: escala verbal de la mediana de log10 LR epistolar; el nivel = escala verbal de la mediana
           de las familias aptas; «discordante» si dos familias aptas tienen signo contrario.
  Nivel 2  dentro / fuera / indeterminado según los IC del percentil en E y en B (bootstrap de autores; si hay IC de
           ventanas, se exige la misma condición en ambos); si difieren min-max y Delta, «indeterminado». Si «fuera»:
           «tamaño de un salto de género» si el IC de pct_G incluye un valor <= 0,90; si no, «tamaño de un cambio de autor».
  Nivel 3  pasa si el núcleo es el autor más próximo en las dos medidas y el IC 95 % del margen (bootstrap de ventanas)
           no incluye 0 en ninguna; se informa siempre el mejor otro autor y el margen.
  Nivel 4  proporción de configuraciones de sensibilidad en las que se mantienen el signo del nivel 1 y la decisión del
           nivel 2; se nombran las que lo cambian.
  Patrón (§ 8.5) a partir de los niveles 1-3.
Uso: python scripts/veredicto.py --run paulinum_1_0
"""
from __future__ import annotations

import argparse
import csv
import glob
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.pipeline import _write_csv, LETTERS_14, FAMILIES  # noqa: E402
from paulinum.verify import verbal  # noqa: E402

P_INTRA = 0.90    # región de equivalencia intra-autor (§ 7.3)
P_INTER = 0.10    # cuerpo de la distribución inter-autor (§ 7.3)


def _read(path: str) -> list[dict]:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _f(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def letters_in(run_dir: str) -> list[str]:
    seen = list(dict.fromkeys(r["id"] for r in _read(os.path.join(run_dir, "summary_by_letter.csv"))))
    seen += [r["id"] for r in _read(os.path.join(run_dir, "bootstrap_percentil_minmax.csv")) if r["id"] not in seen]
    return [L for L in LETTERS_14 if L in seen] + [L for L in seen if L not in LETTERS_14]


def nivel1(run_dir: str) -> dict[str, dict]:
    apt = {r["family"] for r in _read(os.path.join(run_dir, "familias_aptitud.csv")) if r["apta"] == "True"}
    summ = _read(os.path.join(run_dir, "summary_by_letter.csv"))
    out = {}
    for L in letters_in(run_dir):
        rows = [r for r in summ if r["id"] == L and r["family"] in apt]
        if not rows:
            continue
        per = {r["family"]: _f(r["log10lr_epist_median"]) for r in rows}
        vals = [v for v in per.values() if not math.isnan(v)]
        med = sorted(vals)[len(vals) // 2] if len(vals) % 2 else (sorted(vals)[len(vals) // 2 - 1] + sorted(vals)[len(vals) // 2]) / 2 if vals else float("nan")
        signs = {"+" if v > 0 else "-" for v in vals if abs(v) >= 0.3}   # solo cuentan las familias discriminantes
        out[L] = {"kind": rows[0]["kind"], "familias_aptas": "|".join(sorted(per)),
                  **{f"log10lr_epist_{f}": per.get(f, float("nan")) for f in FAMILIES},
                  "log10lr_epist_mediana_familias": med, "nivel1_verbal": verbal(med) if not math.isnan(med) else "",
                  "nivel1_concordancia": "discordante" if len(signs) > 1 else "concordante",
                  "nivel1": ("discordante" if len(signs) > 1 else verbal(med)) if not math.isnan(med) else "sin datos"}
    return out


def _decision_metric(r: dict, use_windows: bool) -> tuple[str, str]:
    """Decisión de equivalencia para una medida a partir de una fila de bootstrap_percentil_<metric>.csv."""
    def ci(k):
        lo, hi = _f(r.get(f"ic_autores_{k}_inf")), _f(r.get(f"ic_autores_{k}_sup"))
        if use_windows and f"ic_ventanas_{k}_inf" in r and not math.isnan(_f(r.get(f"ic_ventanas_{k}_inf"))):
            lo = min(lo, _f(r[f"ic_ventanas_{k}_inf"]))
            hi = max(hi, _f(r[f"ic_ventanas_{k}_sup"]))
        return lo, hi
    e_lo, e_hi = ci("E")
    b_lo, b_hi = ci("B")
    g_lo, g_hi = ci("G")
    if math.isnan(e_lo):
        return "sin datos", ""
    if e_lo <= P_INTRA:
        dec = "dentro"
    elif e_lo > P_INTRA and not math.isnan(b_lo) and b_lo >= P_INTER:
        dec = "fuera"
    else:
        dec = "indeterminado"
    size = ""
    if dec == "fuera":
        size = "salto de género" if (not math.isnan(g_lo) and g_lo <= P_INTRA) else "cambio de autor"
    return dec, size


def nivel2(run_dir: str) -> dict[str, dict]:
    out = {}
    per_metric = {m: {r["id"]: r for r in _read(os.path.join(run_dir, f"bootstrap_percentil_{m}.csv"))} for m in ("minmax", "delta")}
    for L in letters_in(run_dir):
        decs = {}
        for m in ("minmax", "delta"):
            r = per_metric[m].get(L)
            if r:
                use_w = "ic_ventanas_E_inf" in r
                decs[m] = _decision_metric(r, use_w)
        if not decs:
            continue
        ds = {d for d, _ in decs.values()}
        if len(ds) == 1:
            dec = next(iter(ds))
        else:
            dec = "indeterminado"
        sizes = {s for _, s in decs.values() if s}
        size = next(iter(sizes)) if len(sizes) == 1 else ("|".join(sorted(sizes)) if sizes else "")
        row = {"nivel2": dec, "nivel2_tamano": size if dec == "fuera" else ""}
        for m in ("minmax", "delta"):
            r = per_metric[m].get(L, {})
            row.update({f"pct_E_{m}": _f(r.get("pct_E")), f"icE_{m}": f"{_f(r.get('ic_autores_E_inf')):.2f}-{_f(r.get('ic_autores_E_sup')):.2f}" if r else "",
                        f"pct_B_{m}": _f(r.get("pct_B")), f"pct_G_{m}": _f(r.get("pct_G")),
                        f"decision_{m}": decs.get(m, ("", ""))[0]})
        out[L] = row
    return out


def nivel3(run_dir: str) -> dict[str, dict]:
    out = {}
    per_metric = {m: {r["id"]: r for r in _read(os.path.join(run_dir, f"nearest_author_{m}.csv"))} for m in ("minmax", "delta")}
    for L in letters_in(run_dir):
        rs = {m: per_metric[m].get(L) for m in ("minmax", "delta") if per_metric[m].get(L)}
        if not rs:
            continue
        first = all(int(r["rank_nucleo"]) == 1 for r in rs.values())
        neg_margin = all(_f(r["margen_nucleo_menos_mejor_otro"]) < 0 and r.get("margen_ic_incluye_0", "") == "False"
                         for r in rs.values())
        out[L] = {"nivel3": "pasa" if (first and neg_margin) else ("no pasa" if not first else "indeterminado (IC del margen incluye 0)"),
                  **{f"rank_nucleo_{m}": int(r["rank_nucleo"]) for m, r in rs.items()},
                  **{f"mejor_otro_{m}": r["mejor_otro_autor"] for m, r in rs.items()},
                  **{f"margen_{m}": _f(r["margen_nucleo_menos_mejor_otro"]) for m, r in rs.items()},
            **{f"margen_ic_{m}": f"{_f(r.get('margen_ic_inf')):+.4f}..{_f(r.get('margen_ic_sup')):+.4f}" for m, r in rs.items()}}
    return out


def nivel4(run_dir: str, n1: dict, n2: dict) -> dict[str, dict]:
    """Robustez: por cada bloque de sensibilidad con resultados, ¿se mantienen el signo del nivel 1 (familia impostores)
    y la decisión del nivel 2 (min-max)?"""
    out = {L: {"nivel4_configs": 0, "nivel4_mantienen": 0, "nivel4_cambian": ""} for L in letters_in(run_dir)}
    for bdir in sorted(glob.glob(os.path.join(run_dir, "sensibilidad", "*"))):
        name = os.path.basename(bdir)
        summ = {r["id"]: r for r in _read(os.path.join(bdir, "summary_by_letter.csv")) if r.get("family") == "impostores"}
        boot = {r["id"]: r for r in _read(os.path.join(bdir, "bootstrap_percentil_minmax.csv"))}
        for L in out:
            if L not in n1 or (L not in summ and L not in boot):
                continue
            changed = []
            if L in summ:
                v = _f(summ[L].get("log10lr_epist_median"))
                ref = n1[L]["log10lr_epist_mediana_familias"]
                if not math.isnan(v) and not math.isnan(ref) and (v > 0) != (ref > 0) and abs(v) >= 0.3:
                    changed.append("signo LR")
            if L in boot and L in n2:
                d, _ = _decision_metric(boot[L], "ic_ventanas_E_inf" in boot[L])
                if d != n2[L]["nivel2"]:
                    changed.append(f"nivel 2 → {d}")
            out[L]["nivel4_configs"] += 1
            if changed:
                out[L]["nivel4_cambian"] += f"{name} ({'; '.join(changed)}); "
            else:
                out[L]["nivel4_mantienen"] += 1
    for L in out:
        c = out[L]["nivel4_configs"]
        out[L]["nivel4_proporcion"] = round(out[L]["nivel4_mantienen"] / c, 3) if c else float("nan")
    return out


def patron(n1: dict, n2: dict, n3: dict) -> str:
    """Tabla de § 8.5: del resultado estilométrico a las hipótesis."""
    l1, l2, l3 = n1.get("nivel1", ""), n2.get("nivel2", ""), n3.get("nivel3", "")
    if l2 == "indeterminado" or l1 in ("sin datos", ""):
        return "indeterminado: compatible con cualquiera"
    if l2 == "dentro" and "mismo-autor" in l1 and l3 == "pasa":
        return "dentro del rango, LR a favor, núcleo el más próximo: compatible con H1-H3; no con H5; H4 improbable"
    if l2 == "dentro" and l1 == "discordante":
        return "dentro del rango con familias discordantes: compatible con H2-H3; no con H5"
    if l2 == "fuera" and n2.get("nivel2_tamano") == "salto de género":
        return "fuera del rango pero del tamaño de un salto de género: no decide (H1-H4)"
    if l2 == "fuera" and l3 == "no pasa":
        return "fuera del rango del tamaño de un cambio de autor, núcleo no el más próximo: compatible con H4-H5; no con H1"
    if l2 == "fuera":
        return "fuera del rango del tamaño de un cambio de autor, núcleo aún el más próximo: compatible con H3-H4; H1 improbable"
    if l2 == "dentro" and "otro-autor" in l1:
        return "dentro del rango con LR en contra: discordancia entre niveles; se informa sin decidir"
    return "dentro del rango, LR no discriminante: compatible con H1-H3; H5 improbable"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    n1, n2, n3 = nivel1(run_dir), nivel2(run_dir), nivel3(run_dir)
    n4 = nivel4(run_dir, n1, n2)
    rows = []
    for L in letters_in(run_dir):
        if L not in n1 and L not in n2:
            continue
        r = {"carta": L, "kind": n1.get(L, {}).get("kind", "")}
        r.update(n1.get(L, {}))
        r.update(n2.get(L, {}))
        r.update(n3.get(L, {}))
        r.update(n4.get(L, {}))
        r["patron_8_5"] = patron(n1.get(L, {}), n2.get(L, {}), n3.get(L, {}))
        revisar = []
        if n1.get(L, {}).get("nivel1_concordancia") == "discordante":
            revisar.append("una familia apta que cambiara de signo")
        if n2.get(L, {}).get("nivel2") == "indeterminado":
            revisar.append("un IC del percentil que dejara de cruzar 0,90 (más autores en la envolvente)")
        if n2.get(L, {}).get("nivel2") == "dentro":
            revisar.append("un IC de pct_E entero por encima de 0,90 en ambas medidas con pct_B >= 0,10")
        if n2.get(L, {}).get("nivel2") == "fuera":
            revisar.append("un IC de pct_E que incluyera 0,90 en cualquiera de las dos medidas")
        if n3.get(L, {}).get("nivel3") == "pasa":
            revisar.append(f"que {n3[L].get('mejor_otro_minmax', '')} pasara por delante del núcleo")
        if n4.get(L, {}).get("nivel4_cambian"):
            revisar.append("las configuraciones de sensibilidad que ya lo cambian: " + n4[L]["nivel4_cambian"].strip("; "))
        r["que_revisaria_este_juicio"] = "; ".join(revisar)
        rows.append(r)
    _write_csv(os.path.join(run_dir, "veredicto.csv"), rows)
    with open(os.path.join(run_dir, "veredicto.md"), "w", encoding="utf-8") as f:
        f.write("# Veredicto mecánico por carta (PROTOCOLO § 8)\n\n")
        f.write("| carta | tipo | nivel 1 (posibilidad) | log10 LR epist. (mediana familias) | nivel 2 (plausibilidad) | "
                "nivel 3 (núcleo más próximo) | nivel 4 (robustez) | patrón § 8.5 |\n|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            n4s = f"{r.get('nivel4_mantienen', 0)}/{r.get('nivel4_configs', 0)}" if r.get("nivel4_configs") else "—"
            l2 = r.get("nivel2", "")
            if r.get("nivel2_tamano"):
                l2 += f" ({r['nivel2_tamano']})"
            med = r.get("log10lr_epist_mediana_familias", float("nan"))
            f.write(f"| {r['carta']} | {r['kind']} | {r.get('nivel1', '')} | {med:.2f} | {l2} | {r.get('nivel3', '')}"
                    f" (mejor otro: {r.get('mejor_otro_minmax', '')}) | {n4s} | {r['patron_8_5']} |\n")
        f.write("\nQué revisaría cada juicio:\n\n")
        for r in rows:
            f.write(f"- **{r['carta']}**: {r['que_revisaria_este_juicio'] or '—'}\n")
    print(f"veredicto: {len(rows)} cartas → {os.path.join(run_dir, 'veredicto.csv')}")
    for r in rows:
        print(f"  {r['carta']:5s} N1 {r.get('nivel1', ''):32s} N2 {r.get('nivel2', ''):14s} N3 {r.get('nivel3', ''):8s} → {r['patron_8_5']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
report.py — informe automático (Markdown) y figuras a partir de results/<run>/.

Produce results/<run>/informe/INFORME_AUTOMATICO.md y las figuras fig_*.png (panorama GI por carta,
calibración por especificación, familias de rasgos en las seis discutidas, mismo rasero, rolling).
El informe automático es una lectura mecánica de las tablas; la interpretación (informe final)
la escribe el investigador.
"""
from __future__ import annotations

import csv
import json
import math
import os

import numpy as np

from . import __version__
from .pipeline import LETTERS_13, _read_csv
from .sources import TARGETS


def _f(v, nd=3):
    if v is None or v == "":
        return "—"
    if isinstance(v, str):
        try:
            x = float(v)
        except ValueError:
            return v
        if v.strip().lstrip("-").isdigit():
            return v
        return "—" if math.isnan(x) else f"{x:.{nd}f}"
    try:
        x = float(v)
        return "—" if math.isnan(x) else f"{x:.{nd}f}"
    except (TypeError, ValueError):
        return str(v)


def _table(rows: list[dict], cols: list[str], names: list[str] | None = None, nd=3) -> str:
    names = names or cols
    out = ["| " + " | ".join(names) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(_f(r.get(c), nd) for c in cols) + " |")
    return "\n".join(out)


def figures(run_dir: str, out_dir: str) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    made = []
    summ = _read_csv(os.path.join(run_dir, "summary_by_letter.csv"))
    if summ:
        ids = [r["id"] for r in summ]
        med = [float(r["score_median"]) for r in summ]
        lo = [float(r["score_min"]) for r in summ]
        hi = [float(r["score_max"]) for r in summ]
        fig, ax = plt.subplots(figsize=(9, 3.8))
        colors = ["#4a6fa5" if r["kind"] == "core_loo" else "#c0504d" for r in summ]
        ax.bar(ids, med, color=colors, alpha=0.85)
        ax.errorbar(ids, med, yerr=[np.array(med) - np.array(lo), np.array(hi) - np.array(med)], fmt="none",
                    ecolor="black", capsize=3, lw=0.8)
        ax.axhline(0.5, ls="--", c="grey", lw=0.8)
        ax.set_ylim(0, 1)
        ax.set_ylabel("GI (mediana; barras: mín-máx)")
        ax.set_title("Panorama: puntuación GI por carta (azul núcleo LOO, rojo discutidas)")
        fig.tight_layout()
        p = os.path.join(out_dir, "fig_overview.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        made.append(p)
    cal = _read_csv(os.path.join(run_dir, "calibration_by_spec.csv"))
    if cal:
        fig, ax = plt.subplots(figsize=(9, 3.5))
        ax.plot([float(r["auc"]) for r in cal], "o-", label="AUC")
        ax.plot([float(r["c_at_1"]) for r in cal], "s-", label="c@1")
        ax.axhline(0.8, ls="--", c="grey", lw=0.8)
        ax.set_xlabel("especificación (índice)")
        ax.set_ylim(0.5, 1.0)
        ax.legend()
        ax.set_title("Calibración por especificación")
        fig.tight_layout()
        p = os.path.join(out_dir, "fig_calibration.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        made.append(p)
    fam = _read_csv(os.path.join(run_dir, "gi_targets_por_especificacion.csv"))
    if fam:
        feats = sorted({r["features"] for r in fam})
        fig, ax = plt.subplots(figsize=(9, 3.8))
        w = 0.8 / max(len(feats), 1)
        for i, ft in enumerate(feats):
            vals = []
            for t in TARGETS:
                v = [float(r[t]) for r in fam if r["features"] == ft and r.get(t) not in ("", None)]
                vals.append(np.median(v) if v else np.nan)
            ax.bar(np.arange(len(TARGETS)) + i * w, vals, width=w, label=ft)
        ax.set_xticks(np.arange(len(TARGETS)) + w * (len(feats) - 1) / 2)
        ax.set_xticklabels(TARGETS)
        ax.axhline(0.5, ls="--", c="grey", lw=0.8)
        ax.set_ylim(0, 1)
        ax.legend(fontsize=8)
        ax.set_title("Seis cartas discutidas: GI mediana por familia de rasgos")
        fig.tight_layout()
        p = os.path.join(out_dir, "fig_families.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        made.append(p)
    led = _read_csv(os.path.join(run_dir, "double_standard_ledger_minmax.csv"))
    env = _read_csv(os.path.join(run_dir, "pair_distances_minmax.csv"))
    if led and env:
        fig, ax = plt.subplots(figsize=(9, 3.8))
        ax.hist([float(r["distance"]) for r in env], bins=30, color="#bbbbbb", label="pares intra-autor (controles)")
        for r in led:
            ax.axvline(float(r["d_mean"]), c="#c0504d" if r["kind"] == "target" else "#4a6fa5", lw=1)
            ax.text(float(r["d_mean"]), ax.get_ylim()[1] * 0.9, r["id"], rotation=90, fontsize=7, va="top")
        ax.set_xlabel("distancia min-max (ventanas de 500, media de 20 sorteos)")
        ax.set_title("Mismo rasero: distancia de cada carta al núcleo dentro de la envolvente intra-autor")
        ax.legend(fontsize=8)
        fig.tight_layout()
        p = os.path.join(out_dir, "fig_same_standard.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        made.append(p)
    roll = _read_csv(os.path.join(run_dir, "rolling_scores.csv"))
    if roll:
        letters = [L for L in LETTERS_13 if any(r["id"] == L for r in roll)]
        fig, axes = plt.subplots(len(letters), 1, figsize=(9, 1.2 * len(letters) + 1), sharex=False)
        if len(letters) == 1:
            axes = [axes]
        for ax, L in zip(axes, letters):
            rs = [r for r in roll if r["id"] == L]
            ax.plot([int(r["start"]) for r in rs], [float(r["score"]) for r in rs], "-o", ms=2, lw=0.8)
            ax.axhline(0.5, ls="--", c="grey", lw=0.6)
            ax.set_ylim(0, 1)
            ax.set_ylabel(L, rotation=0, labelpad=18, fontsize=8)
            ax.tick_params(labelsize=7)
        axes[0].set_title("Ventanas deslizantes (400 palabras, paso 100): GI por tramo")
        fig.tight_layout()
        p = os.path.join(out_dir, "fig_rolling.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        made.append(p)
    return made


def build_report(run_dir: str) -> str:
    out_dir = os.path.join(run_dir, "informe")
    os.makedirs(out_dir, exist_ok=True)
    cfg = {}
    cp = os.path.join(run_dir, "config_used.json")
    if os.path.exists(cp):
        with open(cp, encoding="utf-8") as f:
            cfg = json.load(f)
    figs = figures(run_dir, out_dir)
    cal = _read_csv(os.path.join(run_dir, "calibration_by_spec.csv"))
    summ = _read_csv(os.path.join(run_dir, "summary_by_letter.csv"))
    lrl = _read_csv(os.path.join(run_dir, "lr_secundaria_por_carta.csv"))
    led_mm = _read_csv(os.path.join(run_dir, "double_standard_ledger_minmax.csv"))
    led_d = _read_csv(os.path.join(run_dir, "double_standard_ledger_delta.csv"))
    fam = _read_csv(os.path.join(run_dir, "gi_targets_por_especificacion.csv"))
    perm = _read_csv(os.path.join(run_dir, "permanova_pauline_windows.csv"))
    noise = _read_csv(os.path.join(run_dir, "edition_noise_pairs.csv"))
    contrib = _read_csv(os.path.join(run_dir, "feature_contributions.csv"))
    roll = _read_csv(os.path.join(run_dir, "rolling_scores.csv"))
    sec = _read_csv(os.path.join(run_dir, "calibracion_secundaria_cristiana.csv"))
    all_rows = _read_csv(os.path.join(run_dir, "gi_results_all_specs.csv"))

    md = [f"# Informe automático · {os.path.basename(run_dir)}", "",
          f"Generado por paulinum {__version__} (reconstrucción). Configuración: `{cfg.get('nombre', '')}` — {cfg.get('descripcion', '')}",
          "", "Este informe es una lectura mecánica de las tablas de results/. La interpretación corresponde al informe final.", ""]
    if cal:
        aucs = [float(r["auc"]) for r in cal if r["auc"]]
        md += ["## 1. Calibración por especificación", "",
               f"{len(cal)} especificaciones; AUC {min(aucs):.3f}–{max(aucs):.3f} (mediana {np.median(aucs):.3f}); "
               f"válidas (AUC ≥ {cfg.get('parametros', {}).get('auc_minima', 0.8)}): {sum(1 for r in cal if r['valid'] == 'True')}.",
               "", _table(cal, ["spec_index", "dia", "features", "metric", "window", "mask", "n_pos", "n_neg", "auc", "c_at_1",
                                "thr_low", "thr_high", "fpr_at_0.5", "fnr_at_0.5"]), ""]
        if sec:
            md += ["Calibración secundaria (negativos cristianos):", "",
                   _table(sec, ["spec_index", "features", "metric", "mask", "n_neg_cristianos", "auc_cristiana",
                                "auc_cristiana_pos_cristianos", "fpr_cristiana_0.5"]), ""]
    if summ:
        md += ["## 2. Resumen por carta (especificaciones válidas)", "", "![panorama](fig_overview.png)", "",
               _table(summ, ["id", "kind", "n_specs", "score_median", "score_q1", "score_q3", "score_min", "score_max",
                             "frac_specs_ge_0_5", "log10lr_median", "log10lr_q1", "log10lr_q3"]), ""]
    if lrl:
        md += ["## 3. Razones de verosimilitud (log10) con todos los negativos y con negativos cristianos", "",
               _table(lrl, ["target", "log10lr_principal_mediana", "log10lr_cristiana_mediana", "log10lr_cristiana_q1",
                            "log10lr_cristiana_q3", "log10lr_cristiana_min", "log10lr_cristiana_max", "verbal_cristiana_mediana",
                            "log10lr_cj_mediana"]), ""]
    if fam:
        md += ["## 4. Seis cartas discutidas por familia de rasgos, distancia y máscara", "", "![familias](fig_families.png)", "",
               _table(fam, ["features", "metric", "mask", "window", "dia"] + TARGETS), ""]
    if led_mm:
        dd = {r["id"]: r for r in led_d}
        rows = [{**r, "pct_delta": dd.get(r["id"], {}).get("percentile")} for r in led_mm]
        md += ["## 5. Mismo rasero", "", "![mismo rasero](fig_same_standard.png)", "",
               f"Envolvente intra-autor (min-max): {led_mm[0].get('env_n_pairs')} pares; mín {_f(led_mm[0].get('env_min'))}, "
               f"Q1 {_f(led_mm[0].get('env_q1'))}, mediana {_f(led_mm[0].get('env_median'))}, Q3 {_f(led_mm[0].get('env_q3'))}, "
               f"máx {_f(led_mm[0].get('env_max'))}.", "",
               _table(rows, ["id", "kind", "d_mean", "d_min", "d_max", "percentile", "pct_delta"],
                      ["carta", "tipo", "d media min-max", "d mín", "d máx", "percentil min-max", "percentil Delta"]), "",
               "Regla preregistrada: ninguna carta se declara anómala si su percentil intra-autor es ≤ 0,90.", ""]
    if perm:
        md += ["## 6. Variables de situación dentro del corpus paulino (PERMANOVA, ventanas de 400)", "",
               _table(perm, ["variable", "n", "k", "R2", "pseudo_F", "p"]), ""]
    if noise:
        md += ["## 7. Ruido de edición (duplicados frente al original, min-max, mfw:300)", "",
               _table(noise, ["duplicate", "original", "author", "d_minmax_mfw300"]), ""]
    if contrib:
        md += ["## 8. Rasgos que separan (z frente a la dispersión interna del núcleo, mfw:300, ‰)", ""]
        for L in LETTERS_13:
            rs = [r for r in contrib if r["id"] == L]
            if rs:
                md.append(f"**{L}**: " + "; ".join(f"{r['feature']} ({r['permil_letter']} ‰ vs {r['permil_core_mean']} ‰, z={r['z_vs_core']})"
                                                   for r in rs[:10]))
                md.append("")
    if roll:
        md += ["## 9. Ventanas deslizantes", "", "![rolling](fig_rolling.png)", ""]
        for L in LETTERS_13:
            rs = [r for r in roll if r["id"] == L]
            if rs:
                sc = [float(r["score"]) for r in rs]
                low = [r for r in rs if float(r["score"]) < 0.5]
                md.append(f"- {L}: {len(rs)} ventanas, mediana {np.median(sc):.2f}, mín {min(sc):.2f} "
                          f"({len(low)} por debajo de 0,5" + (": " + "; ".join(f"{r['ref_start']}–{r['ref_end']}" for r in low[:5]) if low else "") + ")")
        md.append("")
    if all_rows:
        negs = [r for r in all_rows if r["kind"] == "neg_target" and r["score"]]
        by_t = {}
        for r in negs:
            by_t.setdefault(r["target"], []).append(float(r["score"]))
        med = sorted(((t, float(np.median(v))) for t, v in by_t.items()), key=lambda x: -x[1])
        passing = [(t, m) for t, m in med if m >= 0.5]
        md += ["## 10. Negativos frente al núcleo con mediana GI ≥ 0,5", "",
               f"{len(passing)} de {len(med)} textos no paulinos.", "",
               "| texto | mediana GI |", "|---|---|"] + [f"| {t} | {m:.3f} |" for t, m in passing] + [""]
        ps = [r for r in all_rows if r["kind"] == "pseudo_pairs" and r["score"]]
        by_p = {}
        for r in ps:
            by_p.setdefault(r["target"], []).append(float(r["score"]))
        if by_p:
            md += ["Pseudoepigrafías conocidas frente al autor imitado (mediana, mín, máx entre especificaciones):", "",
                   "| pseudoepígrafo | mediana | mín | máx |", "|---|---|---|---|"]
            md += [f"| {t} | {np.median(v):.3f} | {min(v):.3f} | {max(v):.3f} |" for t, v in sorted(by_p.items())]
            md.append("")
    md += ["## Archivos", "", "Figuras: " + ", ".join(os.path.basename(p) for p in figs), ""]
    path = os.path.join(out_dir, "INFORME_AUTOMATICO.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    return path

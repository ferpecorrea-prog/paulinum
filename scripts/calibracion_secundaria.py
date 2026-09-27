#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibracion_secundaria.py — razón de verosimilitud con negativos cristianos (o cristianos y
judeo-helenísticos) a partir de results/<run>/specs/*.json.

Regla preregistrada: además de la LR con todos los negativos, se informa la LR recalculada con los
negativos restringidos a textos cristianos (tradition == cristiano) y, en la campaña 03, con cristianos
+ judeo-helenísticos (sufijo _cj). Salidas en results/<run>/:
  calibracion_secundaria_cristiana.csv, calibracion_secundaria_cristiana_cj.csv (AUC y FPR por especificación)
  lr_secundaria_por_spec.csv, lr_secundaria_por_spec_cj.csv (LR por carta y especificación)
  lr_secundaria_por_carta.csv, lr_secundaria_por_carta_cj.csv (mediana, Q1-Q3, mín-máx, escala verbal)

Uso: python scripts/calibracion_secundaria.py --run campana_03
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.verify import LRCalibrator, auc, verbal  # noqa: E402
from paulinum.pipeline import _write_csv, LETTERS_13  # noqa: E402


def run(run_dir: str, traditions: tuple[str, ...], suffix: str) -> None:
    tag = "cristiana" if not suffix else "cj"
    rows_cal, rows_spec, per_letter = [], [], {L: [] for L in LETTERS_13}
    per_letter_main = {L: [] for L in LETTERS_13}
    kinds = {}
    for path in sorted(glob.glob(os.path.join(run_dir, "specs", "*.json"))):
        o = json.load(open(path, encoding="utf-8"))
        res = o["results"]
        s = o["spec"]
        valid = o["calibration"]["valid"]
        pos = np.array([r["score"] for r in res if r["label"] == 1 and not math.isnan(r["score"])])
        neg = np.array([r["score"] for r in res if r["label"] == 0 and r.get("tradition") in traditions
                        and not math.isnan(r["score"])])
        posc = np.array([r["score"] for r in res if r["label"] == 1 and r.get("tradition") in traditions
                         and not math.isnan(r["score"])])
        rows_cal.append({"spec_index": s["index"], "label": o["label"], "features": s["features"], "metric": s["metric"],
                         "window": s["window"] or "all", "mask": s["mask"], "n_pos": len(pos), ("n_neg_cristianos" if tag == "cristiana" else "n_neg_cj"): len(neg),
                         f"auc_{tag}": auc(pos, neg), ("auc_cristiana_pos_cristianos" if tag == "cristiana" else "auc_cj_pos_cj"): auc(posc, neg),
                         f"fpr_{tag}_0.5": float((neg >= 0.5).mean()) if len(neg) else float("nan"),
                         "fnr_at_0.5": float((pos < 0.5).mean()) if len(pos) else float("nan"), "valid": valid})
        cal = LRCalibrator(pos, neg)
        for r in res:
            if r["kind"] in ("target", "core_loo") and not math.isnan(r["score"]):
                lr = cal.log10lr(r["score"])
                rows_spec.append({"spec_index": s["index"], "label": o["label"], "features": s["features"],
                                  "metric": s["metric"], "window": s["window"] or "all", "mask": s["mask"],
                                  "target": r["target"], "kind": r["kind"], "score": r["score"], "log10lr": lr,
                                  "verbal": verbal(lr), "valid": valid})
                if valid and r["target"] in per_letter:
                    per_letter[r["target"]].append(lr)
                    kinds[r["target"]] = r["kind"]
                    if r.get("log10lr") is not None and not math.isnan(r.get("log10lr", float("nan"))):
                        per_letter_main[r["target"]].append(r["log10lr"])
    rows_letter = []
    for L, v in per_letter.items():
        if not v:
            continue
        v = np.array(v)
        vm = np.array(per_letter_main[L])
        rows_letter.append({"target": L, "kind": kinds.get(L, ""), "n_specs": len(v),
                            "log10lr_principal_mediana": float(np.median(vm)) if len(vm) else float("nan"),
                            f"log10lr_{tag}_mediana": float(np.median(v)),
                            f"log10lr_{tag}_q1": float(np.percentile(v, 25)), f"log10lr_{tag}_q3": float(np.percentile(v, 75)),
                            f"log10lr_{tag}_min": float(v.min()), f"log10lr_{tag}_max": float(v.max()),
                            f"verbal_{tag}_mediana": verbal(float(np.median(v)))})
    _write_csv(os.path.join(run_dir, f"calibracion_secundaria_cristiana{suffix}.csv"), rows_cal)
    _write_csv(os.path.join(run_dir, f"lr_secundaria_por_spec{suffix}.csv"), rows_spec)
    _write_csv(os.path.join(run_dir, f"lr_secundaria_por_carta{suffix}.csv"), rows_letter)
    print(f"{suffix or '_cristiana'}: {len(rows_cal)} especificaciones; negativos {traditions}")
    for r in rows_letter:
        print(f"  {r['target']:5s} log10LR mediana {r[f'log10lr_{tag}_mediana']:+.3f} [{r[f'log10lr_{tag}_q1']:+.3f}, {r[f'log10lr_{tag}_q3']:+.3f}] "
              f"({r[f'log10lr_{tag}_min']:+.3f}…{r[f'log10lr_{tag}_max']:+.3f}) {r[f'verbal_{tag}_mediana']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    run(run_dir, ("cristiano",), "")
    run(run_dir, ("cristiano", "judeo-helenistico"), "_cj")
    # el archivo principal lleva también la mediana cristianos + judeo-helenísticos (columna del Apéndice A.4.2)
    import csv
    main_p = os.path.join(run_dir, "lr_secundaria_por_carta.csv")
    cj_p = os.path.join(run_dir, "lr_secundaria_por_carta_cj.csv")
    if os.path.getsize(main_p) and os.path.getsize(cj_p):
        cj = {r["target"]: r["log10lr_cj_mediana"] for r in csv.DictReader(open(cj_p, encoding="utf-8"))}
        rows = list(csv.DictReader(open(main_p, encoding="utf-8")))
        for r in rows:
            r["log10lr_cj_mediana"] = cj.get(r["target"], "")
        _write_csv(main_p, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())

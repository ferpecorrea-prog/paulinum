#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py — ejecuta la secuencia completa de una campaña (las órdenes del Apéndice A.1) y anota cada paso.

Uso: python scripts/run_all.py --config config/campana_03.yaml --run campana_03 [--tier 3] [--diorisis-zip ruta]
     python scripts/run_all.py --config config/prueba_reducida.yaml --run prueba_reducida --tier 1
Pasos: fetch → build → inventory → (construir_lexicon si hay --diorisis-zip o lemma_dict en la rejilla) →
detectar_reutilizacion → variables_controles → seal → run → calibracion_secundaria → bootstrap_percentil
(minmax y delta) → modelo_svm → cobertura_lexicon → controles_genero → lectura_modelo_svm → report.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

import yaml

PY = sys.executable


def sh(cmd: list[str], bit: str) -> None:
    t0 = time.time()
    print("\n$ " + " ".join(cmd), flush=True)
    rc = subprocess.call(cmd)
    with open(bit, "a", encoding="utf-8") as f:
        f.write(f"| {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t0))} | {' '.join(cmd)} | {time.time() - t0:,.1f} s | rc={rc} |\n")
    if rc != 0:
        print(f"[run_all] la orden devolvió {rc}; se continúa con las siguientes", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run", default=None)
    ap.add_argument("--tier", type=int, default=None)
    ap.add_argument("--diorisis-zip", default="")
    ap.add_argument("--sin-bootstrap-ventanas", action="store_true")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    run = a.run or cfg["nombre"]
    tier = a.tier or int(cfg.get("corpus", {}).get("tier", 1))
    os.makedirs(os.path.join("results", run), exist_ok=True)
    bit = os.path.join("results", run, "bitacora.md")
    if not os.path.exists(bit):
        open(bit, "w", encoding="utf-8").write(f"# Bitácora de {run}\n\n| inicio (UTC) | orden / etapa | duración | nota |\n|---|---|---|---|\n")
    editions = cfg.get("rejilla", {}).get("ediciones", ["sblgnt"])
    fetch = [PY, "-m", "paulinum", "fetch", "--tier", str(tier)]
    if len(editions) > 1:
        fetch.append("--editions")
    sh(fetch, bit)
    sh([PY, "-m", "paulinum", "build", "--config", a.config], bit)
    sh([PY, "-m", "paulinum", "inventory", "--config", a.config, "--run", run], bit)
    needs_lex = any(r.startswith("lemma_dict") for r in cfg.get("rejilla", {}).get("rasgos", []))
    if needs_lex or a.diorisis_zip:
        lex = [PY, "scripts/construir_lexicon.py"]
        if a.diorisis_zip:
            lex += ["--diorisis-zip", a.diorisis_zip]
        sh(lex, bit)
    sh([PY, "scripts/detectar_reutilizacion.py", "--run", run, "--comparar"], bit)
    sh([PY, "scripts/variables_controles.py", "--run", run], bit)
    sh([PY, "-m", "paulinum", "seal", "--config", a.config, "--run", run], bit)
    sh([PY, "-m", "paulinum", "run", "--config", a.config, "--run", run], bit)
    sh([PY, "scripts/calibracion_secundaria.py", "--run", run], bit)
    for m in ("minmax", "delta"):
        cmd = [PY, "scripts/bootstrap_percentil.py", "--run", run, "--metric", m, "--config", a.config]
        if a.sin_bootstrap_ventanas:
            cmd.append("--sin-ventanas")
        sh(cmd, bit)
    feats = ",".join(cfg.get("segundo_modelo", {}).get("rasgos", cfg.get("rejilla", {}).get("rasgos", ["mfw:300"])))
    sh([PY, "scripts/modelo_svm.py", "--run", run, "--features", feats], bit)
    if needs_lex:
        sh([PY, "scripts/cobertura_lexicon.py", "--run", run], bit)
    sh([PY, "scripts/controles_genero.py", "--run", run], bit)
    sh([PY, "scripts/lectura_modelo_svm.py", "--run", run], bit)
    sh([PY, "-m", "paulinum", "report", "--run", run], bit)
    print(f"\nrun_all: terminado → results/{run}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

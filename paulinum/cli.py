# -*- coding: utf-8 -*-
"""
cli.py — órdenes: fetch, build, inventory, selftest, seal, run, report.

  python -m paulinum fetch --tier 2 [--force] [--editions]
  python -m paulinum build --config config/default.yaml [--edition sblgnt]
  python -m paulinum inventory --config config/default.yaml
  python -m paulinum selftest
  python -m paulinum seal --config config/campana_03.yaml --run campana_03
  python -m paulinum run --config config/campana_03.yaml [--run campana_03] [--stage specs,calibration,...]
  python -m paulinum report --run campana_03

El sello (seal) es la huella SHA-256 del conjunto ordenado de archivos que fija el protocolo:
los módulos de paulinum/, los archivos de metadata/, la configuración con su bloque de preregistro,
scripts/*.py (campañas 03 y de prueba) y data/cache/lexicon_uniforme.tsv cuando la rejilla usa lemma_dict. Se escribe en
results/PROTOCOLO_SELLADO_<run>.json con la lista de archivos y la huella de cada uno.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import hashlib
import json
import os
import subprocess
import sys

from . import __version__


def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def seal(config_path: str, run_name: str, results_dir: str = "results", include_scripts: bool | None = None,
         include_lexicon: bool | None = None) -> dict:
    root = os.getcwd()
    files = sorted(glob.glob(os.path.join("paulinum", "*.py")))
    files += sorted(glob.glob(os.path.join("metadata", "*.csv")))
    files.append(config_path)
    if include_scripts is None:
        include_scripts = "03" in run_name or "prueba" in run_name
    if include_scripts:
        files += sorted(glob.glob(os.path.join("scripts", "*.py")))
    lex = os.path.join("data", "cache", "lexicon_uniforme.tsv")
    if include_lexicon is None:
        # el lexicón entra en el sello solo cuando la rejilla usa lemma_dict (campaña 03)
        with open(config_path, encoding="utf-8") as f:
            include_lexicon = "lemma_dict" in f.read()
    if include_lexicon:
        if not os.path.exists(lex):
            raise SystemExit(f"la configuración usa lemma_dict y falta {lex}: ejecute scripts/construir_lexicon.py antes de sellar")
        files.append(lex)
    files = [f for f in dict.fromkeys(files) if os.path.exists(f)]
    h = hashlib.sha256()
    detail = {}
    for f in files:
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        fh = _sha(f)
        detail[rel] = fh
        h.update(rel.encode("utf-8") + b"\n" + bytes.fromhex(fh) + b"\n")
    sello = {"run": run_name, "config": config_path, "version": __version__,
             "sealed_utc": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
             "n_files": len(files), "files": detail, "sha256": h.hexdigest(),
             "nota": "Reconstrucción: este sello NO coincide con los sellos publicados en el libro (código original perdido)."}
    os.makedirs(results_dir, exist_ok=True)
    out = os.path.join(results_dir, f"PROTOCOLO_SELLADO_{run_name}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(sello, f, ensure_ascii=False, indent=1)
    print(f"sello {run_name}: {sello['sha256']} ({len(files)} archivos) → {out}")
    return sello


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="paulinum", description=f"paulinum {__version__} — verificación convergente")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("fetch", help="descargar textos y registrar huellas")
    p.add_argument("--tier", type=int, default=1)
    p.add_argument("--force", action="store_true")
    p.add_argument("--editions", action="store_true", help="descargar también PROIEL y MACULA")
    p.add_argument("--data", default="data")
    p = sub.add_parser("build", help="construir el corpus normalizado con máscaras")
    p.add_argument("--config", required=True)
    p.add_argument("--edition", default=None)
    p.add_argument("--data", default="data")
    p = sub.add_parser("inventory", help="inventario del corpus (results/<run>/inventory.csv)")
    p.add_argument("--config", required=True)
    p.add_argument("--run", default=None)
    p.add_argument("--data", default="data")
    sub.add_parser("selftest", help="pruebas de referencia (scripts/selftest.py)")
    p = sub.add_parser("seal", help="sellar el protocolo")
    p.add_argument("--config", required=True)
    p.add_argument("--run", required=True)
    p = sub.add_parser("run", help="ejecutar la campaña")
    p.add_argument("--config", required=True)
    p.add_argument("--run", default=None)
    p.add_argument("--stage", default=None, help="etapas separadas por comas")
    p.add_argument("--data", default="data")
    p = sub.add_parser("report", help="informe automático y figuras")
    p.add_argument("--run", required=True)
    a = ap.parse_args(argv)

    if a.cmd == "fetch":
        from .fetch import fetch_all
        fetch_all(tier=a.tier, data_dir=a.data, force=a.force, editions=a.editions)
        return 0
    if a.cmd == "build":
        from .pipeline import load_config
        from .corpus import build_corpus, save_corpus
        cfg = load_config(a.config)
        tier = int(cfg.get("corpus", {}).get("tier", 1))
        editions = [a.edition] if a.edition else cfg["rejilla"].get("ediciones", ["sblgnt"])
        for ed in editions:
            docs = build_corpus(tier=tier, edition_key=ed, data_dir=a.data)
            p = save_corpus(docs, ed, a.data)
            print(f"  → {p}")
        return 0
    if a.cmd == "inventory":
        from .pipeline import load_config, _write_csv
        from .corpus import load_corpus, inventory_rows
        cfg = load_config(a.config)
        run = a.run or cfg.get("nombre", "campana")
        ed = cfg.get("corpus", {}).get("edicion", "sblgnt")
        docs = load_corpus(ed, a.data)
        rows = inventory_rows(docs)
        os.makedirs(os.path.join("results", run), exist_ok=True)
        out = os.path.join("results", run, "inventory.csv")
        _write_csv(out, rows)
        from collections import Counter
        c = Counter((r["author"], r["tradition"], r["status"]) for r in rows)
        w = Counter()
        for r in rows:
            w[(r["author"], r["tradition"], r["status"])] += r["tokens"]
        print(f"{len(rows)} documentos, {sum(r['tokens'] for r in rows)} tokens → {out}")
        for k in sorted(c):
            print(f"  {k[0]:26s} {k[1]:18s} {k[2]:10s} {c[k]:4d} {w[k]:8d}")
        return 0
    if a.cmd == "selftest":
        return subprocess.call([sys.executable, os.path.join("scripts", "selftest.py")])
    if a.cmd == "seal":
        seal(a.config, a.run)
        return 0
    if a.cmd == "run":
        from .pipeline import run_campaign
        stages = a.stage.split(",") if a.stage else None
        run_campaign(a.config, a.run, stages, data_dir=a.data)
        return 0
    if a.cmd == "report":
        from .report import build_report
        p = build_report(os.path.join("results", a.run))
        print(f"informe → {p}")
        return 0
    return 1

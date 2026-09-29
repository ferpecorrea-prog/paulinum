#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sellar_resultados.py — huella del conjunto de resultados (Sello 3, PROTOCOLO § 3.3 y § 12).

Fuera del conjunto sellado del Sello 2 (no está en `scripts/` ni en `paulinum/`), porque el código congelado no
incluía un sello de resultados. Usa la misma convención que `python -m paulinum seal`: para cada archivo, en orden
de ruta, `ruta\\n` + SHA-256 binario + `\\n` alimentan una SHA-256 global. Entran todos los archivos versionados de `results/`
(campaña definitiva, run auxiliar de calibración, anotación, pruebas), salvo los parciales de reanudación (`*.parcial.jsonl`).

Uso: python herramientas/sellar_resultados.py --etiqueta resultados-1.0.0 [--raiz results] [--salida protocols/paulinum_1_0]
Comprobación: python herramientas/sellar_resultados.py --comprobar protocols/paulinum_1_0/SELLO_resultados-1.0.0.json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import subprocess
import sys


def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def listar(raiz: str) -> list[str]:
    """Archivos versionados bajo `raiz` (`git ls-files`), de modo que la huella es la del árbol de la etiqueta y no
    depende de archivos locales no versionados (`.npy` ignorados, parciales de reanudación); sin git, todos los
    archivos del disco salvo `*.parcial.jsonl`."""
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--", raiz], check=True, capture_output=True).stdout
        files = [f.decode("utf-8") for f in out.split(b"\0") if f]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for d, _, fs in os.walk(raiz):
            files += [os.path.join(d, f).replace(os.sep, "/") for f in fs]
    return sorted(f for f in files if not f.endswith(".parcial.jsonl") and os.path.exists(f))


def sellar(raiz: str) -> tuple[str, dict[str, str]]:
    h = hashlib.sha256()
    detail = {}
    for f in listar(raiz):
        fh = _sha(f)
        detail[f] = fh
        h.update(f.encode("utf-8") + b"\n" + bytes.fromhex(fh) + b"\n")
    return h.hexdigest(), detail


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etiqueta", default="resultados-1.0.0")
    ap.add_argument("--raiz", default="results")
    ap.add_argument("--salida", default=os.path.join("protocols", "paulinum_1_0"))
    ap.add_argument("--comprobar", default=None, help="ruta de un SELLO_<etiqueta>.json: recalcula y compara la huella")
    a = ap.parse_args()
    if a.comprobar:
        with open(a.comprobar, encoding="utf-8") as f:
            sello = json.load(f)
        sha, detail = sellar(sello.get("raiz", a.raiz))
        ok = sha == sello["sha256"]
        cambiados = sorted(set(detail) ^ set(sello["files"])) + sorted(k for k in detail if k in sello["files"] and detail[k] != sello["files"][k])
        print(f"huella registrada {sello['sha256']}\nhuella recalculada {sha}\n{'COINCIDEN' if ok else 'NO COINCIDEN'}"
              + (f" · archivos distintos o nuevos: {len(cambiados)}" if cambiados else ""))
        for k in cambiados[:40]:
            print("  ", k)
        return 0 if ok else 1
    sha, detail = sellar(a.raiz)
    sello = {"etiqueta": a.etiqueta, "raiz": a.raiz, "sello": 3,
             "sealed_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
             "n_files": len(detail), "files": detail, "sha256": sha,
             "nota": ("Sello 3 (resultados): huella de todos los archivos versionados de results/ (sin parciales de reanudación), "
                      "misma convención que `python -m paulinum seal`; reproducible con "
                      f"`python herramientas/sellar_resultados.py --etiqueta {a.etiqueta}` en la etiqueta de git indicada "
                      "(el campo sealed_utc cambia; la huella no).")}
    os.makedirs(a.salida, exist_ok=True)
    out = os.path.join(a.salida, f"SELLO_{a.etiqueta}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(sello, f, ensure_ascii=False, indent=1)
    print(f"{out}: {len(detail)} archivos · sha256 {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

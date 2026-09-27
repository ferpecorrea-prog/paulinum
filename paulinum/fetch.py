# -*- coding: utf-8 -*-
"""
fetch.py — descarga de los textos del manifiesto y registro de huellas en data/provenance.json.

Cada archivo se guarda en data/raw/<repo>/<ruta> y se anota con: url, sha256, bytes, fecha de
descarga y estado. Las descargas son idempotentes: un archivo ya presente con la huella registrada
no se vuelve a bajar salvo --force. `--tier N` limita el manifiesto (1: NT y Padres Apostólicos;
2: + controles de la campaña 01; 3: + ampliación de la campaña 03).
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import sys
import time

import requests

from .sources import ALL_SOURCES, EDITION_SOURCES, REPOS, Source, by_tier

DATA_DIR = os.environ.get("PAULINUM_DATA", "data")


def raw_path(src: Source, data_dir: str = DATA_DIR) -> str:
    if src.repo == "local":
        return os.path.join(data_dir, "local", src.path)
    return os.path.join(data_dir, "raw", src.repo, src.path)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_provenance(data_dir: str = DATA_DIR) -> dict:
    p = os.path.join(data_dir, "provenance.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"repos": REPOS, "files": {}}


def save_provenance(prov: dict, data_dir: str = DATA_DIR) -> None:
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "provenance.json"), "w", encoding="utf-8") as f:
        json.dump(prov, f, ensure_ascii=False, indent=1, sort_keys=True)


def download(url: str, dest: str, retries: int = 3, timeout: int = 120) -> tuple[bool, str]:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    last = ""
    for i in range(retries):
        try:
            r = requests.get(url, timeout=timeout, stream=True)
            if r.status_code == 200:
                tmp = dest + ".part"
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
                os.replace(tmp, dest)
                return True, ""
            last = f"HTTP {r.status_code}"
            if r.status_code == 404:
                break
        except requests.RequestException as e:  # pragma: no cover
            last = str(e)
        time.sleep(2 * (i + 1))
    return False, last


def fetch_all(tier: int = 1, data_dir: str = DATA_DIR, force: bool = False, quiet: bool = False,
              editions: bool = False) -> dict:
    prov = load_provenance(data_dir)
    sources = by_tier(tier)
    if editions:
        sources = sources + [s for s in EDITION_SOURCES.values() if s is not None]
    seen = set()
    ok = fail = skipped = 0
    for src in sources:
        key = f"{src.repo}/{src.path}"
        if key in seen:
            continue
        seen.add(key)
        dest = raw_path(src, data_dir)
        if src.repo == "local":
            if os.path.exists(dest):
                prov["files"][key] = {"url": "", "path": dest, "sha256": sha256_file(dest),
                                      "bytes": os.path.getsize(dest), "status": "local",
                                      "fetched": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"}
                ok += 1
            else:
                prov["files"][key] = {"url": "", "path": dest, "status": "missing_local",
                                      "note": "preparar a mano; véase data/local/LEEME_3Cor.md"}
                skipped += 1
                if not quiet:
                    print(f"  [local ausente] {dest}")
            continue
        if os.path.exists(dest) and not force and key in prov["files"] and prov["files"][key].get("status") == "ok":
            skipped += 1
            continue
        good, err = download(src.url, dest)
        if good:
            prov["files"][key] = {"url": src.url, "path": dest, "sha256": sha256_file(dest),
                                  "bytes": os.path.getsize(dest), "status": "ok",
                                  "fetched": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
                                  "license": REPOS[src.repo]["licencia"], "edition": src.edition}
            ok += 1
            if not quiet:
                print(f"  [ok] {key} ({prov['files'][key]['bytes']} bytes)")
        else:
            prov["files"][key] = {"url": src.url, "path": dest, "status": "error", "error": err}
            fail += 1
            print(f"  [ERROR] {key}: {err}", file=sys.stderr)
        save_provenance(prov, data_dir)
    save_provenance(prov, data_dir)
    print(f"fetch: {ok} descargados, {skipped} ya presentes/omitidos, {fail} errores → {data_dir}/provenance.json")
    return prov


def verify_provenance(data_dir: str = DATA_DIR) -> list[str]:
    """Recalcula las huellas de los archivos descargados y devuelve la lista de discrepancias."""
    prov = load_provenance(data_dir)
    bad = []
    for key, rec in prov["files"].items():
        if rec.get("status") not in ("ok", "local"):
            continue
        if not os.path.exists(rec["path"]):
            bad.append(f"{key}: archivo ausente")
        elif sha256_file(rec["path"]) != rec["sha256"]:
            bad.append(f"{key}: huella distinta")
    return bad

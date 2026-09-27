#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara los testigos manuscritos solicitados para el proyecto nuevo_paulinum.

Descarga:
1) Codex Sinaiticus, transcripción oficial publicada v1.05 (UBIRA/ITSEE).
2) P46 (GA P46, NTVMR docID 10046), transcripción TEI XML publicada.
3) Opcionalmente, Codex Sinaiticus desde NTVMR (docID 20001) para disponer
   de ambos testigos bajo el mismo esquema/API.

Solo usa la biblioteca estándar de Python.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

USER_AGENT = (
    "nuevo-paulinum-witness-fetch/1.0 "
    "(academic research; respectful NTVMR access)"
)

SINAITICUS_V105_ZIP = (
    "https://epapers.bham.ac.uk/id/eprint/3306/1/"
    "FINAL_TRANSCRIPTION_version105.xml.zip"
)

NTVMR_BASE = (
    "https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/"
)

P46_DOCID = "10046"
SINAITICUS_NTVMR_DOCID = "20001"

# Libros conservados/transcritos en P46; se usan solo como fallback si la
# descarga completa pageID=ALL no funcionara.
P46_BOOKS = [
    "Rom", "Heb", "1Cor", "2Cor", "Eph", "Gal", "Phil", "Col", "1Thess"
]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path, timeout: int = 120, attempts: int = 4) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err = None

    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "*/*",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r, tmp.open("wb") as out:
                shutil.copyfileobj(r, out)
                headers = {k: v for k, v in r.headers.items()}
                status = getattr(r, "status", 200)
            tmp.replace(dest)
            return {
                "url": url,
                "status": status,
                "headers": headers,
                "downloaded_at_utc": now_utc(),
                "bytes": dest.stat().st_size,
                "sha256": sha256_file(dest),
            }
        except Exception as e:
            last_err = e
            if tmp.exists():
                tmp.unlink()
            if attempt < attempts:
                time.sleep([2, 5, 12][min(attempt - 1, 2)])
    raise RuntimeError(f"No se pudo descargar {url}: {last_err}")


def ntvmr_url(docid: str, **params) -> str:
    q = {"docID": docid}
    q.update(params)
    return NTVMR_BASE + "?" + urllib.parse.urlencode(q)


def looks_like_xml(path: Path) -> bool:
    with path.open("rb") as f:
        head = f.read(4096)
    # quitar BOM y espacios
    head = head.lstrip(b"\xef\xbb\xbf\xff\xfe\x00\t\r\n ")
    return head.startswith(b"<")


def xml_parse_status(path: Path) -> dict:
    result = {"looks_like_xml": looks_like_xml(path)}
    if not result["looks_like_xml"]:
        result["well_formed_xml"] = False
        result["parse_error"] = "El contenido no comienza con '<'."
        return result
    try:
        ET.parse(path)
        result["well_formed_xml"] = True
    except Exception as e:
        # Algunas ediciones XML antiguas usan DTD/entidades externas. No borrar
        # el original por ello: se registra el aviso para auditoría.
        result["well_formed_xml"] = False
        result["parse_error"] = repr(e)
    return result


def extract_largest_xml(zip_path: Path, dest_xml: Path) -> dict:
    with zipfile.ZipFile(zip_path, "r") as z:
        xml_members = [
            i for i in z.infolist()
            if not i.is_dir() and i.filename.lower().endswith(".xml")
        ]
        if not xml_members:
            raise RuntimeError(f"No se encontró XML dentro de {zip_path}")
        member = max(xml_members, key=lambda i: i.file_size)
        dest_xml.parent.mkdir(parents=True, exist_ok=True)
        with z.open(member, "r") as src, dest_xml.open("wb") as out:
            shutil.copyfileobj(src, out)
    return {
        "zip_member": member.filename,
        "bytes": dest_xml.stat().st_size,
        "sha256": sha256_file(dest_xml),
        **xml_parse_status(dest_xml),
    }


def fetch_ntvmr_full(docid: str, dest: Path) -> dict:
    # Endpoint documentado para una transcripción completa:
    # ?docID=<ID>&pageID=ALL&format=teiraw
    url = ntvmr_url(docid, pageID="ALL", format="teiraw")
    rec = download(url, dest)
    rec.update(xml_parse_status(dest))
    if not rec["looks_like_xml"]:
        raise RuntimeError(
            f"NTVMR devolvió contenido no XML para docID={docid}; "
            f"se conserva en {dest} para inspección."
        )
    return rec


def fetch_ntvmr_copyright(docid: str, dest: Path) -> dict:
    url = ntvmr_url(docid, getCopyright="true")
    return download(url, dest, timeout=60, attempts=2)


def fallback_p46_by_book(root: Path) -> list[dict]:
    """
    Descarga P46 por libro si pageID=ALL falla.
    No concatena TEI arbitrariamente: conserva cada respuesta original.
    """
    parts_dir = root / "p46_ntvmr_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for i, book in enumerate(P46_BOOKS):
        if i:
            time.sleep(2)  # trato respetuoso del servidor NTVMR
        url = ntvmr_url(
            P46_DOCID,
            indexContent=book,
            fullPage="true",
            format="teiraw",
        )
        dest = parts_dir / f"p46_{book}.xml"
        rec = download(url, dest)
        rec["book"] = book
        rec["file"] = str(dest.relative_to(root))
        rec.update(xml_parse_status(dest))
        records.append(rec)
    return records


def write_readme(root: Path, manifest_name: str) -> None:
    readme = f"""# Testigos manuscritos para `nuevo_paulinum`

Este directorio fue preparado automáticamente para el control de sensibilidad
textual/manuscrita del proyecto.

## Archivos principales

- `sinaiticus_project_v105.xml`: transcripción oficial publicada del Codex
  Sinaiticus, versión 1.05 (7-09-2020), depositada por ITSEE/University of
  Birmingham.
- `p46_ntvmr_10046.xml`: transcripción TEI XML publicada por NTVMR del testigo
  GA P46 (docID 10046), obtenida con `pageID=ALL&format=teiraw`.
- `sinaiticus_ntvmr_20001.xml`: solo si se usó
  `--include-ntvmr-sinaiticus`; permite comparar 01 y P46 bajo la misma
  infraestructura NTVMR.
- `{manifest_name}`: procedencia, URL exacta, fecha de adquisición, tamaño y
  SHA-256 de cada descarga.

## Criterio metodológico

Estos archivos deben usarse como **testigos de sensibilidad textual**, no como
si la ortografía, puntuación, segmentación o hábitos gráficos de los copistas
fueran rasgos autorales de Pablo. Para análisis de autoría:

1. conservar el XML bruto sin modificar;
2. generar derivados normalizados en archivos separados;
3. trabajar solo sobre pasajes realmente conservados en cada testigo;
4. no imputar lagunas de P46;
5. documentar exactamente cualquier normalización (nomina sacra, diacríticos,
   puntuación, itacismos, correcciones, expansiones, supplied/lacunae, etc.);
6. ejecutar el análisis principal sobre la representación textual fijada por el
   protocolo y usar 01/P46 como prueba de robustez frente a variación textual y
   scribal;
7. conservar los SHA-256 del manifiesto para que el estado exacto usado en una
   publicación pueda reproducirse.

P46 es lacunoso y no conserva todo el corpus paulino. El control directo entre
01 y P46 debe restringirse a las unidades textuales solapadas.

## Fuentes

Sinaiticus v1.05:
https://epapers.bham.ac.uk/id/eprint/3306/

NTVMR API:
https://ntvmr.uni-muenster.de/community/api/transcript/get/

P46: docID 10046.
Sinaiticus/01: docID 20001.
"""
    (root / "README_TESTIGOS.md").write_text(readme, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        default="nuevo_paulinum",
        help="Directorio de salida (por defecto: nuevo_paulinum)",
    )
    ap.add_argument(
        "--include-ntvmr-sinaiticus",
        action="store_true",
        help="Descarga también Sinaiticus desde NTVMR (docID 20001).",
    )
    ap.add_argument(
        "--keep-sinaiticus-zip",
        action="store_true",
        help="Conserva el ZIP fuente de Sinaiticus v1.05.",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra lo que se descargaría sin hacer peticiones.",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()

    if args.dry_run:
        print("Directorio:", root)
        print("Sinaiticus v1.05 ZIP:", SINAITICUS_V105_ZIP)
        print("P46 NTVMR:", ntvmr_url(P46_DOCID, pageID="ALL", format="teiraw"))
        if args.include_ntvmr_sinaiticus:
            print(
                "Sinaiticus NTVMR:",
                ntvmr_url(SINAITICUS_NTVMR_DOCID, pageID="ALL", format="teiraw"),
            )
        return 0

    root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at_utc": now_utc(),
        "project_directory": str(root),
        "tool": "preparar_testigos.py",
        "sources": [],
        "warnings": [],
    }

    # 1) Sinaiticus v1.05 oficial
    zip_path = root / "sinaiticus_project_v105_source.zip"
    xml_path = root / "sinaiticus_project_v105.xml"
    print("[1/3] Descargando Codex Sinaiticus v1.05 (ITSEE/UBIRA)...")
    rec_zip = download(SINAITICUS_V105_ZIP, zip_path)
    rec_zip["label"] = "Codex Sinaiticus official published transcription v1.05 (ZIP)"
    rec_zip["file"] = zip_path.name
    manifest["sources"].append(rec_zip)

    rec_xml = extract_largest_xml(zip_path, xml_path)
    rec_xml.update({
        "label": "Codex Sinaiticus official published transcription v1.05 (XML extracted)",
        "file": xml_path.name,
        "derived_from": zip_path.name,
    })
    manifest["sources"].append(rec_xml)

    if not args.keep_sinaiticus_zip:
        zip_path.unlink(missing_ok=True)
        rec_zip["local_zip_removed_after_verification"] = True

    # 2) P46 completo desde NTVMR
    print("[2/3] Descargando P46 (NTVMR docID 10046)...")
    p46_path = root / "p46_ntvmr_10046.xml"
    try:
        rec = fetch_ntvmr_full(P46_DOCID, p46_path)
        rec.update({
            "label": "P46 NTVMR published TEI transcription",
            "file": p46_path.name,
            "docID": P46_DOCID,
            "ga": "P46",
        })
        manifest["sources"].append(rec)
    except Exception as e:
        manifest["warnings"].append(
            "Falló la descarga completa de P46; se activó el fallback por libros: "
            + repr(e)
        )
        print("  Aviso: descarga completa fallida; descargando P46 por libros...")
        parts = fallback_p46_by_book(root)
        manifest["p46_fallback_parts"] = parts

    # Copyright/licencia publicada por NTVMR (si el endpoint responde)
    try:
        time.sleep(2)
        cp = root / "p46_ntvmr_copyright.txt"
        rec = fetch_ntvmr_copyright(P46_DOCID, cp)
        rec.update({"label": "NTVMR copyright response for P46", "file": cp.name})
        manifest["sources"].append(rec)
    except Exception as e:
        manifest["warnings"].append(
            "No se pudo guardar la respuesta getCopyright de P46: " + repr(e)
        )

    # 3) Sinaiticus NTVMR opcional, útil para codificación homogénea
    if args.include_ntvmr_sinaiticus:
        print("[3/3] Descargando Sinaiticus desde NTVMR (docID 20001)...")
        time.sleep(2)
        nt_sin = root / "sinaiticus_ntvmr_20001.xml"
        try:
            rec = fetch_ntvmr_full(SINAITICUS_NTVMR_DOCID, nt_sin)
            rec.update({
                "label": "Codex Sinaiticus NTVMR published TEI transcription",
                "file": nt_sin.name,
                "docID": SINAITICUS_NTVMR_DOCID,
                "ga": "01",
            })
            manifest["sources"].append(rec)
        except Exception as e:
            manifest["warnings"].append(
                "No se pudo descargar Sinaiticus desde NTVMR: " + repr(e)
            )
    else:
        print("[3/3] Sinaiticus NTVMR omitido (use --include-ntvmr-sinaiticus si lo desea).")

    manifest_name = "TESTIGOS_MANIFEST.json"
    write_readme(root, manifest_name)

    # añadir hashes de los archivos auxiliares generados
    for name in ["README_TESTIGOS.md"]:
        p = root / name
        manifest.setdefault("generated_files", []).append({
            "file": name,
            "bytes": p.stat().st_size,
            "sha256": sha256_file(p),
        })

    (root / manifest_name).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("Listo:", root)
    print("Entregue a Claude el directorio completo 'nuevo_paulinum/'.")
    print("Revise TESTIGOS_MANIFEST.json para hashes y procedencia.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

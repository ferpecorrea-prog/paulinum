#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detectar_reutilizacion.py — tramos paralelos entre pares de cartas (Ef↔Col, 2Tes↔1Tes).

Método (§ 0.3 del informe de la campaña 03): 4-gramas de formas (sin diacríticos) compartidos por
las dos cartas; las posiciones cubiertas se unen en tramos si el hueco entre 4-gramas es ≤ 3 palabras
y el tramo resultante tiene ≥ 6 palabras. Salidas:
  results/<run>/reutilizacion_pares.csv   — todos los 4-gramas compartidos con sus posiciones
  metadata/reuse_ranges.csv                — tramos por carta (start, end exclusivo, pair, ref_start, ref_end, tokens)
«Hueco ≤ 3» se entiende como distancia ≤ 3 entre posiciones cubiertas consecutivas (hasta dos palabras
no compartidas entre medias); con esa lectura se reproducen los tramos publicados.
Con --comparar se cotejan los tramos calculados con los de metadata/reuse_ranges.csv (publicados).

Cotejo de la reconstrucción (25-IX-2026): los 14 tramos de Ef↔Col y los 4 primeros de 2Tes↔1Tes se
reproducen posición a posición; los dos tramos finales (2Tes 810-817, 1Tes 1464-1471) terminan en el
original una palabra antes que aquí (810-818, 1464-1472): el guion original no generaba el último
4-grama del documento. La máscara sellada sigue siendo la publicada (metadata/reuse_ranges.csv).

Uso: python scripts/detectar_reutilizacion.py --run campana_03 [--pares Ef:Col,2Tes:1Tes] [--escribir] [--comparar]
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import load_corpus  # noqa: E402

DEFAULT_PAIRS = ["Ef:Col", "2Tes:1Tes"]


def shared_ngrams(a: list[str], b: list[str], n: int = 4) -> list[tuple[int, int, str]]:
    idx = {}
    for j in range(len(b) - n + 1):
        idx.setdefault(tuple(b[j:j + n]), []).append(j)
    out = []
    for i in range(len(a) - n + 1):
        g = tuple(a[i:i + n])
        for j in idx.get(g, []):
            out.append((i, j, " ".join(g)))
    return out


def spans(positions: list[int], n: int = 4, gap: int = 3, min_len: int = 6) -> list[tuple[int, int]]:
    """
    Une las posiciones cubiertas por los 4-gramas compartidos en tramos [start, end) cuando la distancia
    entre posiciones cubiertas consecutivas es ≤ gap (es decir, hasta gap − 1 palabras no compartidas
    entre medias) y conserva los tramos de ≥ min_len palabras.
    """
    covered = sorted(set(p for s in positions for p in range(s, s + n)))
    out = []
    if not covered:
        return out
    start = prev = covered[0]
    for p in covered[1:]:
        if p - prev > gap:
            if prev + 1 - start >= min_len:
                out.append((start, prev + 1))
            start = p
        prev = p
    if prev + 1 - start >= min_len:
        out.append((start, prev + 1))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="campana_03")
    ap.add_argument("--pares", default=",".join(DEFAULT_PAIRS))
    ap.add_argument("--edicion", default="sblgnt")
    ap.add_argument("--escribir", action="store_true", help="sobrescribir metadata/reuse_ranges.csv")
    ap.add_argument("--comparar", action="store_true")
    a = ap.parse_args()
    docs = {d.id: d for d in load_corpus(a.edicion)}
    rows_ng, rows_rng = [], []
    for pair in a.pares.split(","):
        x, y = pair.split(":")
        A, B = docs[x], docs[y]
        ng = shared_ngrams(A.forms_nodia, B.forms_nodia)
        for i, j, g in ng:
            rows_ng.append({"pair": f"{x}~{y}", "pos_a": i, "pos_b": j, "ref_a": A.refs[i], "ref_b": B.refs[j], "ngram": g})
        for doc, other, pos in ((A, B, [i for i, _, _ in ng]), (B, A, [j for _, j, _ in ng])):
            for s, e in spans(pos):
                rows_rng.append({"id": doc.id, "start": s, "end": e, "pair": other.id, "ref_start": doc.refs[s],
                                 "ref_end": doc.refs[e - 1], "tokens": e - s})
        print(f"{x}↔{y}: {len(ng)} 4-gramas compartidos")
    out_dir = os.path.join("results", a.run)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "reutilizacion_pares.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "pos_a", "pos_b", "ref_a", "ref_b", "ngram"])
        w.writeheader()
        w.writerows(rows_ng)
    for r in rows_rng:
        print(f"  {r['id']:5s} {r['start']:5d} {r['end']:5d} {r['pair']:5s} {r['ref_start']:>6s} {r['ref_end']:>6s} {r['tokens']:3d}")
    by_id = {}
    for r in rows_rng:
        by_id[r["id"]] = by_id.get(r["id"], 0) + r["tokens"]
    print("tokens enmascarados por carta:", by_id)
    target = os.path.join("metadata", "reuse_ranges.csv")
    if a.comparar and os.path.exists(target):
        pub = list(csv.DictReader(open(target, encoding="utf-8")))
        pub_set = {(r["id"], int(r["start"]), int(r["end"])) for r in pub}
        new_set = {(r["id"], r["start"], r["end"]) for r in rows_rng}
        print(f"cotejo con metadata/reuse_ranges.csv: {len(pub_set & new_set)} tramos idénticos de {len(pub_set)} publicados; "
              f"{len(new_set - pub_set)} nuevos no publicados")
        for t in sorted(pub_set - new_set):
            print("   publicado y no reproducido:", t)
        for t in sorted(new_set - pub_set):
            print("   reproducido y no publicado:", t)
    if a.escribir:
        with open(target, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "start", "end", "pair", "ref_start", "ref_end", "tokens"])
            w.writeheader()
            w.writerows(rows_rng)
        print(f"→ {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

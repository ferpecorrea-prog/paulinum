#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_sensibilidad.py — escribe las configuraciones de los bloques de sensibilidad (PROTOCOLO § 6.2) a partir de la
configuración principal, cambiando UNA dimensión por bloque y dejando todo lo demás igual. Cada bloque se ejecuta como
campaña aparte (results/paulinum_1_0/sensibilidad/<bloque>/) y solo se informa: nunca sustituye a la rejilla principal.

Bloques: nucleos (hauptbriefe, seven_plus, trece), ediciones (tischendorf, nestle1904), testigos (sinaiticus y su SBLGNT
recortado; p46 y su SBLGNT recortado; sin diacríticos), ventana300, documento_entero, rasgos (mfw:100, mfw:500, char4:1000),
pos3 (solo si la anotación uniforme superó el umbral), coseno, nodia. La familia NCD (lenta) entra solo en «testigos»;
Dirichlet en todos los bloques en los que tiene sentido (no en «rasgos» ni «coseno»).
Uso: python scripts/generar_sensibilidad.py [--config config/paulinum_1_0.yaml]
"""
from __future__ import annotations

import argparse
import copy
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/paulinum_1_0.yaml")
    a = ap.parse_args()
    with open(a.config, encoding="utf-8") as f:
        base = yaml.safe_load(f)
    out_dir = os.path.join("config", "sens")
    os.makedirs(out_dir, exist_ok=True)
    blocks = {
        "nucleos": {"rejilla": {"nucleos": ["hauptbriefe", "seven_plus", "trece"]}},
        "ediciones": {"rejilla": {"ediciones": ["tischendorf", "nestle1904"]}},
        "testigos": {"rejilla": {"ediciones": ["sinaiticus", "sblgnt_rec_sinaiticus", "p46", "sblgnt_rec_p46"],
                                 "diacriticos": ["nodia"]}, "ncd": True},
        "ventana300": {"rejilla": {"ventanas": [300]}},
        "documento_entero": {"rejilla": {"ventanas": [None]}},
        "rasgos": {"rejilla": {"rasgos": ["mfw:100", "mfw:500", "char4:1000"]}, "sin_dirichlet": True},
        "pos3": {"rejilla": {"rasgos": ["pos3:200"]}, "sin_dirichlet": True,
                 "nota": "solo si results/anotacion/acuerdo_nt.json dice apto (PROTOCOLO § 5.3)"},
        "coseno": {"rejilla": {"distancias": ["cosine"]}, "sin_dirichlet": True},
        "nodia": {"rejilla": {"diacriticos": ["nodia"]}},
    }
    written = []
    for name, spec in blocks.items():
        cfg = copy.deepcopy(base)
        cfg["nombre"] = f"paulinum_1_0/sensibilidad/{name}"
        cfg["descripcion"] = f"sensibilidad {name} de paulinum 1.0 (PROTOCOLO § 6.2): una dimensión cambiada, el resto igual"
        cfg["bloque_sensibilidad"] = name
        if "nota" in spec:
            cfg["nota"] = spec["nota"]
        for k, v in spec["rejilla"].items():
            cfg["rejilla"][k] = v
        fam = cfg.setdefault("familias", {})
        fam.setdefault("ncd", {})["activa"] = bool(spec.get("ncd", False))
        if spec.get("ncd"):
            fam["ncd"]["iters"] = 100
        if spec.get("sin_dirichlet"):
            fam.setdefault("dirichlet", {})["activa"] = False
        cfg.pop("sensibilidad", None)
        cfg["preregistro"] = {"bloque": name, "regla": "solo se informa; nunca sustituye a la rejilla principal; si contradice a la principal, se informa la contradicción (PROTOCOLO § 6.2)"}
        path = os.path.join(out_dir, f"paulinum_1_0_{name}.yaml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Bloque de sensibilidad «{name}» generado por scripts/generar_sensibilidad.py a partir de {a.config}\n")
            yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
        written.append(path)
    print("\n".join(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())

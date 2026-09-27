# -*- coding: utf-8 -*-
"""pytest: ejecuta las pruebas de referencia (scripts/selftest.py) y exige que todas pasen."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_selftest_passes():
    rc = subprocess.call([sys.executable, os.path.join(ROOT, "scripts", "selftest.py")], cwd=ROOT)
    assert rc == 0


def test_capa_13_lemas_cotejo():
    out = subprocess.run([sys.executable, os.path.join(ROOT, "investigacion_1", "capa_13_lemas", "cotejo_con_el_libro.py")],
                         cwd=os.path.join(ROOT, "investigacion_1", "capa_13_lemas"), capture_output=True, text=True)
    assert out.stdout.strip().startswith("313/313"), out.stdout[:200]

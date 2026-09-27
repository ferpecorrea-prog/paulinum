# -*- coding: utf-8 -*-
"""Punto de entrada: python -m paulinum <orden> ..."""
import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())

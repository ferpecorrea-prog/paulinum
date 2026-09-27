# -*- coding: utf-8 -*-
"""
distances.py — medidas de distancia entre vectores de rasgos.

  delta     Delta de Burrows: media de |z_a − z_b| sobre frecuencias relativas estandarizadas con la
            media y la desviación típica del conjunto de referencia (Burrows 2002; Evert et al. 2017).
  minmax    Ruzicka / min-max (Koppel y Winter 2014): 1 − Σ min(a,b) / Σ max(a,b) sobre frecuencias relativas.
  cosine    distancia coseno sobre z-scores (Delta coseno, Evert et al. 2017).
  eder      Delta de Eder: Σ |z_a − z_b| · (n − i + 1)/n, con los rasgos ordenados por frecuencia.
  manhattan / euclidean sobre frecuencias relativas.
  labbe     distancia intertextual de Labbé (2007) sobre recuentos brutos, con reducción del texto
            largo a la extensión del corto.

Todas las funciones aceptan matrices (m × k) frente a un vector (k) o frente a otra matriz (m × k)
fila a fila, y devuelven un vector de m distancias.
"""
from __future__ import annotations

import numpy as np

EPS = 1e-12


class Standardizer:
    """Media y desviación típica por rasgo, estimadas sobre frecuencias relativas de los documentos de referencia."""

    def __init__(self, rel_matrix: np.ndarray):
        self.mean = rel_matrix.mean(axis=0)
        sd = rel_matrix.std(axis=0, ddof=1) if rel_matrix.shape[0] > 1 else np.ones(rel_matrix.shape[1])
        sd[sd < EPS] = 1.0
        self.sd = sd

    def z(self, rel: np.ndarray, cols: np.ndarray | None = None) -> np.ndarray:
        if cols is None:
            return (rel - self.mean) / self.sd
        return (rel - self.mean[cols]) / self.sd[cols]


def _pair(a: np.ndarray, b: np.ndarray):
    a = np.atleast_2d(a)
    b = np.atleast_2d(b)
    if b.shape[0] == 1 and a.shape[0] > 1:
        b = np.broadcast_to(b, a.shape)
    elif a.shape[0] == 1 and b.shape[0] > 1:
        a = np.broadcast_to(a, b.shape)
    return a, b


def delta(za: np.ndarray, zb: np.ndarray) -> np.ndarray:
    a, b = _pair(za, zb)
    return np.abs(a - b).mean(axis=1)


def eder(za: np.ndarray, zb: np.ndarray) -> np.ndarray:
    a, b = _pair(za, zb)
    n = a.shape[1]
    w = (n - np.arange(n)) / n
    return (np.abs(a - b) * w).sum(axis=1) / n


def cosine(za: np.ndarray, zb: np.ndarray) -> np.ndarray:
    a, b = _pair(za, zb)
    num = (a * b).sum(axis=1)
    den = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1) + EPS
    return 1.0 - num / den


def minmax(ra: np.ndarray, rb: np.ndarray) -> np.ndarray:
    a, b = _pair(ra, rb)
    num = np.minimum(a, b).sum(axis=1)
    den = np.maximum(a, b).sum(axis=1) + EPS
    return 1.0 - num / den


def manhattan(ra: np.ndarray, rb: np.ndarray) -> np.ndarray:
    a, b = _pair(ra, rb)
    return np.abs(a - b).sum(axis=1)


def euclidean(ra: np.ndarray, rb: np.ndarray) -> np.ndarray:
    a, b = _pair(ra, rb)
    return np.sqrt(((a - b) ** 2).sum(axis=1))


def labbe(ca: np.ndarray, cb: np.ndarray) -> np.ndarray:
    """Distancia de Labbé sobre recuentos brutos (a: m × k, b: m × k). El texto largo se reduce al corto."""
    a, b = _pair(ca, cb)
    na, nb = a.sum(axis=1, keepdims=True), b.sum(axis=1, keepdims=True)
    scale_a = np.where(na > nb, nb / (na + EPS), 1.0)
    scale_b = np.where(nb > na, na / (nb + EPS), 1.0)
    a2, b2 = a * scale_a, b * scale_b
    return np.abs(a2 - b2).sum(axis=1) / (a2.sum(axis=1) + b2.sum(axis=1) + EPS)


Z_BASED = {"delta", "eder", "cosine"}
REL_BASED = {"minmax", "manhattan", "euclidean"}
COUNT_BASED = {"labbe"}
METRICS = {"delta": delta, "eder": eder, "cosine": cosine, "minmax": minmax, "manhattan": manhattan,
           "euclidean": euclidean, "labbe": labbe}


def distance(metric: str, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return METRICS[metric](a, b)

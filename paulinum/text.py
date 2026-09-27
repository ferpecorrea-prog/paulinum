# -*- coding: utf-8 -*-
"""
text.py — normalización de formas griegas y conversión de Beta Code.

Reglas (Apéndice A.1 y § 8.1 del libro):
  * descomposición/composición Unicode (NFD → NFC) y minúsculas;
  * sigma final ς → σ (la posición final no es un rasgo de mano);
  * acento grave → agudo (la variación grave/agudo depende de la puntuación del editor);
  * filtro de letras griegas: se descartan los tokens sin ninguna letra griega (latín de las
    lagunas de Policarpo, Josefo *C. Ap.* II y Hermas; números; siglas editoriales);
  * variante «sin diacríticos» (nodia): se eliminan todos los signos combinatorios
    (espíritus, acentos, iota suscrita, diéresis) y se conserva la letra base.
  * Beta Code → Unicode para el corpus Diorisis.

Todas las funciones son puras y deterministas.
"""
from __future__ import annotations

import re
import unicodedata

GREEK_LETTER_RE = re.compile(r"[Ͱ-Ͽἀ-῿]")
_NON_LETTER_RE = re.compile(r"[^Ͱ-Ͽἀ-῿]+")
# apóstrofo / coronis de elisión: se conserva como marca «’» normalizada
_APOSTROPHES = "’ʼ᾽᾿'´‘"
_GRAVE_TO_ACUTE = {"̀": "́"}  # combinación grave → aguda (tras NFD)


def strip_diacritics(s: str) -> str:
    """Elimina todos los signos combinatorios; devuelve la cadena en NFC."""
    d = unicodedata.normalize("NFD", s)
    d = "".join(ch for ch in d if not unicodedata.combining(ch))
    return unicodedata.normalize("NFC", d)


def normalize_form(token: str, keep_diacritics: bool = True) -> str:
    """
    Normaliza una forma: minúsculas, NFC, sigma final → σ, grave → agudo, sin puntuación.
    Devuelve '' si el token no contiene ninguna letra griega.
    """
    if not token or not GREEK_LETTER_RE.search(token):
        return ""
    t = unicodedata.normalize("NFD", token)
    t = t.lower()
    # grave → agudo
    t = "".join(_GRAVE_TO_ACUTE.get(ch, ch) for ch in t)
    # elisión: se conserva una marca uniforme
    elided = t.endswith(tuple(_APOSTROPHES))
    # filtro de caracteres: solo letras griegas y signos combinatorios
    t = "".join(ch for ch in t if GREEK_LETTER_RE.match(ch) or unicodedata.combining(ch))
    t = unicodedata.normalize("NFC", t)
    t = t.replace("ς", "σ")
    if not keep_diacritics:
        t = strip_diacritics(t)
    if elided and t:
        t += "’"
    return t


def tokenize(text: str) -> list[str]:
    """Divide un texto corrido en tokens crudos (por espacios y puntuación)."""
    # separar la puntuación griega y latina; conservar apóstrofos finales
    text = text.replace("·", " ").replace("·", " ")
    return [t for t in re.split(r"[\s\.,;:!\?\(\)\[\]«»\"“”—–\-…†‡<>{}]+", text) if t]


# ---------------------------------------------------------------------------------------------
# Beta Code (TLG) → Unicode, suficiente para las formas del corpus Diorisis
# ---------------------------------------------------------------------------------------------
_BETA_LETTERS = {
    "a": "α", "b": "β", "g": "γ", "d": "δ", "e": "ε", "z": "ζ", "h": "η", "q": "θ", "i": "ι",
    "k": "κ", "l": "λ", "m": "μ", "n": "ν", "c": "ξ", "o": "ο", "p": "π", "r": "ρ", "s": "σ",
    "t": "τ", "u": "υ", "f": "φ", "x": "χ", "y": "ψ", "w": "ω", "v": "ϝ",
}
_BETA_DIACRITICS = {
    ")": "̓",  # espíritu suave
    "(": "̔",  # espíritu áspero
    "/": "́",  # agudo
    "\\": "̀",  # grave
    "=": "͂",  # circunflejo
    "|": "ͅ",  # iota suscrita
    "+": "̈",  # diéresis
}


def beta_to_unicode(beta: str) -> str:
    """Convierte Beta Code (minúsculas o mayúsculas TLG con '*') a griego Unicode NFC."""
    out = []
    i = 0
    s = beta
    while i < len(s):
        ch = s[i]
        if ch == "*":  # mayúscula
            i += 1
            # los diacríticos de mayúscula pueden preceder a la letra: *)a
            pre = ""
            while i < len(s) and s[i] in _BETA_DIACRITICS:
                pre += _BETA_DIACRITICS[s[i]]
                i += 1
            if i >= len(s):
                break
            ch = s[i]
            base = _BETA_LETTERS.get(ch.lower(), "")
            if not base:
                i += 1
                continue
            out.append(base.upper() + pre)
            i += 1
            continue
        low = ch.lower()
        if low in _BETA_LETTERS:
            base = _BETA_LETTERS[low]
            i += 1
            dia = ""
            while i < len(s) and s[i] in _BETA_DIACRITICS:
                dia += _BETA_DIACRITICS[s[i]]
                i += 1
            # sigma final
            if low == "s" and (i >= len(s) or not s[i].isalpha()):
                base = "ς"
            elif low == "s" and i < len(s) and s[i] in "12":
                base = {"1": "σ", "2": "ς"}[s[i]]
                i += 1
            out.append(base + dia)
            continue
        if ch.isdigit() and out:
            i += 1
            continue
        out.append(ch)
        i += 1
    return unicodedata.normalize("NFC", "".join(out))


def is_greek(token: str) -> bool:
    return bool(GREEK_LETTER_RE.search(token))

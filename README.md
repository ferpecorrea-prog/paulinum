# paulinum — verificación convergente de la autoría del corpus paulino canónico

[![selftest](https://github.com/ferpecorrea-prog/paulinum/actions/workflows/selftest.yml/badge.svg)](https://github.com/ferpecorrea-prog/paulinum/actions/workflows/selftest.yml)

Software, corpus de control, protocolos preregistrados, resultados e informes de una investigación de
**verificación de autoría** sobre las catorce cartas del corpus paulino canónico (las trece que llevan el
nombre de Pablo y la Epístola a los Hebreos), con controles de autoría segura, calibración de la tasa de
error, envolvente intra-autor («mismo rasero»), análisis de las variables de situación y canales no
estilométricos (recepción y transmisión, onomástica y prosopografía, epigrafía institucional).

Autor: Jesús Fernández-Pedrera Correa (ORCID [0009-0000-7024-5028](https://orcid.org/0009-0000-7024-5028)),
investigador independiente, Barcelona. Todo el material está en español.

## Estado

| | |
|---|---|
| Versión en desarrollo | `1.0.0.dev0` |
| Protocolo preregistrado | [`protocols/paulinum_1_0/PROTOCOLO.md`](protocols/paulinum_1_0/PROTOCOLO.md) — Sello 1 (`protocolo-1.0.0`) el 27-IX-2026; Sello 2 (código congelado) y Sello 3 (resultados) pendientes |
| Punto de partida | `v0.2.0-r`: reconstrucción declarada del laboratorio publicado en 2026 (véase `LEEME_PRIMERO.md` y `docs/README_reconstruccion_0.2.0-r.md`) |
| Registro de investigación | `docs/registro_investigacion.md` (bitácora por sesiones) |
| Decisiones metodológicas y filológicas | `docs/decisiones.md` (numeradas, fechadas, con motivo) |
| Cambios por versión | `CHANGELOG.md` |
| Preregistro y sellado | `protocols/` (cada campaña: protocolo, huella SHA-256, registro público y DOI) |
| Archivo con DOI | Zenodo, a partir de cada *release* de GitHub. DOI de concepto (todas las versiones): [10.5281/zenodo.22993121](https://doi.org/10.5281/zenodo.22993121). Sello 1 (`protocolo-1.0.0`): [10.5281/zenodo.22993122](https://doi.org/10.5281/zenodo.22993122) |

## Qué hay en el repositorio

| carpeta | contenido |
|---|---|
| `paulinum/` | paquete Python: `sources` (manifiesto de textos), `fetch`, `parsers`, `text`, `corpus`, `features`, `distances`, `verify`, `variables`, `rolling`, `pipeline`, `report`, `cli` |
| `scripts/` | guiones auxiliares (calibración secundaria, lexicón, reutilización, variables de los controles, *bootstrap*, segundo modelo, lecturas) |
| `config/` | configuraciones de campaña, cada una con su bloque de preregistro literal |
| `protocols/` | protocolos sellados de la nueva investigación: `paulinum_1_0/` (protocolo, sello, registro público) |
| `metadata/` | máscaras por referencia, pasajes paralelos, variables de situación, auditoría de estados de los controles |
| `data/` | `raw/` (descargas, no versionadas), `cache/` (corpus construidos, no versionados), `local/` (3 Corintios preparado a partir de P. Bodmer X), `provenance.json` (huellas SHA-256) |
| `results/` | resultados de las ejecuciones (tablas CSV/JSON, figuras, bitácoras) |
| `results_publicados/` | tablas publicadas en el libro de 2026, transcritas, como datos de referencia históricos |
| `informes/` | informes íntegros de las campañas |
| `investigacion_1/` | material de la primera investigación publicada (capa de trece lemas y segunda campaña), conservado como registro histórico |
| `docs/` | especificación, guías, registro de investigación, decisiones, inventarios de fuentes |
| `tests/` | pruebas (`pytest`) |

## Instalación y comprobación

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/selftest.py                              # 25 comprobaciones deterministas; imprime una huella de referencia
pytest -q
```

## Reproducibilidad

- Los textos de origen no se redistribuyen: `python -m paulinum fetch` los descarga de sus repositorios
  (MorphGNT/SBLGNT, Open Apostolic Fathers, Perseus, First1KGreek, PROIEL, MACULA y los que se incorporen)
  y anota la huella SHA-256 de cada archivo en `data/provenance.json`.
- Cada campaña se **sella antes de ejecutarse** (`python -m paulinum seal`): la huella cubre el código, los
  metadatos, la configuración y el preregistro. La huella, el protocolo y su registro público quedan en
  `protocols/<campaña>/`, y el estado sellado se archiva en Zenodo con DOI antes de mirar ningún resultado.
- Cada resultado publicado remite a la versión exacta (etiqueta de git y DOI) del código, del corpus y de
  la configuración que lo produjo; la bitácora de cada campaña (`results/<campaña>/bitacora.md`) registra
  cada orden con su hora y su duración.
- Los cálculos se ejecutan en dos entornos con las mismas versiones de las bibliotecas numéricas y se
  comprueba que las pruebas de referencia dan la misma huella.

## Licencias

Código: MIT (`LICENSE`). Datos, metadatos, resultados, informes y documentación: CC BY 4.0 (`LICENSE-DATA`).
Los textos griegos de terceros conservan las licencias de sus editores.

## Cómo citar

Véase `CITATION.cff`. Forma breve: Fernández-Pedrera Correa, Jesús. *paulinum: verificación convergente de
la autoría del corpus paulino canónico*, versión X, Barcelona, 2026, https://github.com/ferpecorrea-prog/paulinum,
DOI (Zenodo) de la versión citada.

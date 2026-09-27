# Registro de investigación (bitácora por sesiones)

Convención: una entrada por sesión de trabajo, con fecha, objeto, lo hecho, lo decidido (remisión a
`docs/decisiones.md`), lo pendiente y el *commit* que la cierra. Las órdenes de cálculo con hora y duración van
en la bitácora de cada campaña (`results/<campaña>/bitacora.md`); aquí se registra el desarrollo de la
investigación, no el detalle de ejecución.

## Sesión 0 — 2026-09-27 — Infraestructura, entornos, inventario de fuentes, 3 Corintios

**Objeto.** Dejar el proyecto en condiciones de investigación reproducible antes de tocar ningún dato de las
cartas: repositorio público con historial, entornos comprobados, fuentes inventariadas, control de
falsificación preparado.

**Hecho.**
- Repositorio `paulinum` creado en GitHub (público), con la reconstrucción `paulinum 0.2.0-r` importada como
  primer *commit* y etiquetada `v0.2.0-r`, para que el punto de partida quede a la vista y declarado.
- Infraestructura: licencias (MIT para el código, CC BY 4.0 para datos e informes), `CITATION.cff` con ORCID,
  `.zenodo.json` (integración Zenodo-GitHub activada por el autor), `CHANGELOG.md`, este registro,
  `docs/decisiones.md`, comprobación automática en GitHub Actions (`selftest` + `pytest`), carpeta `protocols/`.
- Entornos: portátil del investigador (Python 3.10; numpy 2.2.6, scipy 1.15.3, scikit-learn 1.7.2, pandas 2.3.3,
  matplotlib 3.10.9, lxml 6.1.3) y réplica en la nube. `scripts/selftest.py`: 25/25, huella
  `ecaf65723ff53cdab462bb3ad014dcf3475a076b011060dc4333f603fa190117`, idéntica a la registrada por la
  reconstrucción el 25-IX-2026.
- Inventario de fuentes abiertas y de accesibilidad de red: `docs/inventario_fuentes_sesion0.md`.
- 3 Corintios (P. Bodmer X): normalización de la transcripción diplomática de referencia (531 palabras, solo la
  respuesta de Pablo) y fichero de alineación con 136 intervenciones no triviales; doce decisiones pendientes de
  validación filológica por el autor (`docs/3Cor_validacion_pendiente.md`); ficheros con sufijo `_BORRADOR`.
- Primer envío a GitHub (`main`, etiqueta `v0.2.0-r`); la comprobación automática (`selftest` + `pytest`) pasó en
  el primer intento (commit `3f6b31f`).

**Decisiones.** D-001 a D-006 en `docs/decisiones.md`.

**Pendiente.** Validación de 3 Corintios por el autor; DOI de concepto de Zenodo tras la primera *release*;
diseño del protocolo y sellado (sesión 1).

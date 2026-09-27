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

**Cierre (27-IX-2026, tarde).** El autor delegó la validación de 3 Corintios; resuelta con D-007; `data/local/3Cor.txt`
registrado. Descarga de nivel 1 (NT y Padres Apostólicos, 43 archivos) comprobada en el portátil.

**Pendiente.** DOI de concepto de Zenodo tras la primera *release*; diseño del protocolo y sellado (sesión 1).

## Sesión 1 — 2026-09-27 — Protocolo preregistrado y Sello 1

**Objeto.** Fijar antes de ejecutar nada las hipótesis, el corpus, las reglas y el orden de la investigación
(`protocols/paulinum_1_0/PROTOCOLO.md`), y sellarlo públicamente.

**Hecho.**
- Protocolo de paulinum 1.0 escrito y sellado: 13 secciones (objeto; hipótesis H1-H5 con predicciones por canal e
  hipótesis sobre el método Hm1-Hm3; diseño con el mismo rasero para las catorce; corpus en cuatro estratos;
  preparación; rejilla de 16 especificaciones y sensibilidad; tres familias de métodos; problemas de respuesta
  conocida con los nuevos `genre_pairs`, `mediated_pairs` y `epist_pairs`; envolventes E, B y G con regla de
  equivalencia; reglas de decisión en cuatro niveles y veredicto mecánico; protocolo de los tres canales no
  estilométricos y regla de convergencia; falsación; reproducibilidad; enmiendas; referencias).
- Configuración `config/paulinum_1_0.yaml` con bloque de preregistro.
- Manifiesto ampliado (estrato 4, 39 entradas): comprobado en la réplica en la nube que los 39 archivos se descargan
  (raw.githubusercontent.com) y se analizan: Basilio 201 cartas de ≥ 200 palabras (114.837 palabras), Libanio 170
  (49.845), Alcifrón 4 libros, Eliano 1 + 14, Plotino 6, Porfirio 1 + 4 + 1, Juliano 9 obras, Libanio 6 discursos,
  Basilio *A los jóvenes*, Ps-Clemente *De virginitate* 2, Hercher 13 colecciones → 86 unidades agrupadas
  (Ps-Antígono se pierde: una sola carta sin numerar, bajo el umbral; se anota, no se corrige).
- Hebreos como diana: `sources.py` (estado `target`, autor `Pablo?`, género `carta` a efectos de calibración,
  subgénero `homilia`), máscaras (cierre 13, 18-25; 28 tramos de citas = 18,6 % de 4.935 palabras; 21,1 % con el
  cierre; Romanos 23,2 %), variables de situación, `TARGETS` con siete cartas, núcleo `trece`.
- `paulinum seal` ampliado (`--protocol`, `--sin-lexicon`, `--etiqueta`); `Source.group_tokens` y agrupación de
  cartas consecutivas; `build_problems` seguro con dianas dentro del núcleo. `scripts/selftest.py` 25/25 con la
  misma huella de referencia (`ecaf6572…`) en la nube y en el portátil tras los cambios.
- Sello 1: `protocols/paulinum_1_0/SELLO.json` (34 archivos), etiqueta `protocolo-1.0.0`, *release* de GitHub;
  DOI de Zenodo pendiente de anotar por el autor en `REGISTRO.md`.

**Decisiones.** D-008 a D-012.

**Pendiente (sesión 2, antes del Sello 2).** Familias NCD y Dirichlet-multinomial; `epist_pairs`, `genre_pairs`,
`mediated_pairs`; envolventes B y G; `nearest_author`; ruido de edición con NA28 (extracción local) y testigos si
el autor los deposita; anotación uniforme y su validación; `scripts/veredicto.py`; lexicón; cotejo de las máscaras
de Hebreos con NA28 por el autor; DOI del Sello 1.


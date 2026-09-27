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
  Zenodo archivó la *release* el mismo día: DOI 10.5281/zenodo.22993122 (registro 22993122); DOI de concepto 10.5281/zenodo.22993121 (anotados en `REGISTRO.md`, `README.md` y `CITATION.cff`).

**Decisiones.** D-008 a D-012.

**Pendiente (sesión 2, antes del Sello 2).** Familias NCD y Dirichlet-multinomial; `epist_pairs`, `genre_pairs`,
`mediated_pairs`; envolventes B y G; `nearest_author`; ruido de edición con NA28 (extracción local) y testigos si
el autor los deposita; anotación uniforme y su validación; `scripts/veredicto.py`; lexicón; cotejo de las máscaras `otq` de
las otras trece cartas con NA28 por el mismo procedimiento (mismo rasero).

**Cotejo de Hebreos con NA28 (27-IX-2026, tarde).** El ejemplar del autor es un escaneo sin capa de texto; el cotejo se
hizo visualmente sobre las 28 páginas de Hebreos (pp. 657-684, renderizadas a 300 ppp), leyendo los tramos en cursiva
del texto y las referencias en cursiva del margen. Resultado: 27 de los 28 tramos de partida confirmados; ocho tramos
añadidos (3,5; 7,1-2; 7,4; 10,8-9; 10,28; 11,21; 12,15; 12,29); uno retirado (12,20, en redonda). Enmienda 1 del
registro del protocolo; `metadata/masks.csv` con 35 tramos `otq` para Hebreos; cobertura 21,7 % (24,1 % con el cierre).

**Testigos manuscritos (27-IX-2026, tarde).** El autor entregó `nuevo_paulinum_testigos_para_Claude.zip` (guion
`preparar_testigos.py`, solo biblioteca estándar, que descarga de UBIRA y NTVMR y escribe el manifiesto de procedencia).
El guion se conserva sin cambios en `scripts/testigos/`. Ni el portátil (espacio de trabajo) ni la réplica en la nube
alcanzan epapers.bham.ac.uk ni ntvmr.uni-muenster.de (lista de dominios; véase el inventario de la sesión 0), así que
la descarga la hizo el autor en su Windows con el guion (10:19 UTC): Sinaítico v1.05 (30,2 MB), Sinaítico NTVMR (3,9 MB), 𝔓46 NTVMR (0,8 MB), los tres XML bien formados; NTVMR declara CC BY 4.0 en la cabecera TEI; la respuesta `getCopyright` llegó vacía. Derivados generados con `scripts/testigos/derivar_testigos.py` (reglas en `docs/testigos_manuscritos.md` § 4; resultados en § 4.5): acuerdo regularizado con SBLGNT 0,958-0,988 (Sinaítico) y 0,927-0,962 (𝔓46); las dos transcripciones del Sinaítico coinciden al 0,996. D-013.


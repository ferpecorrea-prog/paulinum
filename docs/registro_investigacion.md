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

## Sesión 2 — 2026-09-27 — Cotejo de las trece cartas con NA28 (enmienda 2)

Mismo procedimiento que el de Hebreos: 176 páginas de NA28 (pp. 481-656) renderizadas a 300 ppp y leídas una a una en
busca de los tramos en cursiva. Resultado: los tramos de partida de las trece cartas están todos en cursiva en NA28;
faltaban once citas breves que NA28 marca (Rom 2,6; 4,23; 11,2; 1 Cor 9,10; 14,25; 15,25; 2 Cor 9,7; 9,10; Ef 1,22;
4,9-10; 1 Tim 5,19), añadidas como enmienda 2 del registro del protocolo. Con esto las catorce cartas tienen la máscara
de citas por la misma regla y la misma fuente. Bloque 4 en curso: implementación de las familias nuevas y Sello 2.


## Sesión 2 (continuación) — 2026-09-27 — Implementación de lo que faltaba y Sello 2

**Objeto.** Punto 2 de § 3.3 del protocolo: implementar las piezas nuevas, probarlas solo con problemas de respuesta
conocida y congelar el código (Sello 2, `paulinum-1.0.0`).

**Hecho (código).**
- `paulinum/verify.py`: familias B (`NCDEngine`, LZMA2 preset 6; D-020) y C (`DirichletEngine`, perfiles de autor a
  ambos lados, α por máxima verosimilitud marginal; D-019) con la misma envoltura de problemas, banco e impostores que
  la familia A; `build_problems` con `pos_epist`/`neg_epist` (D-014), `genre_pairs`, `mediated_pairs`, modo
  `sin_dianas` y núcleo/dianas a medida (`nucleo_ids`/`dianas_ids`); calibraciones general, epistolar y cristiana;
  razones de verosimilitud `log10lr`, `log10lr_epistolar`, `log10lr_cristiana`, `log10lr_cj`.
- `paulinum/pipeline.py`: rejilla por familia con semillas propias; etapa `specs` reanudable por problema y
  paralelizable (`--workers`, `--familias`, `--solo`); etapa `calibration` con `familias_aptitud.csv` (AUC epistolar
  mediana ≥ `auc_minima`), `concordancia_familias.csv`, `lr_secundaria_por_carta.csv`; etapa `ledger` con envolventes
  E, B y G, percentiles con estadísticas, tensor carta × documento (D-021) y `nearest_author_<m>.csv` con IC del
  margen; `campaign_sets` que respeta `sin_dianas`; capa `pos_uniforme` opcional (D-016).
- `paulinum/variables.py`: `inter_author_pairs`, `genre_pairs`, `same_standard_ledger` con tres envolventes,
  `matrix_rect`, `nearest_authors` con réplicas de ventana.
- `paulinum/features.py`: espacio `pos3:N` sobre la anotación uniforme; `paulinum/corpus.py` y `sources.py`:
  ediciones de testigos (`sinaiticus`, `sblgnt_rec_sinaiticus`, `p46`, `sblgnt_rec_p46`) a partir de los derivados
  de D-013; `paulinum/cli.py`: `run --workers/--familias/--solo`, `seal` con `SELLO_<etiqueta>.json`, guiones de
  `scripts/testigos/` y `config/sens/*.yaml` en el sello.
- Guiones: `scripts/veredicto.py` (reglas de § 8, cuatro niveles, patrón de § 8.5, «qué revisaría este juicio»),
  `scripts/bootstrap_percentil.py` (IC por autores, leave-one-author-out, IC por ventanas, para pct_E, pct_B y pct_G),
  `scripts/anotacion_uniforme.py` (validación de greCy contra MorphGNT, umbrales 0,95/0,95),
  `scripts/generar_sensibilidad.py` → nueve configuraciones en `config/sens/`.
- Lexicón uniforme (`data/cache/lexicon_uniforme.tsv`, no versionado): construido en la réplica en la nube con
  MorphGNT + PROIEL + Diorisis (Diorisis.zip del autor, SHA-256 `fb32b7ff…`); 397.681 formas, 15.719 con las tres
  fuentes; SHA-256 `b0ea6312655cbe8fdd5f92337089a7b9e5f961d7f2d5aa1b6e67bf25440c4ea7`, copiado al portátil con la
  huella verificada. Entra en el Sello 2; el laboratorio de Actions lo reconstruye y comprueba la huella (D-017).
- Laboratorio en GitHub Actions: `.github/workflows/campana.yml` y `docs/laboratorio_actions.md` (D-017).
- `tests/test_paulinum_1_0.py`: ocho pruebas con corpus sintético (rejilla por familia, problemas, separación de
  autores en las tres familias, Dirichlet-multinomial y α, propiedades de NCD, envolventes, conjuntos de campaña y
  testigos, determinismo por problema).

**Hecho (validación sin dianas, D-018).**
- `results/prueba_1_0/` (estrato 1, `sin_dianas`, 20 iteraciones; ninguna fila de diana): las tres familias corren de
  punta a punta; AUC epistolar mediana: impostores 0,885, NCD 0,962, Dirichlet 1,000 (en un corpus pequeño, solo
  como prueba de funcionamiento).
- `results/prueba_veredicto_ignacio/` (estrato 4, 857 documentos; núcleo = las siete cartas de Ignacio, dianas = ocho
  cartas de la recensión larga; impostores 4 especificaciones × 50 iteraciones, Dirichlet 1 × 50): AUC epistolar
  0,988 (impostores) y 0,979 (Dirichlet); las siete cartas genuinas en *leave-one-out* dan «apoyo moderado a
  H_mismo-autor» (log10 LR ≈ +1,9) y el núcleo es el autor más próximo en todas; de las seis cartas espurias de la
  recensión larga (#1, #4, #5, #9, #10, #13), tres dan LR en contra (#1 −1,0; #5 −0,9; #13 −1,0) y no pasan el
  nivel 3, dos son discordantes entre familias (#4, #10) y una (#9, +0,8) se lee débilmente como Ignacio: un fallo
  que la prueba deja a la vista; de las dos genuinas interpoladas (`mixed`), #11 se lee como Ignacio (+1,8, lo
  esperable de un texto interpolado y no reescrito) y #2 es discordante. El nivel 2 es conservador («dentro» para todas: la envolvente B solapa a E en un 41 %
  y G queda dentro de E en un 88 % con este núcleo de siete cartas breves), lo que el protocolo prevé: el nivel 2 no
  decide solo. Ninguna cifra de estas pruebas es un resultado de la investigación.

- Ruido de edición (§ 5.4): `scripts/ruido_edicion.py` con ventanas alineadas y recorte simétrico (D-022); probado
  con Tischendorf y Nestle 1904 sobre el corpus del estrato 4 (`results/prueba_ruido/`): ruido alineado 0,03-0,12
  (min-max) frente a una distancia mínima entre cartas del núcleo de 0,54; hallazgo de datos: el NT de PROIEL no
  contiene Hebreos 13 (ni 1-2 Juan ni 2 Pedro), de ahí el recorte simétrico (278 de 303 versículos de Hebreos).
  La distancia de una carta larga consigo misma con ventanas independientes (0,4-0,58) es del orden de la distancia
  entre cartas del núcleo: las distancias del «mismo rasero» llevan dentro la variación entre pasajes, que afecta por
  igual a las envolventes y a las cartas y que el *bootstrap* de ventanas cuantifica.

- Sello 2: versión `1.0.0`; `python -m paulinum seal … --etiqueta paulinum-1.0.0` en el portátil → huella
  `cd32dad63855460c77a200606d81b2bd863f9e4d3121926aead66e9a6b0a29ef` (50 archivos: paquete, metadatos, configuración,
  protocolo, 18 guiones, 2 guiones de testigos, 9 configuraciones de sensibilidad y el lexicón), `SELLO.json` y
  `SELLO_paulinum-1.0.0.json`; el Sello 1 se conserva en `SELLO_protocolo-1.0.0.json`. Etiqueta `paulinum-1.0.0`,
  *release* de GitHub; Zenodo archivó la *release* el mismo día: DOI 10.5281/zenodo.22996786 (registro 22996786). `pytest` 10/10 y `selftest` 25/25 (huella `ecaf6572…`)
  en el portátil y en la nube.

**Decisiones.** D-014 a D-022; enmiendas 3 y 4 del registro del protocolo.

**Pendiente (bloque 5, después del Sello 2).** Campaña principal en el laboratorio de Actions en el orden de
`docs/laboratorio_actions.md` (anotación; especificaciones por familia; calibración, envolventes y variables
publicadas antes de las dianas; *bootstrap*; segundo modelo; sensibilidad; veredicto; Sello 3); después, los tres
canales no estilométricos (§ 9) y el montaje de los Tomos IV-VI.

## Sesión 3 — 2026-09-27 — Bloque 5: campaña principal `paulinum_1_0` en el laboratorio de Actions

**Objeto.** Puntos 4 y 5 de § 3.3: ejecutar la campaña principal con el código del Sello 2 (`paulinum-1.0.0`), en el
orden de `docs/laboratorio_actions.md`, y cerrar con el veredicto mecánico y el Sello 3.

**Antes de lanzar nada (13:00 UTC).** Enmienda 5 del registro del protocolo: *run* auxiliar `paulinum_1_0_calibracion`
(`config/paulinum_1_0_calibracion.yaml`, copia del sellado con `sin_dianas: true`) para publicar calibración y
envolventes antes de la primera fila de diana; anotada la observación sobre las semillas por índice (las filas de
respuesta conocida del auxiliar y del definitivo son equivalentes, no idénticas; las envolventes sí son idénticas).
El laboratorio `campana.yml` no se había ejecutado nunca: la primera orden (`anotacion`) sirve también de prueba de
punta a punta de la descarga de Diorisis desde figshare, la reconstrucción del lexicón y la comprobación de su huella.
Permiso de borrado concedido de nuevo para `Correccion_Fondo` (archivos de bloqueo de git). Las órdenes con hora y
duración quedan en `results/<run>/bitacora.md` (las escribe el propio código) y en los *logs* públicos de Actions.

**Primeras órdenes (13:14 UTC).** El token de acceso necesitaba el permiso `Actions: write` (el autor lo añadió). Lanzadas
`anotacion` (run `paulinum_1_0`) y `specs` de impostores del run auxiliar. La primera ejecución del laboratorio mostró un
fallo de infraestructura: el envío de resultados fallaba en silencio (árbol sucio por `data/provenance.json`, que `fetch`
reescribe). Flujo corregido (comprobación real de huellas, restauración del archivo canónico, fallo visible y artefacto
de respaldo; `docs/laboratorio_actions.md`); la ejecución de `specs` se canceló a los 25 min y se relanza con el flujo
corregido; `anotacion` se repite. Los resultados de `anotacion` de la primera ejecución no llegaron al repositorio.

**Laboratorio en marcha (13:29-13:46 UTC).** Con el flujo corregido: `ruido` publicado (`7acbd58`; ruido de edición
alineado 0,03-0,12 en min-max y 0,05-0,10 en Delta frente a una distancia mínima entre cartas del núcleo de 0,54-0,58,
en las ocho combinaciones de edición × métrica × máscara; `inventory.csv` de 857 documentos); `anotacion` publicado
(`c53f883`): el modelo de greCy no está disponible (D-023), se relanza con OdyCy `grc_odycy_joint_sm`. `specs` de
impostores del run auxiliar en curso desde las 13:36 UTC; dirichlet + NCD en cola. Réplica en la nube preparada
(corpus 857 documentos; lexicón y derivados de testigos traídos del portátil, huella del lexicón verificada; huella del
Sello 2 reproducida: `cd32dad6…`; `pytest` 10/10, `selftest` 25/25).

**Anotación uniforme (14:13-15:45 UTC).** Tres intentos hasta cargar OdyCy en el ejecutor (permiso `click` ausente con
typer ≥ 0,20; wheel publicado sin versión en el nombre, que pip rechaza: se descarga y se instala con nombre válido). El
guion sellado da acuerdo 0,148 / 0,487 (`ea436c9`, `7d6eb95`); el diagnóstico fuera del sello (`diagnostico/`,
`64a8a8d`) atribuye la cifra a dos defectos del guion (formato de etiqueta, sigma final) y mide 0,844 (0,916 con
equivalencias) / 0,942. Resultado del protocolo: **`pos3` descartada** (D-024); el bloque de sensibilidad `pos3` no se
ejecuta. Aux impostores: 16 especificaciones publicadas (`9029391`, 1 h 35 min; AUC epistolar 0,964-0,991, general
0,757-0,901 — las AUC generales bajas son de `lemma_dict:300` con Delta); dirichlet + NCD del auxiliar en curso.

**Registro en OSF (17:47 UTC).** Hecho desde el navegador integrado con la sesión del autor (proyecto OSF `bvq4n`,
creado por el autor; registro `nphcu`, plantilla *Open-Ended Registration*, licencia CC-BY 4.0, materias y etiquetas,
resumen con los diez puntos del protocolo y los tres DOI; público sin embargo; el autor pulsó la orden de registrar).
El autor lo aprobó minutos después: el registro es público (`Public registration`). Anotado en `REGISTRO.md` y `README.md`.

## Sesión 3 (continuación) — 2026-09-28 — Run auxiliar: dirichlet recuperado, NCD en paralelo

**Incidencia de cola (27-IX, 20:18 UTC).** La ejecución 36323226094 (`specs` dirichlet + NCD del auxiliar) agotó el tope de
5 h y su envío falló por conflicto con los archivos comunes de la campaña (arrancó del *commit* del lanzamiento, anterior
al de impostores). Dirichlet quedó completo (4 especificaciones; AUC epistolar 0,945-0,988; 2-3 min cada una) y NCD 000
con 964 de 1.597 problemas (≈ 18 s por problema con cuatro procesos: ≈ 8 h por especificación, muy por encima de las
≈ 1,5 h estimadas tras D-020). El autor descargó el artefacto `results-36323226094` y los archivos se integraron a mano
en `main` (`1365734`), con el registro de la ejecución añadido a `run.log`. Correcciones del flujo: avance a `main` al
inicio de cada ejecución, fusión por unión de bitácoras (`.gitattributes`), *rebase* con prevalencia de la ejecución
que envía, y clave de concurrencia por campaña × etapa × familias × `solo` (`14dff77`, `311a720`).
**Lanzamientos (04:45 UTC):** NCD `solo=0` (reanuda desde 964/1597) y NCD `solo=1` en paralelo; `ledger,variables` del
auxiliar (las envolventes E/B/G no dependen de las especificaciones). Falta `calibration` cuando NCD termine; después,
el *run* definitivo, cuyas familias correrán en paralelo.

**Envolventes del auxiliar publicadas (04:50 UTC, `8ddee38`; 12 s de cálculo).** E (intra-autor, cartas) 917 pares, B
(inter-autor) 1.560, G (saltos de género intra-autor) 715. Min-max: E mediana 0,624 (p90 0,681), G 0,631 (p90 0,684), B
0,690 (p90 0,744); el 88 % de G y el 41 % de B quedan por debajo del p90 de E. Delta: E 0,761 (p90 0,845), G 0,779
(0,856), B 0,817 (0,909); el 87 % de G y el 65 % de B por debajo del p90 de E. Lectura previa a las dianas (Hm2, § 2.3):
los saltos de género de un mismo autor se distribuyen como la variación intra-autor y por debajo de la inter-autor en
las dos medidas, pero B solapa mucho con E (más con Delta): el nivel 2 tendrá poca potencia para declarar «fuera», como
ya anticipó la prueba Ignacio (D-018). Las tres fusiones concurrentes de esta mañana (`1365734`, `8ddee38` y los NCD en
curso) se han integrado sin marcadores de conflicto en `bitacora.md` ni `run.log`.

**Run auxiliar cerrado (13:52 UTC, `f0c4cd2`): calibración sin dianas publicada.** 22 especificaciones (16 impostores +
4 Dirichlet + 2 NCD; NCD 001 en dos tramos, 884 + 713 problemas). 35.134 filas de respuesta conocida, ninguna de carta.
**Hm1 (§ 2.3, § 7.2): las tres familias son aptas.** AUC epistolar mediana: impostores 0,980 (mín. 0,964; 16/16 válidas),
NCD 0,975 (2/2), Dirichlet 0,963 (mín. 0,945; 4/4); AUC general 0,860 / 0,870 / 0,957; AUC cristiana 0,802 / 0,854 / 0,924.
**Falsación del método (§ 10.1), 3 Corintios frente al núcleo:** impostores lo detecta (puntuación < 0,5) solo en 6 de 16
especificaciones (las seis de `char3:600` y ninguna de `mfw`, `closed` ni `lemma_dict`: mediana 0,64) → **límite declarado
de la familia A frente a un imitador del mismo registro**, que acompañará como reserva expresa a todo veredicto que dependa
de ella; NCD (0,17; 0,19) y Dirichlet (0,00-0,06) lo detectan en todas. Otras pseudoepigrafías (impostores, mediana):
Ps-Clemente 0,14 (80/80 detectadas), Ps-Plutarco 0,34 (27/32), Ps-Ignacio 0,36 (67/96), Ps-Juliano 0,70 (25/160),
Ps-Basilio 0,89 (0/48: las cartas «espurias» de Basilio no se distinguen de las genuinas por estilo). Hm3 (`mediated_pairs`)
y el resto se leen con el veredicto. **Orden de § 3.3 cumplido:** calibración (`f0c4cd2`) y envolventes (`8ddee38`)
publicadas antes de calcular ninguna fila de diana.

## Sesión 4 — 2026-09-28 — Campaña definitiva `paulinum_1_0`

**13:53 UTC.** Lanzadas en paralelo las cuatro piezas de `specs` del *run* definitivo (`config/paulinum_1_0.yaml`, con
dianas): impostores (36431844159), Dirichlet (36431855988), NCD `solo=0` (36431867554) y NCD `solo=1` (36431879813); los
dos NCD necesitarán un segundo tramo. Después: `calibration,ledger,variables,rolling,extras`, `bootstrap`, `svm`,
bloques de sensibilidad (sin `pos3`, D-024; `testigos` en la réplica local) y `veredicto`.

**21:02-21:46 UTC.** Especificaciones del definitivo completas (22: NCD 000 y 001 en dos tramos cada una). Lanzados y
publicados el cierre del definitivo `calibration,ledger,variables,rolling,extras` (36483350754, `ef0bdee`) y el de
`nucleos` (36483342044, `8d1ede3`), sin errores. Las `specs` del bloque `ediciones` (36483333382, `3dd808d`) se detuvieron
en la especificación 008 (`closed:150` sobre Tischendorf): el inventario de clase cerrada del código sellado depende de
las etiquetas MorphGNT y esas ediciones llevan PROIEL y MACULA (inventario vacío, `ValueError` en la primera iteración).
Comprobado en la réplica: `closed` = 0 formas en Tischendorf y Nestle 1904, 346 en SBLGNT y 308 en los derivados de los
testigos (que sí llevan MorphGNT). **D-025:** las 8 + 4 especificaciones `closed:150` del bloque quedan sin calcular; el
resto (impostores 016-031, Dirichlet 000-003) se lanza con `solo`. El bloque `testigos` sigue en la réplica de la nube
(64 impostores + 16 Dirichlet, dos procesos, ≈ 6 min por especificación; el contenedor pierde los procesos al quedar
inactivo, así que se mantiene la sesión activa hasta que termine). Lanzados `bootstrap` y `svm` del definitivo (22:04 UTC) y las dos piezas restantes de `ediciones` (22:05 UTC).
**29-IX, 00:04-00:20 UTC.** Bloque `ediciones` cerrado (`calibration,ledger,extras`, 36500436863, `cf4574d`; 28
especificaciones, D-025). Ruido de edición con los testigos manuscritos, calculado en la réplica (los derivados no se
publican; `scripts/ruido_edicion.py --ediciones sinaiticus,p46`, 32 s) y añadido a `ruido_edicion_{minmax,delta,resumen}.csv`
del definitivo: Sinaítico en las 14 cartas, 𝔓46 en 8 (el papiro no conserva, o no llega a 100 palabras, en 1 Tes, 2 Tes,
1 Tim, 2 Tim, Tit y Flm: dato del canal de transmisión); el ruido máximo queda por debajo de la distancia mínima entre
cartas del núcleo en las ocho combinaciones (medida × máscara × testigo). El bloque `testigos` pasa a ejecutarse por
trozos de cuatro especificaciones en procesos nuevos: el proceso único crecía ≈ 100 MB por especificación y el límite
de memoria del contenedor (6,27 GB) lo abatió en la 29.ª (reanudado por problema, sin pérdida).

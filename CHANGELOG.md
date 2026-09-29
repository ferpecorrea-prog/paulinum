# Registro de cambios

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado semántico para el software;
cada campaña de investigación lleva además su propia etiqueta (`campana-XX-sellado`, `campana-XX-resultados`).

## [resultados-1.0.0] — 2026-09-29 — Sello 3 (resultados de la campaña `paulinum_1_0`)

Sin cambio de versión del software (sigue 1.0.0; el código sellado no se ha tocado: huella del Sello 2 `cd32dad6…29ef`
comprobada). Esta etiqueta congela `results/` (huella `980b3ab2…c1b3`, 765 archivos, `protocols/paulinum_1_0/SELLO_resultados-1.0.0.json`).

### Añadido
- **Resultados de la campaña `paulinum_1_0`** (`results/paulinum_1_0/`): 22 especificaciones (16 impostores, 2 NCD,
  4 Dirichlet) con filas de diana; calibraciones (Hm1: las tres familias aptas), envolventes E/B/G, «mismo rasero»,
  núcleo más próximo, bootstrap de percentiles, segundo modelo (SVM), variables de situación, ventanas deslizantes,
  ruido de edición con Tischendorf, Nestle 1904, Sinaítico y 𝔓46, y el **veredicto mecánico** (`veredicto.csv`,
  `veredicto.md`; § 8 del protocolo, `scripts/veredicto.py` sellado).
- **Run auxiliar `paulinum_1_0_calibracion`** (enmienda 5): calibración y envolventes publicadas antes de calcular
  ninguna fila de diana (§ 3.3).
- **Siete bloques de sensibilidad** (`results/paulinum_1_0/sensibilidad/`): `nucleos`, `ventana300`,
  `documento_entero`, `rasgos`, `coseno`, `nodia`, `ediciones` (28 de 40 especificaciones, D-025) y `testigos`
  (80 especificaciones, calculadas en la réplica local: los derivados de los testigos no se redistribuyen).
  `pos3` descartado (D-024).
- **Validación de la anotación uniforme** (`results/anotacion/`): OdyCy en lugar de greCy (D-023), diagnóstico
  fuera del conjunto sellado (`diagnostico/`).
- **Comprobaciones de falsación** (§ 10): 3 Corintios (límite declarado de la familia A), cartas breves de Basilio y
  Libanio (`falsacion_cartas_breves_*.csv`, D-026), Hm2, Hm3 y § 10.3, documentadas en `docs/registro_investigacion.md`.
- `herramientas/` (fuera del conjunto sellado): `sellar_resultados.py` y `falsacion_cartas_breves.py` (D-026).
- Laboratorio de cómputo en GitHub Actions (`.github/workflows/campana.yml`, `docs/laboratorio_actions.md`): registros
  públicos de cada ejecución en `results/`, reanudación por problema, fusión por unión de bitácoras.

### Registrado
- Enmienda 5 (`protocols/paulinum_1_0/REGISTRO.md`), decisiones D-023 a D-026 (`docs/decisiones.md`), registro en OSF
  (osf.io/nphcu), sesiones 3-5 del registro de investigación.

## [1.0.0] — 2026-09-27 — Sello 2 (`paulinum-1.0.0`, código congelado)

El código de esta versión es el que ejecuta la campaña `paulinum_1_0`; después de este sello no cambia salvo por
enmienda registrada en `protocols/paulinum_1_0/REGISTRO.md` (§ 12 del protocolo), que llevaría versión 1.0.1.

### Añadido
- **Protocolo preregistrado de paulinum 1.0** (`protocols/paulinum_1_0/PROTOCOLO.md`, `config/paulinum_1_0.yaml`,
  `SELLO.json`, `REGISTRO.md`): hipótesis H1-H5 con predicciones por canal, catorce dianas con el mismo rasero,
  tres familias de métodos (impostores, compresión NCD, Dirichlet-multinomial jerárquico), calibración epistolar
  principal, envolventes intra-autor, inter-autor y de saltos de género con regla de equivalencia, veredicto
  mecánico, protocolo de los tres canales no estilométricos, falsación, tres sellos.
- Ampliación del corpus (estrato 4, `sources.CONTROLS_10`): Basilio de Cesarea (368 cartas con auditoría
  conservadora de estados; *A los jóvenes*), Libanio (839 cartas; seis discursos), Juliano (siete discursos y dos
  cartas públicas), Alcifrón por libros, Eliano, Plotino/Porfirio, Ps-Clemente *De virginitate*, trece colecciones
  pseudoepigráficas de Hercher.
- Hebreos como diana (`target`, D-002): máscaras de cierre epistolar y de 35 tramos de citas del AT cotejados
  con NA28 (`metadata/masks.csv`; enmienda 1 del protocolo); máscara de citas de las otras trece cartas cotejada con
  NA28 por el mismo procedimiento (enmienda 2: once tramos añadidos), variables de situación (`metadata/letter_variables.csv`); `TARGETS` con siete cartas;
  núcleo de sensibilidad `trece`.
- `paulinum seal --protocol/--sin-lexicon/--etiqueta`; `Source.group_tokens` y agrupación de cartas consecutivas en
  `parsers.parse_tei`; `by_tier(4)` con sustitución de `Liban_Ep` y `Alciphr`.
- 3 Corintios validado (D-007): `data/local/3Cor.txt` y `3Cor_alineacion.tsv` definitivos, huella en `data/provenance.json`.
- Infraestructura de investigación reproducible: `.zenodo.json`, `CITATION.cff` con ORCID, licencias MIT + CC BY 4.0,
  `docs/registro_investigacion.md`, `docs/decisiones.md`, comprobación automática (`.github/workflows/selftest.yml`).
- Carpeta `protocols/` para los protocolos sellados y sus registros públicos.
- **Implementación completa del protocolo paulinum 1.0 (Sello 2, `paulinum-1.0.0`)**: familias de métodos B
  (`verify.NCDEngine`, compresión LZMA2 preset 6, D-020) y C (`verify.DirichletEngine`, Dirichlet-multinomial
  jerárquico con perfiles de autor, D-019); problemas `pos_epist`/`neg_epist` (D-014), `genre_pairs`,
  `mediated_pairs`, modo `sin_dianas` y núcleo/dianas a medida; calibraciones general, epistolar (principal) y
  cristiana con sus razones de verosimilitud; etapa `specs` reanudable por problema y paralela
  (`run --workers/--familias/--solo`); envolventes E, B y G, `nearest_author` con IC del margen (D-021);
  `scripts/veredicto.py` (veredicto mecánico de § 8), `scripts/bootstrap_percentil.py` (IC por autores, por ventanas y
  *leave-one-author-out* de pct_E, pct_B, pct_G), `scripts/anotacion_uniforme.py` (validación de la anotación
  uniforme, D-016), `scripts/generar_sensibilidad.py` y `config/sens/*.yaml` (nueve bloques de sensibilidad);
  espacio `pos3:N`; ediciones de testigos manuscritos (`sinaiticus`, `sblgnt_rec_sinaiticus`, `p46`,
  `sblgnt_rec_p46`, D-013); `seal` con `SELLO_<etiqueta>.json`, `scripts/*/` y `config/sens/` en el sello.
- Laboratorio de cómputo en GitHub Actions (`.github/workflows/campana.yml`, `docs/laboratorio_actions.md`, D-017),
  con reconstrucción del lexicón y comprobación de su huella contra el sello.
- Pruebas de validación sin dianas (D-018): `config/prueba_1_0.yaml`, `config/prueba_veredicto_ignacio.yaml` y sus
  resultados en `results/prueba_1_0/` y `results/prueba_veredicto_ignacio/`; `tests/test_paulinum_1_0.py`.
- NA28 no entra como edición (escaneo sin capa de texto; D-015, enmienda 3): solo máscaras.
- `scripts/ruido_edicion.py` (ruido de edición con ventanas alineadas y recorte simétrico, D-022) y máscara `reuse`
  trasladable a otras ediciones y testigos por versículo y posición (`corpus.reuse_refs_table`).

### Cambiado
- `paulinum/__init__.py`: versión `1.0.0.dev0` durante el desarrollo y `1.0.0` en el Sello 2; `verify.build_problems` no incluye la diana entre sus candidatos
  con el núcleo `trece`.
- `pipeline.Context.corpus` lee la capa `pos_uniforme` de `data/cache/` o, si falta, de
  `results/anotacion/pos_uniforme_<edición>.jsonl.gz`; `selftest.yml` no se lanza por cambios en `results/`;
  `.gitignore` excluye los tensores `.npy` de resultados y los XML y derivados de testigos.
- `README.md` reescrito para la nueva investigación; el README de la reconstrucción pasa a `docs/README_reconstruccion_0.2.0-r.md`.
- `pyproject.toml` y `CITATION.cff`: versión `1.0.0`.

## [0.2.0-r] — 2026-09-25

- Reconstrucción del laboratorio publicado (código reimplementado a partir de la especificación del libro; resultados
  publicados transcritos como referencia; sellos publicados no reproducibles). Véase `LEEME_PRIMERO.md`.

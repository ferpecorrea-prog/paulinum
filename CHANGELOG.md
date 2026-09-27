# Registro de cambios

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado semántico para el software;
cada campaña de investigación lleva además su propia etiqueta (`campana-XX-sellado`, `campana-XX-resultados`).

## [Sin publicar] — 1.0.0.dev0

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
- `paulinum/__init__.py`: versión `1.0.0.dev0`; `verify.build_problems` no incluye la diana entre sus candidatos
  con el núcleo `trece`.
- `pipeline.Context.corpus` lee la capa `pos_uniforme` de `data/cache/` o, si falta, de
  `results/anotacion/pos_uniforme_<edición>.jsonl.gz`; `selftest.yml` no se lanza por cambios en `results/`;
  `.gitignore` excluye los tensores `.npy` de resultados y los XML y derivados de testigos.
- `README.md` reescrito para la nueva investigación; el README de la reconstrucción pasa a `docs/README_reconstruccion_0.2.0-r.md`.
- `pyproject.toml`: versión `1.0.0.dev0`.

## [0.2.0-r] — 2026-09-25

- Reconstrucción del laboratorio publicado (código reimplementado a partir de la especificación del libro; resultados
  publicados transcritos como referencia; sellos publicados no reproducibles). Véase `LEEME_PRIMERO.md`.

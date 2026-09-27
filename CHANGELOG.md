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
  con NA28 (`metadata/masks.csv`; enmienda 1 del protocolo), variables de situación (`metadata/letter_variables.csv`); `TARGETS` con siete cartas;
  núcleo de sensibilidad `trece`.
- `paulinum seal --protocol/--sin-lexicon/--etiqueta`; `Source.group_tokens` y agrupación de cartas consecutivas en
  `parsers.parse_tei`; `by_tier(4)` con sustitución de `Liban_Ep` y `Alciphr`.
- 3 Corintios validado (D-007): `data/local/3Cor.txt` y `3Cor_alineacion.tsv` definitivos, huella en `data/provenance.json`.
- Infraestructura de investigación reproducible: `.zenodo.json`, `CITATION.cff` con ORCID, licencias MIT + CC BY 4.0,
  `docs/registro_investigacion.md`, `docs/decisiones.md`, comprobación automática (`.github/workflows/selftest.yml`).
- Carpeta `protocols/` para los protocolos sellados y sus registros públicos.

### Cambiado
- `paulinum/__init__.py`: versión `1.0.0.dev0`; `verify.build_problems` no incluye la diana entre sus candidatos
  con el núcleo `trece`.
- `README.md` reescrito para la nueva investigación; el README de la reconstrucción pasa a `docs/README_reconstruccion_0.2.0-r.md`.
- `pyproject.toml`: versión `1.0.0.dev0`.

## [0.2.0-r] — 2026-09-25

- Reconstrucción del laboratorio publicado (código reimplementado a partir de la especificación del libro; resultados
  publicados transcritos como referencia; sellos publicados no reproducibles). Véase `LEEME_PRIMERO.md`.

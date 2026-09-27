# Registro de cambios

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado semántico para el software;
cada campaña de investigación lleva además su propia etiqueta (`campana-XX-sellado`, `campana-XX-resultados`).

## [Sin publicar] — 1.0.0.dev0

### Añadido
- Infraestructura de investigación reproducible: `.zenodo.json`, `CITATION.cff` con ORCID, licencias MIT + CC BY 4.0,
  `docs/registro_investigacion.md`, `docs/decisiones.md`, comprobación automática (`.github/workflows/selftest.yml`).
- Carpeta `protocols/` para los protocolos sellados y sus registros públicos.

### Cambiado
- `README.md` reescrito para la nueva investigación; el README de la reconstrucción pasa a `docs/README_reconstruccion_0.2.0-r.md`.
- `pyproject.toml`: versión `1.0.0.dev0`.

## [0.2.0-r] — 2026-09-25

- Reconstrucción del laboratorio publicado (código reimplementado a partir de la especificación del libro; resultados
  publicados transcritos como referencia; sellos publicados no reproducibles). Véase `LEEME_PRIMERO.md`.

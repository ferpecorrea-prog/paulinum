# Protocolos sellados

Cada campaña de la nueva investigación tendrá aquí una carpeta `<campaña>/` con:

- `PROTOCOLO.md`: hipótesis, corpus, controles y estados, rejilla de especificaciones, reglas de decisión,
  condiciones de falsación y regiones de equivalencia, todo fijado antes de ejecutar.
- `SELLO.json`: huella SHA-256 del conjunto sellado (código, metadatos, configuración, protocolo) y la lista de
  archivos que cubre, calculada con `python -m paulinum seal`.
- `REGISTRO.md`: identificadores del registro público (DOI de Zenodo de la *release* de sellado; registro en OSF
  cuando se haga) y fecha.

Ningún resultado de una diana se mira antes de que exista la carpeta correspondiente con sus tres archivos.

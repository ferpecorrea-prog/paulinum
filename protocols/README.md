# Protocolos sellados

Cada campaña de la nueva investigación tiene aquí una carpeta `<campaña>/` con:

- `PROTOCOLO.md`: hipótesis, corpus, controles y estados, preparación de los textos, rejilla de especificaciones,
  familias de métodos, problemas de calibración, reglas de decisión, condiciones de falsación y regiones de
  equivalencia, protocolo de los canales no estilométricos, orden de ejecución y política de enmiendas, todo fijado
  antes de ejecutar.
- `SELLO.json`: huella SHA-256 del conjunto sellado (protocolo, configuración, código, metadatos, guiones) y la lista
  de archivos que cubre, calculada con `python -m paulinum seal --protocol protocols/<campaña>`.
- `REGISTRO.md`: etiquetas de git, *releases* de GitHub, DOI de Zenodo (y registro en OSF cuando se haga) de cada
  sello, y la lista de enmiendas.

Campañas:

| campaña | protocolo | sellos |
|---|---|---|
| `paulinum_1_0` — verificación convergente de las catorce cartas | [`paulinum_1_0/PROTOCOLO.md`](paulinum_1_0/PROTOCOLO.md) | 1 protocolo (`protocolo-1.0.0`) · 2 código congelado (`paulinum-1.0.0`, pendiente) · 3 resultados (`resultados-1.0.0`, pendiente) |

Ningún resultado de una diana se calcula antes de que existan el Sello 1 y el Sello 2 de su campaña.

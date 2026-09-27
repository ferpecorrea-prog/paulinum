# Testigos manuscritos para `nuevo_paulinum`

Este directorio fue preparado automáticamente para el control de sensibilidad
textual/manuscrita del proyecto.

## Archivos principales

- `sinaiticus_project_v105.xml`: transcripción oficial publicada del Codex
  Sinaiticus, versión 1.05 (7-09-2020), depositada por ITSEE/University of
  Birmingham.
- `p46_ntvmr_10046.xml`: transcripción TEI XML publicada por NTVMR del testigo
  GA P46 (docID 10046), obtenida con `pageID=ALL&format=teiraw`.
- `sinaiticus_ntvmr_20001.xml`: solo si se usó
  `--include-ntvmr-sinaiticus`; permite comparar 01 y P46 bajo la misma
  infraestructura NTVMR.
- `TESTIGOS_MANIFEST.json`: procedencia, URL exacta, fecha de adquisición, tamaño y
  SHA-256 de cada descarga.

## Criterio metodológico

Estos archivos deben usarse como **testigos de sensibilidad textual**, no como
si la ortografía, puntuación, segmentación o hábitos gráficos de los copistas
fueran rasgos autorales de Pablo. Para análisis de autoría:

1. conservar el XML bruto sin modificar;
2. generar derivados normalizados en archivos separados;
3. trabajar solo sobre pasajes realmente conservados en cada testigo;
4. no imputar lagunas de P46;
5. documentar exactamente cualquier normalización (nomina sacra, diacríticos,
   puntuación, itacismos, correcciones, expansiones, supplied/lacunae, etc.);
6. ejecutar el análisis principal sobre la representación textual fijada por el
   protocolo y usar 01/P46 como prueba de robustez frente a variación textual y
   scribal;
7. conservar los SHA-256 del manifiesto para que el estado exacto usado en una
   publicación pueda reproducirse.

P46 es lacunoso y no conserva todo el corpus paulino. El control directo entre
01 y P46 debe restringirse a las unidades textuales solapadas.

## Fuentes

Sinaiticus v1.05:
https://epapers.bham.ac.uk/id/eprint/3306/

NTVMR API:
https://ntvmr.uni-muenster.de/community/api/transcript/get/

P46: docID 10046.
Sinaiticus/01: docID 20001.

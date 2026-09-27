# Derivados de los testigos manuscritos: qué se publica y con qué licencia

Los ficheros de esta carpeta que contienen recuentos y huellas (`RESUMEN.json`, `cobertura.csv`, `acuerdo_*.csv`,
`p46_contenido_y_orden.csv`) son datos propios del proyecto (CC BY 4.0). Los ficheros con texto íntegro
(`*_bruto.txt`, `*_reg.txt`, `*_sblgnt_recortado.txt`) no se versionan ni se redistribuyen; se publican sus huellas.

`intervenciones.tsv` y `discrepancias_transcripciones_01_muestra.tsv` contienen palabras sueltas de las
transcripciones (forma original y forma resultante de cada transformación), imprescindibles para verificar las reglas.
Las filas con testigo `sinaiticus` derivan de la transcripción del proyecto Codex Sinaiticus (© Codex Sinaiticus
Project Board; ITSEE, Universidad de Birmingham; versión 1.05, 2020; https://epapers.bham.ac.uk/id/eprint/3306/),
disponible para reutilización no comercial con atribución (CC BY-NC-SA 3.0): esas filas se publican bajo esa misma
licencia. Las filas con testigo `p46` (y la copia NTVMR del Sinaítico) derivan de las transcripciones del INTF
publicadas en NTVMR (docID 10046 y 20001), CC BY 4.0.

Reglas de derivación: `docs/testigos_manuscritos.md`; guion: `scripts/testigos/derivar_testigos.py`.

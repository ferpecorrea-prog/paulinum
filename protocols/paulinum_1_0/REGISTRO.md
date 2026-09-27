# Registro público del protocolo paulinum 1.0

| sello | etiqueta de git | huella SHA-256 del conjunto | *release* de GitHub | DOI de Zenodo | fecha |
|---|---|---|---|---|---|
| 1. Protocolo preregistrado | `protocolo-1.0.0` | véase `SELLO.json` (campo `sha256`) | https://github.com/ferpecorrea-prog/paulinum/releases/tag/protocolo-1.0.0 | https://doi.org/10.5281/zenodo.22993122 (registro 22993122; DOI de concepto de todas las versiones: https://doi.org/10.5281/zenodo.22993121) | 2026-09-27 |
| 2. Código congelado | `paulinum-1.0.0` | — | — | — | — |
| 3. Resultados | `resultados-1.0.0` | — | — | — | — |

Registro en OSF: pendiente (se hará con el DOI del Sello 1 como documento de preregistro).

## Enmiendas

Formato de cada entrada: fecha · alcance · motivo · afecta a filas de diana ya calculadas: sí/no · nuevo sello: sí/no.

1. **2026-09-27** · metadatos: `metadata/masks.csv`, máscara `otq` de Hebreos · motivo: cotejo previsto en § 5.2 y D-012
   con el texto de NA28 (2012), hecho página a página sobre el ejemplar del autor (pp. 657-684; criterio: tramos en
   cursiva = citas): se añaden ocho tramos que NA28 imprime en cursiva y faltaban en la lista de partida (3,5; 7,1-2; 7,4;
   10,8-9; 10,28; 11,21; 12,15; 12,29) y se retira uno que NA28 imprime en redonda (12,20). Cobertura de Hebreos: citas
   21,7 % (antes 18,6 %), total con cierre 24,1 % (Romanos 23,2 %). SHA-256 de `metadata/masks.csv`: antes `757c3761fa341edefc0ddb4288adc439c9dfcc52939baea62af67fee72cda93a`,
   después `7b1a49f2f06c4ea57755ed31f711c7bf84b9ba48c0be6b1f340620eb7b1d6cf0` · afecta a filas de diana ya calculadas: **no** (ninguna calculada) · nuevo sello: **no** (§ 12:
   enmienda de metadatos prevista; el Sello 2 cubrirá el archivo corregido).

2. **2026-09-27** · metadatos: `metadata/masks.csv`, máscara `otq` de las trece cartas con nombre de Pablo · motivo: mismo
   rasero con Hebreos (enmienda 1): las máscaras de citas de las trece venían de las fichas del libro anterior y se han
   cotejado página a página con el texto de NA28 (pp. 481-656 del ejemplar del autor; criterio: cursiva = cita, por
   versículos completos). Los tramos de partida están todos en cursiva en NA28; se añaden once tramos breves que NA28
   imprime en cursiva y faltaban: Rom 2,6; 4,23; 11,2; 1 Cor 9,10; 14,25; 15,25; 2 Cor 9,7; 9,10; Ef 1,22; 4,9-10;
   1 Tim 5,19. Sin cambios en Flp, Col, 1-2 Tes, 2 Tim, Tit y Flm (Tit 1,12, cita pagana, no es del AT; Ef 5,14, de
   origen desconocido, ya está en `preformed`). Cobertura de citas: Rom 14,6 % (antes 14,0), 1 Cor 4,9 % (4,1),
   2 Cor 4,2 % (3,3), Ef 5,3 % (3,4), 1 Tim 1,8 % (0,9). SHA-256 de `metadata/masks.csv`: antes `7b1a49f2f06c4ea57755ed31f711c7bf84b9ba48c0be6b1f340620eb7b1d6cf0`, después
   `2410dadf8b3dae40299b19e9a1e16ada2a94b92db5f669dff37635066ef29bf7` · afecta a filas de diana ya calculadas: **no** · nuevo sello: **no** (§ 12).

3. **2026-09-27** · § 5.4, edición NA28 de sensibilidad · motivo: contingencia prevista en el propio § 5.4 («si la
   extracción resulta ruidosa … se descarta y se dice»): el ejemplar del autor es un escaneo sin capa de texto y no se
   hace OCR (D-015); NA28 queda solo como fuente de las máscaras `otq` (enmiendas 1 y 2) y el ruido de edición se mide
   con Tischendorf, Nestle 1904 y los testigos manuscritos (D-013) · afecta a filas de diana ya calculadas: **no** ·
   nuevo sello: **no** (no cambia ninguna regla; el Sello 2 congela la implementación resultante).

4. **2026-09-27** · implementación previa al Sello 2, sin cambio de reglas (§ 12) · alcance y motivo: (a) `epist_pairs`
   de § 7.1 como conjuntos propios `pos_epist`/`neg_epist` (D-014); (b) familia C con perfiles de autor a ambos lados
   (D-019); (c) familia B con diccionario LZMA2 ajustado, salida idéntica al preset 6 (D-020); (d) tensor rectangular
   para envolventes y núcleo más próximo, y nombres de archivos de resultados (D-021); (e) anotación uniforme
   validada en GitHub Actions o descartada con informe (D-016); (f) entorno de cómputo adicional al de § 3.4: laboratorio
   de GitHub Actions, 4 procesos por tarea, mismo código sellado, resultados publicados por *commit* (D-017); (g) modo
   `sin_dianas` y prueba de respuesta conocida Ignacio/Ps-Ignacio como validación del veredicto antes de congelar el
   código (D-018); (h) ruido de edición con ventanas alineadas y recorte simétrico, y máscara `reuse` por versículo en
   las otras ediciones (D-022) · afecta a filas de diana ya calculadas: **no** (ninguna calculada) · nuevo sello: **no** (todo queda
   dentro del Sello 2).

## Verificación

Con el repositorio en la etiqueta indicada:

```bash
python -m paulinum seal --config config/paulinum_1_0.yaml --run paulinum_1_0 --protocol protocols/paulinum_1_0 --sin-lexicon --etiqueta protocolo-1.0.0
```

debe reproducir la huella de `SELLO.json` (el campo `sealed_utc` cambia; la huella no).

# Registro público del protocolo paulinum 1.0

| sello | etiqueta de git | huella SHA-256 del conjunto | *release* de GitHub | DOI de Zenodo | fecha |
|---|---|---|---|---|---|
| 1. Protocolo preregistrado | `protocolo-1.0.0` | `9b65c9d823691887279abb93522a8dbd1479ec7b08fef411dc099bf083edbfe4` (34 archivos, sin lexicón; conservado en `SELLO_protocolo-1.0.0.json`) | https://github.com/ferpecorrea-prog/paulinum/releases/tag/protocolo-1.0.0 | https://doi.org/10.5281/zenodo.22993122 (registro 22993122; DOI de concepto de todas las versiones: https://doi.org/10.5281/zenodo.22993121) | 2026-09-27 |
| 2. Código congelado | `paulinum-1.0.0` | `cd32dad63855460c77a200606d81b2bd863f9e4d3121926aead66e9a6b0a29ef` (50 archivos, con el lexicón; `SELLO.json` = `SELLO_paulinum-1.0.0.json`) | https://github.com/ferpecorrea-prog/paulinum/releases/tag/paulinum-1.0.0 | https://doi.org/10.5281/zenodo.22996786 (registro 22996786; misma serie que el Sello 1 bajo el DOI de concepto 10.5281/zenodo.22993121) | 2026-09-27 |
| 3. Resultados | `resultados-1.0.0` | — | — | — | — |

Registro en OSF: **https://osf.io/nphcu** (plantilla *Open-Ended Registration*, proyecto https://osf.io/bvq4n; documento registrado: el protocolo del Sello 1 con DOI 10.5281/zenodo.22993122; enviado el 27-IX-2026, 17:47 UTC, público sin embargo, pendiente de la aprobación del autor como administrador, que OSF concede automáticamente a las 48 h si no se pulsa antes; texto en `docs/osf_registro_texto.md`).

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

5. **2026-09-27** · operativa (§ 3.3, punto 4; § 11), sin cambio de código ni de reglas · alcance: se añade
   `config/paulinum_1_0_calibracion.yaml`, copia exacta del archivo sellado `config/paulinum_1_0.yaml` con dos diferencias
   y solo dos (`nombre: paulinum_1_0_calibracion` y `parametros.sin_dianas: true`; comprobable con `diff`), para ejecutar en
   el laboratorio de Actions un *run* auxiliar con **solo problemas de respuesta conocida** (etapas `specs`,
   `calibration`, `ledger`, `variables`) y publicarlo (*commit* `[lab]`) **antes** de que la campaña `paulinum_1_0`
   calcule ninguna fila de diana · motivo: la etapa `specs` del código sellado calcula en una sola pasada los problemas
   de respuesta conocida y las filas `target`/`core_loo`, así que sin el *run* auxiliar no podría cumplirse literalmente
   el punto 4 de § 3.3 (calibración y envolventes cerradas y publicadas antes de calcular ninguna diana) ·
   observación registrada antes de ejecutar: en `paulinum/pipeline.py` la semilla de cada problema es
   `semilla_de_la_especificación × 100003 + índice_del_problema_en_la_lista`, y con `sin_dianas` la lista no contiene los
   14 problemas de carta (7 `core_loo` + 7 `target`) que encabezan la lista de la campaña completa; los índices —y por
   tanto las semillas— de los problemas de respuesta conocida difieren en 14 posiciones entre el *run* auxiliar y el
   definitivo, de modo que sus puntuaciones son **equivalentes** (mismos problemas, mismos parámetros, distinto
   sorteo), **no idénticas** (corrige lo que decía `docs/ESTADO_DEL_PROYECTO_2026-09-27.md` § 5). Las envolventes E, B y G
   y los pares de género usan semillas fijas propias (`variables.py`) y sí son idénticas en ambos *runs*. Consecuencias
   fijadas ahora: (a) no se copian parciales del auxiliar al definitivo: cada *run* se reproduce desde cero con su
   orden; (b) el veredicto usa la calibración del *run* definitivo, calculada por el mismo código sellado; (c) la
   comparación auxiliar/definitivo (AUC por especificación, aptitud de familias, envolventes) se informa como
   comprobación de estabilidad Monte Carlo · afecta a filas de diana ya calculadas: **no** (ninguna calculada) · nuevo
   sello: **no** (§ 12: el archivo nuevo no está en el conjunto sellado y ningún archivo sellado cambia; la huella
   `cd32dad6…` sigue siendo reproducible).

## Verificación

Con el repositorio en la etiqueta indicada:

```bash
# Sello 1 (etiqueta protocolo-1.0.0): sin lexicón
python -m paulinum seal --config config/paulinum_1_0.yaml --run paulinum_1_0 --protocol protocols/paulinum_1_0 --sin-lexicon --etiqueta protocolo-1.0.0
# Sello 2 (etiqueta paulinum-1.0.0): con el lexicón uniforme reconstruido desde MorphGNT + PROIEL + Diorisis
python -m paulinum fetch --tier 1 --editions
python scripts/construir_lexicon.py --diorisis-zip <ruta a Diorisis.zip>     # SHA-256 esperado: b0ea6312…4ea7
python -m paulinum seal --config config/paulinum_1_0.yaml --run paulinum_1_0 --protocol protocols/paulinum_1_0 --etiqueta paulinum-1.0.0
```

debe reproducir la huella de `SELLO_<etiqueta>.json` (el campo `sealed_utc` cambia; la huella no). El lexicón no se
redistribuye (Diorisis es CC BY-NC-SA): su huella `b0ea6312655cbe8fdd5f92337089a7b9e5f961d7f2d5aa1b6e67bf25440c4ea7` está
en el sello y el laboratorio de GitHub Actions la comprueba en cada ejecución (`docs/laboratorio_actions.md`).

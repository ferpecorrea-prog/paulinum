# Segunda campaña de la Investigación 1 (P1-P12): protocolo reconstruido

El protocolo original se selló el 3 de septiembre de 2026 a las 17:08:17 UTC con la huella SHA-256
`6071b19c18a3025422a71dc870ce9784dcadfbdb25b870e5a3b3640687867419` (nota 46 del libro). Ese archivo,
la biblioteca `stylolib` original, los resultados en CSV, el manifiesto de huellas y el fichero de
desviaciones se perdieron con el laboratorio. Lo que sigue es la reconstrucción de los doce
experimentos a partir del § 4.5 del capítulo 2 y de los apartados 8-10 del Apéndice de auditoría, con
el estado de cada uno en esta carpeta.

| exp. | contenido (según el libro) | regla de decisión / condición de falsación publicada | estado en la reconstrucción |
|---|---|---|---|
| P1 | co-remitente: efecto de los co-remitentes sobre las trece cartas (13 lemas) | descriptivo | reconstruible con `stylolib.matriz_13_lemas` y `metadata/letter_variables.csv` (n_cosenders); no se ha ejecutado |
| P2 | réplica de la capa de 13 lemas sobre MorphGNT y Diorisis | orden conservado (correlación de rangos ≥ 0,9) | `p2_replica_morphgnt.py`: rho = 0,991 (publicado 0,99); Col 2,32 ✓; LOO del núcleo reproducido con diferencias ≤ 0,1; Diorisis requiere el zip |
| P3 | morfosintaxis (MorphGNT): categorías, casos, tiempos, modos, voces, bigramas de categorías | divergente si queda más lejos que todos los controles ajenos en 2 de 3 familias | `p3_p7_p9_p11_lemas_morfologia.py` (familias: categorías, modos+personas, bigramas; los casos no están en la caché del corpus y se documentan como extensión) |
| P4 | diacronía: trayectoria de las siete indiscutidas por fecha | «con siete puntos no tiene potencia» (resultado nulo publicado) | no reconstruido (resultado nulo declarado en el libro) |
| P5 | tasa de error por longitud: 13 autores seguros, 4.200 problemas, núcleo de 6 fragmentos de 2.000 palabras, prueba de 300-5.000 palabras; 13 lemas, Delta coseno, impostores | AUC por longitud; rechazo de auténticos; P(auténtico > Tito/1 Tim/Col) | `p5_calibracion_longitud.py` sobre los autores de control del corpus construido (campaña 01/03); tabla publicada en `results_publicados/investigacion_1/p5_calibracion_longitud.csv` |
| P6 | Delta coseno sobre 200 formas frecuentes y verificación por impostores; banco amplio preregistrado (100 iteraciones) y banco epistolar añadido después (200) | «3 Corintios queda entre las evaluadas» = adverso; se imprimen los dos bancos | `p6_p7_impostores_falsificacion.py` (min-max y coseno); tabla publicada en `p6_impostores.csv` |
| P7 | controles de falsificación: 3 Corintios frente al núcleo paulino; Ignacio (7 auténticas LOO) frente a la recensión larga (7 interpoladas, 6 espurias) | 3 Cor entre las evaluadas = adverso (se cumplió) | `p3_p7_p9_p11…` (13 lemas) y `p6_p7…` (impostores): Ignacio LOO 0,65-3,45 (publicado 0,75-2,97, máx. IgnRom en ambos); espurias 0,02-0,22 con coseno (publicado 0,005-0,205 y 0,515); 3 Cor requiere `data/local/3Cor.txt` |
| P8 | sintaxis sobre el treebank PROIEL (NT); distancia completa, sin el rasgo dominante y acotada | adverso si una discutida supera a todos los controles y a Filemón (Tito lo hizo) | `p8_sintaxis_proiel.py`: modificadores adjetivales ‰ núcleo 9-15, Tit 64, 1 Tim 48, 1 Pe 56, 2 Tim 32, Sant 30 (publicado 9-13, 64, 47, 45, 29, 28); Tito adversa por la regla ✓ |
| P9 | modelo Dirichlet-multinomial sobre 13 lemas con la dispersión intra-autor de los controles | LR por carta; rango de las auténticas de Ignacio como referencia | `p3_p7_p9_p11…`: Ef −8,4 (publicado −8,7), Heb −10,8 (−8,4), Col −5,4 (−6,4), 1 Tim −5,1 (−3,2), Tit −2,8 (−4,8), 2 Tes +2,8 (+4,9), Flm +3,0 (+7,0), Flp +0,6 (+0,4), 1 Pe −4,0 (−3,2); Ignacio de −4,9 a +5,9 (publicado −6,2 a +7,0) |
| P10 | primera atestación datable del léxico exclusivo en Diorisis; proporción ≤ 50 por carta y por bloque; Fisher | adverso: Pastorales 0,70 frente a 0,79 (p = 0,0064) | `p10_primera_atestacion.py` (requiere Diorisis.zip); resultado histórico y validación externa P10-R(sym-ext) en `results_publicados/investigacion_1/p10_*.csv`; los 117 testimonios validados a mano no son reconstruibles |
| P11 | afinidad lucana: distancia a Lucas-Hechos frente a la distancia al núcleo (13 lemas y morfología) | apoyo a la hipótesis del amanuense lucano si las Pastorales están más cerca de Lucas-Hechos que las indiscutidas | `p3_p7_p9_p11…`: Pastorales 1,8-3,0 veces más lejos de Lucas-Hechos que del núcleo (publicado 1,6-2,6); Mt y Mc caen junto a Lucas |
| P12 | censos histórico-filológicos (P12a-c) y validaciones posteriores (P12b onomástica; P12d-f léxico) | de juicio; declarados como no estadísticos | no reconstruibles desde el código; tablas publicadas en `results_publicados/investigacion_1/` |

Desviaciones publicadas respecto del protocolo original (diez; dos adoptadas tras ver el resultado): el
segundo banco de impostores de P6 y las dos variantes de la distancia sintáctica de P8; la condición de
falsación de P7 se cumplió en su forma adversa. El decimocuarto autor previsto en P5 (Dionisio de
Halicarnaso) no llegó a cargarse. Ninguna cifra procedente de una variante posterior se presenta como
preregistrada.

Ejecución: desde la raíz de `paulinum_lab`, con el corpus de prueba construido
(`python -m paulinum fetch --tier 1 && python -m paulinum build --config config/prueba_reducida.yaml`)
y, para P8, `python -m paulinum fetch --editions`.

Nota sobre el lexicón: los guiones que lematizan textos sin anotación (Padres Apostólicos, recensión larga
de Ignacio) usan `data/cache/lexicon_uniforme.tsv`; si no existe, lo construyen con MorphGNT y, si está
descargado, PROIEL (`--sin-diorisis`). Las cifras de P7 y P9 para esos textos dependen de con qué fuentes
se construyó el lexicón (los resultados versionados en `results/` se obtuvieron con MorphGNT + PROIEL).

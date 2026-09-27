# Especificación reconstruida: qué fija el libro y qué ha decidido la reconstrucción

Este documento enumera, módulo a módulo, lo que el Apéndice técnico (A.1-A.6), los capítulos 7-9 y los
dos informes íntegros (Anexos I y II) fijan de manera explícita, y lo que la reconstrucción ha tenido que
decidir por su cuenta. Todo lo de la segunda columna está marcado en el código con `reconstruido=True`
o con un comentario «RECONSTRUCCIÓN».

## 1. Corpus y manifiesto (`paulinum/sources.py`)

| fijado por el libro | decidido en la reconstrucción |
|---|---|
| Fuentes y ediciones (A.2, § 8.1): MorphGNT/SBLGNT 6.12, Open Apostolic Fathers (Lake), PROIEL (Tischendorf), MACULA (Nestle 1904), Perseus canonical-greekLit, First1KGreek, Diorisis (solo lexicón), P. Bodmer X (Testuz) | Rutas concretas de cada archivo en los repositorios (comprobadas el 25-IX-2026 con los listados de los dos repositorios) |
| Composición por autor, tradición y estado, con número de documentos y de palabras (tabla de A.2) | Qué obras concretas cuando el libro no las nombra: los 5 opúsculos de Luciano (Nigrino, Demonacte, Timón, Hermótimo, De morte Peregrini), los 6 discursos de Aristides (himnos 43, 45, 41; discursos 26, 24, 48), los 5 discursos de Isócrates (Panegírico, A Nicocles, Nicocles, Evágoras, Areopagítico), los 7 opúsculos de Plutarco (De curiositate y Conjugalia praecepta —nombrados— más De garrulitate, De tranquillitate, De cohibenda ira, De superstitione, De virtute morali), las 3 obras de Filón de la campaña 01 (De opificio, Legatio, In Flaccum), el documento de Filóstrato (Cartas y dialexeis, 7.595 palabras en el inventario), la recensión de las Vidas de los profetas |
| Estados auditados con su fuente (§ 8.2): Juliano/Ps-Juliano por el índice de Wright; Isócrates genuino (Van Hook); De liberis educandis y De fato espurios, Consolatio ad Apollonium disputado; Ignacio recensión media genuina y larga espuria/interpolada; 2 Clem espuria; Bernabé anónima; Ps-Clementinas espurias; Lucas-Hechos un autor; 1 Jn, De resurrectione y De aeternitate disputados | Numeración de las 13 cartas de la recensión larga de Ignacio según el archivo de First1KGreek (13, 1, 4, 5, 9, 10 espurias; 2, 3, 6, 7, 8, 11, 12 interpoladas), verificada con los títulos del archivo y coherente con «IgnLong#9» (Antioquenos) y «#10» (Herón) del libro |
| Tope de 120 pares por autor en la envolvente; solo genuine; duplicados solo para ruido de edición | Umbral de extensión de las cartas de las colecciones (200 palabras; 300 para el prefacio de Epicteto) y regla «44 primeras cartas de Libanio que superan el umbral» |
| Grupos de obra: los libros de una misma obra no se comparan entre sí como obras distintas (`work_group`) | Aplicado a Josefo (AJ, BJ, C. Ap.), Arriano (Anábasis), Epicteto (Disertaciones), Marco Aurelio, Filón (Leg. all., Somn., Mos., Spec.), Teófilo, Clemente (Pedagogo), Orígenes (Contra Celso), Vetio Valente, Justino (Diálogo) |
| Diálogo con Trifón en 40 «capítulos» | Agrupación de capítulos consecutivos hasta ≥ 400 palabras, tope 40 |

## 2. Normalización y máscaras (`paulinum/text.py`, `paulinum/corpus.py`, `metadata/`)

| fijado | decidido |
|---|---|
| Sigma final, acento grave→agudo, filtro de letras griegas, variante sin diacríticos, conversión de Beta Code (A.1) | Tratamiento de la elisión (se conserva una marca «’» uniforme); NFC |
| Máscaras «declaradas por referencia» de fórmulas epistolares, material preformado y citas del AT (§ 8.3); extensiones enmascarables: Ef 35 %, Col 42 %, 2 Tes 820→542, 1 Tim 1.591→1.419, 2 Tim 1.235→1.048, Tit 659→452; tramos nombrados en las fichas del capítulo 10 | Tramos concretos de `metadata/masks.csv` para las 13 cartas (reconstruidos con las fichas y las extensiones publicadas: 2 Tes 278 y Tit 207 tokens enmascarados coinciden exactamente; Ef 35,5 %, Col 42,4 %, 1 Tim 180, 2 Tim 176) |
| Pasajes paralelos: tabla completa de `metadata/reuse_ranges.csv` (A.2) | Ninguna: se usa la tabla publicada |
| Variables de situación de las cartas: destinatario, cautividad, polémica (4 niveles), co-remitentes (3), registro litúrgico (4), orden eclesial, grupo (§ 9.7, tabla PERMANOVA con k por variable) | Valores concretos de `metadata/letter_variables.csv` (fichas del capítulo 10) |

## 3. Rasgos y distancias (`features.py`, `distances.py`)

| fijado | decidido |
|---|---|
| mfw:300, closed:150, char3:600, lemma:N (anotación), lemma_dict:300 (diccionario uniforme: forma sin diacríticos → lema más frecuente; desconocida → forma), char4:1000, mfw:100/500 | Definición operativa de «clase cerrada»: formas que en MorphGNT llevan categoría RA, C, P, RP, RD, RR, RI o X en ≥ 90 % de sus apariciones; vocabulario fijado por frecuencia total en el corpus de la especificación; n-gramas de caracteres con marca de límite «_» |
| Exclusión de las formas de 1.ª y 2.ª persona | Lista cerrada de pronombres y posesivos + formas verbales etiquetadas en 1.ª/2.ª persona en el NT, aplicadas por igual a todos los documentos (una forma excluida sigue contando como «palabra» de la ventana) |
| Delta de Burrows, min-max (Ruzicka), coseno, Eder, Manhattan, euclídea, Labbé | Delta y coseno sobre z-scores estandarizados con media y desviación típica de los documentos completos de referencia |

## 4. Verificación (`verify.py`)

| fijado | decidido |
|---|---|
| Impostores generales: 50 % de rasgos, 30 impostores, ventana aleatoria de 500 palabras (o documento entero), 100/300 iteraciones; acierto si el candidato más cercano supera al impostor más cercano | Banco de impostores: todos los documentos salvo el propio autor, los candidatos, los excluidos del problema, los disputed, los duplicados y los del mismo grupo de obra |
| Problemas de respuesta conocida: core_loo (7), pos_pairs (60 en c01; 60+72 en c03), neg_pairs (150; 351), pseudo_pairs (12), neg_target (97; 367), target (6); carta hermana excluida (SISTERS) e informada aparte | Regla de muestreo de pos_pairs (hasta N obras por autor, repartidas) y de neg_pairs (pares de autores sorteados con semilla); el número exacto depende del corpus construido |
| AUC, c@1, banda de indecisión, FPR/FNR a 0,5, LR por densidades (KDE) de los controles de la misma especificación, escala verbal ENFSI | Banda de indecisión simétrica en torno a 0,5 que maximiza c@1 (paso 0,025, semianchura ≤ 0,25); KDE gaussiana con reflexión en 0 y 1 y suelo de densidad 10⁻³ |

## 5. Variables, mismo rasero, rolling (`variables.py`, `rolling.py`)

| fijado | decidido |
|---|---|
| PERMANOVA (Anderson) con 499 permutaciones en Pablo y 299 en cada control; ventanas de 400; dbRDA | Ventanas contiguas sin solapamiento; matriz Delta sobre mfw:200 (el informe de la campaña 03 lo dice para los controles; se aplica igual a Pablo) |
| Envolvente: pares de obras distintas de un mismo autor genuine, ventanas de 500, 20 sorteos, tope 120 pares/autor; percentil de la distancia media de la carta al núcleo | Distancia media al núcleo sin la propia carta ni su hermana |
| Rolling: 400 palabras, paso 100, 60 iteraciones | Referencias inicial y final de cada ventana tomadas de la secuencia enmascarada |
| Bootstrap: 2.000 remuestreos de autores, 100 réplicas de ventanas, leave-one-author-out; «indeterminado» si el IC cruza 90 | Semillas |
| Segundo modelo: SVM lineal con calibración sigmoide y regresión logística; ventanas de 500; topes 20/documento y 120/autor; z-scores solo en entrenamiento; class_weight equilibrado; GroupKFold 10 por autor; LOO por carta | Percentil entre negativos calculado sobre las ventanas negativas en validación cruzada |

## 6. Sello (`cli.py seal`)

| fijado | decidido |
|---|---|
| El sello de la campaña 01 cubre los quince módulos, los cuatro archivos de metadata/ y config/default.yaml; el de la 03 añade scripts/*.py, reuse_ranges.csv, control_variables.csv y el lexicón | Procedimiento concreto: SHA-256 de la concatenación ordenada de «ruta\n + SHA-256 del archivo» (el procedimiento original no consta); por eso, y porque el código es distinto, **los sellos no coinciden con los publicados** |

## 7. Lo que la reconstrucción añade

- `config/prueba_reducida.yaml` y `results/prueba_reducida/`: una ejecución completa de prueba con NT + Padres Apostólicos.
- `scripts/detectar_reutilizacion.py --comparar`: cotejo automático con la tabla publicada de pasajes paralelos.
- `investigacion_1/capa_13_lemas/cotejo_con_el_libro.py`: cotejo automático de 313 valores con el libro.
- `results_publicados/`: todas las tablas publicadas en CSV, con nota de origen en la primera línea.
- Este documento y `LEEME_PRIMERO.md`.

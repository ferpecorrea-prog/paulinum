# Protocolo preregistrado de paulinum 1.0

Verificación convergente de la autoría de las catorce cartas de la tradición paulina
(Romanos, 1-2 Corintios, Gálatas, Efesios, Filipenses, Colosenses, 1-2 Tesalonicenses, 1-2 Timoteo, Tito, Filemón y Hebreos)

| | |
|---|---|
| Versión del protocolo | 1.0.0 |
| Fecha de cierre del texto | 27 de septiembre de 2026 |
| Autor | Jesús Fernández-Pedrera Correa (ORCID 0009-0000-7024-5028) |
| Repositorio | https://github.com/ferpecorrea-prog/paulinum |
| Sello | `protocols/paulinum_1_0/SELLO.json` (SHA-256 del conjunto: este documento, `config/paulinum_1_0.yaml`, `paulinum/*.py`, `scripts/*.py`, `metadata/*.csv`) |
| Registro público | `protocols/paulinum_1_0/REGISTRO.md` (etiqueta `protocolo-1.0.0`, *release* de GitHub archivada en Zenodo con DOI; registro en OSF cuando se haga) |
| Estado | sellado antes de ejecutar cualquier análisis sobre las dianas |

Este protocolo fija, antes de ejecutar nada, las hipótesis, el corpus, los estados de los textos, la preparación, la rejilla de especificaciones, las familias de métodos, los problemas de calibración, las reglas de decisión, las condiciones de falsación y el orden de ejecución de la investigación estilométrica, y el protocolo de codificación de los tres canales no estilométricos con los que converge. Lo que aquí no está previsto no se hace dentro de la campaña; si hay que hacerlo, se anota antes como enmienda (§ 12) y el libro lo dice.

---

## 1. Objeto y alcance

**Pregunta.** Para cada una de las catorce cartas, ¿es compatible su forma lingüística con la de las cartas indiscutidas de Pablo en la medida en que lo son entre sí las obras de un mismo autor antiguo, y, si no lo es, de qué tamaño y de qué clase es la diferencia?

**Lo que se hace.** Verificación de autoría (¿es de este autor, sí o no, y con qué fuerza lo dice la prueba?), no atribución (¿de quién es?). No se propone ningún autor alternativo concreto para ninguna carta, y ningún resultado se convierte en nombre.

**Lo que no se hace.** No se ajustan parámetros a la vista de los resultados de las dianas; no se eligen las especificaciones que «salen mejor»; no se multiplican razones de verosimilitud de canales distintos como si fueran independientes; no se sustituye ningún resultado adverso por otro más favorable; no se asigna ningún «grado» de autenticidad.

**Punto de partida declarado.** La hipótesis de trabajo del autor, expresada antes de esta investigación, es que el corpus de trece cartas procede de Pablo al menos intelectualmente (H1-H3 de § 2.1). Hebreos entra sin ninguna hipótesis previa (§ 2.4). Que la hipótesis de partida sea esta obliga a fijar con más cuidado, no con menos, las condiciones en las que se daría por refutada (§ 10).

**Relación con la investigación anterior.** El código de paulinum 1.0 desciende de la reconstrucción 0.2.0-r del laboratorio de las campañas 01-03 (D-001). Ninguna cifra de aquellas campañas se reutiliza como resultado: todo se vuelve a calcular con el corpus, las reglas y las semillas de este protocolo.

## 2. Hipótesis

### 2.1 Hipótesis de autoría, por carta

Para cada carta *L* se consideran cinco hipótesis mutuamente excluyentes sobre su composición:

- **H1. Autógrafa o dictada.** Pablo compuso el texto, de su mano o dictándolo a un escriba que transcribe (el caso de Tercio en Rom 16, 22).
- **H2. Composición mediada.** Pablo es el autor intelectual y el responsable del contenido, pero un secretario con libertad redaccional dio forma al texto, en vida de Pablo y bajo su control.
- **H3. Colaboración del círculo.** Un colaborador nombrado en la carta o conocido por las demás (Timoteo, Silvano, Sóstenes, Lucas, Tíquico…) compuso el texto en vida de Pablo y con su participación, con una parte de la forma y del contenido que no es de Pablo.
- **H4. Escuela póstuma.** Un discípulo compuso la carta después de la muerte de Pablo, en su nombre y dentro de su tradición, con o sin materiales suyos.
- **H5. Composición ajena al círculo.** La carta fue compuesta fuera del círculo paulino, en otro tiempo o lugar, por alguien que no perteneció a él (falsificación externa, o texto anónimo incorporado después a la colección).

Para las siete cartas indiscutidas la hipótesis consensuada es H1/H2; se someten al mismo procedimiento que las siete dianas (§ 3.1) porque el procedimiento se juzga por lo que dice de ellas.

### 2.2 Predicciones observables por canal

Ningún canal separa por sí solo las cinco hipótesis. La tabla fija, antes de mirar nada, qué patrón predice cada hipótesis en cada canal; el capítulo de convergencia del libro se atendrá a ella (§ 9.4).

| canal | H1 | H2 | H3 | H4 | H5 |
|---|---|---|---|---|---|
| Estilometría (nivel 1-2, § 8) | dentro del rango intra-autor en la mayoría de familias y rasgos | dentro del rango en léxico (mfw, lemma) y borde o fuera en morfología/caracteres (closed, char3): la «firma de secretario» | como H2, con posible desplazamiento léxico de tamaño intermedio | fuera del rango en la mayoría de familias; distancia del tamaño de un cambio de autor, no de género | fuera del rango en todas las familias; distancia inter-autor |
| Estilometría (variables, § 7.5) | la diferencia se explica por destinatario/registro (R² situacional dentro del rango de los controles) | como H1 | como H1 | la diferencia no se explica por variables de situación | como H4 |
| Recepción y transmisión (§ 9.1) | atestación temprana, simétrica y con atribución estable | como H1 | como H1 | atestación tardía o desigual; entrada tardía en las colecciones | atestación tardía, asimétrica, atribución vacilante o ausente |
| Onomástica y prosopografía (§ 9.2) | nombres coherentes con Hechos y con la documentación de la región y el periodo; proporción normal de nombres no famosos | como H1 | como H1 | nombres tomados de las cartas seguras o de Hechos; pocos nombres nuevos verificables | nombres literarios, anacrónicos o incoherentes; o ausencia de prosopografía |
| Institucional (§ 9.3) | vocabulario de organización compatible con las asociaciones del s. I | como H1 | como H1 | vocabulario compatible con finales del s. I-inicios del II | vocabulario del s. II o posterior |

### 2.3 Hipótesis sobre el método (se contrastan antes de leer las dianas)

- **Hm1.** El procedimiento detecta las pseudoepigrafías conocidas del corpus (Ps-Ignacio, Ps-Clemente, Ps-Plutarco, Ps-Juliano, Ps-Basilio, 3 Corintios) con AUC ≥ 0,80 en los problemas epistolares de respuesta conocida (§ 7.2). Si no, la familia de métodos correspondiente no es apta (§ 10.1).
- **Hm2.** La distancia entre obras de un mismo autor antiguo de géneros distintos (carta frente a discurso) es sistemáticamente menor que la distancia entre autores distintos del mismo género. Si no, la estilometría no puede separar género de autor en este corpus y el nivel 2 (§ 8.2) se declara no concluyente para Hebreos.
- **Hm3.** El texto de un autor editado por otro (Epicteto por Arriano; Plotino por Porfirio) se reconoce como del autor, no del editor. Si no, H2 no puede distinguirse de H4 por estilometría y se dirá.

### 2.4 Hebreos

Hebreos entra como diana número catorce con exactamente el mismo procedimiento que las otras seis (D-002): mismo núcleo de referencia, mismas máscaras, mismas familias, mismas reglas. No se parte de ninguna hipótesis sobre su autoría. Dos hechos suyos se tratan como datos, no como premisas: (a) carece de prescripto y de nombre de remitente, lo que es un dato del canal de recepción (§ 9.1), no un argumento estilométrico; (b) su género declarado (λόγος τῆς παρακλήσεως, 13, 22) difiere del de las cartas, lo que obliga a leer su distancia frente a la distribución de saltos de género dentro de un mismo autor (§ 7.4) antes de interpretarla como distancia de autor.

## 3. Diseño general

### 3.1 Unidades, núcleo y dianas: el mismo rasero

- Unidad de análisis: la carta entera (con máscaras o sin ellas). Las ventanas de 500 palabras son unidades de muestreo, no de decisión.
- Núcleo de referencia principal: las siete cartas indiscutidas (Rom, 1 Cor, 2 Cor, Gal, Flp, 1 Tes, Flm).
- Dianas: Ef, Col, 2 Tes, 1 Tim, 2 Tim, Tit, Heb. Cada una se compara con el núcleo entero (excluida la carta hermana: Col para Ef, 1 Tes para 2 Tes).
- Mismo rasero: cada carta del núcleo se compara con las otras seis por el mismo procedimiento (leave-one-out). Los umbrales, las envolventes y las escalas verbales son idénticos para las catorce. Ninguna regla se enuncia para una carta en particular.
- Núcleos de sensibilidad (§ 6.3): Hauptbriefe (4), siete más Col y 2 Tes (9), y las trece cartas con nombre de Pablo (13), este último solo para el leave-one-out de las trece y para Hebreos frente a la colección entera.

### 3.2 Cuatro niveles de lectura

Cada carta se lee en cuatro niveles, cada uno con su regla (§ 8): **posibilidad** (¿es compatible con el núcleo según la razón de verosimilitud calibrada?), **plausibilidad** (¿queda dentro del rango en que varían entre sí las obras de un mismo autor antiguo, y dentro del rango de los saltos de género intra-autor?), **superioridad comparativa** (¿es el núcleo paulino, entre todos los autores del corpus, el más próximo, y con qué margen?) y **robustez** (¿sobrevive el resultado a los cambios de edición, máscara, ventana, rasgos, núcleo y modelo?).

### 3.3 Orden de ejecución y registro

1. Sello 1 (este protocolo, el manifiesto del corpus, los metadatos y el código de partida): etiqueta `protocolo-1.0.0`, *release* archivada en Zenodo.
2. Implementación de lo que falta (familias NCD y Dirichlet-multinomial, edición NA28, testigos, anotación uniforme, veredicto mecánico), probada **solo** con los problemas de respuesta conocida y con los controles: ninguna orden que produzca filas de diana se ejecuta en esta fase.
3. Sello 2 (código congelado): etiqueta `paulinum-1.0.0`, *release* archivada en Zenodo. A partir de aquí el código no cambia salvo por enmienda registrada.
4. Ejecución por etapas reanudables; las etapas de calibración y envolvente se cierran y se publican (commit) **antes** de que se calcule ninguna fila de diana. El historial de git es el registro del orden.
5. Veredicto mecánico (`scripts/veredicto.py`, sellado en 3) y Sello 3 (resultados): etiqueta `resultados-1.0.0`, archivada en Zenodo. El libro cita los tres DOI.

No hay lectura ciega en sentido estricto: las extensiones de las cartas las identifican a quien conoce el corpus, y el investigador conoce el corpus. Por eso la protección no se confía al ocultamiento sino a tres cosas verificables: las reglas están escritas antes, el veredicto lo calcula un guion sellado, y el orden de las etapas queda en el historial público.

### 3.4 Semillas y determinismo

Semilla principal 20260927. Cada etapa deriva sus generadores de la semilla principal y del nombre de la etapa; con las versiones fijadas en `requirements.txt`, dos máquinas producen resultados idénticos. Las ejecuciones pesadas se hacen en la réplica en la nube (2 núcleos, 7 GB) y las pruebas de referencia en el portátil (2 núcleos, 3 GB); ambas se anotan en el registro.

## 4. Corpus

### 4.1 Estratos

| estrato | contenido | fuente | origen |
|---|---|---|---|
| 1 | 27 libros del NT; 15 escritos de los Padres Apostólicos; 3 Corintios | MorphGNT/SBLGNT; Open Apostolic Fathers (Lake); P. Bodmer X (Testuz 1959), preparado en `data/local/` (D-006, D-007) | campañas 01-03 |
| 2 | controles de la campaña 01: Josefo, Filón (3 obras), Juliano (cartas, con las apócrifas separadas), Isócrates (cartas y 5 discursos), Plutarco (7 opúsculos, 2 espurios, 1 disputado), Luciano (5), Arriano, Epicteto/Arriano, Marco Aurelio, Filóstrato, Ps-Ignacio (recensión larga), Ps-Clementinas, duplicados de edición | Perseus canonical-greekLit; First1KGreek | campaña 01 |
| 3 | ampliación de la campaña 03: Filón (resto), apologistas (Justino, Taciano, Atenágoras, Teófilo), Clemente de Alejandría, Orígenes, Hechos de Tomás, Pasión de Perpetua, pseudepígrafos judíos, Vetio Valente, Hermetica, Polemón, Elio Aristides, Ps-Diógenes, Ps-Eurípides, Ps-Solón, cartas de Demóstenes y de Platón (disputadas) | ídem | campaña 03 |
| 4 | **ampliación de paulinum 1.0** (§ 4.2) | Perseus; First1KGreek | este protocolo |

Todo el estrato 4 se fijó en `paulinum/sources.py` (`CONTROLS_10`) antes del sello, y se comprobó que cada archivo se descarga y se analiza (registro de la sesión 1). Regla: un documento que no se analiza o no alcanza el umbral se pierde y se anota en el inventario; **nunca se añade nada** después del sello.

### 4.2 Ampliación de paulinum 1.0 (estrato 4)

| grupo | documentos | para qué |
|---|---|---|
| Basilio de Cesarea, *Cartas* (368; 201 de ≥ 200 palabras, ~115.000 palabras) y *A los jóvenes* | envolvente **epistolar cristiana** de autor seguro, con cartas a individuos y a iglesias; control de género dentro del autor | plausibilidad (§ 7.3), género (§ 7.4), negativos epistolares cristianos (§ 7.2) |
| Libanio, *Cartas* (839; 170 de ≥ 200 palabras, ~50.000 palabras; sustituye a las 44 de la campaña 03) y seis discursos (1, 2, 11, 30, 47, 64) | envolvente epistolar pagana de cartas breves; control de género dentro del autor | ídem |
| Juliano: discursos 1, 2, 3, 4, 7, 9, *Misopogon*; *Carta a los atenienses* (pública, a una comunidad) y *Carta a Temistio* | control de género dentro del autor; par carta pública / carta privada | § 7.4 |
| Alcifrón (4 libros; sustituye al documento único) y Eliano (*Cartas rústicas*; *Varia historia*, 14 libros) | cartas ficticias de autor seguro: control de género epistolar no auténtico; género dentro del autor | § 7.2, § 7.4 |
| Plotino (*Enéadas*, 6 documentos, texto editado por Porfirio) y Porfirio (*Vida de Pitágoras*, *De abstinentia*, *Carta a Marcela*) | segundo caso de composición mediada, con Epicteto/Arriano | Hm3, § 7.4 |
| Ps-Clemente, *Cartas sobre la virginidad* | pseudoepigrafía epistolar cristiana | § 7.2 |
| Hercher, *Epistolographi Graeci*: Fálaris, Quión, Bruto, Sócrates, socráticos, Crates, Anacarsis, Temístocles, Antígono, Antíoco, Artajerjes, Mitrídates, Nicias (cartas consecutivas agrupadas hasta ≥ 400 palabras) | falsificaciones epistolares antiguas reconocidas; el autor imitado no se conserva: solo negativos e impostores | § 7.2 |

### 4.3 Estados y auditoría

Estados: `core` (núcleo), `target` (diana), `genuine` (autoría segura), `spurious` (pseudoepigrafía reconocida), `disputed` (atribución debatida: fuera de la calibración), `other` (anónimo o no verificable: solo impostor y negativo), `duplicate` (misma obra en otra edición: solo ruido de edición), `mixed` (texto genuino interpolado: solo impostor). Cada estado y su fuente constan en `metadata/status_audit.csv`.

Regla conservadora de auditoría: cuando la bibliografía de referencia expresa **cualquier** reserva sobre una obra o una carta, esta queda fuera de la calibración (`disputed`), aunque la opinión mayoritaria la tenga por auténtica. Excluir de más no sesga la calibración; incluir de más sí. Aplicaciones fijadas antes del sello: cartas de Basilio (espurias: 8, 16, 38, 39-41, 47, 189, 360, 365-368; dudosas o debatidas: 42-46, 50, 81, 115, 166-167, 169-171, 197, 321, 335-359, 361-364; el resto, genuinas); cartas de Juliano (74-83 apócrifas; 82 de Galo); Isócrates (cartas 3, 4, 9 genuinas según Van Hook); Plutarco, Atenágoras, Filón, 1 Juan, Ignacio y Clemente como en la campaña 03. Hebreos deja de ser `other` y pasa a `target` (D-002): no vuelve a usarse ni como impostor ni como negativo.

### 4.4 Reglas de inclusión y de división

- Umbral de extensión de las partes de una colección: 200 palabras griegas (300 para el prefacio de Epicteto). Los documentos de menos de 100 palabras no entran en ningún problema.
- Colecciones pseudoepigráficas de cartas breves (Hercher): cartas consecutivas agrupadas hasta ≥ 400 palabras; la unidad es la colección (un solo autor falso), no la carta.
- Grupos de obra (`work_group`): los libros de una misma obra no forman pares positivos entre sí (Josefo, Arriano, Epicteto, Marco Aurelio, Filón, Teófilo, Clemente, Orígenes, Vetio Valente, Justino, Eliano, Plotino, Porfirio).
- Sustituciones: en el estrato 4, `Liban_Ep` (44 cartas) y `Alciphr` (un documento) se reemplazan por `Liban_Ep10` (todas las cartas de ≥ 200 palabras) y `Alciphr10` (por libros); nunca coexisten.
- Todo texto se toma de la edición declarada en el encabezamiento TEI de su archivo y en `paulinum/sources.py`; las huellas SHA-256 de los archivos descargados quedan en `data/provenance.json`.

### 4.5 Licencias y redistribución

Los textos de terceros no se redistribuyen: el repositorio contiene el manifiesto, las huellas y el código para descargarlos. El lexicón derivado de Diorisis (CC BY-NC-SA) tampoco se redistribuye; se publica su huella. NA28, 𝔓46 y el Sinaítico se usan solo en local (D-004, § 5.4) y de ellos se publican únicamente agregados.

## 5. Preparación de los textos

### 5.1 Normalización

Como en las campañas 01-03 (`paulinum/text.py`): Unicode NFC; sigma final unificada; acento grave → agudo; filtro de letras griegas; variante sin diacríticos; conversión de Beta Code; marca uniforme de elisión. Exclusión de las formas de 1.ª y 2.ª persona (pronombres, posesivos y formas verbales), aplicada por igual a todos los documentos; una forma excluida sigue contando como palabra de la ventana.

### 5.2 Máscaras

Cuatro máscaras por referencia, declaradas en `metadata/masks.csv` y `metadata/reuse_ranges.csv`, aplicadas por versículos completos:

- `formulae`: prescripto, acción de gracias o bendición inicial y cierre epistolar;
- `preformed`: himnos, fórmulas de fe, códigos domésticos, «dichos fieles», doxologías y material apocalíptico tradicional, **solo cuando su carácter preformado es de consenso**; los pasajes debatidos (Heb 1, 3; Col 1, 15-20 sí, por consenso) se tratan según la misma regla en las catorce cartas;
- `otq`: citas explícitas del Antiguo Testamento según la lista de NA28 (*Loci citati vel allegati*, entradas en cursiva = citas), por versículos completos;
- `reuse`: tramos paralelos entre cartas hermanas (Ef/Col, 1 Tes/2 Tes), por posiciones de palabra.

Hebreos recibe las tres primeras por la misma regla: cierre epistolar 13, 18-25; sin prescripto; 28 tramos de cita (Heb 1, 5-13; 2, 6-8. 12-13; 3, 7-11. 15; 4, 3-5. 7; 5, 5-6; 6, 14; 7, 17. 21; 8, 5. 8-12; 9, 20; 10, 5-7. 16-17. 30. 37-38; 11, 18; 12, 5-6. 20-21. 26; 13, 5-6), que enmascaran el 18,6 % de sus 4.935 palabras (21,1 % con el cierre; Romanos: 23,2 %). El autor coteja la lista con el apéndice de su ejemplar de NA28 antes del segundo sello; una corrección de tramos es una enmienda de metadatos (§ 12) y no cambia nada más.

La rejilla principal ejecuta cada especificación **sin máscara** y **con las cuatro** (`formulae+preformed+otq+reuse`). Si el signo de la razón de verosimilitud de una carta cambia entre ambas, se informa como dependencia del material enmascarado y se dice de cuál (se recalcula con cada máscara por separado, solo para explicar, no para decidir).

### 5.3 Anotación uniforme

- Lemas: diccionario uniforme forma → lema más frecuente, construido con MorphGNT, PROIEL y Diorisis (`scripts/construir_lexicon.py`), aplicado **a todos los documentos por igual**; forma desconocida → forma sin diacríticos; cobertura por documento informada. Es el único lematizador de la rejilla principal.
- Morfosintaxis: se ensaya un analizador uniforme (greCy/OdyCy o dilemma, según lo que se pueda instalar sin salir de los dominios accesibles) sobre las 27 obras del NT y se mide su acuerdo con la anotación manual de MorphGNT. Umbral fijado ahora: exactitud de lema ≥ 0,95 y de categoría gramatical ≥ 0,95 en el NT. Si se alcanza, el espacio `pos3:200` (trigramas de categoría gramatical) entra **solo** en la sensibilidad (§ 6.2); si no, la capa se descarta y se informa el acuerdo obtenido. En ningún caso se usa la anotación manual de MorphGNT como rasgo, porque solo el NT la tiene.

### 5.4 Ediciones y testigos manuscritos

- Edición principal: SBLGNT (MorphGNT 6.12). Ediciones de sensibilidad: Tischendorf (PROIEL) y Nestle 1904 (MACULA), como en la campaña 02b.
- NA28 (ejemplar del autor, uso local, D-004): se extrae el texto de las catorce cartas y se ejecuta la rejilla principal con él; se publican solo los agregados y el guion de extracción. Si la extracción resulta ruidosa (acuerdo de tokens con SBLGNT < 0,98 en cualquier carta), se descarta y se dice.
- Testigos: 𝔓46 (transcripción INTF/NTVMR) y el Sinaítico (transcripción XML del proyecto Codex Sinaiticus, CC BY-NC-SA) entran como «ediciones» de sensibilidad si el autor deposita las transcripciones en `nuevo_paulinum/` antes del segundo sello; se normalizan con el mismo guion (nomina sacra expandidos, ortografía regularizada por la misma tabla que 3 Corintios, lagunas como ausencia de texto) y se usan solo en local. Con 𝔓46 se mide, además, si la ausencia de las Pastorales y la posición de Hebreos en el códice cambian algo: no cambian nada estilométricamente, y se dirá; el dato es del canal de transmisión (§ 9.1).
- Ruido de edición: para cada carta, la distancia entre sus ediciones se compara con la distancia entre cartas distintas del núcleo; una diferencia entre cartas no se interpreta si es del tamaño del ruido de edición.

## 6. Rasgos, distancias, núcleos y familias de métodos

### 6.1 Rejilla principal (16 especificaciones)

4 rasgos (`mfw:300`, `closed:150`, `char3:600`, `lemma_dict:300`) × 2 distancias (min-max de Ruzicka, Delta de Burrows) × 1 ventana (500 palabras) × 2 máscaras (ninguna; las cuatro) × diacríticos conservados × núcleo `seven` × SBLGNT; 300 iteraciones por problema. Definiciones operativas como en la reconstrucción (`docs/ESPECIFICACION_RECONSTRUIDA.md` § 3): clase cerrada = formas con categoría RA, C, P, RP, RD, RR, RI o X en ≥ 90 % de sus apariciones en MorphGNT; vocabulario fijado por frecuencia total en el corpus; n-gramas de caracteres con marca de límite; Delta y coseno sobre z-scores estandarizados con media y desviación típica de los documentos completos de referencia.

### 6.2 Sensibilidad (cada bloque es una campaña aparte, con el mismo sello; solo se informa)

Núcleos `hauptbriefe`, `seven_plus`, `trece`; ediciones Tischendorf, Nestle 1904, NA28, y testigos si se depositan; ventanas de 300 palabras y documento entero; rasgos `mfw:100`, `mfw:500`, `char4:1000`, `pos3:200` (condicional, § 5.3); distancia coseno; sin diacríticos. Ningún bloque de sensibilidad sustituye a la rejilla principal; si contradice a la principal, se informa la contradicción.

### 6.3 Núcleos

`seven` (principal); `hauptbriefe` y `seven_plus` (sensibilidad, como en la campaña 02a); `trece` (sensibilidad): leave-one-out de cada una de las trece cartas con nombre de Pablo frente a las otras doce, y Hebreos frente a las trece. El núcleo `trece` responde a otra pregunta («¿es Hebreos como la colección?») y así se presenta; no se promedia con `seven`.

### 6.4 Tres familias de métodos

Las tres familias producen, para cada problema (diana o de respuesta conocida) y cada especificación, una puntuación en [0, 1] = fracción de iteraciones en las que el candidato supera al impostor más próximo; las tres se calibran con los mismos problemas de respuesta conocida (§ 7) y con la misma razón de verosimilitud (§ 7.2). Así son comparables y así se informa su concordancia.

**A. Impostores generales** (familia de referencia; Koppel y Winter 2014; Kestemont *et al.* 2016). En cada iteración: 50 % de los rasgos al azar, 30 impostores al azar del banco (todos los documentos salvo los del propio autor, los candidatos, los excluidos del problema, los `disputed`, los `duplicate` y los del mismo grupo de obra), una ventana aleatoria de 500 palabras por documento (o el documento entero si es más corto); acierto si el candidato más cercano supera al impostor más cercano.

**B. Distancia de compresión normalizada** (Cilibrasi y Vitányi 2005; Benedetto *et al.* 2002). NCD(x, y) = [C(xy) − mín(C(x), C(y))] / máx(C(x), C(y)), con C = longitud comprimida con LZMA (preset 6, un solo flujo) de la ventana como cadena de caracteres sin diacríticos, formas de 1.ª y 2.ª persona sustituidas por un marcador. No usa rasgos ni vocabulario fijado: es una familia independiente de la selección de rasgos, con la misma envoltura de impostores y ventanas que A (sin muestreo de rasgos).

**C. Modelo probabilístico jerárquico Dirichlet-multinomial.** Para cada espacio de rasgos (`mfw:300`, `closed:150`), el perfil de un autor *a* es un vector de probabilidades θ_a con prior Dirichlet(α·m), donde m es el perfil medio del corpus de referencia y α la concentración estimada por máxima verosimilitud marginal en la envolvente de autores seguros (hiperparámetro compartido: de ahí «jerárquico»). La verosimilitud predictiva de las cuentas de una ventana de la diana bajo el candidato es la Dirichlet-multinomial posterior con los documentos del candidato; se compara con la de cada impostor de la iteración. Cada iteración usa la misma ventana, el mismo banco y el mismo muestreo de impostores que A, y omite el muestreo de rasgos. Es la formalización probabilística de lo que A hace por distancias y de lo que la campaña 03 ensayó (`investigacion_1/segunda_campana/p9_dirichlet_multinomial.py`).

### 6.5 Segundo modelo

SVM lineal con calibración sigmoide y regresión logística sobre ventanas de 500 palabras (topes 20/documento y 120/autor; z-scores solo en entrenamiento; clases equilibradas; GroupKFold de diez pliegues por autor; leave-one-letter-out para el núcleo), como en la campaña 03. Se informa la concordancia con las tres familias; no se elige el modelo que dé «mejor» resultado.

## 7. Problemas de respuesta conocida, calibración y envolventes

### 7.1 Problemas

| tipo | construcción | etiqueta |
|---|---|---|
| `core_loo` | cada carta del núcleo frente a las otras seis (hermana excluida) | 1 |
| `target` | cada diana frente al núcleo (hermana excluida) | ? |
| `pos_pairs` | obra de un autor `genuine` frente a sus otras obras de grupo distinto (hasta 6 por autor, repartidas) | 1 |
| `neg_pairs` | obra de A frente a las obras de B (400 pares sorteados con semilla; B con ≥ 2 obras) | 0 |
| `pseudo_pairs` | cada pseudoepigrafía frente a las obras del autor imitado (Ps-Ignacio, Ps-Clemente, Ps-Plutarco, Ps-Juliano, Ps-Basilio, 3 Corintios) | 0 |
| `neg_target` | todo texto no paulino (`genuine`, `spurious`, `other`, `mixed`) frente al núcleo | 0 |
| **`genre_pairs`** (nuevo) | obra de un género de un autor frente a sus obras de otro género (Libanio, Juliano, Basilio, Isócrates, Eliano, Orígenes, Ignacio a Policarpo/iglesias, Porfirio) | 1 |
| **`mediated_pairs`** (nuevo) | Epicteto (ap. Arriano) frente a Arriano; Plotino (ed. Porfirio) frente a Porfirio; y viceversa | 0 |
| **`epist_pairs`** (nuevo) | los positivos y negativos de arriba restringidos a documentos de género `carta` de ambos lados | 1/0 |

Ni las dianas ni el núcleo entran nunca en el banco de impostores de ningún problema de respuesta conocida, y ningún texto de la tradición paulina (`Pablo`, `Pablo?`) es impostor de nadie.

### 7.2 Calibración y razón de verosimilitud

Por especificación y familia: AUC, c@1 con banda de indecisión simétrica en torno a 0,5 que maximiza c@1 (paso 0,025; semianchura ≤ 0,25), tasas de falsos positivos y negativos a 0,5. Razón de verosimilitud LR(s) = f₁(s)/f₀(s) por densidades KDE gaussianas (reflexión en 0 y 1; suelo 10⁻³) de las puntuaciones de los problemas positivos y negativos de la misma especificación y familia. Escala verbal (por |log10 LR|): < 0,3 no discriminante; 0,3-1 apoyo débil; 1-2 moderado; ≥ 2 fuerte; a favor de H_mismo-autor si LR > 1 y de H_otro-autor si LR < 1.

Tres conjuntos de calibración, en este orden de importancia: **epistolar** (principal: positivos y negativos de `epist_pairs`, más `pseudo_pairs` de cartas), **general** (todos) y **cristiana** (negativos de tradición cristiana). La epistolar es la principal porque las catorce dianas son cartas y sus alternativas realistas también lo son; las otras dos se informan al lado.

Regla de aptitud: una especificación con AUC epistolar < 0,80 no produce LR; una familia cuya mediana de AUC epistolar es < 0,80 se declara no apta y queda fuera del veredicto (Hm1).

### 7.3 Envolvente intra-autor e inter-autor (mismo rasero)

- **E, intra-autor:** distancias (min-max y Delta sobre `mfw:300`, ventanas de 500 palabras, 20 sorteos) entre pares de obras distintas de un mismo autor `genuine`, tope 120 pares por autor, con cartas y con obras de otros géneros por separado (E_carta y E_todo).
- **B, inter-autor:** distancias entre obras de autores distintos, emparejadas por género (carta frente a carta) y por tradición cuando sea posible; mismo tope.
- Para cada carta *L*: d(L) = distancia media de *L* al núcleo sin *L* ni su hermana; percentil de d(L) en E_carta (pct_E) y en B (pct_B), con IC 95 % por bootstrap de autores (2.000) y de ventanas (100), y leave-one-author-out (autor más influyente y percentil sin él).

Regla de equivalencia (esquema de dos pruebas unilaterales adaptado): *L* queda **dentro del rango intra-autor** si el IC 95 % de pct_E incluye un valor ≤ 90; queda **fuera** solo si el IC entero está por encima de 90 **y** el IC de pct_B está entero en ≥ 10 (la distancia cae en el cuerpo de la distribución inter-autor); en cualquier otro caso, **indeterminado**. «Indeterminado» es un resultado válido y se informa como tal.

### 7.4 Distribución de saltos de género (G) y composición mediada

- **G:** distancias entre una obra de un género y las obras de otro género del mismo autor (`genre_pairs`), con las mismas medidas y ventanas que E. Se informa su solapamiento con E y con B (Hm2).
- Lectura de Hebreos y de cualquier carta con d(L) fuera del rango intra-autor: si d(L) cae dentro del rango de G (percentil ≤ 90 en G, con IC), la diferencia es del tamaño de un cambio de género intra-autor y **no se interpreta como cambio de autor**; si cae fuera de G y dentro de B, se interpreta como del tamaño de un cambio de autor. Esta regla se aplica a las catorce cartas, no solo a Hebreos.
- Composición mediada (Hm3): puntuaciones de `mediated_pairs` por familia. Si en las tres familias el texto editado se reconoce como del autor y no del editor (puntuación < 0,5 frente al editor), se dice que el procedimiento no confunde autor con editor y que un secretario con libertad (H2) no debería, por sí solo, sacar una carta del rango; si no, se dice que H2 y H4 no se distinguen estilométricamente.

### 7.5 Variables de situación

PERMANOVA (Anderson 2001; 499 permutaciones) y dbRDA sobre ventanas contiguas de 400 palabras dentro del corpus paulino (catorce cartas; Delta sobre `mfw:200`) para destinatario, cautividad, nivel de polémica, co-remitentes, registro litúrgico, orden eclesial y grupo (`metadata/letter_variables.csv`, con Hebreos anotada); el R² de cada variable se lee frente a la distribución de los mismos R² dentro de cada autor de control (299 permutaciones; `scripts/variables_controles.py`), y no se interpreta como anómalo si cae dentro del rango de los controles. Para Basilio y Libanio, sin anotación por carta, las variables se leen solo a nivel de colección (destinatario individuo/comunidad cuando conste).

### 7.6 Ventanas deslizantes

Ventanas de 400 palabras con paso de 100 y 60 iteraciones (`mfw:300`, min-max) para localizar dentro de cada carta los tramos que se alejan del núcleo; se informan como descripción, nunca como veredicto, y se cotejan con las máscaras (si el tramo alejado coincide con material enmascarado, se dice).

## 8. Reglas de decisión por carta

El veredicto de cada carta lo calcula `scripts/veredicto.py` (sellado en el Sello 2) a partir de los archivos de resultados, con estas reglas y sin intervención manual. El libro reproduce la tabla que produce y la comenta; no la corrige.

### 8.1 Nivel 1, posibilidad

Por familia apta: mediana de log10 LR epistolar entre las especificaciones válidas (con Q1-Q3 y mín-máx) → escala verbal. Resultado del nivel: la escala verbal de la mediana de las familias aptas, y la concordancia (todas del mismo signo / discordantes). Con dos familias de signo contrario, el nivel se declara **discordante** y se informa cuál es cuál.

### 8.2 Nivel 2, plausibilidad

Regla de equivalencia de § 7.3 (dentro / fuera / indeterminado) para min-max y Delta; si difieren, prevalece «indeterminado». Si «fuera», regla de género de § 7.4 (del tamaño de un cambio de género / de un cambio de autor).

### 8.3 Nivel 3, superioridad comparativa

Para cada carta, orden de todos los autores del corpus con ≥ 2 obras por su distancia media a la carta (`mfw:300`, min-max y Delta, ventanas de 500, 20 sorteos): posición del núcleo paulino y margen sobre el segundo autor, con IC por bootstrap de ventanas. La carta pasa el nivel si el núcleo es el autor más próximo en las dos medidas y el IC del margen no incluye 0. Se informa siempre quién es el segundo, sin convertirlo en atribución.

### 8.4 Nivel 4, robustez

Se cuenta, sobre los bloques de sensibilidad (§ 6.2), el segundo modelo (§ 6.5) y las ediciones (§ 5.4), la proporción de configuraciones en las que se mantiene el resultado de los niveles 1 y 2; se informa la proporción y se nombran las configuraciones que lo cambian. No hay umbral: la robustez se describe.

### 8.5 Del resultado estilométrico a las hipótesis

Lo que la estilometría puede decir por sí sola, y solo esto, se codifica así para el capítulo de convergencia:

| patrón estilométrico (niveles 1-3) | compatible con | no compatible con |
|---|---|---|
| dentro del rango, LR a favor, núcleo el más próximo | H1, H2, H3 | H5; H4 improbable |
| dentro del rango en léxico y fuera en morfología/caracteres, LR discordante | H2, H3 | H5 |
| fuera del rango pero del tamaño de un salto de género | H1-H3 (con cambio de género), H4 | — (no decide) |
| fuera del rango del tamaño de un cambio de autor, núcleo no el más próximo | H4, H5 | H1; H2 y H3 improbables |
| indeterminado | cualquiera | — |

### 8.6 Formato del veredicto

Por carta: una fila con nivel 1 (verbal, log10 LR mediana, concordancia de familias), nivel 2 (dentro/fuera/indeterminado; tamaño de género/autor), nivel 3 (posición del núcleo, margen), nivel 4 (proporción de configuraciones), patrón de § 8.5 y la lista de las configuraciones que cambiarían el resultado («qué revisaría este juicio»). Sin grado, sin adjetivos.

## 9. Canales no estilométricos: protocolo de codificación

Los tres canales se codifican con libros de códigos fijados aquí, por dos codificadores independientes (el autor y el asistente de investigación), con registro de cada fuente consultada (fecha, URL o referencia, resultado) y con resolución documentada de las discrepancias. Las colecciones de referencia (cartas seguras y pseudoepigrafías conocidas) se codifican **antes** que las catorce cartas.

### 9.1 Recepción y transmisión

- Testigos fijos (lista cerrada): 1 Clemente; Ignacio; Policarpo; Marción (según Tertuliano y Epifanio); fragmento de Muratori; Ireneo; Clemente de Alejandría; Tertuliano; Orígenes (incluida su noticia sobre Hebreos en Eusebio, HE VI 25); 𝔓46 (contenido y orden); 𝔓32, 𝔓87 y los demás papiros paulinos de los siglos II-III (según la lista del INTF); Eusebio (HE III 3 y 25); Atanasio (carta festal 39); el orden de las colecciones (Marción, Muratori, 𝔓46, códices mayúsculos).
- Codificación por carta y testigo: 0 = sin atestación; 1 = alusión posible; 2 = alusión probable o uso claro sin nombre; 3 = cita o atribución explícita a Pablo; con fecha del testigo y la fuente de la atestación (Biblindex, ediciones, bibliografía). Se codifica también la **atribución** (a Pablo / a otro / anónima / negada) y la **posición** en la colección.
- Medidas: fecha de primera atestación en cada nivel; asimetría Oriente/Occidente (diferencia de fechas de la primera atestación de nivel 3); estabilidad de la atribución. Predicciones en § 2.2.
- Hebreos: su anonimato y su recepción desigual son datos de este canal; se codifican como los de cualquier otra carta.

### 9.2 Onomástica y prosopografía

- Inventario: todos los nombres de persona de las catorce cartas (con lugar, función y relación con el remitente) y de las colecciones de referencia: Ignacio y Ps-Ignacio, 1 Clemente y Ps-Clemente, Juliano y Ps-Juliano, Basilio (muestra fija de 60 cartas sorteadas con semilla) y Ps-Basilio, Libanio (muestra fija de 60 cartas), 3 Corintios, Hechos de Pablo (Tecla) y las cartas de Hercher. El libro de códigos de cada nombre: (a) atestado en otra carta paulina; (b) atestado en Hechos; (c) atestado en documentación de la región y el periodo (LGPN, Trismegistos, papyri.info, PHI), con clase de frecuencia; (d) nombre «famoso» (de la literatura o la historia conocida); (e) coherencia interna (lugar, función y cronología compatibles con el resto del corpus).
- Índices por documento: proporción de nombres no famosos y no tomados de otras fuentes del corpus (nombres «nuevos»); proporción de nombres nuevos documentados en la región y el periodo; proporción de incoherencias. Las cartas seguras y las pseudoepigrafías de referencia dan la distribución de cada índice bajo autenticidad y bajo falsificación; cada carta se sitúa en ambas con su percentil. Predicciones en § 2.2.
- Las consultas a bases externas se hacen por navegador y se registran una a una (`docs/registro_onomastica.md`); ninguna se hace con automatismos.

### 9.3 Canal institucional

- Léxico cerrado de organización y culto: ἐπίσκοπος, πρεσβύτερος, διάκονος, προϊστάμενος, ἡγούμενος, χήρα (como categoría), νεώτερος, ἐκκλησία (usos), οἶκος (como célula), χειροτονία/ἐπίθεσις τῶν χειρῶν, y sus contextos, en las catorce cartas y en Hechos, 1 Clemente, Didajé, Ignacio, Policarpo, Hermas.
- Comparación externa: inscripciones de asociaciones (AGRW/Harland) con cargos y fórmulas datables, consultadas por navegador y registradas una a una; se codifica para cada término si el uso de la carta tiene paralelo en el s. I, solo desde finales del s. I, o solo desde el s. II.
- Este canal data, no atribuye: su resultado se traduce a H1-H5 solo a través de la tabla de § 2.2, y su límite (una organización puede ser temprana en un lugar y tardía en otro) se declara en el libro.

### 9.4 Convergencia

Para cada carta, tabla de cuatro filas (estilometría, recepción, onomástica, institucional) × cinco columnas (H1-H5) con tres valores: compatible, no compatible, no decide. Regla de lectura: una hipótesis se declara **sostenida** si ningún canal la hace no compatible y al menos dos la hacen compatible; **debilitada** si un canal la hace no compatible; **descartada** si dos o más canales independientes la hacen no compatible; el resto, **abierta**. No se calcula ninguna probabilidad combinada. Si los canales se contradicen, la contradicción es el resultado y se informa.

## 10. Falsación y resultados adversos

### 10.1 Del método

- Familia con mediana de AUC epistolar < 0,80: no apta; fuera del veredicto.
- 3 Corintios no detectado (puntuación ≥ 0,5 frente al núcleo en la mayoría de las especificaciones de una familia): límite de esa familia frente a un imitador del mismo registro; se informa y la familia sigue, con esa reserva expresa en cada veredicto que dependa de ella.
- Más del 10 % de las cartas `genuine` de Basilio o de Libanio fuera de su propia envolvente (percentil > 90 con IC entero por encima): la envolvente E no representa la variación intra-autor de cartas breves; el nivel 2 se declara no concluyente para todas las cartas de menos de 1.000 palabras (Flm, Tit, 2 Tes).
- Hm2 falsa (G no separable de B): nivel 2 no concluyente para Hebreos y para cualquier carta cuya diferencia sea del tamaño de un cambio de género.

### 10.2 De la hipótesis de partida del autor

La hipótesis de partida (H1-H3 para las trece) queda **refutada para una carta** si esa carta queda fuera del rango intra-autor del tamaño de un cambio de autor (§ 7.3-7.4) en las dos medidas, con LR epistolar en contra en las familias aptas, y el canal de recepción o el onomástico la hacen no compatible con H1-H3 (§ 9.4). Queda **debilitada** si se cumple la parte estilométrica sin el apoyo de otro canal. Con cualquier resultado indeterminado la hipótesis queda **abierta**, y así se dirá. Ninguna de estas conclusiones se atenúa por el número de cartas que la reciban.

### 10.3 Del núcleo

Si alguna carta del núcleo queda por debajo de 0,5 en leave-one-out en la mayoría de las especificaciones de una familia, se informa como heterogeneidad del núcleo; no se cambia el núcleo ni los parámetros dentro de la campaña; el veredicto de las dianas se acompaña del de las cartas del núcleo en la misma tabla, y el lector ve las catorce a la vez.

## 11. Reproducibilidad y registro público

- **Tres sellos** (§ 3.3): `protocolo-1.0.0` (este documento y el conjunto de § 0), `paulinum-1.0.0` (código congelado, antes de calcular ninguna diana), `resultados-1.0.0` (resultados y veredicto). Cada uno es una *release* de GitHub archivada automáticamente en Zenodo; los DOI se anotan en `REGISTRO.md`, `README.md` y `.zenodo.json`, y el libro los cita.
- **Sello técnico:** SHA-256 de la concatenación ordenada de «ruta + SHA-256 del archivo» de todos los archivos cubiertos (`python -m paulinum seal --config config/paulinum_1_0.yaml --run paulinum_1_0 --protocol protocols/paulinum_1_0`), guardado en `SELLO.json`, reproducible por cualquiera con el repositorio en la etiqueta.
- **Etapas** reanudables con bitácora (`results/paulinum_1_0/bitacora.md`): construcción del corpus e inventario; lexicón; anotación (condicional); problemas y calibración por familia; envolventes E, B, G; variables; ventanas deslizantes; dianas; segundo modelo; sensibilidad; veredicto. Las etapas 1-7 se publican antes de la 8.
- **Archivos de resultados:** `inventory.csv`, `problems.csv`, `gi_results_all_specs.csv` (por familia), `calibration_by_spec.csv` (por familia y conjunto de calibración), `summary_by_letter.csv`, `envelope_E.csv`, `envelope_B.csv`, `envelope_G.csv`, `same_standard_ledger.csv` con IC, `nearest_author.csv`, `permanova_*.csv`, `dbrda_*.csv`, `rolling_*.csv`, `edition_noise.csv`, `modelo_svm_*.csv`, `sensibilidad/*/…`, `veredicto.csv`, `config_used.json`, `bitacora.md`.
- **Entornos:** Python 3.10 (portátil) y 3.11 (nube y CI); bibliotecas de `requirements.txt`; pruebas de referencia (`scripts/selftest.py`, `pytest`) verdes en la integración continua en cada sello.
- **Registro en OSF:** cuando se haga, con el DOI de Zenodo del Sello 1 como documento de preregistro; se anota en `REGISTRO.md`.

## 12. Enmiendas

Cualquier desviación de este protocolo se anota en `protocols/paulinum_1_0/REGISTRO.md` **antes** de ejecutarse, con fecha, motivo, alcance y si afecta o no a alguna fila de diana ya calculada (si afecta, la fila se recalcula y ambas versiones se conservan). Las enmiendas admisibles sin nuevo sello son las de metadatos (§ 5.2, cotejo de máscaras con NA28; estados de cartas de Basilio a la vista de bibliografía nueva) y las de implementación que no cambian ninguna regla; cualquier otra exige nuevo sello con nuevo número de versión (1.0.1, …) y nueva *release*. Después del Sello 2 no hay enmiendas que cambien reglas de decisión.

## 13. Referencias metodológicas

Anderson, M. J. (2001), «A new method for non-parametric multivariate analysis of variance», *Austral Ecology* 26. Benedetto, D., Caglioti, E. y Loreto, V. (2002), «Language trees and zipping», *Physical Review Letters* 88. Burrows, J. (2002), «'Delta': a measure of stylistic difference and a guide to likely authorship», *Literary and Linguistic Computing* 17. Cilibrasi, R. y Vitányi, P. (2005), «Clustering by compression», *IEEE Transactions on Information Theory* 51. ENFSI (2015), *Guideline for evaluative reporting in forensic science*. Kestemont, M., Stover, J., Koppel, M., Karsdorp, F. y Daelemans, W. (2016), «Authenticating the writings of Julius Caesar», *Expert Systems with Applications* 63. Koppel, M. y Winter, Y. (2014), «Determining if two documents are written by the same author», *JASIST* 65. Legendre, P. y Anderson, M. J. (1999), «Distance-based redundancy analysis», *Ecological Monographs* 69. Nosek, B. A. *et al.* (2018), «The preregistration revolution», *PNAS* 115. Schuirmann, D. J. (1987), «A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability», *Journal of Pharmacokinetics and Biopharmaceutics* 15. Stamatatos, E. (2009), «A survey of modern authorship attribution methods», *JASIST* 60. Fedwick, P. J. (1981), «A chronology of the life and works of Basil of Caesarea», en *Basil of Caesarea: Christian, Humanist, Ascetic*. Deferrari, R. J. (1926-1934), *Saint Basil: The Letters*, Loeb. Foerster, R. (1903-1927), *Libanii opera*, Teubner. Hercher, R. (1873), *Epistolographi Graeci*. Wright, W. C. (1913-1923), *The Works of the Emperor Julian*, Loeb.

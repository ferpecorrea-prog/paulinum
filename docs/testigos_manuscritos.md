# Testigos manuscritos en paulinum 1.0: Codex Sinaiticus y 𝔓46

Desarrolla el § 5.4 del protocolo (`protocols/paulinum_1_0/PROTOCOLO.md`). Fija, antes de tocar los archivos, qué
derivados se construyen a partir de las transcripciones, con qué reglas y cómo entran en la sensibilidad. Todo lo que
aquí se fija se ejecuta con guiones versionados, y ninguna transformación se hace a mano.

## 1. Estatuto

Los testigos son **ediciones de sensibilidad**, no fuentes de rasgos autorales: la ortografía, la división de palabras,
las correcciones y los hábitos gráficos de los copistas del s. III (𝔓46) y del s. IV (Sinaítico) no dicen nada de Pablo.
Sirven para dos cosas: (a) medir cuánto cambia el resultado de cada carta cuando el texto no es el de una edición
crítica moderna sino el de un testigo concreto (ruido de transmisión, junto a Tischendorf, Nestle 1904 y NA28); (b)
aportar al canal de recepción y transmisión (§ 9.1) el dato del contenido y el orden de 𝔓46 (Hebreos tras Romanos;
Pastorales ausentes), que es un dato de transmisión, no un argumento estilométrico.

## 2. Fuentes, adquisición y licencias

| testigo | fuente | archivo bruto | uso |
|---|---|---|---|
| Codex Sinaiticus (GA 01) | transcripción del proyecto Codex Sinaiticus, v1.05 (ITSEE / Universidad de Birmingham, UBIRA e-prints 3306) | `sinaiticus_project_v105.xml` | **transcripción principal** del Sinaítico |
| Codex Sinaiticus (GA 01) | NTVMR, docID 20001 (INTF, Münster) | `sinaiticus_ntvmr_20001.xml` | control de transcripción (§ 4.4) y codificación homogénea con 𝔓46 |
| 𝔓46 (P. Chester Beatty II + P. Mich. inv. 6238) | NTVMR, docID 10046 | `p46_ntvmr_10046.xml` | única transcripción completa accesible de 𝔓46 |

- Adquisición: `scripts/testigos/preparar_testigos.py` (guion del autor, conservado sin cambios; SHA-256 en
  `data/provenance.json`), que descarga de las fuentes primarias y escribe `TESTIGOS_MANIFEST.json` con URL, fecha,
  cabeceras, tamaño y SHA-256 de cada archivo, y la respuesta de copyright de NTVMR cuando existe. Los XML brutos no
  se editan nunca; cualquier lectura discutible se resuelve en los derivados, con registro.
- Licencias: la transcripción del proyecto Codex Sinaiticus es CC BY-NC-SA 3.0; las de NTVMR llevan la licencia que
  declare su respuesta `getCopyright` (se guarda). Ninguno de los tres XML ni ningún derivado con texto íntegro se
  versiona ni se redistribuye (`.gitignore`); se publican el manifiesto con las huellas, los guiones y los agregados.
- Si un archivo no se obtiene, se anota en el manifiesto y el testigo queda fuera; no se sustituye por otra fuente.

## 3. Derivados (los genera `scripts/testigos/derivar_testigos.py`, determinista, ~5 s)

| derivado | contenido | se publica |
|---|---|---|
| `derivados/<testigo>_<carta>_bruto.txt` | `ref\ttexto` por versículo: mano primera, palabras íntegramente atestiguadas, nomina sacra expandidos, ν suspendida restituida, minúsculas, sin diacríticos, ϲ→σ | no (texto íntegro); sí su SHA-256 en `RESUMEN.json` |
| `derivados/<testigo>_<carta>_reg.txt` | ídem con la regularización ortográfica guiada de § 4.3 | no; sí su SHA-256 |
| `derivados/<testigo>_<carta>_sblgnt_recortado.txt` | SBLGNT sin diacríticos recortado a las palabras alineadas con texto atestiguado (recorte simétrico) | no; sí su SHA-256 |
| `derivados/cobertura.csv` | por testigo, carta y versículo: `conservado` / `parcial` / `laguna` / `no_contenido` / `sin_correspondencia_sblgnt`, con recuentos | sí |
| `derivados/intervenciones.tsv` | cada transformación (exclusión, expansión, ν restituida, regularización), con testigo, carta, versículo, posición, forma original, forma resultante y regla | sí |
| `derivados/acuerdo_ediciones.csv` | acuerdo de tokens de cada testigo con SBLGNT por carta, bruto y regularizado | sí |
| `derivados/acuerdo_transcripciones_01.csv` y `discrepancias_transcripciones_01_muestra.tsv` | acuerdo entre las dos transcripciones del Sinaítico por carta (versículos comunes), y muestra de discrepancias | sí |
| `derivados/p46_contenido_y_orden.csv` | libros contenidos en 𝔓46 y su orden en el códice, versículos transcritos y con texto atestiguado | sí |
| `derivados/RESUMEN.json` | huellas de los XML y de todos los derivados, recuentos por regla, orden de los libros en cada códice | sí |
| `TESTIGOS_MANIFEST.publicado.json` | el manifiesto del guion de adquisición, idéntico al original salvo las cabeceras `Set-Cookie` (cookies de sesión de los servidores), suprimidas; el original queda intacto en local | sí |

## 4. Reglas de transformación (fijas; son las que ejecuta el guion)

### 4.1 Qué texto se toma
- **Mano primera.** NTVMR: `rdg type="orig"`; proyecto Codex Sinaiticus: `rdg type="main-corr"`. Las correcciones de
  todos los correctores se excluyen. Una `<w/>` vacía en la mano primera es una omisión del copista (no hay nada que
  excluir; se cuenta: 360 en las catorce cartas del Sinaítico).
- **`supplied` (texto restituido por el editor) y `gap`: excluidos** a nivel de palabra (no se imputan lagunas); el
  versículo se marca `parcial`. En 𝔓46 son 3.019 palabras de 25.603 (bordes dañados del papiro).
- **`unclear`: incluido** con la lectura de la transcripción, y contado (1.397 en 𝔓46).
- **División de palabras:** la de la transcripción (`<w>`), con los saltos de línea internos unidos. Signos de
  puntuación transcritos como palabras (`<w>·</w>`) no cuentan. Apóstrofos y diástoles del copista (tras nombres
  indeclinables) se eliminan.

### 4.2 Nomina sacra y rayas
- **Nomina sacra**: tabla cerrada `NOMINA_SACRA` del guion (θεός, κύριος, Ἰησοῦς, Χριστός, πνεῦμα y derivados, πατήρ,
  υἱός, ἄνθρωπος, οὐρανός, Ἰσραήλ, Ἰερουσαλήμ, Δαυίδ, σταυρός y derivados, σωτήρ, μήτηρ, con sus casos), aplicada a las
  palabras marcadas como abreviatura (NTVMR: `abbr type="nomSac"`; proyecto: `hi rend="ol2"`). Es la misma tabla de
  3 Corintios (D-006), completada.
- **Raya sobre vocal (proyecto, `ol2` sin correspondencia en la tabla)**: es la ν suspendida del copista. Se restituye
  (a) donde, con la ν añadida al final o en posición interior, la forma coincide bajo la tabla T con una forma de SBLGNT
  del mismo versículo (1.096 casos); (b) si no hay coincidencia y la raya cae sobre vocal final, ν final por la
  convención del códice (33 casos). Lo demás se conserva y se registra (8 casos). `hi rend="ol"` (raya sobre υ/ι
  inicial) no es abreviatura y se ignora.

### 4.3 Regularización ortográfica guiada por alineación
Los testigos no llevan diacríticos, y su ortografía refleja la pronunciación del copista. Para no confundir ese ruido
con variantes reales, el derivado `_reg` aplica esta regla mecánica: cada versículo del testigo se alinea con el de
SBLGNT (sin diacríticos) por `difflib` en dos niveles (formas exactas; luego formas canonizadas); una forma se
**sustituye por la de SBLGNT alineada solo si difiere de ella exclusivamente** por las sustituciones de la tabla T:
ει~ι, η~ι, οι~υ, αι~ε, ω~ο, consonante geminada ~ simple, ν final. Cualquier otra diferencia (palabra distinta, forma
morfológica distinta, orden, omisión, adición) se conserva tal cual: son las variantes textuales, que es lo que se
quiere medir (1.261 conservadas en el Sinaítico, 1.241 en 𝔓46). Toda sustitución queda en `intervenciones.tsv`.

### 4.4 Dos transcripciones del Sinaítico
La del proyecto Codex Sinaiticus es la principal. La copia NTVMR se procesa con las mismas reglas y se alinea con ella
versículo a versículo: acuerdo de 0,988 a 0,999 por carta (media 0,996); la copia NTVMR carece de 31 versículos de
1 Tesalonicenses y 25 de Hebreos. Las discrepancias (muestra publicada) no se resuelven a mano; el análisis usa la
principal.

### 4.5 Resultado de la primera ejecución (27-IX-2026)
Acuerdo regularizado con SBLGNT: Sinaítico 0,958-0,988 por carta; 𝔓46 0,927-0,962. Todas las cartas superan el umbral
de aptitud de § 5 (≥ 0,90). 𝔓46 conserva Rom (232 versículos con texto), Heb (300), 1 Cor (433), 2 Cor (251), Ef (150),
Gal (136), Flp (93), Col (77) y 1 Tes (10 versículos, 29 palabras), en ese orden; no contiene 2 Tes, las Pastorales
ni Filemón.

## 5. Uso en la sensibilidad (§ 5.4 y § 6.2 del protocolo)

- Cada testigo entra como una «edición» más de la rejilla de sensibilidad, con la variante `nodia` (los testigos no
  tienen diacríticos; SBLGNT se compara sin ellos) y con el derivado `_reg` como texto; el `_bruto` solo se informa.
- **Recorte simétrico.** Para cada testigo y carta se construye también la edición SBLGNT **recortada a los versículos
  que el testigo conserva** (`conservado`; los `parcial` se excluyen de ambos lados). Así la distancia testigo-edición
  mide solo diferencias de texto, no de cobertura, y se compara con la distancia entre cartas distintas del núcleo
  (regla del ruido de edición de § 5.4).
- 𝔓46 no contiene las Pastorales ni Filemón ni 2 Tesalonicenses: para esas cartas no hay sensibilidad con 𝔓46 y se
  dice; su ausencia es un dato del canal de transmisión (§ 9.1), no del estilométrico.
- El Sinaítico contiene las catorce cartas; es el único testigo con sensibilidad completa.
- Umbral de aptitud: si el acuerdo regularizado de un testigo con SBLGNT en una carta es < 0,90 (texto muy lagunoso o
  transcripción problemática), o el testigo conserva menos de 300 palabras de la carta (𝔓46 en 1 Tesalonicenses: 29),
  esa carta queda fuera de la sensibilidad de ese testigo y se informa.

## 6. Reproducibilidad

Guiones (`scripts/testigos/`), manifiesto de descargas (`TESTIGOS_MANIFEST.json`, copiado a `data/local/testigos/` y
versionado), huellas de los derivados (`data/provenance.json`) y agregados publicados entran en el Sello 2 y en la
*release* archivada en Zenodo; el registro en OSF remitirá a ese DOI. Con los tres XML (que cualquiera puede obtener
de las mismas fuentes con el mismo guion) y el repositorio en la etiqueta, los derivados se regeneran byte a byte.

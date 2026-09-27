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

## 3. Derivados (todos los genera `scripts/testigos/derivar_testigos.py`, determinista)

| derivado | contenido | se publica |
|---|---|---|
| `derivados/<testigo>_<carta>_bruto.txt` | `ref\ttexto` por versículo, mano primera, nomina sacra expandidos, minúsculas, sin regularizar | no (texto íntegro); sí su SHA-256 |
| `derivados/<testigo>_<carta>_reg.txt` | ídem, con la regularización ortográfica guiada de § 4.3 | no; sí su SHA-256 |
| `derivados/<testigo>_cobertura.csv` | por carta y versículo: `conservado` / `parcial` / `laguna` / `no_contenido` | sí |
| `derivados/<testigo>_intervenciones.tsv` | cada transformación aplicada, con carta, versículo, posición, forma original, forma resultante y regla | sí |
| `derivados/acuerdo_transcripciones_01.csv` | acuerdo de tokens entre las dos transcripciones del Sinaítico, por carta (§ 4.4) | sí |
| `derivados/acuerdo_ediciones.csv` | acuerdo de tokens de cada testigo con SBLGNT (sin diacríticos), por carta, en bruto y regularizado | sí |
| `derivados/p46_contenido_y_orden.csv` | libros contenidos, orden, folios conservados y perdidos (para § 9.1) | sí |

## 4. Reglas de transformación (fijas)

### 4.1 Qué texto se toma
- **Mano primera.** Se toma la lectura del copista original; las correcciones de todos los correctores se excluyen del
  texto y se cuentan en `intervenciones.tsv` (número por carta). Motivo: el texto del testigo es el que escribió su
  copista; las correcciones son otros testigos superpuestos.
- **`supplied` (texto restituido por el editor): excluido.** Una laguna es ausencia de texto, no texto conjetural
  (regla del paquete: no imputar lagunas). El versículo afectado se marca `parcial`.
- **`unclear`: incluido** con la lectura que da la transcripción, y contado.
- **`gap` / folios perdidos:** el versículo se marca `laguna`; un libro que el testigo no contiene, `no_contenido`.
- **División de palabras:** la de la transcripción (`<w>`); no se resegmenta.
- **Números, abreviaturas y ligaduras:** como los transcribe la fuente; las abreviaturas no sagradas se expanden solo
  si la transcripción da la expansión.

### 4.2 Nomina sacra
Se expanden con una tabla cerrada (forma abreviada → forma plena por caso, deducida de la terminación): ΘΣ/ΘΥ/ΘΩ/ΘΝ
(θεός), ΚΣ/ΚΥ/ΚΩ/ΚΝ/ΚΕ (κύριος), ΙΣ/ΙΥ/ΙΝ (Ἰησοῦς), ΧΣ/ΧΥ/ΧΩ/ΧΝ (Χριστός), ΠΝΑ/ΠΝΣ/ΠΝΙ (πνεῦμα), ΠΗΡ/ΠΡΣ/ΠΡΙ/ΠΡΑ
(πατήρ), ΥΣ/ΥΥ/ΥΩ/ΥΝ (υἱός), ΑΝΟΣ/ΑΝΟΥ… (ἄνθρωπος), ΟΥΝΟΣ… (οὐρανός), ΙΗΛ (Ἰσραήλ), ΙΛΗΜ (Ἰερουσαλήμ), ΔΑΔ (Δαυίδ),
ΣΤΡΣ/ΣΤΡΟΥ… (σταυρός), ΣΩΡ/ΣΡΣ… (σωτήρ), ΜΗΡ/ΜΡΣ… (μήτηρ). Es la misma tabla que se aplicó a 3 Corintios (D-006),
completada; cada expansión se registra.

### 4.3 Regularización ortográfica guiada por alineación
Los testigos no llevan diacríticos, y su ortografía refleja la pronunciación del copista. Para no confundir ese ruido
con variantes reales, el derivado `_reg` aplica esta regla mecánica: cada forma del testigo se alinea con la forma de
SBLGNT (sin diacríticos) del mismo versículo por alineación de secuencias (`difflib`, coste de sustitución por
similitud de caracteres); una forma se **sustituye por la de SBLGNT solo si difiere de ella exclusivamente** por
sustituciones de la tabla T: ει~ι, ι~ει, αι~ε, ε~αι, ο~ω, ω~ο, η~ι, η~ει, οι~υ, υ~οι, ου~υ, ν efelcística final,
geminación o simplificación de consonante, ς/σ. Cualquier otra diferencia (palabra distinta, forma morfológica
distinta, orden, omisión, adición) se conserva tal cual: son las variantes textuales, que es lo que se quiere medir.
Toda sustitución queda en `intervenciones.tsv` con la regla que la autorizó.

### 4.4 Dos transcripciones del Sinaítico
La del proyecto Codex Sinaiticus es la principal. La copia NTVMR se alinea con ella versículo a versículo y se
informa el acuerdo de tokens por carta; una discrepancia no se resuelve a mano: si el acuerdo en una carta es
< 0,995 se lista en `acuerdo_transcripciones_01.csv` y se dice en el informe. El análisis usa siempre la principal.

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
  transcripción problemática), esa carta queda fuera de la sensibilidad de ese testigo y se informa.

## 6. Reproducibilidad

Guiones (`scripts/testigos/`), manifiesto de descargas (`TESTIGOS_MANIFEST.json`, copiado a `data/local/testigos/` y
versionado), huellas de los derivados (`data/provenance.json`) y agregados publicados entran en el Sello 2 y en la
*release* archivada en Zenodo; el registro en OSF remitirá a ese DOI. Con los tres XML (que cualquiera puede obtener
de las mismas fuentes con el mismo guion) y el repositorio en la etiqueta, los derivados se regeneran byte a byte.

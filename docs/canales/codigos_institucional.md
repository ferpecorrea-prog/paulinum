# Libro de códigos · Canal institucional (PROTOCOLO § 9.3)

Este canal **data, no atribuye**: dice con qué fase de la organización de las comunidades es compatible el vocabulario
de cada carta. Su traducción a H1-H5 pasa solo por la tabla de § 2.2, y su límite (una organización puede ser
temprana en un lugar y tardía en otro) se declara en el libro.

## 1. Léxico cerrado (del protocolo)

ἐπίσκοπος (y ἐπισκοπή, ἐπισκοπέω como cargo), πρεσβύτερος / πρεσβυτέριον (como cargo, no como «anciano» de edad),
διάκονος / διακονία (como cargo o función reconocida), προϊστάμενος, ἡγούμενος, χήρα (como categoría reconocida, no
como estado civil), νεώτερος (como grupo), ἐκκλησία (usos: local / universal / reunión), οἶκος (como célula:
«la iglesia en su casa», «casa» como unidad de bautismo o de gobierno), χειροτονία / ἐπίθεσις τῶν χειρῶν (como rito
de institución). Cada aparición se codifica en su **contexto**: la misma palabra puede ser cargo en un pasaje y no en otro.

## 2. Corpus de comparación

Las catorce cartas; Hechos; 1 Clemente; Didajé; Ignacio (siete cartas); Policarpo; Hermas. Para cada texto se usa la
edición del corpus (SBLGNT para el NT; Ehrman LCL 24-25 y Holmes 2007 para los Padres apostólicos).

## 3. Codificación (`results/canales/institucional.csv`)

| columna | valores |
|---|---|
| `documento` | id (carta, Hch, 1Clem, Did, Ign*, Pol, Herm) |
| `termino` | lema del léxico § 1 |
| `pasaje` | referencia |
| `forma` | forma del texto |
| `uso` | `cargo` (título de una función estable con requisitos, elección o institución) · `funcion` (actividad sin título fijo) · `categoria` (grupo reconocido: viudas, jóvenes) · `celula` (οἶκος) · `reunion` / `local` / `universal` (ἐκκλησία) · `rito` (imposición de manos como institución) · `no_institucional` (sentido común de la palabra) |
| `rasgos` | lista cerrada, separada por `;`: `requisitos` (lista de cualidades exigidas), `eleccion`, `remuneracion`, `disciplina`, `jerarquia` (subordinación explícita entre cargos), `monoepiscopado` (un ἐπίσκοπος distinto de los πρεσβύτεροι), `colegio` (plural de presbíteros/obispos), `registro` (lista de viudas), `sucesion` |
| `paralelo_epigrafico` | resultado de la comparación externa § 4: `s1` (uso con paralelo en asociaciones del s. I), `fin_s1` (solo desde finales del s. I), `s2` (solo desde el s. II), `sin_paralelo`, `no_aplica` (usos no institucionales) |
| `fuente` | inscripción o texto de comparación (AGRW n.º, referencia de la edición) |
| `cita` | texto breve |
| `juicio` | `sí` si la asignación de `uso` o de `paralelo_epigrafico` depende de apreciación |
| `nota` | |

## 4. Comparación externa

Inscripciones de asociaciones (AGRW, Ascough-Harland-Kloppenborg 2012, y la base philipharland.com) con cargos y
fórmulas datables: para cada término con `uso`=`cargo`, `categoria` o `rito` se busca el uso más próximo (título +
rasgos) y se registra la inscripción datada más antigua que lo ofrece, una consulta por término y rasgo, anotada en
`registro_consultas.md`. Términos eclesiales sin equivalente en asociaciones (ἐπίθεσις τῶν χειρῶν) se comparan con el
corpus § 2 (uso más antiguo datable en los textos cristianos) y se codifican por esa fecha.

## 5. Lectura (`results/canales/institucional_resumen.csv`, una fila por documento) y § 2.2

- `n_cargos`, `n_rasgos`, `fecha_compatible`: la fase más tardía exigida por el conjunto de usos institucionales del
  documento (`s1` / `fin_s1` / `s2`), con y sin las filas `juicio=sí`.
- H1-H3: vocabulario compatible con las asociaciones del s. I (`s1`); H4: `fin_s1`; H5: `s2` o posterior. Un
  documento sin usos institucionales (`n_cargos`=0) → «no decide».
- Los textos de comparación cristianos (Hechos, 1 Clemente, Didajé, Ignacio, Policarpo, Hermas) se codifican primero
  y fijan qué rasgos aparecen en cada fase; la lectura de las catorce cartas se hace con esa escala y no al revés.

# Libro de códigos · Onomástica y prosopografía (PROTOCOLO § 9.2)

## 1. Inventario (`results/canales/onomastica_inventario.csv`)

Una fila por **nombre de persona** × documento. Entran todos los nombres propios de persona (no de lugar, pueblo ni
divinidad) de las catorce cartas y de las colecciones de referencia; el remitente y el destinatario nominal también
entran, marcados en `funcion`. Un mismo nombre en dos documentos son dos filas; un mismo nombre dos veces en el
mismo documento es una fila con `n_menciones`.

| columna | valores |
|---|---|
| `coleccion` | `paulinas` (las 14), `Ignacio`, `Ps-Ignacio`, `1Clem`, `Ps-Clemente`, `Juliano`, `Ps-Juliano`, `Basilio` (muestra § 4), `Ps-Basilio`, `Libanio` (muestra § 4), `3Cor`, `HechosPablo` (Hechos de Pablo y Tecla), `Hercher` (las colecciones pseudoepigráficas del corpus: Ps-Fálaris, Ps-Diógenes, Ps-Socráticos, Ps-Temístocles, Ps-Bruto, Ps-Crates, Ps-Quión, Ps-Eurípides, Ps-Sócrates, Ps-Anacarsis, Ps-Solón, Ps-Nicias, Ps-Mitrídates, Ps-Antíoco, Ps-Artajerjes) |
| `documento` | id del documento en el corpus (`Rom`, `IgnEf`, `Bas_Ep#105`…) o referencia externa (`AP Tecla`) |
| `estado` | `core` / `target` / `genuine` / `spurious` / `mixed` (el del corpus) |
| `nombre` | forma griega nominativa normalizada (sin diacríticos, σ final unificada) |
| `nombre_es` | forma castellana usual |
| `pasaje` | capítulo y versículo, o número de carta y párrafo |
| `n_menciones` | entero |
| `lugar` | lugar asociado en el texto (ciudad, región) o `—` |
| `funcion` | `remitente` / `destinatario` / `colaborador` / `saludado` / `mencionado` / `adversario` / `personaje literario` |
| `relacion` | relación explícita con el remitente (`hermano`, `colaborador`, `hijo`, `prisionero conmigo`…) o `—` |
| `a_otra_carta` | 1 si el nombre aparece en **otra** carta paulina (de las 14) con la misma identidad probable; 0 si no; `na` fuera de las paulinas (para las colecciones, «otra carta de la misma colección») |
| `b_hechos` | 1 si aparece en Hechos con identidad compatible; 0 si no |
| `c_region_periodo` | atestación del nombre (no de la persona) en la documentación de la región y del periodo (ss. I a. C.-II d. C.): `0` no atestado; `1` raro (1-5 portadores en LGPN + Trismegistos + PHI para la región); `2` corriente (6-50); `3` muy corriente (> 50). Región = la del lugar asociado o, sin lugar, la del destinatario de la carta |
| `d_famoso` | 1 si el nombre es «famoso» (personaje de la literatura o la historia conocidas antes del documento: reyes, filósofos, héroes, personajes bíblicos) usado como tal; 0 si no |
| `e_coherencia` | `coherente` / `incoherente` / `no comprobable`: lugar, función y cronología compatibles con el resto del corpus paulino (para las paulinas) o con la colección (para las de referencia). `incoherente` exige una contradicción concreta anotada en `cita` |
| `nuevo` | derivado: 1 si `a_otra_carta`=0, `b_hechos`=0 y `d_famoso`=0 (nombre que la carta no ha podido tomar de otra fuente del corpus) |
| `fuente` | base o edición consultada para `c` (LGPN vol./región, Trismegistos NAM id, papyri.info, PHI) y para `b`/`d` |
| `cita` | registro breve (p. ej. «LGPN V.A: 12 portadores, Éfeso, ss. I-II») |
| `juicio` | `sí` en `e_coherencia`, en `a`/`b` cuando la identidad es dudosa, y en `c` cuando la región se ha inferido |
| `nota` | observaciones |

## 2. Índices por documento (`results/canales/onomastica_indices.csv`)

- `n_nombres`: nombres distintos (sin remitente ni destinatario nominal).
- `p_nuevos`: proporción de nombres `nuevo`=1.
- `p_nuevos_documentados`: proporción de los nombres nuevos con `c_region_periodo` ≥ 1.
- `p_incoherencias`: proporción de nombres con `e_coherencia`=`incoherente`.
- `p_famosos`: proporción de `d_famoso`=1.
Cada índice se calcula dos veces: con todas las filas y sin las filas `juicio=sí`. Las cartas seguras (Ignacio,
1 Clemente, Juliano, Basilio, Libanio) dan la distribución bajo autenticidad; las pseudoepigrafías (Ps-Ignacio,
Ps-Clemente, Ps-Juliano, Ps-Basilio, 3 Corintios, Hechos de Pablo, Hercher) la distribución bajo falsificación; cada
una de las catorce cartas se sitúa en ambas con su percentil (`pct_autenticidad`, `pct_falsificacion`). Los documentos
sin nombres (`n_nombres`=0) se informan y no entran en las distribuciones.

## 3. Lectura con § 2.2

- H1-H3: `p_nuevos` y `p_nuevos_documentados` dentro del rango de las cartas seguras (percentil 10-90 bajo
  autenticidad) y `p_incoherencias` en su rango.
- H4: `p_nuevos` bajo (percentil < 10 bajo autenticidad) con `a_otra_carta` o `b_hechos` altos: nombres tomados de las
  cartas seguras o de Hechos.
- H5: `p_famosos` o `p_incoherencias` en el rango de las pseudoepigrafías (percentil > 90 bajo autenticidad), o
  `n_nombres`=0 en una carta de un género que en las seguras lleva nombres.
- Lo demás: «no decide». Los umbrales de percentil se fijan aquí, antes de codificar.

## 4. Muestras fijas (sorteo con semilla 20260929, `numpy.random.default_rng`, 60 sin reemplazo sobre las cartas genuinas del corpus, ordenadas por id)

- Basilio de Cesarea (174 cartas genuinas en el corpus): Ep. 1, 3, 6, 14, 18, 20, 22, 23, 25, 28, 32, 34, 37, 51, 53,
  55, 65, 68, 70, 73, 84, 89, 90, 91, 92, 93, 96, 105, 114, 116, 124, 125, 135, 136, 138, 148, 150, 155, 160, 162,
  165, 172, 191, 212, 213, 219, 222, 224, 235, 237, 238, 243, 244, 245, 248, 250, 262, 271, 272, 294.
- Libanio (170 cartas genuinas en el corpus, numeración Foerster): Ep. 25, 37, 70, 81, 97, 101, 113, 114, 119, 150,
  163, 173, 175, 192, 195, 208, 219, 224, 238, 245, 256, 267, 281, 282, 298, 309, 315, 316, 319, 326, 330, 340, 359,
  362, 369, 374, 375, 379, 405, 432, 438, 493, 495, 497, 503, 516, 557, 560, 580, 620, 673, 731, 791, 793, 796, 802,
  810, 811, 819, 833.
Las demás colecciones entran enteras (Ignacio 7, Ps-Ignacio 13, 1 Clemente, Ps-Clemente 5, Juliano 36, Ps-Juliano 10,
Ps-Basilio 3, 3 Corintios, Hechos de Pablo y Tecla, Hercher 105 cartas).

## 5. Fuentes para `c_region_periodo` (consultadas por navegador, una a una, y registradas)

LGPN (lgpn.ox.ac.uk, búsqueda por nombre y región), Trismegistos People (trismegistos.org/name; verificación
anti-robots que pasa el autor), papyri.info (búsqueda de texto), PHI Greek Inscriptions (inscriptions.packhum.org,
búsqueda por región). Se registra el número de portadores y la horquilla de fechas que la base ofrece; si la base no
permite acotar por fecha, se anota y se codifica con la cifra total marcando `juicio=sí`.

## 6. Concreción fijada antes de consultar (29-IX-2026, D-028)

Consulta (c) para todos los nombres nuevos de las catorce cartas y para una muestra sorteada (semilla 20260929) de
hasta 15 nombres nuevos por colección de referencia; fuente principal PHI Greek Inscriptions (recuento total y por
región, sin fecha → `juicio=sí`), papyri.info si PHI da 0. Escala de `c_region_periodo` aplicada al recuento total de
PHI (o de papyri.info): 0 = 0; 1 = 1-5; 2 = 6-50; 3 = > 50; se anota además el recuento de la región del documento
cuando PHI la desglosa. Los nombres no muestreados quedan con `c_region_periodo` vacío y no entran en
`p_nuevos_documentados`.

## 7. Precisiones fijadas tras codificar (29-IX-2026; D-029)

La lectura de § 3 se aplica por hipótesis (compatible / no compatible / no decide), como exige § 9.4, con tres
precisiones que la codificación del núcleo hizo necesarias y que se declaran aquí: (a) una carta sin nombres fuera del
prescripto (`n_nombres` = 0) queda «no decide» en las tres hipótesis, porque 1 Tesalonicenses, del núcleo, tampoco los
lleva: el cero no distingue; (b) H4 se declara «no compatible» cuando la mitad o más de los nombres son nuevos
(`p_nuevos` ≥ 0,5: no pueden proceder de las cartas seguras ni de Hechos) y «no decide» en los demás casos salvo la
señal positiva de § 3; (c) H5 se declara «no compatible» cuando la mitad o más de los nombres nuevos consultados están
documentados en la epigrafía (`p_nuevos_documentados` ≥ 0,5) y no hay incoherencias por encima del percentil 90.
El remitente y el destinatario nominal no cuentan como nombres del documento (en las colecciones de referencia, tampoco
el nombre del autor real o supuesto). Percentiles calculados sobre los documentos con al menos un nombre: 134 bajo
autenticidad, 123 bajo falsificación. papyri.info, prevista como segunda fuente cuando PHI da 0, no se usa: su búsqueda
por subcadena sin mayúsculas ni acentos devuelve ruido (ἤλεκτρον para «Λέκτρ») que exigiría revisar cada resultado a
mano; los 17 nombres con 0 apariciones en PHI quedan con `c_region_periodo` = 0 y `juicio` = sí.

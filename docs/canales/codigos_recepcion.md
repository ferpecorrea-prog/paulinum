# Libro de códigos · Canal de recepción y transmisión (PROTOCOLO § 9.1)

## 1. Testigos (lista cerrada del protocolo, con fecha y fuente de referencia)

| id | testigo | fecha (convencional) | ámbito | fuente de referencia para la codificación |
|---|---|---|---|---|
| 1Clem | 1 Clemente | c. 96 (horquilla 80-140) | Roma (Occidente) | Ehrman, LCL 24 (2003); Lindemann 1979; Biblindex |
| Ign | Ignacio de Antioquía (recensión media, siete cartas) | c. 110 (horquilla 105-170) | Asia Menor (Oriente) | Ehrman, LCL 24; Holmes 2007; Biblindex |
| Pol | Policarpo, *A los Filipenses* | c. 110-140 | Esmirna (Oriente) | Holmes 2007; Berding 2002 |
| Marc | Marción, *Apostolikon* (según Tertuliano, *Adv. Marc.* V, y Epifanio, *Pan.* 42) | c. 140-144 | Roma / Asia Menor | Schmid 1995; BeDuhn 2013; Roth 2015 |
| Mur | Fragmento de Muratori | fines s. II (tesis mayoritaria; s. IV según Hahneman 1992) | Roma | Hahneman 1992; Verheyden 2003 |
| Iren | Ireneo, *Adversus haereses* | c. 180 | Lyon (Occidente) | SC 100-294; Biblindex |
| ClemAl | Clemente de Alejandría | c. 190-215 | Alejandría (Oriente) | SC / GCS; Biblindex |
| Tert | Tertuliano | c. 197-220 | Cartago (Occidente) | CCSL 1-2; Biblindex |
| Orig | Orígenes (incl. la noticia sobre Hebreos en Eusebio, HE VI 25, 11-14) | c. 220-250 | Alejandría / Cesarea (Oriente) | GCS; Biblindex; Eusebio, SC 41 |
| P46 | 𝔓46 (P. Chester Beatty II + P. Mich. inv. 6238): contenido y orden | c. 200 (horquilla 175-250) | Egipto | NTVMR 10046; derivados de la campaña (`results/…/p46_contenido_y_orden.csv`) |
| Pap | 𝔓32 (Tit), 𝔓87 (Flm) y los demás papiros paulinos de los siglos II-III: la lista se toma de la Kurzgefasste Liste del INTF en el momento de codificar (consulta registrada), con la datación del INTF y, si difiere, la de Orsini-Clarysse 2012; se codifica por carta el papiro más antiguo que la contiene | ss. II-III | Egipto | INTF, NTVMR (Liste); Orsini-Clarysse 2012 |
| Eus | Eusebio, HE III 3 y III 25 | c. 313-325 | Cesarea (Oriente) | SC 31 |
| Athan | Atanasio, carta festal 39 | 367 | Alejandría (Oriente) | Brakke 2010 (trad.); PG 26 |
| Orden | orden de las cartas en las colecciones: Marción, Muratori, 𝔓46, Sinaítico, Vaticano, Alejandrino, Claromontano (catálogo) | ss. II-VI | — | Trobisch 1994; Gamble 1995; NTVMR |

El ámbito Oriente/Occidente sigue el lugar de composición del testigo (no de la tradición manuscrita). Las fechas
son las convencionales de los manuales citados; cuando la datación es discutida se anota la horquilla y la codificación
usa el **extremo tardío** (regla conservadora: nunca se adelanta la primera atestación por una datación temprana discutida).

## 2. Códigos por carta y testigo (`results/canales/recepcion.csv`)

Una fila por carta (14) × testigo (14 filas de la tabla anterior; `Pap` y `Orden` se codifican por carta con sus
propios campos). Columnas:

| columna | valores |
|---|---|
| `carta` | Rom, 1Cor, 2Cor, Gal, Flp, 1Tes, Flm (núcleo); Ef, Col, 2Tes, 1Tim, 2Tim, Tit, Heb (dianas) |
| `testigo` | id de la tabla § 1 |
| `fecha_testigo` | año o horquilla; para `Pap`, la datación del papiro más antiguo que contiene la carta |
| `atestacion` | **0** sin atestación · **1** alusión posible (coincidencia verbal breve, explicable por lengua común) · **2** alusión probable o uso claro sin nombre (secuencia verbal o de ideas que exige la carta) · **3** cita o atribución explícita a Pablo (nombre, «el Apóstol», o inclusión en una colección paulina) |
| `atribucion` | `Pablo` / `otro` (con el nombre) / `anonima` / `negada` / `na` (sin atestación) |
| `posicion` | posición ordinal de la carta en la colección del testigo (solo Marc, Mur, P46, Orden), o `ausente` |
| `pasaje` | referencia del testigo (libro, capítulo, párrafo) o del papiro (contenido) |
| `fuente` | edición o base de datos con la que se ha verificado |
| `cita` | texto breve (≤ 25 palabras) del pasaje o de la ficha |
| `juicio` | `sí` si el código 1 o 2 depende de apreciación del codificador; `no` en los códigos 0 y 3 y en los 2 con paralelo verbal extenso |
| `nota` | observaciones |

Reglas:
- Para cada testigo se codifica el **nivel máximo** alcanzado en toda su obra conservada; el `pasaje` es el que lo
  alcanza. Un testigo con varios pasajes de nivel inferior no suma.
- `3` exige nombre o inclusión en colección; una cita literal sin nombre en un autor que en otro lugar nombra a Pablo
  se codifica `2` (el nombre no se traslada de un pasaje a otro).
- Marción: `3` = presente en el *Apostolikon* según Tertuliano o Epifanio; `negada` = rechazada expresamente; las
  Pastorales, ausentes del *Apostolikon* según Tertuliano (*Adv. Marc.* V 21), se codifican `0` con `nota`
  «ausente; Tertuliano lo señala».
- Hebreos: anónima en 𝔓46 (posición tras Romanos), atribuida a Pablo en Oriente (Clemente de Alejandría, Orígenes con
  reserva: «quién escribió la carta, en verdad Dios lo sabe») y no reconocida en Occidente hasta el s. IV: cada
  testigo se codifica por lo que dice, sin trasladar el juicio de un testigo a otro.

## 3. Medidas (una fila por carta, `results/canales/recepcion_medidas.csv`, derivadas mecánicamente de la tabla)

- `primera_atestacion_n1`, `_n2`, `_n3`: fecha (extremo tardío de la horquilla) de la primera atestación en cada nivel.
- `asimetria`: diferencia en años entre la primera atestación de nivel 3 en Oriente y en Occidente (positivo = Occidente
  más tardío).
- `estabilidad_atribucion`: `estable` (todas las atribuciones `Pablo`), `vacilante` (alguna `anonima` u `otro`),
  `negada` (alguna `negada`), `sin datos`.
- `papiro_mas_antiguo` y `posicion_P46`, `posicion_Marcion`, `posicion_Muratori`.

## 4. Lectura con § 2.2

- H1-H3: atestación temprana (nivel ≥ 2 antes de 150 y nivel 3 antes de 200 en los dos ámbitos), simétrica
  (asimetría ≤ 50 años) y atribución estable.
- H4: atestación tardía o desigual (nivel 3 después de 200 en algún ámbito, o asimetría > 50 años), entrada tardía en las
  colecciones (ausente de Marción o de 𝔓46 conservando el códice el lugar que le correspondería).
- H5: atestación tardía, asimétrica, atribución vacilante o ausente.
- Cuando la carta cumple parte de un patrón y parte de otro, el canal «no decide» entre las hipótesis afectadas.
Los umbrales (150, 200, 50 años) se fijan aquí, antes de codificar, y se aplican igual a las catorce cartas.

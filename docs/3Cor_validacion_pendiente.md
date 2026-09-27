# 3 Corintios (P. Bodmer X): normalización y decisiones filológicas

Estado: **validado el 27-IX-2026**. El autor delegó las doce decisiones de abajo («decide tú lo mejor con total
libertad»); se adoptó en todas la opción *borrador*, por el criterio de no corregir nunca en silencio el papiro y
de regularizar solo la ortografía. Ficheros definitivos: `data/local/3Cor.txt` (531 palabras; SHA-256
`04fd948567e980d1f94fd4656e964bea7da93cc299ba6a91ccaccba6934a3a42`, registrada en `data/provenance.json`) y
`data/local/3Cor_alineacion.tsv`. Véase D-007.

## Fuente y alcance

- Transcripción diplomática de P. Bodmer X, pp. 50-57, según el paquete depositado por el autor el 27-IX-2026
  (`3Cor_PBodmerX_Claude_package.zip`: texto electrónico que reproduce la edición de M. Testuz, *Papyrus Bodmer
  X-XII*, Cologny-Ginebra, 1959, pp. 30-44; SHA-256 de la transcripción
  `8ebec730f58ad6c07643ad399a15fcc8f2c905fefcbdad70323b081d2f5c7d46`).
- Alcance: **solo la respuesta de Pablo** (pp. 51-57, desde «Παῦλος ὁ δέσμιος»), sin la carta de los corintios y
  sin el título escribal «ΠΑΥΛΟΣ ΚΟΡΙΝΘΕΙΟΙΣ ΠΕΡΕΙ ΣΑΡΚΟΣ». Resultado: **531 palabras**, la cifra del laboratorio
  original.

## Reglas aplicadas (registradas una a una en la alineación)

| tipo de intervención | n.º |
|---|---|
| minúsculas y acentuación (sin cambio de letras) | 396 |
| ortografía del copista regularizada a la norma de las demás fuentes (itacismos ΕΙ/Ι, Ε/ΑΙ, Ο/Υ, ΟΙ/Υ; ΜΣ→ΜΨ; ΝΦ→ΜΦ) y acentuación | 45 |
| expansión de *nomina sacra* (ΧΡΣ, ΙΗΣ, ΚΣ, ΘΣ, ΠΝΑ, ΠΡΣ, ΑΝΠΣ, ΙΣΡΛ, ΔΑΥΙΔ…) | 37 |
| unión de palabras partidas por cambio de línea en la transcripción | 31 |
| resegmentación (ΤΗΝΕΛ ΕΥΣΙ → τὴν ἔλευσιν) | 1 |
| restitución editorial de letras entre corchetes o ángulos (Testuz) | 18 |
| supresión: letra tachada por el copista ([[Ο]]) y palabra incompleta en laguna (ΠΡΟΟΔΥΠΟΡ[…]Μ) | 2 |
| formas corruptas conservadas sin corregir, pendientes | 3 |

Los signos de puntuación del copista (¦), los números de línea de la presentación electrónica (10, 20) y los
encabezados de página no son palabras y no cuentan.

## Decisiones (todas resueltas con la opción «borrador»)

| n.º | lugar | lectura del papiro | borrador | alternativa | comentario |
|---|---|---|---|---|---|
| 1 | p. 51 | título «ΠΑΥΛΟΣ ΚΟΡΙΝΘΕΙΟΙΣ ΠΕΡΕΙ ΣΑΡΚΟΣ» | excluido | incluirlo | es rúbrica escribal, no texto de la carta |
| 2 | p. 53 | ΤΥΠΟΝ Ε̣Ν̣ Τ̣Υ̣Π̣Ο̣Ν̣ (segundo grupo con puntos de lectura insegura) | τύπον ἐν τύπον (conservado) | suprimir «ἐν τύπον» como ditografía | la transcripción marca insegura la repetición |
| 3 | p. 53 | ΘΕΛΩΝ ΕΙΝΑΙ ΖΕΙΕΧΕΙΡΙΖΕΤΟ | ζειεχειριζετο (sin acento, corrupta) | διεχειρίζετο (Δ→Ζ, ΕΙ→Ι) | además, parece faltar en la transcripción electrónica el sujeto «ὁ ἄρχων ἄδικος ὢν θεός» que las versiones dan antes de «θέλων εἶναι»: **cotejar con Testuz** |
| 4 | p. 54 | ΝΙΚΗΘΕΙΣ ΕΛΕΓ’ΧΘΗΤΟ ΜΗ ΩΝ ΘΣ | ἐλεγχθητο (sin acento, corrupta) | ἐλεγχθῇ τὸ / ἐλεγχθήτω | forma no atestiguada tal cual |
| 5 | p. 55 | ΕΝ ΣΩ ΜΑ ΚΑΙ ΗΜΦΙΕΣΜΕΝΑ | ἔνσωμα (una palabra: «corpóreos y vestidos») | ἐν σῶμα | lectura propia; comprobar con Testuz |
| 6 | p. 55 | ΣΥΝΦΘΑΡΕΝΤΑ | συμφθαρέντα | συνφθαρέντα | asimilación ortográfica, como hacen las ediciones críticas del NT |
| 7 | p. 55 | ΗΥΛΟΓΗΜΕΝΟΝ | εὐλογημένον | ηὐλογημένον | el aumento en el participio de perfecto es grafía del copista |
| 8 | p. 56 | ΟΥΤΕ ΕΡΞ· ΟΥΤΕ ΒΛΕΦΑΡΟΝ | ερξ (sin acento, corrupta) | θρίξ | «ni un cabello ni una pestaña»; la transcripción trae un signo tras ΕΡΞ |
| 9 | p. 56 | ΕΞΕΓΕΙΡΕΙ | ἐξεγείρει (presente, como está escrito) | ἐξεγερεῖ (futuro) | ΕΙ por Ε no es itacismo corriente; se conserva |
| 10 | p. 57 | ΤΕΚΝΗΜΑΤΑ ΕΧΕΙΔΝΩΝ | τεκνήματα (conservado) | γεννήματα | «engendros de víboras»; τέκνημα es forma rara; se conserva la del papiro |
| 11 | p. 57 | ..... ΟΥ]ΤΩΣ ΠΡΟΟΔΥΠΟΡ[ ]Μ Α]ΘΕΩΝ | οὕτως … ἀθέων (la palabra incompleta se omite) | omitir también οὕτως y ἀθέων por estar en laguna | restituciones de una o dos letras se admiten; palabras incompletas no |
| 12 | general | restituciones de Testuz de una a tres letras (Ε]Ι, Τ]ΩΝ, ΟΙ]ΔΑΤΕ, ΙΝΑ], ΤΟΣ], Κ]ΑΙ, Α]ΔΟΥ, ΚΕΡΔΗΣ[Ω, ΑΝ[ΑΣ, ΕΥΑΓΓΕΛΕΙ[ΟΥ, ΠΥ<Ρ>, ΤΡΙ<Σ>, ΥΙ<Ω>, ΕΧΟΥΣ<Ι>, ΑΜΑΡΤΙ<Ω>, Τ<Η>, ΗΜ<Ω>, ΕΥΣ<Ι>, ΠΟΙΕΙ<Σ>ΘΑΙ, ΑΠ[[Α<Ο>]]) | admitidas | excluir las palabras afectadas | criterio: la palabra está segura aunque falte una letra |

Comprobación adicional del 27-IX-2026: la transcripción electrónica de dhspriory.org, leída de nuevo, coincide letra
por letra con el paquete del autor en los seis lugares dudosos (decisiones 2, 3, 4, 5, 8 y 10) y no trae aparato; por
tanto no hay base documental accesible para emendar, y se conserva la lectura del papiro. La lectura ἔνσωμα
(decisión 5) la apoya la versión latina de 3 Cor 3, 26 (*corporata et vestita*).

## Reserva preregistrada

La ortografía regularizada del copista introduce una incertidumbre propia de este documento que no afecta a
ningún otro; por eso 3 Corintios actúa solo como control de falsificación y negativo, y nunca como argumento a
favor ni en contra de una carta concreta (regla `tres_corintios`, D-006).

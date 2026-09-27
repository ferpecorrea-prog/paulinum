# Inventario de fuentes y de accesibilidad de red — sesión 0 (2026-09-27)

Comprobación hecha desde los dos entornos de trabajo (portátil del investigador, dentro del espacio de trabajo
de Cowork, y réplica en la nube). La red de ambos pasa por una lista de dominios permitidos: solo son
alcanzables por programa **GitHub** (github.com, api.github.com, raw.githubusercontent.com) y **PyPI**. Todo lo
demás (Zenodo, OSF, ORCID, NTVMR, Codex Sinaiticus, papyri.info, PHI, LGPN, Trismegistos, Biblindex, Harland,
Scaife, TLG, Hugging Face, figshare, CCEL, Wikisource) **no es alcanzable por programa**; sí puede leerse página a
página con el navegador (lectura, no descarga masiva), y los ficheros que haga falta descargar los deposita el
autor en `nuevo_paulinum/`.

## 1. Corpus griegos accesibles por programa (GitHub)

| fuente | repositorio | uso | estado |
|---|---|---|---|
| MorphGNT / SBLGNT 6.12 | github.com/morphgnt/sblgnt | texto principal del NT, lemas y morfología | alcanzable |
| PROIEL (Tischendorf) | github.com/proiel/proiel-treebank | segunda edición del NT; sintaxis de dependencias | alcanzable |
| MACULA Greek (SBLGNT, Nestle 1904) | github.com/Clear-Bible/macula-greek | tercera edición del NT | alcanzable |
| Open Apostolic Fathers (Lake) | github.com/jtauber/apostolic-fathers | Ignacio, Policarpo, 1-2 Clemente, Bernabé, Didajé, Hermas, Diogneto, Martirio de Policarpo | alcanzable |
| Perseus canonical-greekLit | github.com/PerseusDL/canonical-greekLit | 100 autores, 1.596 ficheros de obra | alcanzable |
| First1KGreek (Open Greek and Latin) | github.com/OpenGreekAndLatin/First1KGreek | 303 autores, 1.160 ficheros de obra | alcanzable |
| papyri.info (idp.data: DDbDP, HGV, APIS, DCLP) | github.com/papyri/idp.data | textos y metadatos de papiros documentales (canal onomástico) | alcanzable |
| GLAUx (Keersmaekers) | github.com/alekkeersmaekers/glaux | corpus anotado automáticamente (lemas, morfología, dependencias) | alcanzable; contenido y licencia por comprobar en la sesión 1 |
| greCy / OdyCy, dilemma | github.com/jmyerston/greCy; github.com/open-greek/dilemma | lematización y análisis morfosintáctico uniformes | instalables desde GitHub/PyPI (los modelos de Stanza en Hugging Face **no** son alcanzables) |

## 2. Epistolografía de autores seguros en formato abierto (hallazgos de esta sesión)

Recuento de tokens griegos aproximado sobre el fichero TEI, sin cabecera.

| autor / colección | identificador | edición | unidades | tokens | uso previsto |
|---|---|---|---|---|---|
| **Libanio, Epistulae 1-839** | First1KGreek tlg2200.tlg001 | Foerster (Teubner, reimpr. 1963) | 839 cartas | ~158.700 | envolvente intra-autor de cartas breves (la campaña 03 usó 44); controles de género con las 64 *Orationes* y 9 *Declamationes* del mismo autor |
| **Basilio de Cesarea, Epistulae** | Perseus tlg2040.tlg004 | Deferrari (Loeb) | 368 cartas | ~139.400 | envolvente **epistolar cristiana** de autor seguro; pares carta a individuo / carta a comunidad; estados: las cartas tenidas por espurias o ajenas (correspondencia con Libanio, cartas de Evagrio, Gregorio de Nisa…) se auditan una a una antes de sellar |
| Juliano, Epistolae | Perseus tlg2003.tlg013 | Wright (Loeb) | 83 | ~27.400 | ya usado; se mantiene con la partición genuinas/apócrifas de Wright |
| Isócrates, cartas 1-9 y discursos | Perseus tlg0010.tlg022-030 (+ tlg001-021) | Norlin / Van Hook (Loeb) | 9 cartas + 21 discursos | — | ya usado; control de género dentro de un mismo autor |
| Alcifrón, Epistulae (4 libros) | First1KGreek tlg0640.tlg001 | Schepers (Teubner 1905) | 4 libros | ~31.200 | cartas **ficticias** del s. II: control de género epistolar no auténtico |
| Filóstrato, Epistulae et dialexeis | Perseus tlg0638.tlg006 | Kayser (Teubner 1871) | — | ~7.600 | ya usado (Filóstrato, una obra) |
| Eliano, Epistulae rusticae | Perseus tlg0545.tlg003 | Hercher (Teubner 1866) | 20 | pequeño | cartas ficticias; control de género |
| Cartas pseudoepigráficas (Hercher): Fálaris, Quión, Bruto, Sócrates y socráticos, Diógenes, Crates, Anacarsis, Eurípides, Solón, Temístocles, Antígono, Antíoco, Artajerjes, Mitrídates, Nicias | First1KGreek tlg0053, 0041, 1803, 0636, 0637, 1325, 0623, 0037, 1367, 1681, 0055, 0618, 0044, 0045, 0039, 0046 | Hercher (1873) | colecciones | — | **falsificaciones antiguas reconocidas**, del género epistolar: controles negativos y de falsificación |
| Orígenes, Epistula ad Africanum; De oratione; Exhortatio ad martyrium; Contra Celsum | First1KGreek tlg2042 | varias | — | — | ya usado; una carta auténtica de autor seguro del s. III |
| Ignacio (7 genuinas; recensión larga) | First1KGreek tlg1443.tlg001-002 | Lightfoot/Funk | 7 + 13 | — | ya usado; Ignacio a Policarpo frente a Ignacio a las iglesias = control de destinatario individual |
| Clemente Romano: 1 Clem, 2 Clem, cartas pseudoclementinas, Epistulae de virginitate [Sp.] | First1KGreek tlg1271 | — | — | — | ya usado; se añaden las *De virginitate* como pseudoepigrafía epistolar |
| Plotino (Enéadas, ed. Porfirio) y Porfirio (obras propias) | First1KGreek tlg2000, tlg2034 | — | — | — | segundo caso de composición mediada (obra editada por otro), junto a Epicteto/Arriano |

Ausentes en formato abierto (por ahora): Sinesio, Gregorio de Nacianzo (cartas), Juan Crisóstomo, Isidoro de
Pelusio, Teodoreto (cartas), Procopio de Gaza. Si el autor localiza ediciones de dominio público digitalizadas de
calidad, se evaluarán; no se hará OCR de griego politónico, porque su ruido contamina precisamente los rasgos
de caracteres.

## 3. Testigos manuscritos y ediciones

| recurso | acceso | acción |
|---|---|---|
| NA28 (2012), ejemplar en PDF del autor | local (`10_fuentes/biblia/`) | extracción del texto para control de ruido de edición; apéndice *Loci citati vel allegati* para la máscara de citas del AT de Hebreos (D-004) |
| Codex Sinaiticus, transcripción XML completa (v. 1.04, 4,4 MB) | codexsinaiticus.org, CC BY-NC-SA 3.0 | **descarga por el autor** a `nuevo_paulinum/`; uso local, sin redistribución; medida directa sobre testigo |
| 𝔓46 (Chester Beatty II / P.Mich. inv. 6238), transcripción INTF/NTVMR | ntvmr.uni-muenster.de (docID 10046) | lectura posible por navegador; **descarga de la transcripción por el autor** si el sitio la ofrece; en su defecto, transcripción por página con el navegador |

## 4. Bases prosopográficas, epigráficas y de recepción

| recurso | acceso | plan |
|---|---|---|
| papyri.info (DDbDP/HGV) | GitHub (idp.data) | consulta local de nombres en papiros documentales fechados |
| LGPN | solo navegador | consultas por nombre desde el navegador, con registro de cada consulta (fecha, URL, resultado) |
| PHI Greek Inscriptions | solo navegador | ídem |
| Trismegistos People | solo navegador | ídem |
| Biblindex (citas patrísticas) | solo navegador (alta) | matriz de primeras atestaciones, carta por carta, con registro de consultas |
| Harland, *Greco-Roman Associations* (AGRW) | solo navegador; sin descarga | inscripciones de asociaciones con cargos, fechadas; se registran una a una |

## 5. Herramientas

- Python 3.10 (portátil) / 3.11 (nube y CI). Bibliotecas fijadas en `requirements.txt`.
- Análisis morfosintáctico uniforme: candidatos greCy/OdyCy (spaCy) y dilemma; la elección y su validación sobre
  el NT (contra MorphGNT, que tiene anotación manual) se hacen en la sesión 1 antes de sellar.
- Cálculo pesado: réplica en la nube (2 núcleos, 7 GB), por etapas reanudables; resultados enviados a GitHub al
  cerrar cada etapa. Portátil: 2 núcleos, 3 GB, para verificación y para las pruebas de referencia.

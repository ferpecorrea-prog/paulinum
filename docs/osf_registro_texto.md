# Texto para el registro en OSF del protocolo paulinum 1.0

Este archivo contiene, campo por campo, el texto que el autor copia en persona en el formulario de registro de OSF
(https://osf.io → *Registrations* → *New registration* → plantilla **Open-Ended Registration**, la más sencilla, o
**OSF Preregistration** si se prefiere la plantilla larga; en ese caso los campos de más se rellenan con «véase el
protocolo con DOI»). El registro no sustituye a los sellos de Zenodo (que son los que fijan fecha y contenido): añade un
segundo depósito independiente y una ficha legible. Cuando esté hecho, se anota el enlace `osf.io/xxxxx` en
`protocols/paulinum_1_0/REGISTRO.md` (línea «Registro en OSF») y en `README.md`.

**Importante:** el registro debe apuntar al **Sello 1** (protocolo preregistrado, `protocolo-1.0.0`, DOI
10.5281/zenodo.22993122), no al Sello 2 ni a los resultados. Es un registro *a posteriori* de un protocolo ya sellado
públicamente el mismo día (27-IX-2026); así se dice en el texto, sin ocultarlo.

---

## Campo «Title» (título)

paulinum 1.0 — Protocolo preregistrado de verificación convergente de la autoría de las catorce cartas de la tradición paulina

## Campo «Description» / «Summary» (resumen)

Protocolo preregistrado de una investigación de **verificación de autoría** (no de atribución) sobre las catorce cartas de
la tradición paulina del Nuevo Testamento: las trece que llevan el nombre de Pablo y la Epístola a los Hebreos, tratada
como decimocuarta diana con el mismo procedimiento y sin hipótesis previa. El protocolo fija, antes de calcular ningún
resultado sobre las cartas: las hipótesis de composición por carta (H1 autógrafa o dictada; H2 composición mediada por
secretario; H3 colaboración del círculo; H4 escuela póstuma; H5 composición ajena al círculo) y sus predicciones
observables por canal; tres hipótesis sobre el método (Hm1-Hm3); el corpus de control (857 documentos griegos, 2,79
millones de palabras, con autores de autoría segura, pseudoepigrafías reconocidas y colecciones epistolares de Basilio y
Libanio como envolvente epistolar); la preparación de los textos (normalización, cuatro máscaras por referencia, lematización
uniforme); la rejilla principal de 16 especificaciones (4 espacios de rasgos × 2 distancias × 2 máscaras) con 300
iteraciones; tres familias de métodos calibradas con los mismos problemas de respuesta conocida (impostores generales,
distancia de compresión normalizada, modelo Dirichlet-multinomial jerárquico); la calibración epistolar como principal
(razón de verosimilitud por densidades KDE); las envolventes intra-autor, inter-autor y de saltos de género con una regla
de equivalencia («mismo rasero» para las catorce cartas: dentro / fuera / indeterminado); un veredicto mecánico en cuatro
niveles (posibilidad, plausibilidad, superioridad comparativa, robustez) calculado por un guion sellado; el protocolo de
codificación de tres canales no estilométricos (recepción y transmisión, onomástica y prosopografía, canal institucional)
y la regla de convergencia; las condiciones de falsación del método y de la hipótesis de partida del autor; y el orden de
ejecución con tres sellos públicos (protocolo, código congelado, resultados), cada uno como *release* de GitHub
archivada en Zenodo con DOI.

El punto de partida declarado del autor es que las trece cartas con nombre de Pablo proceden de Pablo al menos
intelectualmente (H1-H3); por eso el protocolo fija con especial cuidado las condiciones en las que esa hipótesis quedaría
refutada o debilitada para cada carta. No se asigna ningún «grado» de autenticidad; los resultados adversos se informan sin
ajustar parámetros. La lectura no es ciega en sentido estricto (las extensiones de las cartas las identifican); la
protección es triple y verificable: reglas escritas y selladas antes, veredicto calculado por código sellado, y orden de
etapas registrado en el historial público de git (calibración y envolventes publicadas antes de calcular ninguna fila de
diana).

Documento registrado: el protocolo sellado (Sello 1, etiqueta `protocolo-1.0.0`, huella SHA-256 del conjunto
9b65c9d823691887279abb93522a8dbd1479ec7b08fef411dc099bf083edbfe4), archivado en Zenodo el 27 de septiembre de 2026 con DOI
10.5281/zenodo.22993122 (DOI de concepto de todas las versiones: 10.5281/zenodo.22993121). Este registro en OSF se hace
después de ese depósito y remite a él; cualquier desviación posterior consta como enmienda numerada en el registro
público del protocolo (`protocols/paulinum_1_0/REGISTRO.md`) antes de ejecutarse.

Repositorio público con protocolo, código, metadatos, bitácoras y resultados: https://github.com/ferpecorrea-prog/paulinum
(código MIT; datos e informes CC BY 4.0; los textos de terceros no se redistribuyen: se publican manifiesto, huellas y
código de descarga). Idioma: español.

## Campo «Contributors» (autoría)

Jesús Fernández-Pedrera Correa, ORCID 0009-0000-7024-5028, investigador independiente (Barcelona).

## Campo «Category»

Project (o «Methods and Measures», si se pide una categoría de contenido).

## Campo «License»

CC-BY 4.0 (texto del protocolo e informes); el código del repositorio es MIT.

## Campo «Subjects» / «Tags» (etiquetas)

autoría; estilometría; verificación de autoría; corpus paulino; Nuevo Testamento; griego antiguo; Epístola a los Hebreos;
preregistro; reproducibilidad; humanidades digitales; filología; método de impostores; distancia de compresión;
Dirichlet-multinomial

## Campo «Data availability» / enlaces

- Protocolo sellado (Sello 1): https://doi.org/10.5281/zenodo.22993122
- Código congelado (Sello 2, `paulinum-1.0.0`): https://doi.org/10.5281/zenodo.22996786
- Todas las versiones: https://doi.org/10.5281/zenodo.22993121
- Repositorio: https://github.com/ferpecorrea-prog/paulinum
- Registro público de enmiendas: https://github.com/ferpecorrea-prog/paulinum/blob/main/protocols/paulinum_1_0/REGISTRO.md

## Campo «Embargo»

Sin embargo: registro público inmediato.

## Preguntas de la plantilla larga («OSF Preregistration»), por si se elige

- *Hypotheses*: § 2 del protocolo (H1-H5 por carta; Hm1-Hm3 sobre el método; Hebreos sin hipótesis previa, § 2.4).
- *Study type*: análisis de datos existentes (textos griegos editados, de libre acceso) con protocolo fijado antes del
  análisis; sin participantes humanos.
- *Blinding*: no hay cegado en sentido estricto; protección por reglas selladas, veredicto mecánico y orden registrado
  (§ 3.3; decisión D-009).
- *Sampling plan / Data collection*: corpus fijado en el manifiesto antes del sello (§ 4; nada se añade después);
  857 documentos.
- *Variables*: rasgos y distancias de § 6; variables de situación de § 7.5.
- *Analysis plan*: § 6-8 (rejilla, familias, calibración, envolventes, veredicto mecánico); § 9 (canales no
  estilométricos y convergencia).
- *Inference criteria*: § 7.2 (escala verbal de la razón de verosimilitud), § 7.3 (regla de equivalencia), § 8 (reglas
  por nivel), § 9.4 (convergencia), § 10 (falsación).
- *Data exclusion*: § 4.3-4.4 (estados `disputed` fuera de la calibración; umbrales de extensión).
- *Missing data*: documentos que no se descargan o no alcanzan el umbral se pierden y se anotan (§ 4.1).
- *Exploratory analysis*: ventanas deslizantes (§ 7.6) y bloques de sensibilidad (§ 6.2) se informan y nunca deciden.

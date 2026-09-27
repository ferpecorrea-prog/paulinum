# LEEME PRIMERO — Nota de procedencia y estado de esta carpeta

**paulinum_lab** es el laboratorio de reproducibilidad de las dos investigaciones sobre la autoría del
corpus paulino canónico publicadas por el autor en *¿Quién escribió las cartas de san Pablo?*
(tomo I, «Investigación 1») y en su Parte II, «La verificación convergente: una investigación
estilométrica con controles» («Investigación 2», software *paulinum*).

## Qué ocurrió con el material original

El laboratorio original (`paulinum_lab`, con el código *paulinum* 0.1.0, los metadatos, las
configuraciones, los resultados de las campañas 01, 02 y 03, los informes y las bitácoras) se
ejecutó entre el 8 y el 10 de septiembre de 2026 en el ordenador del investigador y en una réplica
en la nube. **Tras la publicación, la carpeta fue borrada por error del ordenador del investigador
y la réplica en la nube era efímera.** No quedó copia de ningún archivo del laboratorio original.

## Qué es esta carpeta

Una **reconstrucción** del laboratorio a partir de la especificación publicada, hecha el 25 de
septiembre de 2026:

1. **El código es una reimplementación**, módulo a módulo, de lo que describe el Apéndice
   técnico (A.1) y los capítulos 7-9 de la Parte II: los mismos quince módulos, los mismos
   guiones auxiliares, las mismas órdenes, los mismos parámetros y las mismas reglas
   preregistradas. No es el código original; se identifica como **paulinum 0.2.0-r**
   («r» de reconstrucción). Las decisiones de diseño que el libro no fija (por ejemplo, qué cinco
   opúsculos de Luciano formaban el corpus) están marcadas con `reconstruido=True` en
   `paulinum/sources.py` y explicadas en `docs/ESPECIFICACION_RECONSTRUIDA.md`.

2. **Los sellos SHA-256 publicados en el libro** (`4eb0a436…` para la campaña 01,
   `33e7b61b…` para la campaña 03, y los cinco de la campaña 02) **corresponden al código
   original perdido y no pueden reproducirse**. Se conservan en
   `results_publicados/sellos_publicados.csv` como dato histórico. La reconstrucción lleva sus
   propios sellos, calculados con el mismo procedimiento (`python -m paulinum seal --config <configuración> --run <campaña>`), que son los
   que hay que citar al verificar esta carpeta.

3. **Los resultados publicados** (todas las tablas del Apéndice A.4 y de la Investigación 1) están
   transcritos como CSV en `results_publicados/`, y los dos informes íntegros (Anexos I y II del
   libro) en `informes/`. Son los **datos de referencia** contra los que comparar cualquier
   réplica.

4. **Verificación de fidelidad realizada**:
   - La capa de trece lemas de la Investigación 1 (matriz 19 × 13 publicada en la nota 43) se
     reproduce **dígito a dígito**: 313 de 313 valores impresos en el libro coinciden
     (`investigacion_1/capa_13_lemas/COTEJO_CON_EL_LIBRO.md`).
   - Los recuentos de tokens del corpus reconstruido coinciden con el inventario publicado en las
     trece cartas paulinas (7.055, 6.812, 4.473, 2.226, 1.626, 1.473, 334, 2.416, 1.580, 820,
     1.591, 1.235, 659), en el núcleo (23.999), en las dianas (8.301) y en los Padres Apostólicos
     (Hermas 27.337, Ignacio 7.746, Policarpo 1.131, etc.); MorphGNT aporta 137.554 tokens y PROIEL
     132.356, las cifras del libro.
   - La máscara de pasajes paralelos (`metadata/reuse_ranges.csv`) es la publicada; el guion
     `scripts/detectar_reutilizacion.py` la reproduce en 18 de los 20 tramos y explica la
     diferencia de una palabra en los dos restantes.
   - Las magnitudes deterministas o poco sensibles al azar (distancias medias al núcleo, R² de la
     PERMANOVA dentro de Pablo con 76 ventanas, densidad de modificadores adjetivales en PROIEL,
     réplica de la capa de 13 lemas sobre MorphGNT) reproducen las publicadas en el orden y en la
     primera o segunda cifra decimal (por ejemplo, Col 2,318 frente a 2,32 publicado; Flm 2,16 frente
     a 2,06; correlación de rangos con Perseus 0,991 frente a 0,99).
   - Las magnitudes basadas en muestreo aleatorio (puntuaciones GI, razones de verosimilitud,
     percentiles bootstrap) se reproducen en sus conclusiones y en su orden de magnitud, **no en
     el tercer decimal**: el generador aleatorio y el orden de los problemas no son los del
     original.

5. **Lo que no se ha podido reconstruir** (y se declara):
   - El texto griego preparado de *3 Corintios* (`data/local/3Cor.txt`, 531 palabras, con su
     archivo de alineación de 105 intervenciones): hay que rehacerlo a partir de la transcripción
     de Testuz siguiendo `data/local/LEEME_3Cor.md`. Sin él, la cadena funciona igual (el
     documento se omite con aviso) y el control de falsificación 3 Cor no se calcula.
   - `Diorisis.zip` (Vatri y McGillivray, CC BY-NC-SA 4.0, ~800 MB) no se redistribuye; hay que
     descargarlo y pasar su ruta a `scripts/construir_lexicon.py`. Sin él, el lexicón se construye
     con MorphGNT y PROIEL (cobertura menor en los controles).
   - Los 117 testimonios de la validación externa P10-R(sym-ext) de la Investigación 1, validados
     a mano por el autor, y los censos histórico-filológicos (P12) no son reconstruibles desde el
     código: solo constan sus resultados agregados.
   - `docs/bibliografia_verificada.md` del laboratorio original: sus entradas están en la
     bibliografía de la Parte II (`docs/bibliografia_parte_II.md`), pero la correspondencia clave
     → entrada (A-n, B-n, E-n, F-n) no se ha reconstruido.
   - El manifiesto exacto de los 408 documentos de la campaña 03: se ha reconstruido por autor y
     obra a partir del inventario publicado y de las rutas reales de Perseus y First1KGreek; el
     número de documentos por autor puede diferir en algunas unidades.

## Cómo citar esta carpeta

Como «reconstrucción del laboratorio *paulinum* a partir de la especificación publicada
(paulinum 0.2.0-r, 25-IX-2026)», nunca como el laboratorio original. El sello de la
reconstrucción figura en `results/PROTOCOLO_SELLADO_<campaña>.json` tras ejecutar
`python -m paulinum seal --config <configuración> --run <campaña>`.

# Estado del proyecto paulinum 1.0 — 29 de septiembre de 2026 (cierre del bloque 5, Sello 3)

Documento de traspaso entre sesiones de trabajo. Lo escribe la sesión que cerró el bloque 5 (campaña principal y
Sello 3) para que la siguiente (un chat nuevo, sin memoria de este) continúe sin perder nada. Sustituye a
`ESTADO_DEL_PROYECTO_2026-09-27.md`, que se conserva como historia. Todo lo que aquí se dice está también, con más
detalle, en los archivos que se citan; este documento es el índice y el orden de lectura.

## 0. Orden de lectura para una sesión nueva

1. Este documento entero.
2. `results/paulinum_1_0/veredicto.md` (la tabla mecánica de las catorce cartas) y la sesión 5 de
   `docs/registro_investigacion.md` (comprobaciones de falsación y reservas).
3. `protocols/paulinum_1_0/PROTOCOLO.md` (sellado, no se toca; § 8 veredicto, § 9 canales no estilométricos, § 10
   falsación) y `protocols/paulinum_1_0/REGISTRO.md` (tres sellos, DOI, enmiendas 1-5).
4. `docs/decisiones.md` (D-001 a D-026) y `docs/laboratorio_actions.md` (cómo se ejecutó la campaña).
5. `CHANGELOG.md` (sección `resultados-1.0.0`), `README.md`.
6. Solo si hace falta el detalle: `docs/testigos_manuscritos.md`, `docs/osf_registro_texto.md`,
   `docs/inventario_fuentes_sesion0.md`, `ESTADO_DEL_PROYECTO_2026-09-27.md`.

## 1. Instrucciones permanentes del autor (Jesús Fernández-Pedrera Correa)

- Se trabaja **por bloques**. Al final de cada bloque: informe breve de lo hecho, indicación del **nivel de esfuerzo**
  del bloque siguiente y la frase «diga *sigue*»; el autor responde «sigue». Cada bloque termina con *commit* y *push*.
- **Autonomía total** sobre la infraestructura científica (GitHub, Zenodo, OSF): no hace falta pedir autorización para
  cada *commit*, etiqueta o *release*.
- **Restricción absoluta:** nunca se suben a GitHub, Zenodo ni a ningún repositorio público tokens, contraseñas, claves
  API, secretos u otras credenciales. `github_token.txt` (en `nuevo_paulinum/`, fuera del repositorio) permanece
  exclusivamente en local y no se añade, copia ni publica. **El token no se pega nunca en el chat** ni se imprime en
  ninguna salida.
- **Hebreos** es la decimocuarta diana, con el mismo rasero que las trece y **sin hipótesis previa**.
- **Ninguna calificación provisional** en el Tomo V antes de tener los resultados; los **títulos** de los tomos se
  deciden al final.
- Idioma de todo el material: español; nombre de autor en citas: «Jesús Fernández-Pedrera Correa»; ORCID
  0009-0000-7024-5028; usuario de GitHub `ferpecorrea-prog`.

## 2. Dónde está cada cosa

| qué | dónde |
|---|---|
| Repositorio público | https://github.com/ferpecorrea-prog/paulinum (rama `main`; CI `selftest` verde) |
| Copia canónica (portátil del autor, Windows) | `C:\Users\ferpe\Desktop\Correccion_Fondo\nuevo_paulinum\paulinum` — en la sesión de Cowork, `$HOME/mnt/Correccion_Fondo/nuevo_paulinum/paulinum` |
| Token de GitHub (solo local; permisos `contents`, `actions: write`) | `C:\Users\ferpe\Desktop\Correccion_Fondo\nuevo_paulinum\github_token.txt` |
| Diorisis.zip (CC BY-NC-SA, no redistribuible; SHA-256 `fb32b7ff4bcfc433f1234aff8134096f524c9a32accbfdf0a072df4a5f019b65`) | `nuevo_paulinum\Diorisis.zip` |
| Lexicón uniforme (no versionado; SHA-256 `b0ea6312655cbe8fdd5f92337089a7b9e5f961d7f2d5aa1b6e67bf25440c4ea7`) | portátil: `paulinum\data\cache\lexicon_uniforme.tsv` |
| Testigos manuscritos (XML brutos, manifiesto original, derivados con texto; no versionados) | portátil: `paulinum\data\local\testigos\` |
| NA28 del autor (escaneo sin capa de texto; uso local, solo máscaras) | `Correccion_Fondo\10_fuentes\biblia\Nestle-Aland-Novum-Testamentum-Graece-28-PDF.pdf` (página PDF = página impresa + 125) |
| Tomos del libro (versiones finales actuales) | `Correccion_Fondo\07_finales\Pablo de Tarso 4_TomoIV_quien_escribio_las_cartas_corregido.docx`, `…5_TomoV_cartas_bajo_prueba_I_corregido.docx`, `…6_TomoVI_cartas_bajo_prueba_II.docx` |
| Dictamen e índice propuesto de los Tomos IV-VI nuevos | `Correccion_Fondo\08_informes\dictamen_reestructuracion_tomos_IV_V_VI.md`, `…\indice_propuesto_tomos_IV_V_VI.md` |
| Reglas de corrección de fondo del autor | `Correccion_Fondo\00_biblia_correccion.md` (§ 15.2 lleva el estado de los Tomos IV y V) |
| Artefacto de Actions recuperado a mano por el autor | `nuevo_paulinum\results-36323226094.zip` (ya integrado; puede ir a `_to_delete\`) |
| Parches ya aplicados y archivo antiguo | `nuevo_paulinum\_to_delete\` (borrar cuando el autor quiera); `Correccion_Fondo\paulinum_lab\` **pendiente de mover a `_to_delete\`** cuando el autor lo diga |

La réplica en la nube de la sesión (contenedor Linux, 2 núcleos, 8 GB con límite de 6,27 GB para los procesos) **no
persiste entre chats**: una sesión nueva clona el repositorio, ejecuta `python -m paulinum fetch --tier 4 --editions`
y `python -m paulinum build --config config/paulinum_1_0.yaml`, y trae del portátil el lexicón (comprobar la huella) y,
si hace falta el bloque `testigos`, los derivados de `data/local/testigos/` y las ediciones `corpus_{sinaiticus,
sblgnt_rec_sinaiticus,p46,sblgnt_rec_p46}.jsonl`.

## 3. Estado del protocolo: los tres sellos están puestos

| sello | etiqueta | huella | DOI | fecha |
|---|---|---|---|---|
| 1. Protocolo preregistrado | `protocolo-1.0.0` | `9b65c9d8…dbfe4` (34 archivos, sin lexicón) | 10.5281/zenodo.22993122 | 2026-09-27 |
| 2. Código congelado | `paulinum-1.0.0` (versión 1.0.0) | `cd32dad6…29ef` (50 archivos, con lexicón) | 10.5281/zenodo.22996786 | 2026-09-27 |
| 3. Resultados | `resultados-1.0.0` | `980b3ab28e85caa7f2bf94dc24b8e6977a191bff7249fb6c21db11407a44c1b3` (765 archivos versionados de `results/`; `SELLO_resultados-1.0.0.json`; `python herramientas/sellar_resultados.py --comprobar …`) | 10.5281/zenodo.23034497 | 2026-09-29 |

DOI de concepto (todas las versiones): 10.5281/zenodo.22993121. Registro en OSF: https://osf.io/nphcu (público,
remite al Sello 1). Enmiendas registradas: 1-4 (sesiones 1-2) y 5 (run auxiliar sin dianas). Decisiones nuevas del
bloque 5: D-023 (OdyCy en lugar de greCy), D-024 (`pos3` descartado), D-025 (`closed:150` sin calcular en `ediciones`
sobre Tischendorf y Nestle 1904), D-026 (`herramientas/`: sello de resultados y comprobación de § 10.1). **El código
sellado no ha cambiado** (huella del Sello 2 comprobada el 29-IX); los dos defectos conocidos (guion de anotación,
D-024; inventario de clase cerrada dependiente del tagset de MorphGNT, D-025) y la ausencia de una etapa que escriba
la comprobación de las cartas breves (D-026) quedan para la versión posterior a la campaña (1.1.0), nunca dentro de ella.

## 4. Qué dice el veredicto mecánico (`results/paulinum_1_0/veredicto.md`; el libro lo reproduce y lo comenta, no lo corrige)

- Nivel 2 (plausibilidad): **«dentro»** del rango intra-autor en las catorce cartas, en min-max y en Delta.
- Nivel 3 (núcleo más próximo): **pasa** en doce; **indeterminado** (IC del margen incluye 0) en 2 Tim y Heb. Mejor
  otro autor: Ignacio en once cartas, Lucas (Hch) en Gal, 2 Tim y Heb.
- Nivel 1 (posibilidad, LR epistolar, mediana de las tres familias aptas): apoyo moderado a mismo autor en Rom, 1 Cor,
  2 Cor, Gal, Flp, 1 Tes, Ef, 2 Tes; débil en Col y 2 Tim; **discordante** (NCD en contra; impostores y Dirichlet a
  favor) en Flm, 1 Tim y Tit; **apoyo débil a otro autor** en Heb (impostores +0,13, NCD −0,62, Dirichlet −0,71).
- Nivel 4 (robustez, ocho bloques con `summary_by_letter.csv`): 8/8 en trece cartas; 5/8 en Heb (cambian de signo
  `coseno`, `documento_entero` y `rasgos`).
- Patrón § 8.5: «compatible con H1-H3; no con H5; H4 improbable» (nueve cartas); «familias discordantes: compatible con
  H2-H3; no con H5» (Flm, 1 Tim, Tit); «LR no discriminante: compatible con H1-H3; H5 improbable» (2 Tim);
  **Hebreos: «dentro del rango con LR en contra: discordancia entre niveles; se informa sin decidir»**.
- Ninguna carta cumple la condición de refutación de § 10.2. El segundo modelo (SVM, `modelo_svm_*.csv`) y las
  ventanas deslizantes (`rolling_scores.csv`) son lecturas complementarias, no entran en el veredicto.

Reservas registradas que acompañan a la lectura (sesión 5 del registro): límite de la familia A ante un imitador del
mismo registro (3 Corintios detectado solo en 6/16, `char3` y `closed`); Flm por debajo de 0,5 en las dos
especificaciones NCD (heterogeneidad del núcleo en la familia B, § 10.3); cartas breves de Libanio frente a la E global
(25 % en min-max; frente a su propia envolvente 1,2 %: el criterio de § 10.1 no se cumple); solapamiento B-E mayor en
Delta (menor potencia para declarar «fuera»); `closed:150` no calculado en `ediciones` (D-025); 𝔓46 no conserva
1 Tes (< 100 palabras), 2 Tes, 1-2 Tim, Tit ni Flm (dato del canal de transmisión).

## 5. Bloque 6: canales no estilométricos y convergencia (HECHO el 29-IX-2026) y montaje del libro (siguiente)

**Hecho (commits `cfd4d42` y siguientes):** enmienda 6 (un solo codificador), libros de códigos en `docs/canales/`,
recepción (`results/canales/recepcion*.csv`, D-027), onomástica (`onomastica_*.csv`, D-028, D-029), institucional
(`institucional*.csv`, D-030, consultas AGRW 172-191) y convergencia § 9.4 (`convergencia.csv`,
`convergencia_veredicto.csv`, D-031). Resumen: H1-H3 sostenidas en las trece; H5 descartada en las trece; H4
debilitada en nueve, descartada en Rom y Flp, abierta en Flm, sostenida en 1 Tim; hipótesis de partida no refutada en
nueve y abierta en Flm, 1 Tim, 2 Tim, Tit; Hebreos H1-H3 descartadas (recepción, onomástica), H4 y H5 sostenidas,
estilometría sin decidir. Detalle en `docs/canales/codigos_convergencia.md` § 4 y en `docs/registro_investigacion.md`
(Sesión 6). **Siguiente: montaje de los Tomos IV, V y VI** (punto 3). Esfuerzo: alto, sin cómputo.

**Bloque 7, primera entrega (29-IX-2026): Tomo IV montado.** Entregado en
`Correccion_Fondo\07_finales\Pablo de Tarso 4_TomoIV_historia_de_la_cuestion_2026-09-29.docx` (nombre nuevo; los
anteriores intocados), con informe en `08_informes\informe_montaje_tomo_IV_2026-09-29.md` y fuentes markdown,
guiones (`ensamblar.py`, `build_tomoIV.py`) y registro de verificaciones en `09_recursos\montaje_tomoIV_2026-09-29.zip`.
Catorce capítulos en cinco Partes, introducción general a los tres tomos y conclusión; 44.100 palabras de cuerpo,
174 notas (ninguna >130 palabras), 161 entradas bibliográficas, sin índice ni apéndices; título de cubierta
provisional. Las remisiones al Tomo V siguen la numeración del índice aprobado y se comprobarán al montarlo.
**Siguiente: Tomo V**, después Tomo VI.

**Bloque 7, segunda entrega (29-IX-2026): Tomo V montado.** Entregado en
`Correccion_Fondo\07_finales\Pablo de Tarso 5_TomoV_el_debate_actual_2026-09-29.docx`, con informe en
`08_informes\informe_montaje_tomo_V_2026-09-29.md`; fuentes y guiones de los dos tomos en
`09_recursos\montaje_tomosIV-V_2026-09-29.zip`. Cuatro Partes, doce capítulos, introducción y epílogo; 56.400 palabras
de cuerpo, 96 notas, 99 entradas bibliográficas; sin grados (cada expediente cierra con «qué habría que medir»); ninguna
cifra de la primera investigación; expediente moderno de Hebreos nuevo (Harnack 1900, Fonck 1910, 1 Clem 36 y 41,
recuentos MorphGNT). El Tomo IV se reentrega como `_v2` con la conclusión literal de Van Nes en § 8.6. **Siguiente:
Tomo VI** (la investigación, desde `results/paulinum_1_0` y los canales), después títulos y metadatos.

**Bloque 7, tercera entrega (29-IX-2026): Tomo VI montado.** Entregado en
`Correccion_Fondo\07_finales\Pablo de Tarso 6_TomoVI_la_investigacion_2026-09-29.docx`, con informe en
`08_informes\informe_montaje_tomo_VI_2026-09-29.md`; fuentes y guiones de los tres tomos en
`09_recursos\montaje_tomosIV-VI_2026-09-29.zip`. Introducción, cuatro Partes (método; las catorce cartas; recepción,
onomástica e institucional; convergencia y conclusiones, con el cierre de la obra en § 10.6), apéndice técnico
(depósitos, corpus, rejilla, tablas A.1-A.9, glosario, archivos) y bibliografía; 29.700 palabras de cuerpo (6.100 en
tablas), 45 notas, 49 entradas bibliográficas, 27 tablas, ~150 páginas. Solo cifras de `paulinum` 1.0 y de
`results/canales/`; desviaciones D-024, D-025, D-027-D-031 y enmienda 6 declaradas; SVM sin Hebreos y variables de
situación sin controles declaradas como tareas. `build_tomo.py` cambia el tratamiento de tablas (anchura completa; 8 pt
con cinco o más columnas): los Tomos IV y V lo tomarán al regenerarse. **Siguiente: títulos definitivos y metadatos de
Amazon de los tres tomos** y regeneración de los tres DOCX; después, versión 1.1.0.

**Bloque 7, cuarta entrega (29-IX-2026): títulos y fichas de Amazon.** Título común «¿Quién escribió las cartas de
san Pablo?»; subtítulos: IV «Historia de la autoría de las epístolas paulinas, de los Padres de la Iglesia y Erasmo a
la crítica bíblica moderna y la estilometría computacional»; V «El debate actual sobre la autenticidad de las epístolas
paulinas: pseudoepigrafía, secretarios, cartas pastorales, Colosenses, Efesios y Hebreos»; VI «Una investigación
estilométrica y convergente sobre la autoría de las trece epístolas paulinas y la Carta a los Hebreos: método,
resultados y conclusiones». Serie «Teología y Exégesis de San Pablo Apóstol», vols. 4-6. Los tres DOCX regenerados
(`07_finales\Pablo de Tarso {4,5,6}_Tomo{IV,V,VI}_quien_escribio_las_cartas_2026-09-29.docx`; solo cambia el
subtítulo y el tratamiento común de tablas) y las fichas KDP (descripción HTML, tres categorías, siete palabras clave,
contraportada) en `07_finales\fichas_KDP_tomos_IV-VI_2026-09-29.txt`. **Siguiente: versión 1.1.0** (D-024, D-025,
D-026, SVM con Hebreos, variables de situación con controles), cuando el autor lo ordene.

Según § 9 del protocolo y `08_informes/indice_propuesto_tomos_IV_V_VI.md`:

1. **Canales no estilométricos** con protocolo de codificación fijado antes de codificar (§ 9.1-9.3): recepción y
   transmisión (𝔓46 y su orden, canon de Marción, Muratori, testimonios patrísticos), onomástica y prosopografía
   (nombres de las cartas frente a epigrafía), canal institucional. Cada canal con su tabla, fuentes citadas y grado
   de compatibilidad con H1-H5 por carta; sin multiplicar LR entre canales (§ 9.4).
2. **Convergencia (§ 9.4)** por carta: tabla de los canales, con Hebreos igual que las trece.
3. **Montaje de los Tomos IV, V y VI nuevos** a partir de los `.docx` de `07_finales` y del índice propuesto: el Tomo V
   reproduce la tabla del veredicto y la comenta con las reservas; nada de calificaciones provisionales; títulos y
   metadatos al final. Reglas de fondo en `00_biblia_correccion.md`.
4. Versión 1.1.0 del software (después del libro o en paralelo, nunca tocando `results/paulinum_1_0`): corregir los
   tres defectos anotados y, si se quiere, repetir la campaña como `paulinum_1_1` con nuevo protocolo sellado.

## 6. Recetario operativo de la sesión de Cowork (probado en los bloques 4 y 5)

- **Red:** desde el portátil (VM de la sesión) y desde la nube solo se alcanzan por programa GitHub y PyPI. Zenodo, OSF
  y Hugging Face solo con el **navegador integrado** (`Claude_Browser`; el autor puede iniciar sesión en él).
  La API de GitHub desde la nube devuelve 403: **las llamadas se hacen desde el portátil**. La nube sí puede hacer
  `git fetch` del repositorio público (lectura); el *push* solo desde el portátil.
- **Portátil (VM):** 2 núcleos, 3 GB, Python 3.10 con numpy, sin scipy; cada llamada ≤ 180 s y los procesos en
  segundo plano mueren al terminar la llamada. Ayudantes que hay que recrear en cada sesión en `$HOME` de la VM
  (fuera de `mnt/`): `askpass.sh` (devuelve el usuario y lee el token del archivo) y `gh_api.py` (`call`, `dispatch`,
  `runs`, `jobs`; el token leído del archivo, nunca impreso). Uso:
  `python3 gh_api.py dispatch <config> <run> <stage> [familias] [solo] [horas]`, `python3 gh_api.py runs N`.
  Push: `GIT_ASKPASS="$HOME/askpass.sh" GIT_TERMINAL_PROMPT=0 git push origin main 2>&1 | grep -v -i token`.
  Commits: `git -c core.safecrlf=false commit -q -m "<mensaje en español>"` con las dos líneas de atribución que la
  sesión indique. El permiso de borrado en `Correccion_Fondo` caduca con la sesión: pedirlo de nuevo si hace falta
  quitar un `index.lock`; si no, mover a `_to_delete\`.
- **Nube:** 2 núcleos, límite de memoria 6,27 GB para los procesos de la sesión; el contenedor se recicla pocos
  minutos después de terminar un turno (los procesos en segundo plano mueren): para cómputo largo hay que **mantener
  el turno activo** (llamadas `sleep 590` encadenadas) o trocear en Actions. Un proceso `paulinum run --stage specs`
  crece ≈ 100-450 MB por especificación: ejecutar por trozos de 2 especificaciones (`--solo a,b`) en procesos nuevos.
- **Traspaso nube → portátil:** `git add -A` y `git diff --cached --binary | gzip -9 > /mnt/user-data/outputs/X.patch.gz`
  (≤ 20 MB por archivo en `device_commit_files`; los resultados comprimen 10-15×); `device_commit_files` a
  `nuevo_paulinum\X.patch.gz`; en el portátil `gunzip -c ../X.patch.gz > $HOME/X.patch && git apply --check $HOME/X.patch
  && git apply $HOME/X.patch`. **Nombre nuevo para cada parche** (una reutilización entregó contenido viejo). Los CSV
  llevan `\r\n`. `data/provenance.json` del portátil es el canónico.
- **Laboratorio de Actions:** `docs/laboratorio_actions.md` (orden, tiempos medidos, incidencias). Resultados en
  *commits* `[lab] …`; `git pull --rebase` en el portátil antes de tocar nada; registros públicos de cada ejecución en
  `results/<run>/lab_*.log`. Artefacto `results-<run_id>` solo descargable por el autor (navegador).
- **Zenodo:** comprobar el DOI de una *release* con el navegador integrado en
  `https://zenodo.org/search?q=parent.id:22993121&f=allversions:true` (puede tardar; las *releases* grandes más).
- **Cotejo con NA28:** `pdftoppm -r 300 -f <p> -l <p> -png` sobre el PDF traído a la nube y lectura visual; sin OCR.

## 7. Cosas pequeñas pendientes

- DOI del Sello 3 anotado (10.5281/zenodo.23034497; Zenodo tardó unas dos horas en archivar la *release*).
- Mover `Correccion_Fondo\paulinum_lab\` a `_to_delete\` y vaciar `nuevo_paulinum\_to_delete\` cuando el autor lo confirme.
- Defectos del código sellado para 1.1.0: guion de anotación (D-024), `learn_closed_class` solo con MorphGNT (D-025),
  comprobación de cartas breves fuera de la etapa `ledger` (D-026), `build` no construye la edición base cuando se le
  pasa una configuración de bloque (tercera incidencia del laboratorio), crecimiento de memoria de `stage specs`.
- Fallo visible de la prueba Ignacio (IgnLong#9 leído débilmente como Ignacio) y la observación sobre la distancia de
  una carta consigo misma con ventanas independientes: siguen siendo pertinentes para leer el nivel 2.

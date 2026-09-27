# Estado del proyecto paulinum 1.0 — 27 de septiembre de 2026 (cierre del bloque 4, Sello 2)

Documento de traspaso entre sesiones de trabajo. Lo escribe la sesión que cerró el bloque 4 para que la siguiente
(un chat nuevo, sin memoria de este) continúe sin perder nada. Todo lo que aquí se dice está también, con más detalle,
en los archivos que se citan; este documento es el índice y el orden de lectura.

## 0. Orden de lectura para una sesión nueva

1. Este documento entero.
2. `protocols/paulinum_1_0/PROTOCOLO.md` (sellado, no se toca) y `protocols/paulinum_1_0/REGISTRO.md` (sellos,
   DOI, enmiendas 1-4).
3. `docs/laboratorio_actions.md` (cómo se ejecuta la campaña y en qué orden) y `docs/decisiones.md` (D-001 a D-022).
4. `docs/registro_investigacion.md` (bitácora por sesiones) y `CHANGELOG.md`.
5. Solo si hace falta el detalle: `docs/testigos_manuscritos.md`, `docs/inventario_fuentes_sesion0.md`,
   `docs/3Cor_validacion_pendiente.md`, `README.md`.

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
| Token de GitHub (solo local) | `C:\Users\ferpe\Desktop\Correccion_Fondo\nuevo_paulinum\github_token.txt` |
| Diorisis.zip (CC BY-NC-SA, no redistribuible; SHA-256 `fb32b7ff4bcfc433f1234aff8134096f524c9a32accbfdf0a072df4a5f019b65`) | `nuevo_paulinum\Diorisis.zip` |
| Lexicón uniforme (no versionado; SHA-256 `b0ea6312655cbe8fdd5f92337089a7b9e5f961d7f2d5aa1b6e67bf25440c4ea7`, 16,5 MB) | portátil: `paulinum\data\cache\lexicon_uniforme.tsv` |
| Testigos manuscritos (XML brutos, manifiesto original, derivados con texto; no versionados) | portátil: `paulinum\data\local\testigos\` (en el repositorio solo el manifiesto publicado, los guiones y los agregados) |
| NA28 del autor (escaneo sin capa de texto; uso local, solo máscaras) | `Correccion_Fondo\10_fuentes\biblia\Nestle-Aland-Novum-Testamentum-Graece-28-PDF.pdf` (página PDF = página impresa + 125) |
| Tomos del libro (versiones finales) | `Correccion_Fondo\07_finales\Pablo de Tarso 4_TomoIV_quien_escribio_las_cartas_corregido.docx`, `…5_TomoV_cartas_bajo_prueba_I_corregido.docx`, `…6_TomoVI_cartas_bajo_prueba_II.docx` |
| Dictamen e índice propuesto de los Tomos IV-VI nuevos (bloques 0 y 1) | `Correccion_Fondo\08_informes\dictamen_reestructuracion_tomos_IV_V_VI.md`, `…\indice_propuesto_tomos_IV_V_VI.md` |
| Reglas de corrección de fondo del autor | `Correccion_Fondo\00_biblia_correccion.md` (§ 15.2 lleva el estado de los Tomos IV y V) |
| Laboratorio antiguo (reconstrucción 0.2.0-r, ya integrado en el repositorio) | `Correccion_Fondo\paulinum_lab\` — **pendiente de mover a `_to_delete/`** cuando el autor lo diga |

La réplica en la nube de la sesión (contenedor Linux) **no persiste entre chats**: una sesión nueva clona el
repositorio (`git clone https://github.com/ferpecorrea-prog/paulinum`), ejecuta `python -m paulinum fetch --tier 4
--editions` y `python -m paulinum build --config config/paulinum_1_0.yaml`, y trae el lexicón del portátil
(`device_stage_files` de `data/cache/lexicon_uniforme.tsv`; comprobar la huella) o lo reconstruye con
`scripts/construir_lexicon.py --diorisis-zip` (Diorisis.zip también se trae del portátil).

## 3. Estado del protocolo (§ 3.3 y § 11 del protocolo)

| sello | etiqueta | huella | DOI | fecha |
|---|---|---|---|---|
| 1. Protocolo preregistrado | `protocolo-1.0.0` | `9b65c9d823691887279abb93522a8dbd1479ec7b08fef411dc099bf083edbfe4` (34 archivos, sin lexicón; `SELLO_protocolo-1.0.0.json`) | 10.5281/zenodo.22993122 | 2026-09-27 |
| 2. Código congelado | `paulinum-1.0.0` (versión 1.0.0) | `cd32dad63855460c77a200606d81b2bd863f9e4d3121926aead66e9a6b0a29ef` (50 archivos, con lexicón; `SELLO_paulinum-1.0.0.json` = `SELLO.json`) | 10.5281/zenodo.22996786 | 2026-09-27 |
| 3. Resultados | `resultados-1.0.0` | — | — | pendiente (fin del bloque 5) |

DOI de concepto (todas las versiones): 10.5281/zenodo.22993121. Registro en OSF: pendiente (con el DOI del Sello 1).
Enmiendas registradas: 1 y 2 (máscaras `otq` cotejadas con NA28, Hebreos y las trece), 3 (NA28 no entra como
edición), 4 (implementación sin cambio de reglas). **Después del Sello 2 no se cambia código salvo enmienda
registrada antes de ejecutarse (§ 12), que llevaría versión 1.0.1 y nuevo sello.** Ninguna fila de diana (las catorce
cartas) se ha calculado todavía. Últimos *commits*: 528bbf8 (implementación), 7e144aa (Sello 2), d9ec68d (DOI).

## 4. Qué hay implementado (todo sellado en el Sello 2)

Paquete `paulinum/`: corpus de 857 documentos (estrato 4; 2,79 M de palabras) con ediciones SBLGNT, Tischendorf
(PROIEL; sin Heb 13, 1-2 Jn, 2 Pe), Nestle 1904 (MACULA) y testigos (`sinaiticus`, `sblgnt_rec_sinaiticus`, `p46`,
`sblgnt_rec_p46`, solo en local); tres familias (impostores, NCD, Dirichlet-multinomial); problemas de respuesta
conocida (`core_loo`, `target`, `pos_pairs`, `neg_pairs`, `pseudo_pairs`, `neg_target`, `pos_epist`, `neg_epist`,
`genre_pairs`, `mediated_pairs`); calibraciones general, epistolar (principal) y cristiana; envolventes E, B, G; núcleo
más próximo; variables de situación; ventanas deslizantes; etapa `specs` reanudable por problema y paralela.
Guiones: `veredicto.py`, `bootstrap_percentil.py`, `ruido_edicion.py`, `anotacion_uniforme.py`,
`generar_sensibilidad.py` (→ `config/sens/*.yaml`, nueve bloques), `modelo_svm.py`, `testigos/derivar_testigos.py`.
Pruebas: `pytest` 10/10, `scripts/selftest.py` 25/25 (huella `ecaf65723ff53cdab462bb3ad014dcf3475a076b011060dc4333f603fa190117`).
Validación sin dianas publicada: `results/prueba_1_0/`, `results/prueba_veredicto_ignacio/`, `results/prueba_ruido/`
(D-018, D-022). Laboratorio de cómputo: `.github/workflows/campana.yml` (D-017).

## 5. Bloque 5 (siguiente): la campaña principal. Esfuerzo: extra alto, con horas de cómputo

Orden exacto en `docs/laboratorio_actions.md` § «Orden de ejecución». Resumen operativo:

1. Lanzar en GitHub Actions (desde el portátil, con la API y el token leído del archivo; véase § 6):
   `stage=anotacion` (una vez) y `stage=ruido` (una vez), `run=paulinum_1_0`, `config=config/paulinum_1_0.yaml`.
2. `stage=specs` con `familias=impostores` (≈ 2 h), `familias=dirichlet` (≈ 0,5 h), `familias=ncd` con `solo=0` y
   `solo=1` (≈ 1,5 h cada uno; reanudables). **Atención al orden de § 3.3/§ 11:** las etapas de calibración y
   envolventes deben publicarse antes de las filas de diana. Como `specs` calcula a la vez problemas de respuesta
   conocida y dianas, se hace así: primero un `run` auxiliar `paulinum_1_0_calibracion` con una copia de la
   configuración con `sin_dianas: true` (etapas `specs,calibration,ledger,variables`), se publica (commit), y solo
   después el `run` definitivo `paulinum_1_0` completo (cuyas filas de respuesta conocida son idénticas a las del
   auxiliar, porque cada problema lleva su semilla). Alternativa equivalente: lanzar `paulinum_1_0` por familias y
   hacer commit de `calibration,ledger` antes de mirar `gi_targets_por_especificacion.csv`. El historial de git es el
   registro del orden.
3. `stage=calibration,ledger,variables,rolling,extras`; `stage=bootstrap`; `stage=svm`.
4. Bloques de sensibilidad `config/sens/paulinum_1_0_{nucleos,ediciones,ventana300,documento_entero,rasgos,coseno,nodia}.yaml`
   en Actions; `pos3` solo si `results/anotacion/acuerdo_nt.json` dice `apto`; `testigos` **solo en el portátil o en la
   nube con los derivados traídos del portátil** (no se publican los textos), y su ruido de edición con
   `scripts/ruido_edicion.py --ediciones sinaiticus,p46` desde el portátil.
5. `stage=veredicto` → `results/paulinum_1_0/veredicto.{csv,md}`. Lectura de los cuatro niveles y del patrón § 8.5
   por carta; falsación (§ 10). Sello 3: etiqueta `resultados-1.0.0`, *release*, DOI, `REGISTRO.md`.
6. Después del Sello 3: canales no estilométricos (§ 9: recepción y transmisión, onomástica y prosopografía, canal
   institucional) con su protocolo de codificación; convergencia (§ 9.4); montaje de los Tomos IV y V nuevos y del
   Tomo VI según `08_informes/indice_propuesto_tomos_IV_V_VI.md`; títulos y metadatos al final.

Tiempos de referencia (un núcleo): impostores 16 especificaciones × 1.611 problemas × 300 iteraciones ≈ 8 h;
Dirichlet ≈ 2 h; NCD ≈ 10 h (D-020). Con cuatro procesos en Actions, un cuarto. El portátil no sirve para cómputo
largo (cada llamada de la sesión dura ≤ 180 s y los procesos en segundo plano mueren al terminar la llamada).

## 6. Recetario operativo de la sesión de Cowork (probado)

- **Red:** desde el portátil (VM de la sesión) y desde la nube solo se alcanzan por programa GitHub y PyPI. No se
  alcanzan Zenodo, Hugging Face, figshare, epapers.bham.ac.uk ni ntvmr.uni-muenster.de. La API de GitHub desde la
  nube devuelve 403 para este repositorio: **las llamadas a la API se hacen desde el portátil** con `urllib` y el token
  leído del archivo (`open(".../github_token.txt").read().strip()`), sin imprimirlo. Zenodo se consulta con el
  **navegador integrado** de la aplicación (herramientas `Claude_Browser`), p. ej.
  `https://zenodo.org/search?q=parent.id:22993121&f=allversions:true`.
- **Push desde el portátil:** crear en cada sesión un `askpass.sh` en `$HOME` de la VM (fuera de `mnt/`) que devuelva
  el usuario y lea el token del archivo, y empujar con
  `GIT_ASKPASS="$HOME/askpass.sh" GIT_TERMINAL_PROMPT=0 git push -q origin main` (con `--tags` para las etiquetas).
  Filtrar cualquier salida de git con `grep -v -i token` por precaución.
- **Traspaso nube → portátil:** en la nube, `git add -A` y `git diff --cached --binary > /mnt/user-data/outputs/X.patch`;
  `device_commit_files` a `C:\Users\ferpe\Desktop\Correccion_Fondo\nuevo_paulinum\X.patch`; en el portátil,
  `git apply --check ../X.patch && git apply ../X.patch && rm -f ../X.patch` (permiso de borrado ya concedido para
  `Correccion_Fondo` en la sesión anterior; en una nueva hay que volver a pedirlo o mover a `_to_delete/`).
  Los CSV llevan `\r\n` (módulo `csv`): usar `git -c core.safecrlf=false commit`. `data/provenance.json` del portátil
  es el canónico (no traer el de la nube).
- **Commits:** mensaje en español; al final las dos líneas de atribución que la sesión indique
  (`Co-Authored-By: Claude …` y `Claude-Session: …`).
- **Lanzar el laboratorio:** `POST https://api.github.com/repos/ferpecorrea-prog/paulinum/actions/workflows/campana.yml/dispatches`
  con `{"ref": "main", "inputs": {"config": "...", "run": "...", "stage": "...", "familias": "...", "solo": "...", "horas": "5"}}`;
  seguimiento con `GET …/actions/runs?per_page=5`. Los resultados llegan a `main` en *commits* `[lab] …`: hacer
  `git pull` en el portátil antes de tocar nada.
- **Cotejo con NA28:** `pdftoppm -r 300 -f <p> -l <p> -png` sobre el PDF traído a la nube y lectura visual; sin OCR.

## 7. Cosas pequeñas pendientes

- Registro en OSF con el DOI del Sello 1 (anotar en `REGISTRO.md`).
- Mover `Correccion_Fondo\paulinum_lab\` a `_to_delete\` cuando el autor lo confirme (ya está todo integrado).
- Bloque `testigos`: 𝔓46 no contiene 2 Tes, las Pastorales ni Flm; decirlo en los resultados (dato del canal de
  transmisión, § 9.1).
- Fallo visible de la prueba Ignacio: IgnLong#9 (espuria) se lee débilmente como Ignacio; el nivel 2 fue conservador
  con ese núcleo de siete cartas breves. Se informa; no se ajusta nada (el código está sellado).
- La distancia de una carta larga consigo misma con ventanas independientes es del orden de la distancia entre cartas
  del núcleo (variación entre pasajes): el *bootstrap* de ventanas es la cuantificación que el protocolo prevé; tenerlo
  presente al leer las envolventes.

# Laboratorio de cómputo en GitHub Actions (paulinum 1.0)

Complemento del § 3.4 y del § 11 del protocolo (D-017). Además del portátil (pruebas de referencia) y de la réplica en
la nube (2 núcleos), las etapas pesadas de la campaña `paulinum_1_0` y de sus bloques de sensibilidad se ejecutan en
ejecutores de GitHub Actions con el flujo `.github/workflows/campana.yml`, que se lanza a mano (`workflow_dispatch`) y
deja cada ejecución registrada en público: el *log* del ejecutor, la bitácora `results/<run>/bitacora.md` y el
*commit* `[lab] …` con los resultados.

## Qué hace cada ejecución

1. Parte de cero: `actions/checkout` del *commit* de `main` en el momento del lanzamiento (después del Sello 2, el
   código de ese *commit* es el sellado; la huella se puede recomputar con `python -m paulinum seal`), Python 3.11 y
   las versiones fijadas en `requirements.txt`.
2. Descarga los textos de origen (`python -m paulinum fetch --tier 4 --editions`) y **comprueba sus huellas contra
   `data/provenance.json`** (el archivo versionado): `fetch` reescribe ese archivo con las huellas y la hora de cada
   descarga; el flujo compara cada huella con la registrada en el repositorio, se detiene si alguna difiere, informa
   de los archivos no registrados o ausentes y restaura el archivo canónico (`git checkout -- data/provenance.json`),
   de modo que el árbol de trabajo queda limpio para el envío final.
3. Si la configuración usa `lemma_dict`, descarga Diorisis desde figshare (artículo 6187256; CC BY-NC-SA 4.0, no se
   redistribuye), reconstruye el lexicón con `scripts/construir_lexicon.py` y **comprueba que su SHA-256 coincide con
   el sellado** en `protocols/paulinum_1_0/SELLO.json`; si no coincide, la ejecución se detiene.
4. Construye el corpus e inventario (`build`, `inventory`).
5. Ejecuta la etapa pedida con tope de horas (`timeout`), cuatro procesos (`--workers 4`) y, si se indica, solo
   algunas familias (`--familias`) o algunas especificaciones (`--solo`, para trocear la familia NCD).
6. Añade `results/` y hace *commit* y *push* a `main` (con reintentos si otra ejecución empujó antes; antes del
   *rebase* restaura cualquier archivo versionado tocado fuera de `results/`). Si el envío no se logra en cinco
   intentos, la ejecución **falla de forma visible**; en todo caso, `results/` se guarda además como artefacto de la
   ejecución (`results-<run_id>`, 30 días), de modo que ningún cómputo se pierde. Si el tope de tiempo cortó la
   etapa, se envía lo hecho: los archivos `specs/<spec>.json.parcial.jsonl` guardan cada problema terminado y la
   siguiente ejecución retoma donde quedó.

Primera ejecución real (27-IX-2026, 13:14 UTC, `anotacion`): la descarga, la reconstrucción del lexicón (4 min; huella
igual a la sellada) y el corpus funcionaron; el envío final falló en silencio porque `fetch` había modificado
`data/provenance.json` y `git pull --rebase` se negaba a continuar con cambios sin confirmar; el bucle de reintentos
no hacía fallar el paso. Corregido en el propio flujo como se describe en los puntos 2 y 6 (sin cambio de código
sellado: el flujo no forma parte del sello). La ejecución de `specs` que corría en paralelo se canceló y se relanzó
con el flujo corregido.

## Entradas del flujo

| entrada | valor | ejemplo |
|---|---|---|
| `config` | configuración | `config/paulinum_1_0.yaml`, `config/sens/paulinum_1_0_nucleos.yaml` |
| `run` | nombre de `results/<run>` (vacío = `nombre` de la configuración) | `paulinum_1_0` |
| `stage` | etapas de `paulinum run` (`specs,calibration,ledger,variables,rolling,extras`) o guion (`bootstrap`, `veredicto`, `svm`, `anotacion`, `ruido`) | `specs` |
| `familias` | `impostores`, `ncd`, `dirichlet` (vacío = las activas) | `ncd` |
| `solo` | índices de especificación | `0` |
| `horas` | tope de cálculo | `5` |

## Orden de ejecución de la campaña principal (§ 3.3)

Cada línea es un lanzamiento del flujo; ninguna produce filas de diana hasta el punto marcado.

1. `stage=anotacion` (una vez): validación de la anotación uniforme (D-016); escribe `results/anotacion/acuerdo_nt.*`
   y, si supera el umbral, `results/anotacion/pos_uniforme_sblgnt.jsonl.gz` (solo etiquetas), que el bloque `pos3`
   de sensibilidad lee.
2. `stage=ruido` (una vez): ruido de edición de las catorce cartas con Tischendorf y Nestle 1904
   (`scripts/ruido_edicion.py`, § 5.4, D-022) → `results/paulinum_1_0/ruido_edicion_{minmax,delta}.csv` y
   `ruido_edicion_resumen.csv`; el ruido con los testigos (Sinaítico, 𝔓46) solo puede calcularse en local, porque
   sus derivados no se publican, y se añade a los mismos archivos desde el portátil (`--ediciones sinaiticus,p46`).
3. `stage=specs`, `familias=impostores` (≈ 2 h con cuatro procesos); `familias=dirichlet` (≈ 0,5 h);
   `familias=ncd`, `solo=0` y `solo=1` (≈ 1,5 h cada una tras D-020; reanudables).
   Con `sin_dianas` **desactivado** en `config/paulinum_1_0.yaml`, estas ejecuciones calculan también las filas de
   diana (`target`, `core_loo`) de cada especificación: son la etapa 8 de § 11 y solo se lanzan cuando las etapas
   1-7 están publicadas. Para cerrar antes la calibración y las envolventes sin dianas se usa un `run` distinto con
   `sin_dianas: true` (como `config/prueba_1_0.yaml`) o se lanzan primero `calibration,ledger,variables` sobre un
   conjunto de especificaciones ya terminado.
4. `stage=calibration,ledger,variables,rolling,extras` (≈ 0,5 h): calibraciones, envolventes E/B/G, núcleo más
   próximo, variables de situación, ventanas deslizantes, tabla de las catorce.
5. `stage=bootstrap` (IC de percentiles por autores y por ventanas, `scripts/bootstrap_percentil.py`; ≈ 3 h).
6. `stage=svm` (segundo modelo, § 6.5).
7. Bloques de sensibilidad (`config/sens/*.yaml`, generados por `scripts/generar_sensibilidad.py`), cada uno con
   `stage=specs` y después `calibration,ledger,extras`; escriben en `results/paulinum_1_0/sensibilidad/<bloque>/`.
8. `stage=veredicto` (`scripts/veredicto.py`): `results/paulinum_1_0/veredicto.csv` y `veredicto.md`. Sello 3.

## Determinismo

Las semillas derivan de `parametros.semilla` (20260927), del índice de especificación y de la familia (§ 3.4); los
resultados por problema son independientes del número de procesos y del orden de ejecución (cada problema tiene su
semilla propia: semilla de la especificación × 100003 + índice del problema), de modo que una etapa troceada o reanudada da las mismas filas que una
ejecución de una pieza. La prueba `test_determinismo_por_problema` de `tests/test_paulinum_1_0.py` lo comprueba con un corpus sintético en las tres familias.

## Qué no hace

- No usa ninguna credencial aparte del `GITHUB_TOKEN` efímero del propio flujo (permiso `contents: write`).
- No redistribuye textos de terceros ni el lexicón: `data/` no se versiona; solo se publican `results/`.
- No decide nada: el veredicto lo calcula `scripts/veredicto.py`, sellado en el Sello 2, con las reglas de § 8.

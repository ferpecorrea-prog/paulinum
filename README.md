# paulinum_lab — Verificación convergente de la autoría del corpus paulino canónico

Laboratorio de reproducibilidad de las dos investigaciones publicadas en *¿Quién escribió las cartas
de san Pablo?*: la capa estilométrica de trece lemas y la segunda campaña (P1-P12) de la Investigación 1,
y las tres campañas del software **paulinum** (verificación por impostores generales con controles de
autoría segura, «mismo rasero», variables de situación, calibración secundaria, segundo modelo) de la
Investigación 2.

> **Lea antes `LEEME_PRIMERO.md`.** Esta carpeta es una **reconstrucción** (paulinum 0.2.0-r) del
> laboratorio original, cuyo código se perdió; el código se ha reimplementado a partir de la
> especificación publicada y los resultados publicados se conservan como datos de referencia.

## Contenido

| carpeta | contenido |
|---|---|
| `paulinum/` | paquete Python: `sources` (manifiesto), `fetch`, `parsers`, `text`, `corpus`, `features`, `distances`, `verify`, `variables`, `rolling`, `pipeline`, `report`, `cli`, `__main__` |
| `scripts/` | guiones auxiliares (A.1): `selftest`, `run_all`, `calibracion_secundaria`, `construir_lexicon`, `detectar_reutilizacion`, `variables_controles`, `bootstrap_percentil`, `modelo_svm`, `cobertura_lexicon`, `controles_genero`, `lectura_modelo_svm` |
| `config/` | `default.yaml` (campaña 01), `campana_02a…02e.yaml` (robustez), `campana_03.yaml` (ampliación), `prueba_reducida.yaml` (prueba técnica); cada una con su bloque de preregistro literal |
| `metadata/` | `masks.csv` (fórmulas, material preformado, citas del AT, por referencia), `reuse_ranges.csv` (pasajes paralelos, publicado), `letter_variables.csv` (variables de situación de las 13 cartas), `status_audit.csv` (estados con fuente), `control_variables.csv` (generado) |
| `data/` | `raw/` (descargas; no se versiona), `cache/` (corpus construidos y lexicón), `local/` (3 Corintios, a preparar), `provenance.json` (huellas SHA-256 de cada archivo descargado) |
| `results/` | salidas de las ejecuciones de esta reconstrucción; `results/prueba_reducida/` contiene una ejecución completa de prueba |
| `results_publicados/` | **tablas publicadas** (Apéndice A.4 e Investigación 1) transcritas a CSV; `sellos_publicados.csv` |
| `informes/` | texto íntegro del informe final de la campaña 01 y del informe de la campaña 03 (Anexos I y II) con sus figuras |
| `investigacion_1/` | `capa_13_lemas/` (matriz publicada, recálculo íntegro y cotejo 313/313), `segunda_campana/` (`stylolib` y guiones P2, P3, P5, P6-P7, P8, P9, P10, P11), `ESPECIFICACION_PUBLICADA.md` |
| `docs/` | apéndice técnico publicado, capítulos 7-12, bibliografía, `ESPECIFICACION_RECONSTRUIDA.md` (decisiones de la reconstrucción), `GUIA_GITHUB.md` |

## Instalación

Python 3.10 o superior. Versiones del original (A.1) en `requirements.txt`; la reconstrucción se ha
probado además con numpy 2.4, scipy 1.17, pandas 3.0 y scikit-learn 1.8.

```bash
python -m venv .venv && source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/selftest.py                              # 25 comprobaciones; imprime una huella de referencia
```

## Prueba de extremo a extremo (unos minutos)

```bash
python scripts/run_all.py --config config/prueba_reducida.yaml --run prueba_reducida --tier 1 --sin-bootstrap-ventanas
```

Descarga el Nuevo Testamento (MorphGNT/SBLGNT) y los Padres Apostólicos, construye el corpus con sus
máscaras, sella el protocolo, ejecuta cuatro especificaciones, el mismo rasero, la PERMANOVA, las ventanas
deslizantes, la calibración secundaria, el bootstrap, el segundo modelo y el informe automático en
`results/prueba_reducida/informe/INFORME_AUTOMATICO.md`. Sus cifras **no** son comparables con las
publicadas (el corpus de control es mucho menor); sirve para comprobar que la cadena funciona.

## Reproducir las campañas publicadas

Órdenes del Apéndice A.1 (la campaña 01 tarda ~2 h y la 03 ~3 h en un ordenador corriente):

```bash
# Campaña 01 (48 especificaciones, 100 iteraciones; 217 documentos)
python -m paulinum fetch --tier 2
python -m paulinum build --config config/default.yaml
python -m paulinum inventory --config config/default.yaml
python -m paulinum seal --config config/default.yaml --run campana_01
python -m paulinum run --config config/default.yaml
python scripts/calibracion_secundaria.py --run campana_01
python -m paulinum report --run campana_01

# Campaña 02 (robustez): las mismas órdenes con config/campana_02a_nucleos.yaml … campana_02e_coseno.yaml
python -m paulinum fetch --tier 2 --editions        # PROIEL (Tischendorf) y MACULA (Nestle 1904) para la 02b

# Campaña 03 (16 especificaciones, 300 iteraciones; 408 documentos; lemas; máscara de reutilización)
python -m paulinum fetch --tier 3
python -m paulinum build --config config/campana_03.yaml
python -m paulinum inventory --config config/campana_03.yaml
python scripts/construir_lexicon.py --diorisis-zip <ruta a Diorisis.zip>
python scripts/detectar_reutilizacion.py --run campana_03 --comparar
python scripts/variables_controles.py --run campana_03
python -m paulinum seal --config config/campana_03.yaml --run campana_03
python -m paulinum run --config config/campana_03.yaml
python scripts/calibracion_secundaria.py --run campana_03
python scripts/bootstrap_percentil.py --run campana_03 --metric minmax --config config/campana_03.yaml
python scripts/bootstrap_percentil.py --run campana_03 --metric delta --config config/campana_03.yaml
python scripts/modelo_svm.py --run campana_03 --features mfw:300,closed:150,char3:600,lemma_dict:300
python scripts/cobertura_lexicon.py --run campana_03
python scripts/controles_genero.py --run campana_03
python scripts/lectura_modelo_svm.py --run campana_03
python -m paulinum report --run campana_03
```

O bien, todo en una orden: `python scripts/run_all.py --config config/campana_03.yaml`.

Comparación con lo publicado: `results_publicados/campana_03/*.csv` frente a `results/campana_03/*.csv`
(mismos nombres de columna). Las puntuaciones GI y las razones de verosimilitud se comparan por su
mediana y su signo, no por el tercer decimal (muestreo aleatorio).

## Investigación 1

```bash
python investigacion_1/capa_13_lemas/recalcular_capa_13.py        # tablas de la capa A/B, Heaps, LOO, bootstrap, PCA, Ward
python investigacion_1/capa_13_lemas/cotejo_con_el_libro.py      # 313/313 coincidencias con el libro
# los tres siguientes requieren el corpus de prueba construido (run_all de arriba o fetch --tier 1 + build);
# descargan por sí mismos la recensión larga de Ignacio y construyen el lexicón (sin Diorisis) si faltan
python investigacion_1/segunda_campana/p2_replica_morphgnt.py     # réplica sobre MorphGNT (rho = 0,99 con Perseus)
python investigacion_1/segunda_campana/p6_p7_impostores_falsificacion.py
python investigacion_1/segunda_campana/p3_p7_p9_p11_lemas_morfologia.py
python investigacion_1/segunda_campana/p8_sintaxis_proiel.py     # requiere: python -m paulinum fetch --editions
python investigacion_1/segunda_campana/p5_calibracion_longitud.py  # requiere el corpus de la campaña 01 o 03
python investigacion_1/segunda_campana/p10_primera_atestacion.py --diorisis-zip <ruta>
```

## Reglas de lectura (preregistradas)

Una especificación con AUC < 0,80 no produce razón de verosimilitud. El veredicto por carta es la mediana
de log10 LR entre especificaciones válidas, con la escala verbal |log10 LR| < 0,3 no discriminante, 0,3-1
débil, 1-2 moderado, ≥ 2 fuerte. Ninguna carta se declara anómala si su percentil intra-autor es ≤ 90 (y,
en la campaña 03, si su IC 95 % cruza 90 se dice «indeterminada»). Las cartas discutidas se valoran una a
una; la carta hermana se excluye de los candidatos. Un resultado adverso se informa sin retocar parámetros.

## Licencias

Código (`paulinum/`, `scripts/`, `investigacion_1/**/*.py`): MIT (`LICENSE`). Datos, metadatos, resultados,
informes y documentación propios: CC BY 4.0 (`LICENSE-DATA`). Los textos fuente conservan su licencia de
origen (MorphGNT CC BY-SA 3.0; Open Apostolic Fathers, Perseus y First1KGreek CC BY-SA 4.0; PROIEL
CC BY-NC-SA 3.0; MACULA CC BY 4.0; Diorisis CC BY-NC-SA 4.0, no redistribuido) y no se versionan en este
repositorio: `python -m paulinum fetch` los descarga y registra su huella en `data/provenance.json`.

## Cita

Véase `CITATION.cff`.

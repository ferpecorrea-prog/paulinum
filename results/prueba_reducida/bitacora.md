# Bitácora de prueba_reducida

| inicio (UTC) | orden / etapa | duración | nota |
|---|---|---|---|
| 2026-09-25 05:58:42 | /usr/bin/python3 -m paulinum fetch --tier 1 | 0.2 s | rc=0 |
| 2026-09-25 05:58:42 | /usr/bin/python3 -m paulinum build --config config/prueba_reducida.yaml | 5.1 s | rc=0 |
| 2026-09-25 05:58:47 | /usr/bin/python3 -m paulinum inventory --config config/prueba_reducida.yaml --run prueba_reducida | 1.0 s | rc=0 |
| 2026-09-25 05:58:48 | /usr/bin/python3 scripts/detectar_reutilizacion.py --run prueba_reducida --comparar | 0.3 s | rc=0 |
| 2026-09-25 05:58:48 | /usr/bin/python3 scripts/variables_controles.py --run prueba_reducida | 1.5 s | rc=0 |
| 2026-09-25 05:58:50 | /usr/bin/python3 -m paulinum seal --config config/prueba_reducida.yaml --run prueba_reducida | 0.0 s | rc=0 |
| 2026-09-25 05:58:51 | python -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida --stage specs | 15.0 s |  |
| 2026-09-25 05:59:06 | python -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida --stage calibration | 0.0 s |  |
| 2026-09-25 05:59:06 | python -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida --stage ledger | 1.1 s |  |
| 2026-09-25 05:59:07 | python -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida --stage variables | 0.3 s |  |
| 2026-09-25 05:59:07 | python -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida --stage rolling | 3.8 s |  |
| 2026-09-25 05:59:11 | python -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida --stage extras | 0.3 s |  |
| 2026-09-25 05:58:50 | /usr/bin/python3 -m paulinum run --config config/prueba_reducida.yaml --run prueba_reducida | 21.3 s | rc=0 |
| 2026-09-25 05:59:11 | /usr/bin/python3 scripts/calibracion_secundaria.py --run prueba_reducida | 0.8 s | rc=0 |
| 2026-09-25 05:59:12 | /usr/bin/python3 scripts/bootstrap_percentil.py --run prueba_reducida --metric minmax --config config/prueba_reducida.yaml --sin-ventanas | 1.3 s | rc=0 |
| 2026-09-25 05:59:13 | /usr/bin/python3 scripts/bootstrap_percentil.py --run prueba_reducida --metric delta --config config/prueba_reducida.yaml --sin-ventanas | 1.3 s | rc=0 |
| 2026-09-25 05:59:15 | /usr/bin/python3 scripts/modelo_svm.py --run prueba_reducida --features mfw:300,char3:600 | 2.6 s | rc=0 |
| 2026-09-25 05:59:17 | /usr/bin/python3 scripts/controles_genero.py --run prueba_reducida | 1.0 s | rc=0 |
| 2026-09-25 05:59:18 | /usr/bin/python3 scripts/lectura_modelo_svm.py --run prueba_reducida | 0.8 s | rc=0 |
| 2026-09-25 05:59:19 | /usr/bin/python3 -m paulinum report --run prueba_reducida | 2.5 s | rc=0 |

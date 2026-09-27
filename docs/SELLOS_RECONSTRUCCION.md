# Sellos y huellas de la reconstrucción (25-IX-2026)

| qué | valor |
|---|---|
| paulinum | 0.2.0-r (reconstrucción) |
| huella del selftest (`python scripts/selftest.py`, Python 3.11.15, numpy 2.4.4, scipy 1.17.1, pandas 3.0.2, scikit-learn 1.8.0) | `ecaf65723ff53cdab462bb3ad014dcf3475a076b011060dc4333f603fa190117` |
| sello de `prueba_reducida` (`python -m paulinum seal --config config/prueba_reducida.yaml --run prueba_reducida`; 32 archivos: 15 módulos, 5 de metadata/, la configuración y 11 guiones) | `2df634138354b4774be94f792f0cfcf54c0731babf7ca5b71ee0e572ab0a6939` |
| SHA-256 de `investigacion_1/capa_13_lemas/data/matriz_19x13.csv` (matriz primaria publicada, formato CSV de esta carpeta) | `4f085f4bb2f097dd88bcfcbbc717173420f55db5818a0ac414e845ced7e39a47` |
| cotejo de la capa de 13 lemas con el libro | 313 de 313 valores |

Los sellos publicados en el libro (`results_publicados/sellos_publicados.csv`) corresponden al código
original, perdido, y no son reproducibles; véase `LEEME_PRIMERO.md`.

Cualquier modificación de un archivo cubierto por el sello (código, metadatos, configuración, guiones)
cambia la huella: quien verifique esta carpeta debe recalcularla con la misma orden y compararla con la de
arriba antes de dar por buenas las cifras de `results/`.

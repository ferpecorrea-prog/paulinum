# results/

Salidas de las ejecuciones de **esta reconstrucción** (paulinum 0.2.0-r). No son los resultados publicados:
esos están transcritos en `../results_publicados/`.

- `prueba_reducida/`: ejecución completa de prueba (NT + Padres Apostólicos; 4 especificaciones, 40
  iteraciones) hecha el 25-IX-2026 con `scripts/run_all.py --config config/prueba_reducida.yaml`. Contiene
  todos los archivos que produce una campaña (A.6): `config_used.json`, `run.log`, `bitacora.md`,
  `specs/000-003.json`, `gi_results_all_specs.csv`, `calibration_by_spec.csv`, `summary_by_letter.csv`,
  `calibracion_secundaria_cristiana*.csv`, `lr_secundaria_por_*.csv`, `distance_matrix_{minmax,delta}.npy`,
  `distance_matrix_ids.csv`, `pair_distances_*.csv`, `double_standard_ledger_*.csv`,
  `permanova_pauline_windows.csv`, `dbrda_partition_pauline_windows.{csv,txt}`, `permanova_controles.csv`,
  `edition_noise_pairs.csv`, `feature_contributions.csv`, `descriptives.csv`, `rolling_scores.csv`,
  `tabla_resumen_13_cartas.csv`, `reutilizacion_pares.csv`, `bootstrap_percentil_*.csv`,
  `loo_autor_percentil_*.csv`, `modelo_svm_*.csv`, `controles_genero*.csv`, `lectura_modelo_svm.md`,
  `inventory.csv`, `informe/INFORME_AUTOMATICO.md` y figuras. **Sus cifras no son comparables con las
  publicadas** (corpus de control mucho menor, sin autores paganos ni judeo-helenísticos).
- `PROTOCOLO_SELLADO_prueba_reducida.json`: sello SHA-256 de la reconstrucción para esa ejecución
  (código, metadatos, configuración y guiones; el lexicón entra en el sello solo en las campañas que usan `lemma_dict`).
- `campana_01/`, `campana_02*/`, `campana_03/`: se crean al ejecutar las campañas publicadas con las
  órdenes del README (varias horas de cómputo).

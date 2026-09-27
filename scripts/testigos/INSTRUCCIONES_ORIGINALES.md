# Paquete de adquisición de testigos para `nuevo_paulinum`

## Qué debe hacer Claude

Desde la raíz del proyecto, ejecutar:

```bash
python preparar_testigos.py --include-ntvmr-sinaiticus
```

Esto creará (o completará) `nuevo_paulinum/` con:

- `sinaiticus_project_v105.xml`
- `p46_ntvmr_10046.xml`
- `sinaiticus_ntvmr_20001.xml` (porque se ha pedido la opción adicional)
- `p46_ntvmr_copyright.txt` (si NTVMR responde al endpoint de copyright)
- `TESTIGOS_MANIFEST.json`
- `README_TESTIGOS.md`

Si se desea exactamente lo mínimo solicitado por Claude, sin la copia NTVMR
adicional del Sinaítico:

```bash
python preparar_testigos.py
```

## Por qué se incluyen dos posibles copias del Sinaítico

La transcripción `sinaiticus_project_v105.xml` es la versión publicada estable
del proyecto Codex Sinaiticus (ITSEE/University of Birmingham). La copia
`sinaiticus_ntvmr_20001.xml` es opcional, pero puede ser útil para comparar
Sinaiticus y P46 bajo una codificación/infraestructura NTVMR más homogénea.

El XML bruto no debe editarse. Las normalizaciones deben escribirse en archivos
derivados y registrarse en el protocolo de reproducibilidad.

## Fuentes

- Codex Sinaiticus v1.05:
  https://epapers.bham.ac.uk/id/eprint/3306/
- NTVMR transcript API:
  https://ntvmr.uni-muenster.de/community/api/transcript/get/
- P46: NTVMR docID 10046.
- Sinaiticus/01: NTVMR docID 20001.

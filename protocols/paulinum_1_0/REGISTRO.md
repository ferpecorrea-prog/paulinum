# Registro público del protocolo paulinum 1.0

| sello | etiqueta de git | huella SHA-256 del conjunto | *release* de GitHub | DOI de Zenodo | fecha |
|---|---|---|---|---|---|
| 1. Protocolo preregistrado | `protocolo-1.0.0` | véase `SELLO.json` (campo `sha256`) | https://github.com/ferpecorrea-prog/paulinum/releases/tag/protocolo-1.0.0 | https://doi.org/10.5281/zenodo.22993122 (registro 22993122; DOI de concepto de todas las versiones: https://doi.org/10.5281/zenodo.22993121) | 2026-09-27 |
| 2. Código congelado | `paulinum-1.0.0` | — | — | — | — |
| 3. Resultados | `resultados-1.0.0` | — | — | — | — |

Registro en OSF: pendiente (se hará con el DOI del Sello 1 como documento de preregistro).

## Enmiendas

Ninguna. (Formato de cada entrada: fecha · alcance · motivo · afecta a filas de diana ya calculadas: sí/no · nuevo sello: sí/no.)

## Verificación

Con el repositorio en la etiqueta indicada:

```bash
python -m paulinum seal --config config/paulinum_1_0.yaml --run paulinum_1_0 --protocol protocols/paulinum_1_0 --sin-lexicon --etiqueta protocolo-1.0.0
```

debe reproducir la huella de `SELLO.json` (el campo `sealed_utc` cambia; la huella no).

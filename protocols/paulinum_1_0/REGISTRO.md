# Registro público del protocolo paulinum 1.0

| sello | etiqueta de git | huella SHA-256 del conjunto | *release* de GitHub | DOI de Zenodo | fecha |
|---|---|---|---|---|---|
| 1. Protocolo preregistrado | `protocolo-1.0.0` | véase `SELLO.json` (campo `sha256`) | https://github.com/ferpecorrea-prog/paulinum/releases/tag/protocolo-1.0.0 | https://doi.org/10.5281/zenodo.22993122 (registro 22993122; DOI de concepto de todas las versiones: https://doi.org/10.5281/zenodo.22993121) | 2026-09-27 |
| 2. Código congelado | `paulinum-1.0.0` | — | — | — | — |
| 3. Resultados | `resultados-1.0.0` | — | — | — | — |

Registro en OSF: pendiente (se hará con el DOI del Sello 1 como documento de preregistro).

## Enmiendas

Formato de cada entrada: fecha · alcance · motivo · afecta a filas de diana ya calculadas: sí/no · nuevo sello: sí/no.

1. **2026-09-27** · metadatos: `metadata/masks.csv`, máscara `otq` de Hebreos · motivo: cotejo previsto en § 5.2 y D-012
   con el texto de NA28 (2012), hecho página a página sobre el ejemplar del autor (pp. 657-684; criterio: tramos en
   cursiva = citas): se añaden ocho tramos que NA28 imprime en cursiva y faltaban en la lista de partida (3,5; 7,1-2; 7,4;
   10,8-9; 10,28; 11,21; 12,15; 12,29) y se retira uno que NA28 imprime en redonda (12,20). Cobertura de Hebreos: citas
   21,7 % (antes 18,6 %), total con cierre 24,1 % (Romanos 23,2 %). SHA-256 de `metadata/masks.csv`: antes `757c3761fa341edefc0ddb4288adc439c9dfcc52939baea62af67fee72cda93a`,
   después `7b1a49f2f06c4ea57755ed31f711c7bf84b9ba48c0be6b1f340620eb7b1d6cf0` · afecta a filas de diana ya calculadas: **no** (ninguna calculada) · nuevo sello: **no** (§ 12:
   enmienda de metadatos prevista; el Sello 2 cubrirá el archivo corregido).

## Verificación

Con el repositorio en la etiqueta indicada:

```bash
python -m paulinum seal --config config/paulinum_1_0.yaml --run paulinum_1_0 --protocol protocols/paulinum_1_0 --sin-lexicon --etiqueta protocolo-1.0.0
```

debe reproducir la huella de `SELLO.json` (el campo `sealed_utc` cambia; la huella no).

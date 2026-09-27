# diagnostico/

Guiones de **diagnóstico** de la infraestructura, fuera del conjunto sellado (el sello recoge `paulinum/*.py`,
`metadata/*.csv`, la configuración, `scripts/*.py`, `scripts/*/*.py`, `config/sens/*.yaml` y el lexicón; esta carpeta
no). Nada de lo que hay aquí produce cifras del protocolo ni interviene en ninguna etapa de la campaña: sirve para
entender un resultado de la infraestructura (p. ej., por qué una validación da un valor anómalo) antes de decidir si
procede una enmienda (§ 12). Sus salidas se publican en `results/` con el prefijo `diagnostico_`.

- `anotacion_diagnostico.py`: acuerdo del anotador uniforme con MorphGNT medido con cuatro variantes de alineación y
  ortografía (V0 = método sellado; V1 = tokenización forzada; V2 = V1 + sigma final; V3 = V2 + equivalencias de tagset).

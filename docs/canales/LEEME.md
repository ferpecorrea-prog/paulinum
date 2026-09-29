# Canales no estilométricos (PROTOCOLO § 9): libros de códigos, plantillas y registro

Esta carpeta fija, **antes de codificar nada**, cómo se codifican los tres canales no estilométricos de la campaña
`paulinum_1_0` (recepción y transmisión, onomástica y prosopografía, canal institucional) y cómo se leen después en la
tabla de convergencia de § 9.4. Los libros de códigos son los de § 9 del protocolo sellado, sin cambio; aquí se
concretan las plantillas, las fuentes de referencia y el procedimiento. Enmienda 6 del registro del protocolo: un
solo codificador (el asistente de investigación), con fuente y cita textual en cada código y marca `juicio=sí` en los
códigos que dependen de apreciación.

## Archivos

| archivo | contenido |
|---|---|
| `codigos_recepcion.md` | lista cerrada de testigos con fecha y edición de referencia; códigos 0-3; atribución; posición; medidas |
| `codigos_onomastica.md` | reglas del inventario de nombres; códigos (a)-(e); índices; colecciones de referencia y muestras sorteadas |
| `codigos_institucional.md` | léxico cerrado; corpus de comparación; códigos de datación; lectura |
| `registro_consultas.md` | una línea por consulta a una fuente externa (fecha UTC, fuente, URL o referencia, consulta, resultado) |
| `../../results/canales/recepcion.csv` | codificación: una fila por carta × testigo |
| `../../results/canales/onomastica_inventario.csv` | una fila por nombre × documento (catorce cartas y colecciones de referencia) |
| `../../results/canales/institucional.csv` | una fila por término × documento × contexto |
| `../../results/canales/convergencia.csv` | § 9.4: una fila por carta × canal × hipótesis (compatible / no compatible / no decide) |

## Procedimiento común

1. Las colecciones de referencia se codifican **antes** que las catorce cartas (§ 9): en onomástica, las cartas seguras
   (Ignacio, 1 Clemente, Juliano, Basilio, Libanio) y las pseudoepigrafías (Ps-Ignacio, Ps-Clemente, Ps-Juliano,
   Ps-Basilio, 3 Corintios, Hechos de Pablo, Hercher) dan la distribución de cada índice bajo autenticidad y bajo
   falsificación; en recepción, las siete cartas del núcleo se codifican antes que las siete dianas y Hebreos se
   codifica con el mismo rasero que las trece.
2. Cada código lleva `fuente` (edición, base de datos o bibliografía) y `cita` (el pasaje o el registro, textual y
   breve) para que un lector pueda recodificar. Las consultas a bases externas se hacen una a una por navegador y se
   anotan en `registro_consultas.md`; ninguna se hace con automatismos.
3. `juicio=sí` marca los códigos que dependen de apreciación (alusión posible o probable; coherencia interna; paralelo
   epigráfico dudoso); los índices se calculan con y sin ellos.
4. Las catorce cartas se leen con la tabla de § 2.2 del protocolo (qué predice cada hipótesis en cada canal); el
   canal institucional data y no atribuye. La convergencia (§ 9.4) no combina probabilidades: sostenida / debilitada /
   descartada / abierta, y la contradicción entre canales es un resultado.
5. Lo que un canal no puede decidir se codifica «no decide», nunca se rellena por analogía con otra carta.

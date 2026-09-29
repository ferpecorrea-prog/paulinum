# Convergencia (PROTOCOLO § 9.4): cómo se rellena la tabla y cómo se lee

`herramientas/convergencia.py` escribe `results/canales/convergencia.csv` (carta × canal × H1-H5, con `base` y
`nota`) y `convergencia_veredicto.csv` (carta × H1-H5 → sostenida / debilitada / descartada / abierta; y la hipótesis
de partida de § 10). No se calcula ninguna probabilidad combinada; la contradicción entre canales es un resultado.

## 1. Traducción de cada canal a los tres valores (fijada el 29-IX-2026 antes de rellenar la tabla, D-031)

| canal | fuente | regla |
|---|---|---|
| estilometría | `results/paulinum_1_0/veredicto.csv`, frase sellada `patron_8_5` (§ 8.5) | «compatible con Hx(-Hy)» → compatible; «no con Hx» y «Hx improbable» → no compatible (la carta está dentro del rango y § 2.2 predice «fuera del rango» para H4 y H5); hipótesis no nombrada → no decide; «se informa sin decidir» → no decide en las cinco |
| recepción | `results/canales/recepcion_medidas.csv`, `lectura_mismo_rasero` (D-027) | «H1, H2, H3, H4 compatibles; H5 no compatible» y «H1-H3 no compatible; H4 compatible; H5 compatible», tal cual |
| onomástica | `results/canales/onomastica_lectura.csv`, `H1_H3`, `H4`, `H5` (D-029) | H1, H2 y H3 reciben el valor de `H1_H3` |
| institucional | `results/canales/institucional_lectura.csv`, `H1_H3`, `H4`, `H5` (D-030) | ídem |

Los cuatro canales se tratan como independientes a efectos de la regla «dos o más canales» de § 9.4, con la reserva
declarada en el libro: recepción y onomástica comparten con la estilometría el mismo texto, no la misma información.

## 2. Regla de § 9.4 (literal)

Una hipótesis queda **sostenida** si ningún canal la hace no compatible y al menos dos la hacen compatible;
**debilitada** si un canal la hace no compatible; **descartada** si dos o más la hacen no compatible; **abierta** en
los demás casos.

## 3. Hipótesis de partida (§ 10, solo las trece; Hebreos no tiene hipótesis previa, D-002)

**Refutada** si la carta queda fuera del rango intra-autor (nivel 2) en las dos medidas, con LR epistolar en contra
(nivel 1) y recepción u onomástica no compatibles con H1-H3; **debilitada** si se cumple la parte estilométrica sin
el otro canal; **abierta** con cualquier resultado indeterminado (nivel 3 indeterminado, nivel 1 discordante o
veredicto «sin decidir»); en los demás casos, **no refutada**.

## 4. Resultado (29-IX-2026)

- Rom, 1 Cor, 2 Cor, Gal, Flp, 1 Tes, Ef, Col, 2 Tes: H1, H2 y H3 sostenidas; H5 descartada (estilometría y
  recepción; en Rom, 1 Cor, Flp, Col también la onomástica); H4 debilitada por la estilometría y descartada en Rom y
  Flp (onomástica: más de la mitad de los nombres son nuevos y documentados). Hipótesis de partida no refutada.
- Flm: H2 y H3 sostenidas, H1 sostenida (recepción y onomástica compatibles; estilometría no decide por familias
  discordantes); H4 abierta; H5 descartada. Hipótesis de partida abierta (nivel 1 discordante).
- 1 Tim: H1-H3 sostenidas (recepción y onomástica); **H4 también sostenida** (recepción e institucional compatibles,
  ningún canal en contra); H5 descartada. Hipótesis de partida abierta (nivel 1 discordante).
- 2 Tim y Tit: H1-H3 sostenidas; H4 debilitada (onomástica: más de la mitad de los nombres son nuevos y documentados);
  H5 descartada. Hipótesis de partida abierta (2 Tim: nivel 3 indeterminado; Tit: nivel 1 discordante).
- Hebreos: H1-H3 descartadas (recepción: atribución negada en Occidente; onomástica: ausencia de prosopografía,
  23 de 24 nombres bíblicos); H4 y H5 sostenidas (recepción, institucional; onomástica para H5); la estilometría
  no decide (nivel 1 en contra, nivel 2 dentro). Sin hipótesis de partida: la tabla se informa y la contradicción
  entre la estilometría (dentro del rango) y los otros dos canales es el resultado.

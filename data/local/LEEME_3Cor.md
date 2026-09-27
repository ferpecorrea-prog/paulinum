# 3 Corintios (P. Bodmer X) — preparación del texto local

El archivo `data/local/3Cor.txt` **no está en esta reconstrucción**: el texto preparado del laboratorio
original (531 palabras, con su archivo de alineación de 105 intervenciones letra a letra) se perdió con él.
Hay que rehacerlo siguiendo el procedimiento que el libro describe (§ 8.1 y nota 48 de la Investigación 1):

1. **Fuente.** Transcripción diplomática de M. Testuz (ed.), *Papyrus Bodmer X-XII*, Cologny-Ginebra,
   Bibliotheca Bodmeriana, 1959, pp. 30-44 (páginas 50-57 del códice), tal como la reproduce la biblioteca
   digital de textos apócrifos de dhspriory.org; cotejable con V. Hovhanessian, *Third Corinthians*, Peter
   Lang, 2000, apéndice 2.
2. **Alcance.** Solo la **respuesta de Pablo** a los corintios (531 palabras en la tokenización del
   laboratorio); la carta de los corintios a Pablo queda fuera. (La Investigación 1 usó las 698 palabras
   de la transcripción completa; la Investigación 2, solo la respuesta.)
3. **Normalización**, registrando cada intervención en `3Cor_alineacion.tsv` (columnas: n, posición,
   forma_papiro, forma_normalizada, tipo): resolución de los *nomina sacra* (ΙΗΣ → Ἰησοῦς, ΧΡΣ → Χριστός,
   ΘΣ → θεός, ΚΣ → κύριος, ΠΝΑ → πνεῦμα, etc.); corrección del itacismo y de las grafías del copista a la
   ortografía estándar que siguen las demás fuentes (ει/ι, αι/ε, ο/ω); acentuación por sintaxis; **sin
   añadir palabra alguna ausente del papiro** (así se deja sin restituir «καὶ Κλεό-» ante «βιος»).
4. **Formato del archivo**: una línea por unidad de referencia, `ref<TAB>texto` (por ejemplo
   `1:1<TAB>Παῦλος ὁ δέσμιος Ἰησοῦ Χριστοῦ …`), UTF-8, o texto corrido (una referencia por línea).
5. **Registro.** `python -m paulinum fetch` anota la huella SHA-256 del archivo en `data/provenance.json`;
   añada al final de este LEEME la fecha, la fuente exacta consultada y la huella.

Estado del documento en el manifiesto (`paulinum/sources.py`, `THREE_COR`): autor «Ps-Pablo», estado
`spurious`, tradición cristiana; interviene solo como control de falsificación (problema `pseudo_pairs`
frente al núcleo) y como negativo frente a Pablo; **nunca como argumento a favor ni en contra de una carta
concreta** (regla preregistrada `tres_corintios`). Mientras el archivo no exista, `build` lo omite con
un aviso y todo lo demás se ejecuta igual.

Reserva ortográfica (regla preregistrada): la ortografía regularizada del copista introduce una
incertidumbre propia de este documento que no afecta a ningún otro.

## Registro de preparación (27-IX-2026)

- Fuente: transcripción diplomática electrónica de P. Bodmer X, pp. 50-57 (texto de Testuz 1959 reproducido por
  dhspriory.org), depositada por el autor en `3Cor_PBodmerX_Claude_package.zip` (SHA-256 de la transcripción
  `8ebec730f58ad6c07643ad399a15fcc8f2c905fefcbdad70323b081d2f5c7d46`); copia de la parte usada en
  `3Cor_diplomatica_respuesta_de_Pablo.txt`.
- Normalización: `scripts/preparar_3cor.py` sobre `3Cor_normalizada_fuente.txt`; alineación en `3Cor_alineacion.tsv`
  (531 filas); decisiones en `docs/3Cor_validacion_pendiente.md` y D-006/D-007.
- Resultado: `3Cor.txt`, 531 palabras, SHA-256 `04fd948567e980d1f94fd4656e964bea7da93cc299ba6a91ccaccba6934a3a42`,
  registrada por `python -m paulinum fetch --tier 1` en `data/provenance.json`.

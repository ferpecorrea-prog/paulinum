# Cotejo de la capa de trece lemas con el libro

Generado por `cotejo_con_el_libro.py` sobre `data/matriz_19x13.csv` (la matriz primaria impresa en la nota 43).
Cada fila compara el valor impreso en Investigación 1 (§ 4.4, notas 42-44) con el recalculado por
`recalcular_capa_13.py`. Tolerancia: 0,0005 (redondeo a tres decimales); 0,01 en los intervalos de
remuestreo de trece lemas y 0,02 en los de ocho (dependen del generador aleatorio); 0,6 lemas en los intervalos de predicción de Heaps (el libro los imprime redondeados a enteros).

**Resultado: 313 de 313 valores coinciden.**

Nota sobre las configuraciones de sensibilidad: el libro rotula la cuarta configuración como «8 conectores y
preposiciones». La búsqueda exhaustiva sobre todos los subconjuntos de 8 y de 7 lemas muestra que las cifras
impresas corresponden, de forma única, a {καί, ἐν, ὅς, εἰς, δέ, γάρ, οὐ, διά} y, sin οὐ, a
{καί, ἐν, ὅς, εἰς, δέ, γάρ, διά}: el depósito original incluía el relativo ὅς y excluía μή en esa configuración.
La reconstrucción adopta esa composición para reproducir las tablas; el rótulo del libro es, en rigor, inexacto.

Partición de Ward recalculada: `[[1Jn, [Ef, Col]], [Flm, [[[Sant, Jud], [1Tim, Tit]], [[[1Cor, Gal], [2Cor, 1Tes]], [[Rom, Heb], [[2Pe, [Flp, 2Tim]], [2Tes, 1Pe]]]]]]]`

| sección | valor | publicado | recalculado | coincide |
|---|---|---|---|---|
| Capa A (8 rasgos, núcleo 6) | 2Cor | 0.638 | 0.638 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Gal | 0.744 | 0.744 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Flp | 0.829 | 0.829 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Jud | 0.875 | 0.875 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 1Cor | 0.905 | 0.905 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 2Tes | 1.005 | 1.005 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 1Tes | 1.049 | 1.049 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 2Tim | 1.136 | 1.136 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Rom | 1.198 | 1.198 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Sant | 1.281 | 1.281 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 2Pe | 1.461 | 1.461 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Tit | 1.520 | 1.520 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 1Pe | 1.646 | 1.646 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Heb | 1.762 | 1.762 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 1Tim | 1.811 | 1.811 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Ef | 2.141 | 2.141 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Col | 2.264 | 2.264 | ✓ |
| Capa A (8 rasgos, núcleo 6) | Flm | 2.817 | 2.817 | ✓ |
| Capa A (8 rasgos, núcleo 6) | 1Jn | 3.197 | 3.197 | ✓ |
| Capa B (13, núcleo 6) | 2Cor | 0.598 | 0.598 | ✓ |
| Capa B (13, núcleo 6) | Gal | 0.629 | 0.629 | ✓ |
| Capa B (13, núcleo 6) | 1Tes | 0.945 | 0.945 | ✓ |
| Capa B (13, núcleo 6) | 1Cor | 0.989 | 0.989 | ✓ |
| Capa B (13, núcleo 6) | Flp | 1.076 | 1.076 | ✓ |
| Capa B (13, núcleo 6) | Rom | 1.104 | 1.104 | ✓ |
| Capa B (13, núcleo 6) | 2Tim | 1.108 | 1.108 | ✓ |
| Capa B (13, núcleo 6) | 2Tes | 1.190 | 1.190 | ✓ |
| Capa B (13, núcleo 6) | 2Pe | 1.262 | 1.262 | ✓ |
| Capa B (13, núcleo 6) | Sant | 1.452 | 1.452 | ✓ |
| Capa B (13, núcleo 6) | Heb | 1.457 | 1.457 | ✓ |
| Capa B (13, núcleo 6) | Jud | 1.514 | 1.514 | ✓ |
| Capa B (13, núcleo 6) | 1Pe | 1.520 | 1.520 | ✓ |
| Capa B (13, núcleo 6) | Tit | 1.733 | 1.733 | ✓ |
| Capa B (13, núcleo 6) | 1Tim | 1.754 | 1.754 | ✓ |
| Capa B (13, núcleo 6) | Ef | 1.990 | 1.990 | ✓ |
| Capa B (13, núcleo 6) | Col | 2.138 | 2.138 | ✓ |
| Capa B (13, núcleo 6) | Flm | 2.433 | 2.433 | ✓ |
| Capa B (13, núcleo 6) | 1Jn | 2.854 | 2.854 | ✓ |
| Capa B (13, núcleo 7) | 2Cor | 0.504 | 0.504 | ✓ |
| Capa B (13, núcleo 7) | Gal | 0.682 | 0.682 | ✓ |
| Capa B (13, núcleo 7) | 1Tes | 0.796 | 0.796 | ✓ |
| Capa B (13, núcleo 7) | 1Cor | 0.989 | 0.989 | ✓ |
| Capa B (13, núcleo 7) | Flp | 0.920 | 0.920 | ✓ |
| Capa B (13, núcleo 7) | Rom | 1.004 | 1.004 | ✓ |
| Capa B (13, núcleo 7) | 2Tim | 0.705 | 0.705 | ✓ |
| Capa B (13, núcleo 7) | 2Tes | 0.918 | 0.918 | ✓ |
| Capa B (13, núcleo 7) | 2Pe | 1.089 | 1.089 | ✓ |
| Capa B (13, núcleo 7) | Sant | 1.371 | 1.371 | ✓ |
| Capa B (13, núcleo 7) | Heb | 1.348 | 1.348 | ✓ |
| Capa B (13, núcleo 7) | Jud | 1.342 | 1.342 | ✓ |
| Capa B (13, núcleo 7) | 1Pe | 1.182 | 1.182 | ✓ |
| Capa B (13, núcleo 7) | Tit | 1.500 | 1.500 | ✓ |
| Capa B (13, núcleo 7) | 1Tim | 1.380 | 1.380 | ✓ |
| Capa B (13, núcleo 7) | Ef | 1.782 | 1.782 | ✓ |
| Capa B (13, núcleo 7) | Col | 1.960 | 1.960 | ✓ |
| Capa B (13, núcleo 7) | 1Jn | 2.643 | 2.643 | ✓ |
| Sensibilidad | Rom · 13 | 1.104 | 1.104 | ✓ |
| Sensibilidad | Rom · 11 sin ἐγώ/σύ | 1.114 | 1.114 | ✓ |
| Sensibilidad | Rom · 10 sin art. | 1.018 | 1.018 | ✓ |
| Sensibilidad | Rom · 8 conect./prep. | 0.984 | 0.984 | ✓ |
| Sensibilidad | Rom · 7 sin οὐ | 1.050 | 1.050 | ✓ |
| Sensibilidad | 1Cor · 13 | 0.989 | 0.989 | ✓ |
| Sensibilidad | 1Cor · 11 sin ἐγώ/σύ | 1.010 | 1.010 | ✓ |
| Sensibilidad | 1Cor · 10 sin art. | 1.058 | 1.058 | ✓ |
| Sensibilidad | 1Cor · 8 conect./prep. | 1.074 | 1.074 | ✓ |
| Sensibilidad | 1Cor · 7 sin οὐ | 1.037 | 1.037 | ✓ |
| Sensibilidad | 2Cor · 13 | 0.598 | 0.598 | ✓ |
| Sensibilidad | 2Cor · 11 sin ἐγώ/σύ | 0.565 | 0.565 | ✓ |
| Sensibilidad | 2Cor · 10 sin art. | 0.573 | 0.573 | ✓ |
| Sensibilidad | 2Cor · 8 conect./prep. | 0.604 | 0.604 | ✓ |
| Sensibilidad | 2Cor · 7 sin οὐ | 0.585 | 0.585 | ✓ |
| Sensibilidad | Gal · 13 | 0.629 | 0.629 | ✓ |
| Sensibilidad | Gal · 11 sin ἐγώ/σύ | 0.668 | 0.668 | ✓ |
| Sensibilidad | Gal · 10 sin art. | 0.690 | 0.690 | ✓ |
| Sensibilidad | Gal · 8 conect./prep. | 0.675 | 0.675 | ✓ |
| Sensibilidad | Gal · 7 sin οὐ | 0.721 | 0.721 | ✓ |
| Sensibilidad | Flp · 13 | 1.076 | 1.076 | ✓ |
| Sensibilidad | Flp · 11 sin ἐγώ/σύ | 1.136 | 1.136 | ✓ |
| Sensibilidad | Flp · 10 sin art. | 1.138 | 1.138 | ✓ |
| Sensibilidad | Flp · 8 conect./prep. | 1.063 | 1.063 | ✓ |
| Sensibilidad | Flp · 7 sin οὐ | 0.977 | 0.977 | ✓ |
| Sensibilidad | 1Tes · 13 | 0.945 | 0.945 | ✓ |
| Sensibilidad | 1Tes · 11 sin ἐγώ/σύ | 0.828 | 0.828 | ✓ |
| Sensibilidad | 1Tes · 10 sin art. | 0.863 | 0.863 | ✓ |
| Sensibilidad | 1Tes · 8 conect./prep. | 0.964 | 0.964 | ✓ |
| Sensibilidad | 1Tes · 7 sin οὐ | 1.002 | 1.002 | ✓ |
| Sensibilidad | 2Tes · 13 | 1.190 | 1.190 | ✓ |
| Sensibilidad | 2Tes · 11 sin ἐγώ/σύ | 1.219 | 1.219 | ✓ |
| Sensibilidad | 2Tes · 10 sin art. | 1.278 | 1.278 | ✓ |
| Sensibilidad | 2Tes · 8 conect./prep. | 1.322 | 1.322 | ✓ |
| Sensibilidad | 2Tes · 7 sin οὐ | 1.337 | 1.337 | ✓ |
| Sensibilidad | 2Tim · 13 | 1.108 | 1.108 | ✓ |
| Sensibilidad | 2Tim · 11 sin ἐγώ/σύ | 1.175 | 1.175 | ✓ |
| Sensibilidad | 2Tim · 10 sin art. | 1.218 | 1.218 | ✓ |
| Sensibilidad | 2Tim · 8 conect./prep. | 1.188 | 1.188 | ✓ |
| Sensibilidad | 2Tim · 7 sin οὐ | 1.194 | 1.194 | ✓ |
| Sensibilidad | Heb · 13 | 1.457 | 1.457 | ✓ |
| Sensibilidad | Heb · 11 sin ἐγώ/σύ | 1.388 | 1.388 | ✓ |
| Sensibilidad | Heb · 10 sin art. | 1.392 | 1.392 | ✓ |
| Sensibilidad | Heb · 8 conect./prep. | 0.970 | 0.970 | ✓ |
| Sensibilidad | Heb · 7 sin οὐ | 1.023 | 1.023 | ✓ |
| Sensibilidad | Tit · 13 | 1.733 | 1.733 | ✓ |
| Sensibilidad | Tit · 11 sin ἐγώ/σύ | 1.844 | 1.844 | ✓ |
| Sensibilidad | Tit · 10 sin art. | 1.738 | 1.738 | ✓ |
| Sensibilidad | Tit · 8 conect./prep. | 1.627 | 1.627 | ✓ |
| Sensibilidad | Tit · 7 sin οὐ | 1.466 | 1.466 | ✓ |
| Sensibilidad | 1Tim · 13 | 1.754 | 1.754 | ✓ |
| Sensibilidad | 1Tim · 11 sin ἐγώ/σύ | 1.684 | 1.684 | ✓ |
| Sensibilidad | 1Tim · 10 sin art. | 1.609 | 1.609 | ✓ |
| Sensibilidad | 1Tim · 8 conect./prep. | 1.361 | 1.361 | ✓ |
| Sensibilidad | 1Tim · 7 sin οὐ | 1.286 | 1.286 | ✓ |
| Sensibilidad | Ef · 13 | 1.990 | 1.990 | ✓ |
| Sensibilidad | Ef · 11 sin ἐγώ/σύ | 2.085 | 2.085 | ✓ |
| Sensibilidad | Ef · 10 sin art. | 1.752 | 1.752 | ✓ |
| Sensibilidad | Ef · 8 conect./prep. | 1.628 | 1.628 | ✓ |
| Sensibilidad | Ef · 7 sin οὐ | 1.571 | 1.571 | ✓ |
| Sensibilidad | Col · 13 | 2.138 | 2.138 | ✓ |
| Sensibilidad | Col · 11 sin ἐγώ/σύ | 2.270 | 2.270 | ✓ |
| Sensibilidad | Col · 10 sin art. | 2.147 | 2.147 | ✓ |
| Sensibilidad | Col · 8 conect./prep. | 2.046 | 2.046 | ✓ |
| Sensibilidad | Col · 7 sin οὐ | 2.066 | 2.066 | ✓ |
| Sensibilidad | Flm · 13 | 2.433 | 2.433 | ✓ |
| Sensibilidad | Flm · 11 sin ἐγώ/σύ | 1.833 | 1.833 | ✓ |
| Sensibilidad | Flm · 10 sin art. | 1.778 | 1.778 | ✓ |
| Sensibilidad | Flm · 8 conect./prep. | 1.849 | 1.849 | ✓ |
| Sensibilidad | Flm · 7 sin οὐ | 1.687 | 1.687 | ✓ |
| Sensibilidad | Sant · 13 | 1.452 | 1.452 | ✓ |
| Sensibilidad | Sant · 11 sin ἐγώ/σύ | 1.439 | 1.439 | ✓ |
| Sensibilidad | Sant · 10 sin art. | 1.507 | 1.507 | ✓ |
| Sensibilidad | Sant · 8 conect./prep. | 1.495 | 1.495 | ✓ |
| Sensibilidad | Sant · 7 sin οὐ | 1.596 | 1.596 | ✓ |
| Sensibilidad | 1Pe · 13 | 1.520 | 1.520 | ✓ |
| Sensibilidad | 1Pe · 11 sin ἐγώ/σύ | 1.309 | 1.309 | ✓ |
| Sensibilidad | 1Pe · 10 sin art. | 1.350 | 1.350 | ✓ |
| Sensibilidad | 1Pe · 8 conect./prep. | 1.451 | 1.451 | ✓ |
| Sensibilidad | 1Pe · 7 sin οὐ | 1.452 | 1.452 | ✓ |
| Sensibilidad | 2Pe · 13 | 1.262 | 1.262 | ✓ |
| Sensibilidad | 2Pe · 11 sin ἐγώ/σύ | 1.268 | 1.268 | ✓ |
| Sensibilidad | 2Pe · 10 sin art. | 1.267 | 1.267 | ✓ |
| Sensibilidad | 2Pe · 8 conect./prep. | 0.912 | 0.912 | ✓ |
| Sensibilidad | 2Pe · 7 sin οὐ | 0.909 | 0.909 | ✓ |
| Sensibilidad | 1Jn · 13 | 2.854 | 2.854 | ✓ |
| Sensibilidad | 1Jn · 11 sin ἐγώ/σύ | 3.091 | 3.091 | ✓ |
| Sensibilidad | 1Jn · 10 sin art. | 3.037 | 3.037 | ✓ |
| Sensibilidad | 1Jn · 8 conect./prep. | 1.948 | 1.948 | ✓ |
| Sensibilidad | 1Jn · 7 sin οὐ | 2.056 | 2.056 | ✓ |
| Sensibilidad | Jud · 13 | 1.514 | 1.514 | ✓ |
| Sensibilidad | Jud · 11 sin ἐγώ/σύ | 1.558 | 1.558 | ✓ |
| Sensibilidad | Jud · 10 sin art. | 1.625 | 1.625 | ✓ |
| Sensibilidad | Jud · 8 conect./prep. | 1.772 | 1.772 | ✓ |
| Sensibilidad | Jud · 7 sin οὐ | 1.737 | 1.737 | ✓ |
| LOO | 2Tim mín | 0.640 | 0.640 | ✓ |
| LOO | 2Tim mediana | 0.671 | 0.671 | ✓ |
| LOO | 2Tim máx | 1.108 | 1.108 | ✓ |
| LOO | 2Tim desv. típ. | 0.183 | 0.183 | ✓ |
| LOO | 2Tes mín | 0.815 | 0.815 | ✓ |
| LOO | 2Tes mediana | 0.938 | 0.938 | ✓ |
| LOO | 2Tes máx | 1.190 | 1.190 | ✓ |
| LOO | 2Tes desv. típ. | 0.141 | 0.141 | ✓ |
| LOO | 2Pe mín | 1.000 | 1.000 | ✓ |
| LOO | 2Pe mediana | 1.096 | 1.096 | ✓ |
| LOO | 2Pe máx | 1.325 | 1.325 | ✓ |
| LOO | 2Pe desv. típ. | 0.131 | 0.131 | ✓ |
| LOO | 1Pe mín | 1.102 | 1.102 | ✓ |
| LOO | 1Pe mediana | 1.256 | 1.256 | ✓ |
| LOO | 1Pe máx | 1.520 | 1.520 | ✓ |
| LOO | 1Pe desv. típ. | 0.143 | 0.143 | ✓ |
| LOO | Heb mín | 1.248 | 1.248 | ✓ |
| LOO | Heb mediana | 1.355 | 1.355 | ✓ |
| LOO | Heb máx | 1.772 | 1.772 | ✓ |
| LOO | Heb desv. típ. | 0.179 | 0.179 | ✓ |
| LOO | Jud mín | 1.207 | 1.207 | ✓ |
| LOO | Jud mediana | 1.414 | 1.414 | ✓ |
| LOO | Jud máx | 1.516 | 1.516 | ✓ |
| LOO | Jud desv. típ. | 0.114 | 0.114 | ✓ |
| LOO | Sant mín | 1.238 | 1.238 | ✓ |
| LOO | Sant mediana | 1.416 | 1.416 | ✓ |
| LOO | Sant máx | 1.554 | 1.554 | ✓ |
| LOO | Sant desv. típ. | 0.109 | 0.109 | ✓ |
| LOO | 1Tim mín | 1.264 | 1.264 | ✓ |
| LOO | 1Tim mediana | 1.418 | 1.418 | ✓ |
| LOO | 1Tim máx | 1.754 | 1.754 | ✓ |
| LOO | 1Tim desv. típ. | 0.162 | 0.162 | ✓ |
| LOO | Tit mín | 1.390 | 1.390 | ✓ |
| LOO | Tit mediana | 1.475 | 1.475 | ✓ |
| LOO | Tit máx | 1.779 | 1.779 | ✓ |
| LOO | Tit desv. típ. | 0.155 | 0.155 | ✓ |
| LOO | Ef mín | 1.665 | 1.665 | ✓ |
| LOO | Ef mediana | 1.764 | 1.764 | ✓ |
| LOO | Ef máx | 2.216 | 2.216 | ✓ |
| LOO | Ef desv. típ. | 0.211 | 0.211 | ✓ |
| LOO | Col mín | 1.850 | 1.850 | ✓ |
| LOO | Col mediana | 1.973 | 1.973 | ✓ |
| LOO | Col máx | 2.301 | 2.301 | ✓ |
| LOO | Col desv. típ. | 0.175 | 0.175 | ✓ |
| LOO | 1Jn mín | 2.430 | 2.430 | ✓ |
| LOO | 1Jn mediana | 2.642 | 2.642 | ✓ |
| LOO | 1Jn máx | 3.398 | 3.398 | ✓ |
| LOO | 1Jn desv. típ. | 0.330 | 0.330 | ✓ |
| LOO núcleo (cada indiscutida fuera) | 2Cor | 0.566 | 0.566 | ✓ |
| LOO núcleo (cada indiscutida fuera) | Gal | 0.841 | 0.841 | ✓ |
| LOO núcleo (cada indiscutida fuera) | 1Tes | 1.008 | 1.008 | ✓ |
| LOO núcleo (cada indiscutida fuera) | Flp | 1.251 | 1.251 | ✓ |
| LOO núcleo (cada indiscutida fuera) | 1Cor | 1.377 | 1.377 | ✓ |
| LOO núcleo (cada indiscutida fuera) | Rom | 1.397 | 1.397 | ✓ |
| LOO núcleo (cada indiscutida fuera) | Flm | 2.433 | 2.433 | ✓ |
| Remuestreo 13 (IC 95 %) | 2Tim inf | 0.905 | 0.905 | ✓ |
| Remuestreo 13 (IC 95 %) | 2Tim sup | 1.768 | 1.768 | ✓ |
| Remuestreo 13 (IC 95 %) | 2Tes inf | 1.036 | 1.036 | ✓ |
| Remuestreo 13 (IC 95 %) | 2Tes sup | 2.031 | 2.031 | ✓ |
| Remuestreo 13 (IC 95 %) | 2Pe inf | 1.015 | 1.015 | ✓ |
| Remuestreo 13 (IC 95 %) | 2Pe sup | 1.969 | 1.969 | ✓ |
| Remuestreo 13 (IC 95 %) | Heb inf | 1.267 | 1.267 | ✓ |
| Remuestreo 13 (IC 95 %) | Heb sup | 1.757 | 1.757 | ✓ |
| Remuestreo 13 (IC 95 %) | Sant inf | 1.278 | 1.278 | ✓ |
| Remuestreo 13 (IC 95 %) | Sant sup | 1.846 | 1.846 | ✓ |
| Remuestreo 13 (IC 95 %) | 1Pe inf | 1.350 | 1.350 | ✓ |
| Remuestreo 13 (IC 95 %) | 1Pe sup | 1.977 | 1.977 | ✓ |
| Remuestreo 13 (IC 95 %) | Jud inf | 1.414 | 1.414 | ✓ |
| Remuestreo 13 (IC 95 %) | Jud sup | 2.235 | 2.235 | ✓ |
| Remuestreo 13 (IC 95 %) | Tit inf | 1.474 | 1.474 | ✓ |
| Remuestreo 13 (IC 95 %) | Tit sup | 2.519 | 2.519 | ✓ |
| Remuestreo 13 (IC 95 %) | 1Tim inf | 1.557 | 1.557 | ✓ |
| Remuestreo 13 (IC 95 %) | 1Tim sup | 2.122 | 2.122 | ✓ |
| Remuestreo 13 (IC 95 %) | Ef inf | 1.753 | 1.753 | ✓ |
| Remuestreo 13 (IC 95 %) | Ef sup | 2.372 | 2.372 | ✓ |
| Remuestreo 13 (IC 95 %) | Col inf | 1.872 | 1.872 | ✓ |
| Remuestreo 13 (IC 95 %) | Col sup | 2.613 | 2.613 | ✓ |
| Remuestreo 13 (IC 95 %) | Flm inf | 2.009 | 2.009 | ✓ |
| Remuestreo 13 (IC 95 %) | Flm sup | 3.698 | 3.698 | ✓ |
| Remuestreo 13 (IC 95 %) | 1Jn inf | 2.435 | 2.435 | ✓ |
| Remuestreo 13 (IC 95 %) | 1Jn sup | 3.392 | 3.392 | ✓ |
| Remuestreo 8 (IC 95 %) | 2Tes inf | 0.747 | 0.748 | ✓ |
| Remuestreo 8 (IC 95 %) | 2Tes sup | 2.001 | 1.995 | ✓ |
| Remuestreo 8 (IC 95 %) | 2Tim inf | 0.742 | 0.751 | ✓ |
| Remuestreo 8 (IC 95 %) | 2Tim sup | 1.952 | 1.955 | ✓ |
| Remuestreo 8 (IC 95 %) | Tit inf | 1.213 | 1.204 | ✓ |
| Remuestreo 8 (IC 95 %) | Tit sup | 2.279 | 2.288 | ✓ |
| Remuestreo 8 (IC 95 %) | 1Tim inf | 1.554 | 1.556 | ✓ |
| Remuestreo 8 (IC 95 %) | 1Tim sup | 2.226 | 2.228 | ✓ |
| Remuestreo 8 (IC 95 %) | Heb inf | 1.495 | 1.497 | ✓ |
| Remuestreo 8 (IC 95 %) | Heb sup | 2.116 | 2.124 | ✓ |
| Remuestreo 8 (IC 95 %) | Ef inf | 1.781 | 1.768 | ✓ |
| Remuestreo 8 (IC 95 %) | Ef sup | 2.636 | 2.641 | ✓ |
| Remuestreo 8 (IC 95 %) | Col inf | 1.840 | 1.828 | ✓ |
| Remuestreo 8 (IC 95 %) | Col sup | 2.909 | 2.910 | ✓ |
| Remuestreo 8 (IC 95 %) | Flm inf | 2.051 | 2.044 | ✓ |
| Remuestreo 8 (IC 95 %) | Flm sup | 4.288 | 4.281 | ✓ |
| Heaps | a | 1.209 | 1.209 | ✓ |
| Heaps | b | 0.648 | 0.648 | ✓ |
| Heaps | R² | 0.993 | 0.993 | ✓ |
| Heaps | Cook (Flm) | 2.675 | 2.675 | ✓ |
| Heaps | a sin Flm | 1.630 | 1.630 | ✓ |
| Heaps | b sin Flm | 0.597 | 0.597 | ✓ |
| Heaps IP95 | Ef inf | 457.000 | 456.765 | ✓ |
| Heaps IP95 | Ef sup | 651.000 | 651.113 | ✓ |
| Heaps IP95 | Col inf | 346.000 | 345.681 | ✓ |
| Heaps IP95 | Col sup | 495.000 | 494.495 | ✓ |
| Heaps IP95 | 2Tes inf | 231.000 | 230.810 | ✓ |
| Heaps IP95 | 2Tes sup | 336.000 | 336.338 | ✓ |
| Heaps IP95 | 1Tim inf | 347.000 | 346.890 | ✓ |
| Heaps IP95 | 1Tim sup | 496.000 | 496.179 | ✓ |
| Heaps IP95 | 2Tim inf | 294.000 | 293.935 | ✓ |
| Heaps IP95 | 2Tim sup | 423.000 | 422.849 | ✓ |
| Heaps IP95 | Tit inf | 190.000 | 190.342 | ✓ |
| Heaps IP95 | Tit sup | 281.000 | 281.187 | ✓ |
| Heaps IP95 | Heb inf | 715.000 | 715.097 | ✓ |
| Heaps IP95 | Heb sup | 1031.000 | 1031.398 | ✓ |
| Heaps IP95 | Sant inf | 366.000 | 365.531 | ✓ |
| Heaps IP95 | Sant sup | 522.000 | 522.189 | ✓ |
| Heaps IP95 | 1Pe inf | 357.000 | 356.611 | ✓ |
| Heaps IP95 | 1Pe sup | 510.000 | 509.729 | ✓ |
| Heaps IP95 | 2Pe inf | 270.000 | 270.100 | ✓ |
| Heaps IP95 | 2Pe sup | 390.000 | 390.086 | ✓ |
| Heaps IP95 | Jud inf | 149.000 | 148.593 | ✓ |
| Heaps IP95 | Jud sup | 224.000 | 224.259 | ✓ |
| Heaps IP95 | 1Jn inf | 426.000 | 425.742 | ✓ |
| Heaps IP95 | 1Jn sup | 607.000 | 606.963 | ✓ |
| Heaps residuo log | 1Tim | 0.314 | 0.314 | ✓ |
| Heaps residuo log | Tit | 0.305 | 0.305 | ✓ |
| Heaps residuo log | 2Tim | 0.264 | 0.264 | ✓ |
| Heaps residuo log | Heb | 0.222 | 0.222 | ✓ |
| Heaps residuo log | Sant | 0.283 | 0.283 | ✓ |
| Heaps residuo log | 1Pe | 0.276 | 0.276 | ✓ |
| Heaps residuo log | 2Pe | 0.251 | 0.251 | ✓ |
| Heaps residuo log | Jud | 0.244 | 0.244 | ✓ |
| Heaps sin Flm IP95 | Tit inf | 204.000 | 204.056 | ✓ |
| Heaps sin Flm IP95 | Tit sup | 315.000 | 314.618 | ✓ |
| PCA | PC1 | 0.375 | 0.375 | ✓ |
| PCA | PC2 | 0.200 | 0.200 | ✓ |
| Pares | Ef-Col | 0.678 | 0.678 | ✓ |
| Pares | Rom-Heb | 0.899 | 0.899 | ✓ |
| Pares | 1Tim-Tit | 1.232 | 1.232 | ✓ |
| Pares | 1Tes-2Tes | 1.406 | 1.406 | ✓ |
| Pares | 1Tim-2Tim | 1.699 | 1.699 | ✓ |
| Pares | 2Tim-Tit | 1.870 | 1.870 | ✓ |
| Pares | Flm-2Tim | 2.095 | 2.095 | ✓ |
| Capa A sin ἐγώ/σύ | Flm | 1.978 | 1.978 | ✓ |
| Capa A sin ἐγώ/σύ | Col | 2.527 | 2.527 | ✓ |
| Capa A sin ἐγώ/σύ | Ef | 2.346 | 2.346 | ✓ |
| Capa A sin ἐγώ/σύ | Heb | 1.754 | 1.754 | ✓ |
| Capa A sin ἐγώ/σύ | 1Tim | 1.706 | 1.706 | ✓ |
| Capa A sin ἐγώ/σύ | Tit | 1.676 | 1.676 | ✓ |
| Capa A Judas | sin pronombres | 0.713 | 0.713 | ✓ |
| Capa A Judas | sin pron. ni artículo | 0.740 | 0.740 | ✓ |
| Capa A Judas | solo conect./prep. (καί ἐν ὅς εἰς) | 0.780 | 0.780 | ✓ |
| Capa A Judas | suelo de ruido multinomial | 1.143 | 1.143 | ✓ |
| Capa A Judas | boot mediana | 1.357 | 1.352 | ✓ |
| Capa A Judas | boot IC inf | 0.819 | 0.832 | ✓ |
| Capa A Judas | boot IC sup | 2.038 | 2.032 | ✓ |
| Capa A subconjuntos | n subconjuntos (=219) | 219.000 | 219.000 | ✓ |
| Capa A subconjuntos | Judas bajo ≥4 del núcleo (fracción) | 0.379 | 0.379 | ✓ |
| Capa A subconjuntos | Flm máxima de las 14 (fracción) | 0.758 | 0.758 | ✓ |

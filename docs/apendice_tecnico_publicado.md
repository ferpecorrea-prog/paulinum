<!-- Apéndice técnico (A.1-A.6) de la Parte II, reproducido del libro: es la especificación a partir de la cual se ha reconstruido este laboratorio. -->

**Apéndice técnico. Reproducción de la investigación**

Este apéndice contiene lo necesario para comprobar cada afirmación de los capítulos 7 a 12 y para repetir la investigación entera. Todo el material ---código, configuraciones, metadatos, resultados, informes y bitácoras--- se distribuye en la carpeta paulinum_lab que acompaña al libro; las rutas que se citan son relativas a ella.

**A.1. El software paulinum**

*Lenguaje y dependencias.* Python 3.10 o superior; numpy 2.2.6, scipy 1.15.3, pandas 2.3.3, scikit-learn 1.7.2, matplotlib 3.10.9, lxml 6.1.1, pyyaml 6.0.3, requests 2.34.2, tqdm 4.70.0, pytest 9.1.1. Las versiones importan: con ellas, dos ordenadores distintos producen resultados idénticos.

*Módulos del paquete paulinum/.* sources.py (manifiesto de los textos: identificador, autor, obra, género, subgénero, destinatario, fecha, estado, tradición, edición, repositorio, licencia; listas NT, AF, CONTROLS y CONTROLS_03); fetch.py (descarga y registro de huellas en data/provenance.json); parsers.py (MorphGNT, Open Apostolic Fathers, TEI de Perseus y First1KGreek, PROIEL, MACULA, Diorisis); text.py (normalización de formas, sigma final, acento grave y agudo, filtro de letras griegas, conversión de Beta Code); corpus.py (construcción de los documentos con sus capas, división en obras y partes, máscaras por referencia y por índice); features.py (espacios de rasgos: palabras frecuentes, clase cerrada, trigramas y tetragramas de caracteres, lemas de la anotación y lemas del diccionario uniforme; exclusión de la persona gramatical; descriptivos); distances.py (Delta, min-max, coseno, Eder, Manhattan, euclídea, Labbé); verify.py (impostores generales con ventanas de igual longitud; construcción de los problemas de calibración; AUC, c@1, banda de indecisión, tasas de error, razón de verosimilitud por densidades, escala verbal); variables.py (PERMANOVA, coordenadas principales, dbRDA, envolvente intra-autor, mismo rasero); rolling.py (ventanas deslizantes); pipeline.py (rejilla de especificaciones, etapas reanudables, ruido de edición, contribuciones de rasgos, resumen por carta); report.py (informe automático y figuras); cli.py y \_\_main\_\_.py (órdenes fetch, build, inventory, selftest, seal, run, report).

*Guiones de scripts/.* selftest.py (pruebas de referencia); run_all.py; calibracion_secundaria.py (razón de verosimilitud con negativos cristianos o cristianos y judeo-helenísticos); construir_lexicon.py (diccionario uniforme forma → lema a partir de MorphGNT, PROIEL y Diorisis); detectar_reutilizacion.py (tramos paralelos entre pares de cartas); variables_controles.py (anotación de los controles y PERMANOVA por autor); bootstrap_percentil.py (intervalos del percentil por remuestreo de autores y de ventanas, y leave-one-author-out); modelo_svm.py (máquina de vectores de soporte lineal calibrada y regresión logística con validación por autor); cobertura_lexicon.py, controles_genero.py y lectura_modelo_svm.py (lecturas posteriores al sellado, que solo leen resultados).

*Órdenes para repetir la campaña 03.* python -m paulinum fetch \--tier 2; python -m paulinum build \--config config/campana_03.yaml; python -m paulinum inventory \--config config/campana_03.yaml; python scripts/construir_lexicon.py \--diorisis-zip \<ruta a Diorisis.zip\>; python scripts/detectar_reutilizacion.py \--run campana_03; python scripts/variables_controles.py \--run campana_03; python -m paulinum seal \--config config/campana_03.yaml \--run campana_03 (debe devolver la huella de A.3); python -m paulinum run \--config config/campana_03.yaml; python scripts/calibracion_secundaria.py \--run campana_03; python scripts/bootstrap_percentil.py \--run campana_03 \--metric minmax (y \--metric delta); python scripts/modelo_svm.py \--run campana_03 \--features mfw:300,closed:150,char3:600,lemma_dict:300; python scripts/controles_genero.py \--run campana_03; python -m paulinum report \--run campana_03. Para la campaña 01, las mismas órdenes con config/default.yaml y \--run campana_01; para las cinco subcampañas de robustez, con config/campana_02a_nucleos.yaml a config/campana_02e_coseno.yaml.

*Parámetros comunes.* Cien iteraciones por problema en las campañas 01 y 02 y trescientas en la 03; en cada iteración, el 50 % de los rasgos, treinta impostores y una ventana aleatoria de quinientas palabras por documento; exclusión de las formas de primera y segunda persona; envolvente del mismo rasero con ventanas de quinientas palabras, veinte sorteos y tope de 120 pares por autor; ventanas deslizantes de cuatrocientas palabras con paso de cien y sesenta iteraciones; PERMANOVA con 499 permutaciones dentro de Pablo y 299 dentro de cada control; bootstrap con 2.000 remuestreos de autores y 100 réplicas de ventanas; segundo modelo con tope de veinte ventanas por documento y ciento veinte por autor, validación GroupKFold de diez pliegues por autor y leave-one-letter-out para el núcleo.

**A.2. El corpus**

*Fuentes.* MorphGNT/SBLGNT 6.12 (github.com/morphgnt/sblgnt; SBLGNT © Society of Biblical Literature y Logos Bible Software; MorphGNT CC BY-SA 3.0); Open Apostolic Fathers, texto de Lake (github.com/jtauber/apostolic-fathers); PROIEL, greek-nt.xml (Tischendorf); MACULA Greek (Clear Bible), SBLGNT y Nestle 1904; Perseus canonical-greekLit (CC BY-SA 4.0); Open Greek and Latin, First1KGreek (CC BY-SA 4.0); Diorisis (Vatri y McGillivray; CC BY-NC-SA 4.0), usado solo para el diccionario de lemas; papiro Bodmer X según la transcripción indicada en el capítulo 8. Las huellas SHA-256 de cada archivo descargado están en data/provenance.json; las ediciones de cada obra, en el encabezamiento TEI de cada archivo y en paulinum/sources.py.

*Composición por autor, tradición y estado (campaña 03; results/campana_03/inventory.csv).*

  ----------------------------------------------------------------------------------------
  autor                      tradición           estado        documentos    palabras
  -------------------------- ------------------- ------------- ------------- -------------
  Atenágoras                 cristiano           disputed      1             8922

  Atenágoras                 cristiano           genuine       1             11315

  Clemente Romano            cristiano           duplicate     1             9830

  Clemente Romano            cristiano           genuine       1             9831

  Clemente de Alejandría     cristiano           genuine       5             89855

  Hermas                     cristiano           genuine       1             27337

  Ignacio                    cristiano           duplicate     7             7764

  Ignacio                    cristiano           genuine       7             7746

  Juan(anon)                 cristiano           disputed      1             2137

  Juan(anon)                 cristiano           genuine       1             15438

  Juan(presb.)               cristiano           other         2             464

  Juan(vidente)              cristiano           other         1             9833

  Judas(?)                   cristiano           other         1             459

  Justino                    cristiano           genuine       42            32048

  Lucas(anon)                cristiano           genuine       2             37858

  Marcos(anon)               cristiano           other         1             11286

  Mateo(anon)                cristiano           other         1             18329

  Orígenes                   cristiano           genuine       12            209905

  Pablo                      cristiano           core          7             23999

  Pablo?                     cristiano           target        6             8301

  Pedro(?)                   cristiano           other         2             2776

  Policarpo                  cristiano           genuine       1             1131

  Ps-Bernabé                 cristiano           spurious      1             6714

  Ps-Clemente                cristiano           spurious      3             6011

  Ps-Ignacio                 cristiano           mixed         7             13062

  Ps-Ignacio                 cristiano           spurious      6             6248

  Ps-Pablo                   cristiano           spurious      1             531

  Santiago(?)                cristiano           other         1             1739

  Taciano                    cristiano           genuine       1             10230

  Teófilo de Antioquía       cristiano           genuine       3             21590

  anon                       cristiano           other         4             12385

  anon(Acta Thomae)          cristiano           other         1             28931

  anon(Passio Perpetuae)     cristiano           other         1             3981

  Filón                      judeo-helenistico   disputed      1             9196

  Filón                      judeo-helenistico   genuine       37            408836

  Josefo                     judeo-helenistico   genuine       30            473436

  anon(Enoch)                judeo-helenistico   other         1             5711

  anon(Test. Abrahae)        judeo-helenistico   other         1             6959

  anon(Vitae Prophetarum)    judeo-helenistico   other         1             4083

  Alcifrón                   pagano              genuine       1             20504

  Arriano                    pagano              genuine       8             92334

  Arriano                    pagano              other         1             196

  Demóstenes/Ps-Demóstenes   pagano              disputed      5             5963

  Elio Aristides             pagano              genuine       6             97904

  Epicteto(ap. Arriano)      pagano              genuine       5             80161

  Filóstrato                 pagano              genuine       1             7595

  Galo César                 pagano              other         1             240

  Isócrates                  pagano              genuine       13            49151

  Juliano                    pagano              genuine       37            18975

  Libanio                    pagano              genuine       44            12130

  Luciano                    pagano              genuine       5             25854

  Marco Aurelio              pagano              genuine       12            29267

  Platón/Ps-Platón           pagano              disputed      11            16808

  Plutarco                   pagano              genuine       7             46575

  Polemón                    pagano              genuine       1             6060

  Ps-Diógenes                pagano              spurious      15            6071

  Ps-Eurípides               pagano              spurious      5             1820

  Ps-Juliano                 pagano              spurious      8             4820

  Ps-Plutarco                pagano              disputed      1             9234

  Ps-Plutarco                pagano              spurious      2             9555

  Ps-Solón                   pagano              spurious      1             227

  Vetio Valente              pagano              genuine       9             103551

  anon(Hermetica)            pagano              other         5             9528
  ----------------------------------------------------------------------------------------

*Cobertura del diccionario uniforme de lemas por tradición (results/campana_03/cobertura_lexicon.csv).*

  ----------------------------------------------------------------------------
  tradición           documentos     mediana       mín           máx
  ------------------- -------------- ------------- ------------- -------------
  cristiano           133            0,969         0,929         1,000

  judeo-helenistico   71             0,965         0,947         0,995

  pagano              204            0,988         0,818         1,000
  ----------------------------------------------------------------------------

*Tramos paralelos enmascarados en la campaña 03 (metadata/reuse_ranges.csv; posiciones de palabra en el documento sin máscara).*

  -----------------------------------------------------------------------------
  id         start      end        pair       ref_start   ref_end    tokens
  ---------- ---------- ---------- ---------- ----------- ---------- ----------
  Ef         0          7          Col        1:1         1:1        7

  Ef         18         26         Col        1:2         1:2        8

  Ef         243        252        Col        1:15        1:15       9

  Ef         1302       1312       Col        4:15        4:16       10

  Ef         1657       1667       Col        5:6         5:6        10

  Ef         2112       2120       Col        6:7         6:8        8

  Ef         2360       2389       Col        6:21        6:22       29

  Col        0          7          Ef         1:1         1:1        7

  Col        20         28         Ef         1:2         1:2        8

  Col        47         57         Ef         1:4         1:4        10

  Col        695        703        Ef         2:10        2:10       8

  Col        1000       1013       Ef         3:6         3:7        13

  Col        1266       1274       Ef         3:23        3:24       8

  Col        1377       1408       Ef         4:7         4:8        31

  2Tes       0          20         1Tes       1:1         1:2        20

  2Tes       672        682        1Tes       3:8         3:8        10

  2Tes       810        817        1Tes       3:18        3:18       7

  1Tes       0          24         2Tes       1:1         1:2        24

  1Tes       358        368        2Tes       2:9         2:9        10

  1Tes       1464       1471       2Tes       5:28        5:28       7
  -----------------------------------------------------------------------------

**A.3. Protocolo sellado y preregistro**

*Sellos SHA-256 (archivos results/PROTOCOLO_SELLADO\_\<campaña\>.json).*

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  campaña                  fecha y hora del sello (UTC)   contenido                                                                                huella SHA-256
  ------------------------ ------------------------------ ---------------------------------------------------------------------------------------- ------------------------------------------------------------------
  campana_01               2026-09-08 13:51:35            48 especificaciones, 100 iteraciones; variables; mismo rasero; rolling                   4eb0a43658f14fa69391faa47e6c4508d02e327ffdfea2737f033b45fa6d08e2

  campana_02a_nucleos      2026-09-08 16:27:30            núcleo seven / Hauptbriefe / seven_plus (9)                                              b19ff50ab9111abefc142d24b0cb2e7948e8ed6298a75fad2da2f7c719504105

  campana_02b_ediciones    2026-09-08 16:27:30            SBLGNT / Tischendorf / Nestle 1904 (9)                                                   d19b0a6acd13a8011d153a7eeba4324586e6fc9ac5b6a971443c8949ef95c19d

  campana_02c_ventana300   2026-09-08 16:27:31            ventana de 300 palabras (6)                                                              fb8a0f9247627c2a8fa68b1bd93b0617853931e594184b49a60dfbd23057cfac

  campana_02d_rasgos       2026-09-08 16:27:31            mfw:100, mfw:500, char4:1000 (6)                                                         4973f2627a9905fb05aa4a2f078ded5d66b823cf2b9531d760409c5682dc059d

  campana_02e_coseno       2026-09-08 16:27:31            distancia coseno (3)                                                                     0edef83ff6a9406e02fef03b4ed90214bc280d159a48841464a6e2cafb2c2d6b

  campana_03               2026-09-09 06:31:51            16 especificaciones, 300 iteraciones; corpus ampliado; lemas; máscara de reutilización   33e7b61b10d63ec486a35bbee8148fe0835918d8c6e1ec6a41e855855505b625
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

El sello de la campaña 01 cubre los quince módulos de paulinum/, los cuatro archivos de metadata/ y config/default.yaml; el de la campaña 03 cubre además scripts/\*.py, metadata/reuse_ranges.csv, metadata/control_variables.csv y data/cache/lexicon_uniforme.tsv (SHA-256 eb404ee239dd6adcf79daf7485e4fbefdd74e61e8e36bb160492f70456b95d9f). Ambos se reprodujeron en el ordenador del investigador y en la réplica de la nube. Los tres guiones de lectura escritos después del sellado de la campaña 03 no forman parte de él.

*Bloque de preregistro de la campaña 01 (config/default.yaml, sección preregistro, 8 de septiembre de 2026).*

*rejilla*: 3 rasgos × 2 distancias × 2 ventanas × 2 máscaras × 2 diacríticos × 1 núcleo × 1 edición = 48 especificaciones, iters 100

*regla_auc*: una especificación con AUC \< 0,80 en los problemas de respuesta conocida no produce LR

*veredicto*: por carta: mediana de log10 LR entre las especificaciones válidas, con Q1-Q3 y mín-máx; escala verbal ENFSI

*mismo_rasero*: ninguna carta se declara anómala si su percentil intra-autor (envolvente de controles genuine, tope 120 pares/autor) es \<= 90

*carta_por_carta*: 1 Tim, 2 Tim, Tit, Ef, Col y 2 Tes se valoran una a una; la carta hermana (Col para Ef, 1 Tes para 2 Tes) se comenta pero no se suma

*calibracion_secundaria*: además de la LR con todos los negativos, se informará la LR recalculada con los negativos restringidos a textos cristianos (grupos nt y af, Ps-Ignacio, Ps-Clementinas, 2 Clem, Bernabé, 3 Cor), porque la calibración rápida mostró que los falsos positivos frente a Pablo se concentran en la epistolografía cristiana (IgnEf 0,825; 2 Pe 0,725; 3 Jn 0,725; 1 Pe 0,70; Sant 0,65) mientras los negativos paganos puntúan ≈ 0

*tres_corintios*: 3 Cor puntuó 0,65 frente al núcleo en la calibración rápida (no detectado como pseudoepígrafo): se informa como límite del método frente a un imitador del mismo registro, con la reserva ortográfica de data/local/LEEME_3Cor.md; nunca se usa como argumento a favor ni en contra de una carta concreta

*resultado_adverso*: si alguna carta del núcleo queda por debajo de 0,5 en leave-one-out en la mayoría de las especificaciones, se informa como heterogeneidad del núcleo; no se cambia el núcleo ni los parámetros dentro de esta campaña

*robustez*: las variantes de núcleo (hauptbriefe, seven_plus), edición (tischendorf, nestle1904), ventana 300 y rasgos mfw:100/500, char4:1000, cosine se ejecutan en una campaña separada (campana_02_robustez) con su propio sello y solo como sensibilidad

*Bloque de preregistro de la campaña 03 (config/campana_03.yaml, 9 de septiembre de 2026).*

*rejilla*: 4 rasgos × 2 distancias × 1 ventana × 2 máscaras × 1 diacríticos × 1 núcleo × 1 edición = 16 especificaciones, iters 300

*regla_auc*: una especificación con AUC \< 0,80 en los problemas de respuesta conocida no produce LR

*veredicto*: por carta: mediana de log10 LR entre las especificaciones válidas, con Q1-Q3 y mín-máx; escala verbal ENFSI; se informa junto al veredicto de la campaña 01, sin sustituirlo

*mismo_rasero*: ninguna carta se declara anómala si su percentil intra-autor es \<= 90; el percentil se acompaña de su IC 95 % por bootstrap de autores y de ventanas (scripts/bootstrap_percentil.py) y del leave-one-author-out; si el IC cruza 90 se dice 'indeterminado', no 'anómalo'

*carta_por_carta*: 1 Tim, 2 Tim, Tit, Ef, Col y 2 Tes se valoran una a una; hermanas excluidas como candidatas (SISTERS); la máscara reuse se informa como especificación aparte y se compara con la sin máscara: si el signo de la LR cambia al enmascarar, se informa como dependencia de los pasajes paralelos

*lematizacion*: lemma_dict aplica el MISMO lexicón a todos los documentos (forma → lema más frecuente en MorphGNT+PROIEL+Diorisis; forma desconocida → forma sin diacríticos); su cobertura por documento se informa; separa léxico (lemma_dict) de morfología (char3, closed) en las Pastorales: se dirá que la señal es 'léxica' si lemma_dict discrimina y closed no, 'morfológica' en el caso inverso

*calibracion_secundaria*: LR con negativos cristianos (tradition == cristiano, ahora con Justino, Taciano, Atenágoras, Teófilo, Clemente de Alejandría, Orígenes, Acta Thomae, Passio Perpetuae además de nt/af y pseudoepígrafos) y, como tercera lectura, con cristianos + judeo-helenísticos (Filón, Josefo, Test. Abr., Vit. Proph., Enoc)

*desconfundido*: PERMANOVA de destinatario/género/polémica/longitud DENTRO de cada autor de control (scripts/variables_controles.py); el R² situacional de Pablo se lee frente a esa distribución: no se interpreta como anómalo si cae dentro del rango de los controles

*segundo_modelo*: SVM lineal calibrado y regresión logística sobre ventanas de 500 tokens, GroupKFold por autor (negativos) y por carta (núcleo); P(Pablo) media por carta; se informa el percentil de cada discutida entre los negativos genuine en validación cruzada y entre las cartas del núcleo en LOO; concordancia o discordancia con el GI se informa; no se elige el modelo que dé 'mejor' resultado

*tres_corintios*: 3 Cor sigue como control negativo de respuesta conocida (pseudo_pairs); nunca se usa como argumento a favor ni en contra de una carta concreta

*resultado_adverso*: si alguna carta del núcleo queda por debajo de 0,5 en LOO en la mayoría de las especificaciones, se informa como heterogeneidad del núcleo; no se cambia el núcleo ni los parámetros dentro de esta campaña; los resultados de la campaña 01 no se retocan

*cambios_de_corpus*: Policarpo Fil. pierde los tokens latinos (caps. 10-12.14) que la campaña 01 incluía por error de filtro; se documenta en auditoria_sesion9.md; no se reabre la campaña 01

**A.4. Tablas de resultados**

***A.4.1. Calibración por especificación***

*Campaña 03 (results/campana_03/calibration_by_spec.csv): 139 positivos y 730 negativos por especificación.*

  --------------------------------------------------------------------------------------
  especificación   auc        c_at_1     thr_low    thr_high   fpr_at_0.5   fnr_at_0.5
  ---------------- ---------- ---------- ---------- ---------- ------------ ------------
  mfw:300          minmax     w500       mnone      0,928      0,928        0,400

  mfw:300          minmax     w500       mreuse     0,928      0,930        0,450

  mfw:300          delta      w500       mnone      0,827      0,916        0,650

  mfw:300          delta      w500       mreuse     0,826      0,913        0,650

  closed:150       minmax     w500       mnone      0,927      0,925        0,650

  closed:150       minmax     w500       mreuse     0,926      0,925        0,550

  closed:150       delta      w500       mnone      0,901      0,921        0,550

  closed:150       delta      w500       mreuse     0,901      0,920        0,600

  char3:600        minmax     w500       mnone      0,943      0,937        0,400

  char3:600        minmax     w500       mreuse     0,943      0,937        0,400

  char3:600        delta      w500       mnone      0,933      0,934        0,600

  char3:600        delta      w500       mreuse     0,932      0,934        0,650

  lemma_dict:300   minmax     w500       mnone      0,933      0,931        0,450

  lemma_dict:300   minmax     w500       mreuse     0,932      0,931        0,450

  lemma_dict:300   delta      w500       mnone      0,829      0,914        0,550

  lemma_dict:300   delta      w500       mreuse     0,829      0,914        0,550
  --------------------------------------------------------------------------------------

*Campaña 01 (results/campana_01/calibration_by_spec.csv): 67 positivos y 259 negativos por especificación. Notación: dia/nodia = con/sin diacríticos; w500/wall = ventana de 500 palabras / documento entero; mnone/mall = sin máscara / con máscara de fórmulas, material preformado y citas.*

  -----------------------------------------------------------------------------------
  especificación   auc           c_at_1       fpr_at_0.5    fnr_at_0.5
  ---------------- ------------- ------------ ------------- -------------------------
  dia              mfw:300       minmax       w500          mnone

  dia              mfw:300       minmax       w500          mformulae+preformed+otq

  dia              mfw:300       minmax       wNone         mnone

  dia              mfw:300       minmax       wNone         mformulae+preformed+otq

  dia              mfw:300       delta        w500          mnone

  dia              mfw:300       delta        w500          mformulae+preformed+otq

  dia              mfw:300       delta        wNone         mnone

  dia              mfw:300       delta        wNone         mformulae+preformed+otq

  dia              closed:150    minmax       w500          mnone

  dia              closed:150    minmax       w500          mformulae+preformed+otq

  dia              closed:150    minmax       wNone         mnone

  dia              closed:150    minmax       wNone         mformulae+preformed+otq

  dia              closed:150    delta        w500          mnone

  dia              closed:150    delta        w500          mformulae+preformed+otq

  dia              closed:150    delta        wNone         mnone

  dia              closed:150    delta        wNone         mformulae+preformed+otq

  dia              char3:600     minmax       w500          mnone

  dia              char3:600     minmax       w500          mformulae+preformed+otq

  dia              char3:600     minmax       wNone         mnone

  dia              char3:600     minmax       wNone         mformulae+preformed+otq

  dia              char3:600     delta        w500          mnone

  dia              char3:600     delta        w500          mformulae+preformed+otq

  dia              char3:600     delta        wNone         mnone

  dia              char3:600     delta        wNone         mformulae+preformed+otq

  nodia            mfw:300       minmax       w500          mnone

  nodia            mfw:300       minmax       w500          mformulae+preformed+otq

  nodia            mfw:300       minmax       wNone         mnone

  nodia            mfw:300       minmax       wNone         mformulae+preformed+otq

  nodia            mfw:300       delta        w500          mnone

  nodia            mfw:300       delta        w500          mformulae+preformed+otq

  nodia            mfw:300       delta        wNone         mnone

  nodia            mfw:300       delta        wNone         mformulae+preformed+otq

  nodia            closed:150    minmax       w500          mnone

  nodia            closed:150    minmax       w500          mformulae+preformed+otq

  nodia            closed:150    minmax       wNone         mnone

  nodia            closed:150    minmax       wNone         mformulae+preformed+otq

  nodia            closed:150    delta        w500          mnone

  nodia            closed:150    delta        w500          mformulae+preformed+otq

  nodia            closed:150    delta        wNone         mnone

  nodia            closed:150    delta        wNone         mformulae+preformed+otq

  nodia            char3:600     minmax       w500          mnone

  nodia            char3:600     minmax       w500          mformulae+preformed+otq

  nodia            char3:600     minmax       wNone         mnone

  nodia            char3:600     minmax       wNone         mformulae+preformed+otq

  nodia            char3:600     delta        w500          mnone

  nodia            char3:600     delta        w500          mformulae+preformed+otq

  nodia            char3:600     delta        wNone         mnone

  nodia            char3:600     delta        wNone         mformulae+preformed+otq
  -----------------------------------------------------------------------------------

***A.4.2. Resumen por carta***

*Campaña 01 (results/campana_01/summary_by_letter.csv; 48 especificaciones).*

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  id     kind       n_specs   score_median   score_q1   score_q3   score_min   score_max   frac_specs_ge_0_5   log10lr_median   log10lr_q1   log10lr_q3
  ------ ---------- --------- -------------- ---------- ---------- ----------- ----------- ------------------- ---------------- ------------ ------------
  Rom    core_loo   48        0,865          0,688      0,990      0,460       1,000       0,979               0,861            0,514        1,691

  1Cor   core_loo   48        0,820          0,627      0,993      0,470       1,000       0,938               0,812            0,424        1,721

  2Cor   core_loo   48        0,890          0,790      1,000      0,690       1,000       1,000               1,113            0,866        1,714

  Gal    core_loo   48        0,925          0,740      1,000      0,610       1,000       1,000               1,343            0,783        1,736

  Flp    core_loo   48        0,755          0,605      0,945      0,420       1,000       0,875               0,654            0,384        1,043

  1Tes   core_loo   48        0,835          0,700      0,963      0,560       1,000       1,000               0,764            0,574        1,378

  Flm    core_loo   48        0,785          0,670      0,897      0,220       1,000       0,938               0,764            0,462        1,068

  Ef     target     48        0,655          0,587      0,750      0,390       0,920       0,812               0,387            0,186        0,517

  Col    target     48        0,660          0,548      0,748      0,310       0,900       0,854               0,371            0,103        0,530

  2Tes   target     48        0,670          0,590      0,812      0,420       1,000       0,938               0,383            0,285        0,567

  1Tim   target     48        0,515          0,260      0,732      0,000       0,910       0,521               0,113            -0,172       0,492

  2Tim   target     48        0,480          0,277      0,685      0,090       0,980       0,458               0,047            -0,135       0,384

  Tit    target     48        0,485          0,110      0,633      0,010       0,940       0,500               0,066            -0,497       0,287
  -------------------------------------------------------------------------------------------------------------------------------------------------------

*Campaña 03 (results/campana_03/summary_by_letter.csv; 16 especificaciones).*

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  id     kind       n_specs   score_median   score_q1   score_q3   score_min   score_max   frac_specs_ge_0_5   log10lr_median   log10lr_q1   log10lr_q3
  ------ ---------- --------- -------------- ---------- ---------- ----------- ----------- ------------------- ---------------- ------------ ------------
  Rom    core_loo   16        0,732          0,676      0,784      0,553       0,843       1,000               0,584            0,487        0,665

  1Cor   core_loo   16        0,690          0,647      0,727      0,553       0,810       1,000               0,487            0,383        0,634

  2Cor   core_loo   16        0,855          0,829      0,874      0,763       0,923       1,000               1,030            0,818        1,179

  Gal    core_loo   16        0,803          0,799      0,842      0,697       0,893       1,000               0,857            0,753        0,943

  Flp    core_loo   16        0,773          0,706      0,821      0,600       0,850       1,000               0,689            0,585        0,831

  1Tes   core_loo   16        0,712          0,697      0,828      0,667       0,853       1,000               0,642            0,563        0,757

  Flm    core_loo   16        0,855          0,802      0,884      0,600       0,963       1,000               1,094            0,653        1,170

  Ef     target     16        0,735          0,622      0,799      0,487       0,827       0,875               0,549            0,482        0,683

  Col    target     16        0,672          0,608      0,745      0,447       0,790       0,875               0,493            0,336        0,546

  2Tes   target     16        0,695          0,688      0,773      0,590       0,793       1,000               0,549            0,439        0,586

  1Tim   target     16        0,598          0,343      0,786      0,163       0,857       0,500               0,361            0,074        0,695

  2Tim   target     16        0,597          0,318      0,772      0,263       0,787       0,500               0,348            0,041        0,589

  Tit    target     16        0,577          0,406      0,758      0,103       0,873       0,625               0,377            0,119        0,545
  -------------------------------------------------------------------------------------------------------------------------------------------------------

*Razones de verosimilitud (log10) por carta, campaña 03 (lr_secundaria_por_carta.csv, lr_secundaria_por_carta_cj.csv), con la mediana cristiana de la campaña 01.*

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  target   log10lr_principal_mediana   log10lr_cristiana_mediana   log10lr_cristiana_q1   log10lr_cristiana_q3   log10lr_cristiana_min   log10lr_cristiana_max   verbal_cristiana_mediana      c01_cristiana   c03_crist+judeo
  -------- --------------------------- --------------------------- ---------------------- ---------------------- ----------------------- ----------------------- ----------------------------- --------------- -----------------
  Rom      0,584                       0,367                       0,305                  0,446                  0,173                   0,528                   apoyo débil a H_mismo-autor   0,600           0,459

  1Cor     0,487                       0,294                       0,202                  0,342                  0,081                   0,466                   no discriminante              0,550           0,373

  2Cor     1,030                       0,929                       0,653                  1,045                  0,414                   1,448                   apoyo débil a H_mismo-autor   1,027           0,977

  Gal      0,857                       0,655                       0,580                  0,728                  0,436                   0,849                   apoyo débil a H_mismo-autor   1,392           0,706

  Flp      0,689                       0,502                       0,386                  0,541                  0,179                   0,662                   apoyo débil a H_mismo-autor   0,326           0,615

  1Tes     0,642                       0,431                       0,316                  0,563                  0,165                   0,775                   apoyo débil a H_mismo-autor   0,553           0,524

  Flm      1,094                       0,851                       0,379                  1,035                  0,182                   1,946                   apoyo débil a H_mismo-autor   0,523           0,966

  Ef       0,549                       0,364                       0,258                  0,466                  0,080                   0,534                   apoyo débil a H_mismo-autor   0,066           0,442

  Col      0,493                       0,239                       0,138                  0,308                  0,027                   0,478                   no discriminante              0,065           0,335

  2Tes     0,549                       0,303                       0,252                  0,358                  0,205                   0,495                   apoyo débil a H_mismo-autor   0,081           0,406

  1Tim     0,361                       0,127                       -0,111                 0,419                  -0,358                  0,826                   no discriminante              -0,203          0,226

  2Tim     0,348                       0,151                       -0,155                 0,327                  -0,215                  0,520                   no discriminante              -0,274          0,240

  Tit      0,377                       0,167                       -0,046                 0,286                  -0,550                  0,794                   no discriminante              -0,258          0,264
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

*Puntuación GI de las seis cartas discutidas por rasgos, distancia y máscara, campaña 03 (gi_results_all_specs.csv, filas target).*

  ---------------------------------------------------------------------------------
  features         metric   mask    Ef      Col     2Tes    1Tim    2Tim    Tit
  ---------------- -------- ------- ------- ------- ------- ------- ------- -------
  char3:600        delta    reuse   0,797   0,750   0,697   0,287   0,323   0,193

  char3:600        delta    sin     0,813   0,750   0,690   0,323   0,347   0,190

  char3:600        minmax   reuse   0,703   0,743   0,690   0,163   0,270   0,103

  char3:600        minmax   sin     0,673   0,727   0,690   0,180   0,263   0,110

  closed:150       delta    reuse   0,493   0,447   0,590   0,350   0,297   0,477

  closed:150       delta    sin     0,487   0,453   0,597   0,360   0,300   0,487

  closed:150       minmax   reuse   0,617   0,543   0,683   0,457   0,443   0,557

  closed:150       minmax   sin     0,610   0,553   0,680   0,437   0,453   0,550

  lemma_dict:300   delta    reuse   0,827   0,790   0,787   0,783   0,783   0,730

  lemma_dict:300   delta    sin     0,823   0,760   0,793   0,763   0,780   0,750

  lemma_dict:300   minmax   reuse   0,633   0,627   0,777   0,753   0,787   0,597

  lemma_dict:300   minmax   sin     0,623   0,637   0,773   0,740   0,770   0,613

  mfw:300          delta    reuse   0,777   0,660   0,743   0,793   0,753   0,867

  mfw:300          delta    sin     0,807   0,653   0,773   0,813   0,740   0,873

  mfw:300          minmax   reuse   0,780   0,697   0,693   0,857   0,783   0,780

  mfw:300          minmax   sin     0,767   0,683   0,703   0,847   0,767   0,790
  ---------------------------------------------------------------------------------

***A.4.3. Mismo rasero***

*Distancia media al núcleo (min-max, campaña 03), percentil intra-autor en las dos campañas y en las dos medidas, e intervalos de confianza al 95 % por bootstrap de autores y de ventanas (double_standard_ledger\_\*.csv, bootstrap_percentil\_\*.csv).*

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------
  carta   d_minmax   pct_mm_c01   pct_mm_c03   IC_autores_mm   IC_ventanas_mm   autor_influyente   sin_ese_autor   pct_delta_c01   pct_delta_c03   IC_autores_delta
  ------- ---------- ------------ ------------ --------------- ---------------- ------------------ --------------- --------------- --------------- ------------------
  Rom     0,634      0,587        0,600        0,37-0,85       0,43-0,63        Juliano            0,676           0,065           0,106           0,05-0,19

  1Cor    0,644      0,662        0,675        0,45-0,93       0,59-0,75        Juliano            0,761           0,190           0,287           0,15-0,45

  2Cor    0,608      0,252        0,283        0,15-0,46       0,17-0,39        Isócrates          0,225           0,023           0,050           0,01-0,11

  Gal     0,631      0,525        0,562        0,34-0,79       0,43-0,63        Juliano            0,630           0,156           0,211           0,11-0,34

  Flp     0,614      0,319        0,371        0,21-0,56       0,25-0,42        Isócrates          0,319           0,031           0,056           0,02-0,12

  1Tes    0,621      0,447        0,434        0,24-0,63       0,32-0,49        Juliano            0,488           0,065           0,113           0,06-0,19

  Flm     0,626      0,530        0,502        0,28-0,72       0,37-0,51        Josefo             0,441           0,068           0,144           0,07-0,23

  Ef      0,623      0,535        0,465        0,25-0,68       0,34-0,59        Josefo             0,406           0,029           0,058           0,02-0,12

  Col     0,650      0,665        0,691        0,47-0,94       0,62-0,72        Juliano            0,780           0,068           0,150           0,07-0,24

  2Tes    0,614      0,216        0,362        0,20-0,55       0,16-0,36        Isócrates          0,309           0,026           0,098           0,04-0,18

  1Tim    0,631      0,556        0,568        0,35-0,80       0,47-0,62        Juliano            0,638           0,171           0,325           0,18-0,50

  2Tim    0,614      0,327        0,352        0,19-0,54       0,21-0,40        Isócrates          0,298           0,171           0,207           0,10-0,34

  Tit     0,672      0,779        0,803        0,63-1,00       0,76-0,81        Juliano            0,879           0,719           0,784           0,63-0,95
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------

***A.4.4. Segundo modelo***

*Validación cruzada por autor (modelo_svm_cv.csv).*

  ----------------------------------------------------------------------------------------
  features         model      n_pos      n_neg      auc_cv_grupo   fpr_cv_05   fnr_cv_05
  ---------------- ---------- ---------- ---------- -------------- ----------- -----------
  mfw:300          svm        45         1447       0,929          0,003       1,000

  mfw:300          logistic   45         1447       0,985          0,017       0,333

  closed:150       svm        45         1447       0,962          0,003       0,867

  closed:150       logistic   45         1447       0,977          0,014       0,267

  char3:600        svm        45         1447       0,885          0,000       1,000

  char3:600        logistic   45         1447       0,995          0,009       0,178

  lemma_dict:300   svm        45         1447       0,951          0,001       1,000

  lemma_dict:300   logistic   45         1447       0,995          0,011       0,111
  ----------------------------------------------------------------------------------------

*Percentiles por carta, mediana entre los ocho modelos (modelo_svm_percentiles_resumen.csv).*

  ----------------------------------------------------------------------------------------------------------------------------
  id       kind       p_media_mediana   pct_neg_mediana   pct_neg_min   pct_nucleo_mediana   pct_nucleo_min   pct_nucleo_max
  -------- ---------- ----------------- ----------------- ------------- -------------------- ---------------- ----------------
  Rom      core_loo   0,407             0,969             0,943         0,250                0,000            0,500

  1Cor     core_loo   0,284             0,967             0,943         0,167                0,000            0,333

  2Cor     core_loo   0,743             0,996             0,959         0,917                0,333            1,000

  Gal      core_loo   0,592             0,990             0,971         0,833                0,500            0,833

  Flp      core_loo   0,445             0,984             0,951         0,500                0,167            0,667

  1Tes     core_loo   0,329             0,988             0,951         0,500                0,000            1,000

  Flm      core_loo   0,301             0,988             0,414         0,750                0,000            1,000

  Ef       target     0,161             0,963             0,914         0,214                0,143            0,429

  Col      target     0,278             0,969             0,943         0,286                0,000            0,429

  2Tes     target     0,576             0,990             0,951         0,500                0,286            0,857

  1Tim     target     0,066             0,949             0,918         0,071                0,000            0,429

  2Tim     target     0,172             0,965             0,926         0,071                0,000            0,571

  Tit      target     0,161             0,971             0,877         0,214                0,000            0,857
  ----------------------------------------------------------------------------------------------------------------------------

***A.4.5. Variables de situación***

*PERMANOVA dentro del corpus paulino, ventanas de 400 palabras (permanova_pauline_windows.csv).*

  --------------------------------------------------------------------------------
  variable              n          k          R2          pseudo_F     p
  --------------------- ---------- ---------- ----------- ------------ -----------
  addressee_type        76         2          0,037       2,849        0,002

  captivity             76         2          0,042       3,256        0,002

  polemic_level         76         4          0,073       1,898        0,002

  n_cosenders           76         3          0,052       1,993        0,002

  liturgical_register   76         4          0,078       2,034        0,002

  church_order          76         2          0,029       2,221        0,002

  letter                76         13         0,260       1,844        0,002

  group                 76         3          0,073       2,890        0,002
  --------------------------------------------------------------------------------

*PERMANOVA dentro de cada autor de control y de Pablo, con R² submuestreado a 76 ventanas (permanova_controles.csv).*

  ------------------------------------------------------------------------------------------------
  author                   variable         n_windows   k         R2         R2_sub76   p
  ------------------------ ---------------- ----------- --------- ---------- ---------- ----------
  Arriano                  work             227         2         0,042      0,049      0,003

  Clemente de Alejandría   addressee_type   223         2         0,018      0,029      0,003

  Clemente de Alejandría   genre            223         3         0,046      0,064      0,003

  Clemente de Alejandría   polemic          223         2         0,026      0,035      0,003

  Clemente de Alejandría   work             223         3         0,046      0,064      0,003

  Elio Aristides           length_class     242         2         0,020      0,028      0,003

  Elio Aristides           work             242         6         0,080      0,121      0,003

  Epicteto(ap. Arriano)    genre            198         2         0,014      0,019      0,003

  Epicteto(ap. Arriano)    length_class     198         2         0,014      0,022      0,003

  Epicteto(ap. Arriano)    work             198         2         0,014      0,021      0,003

  Filón                    genre            1006        3         0,014      0,035      0,003

  Filón                    polemic          1006        2         0,007      0,018      0,003

  Filón                    length_class     1006        2         0,001      0,013      0,117

  Filón                    work             1006        30        0,088      0,378      0,003

  Ignacio                  length_class     15          2         0,070      0,070      0,517

  Ignacio                  work             15          7         0,425      0,425      0,567

  Isócrates                addressee_type   118         2         0,015      0,021      0,007

  Isócrates                genre            118         2         0,015      0,020      0,007

  Isócrates                length_class     118         3         0,029      0,039      0,003

  Isócrates                work             118         13        0,146      0,175      0,003

  Josefo                   addressee_type   1171        2         0,008      0,020      0,003

  Josefo                   genre            1171        3         0,013      0,040      0,003

  Josefo                   polemic          1171        2         0,008      0,020      0,003

  Josefo                   work             1171        4         0,042      0,075      0,003

  Juliano                  addressee_type   49          2         0,028      0,028      0,040

  Juliano                  length_class     49          2         0,042      0,042      0,003

  Juliano                  work             49          37        0,791      0,791      0,003

  Justino                  genre            84          2         0,048      0,049      0,003

  Justino                  length_class     84          3         0,066      0,069      0,003

  Justino                  work             84          3         0,066      0,068      0,003

  Lucas(anon)              work             94          2         0,069      0,071      0,003

  Luciano                  addressee_type   62          2         0,038      0,038      0,003

  Luciano                  genre            62          4         0,117      0,117      0,003

  Luciano                  polemic          62          2         0,041      0,041      0,003

  Luciano                  length_class     62          2         0,028      0,028      0,003

  Luciano                  work             62          5         0,146      0,146      0,003

  Orígenes                 genre            518         4         0,030      0,059      0,003

  Orígenes                 polemic          518         3         0,026      0,045      0,003

  Orígenes                 length_class     518         2         0,004      0,012      0,003

  Orígenes                 work             518         4         0,030      0,057      0,003

  Pablo (13 cartas)        addressee_type   76          2         0,037      0,037      0,003

  Pablo (13 cartas)        polemic          76          3         0,045      0,045      0,007

  Pablo (13 cartas)        length_class     76          3         0,060      0,060      0,003

  Pablo (13 cartas)        work             76          13        0,260      0,260      0,003

  Plutarco                 addressee_type   113         2         0,054      0,058      0,003

  Plutarco                 genre            113         5         0,135      0,149      0,003

  Plutarco                 polemic          113         2         0,027      0,031      0,003

  Plutarco                 length_class     113         2         0,033      0,036      0,003

  Plutarco                 work             113         7         0,170      0,192      0,003

  Teófilo de Antioquía     length_class     52          2         0,033      0,033      0,017
  ------------------------------------------------------------------------------------------------

*Controles de género (controles_genero_resumen.csv): puntuación media de cada clase de subgénero como positivo intra-autor y como negativo frente a Pablo, mediana entre especificaciones.*

  ----------------------------------------------------------------------------------------------------------------------------------------------------
  clase           n_pos   pos_media   pos_otros   pos_pct   pos_frac_menor_05   n_neg   neg_media   neg_otros   neg_cartas_otras   neg_frac_mayor_05
  --------------- ------- ----------- ----------- --------- ------------------- ------- ----------- ----------- ------------------ -------------------
  apologia        14      0,405       0,661       0,250     0,857               22      0,108       0,121       0,137              0,000

  circular        0                   0,635                                     2       0,448       0,118       0,134              0,500

  consolatoria    1       0,722       0,635       0,527     0,000               1       0,038       0,120       0,137              0,000

  exhortacion     2       0,588       0,636       0,398     0,500               3       0,227       0,119       0,137              0,000

  mandato         13      0,907       0,606       0,788     0,000               46      0,056       0,128       0,171              0,022

  otra            101     0,629       0,642       0,504     0,337               290     0,124       0,106       0,091              0,066

  parenetica      1       0,700       0,635       0,538     0,000               2       0,288       0,119       0,135              0,500

  testamentaria   0                   0,635                                     1       0,597       0,119       0,135              1,000
  ----------------------------------------------------------------------------------------------------------------------------------------------------

***A.4.6. Falsificaciones y negativos que pasan***

*Pseudoepigrafías conocidas frente al autor imitado, campaña 03 (gi_results_all_specs.csv, filas pseudepigraphy).*

  -------------------------------------------------------------------------
  pseudoepígrafo        mediana           mín              máx
  --------------------- ----------------- ---------------- ----------------
  2Clem                 0,133             0,060            0,290

  3Cor                  0,542             0,253            0,717

  IgnLong#1             0,312             0,077            0,530

  IgnLong#10            0,593             0,137            0,837

  IgnLong#13            0,162             0,067            0,543

  IgnLong#4             0,377             0,227            0,730

  IgnLong#5             0,215             0,080            0,467

  IgnLong#9             0,678             0,520            0,920

  Plut_Fato             0,273             0,173            0,387

  Plut_LibEd            0,515             0,453            0,613

  PsClem_EpJac          0,050             0,030            0,077

  PsClem_EpPet          0,065             0,040            0,110
  -------------------------------------------------------------------------

*Textos no paulinos con mediana GI ≥ 0,5 frente al núcleo, campaña 03 (24 de 367).*

  -------------------------------------------------------------------------
  texto              author             tradition         mediana GI
  ------------------ ------------------ ----------------- -----------------
  IgnFil             Ignacio            cristiano         0,778

  IgnEf              Ignacio            cristiano         0,767

  1Pe                Pedro(?)           cristiano         0,760

  2Jn                Juan(presb.)       cristiano         0,703

  IgnMagn            Ignacio            cristiano         0,697

  IgnTral            Ignacio            cristiano         0,677

  3Jn                Juan(presb.)       cristiano         0,662

  IgnLong#11         Ps-Ignacio         cristiano         0,638

  IgnRom             Ignacio            cristiano         0,637

  PolFil             Policarpo          cristiano         0,627

  IgnLong#12         Ps-Ignacio         cristiano         0,597

  2Pe                Pedro(?)           cristiano         0,597

  IgnPol             Ignacio            cristiano         0,577

  IgnLong#8          Ps-Ignacio         cristiano         0,575

  IgnEsm             Ignacio            cristiano         0,572

  Sant               Santiago(?)        cristiano         0,562

  3Cor               Ps-Pablo           cristiano         0,558

  Just_Dial#21       Justino            cristiano         0,545

  IgnLong#6          Ps-Ignacio         cristiano         0,523

  2Clem              Ps-Clemente        cristiano         0,522

  IgnLong#4          Ps-Ignacio         cristiano         0,517

  Just_Dial#12       Justino            cristiano         0,517

  IgnLong#3          Ps-Ignacio         cristiano         0,507

  IgnLong#10         Ps-Ignacio         cristiano         0,500
  -------------------------------------------------------------------------

**A.5. Glosario**

*GI*: puntuación de los impostores generales, fracción de iteraciones en que el candidato más cercano supera al impostor más cercano. *AUC*: área bajo la curva ROC, probabilidad de que un positivo puntúe más que un negativo. *c@1*: exactitud que recompensa la abstención. *LR*: razón de verosimilitud, cociente entre la densidad de la puntuación observada entre pares del mismo autor y entre pares de autores distintos, estimada por densidades de núcleo en los controles de la misma especificación; se da su logaritmo decimal. *Escala verbal*: \|log10 LR\| \< 0,3 no discriminante; 0,3-1 débil; 1-2 moderado; ≥ 2 fuerte. *Delta*: distancia de Burrows sobre frecuencias estandarizadas. *Min-max* (Ruzicka): 1 − Σmin/Σmax sobre frecuencias relativas. *Envolvente intra-autor*: distribución de distancias entre obras distintas de un mismo autor de control. *Percentil intra-autor*: posición de la distancia media de una carta al núcleo en esa distribución. *PERMANOVA*: análisis de varianza por permutaciones sobre una matriz de distancias; R² = fracción de la variación explicada. *dbRDA*: regresión sobre coordenadas principales. *Máscara*: exclusión de tramos declarados por referencia (fórmulas epistolares, material preformado, citas del Antiguo Testamento) o por posición (pasajes paralelos). *Especificación*: combinación de rasgos, distancia, ventana, máscara, ortografía, núcleo y edición. *H1-H5*: redacción personal; secretario con libertad limitada; composición delegada en vida de Pablo; escuela paulina posterior; pseudonimia ajena al círculo.

**A.6. Archivos de resultados**

results/campana_01/: config_used.json, run.log, specs/000-047.json, gi_results_all_specs.csv (20.160 filas), calibration_by_spec.csv, summary_by_letter.csv, calibracion_secundaria_cristiana.csv, lr_secundaria_por_spec.csv, lr_secundaria_por_carta.csv, distance_matrix\_{minmax,delta}.npy, distance_matrix_ids.csv, pair_distances\_\*.csv, double_standard_ledger\_\*.csv, permanova_pauline_windows.csv, dbrda_partition_pauline_windows.{csv,txt}, edition_noise_pairs.csv, feature_contributions.csv, descriptives.csv, rolling_scores.csv, tabla_resumen_13_cartas.csv, lectura_sesion5.md, lectura_sesion6.md, bitacora.md, informe/INFORME_AUTOMATICO.md y 37 figuras, informe/INFORME_FINAL.md y .docx, codigo_sellado_campana_01.tgz. results/campana_02{a,b,c,d,e}\_\*/: calibration_by_spec.csv, gi_results_all_specs.csv, summary_by_letter.csv, specs/. results/campana_03/: los mismos archivos que la campaña 01 más inventory.csv, calibracion_secundaria_cristiana_cj.csv, lr_secundaria_por\_\*\_cj.csv, bootstrap_percentil\_\*.csv, loo_autor_percentil\_\*.csv, permanova_controles.csv, reutilizacion_pares.csv, cobertura_lexicon.csv, controles_genero\*.csv, modelo_svm\_\*.csv, lectura_sesion11_12.md, informe/INFORME_CAMPANA_03.md y .docx. Además: results/auditoria_sesion2.md, results/auditoria_sesion9.md, results/bitacora_preparacion.md, docs/bibliografia_verificada.md, metadata/\*.csv, data/local/ (3 Corintios con su alineación), data/provenance.json.

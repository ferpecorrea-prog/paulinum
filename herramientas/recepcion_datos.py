# -*- coding: utf-8 -*-
"""Datos de codificación del canal de recepción (PROTOCOLO § 9.1; docs/canales/codigos_recepcion.md).
Cada fila: (carta, testigo, fecha_testigo, atestacion, atribucion, posicion, pasaje, fuente, cita, juicio, nota)."""
CARTAS = ["Rom","1Cor","2Cor","Gal","Flp","1Tes","Flm","Ef","Col","2Tes","1Tim","2Tim","Tit","Heb"]
R = []
def add(carta, testigo, fecha, at, atr, pos, pasaje, fuente, cita, juicio="no", nota=""):
    R.append(dict(carta=carta, testigo=testigo, fecha_testigo=fecha, atestacion=at, atribucion=atr, posicion=pos,
                  pasaje=pasaje, fuente=fuente, cita=cita, juicio=juicio, nota=nota))

# ---- Marción (según Tertuliano, Adv. Marc. V; Epifanio, Pan. 42) ----
MARC = {"Gal":(1,"V 2-4"),"1Cor":(2,"V 5-10"),"2Cor":(3,"V 11-12"),"Rom":(4,"V 13-14"),"1Tes":(5,"V 15"),"2Tes":(6,"V 16"),
        "Ef":(7,"V 17-18 («Laodicenses»)"),"Col":(8,"V 19"),"Flp":(9,"V 20"),"Flm":(10,"V 21")}
F_TERT = "Tertuliano, Adversus Marcionem V (trad. Holmes, ANF 3; verificado en newadvent.org/fathers/03125.htm el 29-IX-2026); orden según Epifanio, Pan. 42,9,4 (Schmid 1995; BeDuhn 2013)"
for c,(p,cap) in MARC.items():
    cita = "capítulo dedicado a la carta en el comentario de Tertuliano al Apostolikon de Marción"
    nota = ""
    if c=="Ef": cita = "«hold to have been written to the Ephesians, but the heretics to the Laodiceans» (V 11; V 17)"; nota="título «a los Laodicenses» en Marción"
    if c=="Flm": cita = "«This Epistle Not Mutilated. Marcion's Inconsistency in Accepting This, and Rejecting Three Other Epistles Addressed to Individuals» (V 21)"
    add(c,"Marc","c. 140-144",3,"Pablo",p,f"Tert. Adv. Marc. {cap}",F_TERT,cita)
for c in ("1Tim","2Tim","Tit"):
    add(c,"Marc","c. 140-144",0,"na","ausente","Tert. Adv. Marc. V 21",F_TERT,
        "«rejecting three other epistles addressed to individuals» (V 21)","no","ausente del Apostolikon; Tertuliano lo señala")
add("Heb","Marc","c. 140-144",0,"na","ausente","—",F_TERT,"ninguna mención de Hebreos en Adv. Marc. V ni en Pan. 42","no","ausente del Apostolikon")

# ---- Fragmento de Muratori ----
F_MUR = "Fragmento de Muratori, líneas 39-68 (trad. Metzger 1987, apéndice IV; verificado en earlychristianwritings.com/text/muratorian-metzger.html el 29-IX-2026)"
MUR = {"1Cor":(1,"«To the Corinthians first» (l. 50-51)"),"2Cor":(1,"«he writes once more to the Corinthians» (l. 54)"),"Ef":(2,"«to the Ephesians second» (l. 51)"),
       "Flp":(3,"«to the Philippians third» (l. 51)"),"Col":(4,"«to the Colossians fourth» (l. 52)"),"Gal":(5,"«to the Galatians fifth» (l. 52)"),
       "1Tes":(6,"«to the Thessalonians sixth» (l. 53)"),"2Tes":(6,"«once more … to the Thessalonians» (l. 55)"),"Rom":(7,"«to the Romans seventh» (l. 53-54)"),
       "Flm":(8,"«one to Philemon» (l. 59-60)"),"Tit":(9,"«one to Titus» (l. 60)"),"1Tim":(10,"«two to Timothy» (l. 60)"),"2Tim":(10,"«two to Timothy» (l. 60)")}
for c,(p,cita) in MUR.items():
    add(c,"Mur","fines s. II (s. IV según Hahneman)",3,"Pablo",p,"l. 39-63",F_MUR,cita,"no","fecha: extremo tardío discutido (s. IV, Hahneman 1992); la codificación usa fines del s. II como fecha convencional y anota la discusión")
add("Heb","Mur","fines s. II",0,"na","ausente","l. 63-68",F_MUR,"no se menciona; «[an epistle] to the Alexandrians … forged in Paul's name» (l. 63-65) no se identifica con Hebreos","sí","identificación de «ad Alexandrinos» con Hebreos: hipótesis minoritaria, no adoptada")

# ---- P46 (contenido y orden; NA28 ap. I y derivados de la campaña) ----
F_P46 = "NA28, Apéndice I, 𝔓46 (p. 794-795, leído en el ejemplar del autor el 29-IX-2026); orden del códice: Kenyon 1936; docs/testigos_manuscritos.md; results/paulinum_1_0/…/p46_contenido_y_orden.csv"
P46 = {"Rom":(1,"R 5,17-6,3.5-14; 8,15-25.27-35; 8,37-9,32; 10,1-11,22.24-33; 11,35-15,9; 15,11-16,27"),"Heb":(2,"H 1,1-9,16; 9,18-10,20.22-30; 10,32-13,25"),
       "1Cor":(3,"1K 1,1-9,2; 9,4-14,14; 14,16-15,15; 15,17-16,22"),"2Cor":(4,"2K 1,1-11,10.12-21; 11,23-13,13"),"Ef":(5,"E 1,1-2,7; 2,10-5,6; 5,8-6,6.8-18.20-24"),
       "Gal":(6,"G 1,1-8; 1,10-2,9.12-21; 3,2-29; 4,2-18; 4,20-5,17; 5,20-6,8.10-18"),"Flp":(7,"Ph 1,1.5-15.17-28; 1,30-2,12.14-27; 2,29-3,8.10-21; 4,2-12.14-23"),
       "Col":(8,"Kol 1,1-2.5-13.16-24; 1,27-2,19; 2,23-3,11.13-24; 4,3-12.16-18"),"1Tes":(9,"1Th 1,1; 1,9-2,3; 5,5-9.23-28")}
for c,(p,cont) in P46.items():
    atr = "anonima" if c=="Heb" else "Pablo"
    nota = "sin nombre de autor; incluida entre las cartas de Pablo, tras Romanos" if c=="Heb" else ""
    add(c,"P46","ca. 200",3,atr,p,cont,F_P46,"contenido según NA28 ap. I","no",nota)
for c in ("2Tes","1Tim","2Tim","Tit","Flm"):
    add(c,"P46","ca. 200",0,"na","ausente","—",F_P46,"no conservada; el final del códice (hojas perdidas) no da cabida a las Pastorales según el cómputo de Kenyon; 2 Tes y Flm cabrían","sí",
        "cómputo de hojas (Kenyon 1936; Duff 1998; Ebojo 2014): 2 Tes probablemente estaba; las Pastorales y Flm probablemente no")

# ---- Papiros ss. II-III (NA28 ap. I; 𝔓133 posterior a NA28) ----
F_PAP = "NA28, Apéndice I, Codices Graeci (pp. 792-798, leído en el ejemplar del autor el 29-IX-2026)"
PAP = {"Rom":("𝔓46 (ca. 200); 𝔓27, 𝔓40, 𝔓113, 𝔓118 (III)","ca. 200"),"1Cor":("𝔓46 (ca. 200); 𝔓15 (III)","ca. 200"),"2Cor":("𝔓46 (ca. 200)","ca. 200"),
       "Gal":("𝔓46 (ca. 200)","ca. 200"),"Flp":("𝔓46 (ca. 200); 𝔓16 (III/IV)","ca. 200"),"1Tes":("𝔓46 (ca. 200, fragmentos); 𝔓30, 𝔓65 (III)","ca. 200"),
       "Flm":("𝔓87 (III)","III"),"Ef":("𝔓46 (ca. 200); 𝔓49 (III); 𝔓92 (III/IV)","ca. 200"),"Col":("𝔓46 (ca. 200)","ca. 200"),
       "2Tes":("𝔓30 (III); 𝔓92 (III/IV)","III"),"Tit":("𝔓32 (ca. 200)","ca. 200"),"Heb":("𝔓46 (ca. 200); 𝔓12, 𝔓114 (III); 𝔓13 (III/IV)","ca. 200")}
for c,(lst,fecha) in PAP.items():
    add(c,"Pap",fecha,3,"Pablo" if c!="Heb" else "anonima","na",lst,F_PAP,"siglos según NA28 ap. I","no","nivel 3 = presencia en un códice o rollo de la colección paulina")
add("1Tim","Pap","III",3,"Pablo","na","𝔓133 (P. Oxy. LXXXI 5259; 1 Tim 3,13-4,8; III)","Kurzgefasste Liste del INTF (posterior a NA28); Shao 2017 (P. Oxy. LXXXI)","no en NA28 (2012); el papiro más antiguo de las Pastorales tras 𝔓32","sí","no verificable hoy en NTVMR (la Liste en línea no se deja leer desde el navegador de la sesión); datación del editor: s. III")
add("2Tim","Pap","IV",0,"na","na","ninguno de los ss. II-III; testigo más antiguo ℵ 01 (IV)",F_PAP,"sin papiro de los ss. II-III en NA28 ap. I","no","B 03 (IV) carece de 1 Tim-Flm (vac.)")

# ---- Eusebio ----
F_EUS = "Eusebio, HE III 3,5 y III 25,2 (trad. McGiffert, NPNF2 1; verificado en newadvent.org/fathers/250103.htm el 29-IX-2026)"
for c in CARTAS:
    if c=="Heb":
        add(c,"Eus","c. 313-325",3,"Pablo",14,"HE III 3,5; III 38,2; VI 14,2-4; VI 25,11-14",F_EUS,
            "«Paul's fourteen epistles are well known and undisputed … some have rejected the Epistle to the Hebrews, saying that it is disputed by the church of Rome, on the ground that it was not written by Paul» (III 3,5)",
            "no","atribución a Pablo con constancia de la disputa romana; recoge a Clemente de Alejandría (Pablo en hebreo, Lucas traductor) y a Orígenes («quién escribió la carta, en verdad Dios lo sabe»)")
    else:
        add(c,"Eus","c. 313-325",3,"Pablo","na","HE III 3,5; III 25,2",F_EUS,"«Paul's fourteen epistles are well known and undisputed» (III 3,5); «the epistles of Paul» entre los reconocidos (III 25,2)")

# ---- Atanasio, carta festal 39 ----
F_ATH = "Atanasio, Epistula festalis 39,5 (367; trad. Payne-Smith, NPNF2 4; verificado en newadvent.org/fathers/2806039.htm el 29-IX-2026)"
ORD_ATH = {"Rom":1,"1Cor":2,"2Cor":3,"Gal":4,"Ef":5,"Flp":6,"Col":7,"1Tes":8,"2Tes":9,"Heb":10,"1Tim":11,"2Tim":12,"Tit":13,"Flm":14}
for c,p in ORD_ATH.items():
    add(c,"Athan","367",3,"Pablo",p,"Ep. fest. 39,5",F_ATH,"«fourteen Epistles of Paul, written in this order …»")

# ---- Orden en las colecciones (catálogo) ----
F_ORD = "Marción: Epifanio, Pan. 42,9,4 y Tertuliano Adv. Marc. V; Muratori l. 42-63; 𝔓46: Kenyon 1936; ℵ B A C: NA28 ap. I y Trobisch 1994; D 06: Tischendorf 1852; Gamble 1995"
ORD = {"Rom":"Marción 4; Muratori 7; 𝔓46 1; ℵ B A C 1; D06 1","1Cor":"Marción 2; Muratori 1; 𝔓46 3; ℵ B A C 2; D06 2","2Cor":"Marción 3; Muratori 1 (segunda); 𝔓46 4; ℵ B A C 3; D06 3",
       "Gal":"Marción 1; Muratori 5; 𝔓46 6; ℵ B A C 4; D06 4","Flp":"Marción 9; Muratori 3; 𝔓46 7; ℵ B A C 6; D06 6","1Tes":"Marción 5; Muratori 6; 𝔓46 9; ℵ B A C 8; D06 8",
       "Flm":"Marción 10; Muratori 8; 𝔓46 ausente; ℵ A C 14 (B vac.); D06 13","Ef":"Marción 7 (Laod.); Muratori 2; 𝔓46 5; ℵ B A C 5; D06 5","Col":"Marción 8; Muratori 4; 𝔓46 8; ℵ B A C 7; D06 7",
       "2Tes":"Marción 6; Muratori 6 (segunda); 𝔓46 perdida (probable); ℵ B A C 9; D06 9","1Tim":"Marción ausente; Muratori 10; 𝔓46 ausente; ℵ A C 11 (B vac.); D06 10",
       "2Tim":"Marción ausente; Muratori 10; 𝔓46 ausente; ℵ A C 12 (B vac.); D06 11","Tit":"Marción ausente; Muratori 9; 𝔓46 ausente; ℵ A C 13 (B vac.); D06 12",
       "Heb":"Marción ausente; Muratori ausente; 𝔓46 2 (tras Rom); ℵ A C 10 (tras 2 Tes); B tras Gal según la numeración de capítulos antigua, tras 2 Tes en el códice; D06 14 (al final, tras Flm)"}
for c,pos in ORD.items():
    add(c,"Orden","ss. II-VI","na","na",pos,"catálogo",F_ORD,"posiciones según las fuentes citadas","sí" if c in ("2Tes","Heb","Flm") else "no",
        "fila de catálogo: sin nivel de atestación propio; la posición se lee en las medidas")

# ---- 1 Clemente (NTAF 1905, «Clement of Rome», pp. 37-62; verificado en archive.org/stream/thenewtestamenti00unknuoft el 29-IX-2026) ----
F_NTAF_C = "Oxford Society, The New Testament in the Apostolic Fathers (1905), Clement of Rome, pp. 37-62 (clases A-D); texto verificado el 29-IX-2026 en archive.org; Gregory-Tuckett 2005"
CLEM = {"1Cor":(3,"Pablo","1 Clem 47,1-3","«ἀναλάβετε τὴν ἐπιστολὴν τοῦ μακαρίου Παύλου τοῦ ἀποστόλου … ἔριδες» (NTAF n.º 8, clase A)","no",""),
        "Rom":(2,"anonima","1 Clem 35,5-6","catálogo de vicios de Rom 1,29-32 «practically certain that Clement is influenced» (NTAF n.º 1, clase A); 33,1 ~ Rom 6,1","no","uso claro sin nombre; Pablo se nombra en 47,1 solo para 1 Cor"),
        "Heb":(2,"anonima","1 Clem 36,2-5","Heb 1,3-4.7.13 «ἀπαύγασμα τῆς μεγαλωσύνης … τοσούτῳ μείζων ἐστὶν ἀγγέλων» (NTAF n.º 19, clase A); Eusebio HE III 38,1 lo señala","no","uso claro sin nombre ni atribución"),
        "Tit":(1,"na","1 Clem 1,3; 2,7","Tit 2,4-5 (οἰκουργεῖν) y 3,1 «ἕτοιμοι εἰς πᾶν ἔργον ἀγαθόν» (NTAF n.º 31-32, clase C/D)","sí",""),
        "2Cor":(1,"na","1 Clem 36,2","2 Cor 3,18 (NTAF n.º 33, clase D)","sí",""),
        "Gal":(1,"na","1 Clem 49,6","(NTAF clase D)","sí",""),
        "Ef":(1,"na","1 Clem 46,6; 59,3","Ef 4,4-6; 1,18 (NTAF clase D)","sí",""),
        "Flp":(1,"na","1 Clem 47,1-2","Flp 4,15 «ἐν ἀρχῇ τοῦ εὐαγγελίου» (NTAF n.º 41, clase D)","sí",""),
        "Col":(1,"na","1 Clem 59,2","Col 1,12-13 (NTAF n.º 42, clase D)","sí",""),
        "1Tim":(1,"na","1 Clem 61,2","1 Tim 1,17 «βασιλεῦ τῶν αἰώνων» (NTAF n.º 44, sin clase)","sí",""),
        "2Tim":(1,"na","1 Clem 2,7","2 Tim 2,21; 3,17 «πᾶν ἔργον ἀγαθόν» (NTAF n.º 32, clase D)","sí",""),
        "1Tes":(0,"na","—","sin paralelo registrado en NTAF","no",""),"2Tes":(0,"na","—","sin paralelo registrado en NTAF","no",""),"Flm":(0,"na","—","sin paralelo registrado en NTAF","no","")}
for c,(at,atr,pas,cita,j,nota) in CLEM.items():
    add(c,"1Clem","c. 96 (80-140)",at,atr,"na",pas,F_NTAF_C,cita,j,nota)

# ---- Ignacio (NTAF 1905, pp. 63-83) ----
F_NTAF_I = "Oxford Society, NTAF (1905), Ignatius, pp. 63-83 (clases A-D); verificado el 29-IX-2026 en archive.org; Foster 2005 (en Gregory-Tuckett)"
IGN = {"1Cor":(2,"anonima","Ign. Ef. 16,1; 18,1; Rom. 5,1; 9,2","1 Cor 6,9-10; 1,18-20; 4,4; 15,8-9 «Ignatius must have known this Epistle almost by heart» (NTAF, clase A)","no","Pablo nombrado en Ign. Ef. 12,2 («ἐν πάσῃ ἐπιστολῇ μνημονεύει ὑμῶν»), Rom. 4,3: alusión a sus cartas, sin cita nominal"),
       "Ef":(2,"anonima","Ign. Pol. 5,1; Ef. 1,1; 20,1","Ef 5,25.29; 1,1?; 2,20-22 (NTAF, clase B)","sí","Ign. Ef. 12,2 podría aludir a la carta a los Efesios: se codifica juicio"),
       "Rom":(1,"na","Ign. Esm. 1,1; Ef. 19,3","Rom 1,3-4 (NTAF, clase C)","sí",""),
       "2Cor":(1,"na","Ign. Tral. 9,2","2 Cor 4,14 (NTAF, clase D)","sí",""),
       "Gal":(1,"na","Ign. Fil. 1,1","Gal 1,1 (NTAF, clase C/D)","sí",""),
       "Flp":(1,"na","Ign. Esm. 4,2","Flp 4,13 (NTAF, clase C/D)","sí",""),
       "1Tim":(1,"na","Ign. Magn. 8,1; Pol. 4,3","1 Tim 1,4; 6,2 (NTAF, clase C/D)","sí",""),
       "2Tim":(1,"na","Ign. Ef. 2,1; Esm. 10,2","2 Tim 1,16 (NTAF, clase C)","sí",""),
       "Tit":(1,"na","NTAF, entrada «Titus c» (pasajes no transcritos aquí)","(NTAF, clase C)","sí",""),
       "Col":(1,"na","Ign. Ef. 2,1; Tral. 5,2","Col 1,7; 1,16 (NTAF, clase D)","sí",""),
       "1Tes":(1,"na","Ign. Ef. 10,1","1 Tes 5,17 (NTAF, clase D)","sí",""),
       "2Tes":(1,"na","—","(NTAF, clase D)","sí",""),
       "Flm":(1,"na","Ign. Ef. 2,1","ἀνέπαυσεν ~ Flm 7.20 (NTAF, clase D)","sí",""),
       "Heb":(1,"na","Ign. Fil. 9,1","«ἀρχιερεύς» (NTAF, clase D)","sí","")}
for c,(at,atr,pas,cita,j,nota) in IGN.items():
    add(c,"Ign","c. 110 (105-170)",at,atr,"na",pas,F_NTAF_I,cita,j,nota)

# ---- Policarpo (NTAF 1905, pp. 84-104) ----
F_NTAF_P = "Oxford Society, NTAF (1905), Polycarp, pp. 84-104 (clases A-D); verificado el 29-IX-2026 en archive.org; Berding 2002; Holmes 2005 (en Gregory-Tuckett)"
POL = {"Flp":(3,"Pablo","Pol. Fil. 3,2; 11,3","«Paul … who, when absent, wrote you letters (ἐπιστολάς)» (3,2); «in principio epistulae eius» (11,3) (NTAF, Filipenses)","no","atribución explícita de carta(s) a los Filipenses a Pablo"),
       "1Cor":(3,"Pablo","Pol. Fil. 11,2","«aut nescimus quia sancti mundum iudicabunt? sicut Paulus docet» = 1 Cor 6,2 (NTAF, clase A)","no",""),
       "Ef":(2,"anonima","Pol. Fil. 12,1; 1,3","«ut his scripturis dictum est: irascimini et nolite peccare, et sol non occidat super iracundiam vestram» = Ef 4,26; Ef 2,8-9 (NTAF, clase B)","no","citada como Escritura, sin nombre"),
       "Gal":(2,"anonima","Pol. Fil. 5,1; 3,3","«Deus non deridetur» = Gal 6,7; «mater omnium nostrum» = Gal 4,26 (NTAF, clase B)","no",""),
       "Rom":(2,"anonima","Pol. Fil. 6,2","Rom 14,10.12 (NTAF, clase B)","sí",""),
       "2Cor":(2,"anonima","Pol. Fil. 2,2; 6,2","2 Cor 4,14; 5,10 (NTAF, clase B)","sí",""),
       "1Tim":(2,"anonima","Pol. Fil. 4,1","«initium omnium malorum est amor pecuniae … nihil intulimus in hunc mundum» = 1 Tim 6,10.7 (NTAF, clase B)","no",""),
       "2Tim":(2,"anonima","Pol. Fil. 5,2; 9,2","2 Tim 2,12; 4,10 (NTAF, clase B)","sí",""),
       "2Tes":(2,"anonima","Pol. Fil. 11,3-4","2 Tes 1,4; 3,15 «non sicut inimicos» (NTAF, clase B)","sí",""),
       "Heb":(1,"na","Pol. Fil. 12,2; 6,3","«sempiternus pontifex» ~ Heb 6,20; 7,3; Heb 4,12-13 (NTAF, clase C)","sí",""),
       "Col":(1,"na","Pol. Fil. 10,1; 11,2","Col 1,23; 3,5 (NTAF, clase D)","sí",""),
       "1Tes":(1,"na","Pol. Fil. 4,3","«orationibus … sine intermissione» ~ 1 Tes 5,17 (NTAF, sin entrada propia)","sí",""),
       "Tit":(0,"na","—","sin entrada en NTAF (Tit 2,4-5 solo como paralelo cruzado)","no",""),
       "Flm":(0,"na","—","sin paralelo registrado","no","")}
for c,(at,atr,pas,cita,j,nota) in POL.items():
    add(c,"Pol","c. 110-140",at,atr,"na",pas,F_NTAF_P,cita,j,nota)

# ---- Ireneo, Adversus haereses (texto ANF completo, libros I-V, earlychristianwritings.com, verificado el 29-IX-2026) ----
F_IREN = "Ireneo, Adversus haereses I-V (trad. Roberts-Rambaut, ANF 1; texto íntegro de los cinco libros leído en earlychristianwritings.com/text/irenaeus-bookN.html el 29-IX-2026); Hebreos: Eusebio HE V 26 (newadvent.org/fathers/250105.htm)"
IREN = {"Rom":(3,"Pablo","AH III 16,3.9; 22,1","«Paul, when writing to the Romans, has explained this very point: “Paul, an apostle of Jesus Christ…”»"),
        "1Cor":(3,"Pablo","AH III 11,9; 13,1; 18,2","«in his Epistle to the Corinthians, he speaks expressly of prophetical gifts»; «writing to the Corinthians, he declares, “But we preach Christ Jesus crucified”»"),
        "2Cor":(3,"Pablo","AH III 7,1","«Paul said plainly in the Second [Epistle] to the Corinthians, “In whom the god of this world hath blinded…”»"),
        "Gal":(3,"Pablo","AH III 7,2; 13,3; 16,3; 22,1","«The Apostle Paul, moreover, in the Epistle to the Galatians, declares plainly, “God sent His Son, made of a woman”»"),
        "Ef":(3,"Pablo","AH V 2,3; 8,1; 14,3; 24,4","«the blessed Paul declares in his Epistle to the Ephesians, that “we are members of His body…”»"),
        "Flp":(3,"Pablo","AH V 13,3-4; IV 18,4","«confessed in his Epistle to the Philippians that “to live in the flesh was the fruit of [his] work”»"),
        "1Tes":(3,"Pablo","AH V 6,1","«the apostle … saying thus in the first Epistle to the Thessalonians, “Now the God of peace sanctify you perfect…”»"),
        "2Tes":(3,"Pablo","AH III 7,2; V 25,1.3","«in the Second to the Thessalonians, speaking of Antichrist, he says…»; «the Apostle Paul again, speaking in the second [Epistle] to the Thessalonians»"),
        "1Tim":(3,"Pablo","AH III 3,3; I praef. 1","«Of this Linus, Paul makes mention in the Epistles to Timothy»"),
        "2Tim":(3,"Pablo","AH III 14,1; III 3,3","«Paul has himself declared also in the Epistles, saying: “Demas hath forsaken me… Only Luke is with me”» (2 Tim 4,10-11)"),
        "Tit":(3,"Pablo","AH III 3,4; I 16,3","«as Paul also says, “A man that is an heretic, after the first and second admonition, reject…”» (Tit 3,10)"),
        "Col":(3,"Pablo","AH III 14,1","«he says, in the Epistle to the Colossians: “Luke, the beloved physician, greets you”»"),
        "Flm":(0,"na","—","ninguna cita ni alusión en AH I-V (búsqueda en el texto íntegro; concuerda con Biblia Patristica 1)"),
        "Heb":(2,"negada","Eusebio HE V 26; AH II 30,9 (Heb 1,3 «verbo virtutis suae»?)","«a volume containing various Dissertations, in which he mentions the Epistle to the Hebrews … making quotations from them» (HE V 26); Esteban Gobar (ap. Focio, Bibl. 232): Ireneo e Hipólito negaban que fuera de Pablo")}
for c,(at,atr,pas,cita) in IREN.items():
    add(c,"Iren","c. 180",at,atr,"na",pas,F_IREN,cita,"sí" if c=="Heb" else "no","" if c!="Heb" else "sin cita nominal en AH; uso atestiguado por Eusebio en obra perdida; atribución negada según Gobar/Focio (testimonio del s. VI/IX)")

# ---- Clemente de Alejandría ----
F_CLAL = "Biblia Patristica 1 (1975), índice de Clemente de Alejandría (Biblindex inaccesible el 29-IX-2026: verificación anti-robots); Hebreos: Eusebio HE VI 14,2-4 (verificado en newadvent.org/fathers/250106.htm)"
for c in CARTAS:
    if c=="Flm":
        add(c,"ClemAl","c. 190-215",0,"na","na","—",F_CLAL,"sin cita ni alusión de Filemón en el índice de Biblia Patristica 1","sí","codificado por índice impreso, sin verificación en línea")
    elif c=="Heb":
        add(c,"ClemAl","c. 190-215",3,"Pablo","na","Hypotyposeis ap. Eusebio HE VI 14,2-4; Strom. VI 8,62",F_CLAL,"«He says that the Epistle to the Hebrews is the work of Paul, and that it was written to the Hebrews in the Hebrew language; but that Luke translated it» (HE VI 14,2)","no","atribución a Pablo con teoría de traducción por Lucas")
    else:
        add(c,"ClemAl","c. 190-215",3,"Pablo","na","Stromata, Paedagogus, Protrepticus (numerosas citas con «ὁ ἀπόστολος»)",F_CLAL,"citas con nombre («Παῦλος», «ὁ ἀπόστολος») registradas en Biblia Patristica 1","sí","codificado por índice impreso, sin verificación en línea del pasaje concreto")

# ---- Tertuliano ----
F_TERT2 = "Tertuliano, Adv. Marc. V (verificado en newadvent.org/fathers/03125.htm), De praescriptione haereticorum 25 y 33 (newadvent.org/fathers/0311.htm), De pudicitia 20 (newadvent.org/fathers/0407.htm), todos leídos el 29-IX-2026; Biblia Patristica 1"
TERT = {"Rom":"Adv. Marc. V 13-14","1Cor":"Adv. Marc. V 5-10","2Cor":"Adv. Marc. V 11-12","Gal":"Adv. Marc. V 2-4; De praescr. 33","Flp":"Adv. Marc. V 20","1Tes":"Adv. Marc. V 15","Flm":"Adv. Marc. V 21",
        "Ef":"Adv. Marc. V 17-18 («we hold to have been written to the Ephesians»)","Col":"Adv. Marc. V 19; De praescr. 7","2Tes":"Adv. Marc. V 16",
        "1Tim":"De praescr. 25 («Paul addressed even this expression to Timothy: O Timothy, guard that which is entrusted to you», 1 Tim 6,20); 33 (1 Tim 4,3)",
        "2Tim":"De praescr. 25 (2 Tim 1,14 «That good thing which was committed unto you keep»)","Tit":"De praescr. 33 («who also intimates to Titus, that a man who is a heretic must be rejected», Tit 3,10-11); 6"}
for c,pas in TERT.items():
    add(c,"Tert","c. 197-220",3,"Pablo","na",pas,F_TERT2,"comentario o cita con nombre de Pablo en el pasaje indicado")
add("Heb","Tert","c. 197-220",2,"otro (Bernabé)","na","De pudicitia 20",F_TERT2,"«there is extant withal an Epistle to the Hebrews under the name of Barnabas»","no","uso claro con atribución a otro autor")

# ---- Orígenes ----
F_ORIG = "Biblia Patristica 3 (1980), índice de Orígenes (Biblindex inaccesible el 29-IX-2026); Hebreos: Eusebio HE VI 25,11-14 (verificado en newadvent.org/fathers/250106.htm)"
for c in CARTAS:
    if c=="Heb":
        add(c,"Orig","c. 220-250",3,"Pablo",14,"Hom. in Hebr. ap. Eusebio HE VI 25,11-14",F_ORIG,"«the thoughts are those of the apostle, but the diction and phraseology are those of some one who remembered the apostolic teachings … who wrote the epistle, in truth, God knows»","no","atribución a Pablo con reserva sobre la redacción")
    elif c=="Flm":
        add(c,"Orig","c. 220-250",3,"Pablo","na","Hom. in Jer. 19,?; Comm. in Matt. (según Biblia Patristica 3)",F_ORIG,"citas de Filemón con nombre de Pablo registradas en Biblia Patristica 3","sí","codificado por índice impreso, sin verificación en línea")
    else:
        add(c,"Orig","c. 220-250",3,"Pablo","na","comentarios y homilías (numerosas citas con «ὁ ἀπόστολος»)",F_ORIG,"citas con nombre registradas en Biblia Patristica 3","sí","codificado por índice impreso, sin verificación en línea del pasaje concreto")

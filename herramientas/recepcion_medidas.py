# -*- coding: utf-8 -*-
"""Escribe results/canales/recepcion.csv y recepcion_medidas.csv a partir de recepcion_datos.py (docs/canales/codigos_recepcion.md § 3-4)."""
import csv, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from recepcion_datos import R, CARTAS
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# fechas (convencional, extremo tardío) y ámbito por testigo
T = {"1Clem":(96,140,"Occ"),"Ign":(110,170,"Or"),"Pol":(120,140,"Or"),"Marc":(144,144,"Occ"),"Mur":(190,200,"Occ"),"Iren":(180,185,"Occ"),
     "ClemAl":(200,215,"Or"),"Tert":(210,220,"Occ"),"Orig":(240,250,"Or"),"P46":(200,250,"Or"),"Eus":(325,325,"Or"),"Athan":(367,367,"Or")}
def pap_fechas(f):
    return {"ca. 200":(200,225),"III":(250,300),"IV":(350,400)}.get(f,(None,None))
def fechas(r):
    if r["testigo"]=="Pap":
        c,t = pap_fechas(r["fecha_testigo"]); return c,t,"Or"
    if r["testigo"]=="Orden": return None,None,None
    return T[r["testigo"]]
cols = ["carta","testigo","fecha_testigo","atestacion","atribucion","posicion","pasaje","fuente","cita","juicio","nota"]
os.makedirs(f"{REPO}/results/canales", exist_ok=True)
order = ["1Clem","Ign","Pol","Marc","Mur","Iren","ClemAl","Tert","Orig","P46","Pap","Eus","Athan","Orden"]
rows = sorted(R, key=lambda r:(CARTAS.index(r["carta"]), order.index(r["testigo"])))
with open(f"{REPO}/results/canales/recepcion.csv","w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols,lineterminator="\r\n"); w.writeheader(); w.writerows(rows)
med=[]
for L in CARTAS:
    rs=[r for r in R if r["carta"]==L and r["testigo"]!="Orden"]
    def first(n, amb=None, key=1, juicio_ok=True):
        vals=[]
        for r in rs:
            if r["atestacion"]=="na" or int(r["atestacion"])<n: continue
            if not juicio_ok and r["juicio"]=="sí": continue
            c,t,a=fechas(r)
            if amb and a!=amb: continue
            vals.append((c,t)[key])
        return min(vals) if vals else None
    n3=[r for r in rs if r["atestacion"]!="na" and int(r["atestacion"])==3]
    atrs=[r["atribucion"] for r in n3]; atrs_all=[r["atribucion"] for r in rs]
    if any(a=="negada" for a in atrs_all): est="negada"
    elif any(a.startswith("otro") for a in atrs_all) or any(a=="anonima" for a in atrs): est="vacilante"
    elif n3: est="estable"
    else: est="sin datos"
    g=lambda t: next((r for r in R if r["carta"]==L and r["testigo"]==t), None)
    pap=g("Pap"); p46=g("P46"); marc=g("Marc"); mur=g("Mur")
    d=dict(carta=L,
           n1_tardia=first(1,key=1), n2_tardia=first(2,key=1), n3_tardia=first(3,key=1),
           n3_tardia_Occ=first(3,"Occ",1), n3_tardia_Or=first(3,"Or",1),
           n1_conv=first(1,key=0), n2_conv=first(2,key=0), n3_conv=first(3,key=0), n3_conv_Occ=first(3,"Occ",0), n3_conv_Or=first(3,"Or",0),
           n2_tardia_sin_juicio=first(2,key=1,juicio_ok=False), n3_tardia_sin_juicio=first(3,key=1,juicio_ok=False),
           estabilidad_atribucion=est, atribuciones_n3=";".join(sorted(set(atrs))) if atrs else "",
           papiro_mas_antiguo=pap["pasaje"].split(";")[0] if pap else "", posicion_P46=p46["posicion"], posicion_Marcion=marc["posicion"], posicion_Muratori=mur["posicion"])
    for k in ("tardia","conv"):
        occ,orr=d[f"n3_{k}_Occ"],d[f"n3_{k}_Or"]
        d[f"asimetria_{k}"]= (occ-orr) if (occ is not None and orr is not None) else None
    # lectura § 2.2 (umbrales fijados en codigos_recepcion.md § 4; regla conservadora: fechas tardías)
    def lectura(k):
        n2,n3,occ,orr,asim=d[f"n2_{k}"],d[f"n3_{k}"],d[f"n3_{k}_Occ"],d[f"n3_{k}_Or"],d[f"asimetria_{k}"]
        temprana = n2 is not None and n2<=150 and occ is not None and orr is not None and occ<=200 and orr<=200
        simetrica = asim is not None and abs(asim)<=50
        ausente_col = (marc["posicion"]=="ausente") or (p46["posicion"]=="ausente" and p46["juicio"]=="no")
        tardia = (occ is None or occ>200) or (orr is None or orr>200) or not simetrica
        if temprana and simetrica and est=="estable": return "H1-H3 (temprana, simétrica, estable)"
        if tardia and est in ("vacilante","negada","sin datos"): return "H5 (tardía o asimétrica, atribución vacilante/ausente)"
        if tardia or ausente_col: return "H4 (tardía o desigual, o ausente de las colecciones antiguas)"
        return "no decide"
    d["lectura_umbrales_absolutos_tardia"]=lectura("tardia"); d["lectura_umbrales_absolutos_conv"]=lectura("conv")
    med.append(d)
# lectura con el mismo rasero (§ 9: «leída con el mismo rasero que las indiscutidas»): rango del núcleo
core=[d for d in med if d["carta"] in ("Rom","1Cor","2Cor","Gal","Flp","1Tes","Flm")]
mx_n2=max(d["n2_tardia"] for d in core); mx_n3=max(d["n3_tardia"] for d in core)
asims=[d["asimetria_tardia"] for d in core if d["asimetria_tardia"] is not None]
for d in med:
    d["nucleo_max_n2_tardia"]=mx_n2; d["nucleo_max_n3_tardia"]=mx_n3; d["nucleo_asimetria_min"]=min(asims); d["nucleo_asimetria_max"]=max(asims)
    dentro = (d["n2_tardia"] is not None and d["n2_tardia"]<=mx_n2+50) and (d["n3_tardia"] is not None and d["n3_tardia"]<=mx_n3+50)
    d["dentro_rango_nucleo"] = "sí" if dentro else "no"
    if d["estabilidad_atribucion"] in ("vacilante","negada"):
        d["lectura_mismo_rasero"]="H1-H3 no compatible (atribución no estable); H4 compatible; H5 compatible"
    elif dentro:
        d["lectura_mismo_rasero"]="H1, H2, H3, H4 compatibles (el canal no las separa: el núcleo muestra el mismo patrón); H5 no compatible"
    else:
        d["lectura_mismo_rasero"]="H1-H3 debilitadas (atestación más tardía que la del núcleo); H4 compatible; H5 no decide"
    d["colecciones_antiguas"] = f"Marción {d['posicion_Marcion']}; 𝔓46 {d['posicion_P46']}; Muratori {d['posicion_Muratori']}"
mcols=list(med[0].keys())
with open(f"{REPO}/results/canales/recepcion_medidas.csv","w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=mcols,lineterminator="\r\n"); w.writeheader(); w.writerows(med)
for d in med:
    print(f"{d['carta']:5s} n2t={d['n2_tardia']} n3t={d['n3_tardia']} Occ={d['n3_tardia_Occ']} Or={d['n3_tardia_Or']} asim={d['asimetria_tardia']} | conv n2={d['n2_conv']} n3={d['n3_conv']} asim={d['asimetria_conv']} | {d['estabilidad_atribucion']:9s} | T: {d['lectura_umbrales_absolutos_tardia'][:6]} | MR: {d['lectura_mismo_rasero'][:40]}")

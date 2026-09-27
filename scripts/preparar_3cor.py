#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preparar_3cor.py — normaliza la transcripción diplomática de la respuesta de Pablo en P. Bodmer X (3 Corintios)
y produce el fichero de alineación con cada intervención (D-006).

Entradas (en data/local/):
  3Cor_diplomatica_respuesta_de_Pablo.txt  transcripción diplomática (texto de Testuz reproducido por dhspriory.org),
                                           solo la respuesta de Pablo, con los signos editoriales del paquete del autor
  3Cor_normalizada_fuente.txt              texto normalizado escrito a mano (531 palabras), una decisión por palabra
Salidas:
  3Cor_BORRADOR.txt / 3Cor_alineacion_BORRADOR.tsv (hasta la validación del autor; después 3Cor.txt / 3Cor_alineacion.tsv)
"""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); LOCAL=os.path.join(os.path.dirname(HERE),'data','local')
DIPLO=os.path.join(LOCAL,'3Cor_diplomatica_respuesta_de_Pablo.txt'); NORM=os.path.join(LOCAL,'3Cor_normalizada_fuente.txt')
suf='' if '--final' in sys.argv else '_BORRADOR'
OUT_TSV=os.path.join(LOCAL,f'3Cor_alineacion{suf}.tsv'); OUT_TXT=os.path.join(LOCAL,f'3Cor{suf}.txt')
import re, unicodedata, json
t=open(DIPLO,encoding='utf-8').read()
toks=[x for x in t.split() if x not in ('¦','.....') and not re.fullmatch(r'\d+',x)]
groups=[ (["ΘΑΥΜΑ","ΖΩ"],1),(["ΠΟΝΗ","ΡΟΥ"],1),(["ΤΗΝΕΛ","ΕΥΣ<Ι>"],2),(["ΠΑΡΑΧΑΡΑ","ΣΟΝΤΩΝ"],1),(["ΠΑΡΕ","ΛΑΒΟΝ"],1),
 (["ΑΠΟΣΤΟ","ΛΩΝ"],1),(["ΑΠΟΣ","ΤΑΛΕΝΤΟΣ"],1),(["ΕΛΕΥΘΕΡΩ","ΣΗ"],1),(["ΤΥ","ΠΟΝ"],1),(["Ι","ΝΑ"],1),(["ΠΑΝΤΟ","ΚΡΑΤΩΡ"],1),
 (["ΖΕΙΕΧΕΙΡΙ","ΖΕΤΟ"],1),(["ΕΝΕΠΟΛΕΙ","ΤΕΥΕΤΟ"],1),(["ΝΙΚΗ","ΘΕΙΣ"],1),(["ΤΕ","ΚΝΑ"],1),(["ΑΝΑΚΟ","ΠΤΟΥΣΕΙΝ"],1),
 (["ΚΑΤΗΡΑΜΕ","ΝΗΝ"],1),(["ΑΠΟ","ΦΕΥΓΕΤΕ"],1),(["ΕΚΕΙ","ΝΟΙΣ"],1),(["ΟΥ","ΤΕ"],1),(["ΒΑΛ","ΛΕΤΕ"],1),(["ΕΝ","ΣΩ","ΜΑ"],1),
 (["ΣΠΕΡΜΑ","Τ]ΩΝ"],1),(["ΚΗ","ΤΟΣ]"],1),(["ΠΡΟΣΕΥΧΟΜΕ","ΝΟΥ"],1),(["ΕΞΕ","ΓΕΙΡΕΙ"],1),(["ΕΠΕΙΡΕΙΦΕΝ","ΤΕΣ"],1),
 (["ΑΝΑΣΤΗ","ΣΕΣΘΕ"],1),(["ΑΝ[ΑΣ","ΤΑΣΙΝ"],1),(["ΠΡΟ","ΦΗΤΩΝ"],1),(["ΜΕ","Τ"],1),(["ΤΕΚΝΗΜΑ","ΤΑ"],1),(["ΑΠΟΤΡΕΠΕΣ","ΘΕ"],1),
 (["[[Ο]]"],0),(["ΠΡΟΟΔΥΠΟΡ[","]Μ"],0)]
# build units: list of (diplo tokens list, n_norm)
units=[]; i=0
while i<len(toks):
    hit=None
    for g,n in groups:
        if toks[i:i+len(g)]==g and (i==0 or True):
            hit=(g,n); break
    if hit: units.append((hit[0],hit[1])); i+=len(hit[0])
    else: units.append(([toks[i]],1)); i+=1
# guard: 'ΟΥ ΤΕ' join only where followed by ΓΑΡ; 'ΑΠΟ ΦΕΥΓΕΤΕ' unique; 'ΠΡΟ ΦΗΤΩΝ' unique; 'ΕΝ ΣΩ ΜΑ' unique; 'Ι ΝΑ' unique; 'ΤΕ ΚΝΑ' unique
norm=open(NORM,encoding='utf-8').read().split()
need=sum(n for _,n in units)
print("unidades",len(units),"normalizados necesarios",need,"normalizados dados",len(norm))
def fold(s):
    s=re.sub(r'[\[\]<>’\'·̣]','',s)  # brackets, apostrophes, underdots
    s=unicodedata.normalize('NFD',s); s=''.join(c for c in s if not unicodedata.combining(c))
    return s.upper().replace('Σ','Σ').replace('ς','Σ')
rows=[]; k=0; pos=0
NS={"<ΧΡΥ>","<ΙΗΥ>","<ΚΣ>","<ΧΡΣ>","<ΙΗΣ>","<ΔΑΥΙΔ>","<ΠΝΣ>","<ΠΡΣ>","<ΑΝΠΣ>","<ΘΣ>","<ΙΣΡΛ>","<ΑΝΠΝ>","<ΠΝΑ>","<ΘΥ>","<ΧΡΝ>","<ΙΗΝ>","<ΙΣΡΗΛ>","<ΑΝΠΟΥ>","<ΚΥ>","<ΑΝΝ̣ΩΝ>"}
CORRUPT={"ζειεχειριζετο","ερξ","ἐλεγχθητο"}
for g,n in units:
    outs=norm[k:k+n]; k+=n; pos+=1
    d=' '.join(g)
    if n==0: tipo="supresión (letra tachada / palabra incompleta en laguna)"
    elif any(o in CORRUPT for o in outs): tipo="forma corrupta conservada sin corregir — PENDIENTE DE DECISIÓN"
    elif any(x in NS for x in g): tipo="expansión de nomen sacrum"
    elif len(g)>1 and n==1: tipo="unión de palabra partida por cambio de línea"
    elif len(g)==2 and n==2: tipo="resegmentación (dos palabras escritas unidas/partidas)"
    elif any(c in d for c in '[]<>'): tipo="restitución editorial de letras (Testuz)"
    else:
        f1=fold(d.replace(' ','')); f2=''.join(fold(o) for o in outs)
        tipo="minúsculas y acentuación" if f1==f2 else "ortografía (itacismo / grafía del copista) y acentuación"
    rows.append((pos,d,' '.join(outs),tipo))
import collections
c=collections.Counter(r[3] for r in rows); print(json.dumps(c,ensure_ascii=False,indent=1))
with open(OUT_TSV,'w',encoding='utf-8') as f:
    f.write("n\tforma_papiro\tforma_normalizada\ttipo\n")
    for r in rows: f.write("\t".join(map(str,r))+"\n")
with open(OUT_TXT,'w',encoding='utf-8') as f: f.write(' '.join(norm)+"\n")
print("tokens normalizados:",len(norm))
# print orthographic rows for review
for r in rows:
    if r[3].startswith(("ortograf","forma corrupta","resegment","restituci")): print(r[0],r[1],"→",r[2],"|",r[3][:22])

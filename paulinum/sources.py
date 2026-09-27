# -*- coding: utf-8 -*-
"""
sources.py — manifiesto de los textos: identificador, autor, obra, género, subgénero,
destinatario, fecha, estado, tradición, edición, repositorio, licencia; listas NT, AF,
CONTROLS (campaña 01) y CONTROLS_03 (ampliación de la campaña 03).

RECONSTRUCCIÓN. El manifiesto original se perdió con el código. Este se ha reconstruido a partir
de: (a) la composición por autor, tradición y estado de results/campana_03/inventory.csv impresa
en el Apéndice A.2; (b) el § 8.2 del libro (composición del conjunto de control y estados
auditados); (c) el § 0.1 de los dos informes (Anexos I y II); y (d) las rutas reales de los
repositorios Perseus canonical-greekLit y First1KGreek, comprobadas el 25-IX-2026. Donde el libro
no fija la obra concreta (p. ej. cuáles son los 5 opúsculos de Luciano o los 6 discursos de
Aristides), la elección se marca con `reconstruido=True` y se justifica en `nota`. El número de
documentos que resulta de cada colección puede diferir en unas unidades del inventario publicado.

Estados (§ 8.2): core (núcleo paulino), target (carta discutida), genuine (autoría segura),
spurious (pseudoepigrafía conocida), disputed (atribución discutida; fuera de la calibración),
other (anónimo o no verificable; solo impostor y negativo), duplicate (misma obra en otra
edición; solo ruido de edición), mixed (carta genuina interpolada, recensión larga de Ignacio).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

RAW_PERSEUS = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/"
RAW_F1K = "https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/"
RAW_MORPHGNT = "https://raw.githubusercontent.com/morphgnt/sblgnt/master/"
RAW_AF = "https://raw.githubusercontent.com/jtauber/apostolic-fathers/master/texts/"
RAW_PROIEL = "https://raw.githubusercontent.com/proiel/proiel-treebank/master/"
RAW_MACULA = "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/"

REPOS = {
    "morphgnt": {"nombre": "MorphGNT/SBLGNT 6.12", "url": "https://github.com/morphgnt/sblgnt",
                 "licencia": "SBLGNT © SBL y Logos; MorphGNT CC BY-SA 3.0", "raw": RAW_MORPHGNT},
    "af": {"nombre": "Open Apostolic Fathers (Lake; Tauber y Macdonald)",
           "url": "https://github.com/jtauber/apostolic-fathers", "licencia": "CC BY-SA 4.0", "raw": RAW_AF},
    "perseus": {"nombre": "Perseus canonical-greekLit", "url": "https://github.com/PerseusDL/canonical-greekLit",
                "licencia": "CC BY-SA 4.0", "raw": RAW_PERSEUS},
    "f1k": {"nombre": "Open Greek and Latin, First1KGreek",
            "url": "https://github.com/OpenGreekAndLatin/First1KGreek", "licencia": "CC BY-SA 4.0", "raw": RAW_F1K},
    "proiel": {"nombre": "PROIEL treebank, greek-nt.xml (Tischendorf)", "url": "https://github.com/proiel/proiel-treebank",
               "licencia": "CC BY-NC-SA 3.0", "raw": RAW_PROIEL},
    "macula": {"nombre": "MACULA Greek (Clear Bible), Nestle 1904", "url": "https://github.com/Clear-Bible/macula-greek",
               "licencia": "CC BY 4.0", "raw": RAW_MACULA},
    "local": {"nombre": "data/local (preparado a mano)", "url": "", "licencia": "véase LEEME de cada archivo", "raw": ""},
}


@dataclass
class Source:
    id: str                 # identificador del documento o de la colección
    author: str
    work: str
    status: str             # core | target | genuine | spurious | disputed | other | duplicate | mixed
    tradition: str          # cristiano | judeo-helenistico | pagano
    repo: str               # morphgnt | af | perseus | f1k | proiel | macula | local
    path: str               # ruta relativa dentro del repositorio (o de data/local)
    parser: str             # morphgnt | af | tei | proiel | macula | local
    genre: str = "prosa"
    subgenre: str = "otra"
    addressee: str = "publico"   # individuo | comunidad | publico | si_mismo
    date: str = ""
    edition: str = ""
    license: str = ""
    split: str = ""          # '' (un documento) | letters | books | chapters
    work_group: str = ""     # marca de obra compuesta (los libros de una misma obra no forman pares positivos)
    tier: int = 1            # 1: NT y Padres Apostólicos; 2: controles campaña 01; 3: ampliación campaña 03
    min_tokens: int = 0      # umbral de extensión para las partes de una colección
    max_docs: int = 0        # tope de documentos de una colección (0 = sin tope)
    edition_key: str = "sblgnt"  # sblgnt | tischendorf | nestle1904 | lake | perseus | f1k | local
    note: str = ""
    reconstruido: bool = False
    part_status: dict = field(default_factory=dict)  # estado por parte (p. ej. cartas apócrifas de Juliano)
    part_author: dict = field(default_factory=dict)  # autor por parte (p. ej. Galo César en las cartas de Juliano)

    @property
    def url(self) -> str:
        return REPOS[self.repo]["raw"] + self.path if self.repo != "local" else ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["url"] = self.url
        return d


# ---------------------------------------------------------------------------------------------
# Nuevo Testamento (MorphGNT / SBLGNT) — 27 libros
# ---------------------------------------------------------------------------------------------
_NT_BOOKS = [
    # id, archivo MorphGNT, autor, obra, estado, subgénero, destinatario
    ("Mt", "61-Mt", "Mateo(anon)", "Evangelio de Mateo", "other", "evangelio", "publico"),
    ("Mc", "62-Mk", "Marcos(anon)", "Evangelio de Marcos", "other", "evangelio", "publico"),
    ("Lc", "63-Lk", "Lucas(anon)", "Evangelio de Lucas", "genuine", "evangelio", "individuo"),
    ("Jn", "64-Jn", "Juan(anon)", "Evangelio de Juan", "genuine", "evangelio", "publico"),
    ("Hch", "65-Ac", "Lucas(anon)", "Hechos de los Apóstoles", "genuine", "historia", "individuo"),
    ("Rom", "66-Ro", "Pablo", "Romanos", "core", "carta_comunidad", "comunidad"),
    ("1Cor", "67-1Co", "Pablo", "1 Corintios", "core", "carta_comunidad", "comunidad"),
    ("2Cor", "68-2Co", "Pablo", "2 Corintios", "core", "carta_comunidad", "comunidad"),
    ("Gal", "69-Ga", "Pablo", "Gálatas", "core", "carta_comunidad", "comunidad"),
    ("Ef", "70-Eph", "Pablo?", "Efesios", "target", "circular", "comunidad"),
    ("Flp", "71-Php", "Pablo", "Filipenses", "core", "carta_comunidad", "comunidad"),
    ("Col", "72-Col", "Pablo?", "Colosenses", "target", "carta_comunidad", "comunidad"),
    ("1Tes", "73-1Th", "Pablo", "1 Tesalonicenses", "core", "carta_comunidad", "comunidad"),
    ("2Tes", "74-2Th", "Pablo?", "2 Tesalonicenses", "target", "carta_comunidad", "comunidad"),
    ("1Tim", "75-1Ti", "Pablo?", "1 Timoteo", "target", "mandato", "individuo"),
    ("2Tim", "76-2Ti", "Pablo?", "2 Timoteo", "target", "testamentaria", "individuo"),
    ("Tit", "77-Tit", "Pablo?", "Tito", "target", "mandato", "individuo"),
    ("Flm", "78-Phm", "Pablo", "Filemón", "core", "recomendacion", "individuo"),
    ("Heb", "79-Heb", "anon", "Hebreos", "other", "homilia", "comunidad"),
    ("Sant", "80-Jas", "Santiago(?)", "Santiago", "other", "parenetica", "comunidad"),
    ("1Pe", "81-1Pe", "Pedro(?)", "1 Pedro", "other", "circular", "comunidad"),
    ("2Pe", "82-2Pe", "Pedro(?)", "2 Pedro", "other", "testamentaria", "comunidad"),
    ("1Jn", "83-1Jn", "Juan(anon)", "1 Juan", "disputed", "homilia", "comunidad"),
    ("2Jn", "84-2Jn", "Juan(presb.)", "2 Juan", "other", "carta_comunidad", "comunidad"),
    ("3Jn", "85-3Jn", "Juan(presb.)", "3 Juan", "other", "recomendacion", "individuo"),
    ("Jud", "86-Jud", "Judas(?)", "Judas", "other", "circular", "comunidad"),
    ("Ap", "87-Re", "Juan(vidente)", "Apocalipsis", "other", "apocalipsis", "comunidad"),
]

NT: list[Source] = [
    Source(id=i, author=a, work=w, status=st, tradition="cristiano", repo="morphgnt",
           path=f"{f}-morphgnt.txt", parser="morphgnt", genre="carta" if "carta" in sg or sg in
           ("circular", "mandato", "testamentaria", "recomendacion", "parenetica") else sg,
           subgenre=sg, addressee=ad, date="s. I", edition="SBLGNT (MorphGNT 6.12)",
           license=REPOS["morphgnt"]["licencia"], tier=1, edition_key="sblgnt")
    for (i, f, a, w, st, sg, ad) in _NT_BOOKS
]

# Ediciones alternativas del NT (campaña 02b): un solo archivo por edición; el analizador
# reparte los 27 libros con los mismos identificadores y estados que NT.
NT_TISCHENDORF = Source(id="NT_tischendorf", author="(NT)", work="Nuevo Testamento, Tischendorf 8.ª",
                        status="collection", tradition="cristiano", repo="proiel", path="greek-nt.xml",
                        parser="proiel", edition="Tischendorf (PROIEL greek-nt.xml)",
                        license=REPOS["proiel"]["licencia"], tier=2, edition_key="tischendorf")
NT_NESTLE1904 = Source(id="NT_nestle1904", author="(NT)", work="Nuevo Testamento, Nestle 1904",
                       status="collection", tradition="cristiano", repo="macula",
                       path="Nestle1904/tsv/macula-greek-Nestle1904.tsv", parser="macula",
                       edition="Nestle 1904 (MACULA)", license=REPOS["macula"]["licencia"], tier=2,
                       edition_key="nestle1904")

# ---------------------------------------------------------------------------------------------
# Padres Apostólicos (Open Apostolic Fathers, texto de Lake)
# ---------------------------------------------------------------------------------------------
_AF = [
    ("1Clem", "001-i_clement", "Clemente Romano", "1 Clemente", "genuine", "carta_comunidad", "comunidad"),
    ("2Clem", "002-ii_clement", "Ps-Clemente", "2 Clemente", "spurious", "homilia", "comunidad"),
    ("IgnEf", "003-ignatius-ephesians", "Ignacio", "Ignacio a los Efesios", "genuine", "carta_comunidad", "comunidad"),
    ("IgnMagn", "004-ignatius-magnesians", "Ignacio", "Ignacio a los Magnesios", "genuine", "carta_comunidad", "comunidad"),
    ("IgnTral", "005-ignatius-trallians", "Ignacio", "Ignacio a los Tralianos", "genuine", "carta_comunidad", "comunidad"),
    ("IgnRom", "006-ignatius-romans", "Ignacio", "Ignacio a los Romanos", "genuine", "carta_comunidad", "comunidad"),
    ("IgnFil", "007-ignatius-philadelphians", "Ignacio", "Ignacio a los Filadelfios", "genuine", "carta_comunidad", "comunidad"),
    ("IgnEsm", "008-ignatius-smyrnaeans", "Ignacio", "Ignacio a los Esmirniotas", "genuine", "carta_comunidad", "comunidad"),
    ("IgnPol", "009-ignatius-polycarp", "Ignacio", "Ignacio a Policarpo", "genuine", "mandato", "individuo"),
    ("PolFil", "010-polycarp-philippians", "Policarpo", "Policarpo a los Filipenses", "genuine", "carta_comunidad", "comunidad"),
    ("Did", "011-didache", "anon", "Didajé", "other", "manual", "comunidad"),
    ("Bern", "012-barnabas", "Ps-Bernabé", "Carta de Bernabé", "spurious", "homilia", "comunidad"),
    ("Herm", "013-shepherd", "Hermas", "El Pastor", "genuine", "apocalipsis", "comunidad"),
    ("MartPol", "014-martyrdom", "anon", "Martirio de Policarpo", "other", "carta_comunidad", "comunidad"),
    ("Diogn", "015-diognetus", "anon", "A Diogneto", "other", "apologia", "individuo"),
]
AF: list[Source] = [
    Source(id=i, author=a, work=w, status=st, tradition="cristiano", repo="af", path=f"{f}.txt", parser="af",
           genre="carta" if sg in ("carta_comunidad", "mandato") else sg, subgenre=sg, addressee=ad,
           date="c. 95-150", edition="Lake, Loeb 1912-1913 (Open Apostolic Fathers)",
           license=REPOS["af"]["licencia"], tier=1, edition_key="lake")
    for (i, f, a, w, st, sg, ad) in _AF
]

# 3 Corintios (P. Bodmer X, Testuz 1959), preparado a mano en data/local — véase data/local/LEEME_3Cor.md
THREE_COR = Source(id="3Cor", author="Ps-Pablo", work="3 Corintios (respuesta de «Pablo»)", status="spurious",
                   tradition="cristiano", repo="local", path="3Cor.txt", parser="local", genre="carta",
                   subgenre="carta_comunidad", addressee="comunidad", date="s. II",
                   edition="Testuz 1959 (P. Bodmer X), ortografía regularizada", license="dominio público (texto antiguo)",
                   tier=1, edition_key="local", note="solo la respuesta de Pablo (531 palabras)")


def _p(id, author, work, status, tradition, path, **kw) -> Source:
    kw.setdefault("license", REPOS["perseus"]["licencia"])
    kw.setdefault("edition_key", "perseus")
    return Source(id=id, author=author, work=work, status=status, tradition=tradition, repo="perseus",
                  path=path, parser="tei", **kw)


def _f(id, author, work, status, tradition, path, **kw) -> Source:
    kw.setdefault("license", REPOS["f1k"]["licencia"])
    kw.setdefault("edition_key", "f1k")
    return Source(id=id, author=author, work=work, status=status, tradition=tradition, repo="f1k",
                  path=path, parser="tei", **kw)


# ---------------------------------------------------------------------------------------------
# Controles de la campaña 01 (217 documentos con NT, AF y 3 Cor)
# ---------------------------------------------------------------------------------------------
CONTROLS: list[Source] = [
    # Josefo: 30 libros (AJ 20, BJ 7, Vita, C. Ap. 2); edición Niese
    _p("Jos_AJ", "Josefo", "Antigüedades judías", "genuine", "judeo-helenistico",
       "tlg0526/tlg001/tlg0526.tlg001.perseus-grc2.xml", split="books", work_group="Jos_AJ", genre="historia",
       date="93-94", edition="Niese 1887-1890", tier=2),
    _p("Jos_BJ", "Josefo", "Guerra judía", "genuine", "judeo-helenistico",
       "tlg0526/tlg004/tlg0526.tlg004.perseus-grc2.xml", split="books", work_group="Jos_BJ", genre="historia",
       date="75-79", edition="Niese 1894", tier=2),
    _p("Jos_Vita", "Josefo", "Vida", "genuine", "judeo-helenistico",
       "tlg0526/tlg002/tlg0526.tlg002.perseus-grc2.xml", genre="autobiografia", addressee="publico",
       date="c. 99", edition="Niese 1890", tier=2),
    _p("Jos_CAp", "Josefo", "Contra Apión", "genuine", "judeo-helenistico",
       "tlg0526/tlg003/tlg0526.tlg003.perseus-grc2.xml", split="books", work_group="Jos_CAp", genre="apologia",
       subgenre="apologia", addressee="individuo", date="c. 97", edition="Niese 1889", tier=2),
    # Juliano: cartas (Wright); las apócrifas 74-83 como spurious; Galo César como autor aparte
    _p("Jul_Ep", "Juliano", "Cartas", "genuine", "pagano",
       "tlg2003/tlg013/tlg2003.tlg013.perseus-grc2.xml", split="letters", genre="carta", subgenre="carta_individuo",
       addressee="individuo", date="355-363", edition="Wright, Loeb 1923", tier=2, min_tokens=200,
       part_status={str(n): "spurious" for n in range(74, 84)},
       part_author={**{str(n): "Ps-Juliano" for n in range(74, 84)}, "82": "Galo César"},
       note="cartas 74-83 apócrifas según el índice de Wright; la 82 (Galo a Juliano) se atribuye a Galo César (status other)"),
    # Isócrates: 8 cartas y 5 discursos (edición Norlin / Van Hook)
    _p("Isoc_Ep", "Isócrates", "Cartas", "genuine", "pagano", "", split="letters", genre="carta",
       subgenre="carta_individuo", addressee="individuo", date="s. IV a. C.", edition="Van Hook, Loeb 1945",
       tier=2, note="ver ISOCRATES_LETTERS: nueve archivos de Perseus, uno por carta"),
    _p("Isoc_Paneg", "Isócrates", "Panegírico", "genuine", "pagano", "tlg0010/tlg011/tlg0010.tlg011.perseus-grc2.xml",
       genre="discurso", subgenre="epidictico", date="380 a. C.", edition="Norlin, Loeb 1928", tier=2),
    _p("Isoc_AdNic", "Isócrates", "A Nicocles", "genuine", "pagano", "tlg0010/tlg013/tlg0010.tlg013.perseus-grc2.xml",
       genre="discurso", subgenre="mandato", addressee="individuo", date="c. 374 a. C.", edition="Norlin, Loeb 1928", tier=2),
    _p("Isoc_Nic", "Isócrates", "Nicocles", "genuine", "pagano", "tlg0010/tlg014/tlg0010.tlg014.perseus-grc2.xml",
       genre="discurso", subgenre="mandato", date="c. 372 a. C.", edition="Norlin, Loeb 1928", tier=2),
    _p("Isoc_Evag", "Isócrates", "Evágoras", "genuine", "pagano", "tlg0010/tlg015/tlg0010.tlg015.perseus-grc2.xml",
       genre="discurso", subgenre="epidictico", date="c. 370 a. C.", edition="Norlin, Loeb 1928", tier=2),
    _p("Isoc_Areop", "Isócrates", "Areopagítico", "genuine", "pagano", "tlg0010/tlg018/tlg0010.tlg018.perseus-grc2.xml",
       genre="discurso", subgenre="deliberativo", date="c. 355 a. C.", edition="Norlin, Loeb 1929", tier=2,
       reconstruido=True, note="el libro fija 5 discursos sin nombrarlos todos; se eligen Panegírico, A Nicocles, Nicocles, Evágoras y Areopagítico"),
    # Plutarco: 7 opúsculos genuinos (Vernardakis), Consolatio ad Apollonium disputed, De lib. educ. y De fato spurious
    _p("Plut_Curios", "Plutarco", "De curiositate", "genuine", "pagano", "tlg0007/tlg102/tlg0007.tlg102.perseus-grc2.xml",
       genre="tratado", subgenre="etica", date="c. 100", edition="Vernardakis (Teubner)", tier=2),
    _p("Plut_Conj", "Plutarco", "Conjugalia praecepta", "genuine", "pagano", "tlg0007/tlg078/tlg0007.tlg078.perseus-grc2.xml",
       genre="tratado", subgenre="mandato", addressee="individuo", date="c. 100", edition="Vernardakis (Teubner)", tier=2),
    _p("Plut_Garr", "Plutarco", "De garrulitate", "genuine", "pagano", "tlg0007/tlg101/tlg0007.tlg101.perseus-grc2.xml",
       genre="tratado", subgenre="etica", date="c. 100", edition="Vernardakis (Teubner)", tier=2, reconstruido=True),
    _p("Plut_Tranq", "Plutarco", "De tranquillitate animi", "genuine", "pagano", "tlg0007/tlg096/tlg0007.tlg096.perseus-grc2.xml",
       genre="tratado", subgenre="consolatoria", addressee="individuo", date="c. 100", edition="Vernardakis (Teubner)", tier=2, reconstruido=True),
    _p("Plut_Ira", "Plutarco", "De cohibenda ira", "genuine", "pagano", "tlg0007/tlg095/tlg0007.tlg095.perseus-grc2.xml",
       genre="dialogo", subgenre="etica", date="c. 100", edition="Vernardakis (Teubner)", tier=2, reconstruido=True),
    _p("Plut_Superst", "Plutarco", "De superstitione", "genuine", "pagano", "tlg0007/tlg080/tlg0007.tlg080.perseus-grc2.xml",
       genre="tratado", subgenre="polemica", date="c. 100", edition="Vernardakis (Teubner)", tier=2, reconstruido=True),
    _p("Plut_VirtMor", "Plutarco", "De virtute morali", "genuine", "pagano", "tlg0007/tlg094/tlg0007.tlg094.perseus-grc2.xml",
       genre="tratado", subgenre="etica", date="c. 100", edition="Vernardakis (Teubner)", tier=2, reconstruido=True),
    _p("Plut_ConsApoll", "Ps-Plutarco", "Consolatio ad Apollonium", "disputed", "pagano", "tlg0007/tlg076/tlg0007.tlg076.perseus-grc2.xml",
       genre="tratado", subgenre="consolatoria", addressee="individuo", date="s. I-II", edition="Vernardakis (Teubner)", tier=2),
    _p("Plut_LibEd", "Ps-Plutarco", "De liberis educandis", "spurious", "pagano", "tlg0007/tlg067/tlg0007.tlg067.perseus-grc2.xml",
       genre="tratado", subgenre="mandato", date="s. I-II", edition="Vernardakis (Teubner)", tier=2, note="imita a Plutarco"),
    _p("Plut_Fato", "Ps-Plutarco", "De fato", "spurious", "pagano", "tlg0007/tlg108/tlg0007.tlg108.perseus-grc2.xml",
       genre="tratado", subgenre="filosofia", date="s. II", edition="Vernardakis (Teubner)", tier=2, note="imita a Plutarco"),
    # Luciano: 5 obras (Harmon / Jacobitz)
    _p("Luc_Nigr", "Luciano", "Nigrino", "genuine", "pagano", "tlg0062/tlg007/tlg0062.tlg007.perseus-grc2.xml",
       genre="dialogo", subgenre="carta_individuo", addressee="individuo", date="s. II", edition="Harmon, Loeb 1913", tier=2, reconstruido=True),
    _p("Luc_Demon", "Luciano", "Demonacte", "genuine", "pagano", "tlg0062/tlg008/tlg0062.tlg008.perseus-grc2.xml",
       genre="biografia", subgenre="otra", date="s. II", edition="Harmon, Loeb 1913", tier=2, reconstruido=True),
    _p("Luc_Timon", "Luciano", "Timón", "genuine", "pagano", "tlg0062/tlg022/tlg0062.tlg022.perseus-grc2.xml",
       genre="dialogo", subgenre="satira", date="s. II", edition="Harmon, Loeb 1915", tier=2, reconstruido=True),
    _p("Luc_Hermot", "Luciano", "Hermótimo", "genuine", "pagano", "tlg0062/tlg063/tlg0062.tlg063.perseus-grc2.xml",
       genre="dialogo", subgenre="polemica", date="s. II", edition="Jacobitz (Teubner)", tier=2, reconstruido=True),
    _p("Luc_Peregr", "Luciano", "De morte Peregrini", "genuine", "pagano", "tlg0062/tlg042/tlg0062.tlg042.perseus-grc2.xml",
       genre="carta", subgenre="carta_individuo", addressee="individuo", date="c. 165", edition="Harmon, Loeb 1936", tier=2, reconstruido=True),
    # Arriano: Anábasis (7 libros) e Índica (Roos); carta a Lucio Gelio (other)
    _p("Arr_Anab", "Arriano", "Anábasis de Alejandro", "genuine", "pagano", "tlg0074/tlg001/tlg0074.tlg001.perseus-grc2.xml",
       split="books", work_group="Arr_Anab", genre="historia", date="s. II", edition="Roos (Teubner)", tier=2),
    _p("Arr_Ind", "Arriano", "Índica", "genuine", "pagano", "tlg0074/tlg002/tlg0074.tlg002.perseus-grc2.xml",
       genre="historia", subgenre="geografia", date="s. II", edition="Roos (Teubner)", tier=2),
    _f("Arr_EpGell", "Arriano", "Carta a Lucio Gelio", "other", "pagano", "tlg0074/tlg008/tlg0074.tlg008.1st1K-grc1.xml",
       genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. II", edition="Hercher 1873", tier=2),
    # Epicteto (Arriano): Disertaciones (4 libros) y Manual (Schenkl)
    _p("Epict_Diss", "Epicteto(ap. Arriano)", "Disertaciones", "genuine", "pagano", "tlg0557/tlg001/tlg0557.tlg001.perseus-grc2.xml",
       split="books", work_group="Epict_Diss", genre="diatriba", subgenre="exhortacion", date="c. 108", edition="Schenkl (Teubner) 1916", tier=2,
       min_tokens=300, note="el prefacio (carta de Arriano a Gelio, ~190 palabras) queda bajo el umbral"),
    _p("Epict_Ench", "Epicteto(ap. Arriano)", "Manual", "genuine", "pagano", "tlg0557/tlg002/tlg0557.tlg002.perseus-grc2.xml",
       genre="tratado", subgenre="mandato", date="c. 125", edition="Schenkl (Teubner) 1916", tier=2),
    # Marco Aurelio: 12 libros
    _p("MAur", "Marco Aurelio", "Meditaciones", "genuine", "pagano", "tlg0562/tlg001/tlg0562.tlg001.perseus-grc2.xml",
       split="books", work_group="MAur", genre="meditacion", subgenre="otra", addressee="si_mismo", date="170-180",
       edition="Haines, Loeb 1916", tier=2),
    # Filón: 3 obras en la campaña 01 (De opificio, De vita Mosis I, Legatio ad Gaium); ampliación en CONTROLS_03
    _f("Phil_Opif", "Filón", "De opificio mundi", "genuine", "judeo-helenistico", "tlg0018/tlg001/tlg0018.tlg001.1st1K-grc1.xml",
       genre="tratado", subgenre="exegesis", date="s. I", edition="Cohn 1896", tier=2, reconstruido=True),
    _f("Phil_Legat", "Filón", "Legatio ad Gaium", "genuine", "judeo-helenistico", "tlg0018/tlg031/tlg0018.tlg031.1st1K-grc1.xml",
       genre="historia", subgenre="apologia", date="c. 41", edition="Reiter 1915", tier=2, reconstruido=True),
    _f("Phil_Flacc", "Filón", "In Flaccum", "genuine", "judeo-helenistico", "tlg0018/tlg030/tlg0018.tlg030.1st1K-grc1.xml",
       genre="historia", subgenre="apologia", date="c. 41", edition="Reiter 1915", tier=2, reconstruido=True),
    # Alcifrón, Filóstrato, Ignacio (edición Perseus/F1K: duplicados), 1 Clemente (duplicado), Ps-Clementinas, Ps-Ignacio
    _f("Alciphr", "Alcifrón", "Cartas", "genuine", "pagano", "tlg0640/tlg001/tlg0640.tlg001.1st1K-grc1.xml",
       genre="carta", subgenre="carta_ficticia", addressee="individuo", date="s. II-III", edition="Schepers 1905", tier=2,
       note="la colección entera como un solo documento (20.504 palabras en el inventario)"),
    _p("Philostr_Ep", "Filóstrato", "Cartas y dialexeis", "genuine", "pagano", "tlg0638/tlg006/tlg0638.tlg006.perseus-grc2.xml",
       genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. III", edition="Kayser (Teubner) 1871", tier=2,
       reconstruido=True, note="el inventario da un documento de 7.595 palabras; se elige el epistolario"),
    _f("Ign_dup", "Ignacio", "Cartas (recensión media, ed. Funk-Diekamp / F1K)", "duplicate", "cristiano",
       "tlg1443/tlg001/tlg1443.tlg001.1st1K-grc1.xml", split="letters", genre="carta", subgenre="carta_comunidad",
       addressee="comunidad", date="c. 110", edition="Funk-Diekamp 1913 (F1K)", tier=2,
       note="duplicado de edición de las siete cartas; solo para el ruido de edición"),
    _f("1Clem_dup", "Clemente Romano", "1 Clemente (ed. F1K)", "duplicate", "cristiano",
       "tlg1271/tlg001/tlg1271.tlg001.1st1K-grc1.xml", genre="carta", subgenre="carta_comunidad", addressee="comunidad",
       date="c. 96", edition="Funk-Bihlmeyer (F1K)", tier=2, note="duplicado de edición; solo ruido de edición"),
    _f("IgnLong", "Ps-Ignacio", "Recensión larga (interpoladas y espurias)", "mixed", "cristiano",
       "tlg1443/tlg002/tlg1443.tlg002.1st1K-grc1.xml", split="letters", genre="carta", subgenre="carta_comunidad",
       addressee="comunidad", date="s. IV", edition="Funk-Diekamp 1913", tier=2,
       note="numeración del archivo de First1KGreek: 13 María de Casóbola a Ignacio, 1 a María, 4 Tarsenses, 5 Filipenses, "
            "9 Antioquenos, 10 Herón = espurias; 2 Tralianos, 3 Magnesios, 6 Filadelfios, 7 Esmirniotas, 8 Policarpo, "
            "11 Efesios, 12 Romanos = interpoladas (mixed)",
       part_status={str(n): "spurious" for n in (1, 4, 5, 9, 10, 13)}),
    _f("PsClem_EpPet", "Ps-Clemente", "Carta de Pedro a Santiago", "spurious", "cristiano",
       "tlg1271/tlg003/tlg1271.tlg003.1st1K-grc1.xml", genre="carta", subgenre="carta_individuo", addressee="individuo",
       date="s. III-IV", edition="Rehm (GCS)", tier=2, note="imita a Clemente Romano (Homilías pseudoclementinas)"),
    _f("PsClem_EpJac", "Ps-Clemente", "Carta de Clemente a Santiago", "spurious", "cristiano",
       "tlg1271/tlg005/tlg1271.tlg005.1st1K-grc1.xml", genre="carta", subgenre="carta_individuo", addressee="individuo",
       date="s. III-IV", edition="Rehm (GCS)", tier=2, note="imita a Clemente Romano"),
]
# Las nueve cartas de Isócrates en Perseus son archivos separados (tlg022-tlg030); se registran una a una.
ISOCRATES_LETTERS: list[Source] = [
    _p(f"Isoc_Ep{n}", "Isócrates", f"Carta (Perseus tlg0010.tlg0{n})", "genuine", "pagano",
       f"tlg0010/tlg0{n}/tlg0010.tlg0{n}.perseus-grc{'3' if n == 26 else '2'}.xml",
       genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. IV a. C.", edition="Van Hook, Loeb 1945",
       tier=2, min_tokens=200, note="las nueve cartas ocupan tlg022-tlg030 en Perseus; el libro cuenta 8 de extensión suficiente")
    for n in range(22, 31)
]
CONTROLS = [s for s in CONTROLS if s.id != "Isoc_Ep"] + ISOCRATES_LETTERS

# ---------------------------------------------------------------------------------------------
# Ampliación de la campaña 03 (sources.CONTROLS_03): 60 entradas → 191 documentos
# ---------------------------------------------------------------------------------------------
_PHILO_F1K = {  # tlg → (id, obra, split)
    "002": ("Phil_LegAll", "Legum allegoriae I-III", "books"), "003": ("Phil_Cher", "De Cherubim", ""),
    "004": ("Phil_Sacr", "De sacrificiis", ""), "005": ("Phil_Det", "Quod deterius", ""),
    "006": ("Phil_Post", "De posteritate Caini", ""), "007": ("Phil_Gig", "De gigantibus", ""),
    "008": ("Phil_Immut", "Quod Deus sit immutabilis", ""), "009": ("Phil_Agr", "De agricultura", ""),
    "010": ("Phil_Plant", "De plantatione", ""), "011": ("Phil_Ebr", "De ebrietate", ""),
    "012": ("Phil_Sobr", "De sobrietate", ""), "013": ("Phil_Conf", "De confusione linguarum", ""),
    "014": ("Phil_Migr", "De migratione Abrahami", ""), "015": ("Phil_Her", "Quis rerum divinarum heres", ""),
    "016": ("Phil_Congr", "De congressu", ""), "017": ("Phil_Fug", "De fuga et inventione", ""),
    "018": ("Phil_Mut", "De mutatione nominum", ""), "019": ("Phil_Somn", "De somniis I-II", "books"),
    "020": ("Phil_Abr", "De Abrahamo", ""), "021": ("Phil_Jos", "De Josepho", ""),
    "022": ("Phil_Mos", "De vita Mosis I-II", "books"), "023": ("Phil_Decal", "De decalogo", ""),
    "024": ("Phil_Spec", "De specialibus legibus I-IV", "books"), "025": ("Phil_Virt", "De virtutibus", ""),
    "026": ("Phil_Praem", "De praemiis et poenis", ""), "027": ("Phil_Prob", "Quod omnis probus liber sit", ""),
    "028": ("Phil_Contempl", "De vita contemplativa", ""),
}
CONTROLS_03: list[Source] = [
    _f(i, "Filón", w, "genuine", "judeo-helenistico", f"tlg0018/tlg{t}/tlg0018.tlg{t}.1st1K-grc1.xml",
       split=sp, work_group=i if sp else "", genre="tratado", subgenre="exegesis", date="s. I",
       edition="Cohn-Wendland-Reiter 1896-1915", tier=3)
    for t, (i, w, sp) in _PHILO_F1K.items()
] + [
    _f("Phil_Aet", "Filón", "De aeternitate mundi", "disputed", "judeo-helenistico", "tlg0018/tlg029/tlg0018.tlg029.1st1K-grc1.xml",
       genre="tratado", subgenre="filosofia", date="s. I", edition="Cohn-Reiter 1915", tier=3, note="autenticidad debatida (F-5)"),
    # Apologistas y escritores cristianos de los siglos II-III
    _f("Just_Apol1", "Justino", "Apología I", "genuine", "cristiano", "tlg0645/tlg001/tlg0645.tlg001.1st1K-grc1.xml",
       genre="apologia", subgenre="apologia", addressee="individuo", date="c. 155", edition="Rauschen 1911", tier=3),
    _f("Just_Apol2", "Justino", "Apología II", "genuine", "cristiano", "tlg0645/tlg002/tlg0645.tlg002.perseus-grc2.xml",
       genre="apologia", subgenre="apologia", addressee="publico", date="c. 155", edition="Rauschen 1911", tier=3),
    _f("Just_Dial", "Justino", "Diálogo con Trifón", "genuine", "cristiano", "tlg0645/tlg003/tlg0645.tlg003.perseus-grc2.xml",
       split="chapters", work_group="Just_Dial", genre="dialogo", subgenre="polemica", addressee="individuo", date="c. 160",
       edition="Archambault 1909", tier=3, max_docs=40, min_tokens=400,
       note="cuarenta capítulos (agrupados hasta ≥ 400 palabras) según el inventario publicado"),
    _f("Tat", "Taciano", "Discurso a los griegos", "genuine", "cristiano", "tlg1766/tlg001/tlg1766.tlg001.perseus-grc1.xml",
       genre="apologia", subgenre="apologia", date="c. 170", edition="Schwartz 1888", tier=3),
    _f("Athen_Leg", "Atenágoras", "Legatio pro Christianis", "genuine", "cristiano", "tlg1205/tlg001/tlg1205.tlg001.perseus-grc2.xml",
       genre="apologia", subgenre="apologia", addressee="individuo", date="c. 177", edition="Schwartz 1891", tier=3),
    _f("Athen_Res", "Atenágoras", "De resurrectione", "disputed", "cristiano", "tlg1205/tlg002/tlg1205.tlg002.perseus-grc2.xml",
       genre="tratado", subgenre="apologia", date="s. II-III", edition="Schwartz 1891", tier=3, note="autenticidad debatida (F-5)"),
    _f("Theoph", "Teófilo de Antioquía", "Ad Autolycum", "genuine", "cristiano", "tlg1725/tlg001/tlg1725.tlg001.perseus-grc2.xml",
       split="books", work_group="Theoph", genre="apologia", subgenre="apologia", addressee="individuo", date="c. 180",
       edition="Otto 1861", tier=3),
    _f("ClemAl_Protr", "Clemente de Alejandría", "Protréptico", "genuine", "cristiano", "tlg0555/tlg001/tlg0555.tlg001.1st1K-grc1.xml",
       genre="apologia", subgenre="exhortacion", date="c. 195", edition="Stählin 1905", tier=3),
    _f("ClemAl_Paed", "Clemente de Alejandría", "Pedagogo", "genuine", "cristiano", "tlg0555/tlg002/tlg0555.tlg002.1st1K-grc1.xml",
       split="books", work_group="ClemAl_Paed", genre="tratado", subgenre="mandato", date="c. 197", edition="Stählin 1905", tier=3),
    _f("ClemAl_QDS", "Clemente de Alejandría", "Quis dives salvetur", "genuine", "cristiano", "tlg0555/tlg006/tlg0555.tlg006.1st1K-grc1.xml",
       genre="homilia", subgenre="exhortacion", date="c. 200", edition="Stählin 1909", tier=3),
    _f("Orig_CC", "Orígenes", "Contra Celso", "genuine", "cristiano", "tlg2042/tlg001/tlg2042.tlg001.perseus-grc1.xml",
       split="books", work_group="Orig_CC", genre="apologia", subgenre="polemica", date="c. 248", edition="Koetschau 1899", tier=3),
    _f("Orig_Orat", "Orígenes", "De oratione", "genuine", "cristiano", "tlg2042/tlg008/tlg2042.tlg008.perseus-grc1.xml",
       genre="tratado", subgenre="exegesis", addressee="individuo", date="c. 233", edition="Koetschau 1899", tier=3),
    _f("Orig_Mart", "Orígenes", "Exhortación al martirio", "genuine", "cristiano", "tlg2042/tlg007/tlg2042.tlg007.perseus-grc1.xml",
       genre="tratado", subgenre="exhortacion", addressee="individuo", date="235", edition="Koetschau 1899", tier=3),
    _f("Orig_EpAfr", "Orígenes", "Carta a Africano", "genuine", "cristiano", "tlg2042/tlg045/tlg2042.tlg045.1st1K-grc1.xml",
       genre="carta", subgenre="carta_individuo", addressee="individuo", date="c. 240", edition="De Lange (SC 302)", tier=3),
    _f("ActThom", "anon(Acta Thomae)", "Hechos de Tomás", "other", "cristiano", "tlg2038/tlg001/tlg2038.tlg001.1st1K-grc1.xml",
       genre="novela", subgenre="otra", date="s. III", edition="Bonnet 1903", tier=3),
    _f("PassPerp", "anon(Passio Perpetuae)", "Pasión de Perpetua (griego)", "other", "cristiano", "tlg2016/tlg001/tlg2016.tlg001.1st1K-grc1.xml",
       genre="relato", subgenre="otra", date="s. III", edition="Robinson 1891", tier=3),
    # Pseudepígrafos judíos
    _f("TestAbr", "anon(Test. Abrahae)", "Testamento de Abrahán (rec. A)", "other", "judeo-helenistico", "tlg1701/tlg001/tlg1701.tlg001.1st1K-grc1.xml",
       genre="relato", subgenre="testamentaria", date="s. I-II", edition="James 1892", tier=3),
    _f("VitProph", "anon(Vitae Prophetarum)", "Vidas de los profetas", "other", "judeo-helenistico", "tlg1750/tlg002/tlg1750.tlg002.1st1K-grc1.xml",
       genre="relato", subgenre="biografia", date="s. I", edition="Schermann 1907", tier=3, reconstruido=True,
       note="recensión anónima (4.083 palabras en el inventario)"),
    _f("Enoch", "anon(Enoch)", "Enoc griego (fragmentos)", "other", "judeo-helenistico", "tlg1463/tlg001/tlg1463.tlg001.1st1K-grc1.xml",
       genre="apocalipsis", subgenre="apocalipsis", date="s. II a. C.-I d. C.", edition="Black 1970 / Swete", tier=3),
    # Paganos añadidos
    _f("VettVal", "Vetio Valente", "Antologías", "genuine", "pagano", "tlg1764/tlg001/tlg1764.tlg001.1st1K-grc1.xml",
       split="books", work_group="VettVal", genre="tratado", subgenre="tecnico", date="s. II", edition="Kroll 1908", tier=3),
    _f("Herm_I", "anon(Hermetica)", "Corpus Hermeticum I (Poimandres)", "other", "pagano", "tlg1286/tlg001/tlg1286.tlg001.1st1K-grc1.xml",
       genre="tratado", subgenre="religioso", date="s. II-III", edition="Scott 1924", tier=3),
    _f("Herm_IV", "anon(Hermetica)", "Corpus Hermeticum IV", "other", "pagano", "tlg1286/tlg004/tlg1286.tlg004.1st1K-grc1.xml",
       genre="tratado", subgenre="religioso", date="s. II-III", edition="Scott 1924", tier=3),
    _f("Herm_X", "anon(Hermetica)", "Corpus Hermeticum X", "other", "pagano", "tlg1286/tlg010/tlg1286.tlg010.1st1K-grc1.xml",
       genre="tratado", subgenre="religioso", date="s. II-III", edition="Scott 1924", tier=3),
    _f("Herm_XIII", "anon(Hermetica)", "Corpus Hermeticum XIII", "other", "pagano", "tlg1286/tlg013/tlg1286.tlg013.1st1K-grc1.xml",
       genre="tratado", subgenre="religioso", date="s. II-III", edition="Scott 1924", tier=3),
    _f("Herm_XVI", "anon(Hermetica)", "Corpus Hermeticum XVI", "other", "pagano", "tlg1286/tlg016/tlg1286.tlg016.1st1K-grc1.xml",
       genre="tratado", subgenre="religioso", date="s. II-III", edition="Scott 1924", tier=3),
    _f("Polemon", "Polemón", "Declamaciones", "genuine", "pagano", "tlg1617/tlg001/tlg1617.tlg001.1st1K-grc1.xml",
       genre="discurso", subgenre="epidictico", date="s. II", edition="Hinck 1873", tier=3),
    # Elio Aristides: seis discursos, tres de ellos himnos en prosa (Dindorf / Keil)
    _p("Arist_Or43", "Elio Aristides", "Or. 43, Himno a Zeus", "genuine", "pagano", "tlg0284/tlg043/tlg0284.tlg043.perseus-grc2.xml",
       genre="discurso", subgenre="himno", date="s. II", edition="Dindorf 1829 / Keil 1898", tier=3, reconstruido=True),
    _p("Arist_Or45", "Elio Aristides", "Or. 45, A Sarapis", "genuine", "pagano", "tlg0284/tlg045/tlg0284.tlg045.perseus-grc2.xml",
       genre="discurso", subgenre="himno", date="s. II", edition="Dindorf 1829 / Keil 1898", tier=3, reconstruido=True),
    _p("Arist_Or41", "Elio Aristides", "Or. 41, A Dioniso", "genuine", "pagano", "tlg0284/tlg041/tlg0284.tlg041.perseus-grc2.xml",
       genre="discurso", subgenre="himno", date="s. II", edition="Dindorf 1829 / Keil 1898", tier=3, reconstruido=True),
    _p("Arist_Or26", "Elio Aristides", "Or. 26, A Roma", "genuine", "pagano", "tlg0284/tlg026/tlg0284.tlg026.perseus-grc2.xml",
       genre="discurso", subgenre="epidictico", date="s. II", edition="Dindorf 1829 / Keil 1898", tier=3, reconstruido=True),
    _p("Arist_Or24", "Elio Aristides", "Or. 24, A los rodios sobre la concordia", "genuine", "pagano", "tlg0284/tlg024/tlg0284.tlg024.perseus-grc2.xml",
       genre="discurso", subgenre="deliberativo", addressee="comunidad", date="s. II", edition="Dindorf 1829 / Keil 1898", tier=3, reconstruido=True),
    _p("Arist_Or48", "Elio Aristides", "Or. 48, Discursos sagrados II", "genuine", "pagano", "tlg0284/tlg048/tlg0284.tlg048.perseus-grc2.xml",
       genre="discurso", subgenre="autobiografia", date="s. II", edition="Dindorf 1829 / Keil 1898", tier=3, reconstruido=True,
       note="el libro no nombra los seis discursos; se eligen tres himnos (43, 45, 41) y tres discursos de otro género (26, 24, 48)"),
    # Epistolografía pseudoepigráfica (Hercher) y Libanio
    _f("PsDiog", "Ps-Diógenes", "Cartas de Diógenes", "spurious", "pagano", "tlg1325/tlg001/tlg1325.tlg001.1st1K-grc1.xml",
       split="letters", genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. I a. C.-II d. C.",
       edition="Hercher 1873", tier=3, min_tokens=200, max_docs=15, note="quince cartas de extensión suficiente"),
    _f("PsEur", "Ps-Eurípides", "Cartas de Eurípides", "spurious", "pagano", "tlg1367/tlg001/tlg1367.tlg001.1st1K-grc1.xml",
       split="letters", genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. I-II", edition="Hercher 1873", tier=3),
    _f("PsSolon", "Ps-Solón", "Carta de Solón", "spurious", "pagano", "tlg1681/tlg001/tlg1681.tlg001.1st1K-grc1.xml",
       genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. I-II", edition="Hercher 1873", tier=3),
    _p("PsDem_Ep", "Demóstenes/Ps-Demóstenes", "Cartas", "disputed", "pagano", "tlg0014/tlg063/tlg0014.tlg063.perseus-grc2.xml",
       split="letters", genre="carta", subgenre="carta_comunidad", addressee="comunidad", date="s. IV a. C.",
       edition="Rennie (OCT) 1931", tier=3, min_tokens=200, note="cinco de las seis cartas superan el umbral"),
    _p("PsPlat_Ep", "Platón/Ps-Platón", "Cartas", "disputed", "pagano", "tlg0059/tlg036/tlg0059.tlg036.perseus-grc2.xml",
       split="letters", genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. IV a. C.",
       edition="Burnet (OCT) 1907", tier=3, min_tokens=200, note="once de las trece cartas superan el umbral"),
    _f("Liban_Ep", "Libanio", "Cartas", "genuine", "pagano", "tlg2200/tlg001/tlg2200.tlg001.1st1K-grc1.xml",
       split="letters", genre="carta", subgenre="carta_individuo", addressee="individuo", date="s. IV",
       edition="Foerster (Teubner) 1921-1922", tier=3, min_tokens=200, max_docs=44, reconstruido=True,
       note="44 cartas (12.130 palabras en el inventario): se toman las 44 primeras que superan las 200 palabras; el criterio original de selección no consta"),
]

ALL_SOURCES: list[Source] = NT + AF + [THREE_COR] + CONTROLS + CONTROLS_03
EDITION_SOURCES = {"sblgnt": None, "tischendorf": NT_TISCHENDORF, "nestle1904": NT_NESTLE1904}

# Núcleos y dianas (config: core = seven | hauptbriefe | seven_plus)
CORE_SETS = {
    "seven": ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm"],
    "hauptbriefe": ["Rom", "1Cor", "2Cor", "Gal"],
    "seven_plus": ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Col", "2Tes"],
}
TARGETS = ["Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit"]
# Cartas hermanas (dependencia literaria): la hermana se excluye de los candidatos (SISTERS)
SISTERS = {"Ef": ["Col"], "Col": ["Ef"], "2Tes": ["1Tes"], "1Tes": ["2Tes"]}
# Pseudoepigrafías conocidas → autor imitado (problemas pseudo_pairs)
IMITATED = {"Ps-Ignacio": "Ignacio", "Ps-Clemente": "Clemente Romano", "Ps-Plutarco": "Plutarco",
            "Ps-Juliano": "Juliano", "Ps-Pablo": "Pablo"}


def by_tier(max_tier: int) -> list[Source]:
    return [s for s in ALL_SOURCES if s.tier <= max_tier]


def manifest_rows() -> list[dict]:
    return [s.to_dict() for s in ALL_SOURCES]

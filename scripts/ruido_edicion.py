#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ruido_edicion.py — ruido de edición de las catorce cartas (PROTOCOLO § 5.4, último punto; D-015, D-013).

Para cada carta y cada edición alternativa o testigo disponible se mide la distancia entre el texto SBLGNT de la carta
y el texto de esa edición/testigo, con la misma distancia que el «mismo rasero» (mfw:300, ventanas de 500 palabras,
20 sorteos; min-max y delta) pero con las ventanas ALINEADAS (misma posición relativa en los dos textos, para que la
distancia mida solo lo que cambia entre ediciones y no la variación entre pasajes distintos de la carta), y se compara
con las distancias entre cartas distintas del núcleo (ventanas sorteadas por separado, como en el «mismo rasero»):
una diferencia entre cartas no se interpreta si es del tamaño del ruido de edición. Como referencia se dan también la
distancia con ventanas independientes y la de la carta SBLGNT consigo misma con ventanas independientes (variación
interna de la carta).

- Ediciones (Tischendorf = PROIEL, Nestle 1904 = MACULA): las dos versiones de la carta se recortan a los versículos
  que ambas contienen (recorte simétrico; p. ej. PROIEL no trae Hebreos 13), y se comparan sin diacríticos, como los
  testigos, para que las cifras sean comparables entre sí.
- Testigos (Sinaítico, 𝔓46): se compara el derivado regularizado del testigo con el SBLGNT recortado a las palabras
  que el testigo conserva (`sblgnt_rec_<testigo>`, docs/testigos_manuscritos.md § 5).
Todo se calcula en el espacio de rasgos del corpus SBLGNT de la campaña (vocabulario y clase cerrada de ahí), con las
dos máscaras de la rejilla. Necesita los corpus construidos (`python -m paulinum build --config config/sens/...`), que
dejan data/cache/corpus_<edición>.jsonl.

Salidas en results/<run>/: ruido_edicion_<métrica>.csv (una fila por carta, edición y máscara, con IC de sorteos y
percentil entre las distancias carta-carta del núcleo) y ruido_edicion_resumen.csv (por edición y máscara: ruido
máximo y mediano frente a la distancia mínima y mediana entre cartas del núcleo).

Uso: python scripts/ruido_edicion.py --run paulinum_1_0 [--config config/paulinum_1_0.yaml]
       [--ediciones tischendorf,nestle1904,sinaiticus,p46] [--edicion-base sblgnt]
"""
from __future__ import annotations

import argparse
import dataclasses
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paulinum.corpus import Document, cache_path, load_corpus, _ref_key  # noqa: E402
from paulinum.features import FeatureSpace, PersonFilter, learn_closed_class, load_lexicon  # noqa: E402
from paulinum.pipeline import _write_csv, load_config, campaign_sets, LETTERS_14  # noqa: E402
from paulinum.sources import WITNESS_EDITIONS  # noqa: E402
from paulinum.variables import DistanceMatrixBuilder, percentile_of, METRICS  # noqa: E402

EDICIONES = ["tischendorf", "nestle1904", "sinaiticus", "p46"]
MASCARAS = ["none", "formulae+preformed+otq+reuse"]
METRICAS = ["minmax", "delta"]


def _cut(doc: Document, keep: set, new_id: str) -> Document:
    """Copia del documento con solo los tokens cuyo versículo está en `keep` (máscaras incluidas)."""
    idx = [i for i, r in enumerate(doc.refs) if _ref_key(r) in keep]
    d = dataclasses.replace(doc, id=new_id, forms=[doc.forms[i] for i in idx],
                            forms_nodia=[doc.forms_nodia[i] for i in idx], lemmas=[doc.lemmas[i] for i in idx],
                            pos=[doc.pos[i] for i in idx], person=[doc.person[i] for i in idx],
                            mood=[doc.mood[i] for i in idx], refs=[doc.refs[i] for i in idx],
                            masks={k: [v[i] for i in idx] for k, v in doc.masks.items()})
    return d


def _verses(doc: Document) -> set:
    return {_ref_key(r) for r in doc.refs if _ref_key(r)[0]}


def aligned_draws(b: DistanceMatrixBuilder, a_id: str, b_id: str, rng: np.random.Generator) -> np.ndarray:
    """
    Distancias entre ventanas ALINEADAS de los dos textos de la misma carta: en cada sorteo se toma la misma posición
    relativa u en ambos (inicio = u · (longitud − W)), de modo que las dos ventanas cubren el mismo pasaje y la distancia
    mide solo lo que cambia entre ediciones, no la variación entre pasajes distintos de la carta (que es lo que medirían
    dos ventanas sorteadas por separado).
    """
    f = METRICS[b.metric]
    W = b.window
    ia, ib = b.ids[a_id], b.ids[b_id]
    out = []
    for _ in range(b.draws):
        u = float(rng.random())
        sa = int(u * max(0, len(ia) - W)) if W else 0
        sb = int(u * max(0, len(ib) - W)) if W else 0
        ca = b.fs.counts_from_ids(ia[sa:sa + W] if W and len(ia) > W else ia)
        cb = b.fs.counts_from_ids(ib[sb:sb + W] if W and len(ib) > W else ib)
        out.append(float(f(b._vec(ca), b._vec(cb))[0]))
    return np.array(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--config", default="config/paulinum_1_0.yaml")
    ap.add_argument("--ediciones", default=",".join(EDICIONES))
    ap.add_argument("--edicion-base", default="sblgnt")
    ap.add_argument("--sorteos", type=int, default=20)
    a = ap.parse_args()
    run_dir = os.path.join("results", a.run)
    os.makedirs(run_dir, exist_ok=True)
    cfg = load_config(a.config)
    base = load_corpus(a.edicion_base)
    by_id = {d.id: d for d in base}
    core, _, _ = campaign_sets(cfg, base)
    core = [c for c in core if c in by_id] or [c for c in ("Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm") if c in by_id]
    lexicon = load_lexicon(os.path.join("data", "cache", "lexicon_uniforme.tsv"))
    pf, closed = PersonFilter(base), learn_closed_class(base)
    # pares (carta, edición): documentos recortados simétricamente, con identificadores propios
    pares: list[tuple[str, str, Document, Document, str]] = []   # (carta, edición, doc_base, doc_alt, nota)
    for ed in [e.strip() for e in a.ediciones.split(",") if e.strip()]:
        if ed in WITNESS_EDITIONS:
            alt_key, rec_key = ed, f"sblgnt_rec_{ed}"
            if not (os.path.exists(cache_path(alt_key)) and os.path.exists(cache_path(rec_key))):
                print(f"  [ausente] {ed}: faltan data/cache/corpus_{alt_key}.jsonl o corpus_{rec_key}.jsonl")
                continue
            alt = {d.id: d for d in load_corpus(alt_key) if d.id in LETTERS_14}
            rec = {d.id: d for d in load_corpus(rec_key) if d.id in LETTERS_14}
            for L in LETTERS_14:
                if L in alt and L in rec and alt[L].n_tokens >= 100 and rec[L].n_tokens >= 100:
                    da = dataclasses.replace(rec[L], id=f"{L}@sblgnt_rec_{ed}")
                    db = dataclasses.replace(alt[L], id=f"{L}@{ed}")
                    pares.append((L, ed, da, db, "recorte simétrico por palabras conservadas (derivados del testigo)"))
                else:
                    print(f"  [sin datos] {ed} {L}: el testigo no conserva la carta o no llega a 100 palabras")
        else:
            if not os.path.exists(cache_path(ed)):
                print(f"  [ausente] {ed}: falta data/cache/corpus_{ed}.jsonl (python -m paulinum build --edition {ed})")
                continue
            alt = {d.id: d for d in load_corpus(ed) if d.id in LETTERS_14}
            for L in LETTERS_14:
                if L not in alt or L not in by_id:
                    continue
                common = _verses(by_id[L]) & _verses(alt[L])
                da = _cut(by_id[L], common, f"{L}@sblgnt_rec_{ed}")
                db = _cut(alt[L], common, f"{L}@{ed}")
                nota = ""
                if len(common) < len(_verses(by_id[L])):
                    nota = f"recorte simétrico a {len(common)} de {len(_verses(by_id[L]))} versículos de SBLGNT"
                if da.n_tokens >= 100 and db.n_tokens >= 100:
                    pares.append((L, ed, da, db, nota))
    if not pares:
        print("ningún par carta-edición disponible")
        return 0
    extra = [d for _, _, da, db, _ in pares for d in (da, db)]
    resumen = []
    filas: dict[str, list] = {m: [] for m in METRICAS}
    for mask in MASCARAS:
        fs = FeatureSpace("mfw:300", base, mask=mask, nodia=True, person_filter=pf, closed_set=closed, lexicon=lexicon)
        for metric in METRICAS:
            b = DistanceMatrixBuilder(base + extra, fs, metric, window=500, draws=a.sorteos, seed=11)
            core_d = np.array([b.pair_distance(x, y) for x, y in itertools.combinations(core, 2)])
            rows = []
            rng = np.random.default_rng(23)
            for L, ed, da, db, nota in pares:
                draws = aligned_draws(b, da.id, db.id, rng)
                d = float(np.mean(draws))
                indep = float(np.mean(b.pair_distance_draws(da.id, db.id)))   # ventanas sorteadas por separado
                mismo = float(np.mean(b.pair_distance_draws(da.id, da.id)))   # la carta SBLGNT consigo misma, ídem
                rows.append({"carta": L, "edicion": ed, "metrica": metric, "mascara": mask,
                             "tokens_sblgnt": da.n_tokens, "tokens_edicion": db.n_tokens, "d_mean": d,
                             "d_ic_inf": float(np.percentile(draws, 2.5)), "d_ic_sup": float(np.percentile(draws, 97.5)),
                             "d_ventanas_independientes": indep, "d_sblgnt_consigo_misma_ventanas_independientes": mismo,
                             "d_nucleo_min": float(core_d.min()), "d_nucleo_mediana": float(np.median(core_d)),
                             "pct_entre_cartas_nucleo": percentile_of(d, core_d),
                             "menor_que_toda_distancia_del_nucleo": bool(d < core_d.min()), "nota": nota})
            filas[metric].extend(rows)
            for ed in sorted({r["edicion"] for r in rows}):
                ds = np.array([r["d_mean"] for r in rows if r["edicion"] == ed])
                resumen.append({"edicion": ed, "metrica": metric, "mascara": mask, "n_cartas": len(ds),
                                "ruido_max": float(ds.max()), "ruido_mediana": float(np.median(ds)),
                                "d_nucleo_min": float(core_d.min()), "d_nucleo_mediana": float(np.median(core_d)),
                                "ruido_max_menor_que_d_nucleo_min": bool(ds.max() < core_d.min())})
            print(f"  {metric:6s} {mask:32s} núcleo mín {core_d.min():.4f} mediana {np.median(core_d):.4f} · "
                  + " · ".join(f"{ed} máx {max(r['d_mean'] for r in rows if r['edicion'] == ed):.4f}"
                               for ed in sorted({r['edicion'] for r in rows})))
    for metric in METRICAS:
        _write_csv(os.path.join(run_dir, f"ruido_edicion_{metric}.csv"), filas[metric])
    _write_csv(os.path.join(run_dir, "ruido_edicion_resumen.csv"), resumen)
    return 0


if __name__ == "__main__":
    sys.exit(main())

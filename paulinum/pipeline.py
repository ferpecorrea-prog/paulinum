# -*- coding: utf-8 -*-
"""
pipeline.py — rejilla de especificaciones, etapas reanudables, ruido de edición, contribuciones de
rasgos, resumen por carta.

Etapas de `run` (todas reanudables: una etapa cuyo archivo de salida existe no se repite):
  specs        puntuaciones GI de todos los problemas en cada especificación → results/<run>/specs/NNN.json
  calibration  calibration_by_spec.csv, gi_results_all_specs.csv, summary_by_letter.csv,
               lr_secundaria_por_spec.csv, lr_secundaria_por_carta.csv, calibracion_secundaria_cristiana.csv
  variables    permanova_pauline_windows.csv, dbrda_partition_pauline_windows.{csv,txt}
  ledger       distance_matrix_{metric}.npy, distance_matrix_ids.csv, pair_distances_{metric}.csv,
               double_standard_ledger_{metric}.csv
  rolling      rolling_scores.csv
  extras       edition_noise_pairs.csv, feature_contributions.csv, descriptives.csv, tabla_resumen_13_cartas.csv
Cada orden ejecutada se anota en results/<run>/bitacora.md con hora y duración.
"""
from __future__ import annotations

import csv
import datetime as _dt
import itertools
import json
import math
import os
import time

import numpy as np
import yaml

from . import __version__
from .corpus import Document, load_corpus, mask_vector
from .features import FeatureSpace, PersonFilter, learn_closed_class, load_lexicon, descriptives, relative
from .sources import CORE_SETS, TARGETS, SISTERS
from .variables import (DistanceMatrixBuilder, fixed_windows, permanova, dbrda_partition, intra_author_pairs,
                        same_standard_ledger)
from .verify import Spec, build_problems, GIEngine, calibrate, attach_lr, verbal
from .rolling import rolling_scores

RESULTS_DIR = os.environ.get("PAULINUM_RESULTS", "results")
METADATA_DIR = os.environ.get("PAULINUM_METADATA", "metadata")
LETTERS_13 = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit"]


# ---------------------------------------------------------------------------------------------
# Configuración y rejilla
# ---------------------------------------------------------------------------------------------
def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg.setdefault("parametros", {})
    cfg["_path"] = path
    return cfg


def expand_grid(cfg: dict) -> list[Spec]:
    g = cfg["rejilla"]
    p = cfg["parametros"]
    specs = []
    combos = itertools.product(g.get("diacriticos", ["dia"]), g["rasgos"], g["distancias"], g.get("ventanas", [500]),
                               g.get("mascaras", ["none"]), g.get("nucleos", ["seven"]), g.get("ediciones", ["sblgnt"]))
    for i, (dia, feat, metric, win, mask, core, ed) in enumerate(combos):
        specs.append(Spec(features=feat, metric=metric, window=win, mask=mask, nodia=(dia == "nodia"), core=core,
                          edition=ed, iters=int(p.get("iters", 100)), feature_frac=float(p.get("fraccion_rasgos", 0.5)),
                          n_impostors=int(p.get("impostores", 30)), seed=int(p.get("semilla", 20260908)) + i, index=i))
    return specs


class Bitacora:
    def __init__(self, run_dir: str):
        self.path = os.path.join(run_dir, "bitacora.md")
        os.makedirs(run_dir, exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(f"# Bitácora de {os.path.basename(run_dir)}\n\n| inicio (UTC) | orden / etapa | duración | nota |\n|---|---|---|---|\n")

    def log(self, etapa: str, t0: float, nota: str = "") -> None:
        dur = time.time() - t0
        ini = _dt.datetime.utcfromtimestamp(t0).strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"| {ini} | {etapa} | {dur:,.1f} s | {nota} |\n")


def _write_csv(path: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("")
        return
    fieldnames = fieldnames or list({k: None for r in rows for k in r}.keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if isinstance(v, float) and math.isnan(v) else v) for k, v in r.items()})


# ---------------------------------------------------------------------------------------------
# Contexto compartido: corpus por edición, filtros, lexicón
# ---------------------------------------------------------------------------------------------
class Context:
    def __init__(self, cfg: dict, data_dir: str = "data"):
        self.cfg = cfg
        self.data_dir = data_dir
        self._corpora: dict[str, list[Document]] = {}
        self._pf: dict[str, PersonFilter] = {}
        self._closed: dict[str, set] = {}
        self.lexicon = load_lexicon(os.path.join(data_dir, "cache", "lexicon_uniforme.tsv"))
        self.min_tokens = int(cfg.get("corpus", {}).get("min_tokens", 100))

    def corpus(self, edition: str = "sblgnt") -> list[Document]:
        if edition not in self._corpora:
            docs = load_corpus(edition, self.data_dir)
            self._corpora[edition] = docs
            self._pf[edition] = PersonFilter(docs)
            self._closed[edition] = learn_closed_class(docs)
        return self._corpora[edition]

    def feature_space(self, spec: Spec) -> FeatureSpace:
        docs = self.corpus(spec.edition)
        return FeatureSpace(spec.features, docs, mask=spec.mask, nodia=spec.nodia, person_filter=self._pf[spec.edition],
                            closed_set=self._closed[spec.edition], lexicon=self.lexicon)


# ---------------------------------------------------------------------------------------------
# Etapa specs
# ---------------------------------------------------------------------------------------------
def run_spec(ctx: Context, spec: Spec, out_path: str, log=print) -> dict:
    t0 = time.time()
    docs = ctx.corpus(spec.edition)
    p = ctx.cfg["parametros"]
    fs = ctx.feature_space(spec)
    engine = GIEngine(docs, spec, fs, min_tokens=ctx.min_tokens)
    problems = build_problems(docs, core_name=spec.core, max_pos_per_author=int(p.get("max_positivos_por_autor", 6)),
                              n_neg_pairs=int(p.get("n_pares_negativos", 150)), seed=int(p.get("semilla", 1)),
                              min_tokens=ctx.min_tokens)
    rng = np.random.default_rng(spec.seed)
    results = []
    for pr in problems:
        r = engine.score(pr, rng, return_detail=(pr.kind in ("target", "core_loo")))
        results.append({"pid": pr.pid, "kind": pr.kind, "target": pr.target, "candidates": "|".join(pr.candidates),
                        "label": pr.label, "author": pr.author, "cand_author": pr.cand_author,
                        "tradition": pr.tradition, **r})
    # carta hermana como candidata (se informa aparte, no se suma): Ef+Col, 2Tes+1Tes
    sister_rows = []
    for t in TARGETS:
        if t in SISTERS and any(x["target"] == t for x in results):
            from .verify import Problem
            core = [c for c in CORE_SETS[spec.core] if c in engine.by_id]
            pr = Problem(f"target_sister:{t}", "target_sister", t, core + [s for s in SISTERS[t] if s not in core],
                         exclude=sorted({d.id for d in docs if d.author in ("Pablo", "Pablo?")}), label=None,
                         author="Pablo?", cand_author="Pablo+hermana", tradition="cristiano")
            r = engine.score(pr, rng)
            sister_rows.append({"pid": pr.pid, "kind": pr.kind, "target": t, "candidates": "|".join(pr.candidates),
                                "label": None, "author": "Pablo?", "cand_author": "Pablo+hermana",
                                "tradition": "cristiano", **r})
    results.extend(sister_rows)
    cal = calibrate(results, auc_min=float(p.get("auc_minima", 0.80)))
    attach_lr(results)
    attach_lr(results, subset_neg=lambda r: r.get("tradition") == "cristiano", key="log10lr_cristiana")
    attach_lr(results, subset_neg=lambda r: r.get("tradition") in ("cristiano", "judeo-helenistico"), key="log10lr_cj")
    out = {"spec": spec.to_dict(), "label": spec.label, "n_features": len(fs.vocab), "vocab_head": fs.vocab[:50],
           "n_docs": len(docs), "calibration": cal, "results": results, "seconds": round(time.time() - t0, 1),
           "version": __version__}
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    log(f"  spec {spec.index:03d} {spec.label}: AUC={cal['auc']:.3f} c@1={cal['c_at_1']:.3f} "
        f"({len(results)} problemas, {out['seconds']} s)")
    return out


def stage_specs(ctx: Context, run_dir: str, log=print) -> list[dict]:
    specs = expand_grid(ctx.cfg)
    outs = []
    for spec in specs:
        path = os.path.join(run_dir, "specs", f"{spec.index:03d}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                outs.append(json.load(f))
            continue
        outs.append(run_spec(ctx, spec, path, log))
    return outs


# ---------------------------------------------------------------------------------------------
# Etapa calibration: tablas transversales
# ---------------------------------------------------------------------------------------------
def _q(v, q):
    return float(np.percentile(v, q)) if len(v) else float("nan")


def stage_calibration(run_dir: str, outs: list[dict], auc_min: float = 0.80) -> None:
    cal_rows, all_rows, lr_spec_rows, sec_rows = [], [], [], []
    for o in outs:
        s = o["spec"]
        c = o["calibration"]
        base = {"spec_index": s["index"], "label": o["label"], "dia": "nodia" if s["nodia"] else "dia",
                "features": s["features"], "metric": s["metric"], "window": s["window"] or "all",
                "mask": s["mask"], "core": s["core"], "edition": s["edition"], "iters": s["iters"]}
        cal_rows.append({**base, **{k: c[k] for k in ("n_pos", "n_neg", "auc", "c_at_1", "thr_low", "thr_high",
                                                       "fpr_at_0.5", "fnr_at_0.5", "valid")}})
        res = o["results"]
        for r in res:
            all_rows.append({**base, **r})
        # calibración secundaria (negativos cristianos): AUC y FPR
        pos = np.array([r["score"] for r in res if r["label"] == 1 and not math.isnan(r["score"])])
        negc = np.array([r["score"] for r in res if r["label"] == 0 and r.get("tradition") == "cristiano"
                         and not math.isnan(r["score"])])
        posc = np.array([r["score"] for r in res if r["label"] == 1 and r.get("tradition") == "cristiano"
                         and not math.isnan(r["score"])])
        from .verify import auc as _auc
        sec_rows.append({**base, "n_neg_cristianos": len(negc), "auc_cristiana": _auc(pos, negc),
                         "auc_cristiana_pos_cristianos": _auc(posc, negc),
                         "fpr_cristiana_0.5": float((negc >= 0.5).mean()) if len(negc) else float("nan")})
        for r in res:
            if r["kind"] in ("target", "core_loo"):
                lr_spec_rows.append({**base, "target": r["target"], "kind": r["kind"], "score": r["score"],
                                     "log10lr": r.get("log10lr"), "log10lr_cristiana": r.get("log10lr_cristiana"),
                                     "log10lr_cj": r.get("log10lr_cj"), "valid": c["valid"]})
    _write_csv(os.path.join(run_dir, "calibration_by_spec.csv"), cal_rows)
    _write_csv(os.path.join(run_dir, "gi_results_all_specs.csv"), all_rows)
    _write_csv(os.path.join(run_dir, "calibracion_secundaria_cristiana.csv"), sec_rows)
    _write_csv(os.path.join(run_dir, "lr_secundaria_por_spec.csv"), lr_spec_rows)
    # resumen por carta (solo especificaciones válidas)
    summary, lr_letter = [], []
    for L in LETTERS_13:
        rows = [r for r in lr_spec_rows if r["target"] == L and r["valid"]]
        if not rows:
            continue
        sc = np.array([r["score"] for r in rows])
        lr = np.array([r["log10lr"] for r in rows if r["log10lr"] is not None and not math.isnan(r["log10lr"])])
        lrc = np.array([r["log10lr_cristiana"] for r in rows if r["log10lr_cristiana"] is not None and not math.isnan(r["log10lr_cristiana"])])
        lrcj = np.array([r["log10lr_cj"] for r in rows if r["log10lr_cj"] is not None and not math.isnan(r["log10lr_cj"])])
        summary.append({"id": L, "kind": rows[0]["kind"], "n_specs": len(rows), "score_median": float(np.median(sc)),
                        "score_q1": _q(sc, 25), "score_q3": _q(sc, 75), "score_min": float(sc.min()),
                        "score_max": float(sc.max()), "frac_specs_ge_0_5": float((sc >= 0.5).mean()),
                        "log10lr_median": float(np.median(lr)) if len(lr) else float("nan"),
                        "log10lr_q1": _q(lr, 25), "log10lr_q3": _q(lr, 75)})
        lr_letter.append({"target": L, "kind": rows[0]["kind"], "n_specs": len(rows),
                          "log10lr_principal_mediana": float(np.median(lr)) if len(lr) else float("nan"),
                          "log10lr_cristiana_mediana": float(np.median(lrc)) if len(lrc) else float("nan"),
                          "log10lr_cristiana_q1": _q(lrc, 25), "log10lr_cristiana_q3": _q(lrc, 75),
                          "log10lr_cristiana_min": float(lrc.min()) if len(lrc) else float("nan"),
                          "log10lr_cristiana_max": float(lrc.max()) if len(lrc) else float("nan"),
                          "verbal_cristiana_mediana": verbal(float(np.median(lrc))) if len(lrc) else "",
                          "log10lr_cj_mediana": float(np.median(lrcj)) if len(lrcj) else float("nan")})
    _write_csv(os.path.join(run_dir, "summary_by_letter.csv"), summary)
    _write_csv(os.path.join(run_dir, "lr_secundaria_por_carta.csv"), lr_letter)
    # puntuación de las dianas por familia de rasgos, distancia y máscara
    fam = {}
    for r in all_rows:
        if r["kind"] == "target":
            key = (r["features"], r["metric"], r["mask"], r["window"], r["dia"], r["core"], r["edition"])
            fam.setdefault(key, {})[r["target"]] = r["score"]
    fam_rows = [{"features": k[0], "metric": k[1], "mask": k[2], "window": k[3], "dia": k[4], "core": k[5],
                 "edition": k[6], **{t: v.get(t) for t in TARGETS}} for k, v in sorted(fam.items())]
    _write_csv(os.path.join(run_dir, "gi_targets_por_especificacion.csv"), fam_rows)


# ---------------------------------------------------------------------------------------------
# Etapa ledger (mismo rasero) y matrices de distancia
# ---------------------------------------------------------------------------------------------
def stage_ledger(ctx: Context, run_dir: str, log=print) -> None:
    mr = ctx.cfg.get("mismo_rasero", {})
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    core_name = ctx.cfg["rejilla"].get("nucleos", ["seven"])[0]
    core = [c for c in CORE_SETS[core_name] if any(d.id == c for d in docs)]
    letters = [L for L in LETTERS_13 if any(d.id == L for d in docs)]
    spec = Spec(features=mr.get("rasgos", "mfw:300"), metric="minmax", window=mr.get("ventana", 500), edition=edition)
    fs = ctx.feature_space(spec)
    pairs = intra_author_pairs(docs, cap_pairs_per_author=int(mr.get("tope_pares_por_autor", 120)))
    for metric in mr.get("distancias", ["minmax", "delta"]):
        path = os.path.join(run_dir, f"double_standard_ledger_{metric}.csv")
        if os.path.exists(path):
            continue
        t0 = time.time()
        b = DistanceMatrixBuilder(docs, fs, metric, window=mr.get("ventana", 500), draws=int(mr.get("sorteos", 20)),
                                  min_tokens=ctx.min_tokens)
        led = same_standard_ledger(b, letters, core, pairs, exclude_sisters=SISTERS)
        _write_csv(os.path.join(run_dir, f"pair_distances_{metric}.csv"), led["envelope"])
        rows = [{"id": L, "kind": "core" if L in core else "target", **v} for L, v in led["letters"].items()]
        for r in rows:
            r.update({f"env_{k}": v for k, v in led["envelope_stats"].items()})
        _write_csv(path, rows)
        # matriz de distancias entre las 13 cartas y los documentos de control (para bootstrap y lecturas)
        ids = letters + [d.id for d in docs if d.status == "genuine" and d.author not in ("Pablo", "Pablo?")]
        M = b.matrix(ids)
        np.save(os.path.join(run_dir, f"distance_matrix_{metric}.npy"), M)
        with open(os.path.join(run_dir, "distance_matrix_ids.csv"), "w", encoding="utf-8") as f:
            f.write("index,id\n" + "\n".join(f"{i},{x}" for i, x in enumerate(ids)) + "\n")
        log(f"  ledger {metric}: {len(pairs)} pares intra-autor; {time.time() - t0:.0f} s")


# ---------------------------------------------------------------------------------------------
# Etapa variables: PERMANOVA y dbRDA dentro del corpus paulino (ventanas de 400)
# ---------------------------------------------------------------------------------------------
def load_letter_variables(path: str | None = None) -> dict[str, dict]:
    path = path or os.path.join(METADATA_DIR, "letter_variables.csv")
    out = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                out[row["id"]] = row
    return out


def stage_variables(ctx: Context, run_dir: str, log=print) -> None:
    path = os.path.join(run_dir, "permanova_pauline_windows.csv")
    if os.path.exists(path):
        return
    v = ctx.cfg.get("variables", {})
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    letters = [L for L in LETTERS_13 if any(d.id == L for d in docs)]
    spec = Spec(features=v.get("rasgos", "mfw:200"), metric=v.get("distancia", "delta"), window=None, edition=edition)
    fs = ctx.feature_space(spec)
    by_id = {d.id: d for d in docs}
    wins = []
    for L in letters:
        wins.extend(fixed_windows(by_id[L], fs, window=int(v.get("ventana", 400))))
    b = DistanceMatrixBuilder(docs, fs, spec.metric, window=None, draws=1, min_tokens=ctx.min_tokens)
    D = b.window_matrix(wins)
    lv = load_letter_variables()
    variables = {k: [] for k in ("addressee_type", "captivity", "polemic_level", "n_cosenders", "liturgical_register",
                                 "church_order", "letter", "group")}
    for d, s, e in wins:
        row = lv.get(d, {})
        for k in variables:
            if k == "letter":
                variables[k].append(d)
            else:
                variables[k].append(row.get(k, "NA"))
    rows = []
    for k, g in variables.items():
        r = permanova(D, g, permutations=int(v.get("permutaciones", 499)))
        rows.append({"variable": k, **r})
    _write_csv(path, rows)
    part = dbrda_partition(D, {k: g for k, g in variables.items() if k not in ("letter",)})
    _write_csv(os.path.join(run_dir, "dbrda_partition_pauline_windows.csv"),
               [{"variable": k, "R2": val} for k, val in part.items()])
    with open(os.path.join(run_dir, "dbrda_partition_pauline_windows.txt"), "w", encoding="utf-8") as f:
        f.write("Partición de varianza (dbRDA sobre coordenadas principales; ventanas de %d palabras; %d ventanas)\n"
                % (int(v.get("ventana", 400)), len(wins)))
        for k, val in part.items():
            f.write(f"  {k:22s} R2 = {val:.4f}\n")
    log(f"  variables: {len(wins)} ventanas; PERMANOVA de {len(rows)} variables")


# ---------------------------------------------------------------------------------------------
# Etapa rolling
# ---------------------------------------------------------------------------------------------
def stage_rolling(ctx: Context, run_dir: str, log=print) -> None:
    path = os.path.join(run_dir, "rolling_scores.csv")
    if os.path.exists(path):
        return
    ro = ctx.cfg.get("rolling", {})
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    core_name = ctx.cfg["rejilla"].get("nucleos", ["seven"])[0]
    core = [c for c in CORE_SETS[core_name] if any(d.id == c for d in docs)]
    letters = [L for L in LETTERS_13 if any(d.id == L for d in docs)]
    spec = Spec(features=ro.get("rasgos", "mfw:300"), metric=ro.get("distancia", "minmax"), window=500, edition=edition,
                iters=int(ro.get("iters", 60)))
    fs = ctx.feature_space(spec)
    engine = GIEngine(docs, spec, fs, min_tokens=ctx.min_tokens)
    rows = rolling_scores(docs, engine, letters, core, window=int(ro.get("ventana", 400)), step=int(ro.get("paso", 100)),
                          iters=int(ro.get("iters", 60)))
    _write_csv(path, rows)
    log(f"  rolling: {len(rows)} ventanas")


# ---------------------------------------------------------------------------------------------
# Etapa extras: ruido de edición, contribuciones de rasgos, descriptivos, tabla resumen
# ---------------------------------------------------------------------------------------------
def stage_extras(ctx: Context, run_dir: str, log=print) -> None:
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    by_id = {d.id: d for d in docs}
    core_name = ctx.cfg["rejilla"].get("nucleos", ["seven"])[0]
    core = [c for c in CORE_SETS[core_name] if c in by_id]
    # descriptivos
    _write_csv(os.path.join(run_dir, "descriptives.csv"), [descriptives(d) for d in docs])
    # ruido de edición: duplicados frente a su original (min-max, mfw:300, ventanas de 500, 20 sorteos)
    spec = Spec(features="mfw:300", metric="minmax", window=500, edition=edition)
    fs = ctx.feature_space(spec)
    b = DistanceMatrixBuilder(docs, fs, "minmax", window=500, draws=20, min_tokens=ctx.min_tokens)
    noise = []
    for d in docs:
        if d.status != "duplicate":
            continue
        # el original: mismo autor, misma obra (por nombre de parte) y estado no duplicado
        cands = [x for x in docs if x.author == d.author and x.status != "duplicate" and x.n_tokens > 0]
        if not cands:
            continue
        # emparejar por posición (cartas de Ignacio en orden) o por único original
        match = None
        if len(cands) == 1:
            match = cands[0]
        else:
            # cartas de Ignacio: emparejar por orden de aparición
            dups = [x for x in docs if x.status == "duplicate" and x.author == d.author]
            i = dups.index(d)
            if i < len(cands):
                match = cands[i]
        if match:
            noise.append({"duplicate": d.id, "original": match.id, "author": d.author,
                          "d_minmax_mfw300": b.pair_distance(d.id, match.id)})
    _write_csv(os.path.join(run_dir, "edition_noise_pairs.csv"), noise)
    # contribuciones de rasgos: z de cada forma en cada carta frente a la dispersión interna del núcleo
    fs2 = ctx.feature_space(Spec(features="mfw:300", metric="delta", window=None, edition=edition))
    core_rel = np.array([relative(fs2.doc_counts(by_id[c])) for c in core]) * 1000.0
    mu, sd = core_rel.mean(axis=0), core_rel.std(axis=0, ddof=1)
    sd[sd < 1e-9] = 1e-9
    contrib = []
    for L in LETTERS_13:
        if L not in by_id:
            continue
        rel = relative(fs2.doc_counts(by_id[L])) * 1000.0
        z = (rel - mu) / sd
        order = np.argsort(-np.abs(z))[:15]
        for rank, j in enumerate(order, 1):
            contrib.append({"id": L, "rank": rank, "feature": fs2.vocab[j], "permil_letter": round(float(rel[j]), 2),
                            "permil_core_mean": round(float(mu[j]), 2), "z_vs_core": round(float(z[j]), 2),
                            "direction": "exceso" if z[j] > 0 else "defecto"})
    _write_csv(os.path.join(run_dir, "feature_contributions.csv"), contrib)
    # tabla resumen de las 13 cartas
    summ = {r["id"]: r for r in _read_csv(os.path.join(run_dir, "summary_by_letter.csv"))}
    lrl = {r["target"]: r for r in _read_csv(os.path.join(run_dir, "lr_secundaria_por_carta.csv"))}
    led_mm = {r["id"]: r for r in _read_csv(os.path.join(run_dir, "double_standard_ledger_minmax.csv"))}
    led_d = {r["id"]: r for r in _read_csv(os.path.join(run_dir, "double_standard_ledger_delta.csv"))}
    rows = []
    for L in LETTERS_13:
        if L not in by_id:
            continue
        s, l, m, dd = summ.get(L, {}), lrl.get(L, {}), led_mm.get(L, {}), led_d.get(L, {})
        rows.append({"carta": L, "tokens": by_id[L].n_tokens, "kind": "core" if L in core else "target",
                     "gi_mediana": s.get("score_median"), "gi_q1": s.get("score_q1"), "gi_q3": s.get("score_q3"),
                     "log10lr_mediana": s.get("log10lr_median"), "log10lr_cristiana": l.get("log10lr_cristiana_mediana"),
                     "escala_verbal_cristiana": l.get("verbal_cristiana_mediana"),
                     "d_minmax": m.get("d_mean"), "pct_minmax": m.get("percentile"), "pct_delta": dd.get("percentile")})
    _write_csv(os.path.join(run_dir, "tabla_resumen_13_cartas.csv"), rows)
    log(f"  extras: {len(noise)} pares de ruido de edición, {len(contrib)} contribuciones de rasgos")


def _read_csv(path: str) -> list[dict]:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------------------------
# Orquestación
# ---------------------------------------------------------------------------------------------
STAGES = ["specs", "calibration", "ledger", "variables", "rolling", "extras"]


def run_campaign(config_path: str, run_name: str | None = None, stages: list[str] | None = None,
                 data_dir: str = "data", results_dir: str = RESULTS_DIR, log=print) -> str:
    cfg = load_config(config_path)
    run_name = run_name or cfg.get("nombre", "campana")
    run_dir = os.path.join(results_dir, run_name)
    os.makedirs(os.path.join(run_dir, "specs"), exist_ok=True)
    with open(os.path.join(run_dir, "config_used.json"), "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in cfg.items() if not k.startswith("_")}, f, ensure_ascii=False, indent=1)
    bit = Bitacora(run_dir)
    logf = open(os.path.join(run_dir, "run.log"), "a", encoding="utf-8")

    def _log(msg):
        stamp = _dt.datetime.utcnow().strftime("%H:%M:%S")
        logf.write(f"[{stamp}] {msg}\n")
        logf.flush()
        log(msg)

    ctx = Context(cfg, data_dir)
    stages = stages or STAGES
    _log(f"run {run_name} (paulinum {__version__}) · etapas: {', '.join(stages)}")
    outs = None
    for st in stages:
        t0 = time.time()
        if st == "specs":
            outs = stage_specs(ctx, run_dir, _log)
        elif st == "calibration":
            if outs is None:
                outs = stage_specs(ctx, run_dir, _log)
            stage_calibration(run_dir, outs, float(cfg["parametros"].get("auc_minima", 0.80)))
        elif st == "ledger":
            stage_ledger(ctx, run_dir, _log)
        elif st == "variables":
            stage_variables(ctx, run_dir, _log)
        elif st == "rolling":
            stage_rolling(ctx, run_dir, _log)
        elif st == "extras":
            stage_extras(ctx, run_dir, _log)
        bit.log(f"python -m paulinum run --config {config_path} --run {run_name} --stage {st}", t0)
        _log(f"etapa {st}: {time.time() - t0:.0f} s")
    logf.close()
    return run_dir

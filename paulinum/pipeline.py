# -*- coding: utf-8 -*-
"""
pipeline.py — rejilla de especificaciones, etapas reanudables, ruido de edición, contribuciones de
rasgos, resumen por carta.

Etapas de `run` (todas reanudables: una etapa cuyo archivo de salida existe no se repite):
  specs        puntuaciones de todos los problemas en cada especificación y familia
               → results/<run>/specs/<familia>_NNN.json (con reanudación por problema en <...>.parcial.jsonl)
  calibration  calibration_by_spec.csv (general, epistolar y cristiana), gi_results_all_specs.csv,
               summary_by_letter.csv (por familia), lr_secundaria_por_spec.csv, lr_secundaria_por_carta.csv,
               calibracion_secundaria_cristiana.csv, concordancia_familias.csv
  ledger       distance_matrix_{metric}.npy, distance_matrix_ids.csv, pair_distances_{metric}.csv (E),
               pair_distances_inter_{metric}.csv (B), pair_distances_genero_{metric}.csv (G),
               double_standard_ledger_{metric}.csv (pct_E, pct_B, pct_G), nearest_author_{metric}.csv
  variables    permanova_pauline_windows.csv, dbrda_partition_pauline_windows.{csv,txt}
  rolling      rolling_scores.csv
  extras       edition_noise_pairs.csv, feature_contributions.csv, descriptives.csv, tabla_resumen_14_cartas.csv
Cada orden ejecutada se anota en results/<run>/bitacora.md con hora y duración.
paulinum 1.0 (PROTOCOLO § 3.3): con `parametros.sin_dianas: true` no se calcula ninguna fila de diana (ni target ni
core_loo): es el modo de la fase de implementación y de las pruebas.
"""
from __future__ import annotations

import csv
import datetime as _dt
import itertools
import json
import math
import multiprocessing as _mp
import os
import time

import numpy as np
import yaml

from . import __version__
from .corpus import Document, load_corpus, mask_vector
from .features import FeatureSpace, PersonFilter, learn_closed_class, load_lexicon, descriptives, relative
from .sources import CORE_SETS, TARGETS, SISTERS
from .variables import (DistanceMatrixBuilder, fixed_windows, permanova, dbrda_partition, intra_author_pairs,
                        inter_author_pairs, genre_pairs, same_standard_ledger, nearest_authors)
from .verify import Spec, build_problems, GIEngine, make_engine, calibrate, attach_lr, verbal
from .rolling import rolling_scores

RESULTS_DIR = os.environ.get("PAULINUM_RESULTS", "results")
METADATA_DIR = os.environ.get("PAULINUM_METADATA", "metadata")
LETTERS_13 = ["Rom", "1Cor", "2Cor", "Gal", "Flp", "1Tes", "Flm", "Ef", "Col", "2Tes", "1Tim", "2Tim", "Tit"]
LETTERS_14 = LETTERS_13 + ["Heb"]     # paulinum 1.0: Hebreos con el mismo rasero (D-002)
FAMILIES = ["impostores", "ncd", "dirichlet"]


# ---------------------------------------------------------------------------------------------
# Configuración y rejilla
# ---------------------------------------------------------------------------------------------
def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg.setdefault("parametros", {})
    cfg["_path"] = path
    return cfg


def campaign_sets(cfg: dict, docs: list[Document], core_name: str | None = None) -> tuple[list[str], list[str], list[str]]:
    """(núcleo, dianas, cartas evaluadas) de la campaña. Con `parametros.nucleo_ids` y `parametros.dianas_ids` (prueba
    de veredicto con autores de control) sustituyen al núcleo paulino y a las catorce cartas."""
    p = cfg.get("parametros", {})
    by_id = {d.id for d in docs}
    if p.get("nucleo_ids"):
        core = [c for c in p["nucleo_ids"] if c in by_id]
        targets = [t for t in p.get("dianas_ids", []) if t in by_id]
    else:
        core_name = core_name or cfg["rejilla"].get("nucleos", ["seven"])[0]
        core = [c for c in CORE_SETS[core_name] if c in by_id]
        targets = [t for t in TARGETS if t in by_id]
    letters = [] if p.get("sin_dianas", False) else core + [t for t in targets if t not in core]
    return core, targets, letters


def active_families(cfg: dict) -> list[str]:
    fam = cfg.get("familias")
    if not fam:
        return ["impostores"]
    return [f for f in FAMILIES if f in fam and fam[f].get("activa", True)]


def expand_grid(cfg: dict, family: str = "impostores") -> list[Spec]:
    """Rejilla de una familia. impostores: rasgos × distancias × ...; ncd: sin rasgos ni distancia (solo ventana,
    máscara, núcleo y edición); dirichlet: sus rasgos (familias.dirichlet.rasgos) × máscara × ventana × núcleo × edición.
    La semilla es semilla + índice + 1000 × posición de la familia, para que las familias sorteen distinto."""
    g = cfg["rejilla"]
    p = cfg["parametros"]
    fcfg = (cfg.get("familias") or {}).get(family, {})
    base = int(p.get("semilla", 20260908)) + 1000 * FAMILIES.index(family)
    if family == "impostores":
        feats, metrics = g["rasgos"], g["distancias"]
    elif family == "ncd":
        feats, metrics = ["ncd"], ["ncd"]
    else:
        feats, metrics = list(fcfg.get("rasgos", ["mfw:300", "closed:150"])), ["dirmult"]
    specs = []
    combos = itertools.product(g.get("diacriticos", ["dia"]), feats, metrics, g.get("ventanas", [500]),
                               g.get("mascaras", ["none"]), g.get("nucleos", ["seven"]), g.get("ediciones", ["sblgnt"]))
    for i, (dia, feat, metric, win, mask, core, ed) in enumerate(combos):
        if family == "ncd" and dia == "nodia":
            continue   # NCD siempre trabaja sin diacríticos: una sola variante
        specs.append(Spec(features=feat, metric=metric, window=win, mask=mask, nodia=(dia == "nodia"), core=core,
                          edition=ed, iters=int(fcfg.get("iters", p.get("iters", 100))),
                          feature_frac=float(p.get("fraccion_rasgos", 0.5)), n_impostors=int(p.get("impostores", 30)),
                          seed=base + i, index=i, family=family))
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
            # capa de anotación uniforme (scripts/anotacion_uniforme.py), si existe y superó el umbral (PROTOCOLO § 5.3)
            # (la capa publicada por el laboratorio de Actions está comprimida en results/anotacion/)
            candidatos = [os.path.join(self.data_dir, "cache", f"pos_uniforme_{edition}.jsonl"),
                          os.path.join("results", "anotacion", f"pos_uniforme_{edition}.jsonl.gz")]
            pu = next((c for c in candidatos if os.path.exists(c)), None)
            if pu:
                import gzip
                tags = {}
                opener = gzip.open if pu.endswith(".gz") else open
                with opener(pu, "rt", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            r = json.loads(line)
                            tags[r["id"]] = r["pos_uniforme"]
                for d in docs:
                    d.pos_uniforme = tags.get(d.id, [])
            self._corpora[edition] = docs
            self._pf[edition] = PersonFilter(docs)
            self._closed[edition] = learn_closed_class(docs)
        return self._corpora[edition]

    def feature_space(self, spec: Spec) -> FeatureSpace:
        docs = self.corpus(spec.edition)
        feats = "mfw:300" if spec.features == "ncd" else spec.features   # NCD: solo necesita la secuencia y el filtro
        return FeatureSpace(feats, docs, mask=spec.mask, nodia=spec.nodia, person_filter=self._pf[spec.edition],
                            closed_set=self._closed[spec.edition], lexicon=self.lexicon)


# ---------------------------------------------------------------------------------------------
# Etapa specs
# ---------------------------------------------------------------------------------------------
_ENGINE = None   # motor compartido por los procesos hijos (fork)


def _score_one(args):
    pid, seed, detail = args
    pr = _ENGINE._problems[pid]
    rng = np.random.default_rng(seed)
    r = _ENGINE.score(pr, rng, return_detail=detail)
    return {"pid": pr.pid, "kind": pr.kind, "target": pr.target, "candidates": "|".join(pr.candidates),
            "label": pr.label, "author": pr.author, "cand_author": pr.cand_author, "tradition": pr.tradition,
            "epistolar": bool(pr.epistolar), **r}


def _is_epist(r: dict) -> bool:
    return bool(r.get("epistolar"))


def run_spec(ctx: Context, spec: Spec, out_path: str, log=print, workers: int = 1) -> dict:
    """Puntúa todos los problemas de una especificación. Reanudable: los resultados parciales se van escribiendo en
    <out_path>.parcial.jsonl (uno por problema, con su semilla propia = semilla de la especificación + índice del
    problema), y al terminar se escribe el JSON completo y se borra el parcial. Con workers > 1 los problemas se
    reparten entre procesos (fork) con el mismo motor."""
    global _ENGINE
    t0 = time.time()
    docs = ctx.corpus(spec.edition)
    p = ctx.cfg["parametros"]
    fs = ctx.feature_space(spec)
    fam_cfg = (ctx.cfg.get("familias") or {}).get(spec.family, {})
    kw = {"preset": int(fam_cfg.get("preset", 6))} if spec.family == "ncd" else {}
    engine = make_engine(docs, spec, fs, min_tokens=ctx.min_tokens, **kw)
    custom = bool(p.get("nucleo_ids"))
    problems = build_problems(docs, core_name=spec.core, max_pos_per_author=int(p.get("max_positivos_por_autor", 6)),
                              n_neg_pairs=int(p.get("n_pares_negativos", 150)), seed=int(p.get("semilla", 1)),
                              min_tokens=ctx.min_tokens, sin_dianas=bool(p.get("sin_dianas", False)),
                              core_ids=p.get("nucleo_ids") if custom else None,
                              target_ids=p.get("dianas_ids") if custom else None)
    # carta hermana como candidata (se informa aparte, no se suma): Ef+Col, 2Tes+1Tes
    if not p.get("sin_dianas", False) and not custom:
        from .verify import Problem
        core = [c for c in CORE_SETS[spec.core] if c in engine.by_id]
        for t in TARGETS:
            if t in SISTERS and any(x.target == t and x.kind == "target" for x in problems):
                problems.append(Problem(f"target_sister:{t}", "target_sister", t, core + [x for x in SISTERS[t] if x not in core],
                                        exclude=sorted({d.id for d in docs if d.author in ("Pablo", "Pablo?")}), label=None,
                                        author="Pablo?", cand_author="Pablo+hermana", tradition="cristiano", epistolar=True))
    engine._problems = {pr.pid: pr for pr in problems}
    _ENGINE = engine
    partial = out_path + ".parcial.jsonl"
    done: dict[str, dict] = {}
    if os.path.exists(partial):
        with open(partial, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    done[r["pid"]] = r
    todo = [(pr.pid, spec.seed * 100003 + i, pr.kind in ("target", "core_loo", "target_sister"))
            for i, pr in enumerate(problems) if pr.pid not in done]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if todo:
        with open(partial, "a", encoding="utf-8") as f:
            if workers > 1:
                with _mp.get_context("fork").Pool(workers) as pool:
                    for r in pool.imap_unordered(_score_one, todo, chunksize=4):
                        done[r["pid"]] = r
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                        f.flush()
            else:
                for a in todo:
                    r = _score_one(a)
                    done[r["pid"]] = r
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                    f.flush()
    results = [done[pr.pid] for pr in problems if pr.pid in done]
    auc_min = float(p.get("auc_minima", 0.80))
    cal = calibrate(results, auc_min=auc_min)
    cal_epist = calibrate(results, auc_min=auc_min, subset=_is_epist)
    cal_crist = calibrate(results, auc_min=auc_min, subset=lambda r: r.get("tradition") == "cristiano")
    attach_lr(results)
    attach_lr(results, subset_pos=_is_epist, subset_neg=_is_epist, key="log10lr_epistolar")
    attach_lr(results, subset_neg=lambda r: r.get("tradition") == "cristiano", key="log10lr_cristiana")
    attach_lr(results, subset_neg=lambda r: r.get("tradition") in ("cristiano", "judeo-helenistico"), key="log10lr_cj")
    out = {"spec": spec.to_dict(), "label": spec.label, "family": spec.family, "n_features": len(fs.vocab),
           "vocab_head": fs.vocab[:50], "n_docs": len(docs), "calibration": cal, "calibration_epistolar": cal_epist,
           "calibration_cristiana": cal_crist, "results": results, "seconds": round(time.time() - t0, 1),
           "version": __version__, "sin_dianas": bool(p.get("sin_dianas", False))}
    if spec.family == "dirichlet" and results:
        out["alpha"] = results[0].get("alpha")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    if os.path.exists(partial):
        os.remove(partial)
    log(f"  spec {spec.family} {spec.index:03d} {spec.label}: AUC={cal['auc']:.3f} (epist. {cal_epist['auc']:.3f}) "
        f"c@1={cal['c_at_1']:.3f} ({len(results)} problemas, {out['seconds']} s)")
    return out


def stage_specs(ctx: Context, run_dir: str, log=print, workers: int = 1, families: list[str] | None = None,
                only: list[int] | None = None) -> list[dict]:
    outs = []
    for family in (families or active_families(ctx.cfg)):
        for spec in expand_grid(ctx.cfg, family):
            if only is not None and spec.index not in only:
                continue
            path = os.path.join(run_dir, "specs", f"{family}_{spec.index:03d}.json")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    outs.append(json.load(f))
                continue
            outs.append(run_spec(ctx, spec, path, log, workers=workers))
    return outs


def load_specs(run_dir: str) -> list[dict]:
    outs = []
    d = os.path.join(run_dir, "specs")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if fn.endswith(".json"):
            with open(os.path.join(d, fn), encoding="utf-8") as f:
                outs.append(json.load(f))
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
        c, ce, cc = o["calibration"], o.get("calibration_epistolar", {}), o.get("calibration_cristiana", {})
        fam = o.get("family", s.get("family", "impostores"))
        base = {"family": fam, "spec_index": s["index"], "label": o["label"], "dia": "nodia" if s["nodia"] else "dia",
                "features": s["features"], "metric": s["metric"], "window": s["window"] or "all",
                "mask": s["mask"], "core": s["core"], "edition": s["edition"], "iters": s["iters"]}
        valid_epist = bool(ce.get("valid", False)) if ce else bool(c["valid"])
        cal_rows.append({**base, **{k: c[k] for k in ("n_pos", "n_neg", "auc", "c_at_1", "thr_low", "thr_high",
                                                       "fpr_at_0.5", "fnr_at_0.5", "valid")},
                         "n_pos_epist": ce.get("n_pos"), "n_neg_epist": ce.get("n_neg"), "auc_epist": ce.get("auc"),
                         "c_at_1_epist": ce.get("c_at_1"), "fpr_epist_0.5": ce.get("fpr_at_0.5"),
                         "fnr_epist_0.5": ce.get("fnr_at_0.5"), "valid_epist": valid_epist,
                         "auc_cristiana": cc.get("auc"), "alpha": o.get("alpha")})
        res = o["results"]
        for r in res:
            all_rows.append({**base, **r})
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
                                     "log10lr": r.get("log10lr"), "log10lr_epistolar": r.get("log10lr_epistolar"),
                                     "log10lr_cristiana": r.get("log10lr_cristiana"), "log10lr_cj": r.get("log10lr_cj"),
                                     "valid": c["valid"], "valid_epist": valid_epist,
                                     "margin_median": r.get("margin_median"), "nearest_impostor": r.get("nearest_impostor")})
    _write_csv(os.path.join(run_dir, "calibration_by_spec.csv"), cal_rows)
    _write_csv(os.path.join(run_dir, "gi_results_all_specs.csv"), all_rows)
    _write_csv(os.path.join(run_dir, "calibracion_secundaria_cristiana.csv"), sec_rows)
    _write_csv(os.path.join(run_dir, "lr_secundaria_por_spec.csv"), lr_spec_rows)
    # aptitud de cada familia (PROTOCOLO § 7.2): mediana de la AUC epistolar ≥ auc_min
    fam_rows = []
    for fam in FAMILIES:
        aucs = [r["auc_epist"] for r in cal_rows if r["family"] == fam and r["auc_epist"] is not None
                and not (isinstance(r["auc_epist"], float) and math.isnan(r["auc_epist"]))]
        if aucs:
            fam_rows.append({"family": fam, "n_specs": len(aucs), "auc_epist_mediana": float(np.median(aucs)),
                             "auc_epist_min": float(min(aucs)), "apta": bool(np.median(aucs) >= auc_min)})
    _write_csv(os.path.join(run_dir, "familias_aptitud.csv"), fam_rows)
    apt = {r["family"] for r in fam_rows if r["apta"]}
    # resumen por carta y familia (solo especificaciones válidas en la calibración epistolar)
    summary, lr_letter = [], []
    letters_seen = list(dict.fromkeys([r["target"] for r in lr_spec_rows]))
    letters_all = [L for L in LETTERS_14 if L in letters_seen] + [L for L in letters_seen if L not in LETTERS_14]
    for fam in FAMILIES:
        for L in letters_all:
            rows = [r for r in lr_spec_rows if r["target"] == L and r["family"] == fam and r["valid_epist"]]
            if not rows:
                continue
            sc = np.array([r["score"] for r in rows])
            def _arr(key):
                return np.array([r[key] for r in rows if r.get(key) is not None and not math.isnan(r[key])])
            lr, lre, lrc, lrcj = _arr("log10lr"), _arr("log10lr_epistolar"), _arr("log10lr_cristiana"), _arr("log10lr_cj")
            summary.append({"family": fam, "apta": fam in apt, "id": L, "kind": rows[0]["kind"], "n_specs": len(rows),
                            "score_median": float(np.median(sc)), "score_q1": _q(sc, 25), "score_q3": _q(sc, 75),
                            "score_min": float(sc.min()), "score_max": float(sc.max()),
                            "frac_specs_ge_0_5": float((sc >= 0.5).mean()),
                            "log10lr_epist_median": float(np.median(lre)) if len(lre) else float("nan"),
                            "log10lr_epist_q1": _q(lre, 25), "log10lr_epist_q3": _q(lre, 75),
                            "log10lr_epist_min": float(lre.min()) if len(lre) else float("nan"),
                            "log10lr_epist_max": float(lre.max()) if len(lre) else float("nan"),
                            "verbal_epist": verbal(float(np.median(lre))) if len(lre) else "",
                            "log10lr_median": float(np.median(lr)) if len(lr) else float("nan"),
                            "log10lr_q1": _q(lr, 25), "log10lr_q3": _q(lr, 75),
                            "log10lr_cristiana_median": float(np.median(lrc)) if len(lrc) else float("nan"),
                            "log10lr_cj_median": float(np.median(lrcj)) if len(lrcj) else float("nan")})
            lr_letter.append({"family": fam, "target": L, "kind": rows[0]["kind"], "n_specs": len(rows),
                              "log10lr_epistolar_mediana": float(np.median(lre)) if len(lre) else float("nan"),
                              "verbal_epistolar": verbal(float(np.median(lre))) if len(lre) else "",
                              "log10lr_principal_mediana": float(np.median(lr)) if len(lr) else float("nan"),
                              "log10lr_cristiana_mediana": float(np.median(lrc)) if len(lrc) else float("nan"),
                              "log10lr_cristiana_q1": _q(lrc, 25), "log10lr_cristiana_q3": _q(lrc, 75),
                              "verbal_cristiana_mediana": verbal(float(np.median(lrc))) if len(lrc) else "",
                              "log10lr_cj_mediana": float(np.median(lrcj)) if len(lrcj) else float("nan")})
    _write_csv(os.path.join(run_dir, "summary_by_letter.csv"), summary)
    _write_csv(os.path.join(run_dir, "lr_secundaria_por_carta.csv"), lr_letter)
    # concordancia entre familias aptas (signo de la LR epistolar mediana por carta)
    conc = []
    for L in letters_all:
        rows = [r for r in summary if r["id"] == L and r["apta"]]
        if not rows:
            continue
        signs = {r["family"]: ("+" if r["log10lr_epist_median"] > 0 else "-") if not math.isnan(r["log10lr_epist_median"]) else "?"
                 for r in rows}
        vals = [v for v in signs.values() if v in "+-"]
        conc.append({"id": L, "kind": rows[0]["kind"], **{f"signo_{f}": signs.get(f, "") for f in FAMILIES},
                     "concordancia": "concordante" if len(set(vals)) <= 1 else "discordante",
                     "mediana_familias_log10lr_epist": float(np.median([r["log10lr_epist_median"] for r in rows
                                                                        if not math.isnan(r["log10lr_epist_median"])]))
                     if vals else float("nan")})
    _write_csv(os.path.join(run_dir, "concordancia_familias.csv"), conc)
    # puntuación de las dianas por familia, rasgos, distancia y máscara
    fam = {}
    for r in all_rows:
        if r["kind"] == "target":
            key = (r["family"], r["features"], r["metric"], r["mask"], r["window"], r["dia"], r["core"], r["edition"])
            fam.setdefault(key, {})[r["target"]] = r["score"]
    tcols = list(dict.fromkeys(t for v in fam.values() for t in v))
    fam_rows2 = [{"family": k[0], "features": k[1], "metric": k[2], "mask": k[3], "window": k[4], "dia": k[5], "core": k[6],
                  "edition": k[7], **{t: v.get(t) for t in tcols}} for k, v in sorted(fam.items())]
    _write_csv(os.path.join(run_dir, "gi_targets_por_especificacion.csv"), fam_rows2)


# ---------------------------------------------------------------------------------------------
# Etapa ledger (mismo rasero) y matrices de distancia
# ---------------------------------------------------------------------------------------------
def stage_ledger(ctx: Context, run_dir: str, log=print) -> None:
    """Envolventes E (intra-autor), B (inter-autor, cartas frente a cartas) y G (saltos de género intra-autor),
    distancia de cada carta al núcleo con sus percentiles, y orden de autores más próximos (PROTOCOLO § 7.3-7.4, § 8.3).
    Con sin_dianas no se calcula nada de las cartas: solo las envolventes."""
    mr = ctx.cfg.get("mismo_rasero", {})
    p = ctx.cfg["parametros"]
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    core, _targets, letters = campaign_sets(ctx.cfg, docs)
    spec = Spec(features=mr.get("rasgos", "mfw:300"), metric="minmax", window=mr.get("ventana", 500), edition=edition)
    fs = ctx.feature_space(spec)
    cap = int(mr.get("tope_pares_por_autor", 120))
    pairs = intra_author_pairs(docs, cap_pairs_per_author=cap)
    pairs_b = inter_author_pairs(docs, cap_pairs_per_author=cap)
    pairs_g = genre_pairs(docs, cap_pairs_per_author=cap)
    for metric in mr.get("distancias", ["minmax", "delta"]):
        path = os.path.join(run_dir, f"double_standard_ledger_{metric}.csv")
        if os.path.exists(path):
            continue
        t0 = time.time()
        b = DistanceMatrixBuilder(docs, fs, metric, window=mr.get("ventana", 500), draws=int(mr.get("sorteos", 20)),
                                  min_tokens=ctx.min_tokens)
        led = same_standard_ledger(b, letters, core, pairs, exclude_sisters=SISTERS, pairs_inter=pairs_b, pairs_genre=pairs_g)
        _write_csv(os.path.join(run_dir, f"pair_distances_{metric}.csv"), led["envelope"])
        _write_csv(os.path.join(run_dir, f"pair_distances_inter_{metric}.csv"), led["envelope_inter"])
        _write_csv(os.path.join(run_dir, f"pair_distances_genero_{metric}.csv"), led["envelope_genre"])
        rows = [{"id": L, "kind": "core" if L in core else "target", **v} for L, v in led["letters"].items()]
        for r in rows:
            r.update({f"env_{k}": v for k, v in led["envelope_stats"].items()})
            r.update({f"inter_{k}": v for k, v in led["inter_stats"].items()})
            r.update({f"genre_{k}": v for k, v in led["genre_stats"].items()})
        _write_csv(path, rows)
        with open(os.path.join(run_dir, f"envolventes_{metric}.json"), "w", encoding="utf-8") as f:
            json.dump({"E": led["envelope_stats"], "B": led["inter_stats"], "G": led["genre_stats"],
                       "solapamiento_G_en_E_p90": led.get("overlap_G_E"), "solapamiento_B_en_E_p90": led.get("overlap_B_E")},
                      f, ensure_ascii=False, indent=1)
        if letters:
            # matriz rectangular cartas × documentos genuine (para el orden de autores y las lecturas posteriores)
            gen = [d.id for d in docs if d.status == "genuine" and d.author not in ("Pablo", "Pablo?") and d.id not in letters]
            T = b.matrix_rect(letters, gen, keep_draws=True)
            np.save(os.path.join(run_dir, f"distance_letters_docs_{metric}.npy"), T.mean(axis=2))
            with open(os.path.join(run_dir, "distance_letters_docs_ids.csv"), "w", encoding="utf-8") as f:
                f.write("axis,index,id\n" + "\n".join(f"fila,{i},{x}" for i, x in enumerate(letters)) + "\n"
                        + "\n".join(f"columna,{j},{x}" for j, x in enumerate(gen)) + "\n")
            _write_csv(os.path.join(run_dir, f"nearest_author_{metric}.csv"),
                       nearest_authors(b, letters, core, SISTERS, precomputed=(T, gen)))
        log(f"  ledger {metric}: E {len(pairs)} pares, B {len(pairs_b)}, G {len(pairs_g)}; {time.time() - t0:.0f} s")


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
    if ctx.cfg["parametros"].get("sin_dianas", False):
        return
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    _core, _t, letters = campaign_sets(ctx.cfg, docs)
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
    if ctx.cfg["parametros"].get("sin_dianas", False):
        return
    edition = ctx.cfg.get("corpus", {}).get("edicion", "sblgnt")
    docs = ctx.corpus(edition)
    core, _t, letters = campaign_sets(ctx.cfg, docs)
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
    core, _t, letters_eval = campaign_sets(ctx.cfg, docs)
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
    sin_dianas = bool(ctx.cfg["parametros"].get("sin_dianas", False))
    for L in letters_eval:
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
    # tabla resumen de las 14 cartas (familia de referencia: impostores)
    summ = {r["id"]: r for r in _read_csv(os.path.join(run_dir, "summary_by_letter.csv")) if r.get("family", "impostores") == "impostores"}
    lrl = {r["target"]: r for r in _read_csv(os.path.join(run_dir, "lr_secundaria_por_carta.csv")) if r.get("family", "impostores") == "impostores"}
    led_mm = {r["id"]: r for r in _read_csv(os.path.join(run_dir, "double_standard_ledger_minmax.csv"))}
    led_d = {r["id"]: r for r in _read_csv(os.path.join(run_dir, "double_standard_ledger_delta.csv"))}
    rows = []
    for L in letters_eval:
        if L not in by_id:
            continue
        s, l, m, dd = summ.get(L, {}), lrl.get(L, {}), led_mm.get(L, {}), led_d.get(L, {})
        rows.append({"carta": L, "tokens": by_id[L].n_tokens, "kind": "core" if L in core else "target",
                     "gi_mediana": s.get("score_median"), "gi_q1": s.get("score_q1"), "gi_q3": s.get("score_q3"),
                     "log10lr_epist_mediana": s.get("log10lr_epist_median"), "escala_verbal_epist": s.get("verbal_epist"),
                     "log10lr_mediana": s.get("log10lr_median"), "log10lr_cristiana": l.get("log10lr_cristiana_mediana"),
                     "d_minmax": m.get("d_mean"), "pct_E_minmax": m.get("percentile"), "pct_B_minmax": m.get("pct_inter"),
                     "pct_G_minmax": m.get("pct_genre"), "pct_E_delta": dd.get("percentile"), "pct_B_delta": dd.get("pct_inter"),
                     "pct_G_delta": dd.get("pct_genre")})
    _write_csv(os.path.join(run_dir, "tabla_resumen_14_cartas.csv"), rows)
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
                 data_dir: str = "data", results_dir: str = RESULTS_DIR, log=print, workers: int = 1,
                 families: list[str] | None = None, only: list[int] | None = None) -> str:
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
    _log(f"run {run_name} (paulinum {__version__}) · etapas: {', '.join(stages)} · familias: "
         f"{', '.join(families or active_families(cfg))} · workers {workers}"
         + (" · SIN DIANAS" if cfg["parametros"].get("sin_dianas", False) else ""))
    outs = None
    for st in stages:
        t0 = time.time()
        if st == "specs":
            outs = stage_specs(ctx, run_dir, _log, workers=workers, families=families, only=only)
        elif st == "calibration":
            outs = load_specs(run_dir)
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

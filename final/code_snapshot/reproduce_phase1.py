"""Module R: reproduce the phase 1 pilot on EEE_2014J with seed 42 (criterion C6, tolerance 1e-6).

Nothing is imported from the pilot folder. Functions marked [pilot Lx-y] are copied from
data/projects/e_learning_pilot/code/pilot_recommender.py (read-only prior evidence), with only these changes: paths come from
this project, the module-level RAW/RESULTS constants are dropped, and the week columns are converted with pd.to_numeric
(same values as the pilot's replace('?')/to_numeric). The pilot's own weaknesses are kept ON PURPOSE (random split, hand-picked
alpha, argsort ties): this file reproduces a number, it does not endorse the design, and it feeds no phase 2 criterion.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass

import numpy as np
import pandas as pd

import common
import data

SEED = common.SEED  # [pilot L17] 42
TARGET_ROWS = 400_000  # [pilot L18]
TOP_K = 10  # [pilot L19]
MIN_ITEMS_FOR_EVAL_USER = 5  # [pilot L20]
COLD_START_VISIBLE = 2  # [pilot L21]
TEST_FRACTION = 0.2  # [pilot L22]
RECORDED = common.PROJECT_ROOT / "inputs" / "prior_evidence" / "pilot_metrics.json"


def pick_module_presentation(vle_counts: pd.Series) -> str:  # [pilot L29-32]
    diffs = (vle_counts - TARGET_ROWS).abs()
    return diffs.sort_values(kind="stable").index[0]


def load_data(raw):  # [pilot L35-49], reading only the needed columns
    vle_raw = pd.read_csv(raw / "studentVle.csv", usecols=["code_module", "code_presentation", "id_student", "id_site", "date", "sum_click"])
    counts = vle_raw.groupby(["code_module", "code_presentation"]).size()
    counts.index = [f"{m}_{p}" for m, p in counts.index]
    chosen = pick_module_presentation(counts)
    module, presentation = chosen.split("_", 1)
    interactions = vle_raw[(vle_raw.code_module == module) & (vle_raw.code_presentation == presentation)]
    items = pd.read_csv(raw / "vle.csv")
    items = items[(items.code_module == module) & (items.code_presentation == presentation)].copy()
    return interactions, items, chosen


def build_item_features(items):  # [pilot L52-83]
    item_ids = items["id_site"].tolist()
    activity = pd.get_dummies(items["activity_type"], prefix="act")
    week_from = pd.to_numeric(items["week_from"], errors="coerce")
    week_to = pd.to_numeric(items["week_to"], errors="coerce")
    week_missing = week_from.isna().astype(float)
    week_from = week_from.fillna(week_from.median() if week_from.notna().any() else 0.0)  # all-NaN column falls back to 0.0
    week_to = week_to.fillna(week_to.median() if week_to.notna().any() else 0.0)
    features = pd.concat([activity.reset_index(drop=True).astype(float),
                          (week_from / max(week_from.max(), 1)).reset_index(drop=True).rename("week_from_n"),
                          (week_to / max(week_to.max(), 1)).reset_index(drop=True).rename("week_to_n"),
                          week_missing.reset_index(drop=True).rename("week_missing")], axis=1).to_numpy(dtype=float)
    features = np.nan_to_num(features, nan=0.0)
    norms = np.linalg.norm(features, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return features / norms, item_ids


@dataclass
class UserSplit:  # [pilot L86-93]
    user: int
    train_items: list
    train_weights: list
    cold_items: list
    cold_weights: list
    test_items: set


def build_splits(interactions, item_ids):  # [pilot L96-126]; the random per-learner permutation is the pilot's, kept for C6
    item_set = set(item_ids)
    engagement = interactions[interactions.id_site.isin(item_set)].groupby(["id_student", "id_site"])["sum_click"].sum().reset_index()
    rng = np.random.default_rng(SEED)
    splits = []
    for user, group in engagement.groupby("id_student"):
        rows = group[["id_site", "sum_click"]].to_numpy()
        if len(rows) < MIN_ITEMS_FOR_EVAL_USER:
            continue
        rows = rows[rng.permutation(len(rows))]
        n_test = max(1, int(round(len(rows) * TEST_FRACTION)))
        test_rows, train_rows = rows[:n_test], rows[n_test:]
        if len(train_rows) < COLD_START_VISIBLE + 1:
            continue
        splits.append(UserSplit(int(user), [int(x) for x in train_rows[:, 0]], [float(x) for x in train_rows[:, 1]],
                                [int(x) for x in train_rows[:COLD_START_VISIBLE, 0]], [float(x) for x in train_rows[:COLD_START_VISIBLE, 1]],
                                set(int(x) for x in test_rows[:, 0])))
    return splits


def build_engagement_matrix(splits, item_ids):  # [pilot L129-137]
    index = {item: i for i, item in enumerate(item_ids)}
    mat = np.zeros((len(splits), len(item_ids)))
    for row, split in enumerate(splits):
        for item, weight in zip(split.train_items, split.train_weights):
            mat[row, index[item]] = weight
    return mat


def cosine_sim_matrix(mat):  # [pilot L140-144]
    norms = np.linalg.norm(mat, axis=0, keepdims=True)
    norms[norms == 0] = 1.0
    normed = mat / norms
    return normed.T @ normed


def minmax(scores):  # [pilot L147-151]
    lo, hi = scores.min(), scores.max()
    if hi - lo < 1e-12:
        return np.zeros_like(scores)
    return (scores - lo) / (hi - lo)


def recommend_cbf(visible_items, visible_weights, item_vectors, index):  # [pilot L154-164]
    if not visible_items:
        return np.zeros(item_vectors.shape[0])
    w = np.array(visible_weights)
    w = w / w.sum()
    vecs = item_vectors[[index[i] for i in visible_items]]
    profile = (vecs * w[:, None]).sum(axis=0)
    norm = np.linalg.norm(profile)
    if norm > 0:
        profile = profile / norm
    return item_vectors @ profile


def recommend_cf(visible_items, visible_weights, item_sim, index):  # [pilot L167-173]
    if not visible_items:
        return np.zeros(item_sim.shape[0])
    idxs = [index[i] for i in visible_items]
    w = np.array(visible_weights)
    return (item_sim[idxs] * w[:, None]).sum(axis=0) / w.sum()


def top_k_excluding(scores, item_ids, exclude, k):  # [pilot L176-186]; default argsort, as the pilot
    order = np.argsort(-scores)
    out = []
    for i in order:
        item = item_ids[i]
        if item in exclude:
            continue
        out.append(item)
        if len(out) == k:
            break
    return out


def evaluate(splits, item_vectors, item_sim, item_ids, index, scenario):  # [pilot L189-228]
    precisions = {"cbf": [], "cf": [], "hybrid": []}
    union = {"cbf": set(), "cf": set(), "hybrid": set()}
    for split in splits:
        if scenario == "warm":
            vi, vw = split.train_items, split.train_weights
        else:
            vi, vw = split.cold_items, split.cold_weights
        cbf = recommend_cbf(vi, vw, item_vectors, index)
        cf = recommend_cf(vi, vw, item_sim, index)
        alpha = min(0.9, 0.2 + 0.05 * len(vi))  # the pilot's hand-picked weight: exploratory, reproduced only for C6
        hybrid = alpha * minmax(cf) + (1 - alpha) * minmax(cbf)
        for name, scores in (("cbf", cbf), ("cf", cf), ("hybrid", hybrid)):
            rec = top_k_excluding(scores, item_ids, set(vi), TOP_K)
            precisions[name].append(len(set(rec) & split.test_items) / TOP_K)
            union[name].update(rec)
    return {n: {"precision_at_10": float(np.mean(v)) if v else 0.0, "n_users": len(v), "distinct_items_recommended": len(union[n])}
            for n, v in precisions.items()}


def run(ctx) -> int:
    """Stage `pilot`. Writes phase1_reproduced_metrics.json (deterministic content, no timings) and returns 0 iff C6 holds."""
    log, t0 = ctx["log"], time.time()
    data.verify_raw_files(data.raw_dir(), log, ("studentVle.csv", "vle.csv"))
    interactions, items, chosen = load_data(data.raw_dir())
    log.measure("P1_selected_presentation_is_EEE_2014J", int(chosen != "EEE_2014J"), chosen=chosen)
    item_vectors, item_ids = build_item_features(items)
    if not np.isfinite(item_vectors).all():
        raise common.LeakageError("non-finite pilot item vectors")
    index = {item: i for i, item in enumerate(item_ids)}
    splits = build_splits(interactions, item_ids)
    item_sim = cosine_sim_matrix(build_engagement_matrix(splits, item_ids))
    warm = evaluate(splits, item_vectors, item_sim, item_ids, index, "warm")
    cold = evaluate(splits, item_vectors, item_sim, item_ids, index, "cold_start")
    report = {"dataset": "OULAD", "module_presentation": chosen, "n_raw_interaction_rows": int(len(interactions)), "n_items": len(item_ids),
              "n_eval_users": len(splits), "hardware": common.HARD_CONSTRAINTS["hardware"], "warm": warm, "cold_start": cold}
    recorded = json.loads(RECORDED.read_text(encoding="utf-8"))
    diffs = {f"{sc}.{m}": abs(report[sc][m]["precision_at_10"] - recorded[sc][m]["precision_at_10"])
             for sc in ("warm", "cold_start") for m in ("cbf", "cf", "hybrid")}
    other = sum(report[k] != recorded[k] for k in ("n_raw_interaction_rows", "n_items", "n_eval_users"))
    other += sum(report[sc][m][f] != recorded[sc][m][f] for sc in ("warm", "cold_start") for m in ("cbf", "cf", "hybrid") for f in ("n_users", "distinct_items_recommended"))
    report["c6"] = {"abs_diff_precision_at_10": diffs, "max_abs_diff": max(diffs.values()), "tolerance": 1e-6, "other_fields_differing": other}
    (ctx["artifact_dir"] / "phase1_reproduced_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    ok = log.flag("C6_values_beyond_1e-6", sum(v > 1e-6 for v in diffs.values()), max_abs_diff=max(diffs.values()), other_fields_differing=other)
    minutes = (time.time() - t0) / 60
    log.flag("C5_reproduction_minutes_over_15", int(minutes > common.HARD_CONSTRAINTS["max_minutes_phase1_reproduction"]), minutes=round(minutes, 2))
    ctx["c6"], ctx["repro_minutes"] = report["c6"], minutes
    log.emit("assert", id="L9", count=None, status="not_applicable", reason="C6 reproduces the pilot unbounded arithmetic; no bound is defined (protocol 5.5)")
    log.emit("assert", id="L1-L8", count=None, status="not_applicable", reason="phase 2 leakage rules do not apply to the phase 1 reproduction (protocol 5.5)")
    return 0 if ok and other == 0 else 3

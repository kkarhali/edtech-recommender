"""Module A orchestration: prepare one presentation and run every foundation check of protocol 13 that exists before any
model does. Parts 2 and 3 call `prepare` for the Prep and reuse the helpers in provenance.py / leakage.py / features.py."""
from __future__ import annotations

import time

import numpy as np

import features
import leakage
import provenance
from common import KS_COLD, canon_hash
from data import item_features
from splits import TEST, TRAIN, VAL, build_prep, make_condition, split_view

# Protocol 4.1: (in log, -<5 items, -<3 days, evaluated, cohort). The run regenerates and compares every cell.
TABLE_41 = {
    "AAA_2013J": (378, 1, 2, 375, 75), "AAA_2014J": (357, 7, 3, 347, 69), "BBB_2013B": (1537, 58, 75, 1404, 281),
    "BBB_2013J": (1870, 82, 88, 1700, 340), "BBB_2014B": (1294, 72, 59, 1163, 233), "BBB_2014J": (1921, 63, 85, 1773, 355),
    "CCC_2014B": (1681, 71, 53, 1557, 311), "CCC_2014J": (2302, 106, 65, 2131, 426), "DDD_2013B": (1214, 25, 39, 1150, 230),
    "DDD_2013J": (1768, 44, 68, 1656, 331), "DDD_2014B": (1116, 35, 41, 1040, 208), "DDD_2014J": (1647, 76, 48, 1523, 305),
    "EEE_2013J": (964, 41, 25, 898, 180), "EEE_2014B": (624, 18, 22, 584, 117), "EEE_2014J": (1097, 48, 31, 1018, 204),
    "FFF_2013B": (1510, 24, 26, 1460, 292), "FFF_2013J": (2098, 46, 63, 1989, 398), "FFF_2014B": (1363, 30, 52, 1281, 256),
    "FFF_2014J": (2121, 78, 55, 1988, 398), "GGG_2013J": (895, 30, 30, 835, 167), "GGG_2014B": (773, 33, 35, 705, 141),
    "GGG_2014J": (698, 31, 32, 635, 127)}
EEE_REFERENCE = {"n_rows": 402947, "n_items": 115, "n_pairs": 47136, "in_log": 1097}  # protocol 2.2 / P3
EEE_QUOTAS = [41, 41, 41, 40, 41]  # protocol 6.1b
ALL_WEEK_MISSING = ("BBB_2013B", "DDD_2013B", "DDD_2013J")  # protocol 2.3: week_from/week_to 100% missing
MODEL_NAMES = ("Random", "MostPop", "PopWeek", "CBF", "ItemKNN-CF", "Hybrid")


def prepare(oulad, pres: str, log):
    """Build the split once per presentation (the object handed unchanged to every model)."""
    t0 = time.time()
    prep = build_prep(oulad, pres, log)
    log.emit("prepared", pres=pres, seconds=round(time.time() - t0, 2), **prep.counts)
    return prep


def _quotas(prep) -> list:
    order = prep.learners.reset_index().sort_values(["n_train", "id_student"], kind="stable").id_student.to_numpy()
    n, cut = len(order), lambda j: (2 * j * len(order) + 5) // 10
    return [int(np.isin(order[cut(j):cut(j + 1)], prep.cohort_A).sum()) for j in range(5)]


def _fit_objects(log, prep, cond, ctx) -> dict:
    """The objects of part 1 (A1-A3) for one condition, each with a provenance record, plus the A1 row-learner check."""
    fit, cold, exp = cond.fit_ids, cond.cold_ids, cond.expected_cold_in_fit
    mat, rid, read = features.engagement_matrix(prep, fit, f"{prep.pres}/{cond.name}/engagement")
    provenance.emit(log, provenance.record("similarity_matrix", read, prep, fit, (TRAIN,), cold), exp, **ctx)
    features.gram_cosine(mat)  # raises on a non-finite similarity
    log.measure("A1_row_learners_in_cold", len(np.intersect1d(rid, cold)), required=exp, n_row_learners=len(rid), n_fit_learners=len(fit), **ctx)
    w = features.clicks_from(read)
    want = prep.pairs[(prep.pairs.role == TRAIN) & prep.pairs.id_student.isin(fit)][["id_student", "id_site"]]
    both = w[["id_student", "id_site"]].merge(want, how="outer", indicator=True)
    log.measure("W_TRAIN_PAIRS_MISMATCH", (both["_merge"] != "both").sum(), **ctx)  # weights exist for exactly the training pairs
    _, pr = features.mostpop_counts(prep, fit)
    for name in ("mostpop_counts", "popweek_counts"):
        provenance.emit(log, provenance.record(name, pr, prep, fit, (TRAIN,), cold), exp, denominator=int(pr.id_student.nunique()), **ctx)
    provenance.coverage(log, provenance.FOUNDATION_OBJECTS, **ctx)
    leakage.l9_hash_equivalence(log, prep, fit, features.training_bound(prep, fit), False, f"{prep.pres}/{cond.name}/train_weights", **ctx)
    leakage.l9_flush(log, **ctx)
    return {"n_row_learners": len(rid), "n_fit_learners": len(fit), "n_train_pairs_weighted": len(w)}


def verify(prep, log, ks=KS_COLD, k_robust: int = 2) -> dict:
    """Run every part-1 check for one presentation; returns the report written to foundation_<pres>.json."""
    pres, c = prep.pres, prep.counts
    got = (c["in_log"], c["drop_lt5"], c["drop_lt3days"], c["evaluated"], len(prep.cohort_A))
    log.measure("T41_population_cells_differing", sum(g != w for g, w in zip(got, TABLE_41[pres])), pres=pres, got=list(got), protocol=list(TABLE_41[pres]))
    quotas = _quotas(prep)
    if pres == "EEE_2014J":
        diff = sum(c[k] != v for k, v in EEE_REFERENCE.items()) + sum(a != b for a, b in zip(quotas, EEE_QUOTAS))
        log.measure("REF_EEE_2014J_cells_differing", diff, pres=pres, quotas=quotas)
    out_of_range = int(not 0.199 <= round(c["test_frac"], 3) <= 0.205) + int(not 0.102 <= round(c["val_frac"], 3) <= 0.120)
    log.flag("SPLIT_FRACTIONS_OUT_OF_RANGE", out_of_range, pres=pres, test_frac=c["test_frac"], val_frac=c["val_frac"])
    leakage.l1(log, prep, pres=pres)
    leakage.l4(log, prep, pres=pres)
    leakage.l5(log, prep, {m: split_view(prep) for m in MODEL_NAMES}, pres=pres, scope="foundation views, not models")
    consts = prep.feature_constants
    log.emit("p5", pres=pres, **{k: v for k, v in consts.items() if k != "n_learner_rows_used"})
    log.measure("P5_nonfinite_feature_cells", (~np.isfinite(prep.features)).sum(), pres=pres)
    log.measure("P5_all_missing_mismatch", int((len(consts["all_missing_columns"]) == 2) != (pres in ALL_WEEK_MISSING)), pres=pres, all_missing=consts["all_missing_columns"])
    f2, c2 = item_features(prep.items)
    log.measure("A4_differing_cells", (f2 != prep.features).sum(), pres=pres, n_learner_rows_used=c2["n_learner_rows_used"])
    for name in ("p5_week_medians", "week_minmax_bounds", "item_feature_matrix"):
        provenance.catalogue_constant(log, name, len(prep.items), pres=pres)
    ids = prep.learners.index.to_numpy()
    leakage.l8(log, prep, "M1", features.exclusion_sets(prep, ids, "M1"), ids, VAL, pres=pres, condition="warm")
    leakage.l8(log, prep, "M2", features.exclusion_sets(prep, ids, "M2"), ids, TEST, pres=pres, condition="warm")
    rep = {"pres": pres, "counts": c, "split_sha256": {"train": prep.hashes[0], "val": prep.hashes[1], "test": prep.hashes[2]},
           "cohort": {"n": len(prep.cohort_A), "quotas": quotas, "sha256": canon_hash(prep.cohort_A.astype("<i8")),
                      "robust_n": len(prep.cohort_R), "robust_sha256": canon_hash(prep.cohort_R.astype("<i8"))},
           "feature_constants": consts, "item_feature_sha256": canon_hash(prep.features.astype("<f8")), "conditions": {}}
    plan = [("warm", None)] + [("A", k) for k in ks] + [("A_robust", k_robust)] + [("B", k) for k in ks]
    for name, k in plan:
        cond = make_condition(prep, name, k)
        ctx = {"pres": pres, "condition": name, "k": k}
        rep["conditions"][f"{name}|{k}"] = _fit_objects(log, prep, cond, ctx)
        if name == "warm":
            continue
        label = f"{pres}/{name}/k{k}"
        vis = features.visible_history(prep, cond.eval_ids, k, label)
        leakage.visible_checks(log, prep, vis, cond.eval_ids, k, pres=pres, condition=name)
        used = features.exclusion_sets(prep, cond.eval_ids, "M3", vis)
        leakage.l8(log, prep, "M3", used, cond.eval_ids, VAL, **ctx)  # validation boundary; ctx already carries k
        leakage.l8(log, prep, "M3", used, cond.eval_ids, TEST, **ctx)  # test boundary: same visible set
        if k > 0:
            leakage.l9_hash_equivalence(log, prep, cond.eval_ids, vis.bound, True, label + "/cold_weights", pairs=vis.pairs, **ctx)
        leakage.l9_flush(log, **ctx)
        log.emit("a8_visible", visible_pairs=int(len(vis.pairs)), mean_active_days=float(vis.active_days.mean()) if len(vis.active_days) else 0.0, **ctx)
    for name, k in (("A", ks[0]), ("A_robust", k_robust)):
        leakage.l7_rebuild(log, prep, make_condition(prep, name, k), ks, pres=pres, condition=name)
    return rep

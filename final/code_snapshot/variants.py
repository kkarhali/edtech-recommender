"""Module A, the runs part 1 deferred (protocol 5.2, 5.3, 5.5, 12.1): derived Prep objects that the same models and checks run on.
`learners.val_start` is the training bound of features.training_bound: D_val+1 (secondary), a value beyond every date (tertiary:
no bound is defined or applied) and the second day d_2 (P4b two-day learners). None of these decides a criterion."""
from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd

import features
from common import MIN_ITEMS, SEED
from splits import TEST, TRAIN, VAL, Prep, draw_cohort, pair_hash, robust_cohort

NO_BOUND = 10 ** 9
D_TABLE = {"AAA_2013J": 192, "AAA_2014J": 188, "BBB_2013B": 159, "BBB_2013J": 181, "BBB_2014B": 163, "BBB_2014J": 179,
           "CCC_2014B": 180, "CCC_2014J": 198, "DDD_2013B": 148, "DDD_2013J": 175, "DDD_2014B": 156, "DDD_2014J": 192,
           "EEE_2013J": 156, "EEE_2014B": 150, "EEE_2014J": 164, "FFF_2013B": 164, "FFF_2013J": 170, "FFF_2014B": 165,
           "FFF_2014J": 184, "GGG_2013J": 201, "GGG_2014B": 191, "GGG_2014J": 194}  # protocol 5.2, row-based 80th percentile


def _learners(pairs: pd.DataFrame, bound) -> pd.DataFrame:
    g = pairs.groupby("id_student")
    L = pd.DataFrame({"n_pairs": g.size(), "first_day": g["first_date"].min(), "n_days": g["first_date"].nunique()})
    for name, r in (("n_train", TRAIN), ("n_val", VAL), ("n_test", TEST)):
        L[name] = pairs[pairs.role == r].groupby("id_student").size().reindex(L.index, fill_value=0)
    L["val_start"] = bound
    L["test_start"] = L["val_start"]
    return L


def _derive(prep: Prep, pairs: pd.DataFrame, bound, extra: dict, na: bool = False) -> Prep:
    pairs = pairs.sort_values(["id_student", "first_date", "id_site"], kind="stable").reset_index(drop=True)
    L = _learners(pairs, bound)
    counts = {**prep.counts, **extra, "evaluated": int(len(L)), "test_frac": float(L.n_test.sum() / L.n_pairs.sum()),
              "val_frac": float(L.n_val.sum() / L.n_pairs.sum())}
    hashes = tuple(pair_hash(pairs[pairs.role == r]) for r in (TRAIN, VAL, TEST))
    return dataclasses.replace(prep, pairs=pairs, learners=L, counts=counts, cohort_A=draw_cohort(L), cohort_R=robust_cohort(L),
                               hashes=hashes, l9_training_na=na)


def secondary(prep: Prep, all_rows: pd.DataFrame, log) -> Prep:
    """5.2 with 5.5: global D (row-based 80th percentile, truncated) and D_val; training bound date <= D_val for everybody."""
    D = int(np.percentile(all_rows.date.to_numpy(), 80))
    log.measure("D_TABLE_MISMATCH", int(D != D_TABLE[prep.pres]), pres=prep.pres, D=D)
    p = prep.pairs.drop(columns="role")
    fd, total = p.first_date.to_numpy(), len(p)
    ds = np.unique(fd[fd <= D])
    cnt = int((fd <= D).sum()) - np.searchsorted(np.sort(fd), ds, side="right")  # pairs with d < first_date <= D
    ok = ds[cnt * 10 <= total]  # smallest D_val whose validation slice does not exceed 10% of the pairs
    dval = int(ok.min()) if len(ok) else D
    p = p.assign(role=np.where(fd > D, TEST, np.where(fd > dval, VAL, TRAIN)))
    keep = p[p.role == TRAIN].id_student.unique()
    dropped = int(len(prep.learners) - len(keep))
    return _derive(prep, p[p.id_student.isin(keep)], dval + 1, {"D": D, "D_val": dval, "dropped_no_training_pair": dropped})


def tertiary(prep: Prep) -> Prep:
    """5.3: the pilot random split, temporally leaky, reporting only. One default_rng(42) over learners in id order, pairs in
    id_site order (the pilot order); 20% test, next 10% validation, 70% training. No date bound exists (5.5)."""
    p = prep.pairs.drop(columns="role").sort_values(["id_student", "id_site"], kind="stable").reset_index(drop=True)
    ids = p.id_student.to_numpy()
    starts = np.flatnonzero(np.r_[True, ids[1:] != ids[:-1]])
    ends = np.r_[starts[1:], len(ids)]
    rng, role = np.random.default_rng(SEED), np.empty(len(p), dtype=np.int64)
    for s, e in zip(starts, ends):
        n = e - s
        perm, nt, nv = rng.permutation(n), max(1, int(round(n * 0.2))), max(1, int(round(n * 0.1)))
        r = np.full(n, TRAIN)
        r[perm[:nt]], r[perm[nt:nt + nv]] = TEST, VAL
        role[s:e] = r
    return _derive(prep, p.assign(role=role), NO_BOUND, {"temporally_leaky": True}, na=True)


def two_day_view(prep: Prep, all_rows: pd.DataFrame):
    """P4b (12.1, 5.5): learners with >= 5 items and exactly two distinct days. Day 1 pairs are training, day 2 pairs are test, the
    bound is d_2 (date < d_2), exclusion M2 with an empty validation set. They are never part of `prep`, so they enter no fit."""
    r = all_rows[all_rows.id_site.isin(prep.item_ids)]
    p = r.groupby(["id_student", "id_site"], sort=True)["date"].min().rename("first_date").reset_index()
    per = p.groupby("id_student").agg(n=("id_site", "size"), m=("first_date", "nunique"))
    sel = per.index[(per.n >= MIN_ITEMS) & (per.m == 2)].to_numpy()
    if len(sel) == 0:
        return None
    p = p[p.id_student.isin(sel)]
    d2 = p.groupby("id_student")["first_date"].transform("max")
    p = p.assign(role=np.where(p.first_date < d2, TRAIN, TEST)).sort_values(["id_student", "first_date", "id_site"]).reset_index(drop=True)
    L = _learners(p, p.groupby("id_student")["first_date"].max())
    rows = r[r.id_student.isin(sel)].sort_values(["id_student", "date", "id_site"]).reset_index(drop=True)
    return features.View(prep.pres, prep.item_ids, p, rows, L, prep.features, prep.feature_constants["week_missing_share"])

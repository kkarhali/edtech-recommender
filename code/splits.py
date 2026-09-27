"""Module A, splitting: pairs, learner filters P4a/P4b, the per-learner day-boundary split (protocol 5.1),
the seeded cohort draw (6.1b) and the conditions warm / A / A_robust / B (6.4). The split needs no seed."""
from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

import numpy as np
import pandas as pd

from common import MIN_DAYS, MIN_ITEMS, SEED, canon_hash
from data import Oulad, item_features

TRAIN, VAL, TEST = 0, 1, 2  # values of pairs.role


@dataclass
class Prep:
    """Everything one presentation's models need, built once and handed unchanged to every model."""
    pres: str
    item_ids: np.ndarray  # catalogue, id_site ascending (the tie-break order of protocol 8.0 i)
    items: pd.DataFrame
    pairs: pd.DataFrame  # evaluated learners only: id_student, id_site, first_date, role
    learners: pd.DataFrame  # index id_student: n_pairs, val_start, test_start, first_day, n_days, n_train, n_val, n_test
    rows: pd.DataFrame  # evaluated learners' rows, sorted by (id_student, date, id_site)
    counts: dict
    cohort_A: np.ndarray
    cohort_R: np.ndarray
    hashes: tuple  # (train, val, test) SHA256 of the serialised pair sets
    features: np.ndarray
    feature_constants: dict
    l9_training_na: bool = False  # tertiary split: no training bound exists (protocol 5.5), L9 is not applicable


def split_learner(fd: np.ndarray) -> tuple[int, int]:
    """Protocol 5.1 for one learner. fd = the learner's first_date values, ascending. Returns (val_start, test_start).

    Integer arithmetic (x5 and x10) keeps the tie rules exact: ties go to the larger j and the larger i.
    """
    n = len(fd)
    days, cnt = np.unique(fd, return_counts=True)
    m = len(days)
    if m < 3:
        raise ValueError("split needs m >= 3 distinct days (filter P4b)")
    suffix = cnt[::-1].cumsum()[::-1]  # suffix[j-1] = pairs on day d_j or later
    js = np.arange(3, m + 1)
    dev = np.abs(5 * suffix[js - 1] - n)  # |suffix(j) - 0.20 n| * 5
    jstar = int(js[np.flatnonzero(dev == dev.min())[-1]])
    st = suffix[jstar - 1]
    iss = np.arange(2, jstar)  # 2 .. j*-1
    dev2 = np.abs(10 * (suffix[iss - 1] - st) - n)  # |(suffix(i) - suffix(j*)) - 0.10 n| * 10
    istar = int(iss[np.flatnonzero(dev2 == dev2.min())[-1]])
    return int(days[istar - 1]), int(days[jstar - 1])


def draw_cohort(learners: pd.DataFrame) -> np.ndarray:
    """Protocol 6.1b: rank strata by (n_train, id_student), largest-remainder quotas, one default_rng(42) per
    presentation consumed stratum 0..4 in rank order (NOT re-sorted by id_student)."""
    n = len(learners)
    target = (2 * n + 5) // 10  # round(0.20 n); never a .5 tie
    ids = learners.reset_index().sort_values(["n_train", "id_student"], kind="stable").id_student.to_numpy()
    cuts = [(2 * j * n + 5) // 10 for j in range(6)]  # round(j n / 5)
    strata = [ids[cuts[j]:cuts[j + 1]] for j in range(5)]
    quota = [target * len(s) // n for s in strata]
    rem = [target * len(s) % n for s in strata]
    for j in sorted(range(5), key=lambda j: (-rem[j], j))[:target - sum(quota)]:
        quota[j] += 1
    rng = np.random.default_rng(SEED)
    return np.sort(np.concatenate([rng.choice(s, size=q, replace=False) for s, q in zip(strata, quota)]))


def robust_cohort(learners: pd.DataFrame) -> np.ndarray:
    """A-robustness: the last round(0.20 n) learners by (first interaction date, id_student). No generator."""
    n = len(learners)
    order = learners.reset_index().sort_values(["first_day", "id_student"], kind="stable").id_student.to_numpy()
    return np.sort(order[n - (2 * n + 5) // 10:])


def pair_hash(df: pd.DataFrame) -> str:
    return canon_hash(df[["id_student", "id_site"]].sort_values(["id_student", "id_site"]).to_numpy(dtype="<i8"))


class SplitView(NamedTuple):
    pres: str
    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame


def split_view(prep: Prep) -> SplitView:
    """The object every model receives; L5 re-hashes it per model."""
    part = {r: prep.pairs[prep.pairs.role == r][["id_student", "id_site"]].reset_index(drop=True) for r in (TRAIN, VAL, TEST)}
    return SplitView(prep.pres, part[TRAIN], part[VAL], part[TEST])


def view_hashes(v: SplitView) -> tuple:
    return pair_hash(v.train), pair_hash(v.val), pair_hash(v.test)


def build_prep(oulad: Oulad, pres: str, log, min_items: int = MIN_ITEMS, min_days: int = MIN_DAYS) -> Prep:
    rows, items = oulad.rows[pres], oulad.items[pres]
    item_ids = items.id_site.to_numpy()
    in_cat = rows.id_site.isin(item_ids).to_numpy()
    log.measure("P2_rows_outside_catalogue", (~in_cat).sum(), pres=pres)  # protocol P2: 0 in all 22
    rows_cat = rows[in_cat]
    pairs = rows_cat.groupby(["id_student", "id_site"], sort=True)["date"].min().rename("first_date").reset_index()  # P3
    per = pairs.groupby("id_student").agg(n=("id_site", "size"), m=("first_date", "nunique"))
    keep5 = per.n >= min_items  # P4a (3 and 10 in the sensitivity reruns)
    per5 = per[keep5]
    keep3 = per5.m >= min_days  # P4b
    evaluated = per5.index[keep3].to_numpy()
    counts = {"n_rows": int(len(rows)), "n_items": int(len(item_ids)), "n_pairs": int(len(pairs)), "in_log": int(len(per)),
              "drop_lt5": int((~keep5).sum()), "drop_lt3days": int((~keep3).sum()), "evaluated": int(len(evaluated)),
              "registered": oulad.registered[pres]}
    pairs = pairs[pairs.id_student.isin(evaluated)].sort_values(["id_student", "first_date", "id_site"], kind="stable").reset_index(drop=True)
    rows_ev = rows_cat[rows_cat.id_student.isin(evaluated)].sort_values(["id_student", "date", "id_site"], kind="stable").reset_index(drop=True)
    ids, fd = pairs.id_student.to_numpy(), pairs.first_date.to_numpy()
    starts = np.flatnonzero(np.r_[True, ids[1:] != ids[:-1]])
    ends = np.r_[starts[1:], len(ids)]
    role, recs = np.empty(len(ids), dtype=np.int64), []
    for s, e in zip(starts, ends):
        v, t = split_learner(fd[s:e])
        role[s:e] = np.where(fd[s:e] >= t, TEST, np.where(fd[s:e] >= v, VAL, TRAIN))
        recs.append((int(ids[s]), e - s, v, t, int(fd[s]), len(np.unique(fd[s:e]))))
    pairs["role"] = role
    learners = pd.DataFrame(recs, columns=["id_student", "n_pairs", "val_start", "test_start", "first_day", "n_days"]).set_index("id_student")
    by_role = pairs.groupby(["id_student", "role"]).size().unstack(fill_value=0).reindex(index=learners.index, columns=[TRAIN, VAL, TEST], fill_value=0)
    learners["n_train"], learners["n_val"], learners["n_test"] = by_role[TRAIN], by_role[VAL], by_role[TEST]
    empty = int(((learners.n_train == 0) | (learners.n_val == 0) | (learners.n_test == 0)).sum())
    log.measure("SPLIT_EXCLUDED_LEARNERS", empty, pres=pres)  # protocol 5.1 step 4: the split itself excludes nobody
    feat, consts = item_features(items)
    tr, va, te = (pair_hash(pairs[pairs.role == r]) for r in (TRAIN, VAL, TEST))
    counts.update(test_frac=float(learners.n_test.sum() / learners.n_pairs.sum()), val_frac=float(learners.n_val.sum() / learners.n_pairs.sum()))
    return Prep(pres, item_ids, items, pairs, learners, rows_ev, counts, draw_cohort(learners), robust_cohort(learners),
                (tr, va, te), feat, consts)


@dataclass(frozen=True)
class Condition:
    """What a model is fitted on (fit_ids) and scored on (eval_ids): a condition is defined by both (protocol 6.4)."""
    name: str  # warm | A | A_robust | B
    k: int | None  # visible pairs for cold conditions, None when warm
    fit_ids: np.ndarray
    eval_ids: np.ndarray
    cold_ids: np.ndarray

    @property
    def expected_cold_in_fit(self) -> int:
        return len(self.cold_ids) if self.name == "B" else 0  # B fits on the cohort on purpose (optimistic)


def make_condition(prep: Prep, name: str, k: int | None = None) -> Condition:
    everyone = prep.learners.index.to_numpy()
    if name == "warm":
        return Condition("warm", None, everyone, everyone, everyone[:0])
    if name not in ("A", "A_robust", "B") or k is None:
        raise ValueError(f"cold condition needs a name in A/A_robust/B and a k, got {name!r}, {k!r}")
    cold = prep.cohort_R if name == "A_robust" else prep.cohort_A
    fit = everyone if name == "B" else np.setdiff1d(everyone, cold)  # A: rows of C removed from the fit itself
    return Condition(name, int(k), fit, cold, cold)

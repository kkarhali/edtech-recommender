"""Leakage assertions L1-L9 (protocol 5.4) plus the visible-history checks of 6.1. Every function emits its measured
count through RunLog.measure, zero included, and aborts on a non-zero count. L2, L3 and L7 counts come from
provenance.py; L9 rows come from features.LEDGER; L7's independent check is the fresh-process rebuild of 6.1a."""
from __future__ import annotations

import collections
import importlib
import json
import os
import pickle
import subprocess
import sys
import time

import numpy as np
import pandas as pd

import features
from common import CODE_DIR, CONFIG, LeakageError, canon_hash
from splits import TEST, TRAIN, VAL, view_hashes


CHILD_SECONDS = [0.0]  # wall seconds of fresh-process workers; time.process_time() does not see children


def l1(log, prep, require_all: bool = True, **ctx) -> None:
    """Per learner: max first_date over train+validation < min first_date over test, strictly. require_all=False (secondary
    split) counts only learners that have both sides: a learner with no test pair has nothing to violate."""
    p = prep.pairs
    a = pd.DataFrame({"tv": p[p.role < TEST].groupby("id_student")["first_date"].max(),
                      "te": p[p.role == TEST].groupby("id_student")["first_date"].min()}).reindex(prep.learners.index)
    bad = (a.tv >= a.te) | ((a.tv.isna() | a.te.isna()) if require_all else False)
    log.measure("L1", bad.sum(), n_learners=len(a), **ctx)


def l4(log, prep, **ctx) -> dict:
    v = {r: prep.pairs[prep.pairs.role == r][["id_student", "id_site"]] for r in (TRAIN, VAL, TEST)}
    out = {}
    for a, b, name in ((TRAIN, VAL, "train_val"), (VAL, TEST, "val_test"), (TRAIN, TEST, "train_test")):
        out[name] = len(v[a].merge(v[b], on=["id_student", "id_site"]))
        log.measure("L4", out[name], pair=name, **ctx)
    return out


def l5(log, prep, views: dict, **ctx) -> None:
    """views: model name -> the SplitView that model actually received. Counts models whose hash triple differs."""
    bad = [m for m, v in views.items() if view_hashes(v) != prep.hashes]
    log.measure("L5", len(bad), n_models=len(views), models_differing=bad, **ctx)


class ScoreCounter:
    """Evaluation calls scored_test once per test scoring; L6 requires that no (model, split, presentation, condition, k, seed)
    cell is scored twice. The split is part of the key (G4 cycle-0 blocker B2): the same (condition, k) cell is run on five
    splits of one presentation (primary, secondary, tertiary, P4a_3, P4a_10), and without the split those are the same key."""

    def __init__(self):
        self.n = collections.Counter()

    def scored_test(self, model, split, pres, condition, k, seed=None) -> None:
        self.n[(model, split, pres, condition, k, seed)] += 1

    def check(self, log, **ctx) -> None:
        log.measure("L6", sum(1 for v in self.n.values() if v > 1), max_count=max(self.n.values(), default=0), n_cells=len(self.n), **ctx)


def _independent_exclusion(prep, ids, moment, k=None) -> dict:
    """Python-loop recomputation of the exclusion set, sharing no code with features.exclusion_sets."""
    want, by = set(int(u) for u in ids), collections.defaultdict(list)
    for u, i, d, r in zip(prep.pairs.id_student.tolist(), prep.pairs.id_site.tolist(), prep.pairs.first_date.tolist(), prep.pairs.role.tolist()):
        if u in want and (r == TRAIN or (r == VAL and moment == "M2")):
            by[u].append((d, i, r))
    out = {u: frozenset() for u in want}
    for u, lst in by.items():
        if moment == "M3":
            lst = sorted(x for x in lst if x[2] == TRAIN)[:k]
        out[u] = frozenset(i for _, i, _ in lst)
    return out


def l8(log, prep, moment: str, used: dict, ids, truth_role: int, k=None, **ctx) -> None:
    """`used` = the exclusion set each learner was actually scored with. Emits failures of the equality with an independent
    recomputation, and the learners whose ground truth sits inside their own exclusion set (the M2-at-M1 degeneracy)."""
    expected, truth = _independent_exclusion(prep, ids, moment, k), features.truth_sets(prep, ids, truth_role)
    log.measure("L8", sum(1 for u in expected if used[u] != expected[u]), moment=moment, n_learners=len(expected), **ctx)
    log.measure("L8_truth_in_exclusion", sum(1 for u in expected if used[u] & truth[u]), moment=moment, **ctx)


def l9_flush(log, na_training: bool = False, **ctx) -> None:
    """Emit and measure every weight-forming call made since the last flush: rows read at or after its own bound."""
    for e in features.LEDGER:
        if na_training and e["bound_kind"] == "training":  # protocol 5.5: no bound is defined, so L9 is not applicable, never 0
            log.emit("assert", id="L9", count=None, status="not_applicable", object=e["object"], n_rows_read=e["n_rows_read"], **ctx)
            continue
        log.measure("L9", e["n_rows_at_or_after_bound"], object=e["object"], bound_kind=e["bound_kind"], n_rows_read=e["n_rows_read"], **ctx)
    features.LEDGER.clear()


def _weights_by_truncation(prep, ids, bound, inclusive, pairs) -> tuple:
    """Second route to the same weights: physically cut each learner's date-sorted rows at the bound (searchsorted), then
    accumulate in a python dict with no bound test at all."""
    u, d, i, c = (prep.rows[x].to_numpy() for x in ("id_student", "date", "id_site", "sum_click"))
    starts = np.flatnonzero(np.r_[True, u[1:] != u[:-1]])
    ends = np.r_[starts[1:], len(u)]
    want = set(int(x) for x in ids)
    allowed = None if pairs is None else set(zip(pairs.id_student.tolist(), pairs.id_site.tolist()))
    acc: dict = {}
    for s, e in zip(starts, ends):
        uid = int(u[s])
        if uid not in want or uid not in bound.index:
            continue
        cut = s + int(np.searchsorted(d[s:e], bound.loc[uid], side="right" if inclusive else "left"))
        for j in range(s, cut):
            key = (uid, int(i[j]))
            if allowed is None or key in allowed:
                acc[key] = acc.get(key, 0) + int(c[j])
    keys = sorted(acc)
    return np.array(keys, dtype="<i8").reshape(-1, 2), np.array([acc[x] for x in keys], dtype="<i8")


def l9_hash_equivalence(log, prep, ids, bound, inclusive: bool, label: str, pairs=None, **ctx) -> None:
    """Independent check for L9 (the ledger is self-reported): weights from the bounded rows must hash equal to weights from
    rows truncated at the bound by a different code path. Any row dated after the bound that leaked in would differ."""
    w = features.clicks_from(features.bounded_rows(prep, ids, bound, inclusive, label + "/hash_check", pairs=pairs))
    features.LEDGER.pop()  # the check's own read is not a fitted object
    h1 = canon_hash(w[["id_student", "id_site"]].to_numpy(dtype="<i8"), w.clicks.to_numpy(dtype="<i8"))
    h2 = canon_hash(*_weights_by_truncation(prep, ids, bound, inclusive, pairs))
    log.measure("L9_hash_equivalence", int(h1 != h2), object=label, sha256_bounded=h1, sha256_truncated=h2, **ctx)


def l7_rebuild(log, prep, cond, ks=(), **ctx) -> None:
    """Section 6.1a: rebuild every registered learner-derived object in a FRESH process from data with the cold cohort's rows
    physically removed, hash inside that process, and require each hash to equal the one this process produced."""
    for m in CONFIG["builder_modules"]:
        importlib.import_module(m)
    fit = np.asarray(cond.fit_ids)
    here = features.build_all(features.as_view(prep), cond.name, fit, ks)  # this process still holds the cold rows
    view = {"pres": prep.pres, "item_ids": prep.item_ids, "pairs": prep.pairs[prep.pairs.id_student.isin(fit)],
            "rows": prep.rows[prep.rows.id_student.isin(fit)], "learners": prep.learners.loc[fit],
            "features": prep.features, "week_missing_share": prep.feature_constants["week_missing_share"]}
    payload = {"modules": CONFIG["builder_modules"], "cold_ids": cond.cold_ids, "fit_ids": fit, "name": cond.name, "ks": list(ks), "view": view}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    t0 = time.time()
    done = subprocess.run([sys.executable, str(CODE_DIR / "rebuild_worker.py")], input=pickle.dumps(payload), capture_output=True, env=env, cwd=str(CODE_DIR), timeout=3600)
    CHILD_SECONDS[0] += time.time() - t0
    if done.returncode != 0:
        raise LeakageError(f"L7 fresh-process rebuild failed: {done.stderr.decode('utf-8', 'replace')[-2000:]}")
    there = json.loads(done.stdout.decode("utf-8").strip().splitlines()[-1])
    log.measure("L7_cold_rows_in_worker_frames", there["n_cold_rows_in_worker"], **ctx)
    mismatched = [k for k in sorted(set(here) | set(there["hashes"])) if here.get(k) != there["hashes"].get(k)]
    for k in sorted(here):
        log.emit("l7_hash_pair", object=k, sha256_main=here[k], sha256_fresh=there["hashes"].get(k), equal=here[k] == there["hashes"].get(k), **ctx)
    log.measure("L7_rebuild_mismatch", len(mismatched), n_objects=len(here), mismatched=mismatched, **ctx)


def visible_checks(log, prep, vis, ids, k: int, **ctx) -> None:
    """Protocol 6.1 and section 13: the visible list is sorted ascending by first_date, is a subset of the learner's training
    pairs, has min(k, n_train) pairs, and every visible pair carries a positive bounded weight."""
    p, ids = vis.pairs, np.asarray(ids)
    unsorted = int(sum(0 if g.is_monotonic_increasing else 1 for _, g in p.groupby("id_student")["first_date"]))
    not_train = int((p.merge(prep.pairs, on=["id_student", "id_site"], suffixes=("", "_all")).role_all != TRAIN).sum())
    n_vis = p.groupby("id_student").size().reindex(ids, fill_value=0).to_numpy()
    wrong_n = int((n_vis != np.minimum(k, prep.learners.n_train.loc[ids].to_numpy())).sum())
    log.measure("V_SORTED", unsorted, k=k, **ctx)
    log.measure("V_SUBSET_OF_TRAIN", not_train, k=k, **ctx)
    log.measure("V_COUNT_MIN_K_NTRAIN", wrong_n, k=k, **ctx)
    log.measure("V_WEIGHT_MISSING", int((p.clicks.isna() | (p.clicks <= 0)).sum()), k=k, **ctx)

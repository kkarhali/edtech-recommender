"""One (presentation, condition, k) cell of the experiment: fit the six models (Random over the five declared seeds), score
the test split exactly once per model through models.score_test, and emit provenance (L2, L3, L7), L8, L9, A5 and the
parity counts. Part 3 (evaluate.py) calls `run_cell` and turns the returned scores into metrics.

Importing this module also registers the fresh-process rebuild builders for N_selection, C_selection, blend_model and
blend_standardiser (configs/experiments.json builder_modules), so L7 covers all seven learner-derived objects."""
from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

import numpy as np

import features
import leakage
import models
import provenance
from common import RANDOM_SEEDS, canon_hash
from splits import TEST, VAL, split_view


@dataclass
class CellResult:
    ids: np.ndarray  # scored learners, ascending
    scores: dict  # model key ("Random|42", "MostPop", ...) -> (n_learners, n_items) scores; rank with models.rank_lists
    excl: np.ndarray  # test-moment exclusion mask (M2 warm, M3 cold)
    truth: np.ndarray  # test ground-truth mask
    item_ids: np.ndarray
    info: dict  # N, blend counts, parity, feature shift: what chapter 3's appendix tables report
    extra: tuple | None = None  # P4b two-day learners: (ids, scores, excl, truth), scored by the same fitted models


def _sets(prep, mask, ids) -> dict:
    return {int(u): frozenset(prep.item_ids[row].tolist()) for u, row in zip(ids, mask)}


def run_cell(prep, cond, log, counter, length: float, pres_index: int, split: str, extra=None) -> CellResult:
    """cond: splits.Condition. length: courses.csv module_presentation_length. pres_index: position of the presentation in the
    sorted list of the 22 (Random's draw seed). split: the split this cell belongs to (primary/secondary/tertiary/P4a_3/P4a_10),
    carried into every log line and into L6's key so a deciding assertion can be told from a robustness one (G4 cycle-0 warning
    W3, blocker B2). Aborts through log.measure on any non-zero leakage count.

    log.provenance is cleared here, at the START of the cell, not at the end (G4 cycle-0 warning W2): otherwise the first cell
    of a run can satisfy provenance.coverage on foundation.verify's leftover records for the same (pres, condition, k) instead
    of its own."""
    log.provenance.clear()
    cell = {"pres": prep.pres, "condition": cond.name, "k": cond.k, "split": split}
    ctx = models.Ctx(prep, cond, length, pres_index)
    fitted = [models.Random(s) for s in RANDOM_SEEDS] + [models.MostPop(), models.PopWeek(), models.CBF(), models.ItemKNN(), models.Hybrid()]
    for m in fitted:
        m.fit(ctx)
    exp = None if cond.name == "B" else 0  # B fits on the cohort by design (optimistic); the count is emitted, not required zero
    for r in ctx.records:
        r = dict(r)
        provenance.emit(log, r, exp, check="L3" if r.pop("kind") == "constant" else "L2", **cell)
    provenance.coverage(log, provenance.SEVEN_OBJECTS, **cell)
    na = getattr(prep, "l9_training_na", False)
    seen = {}
    for m in fitted:  # L5: the split object each model actually holds, re-hashed per model
        seen.setdefault(id(m.ctx.view), split_view(m.ctx.view))
    leakage.l5(log, prep, {m.key: seen[id(m.ctx.view)] for m in fitted}, **cell)
    leakage.l9_flush(log, na_training=na, **cell)
    # validation-time exclusion actually applied (M1 warm, M3 cold), then the test-time history and exclusion (M2 warm, M3 cold)
    vh = ctx.valhist
    mv = "M3" if ctx.cold else "M1"
    leakage.l8(log, prep, mv, _sets(prep, vh.excl, vh.ids), vh.ids, VAL, k=cond.k, pres=prep.pres, condition=cond.name, split=split)
    ids = np.sort(cond.eval_ids)
    mt = "M3" if ctx.cold else "M2"
    h = models.make_history(prep, ids, ctx.cold, cond.k, mt, ctx.label + "/test")
    leakage.l8(log, prep, mt, _sets(prep, h.excl, h.ids), h.ids, TEST, k=cond.k, pres=prep.pres, condition=cond.name, split=split)
    leakage.l9_flush(log, na_training=na, **cell)
    truth = models.pair_mask(prep, ids, (TEST,))[0]
    scores = {m.key: models.score_test(m, h, counter, split, prep.pres, cond.name, cond.k) for m in fitted}  # each exactly once (L6)
    hyb = next(m for m in fitted if m.name == "Hybrid")
    info = {**ctx.info, "N": ctx.N, "n_test_learners": len(ids)}
    if not ctx.cold:  # warm: validation-time (M1) and test-time (M2) features differ only through the exclusion set; disclose
        # ctx.val_features has one row per learner in vh.ids (Ctx.sel_ids, the fitted learners WITH a validation pair); hyb.X has
        # one row per learner in h.ids (cond.eval_ids). These coincide on the primary, tertiary and P4a splits but not on the
        # secondary split, where a learner can keep a test pair with no validation pair (protocol 5.5) and so sits in h.ids only
        # (G4 cycle-0 blocker B1). Align by id_student and compare only learners present in both.
        common_ids, iv, ih = np.intersect1d(vh.ids, h.ids, assume_unique=True, return_indices=True)
        info["warm_feature_shift"] = {models_name: (float(np.abs(ctx.val_features[iv, c] - hyb.X[ih, c]).mean()) if len(common_ids) else None)
                                      for c, models_name in ((3, "cf_top1"), (4, "cf_top10_mass"), (5, "cbf_top1"), (6, "cbf_top10_mass"))}
        info["warm_feature_shift_n_learners_compared"] = int(len(common_ids))
        info["warm_feature_shift_n_val_only_or_eval_only"] = int(len(vh.ids) + len(h.ids) - 2 * len(common_ids))
    extra_out = None
    if extra is not None:
        # P4b two-day learners: never in prep, so never in cond.fit_ids or ctx.fit_ids and never a row of any fitted object of the
        # main run (similarity, MostPop/PopWeek counts, N, C, blend model and standardiser) — variants.two_day_view already builds
        # them from a separate view, so this is true by construction, one level stronger than protocol 12.1's wording requires.
        # They are scored here with the already-fitted models under 5.5's rule: bound d_2 (day 2), exclusion M2 with an empty
        # validation set (their day-1 pairs only).
        ids2 = np.sort(extra.learners.index.to_numpy())
        cond2 = cond.name + "+P4b"
        log.measure("P4B_TWO_DAY_LEARNERS_IN_FIT", len(np.intersect1d(ids2, ctx.fit_ids)), n_two_day=len(ids2), **cell)
        h2 = models.make_history(extra, ids2, ctx.cold, cond.k, mt, ctx.label + "/p4b")
        leakage.l8(log, extra, mt, _sets(extra, h2.excl, h2.ids), h2.ids, TEST, k=cond.k, pres=prep.pres, condition=cond2)
        leakage.l9_flush(log, **{**cell, "condition": cond2})
        h2.lidx = h2.lidx + 10 ** 6
        extra_out = (ids2, {m.key: models.score_test(m, h2, counter, split, prep.pres, cond2, cond.k) for m in fitted}, h2.excl, models.pair_mask(extra, ids2, (TEST,))[0])
    log.measure("A5", ctx.a5_bad, n_learner_rows_scaled=ctx.a5_rows, **cell)  # rows of another learner read for min-max bounds
    b = info.get("blend", {})
    counts = b.get("n_configurations", {})
    log.measure("PARITY_configurations_above_5", int(max(counts.values(), default=0) > 5), n_configurations=counts,
                n_label_grid_points=b.get("n_label_grid_points"), **cell)
    log.emit("cell_fit", **{k: v for k, v in info.items()}, **cell)
    return CellResult(ids, scores, h.excl, truth, prep.item_ids, info, extra_out)


_MEMO: dict = {}


def _ctx(view, cond) -> models.Ctx:
    """One fit per (view, condition, k): the four builders share it. The view is held only to pin its id."""
    key = (id(view), cond["name"], cond["k"], len(cond["fit_ids"]))
    if key not in _MEMO:
        _MEMO.clear()
        c = SimpleNamespace(name=cond["name"], k=cond["k"], fit_ids=cond["fit_ids"], cold_ids=np.array([], dtype="int64"))
        _MEMO[key] = (view, models.Ctx(view, c, 0.0, 0))
    return _MEMO[key][1]


def _b_N(view, cond) -> str:
    return canon_hash(np.array([models.N_GRID.index(_ctx(view, cond).N)], dtype="<i8"))


def _b_C(view, cond) -> str:
    C = _ctx(view, cond).blend.C
    return canon_hash(np.array([-1.0 if C is None else C], dtype="<f8"))


def _b_model(view, cond) -> str:
    return canon_hash(*_ctx(view, cond).blend.digest_arrays()[0])


def _b_std(view, cond) -> str:
    return canon_hash(*_ctx(view, cond).blend.digest_arrays()[1])


features.BUILDERS.update({"N_selection": (_b_N, True), "C_selection": (_b_C, True), "blend_model": (_b_model, True),
                          "blend_standardiser": (_b_std, True)})

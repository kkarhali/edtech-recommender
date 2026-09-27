"""Diagnostics stage (unit u13b_diag_code): the two additions the human approved after the main run, both explicitly
designed to decide no criterion. Neither touches the split, exclusion, bound or filter logic, any protocol number, or the
existing full Hybrid's fit and scores; both reuse the unmodified production code (splits.py, models.py, blend.py,
evaluate.cell_metrics) through the same Ctx a main-run cell would build.

D1 alpha logging: on condition A at k=2 (the "A|2" cold-start-refit cell), for every test-scored learner, the fitted
alpha models.Hybrid.score actually used (captured off Hybrid.alpha_, not recomputed), the learner id and k=2 (the cell's
visible-item count, constant per presentation). One record per learner per presentation, all 22 presentations, written to
results/run_artifacts/<unit>/alpha_log_<presentation>.jsonl.

D2 behavioural-signal ablation: models.HybridAblated (blend.blend_features/fit_blend with ablate=True; see blend.py) scored
on the warm cell and the A|2 cold-start cell, alongside (not instead of) the production Hybrid, for all 22 presentations,
using evaluate.cell_metrics -- the same metric code the main run uses -- so Precision@10 and every other cell metric are
computed identically for both models. Written to results/run_artifacts/<unit>/ablation_<presentation>.json.
"""
from __future__ import annotations

import json

import numpy as np

import data
import evaluate
import models
from common import _jsonable
from splits import TEST, build_prep, make_condition

COLD_NAME, COLD_K = "A", 2


def _ablation_cell(prep, cond, pres_index: int, types: np.ndarray, want_alpha: bool) -> tuple[dict, list[dict]]:
    """One (presentation, condition) cell for D2, and D1's alpha records when want_alpha (condition A, k=2 only). One Ctx,
    shared by the production Hybrid and the diagnostic HybridAblated, exactly as cell.run_cell shares one Ctx across every
    model of a main-run cell: same N, same similarity/CBF matrices, same exclusion moment, same fit_ids/eval_ids."""
    ctx = models.Ctx(prep, cond, 0.0, pres_index)  # length (course week window) is never read by Hybrid or its blend
    hyb, abl = models.Hybrid(), models.HybridAblated()
    for m in (hyb, abl):
        m.fit(ctx)
    ids = np.sort(cond.eval_ids)
    mt = "M3" if ctx.cold else "M2"
    h = models.make_history(prep, ids, ctx.cold, cond.k, mt, ctx.label + "/diagnostics")
    truth = models.pair_mask(prep, ids, (TEST,))[0]
    scores = {}
    for m in (hyb, abl):
        s = m.score(h)
        if s.shape != h.excl.shape or not np.isfinite(s).all():  # same guard as models.score_test
            raise ValueError(f"{m.key}: non-finite or mis-shaped diagnostic scores")
        scores[m.key] = s
    metrics, meta, *_ = evaluate.cell_metrics(scores, h.excl, truth, prep.item_ids, types)
    cell = {"condition": cond.name, "k": cond.k, **meta, "models": metrics}
    alpha_records = []
    if want_alpha:
        alpha_records = [{"presentation": prep.pres, "learner_id": int(u), "k": cond.k, "alpha": float(a)}
                          for u, a in zip(h.ids, hyb.alpha_)]
    return cell, alpha_records


def run(ctx) -> int:
    log, art = ctx["log"], ctx["artifact_dir"]
    oulad = data.load_oulad(log)
    all_names = sorted(oulad.rows)
    names = all_names
    if ctx["only"]:
        if ctx["only"] not in all_names:
            raise SystemExit(f"error: --only {ctx['only']} is not in this stage's matrix")
        names = [ctx["only"]]
    n_alpha_total = 0
    for pres_index, pres in enumerate(all_names):
        if pres not in names:
            continue
        prep = build_prep(oulad, pres, log)
        types = np.unique(prep.items.activity_type.to_numpy(), return_inverse=True)[1]
        cond_warm = make_condition(prep, "warm")
        cond_cold = make_condition(prep, COLD_NAME, COLD_K)
        warm_cell, _ = _ablation_cell(prep, cond_warm, pres_index, types, want_alpha=False)
        cold_cell, alpha_records = _ablation_cell(prep, cond_cold, pres_index, types, want_alpha=True)
        (art / f"alpha_log_{pres}.jsonl").write_text(
            "".join(json.dumps(r, default=_jsonable) + "\n" for r in alpha_records), encoding="utf-8")
        ablation = {"pres": pres, "cells": {"warm|None": warm_cell, f"{COLD_NAME}|{COLD_K}": cold_cell}}
        (art / f"ablation_{pres}.json").write_text(json.dumps(ablation, indent=1, default=_jsonable), encoding="utf-8")
        n_alpha_total += len(alpha_records)
        log.emit("diagnostics_presentation", pres=pres, n_alpha_records=len(alpha_records),
                 hybrid_p10_warm=warm_cell["models"]["Hybrid"]["P@10"]["mean"],
                 hybrid_ablated_p10_A2=cold_cell["models"]["Hybrid_ablated"]["P@10"]["mean"])
        del prep
    log.emit("diagnostics_done", n_presentations=len(names), n_alpha_records_total=n_alpha_total)
    return 0

"""Module C: metrics per cell, the identical-rankings guard, the statistics of protocol 10 and the verdicts of C1-C4 for the
main and iteration stages. main.py calls run_presentation(prep, ctx) once per presentation and finalize(ctx) once at the end.
ctx keys used: log, oulad, counter, artifact_dir (set by main.run_matrix); this module adds acc, c4, stats."""
from __future__ import annotations

import collections
import hashlib
import json
from itertools import combinations

import numpy as np
import scipy.stats as st

import behaviour
import cell as cellmod
import leakage
import models
import stats
import variants
from common import CONFIG, KS_COLD, _jsonable
from splits import build_prep, make_condition

MODELS = ("MostPop", "PopWeek", "CBF", "ItemKNN-CF", "Hybrid")
F3_PAIRS = (("Hybrid", "CBF"), ("Hybrid", "ItemKNN-CF"), ("Hybrid", "MostPop"), ("ItemKNN-CF", "CBF"), ("ItemKNN-CF", "MostPop"), ("CBF", "MostPop"))
STAT_CELLS = (("warm", None), ("A", 2))  # the cells that decide C1, C2, C3 (k = 2)
DISC = 1.0 / np.log2(np.arange(1, 21) + 1)  # binary-gain discount for positions 1..20
HP_OBJECTS = ("N_selection", "C_selection", "blend_model", "blend_standardiser")
# G4 cycle-1 warning W2, confirmed by reading models.Ctx.rec / .pairs_read and blend.fit_blend, not assumed: for all four of
# these, `read` is drawn from a subset of `sel_ids` (or `sel_ids[lab]`) restricted to role in (TRAIN, VAL), and `allowed_ids`
# passed to provenance.record is `fit_ids` with the same role filter; since sel_ids <= fit_ids, `read` is a subset of `allowed`
# by construction, so hp_outside_train_or_val below is structurally 0 and cannot fire -- it is not a real check for these four
# objects. It IS a real, non-trivial measurement for similarity_matrix and the other foundation objects, whose `read` frame is
# whatever bounded_rows actually returned. The real protection for a hyperparameter object reading a test row is L7 (the
# fresh-process rebuild), L8 (the exclusion-set equality) and L9 (the date-bound hash equivalence), not this count; chapter 5
# should cite those, not this field, as evidence for the blend.


def vector_metrics(H, nt) -> dict:
    """H: (L, 20) bool hit matrix of the ranked lists, nt: (L,) test-set sizes (> 0). Precision divides by K, MRR is @K, NDCG is
    binary with IDCG over min(K, |T|) positions (protocol 9). Cross-checked against metrics.py in tests/test_evaluate.py."""
    out = {}
    for K in (5, 10, 20):
        h = H[:, :K]
        hits = h.sum(1)
        first = np.where(h.any(1), h.argmax(1) + 1, 0)
        out[f"P@{K}"] = hits / K
        out[f"R@{K}"] = hits / nt
        out[f"HR@{K}"] = (hits > 0).astype(float)
        out[f"MRR@{K}"] = np.where(first > 0, 1.0 / np.maximum(first, 1), 0.0)
        out[f"NDCG@{K}"] = (h * DISC[:K]).sum(1) / np.cumsum(DISC)[np.minimum(K, nt) - 1]
    return out


def cell_metrics(scores, excl, truth, item_ids, types, want=()):
    """Per model: the 15 metrics (mean and median over learners with a non-empty test set), coverage@10, empty-list count and
    intra-list diversity@10 (mean pairwise Hamming distance over activity_type). Also a SHA256 of every model's full ranking."""
    n, nt = len(item_ids), truth.sum(1)
    has = nt > 0
    out, vec, hashes, orders = {}, {}, {}, {}
    for key, s in scores.items():
        pos, valid = models.top_positions(s, excl, n)  # full total order (score desc, id_site asc)
        hashes[key] = hashlib.sha256(np.ascontiguousarray(pos).tobytes()).hexdigest()
        if key in want:
            orders[key] = pos
        p20, v20 = pos[:, :20], valid[:, :20]
        vm = vector_metrics((np.take_along_axis(truth, p20, axis=1) & v20)[has], nt[has]) if has.any() else {}
        m = {k: {"mean": float(v.mean()), "median": float(np.median(v))} for k, v in vm.items()}
        t10, v10 = p20[:, :10], v20[:, :10]
        ty, pair = types[t10], v10[:, :, None] & v10[:, None, :] & ~np.eye(10, dtype=bool)
        m["coverage@10"] = float(len(np.unique(t10[v10])) / n)
        m["empty_lists"] = int((~v10.all(axis=1)).sum())
        m["diversity@10"] = float((((ty[:, :, None] != ty[:, None, :]) & pair).sum((1, 2)) / np.maximum(pair.sum((1, 2)), 1)).mean())
        out[key], vec[key] = m, vm.get("P@10")
    seeds = [k for k in out if k.startswith("Random|")]
    if seeds and has.any():
        out["Random"] = {met: {"mean_over_seeds": float(np.mean([out[s][met]["mean"] for s in seeds])),
                               "sd_over_seeds": float(np.std([out[s][met]["mean"] for s in seeds], ddof=1))} for met in out[seeds[0]] if isinstance(out[seeds[0]][met], dict)}
    ceiling = float(np.minimum(nt[has], 10).mean() / 10) if has.any() else None  # best attainable Precision@10 given |T(u)|
    meta = {"n_scored": int(len(excl)), "n_excluded_no_truth": int((~has).sum()), "ceiling_p10": ceiling,
            "share_learners_test_lt10": float((nt[has] < 10).mean()) if has.any() else None}
    return out, meta, vec, hashes, orders


def identical_guard(log, hashes: dict, prep, cname: str, k, **ctx) -> None:
    """Two different models with byte-identical full rankings for every learner stop the run (the phase 1 NaN bug looked like this).
    Expected identities are exempt and logged: at k = 0 CF, CBF and the hybrid all rank by id_site (8.0 iii) and PopWeek equals
    MostPop; PopWeek equals MostPop wherever every week field is missing (P5)."""
    exempt = set()
    if cname != "warm" and k == 0:
        exempt |= {frozenset(p) for p in combinations(("CBF", "ItemKNN-CF", "Hybrid"), 2)} | {frozenset(("MostPop", "PopWeek"))}
    if len(prep.feature_constants["all_missing_columns"]) == 2:
        exempt.add(frozenset(("MostPop", "PopWeek")))
    same = [(a, b) for a, b in combinations(sorted(hashes), 2) if hashes[a] == hashes[b]]
    bad = [p for p in same if frozenset(x.split("|")[0] for x in p) not in exempt]
    # log.flag, not log.measure (G4 cycle-0 warning W7): an unexempted tie CAN arise legitimately (a degenerate CBF profile, or a
    # cell where the fitted alpha is 1 for every learner), and losing a full 22-presentation run at its last cell over a
    # legitimate tie is a worse outcome than flagging it for investigation. Every occurrence is still written to the run log and
    # to `flags` in run_summary.json, so the signal the phase-1 NaN bug would have tripped is preserved, not silenced.
    log.flag("IDENTICAL_RANKINGS_PAIRS", len(bad), pairs=bad, exempt_identical=[p for p in same if p not in bad], condition=cname, k=k, **ctx)


def popularity_agreement(orders, excl, n) -> dict:
    """Kendall tau between the hybrid's and MostPop's full rankings over each learner's candidates, and the top-10 overlap."""
    L = len(excl)
    rk = {}
    for key in ("Hybrid", "MostPop"):
        rk[key] = np.zeros_like(orders[key])
        np.put_along_axis(rk[key], orders[key], np.broadcast_to(np.arange(n), (L, n)), axis=1)
    taus = [st.kendalltau(rk["Hybrid"][i][~excl[i]], rk["MostPop"][i][~excl[i]])[0] for i in range(L) if (~excl[i]).sum() > 2]
    taus = [t for t in taus if np.isfinite(t)]
    ov = float(np.mean([len(set(a) & set(b)) / 10 for a, b in zip(orders["Hybrid"][:, :10], orders["MostPop"][:, :10])]))
    return {"kendall_tau_mean": float(np.mean(taus)) if taus else None, "top10_overlap_mean": ov}


def stats_block(vec) -> dict:
    """Within one presentation and cell: bootstrap 95% intervals of each model's Precision@10, and the F3 family of paired
    per-learner Wilcoxon tests (Holm over 6) with rank-biserial effect size and the bootstrap interval of the paired difference.
    These are reported beside the deciding numbers and decide nothing."""
    V = np.stack([vec[m] for m in MODELS])
    B, ix = stats.bootstrap_means(V), {m: i for i, m in enumerate(MODELS)}
    f3 = {}
    for a, b in F3_PAIRS:
        f3[f"{a}-{b}"] = {"wilcoxon": stats.wilcoxon_paired(vec[a], vec[b]), "sign_test": stats.sign_test(vec[a], vec[b]),
                          "mean_diff": float(vec[a].mean() - vec[b].mean()), "diff_ci95": stats.ci95(B[ix[a]] - B[ix[b]])}
    for name, p in zip(f3, stats.holm([v["wilcoxon"]["p"] for v in f3.values()])):
        f3[name]["p_holm_F3"] = p
    return {"n_learners": int(V.shape[1]), "p10_ci95": {m: stats.ci95(B[ix[m]]) for m in MODELS}, "F3": f3}


def run_split(ctx, name: str, sp, plan, v2) -> dict:
    log, pres = ctx["log"], sp.pres
    log.emit("split_start", pres=pres, split=name, **{k: v for k, v in sp.counts.items() if not isinstance(v, dict)})
    c4 = ctx.setdefault("c4", collections.Counter())
    for key, v in leakage.l4(log, sp, pres=pres, split=name).items():
        c4[key] += v
    if name == "tertiary":
        log.emit("assert", id="L1", count=None, status="not_applicable", reason="random split interleaves time (protocol 5.3, 5.5)", pres=pres, split=name)
    else:
        leakage.l1(log, sp, require_all=(name != "secondary"), pres=pres, split=name)
    if name in ("secondary", "tertiary"):  # L7 fresh-process rebuild at k = 2 (the primary split is rebuilt at every k by foundation.verify)
        leakage.l7_rebuild(log, sp, make_condition(sp, "A", 2), (2,), pres=pres, split=name, condition="A")
    types = np.unique(sp.items.activity_type.to_numpy(), return_inverse=True)[1]
    out = {"counts": sp.counts, "cells": {}}
    for cname, k in plan:
        cond = make_condition(sp, cname, k)
        r = cellmod.run_cell(sp, cond, log, ctx["counter"], ctx["length"], ctx["pi"], name, extra=v2 if (name == "primary" and (cname, k) in STAT_CELLS) else None)
        # cell.run_cell already cleared log.provenance at ITS start (G4 cycle-0 warning W2), so everything here is this cell's own
        # records; the next cell's run_cell clears again before it runs, so nothing needs clearing on this side.
        for rec in log.provenance:  # C4: hyperparameter objects must read only allowed (training + validation) pairs
            if rec["object_name"] in HP_OBJECTS:
                c4["hp_records"] += 1
                c4["hp_outside_train_or_val"] += rec["n_rows_outside_allowed"]
        m, meta, vec, hashes, orders = cell_metrics(r.scores, r.excl, r.truth, r.item_ids, types, ("Hybrid", "MostPop") if (name == "primary" and cname == "A") else ())
        identical_guard(log, hashes, sp, cname, k, pres=pres, split=name)
        rec = {**meta, "models": m, "info": r.info}
        if orders:
            rec["popularity_agreement"] = popularity_agreement(orders, r.excl, len(r.item_ids))
        if name == "primary" and (cname, k) in STAT_CELLS:
            rec["stats"] = stats_block(vec)
        if r.extra is not None:  # P4b: the two-day learners alone, and pooled with this cell's evaluated learners
            m2, meta2, vec2, _, _ = cell_metrics(r.extra[1], r.extra[2], r.extra[3], r.item_ids, types)
            rec["p4b"] = {**meta2, "group_P@10": {x: m2[x]["P@10"]["mean"] for x in MODELS},
                          "union_P@10": {x: float((vec[x].sum() + vec2[x].sum()) / (len(vec[x]) + len(vec2[x]))) for x in MODELS}}
        out["cells"][f"{cname}|{k}"] = rec
        log.emit("cell_metrics", pres=pres, split=name, condition=cname, k=k, P10={x: round(m[x]["P@10"]["mean"], 4) for x in MODELS},
                 ceiling_p10=meta["ceiling_p10"], n_scored=meta["n_scored"], n_excluded_no_truth=meta["n_excluded_no_truth"])
    return out


def run_presentation(prep, ctx) -> None:
    oulad, log, pres = ctx["oulad"], ctx["log"], prep.pres
    ctx["length"], ctx["pi"] = oulad.length[pres], sorted(oulad.rows).index(pres)
    kr = CONFIG["k_robust"]
    full = [("warm", None)] + [("A", k) for k in KS_COLD] + [("A_robust", kr)] + [("B", k) for k in KS_COLD]
    v2 = variants.two_day_view(prep, oulad.rows[pres])
    if v2 is None:
        log.unchecked(f"P4b:{pres}", "no learner with >= 5 items and exactly two active days")
    res = {"pres": pres, "p4b_two_day_learners": 0 if v2 is None else int(len(v2.learners)), "splits": {}}
    res["splits"]["primary"] = run_split(ctx, "primary", prep, full, v2)
    res["splits"]["secondary"] = run_split(ctx, "secondary", variants.secondary(prep, oulad.rows[pres], log), full, None)
    res["splits"]["tertiary"] = run_split(ctx, "tertiary", variants.tertiary(prep), full, None)
    for th in (3, 10):  # P4a: primary split, warm slice and Condition A at k = 2 only
        res["splits"][f"P4a_{th}"] = run_split(ctx, f"P4a_{th}", build_prep(oulad, pres, log, min_items=th), [("warm", None), ("A", 2)], None)
    res["behaviour"] = behaviour.describe(prep)  # descriptive only; feeds no model
    ctx.setdefault("acc", {})[pres] = res
    (ctx["artifact_dir"] / f"results_{pres}.json").write_text(json.dumps(res, indent=1, default=_jsonable), encoding="utf-8")


def finalize(ctx) -> None:
    """L6, then C1-C4 across the presentations and the reporting tables (optimism, secondary reversal, P4a, P4b, per module)."""
    log, acc, counter = ctx["log"], ctx.get("acc", {}), ctx["counter"]
    counter.check(log)
    pres, c4, out, detail = sorted(acc), ctx.get("c4", {}), {}, {}
    full = len(pres) == 22

    def M(split, cell, model, met="P@10"):
        return {p: acc[p]["splits"][split]["cells"][cell]["models"][model][met]["mean"] for p in pres}

    for cid, cell, strict, thr in (("C1", "warm|None", False, 0.10), ("C2", "A|2", True, 0.0)):
        if not full:
            out[cid] = {"verdict": stats.UNCHECKED, "reason": f"defined over all 22 presentations; {len(pres)} were run", "values": {}}
            continue
        rows = stats.effect_family(M("primary", cell, "Hybrid"), {"vs_CBF": M("primary", cell, "CBF"), "vs_CF": M("primary", cell, "ItemKNN-CF")})
        v, why = stats.decide(rows, thr, strict)
        out[cid] = {"verdict": v, "reason": why, "values": rows}
        mods = sorted({p[:3] for p in pres})
        detail[f"{cid}_per_module"] = {mo: {b: float(np.median(stats.rel_gain([M("primary", cell, "Hybrid")[p] for p in pres if p[:3] == mo], [M("primary", cell, b2)[p] for p in pres if p[:3] == mo])[0]) or 0.0)
                                            for b, b2 in (("vs_CBF", "CBF"), ("vs_CF", "ItemKNN-CF"))} for mo in mods}
    if full:
        per = {}
        for p in pres:
            c = acc[p]["splits"]["primary"]["cells"]["A|2"]
            mm, d = c["models"], c["stats"]["F3"]
            e = {"hybrid": mm["Hybrid"]["P@10"]["mean"], "cbf": mm["CBF"]["P@10"]["mean"], "mostpop": mm["MostPop"]["P@10"]["mean"]}
            e.update(ge_cbf=e["hybrid"] >= e["cbf"], gt_mostpop=e["hybrid"] > e["mostpop"], empty_lists=mm["Hybrid"]["empty_lists"],
                     coverage10=mm["Hybrid"]["coverage@10"], ceiling_p10=c["ceiling_p10"], diff_vs_cbf_ci95=d["Hybrid-CBF"]["diff_ci95"],
                     diff_vs_mostpop_ci95=d["Hybrid-MostPop"]["diff_ci95"])
            e["all_conjuncts"] = bool(e["ge_cbf"] and e["gt_mostpop"] and e["empty_lists"] == 0 and e["coverage10"] >= 0.10)
            per[p] = e
        bad = [p for p in pres if not per[p]["all_conjuncts"]]
        out["C3"] = {"verdict": stats.MET if not bad else stats.NOT_MET, "reason": "all four conjuncts in each of the 22" if not bad else f"{len(bad)} presentations fail a conjunct",
                     "values": {"per_presentation": per, "failing": bad, "note": "a shortfall inside its bootstrap interval is still not met (10.5); cold-start P@10 of 0.02-0.03 is read against ceiling_p10, not as model failure"}}
        detail["F4_C3ab_as_C1C2"] = stats.effect_family(M("primary", "A|2", "Hybrid"), {"vs_CBF": M("primary", "A|2", "CBF"), "vs_MostPop": M("primary", "A|2", "MostPop")})
    else:
        out["C3"] = {"verdict": stats.UNCHECKED, "reason": f"defined over all 22 presentations; {len(pres)} were run", "values": {}}
    mx, hp = max(counter.n.values(), default=0), c4.get("hp_records", 0)
    ok = c4.get("val_test", 0) == 0 and c4.get("hp_outside_train_or_val", 0) == 0 and mx == 1
    out["C4"] = {"verdict": stats.UNCHECKED if hp == 0 or not counter.n else (stats.MET if ok else stats.NOT_MET),
                 "reason": "counted across every split and cell run", "values": {"val_test_shared_rows": c4.get("val_test", 0), "train_val_shared_rows": c4.get("train_val", 0),
                 "train_test_shared_rows": c4.get("train_test", 0), "hyperparameter_records": hp,
                 # what this counts, exactly (G4 cycle-0 warning W1): rows read by a hyperparameter object (N, C, the blend model,
                 # its standardiser) that lie outside that object's fitted learners' TRAIN-or-VAL pairs, i.e. a TEST row it should
                 # never have touched. It does not mean "read no training row" -- the blend must read training-side history to
                 # build its features, and plan.md C4's "fitted outside the validation split" is read as "leaked a test row".
                 "hyperparameter_rows_reading_test_data": c4.get("hp_outside_train_or_val", 0),
                 "max_test_scoring_count": mx, "n_scoring_cells": len(counter.n)}}

    def rg(split, cell, model, base):
        g = stats.rel_gain(list(M(split, cell, model).values()), list(M(split, cell, base).values()))[0]
        return float(np.median(g)) if len(g) else float("nan")

    def _optimism_diffs(m, k):
        return [acc[p]["splits"]["primary"]["cells"][f"B|{k}"]["models"][m]["P@10"]["mean"] - acc[p]["splits"]["primary"]["cells"][f"A|{k}"]["models"][m]["P@10"]["mean"] for p in pres]

    # G4 cycle-1 warning W6: min()/max() over an empty `pres` raise ValueError. finalize() cannot be reached with an empty `acc`
    # from main.run_matrix today (an abort re-raises before finalize, and a matrix always has >= 1 presentation), but a future
    # --only combination could reach here with acc empty; guard so a clean partial run cannot crash in the summary writer.
    detail["optimism_B_minus_A_P10"] = {m: {str(k): ({"median": float(np.median(d)), "min": float(min(d)), "max": float(max(d))} if (d := _optimism_diffs(m, k)) else
                                                      {"median": None, "min": None, "max": None, "note": "no presentations accumulated"})
                                              for k in KS_COLD} for m in MODELS}
    for split in ("secondary", "tertiary", "P4a_3", "P4a_10"):  # robustness / sensitivity: decide nothing (5.3a, 5.5, 12.1)
        detail[f"{split}_median_rel_gain"] = {cell: {b: rg(split, cell, "Hybrid", b2) for b, b2 in (("vs_CBF", "CBF"), ("vs_CF", "ItemKNN-CF"))}
                                              for cell in ("warm|None", "A|2")}
        detail[f"{split}_sign_reversal_vs_primary"] = {cell: {b: bool(np.sign(detail[f"{split}_median_rel_gain"][cell][b]) != np.sign(rg("primary", cell, "Hybrid", b2)))
                                                              for b, b2 in (("vs_CBF", "CBF"), ("vs_CF", "ItemKNN-CF"))} for cell in ("warm|None", "A|2")}
    detail["P4b_union_median_P10"] = {cell: {m: float(np.median([acc[p]["splits"]["primary"]["cells"][cell]["p4b"]["union_P@10"][m] for p in pres if "p4b" in acc[p]["splits"]["primary"]["cells"][cell]] or [np.nan])) for m in MODELS}
                                      for cell in ("warm|None", "A|2")}
    ctx["stats"] = out
    (ctx["artifact_dir"] / "results_summary.json").write_text(json.dumps({"presentations": pres, "criteria": out, "reporting": detail}, indent=1, default=_jsonable), encoding="utf-8")
    log.emit("finalize", presentations=len(pres), verdicts={c: v["verdict"] for c, v in out.items()})

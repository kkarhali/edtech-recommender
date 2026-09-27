"""Protocol section 10: paired Wilcoxon with the zero-difference rule, exact sign test, Holm, the undefined-ratio rule,
rank-biserial effect size and the bootstrap percentile interval. Verdict wording follows 10.2a item 3a and rule 6."""
from __future__ import annotations

import warnings

import numpy as np
import scipy.stats as st

from common import SEED

MET, NOT_MET, NOT_MET_UNCHECKED, UNCHECKED = "met", "not met", "not met (unchecked conjunct)", "unchecked"
MIN_EFFECTIVE_N = 6  # below this a two-sided exact Wilcoxon cannot reach p < 0.05: the conjunct is unchecked, not failed


def holm(ps: list) -> list:
    """Holm-adjusted p-values over a family whose size is len(ps); None (no test possible) stays None but keeps its slot."""
    m, idx = len(ps), sorted((i for i, p in enumerate(ps) if p is not None), key=lambda i: ps[i])
    out, run = [None] * m, 0.0
    for rank, i in enumerate(idx):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        out[i] = run
    return out


def wilcoxon_paired(x, y) -> dict:
    """zero_method='wilcox' (zero differences discarded), two-sided, no continuity correction, exact where scipy permits.
    The effective n after discarding is always reported."""
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    nz = d[d != 0]
    out = {"n_pairs": int(len(d)), "n_eff": int(len(nz)), "n_zero_dropped": int(len(d) - len(nz)),
           "median_diff": float(np.median(d)) if len(d) else None, "p": None, "method": None, "rank_biserial": None}
    if len(nz) == 0:
        return out
    r = st.rankdata(np.abs(nz))
    wp, wm = r[nz > 0].sum(), r[nz < 0].sum()
    out["rank_biserial"] = float((wp - wm) / (wp + wm))
    for method in (("exact", "approx") if len(nz) <= 50 else ("approx",)):  # exact is only tractable for small n
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                res = st.wilcoxon(nz, zero_method="wilcox", alternative="two-sided", correction=False, method=method)
            out.update(p=float(res.pvalue), method=method)
            break
        except Exception:  # scipy refuses exact in some tie situations: fall back and say so
            continue
    return out


def sign_test(x, y) -> dict:
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    nz = d[d != 0]
    pos = int((nz > 0).sum())
    return {"n_eff": int(len(nz)), "n_favouring_first": pos, "n_favouring_second": int(len(nz) - pos),
            "p": float(st.binomtest(pos, len(nz), 0.5, alternative="two-sided").pvalue) if len(nz) else None}


def rel_gain(h, b) -> tuple:
    """(h - b) / b over presentations with b > 0; a zero baseline is excluded and counted, never imputed or capped."""
    h, b = np.asarray(h, dtype=float), np.asarray(b, dtype=float)
    ok = b > 0
    return (h[ok] - b[ok]) / b[ok], int((~ok).sum())


def bootstrap_means(V, B: int = 10000, chunk: int = 500) -> np.ndarray:
    """Percentile-bootstrap resampled means over learners (columns) for every row of V, sharing resamples so paired
    differences are the differences of the returned means. default_rng(42), 10,000 resamples."""
    V = np.asarray(V, dtype=float)
    rng, n = np.random.default_rng(SEED), V.shape[1]
    out = np.empty((V.shape[0], B))
    for s in range(0, B, chunk):
        idx = rng.integers(0, n, size=(min(chunk, B - s), n))
        out[:, s:s + len(idx)] = V[:, idx].mean(axis=2)
    return out


def ci95(samples) -> list:
    return [float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))]


def effect_family(h: dict, bases: dict) -> dict:
    """h: presentation -> hybrid Precision@10; bases: name -> (presentation -> value). Median relative gain, the deciding
    Wilcoxon on paired absolute values, Holm over the family, and the sign-test companion, per baseline."""
    pres = sorted(h)
    hv = np.array([h[p] for p in pres])
    rows = {}
    for name, b in bases.items():
        bv = np.array([b[p] for p in pres])
        gains, n_excl = rel_gain(hv, bv)
        rows[name] = {"median_rel_gain": float(np.median(gains)) if len(gains) else None, "n_excluded_undefined_ratio": n_excl,
                      "n_presentations": len(pres), "wilcoxon": wilcoxon_paired(hv, bv), "sign_test": sign_test(hv, bv)}
    for name, p in zip(rows, holm([r["wilcoxon"]["p"] for r in rows.values()])):
        rows[name]["p_holm"] = p
    return rows


def decide(rows: dict, threshold: float, strict: bool) -> tuple:
    """Threshold conjunct (median relative gain against EVERY baseline) and test conjunct (Holm p < 0.05 against every
    baseline). A met threshold with an inconclusive test is 'not met (unchecked conjunct)', never 'met'."""
    gains = [r["median_rel_gain"] for r in rows.values()]
    if any(g is None for g in gains):
        return UNCHECKED, "a baseline is zero in every presentation: the median gain is undefined"
    if not all((g > threshold) if strict else (g >= threshold) for g in gains):
        return NOT_MET, "median relative gain below the threshold against at least one baseline"
    if any(r["wilcoxon"]["n_eff"] < MIN_EFFECTIVE_N or r["p_holm"] is None for r in rows.values()):
        return NOT_MET_UNCHECKED, f"threshold met; test inconclusive (effective n < {MIN_EFFECTIVE_N})"
    if all(r["p_holm"] < 0.05 for r in rows.values()):
        return MET, "threshold and Holm-corrected Wilcoxon both met"
    return NOT_MET, "threshold met but a Holm-corrected p >= 0.05"

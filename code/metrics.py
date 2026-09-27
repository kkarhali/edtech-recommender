"""Ranking and metrics (protocol 8.0 i and 9): one order for every model, and Precision, Recall, NDCG, HitRate and MRR
at K = 5, 10, 20 with binary relevance. Per-learner values first, then the macro mean over learners."""
from __future__ import annotations

import math

import numpy as np

from common import TOP_KS


def rank_topk(scores, item_ids, exclude, k: int) -> list:
    """Top-k ids by score descending then id_site ascending, scores rounded to 12 decimals, `exclude` removed first.
    Raises on any non-finite score (argsort over NaN returns index order and looks like a ranking)."""
    scores = np.asarray(scores, dtype=float)
    ids = np.asarray(item_ids)
    if scores.shape != ids.shape or not np.isfinite(scores).all():
        raise ValueError("scores must be finite and one per catalogue item")
    keep = ~np.isin(ids, np.fromiter(exclude, dtype=ids.dtype, count=len(exclude)))
    ids, scores = ids[keep], np.round(scores[keep], 12)
    order = np.lexsort((ids, -scores))  # last key is primary
    return ids[order][:k].tolist()


def precision_at_k(ranked, truth, k: int) -> float:
    return len(set(ranked[:k]) & set(truth)) / k  # always divided by K, even for a short list


def recall_at_k(ranked, truth, k: int) -> float:
    return len(set(ranked[:k]) & set(truth)) / len(truth)


def hitrate_at_k(ranked, truth, k: int) -> float:
    return 1.0 if set(ranked[:k]) & set(truth) else 0.0


def mrr_at_k(ranked, truth, k: int) -> float:
    for rank, item in enumerate(ranked[:k], start=1):
        if item in truth:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked, truth, k: int) -> float:
    dcg = sum(1.0 / math.log2(rank + 1) for rank, item in enumerate(ranked[:k], start=1) if item in truth)
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(k, len(truth)) + 1))
    return dcg / idcg


METRICS = {"precision": precision_at_k, "recall": recall_at_k, "ndcg": ndcg_at_k, "hitrate": hitrate_at_k, "mrr": mrr_at_k}


def learner_metrics(ranked, truth, ks=TOP_KS) -> dict:
    """All metrics for one learner; the caller must have removed learners with an empty truth set."""
    truth = set(truth)
    if not truth:
        raise ValueError("empty ground truth: exclude and count the learner instead of scoring it 0")
    return {f"{name}@{k}": fn(ranked, truth, k) for name, fn in METRICS.items() for k in ks}


def aggregate(rankings: dict, truths: dict, ks=TOP_KS) -> dict:
    """Macro mean and median over learners with a non-empty truth set; the excluded count is reported, never scored 0."""
    per = {u: learner_metrics(rankings[u], t, ks) for u, t in truths.items() if len(t) > 0}
    out = {"n_learners": len(per), "n_excluded_no_truth": len(truths) - len(per)}
    for key in (next(iter(per.values())) if per else {}):
        vals = np.array([m[key] for m in per.values()])
        out[key] = {"mean": float(vals.mean()), "median": float(np.median(vals))}
    return out


def coverage_at_k(rankings: dict, n_items: int, k: int = 10) -> float:
    return len({i for r in rankings.values() for i in r[:k]}) / n_items


def n_short_lists(rankings: dict, k: int = 10) -> int:
    return sum(1 for r in rankings.values() if len(r) < k)

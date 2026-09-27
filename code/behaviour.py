"""Module D: behaviour features and learner segmentation. DESCRIPTIVE ONLY: nothing here is imported by models, blend, cell,
features or the scoring path, and no result of it enters any model (checked by tests/test_evaluate.py).

The declared proxy for the dwell time OULAD does not record (protocol 3.2): click volume, distinct active days and the
day-ordered click sequence per learner. Features are read from the evaluated learners' rows without a bound because nothing is
predicted from them; they must never be used as a model input."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from common import SEED

N_SEGMENTS = 4  # plan.md does not name k; 4 is this module's default (recorded in the return notes)
FEATURES = ("click_volume", "n_items", "active_days", "n_first_days", "mean_gap_days_between_new_items", "clicks_per_active_day")


def behaviour_features(prep) -> pd.DataFrame:
    r, p = prep.rows, prep.pairs
    g = r.groupby("id_student")
    f = pd.DataFrame({"click_volume": g["sum_click"].sum(), "active_days": g["date"].nunique()})
    f["n_items"] = p.groupby("id_student").size()
    f["n_first_days"] = p.groupby("id_student")["first_date"].nunique()
    span = p.groupby("id_student")["first_date"].agg(lambda s: s.max() - s.min())  # sequence: spread of first-opening days
    f["mean_gap_days_between_new_items"] = span / np.maximum(f["n_items"] - 1, 1)
    f["clicks_per_active_day"] = f["click_volume"] / f["active_days"]
    return f[list(FEATURES)]


def segment_learners(f: pd.DataFrame, k: int = N_SEGMENTS) -> tuple:
    """KMeans(k, n_init=10, random_state=42) on z-scored log1p features. Returns (labels, summary)."""
    X = np.log1p(f.to_numpy(dtype=float))
    sd = X.std(0)
    Z = (X - X.mean(0)) / np.where(sd > 0, sd, 1.0)
    k = min(k, len(f))
    labels = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(Z)
    sil = float(silhouette_score(Z, labels, sample_size=min(1000, len(f)), random_state=SEED)) if k > 1 and len(set(labels)) > 1 else None
    means = f.assign(segment=labels).groupby("segment").mean()
    return labels, {"k": k, "sizes": np.bincount(labels, minlength=k).tolist(), "silhouette": sil, "segment_means": means.round(3).to_dict("index")}


def describe(prep) -> dict:
    """Per-presentation distribution of every feature plus the segmentation summary."""
    f = behaviour_features(prep)
    q = f.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    _, seg = segment_learners(f)
    return {"n_learners": len(f), "quantiles": {c: q[c].round(3).tolist() for c in f.columns}, "quantile_levels": [0.05, 0.25, 0.5, 0.75, 0.95],
            "mean": f.mean().round(3).to_dict(), "segmentation": seg}

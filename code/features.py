"""Module A, features: date-bounded click weights and active days (protocol 4), the cold-start visible history
(6.1), the engagement matrix and item-item cosine, exclusion sets (7.1) and the registry of learner-derived
objects that the fresh-process rebuild (6.1a) re-creates. Every weight is formed by `bounded_rows`."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from common import canon_hash
from splits import TRAIN, VAL, Prep

LEDGER: list[dict] = []  # one entry per bounded_rows call; leakage.l9_flush emits and measures every entry


@dataclass
class View:
    """The slice of a Prep that fitting code may read; the fresh-process rebuild constructs it without cold rows."""
    pres: str
    item_ids: np.ndarray
    pairs: pd.DataFrame
    rows: pd.DataFrame
    learners: pd.DataFrame
    features: np.ndarray | None = None  # catalogue-derived CBF item matrix (no learner row)
    week_missing_share: float = 0.0


@dataclass
class Visible:
    pairs: pd.DataFrame  # id_student, id_site, first_date, role, clicks (date-bounded, cold bound inclusive)
    bound: pd.Series  # id_student -> first_date of the k-th visible pair
    active_days: pd.Series  # id_student -> distinct dates on or before the bound


def bounded_rows(prep, ids, bound: pd.Series, inclusive: bool, label: str, pairs: pd.DataFrame | None = None) -> pd.DataFrame:
    """Rows of `ids` dated inside each learner's bound: date < t (training bound, strict) or date <= t (cold bound,
    inclusive). Optionally only rows of the given (learner, item) pairs. No weight is ever formed any other way."""
    r = prep.rows[prep.rows.id_student.isin(ids)]
    d, b = r.date.to_numpy(dtype=float), r.id_student.map(bound).to_numpy(dtype=float)
    read = r[(d <= b) if inclusive else (d < b)]  # a learner without a bound reads nothing (NaN compares False)
    if pairs is not None:
        read = read.merge(pairs[["id_student", "id_site"]].drop_duplicates(), on=["id_student", "id_site"], how="inner")
    rd, rb = read.date.to_numpy(dtype=float), read.id_student.map(bound).to_numpy(dtype=float)  # independent re-check of what was read
    late = int(((rd > rb) if inclusive else (rd >= rb)).sum())
    LEDGER.append({"object": label, "bound_kind": "cold" if inclusive else "training", "n_rows_read": int(len(read)),
                   "n_rows_at_or_after_bound": late})
    return read


def clicks_from(read: pd.DataFrame) -> pd.DataFrame:
    """clicks(u,i|t): an explicit sum over all rows of the pair (studentVle has duplicate learner-item-day rows)."""
    return read.groupby(["id_student", "id_site"], sort=True)["sum_click"].sum().rename("clicks").reset_index()


def active_days_from(read: pd.DataFrame) -> pd.Series:
    """active_days(u|t): distinct dates, never a row count."""
    return read.groupby("id_student", sort=True)["date"].nunique()


def training_bound(prep, ids) -> pd.Series:
    return prep.learners.val_start.loc[np.asarray(ids)]  # the learner's first validation day


def train_weights(prep, ids, label: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Training-bound weights for every training pair of `ids`; returns (clicks frame, rows read)."""
    read = bounded_rows(prep, ids, training_bound(prep, ids), False, label)
    return clicks_from(read), read


def visible_history(prep, ids, k: int, label: str) -> Visible:
    """The earliest k TRAINING pairs by (first_date, id_site), sorted explicitly here, weighted under the cold bound."""
    tr = prep.pairs[(prep.pairs.role == TRAIN) & prep.pairs.id_student.isin(ids)]
    tr = tr.sort_values(["id_student", "first_date", "id_site"], kind="stable")
    vis = tr.groupby("id_student", sort=True).head(k).reset_index(drop=True)
    bound = vis.groupby("id_student")["first_date"].max()  # the k-th visible pair's first_date
    w = clicks_from(bounded_rows(prep, ids, bound, True, label + "/clicks", pairs=vis))
    vis = vis.merge(w, on=["id_student", "id_site"], how="left")
    days = active_days_from(bounded_rows(prep, ids, bound, True, label + "/active_days"))
    return Visible(vis, bound, days)


def engagement_matrix(view, fit_ids, label: str = "engagement") -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """Learner x item matrix of training-bound clicks over `fit_ids` only (rows of other learners are never read)."""
    fit_ids = np.sort(np.asarray(fit_ids))
    w, read = train_weights(view, fit_ids, label)
    mat = np.zeros((len(fit_ids), len(view.item_ids)))
    mat[np.searchsorted(fit_ids, w.id_student.to_numpy()), np.searchsorted(view.item_ids, w.id_site.to_numpy())] = w.clicks.to_numpy()
    return mat, fit_ids, read


def gram_cosine(mat: np.ndarray) -> np.ndarray:
    """Item-item cosine. Click sums are integers, so the Gram matrix is exact in float64 whatever the BLAS summation
    order; that makes the fresh-process hash comparison bit-stable. Zero columns give 0, never NaN."""
    g = mat.T @ mat
    d = np.sqrt(np.diag(g))
    den = np.outer(d, d)
    sim = np.divide(g, den, out=np.zeros_like(g), where=den > 0)
    if not np.isfinite(sim).all():
        raise ValueError("non-finite similarity matrix")
    return sim


def mostpop_counts(view, fit_ids) -> tuple[np.ndarray, pd.DataFrame]:
    """Distinct training learners per item (protocol 8.0 iv); also returns the pairs read, for provenance."""
    pr = view.pairs[(view.pairs.role == TRAIN) & view.pairs.id_student.isin(np.asarray(fit_ids))]
    counts = np.bincount(np.searchsorted(view.item_ids, pr.id_site.to_numpy()), minlength=len(view.item_ids))
    return counts.astype("<i8"), pr


def exclusion_sets(prep, ids, moment: str, visible: Visible | None = None) -> dict:
    """The exclusion set of a prediction moment (7.1): M1 training; M2 training u validation; M3 the visible k pairs."""
    if moment == "M3":
        src = visible.pairs
    else:
        src = prep.pairs[prep.pairs.role.isin((TRAIN,) if moment == "M1" else (TRAIN, VAL)) & prep.pairs.id_student.isin(ids)]
    out = {int(u): frozenset() for u in ids}
    out.update({int(u): frozenset(g.tolist()) for u, g in src.groupby("id_student")["id_site"]})
    return out


def truth_sets(prep, ids, role: int) -> dict:
    src = prep.pairs[(prep.pairs.role == role) & prep.pairs.id_student.isin(ids)]
    out = {int(u): frozenset() for u in ids}
    out.update({int(u): frozenset(g.tolist()) for u, g in src.groupby("id_student")["id_site"]})
    return out


def _b_similarity(view, cond) -> str:
    mat, ids, _ = engagement_matrix(view, cond["fit_ids"], "rebuild/similarity")
    return canon_hash(ids.astype("<i8"), gram_cosine(mat).astype("<f8"))


def _b_counts(view, cond) -> str:
    return canon_hash(mostpop_counts(view, cond["fit_ids"])[0])


# object name -> (builder(view, cond) -> sha256 hex, depends_on_k). Parts 2 and 3 register N_selection,
# C_selection, blend_model and blend_standardiser here (via config builder_modules) so the fresh-process rebuild covers
# all seven learner-derived objects. PopWeek's fitted counts are the same distinct-learner counts; its week window is
# catalogue-derived (A3).
BUILDERS = {"similarity_matrix": (_b_similarity, False), "mostpop_counts": (_b_counts, False), "popweek_counts": (_b_counts, False)}


def build_all(view, name: str, fit_ids, ks) -> dict:
    out = {}
    for obj, (fn, k_dependent) in BUILDERS.items():
        for k in (list(ks) if k_dependent else [None]):
            out[f"{obj}|{k}"] = fn(view, {"name": name, "k": k, "fit_ids": np.asarray(fit_ids)})
    return out


def as_view(prep: Prep) -> View:
    return View(prep.pres, prep.item_ids, prep.pairs, prep.rows, prep.learners, prep.features, prep.feature_constants["week_missing_share"])


def week_missing_share(view) -> float:
    """One accessor for the P5 week-missing-share constant, for either a splits.Prep (feature_constants dict, used by every
    ordinary fit) or a features.View (its own float attribute, used only by the L7 fresh-process rebuild path in cell.py,
    which builds a View so a rename in one direction would break it — G4 cycle-1 blocker B2)."""
    if isinstance(view, View):
        return view.week_missing_share
    return view.feature_constants["week_missing_share"]


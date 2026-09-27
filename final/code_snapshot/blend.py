"""Protocol 8.1: the learned blend weight alpha(u), all eleven numbered points. Fitted on VALIDATION data of the fitted
learners only (M1 warm, M3 cold), refit per (presentation, condition, k), never on test data."""
from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

from common import SEED
from features import week_missing_share
from models import ALPHA_GRID, C_GRID, TRAIN, VAL, cbf_scores, cf_scores, precision10

FEATURE_NAMES = ("n_visible", "log1p_visible_clicks", "n_active_days", "cf_top1", "cf_top10_mass", "cbf_top1",
                 "cbf_top10_mass", "week_missing_share")  # step 3, fixed order
SHIFT_COLUMNS = (3, 4, 5, 6)  # the four features whose candidate set differs between M1 and M2 (disclosed shift, T29)
# D2 diagnostic only (human-approved, decides no criterion): the three learner-activity columns -- n_visible, log1p_visible_clicks
# (click-volume) and n_active_days (active-day) -- that models.HybridAblated drops via blend_features(..., ablate=True) /
# fit_blend(ctx, ablate=True). The production Hybrid never passes ablate=True, so this tuple is inert for the main run.
BEHAVIOURAL_COLUMNS = (0, 1, 2)
ABLATED_FEATURE_NAMES = tuple(n for i, n in enumerate(FEATURE_NAMES) if i not in BEHAVIOURAL_COLUMNS)


def blend_features(h, cfm, cbm, week_missing_share: float, ablate: bool = False) -> np.ndarray:
    """Step 3 / step 4: one construction for validation time and test time. cfm and cbm are the min-max scaled component
    scores over the learner's candidate set (the exclusion of the prediction moment).

    ablate=True is the D2 diagnostic only (models.HybridAblated): drops BEHAVIOURAL_COLUMNS from the returned matrix so the
    fit below never sees n_visible / log1p_visible_clicks / n_active_days. Default False, used by every other caller
    (models.Hybrid via fit_blend), reproduces the original 8-column matrix unchanged."""
    def top(x):
        t = np.sort(np.where(h.excl, -np.inf, x), axis=1)[:, ::-1][:, :10]
        t = np.where(np.isfinite(t), t, 0.0)
        return t[:, 0], t.sum(1)
    c1, cm = top(cfm)
    b1, bm = top(cbm)
    X = np.column_stack([h.n_vis, np.log1p(h.clicks), h.days, c1, cm, b1, bm, np.full(len(h.ids), week_missing_share)])
    if ablate:
        X = X[:, [i for i in range(X.shape[1]) if i not in BEHAVIOURAL_COLUMNS]]
    if not np.isfinite(X).all():
        raise ValueError("non-finite blend features")
    return X


def _z(X, mu, sd):  # step 5: a zero-variance feature is passed through as a constant zero
    return np.where(sd > 0, (X - mu) / np.where(sd > 0, sd, 1.0), 0.0)


def _make_lr(C):  # step 6: protocol 8.1 asks for penalty="l2"
    kw = dict(solver="lbfgs", tol=1e-4, max_iter=1000, fit_intercept=True, class_weight=None, random_state=SEED, C=C)
    try:
        # scikit-learn >= 1.8 (this project's 1.9.1 included) deprecated the `penalty` argument in favour of `l1_ratio`, and warns
        # on every fit if `penalty` is passed at all -- thousands of lines of runner noise over one run (G4 cycle-1 warning W4).
        # `l1_ratio=0.0` is L2 (`l1_ratio=1.0` would be L1), so this gets step 6's L2 penalty without passing the deprecated name.
        return LogisticRegression(l1_ratio=0.0, **kw)
    except TypeError:  # l1_ratio not yet introduced on an older scikit-learn: penalty="l2" is that version's spelling of L2
        return LogisticRegression(penalty="l2", **kw)


def _proba(lr, Z):  # step 7: alpha = P(y = 1 | x), no clipping
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        return lr.predict_proba(Z)[:, list(lr.classes_).index(1)]


@dataclass
class Blend:
    kind: str  # "lr" or "constant"
    const: float = 0.5
    mu: np.ndarray | None = None
    sd: np.ndarray | None = None
    lr: object = None
    C: float | None = None
    c_status: str = "n/a"

    def alpha(self, X) -> np.ndarray:
        if self.kind == "constant":
            return np.full(len(X), self.const)
        a = _proba(self.lr, _z(X, self.mu, self.sd))
        if not ((a >= 0) & (a <= 1)).all():
            raise ValueError("alpha outside [0, 1]")
        return a

    def digest_arrays(self) -> tuple:
        """(model arrays, standardiser arrays), rounded to 10 decimals, for the fresh-process hash comparison."""
        r = lambda x: np.round(np.asarray(x, dtype="<f8"), 10)  # noqa: E731
        if self.kind == "constant":
            return (r([self.const]), r([])), (r([]), r([]))
        return (r(np.r_[self.lr.coef_.ravel(), self.lr.intercept_, -1.0 if self.C is None else self.C]), r([])), (r(self.mu), r(self.sd))


def fit_blend(ctx, ablate: bool = False) -> Blend:
    """Steps 1-11 for one (presentation, condition, k). Emits its provenance records through ctx and its counts in ctx.info.

    ablate=True is the D2 diagnostic only (models.HybridAblated / Ctx.blend_ablated): the same eleven steps over
    blend_features(..., ablate=True)'s reduced matrix, sharing the split, seed, exclusion moment, N and the C-selection
    procedure with the production fit (all read off `ctx` unchanged), but writing to ctx.info["blend_ablated"] instead of
    ctx.info["blend"] and skipping ctx.val_features / ctx.rec so this diagnostic path never touches the production fit's
    cached features or provenance records, even when both share one Ctx (models.Ctx.blend and .blend_ablated are cached
    separately). Default False, used by every other caller, executes exactly the original statements in the original order."""
    h, truth, view = ctx.valhist, ctx.val_truth, ctx.view
    cfm = ctx.scale(cf_scores(h.H, ctx.sim_n(ctx.N)), h.excl)  # step 9: inherits N from ItemKNN-CF
    cbm = ctx.scale(cbf_scores(h.H, ctx.Vn, view.features), h.excl)
    X = blend_features(h, cfm, cbm, week_missing_share(view), ablate=ablate)  # step 4: validation-time features
    if not ablate:
        ctx.val_features = X
    # step 2: learner-level target from the 11-point label grid, on validation items, exclusion of the validation moment
    P = np.stack([precision10(a * cfm + (1 - a) * cbm, h.excl, truth) for a in ALPHA_GRID], axis=1)
    mx = P.max(axis=1)
    astar = np.array([np.median(np.array(ALPHA_GRID)[P[i] == mx[i]]) for i in range(len(P))])
    labelled = mx > 0  # all-zero learners are dropped from the fit, not labelled (still scored at test time)
    y = (astar >= 0.5).astype(int)
    lab = np.flatnonzero(labelled)
    yl, n1 = y[lab], int((y[lab] == 1).sum())
    n0 = len(lab) - n1
    info = {"n_validation_learners": len(P), "n_labelled": len(lab), "n_dropped_all_zero": int((~labelled).sum()),
            "share_dropped_all_zero": float((~labelled).mean()), "n_label_grid_points": len(ALPHA_GRID),
            "n_configurations": {"ItemKNN-CF": 5, "Hybrid": 0, "CBF": 0, "MostPop": 0, "PopWeek": 0, "Random": 0}, "n_y1": n1, "n_y0": n0}
    if ablate:
        info["ablated_feature_names"] = list(ABLATED_FEATURE_NAMES)
    used = ctx.sel_ids[lab]
    if len(lab) < 20 or n1 == 0 or n0 == 0:  # steps 2 and 10: no fit possible, alpha is a constant
        b = Blend("constant", float(np.median(astar[lab])) if len(lab) else 0.5)
        info["alpha_model"] = "constant"
    else:
        Xl = X[lab]
        info["alpha_model"] = "lr"
        if min(n1, n0) < 10:  # step 10: stratified 5-fold impossible
            C, info["C_selection"] = 1.0, "skipped"
        else:  # step 8: C by stratified 5-fold CV within the labelled validation learners, standardiser refitted per fold
            folds = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED).split(lab, yl))
            best, bestm, info["C_cv_precision10"] = None, -1.0, {}
            for C_ in C_GRID:
                fm = []
                for tr, te in folds:
                    mu, sd = Xl[tr].mean(0), Xl[tr].std(0)
                    lr = _make_lr(C_).fit(_z(Xl[tr], mu, sd), yl[tr])
                    a = _proba(lr, _z(Xl[te], mu, sd))
                    r = lab[te]
                    fm.append(precision10(a[:, None] * cfm[r] + (1 - a)[:, None] * cbm[r], h.excl[r], truth[r]).mean())
                info["C_cv_precision10"][str(C_)] = float(np.mean(fm))
                if np.mean(fm) > bestm:  # strict: ties go to the smaller C (grid is ascending)
                    best, bestm = C_, float(np.mean(fm))
            C, info["C_selection"] = best, "cv"
            info["n_configurations"]["Hybrid"] = len(C_GRID)
        mu, sd = Xl.mean(0), Xl.std(0)  # final standardiser: all labelled validation rows
        b = Blend("lr", 0.5, mu, sd, _make_lr(C).fit(_z(Xl, mu, sd), yl), float(C), info["C_selection"])
    read = ctx.pairs_read(used, (TRAIN, VAL))
    if not ablate:
        ctx.rec("C_selection", read, (TRAIN, VAL))
        ctx.rec("blend_model", read, (TRAIN, VAL))
        ctx.rec("blend_standardiser", read, (TRAIN, VAL))
    ctx.info["blend_ablated" if ablate else "blend"] = info
    return b

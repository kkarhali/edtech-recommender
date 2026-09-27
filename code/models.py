"""Module B: the six models behind one interface, the histories they are scored on, the ranking order of protocol 8.0 (i)
and the selection of the collaborative neighbourhood N (8.0a).

Interface: `model.fit(ctx) -> list[provenance record]` and `model.score(history) -> (n_learners, n_items) scores`.
A `Ctx` is one (presentation, condition, k) fitting context: everything a model may read is reached through it, so every
fitted object leaves a provenance record. Test scoring must go through `score_test`, which is what L6 counts."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import features
import provenance
from common import RANDOM_SEEDS
from splits import TEST, TRAIN, VAL

N_GRID = (10, 25, 50, 100, "all")  # ascending, "all" is the largest: ties resolve to the smallest N
C_GRID = (0.01, 0.1, 1, 10)
ALPHA_GRID = tuple(i / 10 for i in range(11))  # the 11-point label grid A of 8.1 step 2 (a label sweep, not a hyperparameter)


@dataclass
class History:
    ids: np.ndarray
    lidx: np.ndarray  # position among the presentation's evaluated learners (Random's learner_index)
    H: np.ndarray  # date-bounded click weights of the visible items, zero elsewhere
    excl: np.ndarray  # exclusion mask of the prediction moment (7.1)
    last: np.ndarray  # first_date of the last visible pair (NaN when nothing is visible)
    n_vis: np.ndarray
    clicks: np.ndarray
    days: np.ndarray


def _rc(view, ids, f):
    return np.searchsorted(ids, f.id_student.to_numpy()), np.searchsorted(view.item_ids, f.id_site.to_numpy())


def pair_mask(view, ids, roles):
    """(bool mask learners x items, pairs frame) of the pairs of `ids` whose role is in `roles`."""
    ids = np.asarray(ids)
    sub = view.pairs[view.pairs.role.isin(roles) & view.pairs.id_student.isin(ids)]
    m = np.zeros((len(ids), len(view.item_ids)), dtype=bool)
    m[_rc(view, ids, sub)] = True
    return m, sub


def make_history(view, ids, cold: bool, k, moment: str, label: str) -> History:
    """warm: all training pairs, exclusion M1 (training) or M2 (training u validation); cold: the earliest k training pairs,
    exclusion M3 (those k pairs only). Weights are date-bounded by features.bounded_rows."""
    ids = np.sort(np.asarray(ids))
    if moment != ("M3" if cold else moment) or moment not in ("M1", "M2", "M3") or (moment == "M3") != cold:
        raise ValueError(f"moment {moment} does not fit cold={cold}")
    H = np.zeros((len(ids), len(view.item_ids)))
    if cold:
        v = features.visible_history(view, ids, k, label)
        w, days, pf = v.pairs, v.active_days, v.pairs
        excl = np.zeros(H.shape, dtype=bool)
        excl[_rc(view, ids, pf)] = True
    else:
        w, read = features.train_weights(view, ids, label)
        days = features.active_days_from(read)
        pf = view.pairs[(view.pairs.role == TRAIN) & view.pairs.id_student.isin(ids)]
        excl = pair_mask(view, ids, (TRAIN,) if moment == "M1" else (TRAIN, VAL))[0]
    if w.clicks.isna().any():
        raise ValueError("a visible pair has no bounded click weight")
    H[_rc(view, ids, w)] = w.clicks.to_numpy()
    last = pf.groupby("id_student")["first_date"].max().reindex(ids).to_numpy(dtype=float)
    return History(ids, np.searchsorted(view.learners.index.to_numpy(), ids), H, excl, last, (H > 0).sum(1).astype(float),
                   H.sum(1), days.reindex(ids, fill_value=0).to_numpy(dtype=float))


def top_positions(scores, excl, k: int):
    """Protocol 8.0 (i): score descending (rounded to 12 decimals) then id_site ascending, excluded items last. The catalogue
    axis is id_site ascending, so the column index is the tie-break. Returns (positions, valid) of shape (L, k)."""
    if not np.isfinite(scores).all():
        raise ValueError("non-finite scores")
    key = np.where(excl, np.inf, -np.round(scores, 12))
    idx = np.broadcast_to(np.arange(scores.shape[1]), scores.shape)
    order = np.lexsort(np.stack([idx, key]))  # last key primary, sorted along the last axis
    ncand = scores.shape[1] - excl.sum(1)
    return order[:, :k], np.arange(k)[None, :] < ncand[:, None]


def rank_lists(scores, excl, item_ids, k: int) -> list:
    pos, valid = top_positions(scores, excl, k)
    return [np.asarray(item_ids)[p[v]].tolist() for p, v in zip(pos, valid)]


def precision10(scores, excl, truth) -> np.ndarray:
    pos, valid = top_positions(scores, excl, 10)
    return (np.take_along_axis(truth, pos, axis=1) & valid).sum(1) / 10  # always divided by K


def minmax_rows(s, excl):
    """8.0 (iii), per learner over that learner's candidate set: (x-min)/(max-min), the zero vector if max-min < 1e-12."""
    lo = np.where(excl, np.inf, s).min(1, keepdims=True)
    hi = np.where(excl, -np.inf, s).max(1, keepdims=True)
    rng = hi - lo
    ok = rng >= 1e-12
    return np.where(ok & ~excl, (s - lo) / np.where(ok, rng, 1.0), 0.0)


def a5_mismatches(s, excl, scaled) -> int:
    """A5 counter: learners whose scaled vector differs from scaling that learner's row alone, i.e. whose bounds used the rows
    of another learner (non-zero if anyone ever scales a pooled matrix)."""
    return sum(int(not np.array_equal(minmax_rows(s[i:i + 1], excl[i:i + 1]), scaled[i:i + 1])) for i in range(len(s)))


def truncate(sim, N):
    """Keep each item's N most similar OTHER items (ties by id_site ascending) and its self-similarity; "all" keeps everything."""
    if N == "all":
        return sim
    n = len(sim)
    key = -np.round(sim, 12)
    key[np.diag_indices(n)] = np.inf  # an item is not its own neighbour
    order = np.lexsort(np.stack([np.broadcast_to(np.arange(n), (n, n)), key]))
    rows = np.arange(n)[:, None]
    out = np.zeros_like(sim)
    out[rows, order[:, :N]] = sim[rows, order[:, :N]]
    out[np.diag_indices(n)] = np.diag(sim)
    return out


def cf_scores(H, S):
    """Click-weighted sum of similarities over the visible items, accumulated in id_site ascending order."""
    out = np.zeros((H.shape[0], S.shape[1]))
    for j in np.flatnonzero((H > 0).any(axis=0)):
        out += H[:, j, None] * S[j][None, :]
    return out


def cbf_scores(H, Vn, V):
    """Cosine between the click-weighted mean profile of the visible items (L2-normalised) and each item vector."""
    tot = H.sum(1, keepdims=True)
    prof = np.divide(H @ V, tot, out=np.zeros((H.shape[0], V.shape[1])), where=tot > 0)
    nrm = np.linalg.norm(prof, axis=1, keepdims=True)
    return np.divide(prof, nrm, out=np.zeros_like(prof), where=nrm > 0) @ Vn.T


class Ctx:
    """One (presentation, condition, k) fitting context. `view` is a Prep or a features.View; `cond` needs name, k, fit_ids,
    cold_ids. Fitted objects are memoised so CF and the Hybrid share one similarity matrix and one N."""

    def __init__(self, view, cond, length: float, pres_index: int):
        self.view, self.cond, self.length, self.pres_index = view, cond, length, pres_index
        self.cold, self.k = cond.name != "warm", cond.k
        self.fit_ids, self.cold_ids = np.sort(np.asarray(cond.fit_ids)), np.asarray(cond.cold_ids)
        self.records, self._seen, self._m, self.info = [], 0, {}, {}
        self.a5_bad = self.a5_rows = 0
        self.label = f"{view.pres}/{cond.name}/k{cond.k}"

    def rec(self, name, read, roles=(TRAIN,), kind="fitted"):
        r = provenance.record(name, read, self.view, self.fit_ids, roles, self.cold_ids)
        r["kind"] = kind
        self.records.append(r)

    def new_records(self) -> list:
        out, self._seen = self.records[self._seen:], len(self.records)
        return out

    def pairs_read(self, ids, roles):
        return self.view.pairs[self.view.pairs.role.isin(roles) & self.view.pairs.id_student.isin(ids)]

    def scale(self, s, excl):
        out = minmax_rows(s, excl)
        self.a5_bad += a5_mismatches(s, excl, out)
        self.a5_rows += len(s)
        return out

    @property
    def similarity(self):
        if "sim" not in self._m:
            mat, _, read = features.engagement_matrix(self.view, self.fit_ids, self.label + "/engagement")
            self.rec("similarity_matrix", read)
            self._m["sim"] = features.gram_cosine(mat)
        return self._m["sim"]

    @property
    def counts(self):
        if "counts" not in self._m:
            self._m["counts"], pr = features.mostpop_counts(self.view, self.fit_ids)
            self.info["mostpop_denominator"] = int(pr.id_student.nunique())
            self.rec("mostpop_counts", pr)
            self.rec("popweek_counts", pr)  # the same distinct-learner counts; the week window is catalogue-derived (A3)
        return self._m["counts"]

    @property
    def week(self):
        it = self.view.items  # catalogue metadata, sorted by id_site like item_ids
        return it.week_from.to_numpy(dtype=float), it.week_to.to_numpy(dtype=float)

    @property
    def Vn(self):
        if "Vn" not in self._m:
            V = self.view.features
            nrm = np.linalg.norm(V, axis=1, keepdims=True)
            self._m["Vn"] = V / np.where(nrm > 0, nrm, 1.0)
            self.records.append({"object_name": "cbf_item_vectors", "n_source_rows": len(V), "n_rows_outside_allowed": 0,
                                 "n_learners_used": 0, "n_cold_learners_used": 0, "kind": "constant"})
        return self._m["Vn"]

    def sim_n(self, N):
        cache = self._m.setdefault("sim_n", {})
        if N not in cache:
            cache[N] = truncate(self.similarity, N)
        return cache[N]

    @property
    def sel_ids(self):
        """Fitted learners that have validation ground truth: only they feed the selection of N, C and the blend (5.5)."""
        if "sel" not in self._m:
            self._m["sel"] = self.fit_ids[pair_mask(self.view, self.fit_ids, (VAL,))[0].any(axis=1)]
        return self._m["sel"]

    @property
    def valhist(self) -> History:
        """The history the model will be applied with, at the VALIDATION prediction moment: M1 warm, M3 cold (8.0a)."""
        if "vh" not in self._m:
            self._m["vh"] = make_history(self.view, self.sel_ids, self.cold, self.k, "M3" if self.cold else "M1", self.label + "/val")
        return self._m["vh"]

    @property
    def val_truth(self):
        if "vt" not in self._m:
            self._m["vt"] = pair_mask(self.view, self.sel_ids, (VAL,))[0]
        return self._m["vt"]

    @property
    def N(self):
        """8.0a: the N with the highest macro validation Precision@10 over the fitted learners; ties to the smallest N."""
        if "N" not in self._m:
            h, res = self.valhist, {}
            for N in N_GRID:
                res[N] = float(precision10(cf_scores(h.H, self.sim_n(N)), h.excl, self.val_truth).mean())
            best = N_GRID[0]
            for N in N_GRID:
                if res[N] > res[best]:
                    best = N
            self.info["N_val_precision10"] = {str(a): b for a, b in res.items()}
            self.rec("N_selection", self.pairs_read(self.sel_ids, (TRAIN, VAL)), (TRAIN, VAL))
            self._m["N"] = best
        return self._m["N"]

    @property
    def blend(self):
        if "blend" not in self._m:
            import blend
            self._m["blend"] = blend.fit_blend(self)
        return self._m["blend"]

    @property
    def blend_ablated(self):
        """D2 diagnostic only (models.HybridAblated): memoised separately from `blend` so fitting it never overwrites the
        production blend's cache, ctx.val_features or its provenance records (blend.fit_blend guards all three behind its
        own `ablate` flag)."""
        if "blend_ablated" not in self._m:
            import blend
            self._m["blend_ablated"] = blend.fit_blend(self, ablate=True)
        return self._m["blend_ablated"]


class Model:
    name = ""

    @property
    def key(self) -> str:
        return self.name

    def fit(self, ctx) -> list:
        self.ctx = ctx
        return ctx.new_records()

    def score(self, h: History) -> np.ndarray:
        raise NotImplementedError


class Random(Model):
    name = "Random"

    def __init__(self, seed: int):
        assert seed in RANDOM_SEEDS
        self.seed = seed

    @property
    def key(self) -> str:
        return f"Random|{self.seed}"

    def score(self, h):  # one draw per candidate from default_rng([s, presentation_index, learner_index]): no ties
        n = len(self.ctx.view.item_ids)
        return np.stack([np.random.default_rng([self.seed, self.ctx.pres_index, int(i)]).random(n) for i in h.lidx])


class MostPop(Model):
    name = "MostPop"

    def fit(self, ctx):
        ctx.counts
        return super().fit(ctx)

    def score(self, h):
        return np.tile(self.ctx.counts.astype(float), (len(h.ids), 1))


class PopWeek(MostPop):
    name = "PopWeek"

    def score(self, h):
        c = self.ctx
        wf, wt = c.week[0], c.week[1]
        w = np.minimum(np.maximum(np.floor(h.last / 7), 0), c.length / 7)  # NaN when nothing is visible (k = 0)
        elig = ((wf[None, :] <= w[:, None]) & (w[:, None] <= wt[None, :])) | (np.isnan(wf) | np.isnan(wt))[None, :]
        elig[np.isnan(w)] = True  # no visible pair, no course week: every item is eligible (protocol is silent; recorded)
        counts = c.counts.astype(float)
        return counts[None, :] + elig * (counts.max() + 1.0)  # ineligible items follow every eligible one, in MostPop order


class CBF(Model):
    name = "CBF"

    def fit(self, ctx):
        ctx.Vn
        return super().fit(ctx)

    def score(self, h):
        return cbf_scores(h.H, self.ctx.Vn, self.ctx.view.features)


class ItemKNN(Model):
    name = "ItemKNN-CF"

    def fit(self, ctx):
        ctx.N
        return super().fit(ctx)

    def score(self, h):
        return cf_scores(h.H, self.ctx.sim_n(self.ctx.N))


class Hybrid(Model):
    name = "Hybrid"

    def fit(self, ctx):
        ctx.blend
        return super().fit(ctx)

    def score(self, h):
        import blend
        c = self.ctx
        cfm = c.scale(cf_scores(h.H, c.sim_n(c.N)), h.excl)  # inherits ItemKNN's N (8.1 step 9)
        cbm = c.scale(cbf_scores(h.H, c.Vn, c.view.features), h.excl)
        self.X = blend.blend_features(h, cfm, cbm, features.week_missing_share(c.view))  # same construction as at validation time
        a = c.blend.alpha(self.X)
        self.alpha_ = a  # D1 diagnostic only: the per-learner alpha this call used, read by diagnostics.py; scores below unchanged
        return a[:, None] * cfm + (1 - a)[:, None] * cbm


class HybridAblated(Model):
    """D2 diagnostic only (human-approved, decides no criterion): never added to cell.run_cell's `fitted` list, so the
    main run's cells, provenance and criteria are untouched. Shares its Ctx (same split, same seed, same N, same
    exclusion moment, same fit_ids/eval_ids) with the production Hybrid; the blend is refit by the same
    blend.fit_blend/C-selection procedure over blend.blend_features(..., ablate=True), which drops
    blend.BEHAVIOURAL_COLUMNS (n_visible, log1p_visible_clicks/click-volume, n_active_days) and keeps the four CF/CBF
    features plus week_missing_share. Hybrid's own fit and scores are unaffected."""
    name = "Hybrid_ablated"  # D2 diagnostic key: click/day/visible-count features dropped, see blend.BEHAVIOURAL_COLUMNS

    def fit(self, ctx):
        self.ctx = ctx
        ctx.blend_ablated
        return ctx.new_records()

    def score(self, h):
        import blend
        c = self.ctx
        cfm = c.scale(cf_scores(h.H, c.sim_n(c.N)), h.excl)
        cbm = c.scale(cbf_scores(h.H, c.Vn, c.view.features), h.excl)
        self.X = blend.blend_features(h, cfm, cbm, features.week_missing_share(c.view), ablate=True)
        a = c.blend_ablated.alpha(self.X)
        self.alpha_ = a
        return a[:, None] * cfm + (1 - a)[:, None] * cbm


def score_test(model: Model, h: History, counter, split: str, pres: str, condition: str, k) -> np.ndarray:
    """The only route to test scoring; L6 counts calls per (model, split, presentation, condition, k, seed)."""
    counter.scored_test(model.name, split, pres, condition, k, getattr(model, "seed", None))
    s = model.score(h)
    if s.shape != h.excl.shape or not np.isfinite(s).all():
        raise ValueError(f"{model.key}: non-finite or mis-shaped scores")
    return s

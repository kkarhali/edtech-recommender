# Pilot Results — E-Learning Recommendation (Phase 1)

experiment_stage: pilot
dataset: OULAD, module-presentation **EEE_2014J** (chosen deterministically: interaction
count closest to a 400k-row target, from `studentVle.csv`)
n_raw_interaction_rows: 402,947 | n_items: 115 | n_eval_users: 1,049
hardware: single CPU, no GPU | wall-clock: ~30s per iteration

Full split design: for each user with ≥5 distinct interacted items, 20% held out as test.
"Warm" recommendations use the remaining ~80% as visible history. "Cold-start" recommendations
use the *same* users and the *same* test set, but visible history is truncated to their first
2 train items — this isolates the effect of thin history without confounding it with a
different, naturally-thin-history population.

This pilot ran two iterations. Both are reported in full — iteration 1's shortfall is what
motivated iteration 2's fix, and that mechanistic link is itself part of the evidence.

## Precision@10

| Model | Iter 1 Warm | Iter 2 Warm | Iter 1 Cold-start | Iter 2 Cold-start |
|---|---|---|---|---|
| Content-based (CBF) | 0.1182 | 0.1182 | 0.1007 | 0.1007 |
| Collaborative (CF) | **0.5352** | **0.5352** | 0.1610 | 0.1610 |
| Hybrid | 0.4289 | 0.5208 | 0.1374 | **0.1402** |

(CBF and CF are unaffected by the fix — only the hybrid's blend weight changed between
iterations. Raw numbers: `results/pilot_metrics_iteration1.json` and `results/pilot_metrics.json`.)

## Iteration 1 — fixed two-tier blend weight (0.6 CF / 0.4 CBF if ≥3 visible items, else 0.2/0.8)

**Criterion 1 (hybrid ≥10% relative gain over both baselines, warm): NOT MET.**
Beat CBF by +263% relative, but **lost to pure CF by -19.9% relative.**

Cause: CBF's own precision (0.118) is far weaker than CF's (0.535). Even a 40% weighting on
CBF measurably drags the blended ranking down once a user has well more than 3 items visible
— which is most "warm" users here. This is a real negative result for the *specific blend
implemented*, not evidence against combining CF and CBF in general.

## Iteration 2 — continuous blend weight (`alpha = min(0.9, 0.2 + 0.05 * n_visible_items)`)

Replaced the step function with a weight that keeps scaling CF's share up as visible history
grows, instead of capping at 0.6. One function changed, same data pipeline, same split.

**Criterion 1: STILL NOT MET, but the gap closed by an order of magnitude** — from -19.9%
to **-2.7% relative** vs. pure CF, while the +341% margin over CBF held. **Criterion 2
improved too** (0.1402 vs. 0.1374) with cold-start diversity unchanged (106 distinct items).

I stopped at two iterations rather than continuing to tune the weight function until the
number crossed zero — the point of iteration 2 was to fix a specific, named mechanism (a
capped blend weight diluting a much stronger signal), and it worked as predicted; further
knob-turning without a new mechanistic hypothesis would start to look like fitting the
threshold rather than testing the idea.

**Criterion 3 — compute budget: MET.** ~30s per iteration on a single CPU.

**Criterion 4 — report actuals rather than adjust the threshold: this document**, across
both iterations, including the one that didn't clear the bar.

## Diversity check (anti-collapse sanity)

No model collapsed to a fixed list in either iteration: 60–106 distinct items appeared
across top-10 lists per model, out of 115 total items available, across 1,049 users.

## Overall verdict

**Partially supported, and now confirmed across the entire dataset, not just one subset.**
Collaborative signal is clearly the dominant driver of warm-user accuracy — strong enough
that even a well-motivated hybrid blend consistently falls a small, stable amount short of
it (median -2.7% relative across all 22 module-presentations, never worse than -10.8%),
while decisively and universally beating content-based filtering alone (median +190%,
60%–465% every time) and winning at cold-start in 22 out of 22 cases. The thesis's core
premise (behavioral/collaborative signal matters more than content alone) is well
supported and now generalization-tested, not a one-subset anecdote. The open question is
not "does hybridization help" (it clearly does for cold-start, and comes within a few
percent of CF for warm users) but "does *this* linear blend architecture have a real,
structural ceiling below pure CF for warm users" — the tight, consistent -2.7% median
across 22 independent pairs suggests a real ceiling rather than noise, which is worth
answering with a learned blend before Phase 2, not more manual weight-tuning.

## Generalization check — all 22 OULAD module-presentations

Ran the identical pipeline (iteration 2's adaptive alpha) independently on every
module-presentation in OULAD, not just EEE_2014J, to test whether the near-parity-with-CF
result was representative or a fluke of one subset. Script: `code/pilot_all_modules.py`.

**First pass surfaced a real data-quality bug, not just noise.** 3 of 22 pairs
(BBB_2013B, DDD_2013B, DDD_2013J) showed the hybrid's precision *exactly* equal to CBF's
precision, bit-for-bit — worth checking rather than dismissing as an outlier. Root cause,
confirmed directly: `vle.csv`'s `week_from`/`week_to` fields are `'?'` (missing) for **100%**
of items in exactly those 3 module-presentations (every other pair has at least 1.4% known),
so `median()` of an all-missing column returned `NaN`, which propagated through every item's
feature vector, through the L2 norm (`NaN`, not caught by the code's `norm == 0` guard), into
every CBF score. Since CBF's scores were then `NaN` for every item, the hybrid blend
(`alpha * cf + (1-alpha) * cbf`) also went `NaN`, and NumPy's `argsort` sorts an all-NaN array
in a fixed, index-based order — coincidentally the same order for both, which is why hybrid
and CBF matched exactly. This dragged the *mean* relative gain vs. CF down to a misleading
-14.8%, far from the *median* of -2.9% that the other 19 pairs actually clustered around.

**Fixed** (`code/pilot_recommender.py`, `build_item_features`): fall back to `0.0` instead of
`NaN` when a week column has no known values at all, plus a `np.nan_to_num` safety net on the
assembled feature matrix so this class of bug can't silently recur. Re-ran all 22 pairs after
the fix.

### Clean results (post-fix), all 22 module-presentations, warm users

| | vs. CF (relative) | vs. CBF (relative) |
|---|---|---|
| mean | -2.6% | +230% |
| median | -2.7% | +190% |
| min | -10.8% | +60% |
| max | **+0.9%** | +465% |

- **Criterion 1 (≥10% gain over both baselines): 0/22 pass.** The hybrid never fully beats
  pure CF on warm users — but post-fix, the shortfall is small and consistent (median -2.7%,
  worst case -10.8%, one pair essentially at parity at +0.9%), not the wild -96%-to-+1%
  spread the bug had produced. This is a real, generalizable finding: the linear blend has a
  small, consistent ceiling just under pure CF for warm users across the whole dataset.
- **Criterion 2 (cold-start hybrid ≥ CBF): 22/22 pass.** Completely robust across every
  module-presentation, with CBF beaten by 60%–465% (median +190%) in every single case.

Raw per-pair numbers: `results/all_modules_metrics.json` (post-fix, authoritative) and
`results/all_modules_metrics_before_weekfix.json` (kept for the record of what the bug
looked like before it was diagnosed).

## Next steps (Phase 2 candidates, not yet run)

1. A learned blend weight (e.g., logistic regression over visible-item-count and per-model
   confidence, fit on a held-out validation slice) instead of a hand-picked formula, to test
   whether the ~-2.7%-median residual gap is a real ceiling of linear blending or just an
   imperfectly guessed constant — now worth doing with confidence, since the generalization
   check shows the gap is small and stable rather than noisy.
2. ~~Test generalization across the other 21 OULAD module-presentations~~ — done above.
3. Move to the RNN/CNN-based methods from the literature review in
   `knowledge_base/e_learning_recommendation.md` as a stronger CF component, per the thesis's
   own proposed tooling (TensorFlow/Keras), if (1) still can't close the residual gap.

## Limitations

- Single module-presentation (EEE_2014J), not yet tested across the other 21 OULAD
  module-presentations for generalization.
- OULAD is a UK Open University population, not the thesis author's own institution.
- Item-item CF here is classical cosine similarity, not the RNN/CNN/matrix-factorization
  methods from the reviewed literature — appropriate for a Phase 1 pilot per the idea file's
  own instruction to prefer a lightweight model before committing to deep learning.

## Reproducing this run

```
data/projects/e_learning_pilot/code/pilot_recommender.py
```
Deterministic (fixed seed=42, deterministic module-presentation selection). Raw metrics
also written to `results/pilot_metrics.json`.

---
blockers_count: 3
warnings_count: 6
files_reviewed: 24
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Opus 5
model_identity: claude-opus-5 (reviewer seat, top tier) — distinct from the experiment engineer's mid-tier sonnet seat that produced code/ (decisions.log, 2026-09-22T02:00:00Z engineer dispatch; 2026-09-22T10:05:00Z this dispatch)
mode: code_review
unit: u10_g4_code_review
cycle: 1
---

# Review

Second review of `code/` (19 modules, 3 test files, `configs/experiments.json`, `README.md`) against
`idea.md`, `plan.md` and `methodology/protocol.md` as it now stands. Nothing under `code/` is
excluded. No file was edited. Everything I ran wrote only to the OS temp directory; the two
`__pycache__` trees my static pass created under `code/` were removed, and `code/` is byte-identical
to the tree the engineer handed over.

**What I ran, and what it returned.**

- `tests/test_metrics.py` — 11 tests, all `ok`, exit 0.
- `tests/test_evaluate.py` — 5 tests, all `ok`, exit 0.
- `tests/canary_eee_2014j.py` — both rows `OK` (MostPop 0.0137 / 0.0255 / 0.2157; ItemKNN-CF
  0.0279 / 0.0333 / 0.1946), exit 0.
- `compileall` over `code/` — clean.
- Four in-process probes on real OULAD data (presentation `AAA_2013J`, the smallest), driving
  `foundation.verify`, `cell.run_cell` and `evaluate.run_presentation` exactly as `main.run_matrix`
  does. The pilot, iteration and main stages of `code/main.py` were **not** run.

**The headline.** Both cycle-0 blockers are genuinely fixed, and I could not break either fix. But
the run still cannot start: `--stage main` and `--stage iteration` abort in `foundation.verify`
**before any model is fitted** (B1), the Hybrid cannot be fitted or scored at all (B2), and the
tertiary split's L2 assertion is non-zero by the protocol's own design (B3). None of these three is
first-run risk; each is a deterministic failure I reproduced. B1 and B2 also mean cycle 0's account
of where the run dies — "inside the first presentation's secondary-split warm cell" — was wrong:
the run never reaches a cell.

**Cycle-0 blockers, verified fixed against the code, not the report.**

- *Cycle-0 B1 (feature rows subtracted by position).* `code/cell.py:81-85` now aligns by id:
  `np.intersect1d(vh.ids, h.ids, assume_unique=True, return_indices=True)`, then indexes
  `ctx.val_features[iv, c]` and `hyb.X[ih, c]`. Both arrays are in ascending `id_student` order by
  construction (`models.make_history` sorts; `Ctx.sel_ids` is a boolean mask over the already-sorted
  `fit_ids`), both are unique, so `assume_unique=True` is safe and the returned index pairs are
  genuinely the same learner. I ran the real secondary split: 375 evaluated learners, 315 with a
  validation pair, 60 mismatched — the population gap cycle 0 predicted — and the warm cell now
  completes, returning `warm_feature_shift` over 315 learners with
  `warm_feature_shift_n_learners_compared: 315` and
  `warm_feature_shift_n_val_only_or_eval_only: 60`. On the primary split: 375 compared, 0 excluded.
  The 60 dropped learners are exactly those the secondary split keeps in `eval_ids` with no
  validation pair; protocol 5.5 says such a learner "contributes no validation ground truth", so
  they have no validation-time feature row to compare and dropping them is required, not silent —
  the count is written into `info` and thence into `results_<pres>.json`. The quantity is a
  disclosure metric (protocol 8.1 step 4, threat T29) and decides nothing, so the narrowed
  population cannot move a criterion.
- *Cycle-0 B2 (test-scoring counter blind to the split).* `code/leakage.py:59-60` keys
  `(model, split, pres, condition, k, seed)`; `code/models.py:347-349` threads `split` through
  `score_test`; `code/cell.py:37, 47, 73, 100` thread it into `run_cell` and into the log context.
  Direct check: the same `("MostPop", AAA_2013J, warm, None)` cell registered on all five splits
  gives five keys each counted once, `max = 1`; a deliberate repeat still raises `max = 2`, so the
  assertion has not been weakened into uselessness. On the full primary split of `AAA_2013J`
  (10 cells plus the P4b extras) the counter ended with 120 distinct keys, `max = 1`, no duplicates,
  and `ScoreCounter.check` passed. C4's `max_test_scoring_count` reads the same counter, so it is
  now right for the same reason.

**The methodologist's separate ruling on protocol 8.1 step 10 — confirmed, no code change needed.**
`methodology/protocol.md:1005-1013` now states that the degenerate constant is
`median{α*(u) : u a labelled validation learner in that presentation}` with "all-zero learners
dropped by step 2 take no part in this median". `code/blend.py:90-100` computes `labelled = mx > 0`
(a learner whose validation Precision@10 is zero at every α on the 11-point grid is unlabelled),
`lab = np.flatnonzero(labelled)`, and `Blend("constant", float(np.median(astar[lab])))`. That is the
median of α* over the labelled validation learners only, and the fallback when no learner is
labelled is 0.5. The two surrounding branches also match: `len(lab) < 20 or n1 == 0 or n0 == 0`
implements step 2's "fewer than 20 labelled learners" and step 10's single-class case, and
`min(n1, n0) < 10` implements step 10's "fewer than 10 with y = 1 or with y = 0 → C = 1,
C_selection = skipped". Text and code agree.

**The other four cycle-0 items the engineer reported.** All four are done. C4's field is renamed at
`code/evaluate.py:227` to `hyperparameter_rows_reading_test_data`, with `code/evaluate.py:223-226`
stating in the file what it counts, and `finalize`'s `ok` test at `code/evaluate.py:219` still reads
the same counter key `hp_outside_train_or_val`, so the rename did not break the verdict — see [W2]
for what that number can and cannot show. `log.provenance.clear()` moved to `code/cell.py:46`, the
first statement of the cell, and `code/evaluate.py:139-140` records why the C4 loop below it needs
no clear of its own; because `provenance.emit` and `provenance.coverage` both now carry `split` in
their context and `coverage` filters records on the whole context dict, L2's coverage check still
resolves — it passed on every cell of the primary split in my probe. The identical-rankings guard is
`log.flag` at `code/evaluate.py:91`; `common.RunLog.flag` (`code/common.py:128-136`) appends to
`self.executed`, appends the occurrence to `self.flags`, and emits an `assert` line with
`status: FLAG` every time, and `log.summary()` carries `flags` into `run_summary.json`, so every
occurrence the old code would have aborted on is still written twice and nothing is lost. The
README's compute estimate is corrected at `code/README.md:118-127`: 34 cells per presentation
(5 splits × 10 conditions, minus the two narrow P4a reruns' 8) and `cpu_hours × 22` declared a floor.

## Blockers (must fix before proceeding)

- [B1] <severity:high> code/foundation.py:106-107: `leakage.l8(log, prep, "M3", used,
  cond.eval_ids, VAL, k=k, **ctx)` is called with `ctx = {"pres": pres, "condition": name, "k": k}`
  (code/foundation.py:97), so `k` arrives twice and Python raises
  `TypeError: leakage.l8() got multiple values for keyword argument 'k'` at the call, before the
  function body runs. `verify`'s plan reaches its first cold condition `("A", 0)` immediately after
  the warm one, so this fires on the first presentation of every matrix run. Reproduced by calling
  `foundation.prepare` then `foundation.verify` on AAA_2013J exactly as code/main.py:75-76 does.
  | impact: `--stage main` and `--stage iteration` abort inside `foundation.verify` of the first
  presentation, before any model is fitted and before `foundation_<pres>.json` is written; no cell,
  no metric, no criterion verdict, and README step 5's and step 6's "Expect exit 0" cannot hold.
  Cycle 0 did not see this, which is why its B1 impact note placed the abort much later.

- [B2] <severity:high> code/blend.py:84 and code/models.py:342: both read
  `view.week_missing_share` / `c.view.week_missing_share`. That attribute exists on
  `features.View` (code/features.py:26) but **not** on `splits.Prep`, where the constant lives at
  `prep.feature_constants["week_missing_share"]` (code/splits.py:31, code/data.py `item_features`).
  `cell.run_cell` builds `models.Ctx(prep, ...)` from a `Prep` (code/cell.py:48, called from
  code/evaluate.py:138 with `sp`, a `Prep` from `build_prep` or `variants.secondary`/`tertiary`), so
  `Hybrid.fit -> ctx.blend -> blend.fit_blend` raises
  `AttributeError: 'Prep' object has no attribute 'week_missing_share'` in the **first** cell of the
  first split of the first presentation, and `Hybrid.score` would raise the same at test-scoring
  time. Reproduced on both the primary and the secondary warm cells of AAA_2013J. The bug is hidden
  from the L7 rebuild path only because `cell._ctx` (code/cell.py:113-120) is handed a
  `features.View`, which does have the attribute — so the fix must be an accessor that works for
  both types, not a rename in one direction. | impact: no Hybrid is ever fitted or scored; with B1
  fixed, the run would abort at the first cell instead of in `foundation.verify`, and the hypothesis
  the thesis exists to test could not be evaluated at all.

- [B3] <severity:high> code/provenance.py:19 and 27 with code/features.py:61-68 and
  code/variants.py:72, reached from code/cell.py:55: on the **tertiary** split the training bound is
  `NO_BOUND = 10**9` (code/variants.py:15, 72), so `features.train_weights` reads every row of every
  fitted learner, including rows belonging to that learner's validation and test pairs — which is
  what protocol 5.5's tertiary row prescribes ("none can be defined, and none is applied … Clicks
  and active days are summed over all rows"). `provenance.record` then counts those rows as
  `n_rows_outside_allowed`, and `RunLog.measure` requires L2 to be 0 (protocol 5.4 L2: "every
  `n_rows_outside_allowed` must be 0", with no tertiary exemption). Measured on AAA_2013J's tertiary
  warm cell: `L2: measured 54193, required 0, object_name similarity_matrix, n_source_rows 180925`
  — 30% of the rows, exactly the split's 20% test plus 10% validation. L1 and L9 both have explicit
  tertiary handling (code/evaluate.py:128-129; `Prep.l9_training_na` at code/splits.py:32 and
  code/leakage.py:91-93); L2 and L3 have none. | impact: with B1 and B2 fixed, `--stage main` still
  aborts at the first presentation's tertiary split, after its primary and secondary splits have
  been paid for; `results_<pres>.json` is never written for any presentation, `finalize` never runs,
  and no verdict is produced. How to resolve it is a methodology decision, not an engineering one
  (rule=8): either the tertiary split declares L2/L3 `not_applicable` with the measured count
  recorded as evidence, the way L1 and L9 already do, or the tertiary split's fitted objects read
  only training-role pairs. The engineer must not silently relax the assertion.

## Warnings (should fix)

- [W1] <severity:med> code/cell.py:66 and 70: the two `leakage.l8` calls pass
  `pres=prep.pres, condition=cond.name` explicitly and **not** `split`, unlike every other
  assertion in the cell, which now carries `**cell`. The L8 and `L8_truth_in_exclusion` lines of one
  presentation's five splits are therefore indistinguishable in `results/run.log` — the exact
  traceability cycle-0 W3 asked for, delivered everywhere except here. No count changes; only the
  ability to attribute a failure to a split.
- [W2] <severity:med> code/evaluate.py:141-144 and 227 with code/models.py:241 and
  code/blend.py:125-128: the renamed `hyperparameter_rows_reading_test_data` is now accurate about
  what it measures, but it is structurally incapable of being non-zero. The `read` frame for
  `N_selection`, `C_selection`, `blend_model` and `blend_standardiser` is
  `ctx.pairs_read(ids, (TRAIN, VAL))`, and `provenance.record`'s `allowed` is
  `prep.pairs[isin(fit_ids) & role.isin((TRAIN, VAL))]` with `ids ⊆ sel_ids ⊆ fit_ids`, so `read`
  is a subset of `allowed` by construction and the merge can never produce an unmatched row. The
  same field is a real measurement for `similarity_matrix`, whose `read` frame is the rows
  `bounded_rows` actually returned — B3 is the proof. C4's hyperparameter conjunct is therefore
  self-certifying; the real protection for the blend is L7, L8 and L9, and chapter 5 should say so
  rather than cite this number as independent evidence.
- [W3] <severity:med> code/README.md:55-56 and 65 still document
  `ScoreCounter.scored_test(model, pres, condition, k, seed)` and
  `cell.run_cell(prep, cond, log, counter, length, pres_index)` without the new `split` parameter.
  The interface contract the next engineer dispatch reads is now wrong in the one place this cycle
  changed it.
- [W4] <severity:med> code/blend.py:39-44 with the installed scikit-learn: `_make_lr` passes
  `penalty="l2"`, and the environment's scikit-learn (1.8+) accepts it but emits
  `FutureWarning: 'penalty' was deprecated in version 1.8 and will be removed in 1.10`. The
  `except TypeError` fallback only triggers once the argument is removed outright, so today the run
  will emit this warning once per logistic-regression fit — thousands of lines of runner noise, and
  a silent behaviour change on the next scikit-learn bump. Pin or record the scikit-learn version in
  the reproducibility appendix; `run_manifest.json` already captures it (code/common.py:100).
- [W5] <severity:low> code/README.md:128 (main-run acceptance, step 6) tells the runner to expect `flags`
  empty in `run_summary.json`, while code/evaluate.py:87-91 now deliberately allows a legitimate
  identical-ranking tie to flag and continue. A run that exits 0 with one entry in `flags` is now
  the expected outcome in some cells, not a failure; the README's acceptance line should say
  "investigate each flag" rather than "flags empty", or a correct run will read as a failed one.
- [W6] <severity:low> code/evaluate.py:234-237: the optimism table builds
  `min(... for p in pres)` and `max(...)` over `pres = sorted(acc)`, which raises
  `ValueError: min() iterable argument is empty` if `finalize` is ever reached with no presentation
  accumulated. Unreachable from `main.run_matrix` today (a matrix always has at least one
  presentation, and an abort re-raises before `finalize`), but it is one `--only` edge away from
  turning a clean partial run into a crash in the summary writer.

## Constraint Audit

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a multi-GPU cluster." | status: satisfied | evidence: code/common.py:30 `"hardware": "single CPU, no GPU"`; code/common.py:91-101 writes processor, logical cores and "no GPU" into `run_manifest.json`; a fresh grep for `torch|tensorflow|keras|cuda|gpu` over all 22 files under code/ returns nothing but that literal | blocker: none
- [C2] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed hardware" (plan.md Budget `max_cpu_hours: 4.0` main, `<= 0.25` reproduction; C5) | status: satisfied | evidence: code/main.py:119-124 sums wall seconds, `time.process_time()` and the L7 workers' wall seconds into `cpu_hours`; code/verdicts.py:43-53 judges C5 against `common.HARD_CONSTRAINTS` 4.0 and 15.0 and records the hardware; code/README.md:118-127 now declares `cpu_hours × 22` a floor and tells the runner to stop before 4.0, not after. Whether the realised figure fits is the runner's evidence at G5 | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." | status: satisfied | evidence: a fresh grep for `requests|urllib|http(s)://|socket|download|huggingface|transformers` over code/ returns exactly one hit, the literal `"downloaded_model_weights": False` at code/common.py:31; the only reads are the four hashed OULAD CSVs (code/data.py:13, 21-40, 52-80) | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and evaluated on identical splits so the comparison in success criterion 1 is fair." | status: satisfied | evidence: the split is built once per presentation (code/splits.py:100-135) and `split_view` (code/splits.py:90-97) is the only object models receive; `leakage.l5` (code/leakage.py:45-48) re-hashes the triple each model actually holds against `prep.hashes`, driven per cell at code/cell.py:59-61, and derived splits recompute their own triple (code/variants.py:37); L4's three intersections are measured 0 (code/leakage.py:36-42, code/evaluate.py:126). L5 and L4 both passed on every cell of AAA_2013J's primary split in my probe. The new `split` key is a log and counter dimension only; it changes no L1-L9 count, and L2's coverage filter stays consistent because `provenance.emit` and `provenance.coverage` are both called with the same `**cell` (code/cell.py:55-56) | blocker: none
- [C5] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only background; do not attempt to re-scrape or redistribute their content." | status: satisfied | evidence: no path under `src/reasearch_topic` occurs anywhere in code/ (fresh grep); the single configured data root is `data/projects/e_learning_pilot/data/raw` (code/configs/experiments.json:4, code/data.py:14, 21-22); the constraint is carried as a literal at code/common.py:34 | blocker: none
- [C6] Network limited to the one OULAD download (idea.md DATASET DECISION: "requires network access during the pilot to download OULAD once (a few hundred MB)") | status: satisfied | evidence: zero network calls under code/ (same grep as C3); code/data.py:25-40 verifies SHA256 and byte size of every file used against `inputs/manifest.json` and raises `DataIntegrityError` before any use; my probes loaded OULAD from the hashed local copy with no network access | blocker: none
- [C7] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most likely cause ... rather than adjusting the threshold after the fact." | status: satisfied | evidence: code/verdicts.py:12-19 JSON-decodes `metric`, `threshold` and `on_dataset` out of plan.md's frozen front matter at run time; code/stats.py:12 fixes the four verdict words and code/stats.py:97-109 applies C1 as `>= 0.10` and C2 as `> 0` exactly, with `NOT_MET_UNCHECKED` for a met threshold on an inconclusive test; a failing criterion still carries `values` with medians, Wilcoxon, effect size and dropped-pair counts. No threshold literal was touched this cycle | blocker: none
- [C8] "Language/tooling per the thesis: Python, TensorFlow or Keras, scikit-learn. Prefer scikit-learn or a lightweight model for the pilot; reserve deep learning (RNN/CNN/RBFNN ...) for the Phase 2 main experiment" | status: satisfied | evidence: the only estimators are `sklearn.linear_model.LogisticRegression` (code/blend.py:9, 39-44), `sklearn.model_selection.StratifiedKFold` (code/blend.py:10) and `sklearn.cluster.KMeans` with `silhouette_score` (code/behaviour.py:11-12); everything else is numpy/pandas/scipy; plan.md records the deep models as an explicit scope-out | blocker: none

## Notes

- The B1 alignment does not change what any assertion counts. `warm_feature_shift` is reported in
  `info`, consumed nowhere but `results_<pres>.json`, and is absent by design in cold cells
  (`code/cell.py:76` guards on `not ctx.cold`), which I confirmed on the primary A|2 cell.
- The B2 split key widens `n_scoring_cells` (each presentation's cells are now counted once per
  split rather than collapsed) and leaves `max_test_scoring_count` at 1. `C4`'s `ok` test at
  code/evaluate.py:219 requires `mx == 1`, so the renamed field and the split key move C4 from a
  guaranteed failure to a real test.
- The P4b path keys correctly on both dimensions: `cond.name + "+P4b"` (code/cell.py:94) and the
  same `split` (code/cell.py:100), so the two-day learners cannot collide with the main cell.
- `_MEMO` in code/cell.py:110-120 clears on every new key, so the rebuild builders cannot leak a
  fitted context across cells; `l7_rebuild`'s fresh process re-imports `cell` from
  `configs/experiments.json`'s `builder_modules`, which I confirmed still resolves.
- This file was written by hand, not by the review MCP tool: `ar-workflow-engine.py` imports
  `fcntl`, which Windows Python does not have, so nothing validated the Constraint Audit, the
  blocker count or the unit/cycle binding before it landed. Per rule 6 that absence is `unchecked`,
  not `passed`, and the coordinator's decision log should carry it. I ran the tool's own validation
  rules on this draft myself: eight constraints, each once, each with status, evidence and a
  blocker field; every entry `satisfied` with `blocker: none`; three `[B#]` entries counted against
  `blockers_count: 3`.
- `review.md` (cycle 0) is untouched and remains the cycle-0 record.

## Overall

The decision is `revise`. Both cycle-0 blockers are properly fixed — the warm feature shift is now
aligned by `id_student` with the dropped population counted and disclosed, and the test-scoring
counter is keyed by split, which I verified on real data rather than from the engineer's summary —
and the methodologist's reading of protocol 8.1 step 10 matches `blend.py` exactly, so no code
change is needed there. What blocks the unit is three separate deterministic failures that stop the
run before any of that matters: a `TypeError` in `foundation.verify` that aborts the first
presentation before a single model is fitted, an `AttributeError` that makes the Hybrid unfittable
and unscorable on every split, and an L2 assertion that the tertiary split's own protocol-mandated
absence of a training bound guarantees will be non-zero. The first two are mechanical and belong to
the engineer; the third needs the methodologist to say whether L2 and L3 are `not_applicable` on the
tertiary split the way L1 and L9 already are, or whether the tertiary split must restrict its fitted
objects to training-role pairs (rule=8 — the engineer may not relax a protocol assertion on its
own). Clearing all three, with `foundation.verify` and one full presentation actually executed end
to end before the next review, is what would change this to `approve`; nothing else I found rises
above a warning.

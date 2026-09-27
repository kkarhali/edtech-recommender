---
blockers_count: 2
warnings_count: 12
files_reviewed: 24
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Opus 5
model_identity: claude-opus-5 (reviewer seat, top tier) — distinct from the experiment engineer's mid-tier sonnet seat that produced code/ (decisions.log, 2026-09-22T06:40:00Z)
mode: code_review
unit: u10_g4_code_review
cycle: 0
---

# Review

Full review of `code/` (22 `.py` files, `configs/experiments.json`, `README.md`) against
`idea.md`, `plan.md` and `methodology/protocol.md` at G3 approval. Nothing under `code/` is
excluded. The code has never been executed; I ran static analysis, the two unit-test files and the
entry-point refusals only, all with the project tree read-only and every scratch path in the OS
temp directory. The pilot, iteration and main stages were not run — they belong to the runner.

The headline: the protocol's leak repairs are implemented correctly, and I could not break the
substantive design tracing. The two blockers are mechanical — a shape mismatch and a missing key —
but each of them stops the main run dead, so neither is a bug a first run would merely "surface":
they are the reason the first run cannot finish.

## Blockers (must fix before proceeding)

- [B1] <severity:high> code/cell.py:69-71 (with code/models.py:210-214 and code/variants.py:52-55):
  the warm `warm_feature_shift` block computes
  `np.abs(ctx.val_features[:, c] - hyb.X[:, c]).mean()`. `ctx.val_features` (set in
  code/blend.py:85) has one row per learner in `Ctx.sel_ids` — the fitted learners that have
  validation ground truth — while `hyb.X` (set in code/models.py:342) has one row per scored
  learner in `cond.eval_ids`. On the primary, tertiary and P4a splits these two sets coincide,
  because every learner there is guaranteed a non-empty validation slice (`SPLIT_EXCLUDED_LEARNERS`
  is asserted 0 at code/splits.py:129-130; the tertiary split gives every learner
  `max(1, round(0.1n))` validation pairs at code/variants.py:68). On the **secondary** global
  cut-off split they do not: `variants.secondary` drops only learners with no *training* pair
  (code/variants.py:53-55), exactly as protocol 5.5 rules, so learners whose pairs all fall on or
  before `D_val` stay in `eval_ids` and are removed from `sel_ids`. Since the secondary validation
  slice is by construction at most 10% of the presentation's pairs (code/variants.py:48-51), that
  population is large, not marginal. The subtraction then raises
  `ValueError: operands could not be broadcast together`. | impact: `--stage main` and
  `--stage iteration` abort deterministically inside the first presentation's secondary-split warm
  cell, before any `results_<pres>.json` is written; no criterion verdict can be produced, and
  README step 5's "Expect exit 0" cannot hold.

- [B2] <severity:high> code/models.py:347-349 and code/leakage.py:51-61, reached from
  code/cell.py:66 and code/evaluate.py:166-170: `ScoreCounter.scored_test` keys a test scoring by
  `(model, presentation, condition, k, seed)` and never by the split. `run_presentation` runs the
  same `(condition, k)` cells on five splits of one presentation — primary, secondary, tertiary,
  `P4a_3`, `P4a_10` — so `("MostPop", pres, "warm", None, None)` is registered five times and
  `("MostPop", pres, "A", 2, None)` three times. `ScoreCounter.check` then measures
  `sum(1 for v in self.n.values() if v > 1)` as a large non-zero count and `RunLog.measure` raises
  `LeakageError`. | impact: assertion L6 fails spuriously in `evaluate.finalize`, after the whole
  22-presentation run has been paid for; `results_summary.json` and `criteria_verdicts.json`'s six
  verdicts are never written, `run_summary.json` records `status: failed`, and C4's
  `max_test_scoring_count` is wrong for the same reason. The P4b path is already keyed correctly
  (`cond.name + "+P4b"`, code/cell.py:75), which shows the split dimension was simply forgotten.

Required to clear both: add the split name to the `ScoreCounter` key (and, for traceability, to
`cell`'s log context at code/cell.py:40), and compute the warm feature shift only over the learners
present in both matrices, aligning by `id_student` rather than by row position.

## Warnings (should fix)

- [W1] <severity:med> code/evaluate.py:135-138 and 213-218 with code/models.py:241 and
  code/blend.py:125-128: C4's reported field is named `hyperparameter_rows_outside_validation`, but
  what it counts is `n_rows_outside_allowed` where `allowed` is the fitted learners' pairs with role
  in `(TRAIN, VAL)`. It therefore detects a hyperparameter object reading a **test** row and nothing
  else. That is the right test — the blend genuinely must read training-side history to build its
  features, so plan.md C4's literal "fitted outside the validation split" cannot mean "reads no
  training row" — but the label will put an overclaim into chapter 5. Rename the field and state in
  `values` what was actually counted.
- [W2] <severity:med> code/evaluate.py:135-139 with code/main.py:76-80 and code/provenance.py:40-44:
  `log.provenance` is cleared only after each cell in `run_split`, so when the first cell of the
  primary split calls `provenance.coverage`, the list still holds `foundation.verify`'s records for
  the same `(pres, condition, k)`. Those records already carry `similarity_matrix`, `mostpop_counts`
  and `popweek_counts`, so L2's coverage check can pass on foundation's evidence even if the cell
  itself recorded nothing for them. Clear the list at the start of each cell, not the end.
- [W3] <severity:med> code/cell.py:40: `cell = {"pres", "condition", "k"}` carries no `split`, so
  every L2/L3/L7/L8/L9/A5/parity line a secondary-split `A|2` cell writes to `results/run.log` is
  byte-indistinguishable from the primary-split `A|2` line. The run receipt and the results analyst
  cannot tell a deciding assertion from a robustness one. `l1`, `l4` and `identical_guard` do carry
  `split` (code/evaluate.py:122-141), which makes the omission look accidental.
- [W4] <severity:med> code/cell.py:52-54: L5 collects views by `id(m.ctx.view)`, and all six models
  share one `Ctx`, so the assertion hashes the same object six times. It confirms that the view
  handed to the models equals `prep.hashes`, which is worth having, but it cannot detect "a model
  quietly receiving a different split", which is what protocol 5.4 says L5 rules out. Either hash
  per model at score time or restate the assertion's scope in the log line.
- [W5] <severity:med> code/cell.py:113-118 with code/blend.py:71-76 and code/leakage.py:128-150: the
  L7 fresh-process rebuild compares logistic-regression coefficients across two processes at 10
  decimal places. lbfgs on identical inputs is deterministic, but BLAS threading and library load
  order are not guaranteed identical between parent and child, so a legitimate run can abort on
  `L7_rebuild_mismatch`. Consider a tolerance for the two blend objects, or pin thread counts in the
  worker's environment (code/leakage.py:139 already sets two env vars, so the hook exists).
- [W6] <severity:med> compute budget, C5. `foundation.verify` (code/foundation.py:112-113) runs two
  fresh-process rebuilds per presentation, each refitting all seven learner-derived objects at four
  `k` values — that is eight full blend fits per rebuild, in-process and again in the worker — and
  `evaluate.run_presentation` then runs 34 cells per presentation (code/evaluate.py:161-170). The
  engineer's own R2 and R3 flag this. README step 5's "multiply `cpu_hours` by 22" underestimates,
  because EEE_2014J (1,018 learners, 115 items) is far cheaper than CCC_2014J (2,131 learners) and
  `cf_scores` (code/models.py:125-130) is O(visible items x learners x catalogue) per call. C5 is
  measured and judged rather than assumed, so this is a warning; the runner should treat the
  extrapolation as a lower bound.
- [W7] <severity:med> code/evaluate.py:76-87: `identical_guard` uses `log.measure`, which aborts the
  run, for a condition that can arise legitimately — a presentation where CBF is degenerate, or a
  cell where the fitted `alpha` is 1 for every learner, would make two models' full orders identical
  without any bug. Losing a 22-presentation run at the last cell over a legitimate tie is a poor
  trade; `log.flag` plus a named investigation step would preserve the signal without the abort.
- [W8] <severity:med> code/stats.py:26-47: protocol 10.2a(2) requires a result with effective n
  below 6 to be **reported** as `inconclusive (effective n = <n>)`, never as "not significant".
  `wilcoxon_paired` returns `n_eff` and a p-value with no such label; only `decide`
  (code/stats.py:105-106) applies the rule, and only for C1 and C2. Every F3 and F4 test reported at
  a small effective n can therefore be read as a plain p-value. Emit the wording in the dict.
- [W9] <severity:med> code/evaluate.py:58-65 and 103-115: when a cell has no learner with a
  non-empty test set, `vec[key]` is `None` and `stats_block`'s `np.stack` raises. Only reachable on
  the secondary split, where learners can lose their test pairs, and only if a whole cell empties —
  but that is the same split B1 already crashes on, so it will not be exercised until B1 is fixed.
- [W10] <severity:med> code/evaluate.py:25, 140, 145: bootstrap intervals and the Kendall-tau
  popularity agreement are computed for the primary split's warm and `A|2` cells only. Protocol 10.2
  says any reported number is quoted as `value [lo, hi]`, "never as a bare number". The secondary,
  tertiary, P4a and P4b figures in `results_summary.json` therefore carry no interval, and chapter 5
  must not quote them as if they did.
- [W11] <severity:low> code/verdicts.py:12-19 with code/main.py:103-107: `load_criteria` re-reads
  `plan.md` at run time, which is the right way to keep the thresholds verbatim, but
  `run_manifest.json` records `config_sha256` and `code_tree_sha256` and **not** `plan.md`'s SHA256.
  An edit to the frozen criteria block between the code review and the run would silently change the
  quoted thresholds with nothing in the receipt to show it. Add the plan hash to the manifest;
  `methodology/protocol.md` already carries the expected value
  (`22bb14a20fe7f111bf342aec51a54b7a3b6daf6c8723e1b5d66120d8d8e462d0`).
- [W12] <severity:low> code/reproduce_phase1.py:199-200: the pilot stage emits one combined
  `id="L1-L8"` not-applicable line instead of eight. `L9` is emitted on its own, correctly, but an
  auditor reconciling the C6 receipt against protocol 5.4 has to read prose for the other eight.

## Constraint Audit

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a multi-GPU cluster." | status: satisfied | evidence: code/common.py:30 `"hardware": "single CPU, no GPU"`; code/common.py:91-101 writes processor, logical cores and "no GPU" into `run_manifest.json`; no torch/tensorflow/keras/cuda reference in any of the 22 files under code/ (grep) | blocker: none
- [C2] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed hardware" (plan.md Budget `max_cpu_hours: 4.0` main, `<= 0.25` reproduction; C5) | status: satisfied | evidence: code/main.py:119-124 measures wall seconds, `time.process_time()` and the L7 workers' wall seconds and reports `cpu_hours` as their sum (an upper bound, engineer's R3); code/verdicts.py:43-53 judges C5 against `common.HARD_CONSTRAINTS` 4.0 and 15.0 and records the hardware; code/reproduce_phase1.py:197 flags the 15-minute conjunct. Whether the realised figure fits is the runner's evidence at G5 — see [W6] | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." | status: satisfied | evidence: no `requests`/`urllib`/`http`/`download`/`transformers`/`huggingface` reference anywhere under code/ (grep over all 22 files; the only hit for the word is the literal `"downloaded_model_weights": False` at code/common.py:31); the only reads are the four hashed OULAD CSVs (code/data.py:13, 52-80) | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and evaluated on identical splits so the comparison in success criterion 1 is fair." | status: satisfied | evidence: the split is built once per presentation (code/splits.py:100-135) and `split_view` (code/splits.py:90-97) is the only object models receive; `pair_hash` (code/splits.py:79-80) is a SHA256 over `(id_student, id_site)` sorted, and `leakage.l5` (code/leakage.py:45-48) re-hashes the triple per model against `prep.hashes`; derived splits recompute their own triple (code/variants.py:37); L4's three intersections are measured 0 (code/leakage.py:36-42). Scope caveat at [W4] | blocker: none
- [C5] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only background; do not attempt to re-scrape or redistribute their content." | status: satisfied | evidence: no path under `src/reasearch_topic` occurs in any file under code/; the single configured data root is `data/projects/e_learning_pilot/data/raw` (code/configs/experiments.json:4, code/data.py:14, 21-22); the constraint is carried as a literal at code/common.py:34; code/reproduce_phase1.py:3-7 states the pilot code was copied, not imported, and the pilot tree is read for raw CSVs only | blocker: none
- [C6] Network limited to the one OULAD download (idea.md DATASET DECISION: "requires network access during the pilot to download OULAD once (a few hundred MB)") | status: satisfied | evidence: zero network calls under code/; code/data.py:25-40 verifies SHA256 and byte size of every file used against `inputs/manifest.json` and raises `DataIntegrityError` before any use, emitting a `data_sha256` line with `manifest_match: true`; plan.md Budget `network: none required` | blocker: none
- [C7] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most likely cause ... rather than adjusting the threshold after the fact." | status: satisfied | evidence: code/verdicts.py:12-19 JSON-decodes `metric`, `threshold` and `on_dataset` straight out of plan.md's frozen front matter at run time rather than restating them — I confirmed the parse returns all six criteria with their thresholds intact; code/stats.py:12 fixes the four verdict words and code/stats.py:97-109 applies C1 as `>= 0.10` and C2 as `> 0` exactly; a failing criterion still carries `values` with the medians, the Wilcoxon, the effect size and the dropped-pair counts (code/stats.py:81-94). Hardening at [W11] | blocker: none
- [C8] "Language/tooling per the thesis: Python, TensorFlow or Keras, scikit-learn. Prefer scikit-learn or a lightweight model for the pilot; reserve deep learning (RNN/CNN/RBFNN ...) for the Phase 2 main experiment" | status: satisfied | evidence: the only estimators are `sklearn.linear_model.LogisticRegression` (code/blend.py:9, 39-44) and `sklearn.cluster.KMeans` (code/behaviour.py:11, 38); everything else is numpy/pandas/scipy; plan.md's Proposal Traceability records the deep models as an explicit scope-out rather than a silent omission | blocker: none

## Notes

**What I verified by running, and what I did not.** Both unit-test files pass on
`.venv-pilot\Scripts\python.exe` with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUTF8=1`:
`tests/test_metrics.py` prints 11 `ok test_...` lines and exits 0, `tests/test_evaluate.py` prints 5
and exits 0. Neither writes a file. All 22 files compile (`py_compile`, doraise) and all 19
non-test modules import cleanly. Nine entry-point invocations were run (see `reviews/code_gate.md`);
`results/` was still absent afterwards. I did not run the canary, the pilot stage, the iteration
stage or the main stage; those read the 453 MB `studentVle.csv` and are the runner's work.

**The canary's constants are right.** `tests/canary_eee_2014j.py:24` asserts
`MostPop (0.0137, 0.0255, 0.2157)` and `ItemKNN-CF (0.0279, 0.0333, 0.1946)`, which match protocol
7.1's measured-effect table to the digit, including the revision-3 re-run of the `ItemKNN-CF` line.
The three columns are built with the right objects: no exclusion (`np.zeros_like(h.excl)`), the
adopted `M3` visible-`k` exclusion (`h.excl` from `make_history(..., "M3")`), and the discarded
revision-1 `training ∪ validation` mask — and `sim_n("all")` keeps self-similarity, which is what the
protocol's footnote to that table requires. Cohort size 204 and fit size 814 are asserted at line 41.

**(1) Split, filters, empty slices.** `splits.split_learner` (code/splits.py:35-53) implements 5.1
exactly: `j*` searched over `3..m` minimising `|5·suffix(j) − n|` with ties to the larger `j` via
`flatnonzero(...)[-1]`, then `i*` over `2..j*−1` minimising `|10·(suffix(i) − suffix(j*)) − n|`, ties
again to the larger. The integer scaling keeps the tie rule exact. I hand-checked the unit test's toy
(n = 20, suffix 20/16/13/11/9/6/4/2): `j* = 7` → day 10 (4 pairs = 0.20n), `i* = 6` → day 9 (2 pairs =
0.10n), which is what the test asserts. P4a and P4b are applied before the split
(code/splits.py:108-111) and `SPLIT_EXCLUDED_LEARNERS` measures learners with an empty train,
validation or test set at 0 (code/splits.py:129-130) — an abort, not a flag.

**(2) The three exclusion moments.** `features.exclusion_sets` (code/features.py:111-119) returns
training for M1, training ∪ validation for M2 and the visible `k` pairs for M3, and the moment is
chosen by condition everywhere it matters: the alpha label grid scores against `h.excl` of the
validation history (code/blend.py:87), the blend features are built from the same history at fitting
time and from the test history at scoring time through one function (code/blend.py:20-32, called at
code/blend.py:84 and code/models.py:342), `N` is selected on `valhist` (code/models.py:218-243), `C`
is selected on the same (code/blend.py:117), and Condition B takes `cold = True` with
`fit_ids = everyone` (code/splits.py:156-160), so it uses M3 at both boundaries while fitting on the
cohort it calls new. The degeneracy the protocol's revision 3 note describes — a warm rule at
validation time scoring exactly 0.0000 and collapsing the blend to a constant 0.5 — is guarded by a
counted assertion, not by comment: `leakage.l8` emits `L8_truth_in_exclusion`, the number of learners
whose ground truth sits inside their own exclusion set, required 0, at both moments
(code/leakage.py:78-83, called at code/cell.py:59, 63 and code/foundation.py:89-90, 106-107).
`_independent_exclusion` (code/leakage.py:64-75) recomputes the expected set in a plain Python loop
sharing no code with `exclusion_sets`, which is the right way to make L8 more than a tautology.

**(3) Date-bounded weights.** Every weight in the model path is formed by `features.bounded_rows`
(code/features.py:36-48), which applies `date < t` for the training bound and `date <= t` for the
cold bound, re-reads what it actually returned and ledgers `n_rows_at_or_after_bound` for L9
(code/leakage.py:86-93). The training bound is the learner's first validation day
(`learners.val_start`, code/features.py:61-62); the cold bound is the `k`-th visible pair's
`first_date` (code/features.py:76). I grepped every reader of `sum_click`: `features.clicks_from`
(fed only by `bounded_rows`), `leakage._weights_by_truncation` (the independent check, which cuts the
learner's date-sorted rows with `searchsorted` and accumulates with no bound test at all — a genuinely
different path, hashed against the first at code/leakage.py:118-125), `behaviour.py:23` (descriptive
only, feeds no model) and `reproduce_phase1.py` (unbounded by design, protocol 5.5). `active_days` is
`nunique()` over the same bounded read, never a row count (code/features.py:56-58). The 17.8% leak
protocol 4 measured cannot recur through this path.

**(4) Condition A fits on the 80% only.** `make_condition` builds `fit_ids` by `setdiff1d(everyone,
cohort)` for A and A_robust (code/splits.py:159) and every fitted object is reached through
`Ctx.fit_ids`: the engagement matrix and similarity (code/models.py:172-177), the `MostPop` and
`PopWeek` counts (code/models.py:180-186 via code/features.py:104-108), `N` (code/models.py:230-243,
scored on `sel_ids ⊆ fit_ids`), and `C`, the blend model and its standardiser (code/blend.py:98,
125-128). The catalogue-derived constants — P5 week medians and the `week_from`/`week_to` min-max
bounds — read `vle.csv` only (code/data.py:83-109) and are asserted identical between conditions by
regenerating them and counting differing cells (`A4_differing_cells`, code/foundation.py:84-85), with
`n_learner_rows_used = 0` emitted as positive evidence (code/provenance.py:35-37). Each object's
`n_cold_learners_used` is measured from the rows the function actually read
(code/provenance.py:13-20) and required 0 except in Condition B, where it is emitted as `info`
against the expected `|C|` (code/provenance.py:28-31, code/splits.py:147-149). The self-report is
then checked independently: `l7_rebuild` (code/leakage.py:128-150) pickles a view whose cold rows are
physically absent into a fresh `sys.executable` process, rebuilds all seven objects there, hashes
inside that process, counts cold rows found in the worker's frames, and logs seven hash pairs. That
is exactly the construction protocol 6.1a's warning W2 demands, and `features.BUILDERS` does cover
all seven once `cell.py` is imported — I confirmed the registry resolves to
`{similarity_matrix, mostpop_counts, popweek_counts, N_selection, C_selection, blend_model,
blend_standardiser}`.

**(5) Ranking, scaling, identity guard.** `models.top_positions` (code/models.py:73-82) builds the
order with `np.lexsort` over `[column index, where(excl, inf, -round(score, 12))]`, so the primary key
is score descending after 12-decimal rounding and the secondary is `id_site` ascending — the catalogue
axis is `id_site` ascending by construction (code/splits.py:102, code/data.py:71) — and excluded items
are pushed past every candidate. `cf_scores` accumulates over items in ascending column order
(code/models.py:128), which is the summation-order half of protocol 8.0(i). `metrics.rank_topk`
(code/metrics.py:12-22) is an independent list-based implementation of the same rule and
`test_matrix_ranking_agrees_with_rank_topk_and_minmax_rule` cross-checks the two. `minmax_rows`
(code/models.py:95-101) returns the zero vector when `max − min < 1e-12`, per learner, over that
learner's candidate set, and `a5_mismatches` (code/models.py:104-107) recomputes each learner's row
alone and counts disagreements, which is precisely the pooled-matrix error A5 exists to catch; the
count is asserted 0 at code/cell.py:82. The identical-rankings guard (code/evaluate.py:76-87) hashes
each model's full order and exempts only the identities the protocol predicts in advance.

**(6) The blend against all eleven points of 8.1.** Level: one row per learner
(code/blend.py:29). Target: the 11-point grid, Precision@10 on validation items under the validation
moment's exclusion, `α*(u) = median` of the maximisers, `y = 1 if α* >= 0.5`
(code/blend.py:87-91) — and all-zero learners are dropped from the fit, not labelled
(`labelled = mx > 0`, code/blend.py:90), with the share reported per cell (code/blend.py:95-96).
Features: the eight of step 3 in the fixed order (code/blend.py:15-16, 29). Construction: one
function for validation and test time (code/blend.py:20-32). Scaling: z-score with a zero-variance
feature passed through as constant zero (code/blend.py:35-36), refitted per CV fold
(code/blend.py:113) and once on all labelled rows for the final model (code/blend.py:123). Estimator:
`penalty="l2"`, `solver="lbfgs"`, `tol=1e-4`, `max_iter=1000`, `fit_intercept=True`,
`class_weight=None`, `random_state=42` (code/blend.py:39-44). Output: `predict_proba` for class 1
with no clipping and a range assertion (code/blend.py:47-50, 66-68). `C`: `StratifiedKFold(5,
shuffle=True, random_state=42)` on `y`, scored by the fold's hybrid Precision@10 against validation
items, strict `>` so ties go to the smaller `C`, then refit on all labelled rows
(code/blend.py:108-124). `N`: inherited from `ItemKNN-CF`, no search of its own
(code/blend.py:82, code/models.py:340). Degenerate cases and the `< 20 labelled` rule of step 2:
code/blend.py:99-106. Refit per `(presentation, condition, k)` including Condition B: one `Ctx` per
cell, `fit_ids = everyone` for B. Parity: `n_configurations` 5 for `ItemKNN-CF`, 4 for `Hybrid` when
CV runs, 0 for the rest, with `n_label_grid_points` reported separately and a measured assertion that
the maximum is not above 5 (code/blend.py:97, 122, code/cell.py:85-86). Eleven for eleven; the one
wording divergence is in the defaults section below.

**(7) Statistics against protocol 10.** The deciding test runs on the paired absolute
presentation-level values, not the ratios (`wilcoxon_paired(hv, bv)`, code/stats.py:91).
`zero_method="wilcox"`, two-sided, `correction=False` (code/stats.py:42), with `n_eff`,
`n_zero_dropped`, `median_diff`, `rank_biserial` and the method always returned. Effective n below 6
never fails a criterion: `decide` returns `not met (unchecked conjunct)` before it looks at any
p-value (code/stats.py:105-106, `MIN_EFFECTIVE_N = 6`), which is 10.2a item 3a's wording exactly.
`rel_gain` (code/stats.py:58-62) excludes a zero baseline from the median and returns the count,
surfaced as `n_excluded_undefined_ratio` (code/stats.py:90) — never imputed, never capped — while the
sign test still runs on the absolute pair, so a zero baseline with a positive hybrid contributes a
`+` and a double zero drops out, as 10.2a item 4 requires. Holm is applied within F1/F2
(code/stats.py:92) and within F3 (code/evaluate.py:113-114) and nowhere else, and keeps a `None` slot
for an impossible test. The reporting duty of 10.2a item 5 is met field by field.

**(8) Verdict wording and verbatim criteria.** `verdicts.load_criteria` (code/verdicts.py:12-19)
parses plan.md's front matter and JSON-decodes the quoted `metric`, `threshold` and `on_dataset`
strings, so the criterion text in `criteria_verdicts.json` is the frozen text and not a restatement.
I ran the parser: all six criteria come back with their thresholds intact. The vocabulary is the four
fixed words (code/stats.py:12) and `_combine` (code/verdicts.py:22-28) produces `not met (unchecked
conjunct)` when one conjunct is true and another was not measured by this stage, which is why the
pilot stage reports C5 that way and leaves C6 to itself while the main stage does the reverse.

**(9) Module D reaches no model.** `behaviour.py` imports only `common` and sklearn, is imported only
by `evaluate.py`, and its single call site stores the result into the report dict
(code/evaluate.py:171). `test_behaviour_feeds_no_model` asserts the string "behaviour" appears in
none of `models.py`, `blend.py`, `cell.py`, `features.py`, `splits.py`, `provenance.py`,
`leakage.py`. Confirmed by grep as well. Note for the planner, not a code finding: plan.md's Module D
task says it supplies "Module B's cold-start prior" and RQ2 asks whether segmentation improves that
prior. The protocol's section 8 compares six models, none segmented, so the code is right to keep
Module D descriptive — but RQ2 as plan.md words it will not be answerable from this run, and chapter 5
must say so rather than let the question stand.

**(10) Assertions and unchecked.** L1 through L9 each emit a measured count including zero: L1
code/leakage.py:26-33, L2/L3/L7 through `provenance.emit` code/provenance.py:23-32, L4
code/leakage.py:36-42, L5 code/leakage.py:45-48, L6 code/leakage.py:60-61, L8 code/leakage.py:78-83,
L9 code/leakage.py:86-93. `RunLog.measure` writes the line first and then aborts
(code/common.py:119-126), so a failure is always on disk. `RunLog.unchecked`
(code/common.py:138-141) is used where a check genuinely did not run — the four late objects and L6
when `evaluate.py` is absent (code/main.py:85-88) and a presentation with no two-day learner
(code/evaluate.py:164) — and never as a substitute for a pass. L9 for the phase 1 reproduction is
emitted with `status: "not_applicable"` and `count: None`, never 0
(code/reproduce_phase1.py:199), and `criteria_verdicts.json` carries
`"assertions_L1_L9": "not applicable: no bound (protocol 5.5)"` (code/verdicts.py:42); the same
`not_applicable` route covers the tertiary split's absent training bound
(code/leakage.py:89-90, code/variants.py:72) and its L1 (code/evaluate.py:125).

**(11) The phase 1 reproduction.** `reproduce_phase1.py` copies rather than imports: it declares the
copy and the three permitted deviations at lines 3-7, and I compared it function by function against
`data/projects/e_learning_pilot/code/pilot_recommender.py`. `pick_module_presentation`,
`build_engagement_matrix`, `cosine_sim_matrix`, `minmax`, `recommend_cbf`, `recommend_cf`,
`top_k_excluding` and `evaluate` are arithmetically identical, including the pilot's default
`np.argsort(-scores)` tie order, its `exclude = set(visible_items)`, its
`alpha = min(0.9, 0.2 + 0.05 * len(visible_items))` and its division of the CF score by `w.sum()`.
`build_splits` consumes the same `default_rng(42)` in the same order (`rows[rng.permutation(n)]` is
the pilot's `order = rng.permutation(n); rows = rows[order]`). The two textual differences are
inert: `usecols=` on the `studentVle.csv` read, which cannot change a count or a sum, and
`pd.to_numeric(col, errors="coerce")` in place of `replace("?", nan)` then `to_numeric`, which maps
`'?'` to `NaN` identically. `python code/main.py --stage pilot` therefore reproduces the pilot's
arithmetic, which is what protocol 5.5 says C6 tests and all it says C6 tests. The engineer's R1
(numpy 2.5.3 argsort tie order) remains the right first suspect if C6 misses 1e-6; the code keeps the
artifacts and exits 3 rather than aborting (code/reproduce_phase1.py:195, 201), which is correct.

### The eighteen defaults, confirmed or rejected

Part 2, from `code/README.md` and decisions.log CR2:

1. **CF neighbourhood keeps the item's own similarity; `N = all` uses the full matrix**
   (code/models.py:110-122). **Confirm.** It changes no criterion-deciding number: the self term
   `H[j]·1` lands only in column `j`, which is the learner's own visible item and is excluded at
   every prediction moment, so it can never enter a top-10. Keeping it is also what reproduces the
   protocol 7.1 no-exclusion probe (0.0279). `N` is effectively "N other items"; the methodologist
   need only record that reading in 8.0a.
2. **`PopWeek` treats every item as eligible when nothing is visible at `k = 0`**
   (code/models.py:301-303). **Confirm.** At `k = 0` there is no course week to compute, and the
   alternative — nobody eligible — gives the same ranking by a worse route. It makes `PopWeek`
   identical to `MostPop` at `k = 0`, which the identity guard exempts by name. `k = 0` decides
   nothing. Record in protocol 8's `PopWeek` row.
3. **Min-max and the top-1/top-10 features are computed over the candidate set**
   (code/models.py:95-101, code/blend.py:23-26). **Confirm — and it is not a free choice:** 8.1 step
   3 says "over the learner's candidate set" and A5 defines the scaling per learner. No
   methodologist action beyond noting it was implemented as written.
4. **The CF score is not divided by the per-learner click total** (code/models.py:125-130).
   **Confirm.** Protocol 8's `ItemKNN-CF` row specifies a click-weighted *sum*, so the code follows
   the protocol and departs from the pilot deliberately. A positive per-learner constant changes no
   ranking and min-max is invariant to it, so no reported number moves. (The pilot's division is
   preserved where it belongs, in `reproduce_phase1.recommend_cf`.)
5. **Constant `alpha = 0.5` when nobody is labelled** (code/blend.py:100). **Confirm.** Only
   reachable where every learner's validation Precision@10 is 0 at every `α`, which in practice
   means `k = 0`, where the blend of two zero vectors is zero anyway. Decides nothing.
6. **Fewer than 20 labelled learners triggers the constant rule** (code/blend.py:99).
   **Confirm — protocol-mandated**, not a default: 8.1 step 2's last sentence says exactly this.
   **But one thing inside it does need the methodologist.** Step 10 defines the constant as
   `median{α*(u) : u in that presentation}`; the code takes the median over the *labelled* learners
   only (`np.median(astar[lab])`, code/blend.py:100). That is the better reading — the all-zero
   learners were dropped precisely because their `α*` of 0.5 is an artefact — but it is a different
   number, and in a small or thin presentation at `k = 2` it can move a hybrid score that C2 and C3
   are judged on. **The methodologist must confirm it and reword step 10** so the protocol and the
   code state the same population.

Part 3, from `code/README.md` and decisions.log `defaults_recorded`:

7. **`D_val` = the smallest day whose validation slice is at most 10% of the pairs**
   (code/variants.py:48-51). **Confirm, and the protocol text is wrong.** Section 5.2's literal
   "largest day such that the pairs in `(D_val, D]` number no more than 10%" is degenerate — the
   largest such day is `D` itself, giving an empty validation slice — while the same paragraph calls
   it "the same closest-to-target-without-exceeding rule as the primary split", which is what the
   code implements. Decides no criterion (5.3a), but C4 audits all splits, so **the methodologist
   must correct the word "largest" in 5.2**.
8. **Secondary and tertiary split population and handling** (code/variants.py:53-55, 58-72, with
   code/evaluate.py:50, 71). **Confirm.** Dropping and counting learners with no training pair,
   keeping learners with no test pair and excluding them from metrics with the count reported, is
   exactly ruling W4a; the tertiary split keeps the primary evaluated population, permutes in
   `id_site` order and takes `max(1, round(0.1n))` validation pairs. Both are reporting-only.
   One caveat for chapter 5: the tertiary split reproduces the pilot's *construction*, not its
   assignment, because the evaluated population differs (P4b did not exist in the pilot), so it
   must not be described as "the pilot's split".
9. **P4a and P4b coverage** (code/evaluate.py:169-170, 147-150; code/cell.py:72-81).
   **Confirm with one caveat.** P4b's two-day group, reported alone and pooled, for the warm and
   `A|2` cells, is the right scope. P4a, however, is protocol P5's "repeat the whole run at 3 and at
   10" implemented as two cells, not the whole run. It decides nothing, but the chapter-5
   sensitivity table will be narrower than the protocol promises, so **the methodologist should
   confirm the narrowing** or the protocol should say two cells.
10. **L7 rebuild at `k = 2` only on secondary and tertiary** (code/evaluate.py:128-129), with the
    primary rebuilt at every `k` (code/foundation.py:112-113). **Confirm.** The deciding split gets
    the full check; the robustness splits get a representative one at the deciding `k`. No criterion
    moves. Given [W6] this is also the right compute trade.
11. **Identical-ranking exemptions at `k = 0` and where every week field is missing**
    (code/evaluate.py:80-84). **Confirm.** Both identities are predicted by the protocol itself —
    8.0(iii) for CF/CBF/hybrid at `k = 0` and for `MostPop` = `PopWeek` there, and P5/2.3 for the
    three presentations with no known week value, whose membership is separately asserted
    (`P5_all_missing_mismatch`, code/foundation.py:83). Exempted pairs are still logged, so nothing
    is hidden. No criterion moves.
12. **Bootstrap and popularity agreement for the primary split only** (code/evaluate.py:25, 140,
    145). **Confirm as a compute decision, with a reporting duty attached** — see [W10]. It changes
    no criterion, because C1 to C3 are judged on the primary split alone (5.3a), but 10.2's "never
    as a bare number" then binds the results analyst: no secondary, tertiary or P4a figure may be
    quoted with an interval it does not have.
13. **Exact Wilcoxon only for effective n at most 50** (code/stats.py:38). **Confirm.** The deciding
    tests run at n = 22, so they are exact; the cut-off only affects the per-learner F3 tests, which
    decide nothing and where the normal approximation is the standard choice at n in the hundreds.
    No deciding number moves.
14. **Verdict wording for C5, C1 and C2** (code/verdicts.py:22-28, code/stats.py:97-109).
    **Confirm.** This is 10.2a item 3a applied literally, including the pilot stage reporting C5 as
    `not met (unchecked conjunct)` because the main-run conjunct belongs to the other run. The two
    receipts must be combined by hand, which `code/README.md` step 4 already tells the runner.
15. **C4 counting** (code/evaluate.py:135-138, 213-218). **Confirm the count, reject the label** —
    see [W1]. What is counted is the right thing (no hyperparameter object read a test row, no
    validation/test row overlap, no cell scored twice); what it is called overstates it.
16. **KMeans `k = 4`** (code/behaviour.py:16, 32-41). **Confirm.** plan.md names no `k`, Module D
    feeds no model, and the silhouette is reported beside the segmentation so the choice is
    auditable rather than asserted. It cannot move a criterion. Chapter 5 should read `k` against
    the reported silhouette rather than presenting 4 as derived.

### The two questions from the methodologist's ruling on section 5.5

**Do two-day learners truly enter no fitted object of the main run? Yes, by construction and by
measurement.** Filter P4b removes every learner with fewer than three distinct first-interaction days
*before* `Prep` is built (code/splits.py:110-111), so those learners' pairs and rows are absent from
`prep.pairs` and `prep.rows` — and those two frames are the only source every fitted object reads
(`features.bounded_rows` code/features.py:39, `features.mostpop_counts` code/features.py:106,
`Ctx.pairs_read` code/models.py:162-163). The two-day group is reconstructed separately from the raw
rows in `variants.two_day_view` (code/variants.py:75-89) and is handed to models that were already
fitted, never to a fit. The code does not rely on that argument alone: `cell.py:76` measures
`P4B_TWO_DAY_LEARNERS_IN_FIT` as `|ids2 ∩ ctx.fit_ids|`, required 0, per cell. So the ruling's
stronger claim holds — not merely "no hyperparameter is refitted", which is all 12.1 said, but "no
fitted object of the main run reads them at all". One reporting caveat: the pooled `union_P@10`
figure (code/evaluate.py:150) mixes a group that entered no fit with one that did, which chapter 5
should state when it quotes the pooled number.

**Should assertion L9 in 5.4 be reworded now that 5.5 states run-specific bounds? Yes.** 5.4's L9
still names "the training bound (the learner's first validation day)" as though it were the only one,
while 5.5 now defines three more — the global `D_val`, none at all, and the learner's second day `d_2`
— plus one run where L9 is not applicable. The code is already ahead of the text: every ledger entry
carries a `bound_kind` of `"training"` or `"cold"` (code/features.py:46), and a run whose training
bound does not exist emits `status: "not_applicable"` with `count: None` rather than 0
(code/leakage.py:89-90). Reword L9 to read "its own bound, as defined in section 4 and section 5.5"
and add `not_applicable` to the assertion's stated outcome vocabulary, so the run log and the
protocol describe the same three-valued result. This is a wording change and moves no number.

## Overall

The decision is `revise`. The substance is sound: I traced the four leaks that four review cycles
found in the design — the day-boundary split with no empty slice, the three prediction moments
including M1 at the validation boundary, the date-bounded click weights in every reader, and Condition
A's refit of all seven learner-derived objects on the 80% with an independent fresh-process rebuild —
and each is implemented as the protocol specifies and, more importantly, as a counted assertion that
aborts rather than as a comment. The blend matches all eleven points of 8.1, the statistics match
section 10 including the zero-difference, effective-n and undefined-ratio rules, the criterion text is
read verbatim out of plan.md at run time, Module D reaches no model, and the canary's six constants
match protocol 7.1 to the digit. What stops approval is not a design fault but two mechanical defects
that each make the run impossible to finish: a shape mismatch that aborts the secondary split's warm
cell on every presentation [B1], and a scoring counter that omits the split name and so fails L6 at
the end of a completed run [B2]. Both are small and local. Fix them, clear W1 through W3, and this
code is ready to run. Written by hand with Write, not by the review MCP tool, which cannot run on this
machine (`ar-workflow-engine.py` imports `fcntl`); under rule 6 the absence of the tool's automated
Constraint-Audit validation is `unchecked`, not passed, and the coordinator's decision log must carry
that deviation.

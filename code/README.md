# code/ - thesis experiment, part 1 of 3 (Modules R and A)

Interpreter: `.venv-pilot\Scripts\python.exe` (numpy 2.5.3, pandas 3.0.5, scikit-learn 1.9.1, scipy 1.18.1), with
`PYTHONDONTWRITEBYTECODE=1` and `PYTHONUTF8=1`. Nothing to install. Single CPU, no GPU, no downloaded weights.

## Entry point contract (`main.py`)

| Argument | Rule |
| --- | --- |
| `--stage pilot\|main\|iteration\|diagnostics` | required, exactly once, no default, no catch-all mode; one stage per process |
| `--artifact-dir` | required, exactly once, must lie under `results/run_artifacts/`, must be empty or absent |
| `--run-log` | required, exactly once, must be `results/run.log`, opened append-only |
| `--only <presentation>` | optional, main/iteration/diagnostics only |
| `--dry-run` | optional, validates and exits 0 writing nothing |

Invalid arguments exit non-zero before any file is created or any data is read. The first file written is
`run_manifest.json` (stage, absolute paths, argv, command line, seed, config and code-tree SHA256, versions, hardware); the last is
`run_summary.json` (status, wall seconds, `cpu_hours`, assertion counts, unchecked list). Exit codes: 0 ok, 1 abort, 3 C6 not met.

```
.venv-pilot\Scripts\python.exe code\main.py --stage pilot       --artifact-dir results\run_artifacts\<unit> --run-log results\run.log
.venv-pilot\Scripts\python.exe code\main.py --stage main        --artifact-dir results\run_artifacts\<unit> --run-log results\run.log
.venv-pilot\Scripts\python.exe code\main.py --stage diagnostics --artifact-dir results\run_artifacts\<unit> --run-log results\run.log
.venv-pilot\Scripts\python.exe -m pytest code\tests -q      (or: python code\tests\test_metrics.py)
```

`pilot` = `reproduce_phase1.py` (C6; writes `phase1_reproduced_metrics.json`, deterministic content). `main`/`iteration` = foundation
checks per presentation (`foundation_<pres>.json`), then `evaluate.run_presentation(prep, ctx)` if `code/evaluate.py` exists.
`diagnostics` = `diagnostics.py` (unit u13b_diag_code; see "Diagnostics (D1, D2)" below); decides no criterion.

## Files -> plan modules

`reproduce_phase1.py` R | `data.py` (SHA256 verified load, P5 item features), `splits.py` (pairs, P4a/P4b, day-boundary split,
cohort draw 6.1b, Condition), `features.py` (bounded clicks, active days, visible history, engagement/similarity, exclusion sets,
BUILDERS), `provenance.py`, `leakage.py` (L1-L9, V checks, fresh-process rebuild), `rebuild_worker.py`, `foundation.py` A |
`metrics.py`, `tests/test_metrics.py` | `common.py` constants, RunLog, hashing | `configs/experiments.json`.

## Fixed interfaces for parts 2 and 3

- `foundation.prepare(oulad, pres, log) -> splits.Prep` (built once; `prep.pairs` role 0/1/2 = train/val/test, `prep.learners`,
  `prep.rows`, `prep.item_ids` ascending, `prep.features` CBF item matrix, `prep.cohort_A`, `prep.cohort_R`, `prep.hashes`).
  `data.load_oulad(log) -> Oulad`.
- `splits.make_condition(prep, "warm"|"A"|"A_robust"|"B", k) -> Condition(name, k, fit_ids, eval_ids, cold_ids)`. Every fit uses
  `fit_ids` only; `Condition.expected_cold_in_fit` is 0 except B (= |C|).
- `splits.split_view(prep) -> SplitView` is what EVERY model receives; `leakage.l5(log, prep, {model: view})` re-hashes it.
- Weights: `features.train_weights(prep, ids, label)` (training bound, strict) and `features.visible_history(prep, ids, k, label)`
  -> `Visible(pairs with clicks, bound, active_days)` (cold bound, inclusive). Never sum `sum_click` any other way: all weights go
  through `features.bounded_rows`, which ledgers each call; call `leakage.l9_flush(log, **ctx)` after every fit/score block.
- Fitting: `features.engagement_matrix`, `features.gram_cosine`, `features.mostpop_counts` return the frame they read; pass it to
  `provenance.record(name, read, prep, allowed_ids, roles, cold_ids)` then `provenance.emit(log, rec, cond.expected_cold_in_fit,
  check="L2"|"L3", pres=, condition=, k=)`. Part 2 must emit records for `N_selection`, `C_selection`, `blend_model`,
  `blend_standardiser` and call `provenance.coverage(log, provenance.SEVEN_OBJECTS, ...)`. Learner-derived constants use check="L3".
- Fresh-process rebuild: register builders in `features.BUILDERS[name] = (fn(view, cond) -> sha256 hex, depends_on_k)` from a module
  listed in `configs/experiments.json` `builder_modules`; builders may read only `view` (pairs, rows, learners, item_ids) and
  `cond["fit_ids"]`, `cond["k"]`. Then `leakage.l7_rebuild(log, prep, cond, ks, pres=, condition=)` covers all seven objects.
- Exclusion: `features.exclusion_sets(prep, ids, "M1"|"M2"|"M3", visible)`; after scoring call
  `leakage.l8(log, prep, moment, used_sets_actually_applied, ids, truth_role, k=, ...)`. `leakage.ScoreCounter.scored_test(model,
  split, pres, condition, k, seed)` once per test scoring, then `.check(log)` (L6). `split` is required (G4 cycle-0 blocker B2):
  the same (condition, k) cell runs on five splits of one presentation, and without it they collide on one counter key.
- Ranking and metrics: `metrics.rank_topk(scores, prep.item_ids, exclusion, k)` for EVERY model (score desc, id_site asc, 12-decimal
  rounding, raises on non-finite), `metrics.aggregate(rankings, truths)`, `coverage_at_k`, `n_short_lists`. Part 3 must add the
  identical-rankings-across-models guard, bootstrap, Wilcoxon/Holm, and Random via `default_rng([s, presentation_index, learner_index])`.
- `common.RunLog`: `measure` (abort on mismatch), `flag` (advisory), `unchecked`, `emit`. Seeds: `common.SEED`, `common.RANDOM_SEEDS`.
- Canary for the cohort draw (rank order, not id order): EEE_2014J, k=2, Condition A, MostPop exclusion=visible must give 0.0255.

## Part 2 (Module B) - what part 3 calls

- `cell.run_cell(prep, cond, log, counter, length, pres_index, split, extra=None) -> CellResult(ids, scores, excl, truth, item_ids,
  info, extra)`. `split` is the split name ("primary", "secondary", "tertiary", "P4a_3", "P4a_10"); it is required, goes into the
  cell's log context and into `ScoreCounter.scored_test`. Fits and
  scores one (presentation, condition, k): `scores["Random|42".."Random|46"]`, `"MostPop"`, `"PopWeek"`, `"CBF"`, `"ItemKNN-CF"`,
  `"Hybrid"`, each (n_learners, n_items). `length` = `oulad.length[pres]`, `pres_index` = index in `sorted(oulad.rows)`.
  Rank with `models.rank_lists(res.scores[key], res.excl, res.item_ids, 20)`; truth sets from `res.truth` (bool mask); then
  `metrics.aggregate`. Warm: eval = all learners, exclusion M2; cold: eval = the cohort, exclusion M3. It emits L2/L3/L7 for all seven
  objects (Condition B: L7 emitted as `info`, expected non-zero), L8 at both moments, L9, A5, the parity count and `cell_fit`
  (N, alpha_model, C, label-grid count, share of all-zero learners dropped, warm feature shift).
- L6: create one `leakage.ScoreCounter()` per run, pass it to every `run_cell`, call `counter.check(log)` once at the end.
- Part 3 still owes: the identical-rankings-across-models guard, metrics per cell, coverage/diversity/popularity agreement, bootstrap,
  Wilcoxon/Holm, C1-C6 verdicts, `evaluate.run_presentation(prep, ctx)`, the secondary/tertiary/P4b splits, and C4's count of
  hyperparameters fitted outside validation. Cells to run per presentation: warm; A and B at k in {0,1,2,5}; A_robust at k=2.
- `python code/tests/canary_eee_2014j.py` (about a minute, writes nothing) must print OK for all six values before a full run.
- Decisions taken where the protocol is silent (report to the methodologist): CF neighbourhood keeps the item's own similarity and
  its N most similar other items; PopWeek treats every item as eligible when nothing is visible (k = 0); min-max scaling and the
  top-1/top-10 features are over the candidate set; the CF score is not divided by the click total (a per-learner constant).

## Not done in part 1 (see the return notes)

Secondary global cut-off split, tertiary random split, P4a/P4b sensitivity reruns, A5 counter, Condition A/B objects N, C, blend
(parts 2-3). L6 is `unchecked` until models score. `week_missing_share` etc. are in `prep.feature_constants`.

## Part 3 (Modules C and D) and how the runner executes everything

Files: `evaluate.py` (metrics per cell, identical-rankings guard, popularity agreement, per-learner F3 tests and bootstrap intervals,
C1-C4 across presentations, reporting tables), `stats.py`, `verdicts.py` (plan.md threshold text verbatim), `variants.py` (secondary,
tertiary, P4b two-day view; P4a uses `build_prep(min_items=)`), `behaviour.py` (descriptive only, feeds no model).
Each main/iteration run writes: `run_manifest.json` (first), `foundation_<pres>.json`, `results_<pres>.json`,
`results_summary.json`, `criteria_verdicts.json`, and `run_summary.json` (last: status, exit code, wall seconds, process CPU seconds,
child-worker seconds, `cpu_hours` = both added, hardware, every criterion verdict, every assertion count, the unchecked list, FLAGs).

Run in this order, from the project root, in PowerShell (a fresh artifact directory for every attempt; a crashed run leaves files
behind and the entry point refuses a non-empty directory):

    $env:PYTHONDONTWRITEBYTECODE="1"; $env:PYTHONUTF8="1"
    $py = "D:\Work\Projects\AutoResearch\.venv-pilot\Scripts\python.exe"; cd D:\Work\Projects\AutoResearch\data\projects\e_learning_thesis

1. Metric and statistics tests (seconds): `& $py code\tests\test_metrics.py` then `& $py code\tests\test_evaluate.py`.
   Expect one `ok test_...` line per test and exit 0 (an AssertionError names the failing test; stop if any fails).
2. Contract refusal (no file may appear): `& $py code\main.py --stage main --run-log results\run.log` must exit 2 saying
   `--artifact-dir` is required; and `& $py code\main.py --stage main --artifact-dir results\run_artifacts\<unit> --run-log results\run.log --dry-run`
   must print `dry run ok` and create nothing.
3. Canary (about 1-2 minutes, writes nothing): `& $py code\tests\canary_eee_2014j.py`. Expect two table rows, both ending `OK`, exit 0:
   MostPop 0.0137 / 0.0255 / 0.2157 and ItemKNN-CF 0.0279 / 0.0333 / 0.1946. Any MISMATCH: stop and report; do not start the main run.
4. Phase 1 reproduction (about 1 minute, limit 15): `& $py code\main.py --stage pilot --artifact-dir results\run_artifacts\<pilot unit> --run-log results\run.log`.
   Expect exit 0; files `run_manifest.json`, `phase1_reproduced_metrics.json`, `criteria_verdicts.json`, `run_summary.json`; in the log two
   `data_sha256` lines with `manifest_match: true`, `C6_values_beyond_1e-6` count 0 status pass, `C5_reproduction_minutes_over_15` count 0,
   `P1_selected_presentation_is_EEE_2014J` count 0, and L9 / L1-L8 lines with `status: not_applicable`. `criteria_verdicts.json`: C6 `met`,
   C5 `not met (unchecked conjunct)` (the main-run conjunct belongs to the main run; combine the two receipts by hand). Exit 3 means C6 missed
   1e-6: keep the files and do not quote phase 2 numbers until explained (first suspect: numpy argsort tie order).
5. Timing run on one presentation: `& $py code\main.py --stage iteration --artifact-dir results\run_artifacts\<iteration unit> --run-log results\run.log`
   (EEE_2014J only). Expect exit 0, `T41_population_cells_differing` 0, `REF_EEE_2014J_cells_differing` 0, `D_TABLE_MISMATCH` 0, every
   `assert` line `status: pass` (Condition B L7 lines `status: info`; tertiary L1 and training-bound L9 lines `not_applicable`; a FLAG
   such as `IDENTICAL_RANKINGS_PAIRS` or `SPLIT_FRACTIONS_OUT_OF_RANGE` does not abort but must still be investigated),
   `results_EEE_2014J.json`, and C1-C3 `unchecked` (one presentation only). **`cpu_hours` x 22 is a lower bound, not an estimate**
   (G4 cycle-0 warning W6): `foundation.verify` runs two fresh-process rebuilds per presentation, each refitting all seven
   learner-derived objects at all four k values (eight full blend fits per rebuild, once in-process and once again in the
   worker), and `evaluate.run_presentation` then runs 34 cells per presentation (5 splits x warm/A-at-4-k/A_robust/B-at-4-k, plus
   the two narrow P4a reruns). EEE_2014J (1,018 learners, 115 items) is also one of the cheaper presentations; `cf_scores` costs
   O(visible items x learners x catalogue) per call, and CCC_2014J alone has 2,131 learners. Treat `cpu_hours x 22` as a floor,
   watch the first two or three presentations of the main run, and stop for the human (protocol 12.1) well before the running
   total would reach 4.0, not only after it does.
6. Main run: `& $py code\main.py --stage main --artifact-dir results\run_artifacts\<main unit> --run-log results\run.log`. Expect exit 0,
   22 `results_<pres>.json`, `results_summary.json`, `criteria_verdicts.json` with six verdicts, and in `run_summary.json`: `unchecked` empty.
   **Do not expect `flags` empty** -- `IDENTICAL_RANKINGS_PAIRS` and `SPLIT_FRACTIONS_OUT_OF_RANGE` are `log.flag`, not `log.measure`
   (a legitimate tie, e.g. a degenerate CBF profile, can flag and let the run continue), so a clean exit-0 run may still carry
   entries in `flags`. Investigate every entry in `flags` before quoting the numbers it touches, the same as any FLAG; do not treat
   a non-empty `flags` list by itself as a failed run. `criteria.C6` `unchecked`
   (decided by step 4). Exit 1: the last `abort` line of `results\run.log` names the failing assertion and count. Hash every file in the
   artifact directory for the receipt, including `criteria_verdicts.json` and `run_summary.json`.

## Diagnostics (D1, D2) -- unit u13b_diag_code

Two diagnostics the human approved after the main run, both explicitly designed to decide no criterion (`criteria_verdicts.json`
from a diagnostics run is all `unchecked`, same as any stage that never touches `ctx["stats"]`/`ctx["acc"]`). Design choice: a
fourth `--stage diagnostics` value on the existing entry point, routed to a new `diagnostics.py`, rather than folding D1/D2 into
`main`/`iteration` -- the main run's cell composition, provenance, leakage checks and criteria stay byte-for-byte what they were
before this unit, and a diagnostics run is a separate, independently receiptable process with its own `run_manifest.json` /
`run_summary.json` / `criteria_verdicts.json`. Both diagnostics reuse the unmodified production code (`splits.build_prep`,
`splits.make_condition`, `models.Ctx`, `models.make_history`, `blend.fit_blend`, `evaluate.cell_metrics`) through the same kind of
`Ctx` a main-run cell builds; `cell.run_cell` itself is never called and never modified, so the split, exclusion, bound and filter
logic and every protocol number are untouched.

```
.venv-pilot\Scripts\python.exe code\main.py --stage diagnostics --artifact-dir results\run_artifacts\<unit> --run-log results\run.log
```

- **D1, alpha logging.** On condition A at k=2 (the "A|2" cold-start-refit cell), for every test-scored learner: the fitted alpha
  `models.Hybrid.score` actually used (captured as `Hybrid.alpha_` inside `score`, a one-line, output-preserving addition -- the
  returned scores are unchanged), the learner id, and k=2 (the cell's visible-item count, logged explicitly per record per the
  approved scope even though it is constant across a presentation's A|2 cell). One JSON object per line, one file per presentation:
  `results\run_artifacts\<unit>\alpha_log_<presentation>.jsonl`, 22 files, keys `presentation`, `learner_id`, `k`, `alpha`.
- **D2, behavioural-signal ablation.** A new model variant, `models.HybridAblated` (key `"Hybrid_ablated"`), fits the same blend
  procedure (`blend.fit_blend`, same C-selection grid and CV, same seed 42) over `blend.blend_features(..., ablate=True)`, which
  drops `blend.BEHAVIOURAL_COLUMNS` -- `n_visible`, `log1p_visible_clicks` (click-volume) and `n_active_days` (active-day) -- from
  the 8-column feature matrix (`blend.FEATURE_NAMES`), keeping the four CF/CBF-derived features and `week_missing_share`
  (`blend.ABLATED_FEATURE_NAMES`). `blend_features`/`fit_blend` default to `ablate=False` and are unchanged for every existing
  caller; `HybridAblated` is never added to `cell.run_cell`'s `fitted` list, so the production `Hybrid`'s fit, cache and
  provenance records are untouched even when both models share one `Ctx` in `diagnostics.py` (`Ctx.blend_ablated` is memoised
  under its own key, separate from `Ctx.blend`). Scored on the warm cell and the A|2 cold-start cell, alongside (not instead of)
  the production Hybrid, for all 22 presentations, using `evaluate.cell_metrics` -- the same function the main run uses -- so
  Precision@10 and every other cell metric (`P@5/10/20`, `R@`, `HR@`, `MRR@`, `NDCG@`, `coverage@10`, `empty_lists`,
  `diversity@10`) are computed identically for both models. One file per presentation:
  `results\run_artifacts\<unit>\ablation_<presentation>.json`, 22 files, `{"pres", "cells": {"warm|None", "A|2"}}`, each cell
  `{"condition", "k", "n_scored", "n_excluded_no_truth", "ceiling_p10", "models": {"Hybrid": {...}, "Hybrid_ablated": {...}}}`.

Runner checklist: run after the main run's 22 `results_<pres>.json` exist (D1/D2 do not depend on them, but they are the point of
comparison); expect exit 0, 22 `alpha_log_<pres>.jsonl` files, 22 `ablation_<pres>.json` files, `criteria_verdicts.json` all
`unchecked`, and `run_summary.json.assertions.unchecked` empty (diagnostics emits no `log.unchecked` entries; it runs no L1-L9
leakage check and asserts no criterion, by design -- it is additional logging alongside the pipeline, not a leakage-checked stage).
A `ValueError: ... non-finite or mis-shaped diagnostic scores` or `... alpha outside [0, 1]` aborts the run (same guards
`models.score_test` and `blend.Blend.alpha` already use); the log's last `abort` line names the presentation and model.

## Defaults chosen where the protocol was silent (part 3)

D_val is the smallest day whose validation slice does not exceed 10% of the pairs; the tertiary split keeps the primary evaluated population,
permutes pairs in id_site order and takes validation = max(1, round(0.1 n)); secondary learners with no training pair are dropped and counted,
learners with no test pair stay and are excluded from metrics; selection of N, C and the blend uses only fitted learners that have validation
ground truth; the L7 fresh-process rebuild on secondary and tertiary runs at k = 2 only; child-worker wall seconds are added to CPU time;
identical-ranking exemptions (k = 0 CF/CBF/hybrid, MostPop = PopWeek at k = 0 and where all weeks are missing); Kendall tau and overlap only for
Condition A of the primary split; bootstrap intervals and F3 tests only for the warm and A k=2 cells of the primary split; P4b reports the
two-day group alone and pooled with the cell's evaluated learners; Module D uses KMeans with k = 4.

---
status: completed
experiment_stage: main
exit_code: 0
debug_rounds_used: 0
venv_prefix: D:/Work/Projects/AutoResearch/.venv-pilot
started_at: 2026-09-22T08:48:34Z
ended_at: 2026-09-22T09:52:00Z
---

# Summary

This unit (`u11_s5_run_main`) covers two receipted runs against the reviewed, G4-approved code
(`code_tree_sha256 = 694c3ea6026939967a6b01ab0698ef7336e77a8dd29f0739157e9f9662b0231c`, confirmed
identical in both run manifests to the value recorded at gate G4 cycle 2):

1. **Pilot stage** (`results/run_artifacts/u11_s5_run_main_pilot/`) -- `--stage pilot`, the phase 1
   reproduction on EEE_2014J that decides C6 and the reproduction half of C5.
2. **Main stage** (`results/run_artifacts/u11_s5_run_main/`) -- `--stage main`, all 22 OULAD module
   presentations, that decides C1-C4 and the main-run half of C5.

Both stages exited 0, no debug round was needed (all commands ran clean on the first attempt), and
`code/tests/test_metrics.py` (11 tests), `code/tests/test_evaluate.py` (5 tests), the four
entry-point refusal cases and `code/tests/canary_eee_2014j.py` (both rows OK, exact match) all
passed before either stage ran -- **unreceipted**: no receipt field and no `run.log` line records
these passes (the log's first event is the pilot `start`), so their execution is `unchecked`
rather than verified, though the files exist and the `def test_` counts match as claimed.

## Verdict

Judged against `plan.md`'s `success_criteria` block, in order, wording per `methodology/protocol.md`
section 10 (`met` / `not met` / `not met (unchecked conjunct)` / `unchecked`):

- **C1** (Precision@10 gain, hybrid vs. CBF AND vs. CF, warm slice, `>= +0.10` relative median AND
  Holm-corrected paired Wilcoxon p < 0.05, both comparisons, n = 22): expected `>= +0.10` and
  `p_holm < 0.05` against both baselines; actual `vs_CBF` median +31.20%, Wilcoxon p = 0.005929,
  p_holm = 0.011857 (n_eff = 22); `vs_CF` median +10.68%, Wilcoxon p = 0.014095, p_holm = 0.014095
  (n_eff = 22); both conjuncts (threshold and significance) hold for both comparisons.
  **met**. Artifact: `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C1`.
- **C2** (Precision@10 gain, hybrid vs. CF AND vs. CBF, cold-start-refit slice, `> 0` relative
  median AND Holm-corrected p < 0.05, both comparisons, n = 22): expected `> 0` and `p_holm < 0.05`
  against both baselines; actual `vs_CF` median +7.32%, p_holm = 0.000241 (n_eff = 21, one zero
  difference dropped) -- this conjunct alone would pass; `vs_CBF` median **-30.28%**, p_holm =
  0.000241 (n_eff = 22) -- median is below zero, so the "both baselines" requirement fails outright
  regardless of significance.
  **not met**. Artifact: `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C2`.
- **C3** (cold-start Precision@10 `>=` CBF AND `>` MostPop AND 0 empty top-10 lists AND `>= 10%`
  catalogue coverage, all four conjuncts, in every one of the 22 presentations): expected all four
  conjuncts true in all 22; actual -- `gt_mostpop` true in 22/22, `empty_lists = 0` in 22/22,
  `coverage10 >= 0.10` in 22/22, but `ge_cbf` true in only **2 of 22** (CCC_2014J, DDD_2013B); the
  other 20 presentations fail the `ge_cbf` conjunct (hybrid below CBF on cold start), so the
  per-presentation universal quantifier is not satisfied.
  **not met**. Artifact: `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C3`
  (`failing` list names all 20; `note` field records protocol 10.5's rule that a shortfall inside
  the bootstrap interval is still `not met`).
- **C4** (0 shared rows val/test AND 0 hyperparameters fitted outside validation AND test split
  scored exactly once per model per presentation): expected all three `== 0`/`== 1`; actual
  `val_test_shared_rows = 0`, `train_val_shared_rows = 0`, `train_test_shared_rows = 0`,
  `hyperparameter_rows_reading_test_data = 0` (2,992 hyperparameter records), `max_test_scoring_count
  = 1` over 7,920 scoring cells.
  **met**. Artifact: `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C4`.
- **C5** (`<= 4.0` CPU-hours main run AND `<= 15` minutes phase-1 reproduction, single CPU, no GPU):
  expected both `<=` their budgets; actual -- reproduction conjunct (pilot stage)
  **0.238 minutes** (14.27 seconds of the 15-minute budget, `results/run_artifacts/u11_s5_run_main_pilot/criteria_verdicts.json#C5`)
  and main-run conjunct (main stage) **1.0140 CPU-hours** (`process_cpu_seconds` 2798.41 +
  `child_worker_wall_seconds` 852.02, wall-clock 3769.12 s = 62.8 minutes,
  `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C5`). Each stage's own file records
  its own conjunct as `not met (unchecked conjunct)` because neither stage alone can see the other's
  number (README step 4/5: "combine the two receipts by hand"). Combined here: both conjuncts hold
  individually (0.238 <= 15, and 1.014 <= 4.0), so the conjunction is true.
  **met** (combined by hand from both receipts; each individual receipt still correctly reads
  "not met (unchecked conjunct)" in isolation).
- **C6** (absolute difference, reproduced vs. recorded phase-1 Precision@10, all 6 values,
  `<= 1e-6`, with receipt SHA256 and exact command line): expected `<= 1e-6` for all 6 values;
  actual all 6 `abs_diff_precision_at_10` values are exactly **0.0** (warm.cbf, warm.cf,
  warm.hybrid, cold_start.cbf, cold_start.cf, cold_start.hybrid), `max_abs_diff = 0.0`, tolerance
  1e-6; `assertions_L1_L9` recorded as `not applicable: no bound (protocol 5.5)`, never as 0, per
  the run log's L9 line and the dispatch instruction.
  **met**. Artifact: `results/run_artifacts/u11_s5_run_main_pilot/phase1_reproduced_metrics.json`,
  `results/run_artifacts/u11_s5_run_main_pilot/criteria_verdicts.json#C6`, receipt
  `results/run_receipts/u11_s5_run_main_pilot.json`.

## The central finding

Under the corrected, receipted design (time-based split, cold-start similarity genuinely refitted
without the held-out learners, learned blend weight, popularity baseline, Holm-corrected
significance): **the hybrid beats collaborative filtering on cold start (median +7.3% relative,
p_holm = 0.00024, n = 22) but loses to content-based filtering on cold start (median -30.3%
relative, p_holm = 0.00024, n = 22)**. This is the opposite pattern from the unreceipted phase 1
pilot, whose `criterion_2_cold_start_hybrid_vs_cbf` reported the hybrid beating CBF on cold start in
22 of 22 presentations (median +73.12%, range +13.55% to +163.85%) while never being checked against CF at all under a design
this protocol found under-specified (`decisions.log`, S3 integrity violations; `methodology/protocol.md`
section 6). C2 is refuted specifically because it requires beating **both** baselines, and the
CBF comparison -- the one direction the pilot got right by construction and never tested against
CF -- is exactly where the corrected design fails. On the warm-user slice the hybrid clears both
baselines by a wide, significant margin (C1 met, median +31.2% vs. CBF, +10.7% vs. CF), so the
warm-user half of the hypothesis holds; the cold-start half, which the plan's Risks section named
as "the decisive one" for the hybrid vs. CF, does hold in the CF direction but not in the CBF
direction C3 also requires as a floor.

## Key Metrics (medians over 22 presentations, primary split)

| Metric | vs. CBF | vs. CF |
| --- | --- | --- |
| Warm Precision@10 relative gain (decides C1) | +31.20% (p_holm 0.011857) | +10.68% (p_holm 0.014095) |
| Cold-start-refit Precision@10 relative gain (decides C2) | -30.28% (p_holm 0.000241) | +7.32% (p_holm 0.000241, n_eff 21) |
| Cold-start-refit Precision@10 relative gain vs. MostPop (F4, reporting only) | -- | +76.46% (p_holm 9.5e-07) |
| C3 all-four-conjuncts pass rate | 2 / 22 (CCC_2014J, DDD_2013B) | n/a |
| C4 leakage count | 0 shared rows, 0 out-of-validation hyperparameters | -- |
| C5 (combined) | 0.238 min reproduction + 1.014 CPU-h main run | budget 15 min + 4.0 CPU-h |
| C6 max abs. diff vs. phase-1 pilot | 0.0 (tolerance 1e-6) | -- |

## Per-presentation table (all 22 module presentations)

`warm` = primary-split warm-user held-out slice; `cold` = Condition A cold-start-refit slice at
k = 2 (the cell that decides C2/C3). All Precision@10 values are per-presentation macro means.

| module_presentation | n_items | n_eval (warm/cold) | warm MostPop | warm CBF | warm CF | warm Hybrid | warm Hybrid vs CBF | warm Hybrid vs CF | cold MostPop | cold CBF | cold CF | cold Hybrid | cold Hybrid vs CBF | cold Hybrid vs CF |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AAA_2013J | 211 | 375/75 | 0.1819 | 0.2816 | 0.1845 | 0.2595 | -7.9% | +40.6% | 0.0120 | 0.1280 | 0.0253 | 0.0693 | -45.8% | +173.7% |
| AAA_2014J | 202 | 347/69 | 0.1896 | 0.2288 | 0.1937 | 0.2383 | +4.2% | +23.1% | 0.0145 | 0.1058 | 0.0275 | 0.0464 | -56.2% | +68.4% |
| BBB_2013B | 315 | 1404/281 | 0.1630 | 0.1217 | 0.1521 | 0.1709 | +40.4% | +12.3% | 0.0278 | 0.0829 | 0.0623 | 0.0676 | -18.5% | +8.6% |
| BBB_2013J | 321 | 1700/340 | 0.1564 | 0.1007 | 0.1365 | 0.1549 | +53.8% | +13.4% | 0.0344 | 0.0612 | 0.0485 | 0.0597 | -2.4% | +23.0% |
| BBB_2014B | 311 | 1163/233 | 0.1387 | 0.1023 | 0.1302 | 0.1583 | +54.7% | +21.6% | 0.0386 | 0.0609 | 0.0536 | 0.0571 | -6.3% | +6.4% |
| BBB_2014J | 207 | 1773/355 | 0.1504 | 0.1737 | 0.1221 | 0.1553 | -10.6% | +27.3% | 0.0177 | 0.0701 | 0.0394 | 0.0423 | -39.8% | +7.1% |
| CCC_2014B | 196 | 1557/311 | 0.1699 | 0.1837 | 0.1836 | 0.2182 | +18.8% | +18.9% | 0.0434 | 0.0881 | 0.0511 | 0.0534 | -39.4% | +4.4% |
| CCC_2014J | 223 | 2131/426 | 0.1599 | 0.1673 | 0.1764 | 0.2085 | +24.6% | +18.2% | 0.0484 | 0.0516 | 0.0624 | 0.0589 | +14.1% | -5.6% |
| DDD_2013B | 428 | 1150/230 | 0.1423 | 0.0923 | 0.1650 | 0.1678 | +81.9% | +1.7% | 0.0209 | 0.0357 | 0.0591 | 0.0613 | +72.0% | +3.7% |
| DDD_2013J | 462 | 1656/331 | 0.1412 | 0.0838 | 0.1268 | 0.1222 | +45.9% | -3.6% | 0.0314 | 0.0982 | 0.0335 | 0.0779 | -20.6% | +132.4% |
| DDD_2014B | 453 | 1040/208 | 0.1495 | 0.0941 | 0.1437 | 0.1480 | +57.2% | +2.9% | 0.0312 | 0.0952 | 0.0404 | 0.0437 | -54.0% | +8.3% |
| DDD_2014J | 365 | 1523/305 | 0.1540 | 0.1248 | 0.1588 | 0.1731 | +38.7% | +9.1% | 0.0341 | 0.0675 | 0.0367 | 0.0439 | -35.0% | +19.6% |
| EEE_2013J | 112 | 898/180 | 0.1821 | 0.1138 | 0.2099 | 0.1551 | +36.3% | -26.1% | 0.0189 | 0.0456 | 0.0339 | 0.0339 | -25.6% | +0.0% |
| EEE_2014B | 109 | 584/117 | 0.1945 | 0.0974 | 0.2111 | 0.1664 | +70.8% | -21.2% | 0.0214 | 0.0795 | 0.0393 | 0.0598 | -24.7% | +52.2% |
| EEE_2014J | 115 | 1018/204 | 0.2116 | 0.1511 | 0.1877 | 0.1691 | +11.9% | -9.9% | 0.0255 | 0.0407 | 0.0343 | 0.0343 | -15.7% | +0.0% |
| FFF_2013B | 508 | 1460/292 | 0.2055 | 0.2427 | 0.2221 | 0.2282 | -6.0% | +2.7% | 0.0120 | 0.1110 | 0.0274 | 0.0295 | -73.5% | +7.5% |
| FFF_2013J | 529 | 1989/398 | 0.2015 | 0.1772 | 0.2061 | 0.2234 | +26.1% | +8.4% | 0.0141 | 0.0754 | 0.0399 | 0.0384 | -49.0% | -3.8% |
| FFF_2014B | 478 | 1281/256 | 0.2098 | 0.1613 | 0.2308 | 0.2304 | +42.9% | -0.2% | 0.0176 | 0.0555 | 0.0305 | 0.0305 | -45.1% | -0.0% |
| FFF_2014J | 452 | 1988/398 | 0.2164 | 0.1260 | 0.2149 | 0.2198 | +74.5% | +2.3% | 0.0186 | 0.0379 | 0.0304 | 0.0312 | -17.9% | +2.5% |
| GGG_2013J | 137 | 835/167 | 0.1131 | 0.2320 | 0.1114 | 0.2153 | -7.2% | +93.3% | 0.0341 | 0.0503 | 0.0377 | 0.0383 | -23.8% | +1.6% |
| GGG_2014B | 124 | 705/141 | 0.1159 | 0.2465 | 0.1112 | 0.1549 | -37.2% | +39.3% | 0.0319 | 0.1418 | 0.0376 | 0.0482 | -66.0% | +28.3% |
| GGG_2014J | 106 | 635/127 | 0.1241 | 0.2665 | 0.1109 | 0.2351 | -11.8% | +112.1% | 0.0283 | 0.1732 | 0.0291 | 0.0693 | -60.0% | +137.8% |
| **median** | -- | -- | 0.1615 | 0.1562 | 0.1707 | 0.1720 | -- | -- | 0.0266 | 0.0728 | 0.0377 | 0.0473 | -- | -- |
| **min** | -- | -- | 0.1131 | 0.0838 | 0.1109 | 0.1222 | -- | -- | 0.0120 | 0.0357 | 0.0253 | 0.0295 | -- | -- |
| **max** | -- | -- | 0.2164 | 0.2816 | 0.2308 | 0.2595 | -- | -- | 0.0484 | 0.1732 | 0.0624 | 0.0779 | -- | -- |

Every value above is read directly from `results/run_artifacts/u11_s5_run_main/results_<pres>.json`
(`splits.primary.cells["warm|None"]` and `["A|2"]`, `models.<model>["P@10"].mean`), not retyped
from an aggregate.

## Per-module breakdown (protocol 10.4: the 22 presentations are 7 modules, not 22 independent draws)

| Module | C1 vs. CBF (relative) | C1 vs. CF (relative) | C2 vs. CBF (relative) | C2 vs. CF (relative) |
| --- | --- | --- | --- | --- |
| AAA | -1.9% | +31.8% | -51.0% | +121.1% |
| BBB | +47.1% | +17.5% | -12.4% | +7.9% |
| CCC | +21.7% | +18.5% | -12.7% | -0.6% |
| DDD | +51.6% | +2.3% | -27.8% | +14.0% |
| EEE | +36.3% | -21.2% | -24.7% | ~0.0% |
| FFF | +34.5% | +2.5% | -47.0% | +1.2% |
| GGG | -11.8% | +93.3% | -60.0% | +28.3% |

No single module drives either result: the warm-user CBF gain (C1) is positive in 5 of 7 modules,
and the cold-start CBF loss (C2's refuting conjunct) is negative in all 7 modules.

## C3 per-presentation conjunct detail

`ge_cbf` is the conjunct that fails; `gt_mostpop`, `empty_lists == 0` and `coverage10 >= 10%` hold
everywhere. Full per-presentation values (hybrid, CBF, MostPop cold-start Precision@10, coverage,
bootstrap CI of the hybrid-vs-CBF and hybrid-vs-MostPop differences) are in
`results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C3.values.per_presentation`.

- Pass all four conjuncts (2/22): **CCC_2014J** (hybrid 0.0589 >= CBF 0.0516), **DDD_2013B**
  (hybrid 0.0613 >= CBF 0.0357).
- Fail on `ge_cbf` only (20/22): AAA_2013J, AAA_2014J, BBB_2013B, BBB_2013J, BBB_2014B, BBB_2014J,
  CCC_2014B, DDD_2013J, DDD_2014B, DDD_2014J, EEE_2013J, EEE_2014B, EEE_2014J, FFF_2013B,
  FFF_2013J, FFF_2014B, FFF_2014J, GGG_2013J, GGG_2014B, GGG_2014J.
- Per protocol 10.5, a shortfall inside the bootstrap interval is still `not met`; several rows
  above (e.g. BBB_2013J, diff_vs_cbf_ci95 = [-0.0126, +0.0097]) have a CI crossing zero and are
  still counted as failing, exactly as pre-declared.
- Per protocol 10.5, cold-start Precision@10 of 0.02-0.03 is not itself evidence of model failure;
  it is read against `ceiling_p10` (0.65-0.94 across presentations), which the table above supplies.

## Sensitivity and robustness (F4, exploratory -- decide no criterion)

| Check | warm vs. CBF | warm vs. CF | cold (A, k=2) vs. CBF | cold (A, k=2) vs. CF |
| --- | --- | --- | --- | --- |
| Primary split (decides C1/C2) | +31.20% | +10.68% | -30.28% | +7.32% |
| Secondary split (global cut-off) | -3.77% (sign reversal) | +18.63% | -51.03% | +85.30% |
| Tertiary split (pilot's random 20%) | +167.11% | -3.57% (sign reversal) | +105.56% (sign reversal) | -3.99% (sign reversal) |
| P4a, item threshold 3 | +31.20% | +10.70% | -28.24% | +11.31% |
| P4a, item threshold 10 | +30.16% | +10.71% | -29.71% | +7.09% |

- The **secondary split** reverses the warm-vs-CBF sign (primary +31.2% -> secondary -3.8%) but
  leaves the cold-start pattern (CBF loss, CF win) qualitatively unchanged.
- The **tertiary split** (the pilot's original random 20% holdout) reverses three of the four
  signs relative to the primary split -- a reminder, consistent with protocol 5.3, that this split
  is reported for continuity with the pilot, not as a robustness check the thesis can rely on; the
  primary time-based split governs per protocol 5.3a.
- **P4a** (item-count filter loosened to 3, tightened to 10) leaves every sign and every magnitude
  close to the primary split's, so the cold-start CBF loss and CF win are not artifacts of the
  min-items-per-learner threshold.
- **P4b** (two-day learners included, union with the primary evaluated population): cold-start
  median Precision@10 is 0.0529 (Hybrid) vs. 0.0683 (CBF) vs. 0.0473 (CF) vs. 0.0471 (MostPop) --
  same qualitative ranking (CBF 0.0683 > Hybrid 0.0529 > CF 0.0473 > MostPop 0.0471 on cold start)
  as the primary split's per-presentation medians.
- Full numbers: `results/run_artifacts/u11_s5_run_main/results_summary.json#reporting`
  (`secondary_median_rel_gain`, `tertiary_median_rel_gain`, `P4a_3_median_rel_gain`,
  `P4a_10_median_rel_gain`, `P4b_union_median_P10`, and each corresponding `*_sign_reversal_vs_primary`).

## Debug History

None. All commands (tests, refusal checks, canary, pilot stage, main stage) exited on the first
attempt with the expected exit code; 0 of the budgeted 3 debug rounds were used.

## Artifacts

- `results/run.log`: 10,257,030 bytes, append-only, shared by both stages. Verified before/after
  each stage per skill step 5: pre-pilot 0 bytes (file did not exist) -> post-pilot 3,758 bytes
  (sha256 `c4dfbd2e...63aa`) -> post-main 10,257,030 bytes (sha256 `d547e943...c0eac`), with the
  first 3,758 bytes of the final file re-hashing to the same post-pilot value, confirming
  append-only growth and no truncation.
- `results/run_artifacts/u11_s5_run_main_pilot/`: 4 files (`run_manifest.json`,
  `phase1_reproduced_metrics.json`, `criteria_verdicts.json`, `run_summary.json`), each hashed in
  `results/run_receipts/u11_s5_run_main_pilot.json`.
- `results/run_artifacts/u11_s5_run_main/`: 48 files (`run_manifest.json`, 22
  `foundation_<pres>.json`, 22 `results_<pres>.json`, `results_summary.json`,
  `criteria_verdicts.json`, `run_summary.json`), each hashed in
  `results/run_receipts/u11_s5_run_main.json`. Directory listing and receipt's `artifacts` array
  confirmed one-to-one (48 == 48, 4 == 4).
- `results/data_manifest.json`: re-verified SHA256 for all 8 OULAD tables against
  `inputs/manifest.json`; all 8 matched exactly, no drift since the S0 freeze.
- `results/run_receipts/u11_s5_run_main_pilot.json`, `results/run_receipts/u11_s5_run_main.json`:
  command line, argv, interpreter, code_tree_sha256, config_sha256, seeds, CPU/wall time, hardware,
  library versions, run.log before/after hashes, and a hand-computed `execution_event_hash`
  (SHA256 over the canonical JSON specified in the skill's step 10) for each stage, because no
  `execute-run` event exists on this Windows machine (deviation D1, `decisions.log`).

## Issues / Caveats

- **"Execution went through the engine" reads, on this project, as:** the entry-point contract
  (`--stage`/`--artifact-dir`/`--run-log`, exactly once each; artifact dir under
  `results/run_artifacts/`; run-log fixed at `results/run.log`) was checked by hand against every
  property `ar-workflow-engine.py`'s `run_command_contract` would enforce, because deviation D1
  (`decisions.log`) records that the literal engine cannot run natively on Windows (`fcntl`
  import). No engine call is claimed to have happened.
- The tertiary-split "not_applicable" lines for assertions L1, L2, L3 and L9 (95 per
  presentation: L1 1, L2 70, L3 10, L9 14, from 2,090 tertiary `not_applicable` records over 22
  presentations) are expected per protocol section 5.5 and were **not** treated as a problem; the
  main run's `run_summary.json.assertions.flags` list is empty (no `IDENTICAL_RANKINGS_PAIRS` or
  `SPLIT_FRACTIONS_OUT_OF_RANGE` violation was raised -- those keys appear under `executed`, i.e.
  the assertion ran cleanly, not under `flags`). Note: `run_summary.json#assertions.executed`
  folds the tertiary `not_applicable` records into `L2` (5,896 = 4,356 compared + 1,540
  not_applicable) and `L3` (814 = 594 + 220), but excludes them from `L1` (110, pass-only) and `L9`
  (6,226, pass-only) -- two counting conventions in one field; nothing changes downstream since
  `flags` is empty and no assertion failed, but the inconsistency is visible against `run.log`.
- C5's combined verdict is written by hand from two separate receipts (pilot decides the
  reproduction conjunct, main decides the main-run conjunct); each individual stage's own
  `criteria_verdicts.json` correctly and separately reports `not met (unchecked conjunct)` because
  neither file alone can see the other stage's number -- this is not a discrepancy, it is the
  documented cross-file merge the README asks for.
- `code/` under `data/projects/e_learning_thesis/` is not itself a git-tracked path (`data/` is
  machine-local, CLAUDE.md); `code_tree_sha256` -- not a git commit SHA -- is therefore the code
  identity recorded in both receipts, matching the value gate G4 cycle 2 approved.
- OULAD's licence is CC BY 4.0, verified on 2026-09-21 by the Methodologist at the dataset authors' own
  figshare deposit (DOI 10.6084/m9.figshare.5081998.v1) and recorded in `thesis/ch03.md` and
  `methodology/data_statement.md`. Residual provenance gap: the local `oulad.zip` archive is not traced
  to that deposit. This summary and `results/data_manifest.json` were written on 2026-09-22, before that
  verification reached the runner, and both said `unverified`; only this licence caveat was updated
  afterwards, no result changed.
- **Population limitation:** OULAD is a UK Open University cohort (32,593 rows in
  `studentInfo.csv`), not the candidate's own institution; per `idea.md`'s dataset decision this
  limit travels with the results, alongside the licence caveat above (`plan.md`:70-73 carries the
  same limitation).
- The main run's wall-clock time was 3,769 s (~62.8 minutes); measured against the plan's linear
  projection of ~0.93 CPU-hours, the run's 1.014 CPU-hours is about 9% over that projection
  (1.014 / 0.93 = 1.090), consistent with the collaborative-filtering scoring cost being superlinear
  in learners x items as flagged in advance; it stayed well inside the 4.0 CPU-hour budget (1.014
  CPU-hours measured), so no mid-run stop was needed.

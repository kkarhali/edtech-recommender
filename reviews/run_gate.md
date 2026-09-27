---
blockers_count: 3
warnings_count: 4
files_reviewed: n/a
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Claude Opus 5
model_identity: claude-opus-5 (self-reported; the artifact under review was produced by the
  mid-tier experiment-runner recorded at `decisions.log:172` and `state.md#agents`, a different
  identity, so rule 1 independence is verified rather than assumed)
mode: run_gate
unit: u12_g5_run_gate
cycle: 0
---

# Review

## Blockers (must fix before proceeding)
- [B1] <severity:high> `results/summary.md`:200-202 (Sensitivity and robustness, P4b bullet): the
  P4b cold-start median Precision@10 for the **Hybrid** is stated as `0.0473`; the artifact the
  same bullet cites, `results/run_artifacts/u11_s5_run_main/results_summary.json#reporting.P4b_union_median_P10["A|2"].Hybrid`,
  is `0.052861847961545305` (0.0529). `0.0473` is two different other numbers — the primary
  split's per-presentation cold Hybrid median (0.0473, the table at line 172) and P4b's own
  `ItemKNN-CF` value (0.047349) — so the sentence prints the CF figure twice and then draws the
  qualitative conclusion "CBF > Hybrid ~ CF" from it. | impact: a stated result does not match the
  artifact it cites (rule=2), and the error suppresses a real +11.6% Hybrid-over-CF margin in the
  one sensitivity run that tests the two-day learners, which is exactly the cold-start population
  the hypothesis is about; chapter 4 copying this line would publish a wrong number.
- [B2] <severity:med> `results/summary.md`:187 (Sensitivity table, tertiary row, "warm vs. CBF"
  cell): `+167.11% (sign reversal)`. The cited artifact records
  `results_summary.json#reporting.tertiary_sign_reversal_vs_primary["warm|None"].vs_CBF = false`,
  and arithmetically there is no reversal (primary `+31.20%`, tertiary `+167.11%`, both positive).
  The summary's own prose at line 192 says the tertiary split "reverses three of the four signs",
  so the table contradicts both the artifact and the adjacent sentence. | impact: a claim in
  summary.md not supported by the artifacts (rule=2); a reader or the results analyst tallying the
  table records four reversals where the run recorded three.
- [B3] <severity:high> `results/summary.md` (whole file): `idea.md`'s DATASET DECISION block
  instructs, verbatim, "Record this choice and its limitation (OULAD is a UK Open University
  population, not the thesis's own institution) explicitly in plan.md and **results/summary.md**."
  `plan.md`:70-73 carries it ("**Population limitation:** OULAD is a UK Open University cohort");
  `results/summary.md` does not — the words "Open University", "population limitation",
  "institution" and any equivalent external-validity caveat are absent (grep over the file returns
  only the unrelated "primary evaluated population" at line 200). The Issues/Caveats section
  records the unverified licence but not the population limit. | impact: a hard constraint from the
  frozen idea file, addressed specifically at this artifact, is unmet (rule=9); the run's first
  full-scale results are now stated without the external-validity limit the idea file required to
  travel with them.

## Warnings (should fix)
- [W1] <severity:low> `results/summary.md`:244-245: "The tertiary-split `not_applicable` lines for
  assertions L1, L2, L3 and L9 (about 80 per presentation)". Counted from `results/run.log`:
  2,090 tertiary `not_applicable` assertion records over 22 presentations = **95** per
  presentation (L1 1, L2 70, L3 10, L9 14). The exemption itself is correct and protocol-declared;
  only the magnitude is understated.
- [W2] <severity:low> `results/run_artifacts/u11_s5_run_main/run_summary.json#assertions.executed`
  counts the tertiary `not_applicable` records inside `L2` (5,896 = 4,356 compared + 1,540
  not_applicable) and `L3` (814 = 594 + 220), but excludes them from `L1` (110, pass-only) and
  `L9` (6,226, pass-only). Nothing changes — `flags` is empty and no assertion failed — but the
  two conventions in one field cannot both be right, and anyone reconciling the counts against
  `run.log` will hit it.
- [W3] <severity:low> `results/summary.md`:22-26 states that `test_metrics.py` (11 tests),
  `test_evaluate.py` (5 tests), four entry-point refusal cases and `canary_eee_2014j.py` all passed
  before either stage ran. No receipt field and no `run.log` line records any of them; the log's
  first event is the pilot `start`. The files exist and `def test_` counts are 11 and 5 as claimed,
  so the statement is plausible, but its execution is `unchecked`, not verified (rule=6).
- [W4] <severity:low> `results/summary.md`:257-260 reads "The main run's **wall-clock** time
  (3,769 s, ~62.8 minutes) exceeded the plan's linear projection of **~0.93 CPU-hours** by about
  9%". The 9% is the CPU-hour comparison (1.014 / 0.93 = 1.090); wall-clock and CPU-hours are
  mixed inside one sentence. The numbers themselves are right.

## Constraint Audit
- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a multi-GPU cluster." | status: satisfied | evidence: `results/run_receipts/u11_s5_run_main.json#hardware` and `results/run.log` `start`/`end` events, both "Intel64 Family 6 Model 158 Stepping 13, GenuineIntel, 12 logical cores, no GPU"; one process plus one fresh-process L7 rebuild worker (`child_worker_wall_seconds` 852.02 counted as CPU, an upper bound); grep over `code/*.py` finds no `torch`, `tensorflow`, `keras`, `cuda` or `nvidia` reference | blocker: none
- [C2] "Prefer scikit-learn or a lightweight model for the pilot; reserve deep learning (RNN/CNN/RBFNN, per the reviewed papers) for the Phase 2 main experiment" | status: satisfied | evidence: `library_versions` in both receipts is numpy 2.5.3, pandas 3.0.5, scikit-learn 1.9.1, scipy 1.18.1 and nothing else; `code/` is 23 `.py`/`.json` files implementing MostPop, PopWeek, CBF, ItemKNN-CF, a learned-blend Hybrid and Random. Deep models remain a recorded scope-out (`state.md#findings`, `plan.md` scale_up_policy), not a silent omission | blocker: none
- [C3] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed hardware" | status: satisfied | evidence: `u11_s5_run_main_pilot.json#wall_clock_seconds` = 16.01 s; `u11_s5_run_main.json#wall_clock_seconds` = 3769.12 s (62.8 min); both far inside "a few hours", and inside plan C5's own 15-minute / 4.0-CPU-hour budgets (0.238 min and 1.0140 CPU-hours) | blocker: none
- [C4] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." | status: satisfied | evidence: no `requests`, `urllib`, `socket`, `http` or download call anywhere in `code/*.py`; `hard_constraints.downloaded_model_weights = false` is a literal in `code/common.py`:31 and is echoed into `run.log`'s `start` event and both `run_manifest.json` files; the only inputs read are the 8 local OULAD CSVs | blocker: none
- [C5] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and evaluated on identical splits so the comparison in success criterion 1 is fair." | status: satisfied | evidence: assertion L5 (`code/leakage.py`:46-48, counts models whose `view_hashes` triple differs from the presentation's) ran **770** times in the main stage with `count: 0, status: pass` every time; L4 (train/val, val/test, train/test pair overlap) 396 records all 0; `SPLIT_FRACTIONS_OUT_OF_RANGE`, `T41_population_cells_differing`, `SPLIT_EXCLUDED_LEARNERS`, `D_TABLE_MISMATCH` all 0 in 22/22; C4's `val_test_shared_rows = 0` in `criteria_verdicts.json#C4` | blocker: none
- [C6] "requires network access during the pilot to download OULAD once (a few hundred MB)" — network limited to that one dataset fetch | status: satisfied | evidence: no network call exists in the code path; this run performed **no** download at all. `results/data_manifest.json` re-verified the 8 OULAD tables against the S0 freeze, and I re-hashed all 8 from `data/projects/e_learning_pilot/data/raw/` myself: every byte count and SHA256 matches `inputs/manifest.json` exactly (studentVle.csv 453,836,331 B, `52668253…937f0`, and 7 others) | blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only background; do not attempt to re-scrape or redistribute their content." | status: satisfied | evidence: all 9 PDFs under `src/reasearch_topic/References/` carry 2023-10 mtimes, untouched by the 2026-09-22 run window; no artifact or log line reads or copies them; `hard_constraints.reference_pdfs_read_only = true` in both manifests | blocker: none
- [C8] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most likely cause … rather than adjusting the threshold after the fact." — no threshold moved after a run | status: satisfied | evidence: I compared `metric`, `threshold` and `on_dataset` for C1-C6 in **both** `criteria_verdicts.json` files against `plan.md`'s frozen `success_criteria` block: all 18 string triples are character-identical, in the pilot file and the main file alike. C2 and C3 are reported `not met` with their actual medians, p-values and the 20 failing presentations named, not re-scoped | blocker: none
- [C9] "Record this choice and its limitation (OULAD is a UK Open University population, not the thesis's own institution) explicitly in plan.md and results/summary.md." | status: violated | evidence: present at `plan.md`:70-73; **absent** from `results/summary.md` — no occurrence of "Open University", "UK", "institution", "population limitation" or an equivalent external-validity caveat anywhere in the file, including its Issues/Caveats section | blocker: B3

## Notes
- **Recomputation (dispatch item 1).** I rebuilt C1 and C2 from the 22 `results_<pres>.json` files
  (`splits.primary.cells["warm|None"]` and `["A|2"]`, `models.<m>["P@10"].mean`), computing the
  paired exact Wilcoxon from its own enumerated null distribution rather than calling SciPy, then
  cross-checking against SciPy. Every reported figure reproduces: warm vs CBF median
  `+0.3120403340` (reported +31.20%), exact p `0.005928516387939453`; warm vs CF `+0.1068490302`,
  p `0.014094829559326172`; cold vs CBF `-0.3028060620`, p `0.00012063980102539062`; cold vs CF
  `+0.0732142857`, p `0.00024127960205078125` with `n_eff` 21 after one zero difference dropped.
  My own Holm correction gives `0.011857032775878906 / 0.014094829559326172` (C1) and
  `0.00024127960205078125` twice (C2) — the reported values to the last digit. C3's `ge_cbf` holds
  in exactly 2 of 22 (CCC_2014J, DDD_2013B) and `gt_mostpop` in 22 of 22. **No difference from the
  reported figures; no verdict changes.** I also re-derived all 14 columns of every one of the 22
  per-presentation table rows in `summary.md`: 0 mismatches.
- **Receipts (dispatch item 2).** Rather than spot-check five per receipt, I hashed **every** file
  both receipts list: 48/48 for the main receipt and 4/4 for the pilot, all byte counts and all
  SHA256 values matching, no file missing, and the on-disk directory listings identical to the
  receipts' `artifacts` arrays (48 == 48, 4 == 4). `run.log` is 10,257,030 bytes hashing to
  `d547e943…c0eac` (= the main receipt's `run_log_after_sha256`); its first 3,758 bytes hash to
  `c4dfbd2e…63aa` (= the pilot's after-hash and the main's before-hash) and the pilot's
  before-hash is the empty-file hash — the append-only, no-truncation claim is real. Both
  `execution_event_hash` values recompute exactly from the receipts' own canonical JSON.
  `code_tree_sha256` `694c3ea6…231c` is identical in both manifests, both receipts, the G4 cycle-2
  approval (`review_cycle2.md`:19), and a fresh recomputation over `code/` today — the reviewed
  code is the code that ran, and it has not drifted since.
- **C6 (dispatch item 3).** Checked against `inputs/prior_evidence/pilot_metrics.json` directly,
  not the runner's restatement: all six Precision@10 values are bit-identical floats
  (`0.11820781696854146`, `0.5351763584366063`, `0.5207816968541468`, `0.10066730219256434`,
  `0.16101048617731176`, `0.14022878932316493`), so every absolute difference is exactly 0.0
  against a 1e-6 tolerance, and `n_raw_interaction_rows`, `n_items`, `n_eval_users` and every
  `distinct_items_recommended` match too. **C6 met is correct.**
- **Log audit (dispatch item 4).** All 33,458 lines parse; 30,455 assertion records. **Zero**
  carry `status: fail`, and **zero** have `count > required` outside a `not_applicable` record —
  anywhere, in either stage. The 2,092 `not_applicable` records are 2,090 on the tertiary split
  (L1, L2, L3, L9) plus two in the pilot stage (`L1-L8` and `L9`), and `methodology/protocol.md`
  section 5.5 declares all four families in advance, including the L2/L3 tertiary case added at G4
  cycle 2. The 2,112 `info` records are all `L7` with `required: null` — measurements, not
  assertions. `IDENTICAL_RANKINGS_PAIRS` ran 748 times and its `pairs` list is **empty in all 748**
  (`count: 0, required: 0, status: pass`). The separate `exempt_identical` field is non-empty in
  216 records, and both families are exactly the ones `review.md` item 11 already confirmed:
  `(CBF, Hybrid)`, `(CBF, ItemKNN-CF)` and `(Hybrid, ItemKNN-CF)` appear **only** at `k = 0`
  (132 each = 22 presentations x conditions A|0 and B|0 x 3 splits), and `(MostPop, PopWeek)`
  appears beyond `k = 0` in exactly three presentations — BBB_2013B, DDD_2013B, DDD_2013J — whose
  `p5` records are the only three with `week_missing_share: 1.0` and
  `all_missing_columns: ["week_from", "week_to"]`, cross-asserted by `P5_all_missing_mismatch`
  (22/22 pass). No duplicate-model failure is hiding here.
- **Summary framing (dispatch item 5).** The central-finding section states the result plainly and
  in the right direction: "the hybrid beats collaborative filtering on cold start (median +7.3%
  relative, p_holm = 0.00024, n = 22) **but loses to content-based filtering on cold start**
  (median -30.3% relative …)", names C2 as refuted because it requires beating both baselines,
  reports C3's `ge_cbf` as 2 of 22 with all 20 failures listed, and explicitly contrasts this with
  the phase 1 pilot's "22 of 22 (median +190%)" overclaim. Nothing in the file says the hybrid
  "beats baselines on cold start". The pilot's failure mode has **not** recurred. B1 and B2 sit in
  the exploratory F4 section, decide no criterion, and both happen to err conservatively — but
  they are still numbers that contradict the artifacts they cite, which is why they are blockers
  and not warnings.
- **Two things chapter 5 should expect an examiner to ask, neither of which changes a verdict.**
  C1's vs-CF conjunct clears its `>= +0.10` threshold by 0.68 percentage points (`+10.68%`); and
  the vs-CBF warm sign test is `p = 0.0525`, above 0.05, while the pre-registered test is the
  exact Wilcoxon (`p = 0.005929`), so C1 stands as pre-registered — but the results analyst should
  surface both rather than let the critic find them.
- The Random baseline's five seeded runs (`Random|42` … `Random|46`) are present per cell in every
  `results_<pres>.json` but are not surfaced anywhere in `summary.md`. They decide no criterion, so
  this is not a rule 4 best-run-only omission; it is worth a line in the chapter-4 table.
- **Manual-write deviation.** This verdict was written by hand with Write. The review MCP tool
  (`ar-gemini-review-mcp.ts`) could not run, because its persistence step shells out to
  `ar-workflow-engine.py`, which imports `fcntl`; Windows Python has no such module. No tool
  injected my model identity, bound this report to its unit and cycle, or validated the Constraint
  Audit — I ran `ar-review-contract.ts`'s checks against my own draft instead. The coordinator's
  decision log must carry this as a deviation (rule=6: the absence of the automated check is
  `unchecked`, never silently `passed`).

## Overall
**revise.** The experiment itself holds up under independent audit: every C1 and C2 median and
p-value recomputes to the last digit from the raw per-presentation files, all 52 receipt-listed
artifacts hash to what the receipts claim, the append-only log and both execution-event hashes
reconcile, C6's zero difference is confirmed against the prior-evidence file directly, no L1-L9
assertion failed or exceeded its bound anywhere, the identical-ranking exemptions are exactly the
two families the code review already approved, and every runtime hard constraint — single CPU with
no GPU, no downloaded weights, no network call, identical splits across all compared models,
read-only reference PDFs, no threshold moved after the run — is satisfied with evidence. The
verdicts `C1 met, C2 not met, C3 not met, C4 met, C5 met (combined), C6 met` are all correct as
stated, and the summary reports the cold-start loss to content-based filtering plainly, without
repeating the pilot's overclaim. What blocks the gate is three defects in `results/summary.md`
alone: one wrong number (B1), one label the cited artifact contradicts (B2), and the OULAD
population limitation that `idea.md` requires this file to carry and it does not (B3). All three
are fixed by editing the summary against artifacts already on disk. **No rerun is needed and no
result changes** — re-dispatch the runner (or the results analyst) for a summary revision, then
re-gate at cycle 1.

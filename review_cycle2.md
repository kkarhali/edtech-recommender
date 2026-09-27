---
blockers_count: 0
warnings_count: 7
files_reviewed: 24
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Opus 5
model_identity: claude-opus-5 (reviewer seat, top tier) — distinct from the experiment engineer's mid-tier sonnet seat that produced code/ (decisions.log, 2026-09-22T11:20:00Z revision 2 and 13:00:00Z revision 3 dispatches to worker=experiment-engineer tier=mid; 2026-09-22T16:10:00Z this dispatch, worker=reviewer tier=top)
mode: code_review
unit: u10_g4_code_review
cycle: 2
---

# Review

Third and final review of `code/` (19 modules, 3 test files, `configs/experiments.json`, `README.md`)
against `idea.md`, `plan.md` and `methodology/protocol.md` as it now stands, including the section 5.5
addition. Nothing under `code/` is excluded. No file was edited. Everything I ran wrote only to the OS
temp directory (`%TEMP%/rev2_probe`); the two `__pycache__` trees my `compileall` pass created under
`code/` were removed, and `common.code_tree_sha256()` is `694c3ea6026939967a6b01ab0698ef7336e77a8dd29f0739157e9f9662b0231c`
both before and after everything I did, so `code/` is byte-identical to the tree the engineer handed over.

**The diff since cycle 1, established without a VCS.** `data/` is untracked in the repository, so no
literal diff of this tree exists. I reconstructed it from mtimes against `review_cycle1.md`
(2026-09-22 09:39:00) and then read every changed file end to end rather than the two the engineer
named. Changed after cycle 1: `foundation.py` (09:40:29), `features.py` (09:40:45), `models.py`
(09:40:54), `cell.py` (09:41:04), `README.md` (09:41:49), `blend.py` (09:42:42), `evaluate.py`
(09:42:56) — the revision-2 round — then `common.py` (11:07:07) and `provenance.py` (11:07:21) — the
revision-3 round, exactly the two files the engineer reported for B3 — plus `methodology/protocol.md`
(09:41:55). Unchanged, and therefore outside this fix: `leakage.py` (09:22:07), `splits.py`,
`variants.py`, `data.py`, `stats.py`, `verdicts.py`, `main.py`, `metrics.py`, `behaviour.py`,
`reproduce_phase1.py`, `configs/experiments.json` and all three test files.

**What I ran, and what it returned.** All under `.venv-pilot/Scripts/python.exe` with
`PYTHONDONTWRITEBYTECODE=1` and `PYTHONUTF8=1`.

- An in-process probe driving `foundation.prepare`, `foundation.verify` and
  `evaluate.run_presentation` on `AAA_2013J` exactly as `main.run_matrix` does, with `artifact_dir`
  and the run log in the OS temp directory. `foundation.verify` completed in 21.8 s, `run_presentation`
  in 24.5 s, `finalize` without error, exit 0, no exception anywhere, `unchecked` empty, `flags` empty.
- `tests/test_metrics.py` — 11 tests, all `ok`, exit 0.
- `tests/test_evaluate.py` — 5 tests, all `ok`, exit 0.
- `tests/canary_eee_2014j.py` — both rows `OK` to four decimals (MostPop 0.0137 / 0.0255 / 0.2157;
  ItemKNN-CF 0.0279 / 0.0333 / 0.1946), exit 0, no file written.
- `compileall` over `code/` — clean.
- An AST scan of every `RunLog.measure` and `RunLog.flag` call site, and negative tests of
  `provenance.emit` and `features.week_missing_share` against every object type and split label that
  can reach them.

**The three cycle-1 blockers, verified fixed by execution, not by reading the report.**

- *Cycle-1 B1 (duplicate `k` to `leakage.l8`).* `code/foundation.py:106-107` now reads
  `leakage.l8(log, prep, "M3", used, cond.eval_ids, VAL, **ctx)` with `ctx = {"pres", "condition", "k"}`
  and no second `k=k`. `foundation.verify` ran the whole plan — `warm`, `A` at k = 0/1/2/5, `A_robust`
  at k = 2, `B` at k = 0/1/2/5 — to completion on `AAA_2013J` and wrote `foundation_AAA_2013J.json`.
  Every cold condition that cycle 1 could not reach now runs.
- *Cycle-1 B2 (`week_missing_share` missing on `splits.Prep`).* `code/features.py:157-163` adds one
  accessor branching on `isinstance(view, View)`; `code/blend.py:88` and `code/models.py:342` are its
  only two callers, both passing `ctx.view`. I checked it against every type that can reach it, not
  only the two sites cycle 1 named: a `Prep` (returns `feature_constants["week_missing_share"]`), a
  `features.View` (returns the attribute), and anything else (raises `AttributeError`, loudly). There
  are exactly three `features.View` construction sites — `features.py:154` `as_view`, `variants.py:89`
  `two_day_view`, and `rebuild_worker.py:20` from the dict `leakage.py:139` pickles — and all three
  pass the field explicitly. The `View` path is not merely reachable, it ran: the L7 fresh-process
  rebuild produced 52 `l7_hash_pair` lines over all seven objects including `blend_model` and
  `blend_standardiser`, every pair equal, `L7_rebuild_mismatch` 0 on all four rebuilds. The Hybrid
  fitted and scored in all 34 cells.
- *Cycle-1 B3 (tertiary L2/L3 non-zero by design).* `common.RunLog.measure` gained
  `na: bool = False` as its fourth parameter (`code/common.py:119-135`); `provenance.emit`
  (`code/provenance.py:31`) sets it as `check in ("L2", "L3") and ctx.get("split") == "tertiary"`.
  The run log of my probe matches the engineer's report line for line: **34 cells** (primary 10,
  secondary 10, tertiary 10, `P4a_3` 2, `P4a_10` 2), **305 L2/L3 lines**, of which **80 tertiary, all
  `not_applicable`**, and **225 non-tertiary, all `pass` with count 0**. Zero L2/L3 failures anywhere;
  zero `FAIL` and zero `FLAG` lines of any id in the whole 1,526-line log. The engineer's "225
  primary/secondary" is the right total and the right status, but the label is loose: the 225 are 160
  primary and secondary, 32 `P4a_3`/`P4a_10`, and 33 emitted by `foundation.verify` with no split key.

**The specific things a crash-driven fix could have left behind, each checked.**

- *Does `na`'s default really leave every other caller unchanged?* Yes, and by construction rather than
  by inspection. An AST scan of all 36 `measure`/`flag` call sites in `code/` shows every one passing
  exactly **two** positional arguments, so none can bind `na` positionally, and `provenance.py:31` is
  the only site in the codebase that passes `na` at all. `measure("ANY", 7)` still aborts;
  `measure("ANY", 7, 7)` still reads the third positional as `required`. The `**ctx` dicts that reach
  `measure` are `{pres, condition, k, split}` and subsets of it, so an `na` key cannot arrive through
  one — and if it ever did, Python would raise a duplicate-keyword `TypeError`, loudly, not silently.
  At runtime the whole probe produced `not_applicable` for exactly four ids: L1 (1 line), L2 (70),
  L3 (10) and L9 (14), every one of them on the tertiary split, L1 and L9 through their own
  pre-existing mechanisms (`evaluate.py:137`, `leakage.l9_flush`). No other assertion anywhere is now
  skipped.
- *Can the tertiary check fire on the wrong split?* No. The split label has exactly one producer —
  the five literals at `evaluate.py:179-183` — and `run_split` is called nowhere else, `run_cell`
  nowhere but `evaluate.py:146`. I tested `provenance.emit` with a count of 5 across every label:
  `primary`, `secondary`, `P4a_3`, `P4a_10`, `Tertiary`, `tertiary ` (trailing space), `None` and
  absent all abort with `LeakageError`; only the exact string `tertiary` records `not_applicable`. A
  typo therefore fails closed — it aborts a legitimate run rather than suppressing a real leak.
- *Is anything else suppressed on the tertiary split?* No. L7 still aborts there (I forced a
  cold-learner read on a tertiary record and it raised), and so do L4, L5, L1 on the other splits, and
  `L2_objects_without_record`, which is a different check id and so is never `na` — 44 coverage lines,
  all pass. C4's hyperparameter provenance also still audits the tertiary split, exactly as protocol
  1.2 and 5.5 require: `evaluate.py:149-152` reads `log.provenance` directly, which `provenance.emit`
  appends to before it measures, so the records survive the `na` status. Measured across the probe:
  136 hyperparameter records (34 cells × 4 objects) and `hp_outside_train_or_val` 0.
- *Did the fix move a protocol number, a criterion string or the plan hash?* No, and I checked this
  against the files rather than against the report. `plan.md` is 15,766 bytes with SHA256
  `22bb14a2…e462d0` and `idea.md` 4,506 bytes with SHA256 `8be52b93…bc1b43`, both byte-for-byte the
  values protocol.md's own header declares. All **18 criterion strings** (6 criteria × metric,
  threshold, on_dataset) are identical between `plan.md`, protocol section 1.1 and
  `verdicts.load_criteria()` read at run time — 0 mismatches. Protocol 4.1's table matches
  `foundation.TABLE_41` in all 22 rows, and protocol 5.2's `D` values match `variants.D_TABLE` in all
  22. `AAA_2013J`'s 4.1 row reproduced live from the data (378 / 1 / 2 / 375 / cohort 75, test frac
  0.199, val frac 0.102) and so did its 9.1 row (test items 12.8 mean / 13 median, 28.3% with < 10,
  0.3% with exactly 1). Section 5.1's split code (`splits.py`) was not touched this cycle at all.
  Within protocol.md, the only "G4 cycle 2" marker is the 5.5 paragraph at line 545, and the step-10
  text cycle 1 verified is intact, shifted down by exactly the length of that insertion.

## Blockers (must fix before proceeding)

None.

## Warnings (should fix)

- [W1] <severity:med> code/README.md:118-119 (pilot/iteration acceptance, step 5): the acceptance line
  still says to expect every `assert` line `status: pass`, listing only "Condition B L7 lines
  `status: info`; tertiary L1 and training-bound L9 lines `not_applicable`" as exceptions. The
  revision-3 fix adds **80 tertiary L2 and L3 `not_applicable` lines per presentation** (measured), and
  they are not in that list. A runner checking the log against this README reads a correct run as a
  deviation. The error direction is safe — a false alarm, never a false pass — but the interface
  contract the runner dispatch reads is now stale in the one place this cycle changed it, which is the
  same defect cycle 1's W3 and W5 raised about `split` and `flags`, both of which were fixed.
- [W2] <severity:med> code/features.py:26 with code/features.py:157-163: `View.week_missing_share`
  carries a dataclass default of `0.0`, and the accessor returns the attribute unconditionally for a
  `View`. A `View` built without the field therefore yields a silently wrong blend feature (0.0 instead
  of the presentation's real share) rather than an error — the one failure mode of this fix that would
  not announce itself. All three current construction sites pass it explicitly, so the code is correct
  today; the default is what makes a future regression silent. Removing the default, or asserting it in
  `blend_features`, would close it.
- [W3] <severity:med> methodology/protocol.md:565-566 with code/provenance.py:31: 5.5's closing
  sentence — "L2 and L3 remain fully `must be 0` … on the primary and secondary splits **and in every
  cold-start condition of section 6**, where a bound is defined" — can be read as keeping L2/L3
  mandatory in the tertiary split's own cold conditions. The code applies `not_applicable` to every
  condition of the tertiary split, which my probe confirms (the 80 lines cover `warm`, `A`, `A_robust`
  and `B`). The code's reading is the only coherent one — the tertiary split has no training bound in
  any condition, and the paragraph's governing sentence says "a non-zero L2 or L3 count on this split
  alone never aborts the run" — but the qualifying clause invites the other reading. `thesis/ch03.md`
  should state which conditions the exemption covers, rather than leave an examiner to resolve it.
- [W4] <severity:low> code/foundation.py:106-107 and code/cell.py:66, 70: `leakage.l8`'s own signature
  (`code/leakage.py:80`) binds `k` as a named parameter, so `k` never reaches `**ctx` and never appears
  in the emitted line — the comment at foundation.py:106 ("ctx already carries k") describes an effect
  the call does not have. Within one presentation and condition the L8 lines for k = 0, 1, 2 and 5 are
  indistinguishable in `results/run.log` (measured: 90 L8 and 90 `L8_truth_in_exclusion` lines, none
  carrying `k`). No count changes and no assertion is skipped; this is attribution only.
- [W5] <severity:low> code/cell.py:97: the P4b `leakage.l8` call passes `pres` and `condition` but not
  `split`, the one remaining instance of cycle-1 W1; the two main-path calls at cell.py:66 and 70 now
  carry it. P4b runs only on the primary split today, so nothing collides, but the log line is the one
  L8 line in the run whose split cannot be read off it.
- [W6] <severity:med> Scale is unexercised, and this is the largest remaining unknown at G5, not G4.
  `AAA_2013J` — 375 evaluated learners, the smallest of the 22 — costs 46.3 s of wall clock for
  `foundation.verify` plus `run_presentation`. The 22 presentations hold 27,212 evaluated learners,
  72.6×, so a purely linear floor is ≈ 0.93 h against C5's 4.0 CPU-hour budget, and `cf_scores` is
  superlinear in learners × items (CCC_2014J alone has 2,131). The README already tells the runner to
  treat `cpu_hours × 22` as a floor and stop before 4.0; nothing here blocks the run, and the real
  figure is the runner's evidence at G5.
- [W7] <severity:med> code/evaluate.py:28-35 and 236 (carried unchanged from cycle 1 W2, now
  documented in the file rather than fixed): `hyperparameter_rows_reading_test_data` is structurally
  incapable of being non-zero for the four hyperparameter objects, because `read` is a subset of
  `allowed` by construction. My probe's 136 records and count of 0 are a consequence of that
  construction, not a measurement. The comment now says so in the code, which is the right outcome for
  a code gate; chapter 5 must cite L7, L8 and L9 as the blend's leakage evidence and must not present
  this field as an independent check.

## Constraint Audit

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a multi-GPU cluster." | status: satisfied | evidence: a fresh case-insensitive grep for `torch|tensorflow|keras|cuda|nvidia|gpu` over all 22 files under `code/` returns exactly two hits, both literals: code/common.py:30 `"hardware": "single CPU, no GPU"` and code/common.py:98, which writes processor, logical core count and "no GPU" into `run_manifest.json`. The full import surface of `code/` is numpy, pandas, scipy.stats, sklearn.{cluster,linear_model,metrics,model_selection} and the standard library. My probe ran the whole presentation on CPU | blocker: none
- [C2] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed hardware, using a data subset if needed to stay within that budget." (plan.md Budget, C5: `<= 4.0` CPU-hours main, `<= 15` minutes reproduction) | status: satisfied | evidence: code/main.py:119-124 sums wall seconds, `time.process_time()` and the L7 workers' wall seconds into `cpu_hours`; code/verdicts.py judges C5 against `common.HARD_CONSTRAINTS` 4.0 and 15.0 and records the hardware; code/README.md:121-128 declares `cpu_hours × 22` a floor and tells the runner to stop before 4.0, not after. Measured this cycle: 46.3 s for the smallest presentation, a 0.93 h linear floor over 22 (see [W6]). Whether the realised figure fits is the runner's evidence at G5 | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." | status: satisfied | evidence: a fresh grep for `requests|urllib|http://|https://|socket|download|huggingface|transformers|wget|curl` over `code/` returns exactly one hit, the literal `"downloaded_model_weights": False` at code/common.py:31; the only file reads are the four hashed OULAD CSVs (code/data.py:13, 25-40, 57) | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and evaluated on identical splits so the comparison in success criterion 1 is fair." | status: satisfied | evidence: the split is built once per presentation and `splits.split_view` is the only object models receive; `leakage.l5` re-hashes the triple each model actually holds against `prep.hashes`, driven per cell at code/cell.py:59-61 and per foundation at code/foundation.py:79. Measured across my full-presentation probe: 35 L5 lines, every one count 0 over 6 models, and 18 L4 lines, every one count 0 on all three intersections, on all five splits. The `split` key added in cycle 1 is a log and counter dimension only and changes no L1-L9 count; the `na` flag added this cycle touches only the L2/L3 status on the tertiary split and left L5 and L4 untouched, which I confirmed by forcing non-zero counts on a tertiary context — both still abort | blocker: none
- [C5] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only background; do not attempt to re-scrape or redistribute their content." | status: satisfied | evidence: no path under `src/reasearch_topic` and no string `References` occurs anywhere in `code/` (fresh grep); the single configured data root is `data/projects/e_learning_pilot/data/raw` (code/configs/experiments.json:4, code/data.py:14, 21-22); the constraint is carried as a literal at code/common.py:34. Every write in `code/` goes to `ctx["artifact_dir"]` or the run log (fresh grep over `write_text|open(...w|to_csv|savefig|mkdir`) | blocker: none
- [C6] Network limited to the one OULAD download (idea.md DATASET DECISION: "requires network access during the pilot to download OULAD once (a few hundred MB)") | status: satisfied | evidence: zero network calls under `code/` (the same grep as C3); code/data.py:25-40 verifies SHA256 and byte size of every file used against `inputs/manifest.json` and raises `DataIntegrityError` before any use. My probe emitted four `data_sha256` lines with `manifest_match: true` for studentVle.csv, vle.csv, courses.csv and studentRegistration.csv and loaded everything from the hashed local copy, with no network access | blocker: none
- [C7] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most likely cause … rather than adjusting the threshold after the fact." | status: satisfied | evidence: strongest of this cycle. `verdicts.load_criteria()` JSON-decodes `metric`, `threshold` and `on_dataset` out of plan.md's frozen front matter at run time, and I compared all 18 strings it returns against plan.md and against protocol section 1.1 — 0 mismatches. `plan.md`'s SHA256 is `22bb14a20fe7f111bf342aec51a54b7a3b6daf6c8723e1b5d66120d8d8e462d0` at 15,766 bytes, byte-identical to the hash protocol.md's header declares, so no threshold moved during either fix round. code/stats.py:97-109 applies C1 as `>= 0.10` and C2 as `> 0` exactly, with `NOT_MET_UNCHECKED` for a met threshold on an inconclusive test, and a failing criterion still carries medians, Wilcoxon, effect size and dropped-pair counts | blocker: none
- [C8] "Language/tooling per the thesis: Python, TensorFlow or Keras, scikit-learn. Prefer scikit-learn or a lightweight model for the pilot; reserve deep learning (RNN/CNN/RBFNN …) for the Phase 2 main experiment" | status: satisfied | evidence: the only estimators are `sklearn.linear_model.LogisticRegression` (code/blend.py:9, 40-48), `sklearn.model_selection.StratifiedKFold` (code/blend.py:10) and `sklearn.cluster.KMeans` with `silhouette_score` (code/behaviour.py:11-12); everything else is numpy, pandas and scipy. plan.md records the deep models as an explicit scope-out | blocker: none

## Notes

- The `na` status is applied uniformly across the tertiary split, including to the 70 of its 80 L2/L3
  lines whose measured count is genuinely 0 (the four hyperparameter objects and `cbf_item_vectors`).
  Only 10 lines carry a non-zero count, the `similarity_matrix`, `mostpop_counts` and `popweek_counts`
  records, up to 54,193 rows of 180,925 — the 30% that is the split's own 20% test plus 10% validation,
  the figure protocol 5.5 now quotes. The evidence protocol 5.5 asks to be retained is retained: the
  measured count is written to every one of those lines, it is simply not compared against zero.
- Cycle 1's W4 is fixed in substance: `code/blend.py:40-48` now passes `l1_ratio=0.0` rather than the
  deprecated `penalty="l2"`, and my probe fit the blend in every one of the 34 cells on
  scikit-learn 1.9.1 without a single `FutureWarning` reaching stderr (stderr was empty). Cycle 1's W3,
  W5 and W6 are fixed at code/README.md:55-57, 66-68 and 131-134 and code/evaluate.py:246-251
  respectively. Cycle 1's W1 is fixed at cell.py:66 and 70 and remains only at cell.py:97 ([W5] above).
- `finalize` ran cleanly on a one-presentation accumulator: C1, C2 and C3 returned `unchecked` with the
  reason "defined over all 22 presentations; 1 were run", which is rule 6 behaving correctly, and C4
  returned its counts. L6 ended the run with 360 distinct scoring keys, `max_count` 1, 0 duplicates.
- Nothing in this code has yet been run at 22-presentation scale, and I did not run it at that scale
  either. Every number in this review comes from `AAA_2013J`, the smallest presentation. [W6] is the
  consequence; it is a runner discovery at G5, not a code-gate finding.
- This file was written by hand, not by the review MCP tool: `ar-workflow-engine.py` imports `fcntl`,
  which Windows Python does not have, so nothing validated the Constraint Audit, the blocker count or
  the unit/cycle binding before it landed. Per rule 6 that absence is `unchecked`, not `passed`, and
  the coordinator's decision log should carry it. I ran the tool's own validation rules on this draft
  myself: eight constraints, each appearing exactly once, each with a status, evidence naming a real
  file or measurement, and a blocker field; every entry `satisfied` with `blocker: none`, which is
  what lets an `approve` stand; zero `[B#]` entries counted against `blockers_count: 0`; seven `[W#]`
  entries counted against `warnings_count: 7`.
- `review.md` (cycle 0) and `review_cycle1.md` (cycle 1) are untouched and remain their cycles' records.

## Overall

The decision is `approve`. All three cycle-1 blockers are fixed, and I verified each by running the
code rather than by reading the engineer's report: `foundation.verify` completes the whole condition
plan on `AAA_2013J`, the Hybrid fits and scores in all 34 cells including through the fresh-process
rebuild that hands it a `features.View`, and `evaluate.run_presentation` reproduces the engineer's
counts exactly — 34 cells, 305 L2/L3 lines, 80 tertiary all `not_applicable`, 225 elsewhere all `pass`
with count 0, and no `FAIL` or `FLAG` line of any id in 1,526 log lines. The fix that mattered most to
scrutinise, the `na` parameter, is scoped exactly as narrowly as it should be: it is passed at one
call site in the codebase, no other `measure` call can bind it even positionally, it fires only on the
literal string `tertiary` and only for L2 and L3, and L7, L4, L5, the L2 coverage check and C4's
hyperparameter provenance all still abort or fail on that split, which I confirmed by forcing each of
them. The protocol's numbers, the 18 criterion strings and both file hashes are untouched. What would
change this verdict is a blocker, and I found none: the seven warnings are a stale README acceptance
line, a dataclass default that could make a future regression silent, an ambiguous sentence in
protocol 5.5, two log-attribution gaps, the unexercised 22-presentation scale, and a C4 sub-field that
cannot fire — none of which can make a result invalid, violate a hard constraint, or bypass an
assertion. The code gate's revision budget is spent and this approval is what lets the run proceed;
[W1] and [W6] should travel to the runner dispatch, and [W3] and [W7] to the writer's chapter 3 and
chapter 5.

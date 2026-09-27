---
blockers_count: 0
warnings_count: 5
files_reviewed: 5
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Claude Opus 5
model_identity: claude-opus-5 (top tier) — the artifact under review was produced by the mid-tier
  Experiment Engineer identity, so rule 1 independence holds; I did not write any of the five files
mode: code_review
unit: u13c_diag_review
cycle: 1
scope: the u13b_diag_code diagnostics addition only (D1 alpha logging, D2 behavioural-signal
  ablation). Not a re-review of splits, exclusions, bounds, filters or the criteria machinery,
  which passed G4 across three cycles (review.md, review_cycle1.md, review_cycle2.md), were
  re-verified at G5 (reviews/run_gate.md), and are unchanged by this unit.
---

# Review

Files reviewed: `code/diagnostics.py` (new), `code/main.py`, `code/models.py`, `code/blend.py`,
`code/README.md`. Read-only except `py_compile` and the two existing unit tests, which write
nothing into the project.

## Blockers (must fix before proceeding)
None.

## Warnings (should fix)
- [W1] <severity:med> `code/common.py:82` `code_tree_sha256` / `results/run_receipts/u11_s5_run_main.json`:
  the four changed `.py` files move the code tree hash from
  `694c3ea6026939967a6b01ab0698ef7336e77a8dd29f0739157e9f9662b0231c` (the value in the main run's
  `run_manifest.json`, in its receipt, and in `decisions.log` line 169 as the G4-approved tree) to
  `5a8f935a8dd05bb2b8428966ae9794a2cfe1bf6b7573b5005698bad267691b21` (recomputed 2026-09-22 with
  `.venv-pilot`). `configs/experiments.json` is untouched (`config_sha256`
  `bf2b77c0a85c58f577b132ac755466a23733f8eb3a5b75f4c967d1c42d6a9409`, identical to the receipt).
  Nothing in the receipted main run changes, but the working tree no longer hashes to the receipted
  value, so a later verifier re-running `code_tree_sha256()` sees a mismatch with no explanation on
  disk. Record the old to new hash and the five-file inventory in `decisions.log` / `state.md` at
  u13d, and state in the diagnostics receipt that its tree hash differs from the main run's by
  exactly this unit.
- [W2] <severity:med> `code/main.py:47-51` (`--run-log` is hard-required to be `results/run.log`) and
  `results/run_receipts/u11_s5_run_main.json` (`run_log_after_sha256`): a diagnostics run appends to
  the same shared log, so the whole-file SHA256 of `results/run.log` will no longer equal the main
  receipt's `run_log_after_sha256`. The log is opened append-only (`common.RunLog.emit`, mode `a`), so
  the main run's prior bytes are unchanged, and the receipt's own note already describes prefix
  semantics; this is the same situation the pilot-then-main sequence already created. Still, the u13d
  receipt must carry its own before/after hashes and repeat that the main receipt's value is a prefix
  hash, or a naive whole-file re-verification of the main run will read as a failed receipt.
- [W3] <severity:med> `code/diagnostics.py:44-50`: the diagnostics stage scores the TEST split a second
  time for the production `Hybrid` (and once for `Hybrid_ablated`) by calling `m.score(h)` directly
  rather than `models.score_test`, so this scoring is invisible to the L6 "scored exactly once per
  model" counter. That is correct for isolation (a fresh process with no `ctx["counter"]`, so it cannot
  touch the main run's counts), and C4 as decided by the receipted main run is unaffected. But it is a
  post-hoc second look at the test split, so chapters 3 and 5 must disclose it as a post-hoc
  diagnostic, and neither D1 nor D2 may be used to revise a criterion, a threshold, a model or the
  frozen protocol (rules 3 and 8).
- [W4] <severity:low> `code/tests/test_evaluate.py:49` `test_behaviour_feeds_no_model`: the guard is a
  case-sensitive literal check that `"behaviour"` appears in none of `models.py, blend.py, cell.py,
  features.py, splits.py, provenance.py, leakage.py`. The new code names the concept
  `BEHAVIOURAL_COLUMNS` / `ABLATED_FEATURE_NAMES` and "learner-activity", so it passes partly by
  spelling: `grep -c behaviour` returns 0 for all seven files and the test passes. The substantive
  protection is intact (see Notes), but the guard would now miss a lowercase reintroduction just as
  easily as it missed the uppercase one. Consider also asserting `"import behaviour" not in` each file,
  or lowercasing the text before the check.
- [W5] <severity:low> `code/diagnostics.py:71-84`: the production `Hybrid`'s own warm and A|2 metrics are
  written into `ablation_<pres>.json`, which makes them directly comparable with the receipted
  `results_<pres>.json` from `u11_s5_run_main` — but nothing asserts they agree. Since the whole
  isolation argument rests on the diagnostics `Ctx` reproducing the main cell exactly, an explicit
  equality check (or at minimum a documented comparison step in u13d/u13e) would turn that argument into
  evidence. `README.md` currently only says they "are the point of comparison" in the runner checklist.

## Constraint Audit
- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a
  multi-GPU cluster" | status: satisfied | evidence: `code/diagnostics.py` imports only `numpy`, `json`,
  `data`, `evaluate`, `models`, `splits`, `common`; no CUDA/torch/GPU path is introduced in any of the
  five files, and `code/main.py:118` still records `hardware` in `run_manifest.json` (the receipted main
  run reports "12 logical cores, no GPU") | blocker: none
- [C2] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware" | status: satisfied | evidence: the diagnostics stage runs two cells (warm, A|2) per
  presentation with no new grid beyond the existing C grid, against the receipted main run's 1.014
  CPU-hours for the full multi-split matrix (`results/run_receipts/u11_s5_run_main.json`); its cost is
  recorded in its own `run_summary.json` (`code/main.py:131-139`) and, per `code/verdicts.py:44-50`, is
  not added into C5's main-run accounting | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints for the pilot" |
  status: satisfied | evidence: no new dependency in any of the five files; the ablated blend reuses the
  existing `sklearn.linear_model.LogisticRegression` at `code/blend.py:45-57` | blocker: none
- [C4] "requires network access during the pilot to download OULAD once ... Record this choice" |
  status: satisfied | evidence: `code/diagnostics.py:67` calls `data.load_oulad`, which reads the local
  `raw_dir()` and verifies file hashes (`code/data.py:52-64`); a grep for `urllib|requests|urlopen|http`
  across `code/*.py` returns no match, so the diagnostics stage performs no network access at all |
  blocker: none
- [C5] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits" | status: satisfied | evidence: `code/diagnostics.py:36-47` builds one
  `models.Ctx(prep, cond, 0.0, pres_index)` and fits and scores both `Hybrid` and `HybridAblated` on it,
  so both share `prep`, `cond.fit_ids`/`cond.eval_ids`, the memoised similarity matrix, `N`, the
  exclusion moment (M3 cold / M2 warm) and the single `History` object `h`; `splits.build_prep` is called
  with default `MIN_ITEMS`/`MIN_DAYS`, exactly as `foundation.prepare` does for the main run
  (`code/foundation.py:32-37`), and `pres_index` is the index in `sorted(oulad.rows)`, matching
  `evaluate.run_presentation`'s `ctx["pi"]` (`code/evaluate.py:172`) | blocker: none
- [C6] "report the actual numbers, the gap, and the most likely cause ... rather than adjusting the
  threshold after the fact" | status: satisfied | evidence: `plan.md`'s frozen criteria block and
  `code/verdicts.py` are unmodified, and `configs/experiments.json` still hashes to the receipted
  `bf2b77c0...`; a diagnostics run's non-pilot branch finds neither `ctx["stats"]` nor `ctx["acc"]`
  (never set by `main.run_diagnostics`), so `_combine({None, None})` yields `unchecked` for every one of
  C1-C6 (`code/verdicts.py:33-52`) and `run_summary.json` mirrors those same verdicts — no `met` or
  `not met` can be produced by this stage. W3 records the governance condition that keeps this true |
  blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background" | status: satisfied | evidence: none of the five changed files reads or writes anything
  outside `code/`, `results/run.log` and the stage's own `--artifact-dir` | blocker: none

## Notes
- **Isolation from main, iteration and pilot (check 1) holds.** `diagnostics.py` never calls
  `cell.run_cell`, `evaluate.run_presentation`, `evaluate.finalize`, `foundation.verify`,
  `provenance.emit/coverage` or any `leakage.*` check. It calls exactly `data.load_oulad`,
  `splits.build_prep`, `splits.make_condition`, `models.Ctx/Hybrid/HybridAblated/make_history/pair_mask`
  and `evaluate.cell_metrics`, which is a pure function (`code/evaluate.py:54-81`: no `log`, no counter,
  no file write). Importing `evaluate` does pull in `cell` and `leakage`, whose only import-time effect
  is the `features.BUILDERS.update(...)` registration at the foot of `cell.py` — which nothing in this
  stage executes. `main.check_paths` (`code/main.py:43-51`) still forces the artifact directory under
  `results/run_artifacts/`, refuses a non-empty one, and so cannot overwrite `u11_s5_run_main`'s
  `results_<pres>.json`, `criteria_verdicts.json` or `run_summary.json`. The stage runs in its own
  process with no `ctx["counter"]`, so no leakage counter or provenance record of the main run is
  reachable, let alone writable.
- **The alpha capture is read-only (check 2).** In `models.Hybrid.score` (`code/models.py:346-355`) the
  only new statement is `self.alpha_ = a`, placed after `a = c.blend.alpha(self.X)` and before the
  unchanged `return a[:, None] * cfm + (1 - a)[:, None] * cbm`. It binds an existing local, copies
  nothing, mutates nothing, and `alpha_` is read nowhere outside `diagnostics.py:54` (grep across
  `code/`). Nothing hashes a model object or its `__dict__`: the L7 rebuild digests go through
  `blend.digest_arrays` (`code/cell.py:113-123`) and the ranking hashes through `cell_metrics` on the
  score array, so the added attribute cannot reach any digest. `Hybrid.fit` is untouched. A byte-for-byte
  rerun of `--stage main` would therefore produce identical results; the one thing that would differ is
  `run_manifest.json`'s `code_tree_sha256`, which is W1.
  *Method limitation, stated under rule 6:* `code/` is untracked in git and no pre-change copy of
  `models.py` or `blend.py` exists anywhere in the project, so this is verified by reading the current
  code plus the change inventory (only `blend.py`, `diagnostics.py`, `main.py`, `models.py` and
  `README.md` carry post-main-run mtimes; every other file predates the run artifacts), not by a literal
  diff. That is the strongest check available on this machine, and it is an inspection, not a diff.
- **The ablation is additive (check 3).** `HybridAblated` is instantiated only at `diagnostics.py:37`; it
  is absent from `cell.run_cell`'s `fitted` list (`code/cell.py:49`), from `evaluate.MODELS` and
  `F3_PAIRS` (`code/evaluate.py:23-24`), from `foundation.MODEL_NAMES` (`code/foundation.py:29`) and from
  `plan.md`'s frozen criteria, which name only hybrid, content-based-only, collaborative-only and
  popularity. Every consumer of a model key uses exact equality or a fixed tuple — `m.name == "Hybrid"`
  (`cell.py:74`), `M(..., "Hybrid")` dict lookups, `k.startswith("Random|")` — so the key
  `"Hybrid_ablated"` cannot be captured by a `"Hybrid"` lookup anywhere. `blend_features` and `fit_blend`
  both default `ablate=False`, and every production caller (`models.Hybrid.score`, `Ctx.blend`, and
  `cell._b_C/_b_model/_b_std` through `Ctx.blend`) uses the default; each new branch in `fit_blend` is
  guarded (`if not ablate` around `ctx.val_features` and the three `ctx.rec` calls; `ctx.info["blend"]`
  versus `["blend_ablated"]`), and `Ctx.blend_ablated` is memoised under its own key so fitting it cannot
  overwrite the production blend. `reproduce_phase1.py` (the C6 pilot path) references neither blend nor
  Hybrid, so it is untouched.
- **The ablation drops exactly three columns (check 4).** `blend.FEATURE_NAMES` is
  `(n_visible, log1p_visible_clicks, n_active_days, cf_top1, cf_top10_mass, cbf_top1, cbf_top10_mass,
  week_missing_share)` and the `np.column_stack` in `blend_features` builds the matrix in that exact
  order. `BEHAVIOURAL_COLUMNS = (0, 1, 2)` therefore removes precisely `n_visible`,
  `log1p_visible_clicks` and `n_active_days`, and `ABLATED_FEATURE_NAMES` keeps `cf_top1`,
  `cf_top10_mass`, `cbf_top1`, `cbf_top10_mass` and `week_missing_share` — matching
  `methodology/protocol.md:975-979` (section 8.1 step 3) for the production hybrid. One consequence to
  keep in mind downstream: the ablated matrix has five columns, so `blend.SHIFT_COLUMNS = (3,4,5,6)` and
  `cell.py`'s hard-coded warm-feature-shift indices would be meaningless on an ablated `X`. Nothing
  currently applies them to one (`diagnostics.py` computes no feature shift), so this is a note, not a
  warning.
- **Neither diagnostic can decide a criterion (check 5).** See [C6]. In addition, no downstream consumer
  reads these files: a grep for `alpha_log_` / `ablation_` across `thesis/`, `results/*.md` and
  `state.md` returns nothing, and no code globs `results/run_artifacts/`. `README.md:140-183` documents
  both outputs as deciding no criterion and predicts `criteria_verdicts.json` all `unchecked`, which
  matches what `verdicts.build` will actually produce. One small inaccuracy in that checklist: a
  diagnostics run does execute two measured assertions inherited from `splits.build_prep` —
  `P2_rows_outside_catalogue` and `SPLIT_EXCLUDED_LEARNERS` — so `run_summary.json.assertions` will not
  be empty (its `unchecked` list will be). The README's "runs no L1-L9 leakage check" is correct as
  written.
- **The Module D guard still protects what it was written to protect (check 6).** `"Hybrid_ablated"`
  does not contain the forbidden literal `"behaviour"`, and `grep -c behaviour` returns 0 for all seven
  guarded files. More importantly the substance holds: `behaviour.py` is imported only at
  `evaluate.py:14` and called only at `evaluate.py:184` (`res["behaviour"] = behaviour.describe(prep)`,
  descriptive output); `diagnostics.py` never calls it, and the three columns D2 drops are the blend's
  own pre-existing features, built from the learner's visible history inside `blend_features`, not
  Module D outputs. So no descriptive Module D feature reaches any model, approved or diagnostic. W4
  records that it is the guard's wording, not its intent, that the new naming skirts.
- **Tooling (check 7), run by me with `.venv-pilot\Scripts\python.exe`, `PYTHONDONTWRITEBYTECODE=1`,
  `PYTHONUTF8=1`.** `py_compile` on `diagnostics.py`, `main.py`, `models.py`, `blend.py`: **pass** (the
  fifth changed file, `README.md`, is Markdown and is not compiled). `tests/test_evaluate.py`: **pass**,
  5 of 5 including `test_behaviour_feeds_no_model`. `tests/test_metrics.py`: **pass**, 11 of 11. Neither
  test wrote anything into the project.
- Determinism of the shared `Ctx`: fitting `HybridAblated` after `Hybrid` cannot perturb the production
  fit. `Ctx.blend` is already memoised by then, `fit_blend(ablate=True)` writes only
  `ctx.info["blend_ablated"]`, and neither `StratifiedKFold(random_state=SEED)` nor lbfgs
  `LogisticRegression` draws from a global RNG. The only shared mutable state the ablated fit touches is
  the A5 counters (`ctx.a5_bad`, `ctx.a5_rows`), which this stage never asserts on and which do not
  exist in the main run's process.

## Overall
Approve. Within the scope I was given — is the addition genuinely isolated from, and inert with respect
to, the receipted pipeline — it is: `diagnostics.py` touches none of `cell.run_cell`,
`evaluate.run_presentation`, the leakage counters or the main unit's artifact directory; the one-line
`Hybrid.alpha_` capture cannot change what `score` returns or what any digest sees; `ablate` defaults to
`False` on every production call path and `"Hybrid_ablated"` appears in no criterion, model tuple or
lookup; the dropped columns are exactly the three named ones and the five kept match protocol 8.1 step 3;
and the stage is structurally incapable of writing a `met` or `not met` verdict because
`verdicts.build`'s non-pilot branch has neither `stats` nor `acc` to read. `py_compile` and both unit
tests pass. I found no blocker. The five warnings are bookkeeping the runner and the writer must carry
rather than defects in the code: the receipted tree hash and the shared `run.log` both change under a
diagnostics run and need saying in u13d's receipt and decision log, and the second, uncounted scoring of
the test split needs disclosing as post-hoc. What would change this verdict: evidence that a diagnostics
run writes into `results/run_artifacts/u11_s5_run_main/`, or that D1/D2 output is later used to revise a
criterion, a threshold or a model. This verdict was written by hand, with no MCP tool validating it,
because `ar-workflow-engine.py` imports `fcntl` and cannot run on this Windows machine — per rule 6 the
absence of that automated check is `unchecked`, not a silent pass, and the coordinator's decision log
should carry it.

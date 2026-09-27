---
blockers_count: 0
warnings_count: 1
files_reviewed: n/a
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Claude Opus 5
model_identity: claude-opus-5 (self-reported; the artifact under review — `results/summary.md`
  revision 1 — was produced by the mid-tier experiment-runner seat recorded at `state.md#agents`
  ("experiment_runner: ... last_unit=u11_s5_run_main revision=1") and `decisions.log`
  `event=revision_returned`, a different model identity, so rule 1 independence is verified rather
  than assumed)
mode: run_gate
unit: u12_g5_run_gate
cycle: 1
---

# Review

Scope of this cycle: the three cycle-0 blockers, the four optional warnings, and whether the fix
introduced anything new. Cycle 0 (`reviews/run_gate.md`, not modified by this session) already
audited the run itself exhaustively and found it sound; I re-established that the run is
byte-identical to what it audited (see [N1]) rather than repeating that audit.

## Blockers (must fix before proceeding)
None.

## Warnings (should fix)
- [W1] <severity:low> `results/summary.md`:203-205 (P4b bullet): the corrected ranking sentence is
  arithmetically right, but its last link — "CF 0.0473 > MostPop 0.0471" — is a median gap of
  +0.54% relative (0.047348769743204046 vs. 0.04709634001138893, recomputed from
  `results_summary.json#reporting.P4b_union_median_P10["A|2"]`), with no significance test, in a
  block the same section labels "F4, exploratory -- decide no criterion". The other two links are
  wide (CBF over Hybrid +29.1%, Hybrid over CF +11.6%). Nothing in the sentence overclaims, but a
  downstream reader tallying the ranking could carry "collaborative filtering beats popularity on
  cold start" into chapter 4 as a finding on a gap that thin. Worth one clause of hedging, or an
  explicit "not tested" marker, before the results analyst reuses it.

## Constraint Audit
- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a multi-GPU cluster." | status: satisfied | evidence: unchanged from cycle 0's post-execution audit, and confirmed still current here: all 48 main-stage and 4 pilot-stage artifacts re-hash to the SHA256 values in `results/run_receipts/u11_s5_run_main.json` and `..._pilot.json` (48/48 and 4/4 matched this session), so the hardware record in both receipts ("12 logical cores, no GPU") is the same evidence cycle 0 checked | blocker: none
- [C2] "Prefer scikit-learn or a lightweight model for the pilot; reserve deep learning (RNN/CNN/RBFNN, per the reviewed papers) for the Phase 2 main experiment" | status: satisfied | evidence: `code/` is unmodified since 2026-09-22 11:07 (newest file `code/provenance.py`, 11:07:21), i.e. before the run at 11:48 and long before cycle 0's review at 15:12; the `library_versions` block in both re-hashed receipts still lists only numpy/pandas/scikit-learn/scipy | blocker: none
- [C3] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed hardware" | status: satisfied | evidence: `results/summary.md`:272 now separates the two measures explicitly — "wall-clock time was 3,769 s (~62.8 minutes)" and "the run's 1.014 CPU-hours is about 9% over that projection (1.014 / 0.93 = 1.090)"; ratio recomputed = 1.0903. Both figures still come from the unmodified receipts | blocker: none
- [C4] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." | status: satisfied | evidence: `code/` untouched since 11:07 (no new network or download path could have been introduced) and both receipts re-hash clean; cycle 0's grep-level evidence therefore still applies to the identical code tree `694c3ea6…231c` | blocker: none
- [C5] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and evaluated on identical splits so the comparison in success criterion 1 is fair." | status: satisfied | evidence: the leakage-assertion evidence lives in `results/run_artifacts/u11_s5_run_main/run_summary.json` and `criteria_verdicts.json`, both re-hashed against the receipt this session with 0 mismatches; no artifact changed since cycle 0 verified L4/L5 and `criteria_verdicts.json#C4` | blocker: none
- [C6] "requires network access during the pilot to download OULAD once (a few hundred MB)" — network limited to that one dataset fetch | status: satisfied | evidence: `results/data_manifest.json` (unmodified, 2026-09-22 11:47) and the re-hashed receipts; this revision touched only `results/summary.md`, so the no-download finding from cycle 0 stands on identical files | blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only background; do not attempt to re-scrape or redistribute their content." | status: satisfied | evidence: the revision's only write was `results/summary.md` (2026-09-22 15:14, the sole file under `results/`, `code/`, or the project root newer than cycle 0's review at 15:12 apart from the coordinator's own `state.md`/`decisions.log`/`workflow_queue.json`); no reference PDF is read, copied or quoted by the new text | blocker: none
- [C8] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most likely cause … rather than adjusting the threshold after the fact." | status: satisfied | evidence: no threshold or criterion string changed in this revision — `criteria_verdicts.json` (both stages) re-hashes to its receipt value, and `results/summary.md`'s Verdict section still reports C2 `not met` at median -30.28% and C3 `not met` with all 20 failing presentations named. The revision moved only reporting text in the Sensitivity and Issues sections | blocker: none
- [C9] "Record this choice and its limitation (OULAD is a UK Open University population, not the thesis's own institution) explicitly in plan.md and results/summary.md." | status: satisfied | evidence: **now present** at `results/summary.md`:266-268, in Issues/Caveats beside the licence caveat: "**Population limitation:** OULAD is a UK Open University cohort (32,593 rows in `studentInfo.csv`), not the candidate's own institution; per `idea.md`'s dataset decision this limit travels with the results, alongside the licence caveat above (`plan.md`:70-73 carries the same limitation)." Substantively equivalent to the idea file's own words ("UK Open University population" → "UK Open University cohort"; "not the thesis's own institution" → "not the candidate's own institution"), and the one new fact it adds is verified: `studentInfo.csv` holds exactly 32,593 data rows (counted this session from `data/projects/e_learning_pilot/data/raw/studentInfo.csv`), matching `plan.md`:73. This was cycle 0's B3 and its `violated` status; it is resolved | blocker: none

## Notes
- [N1] **The run is provably unchanged since cycle 0.** All 48 files under
  `results/run_artifacts/u11_s5_run_main/` and all 4 under `.../u11_s5_run_main_pilot/` re-hash to
  the SHA256 values recorded in their receipts (48/48, 4/4, zero mismatches). Both receipts are
  dated 14:55:14, `plan.md` 2026-09-20 15:43, the newest file in `code/` 2026-09-22 11:07 — every
  one of them older than cycle 0's verdict (15:12). `results/summary.md` (15:14) is the only
  reviewed file that moved. The revision was scoped exactly as dispatched.
- [N2] **B1 verified by recomputation, not by reading.** `results/summary.md`:203-205 now reads
  "cold-start median Precision@10 is 0.0529 (Hybrid) vs. 0.0683 (CBF) vs. 0.0473 (CF) vs. 0.0471
  (MostPop) -- same qualitative ranking (CBF 0.0683 > Hybrid 0.0529 > CF 0.0473 > MostPop 0.0471
  on cold start) as the primary split's per-presentation medians." Read from the artifact:
  `reporting.P4b_union_median_P10["A|2"]` = Hybrid 0.052861847961545305, CBF 0.06825929377653515,
  ItemKNN-CF 0.047348769743204046, MostPop 0.04709634001138893 — rounding to 4 dp gives exactly
  0.0529 / 0.0683 / 0.0473 / 0.0471, and `CBF > Hybrid > CF > MostPop` is true as stated. The
  "same qualitative ranking as the primary split" clause also holds: I recomputed the primary
  per-presentation medians from all 22 `results_<pres>.json` files (`splits.primary.cells["A|2"]`)
  and got MostPop 0.0266, CBF 0.0728, CF 0.0377, Hybrid 0.0473 — the same ordering. The old error
  is gone and the 0.0473 that remains in the table at line 142 is the primary split's own cold
  Hybrid median, which is correct there.
- [N3] **B2 verified as a genuine correction, not a cover-up.** `reporting.tertiary_sign_reversal_vs_primary`
  reads `{"warm|None": {"vs_CBF": false, "vs_CF": true}, "A|2": {"vs_CBF": true, "vs_CF": true}}`
  — three true, one false, and the false one is exactly the cell whose label was removed. Line 189
  now reads "| Tertiary split (pilot's random 20%) | +167.11% | -3.57% (sign reversal) | +105.56%
  (sign reversal) | -3.99% (sign reversal) |": three labels, matching the three `true` entries and
  the prose at line 195 ("reverses three of the four signs"). No other cell in the row was altered
  to absorb the change, and the magnitudes still match `tertiary_median_rel_gain` exactly
  (1.6710582613, -0.0357180652, 1.0556430313, -0.0399271118). I also re-checked the row above it:
  `secondary_sign_reversal_vs_primary` has `warm|None.vs_CBF: true` and the other three false,
  which is precisely the one label line 188 carries.
- [N4] **The four optional warnings were applied and are arithmetically sound.** W1: line 246 now
  says 95 per presentation with the breakdown "L1 1, L2 70, L3 10, L9 14, from 2,090 tertiary
  `not_applicable` records over 22 presentations" — 1+70+10+14 = 95 and 95x22 = 2,090, both check.
  W2: the L2/L3-versus-L1/L9 counting-convention note is present in the same bullet and its
  arithmetic holds (5,896 = 4,356+1,540; 814 = 594+220). W3: line 25 now marks the pre-run test,
  refusal-check and canary passes "**unreceipted** ... `unchecked` rather than verified", which is
  the correct rule-6 disclosure rather than a claim of verification. W4: line 272's clauses are
  now separated as noted under [C3].
- [N5] The whole sensitivity table was re-derived from `results_summary.json` while checking B2, so
  the fix is confirmed not to have disturbed neighbouring cells: secondary -3.77/+18.63/-51.03/
  +85.30, P4a-3 +31.20/+10.70/-28.24/+11.31, P4a-10 +30.16/+10.71/-29.71/+7.09 all match the
  artifact to the printed precision.
- [N6] **Manual-write deviation.** This verdict was written by hand, with Write, to the path the
  manager named. The review MCP tool could not run (`ar-gemini-review-mcp.ts` persists through
  `ar-workflow-engine.py`, which imports `fcntl`, unavailable on Windows Python), so no tool
  injected `model`, `unit` or `cycle`, and no tool validated the Constraint Audit. I ran
  `ar-review-contract.ts`'s checks on this draft myself: 0 `[B#]` entries and `blockers_count: 0`;
  1 `[W#]` entry and `warnings_count: 1`; nine Constraint Audit entries, one per hard constraint in
  `idea.md`, each with status, evidence and a `blocker` field; every entry `satisfied` with
  `blocker: none`; no non-`satisfied` entry exists, so none is left without a blocker behind it.
  Cycle 0's `reviews/run_gate.md` was read but not modified.

## Overall
Approve. All three cycle-0 blockers are fixed correctly at the source of the error, not papered
over: the P4b Hybrid median is now 0.0529, which I recomputed from the cited artifact field rather
than accepting the runner's report of it, and the ranking sentence built on it is both
arithmetically correct and genuinely the same ordering as the primary split it claims to match;
the removed "(sign reversal)" label corresponds to the one `false` entry in
`tertiary_sign_reversal_vs_primary`, leaving the table consistent with both the artifact and the
adjacent "three of the four signs" prose; and the population-limitation caveat now carries the
idea file's own substance, not a token sentence, with its one new number (32,593 rows) verified
against `studentInfo.csv` itself. Nothing outside `results/summary.md` moved — all 52 receipt
hashes still match, `plan.md` and `code/` predate the previous verdict — so cycle 0's exhaustive
audit of the run remains in force and constraint C9, its only `violated` entry, is now `satisfied`.
What would change this verdict: a figure in the revised text that failed to trace to
`results_summary.json`, a receipt hash that no longer matched its artifact, or a sign-reversal
label removed where the artifact recorded `true`; none of the three occurred. The single warning
is a hedging suggestion about a 0.54% exploratory margin and does not bear on any criterion, so
gate G5 passes and the experiment stage can close.

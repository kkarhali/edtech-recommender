---
blockers_count: 1
warnings_count: 5
files_reviewed: thesis/front_matter.md (e6d1bcdf), thesis/ch01.md (23866a35), thesis/ch03.md (874aa052), thesis/ch05.md (63276615), thesis/ch06.md (c5adbf27), thesis/claim_ledger.csv (d6af70b4, 580 rows), thesis/figures/figure_5_2_coldstart_relative_gain_spread.png (743385f2), thesis/figures/captions.md (b2573378), thesis/figures/make_figure_5_2.py (22f03a74, existence and hash only), thesis/tables/table_5_14_condition_a_vs_b.md (4e7b1ce7, unchanged), results/run_artifacts/u11_s5_run_main/results_<pres>.json (22), criteria_verdicts.json (8f779bca)
reviewer: manual (project engine unavailable on Windows; ar-workflow-engine.py imports fcntl — see thesis-reviewer SKILL.md). Hand-written, self-checked against review_md.md; deviation to log.
model: Claude Opus 5.5 (self-reported; top-tier reviewer seat)
model_identity: claude-opus-5-5, top tier, reviewer seat. Fixes produced by writer_B (mid tier, sonnet; u19e_g7_fix) and the results analyst (u19d_fig_fix); I produced none of them.
mode: chapter_gate
gate: G7 (scoped re-pass, fix verification of reviews/chapter_gate_attribution.md)
unit: u19c_g7_repass
cycle: 3 (second pass)
---

# Review

All file hashes match the coordinator's list. `check_claim_ledger.py` → PASS (580 rows, 0 errors,
193 warnings of the pre-existing kinds). Bash used read-only, as dispatched.

## Fix verification

- **B1 fixed.** front_matter.md abstract now states the pilot's cold-start pattern (+73.12% vs CBF,
  −17.90% vs CF, 22 of 22 each) before "this inversion"; C0.6 ledger text matches.
- **B2 fixed, and the numbers are right.** Recomputed from the 22 results JSONs
  (`splits.primary.cells["A|2"|"B|2"].models.<Hybrid|ItemKNN-CF>["P@10"].mean`): paired A→B shift in
  hybrid-vs-CF gain has median **+0.01 pp, 11 up / 11 down**; AAA_2014J goes +68.42% (A) → +15.00%
  (B), a shift of **−53.42 pp**, the largest magnitude of the 22 (next: EEE_2014B +52.83 pp), so
  "reaches about −53 pp … AAA_2014J" is correct in sign and size. **Source of record:** the writer's
  figures are in `thesis/tables/table_5_14_condition_a_vs_b.md` (sha256 4e7b1ce7…, receipted-derived,
  two-pass verified): §2 last paragraph gives "+0.01 pp vs. CF (11 up, 11 down)" and §3's AAA_2014J
  row gives +68.42% / +15.00%. C0.6, C5.37 and C6.13 cite exactly that artifact and hash. Legitimate.
  "At most" is gone; every occurrence (abstract, C5.37, 5.12, C6.13) now says difference of medians.
- **B3 fixed.** C6.33 is stated at the median and names the per-presentation crossings (FFF_2013J,
  FFF_2014J primary; AAA_2013J tertiary) — verified against the JSONs. Same qualifier added in the
  abstract, C5.136, C6.13, C6.24.
- **B4 fixed.** C1.23, C6.13 and K4 now read "under the primary split, the receipted run inverts…".
- **B5 fixed.** New PNG footer: "17 WINS, 3 TIES, 2 LOSSES; TIE = |DIFF| < 1E-12, CORRECTION E2" and
  "right of zero in 17 of 22 and on it in 3"; the markers for EEE_2013J, EEE_2014J and FFF_2014B sit on
  zero; captions.md:58-63 gives 17/3/2 with the E2 note. The SVG-via-Chrome rendering is disclosed
  in decisions.log; the image is legible and plots the same values as before.
- **B6 fixed.** ch03.md:401-403 now says "at k = 2, for the hybrid, CBF and ItemKNN-CF, per
  presentation, on the primary and tertiary splits (Table 5.14)".
- **B7 fixed.** C5.24 and C5.31 now cite table_5_2 (33cb137c), which contains 17/3/2, p_holm
  0.00024128 and n_eff 21; new C5.138 cites criteria_verdicts.json (8f779bca), which holds
  `vs_CF.wilcoxon.median_diff` 0.003091 and `rank_biserial` 0.844156 — both verified.
- **W1, W2, W4 (partly — see B1 below), W6 fixed:** heading and ToC now "…and what the receipted
  cells show"; "together with Table 5.14" dropped from C5.36; Table 5.14 in the list of tables and
  the reading order. W3 largely fixed ("within these receipted cells", "a measured evaluation-design
  effect", "alone" removed).

## Blockers (must fix before proceeding)

- [B1] <severity:med> thesis/ch06.md:100: the W4 rewrite introduced a new overclaim, "The inversion
  is real **across all 22 presentations**". The receipted run inverts the pilot per presentation in
  20 of 22 against CBF and 17 of 22 against CF (3 ties, 2 losses; ch05 C5.35, table_5_2), so the
  inversion is not present in all 22. Say "in the median over the 22 presentations (20 of 22 against
  CBF, 17 of 22 against CF)" or drop the count (rule 2). | impact: a per-presentation statement the
  thesis's own C5.35 contradicts, in the contributions list.

## Warnings (should fix)

- [W1] <severity:low> thesis/front_matter.md abstract length: 454 words (my count, ids and note
  excluded, agrees). The standards' front-matter row requires the abstract to state question,
  method, main numeric result and conclusion **"in under one page"** (standards-excerpt.md:69); there
  is no word limit in the standards or plan. 454 words fits one page single-spaced but not at the
  double spacing many templates require, and the university template is not in the repository
  (SKILL.md open question 1). Not a blocker; the disclosed note hands the decision to the candidate.
  The C0.6 sentence carries most of the growth and could drop the AAA_2014J clause (kept in ch05).
- [W2] <severity:low> thesis/front_matter.md length note: "the contrast that **explains** it" —
  the thesis states the contrast does not explain the inversion; say "the contrast that bears on it".
  (A note, not abstract text; not a ledger claim.)
- [W3] <severity:low> thesis/ch06.md:162 "the most consistent practical finding" and the 6.7 closing
  "the most consistent finding within these receipted cells": an unmeasured superlative replacing
  "most transferable". Harmless but uncited; "a consistent finding" suffices.
- [W4] <severity:low> thesis/tables/table_5_14_condition_a_vs_b.md:98 (carried from the first pass as
  W5): still states ch05 C5.35 and table_5_2 say "18 of 22" and that "this unit edits neither", which is
  now false. **Does not block:** no thesis sentence relies on it, the correction is recorded in
  decisions.log (E2), table_5_2 and ch05, and the table's numbers are all correct. The analyst should
  add a one-line "since corrected (E2)" note and re-hash the rows citing 4e7b1ce7 before submission.
- [W5] <severity:low> thesis/claim_ledger.csv C6.13 is now `partial`, consistent with C5.37 (first
  pass W7 resolved); C6.24 and C6.33 stay `supported` while restating the `partial` C5.37 — they
  restate only its fully supported median-sign part, so acceptable; noted for consistency.

## Constraint Audit

Wording, one regenerated figure from receipted values, and ledger rows; no run, split, model,
download or threshold changed (decisions.log 10:56:54Z, 11:05:52Z).

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume
  a multi-GPU cluster." | status: satisfied | evidence: no new run; figure regenerated from
  results_<pres>.json on the local machine | blocker: none
- [C2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." |
  status: satisfied | evidence: make_figure_5_2.py renders an SVG; no model code touched | blocker:
  none
- [C3] "requires network access during the pilot to download OULAD once" | status: satisfied |
  evidence: no data fetched; headless browser used only to rasterise a local SVG (decisions.log
  10:56:54Z) | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits" | status: satisfied | evidence: no evaluation change; Table 5.14
  n_scored identical across A|2/B|2 | blocker: none
- [C5] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware" | status: satisfied | evidence: no new run | blocker: none
- [C6] "no threshold moved after a run" (idea.md criterion 4; plan.md criteria_frozen) | status:
  satisfied | evidence: C2 threshold line in Figure 5.2 unchanged at 0%; verdicts unchanged | blocker:
  none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background" | status: satisfied | evidence: no reference content changed | blocker: none

## Notes

- The first-pass file reviews/chapter_gate_attribution.md was left unedited.
- The coherence check of the whole thesis now passes: the abstract, ch01 K4/1.7.1, ch05 5.4.1/5.12,
  ch06 6.2 item 2, 6.4, 6.6 and 6.7 all say the same thing. The median direction tracks the split.
  The construction changes only the median CF gain, a difference of medians with the paired caveat.
  Why the split matters is not established. A grep for "only deliberate", "same code and the same
  data", "split alone", "at most" (in this context), "18 of 22" (for this count) and "real and
  reproducible" finds no remaining hit.

## Overall

Decision: **revise**, narrowly. All seven first-pass blockers are fixed and verified. The B2
numbers are correct against the raw results and come from Table 5.14 §2/§3 as cited. The one
remaining blocker is a new phrase from the W4 fix, "real across all 22 presentations" (ch06.md:100).
The thesis's own C5.35 contradicts it (20 of 22 and 17 of 22). It is a one-phrase edit plus a
matching ledger check for C6.13. With it fixed, this gate approves with the warnings above, none of
which blocks, including the stale note in Table 5.14 (W4) and the 454-word abstract (W1).

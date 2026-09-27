---
blockers_count: 7
warnings_count: 7
files_reviewed: thesis/front_matter.md, thesis/ch01.md, thesis/ch03.md, thesis/ch04.md (grep sweep), thesis/ch05.md, thesis/ch06.md, thesis/tables/table_5_14_condition_a_vs_b.md, thesis/tables/table_5_2_coldstart_refit_slice.md, thesis/figures/captions.md, thesis/figures/figure_5_2_coldstart_relative_gain_spread.png, thesis/claim_ledger.csv (C0.6, C1.23, C5.24, C5.31, C5.35-C5.37, C5.133-C5.137, C6.13, C6.24, C6.33), results/run_artifacts/u11_s5_run_main/results_<pres>.json (all 22), critic.md, reviews/critic_seat_a.md, decisions.log
reviewer: manual (project engine unavailable on Windows; ar-workflow-engine.py imports fcntl — see thesis-reviewer SKILL.md). No tool validated this file; it was self-checked against review_md.md's rules. Deviation to log.
model: Claude Opus 5.5 (self-reported; top-tier reviewer seat)
model_identity: claude-opus-5-5, top tier, reviewer seat. The revision was produced by writer_B, mid tier, sonnet (decisions.log 2026-09-26T10:31:32Z dispatch, 10:45:44Z close of u19b_attribution_write); Table 5.14 by the results analyst (u19_attribution_analysis). I produced none of the artifacts under review.
mode: chapter_gate
gate: G7 (scoped re-pass after G8 critic cycle 3; revision cycle 3, the last)
unit: u19c_g7_repass
cycle: 3
---

# Review

Bash was used read-only (hashes, recomputation from the receipted JSON, the ledger checker), as the
dispatch instructs, despite the skill's no-Bash default. Nothing except this file was written.

## What was verified and holds

- **Table 5.14 against the raw artifacts, all 22 presentations** (not only the 4 required):
  `splits.<primary|tertiary>.cells["A|2"|"B|2"].models.<Hybrid|CBF|ItemKNN-CF>["P@10"].mean`
  recomputed independently. Medians and W/L/T match the table exactly: primary A −30.28% (2/20/0) |
  +7.32% (17/2/3); primary B −30.16% (2/20/0) | +13.34% (18/3/1); tertiary A +105.56% (22/0/0) |
  −3.99% (5/16/1); tertiary B +94.77% (22/0/0) | −5.42% (3/18/1). Per-presentation spot values
  checked for AAA_2014J, CCC_2014J, EEE_2014J, FFF_2013J, GGG_2014J (all four cells) match Table
  5.14's rows. EEE_2014J primary A hybrid − CF = +6.9e-18 in P@10 (a float tie), confirming E2.
- **E2 in the thesis text:** 17 W / 3 T / 2 L is used consistently in ch05 C5.24, C5.31, C5.35,
  the embedded Table 5.2 distribution row (ch05.md:251), and table_5_2_coldstart_refit_slice.md
  (lines 72, 81, 83, 85). The unrelated 18-of-22 counts (Module D monotonicity ch05.md:119,
  silhouette ch05.md:126 / ch06.md:41, PopWeek ch05.md:322) are untouched and correct.
- **Stale attribution phrases removed:** "only deliberate change", "same code and the same data",
  "did not run that contrast", "controlled ablation" no longer occur in any chapter. ch04 4.4.1
  (ch04.md:118) already declines to attribute the phase difference to any one change.
- **Hashes:** table_5_14 = `4e7b1ce7…c427`, table_5_2 = `33cb137c…71c7`,
  phase1_reproduced_metrics.json = `f9dabae0…fc59`; every touched ledger row carries the correct
  hash for the artifact it names. `check_claim_ledger.py` → PASS (579 rows, 0 errors, 193 warnings,
  all of the pre-existing kinds: numbers whose id sits on the next line, C0.* ids not in a checked
  chapter).
- ch05 5.4.1 C5.137 and ch06 6.2 item 2's last sentence correctly state that *why* the split
  matters is not established and that the pilot's magnitude gap stays undetermined.

## Blockers (must fix before proceeding)

- [B1] <severity:high> thesis/front_matter.md:47 (C0.6): the abstract says "the direction of **this
  inversion** tracks the evaluation split", but no sentence of the abstract states the inversion
  (lines 38-46 never mention the pilot's cold-start result); the pilot sentence was dropped in the
  rewrite. The ledger row C0.6 still describes a sentence ("The phase 1 pilot reported a median
  +73.12 percent over CBF on cold start in 22 of 22 …") that the abstract no longer contains, and
  omits the +7.32%/+13.34% clause it now does contain (rule 2). | impact: the abstract no longer
  states the thesis's most-cited secondary finding and its ledger row does not match its text.
- [B2] <severity:high> thesis/front_matter.md:47 (C0.6), thesis/ch05.md:382 (C5.37),
  thesis/ch05.md:685 (5.12), thesis/ch06.md:99 (C6.13): each says the corrected construction
  "changes the size/magnitude of the gain against CF (+7.32% against +13.34%)", and ch06.md:99 adds
  "moving the gain … from +7.32% to +13.34% **at most**". Table 5.14 §2 (its own paired analysis,
  re-verified here) shows switching A→B on the primary split moves the gain vs CF by a median
  **+0.01 pp (11 up, 11 down)**, and states the +7.32/+13.34 gap "reflects which presentation sits at
  the median, not a consistent per-presentation shift". "At most" is false: per presentation the
  shift reaches −53.4 pp (AAA_2014J +68.42% → +15.00%) and +17.6 pp (FFF_2013J). The magnitude
  statement may stay, but only as a difference between the two **medians**, with the paired caveat
  beside it (rule 2; invalid conclusion). | impact: the one effect the thesis still attributes to
  the construction is contradicted by the table it cites.
- [B3] <severity:high> thesis/ch06.md:217-221 (C6.33, refutation condition): "a contrast … in which
  moving from Condition A to Condition B changes the sign of the hybrid's gain against CBF or
  against CF. Table 5.14 runs exactly that contrast … and finds no such sign change." Per
  presentation Table 5.14 itself shows strict sign changes: primary vs CF FFF_2013J −3.77% →
  +13.87% and FFF_2014J +2.48% → −2.50%; tertiary vs CF AAA_2013J +0.75% → −4.35% (plus four
  tie↔non-tie moves). As written, the refutation condition is already met by the thesis's own
  table. It must say "the sign of the **median** gain" (and the same qualifier belongs in
  front_matter.md:47 "reverses no comparison", ch05.md:380 C5.136, ch06.md:99 C6.13, ch06.md:161
  C6.24). | impact: an examiner can refute the stated conclusion from the appendix table.
- [B4] <severity:med> thesis/ch01.md:198 (C1.23) "The corrected cold-start condition inverts the
  reading of the phase 1 pilot", thesis/ch06.md:99 (C6.13) "the corrected refit condition inverts the
  pilot's reported pattern": both make the construction the agent of the inversion, then the next
  clause says the inversion tracks the split, not the construction. Under Condition B on the
  primary split the pattern is equally inverted (−30.16% vs CBF, +13.34% vs CF), so the first
  clause is the old attribution surviving in the chapters' own words. Reword to "under the primary
  split the receipted run inverts…" or "on the receipted primary-split cells…". (ch01.md:188 K4
  "inverts under the corrected condition" is descriptively true but should follow the same fix.)
  | impact: residual old attribution in ch01's findings preview and ch06's contribution list.
- [B5] <severity:med> thesis/figures/figure_5_2_coldstart_relative_gain_spread.png (footer: "vs. CF
  … +7.32% (18 WINS, 1 TIE, 3 LOSSES …)", "orange diamonds right of zero in 18 of 22") and
  thesis/figures/captions.md:58-59 ("fall right of zero in 18 of 22, with one exact tie and three
  losses"): stale pre-E2 count for exactly this comparison; E2 is 17 W / 3 T / 2 L. Figure 5.2 is
  cited in ch05.md:39 and ch05.md:208. | impact: the thesis states two different counts for one
  comparison on facing pages.
- [B6] <severity:med> thesis/ch03.md:401-402: "it is reported per model, per presentation and per k,
  in chapter 5 (Table 5.14)". Table 5.14 reports k = 2 only and three of the six models; the B|0,
  B|1, B|5 cells exist in the artifacts but are reported nowhere. Either report them or narrow the
  sentence to "at k = 2, for the hybrid, CBF and ItemKNN-CF" (rule 4 / rule 6: the chapter says
  more was reported than was). | impact: the promise the critic flagged is repointed, not kept.
- [B7] <severity:med> thesis/claim_ledger.csv C5.24 and C5.31: both were repointed from
  criteria_verdicts.json to table_5_14_condition_a_vs_b.md, which contains none of p_holm 0.000241,
  rank-biserial +0.844 or median absolute difference +0.0031 (grep: 0 hits). The claims are true
  (criteria_verdicts.json holds rank_biserial 0.8441558…, p_holm; table_5_2 holds p_holm
  0.00024128 and the corrected 17/3/2), but each row must cite an artifact that contains all its
  numbers: split the rows or point them at table_5_2 plus a row for the rank-biserial/absolute
  difference at criteria_verdicts.json (rule 2). | impact: the central finding's ledger row fails
  the "artifact contains the number" check.

## Warnings (should fix)

- [W1] <severity:med> thesis/ch05.md:361 and front_matter.md:193 (ToC): heading "5.4.1 The phase 1
  pilot reported the opposite pattern, **and why**" promises an explanation the section (C5.137)
  now says is not established. Suggest "…, and what the receipted cells show".
- [W2] <severity:low> thesis/ch05.md:384 (C5.36): "That reproduction, together with Table 5.14,
  rules out a difference in the pilot's arithmetic on EEE_2014J" — Table 5.14 has no bearing on the
  pilot's arithmetic; the ledger row C5.36 (correctly) does not mention it. Drop "together with
  Table 5.14".
- [W3] <severity:med> thesis/ch05.md:382 "that is fixed by the split alone"; ch06.md:161-162 "the
  choice of evaluation split can decide the conclusion … the most transferable practical finding";
  ch06.md:246-249 "the finding most likely to transfer beyond this dataset", "a demonstrated
  evaluation artefact". One exploratory F4 contrast on one dataset, where the splits differ in more
  than one way and the pilot's blend/population/candidate rule were never varied (Table 5.14 §6),
  does not support "alone", a transfer claim, or labelling either split's result an "artefact"
  (which implies a why). Hedge to "within these receipted cells".
- [W4] <severity:low> thesis/ch06.md:100 "The inversion is real and reproducible": the pilot side is
  receipted on EEE_2014J only (C5.36); "reproducible" over 22 presentations is not shown.
- [W5] <severity:low> thesis/tables/table_5_14_condition_a_vs_b.md:98: the source table still says
  ch05 (C5.35) and table_5_2 state "18 of 22" and "this unit edits neither" — now false about the
  thesis after E2. Needs a one-line "since corrected" note (the table hash then changes and its
  rows must be re-hashed).
- [W6] <severity:low> thesis/front_matter.md:216-270: List of tables has no entry for Table 5.14;
  front_matter.md:53 length note says 328 words, the abstract body now counts about 380 with ids
  removed.
- [W7] <severity:low> thesis/claim_ledger.csv C6.13: text "changes only the magnitude against CF"
  differs from the chapter's "at most" wording, and it is `supported` while restating C5.37, which
  is `partial`. Align after B2.

## Constraint Audit

This revision is text, tables recomputed read-only from receipted artifacts, and ledger rows; no
run, split, model, download or threshold was touched (Table 5.14 header: "no new run, no model
refitted"; decisions.log 10:31:32Z).

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume
  a multi-GPU cluster." | status: satisfied | evidence: no new run; Table 5.14 reads
  results/run_artifacts/u11_s5_run_main (receipt u11_s5_run_main.json, hashes match per the table's
  §7) | blocker: none
- [C2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." |
  status: satisfied | evidence: no code changed or run in u19/u19b | blocker: none
- [C3] "requires network access during the pilot to download OULAD once" | status: satisfied |
  evidence: text and read-only recomputation only; nothing fetched | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits" | status: satisfied | evidence: per-presentation n_scored identical
  in A|2 and B|2 cells (table_5_14 header); CBF bit-identical across A/B (table_5_14 §5) |
  blocker: none
- [C5] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware" | status: satisfied | evidence: no new run | blocker: none
- [C6] "no threshold moved after a run" (idea.md criterion 4; plan.md criteria_frozen) | status:
  satisfied | evidence: Table 5.14 labelled F4 exploratory, decides no criterion; C2/C3 verdicts and
  medians unchanged (ch05.md:342, table_5_2 line 81); E2 changes a count only | blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background" | status: satisfied | evidence: no reference content in the changed text | blocker:
  none

## Notes

- The dispatch asked that the thesis "keep that the construction changes the CF magnitude". B2 does
  not remove that; it requires it to be stated as a difference of medians with Table 5.14's own
  paired caveat, because the table's analyst already wrote that the median gap is not a consistent
  shift. That is the only formulation the artifact supports.
- ch05.md:262 and table_5_2 report "3 ties" beside a Wilcoxon with "one exact zero dropped,
  n_eff 21": consistent (the two float ties are non-zero to Wilcoxon), and the text explains it.
- ch03 3.5.2's "the difference between them **is** the optimism of the cheap construction" is a
  pre-registered definition; the measured difference turns out not to be uniformly optimistic
  (tertiary B is further below CF than A). Worth a clause in 5.4.1, not a finding here.
- Checker warnings at ch06.md:219-220 are the C6.33 bullet whose id sits on line 221; not a defect.

## Overall

Decision: **revise**. The core numbers are right — Table 5.14 and the E2 count reproduce exactly
from all 22 receipted results files, the hashes are correct, and the main reframe (direction tracks
the split, why is unestablished) is present in ch05, ch06 and the abstract. But the revision leaves
the abstract without the inversion it refers to (B1), keeps attributing a CF magnitude change to
the construction that Table 5.14's own paired analysis contradicts (B2), states a refutation
condition the thesis's own table already meets per presentation (B3), keeps "the corrected
condition inverts" in ch01 and ch06 (B4), leaves Figure 5.2 at 18 wins (B5), and overstates ch03's
pointer (B6) and two ledger rows' artifact (B7). All seven are wording, caption/figure and ledger
fixes needing no new computation; with them applied (and the median qualifier added throughout)
this would approve.

- unit: u16_s9_critic
- cycle: 3
- seat: A
- model_identity: top tier, claude-opus-5-5 (Claude Opus 5.5, self-reported; the dispatch labelled the top-tier seat claude-opus-5)
- verdict: needs_revision
- confidence: high
- required_next_focus: in ch05 5.4.1 report the Condition B (optimistic, shared-similarity) cells at k = 2 on the primary split beside Condition A at k = 2 for Hybrid, CBF and ItemKNN-CF, per presentation with medians and win counts, read from the existing receipted results_<pres>.json of u11_s5_run_main with new ledger rows and labelled F4 exploratory, as ch03 3.5.2 and 3.12 and human decision Q1 promise (if those cells are absent from the artifacts, say so and withdraw ch03's "measured rather than asserted" sentence instead); rewrite the pilot-inversion attribution in the abstract (C0.6), ch01 K4 and C1.23, ch05 5.4.1 (C5.36, C5.37) and 5.12, and ch06 6.2 item 2 (C6.13), 6.4 (C6.24), 6.6 (C6.33) and 6.7 so that it states what the A-versus-B contrast and Table 5.8's tertiary row (refit condition held, pilot's random split: hybrid +105.56% vs CBF and -3.99% vs CF, the pilot's direction) actually show, deleting "the cold-start construction is the only deliberate change" and "on the same code and the same data"; re-run the G7 chapter gate over the rewritten sections and the new ledger rows with a reviewer identity distinct from the writer who makes the change
- optional_next_focus: add table D.4 of thesis/tables/table_module_d_behaviour.md to ledger row C5.132's artifact (G7 module D cycle 2 open warning W2); resolve or record the ledger reverse-hash residue 3ef15512 vs 4f248439 (G7 module D cycle 2 open warning W1); state in ch05 5.4.1 that the reproduction (C6) covers EEE_2014J only, so "not the code" rules out the pilot's arithmetic on one presentation, not a code difference between phase 1 and phase 2
- stop_reason: none

# Critic Review

## Blocking Gaps

1. **The thesis's causal explanation of the pilot inversion is contradicted by its own Table 5.8,
   and the contrast that would test it was run but is never reported.** This is a headline claim,
   not a side remark: it is the abstract's sentence C0.6 ("an artifact of its cold-start condition,
   not its code"), contribution K4 in ch01, contribution 2 in ch06 6.2 ("A demonstration that the
   cold-start condition, not the code, decides that conclusion"), and what ch06 6.4 and 6.7 call "the
   most transferable practical finding" / "the finding most likely to transfer beyond this dataset".

   - *What the thesis says.* ch05 5.4.1 (line 370): "The cause is the cold-start condition, not the
     code." Line 373: the attribution rests on the reproduction "and the fact that the cold-start
     condition is the only deliberate change to how the slice is built", and "the two conditions were
     not run as a controlled ablation of one another under the receipted design". ch06 6.2 item 2
     repeats "the only deliberate change"; ch06 6.6 says "This thesis did not run that contrast";
     ch06 6.4 says the leaky slice "inverted the direction of this thesis's central comparison, on the
     same code and the same data".
   - *Contradiction 1, a measurement in the thesis itself.* Table 5.8 (ch05 5.6.2, from
     `results_summary.json#reporting`) gives the tertiary split, the pilot's random 20% construction,
     with the **refit** cold-start condition A at k = 2 (ch04 C4.8 confirms condition A runs on the
     tertiary split): hybrid **+105.56% vs CBF** and **-3.99% vs CF**. That is the pilot's direction
     (above CBF, below CF), obtained with the corrected cold-start construction held fixed, the same
     phase 2 code, the same evaluated population and the same learned blend; only the split differs
     from the primary row (-30.28% vs CBF, +7.32% vs CF). So the one near-controlled contrast on disk
     points at the **split**, not the cold-start construction, as what flips both signs. The chapters
     report the tertiary row only as "reported for comparability with phase 1" and never connect it to
     the attribution.
   - *Contradiction 2, internal to ch06.* ch06 RQ3 (lines 72-74) says the phase 2 design "also changed
     the split, the cold-start construction and the exclusion rules", so the improvement "cannot be
     attributed to the learned weight alone". The same logic defeats "the cold-start construction is
     the only deliberate change" in 6.2 item 2 and ch05 5.4.1. Phase 1 to phase 2 also changed the
     blend weight, the CF normalisation (review.md default 4), the P4b day filter and the split.
   - *Contradiction 3, the controlled contrast exists.* ch03 3.5.2 (lines 392-403) defines Condition
     B, the pilot's shared-similarity construction, run "on identical splits with identical test sets
     and identical k", and promises that the A-minus-B difference "is the optimism of the cheap
     construction, measured rather than asserted, and it is reported per model, per presentation and
     per k"; ch03 3.12 repeats "reported beside the optimistic construction it replaces so the
     difference between them is measured rather than argued". ch04 C4.8 says condition B ran at k of
     0, 1, 2 and 5 on every split of every presentation. The human decision Q1 (state.md) is "report
     both conditions ... the pilot's thin-history condition kept and labelled optimistic". Yet
     "Condition B" does not appear once in ch05, ch06 or results/summary.md, and ch05/ch06 then say the
     contrast was not run. That is a promised, human-decided result left unreported (rule 4) and a
     sentence that says a measurement is absent when the run contains it (rule 6 in reverse).
   - *Why this would change the conclusion.* The A|2-versus-B|2 contrast on the primary split is
     exactly the test ch06 6.6 names as the evidence that would overturn the attribution. Together
     with the tertiary row it will either confirm the attribution (then say so with numbers) or show
     that the inversion comes mainly from the split (then contribution 2, K4, the abstract's C0.6 and
     ch06 6.4's "most transferable" finding must be rewritten to "the evaluation design, chiefly the
     split, decides the direction"). Either outcome changes what the thesis tells the examiner about
     why its central result differs from the pilot. The G7 gate for ch04-06 (item 13) accepted the
     sentence because it was hedged as "a design argument, not a measured contrast"; the hedge is
     itself wrong, because a measured contrast exists and a second one already disagrees.
   - *Defect type.* Reporting and analysis from existing receipted artifacts: no new experiment, no
     criterion, threshold or verdict moves (C1 met; C2, C3 not met; C4-C6 met all stay). Hence
     `needs_revision`, not `needs_more_research`.

## High-ROI Improvements

- The three required items above, in order: (1) one exploratory table in ch05 5.4.1 of A|2 vs B|2 on
  the primary split for Hybrid, CBF and ItemKNN-CF from the existing per-presentation files, with
  ledger rows; (2) one rewrite of the attribution in the nine places listed, reading the A-vs-B table
  and the tertiary row together, and naming every design change between phase 1 and phase 2 rather
  than one; (3) a scoped G7 re-pass on those sections and rows by a reviewer who did not write them.
- Cycle 2's two required items are resolved on the evidence I read: ch05 5.1.4 (lines 134-135), ch05
  5.11 limitation 12, ch05 5.12, ch06 6.1 RQ1 (lines 40, 50-58) and ch01 Table 1.2 (line 66) now say
  RQ1's descriptive half covers three of four named families, that activity type was never a
  learner-level Module D feature, and that day-ordered sequence is covered only by two scalar
  summaries; `reviews/chapter_gate_module_d_cycle2.md` is `approve_with_warnings`, 0 blockers.

## Low-ROI / Ignore

- Table numbering in ch05 (5.13 appearing first): disclosed at ch05 lines 11-17; cosmetic.
- Abstract at 328 words against a brief of about 250: a regulations question for the candidate.
- The run.log prefix-hash note (ch05 C5.118), the unreceipted pre-run tests, hand-written receipts:
  all disclosed as limitation 11 and in ch04.
- Any new experiment on the closed criteria (a fixed-alpha sweep, a behavioural component, a deep
  model): correctly listed as future work under a new pre-registration; running one now would be
  knob-turning on a closed criterion (rule 3).
- review.md is the G4 cycle 0 code review (2 blockers, 12 warnings); state.md and results/summary.md
  record the blockers fixed in code revision 3 and approved at G4; not a live gap.

## Rationale

Stage S9, unit u16_s9_critic, cycle 3 of max_cycles 3. The manager's stop rationale (state.md
`stop_reason`): the main experiment and both diagnostics are complete and receipted, all six criteria
are judged, and the result is a terminal partial one. I attacked it and it holds for the
**experiment**: raw counts checked against results/summary.md and ch05 Tables 5.2, 5.3 and 5.8 —
warm, hybrid beats CBF in 16 of 22 and CF in 17 of 22 (C1 met, vs-CF margin 0.68 pp); cold-start
refit, hybrid loses to CBF in 20 of 22 and beats CF in 18 of 22 with 1 tie (C2 not met on the
threshold), C3 all four conjuncts in 2 of 22; the cold-start claim is judged against both baselines
and a popularity baseline, with a random floor showing only CBF clearly above chance; the split is
time-based; the cold-start slice is refit; the population (engaged UK Open University learners,
27,212 of 29,228 after two filters) and the missing dwell time are stated in limitations 1-3; RQ2 is
reported unanswerable; the behavioural clause stays `unchecked`; the claim ledger holds 574 rows
(565 supported, 9 partial). No further experiment would move a verdict, and a negative/partial result
is a legitimate terminal state (rule 5).

It does not hold for the **thesis's explanation** of its most-cited secondary finding. The inversion
of the pilot is attributed to the cold-start construction in the abstract, two contribution lists,
and the practical-implications and closing sections, while (a) the thesis's own tertiary-split row,
with the refit construction held fixed, reproduces the pilot's direction, (b) ch06 itself lists four
design changes between the phases when discussing RQ3, and (c) the Condition B contrast that ch03
and the human's Q1 decision promised was run on every presentation but is never reported, and the
chapters then say it was not run. Another iteration — reporting one existing contrast and rewriting
one attribution — would change what the thesis concludes about why its central result differs from
the pilot, which is a conclusion an examiner will test against Table 5.8 at the viva. That is a
defect in analysis and reporting, so `needs_revision`.

This is the last cycle of the budget. Budget exhaustion does not change the verdict: per the skill,
the engine (here the manager) records the stop; the verdict stays what the evidence says. If the
budget forbids a fourth cycle, the defect goes to the human and to the blind examiners as a known
open item, not as a pass.

Deviation, recorded as the skill requires: the critic tool cannot run on this machine
(`ar-workflow-engine.py` imports `fcntl`), so this seat file was written by hand and self-checked
against the header checklist; I did not read any other cycle 3 seat file (none exists). I used Bash
read-only three times (a directory listing with line counts, one ch04 line and the ledger status
count with four ledger rows), against the skill's no-Bash note; nothing was written except this file.
I did not open `code/`.

## Bundle manifest
plan.md: 199
review.md: 453
results/summary.md: 278
state.md: 72
decisions.log: 306 (lines 292-306, the tail)
thesis/front_matter.md: 60 (lines 36-60, the abstract; section headings by grep)
thesis/ch01.md: 201 (lines 52-201, objectives, scope, research questions, criteria, contributions)
thesis/ch05.md: 680 (lines 1-140, 200-449, 630-680; section headings by grep)
thesis/ch06.md: 260 (full)
thesis/claim_ledger.csv: 575 (status counts over all rows; rows 227, 276, 287, 354 by grep)
thesis/ch03.md: 806 (lines 380-415, 612-618, 800-806; grep for Condition B)
thesis/ch04.md: 106 (line 106 only, by grep for "tertiary")
reviews/critic_cycle2_consensus.md: 60
reviews/chapter_gate_module_d_cycle2.md: 30
reviews/chapter_gate_ch04_06.md: 314 (lines 285-314)
reviews/critic_cycle1_seat_a.md, reviews/critic_cycle1_seat_b.md, reviews/critic_cycle1_consensus.md, reviews/critic_cycle2_seat_b.md: grep hits for "tertiary" only, no full read
missing files: results/notifications.log; blind_review.md (no blind review yet)

- unit: u16_s9_critic
- cycle: 2
- seat: A
- model_identity: top tier, claude-opus-5 (Claude Opus 5), self-reported
- verdict: needs_revision
- confidence: medium
- required_next_focus: state in ch05 5.1.4, ch06 6.1 RQ1 and ch05 5.11 that activity type, one of the four behaviour families RQ1 names in ch01 1.6 and plan.md, was never computed as a learner-level Module D feature, so RQ1's first half is answered for the click-volume, active-day and day-order families only, with one ledger row pointing at the module's feature list; re-run the G7 chapter gate over the material added after it passed (ch05 5.1.4 with Table 5.13, ch06 6.1 RQ1, the 15 new ledger rows C5.119 to C5.129 and C6.43 to C6.46) with a reviewer seat of an identity distinct from writer_B, re-hashing thesis/tables/table_module_d_behaviour.md and checking each new row against it
- optional_next_focus: renumber the ch05 tables into reading order so the 5.1.4 table is not Table 5.13; refresh state.md's artifacts block ("thesis: not started") and agents block, which now contradict the chapters on disk; record correction E1 against plan.md's Phase 2 Scale-up Notes, where the pilot's +190% is still attributed to criterion 2 (cold start) although E1 established it as the pilot's warm figure, as a deviation note rather than an edit of the frozen plan
- stop_reason: none

# Critic Review

## Blocking Gaps

**1. RQ1 names four behaviour families; the results chapters answer it for three and never say so.**
`plan.md` and `ch01.md`:138 word RQ1 as "which observable VLE behaviours (click volume, active-day
count, day-ordered sequence, activity type) separate learners well enough to carry recommendation
signal". Section 5.1.4 and `thesis/tables/table_module_d_behaviour.md` report six Module D features
— click volume, distinct items, active days, distinct first-opening days, mean gap between new
items, clicks per active day — and none of them is an activity-type feature. `activity_type` appears
nowhere in ch05 or ch06; in ch03 it appears only as an input to the content-based item vectors
(ch03:485) and as the axis of a diversity metric (ch03:572), neither of which is a learner-level
behaviour that separates learners. Section 5.1.4 nevertheless answers RQ1's first half
"descriptively and affirmatively" over the features it has, section 5.12 generalises it to "the six
behavioural features", and ch06 6.1 RQ1 lists four features as the answer. Nothing in chapter 5,
chapter 6 or the table says the fourth named family was not examined.

This is the cycle-1 defect's own type — a promise in chapter 1 that the results chapters do not
deliver — and it is the last instance I can find. It is also a defect by this thesis's own standard:
ch01:7 undertakes that scope decisions "are not left for the reader to find", and dwell time, the
k = 4 default, the missing time bound, the unsegmented protocol and the unchecked behavioural-signal
clause are each named in exactly that way. Under integrity rule 6 an unexamined family is
`unchecked`, not covered. The fix is disclosure, not a run: one labelled sentence in 5.1.4, one
clause in the ch06 RQ1 answer, one line in limitation 7 or a twelfth limitation, and one ledger row.
It changes no number and no verdict.

**2. The Module D material has never passed a chapter gate.**
`reviews/chapter_gate_ch04_06.md` is unit `u15_g7_chapter_gate` cycle 0, written 2026-09-24 with
`blockers_count: 0`, and `reviews/chapter_gate_ch01_03_cycle2.md` is cycle 2, 2026-09-25. Section
5.1.4, Table 5.13, the ch06 RQ1 answer and the 15 new ledger rows were written on 2026-09-26
(`decisions.log`, `u17b_module_d_write`). The only check on them recorded anywhere is the writer's
own "checker PASS" in its close line. So the artifact that closes the cycle-1 defect enters G8
un-reviewed by any seat other than its author, which is what rule 1 and rule 7 exist to prevent. I
checked what a summary-level read can check — the 15 rows exist, carry an artifact and a SHA256, and
the table hash `cfad80d8...0522` in rows C5.119 to C5.129 matches the hash the analyst's close line
records — and the numbers in 5.1.4, in ch06 6.1 and in the table agree with each other everywhere I
compared them. That is not a substitute for the gate.

## High-ROI Improvements

- Section 5.1.4's own framing would carry the first blocking gap almost for free: it already lists
  four properties of Module D "read from the code rather than assumed". A fifth — which behaviours
  the module does and does not measure, against RQ1's wording — belongs in that list.
- Chapter 6 6.1 RQ1's closing sentence ("these behaviours separate learners well enough to describe
  them") is the one place a reader meets the answer without the caveat. Naming the families there
  costs a clause.
- The optional state.md refresh matters more than it looks: `## artifacts` still reads "thesis: not
  started" and `## agents` still reads `results_analyst: status=not_started`, while the dispatch
  correctly points at `## agents` as the place to read real progress. A stale state file is the
  record rule 6 governs.

## Low-ROI / Ignore

- The ch05 table numbers not being in reading order. The writer recorded it, Table 5.13 names its
  own reason, and no claim depends on the ordering.
- The two p95/p05 conventions (40.0 / 8.2 / 23.4 in the table's D.5 against 42.8 / 8.1 / 23.6 in
  panel (a) and in 5.1.4): both are stated, the difference is explained in the table itself, and
  5.1.4 and ch06 use one of them consistently and label it correctly.
- Any further cold-start experiment, fixed-alpha sweep or segmented-hybrid run. C2 and C3 are
  closed criteria; 5.11 limitation 9 already refuses the sweep as knob-turning, and a segmented
  model is a change of design that belongs with the human (rule 8), not in a revision cycle.
- The residual OULAD provenance link, the licence, the university regulations, OQ6, OQ7, OQ8/RQ2,
  Q10, the supervisor's sight of the five proposal-versus-paper discrepancies. Human items, all
  recorded; none is a defect the team can fix.
- The deferred interface and deep models, the dwell-time proxy, the both-ways cold-start reporting
  with refit primary, the English review package, the 5.5 threshold. Human decisions, not defects.

## Rationale

**Would another iteration change the conclusion? No.** The conclusion is: C1 met on warm users
(median +31.20% over CBF, +10.68% over CF, Holm-corrected p 0.011857 and 0.014095, n = 22); C2 and
C3 not met through the same conjunct on the cold-start-refit slice (hybrid −30.28% against CBF,
+7.32% against CF, both p_holm 0.000241; C3's `ge_cbf` true in 2 of 22 while `gt_mostpop`,
`empty_lists == 0` and coverage ≥ 10% hold in 22 of 22); C4, C5, C6 met; the hypothesis partially
supported with its behavioural-signal clause `unchecked`; RQ2 unanswerable by this design. Every
one of those is a receipted number with a ledger row, and the two required items above are a
disclosure and a review — neither can move any of them. A fully evidenced partial result is a
terminal state (rule 5), and I would not ask for another run.

**Why the verdict is not finish_ok.** The skill sets the verdict by defect type, not by whether the
conclusion moves. Both items are defects in reporting and in gate coverage, which is
`needs_revision` by definition; `needs_more_research` would be wrong, because nothing here needs an
experiment. I am aware this consumes a cycle of a budget of 3, and that is not a reason to soften
the word (rule 12 and the skill's step 10).

**I attacked the stop rationale rather than restating it.** `state.md`'s `stop_reason` says the
empirical work has reached a terminal partial result with no further phase in plan.md. Tested
against the plan's own Risks section, that holds: the decisive risk (cold start against CF) was
measured and, unusually, came out in the plan's favour while the CBF direction the pilot got right
by construction failed, and the plan's alpha-near-1 risk was answered in the negative by D1.
Tested against the raw counts rather than the summary sentence, it holds harder than the sentence
does. Warm slice: hybrid above CBF in 16 of 22 and above CF in 17 of 22, so the C1 median is not a
sweep — six presentations lose against CBF (AAA_2013J −7.9%, BBB_2014J −10.6%, FFF_2013B −6.0%,
GGG_2013J −7.2%, GGG_2014B −37.2%, GGG_2014J −11.8%) and five against CF — and the vs-CF conjunct
clears its pre-registered +10% by 0.68 points, which ch06 6.1 RQ4 says out loud. Cold-start slice:
above CBF in 2 of 22, above CF in 18 of 22 with 1 tie and 3 losses. Per module: warm vs CBF positive
in 5 of 7, cold vs CBF negative in 7 of 7. The chapters report both directions of every one of these
and never the friendlier half alone — which the pilot's summary did do, and which is why I checked.
The pilot's own cold-start figure is +73.12% in ch05:363 and in the abstract (C0.6), not the +190%
that correction E1 identified as the warm figure; the withdrawn label-collapse explanation is
recorded as withdrawn in 5.7.5 and in state.md; the random floor (only CBF clearly above it on cold
start, the hybrid indistinguishable from it, CF below it) is carried into the answers, the
hypothesis paragraph and limitation 5 rather than buried in an exploratory table. Dwell time appears
in ch05 and ch06 only as a thing the data does not record. The population is named as engaged
learners, with the 997 learners the second filter removes described in limitation 1.

**The cycle-1 defect is closed.** It is closed in substance, not by a pointer.
`thesis/tables/table_module_d_behaviour.md` (114 lines) tabulates the receipted `#behaviour` block
for all 22 presentations with the run receipt named; ch05 gained 5.1.4 with Table 5.13 in two
panels, the cohort reconciled to `foundation_<pres>.json#counts.evaluated` in 22 of 22, the
silhouette median 0.3274 with its range, quartiles and subsample caveat, and the segment ranks with
their monotonicity counts; ch06 6.1 RQ1 answers in two labelled halves — separation answered
descriptively, recommendation signal not established — and 6.2 refuses a behavioural-component
contribution; the ledger carries 570 rows, 561 supported and 9 partial, with the 15 new rows
(C5.119 to C5.129, C6.43 to C6.46) each citing the table or `code/behaviour.py` with a hash. The two
facts the dispatch told me to hold are both in the chapters and in the table, unsoftened: k = 4 is
the module's default with no search over k, so the silhouettes describe one fit rather than a
winner; and the features have no time bound, are computed in hindsight, feed no scored model, and
therefore could not serve as a cold-start prior without leaking the test period — which is stated as
the concrete reason RQ2 is unanswerable rather than as a generality.

**What I did not do.** I did not open `code/`, so every code fact above is quoted from the chapters
or the table, which say they read it. `results/notifications.log` and `blind_review.md` do not
exist; no blind-review weakness is carried in this bundle. I read `review.md` (the G4 code gate) and
the two chapter gates at header level only. No engine and no critic tool exists on this machine, so
this file is written by hand and reproduces the header contract and the consensus rule myself
(deviations D1 and D2). I listed `reviews/` before writing this file and saw neither
`critic_seat_b.md` nor `critic.md`, but I read neither file's contents, and cycle 1's archived
`critic_cycle1_*.md` files I also left unread: the cycle-1 defect reached me through the dispatch,
and I verified its closure against the chapters instead.

## Bundle manifest

plan.md: 199 (full)
review.md: 28 of 453 (G4 code gate, unit u10_g4_code_review cycle 0: blockers 2, warnings 12, files_reviewed 24)
reviews/chapter_gate_ch01_03_cycle2.md: 22 of 249 (header only; unit u15_g7_chapter_gate cycle 2, approve_with_warnings, 0 blockers, 6 warnings, chapters 1 to 3)
reviews/chapter_gate_ch04_06.md: 22 of 430 (header only; unit u15_g7_chapter_gate cycle 0, approve_with_warnings, 0 blockers, 6 warnings, chapters 4 to 6)
results/summary.md: 279 (full)
state.md: 73 (full)
decisions.log: 289 (last 15 lines only, 275 to 289)
results/notifications.log: absent
thesis/front_matter.md: 371 (abstract claim lines 40 to 51, rows C0.1 to C0.9)
thesis/ch01.md: 220 (headings plus lines 7, 66 to 69, 81, 137 to 143, 166 to 170, 220)
thesis/ch03.md: 825 (lines 30 to 46 plus matches at 158, 159, 485, 572, 793 to 795)
thesis/ch05.md: 679 (all 25 headings, lines 85 to 139 and 646 to 679, plus matches at 363, 364, 366, 399, 638, 652)
thesis/ch06.md: 256 (all 13 headings and lines 22 to 136)
thesis/claim_ledger.csv: 571 (header, status tally 561 supported and 9 partial over 570 rows, and rows C5.110 to C5.129, C6.40 to C6.46)
thesis/tables/table_module_d_behaviour.md: 114 (lines 1 to 30 and 105 to 114)
blind_review.md: absent
critic.md: absent (existence checked, not read)
reviews/critic_seat_b.md: absent (existence checked, not read)
code/: not opened, by the skill's boundary

- unit: u16_s9_critic
- cycle: 1
- verdict: needs_revision
- confidence: medium
- required_next_focus: Report the Module D descriptive results (feature distributions per presentation and the K-Means segments) in chapter 5 with ledger rows against the receipted artifact, and rewrite the chapter 6 RQ1 answer to state both what Module D showed and what D2 showed, or else change the chapter 1 traceability table and the plan's RQ1 pointer to say RQ1 is answered by D2 alone
- optional_next_focus: read the roughly 150 of the 243 ch02/ch03 ledger rows that were never read against their artifact, since 12 attribution or qualifier defects were found in the 92 that were, and re-point or re-word each row that fails; refresh state.md's `## agents` and `## artifacts` sections, which still read writer/analyst/critic `not_started`, `thesis: not started` and `code: revision 2 running` against six chapters, a 555-row ledger and two closed G7 halves on disk; add one labelled reading in chapter 5 section 5.3.2 for why both popularity baselines sit below the random floor on the cold-start slice, for example concentration on early, already-visible catalogue items against later-week held-out items, marked as a reading and not a mechanism
- stop_reason: none

# External Critic Consensus

Consensus by the fixed rule: seat A finish_ok, seat B needs_revision, so any needs_revision wins and the consensus is needs_revision. Required items are seat A's (none) followed by seat B's (one), cut at 3; optional items are seat A's three followed by seat B's, cut at 3, so seat B's optional items (a warm-slice hybrid-versus-MostPop comparison with a note on CF's margin over popularity, table order, state.md refresh) appear only in seat B's own text below, apart from the state.md refresh which seat A also names. No automated engine exists on this machine (fcntl); this file was written by hand by the second seat (seat B) as the skill's manual path prescribes.

Independence: the two model identities differ (seat A claude-opus-5, top tier; seat B claude-sonnet-5, mid tier). Both seat files carry unit u16_s9_critic and cycle 1.

Bundle manifests differ, as the dispatch allowed: both seats read plan.md, results/summary.md, state.md, the decisions.log tail, the front-matter abstract, chapters 1, 5 and 6 and the ledger counts. Seat A also read results/diagnostics_summary.md (60 of 154 lines), the two G7 chapter-gate reports and searched workflow_queue.json; seat B also read the first 40 lines of review.md and did not open the diagnostics summary or gate reports. Both manifests are in the seat texts below. Line counts differ by one or two lines for summary.md and state.md (279 and 73 against 278 and 72), which is a counting convention, not a different file.

## Role Status
- critic_seat_a: status=ok model=claude-opus-5 identity=Claude Opus 5, top tier
- critic_seat_b: status=ok model=claude-sonnet-5 identity=Claude Sonnet 5, mid tier

## critic_seat_a
    - unit: u16_s9_critic
    - cycle: 1
    - seat: A
    - model_identity: Claude Opus 5, model id claude-opus-5, top tier (self-reported; distinct from the mid-tier sonnet writer seats that produced the chapters and from the mid-tier seat B the manager dispatches separately)
    - verdict: finish_ok
    - confidence: high
    - required_next_focus: none
    - optional_next_focus: read the roughly 150 of the 243 ch02/ch03 ledger rows that were never read against their artifact, since 12 attribution or qualifier defects were found in the 92 that were, and re-point or re-word each row that fails; refresh state.md's `## agents` and `## artifacts` sections, which still read writer/analyst/critic `not_started`, `thesis: not started` and `code: revision 2 running` against six chapters, a 555-row ledger and two closed G7 halves on disk; add one labelled reading in chapter 5 section 5.3.2 for why both popularity baselines sit below the random floor on the cold-start slice, for example concentration on early, already-visible catalogue items against later-week held-out items, marked as a reading and not a mechanism
    - stop_reason: The six pre-registered criteria are all judged on two receipted runs with per-presentation evidence published in full, the partial result is reported at its exact strength in both directions and against a random floor, and every route that could still move the conclusion is either a human decision already escalated (OQ7, OQ6, OQ8/RQ2, regulations, supervisor sign-off) or a new pre-registered study that integrity rules 3 and 8 forbid this run to perform on closed criteria.

# Critic Review

## Blocking Gaps

None.

I looked for a blocking gap in five specific places named in the dispatch and in the standards, and
each one is either already reported at full strength or cannot be closed by an iteration this team
is permitted to run.

1. **The blend's cold-start behaviour.** D1 measures the fitted weight on the collaborative
   component over 5,444 cold-start learner records: median 0.5150, quartiles 0.4019 and 0.6181,
   83.9% between 0.3 and 0.7, 0.04% at or above 0.9. On the 20 presentations where content-based
   filtering is the stronger component the median weight on the weaker collaborative component is
   still 0.494, and the hybrid lands between its own two components in 19 of 22. That is the
   thesis's own account of where C2 and C3 find the hybrid, labelled a correlate and not a
   mechanism, with the confirming experiment (manipulating the weight) named as forbidden on a
   closed criterion and carried as future work. A fixed-alpha or content-leaning-alpha sweep is the
   obvious next experiment and it is exactly what rule 3 calls tuning until a number crosses the
   line; run now it could not revise C2, which is closed. So the gap is real as science and is not a
   defect of this thesis.
2. **OQ7, actual new learners.** Cold start here is simulated by truncating an evaluated learner's
   history to k = 2 and refitting without that learner, and the 997 learners whose whole activity
   falls on one or two days — the closest thing in the data to a real new registration — are removed
   by the pre-registered day filter. The thesis states this as limitation 2, states the filter's own
   numbers in limitation 1, and escalates the reading question to the supervisor in chapter 3 with
   the consequence spelled out ("would put the whole filter design in question and would require a
   redesign"). It also supplies the closest available test of the stricter reading: the P4b union
   population, which puts the excluded two-day learners back in, preserves the cold-start ordering
   (CBF 0.0683 > Hybrid 0.0529 > ItemKNN-CF 0.0473 > MostPop 0.0471). The direction of the finding
   therefore survives the approximation to OQ7 that the data allows; the rest is a human redesign
   decision under rule 8, not an iteration.
3. **RQ2 unanswered.** Recorded before the main run by the G4 code review, not discovered after it;
   stated in chapter 1 section 1.3.3 item 4, in Table 1.2 and Table 1.6, as limitation 7 of chapter
   5, as the RQ2 answer in chapter 6 and as future work item 6. Answering it needs a design in which
   a segmentation actually supplies the cold-start prior, which is a changed research question and
   goes to the human (rule 8). It changes the status of one sub-question, not the thesis's
   conclusion, and it is already carried as OQ8 for the human.
4. **Weak baselines.** The comparison set is MostPop, PopWeek, CBF, ItemKNN-CF, the hybrid and a
   random floor. No matrix-factorisation or session model is present, and the deep models are a
   recorded human scope-out. But no claim in the thesis asserts competitive standing against a
   strong baseline: every criterion compares the hybrid with its own two components plus a
   popularity floor, and limitation 8 binds the conclusions to one family of linear score-level
   hybrid. A stronger baseline could narrow the thesis's significance; it could not refute a claim
   the thesis makes, and adding one is a new pre-registration.
5. **Single dataset.** OULAD only, one UK distance-learning cohort, stated in limitation 3, in the
   abstract's bounds sentence, in chapter 1 section 1.6.4 and as future work item 3. No
   generalisation claim exists for a second dataset to overturn.

Two checks the standards make me run on the deciding numbers rather than on a summary sentence, both
clean. The four facts the dispatch told me to verify are carried correctly everywhere I read them:
the pilot's cold-start margin over content-based filtering is +73.12% (range +13.55% to +163.85%)
with +189.54% correctly attributed to the pilot's warm slice, in chapter 5 section 5.4.1, in the
abstract row C0.6, in `results/summary.md` and in state.md's findings, recorded as integrity
violation E1; the warm gain over content-based filtering is "positive in 5 of 7 modules" with AAA
(−1.85%) and GGG (−11.76%) named, in chapter 5 section 5.6.1 and in `results/summary.md`, recorded
as E2; the random-floor reading that only content-based filtering clearly beats chance on cold start
appears in chapter 5 sections 5.3.2, 5.4, 5.5, 5.11 and 5.12 and in chapter 6 sections 6.1, 6.3,
6.4, 6.5 and 6.6 with its exploratory status stated before its numbers every time; the label-collapse
explanation is withdrawn on the wrong-sign evidence (Spearman +0.434, p = 0.0435) in section 5.7.5
and appears nowhere as a cause. And "dwell time" is used in the thesis only inside the quoted frozen
hypothesis, with the proxy declared in chapter 1 section 1.3.3 item 3 and the clause left
`unchecked` in chapter 5 section 5.5 and chapter 6 section 6.3.

## High-ROI Improvements

- **Finish the ledger's attribution audit.** The 243 rows added for chapters 2 and 3 were accepted on
  machine number-matching plus hand vetting of 50 rows, and the cycle-2 gate then read 92 of them
  against their artifacts and found 6 defective, after which the writer's own re-read found 6 more
  (C2.8, C2.19, C2.26, C2.38, C2.47, C2.67). Twelve defects in the rows that were actually read, and
  roughly 150 rows never read, is a rule 2 exposure that a blind examiner can sample into. The
  defects found were mis-citations, dropped qualifiers and one over-stated range (C3.102), none of
  them a deciding number — which is why this is an improvement and not a blocker — but the cheapest
  version of the fix is to read the remaining rows against their artifacts before submission rather
  than to re-derive them.
- **Make state.md tell the truth about what exists.** Its header is dated 2026-09-20, its `## agents`
  block still reads `results_analyst: status=not_started`, `writer: status=not_started`,
  `critic: status=not_started` and `code: revision 2 running`, and its `## artifacts` block reads
  `thesis: not started`, while six chapters, front matter, a 555-row ledger, two closed G7 halves and
  two receipted runs are on disk; `workflow_queue.json` still reads `current_cycle: 0` against a
  dispatch at cycle 1. The `## findings` and `## human decisions` blocks are current, so the file is
  internally inconsistent rather than uniformly stale, and the standards' instruction to read real
  progress from state.md's own sections is what makes that worth ten minutes. The "still open" line
  also lists university regulations twice.
- **Close the one artifact outside the thesis that still carries the pre-correction story.** state.md
  records as open (Q3) that the Thesis Control Room page repeats the pilot's cold-start framing and
  states 32,594 students where every table and chapter says 32,593. It is the one artifact a reader
  outside this project sees, and the thesis's own corrections do not reach it.
- **Answer the question an examiner will ask about Table 5.5.** Section 5.3.2 says plainly that no
  mechanism is claimed, which is honest, but the table's most surprising cells are that both
  popularity baselines sit *below* a random ranker on the cold-start slice (MostPop a median 0.0264
  below it, 3 of 22 wins) and that collaborative filtering does too. Since this table is what demotes
  the surviving half of C2 and the `gt_mostpop` conjunct of C3, one labelled reading — popularity and
  item-item similarity both concentrate on early, frequently-visible catalogue items while the
  cold-start held-out items sit later in the course, which the PopWeek row at 0.0317 above MostPop's
  0.0266 is consistent with — would turn a viva ambush into a prepared answer, without claiming a
  mechanism.

## Low-ROI / Ignore

- Renumbering chapter 5's Tables 5.6 to 5.12 so the sequence reads in order. Recorded as a cosmetic
  assembly decision; every table is referenced before it appears and the numbering rule is stated at
  the top of the chapter.
- The 328-word abstract against a 250-word brief. Disclosed in the file with the exact two sentences
  the candidate should cut first if the regulations impose a hard cap, and the cap is not known.
- Re-hashing the 18 ledger rows that cited `decisions.log`. Resolved by re-pointing them at the frozen
  snapshot `thesis/evidence/decisions_log_snapshot.txt`; chasing a moving hash further buys nothing.
- Re-deriving the G4-approved code tree `694c3ea6…231c`, of which no copy exists. The diagnostics tree
  differs in exactly five files, its inertness was measured rather than assumed (44 of 44 cells, zero
  differences, maximum absolute difference 0.0), both hashes are disclosed in chapters 3 and 4, and
  the prefix run-log hash is disclosed and independently re-hashed by the chapter gate.
- Pressing for the deep models, the user interface, the primary/secondary split question or the
  thin-history-versus-refit reporting choice. All four are recorded human decisions or open
  methodological questions, and the dispatch rules three of them out as decided; nothing here
  reopens them.

## Rationale

The one question is whether another iteration would change this thesis's conclusion. The conclusion
is that the hypothesis is partially supported: C1 met on the warm slice, C2 and C3 not met on the
cold-start-refit slice, C4 to C6 met, the behavioural-signal clause `unchecked`, and the cold-start
half with no evidence of competence in either direction. I attacked that rationale with the raw
per-presentation counts in front of me, not the summary sentences.

Warm slice, primary split, n = 22: hybrid over content-based filtering, median +31.20%, 16 wins, 0
ties, 6 losses, exact Wilcoxon p = 0.005929, p_holm = 0.011857, rank-biserial +0.652, and the
companion sign test disagreeing at p = 0.052479; hybrid over item-based collaborative filtering,
median +10.68%, 17 wins, 5 losses, p_holm = 0.014095, clearing its +10% threshold by 0.68 percentage
points. Per module the warm gain over content-based filtering is positive in 5 of 7 and the gain over
collaborative filtering in 6 of 7 (EEE −21.17%). Cold-start-refit slice at k = 2, n = 22: hybrid over
content-based filtering, median −30.28%, 2 wins, 20 losses, p_holm = 0.000241, rank-biserial −0.858;
hybrid over collaborative filtering, median +7.32%, 18 wins, 1 exact tie, 3 losses, p_holm = 0.000241
at n_eff 21. C3 conjunct by conjunct: `ge_cbf` 2 of 22, `gt_mostpop` 22 of 22, zero empty top-10
lists 22 of 22, coverage at or above 10% 22 of 22, all four together 2 of 22. Against the random
floor on that slice: content-based filtering +0.0310 (16 of 22, p_Holm 0.011014), hybrid −0.0038 (10
of 22, p 0.750238), collaborative filtering −0.0126 (6 of 22, p_Holm 0.092320), MostPop −0.0264 (3 of
22). The pilot, unreceipted prior evidence, had the opposite cold-start pattern: +73.12% over
content-based filtering in 22 of 22 and −17.90% against collaborative filtering in 22 of 22, with
warm +189.54% over content-based filtering and −2.66% against collaborative filtering, winning 3 of
22 by at most +0.91%. Both halves of every comparison are published, and the direction the pilot
never tested is the one that now holds.

The strongest case for another iteration is that the design leaves a fixable defect: a roughly even
blend weight on a slice where one component is clearly stronger looks like something a single
re-fitting or a content-leaning weight could repair, and if it were repaired the cold-start verdict
could flip and with it the thesis's headline. I do not accept that case, for three reasons. First,
the criteria are a pre-registration and C2 is closed; re-running with a new weight until the median
crosses zero is the thing rule 3 names as forbidden, and the thesis has already excluded the
fixed-alpha sweep on exactly that ground and listed it as future work with its own pre-registration.
Second, the repair would not rescue the claim it is supposed to rescue: on this slice the hybrid is
indistinguishable from a random ranker and collaborative filtering sits below it, so the only model
with demonstrated cold-start signal is the baseline the hybrid loses to, and a weight tuned towards
that baseline would be a re-discovery of content-based filtering rather than evidence for a hybrid.
Third, the thesis already states this outcome more harshly than my critique would: chapter 6 section
6.4 tells a platform that for genuinely new learners this hybrid gives no measurable benefit over
ranking at random while content-based filtering does. A conclusion that is already reported against
its own hypothesis's interest is not one an iteration improves.

I checked the remaining paths to a different conclusion and each leaves the project rather than
returning to it. A behavioural recommender component, a segmented prior for RQ2, the deep models, a
second dataset or institution, an actual new-learner population, and a controlled contrast of the two
cold-start conditions are all new designs needing new pre-registration, and four of them are recorded
human scope decisions. The items the chapters leave open are open for the human, not for a model:
university regulations and the language, format, citation style and disclosure wording that follow
from them; the supervisor's sight of the five proposal-versus-paper discrepancies and sign-off on the
two deferred scope-outs; OQ6 on whether C3's accuracy conjuncts stay per-presentation; OQ7 on whether
the cold-start criterion means actual rather than simulated new learners; OQ8 on RQ2's wording; and
Q10. None of them is a defect an iteration closes, and the thesis names each in the chapter where it
bears.

What makes this a terminal partial result rather than an unfinished one is that the evidence is
complete on its own terms and the failures are reported as findings (rule 5). All 22 presentations
appear in both slices with per-presentation values, not a best case. Both corrections found upstream
are applied everywhere and logged as integrity violations rather than quietly fixed. The two
diagnostics carry a post-hoc disclosure naming the second test-split scoring, the different code
tree, and the measured inertness check. The withdrawn label-collapse explanation stays in the record
with the wrong-sign evidence that killed it. The weaknesses that would embarrass the thesis at a viva
are in the thesis: the 0.68-percentage-point C1 margin, the sign test's disagreement, the
secondary-split sign reversal of the warm result, the tertiary split's three reversals, the
ceiling-bound metric, 7 modules rather than 22 draws, the hand-written receipts, the unreceipted
pre-run tests, and the one unverified link in the licence provenance. Chapter 6 also states, for each
conclusion, what would count as evidence against it, which is what lets a reader check rather than
accept it.

Two limits on my own judgement, stated because a verdict with no stated limits is worth less. I read
summary-level artifacts only and opened no file under `code/`, so the one thing that could overturn
this verdict — the blend's alpha model being fitted on learners whose visible history is not
truncated and then applied to k = 2 learners, which would make the cold-start loss an implementation
artifact rather than an architectural finding — I could not verify myself; I rely on the G4 code
review, an independent top-tier seat that traced the blend against all eleven points of the protocol's
section 8.1 and confirmed a refit per presentation, condition and k, on chapter 5 section 5.10 stating
the same, and on D1's per-presentation alpha distributions differing widely across cells as that
refit predicts. And this project has no automated engine: no tool bound this report to its unit,
cycle and model identity, so I reproduced the header contract and the consensus rule by hand as my
own self-check, and the absence of the tool's validation is `unchecked`, not passed.

## Bundle manifest

- plan.md: 199
- review.md: 453
- results/summary.md: 279
- results/diagnostics_summary.md: 60 (of 154)
- state.md: 73
- decisions.log: 277 (lines 258-277, the last 15 events plus the S9 dispatch)
- workflow_queue.json: max_cycles 3, current_cycle 0 (searched, not read in full)
- thesis/ch01.md: 220
- thesis/ch05.md: 621
- thesis/ch06.md: 244
- thesis/front_matter.md: 80 (of 368; abstract and title page)
- thesis/claim_ledger.csv: 4 read plus a full status count: 555 data rows, 9 `partial`, the rest `supported`, 0 `unsupported`, `unchecked`, `pending` or `withdrawn`
- reviews/chapter_gate_ch04_06.md: 70 (of 430; header, blockers, first warnings)
- reviews/chapter_gate_ch01_03_cycle2.md: 90 (of 249; header, blockers, first warnings)

Not read, existence and length only: review_cycle1.md (238), review_cycle2.md (230),
reviews/chapter_gate_ch01_03.md (268), reviews/run_gate.md (168), reviews/run_gate_cycle1.md (116),
reviews/diag_code_review.md (208), reviews/code_gate.md (78), reviews/method_gate*.md,
reviews/plan_gate.md (132), reviews/literature_gate.md (245), thesis/ch02.md (117), thesis/ch03.md
(825), thesis/ch04.md (331), idea.md, inputs/manifest.json, literature/.

Missing files, named rather than invented:
- `results/notifications.log`: absent; no notification tail exists for this project.
- `blind_review.md`: absent; S10 has not run, so there are no previous blind-review weaknesses to
  carry into this bundle.
- `reviews/critic_seat_b.md`: not present when this bundle was built, and not read.
- The G4-approved code tree `694c3ea6…231c`: no copy exists on disk (decisions.log, 2026-09-25
  `artifact_archived`); `final/code_snapshot` holds the diagnostics tree `5a8f935a…691b21`.
- `code/`: deliberately not opened, per the critic protocol.

## critic_seat_b
    - unit: u16_s9_critic
    - cycle: 1
    - seat: B
    - model_identity: Claude Sonnet 5 (claude-sonnet-5), mid tier
    - verdict: needs_revision
    - confidence: medium
    - required_next_focus: Report the Module D descriptive results (feature distributions per presentation and the K-Means segments) in chapter 5 with ledger rows against the receipted artifact, and rewrite the chapter 6 RQ1 answer to state both what Module D showed and what D2 showed, or else change the chapter 1 traceability table and the plan's RQ1 pointer to say RQ1 is answered by D2 alone
    - optional_next_focus: Add a warm-slice hybrid-versus-MostPop paired comparison from the already-scored per-presentation files to chapter 5 (labelled exploratory) and one sentence in section 5.2 saying item-based CF sits only 0.0092 Precision@10 above global popularity at the warm median (0.1707 against 0.1615), so the warm half of the hypothesis is measured against a weak collaborative baseline; renumber or reorder Tables 5.6 to 5.12 at assembly; refresh state.md agents and artifacts blocks, which still read results_analyst not_started, thesis not started and code revision 2 running
    - stop_reason: none

# Critic Review

## Blocking Gaps
The question asked is whether another iteration would change the conclusion. It would not change the empirical conclusion (partial result: warm half C1 met, cold-start half refuted against content-based filtering, C2 and C3 not met). One reporting defect remains, and it is a chapter defect, not a missing experiment.

1. RQ1 has no reported evidence base beyond D2. Chapter 1 (traceability table, section 1.3.3 items 4 and the RQ list) and `plan.md` say RQ1 (which observable behaviours separate learners) is "answered by Module D, chapters 3 and 5" and that Module D "delivers a description of the behavioural features". Chapter 4 says `behaviour.py` produces per-learner descriptive features and K-Means segments with four clusters, and the run artifacts carry silhouette fields (`results_<pres>.json` matched a silhouette search). A grep of `thesis/ch05.md` for "Module D", "cluster", "segment" and "silhouette" returns only limitation 7 (the RQ2 statement). A grep of `ch03.md` and `ch04.md` returns design statements only. So the Module D output the plan promised to answer RQ1 is not shown anywhere I could find at summary level, and chapter 6 answers RQ1 solely from the post-hoc D2 ablation of the blend's feature set, which the thesis itself says measures the blend's weighting and not a behavioural recommender component. That is a mismatch between the stated question, the module that was built to answer it and the answer given. It is a reporting defect (rule 2: a run output either enters the thesis with a ledger row or the claim that it answers RQ1 is withdrawn). I could not verify at summary level that the segments are nowhere in the thesis; the first action of the revision is to confirm that by search of chapters 3 to 5 and either add the results or narrow the RQ1 wording.

## High-ROI Improvements
- Warm slice baseline strength. Table 5.1 shows ItemKNN-CF at a warm median of 0.1707 against MostPop 0.1615 and PopWeek 0.1650, and the hybrid at 0.1720. The C1 pass over CF is by 0.68 percentage points and is already disclosed as narrow, and the secondary split reverses the warm-versus-CBF sign; both are reported honestly. What is missing is a stated hybrid-versus-popularity comparison on the warm slice: from Table 5.1 the hybrid is below MostPop in 4 of 22 (DDD_2013J, EEE_2013J, EEE_2014B, EEE_2014J) and only 6.5% above it at the median. A reader will ask whether "hybrid beats CF warm" means anything when CF barely beats popularity. This can be answered from files already scored; no new experiment.
- Chapter 5 table order (5.1, 5.2, 5.6, 5.5, 5.3, ...) is an open cosmetic item recorded in `decisions.log` and will be noticed by an examiner.
- The Random-floor result (Table 5.5) is exploratory and post-hoc; it is honestly labelled. Nothing further needed beyond what seat outputs already recommend.

## Low-ROI / Ignore
- A fixed-alpha sweep, a content-leaning weight, a stronger CF (ALS or BPR), deep models and the interface: deferred by the human or forbidden as knob-turning on a closed criterion. A further run would test a new hypothesis, not this one, and the cold-start refutation against CBF (2 wins, 20 losses, negative in all 7 modules, unchanged on the secondary split and under both item filters) cannot be reversed by a better CF baseline, since CBF is already the stronger cold-start component.
- The 328-word abstract against about 250: disclosed in the file, pending university regulations.
- The five proposal-versus-paper discrepancies, OQ6, OQ7, OQ8/RQ2, Q10, regulations: human items, not defects.

## Rationale
Checked against the attack list. Corrected upstream facts are carried correctly: cold-start pilot gain over CBF is +73.12% (range +13.55% to +163.85%) and the +190% is labelled as the warm figure (ch05 5.4.1, E1); warm gain over CBF is positive in 5 of 7 modules (E2 correction; Table 5.7 confirms AAA -1.85% and GGG -11.76%); only CBF clearly beats the random floor on cold start (+0.0310, 16 of 22, p_Holm 0.011014) while the hybrid is indistinguishable (10 of 22, p 0.750238); the label-collapse explanation is withdrawn with its Spearman +0.434 wrong-sign evidence. Raw counts are shown, not only summary sentences: cold start vs CBF 2 wins 20 losses, vs CF 18 wins 1 tie 3 losses; warm vs CBF 16 of 22, vs CF 17 of 22; C3 ge_cbf 2 of 22. A popularity baseline (MostPop and PopWeek), a random floor, a time-based primary split, Holm-corrected exact Wilcoxon tests, a sign-test companion, secondary and tertiary splits, item-filter sensitivity and a per-module breakdown are all present. The limitations name the engaged population (997 one- and two-day learners removed, median 49 of 115 resources in EEE_2014J), simulated cold start, 7 modules not 22 draws, and no dwell time; the word dwell time appears only to say it is not measured. The ledger has 555 rows, 546 supported and 9 partial, none unsupported. Chapter 6 answers RQ0, RQ2 (unanswerable, reported as such), RQ3 and RQ4 in the terms chapter 1 sets, and RQ1 is the one question whose answer does not match the evidence the plan promised. Because the empirical work is a fully evidenced terminal partial result and a further experiment would not change its conclusion, the verdict is not needs_more_research; because one reporting defect remains against a stated research question, it is not finish_ok. It is small, one revision cycle of one chapter, and should not reopen any criterion.

Process note for the record: the last 15 lines of `decisions.log`, which this skill requires reading, contain the manager's line recording seat A's returned verdict and optional items. That was visible before this seat's file was written. The judgement above rests on the artifacts read, and `reviews/critic_seat_a.md` was not opened before this file was written. No engine exists on Windows; this file was written by hand.

## Bundle manifest
plan.md: line 199 (whole file)
results/summary.md: line 278 (whole file)
state.md: line 72 (whole file)
decisions.log: line 279 (last 15 lines, 265 to 279)
results/notifications.log: absent (missing file)
review.md: line 40 of 453 (header and first blockers only)
blind_review.md: absent (no blind review exists yet)
thesis/front_matter.md: line 60 of 368 (abstract, section 2)
thesis/ch01.md: line 170 of 220 (lines 76 to 84 and 129 to 170 by excerpt)
thesis/ch05.md: line 470 of 620, plus lines 575 to 620
thesis/ch06.md: line 245 of 245 (whole file)
thesis/claim_ledger.csv: 556 lines (counts by status only: 546 supported, 9 partial, 555 rows)

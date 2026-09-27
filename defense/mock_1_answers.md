# Mock defense 1 — candidate answers (2026-09-27)

    unit: u18_s11_defense_prep        cycle: 1        mock: 1        sub-step: candidate
    date: 2026-09-27
    role: candidate only; this file answers and does not grade
    sources read: defense/mock_1_panel.md; thesis/front_matter.md; thesis/ch01.md (§1.6, §1.7);
      thesis/ch02.md (§2.6-§2.10); thesis/ch03.md (§3.5-§3.8); thesis/ch04.md (§4.5, §4.7, §4.8,
      seed statements); thesis/ch05.md (all); thesis/ch06.md (all); thesis/claim_ledger.csv rows
      C1.23, C2.40, C5.36, C5.37, C5.78, C5.79, C5.137; defense/question_bank.md (rehearsal notes;
      where they go beyond the chapters, the chapters were followed)
    coaching rules applied: answer first, then evidence with its number and section, then the limit,
      then one bridging sentence; double-barrelled questions restated first; no number that is not
      in the thesis text

## Presentation (20 minutes, one line per block)

1. **Problem and research question (2 min).** "I ask whether a hybrid of content-based filtering, item-based collaborative filtering and a behavioural proxy outranks either technique alone, for learners with history and for new ones, on OULAD: 32,593 learner rows, 22 module presentations of 7 modules." (ch01 §1.6.2 RQ0, §1.6.4; abstract)
2. **Gap from the literature (2 min).** "Among the sources I opened, none evaluates a behaviour-aware hybrid with a ranking metric on public learner clickstream data with a cold-start slice refitted without the held-out learners and replicated across course presentations; that is a claim about the sources opened, and 14 items could not be opened." (ch02 §2.8, §2.9)
3. **Data and protocol (4 min).** "29,228 learners appear in the logs and 27,212 are evaluated after two pre-registered filters remove 2,016; each learner is split by day so the latest training or validation day precedes the earliest test day, realised test fraction 0.199 to 0.205; the cold-start slice holds 5,444 learners at k = 2, every fitted quantity rebuilt without them; Precision@10, six criteria frozen before the run, exact paired Wilcoxon with Holm over the 22 presentations; C4 found 0 of 2,992 hyperparameter records fitted outside validation and a maximum test-scoring count of 1 over 7,920 cells." (ch03 §3.5.1, §3.5.2, §3.8; ch05 §5.1.2, §5.5)
4. **Models compared (2 min).** "Six models on byte-identical splits: random (seeds 42 to 46), global popularity, week-aware popularity, CBF, ItemKNN-CF and the hybrid, which scores alpha × CF + (1 − alpha) × CBF, alpha coming per learner from a logistic regression over eight learner-level features fitted on validation only; three of those eight features are the behavioural proxy." (ch03 §3.6; ch04 §4.5.1)
5. **Results, warm and cold, 22-presentation check (6 min).** "C1 is met: warm-user median gains of +31.20% over CBF and +10.68% over CF, p_holm 0.011857 and 0.014095. C2 and C3 are not met: on new learners the hybrid loses a median 30.28% to CBF (2 wins, 20 losses) and gains 7.32% over CF (17 wins, 3 ties, 2 losses), both p_holm 0.000241, and 2 of 22 presentations pass all four C3 conjuncts. Against a random floor only CBF is clearly above chance on cold start (+0.0310 Precision@10, 16 of 22, p_Holm 0.011014); the hybrid is indistinguishable from it (−0.0038, p = 0.750238). The cold-start loss to CBF is negative in all 7 modules. Table 5.14 shows the direction of the pilot-versus-main inversion tracks the split, not the cold-start construction." (ch05 §5.2, §5.3, §5.3.2, §5.4.1, §5.6.1, Tables 5.1, 5.2, 5.5, 5.7, 5.14)
6. **What did not work, limitations (2 min).** "The cold-start half of the hypothesis is refuted against CBF; the C1 margin over CF is 0.68 percentage points; the secondary global cut-off split reverses the warm gain over CBF from +31.20% to −3.77%; my first explanation of the cold-start shortfall, label collapse, was withdrawn because its correlation ran the wrong way (rho +0.434, p = 0.0435); no behavioural component exists, so that clause is unchecked; RQ2 cannot be answered; cold start is simulated and the 997 one- and two-day learners were filtered out." (ch05 §5.2, §5.6.2, §5.7.5, §5.8.2, §5.11; ch06 §6.3)
7. **Contributions and future work (2 min).** "The principal contribution is a receipted negative result on the cold-start claim, alongside a re-runnable leakage-controlled design and a measured split-versus-construction contrast; the next steps are a genuine behavioural component under a new pre-registration, a pre-registered fixed-alpha study, evaluation on actual new learners and a second dataset, and a cold-start design that clears the random floor at all." (ch06 §6.2, §6.5)

## Answers to the panel's questions

### Q1

I cannot rule it out, and I won't pretend otherwise. No syllabus-order or sequential baseline was run. What I can show is narrower: on cold start only CBF is clearly above the random floor, +0.0310 Precision@10 in 16 of 22 presentations, p_Holm = 0.011014, and CBF's item vectors do carry normalised `week_from`/`week_to` (Table 5.5, §3.6). The week-aware popularity ranker, which does use course week, sits below random at −0.0263, but that ranks by popularity within a week, not by syllabus order, so it is weak evidence. One observation only: in the three presentations where week fields are entirely missing, CBF still beat the hybrid in two, BBB_2013B and DDD_2013J (Table 5.2, §5.7.1) — not a test. The fix is a "next unopened resource by `week_from`" ranker added as a new pre-registered baseline, noting it is undefined where weeks are missing. Until then, the cold-start finding says CBF beats the hybrid, not that CBF beats course order.

Sections relied on: ch05 §5.3.2, Table 5.5; ch03 §3.6; ch05 §5.7.1, Table 5.2; ch05 §5.11; ch06 §6.5 item 7.

### Q2

Restating: you ask what actually differs between the splits, and whether I have swapped one unexplained causal claim for another. I have not established a mechanism, and C5.137 is `partial` for exactly that reason. What Table 5.14 does is falsify one explanation: holding the split fixed, moving between Condition A and B changes the sign of no median comparison; holding the construction fixed, moving to the tertiary split reverses both. "Tracks the split" is a statement about which varied factor the sign moves with, not a cause. What is known to differ: the tertiary split has no time bound, so test resources can precede the visible ones, and the hybrid's cold-start Precision@10 is about 3.6 times higher under it (§5.4.1). Which of those differences matters, no receipted cell isolates. The test would be a split that varies only the time bound while keeping the test fraction and candidate rule fixed.

Sections relied on: ch05 §5.4.1, Table 5.14; claim_ledger.csv C5.137, C5.37; ch06 §6.2 item 2.

### Q3

RQ3 answers a narrower question than its wording invites. Under the protocol that decides the criteria, the gap to CF closes: the pilot's hand-picked weight trailed CF on warm users by a median −2.66%, winning 3 of 22, while the phase 2 validation-fitted weight leads by +10.68%, 17 of 22, p_holm = 0.014095 (§6.1 RQ3). But phase 2 changed the split, the cold-start construction and the exclusion rules at the same time, so the closure cannot be attributed to the weight alone. There is one partial check: under the pilot's own random split, re-run inside phase 2, the hybrid with the learned weight still trails CF by −3.57% (§5.6.2) — so the learned weight by itself did not close the gap on that split. Precisely, then: the gap closes under a time-based split with a validation-fitted weight, and the weight's own share was not isolated by any run.

Sections relied on: ch06 §6.1 RQ3; ch05 §5.4.1, §5.6.2, Table 5.8; ch01 §1.6.2.

### Q4

It tells you less than it appears to, and I'd read it that way. p_holm = 0.000241 says that, treating the 22 presentations as exchangeable units, the hybrid-minus-CBF differences are consistently negative: 20 losses in 22, rank-biserial −0.858 (Table 5.2). Because the 22 are 7 modules sharing catalogues and syllabi, the effective sample may be closer to 7, and a p-value that accounted for that would likely be larger; I did not run a cluster-robust or mixed-effects test, so I cannot give you the corrected value. What survives the clustering is direction: the cold-start loss to CBF is negative in all 7 modules (Table 5.7). And C2's verdict does not hang on that p-value at all — it fails on the threshold, a median of −30.28% below zero, which no correction can reverse. A module-level analysis with a module random effect is what I would add.

Sections relied on: ch05 §5.3, Table 5.2; ch05 §5.6.1, Table 5.7; ch03 §3.8; ch05 §5.4, §5.11 limitation 4.

### Q5

Yes, largely — that is a fair description of what the slice measures. Condition A shows each learner their earliest two resources by day and rebuilds every fitted quantity without them, so the model was not shaped by the learner it ranks for (§3.5.2). But those learners passed both engagement filters, and the day filter removed the 997 who look most like new registrants: a median of 8 distinct resources over a median of 2 active days, against 55 resources over 52 days for the 27,212 retained (§5.11 limitation 1). So the slice measures thin visible history among retained learners, and limitation 2 says no result speaks for the excluded ones. One partial check: adding the two-day learners back (P4b) leaves the same cold-start ordering, CBF 0.0683 above the hybrid's 0.0529, with no significance test run (§5.6.2). A real new-learner evaluation is future work item 3.

Sections relied on: ch03 §3.5.2, Table 3.2; ch05 §5.11 limitations 1-2; ch05 §5.6.2; ch06 §6.5 item 3.

### Q6

Concretely, the behaviour is in the blend weight, not in a recommender component. Three of the eight features the logistic regression uses to set alpha per learner are behavioural proxies — visible-resource count, log visible click total and active-day count — and the click-weighted learner profiles of CBF and CF carry click volume too (§4.5.1). There is no sequence or session scorer. The D2 ablation measures that weighting use: removing the three columns costs a median 0.001088 Precision@10 on warm users, −0.65% relative, lower in 15 of 22, p = 0.003279 uncorrected, and nothing detectable on cold start, p = 0.674223 (§5.8.2). That is post-hoc and tests the blend's features, so the hypothesis's behavioural clause is neither supported nor refuted — it stays unchecked. Module D shows the behaviours separate learners, silhouette median 0.3274, but feeds no model. A genuine behavioural component is future work item 1.

Sections relied on: ch04 §4.5.1; ch03 §3.6; ch05 §5.8.2, Tables 5.10-5.11; ch05 §5.1.4; ch06 §6.1 RQ1, §6.3, §6.5 item 1.

### Q7

You shouldn't treat it as evidence of learning, and the thesis doesn't ask you to. A click records that a resource was opened, not that it was read, understood or useful; §5.10 says no causal claim about learning, retention or attainment follows from any number, and §6.4 states "Nothing here is an implication about learning." What the thesis does measure is narrower and checkable: whether a ranker puts a learner's later-opened resources in the top ten, under a leakage-controlled split. That's a precondition, not a benefit — a recommender that cannot even anticipate what learners go on to open is unlikely to help them. The limit is real: exposure is missing-not-at-random and unopened items are counted as negatives (§5.10). Whether showing the list changes engagement or completion needs an online, controlled study, which this design cannot provide and ch06 §6.2 declines to claim.

Sections relied on: ch05 §5.10; ch06 §6.2 (what is not claimed), §6.4; ch03 §3.5.3.

### Q8

Less than the question assumes, but more than I'd like. First, a correction to the framing: chapter 2 does not claim the thesis is more rigorous than the literature; §2.9 states a gap in the sources opened. The claim at issue is one sentence of that gap: repeated evaluation across presentations with a significance test is "absent from the nine reviewed papers as recorded in the notes on them." C2.40 is `partial` because only Zhang et al. and Gao et al. state the absence explicitly; for the other seven I inferred it from the notes' silence without a further full-text check (§2.6). The other parts of the gap — no refitted cold-start slice, OULAD work predicting outcomes rather than ranking — do not rest on that inference. Before submission I would do the full-text check of those seven papers, and either confirm the sentence or narrow it.

Sections relied on: ch02 §2.6, §2.9; claim_ledger.csv C2.40; ch06 §6.2 item 4, §6.6.

### Q9

Restating: is K4 a contribution, or an open question dressed as a finding? It is a contribution of a narrower kind than its wording in Table 1.7 suggests. What is measured: all six phase 1 values reproduced at exactly 0.0 difference on EEE_2014J, ruling out the pilot's arithmetic there; and a controlled contrast, Table 5.14, showing that changing the cold-start construction flips no median sign while changing the split flips both (§5.4.1). That eliminates one explanation with a measurement. C1.23 and C5.37 stay `partial` because the mechanism behind the split effect is not established and the reproduction covers one presentation only. So "a measured test of what decides the inversion" overstates it; I'd accept rewording K4 to "a measured contrast that rules out the cold-start construction as what sets the inversion's direction." That is a finding, with its open question stated beside it.

Sections relied on: ch01 §1.7, Table 1.7; ch05 §5.4.1, Table 5.14; claim_ledger.csv C1.23, C5.37, C5.36; ch06 §6.2 item 2.

### Q10

No evidence-based basis, and I won't predict the answer. The fitted components use seed 42 throughout; the logistic regression and the cold-start cohort draw are seeded from that constant, and only the random baseline was run over five seeds (§4.8, §3.8). What I have shown is determinism under the same seed: the production hybrid's metrics were recomputed in a separate process and matched in all 44 cells (§4.8, §5.8). That is not seed sensitivity. With C1's CF margin at 0.68 percentage points, I can't say whether a different seed would move it across +10%. On D1, the alpha reading — pooled median 0.5150, and the hybrid between its components in 19 of 22 — is a correlate, not a mechanism, which is why C5.78 and C5.79 are `partial`. The test is a re-fit with seeds 43 to 46, reported as exploratory, not as a re-judgement of C1.

Sections relied on: ch04 §4.5.1, §4.8; ch03 §3.8; ch05 §5.2, §5.8, §5.8.1, Table 5.9; claim_ledger.csv C5.78, C5.79.

### Q11

Restating: should C1 read "met", or "met under one defensible protocol and not the other"? The second is the more accurate reading, and I'd accept it. C1 is met as the pre-registration defines it: chapter 3 fixed before the run that C1 to C3 are judged on the primary split, and that a reversal under the global cut-off would be reported beside the verdict as a limitation (§3.5.1). That is what happened: +31.20% against CBF under the primary split becomes −3.77% under the secondary, while the gain over CF stays positive at +18.63% (Table 5.8). Chapter 6 §6.3 says robustness is not established for exactly this reason. The rule is what prevents choosing a split after seeing the answer; it does not make the result robust. The honest summary is: met under the pre-registered split, the CBF half not robust to the alternative.

Sections relied on: ch03 §3.5.1; ch05 §5.2, §5.6.2, Table 5.8; ch05 §5.10; ch06 §6.3, §6.5 item 8.

### Q12

First a precision about RQ3's wording: it asks whether a validation-fitted weight closes the warm-user gap to CF that the pilot's hand-picked weight left open, not whether a learned weight beats every fixed one (§1.6.2). And the fixed-alpha sweep I excluded concerned cold start against CBF (§5.11 limitation 9). But your core point stands: without a fixed-weight arm under the same protocol, RQ3 is answered only in the joint sense — the gap closes under phase 2's design, +10.68% against the pilot's −2.66% — and the weight's own contribution is not isolated, as ch06 says. It is not deferred indefinitely: §6.5 item 4 names it as a legitimate, cheap next experiment with its own pre-registration and held-out data. I didn't run it here because running it after C2 closed would be searching a decided criterion.

Sections relied on: ch01 §1.6.2; ch05 §5.11 limitation 9; ch06 §6.1 RQ3, §6.5 item 4.

## Answers to the follow-ups

### F on Q1

I don't believe chapter 6 uses that phrase — §6.4 calls the split-versus-construction result "a consistent practical finding within these receipted cells," and that finding is about evaluation design, not about CBF's advantage. But your concern does bite on the neighbouring implication in §6.4, that for new learners CBF alone gives a measurable benefit over random: +0.0310 Precision@10, 16 of 22, p_Holm = 0.011014. That is true against random; whether CBF adds anything beyond course position is unknown, because no syllabus-order baseline was run. So that implication should read "CBF is the only compared model clearly above random," not a recommendation to deploy CBF. I'd accept that correction to §6.4 and add a syllabus-order baseline to the future-work list.

Sections relied on: ch06 §6.4; ch05 §5.3.2, Table 5.5; ch06 §6.5.

### F on Q2

Mechanically, the split changes which resources are the targets. Under the per-learner time split the targets are resources first opened after the learner's test cut, so later in the course than the two visible ones; under the random 20% split they are drawn from the whole history, and can precede the visible resources (§5.4.1, §3.5.1). A plausible route is that this changes how well week-position similarity or co-occurrence predicts the targets — but that is my conjecture, and no cell tests it. So you're partly right: "the split" is a location for the effect, not an explanation. It is still progress, because it rules the construction out with a measurement, and ch06 §6.6 states what would overturn even that. The discriminating experiment is a split that varies only the time bound.

Sections relied on: ch05 §5.4.1, Table 5.14; ch03 §3.5.1; claim_ledger.csv C5.137; ch06 §6.6.

### F on Q6

Because the abstract states the question in the hypothesis's own terms, and I agree that it misleads before the qualification arrives. The abstract's last paragraph says the behavioural clause is unchecked "since no dwell time is recorded and no behavioural component was built" — but a reader meets "a hybrid of CBF, CF and a behavioural proxy" first, and Table 5.1 labels the model the same way. The accurate description is a two-component hybrid of CBF and CF whose per-learner blend weight uses three behavioural-proxy features (§3.6, §4.5.1). I'd accept rewording the first sentence of the abstract to that, keeping the hypothesis quoted verbatim in chapter 1 where it belongs.

Sections relied on: front_matter.md §2 (abstract); ch03 §3.6; ch04 §4.5.1; ch05 §5.5, §5.8.2; ch01 §1.6.1.

### F on Q11

On my own chapter 3, the secondary split: §3.5.1 describes the global cut-off as "the closest analogue of deployment," and §5.10 notes it removes the cross-cohort leakage the primary split leaves. Under that split the warm gain over CBF is −3.77%. So the committee should not accept the CBF half of C1 as a deployment claim. The primary split was pre-registered as deciding the criteria because the plan's dataset fields name it and because the global cut-off drops late-joining learners (§3.5.1, §5.10), and ch06 §6.5 item 8 leaves the choice open. Accept C1 as met under the pre-registered rule; read "better than CBF for engaged learners in deployment" as not established.

Sections relied on: ch03 §3.5.1; ch05 §5.6.2, Table 5.8, §5.10; ch06 §6.5 item 8, §6.6.

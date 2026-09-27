# Mock defense 1 — panel and questions (2026-09-27)

Written to `defense/mock_1_panel.md`. This session sets the panel and the questions only; it does
not answer and does not grade (integrity rule 1: nobody grades their own work). A separate
candidate session answers, and a fresh examiner session scores the transcript against these
questions and writes the graded `mock_1.md` record.

    unit: u18_s11_defense_prep        cycle: 1        mock: 1        sub-step: panel
    date: 2026-09-27
    inputs read: thesis/ch01.md-ch06.md, thesis/front_matter.md (draft, 2026-09-25),
      thesis/claim_ledger.csv (580 rows: 567 supported, 13 partial, 0 unsupported),
      blind_review.md (unit u17_s10_blind_review, cycle 1, avg_rating 5.5, decision borderline,
      n_reviews 2), critic.md (unit u16_s9_critic, cycle 3, consensus needs_revision),
      defense/question_bank.md (unit u18_s11_defense_prep, cycle 1, 61 questions, 10 categories)
    answered by: separate candidate session (different model)
    graded by: separate examiner session
    format assumed: 20-minute presentation plus questions (university regulations not supplied)

## Panel

| Persona | Brief | Questions asked |
| --- | --- | --- |
| Methods skeptic | Design: splits, leakage, baselines, what was compared with what; any gap between what the hypothesis claims and what a criterion tests | 1, 2, 3, 4 |
| E-learning and recommender-systems domain expert | Whether the task is the right task: are VLE clicks a learning signal, is Precision@10 meaningful for course material, does personalisation help learning at all; domain transfer and pedagogical meaning | 5, 6, 7, 8 |
| Empirical-rigor examiner | Variance, significance, seeds, reproducibility; whether every run and every fitted component is reported and stress-tested | 9, 10, 11, 12 |

## Presentation outline the candidate is to give (20 minutes)

1. Problem and research question — 2 min
2. Gap from the literature — 2 min
3. Data and protocol — 4 min
4. Models compared — 2 min
5. Warm and cold-start results, 22-presentation check — 6 min
6. What did not work, limitations — 2 min
7. Contributions and future work — 2 min

## Questions

| # | Persona | Category | Question | Source |
| --- | --- | --- | --- | --- |
| 1 | Methods skeptic | Method | You ran no sequential or course-position baseline and no fixed-alpha sweep. On cold start, MostPop and PopWeek both fall below a uniform random ranker, and CBF — the only model clearly above chance — is the one carrying `week_from`/`week_to` features. Before I hear about the hybrid at all: how do you rule out that a plain "next unopened resource in syllabus order" ranker would match or beat everything you've built? | question_bank.md ME2 (blind review weakness 2) |
| 2 | Methods skeptic | Results | Your revised attribution says the direction of the pilot-versus-main inversion tracks the evaluation split, not the cold-start construction — Table 5.14 shows that. But your own claim ledger row C5.137 states plainly that *why* the tertiary split reverses direction is "not established by any receipted cell." You've replaced one unexplained causal claim your critic rejected with a second one you haven't explained either. What's actually different? | thesis/claim_ledger.csv row C5.137; thesis/tables/table_5_14_condition_a_vs_b.md; critic.md (required_next_focus, cycle 3) |
| 3 | Methods skeptic | Question and hypotheses | RQ3 asks whether a validation-fitted weight closes the pilot's warm-user gap to CF. You show it does under phase 2's protocol — but phase 2 also changed the split, the cold-start construction and the exclusion rules in the same move. Chapter 6 admits the improvement "cannot be attributed to the learned weight alone." So what, precisely, does RQ3 answer? | question_bank.md H6 |
| 4 | Methods skeptic | Metrics and statistics | Your Wilcoxon/Holm tests treat 22 module presentations as 22 independent draws, but your own limitations section says they are 7 modules sharing catalogues and syllabi. You publish a per-module table as a mitigation, but you never ran a cluster-robust or mixed-effects test. Given that, what is p_holm = 0.000241 on the cold-start CBF comparison actually telling this committee? | question_bank.md S2 (blind review weakness 4) |
| 5 | Domain expert | Data | Your cold-start slice (`A\|2`) truncates an already-retained, engaged learner's history to the earliest 2 resources by day and refits every quantity around that. Meanwhile you exclude 997 learners with only 1-2 active days — learners who look far more like an actual new registrant. Isn't your cold-start condition measuring thin history among learners you've already selected for engagement, rather than anything close to a genuinely new learner arriving at the platform? | question_bank.md D6; question_bank.md LIM1 |
| 6 | Domain expert | Method | Your title and hypothesis promise a hybrid of content-based filtering, collaborative filtering, and a behavioural session signal. Your own D2 ablation shows that removing the three behavioural-proxy features from the blend-weight classifier costs a median of only -0.65% on warm users and nothing detectable on cold start. Where, concretely, is the behaviour in this recommender? | question_bank.md ME1 (blind review weakness 1) |
| 7 | Domain expert | Motivation | Everything you've measured is whether a ranked list of resources matches what a learner later clicked. Nothing here tells us whether being shown that ranked list would help anyone learn more, engage more, or finish the module. Why should this committee treat "ranks later-clicked resources correctly" as evidence this system does anything an e-learning platform should want? | question_bank.md M3 |
| 8 | Domain expert | Literature | Your own claim ledger, row C2.40, admits that for most of the nine reviewed papers you inferred "no reported variance or significance test" from the notes' *silence*, not from a further full-text check — only for two of the nine sources was the absence stated explicitly. How much of chapter 2's "this thesis is more rigorous than the literature" framing rests on evidence you didn't actually verify? | thesis/claim_ledger.csv row C2.40 |
| 9 | Empirical rigor | Contributions | You list "a measured test of what decides the pilot's cold-start inversion" (K4) as a contribution. But by your own account it rules out one explanation without establishing what the real mechanism is, and your claim ledger keeps rows C1.23 and C5.37 on this contribution at status `partial`, not `supported`. Is an unresolved partial claim really a contribution, or is it a flagged, still-open question dressed as a finding? | question_bank.md C3q; thesis/claim_ledger.csv rows C1.23, C5.37 |
| 10 | Empirical rigor | Limitations | Your D1 diagnostic reports that the fitted blend weight sits near 0.5 on cold start even where CBF is the stronger component in 20 of 22 presentations, and you call this "a correlate, not a confirmed mechanism" — claim ledger rows C5.78 and C5.79 say so explicitly, still at `partial`. Meanwhile the alpha model, its regulariser and the CF neighbourhood size were all fitted with a single seed, no repeated-fit or seed-sensitivity check anywhere. If I asked you to re-fit alpha with a different seed right now, do you have any basis for predicting whether C1 would still pass? | question_bank.md S6; thesis/claim_ledger.csv rows C5.78, C5.79 |
| 11 | Empirical rigor | Results | C1's margin against collaborative filtering is +10.68% against a +10% threshold — a pass by 0.68 percentage points. Under your own secondary, equally defensible global-cut-off split, the warm-vs-CBF result doesn't just shrink, it reverses sign, from +31.20% to -3.77%. A criterion that flips under an alternative reasonable protocol is not a robust criterion. Why should the committee read C1 as "met" rather than "met under one of at least two defensible protocols, and not under the other"? | question_bank.md S3; blind_review.md top_weaknesses (C1 protocol fragility) |
| 12 | Empirical rigor | Future work and ethics | You deliberately did not run a fixed-alpha sweep, calling it future work rather than a test you owed RQ3 now, on the grounds that running it after C2 was decided would be knob-turning on a closed criterion. But RQ3 explicitly asks whether a *learned* weight beats a *fixed* one — without that sweep, under one protocol, how is RQ3 answered at all rather than deferred indefinitely? | question_bank.md F4; question_bank.md LIM6 |

## Follow-ups

| On question | Follow-up asked | Persona |
| --- | --- | --- |
| 1 | You've just conceded no sequential or syllabus-order baseline exists. Then why does chapter 6 still call the cold-start comparison "the most transferable practical finding," when you can't rule out that it's just tracking course position? | Methods skeptic |
| 2 | You say the split decides the direction, not the construction. Then what, mechanically, does the split change that would cause a sign flip — and if you don't know, isn't "the split" just a new name for the same unexplained effect the critic already rejected once? | Methods skeptic |
| 6 | You say the behavioural clause stays "unchecked." Then why does the abstract's first sentence still describe the model under test as a hybrid "of content-based filtering, collaborative filtering, and a behavioural proxy" rather than a two-component hybrid with a behaviour-informed weight? | Domain expert |
| 11 | You say C1 is "met." Then which of your two temporal splits is the one a real deployment would actually use — and if you can't say, on what basis does the committee accept either verdict over the other? | Empirical rigor examiner |

## Do not include

No candidate answers, no bank answers, and no expected verdicts appear in this file. The candidate
reads this file before the mock; answers, section citations and verdicts belong only in the graded
record a separate examiner session writes afterward.

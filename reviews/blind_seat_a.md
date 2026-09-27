- unit: u17_s10_blind_review
- cycle: 1
- seat: A
- persona: methods-focused skeptic
- model_identity: top tier, Claude Opus, claude-opus-5-5
- venue: MSc thesis examination, Web Sciences
- rating: 5
- soundness: 3
- contribution: 2
- presentation: 3
- decision: borderline
- confidence: 4
- top_weaknesses: The behavioural signal named in the title and hypothesis is never a recommender component, only 3 of 8 inputs to the blend-weight classifier (removing them costs -0.65% warm, nothing detectable cold), so the central claim is untested and RQ2 is unanswered (fix: add a behaviour/sequence-based component and ablate it as a component); No sequential or course-position baseline and no fixed-alpha sweep: MostPop and PopWeek fall below random on cold start and CBF wins largely through week features, which points to syllabus order driving the target, so gains cannot be attributed and RQ3 (learned vs fixed weight) is not isolated under one protocol; C1 is protocol-fragile and the blend design is unjustified: the margin over CF clears +10% by 0.68 pp, the global cut-off split reverses the sign vs CBF (+31.20% to -3.77%), and alpha comes from the probability of a binarised "CF-leaning" classifier that D1 shows does not move toward the stronger component on cold start

# Blind Review

## Summary

The submission evaluates a score-level hybrid (min-max-scaled ItemKNN-CF and CBF blended by a
per-learner weight alpha) against CBF, ItemKNN-CF, two popularity baselines and a random ranker on
the 22 OULAD module presentations, with a per-learner day-boundary split, a cold-start condition
built by refitting all learner-dependent quantities without held-out learners (k = 2 visible
items), Precision@10 as the primary metric, six pre-registered criteria and Holm-corrected exact
Wilcoxon tests over presentations. Warm users: the hybrid beats CBF (+31.20%) and CF (+10.68%),
both significant (C1 met). Cold start: the hybrid loses to CBF (-30.28%, 20 of 22 presentations)
and beats CF (+7.32%), but is indistinguishable from random while CF sits below random (C2 and C3
not met). Leakage, budget and reproduction criteria are met. The hypothesis is reported as partially
supported.

## Strengths

- Pre-registered criteria, splits, test families and correction, reported character for character,
  with unmet criteria stated as not met with measured value and gap.
- Genuinely careful cold-start construction (Condition A refits similarity, popularity,
  neighbourhood size and the blend without held-out learners) and an explicit contrast showing that
  the sign of the prior pilot's cold-start result tracks its leaky random split, not the
  construction.
- Counted leakage assertions (0 shared rows, 0 of 2,992 hyperparameter records outside validation,
  test scored at most once per model per cell) and a bit-exact reproduction of one prior
  presentation.
- Every presentation reported, the random floor included, attainable ceilings reported beside
  Precision@10, and the 22-presentations-of-7-modules dependence acknowledged.
- Limitations are specific and quantified (filtered-out learners, simulated cold start, no dwell
  time, unreceipted pre-run checks).

## Weaknesses

1. **The behavioural component of the hypothesis is not in the method.** The title and hypothesis
   promise a hybrid of CBF, CF and a behavioural session signal. In the method, the behavioural proxy
   is three of eight features of a logistic regression that sets the blend weight; there is no
   behavioural or sequence scorer. The post-hoc ablation D2 shows removing those columns costs a
   median -0.65% on warm users and nothing detectable on cold start. RQ1 is descriptive and its
   output feeds no model; RQ2 is declared unanswerable by the design. So the thesis's distinctive
   claim is untested, and what remains is a two-component linear blend of cosine CF and cosine CBF,
   a well-known construction. Fix: add an explicit behaviour/sequence component (e.g. a first-order
   item-transition or engagement-weighted scorer) as a third blend term and ablate it as a
   component, or narrow the title and hypothesis to what was built.
2. **Baselines do not rule out the most obvious explanation.** On cold start MostPop (0.0266) and
   PopWeek (0.0317) sit below a uniform random ranker (0.0484), and CF sits below random too. That
   is a signature of a target dominated by course position: the test set is each learner's latest
   20% of first-opened resources, and CBF, the only model above chance, is the one carrying
   `week_from`/`week_to` features. Without a sequential baseline (item-to-item Markov transitions,
   or a GRU4Rec/SASRec-class model) or a simple "next unopened resources in syllabus order"
   baseline, neither the warm gains nor the cold-start ordering can be attributed to the hybrid's
   design. Relatedly, no fixed-alpha sweep was run (limitation 9), so RQ3 (does a learned weight
   close the gap a hand-picked weight left open) compares against a pilot run under a different,
   leaky protocol and is not actually answered under a single protocol.
3. **C1 is fragile to protocol and the blend design is not justified.** The warm margin over CF
   clears the +10% threshold by 0.68 pp, and the secondary (global cut-off) split reverses the
   warm gain over CBF from +31.20% to -3.77%; the claim therefore holds for one of two
   defensible temporal splits. The alpha procedure (sweep an 11-point grid per validation learner,
   binarise the best value into "CF-leaning", fit a classifier, use its probability as the weight)
   discards the magnitude information it computes and is not compared to directly selecting alpha on
   validation. D1 shows the fitted weight stays near 0.5 (pooled median 0.515) on cold start even
   though CBF is the stronger component in 20 of 22 presentations, which is a plausible direct cause
   of the C2/C3 failure and is left undiagnosed as a design choice.
4. **Statistical unit.** Wilcoxon over 22 presentation means treats them as exchangeable pairs, while
   they are 7 modules with shared catalogues; a module-level test (n = 7) or a mixed model would be
   the honest primary unit. Acknowledged, but not acted on.
5. **Minor inconsistencies.** Hybrid-vs-CBF cold-start p_Holm is 0.000241 in the F2 paragraph and
   0.000121 in the C3 section; floating-point "ties" are kept as nonzero differences while one exact
   tie is dropped, which is inconsistent zero handling. The document is long and dense for its
   findings; an examiner has to reconstruct the main message from 20 tables.

## Questions

1. How are the blend-weight features and labels built for the cold-start condition at k = 2: are the
   validation learners' features computed on truncated histories, so that the classifier sees the
   regime it is applied to?
2. Why binarise the per-learner best alpha rather than regress it or choose a global alpha on
   validation? What does a fixed alpha, chosen on validation, score on both slices?
3. What does a pure syllabus-order baseline (rank unopened resources by `week_from`, then by id)
   score on the warm and cold slices? If it matches or beats CBF, what is left of the hybrid's
   contribution?
4. Why does the global cut-off split reverse the warm result against CBF, and which split better
   matches a deployed recommender?
5. Why is MostPop below random on cold start; does popularity counted over training learners
   concentrate on early-course resources that are rarely in anyone's test window?

## Rationale

The empirical protocol is careful and unusually honest: pre-registration, leakage counting, a
refit cold-start construction, full per-presentation reporting and a random floor. Those earn the
soundness score. But a methods examiner judges whether the method answers the question posed, and
here it largely does not: the behavioural signal is not a recommender component, the segmentation
research question is unanswerable by design, the learned-weight question has no same-protocol
control, and the baselines omit the sequential/course-order models that the data's structure (popularity
below random, CBF winning via week features) points to. The one positive primary result clears its
threshold by 0.68 pp and reverses under an alternative temporal split. Against a harsh calibration
where the median submission is rejected, this sits just below the line: a defensible, well-audited
negative-leaning evaluation of a standard two-component hybrid, not a demonstration of the
behaviour-based hybrid the title claims. Rating 5, borderline.

- unit: u17_s10_blind_review
- cycle: 1
- avg_rating: 5.5
- n_reviews: 2
- decision: borderline
- top_weaknesses: The behavioural signal named in the title and hypothesis is never a recommender component, only 3 of 8 inputs to the blend-weight classifier (removing them costs -0.65% warm, nothing detectable cold), so the central claim is untested and RQ2 is unanswered (fix: add a behaviour/sequence-based component and ablate it as a component); No sequential or course-position baseline and no fixed-alpha sweep: MostPop and PopWeek fall below random on cold start and CBF wins largely through week features, which points to syllabus order driving the target, so gains cannot be attributed and RQ3 (learned vs fixed weight) is not isolated under one protocol; C1 is protocol-fragile and the blend design is unjustified: the margin over CF clears +10% by 0.68 pp, the global cut-off split reverses the sign vs CBF (+31.20% to -3.77%), and alpha comes from the probability of a binarised "CF-leaning" classifier that D1 shows does not move toward the stronger component on cold start; Significance tests treat 22 module presentations as independent draws for Wilcoxon/Holm correction, but they are 22 presentations of only 7 modules sharing catalogues and syllabi, and no cluster-robust or module-level test addresses this pseudo-replication
- self_claimed_rating: none
- calibration_gap: none

# Blind Review Panel (memoryless)

## Role Status
- blind_seat_a: status=ok model=top tier identity=Claude Opus, claude-opus-5-5
- blind_seat_b: status=ok model=mid tier identity=claude-sonnet-5

## Reviewer A

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

## Reviewer B

    - unit: u17_s10_blind_review
    - cycle: 1
    - seat: B
    - persona: empirical-rigor skeptic
    - model_identity: mid tier, claude-sonnet-5
    - venue: MSc thesis examination, Web Sciences
    - rating: 6
    - soundness: 3
    - contribution: 3
    - presentation: 4
    - decision: borderline
    - confidence: 4
    - top_weaknesses: Significance tests treat 22 module presentations as independent draws for Wilcoxon/Holm correction, but they are 22 presentations of only 7 modules sharing catalogues and syllabi, and no cluster-robust or module-level test addresses this pseudo-replication; The blend weight (alpha), its regulariser and the collaborative neighbourhood size are all selected with a single seed (42) and no seed-sensitivity analysis, leaving the razor-thin C1 margin against ItemKNN-CF (+10.68% vs. a +10% threshold, a 0.68-point margin) unstress-tested; The C2-deciding win against ItemKNN-CF on cold start is a win over a baseline that itself sits below the random-ranker floor on that slice, and the criterion verdict table does not surface that this half of C2 is a comparison against a non-informative baseline

# Blind Review

## Summary

The submission evaluates a score-level hybrid (content-based + item-based collaborative filtering,
with a validation-fitted blend weight informed by behavioural-proxy features) against single-technique
baselines on OULAD, across 22 module presentations, under a pre-registered set of six criteria (C1-C6)
with paired exact Wilcoxon tests and Holm correction. The hybrid clears its warm-user threshold (C1,
met) but fails both cold-start criteria (C2, C3, not met) against content-based filtering specifically,
while beating collaborative filtering on cold start. Anti-cheating and feasibility criteria (C4, C5,
C6) are met. The reporting is unusually complete for negative and exploratory results, including a
random-floor comparison that shows the hybrid is statistically indistinguishable from chance on cold
start. My evaluation as the empirical-rigor seat focuses on whether the significance machinery and the
splits actually support the certainty implied by the p-values, independent of whether the outcome is
positive or negative.

## Strengths

- Splits are verified byte-identical across all six models via serialised-set hash comparison before
  scoring, and the leakage audit (C4) reports nine counted assertions including cross-split row
  disjointness and hyperparameter provenance, with a measured value even when zero.
- Statistical families (F1-F4) and the primary Precision@10 metric were declared before any run, and
  the deciding test (paired exact Wilcoxon over presentation-level values, Holm-corrected within
  family) is applied consistently rather than picked post hoc; a distribution-free sign-test companion
  is reported alongside, and it disagrees with Wilcoxon on the warm CBF comparison (p=0.052 vs.
  p=0.006) — a disagreement the authors surface rather than suppress.
- The random-floor exploratory analysis is the strongest rigor move in the submission: it independently
  checks whether each model clears chance on the cold-start slice, and reveals that ItemKNN-CF (the
  baseline C2's headline win is measured against) does not clear chance itself. Most submissions would
  have stopped at "the hybrid beats ItemKNN-CF, p<0.001" and left it there.
- Zero-difference pairs are explicitly dropped from the Wilcoxon calculation with the resulting
  effective n reported next to every p-value, and the submission states the point below which the exact
  test structurally cannot reach significance (effective n < 6), which was never reached here.
- Split sensitivity is checked directly: a secondary (global cut-off) split and a tertiary
  (temporally leaky, matching a prior pilot) split are both run through the same models, and the
  submission states plainly that the secondary split reverses the sign of the warm-vs-CBF result.

## Weaknesses

1. **Pseudo-replication in the significance tests.** The Wilcoxon/Holm procedure treats the 22
   presentation-level Precision@10 values as 22 exchangeable paired observations, but the submission's
   own limitations section states they are 7 modules with 2-4 presentations each, sharing catalogues
   and syllabi. Presentations of the same module are not independent draws, so the effective statistical
   power behind p_holm=0.000241 (C2's headline cold-start numbers) is almost certainly smaller than
   n=21-22 implies. No cluster-robust variant, module-level bootstrap, or mixed-effects specification
   is used to check whether the significance claims survive when non-independence is modelled rather
   than merely disclosed in prose.
2. **No variance/seed analysis for the hybrid's own fitted components.** Random is run over 5 seeds
   with mean and SD reported, but the parts of the pipeline that decide the criteria — the alpha
   logistic regression, its regulariser (chosen by 5-fold CV), and the ItemKNN-CF neighbourhood size —
   are all fit with seed 42 only. C1's ItemKNN-CF margin (+10.68% against a +10% threshold) is a 0.68
   percentage-point margin on a median with an IQR of 20.82pp; without a seed-sensitivity or repeated-fit
   analysis of the alpha model, a reader cannot tell whether this pass is stable or an artifact of one
   fit.
3. **A criterion-deciding "win" against a baseline that is itself below chance.** The random-floor table
   shows the hybrid statistically indistinguishable from random on cold start (p=0.750) while ItemKNN-CF
   sits further below random. C2's ItemKNN-CF conjunct nonetheless registers as a Holm-significant win
   for the hybrid. The main criterion table (Every success criterion, judged as written) reports this as
   part of a "not met" verdict (correctly, since the CBF conjunct fails), but does not itself flag that
   the surviving half of the comparison is a win over a baseline that fails a basic sanity check; a
   reader relying on that table alone would not know this without cross-referencing a different section.
4. **No confidence interval reported at the point of criterion determination.** The submission states a
   bootstrap 95% percentile interval "accompanies every reported number," but the criterion table (C1's
   +10.68% margin in particular) reports point estimates and p-values only, not the interval, at exactly
   the place where a thin margin most needs one.
5. **Three presentations with 100% missing week metadata are pooled without a stratified check.**
   BBB_2013B, DDD_2013B and DDD_2013J have entirely imputed `week_from`/`week_to` values (flagged as a
   historical source of bit-identical hybrid/CBF scores in the unreceipted pilot). The current submission
   states the missing-value fallback prevents that degeneracy but does not report the median comparisons
   with and without these three presentations, so a reader cannot verify the imputation's effect on the
   headline medians.

## Questions

- Under a cluster-robust test (e.g., resampling at the module level, or a mixed-effects model with
  module as a random effect) rather than treating all 22 presentations as independent, do C1 and C2 still
  reach p<0.05 after Holm correction?
- What is the bootstrap 95% interval for the hybrid-vs-ItemKNN-CF median relative gain on the warm slice
  (the one that decides C1 by a 0.68-point margin), and does it include +10%?
- If the alpha logistic regression, its regulariser, and the ItemKNN-CF neighbourhood size are refit with
  a different seed (or repeated k times with different train/validation shuffles within the same split),
  does the direction and Holm-significance of C1's ItemKNN-CF margin and C2's ItemKNN-CF margin remain
  stable?
- Excluding the three presentations with 100% missing week metadata, do the warm and cold-start medians
  against CBF and ItemKNN-CF change materially?

## Rationale

The design is genuinely strong on the axes usually missing from work like this: pre-registration, split
verification, leakage accounting, honest negative results, and — unusually — an exploratory check that
undercuts one of its own significant findings (the random-floor comparison). That transparency is why I
do not rate this lower. But as the empirical-rigor seat I am asked to calibrate harshly and to weigh
missing significance/variance controls heavily, and two structural issues remain unaddressed rather than
merely disclosed: the 22 "presentations" are pseudo-replicated draws from 7 modules, which the Wilcoxon/
Holm machinery does not account for despite the authors knowing it; and the pipeline's own fitted
components (alpha, its regulariser, neighbourhood size) carry no seed-sensitivity check even though C1's
surviving margin against ItemKNN-CF is a 0.68-percentage-point pass. Combined with a criterion-deciding
win over a below-chance baseline that is not flagged where the verdict is read, these are fixable
methodological gaps rather than fatal flaws — hence borderline rather than reject, and not higher than
6/10 given how much of the reported significance rests on an independence assumption the authors' own
limitations section contradicts.

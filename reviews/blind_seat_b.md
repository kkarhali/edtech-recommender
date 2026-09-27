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

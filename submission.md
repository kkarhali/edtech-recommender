# A Recommendation System for E-Learning Based on User Behaviour Analysis

### An evidence-bound evaluation on the Open University Learning Analytics Dataset

## Abstract

Hybrid recommenders are expected to help learners with the least history most, yet are rarely
tested on public learner-behaviour data with an explicit new-learner condition. This work asks
whether a hybrid of content-based filtering (CBF), item-based collaborative filtering (CF, here
ItemKNN-CF) and a behavioural engagement proxy outranks either technique alone, for learners with
history (warm users) and for learners with almost none (cold-start users).

The data are the Open University Learning Analytics Dataset (OULAD): 32,593 learner rows
(`studentInfo.csv`), 22 module presentations of 7 modules, and a virtual-learning-environment
click log. After two pre-registered learner filters (at least 5 distinct resources; at least 3
distinct first-interaction days), 27,212 of 29,228 logged learners are evaluated on the warm
slice. The cold-start-refit slice holds 5,444 learners (69 to 426 per presentation), built by
truncating a held-out learner's visible history to the earliest k = 2 resources by day and
refitting every learner-dependent fitted quantity — the similarity model, the popularity counts,
the neighbourhood-size and blend-weight selection, and the blend model itself — without that
learner's rows.

The method is pre-registered: identical time-based splits for all six compared models, Precision@10
(K = 10) as the primary metric, six binary success criteria fixed before any run, and paired exact
Wilcoxon signed-rank tests with Holm correction over the 22 module presentations.

**Warm slice (criterion C1, met).** The hybrid's median Precision@10 (0.1720) exceeds CBF's
(0.1562) by +31.20% relative and ItemKNN-CF's (0.1707) by +10.68% relative, both against a
pre-registered threshold of +10% and both Holm-corrected significant (p_holm = 0.011857 and
0.014095, effective n = 22). The margin against ItemKNN-CF clears its threshold by 0.68 percentage
points.

**Cold-start-refit slice (criteria C2 and C3, not met).** Against CBF the hybrid loses a median
30.28% relative (p_holm = 0.000241); against ItemKNN-CF it gains a median 7.32% relative
(p_holm = 0.000241, effective n = 21). Criterion C2 requires a positive median gain against both
baselines and is not met on the CBF comparison. Criterion C3 requires the hybrid's Precision@10 to
be at least CBF's in every one of the 22 presentations; this conjunct holds in 2 of 22
(CCC_2014J, DDD_2013B), so C3 is not met, although the hybrid beats a global-popularity baseline in
22 of 22 presentations, produces zero empty top-10 lists, and covers at least 10% of the catalogue
in every presentation. An exploratory comparison against a random ranker (five seeds, deciding no
criterion) shows that on this slice only CBF is clearly above chance (+71.2% relative to random,
16 of 22 wins, p_Holm = 0.011014); the hybrid is indistinguishable from the random floor (−7.0%
relative, 10 of 22 wins, p = 0.750238), and ItemKNN-CF sits below it. The cold-start gain the
hybrid does record is therefore a gain over a baseline that does not itself clear chance.

**Anti-cheating and feasibility criteria (C4, C5, C6; all met).** Zero rows are shared between any
two of the training, validation and test splits; zero of 2,992 hyperparameter records were fitted
on data outside the validation split; the test split is scored at most once per model per
presentation (maximum count 1 over 7,920 scoring cells). The main run over all 22 presentations
cost 1.0140 of a 4.0 CPU-hour budget; a reproduction of one prior, unreceipted pilot presentation
(EEE_2014J) cost 0.238 of a 15-minute budget and reproduced all six of that pilot's recorded
Precision@10 values to an absolute difference of exactly 0.0 (tolerance 1e-6).

**Relation to prior, unreceipted evidence.** An earlier, unreceipted pilot run on the same 22
presentations reported the opposite cold-start pattern: the hybrid ahead of CBF in 22 of 22
presentations (median +73.12% relative, range +13.55% to +163.85%) and behind ItemKNN-CF in 22 of
22 (median −17.90%, range −29.12% to −10.03%). A direct contrast that holds the evaluation split
fixed while varying the cold-start construction, and holds the construction fixed while varying
the split, shows that the sign of the median comparison against either baseline tracks which split
is used, not which cold-start construction is used: under the pilot's own (temporally leaky) split,
the corrected refit construction still shows the hybrid ahead of CBF (median +105.56%) and behind
ItemKNN-CF (median −3.99%) on cold start, matching the pilot's direction; under the time-based
split used to decide C1–C3, both the refit construction and the pilot's shared-similarity
construction show the hybrid behind CBF and ahead of ItemKNN-CF. The refit construction changes the
median gain against ItemKNN-CF from +7.32% (refit) to +13.34% (shared-similarity) on the primary
split — a difference between medians only; the paired per-presentation shift has a median of about
+0.01 percentage points (11 up, 11 down) and reaches about −53 percentage points in one presentation
(AAA_2014J).

**Conclusion.** The hypothesis is partially supported. On warm users the hybrid beats both
single-technique baselines (+31.20% vs. CBF, +10.68% vs. CF, both Holm-corrected p < 0.02). On
cold-start (new) learners the
cold-start claim is refuted against content-based filtering and holds only against a collaborative
baseline that does not itself clear a random floor. The hypothesis's behavioural-signal clause
(browsing sequence, dwell time, engagement pattern) is not tested by any criterion: the dataset
records no dwell time, and the behavioural proxy used (click volume, active-day count, click
sequence) enters the blend weight's own feature set rather than functioning as a separate,
independently tested recommender component. Results describe UK Open University distance learners
in 2013–2014 who used at least 5 resources on at least 3 distinct days; they do not describe
disengaged learners, actual (rather than simulated) new registrations, or other institutions.

## Research Questions

The hypothesis, the five research questions and the six success criteria below are reproduced as
they were fixed before any run.

**Hypothesis.** A hybrid recommender that combines (a) content-based filtering over
course/content metadata, (b) collaborative filtering over learner–content interaction history, and
(c) a behavioural session signal (browsing sequence, dwell time, engagement pattern) will produce
more accurate and more robust recommendations for e-learning content than either content-based or
collaborative filtering alone, and will specifically outperform them on cold-start learners (users
with very little interaction history). It is refutable in exactly the terms of C1 and C2: if the
hybrid does not beat both baselines by at least 10% relative on warm users, or does not beat both
on new learners, it is not supported.

**Scope reduction.** The hypothesis names dwell time. OULAD records only a day offset (`date`) and
a click count (`sum_click`) per learner, resource and day, and holds no duration or session-length
field. The behavioural signal is therefore operationalised as a proxy: click volume per
learner-item, count of distinct active days, and day-ordered click sequence. This proxy is
narrower than "dwell time" — a click count cannot distinguish a resource opened by accident from
one studied for an hour — and the phrase "dwell time" is never used below for anything measured.

- **RQ0 (main):** Does a hybrid of content-based filtering, collaborative filtering and a
  behavioural engagement signal produce more accurate and more robust top-K e-learning
  recommendations than either alone, and on cold-start learners? Decided by C1–C3.
- **RQ1 (behaviour analysis):** Which observable VLE behaviours (click volume, active-day count,
  day-ordered sequence, activity type) separate learners well enough to carry recommendation
  signal? Answered descriptively only; see Results.
- **RQ2 (data-analysis models):** Does segmenting learners by behavioural profile (clustering over
  behavioural features) improve the cold-start prior over a non-segmented hybrid? **Not answerable
  from this design**: no segmented model is compared, and no cold-start prior is fitted from
  behavioural segments; the descriptive clustering feeds no scored model.
- **RQ3 (recommendation model):** Does a blend weight learned on a validation split close the
  warm-user gap to pure collaborative filtering that a hand-picked weight left open? Decided by C1.
- **RQ4 (evaluation and improvement):** Under a time-based split and a new-learner condition, does
  the hybrid's advantage survive significance testing across the 22 module presentations? Decided
  by C1–C3 with their significance conjuncts.

**Success criteria** (character for character as pre-registered; no threshold was changed after any
run):

| # | Kind | Metric | Threshold | Dataset |
| --- | --- | --- | --- | --- |
| C1 | primary | Precision@10 relative gain, hybrid vs. CBF AND vs. CF, warm-user held-out slice | `>= +0.10` relative against BOTH baselines, median over 22 presentations, AND paired Wilcoxon p < 0.05 (Holm-corrected) for both | OULAD, all 22 presentations, time-based split, identical splits for all four models |
| C2 | primary | Precision@10 relative gain, hybrid vs. CF AND vs. CBF, cold-start slice built by refitting the similarity model without held-out learners | `> 0` relative against BOTH baselines, median over 22 presentations, AND paired Wilcoxon p < 0.05 (Holm-corrected) for both | OULAD, all 22 presentations, cold-start-refit condition, identical splits |
| C3 | primary | Cold-start Precision@10, hybrid vs. CBF and vs. a global-popularity baseline; non-degeneracy of top-10 lists | `>= CBF` AND `> popularity baseline` AND `== 0` empty top-10 lists AND `>= 10%` of catalogue items appearing across top-10 lists, in **each** of 22 presentations | OULAD, all 22 presentations, cold-start-refit condition |
| C4 | anti-cheating | Tuning-on-test leakage count: rows shared between validation and test splits; hyperparameters fitted on non-validation data | `== 0` shared rows AND `== 0` hyperparameters fitted outside validation; test split scored exactly once per model per presentation | OULAD, all 22 presentations |
| C5 | feasibility | Wall-clock time and hardware, main run and phase-1 reproduction | `<= 4.0` CPU-hours (main run) AND `<= 15` minutes (reproduction), single CPU, no GPU, no downloaded weights | OULAD, all 22 presentations |
| C6 | anti-cheating | Absolute difference, reproduced vs. recorded phase-1 Precision@10, all 3 models, warm and cold-start, EEE_2014J | `<= 1e-6` absolute for all 6 values, with SHA256 receipt and exact command line | OULAD, EEE_2014J, seed 42, deterministic selection |

C3 operationalises a conditional clause of the frozen hypothesis (non-degenerate top-K lists that do
not simply fall back to global popularity without at least matching CBF's cold-start Precision@10)
into four evaluable conjuncts; no numeric threshold was moved in doing so. C3 is judged in **each**
of the 22 presentations, while C1 and C2 are judged on the **median** over the 22 with a
significance test.

## Method

**Task.** For each evaluated learner, every catalogue resource not already in that learner's visible
history is ranked; the measure is how many of the learner's held-out later resources appear in the
top 10. The full catalogue is ranked (106 to 529 resources depending on the presentation) with no
negative sampling. Resources already opened as of the moment of recommendation are excluded from
the candidate list — only those resources, nothing from the learner's future — separately for three
moments: warm validation (training resources excluded), warm test (training and validation
resources excluded), and cold start (only the k visible resources excluded). Candidates are ordered
by score descending, then resource id ascending (a fixed, model-independent tie rule).

**Data preparation.** The unit of analysis is a (learner, resource) pair, keyed by the day of first
interaction. A pair's click weight is the sum of `sum_click` over its rows **within a stated day
bound**: for training use, the bound is the learner's first validation day; for a cold-start
learner's visible history, the bound is the day of the k-th visible interaction. Active-day counts
count distinct days within the same bound. Missing `week_from`/`week_to` values are imputed with
the known median for that presentation, or 0.0 with a binary missing-indicator when a presentation
has no known value at all (three presentations — BBB_2013B, DDD_2013B, DDD_2013J — have 100%
missing `week_from`/`week_to`); every assembled feature matrix is asserted to contain no undefined
value.

**Learner filters (pre-registered).** Learners are kept if they interacted with at least 5 distinct
resources (removes 1,019 of 29,228 across the 22 presentations) and have at least 3 distinct
first-interaction days (removes a further 997, 3.53%, leaving 27,212 evaluated learners). The
second filter is what the day-boundary split (below) requires to produce a non-empty training,
validation and test set for every learner.

**Split rule.** The primary split is a per-learner day-boundary split, applied independently within
each presentation: (learner, resource) pairs are grouped by day of first interaction; a test cut is
chosen at the day boundary whose test set is closest to 20% of that learner's pairs, and a
validation cut at the boundary closest to 10%, with everything earlier as training. The test cut
may fall no earlier than the learner's third distinct day. By construction, for every learner the
latest training or validation day is strictly earlier than the earliest test day. No random seed is
needed. Realised test fractions run 0.199–0.205 and validation fractions 0.102–0.120 across the 22
presentations. All six compared models receive byte-identical training/validation/test sets per
presentation, verified by comparing serialised-set hashes across models before scoring.

Two further splits are reported for context and decide no criterion: a **secondary (global
cut-off)** split at the day below which 80% of the presentation's rows fall, and a **tertiary
(random 20%)** split that reproduces the design of an earlier, unreceipted pilot and is labelled
temporally leaky wherever it appears.

**Cold-start constructions.** **Condition A (primary; decides C2 and C3).** Within each
presentation, 20% of evaluated learners are set aside as cold-start learners by a seeded draw
stratified by training-activity quintile (cohort sizes 69 to 426). Every learner-dependent fitted
quantity — the item–item similarity model, global and week-aware popularity counts, the
collaborative neighbourhood size, the blend model's regulariser, and the blend model itself — is
refit using only the remaining 80% of learners; the held-out learners' rows are removed from each of
these, not merely hidden at scoring time. Each cold-start learner is shown the earliest k resources
by day (k = 0, 1, 2, 5; k = 2 decides C2 and C3) and scored on the same held-out test set used for
the warm slice. **Condition B (secondary; labelled optimistic, decides nothing).** The same
learners and test sets, but the similarity model is fitted on **every** evaluated learner's full
training history, with visible history truncated only at scoring time; this construction passes
every leakage check but cannot support a claim about new learners, because the learners it calls new
shaped the model that ranks for them.

**Models compared.** Six models, on identical splits:

| Model | Specification | Tuned on validation |
| --- | --- | --- |
| Random | uniform draw over candidate set, 5 seeds (42–46), mean and SD reported | nothing |
| MostPop (global popularity) | ranked by number of distinct **training learners** who used the resource | nothing |
| PopWeek (week-aware popularity, reporting only) | popularity restricted to resources whose week window contains the learner's current course week | nothing |
| CBF (content-based) | cosine similarity between a click-weighted learner profile and item vectors (one-hot `activity_type`, normalised `week_from`/`week_to`, missing-week indicator) | nothing |
| ItemKNN-CF (collaborative) | cosine similarity between resource columns of the learner–resource click matrix, truncated neighbourhood | neighbourhood size (5 candidate values) |
| Hybrid | score-level blend of min–max-scaled CF and CBF scores: `score = alpha × CF + (1 − alpha) × CBF` | blend weight (alpha) and its regulariser |

MostPop and CBF/CF/Hybrid are the models named in the pre-registered plan; Random and PopWeek are
additions for reporting and decide no criterion. C3's "global-popularity baseline" refers to MostPop
only.

**The hybrid's blend weight.** Alpha is a single scalar per learner, produced by a logistic
regression fitted on the **validation split only**: for each validation learner, an eleven-point
grid of candidate alpha values is swept against that learner's own validation resources, the best
value is binarised into a label ("collaborative-leaning" vs. not), and a logistic regression over
eight learner-level features (visible-resource count, log visible click total, active-day count,
each component's top-1 and top-10 score mass, and the share of resources with missing week data) is
fitted to that label with validation-only z-scoring. Alpha is the model's predicted probability
(in [0,1] by construction). Its regulariser is chosen by stratified five-fold cross-validation
within the validation learners (values 0.01, 0.1, 1, 10). The neighbourhood size, regulariser and
blend weight are refit separately per presentation, per cold-start condition, and per k. A prior,
unreceipted pilot run used a hand-picked weight, `alpha = min(0.9, 0.2 + 0.05 × visible items)`,
chosen after that pilot's own test-set results had been seen; that weight is not used in, and is
not evidence for, the criteria reported here — it is reported only as prior context in Results.

**Metrics.** Precision@10 is the primary metric and decides C1–C3: for a learner, the number of
held-out resources in the top 10 divided by 10, averaged over learners then reported as a
per-presentation macro mean. A learner with fewer than 10 held-out resources cannot reach a
Precision@10 of 1; the attainable ceiling is reported alongside every Precision@10 table.
Recall@K, NDCG@K, HitRate@K and MRR@K (K = 5, 10, 20), catalogue coverage, intra-list diversity,
an empty-list count, and a popularity-agreement diagnostic are also computed for every model and
slice; none of these decides a criterion.

**Significance plan (fixed before any run).** Families of comparisons are declared in advance and
Holm correction is applied within each family only: F1 is the two warm comparisons deciding C1; F2
the two cold-start comparisons deciding C2; F3 within-presentation per-learner comparisons (context
only); F4 everything else (other splits, other K, the k curve, Condition B), exploratory and
deciding no criterion. The deciding test for C1 and C2 is a two-sided, exact, paired Wilcoxon
signed-rank test over the 22 presentation-level Precision@10 values (not the relative gains),
Holm-corrected within its family; an exact binomial sign test accompanies it as a distribution-free
companion, not as the pre-registered test. Zero paired differences are discarded by both tests, and
the effective number of pairs after discarding is reported beside every p-value. Below an effective
6 pairs the exact two-sided test cannot reach p < 0.05 at any effect size, in which case the test
conjunct is recorded as **unchecked**, never as failed. A bootstrap 95% percentile interval
(10,000 resamples over learners) accompanies every reported number.

**Post-hoc additions (outside the pre-registered plan; family F4; decide no criterion).** Two
diagnostics were run, on the approved code path, after the criteria above were closed, and score the
test split a second time: **D1** logs the blend weight the production hybrid used for every learner
on the cold-start-refit cell (k = 2). **D2** refits the blend without the three columns that carry
the behavioural proxy (visible-resource count, log visible clicks, active-day count) and scores the
resulting `Hybrid_ablated` on the warm cell and the k = 2 cold-start cell alongside the production
hybrid. D2 removes columns from the blend's own feature set; it does not remove a behavioural
recommender component (none exists in this design), so it does not test the hypothesis's
behavioural-signal clause on its own terms. A third addition compares every model against the
random ranker on already-scored results, reports uncorrected p-values, and makes no new run.

## Experimental Setup

**Dataset.** Open University Learning Analytics Dataset (OULAD), licensed CC BY 4.0 by its authors.
32,593 learner rows (`studentInfo.csv`), 22 module presentations of 7 modules (named AAA, BBB, CCC,
DDD, EEE, FFF, GGG; presentations beginning February "B" or October "J" of 2013/2014). The
population is UK Open University distance learners; it is not the evaluating institution's own
population. `studentInfo.csv` demographic columns are never used as model features, filters or
strata.

*Population per module presentation (interactions and learners from `studentVle.csv`,
`studentRegistration.csv`; all counted from the tables named).*

| Presentation | Interactions | Resources | Registered | In the log | Evaluated |
| --- | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 180,982 | 211 | 383 | 378 | 375 |
| AAA_2014J | 169,316 | 202 | 365 | 357 | 347 |
| BBB_2013B | 403,266 | 315 | 1,767 | 1,537 | 1,404 |
| BBB_2013J | 452,638 | 321 | 2,237 | 1,870 | 1,700 |
| BBB_2014B | 273,236 | 311 | 1,613 | 1,294 | 1,163 |
| BBB_2014J | 438,424 | 207 | 2,292 | 1,921 | 1,773 |
| CCC_2014B | 496,181 | 196 | 1,936 | 1,681 | 1,557 |
| CCC_2014J | 711,646 | 223 | 2,498 | 2,302 | 2,131 |
| DDD_2013B | 536,837 | 428 | 1,303 | 1,214 | 1,150 |
| DDD_2013J | 680,806 | 462 | 1,938 | 1,768 | 1,656 |
| DDD_2014B | 379,942 | 453 | 1,228 | 1,116 | 1,040 |
| DDD_2014J | 568,901 | 365 | 1,803 | 1,647 | 1,523 |
| EEE_2013J | 356,262 | 112 | 1,052 | 964 | 898 |
| EEE_2014B | 202,224 | 109 | 694 | 624 | 584 |
| EEE_2014J | 402,947 | 115 | 1,188 | 1,097 | 1,018 |
| FFF_2013B | 946,765 | 508 | 1,614 | 1,510 | 1,460 |
| FFF_2013J | 1,172,101 | 529 | 2,283 | 2,098 | 1,989 |
| FFF_2014B | 685,274 | 478 | 1,500 | 1,363 | 1,281 |
| FFF_2014J | 1,210,359 | 452 | 2,365 | 2,121 | 1,988 |
| GGG_2013J | 145,995 | 137 | 952 | 895 | 835 |
| GGG_2014B | 123,319 | 124 | 833 | 773 | 705 |
| GGG_2014J | 117,859 | 106 | 749 | 698 | 635 |

Across the 22 presentations, 29,228 learners appear in the interaction logs and 27,212 are evaluated
on the warm slice (2,016 removed by the two learner filters). The cold-start-refit slice holds 5,444
learners in total (69 to 426 per presentation).

**Baselines and models.** Random (5 seeds, 42–46), MostPop, PopWeek, CBF, ItemKNN-CF, Hybrid — see
Method.

**Metric.** Precision@10, K = 10, per-learner then averaged per presentation (macro mean); decides
C1–C3.

**Seeds.** 42 for every stochastic step that needs one (cold-start cohort draw, blend-weight
logistic regression, K-Means segmentation used only for the descriptive behaviour analysis,
bootstrap resampling); the day-boundary split needs no seed; the Random baseline uses seeds 42–46,
and its reported mean and standard deviation are computed over all five seeds, never the best.

**Hardware and software.** Single CPU, no GPU, no downloaded model weights, no network access at
run time (Windows 10 build 19045, Intel64 12 logical cores). Python 3.12.3, NumPy 2.5.3, pandas
3.0.5, scikit-learn 1.9.1, SciPy 1.18.1.

**Wall-clock and compute (criterion C5).** The main run over all 22 presentations, three splits, six
models, two cold-start conditions and four values of k cost 1.0140 CPU-hours (process CPU 2,798.41 s
+ child-worker wall time 852.02 s; wall-clock 3,769.12 s ≈ 62.8 minutes) against a 4.0 CPU-hour
budget. A reproduction of one prior, unreceipted presentation (EEE_2014J, seed 42) cost 0.238
minutes (14.27 s) against a 15-minute budget. Post-hoc diagnostics (deciding no criterion) cost a
further 0.1413 CPU-hours (507.89 s wall-clock).

**Leakage controls (criterion C4).** Nine counted assertions are executed and logged with their
measured value, including when zero: strict temporal ordering per learner; every fitted object
reading only its declared row set; pairwise-disjoint splits; identical split hashes across models;
the test set scored exactly once per model; in the cold-start refit condition, no fitted object
reading a held-out learner's row; the candidate exclusion set matching the information available at
each of the three scoring moments; and no click weight or active-day count reading a row dated
after its bound.

## Results

### Warm-user slice (K = 10, primary split, all 22 presentations)

| Presentation | n_items | n_eval | ceiling P@10 | MostPop | PopWeek | CBF | ItemKNN-CF | Hybrid | Hybrid vs. CBF (rel.) | Hybrid vs. CF (rel.) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 211 | 375 | 0.9029 | 0.1819 | 0.1803 | 0.2816 | 0.1845 | 0.2595 | −7.86% | +40.61% |
| AAA_2014J | 202 | 347 | 0.8657 | 0.1896 | 0.1888 | 0.2288 | 0.1937 | 0.2383 | +4.16% | +23.07% |
| BBB_2013B | 315 | 1404 | 0.6948 | 0.1630 | 0.1630 | 0.1217 | 0.1521 | 0.1709 | +40.37% | +12.31% |
| BBB_2013J | 321 | 1700 | 0.6865 | 0.1564 | 0.2208 | 0.1007 | 0.1365 | 0.1549 | +53.80% | +13.44% |
| BBB_2014B | 311 | 1163 | 0.6689 | 0.1387 | 0.2161 | 0.1023 | 0.1302 | 0.1583 | +54.71% | +21.60% |
| BBB_2014J | 207 | 1773 | 0.8267 | 0.1504 | 0.1150 | 0.1737 | 0.1221 | 0.1553 | −10.58% | +27.26% |
| CCC_2014B | 196 | 1557 | 0.7432 | 0.1699 | 0.1759 | 0.1837 | 0.1836 | 0.2182 | +18.81% | +18.85% |
| CCC_2014J | 223 | 2131 | 0.7502 | 0.1599 | 0.1671 | 0.1673 | 0.1764 | 0.2085 | +24.63% | +18.20% |
| DDD_2013B | 428 | 1150 | 0.9072 | 0.1423 | 0.1423 | 0.0923 | 0.1650 | 0.1678 | +81.90% | +1.74% |
| DDD_2013J | 462 | 1656 | 0.8725 | 0.1412 | 0.1412 | 0.0838 | 0.1268 | 0.1222 | +45.93% | −3.62% |
| DDD_2014B | 453 | 1040 | 0.8675 | 0.1495 | 0.1509 | 0.0941 | 0.1437 | 0.1480 | +57.20% | +2.94% |
| DDD_2014J | 365 | 1523 | 0.8415 | 0.1540 | 0.1560 | 0.1248 | 0.1588 | 0.1731 | +38.72% | +9.06% |
| EEE_2013J | 112 | 898 | 0.8281 | 0.1821 | 0.1465 | 0.1138 | 0.2099 | 0.1551 | +36.30% | −26.10% |
| EEE_2014B | 109 | 584 | 0.7755 | 0.1945 | 0.1615 | 0.0974 | 0.2111 | 0.1664 | +70.83% | −21.17% |
| EEE_2014J | 115 | 1018 | 0.8111 | 0.2116 | 0.1990 | 0.1511 | 0.1877 | 0.1691 | +11.90% | −9.94% |
| FFF_2013B | 508 | 1460 | 0.9406 | 0.2055 | 0.2169 | 0.2427 | 0.2221 | 0.2282 | −5.98% | +2.75% |
| FFF_2013J | 529 | 1989 | 0.9227 | 0.2015 | 0.1739 | 0.1772 | 0.2061 | 0.2234 | +26.11% | +8.42% |
| FFF_2014B | 478 | 1281 | 0.9123 | 0.2098 | 0.1832 | 0.1613 | 0.2308 | 0.2304 | +42.88% | −0.17% |
| FFF_2014J | 452 | 1988 | 0.9087 | 0.2164 | 0.1803 | 0.1260 | 0.2149 | 0.2198 | +74.45% | +2.29% |
| GGG_2013J | 137 | 835 | 0.6764 | 0.1131 | 0.1192 | 0.2320 | 0.1114 | 0.2153 | −7.18% | +93.33% |
| GGG_2014B | 124 | 705 | 0.6474 | 0.1159 | 0.1217 | 0.2465 | 0.1112 | 0.1549 | −37.17% | +39.29% |
| GGG_2014J | 106 | 635 | 0.6912 | 0.1241 | 0.1323 | 0.2665 | 0.1109 | 0.2351 | −11.76% | +112.07% |

*Distribution:* Median Precision@10 — MostPop 0.1615, PopWeek 0.1650, CBF 0.1562, ItemKNN-CF
0.1707, Hybrid 0.1720, Random (mean over 5 seeds) 0.0679. Hybrid vs. CBF relative gain: median
+31.20%, mean +27.37%, range −37.17% to +81.90%, IQR 55.28 pp, 16 wins / 0 ties / 6 losses. Hybrid
vs. ItemKNN-CF relative gain: median +10.68%, mean +17.56%, range −26.10% to +112.07%, IQR 20.82 pp,
17 wins / 0 ties / 5 losses. On the warm slice the hybrid is above both of its own components in 11
of 22 presentations, between them in 11, and below both in none.

*Significance (family F1, decides C1):* Hybrid vs. CBF: n pairs 22, n effective 22, Wilcoxon
p = 0.005929, p_Holm = 0.011857, rank-biserial +0.652, sign-test p = 0.052479 (companion, not the
pre-registered test — it disagrees with the Wilcoxon result here, at p = 0.052479 vs. 0.005929,
because the hybrid's 6 losses are mostly small while its 16 wins include large magnitudes up to
+81.90%). Hybrid vs. ItemKNN-CF: n effective 22, Wilcoxon p = 0.014095, p_Holm = 0.014095,
rank-biserial +0.589, sign-test p = 0.016901.

*Random-floor comparison (exploratory, decides no criterion):* on the warm slice all five
non-random models beat the random floor by a wide margin; the smallest median gap is CBF's +0.0913
Precision@10 (+155.1% relative, 20 of 22 wins).

### Cold-start-refit slice (k = 2, primary split, all 22 presentations)

| Presentation | n_items | n_eval | ceiling P@10 | MostPop | PopWeek | CBF | ItemKNN-CF | Hybrid | Hybrid vs. CBF (rel.) | Hybrid vs. CF (rel.) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 211 | 75 | 0.9293 | 0.0120 | 0.0187 | 0.1280 | 0.0253 | 0.0693 | −45.83% | +173.68% |
| AAA_2014J | 202 | 69 | 0.8609 | 0.0145 | 0.0188 | 0.1058 | 0.0275 | 0.0464 | −56.16% | +68.42% |
| BBB_2013B | 315 | 281 | 0.6961 | 0.0278 | 0.0278 | 0.0829 | 0.0623 | 0.0676 | −18.45% | +8.57% |
| BBB_2013J | 321 | 340 | 0.6912 | 0.0344 | 0.0553 | 0.0612 | 0.0485 | 0.0597 | −2.40% | +23.03% |
| BBB_2014B | 311 | 233 | 0.6614 | 0.0386 | 0.0515 | 0.0609 | 0.0536 | 0.0571 | −6.34% | +6.40% |
| BBB_2014J | 207 | 355 | 0.8279 | 0.0177 | 0.0341 | 0.0701 | 0.0394 | 0.0423 | −39.76% | +7.14% |
| CCC_2014B | 196 | 311 | 0.7431 | 0.0434 | 0.0457 | 0.0881 | 0.0511 | 0.0534 | −39.42% | +4.40% |
| CCC_2014J | 223 | 426 | 0.7451 | 0.0484 | 0.0507 | 0.0516 | 0.0624 | 0.0589 | +14.09% | −5.64% |
| DDD_2013B | 428 | 230 | 0.9130 | 0.0209 | 0.0209 | 0.0357 | 0.0591 | 0.0613 | +71.95% | +3.68% |
| DDD_2013J | 462 | 331 | 0.8710 | 0.0314 | 0.0314 | 0.0982 | 0.0335 | 0.0779 | −20.62% | +132.43% |
| DDD_2014B | 453 | 208 | 0.8620 | 0.0312 | 0.0312 | 0.0952 | 0.0404 | 0.0437 | −54.04% | +8.33% |
| DDD_2014J | 365 | 305 | 0.8380 | 0.0341 | 0.0341 | 0.0675 | 0.0367 | 0.0439 | −34.95% | +19.64% |
| EEE_2013J | 112 | 180 | 0.8306 | 0.0189 | 0.0217 | 0.0456 | 0.0339 | 0.0339 | −25.61% | +0.00% (exact tie) |
| EEE_2014B | 109 | 117 | 0.7872 | 0.0214 | 0.0419 | 0.0795 | 0.0393 | 0.0598 | −24.73% | +52.17% |
| EEE_2014J | 115 | 204 | 0.8015 | 0.0255 | 0.0392 | 0.0407 | 0.0343 | 0.0343 | −15.66% | +0.00% (equal to floating-point precision) |
| FFF_2013B | 508 | 292 | 0.9435 | 0.0120 | 0.0147 | 0.1110 | 0.0274 | 0.0295 | −73.46% | +7.50% |
| FFF_2013J | 529 | 398 | 0.9249 | 0.0141 | 0.0143 | 0.0754 | 0.0399 | 0.0384 | −49.00% | −3.77% |
| FFF_2014B | 478 | 256 | 0.9152 | 0.0176 | 0.0180 | 0.0555 | 0.0305 | 0.0305 | −45.07% | −0.00% (equal to floating-point precision) |
| FFF_2014J | 452 | 398 | 0.9030 | 0.0186 | 0.0183 | 0.0379 | 0.0304 | 0.0312 | −17.88% | +2.48% |
| GGG_2013J | 137 | 167 | 0.6934 | 0.0341 | 0.0365 | 0.0503 | 0.0377 | 0.0383 | −23.81% | +1.59% |
| GGG_2014B | 124 | 141 | 0.6482 | 0.0319 | 0.0319 | 0.1418 | 0.0376 | 0.0482 | −66.00% | +28.30% |
| GGG_2014J | 106 | 127 | 0.6732 | 0.0283 | 0.0339 | 0.1732 | 0.0291 | 0.0693 | −60.00% | +137.84% |

*Distribution:* Median Precision@10 — MostPop 0.0266, PopWeek 0.0317, CBF 0.0728, ItemKNN-CF
0.0377, Hybrid 0.0473, Random (mean over 5 seeds) 0.0484. Hybrid vs. CBF relative gain: median
−30.28%, mean −28.78%, range −73.46% to +71.95%, IQR 30.18 pp, 2 wins / 0 ties / 20 losses. Hybrid
vs. ItemKNN-CF relative gain: median +7.32%, mean +30.74%, range −5.64% to +173.68%, IQR 25.17 pp,
**17 wins, 3 ties (EEE_2013J exact; EEE_2014J and FFF_2014B equal to within floating-point
summation order), 2 losses (CCC_2014J, FFF_2013J)**.

*Significance (family F2, decides C2):* Hybrid vs. CBF: n effective 22, Wilcoxon p = 0.000121,
p_Holm = 0.000241, rank-biserial −0.858. Hybrid vs. ItemKNN-CF: n effective 21 (1 exact zero
difference dropped), Wilcoxon p = 0.000241, p_Holm = 0.000241, rank-biserial +0.844.

*Random-floor comparison (exploratory, decides no criterion):* median Precision@10 in rank order —
CBF 0.0728 > Random 0.0484 > Hybrid 0.0473 > ItemKNN-CF 0.0377 > PopWeek 0.0317 > MostPop 0.0266.

| Model | Median P@10 | Median P@10 − Random | Beats Random in | n eff. | p (uncorrected) | p (Holm within slice) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CBF | 0.0728 | +0.0310 (+71.2%) | 16 of 22 | 22 | 0.003671 | 0.011014 |
| Hybrid | 0.0473 | −0.0038 (−7.0%) | 10 of 22 | 22 | 0.750238 | 0.750238 |
| ItemKNN-CF | 0.0377 | −0.0126 (−27.1%) | 6 of 22 | 22 | 0.046160 | 0.092320 |
| PopWeek | 0.0317 | −0.0263 (−46.4%) | 4 of 22 | 22 | 0.000593 | 0.002371 |
| MostPop | 0.0266 | −0.0264 (−57.7%) | 3 of 22 | 22 | 8.06e-05 | 0.000403 |

Only content-based filtering is clearly above chance on this slice. The hybrid is indistinguishable
from the random floor, and ItemKNN-CF and both popularity baselines sit below it (ItemKNN-CF's
apparent p = 0.046160 does not survive Holm correction within this slice's five tests,
p_Holm = 0.092320). The conjunct of C2 that passes (hybrid vs. ItemKNN-CF) is therefore a gain over
a comparator that does not itself clear chance on this slice.

### Criterion C3, conjunct by conjunct (cold-start-refit slice, k = 2, all 22 presentations)

| Presentation | Hybrid | CBF | MostPop | ≥ CBF | > MostPop | Empty lists | Coverage@10 | All 4 conjuncts |
| --- | ---: | ---: | ---: | :---: | :---: | ---: | ---: | :---: |
| AAA_2013J | 0.0693 | 0.1280 | 0.0120 | no | yes | 0 | 0.1469 | no |
| AAA_2014J | 0.0464 | 0.1058 | 0.0145 | no | yes | 0 | 0.1337 | no |
| BBB_2013B | 0.0676 | 0.0829 | 0.0278 | no | yes | 0 | 0.1905 | no |
| BBB_2013J | 0.0597 | 0.0612 | 0.0344 | no | yes | 0 | 0.1215 | no |
| BBB_2014B | 0.0571 | 0.0609 | 0.0386 | no | yes | 0 | 0.1640 | no |
| BBB_2014J | 0.0423 | 0.0701 | 0.0177 | no | yes | 0 | 0.2705 | no |
| CCC_2014B | 0.0534 | 0.0881 | 0.0434 | no | yes | 0 | 0.3163 | no |
| CCC_2014J | 0.0589 | 0.0516 | 0.0484 | **yes** | yes | 0 | 0.3229 | **yes** |
| DDD_2013B | 0.0613 | 0.0357 | 0.0209 | **yes** | yes | 0 | 0.1869 | **yes** |
| DDD_2013J | 0.0779 | 0.0982 | 0.0314 | no | yes | 0 | 0.1840 | no |
| DDD_2014B | 0.0437 | 0.0952 | 0.0312 | no | yes | 0 | 0.1435 | no |
| DDD_2014J | 0.0439 | 0.0675 | 0.0341 | no | yes | 0 | 0.1589 | no |
| EEE_2013J | 0.0339 | 0.0456 | 0.0189 | no | yes | 0 | 0.2768 | no |
| EEE_2014B | 0.0598 | 0.0795 | 0.0214 | no | yes | 0 | 0.3670 | no |
| EEE_2014J | 0.0343 | 0.0407 | 0.0255 | no | yes | 0 | 0.2957 | no |
| FFF_2013B | 0.0295 | 0.1110 | 0.0120 | no | yes | 0 | 0.1417 | no |
| FFF_2013J | 0.0384 | 0.0754 | 0.0141 | no | yes | 0 | 0.1456 | no |
| FFF_2014B | 0.0305 | 0.0555 | 0.0176 | no | yes | 0 | 0.1276 | no |
| FFF_2014J | 0.0312 | 0.0379 | 0.0186 | no | yes | 0 | 0.1305 | no |
| GGG_2013J | 0.0383 | 0.0503 | 0.0341 | no | yes | 0 | 0.3504 | no |
| GGG_2014B | 0.0482 | 0.1418 | 0.0319 | no | yes | 0 | 0.3468 | no |
| GGG_2014J | 0.0693 | 0.1732 | 0.0283 | no | yes | 0 | 0.5566 | no |
| **Pass count** | | | | **2/22** | 22/22 | 22/22 (all zero) | 22/22 | **2/22** |

Three of C3's four conjuncts hold in all 22 presentations (beats global-popularity, zero empty
lists, ≥10% catalogue coverage, range 0.1215–0.5566). The `≥ CBF` conjunct holds in 2 of 22. Several
of the 20 shortfalls fall inside a bootstrap 95% interval that crosses zero (e.g. BBB_2013J,
hybrid-minus-CBF 95% interval [−0.0126, +0.0097]); each such case is still counted as failing, per
the pre-registered rule. Reported separately for context (decides nothing): against CBF the median
relative difference is −30.28% (p_Holm = 0.000121); against MostPop it is +76.46%
(p_Holm = 9.5e-07, 22 of 22 wins) — a floor the hybrid clears easily in part because MostPop itself
sits a median 0.0264 Precision@10 below the random ranker on this slice (see above).

### Every success criterion, judged as written

| Criterion | Threshold | Measured value | Verdict |
| --- | --- | --- | :---: |
| C1 | warm gain ≥ +10% vs. both AND p_Holm < 0.05 both | vs. CBF +31.20% (p_Holm 0.011857, n=22); vs. CF +10.68% (p_Holm 0.014095, n=22) | **met** |
| C2 | cold-start gain > 0 vs. both AND p_Holm < 0.05 both | vs. CF +7.32% (p_Holm 0.000241, n=21); vs. CBF **−30.28%** (p_Holm 0.000241, n=22) — below zero | **not met** — gap: median needs to exceed 0% against CBF; measured −30.28%, a 30.28-percentage-point shortfall |
| C3 | all 4 conjuncts, each of 22 presentations | `> MostPop` 22/22, `0` empty lists 22/22, `≥10%` coverage 22/22; `≥ CBF` **2/22** | **not met** — gap: 20 of 22 presentations fail the `≥ CBF` conjunct, where all 22 are required |
| C4 | 0 shared rows; 0 hyperparameters outside validation; test scored exactly once | 0 shared rows (val/test, train/val, train/test); 0 of 2,992 hyperparameter records read test data; max test-scoring count 1 of 7,920 cells | **met** |
| C5 | ≤4.0 CPU-h main run AND ≤15 min reproduction | main run 1.0140 CPU-h; reproduction 0.238 min (14.27 s) | **met** (combined from both runs; each run's own file records its own conjunct only, since neither can see the other's number) |
| C6 | ≤1e-6 abs. diff., all 6 phase-1 values, EEE_2014J | all 6 values differ by exactly 0.0 | **met** |

Four criteria are met (C1, C4, C5, C6) and two are not met (C2, C3). Both unmet criteria fail on the
threshold itself (a negative or below-CBF median), not for lack of statistical power: both have an
effective n of 21–22 and Holm-corrected p well below 0.05 in the direction that shows the hybrid
losing to CBF on cold start.

### Generalisation across the 7 modules

| Module | Warm vs. CBF | Warm vs. CF | Cold vs. CBF | Cold vs. CF |
| --- | ---: | ---: | ---: | ---: |
| AAA | −1.85% | +31.84% | −50.99% | +121.05% |
| BBB | +47.09% | +17.52% | −12.40% | +7.86% |
| CCC | +21.72% | +18.52% | −12.66% | −0.62% |
| DDD | +51.56% | +2.34% | −27.78% | +13.99% |
| EEE | +36.30% | −21.17% | −24.73% | +0.00% |
| FFF | +34.50% | +2.52% | −47.04% | +1.24% |
| GGG | −11.76% | +93.33% | −60.00% | +28.30% |

The cold-start loss to CBF is negative in all 7 of 7 modules. The warm-user gain over CBF is
positive in 5 of 7 modules (negative in AAA and GGG); the warm gain over CF is positive in 6 of 7
(negative in EEE); the cold-start gain over CF is positive in 5 of 7, exactly zero in EEE and
negative in CCC. The 22 presentations are 22 presentations of only 7 modules, not 22 independent
draws, so the across-22 tests are indicative of generalisation and not a random sample of courses.

### Generalisation across alternative splits and item filters (exploratory, decides no criterion)

| Check | Warm vs. CBF | Warm vs. CF | Cold (A, k=2) vs. CBF | Cold (A, k=2) vs. CF |
| --- | ---: | ---: | ---: | ---: |
| Primary split (decides C1/C2) | +31.20% | +10.68% | −30.28% | +7.32% |
| Secondary split (global cut-off) | −3.77% (sign reversal) | +18.63% | −51.03% | +85.30% |
| Tertiary split (random 20%, temporally leaky) | +167.11% | −3.57% (sign reversal) | +105.56% (sign reversal) | −3.99% (sign reversal) |
| Item filter loosened to ≥3 resources | +31.20% | +10.70% | −28.24% | +11.31% |
| Item filter tightened to ≥10 resources | +30.16% | +10.71% | −29.71% | +7.09% |

The secondary (global cut-off) split reverses the sign of the warm-user gain over CBF (+31.20% to
−3.77%) while leaving the cold-start pattern qualitatively unchanged. The tertiary (random,
temporally leaky) split reverses three of the four signs and is reported for continuity with prior
evidence, not as a robustness check relied on here. Loosening or tightening the item-count filter
changes no sign and little magnitude. Including two-day learners the day filter excludes (P4b,
union population, not significance-tested) leaves the same cold-start ordering as the primary
split: CBF 0.0683 > Hybrid 0.0529 > ItemKNN-CF 0.0473 > MostPop 0.0471; the last (Hybrid-vs-CF) gap,
+0.54% relative, was never significance-tested and is carried as untested.

### Cold-start construction × split contrast

| Split | Condition A (refit) vs. CBF | Condition A vs. CF | Condition B (shared similarity) vs. CBF | Condition B vs. CF |
| --- | ---: | ---: | ---: | ---: |
| Primary (time-based; decides C1–C3) | −30.28%; 2 W / 20 L / 0 T | +7.32%; 17 W / 2 L / 3 T | −30.16%; 2 W / 20 L / 0 T | +13.34%; 18 W / 3 L / 1 T |
| Tertiary (random 20%; temporally leaky) | +105.56%; 22 W / 0 L / 0 T | −3.99%; 5 W / 16 L / 1 T | +94.77%; 22 W / 0 L / 0 T | −5.42%; 3 W / 18 L / 1 T |

Holding the split fixed, moving between cold-start constructions (A to B) reverses the sign of no
median comparison. Holding the construction fixed, moving between splits (primary to tertiary)
reverses both median directions, under both constructions. Individual presentations do cross zero
on the A-to-B move (e.g., vs. CF on the primary split: FFF_2013J −3.77% under A to +13.87% under B;
FFF_2014J +2.48% to −2.50%; on the tertiary split: AAA_2013J +0.75% to −4.35%), so the statement
above is about the median direction only.

### Prior evidence: an earlier, unreceipted pilot run (context, not evidence for C1–C5)

A pilot evaluation on the same 22 presentations, run before the design above and without a
verifiable execution receipt, used a random 20% per-learner holdout (no time bound) and a
hand-picked blend weight chosen after that pilot's own test results had been seen. Its results are
reported here as prior context only, and are not comparable one-to-one with the receipted numbers
above (they use a different split, click-weighting rule and candidate-exclusion rule).

- Warm slice: hybrid above CBF in 22 of 22 presentations (median +189.54%, range +60.04% to
  +464.55%); hybrid below ItemKNN-CF in 19 of 22 (median −2.66%, best case +0.91% in the 3 wins).
- Cold-start slice (thin-history construction, no refit): hybrid above CBF in 22 of 22 presentations
  (median +73.12%, range +13.55% to +163.85%); hybrid below ItemKNN-CF in 22 of 22 (median −17.90%,
  range −29.12% to −10.03%).
- In three presentations (BBB_2013B, DDD_2013B, DDD_2013J), `week_from`/`week_to` were unknown for
  100% of resources; before the missing-value fallback described in Method existed, this made the
  pilot's hybrid and CBF scores bit-identical in those three presentations, and moved the pilot's
  mean (not median) warm-vs-CF relative gain to −14.8% against a median near −2.9% for the other 19.

**Reproduction (criterion C6).** All six of the pilot's recorded Precision@10 values on EEE_2014J
(warm and cold-start, for CBF, ItemKNN-CF and the pilot's hybrid) were regenerated under the
pilot's own method and matched the recorded values to an absolute difference of exactly 0.0
(tolerance 1e-6):

| Model | Warm slice | Cold-start slice (pilot's construction) |
| --- | ---: | ---: |
| CBF | 0.1182 | 0.1007 |
| ItemKNN-CF | 0.5352 | 0.1610 |
| Hybrid (pilot's hand-picked weight) | 0.5208 | 0.1402 |

This reproduction establishes that the pilot's arithmetic on this one presentation is reproducible
from its own description; it applies none of the leakage bounds used in the design above (the
pilot's click weights carry no date bound), and it does not cover the other 21 presentations.

### Diagnostic D1: fitted blend weight on the cold-start-refit cell (post-hoc, decides no criterion)

| Presentation | n learners | min | Q1 | median | Q3 | max | share ≥0.9 | share ≤0.1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 75 | 0.0933 | 0.1853 | 0.2415 | 0.3123 | 0.4617 | 0.0000 | 0.0133 |
| AAA_2014J | 69 | 0.2853 | 0.3166 | 0.3375 | 0.3606 | 0.3840 | 0.0000 | 0.0000 |
| BBB_2013B | 281 | 0.5156 | 0.6369 | 0.6534 | 0.6689 | 0.7142 | 0.0000 | 0.0000 |
| BBB_2013J | 340 | 0.3601 | 0.5126 | 0.5635 | 0.6143 | 0.8438 | 0.0000 | 0.0000 |
| BBB_2014B | 233 | 0.2461 | 0.5208 | 0.5951 | 0.6483 | 0.7815 | 0.0000 | 0.0000 |
| BBB_2014J | 355 | 0.2432 | 0.3443 | 0.3691 | 0.3999 | 0.5079 | 0.0000 | 0.0000 |
| CCC_2014B | 311 | 0.2867 | 0.4984 | 0.5411 | 0.5810 | 0.9651 | 0.0064 | 0.0000 |
| CCC_2014J | 426 | 0.4508 | 0.6213 | 0.6414 | 0.6534 | 0.8908 | 0.0000 | 0.0000 |
| DDD_2013B | 230 | 0.1451 | 0.5908 | 0.6404 | 0.7390 | 0.7902 | 0.0000 | 0.0000 |
| DDD_2013J | 331 | 0.0757 | 0.3546 | 0.4362 | 0.5207 | 0.7376 | 0.0000 | 0.0030 |
| DDD_2014B | 208 | 0.3523 | 0.4354 | 0.4632 | 0.4909 | 0.5518 | 0.0000 | 0.0000 |
| DDD_2014J | 305 | 0.3121 | 0.4127 | 0.4565 | 0.5131 | 0.6841 | 0.0000 | 0.0000 |
| EEE_2013J | 180 | 0.4647 | 0.5097 | 0.5345 | 0.5910 | 0.7998 | 0.0000 | 0.0000 |
| EEE_2014B | 117 | 0.4074 | 0.4512 | 0.5689 | 0.6653 | 0.8669 | 0.0000 | 0.0000 |
| EEE_2014J | 204 | 0.3809 | 0.5577 | 0.6349 | 0.7112 | 0.8728 | 0.0000 | 0.0000 |
| FFF_2013B | 292 | 0.1463 | 0.2160 | 0.2446 | 0.3060 | 0.4680 | 0.0000 | 0.0000 |
| FFF_2013J | 398 | 0.1204 | 0.3008 | 0.3688 | 0.4356 | 0.6648 | 0.0000 | 0.0000 |
| FFF_2014B | 256 | 0.2713 | 0.4805 | 0.5428 | 0.6034 | 0.8019 | 0.0000 | 0.0000 |
| FFF_2014J | 398 | 0.4835 | 0.5682 | 0.6054 | 0.6812 | 0.8593 | 0.0000 | 0.0000 |
| GGG_2013J | 167 | 0.1534 | 0.4647 | 0.5253 | 0.5806 | 0.7208 | 0.0000 | 0.0000 |
| GGG_2014B | 141 | 0.4068 | 0.4305 | 0.4384 | 0.4511 | 0.5162 | 0.0000 | 0.0000 |
| GGG_2014J | 127 | 0.0696 | 0.1929 | 0.2754 | 0.3495 | 0.5594 | 0.0000 | 0.0315 |
| **Pooled (n=5,444)** | 5444 | 0.0696 | 0.4019 | 0.5150 | 0.6181 | 0.9651 | 0.0004 | 0.0011 |

Alpha is the weight on the collaborative component. Pooled median is 0.5150 (83.9% of records
between 0.3 and 0.7; 0.04% at or above 0.9; 0.11% at or below 0.1) — the fitted weight does not
converge near 1 on this cell. CBF is the stronger single component on the cold-start slice in 20 of
22 presentations, and across exactly those 20 the per-presentation median weight on the weaker
(collaborative) component ranges 0.241 to 0.653 (median 0.494); the hybrid's cold-start Precision@10
lies between its own two components in 19 of 22 presentations, above both in 1, below both in 2.

### Diagnostic D2: behavioural-feature ablation of the blend (post-hoc, decides no criterion)

*Warm-user slice.*

| Presentation | Hybrid P@10 | Hybrid_ablated P@10 | Diff. (ablated − Hybrid) | Relative |
| --- | ---: | ---: | ---: | ---: |
| AAA_2013J | 0.2595 | 0.2560 | −0.0035 | −1.34% |
| AAA_2014J | 0.2383 | 0.2383 | +0.0000 | +0.00% |
| BBB_2013B | 0.1709 | 0.1684 | −0.0024 | −1.42% |
| BBB_2013J | 0.1549 | 0.1538 | −0.0011 | −0.68% |
| BBB_2014B | 0.1583 | 0.1572 | −0.0011 | −0.71% |
| BBB_2014J | 0.1553 | 0.1566 | +0.0013 | +0.84% |
| CCC_2014B | 0.2182 | 0.2181 | −0.0001 | −0.06% |
| CCC_2014J | 0.2085 | 0.2071 | −0.0014 | −0.65% |
| DDD_2013B | 0.1678 | 0.1675 | −0.0003 | −0.21% |
| DDD_2013J | 0.1222 | 0.1223 | +0.0001 | +0.10% |
| DDD_2014B | 0.1480 | 0.1457 | −0.0023 | −1.56% |
| DDD_2014J | 0.1731 | 0.1691 | −0.0041 | −2.35% |
| EEE_2013J | 0.1551 | 0.1541 | −0.0010 | −0.65% |
| EEE_2014B | 0.1664 | 0.1676 | +0.0012 | +0.72% |
| EEE_2014J | 0.1691 | 0.1693 | +0.0002 | +0.12% |
| FFF_2013B | 0.2282 | 0.2234 | −0.0047 | −2.07% |
| FFF_2013J | 0.2234 | 0.2221 | −0.0014 | −0.61% |
| FFF_2014B | 0.2304 | 0.2304 | +0.0000 | +0.00% |
| FFF_2014J | 0.2198 | 0.2202 | +0.0004 | +0.16% |
| GGG_2013J | 0.2153 | 0.2121 | −0.0032 | −1.50% |
| GGG_2014B | 0.1549 | 0.1374 | −0.0174 | −11.26% |
| GGG_2014J | 0.2351 | 0.2317 | −0.0035 | −1.47% |
| **Median over 22** | **0.1720** | **0.1692** | **−0.001088** | **−0.65%** |

Paired exact Wilcoxon (effective n = 21, one tie dropped): W = 34.0, p = 0.003279 (uncorrected, the
only test in this table), rank-biserial −0.706; ablated lower in 15, higher in 6, equal in 1.

*Cold-start-refit slice (k = 2).*

| Presentation | Hybrid P@10 | Hybrid_ablated P@10 | Diff. (ablated − Hybrid) | Relative |
| --- | ---: | ---: | ---: | ---: |
| AAA_2013J | 0.0693 | 0.0640 | −0.0053 | −7.69% |
| AAA_2014J | 0.0464 | 0.0449 | −0.0014 | −3.13% |
| BBB_2013B | 0.0676 | 0.0683 | +0.0007 | +1.05% |
| BBB_2013J | 0.0597 | 0.0591 | −0.0006 | −0.99% |
| BBB_2014B | 0.0571 | 0.0549 | −0.0021 | −3.76% |
| BBB_2014J | 0.0423 | 0.0420 | −0.0003 | −0.67% |
| CCC_2014B | 0.0534 | 0.0524 | −0.0010 | −1.81% |
| CCC_2014J | 0.0589 | 0.0592 | +0.0002 | +0.40% |
| DDD_2013B | 0.0613 | 0.0613 | +0.0000 | +0.00% |
| DDD_2013J | 0.0779 | 0.0822 | +0.0042 | +5.43% |
| DDD_2014B | 0.0437 | 0.0442 | +0.0005 | +1.10% |
| DDD_2014J | 0.0439 | 0.0436 | −0.0003 | −0.75% |
| EEE_2013J | 0.0339 | 0.0350 | +0.0011 | +3.28% |
| EEE_2014B | 0.0598 | 0.0590 | −0.0009 | −1.43% |
| EEE_2014J | 0.0343 | 0.0353 | +0.0010 | +2.86% |
| FFF_2013B | 0.0295 | 0.0329 | +0.0034 | +11.63% |
| FFF_2013J | 0.0384 | 0.0347 | −0.0038 | −9.80% |
| FFF_2014B | 0.0305 | 0.0305 | +0.0000 | +0.00% |
| FFF_2014J | 0.0312 | 0.0312 | +0.0000 | +0.00% |
| GGG_2013J | 0.0383 | 0.0377 | −0.0006 | −1.56% |
| GGG_2014B | 0.0482 | 0.0475 | −0.0007 | −1.47% |
| GGG_2014J | 0.0693 | 0.0709 | +0.0016 | +2.27% |
| **Median over 22** | **0.0473** | **0.0462** | **−0.000141** | **−0.33%** |

Paired exact Wilcoxon (effective n = 20, two ties dropped): W = 93.0, p = 0.674223 (uncorrected);
rank-biserial −0.114; ablated lower in 11, higher in 9, equal in 2. Removing the three
behavioural-proxy columns from the blend's feature set costs a small, detectable amount on warm
users and nothing detectable on cold start; both effects are small beside the gaps the criteria turn
on (warm hybrid-minus-CBF median +0.0413 Precision@10; cold hybrid-minus-CBF median −0.0219).
Because this ablation removes columns from the blend's own feature set rather than a separate
behavioural recommender component, it does not test the hypothesis's behavioural-signal clause on
its own terms.

*Exploratory association check (5 uncorrected Spearman correlations against the hybrid-vs-CBF
cold-start relative gain, n = 22, decides nothing):* all-zero-label drop share in the blend fit,
rho +0.434 (p = 0.0435); alpha IQR within presentation, rho +0.219 (p = 0.3286, uninformative);
alpha median within presentation, rho +0.825 (p < 0.0001); cold ItemKNN-CF/CBF Precision@10 ratio,
rho +0.884 (p < 0.0001); alpha median vs. that ratio (not against the gain itself), rho +0.874
(p < 0.0001). Only the last association is read as informative beyond arithmetic: the
validation-fitted weight tracks which single component is stronger on the test slice across
presentations.

### Descriptive behaviour analysis (RQ1; decides no criterion; feeds no scored model)

Computed over the 27,212 evaluated learners with no time bound (i.e., computed in hindsight over the
whole presentation, which is why these features could not serve as an input to any scored model
without leaking the test period).

*(a) Shape of each behavioural feature, median over the 22 presentations of that presentation's own
percentile.*

| Feature | p05 | p25 | p50 | p75 | p95 | p95/p05 | Range of 22 per-presentation medians |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Click volume | 81.8 | 314.2 | 762.2 | 1572.6 | 3497.4 | 42.8 | 389.0 to 2475.0 |
| Distinct items | 13.0 | 35.0 | 53.0 | 77.0 | 105.3 | 8.1 | 34.0 to 115.0 |
| Active days | 7.0 | 27.5 | 60.5 | 99.4 | 165.3 | 23.6 | 30.0 to 81.0 |
| Distinct first-opening days | 4.0 | 12.9 | 24.0 | 31.5 | 50.0 | 12.5 | 14.0 to 35.0 |
| Mean gap (days) between new items | 1.327 | 2.526 | 3.331 | 4.581 | 7.194 | 5.4 | 1.478 to 5.846 |
| Clicks per active day | 7.456 | 12.112 | 16.224 | 21.206 | 32.082 | 4.3 | 10.341 to 30.114 |

*(b) K-Means, k = 4 (fixed, not selected), four segments per presentation ordered by mean click
volume; median silhouette coefficient 0.3274 (range 0.2782 to 0.3614), computed on a seeded 1,000
learner subsample in the 15 presentations exceeding 1,000 evaluated learners.*

| Segment rank | Median share of cohort | Median click volume | Median distinct items | Median active days |
| --- | ---: | ---: | ---: | ---: |
| Rank 1 (highest) | 0.410 | 2365.8 | 86.9 | 113.7 |
| Rank 2 | 0.347 | 706.6 | 50.2 | 55.0 |
| Rank 3 | 0.147 | 297.2 | 24.7 | 15.9 |
| Rank 4 (lowest) | 0.117 | 126.8 | 19.1 | 13.5 |

Click volume, distinct items, active-day count and distinct first-opening days separate the
evaluated learners widely and produce a non-empty four-way segmentation in 22 of 22 presentations
(smallest cohort 347 learners); the volume ordering is monotonic across ranks in 18 of 22
presentations for distinct items and 14 of 22 for active days, but only 4 of 22 for clicks per
active day and 0 of 22 for the mean gap between new items. `activity_type`, the fourth behaviour
family named in RQ1, was not computed as a learner-level feature here; it is used elsewhere only as
a content-side input to the CBF item vectors and as the axis of the intra-list diversity metric.
No output of this analysis is an input to any of the six compared models.

## Limitations

1. **The evaluated population is narrowed twice, towards engaged learners.** Two pre-registered
   filters (≥5 distinct resources; ≥3 distinct active days) remove 2,016 of 29,228 logged learners;
   the second filter's 997 excluded learners hold a median of 8 distinct resources over a median of
   2 active days, against 55 resources over 52 days for the 27,212 retained. These are learners who
   opened a handful of resources in one or two sittings and did not return.
2. **Cold start here is simulated, not observed.** The cold-start slice truncates an evaluated
   learner's visible history to k items and refits every fitted quantity without that learner; it is
   not a measurement of an actual new-user population, and the learners closest to real new
   registrations (those whose whole recorded activity falls on 1–2 days) were removed by filter 4
   above.
3. **The dataset is one institution's, and records no dwell time.** OULAD is a UK Open University
   distance-learning cohort of 32,593 learner rows; its interaction table (`studentVle.csv`) carries
   only a day offset and a click count, with no duration field anywhere.
4. **The replication unit is not 22 independent draws.** The 22 presentations are 7 modules (2 to 4
   presentations each), sharing catalogues and syllabi; the across-22 tests are indicative of
   generalisation, not a random sample of courses.
5. **Cold-start Precision@10 is small and must be read against its ceiling.** Hybrid cold-start
   values range 0.0295 to 0.0779 (median 0.0473) against a per-presentation attainable ceiling of
   0.6482 to 0.9435; on EEE_2014J at k = 2, 81% of cold-start learners score exactly 0. C3's floors
   are judged on this noisy per-presentation quantity, as pre-registered. On this slice only CBF is
   clearly above a random floor; no cold-start comparison here should be read as showing the hybrid
   ranks new learners well.
6. **The dataset licence is verified for the deposit but not traced to the local copy.** CC BY 4.0
   was verified at the authors' own deposit; the fetch URL of the locally analysed archive is not
   documented, so provenance has one unverified link. No part of the data is redistributed here.
7. **RQ2, as posed, cannot be answered by this design.** The design compares six models, none
   segmented, so no cold-start prior is fitted from behavioural segments and no segmented-vs-unsegmented
   comparison exists.
8. **Conclusions are about one family of hybrid.** A linear score-level blend of cosine CF and
   cosine CBF scores with a validation-fitted weight; no neural or deep architecture was run.
9. **A fixed (non-learned) blend-weight sweep was not run** as a criterion-deciding comparison.
10. **The two post-hoc diagnostics (D1, D2) ran on a separately-hashed code tree from the receipted
    main run** (five files changed: the addition itself); the production hybrid's own metrics inside
    the diagnostics files were checked and agree with the main run's in all 44 cells checked (both
    slices × 22 presentations), with zero differences. Both diagnostics score the test split a
    second time and decide no criterion.
11. **Some execution evidence is unreceipted.** Pre-run unit-test, refusal-check and canary passes
    are not recorded in any run log and are therefore `unchecked` rather than verified, though the
    underlying files exist and their counts match what is claimed.
12. **RQ1's descriptive half covers three of its four named behaviour families.** Click volume,
    active-day count and day-ordered sequence (the last as two scalar summaries only, not an
    ordered-sequence model) were computed at the learner level; activity type was not computed as a
    learner-level behavioural feature, so nothing here says whether it would separate learners.

**What this design cannot conclude, stated directly.** Offline ranking accuracy is not learning
gain: a click records that a resource was opened, not that it was read, understood or useful, so no
causal claim about learning, retention or attainment follows from any number above. No demographic
attribute of `studentInfo.csv` was used as a model feature, filter or stratifier. The candidate set
excludes only what a learner had opened as of the moment scored; unobserved items are treated as
negatives although some may be unobserved positives. Two-sided exact Wilcoxon tests below an
effective 6 pairs cannot reach p < 0.05 at any effect size (not encountered here: effective n was
21 or 22 throughout).

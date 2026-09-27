**Table (Module D). Behavioural feature distributions and K-Means learner segments, all 22 OULAD module presentations.** *(File named `table_module_d_behaviour.md` rather than `table_5_6_*`: chapter 5 already uses 5.6 to 5.12 for its own tables, so the writer assigns the final number.)*

Dataset: OULAD, 22 module presentations across 7 modules. Population: the **evaluated learner cohort** of each presentation -- the learners left after the >= 5 distinct items and >= 3 active days filters -- 27,212 learners in total, 347 to 2131 per presentation; `behaviour.n_learners` equals `foundation_<pres>.json#counts.evaluated` in 22 of 22 presentations, checked here. Source: `results/run_artifacts/u11_s5_run_main/results_<pres>.json#behaviour`, receipt `results/run_receipts/u11_s5_run_main.json`. Produced by `code/behaviour.py`. Values are reproduced as the artifact stores them (feature quantiles and means rounded to 3 decimal places, `segment_means` to 3); nothing was recomputed from raw OULAD and no code was run for this table.

> **Scope of Module D, read from `code/behaviour.py`.** (i) **Descriptive only.** The module is imported by nothing in the scoring path -- not by `models`, `blend`, `cell` or `features` -- and no output of it enters any model; its own docstring states this and `code/tests/test_evaluate.py` checks it. (ii) **No time bound.** The features are computed from the evaluated learners' rows over the whole presentation, not from history before the train/test cut: the module's docstring says they "are read from the evaluated learners' rows without a bound because nothing is predicted from them; they must never be used as a model input". They therefore describe learners in hindsight and could not be used as a cold-start prior without leakage. (iii) **K was fixed, not selected.** `N_SEGMENTS = 4` with the comment that `plan.md` does not name k and 4 is the module's default; there is no search over k and no model-selection criterion, so the silhouette values below are a property of the one k = 4 fit, not the winner of a comparison. (iv) **Fit detail.** `KMeans(n_clusters=4, n_init=10, random_state=42)` on z-scored `log1p` features; `silhouette_score` is computed on a random subsample of `min(1000, n_learners)` learners with `random_state=42`, so for the 15 presentations with more than 1,000 evaluated learners it is an estimate on a 1,000-learner subsample. (v) **Decides no criterion.** Module D appears in no threshold in `plan.md`'s frozen `success_criteria` block.

## D.1 Per-presentation median of each behavioural feature

Median (the 0.50 quantile of the five the artifact stores: 0.05, 0.25, 0.50, 0.75, 0.95).

| Module presentation | n learners | click volume | distinct items | active days | distinct first-opening days | mean gap (days) between new items | clicks per active day |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 375 | 1241.0 | 65.0 | 81.0 | 30.0 | 3.333 | 16.573 |
| AAA_2014J | 347 | 1158.0 | 56.0 | 75.0 | 27.0 | 3.891 | 15.875 |
| BBB_2013B | 1404 | 532.0 | 36.0 | 44.0 | 15.0 | 4.519 | 13.098 |
| BBB_2013J | 1700 | 437.0 | 36.0 | 40.0 | 15.0 | 5.165 | 11.487 |
| BBB_2014B | 1163 | 389.0 | 34.0 | 37.0 | 14.0 | 5.050 | 11.411 |
| BBB_2014J | 1773 | 705.0 | 62.0 | 38.0 | 20.0 | 2.912 | 18.049 |
| CCC_2014B | 1557 | 687.0 | 45.0 | 42.0 | 18.0 | 2.918 | 17.333 |
| CCC_2014J | 2131 | 772.0 | 48.0 | 47.0 | 19.0 | 3.329 | 17.163 |
| DDD_2013B | 1150 | 892.0 | 105.0 | 67.0 | 30.0 | 1.547 | 13.644 |
| DDD_2013J | 1656 | 752.5 | 87.0 | 64.0 | 27.0 | 2.000 | 12.608 |
| DDD_2014B | 1040 | 652.0 | 76.0 | 54.0 | 24.0 | 1.914 | 12.550 |
| DDD_2014J | 1523 | 584.0 | 71.0 | 60.0 | 26.0 | 2.667 | 10.341 |
| EEE_2013J | 898 | 1349.0 | 50.0 | 67.0 | 24.0 | 3.933 | 20.907 |
| EEE_2014B | 584 | 1160.0 | 46.0 | 61.0 | 21.0 | 4.105 | 19.596 |
| EEE_2014J | 1018 | 1346.0 | 50.0 | 68.5 | 24.0 | 4.187 | 19.439 |
| FFF_2013B | 1460 | 2475.0 | 115.0 | 78.0 | 35.0 | 1.478 | 30.114 |
| FFF_2013J | 1989 | 2060.0 | 106.0 | 72.0 | 32.0 | 1.645 | 27.734 |
| FFF_2014B | 1281 | 1853.0 | 94.0 | 63.0 | 30.0 | 1.791 | 27.667 |
| FFF_2014J | 1988 | 2161.0 | 105.0 | 74.0 | 33.0 | 1.755 | 27.957 |
| GGG_2013J | 835 | 516.0 | 36.0 | 33.0 | 17.0 | 5.846 | 15.107 |
| GGG_2014B | 705 | 474.0 | 34.0 | 30.0 | 15.0 | 5.667 | 15.391 |
| GGG_2014J | 635 | 513.0 | 37.0 | 34.0 | 16.0 | 5.462 | 15.158 |
| **median over the 22** | **1222** | **762.2** | **53.0** | **60.5** | **24.0** | **3.331** | **16.224** |

## D.2 Shape of each feature: the median across the 22 presentations of each stored quantile

Values are rounded half-to-even from the artifact's own 3-decimal figures, so a cell ending in a tie (for example a true 314.25 printed as 314.2) is rounding, not a discrepancy. Each cell is the median over the 22 presentations of that presentation's own quantile, so the row describes a typical presentation's spread rather than a pooled learner distribution (the artifact stores quantiles, not per-learner values, so a true pooled distribution is not recoverable from it).

| Feature | p05 | p25 | p50 | p75 | p95 | p95 / p05 | range of the per-presentation medians |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| click volume | 81.8 | 314.2 | 762.2 | 1572.6 | 3497.4 | 42.8 | 389.0 to 2475.0 (BBB_2014B to FFF_2013B) |
| distinct items | 13.0 | 35.0 | 53.0 | 77.0 | 105.3 | 8.1 | 34.0 to 115.0 (BBB_2014B to FFF_2013B) |
| active days | 7.0 | 27.5 | 60.5 | 99.4 | 165.3 | 23.6 | 30.0 to 81.0 (GGG_2014B to AAA_2013J) |
| distinct first-opening days | 4.0 | 12.9 | 24.0 | 31.5 | 50.0 | 12.5 | 14.0 to 35.0 (BBB_2014B to FFF_2013B) |
| mean gap (days) between new items | 1.327 | 2.526 | 3.331 | 4.581 | 7.194 | 5.4 | 1.478 to 5.846 (FFF_2013B to GGG_2013J) |
| clicks per active day | 7.456 | 12.112 | 16.224 | 21.206 | 32.082 | 4.3 | 10.341 to 30.114 (DDD_2014J to FFF_2013B) |

## D.3 Segmentation, k = 4, one fit per presentation

`sizes` is `numpy.bincount` over the KMeans labels, so the four numbers are in **label order (0, 1, 2, 3), and a KMeans label id is arbitrary** -- label 0 of one presentation has no relation to label 0 of another. Sizes are therefore also given sorted, largest first, which is comparable across presentations.

| Module presentation | n learners | sizes (label order) | sizes (sorted, largest first) | largest segment share | smallest segment share | silhouette |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| AAA_2013J | 375 | 170, 139, 30, 36 | 170, 139, 36, 30 | 0.453 | 0.080 | 0.3582 |
| AAA_2014J | 347 | 45, 142, 131, 29 | 142, 131, 45, 29 | 0.409 | 0.084 | 0.3515 |
| BBB_2013B | 1404 | 252, 581, 355, 216 | 581, 355, 252, 216 | 0.414 | 0.154 | 0.2789 |
| BBB_2013J | 1700 | 538, 269, 215, 678 | 678, 538, 269, 215 | 0.399 | 0.126 | 0.2821 |
| BBB_2014B | 1163 | 222, 344, 458, 139 | 458, 344, 222, 139 | 0.394 | 0.120 | 0.2782 |
| BBB_2014J | 1773 | 211, 536, 815, 211 | 815, 536, 211, 211 | 0.460 | 0.119 | 0.3545 |
| CCC_2014B | 1557 | 550, 199, 346, 462 | 550, 462, 346, 199 | 0.353 | 0.128 | 0.3154 |
| CCC_2014J | 2131 | 313, 642, 405, 771 | 771, 642, 405, 313 | 0.362 | 0.147 | 0.2965 |
| DDD_2013B | 1150 | 129, 365, 163, 493 | 493, 365, 163, 129 | 0.429 | 0.112 | 0.3213 |
| DDD_2013J | 1656 | 207, 657, 252, 540 | 657, 540, 252, 207 | 0.397 | 0.125 | 0.3245 |
| DDD_2014B | 1040 | 400, 148, 322, 170 | 400, 322, 170, 148 | 0.385 | 0.142 | 0.3302 |
| DDD_2014J | 1523 | 583, 543, 215, 182 | 583, 543, 215, 182 | 0.383 | 0.120 | 0.3290 |
| EEE_2013J | 898 | 314, 450, 40, 94 | 450, 314, 94, 40 | 0.501 | 0.045 | 0.3464 |
| EEE_2014B | 584 | 162, 293, 97, 32 | 293, 162, 97, 32 | 0.502 | 0.055 | 0.3534 |
| EEE_2014J | 1018 | 505, 70, 312, 131 | 505, 312, 131, 70 | 0.496 | 0.069 | 0.3183 |
| FFF_2013B | 1460 | 601, 208, 126, 525 | 601, 525, 208, 126 | 0.412 | 0.086 | 0.3348 |
| FFF_2013J | 1989 | 865, 311, 130, 683 | 865, 683, 311, 130 | 0.435 | 0.065 | 0.3614 |
| FFF_2014B | 1281 | 148, 487, 213, 433 | 487, 433, 213, 148 | 0.380 | 0.116 | 0.3258 |
| FFF_2014J | 1988 | 798, 223, 326, 641 | 798, 641, 326, 223 | 0.401 | 0.112 | 0.3377 |
| GGG_2013J | 835 | 47, 371, 106, 311 | 371, 311, 106, 47 | 0.444 | 0.056 | 0.3063 |
| GGG_2014B | 705 | 325, 252, 49, 79 | 325, 252, 79, 49 | 0.461 | 0.070 | 0.3384 |
| GGG_2014J | 635 | 306, 75, 52, 202 | 306, 202, 75, 52 | 0.482 | 0.082 | 0.3133 |
| **median over the 22** | **1222** | -- | -- | **0.413** | **0.112** | **0.3274** |

Every presentation returned k = 4 non-empty segments (22 of 22; `min(k, n_learners)` never bound, since the smallest cohort is 347). **Silhouette: median 0.3274, range 0.2782 (BBB_2014B) to 0.3614 (FFF_2013J), quartiles 0.3139 and 0.3444.** All 22 values fall between 0.25 and 0.40.

## D.4 How stable the four segment profiles are across presentations

**What is checkable from the artifact, and what is not.** The artifact stores each segment's feature means under an arbitrary KMeans label id. No correspondence between one presentation's segments and another's is recorded, and inventing a matching procedure (nearest-centroid, Hungarian assignment or similar) would be a new analysis rather than a reading of the artifact. What *can* be checked without inventing anything is whether, **within each presentation**, ordering the four segments by mean click volume also orders them consistently on the other five features. That is done below: rank 1 is the highest-click-volume segment of that presentation, rank 4 the lowest.

| Segment rank (by mean click volume, within each presentation) | median share of the cohort | median click volume | median distinct items | median active days | median distinct first-opening days | median mean gap (days) between new items | median clicks per active day |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| rank 1 (highest) | 0.410 | 2365.8 | 86.9 | 113.7 | 38.7 | 2.806 | 22.218 |
| rank 2 | 0.347 | 706.6 | 50.2 | 55.0 | 20.2 | 4.722 | 16.774 |
| rank 3 | 0.147 | 297.2 | 24.7 | 15.9 | 8.1 | 1.956 | 19.783 |
| rank 4 (lowest) | 0.117 | 126.8 | 19.1 | 13.5 | 6.9 | 4.514 | 11.149 |

**Consistency of the ordering, counted over the 22 presentations.** For each feature, the number of presentations in which that feature is monotonic (non-increasing or non-decreasing) across the four click-volume ranks:

| Feature | monotonic in |
| --- | ---: |
| click volume | **22 of 22** |
| distinct items | **18 of 22** |
| active days | **14 of 22** |
| distinct first-opening days | **15 of 22** |
| mean gap (days) between new items | **0 of 22** |
| clicks per active day | **4 of 22** |

Reading: the click-volume ordering carries **distinct items, active days and distinct first-opening days** with it in 18, 14 and 15 of 22 presentations respectively, so the dominant axis the four segments separate on is simply *how much a learner did*. The two rate/shape features behave differently -- clicks per active day is monotonic in 4 of 22 and the mean gap between new items in 0 of 22 -- so the segments are not a single activity ranking on every feature, but they are close to one on the volume features. Segment sizes are uneven: the largest segment holds a median 41.3% of the cohort and the smallest a median 11.2%.

## D.5 What RQ1 can and cannot be answered from this

RQ1 asks which observable VLE behaviours separate learners well enough to **carry recommendation signal**. Module D answers the first half and not the second.

- **Answered, descriptively.** The six features do separate the evaluated learners, and the spread is wide: taking each presentation's own p95/p05 ratio and reporting the median of the 22, click volume spans about **40 times** between the 5th and 95th percentile (8.2 times for distinct items, 23.4 for active days). These are medians of ratios; the `p95 / p05` column in D.2 divides the median p95 by the median p05 and so reads slightly differently (42.8, 8.1, 23.6) -- both are correct and neither is a pooled learner statistic. A four-way K-Means segmentation is obtainable in 22 of 22 presentations, and its leading axis is activity volume (D.4).
- **Separation is weak to moderate, and that is the actual number.** Silhouette median 0.3274, range 0.2782 to 0.3614 across the 22 presentations: 18 of the 22 fall in the 0.30-0.40 band and 4 fall below 0.30 (BBB_2013B, BBB_2013J, BBB_2014B, CCC_2014J). A silhouette at this level indicates structure that is present but not well separated -- the clusters overlap substantially -- and because k = 4 was fixed rather than selected, these values are not evidence that four is the right number of segments, only that the four-way split is of this quality.
- **Not answered: the "carries recommendation signal" half.** The segments feed no model. `code/behaviour.py` enters no scoring path, no segment label is an input to the hybrid, the content model or the blend, and no criterion depends on Module D. The features are also computed without a time bound, so they could not serve as a cold-start prior even in principle without leaking the test period.
- **The only measured link to recommendation signal is D2**, the post-hoc ablation of the three behavioural columns inside the blend's own feature set (`n_visible`, `log1p_visible_clicks`, `n_active_days`): removing them costs a median **-0.65% relative** Precision@10 on warm users (median -0.001088, 15 of 22 presentations lower, p = 0.003279) and **nothing detectable on cold start** (median -0.000141, -0.33% relative, p = 0.674). That measures the blend's *weighting* use of three behavioural columns, not a behavioural recommender component, and it is post-hoc (see the diagnostics table).
- **Status.** Module D is descriptive analysis computed inside the receipted main run; it is not post-hoc in the sense the D1/D2 diagnostics are, because it was part of the approved code and ran once with the main run under its receipt. It nevertheless **decides no criterion** and revises nothing (rules 3 and 8).

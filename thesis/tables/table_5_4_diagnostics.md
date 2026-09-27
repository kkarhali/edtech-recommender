**Table 5.4. Post-hoc diagnostics D1 (fitted blend weight) and D2 (behavioural-feature ablation), all 22 OULAD module presentations.**

Dataset: OULAD, 22 module presentations across 7 modules. D1: the fitted blend weight `alpha` actually used by the production `Hybrid` when scoring the cold-start-refit cell `A|2` (k = 2 visible items), one record per test-scored learner, 5,444 records in total, equal to that cell's `n_scored` in 22 of 22 presentations. In `models.Hybrid.score` the score is `alpha * CF + (1 - alpha) * CBF`, so **alpha is the weight on the collaborative component** and `1 - alpha` the weight on the content component. D2: Precision@10 at K = 10 for the production `Hybrid` against `Hybrid_ablated`, which drops the three behavioural columns `n_visible`, `log1p_visible_clicks` and `n_active_days` from the blend's own feature set and keeps `cf_top1`, `cf_top10_mass`, `cbf_top1`, `cbf_top10_mass` and `week_missing_share`; identical splits, identical seed 42, same `Ctx`. Sources: `results/run_artifacts/u13d_diag_run/alpha_log_<pres>.jsonl` and `ablation_<pres>.json`, receipt `results/run_receipts/u13d_diag_run.json`; the association block below also reads `results/run_artifacts/u11_s5_run_main/results_<pres>.json`. Recomputed on 2026-09-24 from those files, not from `results/diagnostics_summary.md`'s prose; every figure the runner reported was reproduced, 0 differences.

> **Post-hoc disclosure (reviewer warning W3, `reviews/diag_code_review.md`; carried into chapters 3 and 5).** Both diagnostics score the test split a second time for the production `Hybrid`, by calling `m.score` directly outside the L6 "scored exactly once per model" counter. They are therefore **post-hoc looks at the test split** and may not revise any criterion, threshold, model or the frozen protocol (rules 3 and 8). Neither decides a criterion: the diagnostics stage's own `criteria_verdicts.json` reads `unchecked` for C1 to C6 by construction, and C1 to C6 stand exactly as the receipted main and pilot runs decided them. The addition was verified inert: the production `Hybrid`'s metrics in the ablation files match the main run's `results_<pres>.json` in all 44 cells (1,452 numeric entries compared independently here, 0 differences, maximum absolute difference 0.0).

## D1. Fitted blend weight on the cold-start-refit cell

| Module presentation | n learners | min | Q1 | median | Q3 | max | share alpha >= 0.9 | share alpha <= 0.1 |
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
| **pooled** | **5444** | **0.0696** | **0.4019** | **0.5150** | **0.6181** | **0.9651** | **0.0004** | **0.0011** |

**What D1 shows.** `plan.md`'s Risks section pre-registered the question "if the learned blend weight converges on alpha close to 1 wherever it helps, the content and behavioural components carry no usable marginal signal here". On the cold-start-refit cell it does not converge near 1. Pooled over 5,444 learner records the weight has median **0.5150**, quartiles **0.4019** and **0.6181**, range **0.0696** to **0.9651**; only **0.04%** of learners sit at or above 0.9 (2 of 5,444) and **0.11%** at or below 0.1 (6), while **83.9%** sit between 0.3 and 0.7. Per-presentation medians run from 0.2415 (AAA_2013J) to 0.6534 (BBB_2013B); 12 of 22 have a median above 0.5. The blend is a genuine, roughly even mixture of the two components, not a disguised single model.

**What D1 does not show.** It does not explain C2. The reading it supports is that on the cold-start slice the blend places roughly half its weight on the component that is the weaker of the two there: content-based filtering beats collaborative filtering on cold start in **20 of 22** presentations, and across exactly those 20 the per-presentation median alpha (the weight on the *weaker* collaborative component) runs 0.241 to 0.653 with a median of 0.494. Consistently with that, the hybrid's cold-start Precision@10 lies between its own two components in **19 of 22** presentations (above both in 1, below both in 2), whereas on the warm slice it is above both components in 11 of 22 and below both in 0. This is a **correlate and a reading, not a confirmed mechanism**: confirming it would require manipulating alpha and re-measuring, which is exactly what rules 3 and 8 forbid on a closed criterion, and nothing in these files manipulates anything.

See **Figure 5.3** (`thesis/figures/figure_5_3_alpha_distribution.png`).

## D2. Behavioural-feature ablation

**What D2 tests, exactly.** `Hybrid_ablated` removes three behavioural columns from the *blend's own feature set*, the features the logistic regression uses to choose alpha per learner. It does **not** remove a behavioural recommender component: no sequence model, session model or behaviour-based scorer exists in this design, and the two scored components remain content-based and collaborative in both arms. D2 therefore measures how much the blend's weighting gains from knowing a learner's visible-item count, click volume and active-day count. It is not a test of the hypothesis's behavioural-signal clause and must not be reported as supporting or refuting it.

### Warm-user slice

| Module presentation | n scored | Hybrid P@10 | Hybrid_ablated P@10 | difference (ablated - Hybrid) | relative |
| --- | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 375 | 0.2595 | 0.2560 | -0.0035 | -1.34% |
| AAA_2014J | 347 | 0.2383 | 0.2383 | +0.0000 | +0.00% |
| BBB_2013B | 1404 | 0.1709 | 0.1684 | -0.0024 | -1.42% |
| BBB_2013J | 1700 | 0.1549 | 0.1538 | -0.0011 | -0.68% |
| BBB_2014B | 1163 | 0.1583 | 0.1572 | -0.0011 | -0.71% |
| BBB_2014J | 1773 | 0.1553 | 0.1566 | +0.0013 | +0.84% |
| CCC_2014B | 1557 | 0.2182 | 0.2181 | -0.0001 | -0.06% |
| CCC_2014J | 2131 | 0.2085 | 0.2071 | -0.0014 | -0.65% |
| DDD_2013B | 1150 | 0.1678 | 0.1675 | -0.0003 | -0.21% |
| DDD_2013J | 1656 | 0.1222 | 0.1223 | +0.0001 | +0.10% |
| DDD_2014B | 1040 | 0.1480 | 0.1457 | -0.0023 | -1.56% |
| DDD_2014J | 1523 | 0.1731 | 0.1691 | -0.0041 | -2.35% |
| EEE_2013J | 898 | 0.1551 | 0.1541 | -0.0010 | -0.65% |
| EEE_2014B | 584 | 0.1664 | 0.1676 | +0.0012 | +0.72% |
| EEE_2014J | 1018 | 0.1691 | 0.1693 | +0.0002 | +0.12% |
| FFF_2013B | 1460 | 0.2282 | 0.2234 | -0.0047 | -2.07% |
| FFF_2013J | 1989 | 0.2234 | 0.2221 | -0.0014 | -0.61% |
| FFF_2014B | 1281 | 0.2304 | 0.2304 | +0.0000 | +0.00% |
| FFF_2014J | 1988 | 0.2198 | 0.2202 | +0.0004 | +0.16% |
| GGG_2013J | 835 | 0.2153 | 0.2121 | -0.0032 | -1.50% |
| GGG_2014B | 705 | 0.1549 | 0.1374 | -0.0174 | -11.26% |
| GGG_2014J | 635 | 0.2351 | 0.2317 | -0.0035 | -1.47% |
| **median over 22** | | **0.1720** | **0.1692** | **-0.001088** | **-0.65%** |

Paired two-sided exact Wilcoxon signed-rank on the 22 presentation-level values (`zero_method="wilcox"`, `correction=False`, protocol 10.2a). **Effect size: median difference -0.001088 Precision@10 (-0.65% relative), mean difference -0.002016, range -0.0174 to +0.0013, rank-biserial -0.706.** Ablated higher in 6 presentations, lower in 15, exactly equal in 1; effective n = 21, W = 34.0, **p = 0.003279** (uncorrected; this and the other cell's test are the only two tests in this diagnostic, and no criterion depends on either).

### Cold-start-refit slice (k = 2)

| Module presentation | n scored | Hybrid P@10 | Hybrid_ablated P@10 | difference (ablated - Hybrid) | relative |
| --- | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 75 | 0.0693 | 0.0640 | -0.0053 | -7.69% |
| AAA_2014J | 69 | 0.0464 | 0.0449 | -0.0014 | -3.13% |
| BBB_2013B | 281 | 0.0676 | 0.0683 | +0.0007 | +1.05% |
| BBB_2013J | 340 | 0.0597 | 0.0591 | -0.0006 | -0.99% |
| BBB_2014B | 233 | 0.0571 | 0.0549 | -0.0021 | -3.76% |
| BBB_2014J | 355 | 0.0423 | 0.0420 | -0.0003 | -0.67% |
| CCC_2014B | 311 | 0.0534 | 0.0524 | -0.0010 | -1.81% |
| CCC_2014J | 426 | 0.0589 | 0.0592 | +0.0002 | +0.40% |
| DDD_2013B | 230 | 0.0613 | 0.0613 | +0.0000 | +0.00% |
| DDD_2013J | 331 | 0.0779 | 0.0822 | +0.0042 | +5.43% |
| DDD_2014B | 208 | 0.0437 | 0.0442 | +0.0005 | +1.10% |
| DDD_2014J | 305 | 0.0439 | 0.0436 | -0.0003 | -0.75% |
| EEE_2013J | 180 | 0.0339 | 0.0350 | +0.0011 | +3.28% |
| EEE_2014B | 117 | 0.0598 | 0.0590 | -0.0009 | -1.43% |
| EEE_2014J | 204 | 0.0343 | 0.0353 | +0.0010 | +2.86% |
| FFF_2013B | 292 | 0.0295 | 0.0329 | +0.0034 | +11.63% |
| FFF_2013J | 398 | 0.0384 | 0.0347 | -0.0038 | -9.80% |
| FFF_2014B | 256 | 0.0305 | 0.0305 | +0.0000 | +0.00% |
| FFF_2014J | 398 | 0.0312 | 0.0312 | +0.0000 | +0.00% |
| GGG_2013J | 167 | 0.0383 | 0.0377 | -0.0006 | -1.56% |
| GGG_2014B | 141 | 0.0482 | 0.0475 | -0.0007 | -1.47% |
| GGG_2014J | 127 | 0.0693 | 0.0709 | +0.0016 | +2.27% |
| **median over 22** | | **0.0473** | **0.0462** | **-0.000141** | **-0.33%** |

Paired two-sided exact Wilcoxon signed-rank on the 22 presentation-level values (`zero_method="wilcox"`, `correction=False`, protocol 10.2a). **Effect size: median difference -0.000141 Precision@10 (-0.33% relative), mean difference -0.000194, range -0.0053 to +0.0042, rank-biserial -0.114.** Ablated higher in 9 presentations, lower in 11, exactly equal in 2; effective n = 20, W = 93.0, **p = 0.674223** (uncorrected; this and the other cell's test are the only two tests in this diagnostic, and no criterion depends on either).

**What D2 shows.** On warm users the three behavioural columns make a small but consistent contribution to the blend: removing them costs a median 0.001088 Precision@10 (0.65% relative), with the ablated model lower in 15 of 22 presentations and higher in 6, p = 0.003279. On the cold-start-refit slice no contribution is detectable: median difference -0.000141 Precision@10 (-0.33% relative), lower in 11 and higher in 9, p = 0.674. Both effects are small in absolute terms next to the gaps the criteria turn on -- the warm effect is about 0.0011 Precision@10 against a hybrid-versus-CBF gap of +0.0413 (median absolute difference, Table 5.1), and the cold effect is about 0.0001 against a hybrid-versus-CBF gap of -0.0219 (Table 5.2). Removing these features would not have changed any criterion verdict, and no criterion may be revised on this evidence in any case (rules 3 and 8).

**Rounding rule for this table.** Precision@10 values, absolute differences and alpha quantiles are printed to 4 decimal places; relative gains and shares-as-percentages to 2 decimal places; p-values to 6 decimal places or 6 significant figures. Every printed value is rounded from the full-precision number read out of the artifact, never truncated, and every test is computed on the full-precision values rather than on the printed ones. The two scale figures quoted in the paragraph above are the medians of the per-presentation absolute differences, +0.041258 -> +0.0413 on warm and -0.021924 -> -0.0219 on cold start (`criteria_verdicts.json#C1.values.vs_CBF.wilcoxon.median_diff` and `#C2.values.vs_CBF.wilcoxon.median_diff`); an earlier version of this table printed the warm figure as +0.0412, a truncation, now corrected.

## Exploratory association check (n = 22, decides nothing)

Spearman rank correlations against the hybrid-versus-CBF relative gain on the cold-start-refit slice, one point per module presentation. **Exploratory: five correlations were run, none corrected for multiplicity, on 22 presentations that `methodology/protocol.md` 10.4 itself treats as 7 modules rather than 22 independent draws. None of these is causal and none decides anything.**

| Quantity correlated with the hybrid-vs-CBF cold-start relative gain | Spearman rho | p (uncorrected) | reading |
| --- | ---: | ---: | --- |
| all-zero-label drop share (A\|2 blend supervision) | +0.434 | 0.0435 | **sign is opposite to the label-collapse explanation offered before these diagnostics ran**, and weak; that explanation is withdrawn |
| alpha IQR within the presentation | +0.219 | 0.3286 | uninformative |
| alpha median within the presentation | +0.825 | 0.0000 | strong, but largely mediated by the CF/CBF strength ratio in the row below |
| cold CF / CBF Precision@10 ratio | +0.884 | 0.0000 | close to arithmetically induced: the hybrid lies between its components in 19 of 22, so its gain over CBF must rise as CF strengthens relative to CBF -- not an empirical finding |
| *(not against the gain)* alpha median vs. cold CF / CBF Precision@10 ratio | +0.874 | 0.0000 | the one association here that is neither definitional nor uninformative: the weight fitted on validation data does track which component is stronger on the test slice, across presentations |

**Outcome of the check.** It is partly uninformative and partly near-definitional, and on the one question it was built to settle it returns the wrong sign: the share of validation learners dropped for all-zero labels correlates **positively** with the hybrid's cold-start gain over CBF (rho +0.434, p = 0.0435, n = 22), whereas the label-collapse explanation recorded in the previous analysis cycle predicts a negative association. That explanation is therefore **withdrawn**, not merely softened. What survives is the weaker, descriptive reading in the D1 section above, and it stays labelled as a reading.

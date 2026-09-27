**Table 5.1. Precision@10, warm-user slice, primary time-based split, all 22 OULAD module presentations, K = 10, identical splits for all six models.**

Dataset: OULAD (Open University Learning Analytics Dataset), 32,593 learner rows counted in `studentInfo.csv`; 22 module presentations across 7 modules. Metric: Precision@10, per-presentation macro mean over evaluated learners. K = 10. Slice: warm-user held-out slice of the primary time-based split (cell `warm|None`); the split is cut per module presentation by the OULAD `date` column, and evaluated learners are filtered to at least 5 distinct items and at least 3 active days (`methodology/protocol.md`). Evaluated learners: 27,212 in total across the 22 presentations (per-presentation counts in the `n_eval` column). Source: `results/run_artifacts/u11_s5_run_main/results_<pres>.json` (`splits.primary.cells["warm|None"].models.<model>["P@10"].mean`) and `foundation_<pres>.json` (`counts.n_items`). Recomputed on 2026-09-22 from the per-presentation artifacts named above, not copied from `results/summary.md`; every value was re-derived to the last printed digit and cross-checked against `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json` with 0 mismatches.

| Module presentation | n_items | n_eval | ceiling P@10 | MostPop | PopWeek | CBF | ItemKNN-CF | Hybrid | Hybrid vs. CBF (rel.) | Hybrid vs. CF (rel.) | Hybrid - CBF (abs.) | Hybrid - CF (abs.) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 211 | 375 | 0.9029 | 0.1819 | 0.1803 | 0.2816 | 0.1845 | **0.2595** | -7.86% | +40.61% | -0.0221 | +0.0749 |
| AAA_2014J | 202 | 347 | 0.8657 | 0.1896 | 0.1888 | 0.2288 | 0.1937 | **0.2383** | +4.16% | +23.07% | +0.0095 | +0.0447 |
| BBB_2013B | 315 | 1404 | 0.6948 | 0.1630 | 0.1630 | 0.1217 | 0.1521 | **0.1709** | +40.37% | +12.31% | +0.0491 | +0.0187 |
| BBB_2013J | 321 | 1700 | 0.6865 | 0.1564 | 0.2208 | 0.1007 | 0.1365 | **0.1549** | +53.80% | +13.44% | +0.0542 | +0.0184 |
| BBB_2014B | 311 | 1163 | 0.6689 | 0.1387 | 0.2161 | 0.1023 | 0.1302 | **0.1583** | +54.71% | +21.60% | +0.0560 | +0.0281 |
| BBB_2014J | 207 | 1773 | 0.8267 | 0.1504 | 0.1150 | 0.1737 | 0.1221 | **0.1553** | -10.58% | +27.26% | -0.0184 | +0.0333 |
| CCC_2014B | 196 | 1557 | 0.7432 | 0.1699 | 0.1759 | 0.1837 | 0.1836 | **0.2182** | +18.81% | +18.85% | +0.0346 | +0.0346 |
| CCC_2014J | 223 | 2131 | 0.7502 | 0.1599 | 0.1671 | 0.1673 | 0.1764 | **0.2085** | +24.63% | +18.20% | +0.0412 | +0.0321 |
| DDD_2013B | 428 | 1150 | 0.9072 | 0.1423 | 0.1423 | 0.0923 | 0.1650 | **0.1678** | +81.90% | +1.74% | +0.0756 | +0.0029 |
| DDD_2013J | 462 | 1656 | 0.8725 | 0.1412 | 0.1412 | 0.0838 | 0.1268 | **0.1222** | +45.93% | -3.62% | +0.0385 | -0.0046 |
| DDD_2014B | 453 | 1040 | 0.8675 | 0.1495 | 0.1509 | 0.0941 | 0.1437 | **0.1480** | +57.20% | +2.94% | +0.0538 | +0.0042 |
| DDD_2014J | 365 | 1523 | 0.8415 | 0.1540 | 0.1560 | 0.1248 | 0.1588 | **0.1731** | +38.72% | +9.06% | +0.0483 | +0.0144 |
| EEE_2013J | 112 | 898 | 0.8281 | 0.1821 | 0.1465 | 0.1138 | 0.2099 | **0.1551** | +36.30% | -26.10% | +0.0413 | -0.0548 |
| EEE_2014B | 109 | 584 | 0.7755 | 0.1945 | 0.1615 | 0.0974 | 0.2111 | **0.1664** | +70.83% | -21.17% | +0.0690 | -0.0447 |
| EEE_2014J | 115 | 1018 | 0.8111 | 0.2116 | 0.1990 | 0.1511 | 0.1877 | **0.1691** | +11.90% | -9.94% | +0.0180 | -0.0187 |
| FFF_2013B | 508 | 1460 | 0.9406 | 0.2055 | 0.2169 | 0.2427 | 0.2221 | **0.2282** | -5.98% | +2.75% | -0.0145 | +0.0061 |
| FFF_2013J | 529 | 1989 | 0.9227 | 0.2015 | 0.1739 | 0.1772 | 0.2061 | **0.2234** | +26.11% | +8.42% | +0.0463 | +0.0173 |
| FFF_2014B | 478 | 1281 | 0.9123 | 0.2098 | 0.1832 | 0.1613 | 0.2308 | **0.2304** | +42.88% | -0.17% | +0.0692 | -0.0004 |
| FFF_2014J | 452 | 1988 | 0.9087 | 0.2164 | 0.1803 | 0.1260 | 0.2149 | **0.2198** | +74.45% | +2.29% | +0.0938 | +0.0049 |
| GGG_2013J | 137 | 835 | 0.6764 | 0.1131 | 0.1192 | 0.2320 | 0.1114 | **0.2153** | -7.18% | +93.33% | -0.0166 | +0.1040 |
| GGG_2014B | 124 | 705 | 0.6474 | 0.1159 | 0.1217 | 0.2465 | 0.1112 | **0.1549** | -37.17% | +39.29% | -0.0916 | +0.0437 |
| GGG_2014J | 106 | 635 | 0.6912 | 0.1241 | 0.1323 | 0.2665 | 0.1109 | **0.2351** | -11.76% | +112.07% | -0.0313 | +0.1243 |

**Distribution across the 22 presentations** (all 22 rows appear above; no presentation is omitted and no best presentation is reported as the result).

| Model | Median | Mean | Min | Max | IQR | Q1 | Q3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MostPop (global popularity baseline, C3's popularity floor) | 0.1615 | 0.1669 | 0.1131 | 0.2164 | 0.0492 | 0.1441 | 0.1933 |
| PopWeek (week-scoped popularity, reported, decides no criterion) | 0.1650 | 0.1660 | 0.1150 | 0.2208 | 0.0391 | 0.1434 | 0.1825 |
| CBF (content-based-only baseline) | 0.1562 | 0.1622 | 0.0838 | 0.2816 | 0.1123 | 0.1052 | 0.2175 |
| ItemKNN-CF (collaborative-only baseline) | 0.1707 | 0.1677 | 0.1109 | 0.2308 | 0.0712 | 0.1318 | 0.2030 |
| **Hybrid** (CBF + CF + behavioural proxy) | 0.1720 | 0.1897 | 0.1222 | 0.2595 | 0.0665 | 0.1561 | 0.2225 |
| Random (floor; mean over 5 seeds 42-46) | 0.0679 | 0.0727 | 0.0286 | 0.1331 | 0.0258 | 0.0567 | 0.0825 |

| Relative gain | Median | Mean | Min | Max | IQR (percentage points) | Hybrid wins / ties / losses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hybrid vs. CBF | +31.20% | +27.37% | -37.17% | +81.90% | 55.28 | 16 / 0 / 6 |
| Hybrid vs. ItemKNN-CF | +10.68% | +17.56% | -26.10% | +112.07% | 20.82 | 17 / 0 / 5 |

**Significance (criterion C1; pre-registered threshold in `plan.md`: >= +0.10 relative against BOTH baselines, median over the 22 module-presentations, AND paired Wilcoxon signed-rank p < 0.05 after Holm correction for both comparisons).** Paired exact Wilcoxon signed-rank over the 22 presentations, Holm-corrected across the two comparisons in this table (Wilcoxon 1945; Holm 1979; Demsar 2006 on comparing models across datasets). The sign test over the same pairs is reported beside it as a companion, not as the pre-registered test.

| Comparison | n pairs | n effective | zeros dropped | Wilcoxon p (exact) | p Holm | Sign test p | Median relative gain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hybrid vs. CBF | 22 | 22 | 0 | 0.00592852 | 0.011857 | 0.0524788 | +31.20% |
| Hybrid vs. ItemKNN-CF | 22 | 22 | 0 | 0.0140948 | 0.0140948 | 0.0169005 | +10.68% |

**Reading of C1 from this table.** The median relative gain clears the +10% threshold against both baselines (+31.20% vs. CBF, +10.68% vs. ItemKNN-CF) and both Holm-corrected Wilcoxon p-values fall below 0.05 (0.011857 and 0.014095), so C1 is **met** exactly as written. Two limitations belong beside it in the chapter text:

1. The vs.-CF conjunct clears the pre-registered threshold by only **0.68 percentage points** (+10.68% measured against +10.00% required). C1 is a pass, not a comfortable one, and the threshold is not moved either way (rule 3).
2. The pre-registered exact Wilcoxon (p = 0.005929) and the companion sign test (p = 0.052479) **disagree at alpha = 0.05** on the vs.-CBF comparison. The Wilcoxon is the pre-registered test and governs the verdict; the disagreement arises because the hybrid wins 16 of 22 presentations with large positive magnitudes (max +81.90%) while the six losses are mostly small, and the sign test discards magnitude. This belongs in chapter 5's limitations, not in a re-scored verdict.

**Population caveat for every warm-slice claim.** In EEE_2014J the evaluated learners hold a median of 49 distinct resources out of a 115-item catalogue (mean 44.8), counted directly from `studentVle.csv`; the >= 5-item filter removes only 48 of 1,097 learners out of 1,188 registered. The course population is already highly active, so "warm user" here means a very active learner, and the warm-slice result should not be read as covering a typical lightly-engaged e-learning cohort.

See **Figure 5.1** (`thesis/figures/figure_5_1_warm_relative_gain_spread.png`) for the per-presentation spread behind these medians.

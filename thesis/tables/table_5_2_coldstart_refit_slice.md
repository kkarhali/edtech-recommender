**Table 5.2. Precision@10, cold-start-refit slice (k = 2), primary time-based split, all 22 OULAD module presentations, K = 10, identical splits for all six models.**

Dataset: OULAD (Open University Learning Analytics Dataset), 32,593 learner rows counted in `studentInfo.csv`; 22 module presentations across 7 modules. Metric: Precision@10, per-presentation macro mean over evaluated learners. K = 10. Slice: cold-start-refit slice at k = 2 visible items (cell `A|2`): the item-item similarity model is refitted with the held-out learners' rows removed from the matrix itself rather than hidden at scoring time. Per the human's Q1 ruling (`decisions.log`) this refit condition is primary and is the one that decides C2 and C3. Evaluated learners: 5,444 in total across the 22 presentations (per-presentation counts in the `n_eval` column). Source: `results/run_artifacts/u11_s5_run_main/results_<pres>.json` (`splits.primary.cells["A|2"].models.<model>["P@10"].mean`) and `foundation_<pres>.json` (`counts.n_items`). Recomputed on 2026-09-22 from the per-presentation artifacts named above, not copied from `results/summary.md`; every value was re-derived to the last printed digit and cross-checked against `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json` with 0 mismatches.

| Module presentation | n_items | n_eval | ceiling P@10 | MostPop | PopWeek | CBF | ItemKNN-CF | Hybrid | Hybrid vs. CBF (rel.) | Hybrid vs. CF (rel.) | Hybrid - CBF (abs.) | Hybrid - CF (abs.) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 211 | 75 | 0.9293 | 0.0120 | 0.0187 | 0.1280 | 0.0253 | **0.0693** | -45.83% | +173.68% | -0.0587 | +0.0440 |
| AAA_2014J | 202 | 69 | 0.8609 | 0.0145 | 0.0188 | 0.1058 | 0.0275 | **0.0464** | -56.16% | +68.42% | -0.0594 | +0.0188 |
| BBB_2013B | 315 | 281 | 0.6961 | 0.0278 | 0.0278 | 0.0829 | 0.0623 | **0.0676** | -18.45% | +8.57% | -0.0153 | +0.0053 |
| BBB_2013J | 321 | 340 | 0.6912 | 0.0344 | 0.0553 | 0.0612 | 0.0485 | **0.0597** | -2.40% | +23.03% | -0.0015 | +0.0112 |
| BBB_2014B | 311 | 233 | 0.6614 | 0.0386 | 0.0515 | 0.0609 | 0.0536 | **0.0571** | -6.34% | +6.40% | -0.0039 | +0.0034 |
| BBB_2014J | 207 | 355 | 0.8279 | 0.0177 | 0.0341 | 0.0701 | 0.0394 | **0.0423** | -39.76% | +7.14% | -0.0279 | +0.0028 |
| CCC_2014B | 196 | 311 | 0.7431 | 0.0434 | 0.0457 | 0.0881 | 0.0511 | **0.0534** | -39.42% | +4.40% | -0.0347 | +0.0023 |
| CCC_2014J | 223 | 426 | 0.7451 | 0.0484 | 0.0507 | 0.0516 | 0.0624 | **0.0589** | +14.09% | -5.64% | +0.0073 | -0.0035 |
| DDD_2013B | 428 | 230 | 0.9130 | 0.0209 | 0.0209 | 0.0357 | 0.0591 | **0.0613** | +71.95% | +3.68% | +0.0257 | +0.0022 |
| DDD_2013J | 462 | 331 | 0.8710 | 0.0314 | 0.0314 | 0.0982 | 0.0335 | **0.0779** | -20.62% | +132.43% | -0.0202 | +0.0444 |
| DDD_2014B | 453 | 208 | 0.8620 | 0.0312 | 0.0312 | 0.0952 | 0.0404 | **0.0437** | -54.04% | +8.33% | -0.0514 | +0.0034 |
| DDD_2014J | 365 | 305 | 0.8380 | 0.0341 | 0.0341 | 0.0675 | 0.0367 | **0.0439** | -34.95% | +19.64% | -0.0236 | +0.0072 |
| EEE_2013J | 112 | 180 | 0.8306 | 0.0189 | 0.0217 | 0.0456 | 0.0339 | **0.0339** | -25.61% | +0.00% | -0.0117 | +0.0000 |
| EEE_2014B | 109 | 117 | 0.7872 | 0.0214 | 0.0419 | 0.0795 | 0.0393 | **0.0598** | -24.73% | +52.17% | -0.0197 | +0.0205 |
| EEE_2014J | 115 | 204 | 0.8015 | 0.0255 | 0.0392 | 0.0407 | 0.0343 | **0.0343** | -15.66% | +0.00% | -0.0064 | +0.0000 |
| FFF_2013B | 508 | 292 | 0.9435 | 0.0120 | 0.0147 | 0.1110 | 0.0274 | **0.0295** | -73.46% | +7.50% | -0.0815 | +0.0021 |
| FFF_2013J | 529 | 398 | 0.9249 | 0.0141 | 0.0143 | 0.0754 | 0.0399 | **0.0384** | -49.00% | -3.77% | -0.0369 | -0.0015 |
| FFF_2014B | 478 | 256 | 0.9152 | 0.0176 | 0.0180 | 0.0555 | 0.0305 | **0.0305** | -45.07% | -0.00% | -0.0250 | -0.0000 |
| FFF_2014J | 452 | 398 | 0.9030 | 0.0186 | 0.0183 | 0.0379 | 0.0304 | **0.0312** | -17.88% | +2.48% | -0.0068 | +0.0008 |
| GGG_2013J | 137 | 167 | 0.6934 | 0.0341 | 0.0365 | 0.0503 | 0.0377 | **0.0383** | -23.81% | +1.59% | -0.0120 | +0.0006 |
| GGG_2014B | 124 | 141 | 0.6482 | 0.0319 | 0.0319 | 0.1418 | 0.0376 | **0.0482** | -66.00% | +28.30% | -0.0936 | +0.0106 |
| GGG_2014J | 106 | 127 | 0.6732 | 0.0283 | 0.0339 | 0.1732 | 0.0291 | **0.0693** | -60.00% | +137.84% | -0.1039 | +0.0402 |

**Distribution across the 22 presentations** (all 22 rows appear above; no presentation is omitted and no best presentation is reported as the result).

| Model | Median | Mean | Min | Max | IQR | Q1 | Q3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MostPop (global popularity baseline, C3's popularity floor) | 0.0266 | 0.0262 | 0.0120 | 0.0484 | 0.0156 | 0.0180 | 0.0336 |
| PopWeek (week-scoped popularity, reported, decides no criterion) | 0.0317 | 0.0314 | 0.0143 | 0.0553 | 0.0192 | 0.0193 | 0.0385 |
| CBF (content-based-only baseline) | 0.0728 | 0.0798 | 0.0357 | 0.1732 | 0.0448 | 0.0526 | 0.0974 |
| ItemKNN-CF (collaborative-only baseline) | 0.0377 | 0.0400 | 0.0253 | 0.0624 | 0.0153 | 0.0312 | 0.0465 |
| **Hybrid** (CBF + CF + behavioural proxy) | 0.0473 | 0.0498 | 0.0295 | 0.0779 | 0.0214 | 0.0384 | 0.0598 |
| Random (floor; mean over 5 seeds 42-46) | 0.0484 | 0.0504 | 0.0242 | 0.0816 | 0.0163 | 0.0405 | 0.0568 |

| Relative gain | Median | Mean | Min | Max | IQR (percentage points) | Hybrid wins / ties / losses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hybrid vs. CBF | -30.28% | -28.78% | -73.46% | +71.95% | 30.18 | 2 / 0 / 20 |
| Hybrid vs. ItemKNN-CF | +7.32% | +30.74% | -5.64% | +173.68% | 25.17 | 17 / 3 / 2 |

**Significance (criterion C2; pre-registered threshold in `plan.md`: > 0 relative against BOTH baselines, median over the 22 module-presentations, AND paired Wilcoxon signed-rank p < 0.05 after Holm correction for both comparisons).** Paired exact Wilcoxon signed-rank over the 22 presentations, Holm-corrected across the two comparisons in this table (Wilcoxon 1945; Holm 1979; Demsar 2006 on comparing models across datasets). The sign test over the same pairs is reported beside it as a companion, not as the pre-registered test.

| Comparison | n pairs | n effective | zeros dropped | Wilcoxon p (exact) | p Holm | Sign test p | Median relative gain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hybrid vs. CBF | 22 | 22 | 0 | 0.00012064 | 0.00024128 | 0.000121117 | -30.28% |
| Hybrid vs. ItemKNN-CF | 22 | 21 | 1 | 0.00024128 | 0.00024128 | 0.00148964 | +7.32% |

**C3 conjunct detail on the same slice.** C3's threshold is `>= CBF Precision@10` AND `> MostPop Precision@10` AND `0 empty top-10 lists` AND `>= 10% catalogue coverage`, required in **each** of the 22 presentations. Source: `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C3.values.per_presentation`, cross-checked against the per-presentation `results_<pres>.json` cells above.

| Module presentation | Hybrid | CBF | MostPop | ge_cbf | gt_mostpop | empty lists | coverage@10 | all four conjuncts |
| --- | ---: | ---: | ---: | :---: | :---: | ---: | ---: | :---: |
| AAA_2013J | 0.0693 | 0.1280 | 0.0120 | **no** | yes | 0 | 0.1469 | no |
| AAA_2014J | 0.0464 | 0.1058 | 0.0145 | **no** | yes | 0 | 0.1337 | no |
| BBB_2013B | 0.0676 | 0.0829 | 0.0278 | **no** | yes | 0 | 0.1905 | no |
| BBB_2013J | 0.0597 | 0.0612 | 0.0344 | **no** | yes | 0 | 0.1215 | no |
| BBB_2014B | 0.0571 | 0.0609 | 0.0386 | **no** | yes | 0 | 0.1640 | no |
| BBB_2014J | 0.0423 | 0.0701 | 0.0177 | **no** | yes | 0 | 0.2705 | no |
| CCC_2014B | 0.0534 | 0.0881 | 0.0434 | **no** | yes | 0 | 0.3163 | no |
| CCC_2014J | 0.0589 | 0.0516 | 0.0484 | yes | yes | 0 | 0.3229 | **yes** |
| DDD_2013B | 0.0613 | 0.0357 | 0.0209 | yes | yes | 0 | 0.1869 | **yes** |
| DDD_2013J | 0.0779 | 0.0982 | 0.0314 | **no** | yes | 0 | 0.1840 | no |
| DDD_2014B | 0.0437 | 0.0952 | 0.0312 | **no** | yes | 0 | 0.1435 | no |
| DDD_2014J | 0.0439 | 0.0675 | 0.0341 | **no** | yes | 0 | 0.1589 | no |
| EEE_2013J | 0.0339 | 0.0456 | 0.0189 | **no** | yes | 0 | 0.2768 | no |
| EEE_2014B | 0.0598 | 0.0795 | 0.0214 | **no** | yes | 0 | 0.3670 | no |
| EEE_2014J | 0.0343 | 0.0407 | 0.0255 | **no** | yes | 0 | 0.2957 | no |
| FFF_2013B | 0.0295 | 0.1110 | 0.0120 | **no** | yes | 0 | 0.1417 | no |
| FFF_2013J | 0.0384 | 0.0754 | 0.0141 | **no** | yes | 0 | 0.1456 | no |
| FFF_2014B | 0.0305 | 0.0555 | 0.0176 | **no** | yes | 0 | 0.1276 | no |
| FFF_2014J | 0.0312 | 0.0379 | 0.0186 | **no** | yes | 0 | 0.1305 | no |
| GGG_2013J | 0.0383 | 0.0503 | 0.0341 | **no** | yes | 0 | 0.3504 | no |
| GGG_2014B | 0.0482 | 0.1418 | 0.0319 | **no** | yes | 0 | 0.3468 | no |
| GGG_2014J | 0.0693 | 0.1732 | 0.0283 | **no** | yes | 0 | 0.5566 | no |
| **conjunct pass count** | -- | -- | -- | **2 / 22** | 22 / 22 | 22 / 22 (all zero) | 22 / 22 | **2 / 22** |

**Reading of C2 and C3 from this table.** C2 requires a positive median relative gain against **both** baselines. Against ItemKNN-CF the hybrid gains a median **+7.32%** (Holm-corrected exact Wilcoxon p = 0.000241, n_eff = 21, one exact zero difference dropped, 17 wins / 3 ties / 2 losses); against CBF it loses a median **-30.28%** (p_holm = 0.000241, n_eff = 22, 2 wins / 20 losses). The CBF conjunct fails on the threshold itself, so C2 is **not met** regardless of significance. C3 fails for the same underlying reason in per-presentation form: `gt_mostpop`, `empty_lists == 0` and `coverage@10 >= 0.10` hold in 22 of 22, while `ge_cbf` holds in only **2 of 22** (CCC_2014J, DDD_2013B), so only 2 of 22 presentations satisfy every conjunct and C3 is **not met**. Per `methodology/protocol.md` 10.5 a shortfall whose bootstrap interval crosses zero (for example BBB_2013J, `diff_vs_cbf_ci95 = [-0.0126, +0.0097]`) is still counted as failing, exactly as pre-declared before the run.

**Correction E2 (`decisions.log` 2026-09-26; applied here and in `thesis/ch05.md`).** An earlier count of this row read 18 wins / 1 tie / 3 losses, treating EEE_2014J's hybrid-versus-CF difference (+2.0e-16, a floating-point artefact of summation order) as a win. Re-derived at a 1e-12 tolerance and cross-checked in `thesis/tables/table_5_14_condition_a_vs_b.md` section 5 by two independently written scripts, the correct count is **17 wins, 3 ties (EEE_2013J exactly; EEE_2014J and FFF_2014B equal only up to floating-point summation order), 2 losses (CCC_2014J, FFF_2013J)**. The median +7.32% and every other value in this table are unaffected; only the win/tie/loss count changes.

**Absolute level caveat.** Cold-start Precision@10 of 0.03-0.08 is not on its own evidence of model failure: it is read against `ceiling_p10` (0.648 to 0.943 across the 22 presentations, column above), the maximum Precision@10 any ranker could reach given how few held-out items the cold-start learners have.

**Contrast with the unreceipted phase 1 pilot, recomputed per presentation from `inputs/prior_evidence/all_modules_metrics.json`.** On its own cold-start condition the pilot beat CBF in 22 of 22 presentations by a median **+73.12%** (range +13.55% to +163.85%) and lost to CF in 22 of 22 by a median **-17.90%** (range -29.12% to -10.03%). The receipted refit condition in the table above reverses both directions: the hybrid now loses to CBF in 20 of 22 (median -30.28%) and beats CF in 17 of 22, with 3 ties and 2 losses (median +7.32%; correction E2 above). Note for chapter 5 (integrity violation E1, `decisions.log` 2026-09-24): the often-quoted "+190%" is the pilot's **warm** gain over CBF (median +189.54%, range +60.04% to +464.55%), not a cold-start figure, and must not be attached to this comparison.

**Hedge carried forward from the run gate (`reviews/run_gate_cycle1.md` W1).** In the exploratory P4b block (two-day learners included; decides no criterion, no significance test run) the cold-start median ranking is CBF 0.0683 > Hybrid 0.0529 > CF 0.0473 > MostPop 0.0471. The last link, CF over MostPop, is a **+0.54% relative gap that was never tested**; it must not be carried into any chapter as a finding that collaborative filtering beats popularity on cold start. The first two links are wide (CBF over Hybrid +29.1%, Hybrid over CF +11.6%) and are consistent with the primary split above.

See **Figure 5.2** (`thesis/figures/figure_5_2_coldstart_relative_gain_spread.png`) for the per-presentation spread behind these medians.

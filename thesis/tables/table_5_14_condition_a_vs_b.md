**Table 5.14. Cold-start construction (Condition A refit vs. Condition B shared similarity) crossed with split (primary time-based vs. tertiary random), hybrid against CBF and ItemKNN-CF, all 22 OULAD module presentations, k = 2 (exploratory, family F4; decides no criterion).**

Dataset: OULAD, 22 module presentations across 7 modules. Metric: Precision@10, per-presentation macro mean over the scored cold-start learners (`models.<model>["P@10"].mean`), K = 10. Slice: the cold-start cohort at k = 2 visible resources (the earliest two by day), 5,444 scored learners in total; per presentation `n_scored` is identical in all four cells, so A and B score the same learners on the same test sets within a split. Conditions, as defined in chapter 3, section 3.5.2: **A** (JSON key `A|2`) refits every fitted quantity without the cohort; **B** (JSON key `B|2`) is the phase 1 construction — one similarity model fitted on every evaluated learner's full training history, visible history truncated only at scoring time — labelled "simulated thin history (optimistic)". Splits: **primary** (per-learner day boundary; decides C1 to C3) and **tertiary** (the pilot's random 20% holdout, labelled temporally leaky wherever it appears). Relative gain = (Hybrid − baseline) / baseline, in percent, not percentage points. CF = ItemKNN-CF.

Source (read-only; no new run, no model refitted; recomputed 2026-09-26 for unit u19_attribution_analysis, revision cycle 3): `results/run_artifacts/u11_s5_run_main/results_<pres>.json`, at `splits.primary.cells["A|2"].models.<model>["P@10"].mean`, `splits.primary.cells["B|2"].models.<model>["P@10"].mean`, `splits.tertiary.cells["A|2"].models.<model>["P@10"].mean` and `splits.tertiary.cells["B|2"].models.<model>["P@10"].mean`, with `<model>` one of `Hybrid`, `CBF`, `ItemKNN-CF`, and `n_scored` from the same cells. The 22 files' SHA256 values match the receipt `results/run_receipts/u11_s5_run_main.json` one for one (listed at the end); combined hash = SHA256 of the 22 lines `<basename>  <sha256>` + newline, in sorted order = **`7aec426953cec622a45ff647b3d7ed1839fcf211fc8654cc11e7ce3a833faf88`**. Pilot contrast recomputed per presentation from `inputs/prior_evidence/all_modules_metrics.json` (`per_module_presentation[].cold_start.<model>.precision_at_10`; SHA256 `9cc04aa6a420b7c6ce5d04b1040c61ab6edd25acd25a56d1e0a7741342795969`; unreceipted prior evidence).

> **Exploratory, family F4; decides no criterion.** Condition B and the tertiary split were pre-declared as reporting only (chapter 3, sections 3.5.2 and 3.12). Nothing here revises C1 to C6, any threshold or any model (rules 3 and 8). The sign-test p-values are two-sided, exact, ties dropped and **uncorrected**, given for scale only; no statement below depends on them.

## 1. Are the Condition B cells present?

Yes. Each of the 22 `results_<pres>.json` files holds `B|0`, `B|1`, `B|2` and `B|5` under `splits.primary.cells`, `splits.secondary.cells` and `splits.tertiary.cells`, beside `A|0` to `A|5` and `A_robust|2`. The key used here is **`B|2`** (Condition A: **`A|2`**). All four cells of the 2 x 2 (condition A/B x split primary/tertiary) exist for all 22 presentations; none is missing. The measured A-versus-B contrast promised in chapter 3 was therefore run inside the receipted main run; chapter 5 had not reported it.

## 2. The 2 x 2 at a glance (medians over the 22 presentations)

| Split \ condition | A (refit): hybrid vs. CBF | A (refit): hybrid vs. CF | B (shared similarity): hybrid vs. CBF | B (shared similarity): hybrid vs. CF |
| --- | ---: | ---: | ---: | ---: |
| Primary (time-based; A decides C2/C3) | **−30.28%**; 2 W / 20 L / 0 T | **+7.32%**; 17 W / 2 L / 3 T | **−30.16%**; 2 W / 20 L / 0 T | **+13.34%**; 18 W / 3 L / 1 T |
| Tertiary (pilot's random 20%; temporally leaky) | **+105.56%**; 22 W / 0 L / 0 T | **−3.99%**; 5 W / 16 L / 1 T | **+94.77%**; 22 W / 0 L / 0 T | **−5.42%**; 3 W / 18 L / 1 T |
| *For contrast: pilot, phase 1 (own code and blend rule, all evaluated learners, random split, B-type construction; unreceipted)* | | | *+73.12%; 22 W / 0 L* | *−17.90%; 0 W / 22 L* |

W / L / T = presentations in which the hybrid is above / below / equal to the baseline. Median Precision@10: primary A — Hybrid 0.0473, CBF 0.0728, CF 0.0377; primary B — 0.0464, 0.0728, 0.0372; tertiary A — 0.1690, 0.0899, 0.1761; tertiary B — 0.1707, 0.0899, 0.1782.

Distribution of the hybrid's relative gain (median [IQR; range]; counts; sign test):

- Primary, A, vs. CBF: −30.28% [IQR −48.21% to −18.02%; range −73.46% to +71.95%]; 2 W / 20 L / 0 T; sign test p = 0.000121
- Primary, A, vs. CF: +7.32% [IQR +1.81% to +26.98%; range −5.64% to +173.68%]; 17 W / 2 L / 3 T; sign test p = 0.000729
- Primary, B, vs. CBF: −30.16% [IQR −47.46% to −13.84%; range −73.15% to +67.07%]; 2 W / 20 L / 0 T; sign test p = 0.000121
- Primary, B, vs. CF: +13.34% [IQR +4.69% to +18.88%; range −4.35% to +160.00%]; 18 W / 3 L / 1 T; sign test p = 0.00149
- Tertiary, A, vs. CBF: +105.56% [IQR +68.75% to +121.98%; range +16.38% to +301.08%]; 22 W / 0 L / 0 T; sign test p = 4.77e-07
- Tertiary, A, vs. CF: −3.99% [IQR −6.30% to −0.11%; range −10.31% to +6.75%]; 5 W / 16 L / 1 T; sign test p = 0.0266
- Tertiary, B, vs. CBF: +94.77% [IQR +69.86% to +125.56%; range +13.79% to +287.10%]; 22 W / 0 L / 0 T; sign test p = 4.77e-07
- Tertiary, B, vs. CF: −5.42% [IQR −7.86% to −2.44%; range −11.90% to +5.35%]; 3 W / 18 L / 1 T; sign test p = 0.00149

Paired per presentation, switching A to B on the same split moves the hybrid's relative gain by a median of 0.00 pp vs. CBF (9 up, 10 down, 3 unchanged) and +0.01 pp vs. CF (11 up, 11 down) on the primary split, and by −1.15 pp vs. CBF (9 up, 13 down) and −0.63 pp vs. CF (8 up, 14 down) on the tertiary split. The gap between the two primary medians vs. CF (+7.32% under A, +13.34% under B) therefore reflects which presentation sits at the median, not a consistent per-presentation shift.

## 3. Per presentation, primary (time-based) split

| Presentation | n | Hybrid (A) | CBF (A) | CF (A) | Hyb vs CBF (A) | Hyb vs CF (A) | Hybrid (B) | CBF (B) | CF (B) | Hyb vs CBF (B) | Hyb vs CF (B) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 75 | 0.0693 | 0.1280 | 0.0253 | −45.83% | +173.68% | 0.0693 | 0.1280 | 0.0267 | −45.83% | +160.00% |
| AAA_2014J | 69 | 0.0464 | 0.1058 | 0.0275 | −56.16% | +68.42% | 0.0333 | 0.1058 | 0.0290 | −68.49% | +15.00% |
| BBB_2013B | 281 | 0.0676 | 0.0829 | 0.0623 | −18.45% | +8.57% | 0.0687 | 0.0829 | 0.0612 | −17.17% | +12.21% |
| BBB_2013J | 340 | 0.0597 | 0.0612 | 0.0485 | −2.40% | +23.03% | 0.0588 | 0.0612 | 0.0482 | −3.85% | +21.95% |
| BBB_2014B | 233 | 0.0571 | 0.0609 | 0.0536 | −6.34% | +6.40% | 0.0567 | 0.0609 | 0.0502 | −7.04% | +12.82% |
| BBB_2014J | 355 | 0.0423 | 0.0701 | 0.0394 | −39.76% | +7.14% | 0.0442 | 0.0701 | 0.0386 | −36.95% | +14.60% |
| CCC_2014B | 311 | 0.0534 | 0.0881 | 0.0511 | −39.42% | +4.40% | 0.0514 | 0.0881 | 0.0502 | −41.61% | +2.56% |
| CCC_2014J | 426 | 0.0589 | 0.0516 | 0.0624 | +14.09% | −5.64% | 0.0568 | 0.0516 | 0.0594 | +10.00% | −4.35% |
| DDD_2013B | 230 | 0.0613 | 0.0357 | 0.0591 | +71.95% | +3.68% | 0.0596 | 0.0357 | 0.0574 | +67.07% | +3.79% |
| DDD_2013J | 331 | 0.0779 | 0.0982 | 0.0335 | −20.62% | +132.43% | 0.0852 | 0.0982 | 0.0387 | −13.23% | +120.31% |
| DDD_2014B | 208 | 0.0437 | 0.0952 | 0.0404 | −54.04% | +8.33% | 0.0452 | 0.0952 | 0.0394 | −52.53% | +14.63% |
| DDD_2014J | 305 | 0.0439 | 0.0675 | 0.0367 | −34.95% | +19.64% | 0.0433 | 0.0675 | 0.0361 | −35.92% | +20.00% |
| EEE_2013J | 180 | 0.0339 | 0.0456 | 0.0339 | −25.61% | 0.00% (tie) | 0.0344 | 0.0456 | 0.0317 | −24.39% | +8.77% |
| EEE_2014B | 117 | 0.0598 | 0.0795 | 0.0393 | −24.73% | +52.17% | 0.0701 | 0.0795 | 0.0342 | −11.83% | +105.00% |
| EEE_2014J | 204 | 0.0343 | 0.0407 | 0.0343 | −15.66% | 0.00% (tie) | 0.0343 | 0.0407 | 0.0314 | −15.66% | +9.38% |
| FFF_2013B | 292 | 0.0295 | 0.1110 | 0.0274 | −73.46% | +7.50% | 0.0298 | 0.1110 | 0.0277 | −73.15% | +7.41% |
| FFF_2013J | 398 | 0.0384 | 0.0754 | 0.0399 | −49.00% | −3.77% | 0.0392 | 0.0754 | 0.0344 | −48.00% | +13.87% |
| FFF_2014B | 256 | 0.0305 | 0.0555 | 0.0305 | −45.07% | 0.00% (tie) | 0.0320 | 0.0555 | 0.0324 | −42.25% | −1.20% |
| FFF_2014J | 398 | 0.0312 | 0.0379 | 0.0304 | −17.88% | +2.48% | 0.0294 | 0.0379 | 0.0302 | −22.52% | −2.50% |
| GGG_2013J | 167 | 0.0383 | 0.0503 | 0.0377 | −23.81% | +1.59% | 0.0383 | 0.0503 | 0.0383 | −23.81% | 0.00% (tie) |
| GGG_2014B | 141 | 0.0482 | 0.1418 | 0.0376 | −66.00% | +28.30% | 0.0475 | 0.1418 | 0.0411 | −66.50% | +15.52% |
| GGG_2014J | 127 | 0.0693 | 0.1732 | 0.0291 | −60.00% | +137.84% | 0.0677 | 0.1732 | 0.0346 | −60.91% | +95.45% |
| **Median (22)** | 5444 | 0.0473 | 0.0728 | 0.0377 | **−30.28%** | **+7.32%** | 0.0464 | 0.0728 | 0.0372 | **−30.16%** | **+13.34%** |
| **Hybrid wins / losses / ties** | | | | | 2 W / 20 L / 0 T | 17 W / 2 L / 3 T | | | | 2 W / 20 L / 0 T | 18 W / 3 L / 1 T |

## 4. Per presentation, tertiary (random) split — Condition A is what Table 5.8's tertiary cold-start cells summarise; Condition B is its counterpart

| Presentation | n | Hybrid (A) | CBF (A) | CF (A) | Hyb vs CBF (A) | Hyb vs CF (A) | Hybrid (B) | CBF (B) | CF (B) | Hyb vs CBF (B) | Hyb vs CF (B) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAA_2013J | 75 | 0.1800 | 0.1547 | 0.1787 | +16.38% | +0.75% | 0.1760 | 0.1547 | 0.1840 | +13.79% | −4.35% |
| AAA_2014J | 69 | 0.1580 | 0.1203 | 0.1638 | +31.33% | −3.54% | 0.1565 | 0.1203 | 0.1739 | +30.12% | −10.00% |
| BBB_2013B | 281 | 0.1605 | 0.0495 | 0.1772 | +224.46% | −9.44% | 0.1580 | 0.0495 | 0.1794 | +219.42% | −11.90% |
| BBB_2013J | 340 | 0.1732 | 0.0703 | 0.1812 | +146.44% | −4.38% | 0.1703 | 0.0703 | 0.1771 | +142.26% | −3.82% |
| BBB_2014B | 233 | 0.1601 | 0.0790 | 0.1730 | +102.72% | −7.44% | 0.1597 | 0.0790 | 0.1734 | +102.17% | −7.92% |
| BBB_2014J | 355 | 0.1470 | 0.1135 | 0.1639 | +29.53% | −10.31% | 0.1493 | 0.1135 | 0.1634 | +31.51% | −8.62% |
| CCC_2014B | 311 | 0.1402 | 0.0656 | 0.1492 | +113.73% | −6.03% | 0.1367 | 0.0656 | 0.1460 | +108.33% | −6.39% |
| CCC_2014J | 426 | 0.1570 | 0.0754 | 0.1629 | +108.41% | −3.60% | 0.1385 | 0.0754 | 0.1566 | +83.80% | −11.54% |
| DDD_2013B | 230 | 0.1622 | 0.0404 | 0.1713 | +301.08% | −5.33% | 0.1565 | 0.0404 | 0.1696 | +287.10% | −7.69% |
| DDD_2013J | 331 | 0.1631 | 0.0704 | 0.1686 | +131.76% | −3.23% | 0.1634 | 0.0704 | 0.1701 | +132.19% | −3.91% |
| DDD_2014B | 208 | 0.1688 | 0.0755 | 0.1716 | +123.57% | −1.68% | 0.1659 | 0.0755 | 0.1697 | +119.75% | −2.27% |
| DDD_2014J | 305 | 0.1692 | 0.0961 | 0.1692 | +76.11% | 0.00% (tie) | 0.1711 | 0.0961 | 0.1731 | +78.16% | −1.14% |
| EEE_2013J | 180 | 0.1906 | 0.1011 | 0.1850 | +88.46% | +3.00% | 0.1894 | 0.1011 | 0.1894 | +87.36% | 0.00% (tie) |
| EEE_2014B | 117 | 0.1889 | 0.0872 | 0.1897 | +116.67% | −0.45% | 0.1846 | 0.0872 | 0.1983 | +111.76% | −6.90% |
| EEE_2014J | 204 | 0.1877 | 0.1113 | 0.1971 | +68.72% | −4.73% | 0.1882 | 0.1113 | 0.1975 | +69.16% | −4.71% |
| FFF_2013B | 292 | 0.1856 | 0.1099 | 0.1983 | +68.85% | −6.39% | 0.1890 | 0.1099 | 0.2014 | +71.96% | −6.12% |
| FFF_2013J | 398 | 0.1874 | 0.1073 | 0.1817 | +74.71% | +3.18% | 0.1930 | 0.1073 | 0.1832 | +79.86% | +5.35% |
| FFF_2014B | 256 | 0.1977 | 0.0926 | 0.1852 | +113.50% | +6.75% | 0.1941 | 0.0926 | 0.1902 | +109.70% | +2.05% |
| FFF_2014J | 398 | 0.1807 | 0.0832 | 0.1759 | +117.22% | +2.71% | 0.1892 | 0.0832 | 0.1827 | +127.49% | +3.58% |
| GGG_2013J | 167 | 0.1707 | 0.0749 | 0.1826 | +128.00% | −6.56% | 0.1772 | 0.0749 | 0.1826 | +136.80% | −2.95% |
| GGG_2014B | 141 | 0.1574 | 0.0993 | 0.1652 | +58.57% | −4.72% | 0.1504 | 0.0993 | 0.1638 | +51.43% | −8.23% |
| GGG_2014J | 127 | 0.1622 | 0.1079 | 0.1764 | +50.36% | −8.04% | 0.1780 | 0.1079 | 0.1906 | +64.96% | −6.61% |
| **Median (22)** | 5444 | 0.1690 | 0.0899 | 0.1761 | **+105.56%** | **−3.99%** | 0.1707 | 0.0899 | 0.1782 | **+94.77%** | **−5.42%** |
| **Hybrid wins / losses / ties** | | | | | 22 W / 0 L / 0 T | 5 W / 16 L / 1 T | | | | 22 W / 0 L / 0 T | 3 W / 18 L / 1 T |

## 5. Notes on the numbers

- **CBF is identical under A and B** in all 22 presentations on both splits (bit-for-bit, e.g. primary EEE_2014J 0.0407 in both cells). This fits CBF depending only on item features and the learner's own visible items, so it has nothing for the refit to change; that mechanism was not checked in code for this table (unchecked). It means every A-versus-B difference in the "vs. CBF" columns comes from the hybrid alone.
- **Ties.** Six presentation-cells show hybrid = CF: exactly equal in primary A EEE_2013J, primary B GGG_2013J and tertiary A DDD_2014J, and equal up to floating-point summation order in primary A EEE_2014J (relative gain +2.0e-16) and FFF_2014B (−1.1e-16) and tertiary B EEE_2013J (−1.5e-16). All six are counted as ties (tolerance 1e-12; the smallest real Precision@10 difference possible here is about 1/(10 x 426) ≈ 2.3e-4). The per-learner blend weights in `results/run_artifacts/u13d_diag_run/alpha_log_EEE_2013J.jsonl` sit around 0.5 to 0.6, so the hybrid is not a copy of CF there; the equal means are taken to be equal hit totals, which is unchecked at the per-learner level.
- **Correction to an earlier count (record; correction E2 applied):** once the two primary-split floating-point ties are counted as ties, the Condition A hybrid on the primary split beats CF in **17** of 22 (2 losses: CCC_2014J, FFF_2013J; 3 ties). The earlier figure of **18 of 22** had counted EEE_2014J's +2.0e-16 as a win. `thesis/ch05.md` (C5.35), `thesis/tables/table_5_2_coldstart_refit_slice.md` and Figure 5.2 have since been corrected to 17 of 22 (3 ties, 2 losses) under correction E2. The median (+7.32%) was unaffected.

## 6. Reading (exploratory; descriptive, not a causal test)

In these receipted cells, the direction of the pilot-versus-phase-2 inversion follows the split, not the cold-start construction. With the split held fixed, moving from A to B changes no direction: on the primary split the hybrid loses to CBF (median −30.28% under A, −30.16% under B; 20 of 22 losses under both) and beats CF (+7.32% and +13.34%; 17 and 18 wins). On the tertiary split it beats CBF in 22 of 22 and trails CF (−3.99% and −5.42%; 16 and 18 losses) under both. With the construction held fixed, moving from the time-based to the random split reverses both directions, under A and under B alike. The statements that the cold-start construction is "the only deliberate change" and that the two phases ran "on the same code and the same data" therefore do not account for the inversion. The construction contrast is measured and small; the split contrast reproduces the pilot's direction. Three things are **not** established. (a) *Why* the random split reverses the result: it differs from the primary split in more than one way (no time bound, so test resources can precede the visible ones; hybrid Precision@10 about 3.6 times higher), and no cell isolates which difference matters. (b) The pilot's magnitude: even tertiary B, the cell closest to the pilot's design, gives −5.42% vs. CF against the pilot's −17.90%. The rest of that gap belongs to pilot-to-phase-2 differences that no receipted cell varies (the pilot's blend rule; its population of all evaluated learners rather than a 20% cohort; its candidate rule), and it stays undetermined. (c) Anything about the pilot code beyond EEE_2014J: C6 reproduced the pilot's six recorded values on EEE_2014J only, so the pilot's 22-presentation figures remain unreceipted prior evidence, and the bridge from pilot to phase 2 is receipted on that one presentation alone. The cell that decides C2 and C3 (primary, A) is unchanged by any of this.

## 7. Independent re-derivation

Every number above was computed twice, by two separately written scripts run as separate processes with `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1`. Neither wrote any project file.

- **Pass 1** (standard library: `json`, `statistics.median` and `quantiles(method="inclusive")`, exact binomial sign test via `math.comb`) found the files by glob, computed gains as `(h − b) / b` and wrote its results to a scratch JSON. This file was rendered from that JSON by a separate script, with no hand transcription of any number.
- **Pass 2** (NumPy `median` and `percentile`, sign test via `lgamma`) took the list of 22 files from the run receipt instead, verified each file's SHA256 against the receipt and computed gains as `h / b − 1`. It then compared all 570 values with pass 1 (per-presentation P@10 and gains, quartiles, ranges, win/loss/tie counts, sign-test p-values, the paired A-to-B shifts and the pilot medians) at a relative tolerance of 1e-12 (1e-9 for p-values).
- **First comparison: 5 mismatches**, all caused by the three floating-point ties above (pass 1 compared with exactly 0; pass 2 used a tolerance). Primary A vs. CF was 18 W / 3 L in pass 1 against 17 W / 2 L in pass 2, and tertiary B vs. CF had 19 losses against 18. Pass 1 was changed to a 1e-12 tie tolerance. **Second comparison: 570 values checked, 0 mismatches.** The Table 5.8 values +105.56%, −3.99%, −30.28% and +7.32% are reproduced exactly from the per-presentation files and match `results_summary.json#reporting.tertiary_median_rel_gain["A|2"]` and the primary medians.

### Source file hashes (each equal to the receipt's)

| File | SHA256 |
| --- | --- |
| `results_AAA_2013J.json` | `4929d5e6f31211807ceea33e4c144b68d922171c029bb3ae13ae963880e71b0d` |
| `results_AAA_2014J.json` | `742c52dde79c352062d7c978194e51a967bb92524599d6d7620c056412172c45` |
| `results_BBB_2013B.json` | `c29567e5852d0d086f1efda9a518456dd9589999b8fae86b5644199db4e04d98` |
| `results_BBB_2013J.json` | `f61af46ddb8cb4c24330a491fcd6dede3b2d76cd95e396bd726ab31285560e81` |
| `results_BBB_2014B.json` | `7570deecb7c6bbcb93b92e57ac73324b196cae998f2a296945f8deb06ceb1934` |
| `results_BBB_2014J.json` | `3d85e274437c2653c4c585a7fa9e710c4749f0488e4a091d4d37006c91f9eb75` |
| `results_CCC_2014B.json` | `cc610547a7fb643f65e730dcb0d5a4cb57441e440aafe9563b1ae679b6644df0` |
| `results_CCC_2014J.json` | `31ecaa5ddb7c1bd29c3ade0dcec22c62de28adab4b34965cf82847b10f53f5d6` |
| `results_DDD_2013B.json` | `2c65ecfaaa2b8117f512a87e595383fe042c3bcec8cf872160b6d711e5db4859` |
| `results_DDD_2013J.json` | `5489d8751fbc9fa0eeb580d7295eced608803fe187d0ae3fb3cef2d966c14c72` |
| `results_DDD_2014B.json` | `599cb328593f77e3247bd8e4aaf81cf7d1a40c2ef6d2d198846339a97def8409` |
| `results_DDD_2014J.json` | `64f778ec07b41f3a00cb1c15e4e236275eabdcb55edb8ad65f8d9d10d98d771e` |
| `results_EEE_2013J.json` | `9c34697e7837271e48aec67f4520feb4898f17bcceb8bcb832f00718d891a7e1` |
| `results_EEE_2014B.json` | `fc7242b590aed1676ffdf3c29b335cdd80657523f55cdd67c94ef31c7d75ed55` |
| `results_EEE_2014J.json` | `37d9d614c86499553c99103eaa15331d7b2bbfe32866d0d49aecdc9577f5cbb3` |
| `results_FFF_2013B.json` | `86252a69b31b7c3ab314e2e6de4f6eadd0b8a8d2e4e7318c5c92e30650f16a73` |
| `results_FFF_2013J.json` | `569f44dbdb3bf215a1f6c3dee6b3fb650f8f723343edd13570865283a414fca4` |
| `results_FFF_2014B.json` | `3a273ea6a15d73a13ffceb7f1c986500eceaf8ee86c7ba46e44ddcf2b4219217` |
| `results_FFF_2014J.json` | `c71f76ea5cc8664e3b431b7355be1bbc033e04e3d5c15a8c796381067da56494` |
| `results_GGG_2013J.json` | `6cdb6e414e99945d3257f6c3f1a60b50a92c28789b5e5a106131b09d3dc21275` |
| `results_GGG_2014B.json` | `4745265ea7cc9a36ce1eef858414b64b47872ec86d3873c33b31df94263aa26a` |
| `results_GGG_2014J.json` | `aeec16008f4377b2ecbf79852d5931c45988e8da6fb835fdd4ca4519c4e994b7` |

**Table 5.5. Every compared model against the Random floor, warm slice and cold-start-refit slice, all 22 OULAD module presentations (exploratory, finding F17).**

Dataset: OULAD, 22 module presentations across 7 modules. Metric: Precision@10, per-presentation macro mean over evaluated learners, K = 10. Slices: the warm-user held-out cell `warm|None` (27,212 evaluated learners in total) and the cold-start-refit cell `A|2` at k = 2 visible items (5,444 evaluated learners in total), both on the primary time-based split. `Random` is the reporting-only random ranker, scored as the mean over the five seeds 42 to 46 (`P@10.mean_over_seeds`; the seed-to-seed standard deviation has median 0.00206 on warm and 0.00451 on cold start, so the floor is stable at the resolution of the gaps below). Source: `results/run_artifacts/u11_s5_run_main/results_<pres>.json` (`splits.primary.cells[<cell>].models.<model>["P@10"]`), the same receipted files that decided C1 to C4. Recomputed on 2026-09-24 from those 22 files; **no new run was made and no model was refitted**.

> **Exploratory and post-hoc; decides no criterion.** `Random` is a reporting model: it appears in no threshold in `plan.md`'s frozen `success_criteria` block, and C1 to C6 stand exactly as the receipted main and pilot runs decided them. This comparison was not pre-registered, it is a re-reading of already-scored results rather than a new measurement, and under rules 3 and 8 it may not revise any criterion, threshold or model. Ten paired tests are reported (five models x two slices). The p-values below are **uncorrected**; a Holm column within each slice's five tests is given beside them for transparency, and no claim here depends on either column.

### Warm-user slice

Median Precision@10 over the 22 presentations, in rank order: Hybrid 0.1720 > ItemKNN-CF 0.1707 > PopWeek 0.1650 > MostPop 0.1615 > CBF 0.1562 > Random 0.0679. Evaluated learners: 27,212.

| Model | Median P@10 | Median P@10 - Random | Median relative vs. Random | Beats Random in | Loses to Random in | n effective | W | p (uncorrected) | p (Holm within this slice) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Random (floor) | 0.0679 | -- | -- | -- | -- | -- | -- | -- | -- |
| Hybrid | 0.1720 | +0.1315 | +205.1% | 22 of 22 | 0 of 22 | 22 | 0.0 | 4.76837e-07 | 2.38419e-06 |
| ItemKNN-CF | 0.1707 | +0.1010 | +144.1% | 22 of 22 | 0 of 22 | 22 | 0.0 | 4.76837e-07 | 2.38419e-06 |
| PopWeek | 0.1650 | +0.0976 | +144.7% | 22 of 22 | 0 of 22 | 22 | 0.0 | 4.76837e-07 | 2.38419e-06 |
| MostPop | 0.1615 | +0.0950 | +139.9% | 22 of 22 | 0 of 22 | 22 | 0.0 | 4.76837e-07 | 2.38419e-06 |
| CBF | 0.1562 | +0.0913 | +155.1% | 20 of 22 | 2 of 22 | 22 | 7.0 | 9.05991e-06 | 9.05991e-06 |

### Cold-start-refit slice (k = 2)

Median Precision@10 over the 22 presentations, in rank order: CBF 0.0728 > Random 0.0484 > Hybrid 0.0473 > ItemKNN-CF 0.0377 > PopWeek 0.0317 > MostPop 0.0266. Evaluated learners: 5,444.

| Model | Median P@10 | Median P@10 - Random | Median relative vs. Random | Beats Random in | Loses to Random in | n effective | W | p (uncorrected) | p (Holm within this slice) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Random (floor) | 0.0484 | -- | -- | -- | -- | -- | -- | -- | -- |
| CBF | 0.0728 | +0.0310 | +71.2% | 16 of 22 | 6 of 22 | 22 | 40.0 | 0.00367117 | 0.0110135 |
| Hybrid | 0.0473 | -0.0038 | -7.0% | 10 of 22 | 12 of 22 | 22 | 116.0 | 0.750238 | 0.750238 |
| ItemKNN-CF | 0.0377 | -0.0126 | -27.1% | 6 of 22 | 16 of 22 | 22 | 65.0 | 0.0461602 | 0.0923204 |
| PopWeek | 0.0317 | -0.0263 | -46.4% | 4 of 22 | 18 of 22 | 22 | 27.0 | 0.000592709 | 0.00237083 |
| MostPop | 0.0266 | -0.0264 | -57.7% | 3 of 22 | 19 of 22 | 22 | 16.0 | 8.05855e-05 | 0.000402927 |

**What this shows, and the limits on reading it.**

1. **On the warm slice the floor is not in play.** Every one of the five models beats Random by a wide margin -- the smallest median gap is CBF's +0.0913 Precision@10 (+155.1% relative, 20 of 22 wins) -- so the warm-user comparisons in Table 5.1 are comparisons between rankers that all clearly carry signal.
2. **On the cold-start-refit slice only content-based filtering clearly beats chance.** CBF sits +0.0310 above Random (median, +71.2% relative, 16 of 22 wins, p = 0.003671, p_Holm = 0.011014). The hybrid is indistinguishable from the floor (median -0.0038, -7.0% relative, 10 of 22 wins, p = 0.750238). Collaborative filtering sits **below** the floor (median -0.0126, -27.1%, 6 of 22 wins, p = 0.046160 uncorrected, p_Holm = 0.092320), and the popularity baselines sit further below it still (MostPop median -0.0264, 3 of 22 wins, p = 8.06e-05).
3. **This makes C2's surviving conjunct a low bar, and it is worth saying so in the text.** The hybrid's significant median +7.32% gain over collaborative filtering on cold start (Table 5.2) is a gain over a baseline that is itself at or below a random ranker on that slice. The C2 verdict does not change -- it already reads `not met` -- but the half of C2 that passed should not be reported as evidence of cold-start competence.
4. **C3's `gt_mostpop` conjunct is a weak floor.** It holds in 22 of 22 presentations, but MostPop sits a median 0.0264 Precision@10 *below* Random on this slice (3 of 22 wins against the floor), so clearing it is close to unavoidable for any ranker with signal. The conjunct that actually discriminates is `ge_cbf`, which holds in 2 of 22. C3's verdict is unchanged; this is a comment on how much its passing conjuncts are worth.
5. **Limits.** n = 22 presentations, which `methodology/protocol.md` 10.4 itself treats as 7 modules rather than 22 independent draws; ten paired tests, uncorrected in the "p (uncorrected)" column; `Random` averages five seeds rather than being resampled per comparison; and the whole table is a post-hoc re-reading of already-scored results. No causal claim and no criterion revision follows from any of it (rules 3 and 8).

**Why this is Table 5.5 and not an extension of Table 5.4.** Table 5.4 reports the human-approved diagnostics run `u13d_diag_run`, which produced new artifacts under its own receipt. This table produces no artifact and reruns nothing: it re-reads the main run's receipted per-presentation files. Keeping them apart leaves Tables 5.1 to 5.4 and their captions untouched in number and in scope, so nothing a chapter writer has already cited moves.

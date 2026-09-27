---
status: completed
experiment_stage: diagnostics
unit: u13d_diag_run
exit_code: 0
debug_rounds_used: 0
venv_prefix: D:/Work/Projects/AutoResearch/.venv-pilot
decides_no_criterion: true
---

# Diagnostics summary (unit u13d_diag_run)

## Status of these numbers

**Neither diagnostic decides a criterion.** C1 to C6 were decided by the receipted main and pilot runs
(`results/summary.md`); this stage's own `criteria_verdicts.json` reads `unchecked` for all six by construction.

**Post-hoc disclosure (reviewer warning W3, `reviews/diag_code_review.md`).** The diagnostics stage scores the test split a
second time for the production `Hybrid` (and once for `Hybrid_ablated`) by calling `m.score` directly, outside the L6
"scored exactly once per model" counter. These numbers are therefore post-hoc looks at the test split. They may not be used to
revise any criterion, threshold, model or the frozen protocol (rules 3 and 8), and chapters 3 and 5 must label them post-hoc.
C4, as decided by the receipted main run, is unaffected: this stage ran in its own process with no counter.

Run: `--stage diagnostics`, all 22 presentations, exit 0, 22 `alpha_log_<pres>.jsonl` and 22 `ablation_<pres>.json`
(5,444 alpha records in total). Wall clock 507.89 s, process CPU 508.86 s (0.1413 CPU-hours), no child worker.

## Reviewer warnings carried

**W1, code tree hash.** Main-run tree (G4-approved, in `u11_s5_run_main` manifest and receipt):
`694c3ea6026939967a6b01ab0698ef7336e77a8dd29f0739157e9f9662b0231c`. Tree recomputed by me with
`common.code_tree_sha256()` before this run and recorded in this run's `run_manifest.json`:
`5a8f935a8dd05bb2b8428966ae9794a2cfe1bf6b7573b5005698bad267691b21` (equals the reviewer's value). The difference is exactly
this diagnostics addition. Files whose mtime is later than the main run's last artifact (2026-09-22 12:52 local): `code/models.py`
(16:37:59), `code/blend.py` (16:38:02), `code/diagnostics.py` (16:38:05, new), `code/main.py` (16:40:05), `code/README.md` (16:40:08).
Every other file under `code/` predates the main run. `config_sha256` is unchanged (`bf2b77c0...9409`). `code/` is untracked in git and
no pre-change copy exists, so I could not recompute the old hash; the old value is the one recorded in the main run's manifest.

**W2, shared run.log.** This run appended to `results/run.log`. Before this run: 10,257,030 bytes, sha256
`d547e943a8e02b9fcc26c807b6072f6fafd4bf1e3ca873815de65bda615c0eac` (identical to the main receipt's `run_log_after_sha256`).
After: 10,274,521 bytes, sha256 `5068dad91db95d600083fd271ce7a4adae8343a747d49c0090061f176b82ac12`. The first 10,257,030 bytes of the
file still hash to `d547e943...c0eac`, so the log only grew. **The main receipt's `run_log_after_sha256` is a prefix hash: it covers only the
first 10,257,030 bytes, not the whole file as it now stands.**

**W5, is the addition inert?** Each `ablation_<pres>.json` carries the production Hybrid's own metrics for the warm and A|2 cells. I compared
every one (18 metric entries with mean and median, plus `n_scored`, `n_excluded_no_truth`, `ceiling_p10`,
`share_learners_test_lt10`) for all 22 presentations and both cells (44 cells) against `results_<pres>.json`
(`splits.primary.cells`) of the receipted main run. **All 44 agree exactly (0 differences, maximum absolute difference 0.0).**

## D1: fitted alpha on the A|2 cell

Alpha is the blend weight `models.Hybrid.score` used, captured from `Hybrid.alpha_`, one record per test-scored learner. k = 2 throughout.
Quartiles use linear interpolation (`numpy.percentile` default). `n` is the number of alpha records; it equals the cell's `n_scored` in every
presentation. Shares are of learners.

| presentation | n learners | min | Q1 | median | Q3 | max | share alpha >= 0.9 | share alpha <= 0.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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
| **pooled** | 5444 | 0.0696 | 0.4019 | 0.5150 | 0.6181 | 0.9651 | 0.0004 | 0.0011 |

Alpha record count equals `n_scored` in 22 of 22 presentations.
Pooled n = 5444 against the summed `n_scored` = 5444.

## D2: behavioural-signal ablation

`Hybrid_ablated` drops the three blend features `n_visible`, `log1p_visible_clicks`, `n_active_days` and keeps the other five
(`cf_top1`, `cf_top10_mass`, `cbf_top1`, `cbf_top10_mass`, `week_missing_share`). Values are per-presentation macro mean Precision@10 on the primary
split; difference = ablated minus production Hybrid (positive means the ablated model scored higher).

### Warm cell

| presentation | n scored | Hybrid P@10 | Hybrid_ablated P@10 | difference (ablated - Hybrid) |
| --- | --- | --- | --- | --- |
| AAA_2013J | 375 | 0.2595 | 0.2560 | -0.0035 |
| AAA_2014J | 347 | 0.2383 | 0.2383 | +0.0000 |
| BBB_2013B | 1404 | 0.1709 | 0.1684 | -0.0024 |
| BBB_2013J | 1700 | 0.1549 | 0.1538 | -0.0011 |
| BBB_2014B | 1163 | 0.1583 | 0.1572 | -0.0011 |
| BBB_2014J | 1773 | 0.1553 | 0.1566 | +0.0013 |
| CCC_2014B | 1557 | 0.2182 | 0.2181 | -0.0001 |
| CCC_2014J | 2131 | 0.2085 | 0.2071 | -0.0014 |
| DDD_2013B | 1150 | 0.1678 | 0.1675 | -0.0003 |
| DDD_2013J | 1656 | 0.1222 | 0.1223 | +0.0001 |
| DDD_2014B | 1040 | 0.1480 | 0.1457 | -0.0023 |
| DDD_2014J | 1523 | 0.1731 | 0.1691 | -0.0041 |
| EEE_2013J | 898 | 0.1551 | 0.1541 | -0.0010 |
| EEE_2014B | 584 | 0.1664 | 0.1676 | +0.0012 |
| EEE_2014J | 1018 | 0.1691 | 0.1693 | +0.0002 |
| FFF_2013B | 1460 | 0.2282 | 0.2234 | -0.0047 |
| FFF_2013J | 1989 | 0.2234 | 0.2221 | -0.0014 |
| FFF_2014B | 1281 | 0.2304 | 0.2304 | +0.0000 |
| FFF_2014J | 1988 | 0.2198 | 0.2202 | +0.0004 |
| GGG_2013J | 835 | 0.2153 | 0.2121 | -0.0032 |
| GGG_2014B | 705 | 0.1549 | 0.1374 | -0.0174 |
| GGG_2014J | 635 | 0.2351 | 0.2317 | -0.0035 |
| **median over 22** | | 0.1720 | 0.1692 | -0.0011 |

Paired two-sided Wilcoxon signed-rank on the 22 presentation-level values (`scipy.stats.wilcoxon`, `zero_method="wilcox"`, `correction=False`, exact, as in protocol 10.2a): median difference -0.001088, mean difference -0.002016, range [-0.0174, +0.0013]; ablated higher in 6, lower in 15, equal in 1; **effective n = 21**, statistic = 34.0, p = 0.003279 (uncorrected; it is the only test in this file, so no Holm family applies).

### A|2 cell (cold-start refit, k = 2)

| presentation | n scored | Hybrid P@10 | Hybrid_ablated P@10 | difference (ablated - Hybrid) |
| --- | --- | --- | --- | --- |
| AAA_2013J | 75 | 0.0693 | 0.0640 | -0.0053 |
| AAA_2014J | 69 | 0.0464 | 0.0449 | -0.0014 |
| BBB_2013B | 281 | 0.0676 | 0.0683 | +0.0007 |
| BBB_2013J | 340 | 0.0597 | 0.0591 | -0.0006 |
| BBB_2014B | 233 | 0.0571 | 0.0549 | -0.0021 |
| BBB_2014J | 355 | 0.0423 | 0.0420 | -0.0003 |
| CCC_2014B | 311 | 0.0534 | 0.0524 | -0.0010 |
| CCC_2014J | 426 | 0.0589 | 0.0592 | +0.0002 |
| DDD_2013B | 230 | 0.0613 | 0.0613 | +0.0000 |
| DDD_2013J | 331 | 0.0779 | 0.0822 | +0.0042 |
| DDD_2014B | 208 | 0.0437 | 0.0442 | +0.0005 |
| DDD_2014J | 305 | 0.0439 | 0.0436 | -0.0003 |
| EEE_2013J | 180 | 0.0339 | 0.0350 | +0.0011 |
| EEE_2014B | 117 | 0.0598 | 0.0590 | -0.0009 |
| EEE_2014J | 204 | 0.0343 | 0.0353 | +0.0010 |
| FFF_2013B | 292 | 0.0295 | 0.0329 | +0.0034 |
| FFF_2013J | 398 | 0.0384 | 0.0347 | -0.0038 |
| FFF_2014B | 256 | 0.0305 | 0.0305 | +0.0000 |
| FFF_2014J | 398 | 0.0312 | 0.0312 | +0.0000 |
| GGG_2013J | 167 | 0.0383 | 0.0377 | -0.0006 |
| GGG_2014B | 141 | 0.0482 | 0.0475 | -0.0007 |
| GGG_2014J | 127 | 0.0693 | 0.0709 | +0.0016 |
| **median over 22** | | 0.0473 | 0.0462 | -0.0001 |

Paired two-sided Wilcoxon signed-rank on the 22 presentation-level values (`scipy.stats.wilcoxon`, `zero_method="wilcox"`, `correction=False`, exact, as in protocol 10.2a): median difference -0.000141, mean difference -0.000194, range [-0.0053, +0.0042]; ablated higher in 9, lower in 11, equal in 2; **effective n = 20**, statistic = 93.0, p = 0.674223 (uncorrected; it is the only test in this file, so no Holm family applies).

## Artifacts

`results/run_artifacts/u13d_diag_run/` (47 files: `run_manifest.json`, `criteria_verdicts.json`, `run_summary.json`, 22 `alpha_log_<pres>.jsonl`,
22 `ablation_<pres>.json`), each hashed in `results/run_receipts/u13d_diag_run.json`. The main run's artifacts and receipts were not touched.


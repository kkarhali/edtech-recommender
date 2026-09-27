# State (last update: 2026-09-27)

## project
- idea: hybrid CBF + CF + behavioural signal for e-learning recommendation, MSc thesis
- idea_file: D:/Work/Projects/AutoResearch/data/ideas/e_learning_recommendation_system.txt
- idea_artifact: data/projects/e_learning_thesis/idea.md
- idea_provenance: data/projects/e_learning_thesis/idea_provenance.json (binding 918162da54511db3)
- project_root: D:/Work/Projects/AutoResearch/data/projects/e_learning_thesis
- slug: e_learning_thesis
- current_step: S11 defense preparation; question bank done (61 questions, 10 categories); mock 1 restarted after the 2026-09-27 rate-limit failure
- experiment_phase: closed (main and diagnostics run, receipted)
- waiting_for: mock 1 examiner panel
- last_action: S10 closed, G9 pass at threshold (avg 5.5, seats 5 and 6); S11 bank closed; mock 1 failed on 429 and is being rerun from scratch (no partial files existed)
- next_action: mock 1, mock 2, corrections, slide outline, G10 defense gate (reviewer), then S12 close; G10 and G11 need human items (format checklist, similarity report, sign-off)
- mode: manager-led, one unit per dispatch

## engine
- status: unavailable natively. ar-workflow-engine.py imports fcntl, which Windows Python has not got.
- consequence: units are tracked in this file and in workflow_queue.json by the manager, and every gate verdict is written to a file before a unit closes.
- alternative: run the engine inside the repository's Docker container when the machine can spare the memory.
- recorded deviation: run receipts are written by hand from real file hashes instead of by execute-run.

## agents
- model policy: top tier for planner, methodologist, results analyst, critic and the plan, method and chapter gates; mid tier for scholar, engineer, runner, writer, defense coach and mechanical gates; small tier for tallying. A critic pair and a blind panel use two different models, which also satisfies the independence rule.
- manager: this session
- planner: status=idle last_unit=u03_s1_plan result=plan.md revision 0 skill=thesis-research-planner tier=top
- literature_scholar: status=idle last_unit=u05_s2_literature skill=thesis-literature-scholar tier=mid
- methodologist: status=idle last=wording pass, 12 edits, no design change skill=thesis-methodologist tier=top
- reviewer: status=idle last=G5 cycle 1 approve, 0 blockers, 1 warning skill=thesis-reviewer
- experiment_engineer: status=idle last_unit=u09_s4_code revision=3, all 3 blockers fixed and execution-verified skill=thesis-experiment-engineer tier=mid
- experiment_runner: status=idle last_unit=u13d_diag_run, clean, 0.141 CPU-hours skill=thesis-experiment-runner tier=mid
- results_analyst: status=idle last_unit=u17_module_d_report (Table Module D, re-derived by an independent verifier) skill=thesis-results-analyst tier=top
- writer: status=idle last_unit=u19g_g7_fix2 skill=thesis-writer tier=mid (writers A and B)
- critic: status=idle last_unit=u16_s9_critic cycle=3 consensus=needs_revision, fixed as revision cycle 3 and verified by G7 approve; budget stop Q14 skill=thesis-critic
- blind_examiner: status=idle last_unit=u17_s10_blind_review avg_rating=5.5 (seat A opus 5, seat B sonnet 6) decision=borderline calibration_gap=none G9 pass at threshold skill=thesis-blind-examiner
- defense_coach: status=running unit=u18_s11_defense_prep mode=mock n=1 skill=thesis-defense-coach tier=mid (one-shot per call)

## findings
- key_findings: C1 met on the warm slice: hybrid median Precision@10 0.1720 beats CBF by a median +31.20% (16 of 22 presentations, exact paired Wilcoxon p=0.005929, p_holm=0.011857) and beats ItemKNN-CF by a median +10.68% (17 of 22, p=0.014095, p_holm=0.014095), n=22, criteria_verdicts.json#C1 and thesis/tables/table_5_1_warm_slice.md; the vs-CF conjunct clears its pre-registered +10% threshold by only 0.68 percentage points | C2 and C3 both not met through the same conjunct: on the cold-start-refit slice (A|2) the hybrid beats ItemKNN-CF by a median +7.32% (18 wins, 1 tie, 3 losses, p_holm=0.000241) but loses to CBF by a median -30.28% (2 wins, 20 losses, p_holm=0.000241), and C2 requires both baselines, so it fails on the threshold rather than on significance; C3's ge_cbf holds in only 2 of 22 presentations while gt_mostpop, empty_lists==0 and coverage@10>=10% each hold in 22 of 22, criteria_verdicts.json#C2 and #C3. Read against the Random floor (F17, exploratory, thesis/tables/table_5_5_random_floor.md): on that slice only CBF clearly beats chance (median +0.0310 over Random, 16 of 22, p=0.003671), the hybrid is indistinguishable from it (10 of 22, p=0.750), and CF sits below it (6 of 22), so the surviving half of C2, beating CF on cold start, is a low bar, and C3's gt_mostpop conjunct is a weak floor because MostPop sits a median 0.0264 below Random itself (3 of 22). No verdict changes; Random decides no criterion. | the corrected cold-start condition inverts the phase 1 pilot exactly: on its own cold-start condition the pilot beat CBF in 22 of 22 by a median +73.12% (range +13.55% to +163.85%) and lost to CF in 22 of 22 by a median -17.90%, whereas the receipted refit run has the hybrid losing to CBF in 20 of 22 and beating CF in 18 of 22; C6 reproduced all 6 pilot values bit-identically (max_abs_diff 0.0), so the pattern was an artifact of the condition, not of the code. Correction E1 (decisions.log 2026-09-24): the +190% previously recorded is the pilot's WARM gain over CBF (median +189.54%, range +60.04% to +464.55%), not a cold-start figure; recomputed from inputs/prior_evidence/all_modules_metrics.json | diagnostic D1 (post-hoc, decides no criterion) answers plan.md's pre-registered alpha-near-1 risk in the negative: over 5,444 cold-start learner records the fitted weight on the collaborative component has median 0.5150, quartiles 0.4019 and 0.6181, with 0.04% at or above 0.9 and 83.9% between 0.3 and 0.7; CBF is the stronger cold-start component in 20 of 22 presentations yet the blend gives a median 0.494 weight to the weaker CF component there, and the hybrid lands between its own two components in 19 of 22 against above both in 11 of 22 on warm -- a correlate and a reading, not a confirmed mechanism, and the previous cycle's label-collapse explanation is withdrawn because the drop share correlates positively with the cold-start gain (Spearman +0.434, p=0.0435, n=22, wrong sign), thesis/tables/table_5_4_diagnostics.md and thesis/figures/figure_5_3_alpha_distribution.png | diagnostic D2 (post-hoc, decides no criterion) measures the blend's use of behavioural features, not a behavioural recommender component: removing n_visible, log1p_visible_clicks and n_active_days from the blend's feature set costs a median 0.001088 Precision@10 on warm users (-0.65% relative, rank-biserial -0.706, lower in 15 of 22, p=0.003279) and nothing detectable on cold start (median -0.000141, -0.33%, rank-biserial -0.114, p=0.674); both are small against the gaps the criteria turn on (+0.0412 warm, -0.0219 cold) and neither supports or refutes the hypothesis's behavioural-signal clause, which remains unchecked
- next_focus: none
- stop_reason: the phase 2 main experiment and the two human-approved post-hoc diagnostics are complete and receipted, all six pre-registered criteria are judged and neither diagnostic decides one, so the empirical work has reached a terminal partial result -- the warm-user half of the hypothesis is supported (C1 met) while the cold-start half is refuted against content-based filtering and upheld only against collaborative filtering (C2 and C3 not met), with C4, C5 and C6 met, and plan.md holds no further experimental phase to reach.
- phase_2_skipped_reason: none
## human decisions
- blind review package language: English
- blind rating threshold: 5.5 of 10, confirmed
- user interface and deep models (RNN, CNN, RBFNN): scope-outs, deferred; chapter 1 states them with the reason, chapter 6 lists them as future work
- cold-start measurement (Q1): report both conditions, the refit condition primary and deciding C2, the pilot's thin-history condition kept and labelled optimistic
- dwell time (Q2): click volume, active days and click sequence as a recorded scope reduction; hypothesis frozen
- still open: student-count fix on the Control Room page (Q3), university regulations, OQ6 whether C3's accuracy conjuncts stay per-presentation, university regulations, supervisor sight of the five proposal-vs-paper discrepancies (F1)

## corrections carried in
- The pilot summary claims the hybrid wins cold start 22 of 22. That holds against content-based filtering only; against collaborative filtering it loses 22 of 22, median -17.9 percent.
- The pilot summary says the hybrid never beats pure CF on warm users; it does in 3 of 22, by at most 0.9 percent.
- The pilot summary's limitations section still says one presentation was tested.
- The Thesis Control Room artifact repeats the cold-start framing and states 32,594 students; the tables hold 32,593.
- The hypothesis names dwell time, which OULAD does not record.

## artifacts
- idea: idea.md (frozen), idea_provenance.json
- inputs: inputs/manifest.json (29 files hashed), inputs/prior_evidence/ (pilot summary and metrics)
- plan: plan.md (revision 0, 199 lines, 6 binary criteria, 5 modules)
- literature: ledger 39 rows (37 verified, 2 unverified), 14 unreachable logged, references.bib, search_log.md, thesis/ch02.md
- methodology: protocol.md (approved at G3 cycle 3), threats_to_validity.md, data_statement.md, thesis/ch03.md; OULAD licence CC BY 4.0 verified via the authors' deposit
- code: complete, revision 3 plus diagnostics (alpha logging, behaviour ablation), approved at G4 and G4-lite
- results: results/summary.md and both receipts written; final verdicts C1 met, C2 not met, C3 not met (2 of 22 pass all conjuncts), C4 met, C5 met (combined), C6 met; key finding is the corrected cold-start condition inverting which baseline the hybrid struggles against
- thesis: ch01 to ch06 and front_matter.md written; claim_ledger.csv about 570 rows, checker PASS; G7 passed for ch01-03 (cycle 2) and ch04-06; Module D added after G7 and awaiting a G7 re-pass; tables in thesis/tables, figures in thesis/figures
- defense: defense/question_bank.md (61 questions, 10 categories, checker bank checks PASS); mocks, corrections, slides outline pending

## recent_events
- 2026-09-20 | S0 | event=project_opened | project_root=data/projects/e_learning_thesis
- 2026-09-20 | S0 | event=idea_frozen | binding=918162da54511db3 sha256=8be52b93fc723207
- 2026-09-20 | S0 | event=inputs_hashed | count=29 missing_for_human=2

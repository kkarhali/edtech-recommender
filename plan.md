---
project_id: e_learning_thesis
phase: 2
plan_revision: 0
experiment_stage: main
status: ready
hypothesis: "A hybrid recommender that combines (a) content-based filtering over course/content metadata, (b) collaborative filtering over learner-content interaction history, and (c) a behavioral session signal (browsing sequence, dwell time, engagement pattern, as used for student profiling in the reviewed literature) will produce more accurate and more robust recommendations for e-learning content than either content-based or collaborative filtering alone, and will specifically outperform them on cold-start learners (users with very little interaction history), which the reviewed hybrid baselines identify as the main failure mode of single-technique approaches."
success_criteria:
  - id: C1
    kind: primary
    metric: "Precision@10 relative gain, hybrid vs. content-based-only AND hybrid vs. collaborative-only, warm-user held-out slice"
    threshold: ">= +0.10 relative against BOTH baselines, median over the 22 module-presentations, AND paired Wilcoxon signed-rank p < 0.05 after Holm correction for both comparisons"
    on_dataset: "OULAD, all 22 module-presentations, time-based split, identical splits for all four models"
    why: "idea.md criterion 1, carried unchanged; the hybrid must beat the stronger baseline, not only the weaker one (prior evidence: 0 of 22 pass, median -2.7% vs. CF)"
  - id: C2
    kind: primary
    metric: "Precision@10 relative gain, hybrid vs. collaborative-only AND hybrid vs. content-based-only, cold-start slice built by refitting the similarity model without the held-out learners"
    threshold: "> 0 relative against BOTH baselines, median over the 22 module-presentations, AND paired Wilcoxon signed-rank p < 0.05 after Holm correction for both comparisons"
    on_dataset: "OULAD, all 22 module-presentations, cold-start-refit condition, identical splits for all four models"
    why: "the hypothesis claims cold-start superiority over BOTH baselines; the pilot's criterion 2 compared against content-based filtering only, and prior evidence shows the hybrid losing to collaborative filtering on cold start in 22 of 22 presentations (median -17.9%, range -29.1% to -10.0%). This is the criterion that can refute the hypothesis."
  - id: C3
    kind: primary
    metric: "Cold-start Precision@10, hybrid vs. content-based-only and vs. a global-popularity baseline; non-degeneracy of the hybrid's top-10 lists"
    threshold: ">= content-based-only Precision@10 AND > popularity-baseline Precision@10 AND == 0 empty top-10 lists AND >= 10% of available items appearing across the slice's top-10 lists, in each of the 22 module-presentations"
    on_dataset: "OULAD, all 22 module-presentations, cold-start-refit condition"
    why: "idea.md criterion 2 verbatim, including its popularity-fallback clause, which the pilot could never judge because no popularity baseline was built (rule 6: an unbuilt comparison is unchecked, never passed)"
  - id: C4
    kind: anti-cheating
    metric: "Tuning-on-test leakage count: rows shared between the validation split and the test split, and hyperparameters (blend weight, K, similarity cut-off) fitted on any data other than the validation split"
    threshold: "== 0 shared rows AND == 0 hyperparameters fitted outside the validation split; the test split is scored exactly once per model per module-presentation"
    on_dataset: "OULAD, all 22 module-presentations"
    why: "the pilot's blend weight was hand-picked after test results were seen; a learned weight is evidence only if it never saw the test slice. Asserted in code and reported in the run receipt."
  - id: C5
    kind: feasibility
    metric: "Wall-clock time and hardware for the phase 2 main run and for the phase 1 reproduction"
    threshold: "<= 4.0 CPU-hours total for the main run over all 22 module-presentations AND <= 15 minutes for the phase 1 reproduction, on a single CPU with no GPU and no downloaded model weights"
    on_dataset: "OULAD, all 22 module-presentations"
    why: "idea.md criterion 3 and its compute/time constraints; keeps the design inside the stated hardware instead of buying a result with compute"
  - id: C6
    kind: anti-cheating
    metric: "Absolute difference between the reproduced phase 1 Precision@10 values and the recorded prior-evidence values, all three models, warm and cold-start, on EEE_2014J"
    threshold: "<= 1e-6 absolute for every one of the 6 values, with a run receipt carrying the SHA256 of the regenerated metrics file and the exact command line"
    on_dataset: "OULAD, module-presentation EEE_2014J, seed 42, deterministic selection rule"
    why: "the phase 1 pilot ran outside any engine and has no receipts, so under rule 7 it is prior evidence, not completed work; nothing in the thesis may cite it until it is reproduced under a receipt (about 3 minutes of CPU, so cost is no reason to skip it)"
---

# Hypothesis

A hybrid recommender that combines (a) content-based filtering over course/content metadata,
(b) collaborative filtering over learner-content interaction history, and (c) a behavioral
session signal (browsing sequence, dwell time, engagement pattern, as used for student
profiling in the reviewed literature) will produce more accurate and more robust
recommendations for e-learning content than either content-based or collaborative filtering
alone, and will specifically outperform them on cold-start learners (users with very little
interaction history), which the reviewed hybrid baselines identify as the main failure mode of
single-technique approaches.

The hypothesis is frozen (`idea.md`, binding `918162da54511db3`) and is not weakened here. It is
refutable in exactly the terms of C1 and C2: if the hybrid does not beat both baselines by
>= 10% relative on warm users, or does not beat both on new learners, it is not supported.

**Scope reduction, recorded and not substituted.** The hypothesis names dwell time. OULAD records
only `date` (a day offset) and `sum_click` per learner, resource and day, and holds no dwell or
session-duration field, so the behavioural signal is operationalised by the proxy *(click volume
per learner-item, active-day count, day-ordered sequence)*. This reduces the signal's richness,
is repeated in chapters 3 and 6, and is never called dwell time.

# Data

OULAD (Open University Learning Analytics Dataset), the eight tables hashed in
`inputs/manifest.json`. **Licence: `unverified`** — the licence text is a recorded missing input
owned by the human candidate; chapter 3 must quote it, and no redistribution of OULAD happens
here. **Population limitation:** OULAD is a UK Open University cohort (32,593 rows in
`studentInfo.csv`), not the candidate's institution. Replication unit: the 22 presentations.

# Research Questions

- **RQ0 (main):** Does a hybrid of content-based filtering, collaborative filtering and a
  behavioural engagement signal produce more accurate and more robust top-K e-learning
  recommendations than either alone, and on cold-start learners? Modules B, C; C1-C3; chapter 5.
- **RQ1 (sub-objective 1, behaviour analysis):** Which observable VLE behaviours (click volume,
  active-day count, day-ordered sequence, activity type) separate learners well enough to carry
  recommendation signal? Answered by Module D, chapters 3 and 5.
- **RQ2 (sub-objective 2, data-analysis models):** Does segmenting learners by behavioural
  profile (clustering over the Module D features) improve the cold-start prior over a
  non-segmented hybrid? Answered by Module D feeding Module B, chapters 4 and 5.
- **RQ3 (sub-objective 3, recommendation model):** Does a blend weight learned on a validation
  split close the warm-user gap to pure collaborative filtering that the pilot's hand-picked
  weight left open (median -2.7%)? Answered by Module B, criterion C1, chapter 4.
- **RQ4 (sub-objective 4, evaluation and improvement):** Under a time-based split and a genuine
  new-learner condition, does the hybrid's advantage survive significance testing across the 22
  module presentations? Answered by Module C, criteria C2 and C3, chapter 5.

# Proposal Traceability

| Proposal sub-objective | Question / module in this plan | Status |
| --- | --- | --- |
| 1. User behaviour analysis | RQ1 / Module D | in scope |
| 2. Data-analysis models (classification, clustering, prediction) | RQ2 / Module D into Module B | in scope, limited to clustering and the learned blend weight; no deep model in phase 2 |
| 3. Development of the recommendation model | RQ0, RQ3 / Modules B, R | in scope |
| 4. Performance evaluation and improvement | RQ4 / Module C | in scope |
| User-friendly interface and related software | none | **out of scope — open question 1 for the human**; no module here builds an interface, and dropping it needs the supervisor's sign-off |
| Proposed technologies: TensorFlow / Keras deep models (RNN, CNN, RBFNN) | none in phase 2 | **out of scope for this phase**; idea.md reserves deep learning for a later phase and C5 bounds compute to a single CPU. Reported as a limitation, not silently omitted. |

Open questions for the human: (1) is the promised interface in scope or formally dropped;
(2) university thesis regulations (format, language, citation style) are not in the repository,
so nothing here assumes a page limit or section order; (3) the OULAD licence text is still
missing and blocks chapter 3's data statement.

# Modules

## Module R -- phase 1 reproduction under a receipt
- file_scope: ["code/reproduce_phase1.py"]; depends_on: []; chapter: 4, 5
- task: "Re-run the phase 1 pipeline on EEE_2014J with seed 42 and the same deterministic rule,
  regenerate the metrics file, and emit a receipt with real SHA256 hashes and the command line."

## Module A -- data preparation, time-based split, cold-start refit
- file_scope: ["code/*: load_data, build_time_split, build_engagement_matrix, build_coldstart_folds"]; depends_on: [Module R]; chapter: 3, 4
- task: "Load OULAD, build the behavioural feature set from `sum_click` and `date`, cut a
  time-based train/validation/test split per module-presentation by the `date` column, and build
  a cold-start condition whose similarity model is refitted with the held-out learners' rows
  removed from the matrix itself, not hidden at scoring time."

## Module B -- four models on identical splits
- file_scope: ["code/*: ContentBased, CollaborativeFiltering, PopularityBaseline, Hybrid"]; depends_on: [Module A]; chapter: 4
- task: "Implement content-based, item-item collaborative, global-popularity and hybrid models,
  the hybrid's blend weight fitted by logistic regression over visible-item count and per-model
  confidence on the validation split only, replacing `alpha = min(0.9, 0.2 + 0.05 * n_visible)`."

## Module C -- evaluation and significance
- file_scope: ["code/*: evaluate, significance, main"]; depends_on: [Module B]; chapter: 5
- task: "Score Precision@10 for all four models on the warm and cold-start-refit slices of all 22
  module presentations, run the paired Wilcoxon tests with Holm correction named in C1 to C3, and
  write `results/summary.md` against every criterion, met or not, with numbers and likely cause."

## Module D -- behaviour analysis and learner segmentation
- file_scope: ["code/*: behaviour_features, segment_learners"]; depends_on: [Module A]; chapter: 3, 5
- task: "Describe the behavioural feature distributions per module presentation and cluster
  learners on them, supplying Module B's cold-start prior and answering RQ1 and RQ2."

# Risks & Falsifiability

- **The decisive one.** If the hybrid's cold-start Precision@10 does not exceed *collaborative
  filtering's* on the refit cold-start slice (median relative gain <= 0 across the 22
  presentations, or a Holm-corrected paired p >= 0.05), the hypothesis's cold-start claim is
  refuted, whatever the content-based comparison says. Prior evidence points this way: hybrid
  vs. CF on cold start was negative in 22 of 22 presentations, median -17.9%.
- If the hybrid's warm-user Precision@10 does not exceed *both* baselines by >= 10% relative
  (C1), criterion 1 is not met; report the actual numbers, the gap and the most likely cause —
  never move the threshold. Prior evidence: 0 of 22 pass, median -2.7% vs. CF, best +0.9%.
- If hybrid cold-start Precision@10 does not exceed the *popularity* baseline's (C3), the
  "principled fallback" half of the hypothesis is falsified even if it still beats CBF.
- If the learned blend weight converges on alpha close to 1 wherever it helps, the content and
  behavioural components carry no usable marginal signal here, refuting "combining is better".
- If the reproduction (C6) misses the recorded phase 1 numbers by more than 1e-6, the prior
  evidence is unreliable and every claim resting on it is withdrawn until re-measured.

# Budget

```
max_runs: 3 (one reproduction, one main run over 22 presentations, one re-run reserved for a
         named mechanism fix; further knob-turning is forbidden by rule 3)
max_revisions: 3
max_cpu_hours: 4.0 total for the main run, <= 0.25 for the reproduction
max_gpu_hours: 0 (single CPU assumed; no GPU, no multi-GPU cluster)
seeds: 42 for every stochastic step; every seed and every run is reported, not the best
network: none required — the OULAD tables are already downloaded and hashed in
         inputs/manifest.json; no model weights or pretrained checkpoints are downloaded
read_only: src/reasearch_topic/References/*.pdf and knowledge_base/ are background only
identical_splits: the content-based, collaborative, popularity and hybrid models are trained and
         evaluated on byte-identical splits in every comparison, per idea.md's constraint
criteria_frozen: the success_criteria block is a pre-registration; nothing in it moves once
         Module R starts. A change is a revise cycle with a `## Revision <N>` entry naming who
         asked and why, reported in the thesis as a deviation.
execution: the workflow engine cannot run on this Windows machine (it imports fcntl), so runs go
         directly through .venv-pilot\Scripts\python.exe with PYTHONDONTWRITEBYTECODE=1 and
         PYTHONUTF8=1, and the runner writes each receipt by hand with real file SHA256 hashes
         and the exact command line (recorded deviations D1 and D2).
scale_up_policy: if_pass, write chapters 4 to 6 from the receipted results; if_fail, report the
         negative result in full (rule 5) and take any deep-model phase 3 to the human.
```

# Phase 2 Scale-up Notes

Prior evidence this plan builds on (`inputs/prior_evidence/summary.md`,
`all_modules_metrics.json`, `pilot_metrics.json`; no receipts, so prior evidence under rule 7):
criterion 1 failed in 0 of 22 presentations (median -2.7% vs. CF, range -10.8% to +0.9%, the
hybrid winning in 3 of 22 by at most 0.9%); criterion 2 passed 22 of 22 against content-based
filtering only (median +190%), while the hybrid lost to collaborative filtering on cold start in
22 of 22 (median -17.9%); about 30 s per run on one CPU, 140 s for all 22.

The five named weaknesses this plan fixes, one mechanism each, named in advance per rule 3:
(1) a blend weight chosen after test results were seen, now fitted on a validation split (C4);
(2) no non-personalised popularity baseline, so criterion 2 could not be judged, now built in
Module B (C3); (3) a random per-learner split ignoring `date`, now time-based (Module A);
(4) a cold-start condition reusing a similarity matrix fitted on the learners it hid, now
refitted without them (Module A, C2); (5) no significance test, now paired Wilcoxon with Holm
correction across the 22 presentations (Module C). No phase 1 criterion is lowered; chapter 5
reports both phases.

---
blockers_count: 0
warnings_count: 2
files_reviewed: n/a (gate reviews idea.md and plan.md, not code)
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: claude-sonnet-5
model_identity: claude-sonnet-5, tier=mid for this dispatch. Independence from the plan's
  author is not assumed: decisions.log records that u03_s1_plan (plan.md) was dispatched to
  worker=research-planner tier=top (2026-09-20T13:25:00Z), that the first u04_g1_plan_gate
  attempt on tier=top failed with HTTP 429 (Fable out of credits), and that the manager then
  redispatched u04_g1_plan_gate to tier=mid specifically to keep the reviewer's identity
  distinct from the planner's (event=manager_decision id=M2, 2026-09-20T13:35:00Z;
  event=unit_redispatched, same timestamp). I am that tier=mid dispatch, so independence is
  verified from the project's own artifact, not assumed.
mode: plan_gate
unit: u04_g1_plan_gate
cycle: 0
---

# Review

**Deviation notice (per SKILL.md and rule 6):** the review MCP tool cannot run on this Windows
machine because its persistence step shells out to `ar-workflow-engine.py`, which imports
`fcntl`. This file was written by hand with `Write`, and the Constraint Audit below was
validated against `ar-review-contract.ts`'s rules manually rather than by the tool. This is a
recorded deviation, not a silently-passed check.

## Blockers (must fix before proceeding)
None.

## Warnings (should fix)
- [W1] <severity:low> `plan.md:26`: the `why` field for C3 says it carries "idea.md criterion 2
  verbatim, including its popularity-fallback clause." It does not. Idea.md's clause is a
  conditional ("must not simply fall back to global popularity ranking *without at least
  matching* the content-based-only baseline's Precision@10") with no numeric bar against
  popularity itself. Plan.md:24 operationalizes this into four conjuncts not literally present
  in idea.md: a strict `>` against a newly-built popularity baseline, `== 0` empty top-10 lists,
  `>= 10%` catalogue coverage, all required in **every one** of the 22 module-presentations. This
  is a defensible way to make an underspecified qualitative clause decidable (idea.md:18-25's
  criterion 2 literally could not be judged in phase 1 because no popularity baseline existed —
  confirmed independently: no "popular" string anywhere in `inputs/prior_evidence/*.json`
  or `summary.md`), but it should be described as an operationalization, not "verbatim" — a
  chapter-3 reader checking this sentence against idea.md word-for-word would not find it there.
- [W2] <severity:low> `plan.md:24-25` vs. `plan.md:14,18`: C3's aggregation is a zero-tolerance
  universal quantifier ("in each of the 22 module-presentations", no median, no significance
  test), while C1 and C2 use median-over-22 plus a Holm-corrected paired Wilcoxon test that
  tolerates per-presentation variance. This is an internal inconsistency in how strict the three
  primary criteria are: C3 can fail chapter 5 on the strength of one atypical presentation (for
  example one of the three module-presentations phase 1 found with a 100%-missing `week_from`/
  `week_to` field, per `inputs/prior_evidence/summary.md`'s "Generalization check" section) even
  if the hybrid clears the bar in 21 of 22, while an equally marginal C1/C2 result would still
  pass on its median. Not a hard-constraint violation, but recommend the methodologist reconcile
  the aggregation rule across C1-C3 in S3, or record the asymmetry as a deliberate, named choice.

## Constraint Audit
- [HC1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not
  assume a multi-GPU cluster." (`idea.md:47-48`) | status: satisfied | evidence: `plan.md:165`
  `max_gpu_hours: 0 (single CPU assumed; no GPU, no multi-GPU cluster)` | blocker: none
- [HC2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot."
  (`idea.md:56`) | status: satisfied | evidence: `plan.md:167-168` `network: none required ...
  no model weights or pretrained checkpoints are downloaded` | blocker: none
- [HC3] Network access limited to the one OULAD download (`idea.md:41-43,47`) | status:
  satisfied | evidence: `plan.md:167-168` states no further network is required because OULAD
  is already downloaded; independently confirmed `inputs/manifest.json` hashes 8 real OULAD
  files (`studentInfo.csv`, `studentVle.csv`, `vle.csv`, `courses.csv`, `studentRegistration.csv`,
  `assessments.csv`, `studentAssessment.csv`, `OULAD.names`) already on disk, so phase 2 needs
  zero additional network access, which is a stricter satisfaction than idea.md required |
  blocker: none
- [HC4] Pilot/time budget: "complete within a few hours of wall-clock time" (`idea.md:54-55`) |
  status: satisfied | evidence: `plan.md` frontmatter C5 (lines 33-38) sets `<= 4.0 CPU-hours`
  for the main run and `<= 15 minutes` for the phase 1 reproduction; independently verified
  against `inputs/prior_evidence/all_modules_metrics.json`'s `aggregate.elapsed_seconds = 140.1`
  for the full 22-presentation phase-1 pipeline (a materially simpler design with 3 models, no
  cold-start refit, no clustering, no significance test) — the 4.0-hour ceiling for the more
  complex phase-2 design (4 models, cold-start refit, Module D clustering, Wilcoxon+Holm) is
  generous headroom, not a contradiction of the recorded timing | blocker: none
- [HC5] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained
  and evaluated on identical splits" (`idea.md:57-58`) | status: satisfied | evidence:
  `plan.md:170-171` `identical_splits: the content-based, collaborative, popularity and hybrid
  models are trained and evaluated on byte-identical splits in every comparison`, backed by
  Module A (`plan.md:117-122`, builds one split per module-presentation) feeding Module B
  (`plan.md:124-128`, all four models). The plan extends the constraint to the added popularity
  model rather than weakening it. This is a design-level commitment, appropriate for a plan
  gate; `code_gate` must re-trace the actual call chain (per the reviewer's step 3) to confirm no
  model receives a differently-built split before it is treated as satisfied there too |
  blocker: none
- [HC6] "Treat `src/reasearch_topic/References/*.pdf` and this idea file's cited papers as
  read-only background; do not attempt to re-scrape or redistribute their content."
  (`idea.md:59-60`) | status: satisfied | evidence: `plan.md:169` `read_only:
  src/reasearch_topic/References/*.pdf and knowledge_base/ are background only` | blocker: none
- [HC7] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the
  most likely cause ... rather than adjusting the threshold after the fact." (`idea.md:28-30`,
  rule 3) | status: satisfied | evidence: `plan.md:172-174` `criteria_frozen: ... nothing in it
  moves once Module R starts. A change is a revise cycle with a "## Revision <N>" entry naming
  who asked and why`; Module C's task (`plan.md:130-134`) requires `results/summary.md` to
  report "every criterion, met or not, with numbers and likely cause" | blocker: none

## Notes
- Independently recomputed the cold-start hybrid-vs-CF relative gain from
  `inputs/prior_evidence/all_modules_metrics.json`'s raw per-presentation Precision@10 values
  (not just the aggregate file): 22 of 22 negative, median -17.90%, range -29.12% to -10.03%.
  This matches plan.md's Risks & Falsifiability section and C2's `why` field exactly, so the
  plan's single most consequential empirical claim is artifact-backed, not asserted.
- Independently read `data/projects/e_learning_pilot/code/pilot_recommender.py`: `main()`
  (line 237) builds the engagement/similarity matrix once from every user's full train-split
  history and reuses it unchanged for the cold-start evaluation call at line 241. This confirms
  the leakage bug SKILL.md's project-context section flags, and confirms Module A's planned fix
  ("similarity model is refitted with the held-out learners' rows removed from the matrix
  itself, not hidden at scoring time", `plan.md:120-122`) targets a real, previously-diagnosed
  mechanism rather than an invented one, satisfying rule 3's "mechanism named in advance."
- `idea_provenance.json`'s recorded `idea_sha256`/`binding_sha256` do not match a fresh SHA256 of
  the on-disk `data/projects/e_learning_thesis/idea.md` (4566 bytes) — but they match exactly
  once CRLF is normalized to LF (4506 bytes), and match `data/ideas/e_learning_recommendation_system.txt`
  byte-for-byte. This is a Windows checkout line-ending artifact, not content drift: the frozen
  hypothesis is unchanged. Flagging for the human/coordinator because any automated re-check of
  this binding on Windows needs to normalize line endings first, or it will misreport an
  untouched idea file as changed.
- `plan.md` is 199 lines, one under the 200-line ceiling.

## Overall
Approve. Every hard constraint in `idea.md` is carried into `plan.md`'s Budget or Modules and is
`satisfied` with file:line evidence, several independently cross-checked against
`inputs/prior_evidence/` and the pilot's own code rather than taken on the plan's word. All six
success criteria are binary and decidable, and the plan directly repairs the five weaknesses the
pilot named in advance (rule 3), including widening C2 to cover collaborative filtering as well
as content-based filtering — the exact narrowing the lessons-learned record warns is a plan-gate
finding, and it is already fixed here rather than left for chapter 5 to discover. The two
warnings (C3's "verbatim" overclaim, and its zero-tolerance aggregation inconsistent with C1/C2's
median-plus-significance approach) are should-fix documentation/design-consistency issues, not
hard-constraint violations or undecidable thresholds, so they do not block G1. This would change
to `revise` if the methodologist's later protocol silently drops the identical-splits commitment,
or if C3's aggregation rule is not reconciled before chapter 5 relies on it.

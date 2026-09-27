---
blockers_count: 0
warnings_count: 6
files_reviewed: 3 chapters (ch04.md, ch05.md, ch06.md) plus 5 tables, 1 caption file, 3 figures and 298 claim-ledger rows
reviewer: manual (project engine unavailable on Windows; ar-workflow-engine.py imports fcntl — see thesis-reviewer SKILL.md)
model: Claude Opus 5
model_identity: claude-opus-5 (reviewer seat, top tier). Independence verified from the project's
  own record, not assumed: decisions.log 2026-09-24T06:53:40Z dispatches u15_g7_chapter_gate to
  "two independent reviewers, chapters 1 to 3 and chapters 4 to 6, different model identity from
  the sonnet writers"; ch04/ch05/ch06 were produced by the mid-tier sonnet Thesis Writer seats
  (writer_A, writer_B) recorded at decisions.log 2026-09-24T06:34:08Z and 06:53:40Z. I produced
  none of the artifacts under review.
mode: chapter_gate
unit: u15_g7_chapter_gate
cycle: 0
scope: chapters 4, 5 and 6 only. Chapters 1 to 3 are the parallel reviewer's unit
  (reviews/chapter_gate_ch01_03.md, verdict revise, 3 blockers); nothing in that file was read,
  written or relied on except its existence as recorded in decisions.log.
verdict: approve_with_warnings
---

# Review — G7 chapter gate, chapters 4 to 6

**Manual-write deviation, stated once as rule 6 requires.** The Bun review MCP tool
(`ar-gemini-review-mcp.ts`) shells out to `ar-workflow-engine.py`, which imports `fcntl` and
cannot run on this Windows machine, so no tool injected this file's model identity, bound it to
its unit and cycle, or validated its Constraint Audit before it landed on disk. I ran that
validation on my own draft instead. The absence of the automated check is `unchecked`, not
`passed`, and the coordinator's decision log should carry it.

**What I did.** I recomputed every table number in chapters 4 to 6 from the receipted
per-presentation artifacts rather than from any summary prose: all 22 rows and 12 columns of
Tables 5.1 and 5.2, every distribution row, every relative-gain row, every win/tie/loss count, all
eight exact paired Wilcoxon tests with their Holm corrections and rank-biserial effect sizes, the
sign tests, the C3 conjunct table, Table 5.5's ten random-floor tests, both D1 and D2 tables, the
per-module breakdown, the sensitivity grid and the P4b union. I re-hashed all 44 distinct ledger
artifacts, all 99 receipted artifact files across the three receipts, both code-tree hashes, the
configuration hash, all three execution-event hashes (recomputed from the receipts' own fields in
the key order chapter 4 documents), and `results/run.log` whole-file and prefix. I parsed the
10,257,030-byte prefix of `results/run.log` for the assertion counts chapter 4 quotes. I
recomputed the phase 1 pilot's 22-presentation aggregates from
`inputs/prior_evidence/all_modules_metrics.json`. Every recomputation is reported below with what
it produced.

## Blockers (must fix before proceeding)

None.

No number, count, p-value, hash, verdict or direction of comparison in chapters 4, 5 or 6 failed
to reproduce from the artifact it cites. The four corrected facts the dispatch named are carried
correctly in every place they appear.

## Warnings (should fix)

- [W1] <severity:med> `thesis/ch05.md`:5.4, the paragraph beginning "Because criterion C2 requires
  the hybrid to beat **both** baselines": the sentence "C3 fails through the same comparison in
  per-presentation form, passing all four conjuncts in only 2 of 22 presentations." carries no
  ledger id, and no other marker appears in that paragraph. The standards' writing rule is "use
  the ledger id in a hidden comment next to each quantitative sentence". The number itself is
  ledgered twice elsewhere (C5.28, C5.41) and I verified it (`ge_cbf` true for CCC_2014J and
  DDD_2013B only, 2 of 22), so rule 2 holds in substance; this is the only unmarked quantitative
  sentence I found in the three chapters. Add the marker rather than the number.
- [W2] <severity:med> `thesis/figures/captions.md`, Figure 5.1 caption, last sentence: "the
  evaluated warm learners are highly active (EEE_2014J median 49 distinct resources of a 115-item
  catalogue, mean 44.8, counted from `studentVle.csv`)". The artifact attributes 49 / 44.8 to the
  **log-present** learners (1,097), not the **evaluated** ones:
  `methodology/threats_to_validity.md` T16 reads "the log-present learners holding a mean of 44.8
  and a median of 49 distinct resources", and the evaluated cohort in
  `results_EEE_2014J.json#behaviour` (n_learners 1018) has median 50.0 and mean 45.971. Chapter 5
  words it correctly (C5.10, "the learners present in the log hold a median of 49"); the caption
  does not. This is checklist item 15's only failure and it is in the caption, not the chapter.
- [W3] <severity:low> `thesis/ch04.md`:3 names `thesis/claim_ledger_A.csv` as "the ledger for
  chapters 1 and 4" and `thesis/ch05.md`:7 names `thesis/claim_ledger_B.csv` for chapters 5 and 6,
  while the authoritative merged ledger is `thesis/claim_ledger.csv`. I confirmed the merge is
  faithful — 140 + 158 = 298 rows, no id appears in both halves, and zero of the 298 rows differ in
  claim, artifact, sha256 or status between the split file and the merged one — so no claim is
  affected. A reader following either chapter header nonetheless reaches a file that is not the
  one the gate treats as the ledger.
- [W4] <severity:low> `thesis/claim_ledger.csv`, row C6.23 (status `partial`) describes the
  hybrid-versus-Random cold-start comparison as "an untested comparison". Its own artifact tests
  it: `thesis/tables/table_5_5_random_floor.md` reports an exact paired Wilcoxon, W = 116.0,
  p = 0.750238, n_eff = 22, which I reproduced exactly, and `thesis/ch06.md`:6.4 quotes that
  p-value. The chapter text is right and the row understates it; the row should say
  "indistinguishable from the floor (p = 0.750238)" rather than "untested".
- [W5] <severity:low> `thesis/ch05.md`: six tables carry no number or caption — the C3 conjunct
  table (5.3.1), the per-module table (5.6.1), the sensitivity table (5.6.2), the D1 alpha table
  and the D2 warm and cold tables (5.8.1, 5.8.2) and the correlation table (5.8.3) — while
  Tables 5.1 to 5.5 are numbered and captioned. Each is introduced in the text before it appears,
  so the writing rule is met, but the list of tables at assembly will not be able to include them.
- [W6] <severity:low> `thesis/ch05.md` discloses the two code trees (C5.73) but not that the main
  receipt's `run_log_after_sha256` is a prefix hash. `thesis/ch04.md`:4.6.6 carries that disclosure
  in full (C4.81, C4.82) and chapter 5 defers the execution record to chapter 4, so this is not a
  chapter 5 defect on its own. It is flagged because the parallel ch01–03 review made the same
  omission a blocker for chapter 3 (decisions.log 2026-09-24T13:01:46Z, B3): the assembly
  consistency sweep should confirm the thesis states it once, clearly, where a reader who re-hashes
  will meet it.

## Constraint Audit

Hard constraints quoted from `data/projects/e_learning_thesis/idea.md`, audited as chapters 4 to 6
carry them.

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not
  assume a multi-GPU cluster." | status: satisfied | evidence: `results/run_receipts/u11_s5_run_main.json`
  `hardware` = "Intel64 Family 6 Model 158 Stepping 13, GenuineIntel, 12 logical cores, no GPU";
  `process_cpu_seconds` 2,798.41 below `wall_clock_seconds` 3,769.12, which is consistent with an
  effectively single-threaded main process. `thesis/ch04.md`:4.6.4 states exactly this and no more:
  "This thesis reads 'single CPU' as one machine, one main process and no GPU, and it says that the
  receipts cannot show more than that." That reading matches `decisions.log` item I3 verbatim,
  which asked the reviewer to confirm it; I confirm it. The chapter does not claim a processor
  affinity or thread count the receipts do not record. | blocker: none
- [C2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." |
  status: satisfied | evidence: `thesis/ch04.md`:4.2 Table 4.1 records TensorFlow, Keras, Random
  Forest and deep neural networks as **not used** and §4.6.4 "Every stage ran without a GPU and
  without downloaded weights" (C4.3); the run manifest's library block is numpy 2.5.3, pandas
  3.0.5, scikit_learn 1.9.1, scipy 1.18.1 and nothing else, which I read from
  `results/run_artifacts/u11_s5_run_main/run_manifest.json`. | blocker: none
- [C3] "requires network access during the pilot to download OULAD once (a few hundred MB)" —
  network limited to that one download | status: satisfied | evidence: `thesis/ch04.md`:4.2 "The
  code makes no network call" (C4.95) and §4.8 "no network access is needed at run time" (C4.2);
  `code/data.py`:26-39 reads the tables from the local `raw_dir` and raises `DataIntegrityError`
  unless each file's SHA256 and byte size match `inputs/manifest.json` (C4.1), and the run log's
  `data_sha256` events record `manifest_match: true` for every file read. | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits so the comparison in success criterion 1 is fair." | status:
  satisfied | evidence: Tables 5.1 and 5.2 are headed "identical splits for all six models" and
  every model in each table is read from the same cell key of the same
  `results_<pres>.json#splits.primary.cells[...]`, which I confirmed cell by cell for all 22
  presentations; `foundation_<pres>.json#split_sha256` records one train/val/test hash triple per
  presentation shared by every model; criterion C4's measured leakage counts are 0 shared rows
  across all three split pairs (`criteria_verdicts.json#C4`, quoted at C4.77 and C5.42). | blocker: none
- [C5] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware" — the compute and time budget | status: satisfied | evidence: C5 met on both conjuncts,
  1.0140 CPU-hours against 4.0 for the main run and 0.238 minutes against 15 for the reproduction
  (`criteria_verdicts.json#C5` main and pilot); `thesis/ch04.md`:4.6.4 and `thesis/ch05.md`:5.5
  both state that the combination was made by hand from two receipts and that each stage's own
  file correctly reads `not met (unchecked conjunct)` in isolation, which is the honest form of
  this pass, not a softening of it. | blocker: none
- [C6] "no threshold moved after a run" (plan.md `criteria_frozen`; idea.md criterion 4) | status:
  satisfied | evidence: `plan.md` hashes today to
  `22bb14a20fe7f111bf342aec51a54b7a3b6daf6c8723e1b5d66120d8d8e462d0`, which is the value recorded
  in `methodology/protocol.md`'s header ("Plan hash: SHA256 `22bb14a2...`, `plan.md`, 15,766
  bytes"), so the pre-registration is byte-identical to the one the run was gated against (C4.36);
  the `metric`, `threshold` and `on_dataset` strings in
  `results/run_artifacts/u11_s5_run_main/criteria_verdicts.json#C1..C5` are character-identical to
  `plan.md`'s `success_criteria` block, and Table 5.3 reproduces them without dropping a conjunct.
  `thesis/ch05.md`:5.5 additionally discloses, rather than quietly fixing, that C3 is an
  *operationalisation* of idea.md's second criterion and not the verbatim carry-over `plan.md`'s
  `why` field calls it, and states that `plan.md` is not edited and no threshold moves (C5.46). |
  blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background; do not attempt to re-scrape or redistribute their content." | status: satisfied |
  evidence: chapters 4 to 6 take no number from a reference PDF; §5.9's literature comparison
  quotes reported figures with their own task labels and attributes them to chapter 2's ledger, and
  no chapter reproduces source content. No file under `src/reasearch_topic/` is written by any
  artifact of this unit. | blocker: none

## Per-checklist-item verdicts

**(1) Every number and claim has a ledger id and the artifact supports it — PASS (one warning).**
ch04 carries 121 hidden markers over 109 distinct ids; ch05 129 over 116; ch06 44 over 43. Every
one of those 268 distinct ids exists in `thesis/claim_ledger.csv`, and every one of the 108 `C4.*`,
116 `C5.*` and 42 `C6.*` ledger rows is cited in its chapter — no orphan ids in either direction.
I re-hashed all 44 distinct artifacts the 298 rows cite: 43 match exactly. The only mismatch is
`decisions.log` (18 rows, ledger `65295f60...`, actual `88fe2e35...`), which is open item I5 and
excluded by the dispatch. The single unmarked quantitative sentence is W1.

**(2) Hypothesis and criteria C1–C6 are as in plan.md, none moved after results — PASS.** See
Constraint Audit [C6]: plan.md's hash equals the protocol header's recorded value, the criterion
strings in the receipted verdict files are character-identical to plan.md's frozen block, and
Table 5.3 reproduces each threshold with all conjuncts intact. C3's status as an operationalisation
rather than a verbatim carry-over is disclosed in the chapter (C5.46) instead of being repaired by
editing the frozen file.

**(3) Verdicts C1 met, C2 and C3 not met, C4 C5 C6 met, no softening or inflation, chapter 6 agrees
with chapter 5 — PASS.** The receipted files read C1 met, C2 not met, C3 not met, C4 met, C5 "not
met (unchecked conjunct)" per stage, C6 met (pilot) / unchecked (main); the diagnostics stage reads
`unchecked` for all six. ch05 §5.5 and ch06 §6.3 report exactly that, with C5 combined by hand and
the isolation caveat stated. I grepped all three chapters for "partially met", "nearly met",
"almost met", "marginally", "essentially/broadly/effectively met": zero hits. Chapter 6 introduces
no number chapter 5 does not establish; its strongest-looking independent phrase, "covers at least
12% of the catalogue in every presentation" (C6.4), is supported by the minimum coverage I
recomputed, 0.12149532710280374 at BBB_2013J, and is a tighter true bound than C3's 10% floor.
Chapter 6 §6.3 explicitly carries "upheld" at reduced weight because the baseline it is upheld
against sits below the random floor.

**(4) The corrected facts — PASS, all four recomputed from
`inputs/prior_evidence/all_modules_metrics.json#per_module_presentation`.** Pilot cold-start
hybrid-vs-CBF: median **+73.12%**, range **+13.55% to +163.85%**, 22 wins of 22 — matches C4.16,
C5.32, table_5_2, table_5_3 and the figure_5_2 caption. Pilot warm hybrid-vs-CBF: median
**+189.54%**, range **+60.04% to +464.55%** — the +190% figure, correctly labelled warm and
explicitly refused for cold start at C4.112, C5.34, table_5_2, table_5_3 and captions.md. I
grepped every chapter, table, caption and `results/summary.md` for "190": it survives only inside
sentences that identify it as the warm figure and forbid its cold-start use. Warm gain over CBF
positive in **5 of 7** modules (AAA −1.85%, GGG −11.76% negative) — ch05 §5.6.1 says 5 of 7 and
records the E2 correction from the earlier "6 of 7" (C5.71). Cold-start (A|2) medians recomputed:
CBF **0.0728** > Random **0.0484** > Hybrid **0.0473** > ItemKNN-CF **0.0377** > PopWeek 0.0317 >
MostPop **0.0266** — identical to Tables 5.2 and 5.5. The low-bar reading is carried in ch05
§5.3.2, §5.4 and §5.11, and in ch06 §6.1, §6.3, §6.4 and §6.5, always labelled exploratory,
post-hoc and deciding no criterion (C5.116), with the CF Holm caveat stated in the exact form the
artifact gives it: p = 0.046160 uncorrected, p_Holm = 0.092320 (I reproduce W = 65.0, p =
0.0461602, and Holm within the slice's five tests as 0.0923204).

**(5) The label-collapse explanation is withdrawn and appears only as a withdrawal — PASS.** Every
occurrence of "collapse" or "supervision" in the three chapters, the five tables and the captions
is a withdrawal statement: ch05 §5.7.5 (C5.69, C5.70), ch05 §5.8.3's correlation table, ch05 §5.12,
table_5_3 §"Most likely cause", table_5_4. I reproduced the withdrawing evidence: median all-zero
drop share 7.69% warm and 43.97% at k = 2, median positive-label share 0.8060 warm and 0.5095 cold,
and Spearman rho **+0.434**, p **0.0435**, n = 22 against the hybrid's cold-start gain over CBF —
the wrong sign, exactly as claimed. No mechanism is claimed for the cold-start result: ch05 §5.3.2
closes "No mechanism is claimed here", §5.8.1 labels D1 "a correlate and a reading, not a confirmed
mechanism" (C5.79), and §5.12 states the chapter did not establish why the hybrid loses to CBF.
I verified D1's supporting numbers: CBF is the stronger cold component in 20 of 22, per-presentation
median alpha across exactly those 20 runs 0.241 to 0.653 with median 0.494, and the hybrid lies
between its components in 19 of 22 cold (above both 1, below both 2) against 11 of 22 above both and
0 below both on warm.

**(6) D1 and D2 are post-hoc, decide no criterion, second looks outside the L6 counter; D2's scope
is stated — PASS.** `results/run_artifacts/u13d_diag_run/criteria_verdicts.json` reads `unchecked`
for all six. ch04 §4.7 "Disclosure" and ch05 §5.8's blockquote both state the second scoring of the
test split outside criterion C4's counter, both forbid revising any criterion, threshold, model or
protocol, and both name the different code tree (C5.72, C5.73). ch05 §5.8.2 (C5.80) and §5.8's
closing (C5.84), ch04 §4.7 and ch06 §6.2's "not claimed" list all state that D2 removes three
columns from the blend's feature set and not a behavioural recommender component, so the
behavioural-signal clause stays `unchecked`. I reproduced D2 exactly on both slices, including the
n_eff of 21 and 20 after ties, W = 34.0 / 93.0 and p = 0.003279 / 0.674223.

**(7) Two code trees and the prefix hash disclosed — PASS (warning W6 on placement).** I recomputed
`common.code_tree_sha256()` on the tree as it stands: `5a8f935a8dd05bb2b8428966ae9794a2cfe1bf6b7573b5005698bad267691b21`,
the diagnostics tree, confirming ch04 §4.6.6's statement that the G4-approved tree
`694c3ea6026939967a6b01ab0698ef7336e77a8dd29f0739157e9f9662b0231c` no longer exists on disk and
cannot be recomputed. I confirmed the function hashes only `.py` and `.json` outside
`__pycache__`, so ch04's claim that `code/README.md` "lies outside the hash" is exact (C4.80), and
that exactly the five named files (`models.py` 16:37:59, `blend.py` 16:38:02, `diagnostics.py`
16:38:05, `main.py` 16:40:05, `README.md` 16:40:08) post-date the main run's last artifact while
every other file under `code/` precedes it. The inertness check reproduces: all 44 cells of the
production hybrid agree between `ablation_<pres>.json` and `results_<pres>.json`, 0 differences,
maximum absolute difference 0.0 (C4.99, C5.74). On the log: `results/run.log` is 10,274,521 bytes
hashing whole to `5068dad9...ac12`, and its first 10,257,030 bytes hash to
`d547e943a8e02b9fcc26c807b6072f6fafd4bf1e3ca873815de65bda615c0eac`, the main receipt's
`run_log_after_sha256` — so ch04 §4.6.6's prefix-hash disclosure (C4.81, C4.82) and the 17,491-byte
append are both exactly right.

**(8) C5's single-CPU reading matches I3 — PASS, and confirmed.** `decisions.log`
2026-09-24T14:00:00Z, `event=for_reviewer id=I3`, asks the reviewer to confirm the reading "one
machine, one main process, no GPU" on a 12-logical-core machine with no affinity or thread count in
the receipts, citing process CPU 2,798.41 s below wall clock 3,769.12 s. ch04 §4.6.4 states that
reading and those two numbers and adds "it says that the receipts cannot show more than that". The
numbers are the receipt's. I confirm the reading and record that the literal single-CPU property is
`unchecked` in the receipts and correctly presented as such rather than asserted.

**(9) The pilot is unreceipted phase 1 evidence; C6 reproduced its six values bit-identically —
PASS.** ch04 §4.4.1 and §4.6.3 and ch05 §5.4.1 all label the pilot prior evidence under rule 7 and
bound what may be cited from it to the six reproduced EEE_2014J values. Those six values in
`phase1_reproduced_metrics.json` are byte-for-byte the values in
`inputs/prior_evidence/pilot_metrics.json` — warm CBF 0.11820781696854146, CF 0.5351763584366063,
Hybrid 0.5207816968541468; cold CBF 0.10066730219256434, CF 0.16101048617731176, Hybrid
0.14022878932316493 — with all six `abs_diff_precision_at_10` exactly 0.0 against tolerance 1e-06
and `other_fields_differing` 0. Table 4.9's rounded values match. ch04 §4.6.3 correctly states what
C6 does not license (no leakage evidence for phase 2; `assertions_L1_L9` recorded "not applicable:
no bound", never 0).

**(10) Statistics: exact paired Wilcoxon, Holm, ties and n_eff as computed — PASS.** Every test
reproduces to the printed digit under `scipy.stats.wilcoxon(zero_method="wilcox",
correction=False, method="exact")` on the 22 presentation-level values. Warm: vs CBF W = 44.0,
p = 0.005929, p_Holm = 0.011857, rank-biserial +0.652, sign test p = 0.052479, n_eff 22, 0 zeros;
vs CF W = 52.0, p = 0.014095, p_Holm = 0.014095, rank-biserial +0.589, sign p = 0.016901. Cold:
vs CBF W = 18.0, p = 0.000121, p_Holm = 0.000241, rank-biserial −0.858, 2/0/20; vs CF W = 18.0,
p = 0.000241, p_Holm = 0.000241, rank-biserial +0.844, **n_eff 21 after one exact zero difference
was dropped** (EEE_2013J, EEE_2014J and FFF_2014B are exact ties at the printed precision; one is
an exact float zero), 18 wins / 1 tie / 3 losses. Table 5.5's Holm within each slice's five tests
reproduces at 0.000403, 0.002371, 0.011014, 0.092320, 0.750238. The narrow margin is stated where
it must be: ch05 §5.2 (C5.18) "the measured median of +10.68% clears C1's pre-registered threshold
of +10.00% by 0.68 percentage points, which is a pass and not a comfortable one", repeated in §5.5,
in ch06 §6.1 RQ4 (C6.10) and in the Figure 5.1 caption. The sign-test disagreement at p = 0.052479
against CBF is reported beside the pass, with a stated cause, not after it.

**(11) OQ6, OQ7 and the other open items are stated honestly in limitations — PASS.** OQ6 (whether
C3's accuracy conjuncts stay per-presentation): ch05 §5.11 limitation 5, "whether those floors
should stay per-presentation is an open question for the candidate", and ch06 §6.7. OQ7 (actual
versus simulated new users): ch05 §5.11 limitations 1 and 2, with the 997 excluded one- and
two-day learners quantified (mean 10.0 and median 8 resources over mean 2.66 and median 2 active
days against 55 over 52 for the 27,212 retained — verified against `threats_to_validity.md` T22 and
the summed `drop_lt3days` of 997), ch06 §6.5 item 3 and §6.7. Also honestly carried: the licence
provenance gap (limitation 6), RQ2's unanswerability (limitation 7), the deliberately unrun
fixed-alpha sweep (limitation 9), the post-hoc diagnostics on a different tree (limitation 10) and
the hand-written receipts plus unreceipted pre-run tests (limitation 11).

**(12) UI and deep models as scope-outs and future work; RQ2/Module D wording matches what was done
— PASS.** ch04 Table 4.1 records TensorFlow/Keras and deep networks as "not used ... **deferred**";
ch06 §6.2's "not claimed" paragraph (C6.16) and §6.5 item 2 (C6.26) list the deep models and the
interface as deferred scope-outs pending the supervisor's confirmation, matching decisions.log Q11.
RQ2: ch05 §5.11 limitation 7 (C5.105) and ch06 §6.1 RQ2 (C6.6) both say the question cannot be
answered from this design because no compared model is segmented and Module D feeds no model, and
report it unanswered rather than answered by proxy — which matches decisions.log's own root-cause
entry that the mismatch originates in frozen `plan.md` and that `plan.md` was not edited.

**(13) No unsupported causal language; limitations honest; defensible in a viva — PASS.** The one
causal sentence that carries weight, ch05 §5.4.1's "The cause is the cold-start condition, not the
code", is immediately bounded in the same section: "the attribution is a design argument supported
by a reproduction, not a measured contrast" (C5.37), and ch06 §6.2 contribution 2 and §6.6 repeat
that the controlled contrast was not run. The two pilot overstatements the skill names as the
standing trap are handled head-on: ch04 §4.4.1 (C4.108) quotes the pilot's "22 out of 22" and its
"never beats CF on warm users" and states that the first holds only against CBF and the second is
contradicted by the pilot's own +0.91% maximum, then says neither is repeated. I verified both
against the pilot file: cold-start vs CBF 22 wins of 22, warm vs CF 3 wins of 22 with a maximum of
+0.91%. Chapter 6 §6.6 names, for each conclusion, the evidence that would overturn it.

**(14) The twelve integrity rules — PASS.** Rule 1: independence verified from decisions.log, not
assumed (frontmatter). Rule 2: 268 of 268 distinct ids ledgered, 43 of 44 artifacts re-hash clean,
the 44th being I5's excluded `decisions.log`; one unmarked sentence (W1). Rule 3: criteria frozen
and unmoved ([C6]); both diagnostics and Table 5.5 explicitly refused the power to revise a
criterion. Rule 4: all 22 presentations reported in Tables 5.1, 5.2, the C3 conjunct table, both D2
tables and the D1 table, with no best-run reporting anywhere; the pilot's NaN week-column defect
stays in the record with its cause (ch04 C4.13/C4.14, ch05 C5.56). Rule 5: the partial result is
reported as terminal, not as a near-miss. Rule 6: `unchecked` is used and never upgraded — the
unreceipted pre-run tests (C5.7), the behavioural-signal clause (C5.45, C5.84), the main stage's C6
and the diagnostics stage's six verdicts. Rule 7: all 99 receipted artifact files re-hash to their
recorded values and all three execution-event hashes recompute from the receipts' own fields;
chapter 4 §4.6.2 states plainly what a hand-made receipt does and does not prove. Rule 8: no scope
drift; the added baselines and metrics beyond plan.md's four models are declared recorded
deviations that decide nothing (C5.97). Rule 9: see the Constraint Audit. Rule 10: no untrusted
source changes any permission or instruction. Rule 11: literature numbers in §5.9 are labelled with
their own task and refused as comparable. Rule 12: the plan's three-run budget is reported as
reached, with no rerun for a mechanism fix taken (C4.39); 0 of 3 debug rounds used.

**(15) Figures and captions match the tables and the regenerated figure_5_2 — PASS with W2.** Every
number in the three captions reproduces from the artifacts, including Figure 5.2's pilot contrast
(+73.12%, +13.55% to +163.85%; −17.90%, −29.12% to −10.03%) and its explicit E1 correction
paragraph, and Figure 5.3's alpha statistics (pooled median 0.5150, quartiles 0.4019 and 0.6181,
range 0.0696 to 0.9651, 0.04% at or above 0.9 = 2 of 5,444, 0.11% at or below 0.1 = 6, 83.9%
between 0.3 and 0.7, per-presentation medians 0.2415 to 0.6534, 12 of 22 above 0.5, 5,444 records
equal to the summed `n_scored`). `figure_5_2_coldstart_relative_gain_spread.png` carries a
modification time later than the E1 fix recorded in decisions.log, consistent with its recorded
regeneration. All three figures are referenced in the text before they appear (§5.2, §5.3, §5.8).
The one caption-to-artifact slip is W2.

## Ledger rows spot-checked against the artifact, not only the hash

Chapter 4 (44 rows). C4.1 (verified in `code/data.py`:26-39, the SHA256-and-size gate that raises
`DataIntegrityError`), C4.2 and C4.3 (run manifest: python 3.12.3, numpy 2.5.3, pandas 3.0.5,
scikit_learn 1.9.1, scipy 1.18.1; hardware string with 12 logical cores and no GPU), C4.5 and C4.87
(`code/README.md`: "MostPop 0.0137 / 0.0255 / 0.2157 and ItemKNN-CF 0.0279 / 0.0333 / 0.1946"),
C4.8 (34 cells: 10 + 10 + 10 + 2 + 2 in `results_AAA_2013J.json#splits`), C4.10 and C4.67 (1,049
learners), C4.12 (`criterion_1_hybrid_vs_baselines_warm.hybrid_vs_cbf_relative_gain` 3.4056 =
+341%, `hybrid_vs_cf_relative_gain` −0.0269), C4.15, C4.16, C4.17, C4.96 and C4.112 (recomputed
pilot aggregates, above), C4.19 and C4.20 (0.5352 pilot against 0.1877 phase 2 on EEE_2014J),
C4.22–C4.30 (gate history checked against the review files' own frontmatter: plan_gate 0/2,
method_gate cycle 0 3/4, cycle 1 3/5, cycle 2 2/7, cycle 3 0/8, code_gate 0/2, review.md 2/12,
review_cycle1 3/6, review_cycle2 0/7), C4.36 (plan.md hash equals the protocol header's), C4.46,
C4.47 and C4.48 (the three receipts' start, finish, exit, wall, CPU, worker, CPU-hours and file
counts, all exact), C4.49–C4.58 (Table 4.8's ten hashes, each recomputed or re-read from the named
receipt), C4.60 (all three execution-event hashes recomputed from the receipt fields in the
documented key order — they match only in that order, not sorted, which is itself evidence the
documented order is the one used), C4.64 (six zeros, tolerance 1e-06), C4.69, C4.70, C4.71 and
C4.94 (0.238 min, 3,769.12 s, 1.0140 CPU-h, the per-stage "unchecked conjunct" wording), C4.72
(2,798.41 s below 3,769.12 s), C4.73 (48 files), C4.75 (33,458 log lines, 30,455 assertion
records), C4.76 (2,092 `not_applicable`, 2,112 L7 information records — and 0 failures and 0 counts
above a required value), C4.77 (C4's five measured values), C4.80 (README outside the hash; the
five changed files by mtime), C4.81 and C4.82 (17,491 bytes appended; the prefix hash), C4.98
(`run_summary.json#assertions.unchecked` = {} and `flags` = []), C4.99 and C4.100 (44 cells, 0
differences), C4.101 (0.1413 CPU-h), C4.102 (receipt `seed` 42, `random_seeds` [42,43,44,45,46]).

Chapter 5 (54 rows). C5.2, C5.4 and C5.5 (code tree, 52 files re-hashed clean, 1.0140 CPU-h /
0.238 min), C5.8, C5.9 and C5.10 (29,228 / 27,212 / 2,016 = 1,019 + 997; 5,444 cold learners from
69 at AAA_2014J to 426 at CCC_2014J; EEE_2014J 79 of 1,097 removed and the 49 / 44.8 attribution,
which is W2's subject), C5.11 and C5.12 (45.58%, 14.38% FFF_2013B, 81.28% GGG_2014B; cold ceiling
0.6482 GGG_2014B to 0.9435 FFF_2013B), C5.13 to C5.19 and C5.21 (every warm distribution,
gain, count, test and effect size, plus the 11/11/0 above-between-below split), C5.22 to C5.26
(every cold distribution, gain, count, test and effect size, and the Random-above-Hybrid ordering),
C5.27 to C5.30 (the whole C3 conjunct table, all 22 rows and 7 columns; coverage 0.1215 to 0.5566;
vs-MostPop +76.46% at p_Holm 9.5e-07 with 22 of 22 wins), C5.31 to C5.36 (the central finding, the
pilot's four aggregates, the E1 correction, the 20-of-22 / 18-of-22 inversion counts, the six
zero differences), C5.39 to C5.46 (the six verdicts and their measured values against
`criteria_verdicts.json`), C5.47, C5.48 and C5.71 (the per-module table, all 7 rows and 4 columns,
and the 5-of-7 count), C5.49 to C5.53 (the sensitivity grid, all 5 rows and 4 columns, and the P4b
union chain 0.068259 / 0.052862 / 0.047349 / 0.047096 giving +29.1%, +11.6% and the untested
+0.54%), C5.67 (the 0.0473-for-0.052862 error the run gate caught), C5.69 and C5.70 (7.69% / 43.97%
drop share, 0.8060 / 0.5095 positive-label share, rho +0.434 at p 0.0435), C5.73 and C5.74 (the two
trees, 44 cells, 0 differences), C5.75 to C5.78 (all of D1), C5.81 to C5.83 (all of D2), C5.85 (the
four surviving correlations +0.219, +0.825, +0.884, +0.874), C5.99 (the 997 excluded learners'
profile), C5.103 (`partial`, and honestly so), C5.110 to C5.116 (the whole of Table 5.5, both
slices, ten tests, uncorrected and Holm).

Chapter 6 (17 rows). C6.1, C6.2, C6.4, C6.5, C6.7, C6.12, C6.13, C6.14, C6.17, C6.18, C6.21,
C6.22, C6.23 (`partial`; W4), C6.39, C6.40, C6.41, C6.42 — each read as a restatement and checked
against the chapter 5 row it restates and against the same artifact. All agree; none strengthens
what chapter 5 says, and C6.39 to C6.42 correctly import the random-floor reading with its
exploratory label intact.

Rows deliberately not counted as defects: the 18 rows citing `decisions.log` (C5.6, C5.57 to
C5.59, C5.62 to C5.64, C5.71, C5.105, C5.107 and others), whose hash goes stale on every append —
open item I5, `decisions.log` 2026-09-24T06:53:40Z.

## Notes

- The single strongest thing about this pair of chapters is that the two places most likely to
  hide an overstatement — the surviving half of C2 and the passing conjuncts of C3 — are the two
  places the text argues hardest against itself, in §5.3.2, §5.4, §5.11 and again in ch06 §6.1,
  §6.3 and §6.4. "On new learners the hybrid is not distinguishable from a random ranker" is a
  sentence a writer protecting a result does not write.
- Chapter 4 §4.6.5's caution that C4's `hyperparameter_rows_reading_test_data` field is
  structurally incapable of being non-zero, and its redirection of the leakage evidence to the
  counted assertions L7, L8 and L9, is an unusually honest piece of self-limitation and chapter 5
  honours it.
- The residual weakness a viva will probe, and which is already action item I4 in decisions.log:
  the G4-approved code tree `694c3ea6...231c` cannot be recomputed by anyone, because `code/` is
  untracked and no pre-diagnostics copy exists. Chapter 4 says exactly this. Snapshotting the
  current tree into `final/` before submission is worth doing.
- Chapters 4 to 6 do not touch the university-template line of the standards' front-matter row;
  the regulations are still absent from the repository, so that line stays `unchecked` for the
  whole thesis and is the candidate's to close.

## Overall

I approve chapters 4, 5 and 6 with warnings. Every number I could recompute — and I recomputed all
of them, from the receipted per-presentation artifacts rather than from any summary — reproduced
exactly: the 22 rows of both result tables, all eight pre-registered Wilcoxon tests with their Holm
corrections and effect sizes, the ten exploratory random-floor tests, both diagnostics, the pilot's
four aggregates, all 99 receipted file hashes, both code-tree hashes, all three execution-event
hashes and the run-log prefix hash. The four corrected facts the dispatch named are carried
correctly everywhere they appear, the +190% figure is used only as the pilot's warm gain and
explicitly refused for cold start, the label-collapse explanation exists only as a withdrawal, no
mechanism is claimed beyond a labelled correlate, and the six criterion verdicts in the chapters
are the six verdicts in the receipted files, with no softening of C2 and C3 and no inflation of C1.
The six warnings are one missing ledger marker on a restated number, one caption that attributes a
population statistic to the wrong cohort, two ledger-bookkeeping slips and two assembly-level
consistency items; none can change a verdict, a direction or a scope. What would change this
decision to `revise` is a number that does not reproduce, a criterion restated at a threshold other
than `plan.md`'s, or the +190% figure reappearing as a cold-start result — none of which is present.

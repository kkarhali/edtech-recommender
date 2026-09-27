---
blockers_count: 3
warnings_count: 8
files_reviewed: n/a (documents: thesis/ch01.md, thesis/ch02.md, thesis/ch03.md, thesis/claim_ledger.csv, literature/ledger.csv, plus the artifacts they cite)
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Opus 5
model_identity: claude-opus-5 (self-reported; the three chapters under review were produced by mid-tier `sonnet` writer/scholar/methodologist agents per `state.md` §agents and each chapter's own draft header, so rule 1 independence holds)
mode: chapter_gate
unit: u15_g7_chapter_gate
cycle: 0
decision: revise
---

# Review

Scope: gate G7, the chapter gate, on chapters 1, 2 and 3. Written by hand, with no MCP tool
validating it, because `ar-workflow-engine.py` imports `fcntl` and cannot run on this machine —
a recorded deviation, per rule 6, not a silent pass. No chapter, ledger or artifact was edited.

Per the manager's note, ledger rows citing `decisions.log` (open item I5) are not counted as
defects. No C1-prefixed row cites `decisions.log`, so I5 did not arise in this gate.

## Blockers (must fix before proceeding)

- [B1] <severity:high> `thesis/claim_ledger.csv` (whole file) versus `thesis/ch03.md` and
  `thesis/ch02.md`: **chapters 2 and 3 have no claim-ledger rows at all.** The merged ledger holds
  299 rows whose ids are only `C1.*` (32, chapter 1), `C4.*` (108), `C5.*` (116) and `C6.*` (42).
  No `C2.*` or `C3.*` row exists, and neither chapter contains a single `<!-- C… -->` id.
  Chapter 3 contains 74 sentences carrying a data number; 59 carry no pointer of any kind, and the
  13 that do carry only a bare `<!-- source: studentVle.csv, computed 2026-09-21 -->` style comment
  with no claim id, no SHA256 and no status field. Examples with no pointer at all:
  "in EEE_2014J, 402,947 rows become 47,136 pairs over 1,097 learners" (§3.4 item 3);
  "the realised test fraction runs from **0.199 to 0.205**" (§3.5.1, the `<!-- source -->` there
  covers the fractions but binds no hash); "cohort sizes run from 69 (AAA_2014J) to 426
  (CCC_2014J)" (§3.5.2); "the collaborative model uses five … the hybrid four" (§3.6);
  "between **14.4%** (FFF_2013B) to **81.3%** (GGG_2014B)" (§3.7.1).
  | impact: the G7 pass condition "every quantitative claim has a ledger row pointing at an
  artifact" and integrity rule 2 are unmet for a 787-line chapter; every number in the thesis's
  methodology chapter is currently unverifiable by hash, so an examiner cannot check one without
  re-deriving it. (I did re-derive a sample and they are **correct** — see Notes — which is why
  this is a missing-evidence blocker and not a wrong-number blocker. rule=2)

- [B2] <severity:high> `thesis/ch03.md` §3.11 (line 751) and §3.12 (line 778): two closed-list
  statements contradicted by the artifact each one names.
  §3.12 says "The full list of deviations from the approved plan, **D3 to D13**, is in
  `methodology/protocol.md` section 16". That section lists **D3 to D14**; D14 is
  "Module D is descriptive only … feeds no model, and supplies no cold-start prior", i.e. exactly
  the deviation that chapter 3 §3.1 itself now carries after cross-artifact fix I1.
  §3.11 says "**Six** questions are open for the candidate and are carried in
  `methodology/protocol.md` §17", and lists six. §17 holds **OQ1 to OQ8**. The chapter omits OQ7
  and OQ8. OQ7 is load-bearing: it records that the evaluated population is narrowed twice,
  removing "2,016 of the 29,228 learners in the logs", that the second filter "removes precisely
  the one- and two-visit learners closest to `idea.md` criterion 2's 'actual new users'", and that
  an "actual new users only" reading "would require a redesign".
  | impact: the chapter presents an exhaustive list of deviations and open questions and both are
  short by one and two items; a reader of chapter 3 alone is not shown the one open question that
  could invalidate the cold-start design the chapter specifies. (rule=2, rule=6)

- [B3] <severity:med-high> `thesis/ch03.md` §3.9 and §3.12: chapter 3 nowhere records that the
  receipted results and the diagnostics come from **different code trees**, nor that the main
  receipt's run-log hash is a **prefix hash**. §3.9 instead states the reproducibility record as
  "the code version; the library versions; … and the exact command line behind every reported
  number, recorded in a run receipt with the hash of every artifact it produced", which reads as
  one tree and whole-file hashes. Chapter 4 does state both, correctly and in detail
  (`thesis/ch04.md`:268 "The receipted results and the diagnostics come from different code
  trees… `694c3ea6...231c` … `5a8f935a...1b21`"; :270 "The main receipt's log hash is now a prefix
  hash … the first 10,257,030 bytes of the file today still hash to that value"). Chapter 3 also
  never mentions the two post-hoc diagnostics or the exploratory random-floor reading, while §3.12
  tells chapter 4 it "needs four things from this chapter and takes nothing else".
  | impact: the checklist requires chapters 3 **and** 4 to state the two-tree split and the prefix
  hash; as drafted, an examiner who verifies `results/run.log` against chapter 3's reproducibility
  promise will get a hash mismatch with no explanation in the chapter that made the promise.
  (rule=6: an undisclosed record gap is `unchecked`, never `passed`)

## Warnings (should fix)

- [W1] <severity:med> `thesis/ch03.md` §3.4 item 4: the 997 excluded learners are described as
  "learners who opened **many** resources in one or two sittings". `methodology/protocol.md`:336-342,
  the artifact the same paragraph counts from, says they "hold a mean of 10.0 and a median of **8**
  distinct resources" and calls them "people who opened **a handful** of resources in one or two
  sittings". `thesis/ch01.md`:175 calls the same group "997 learners who opened **few** resources
  on one or two days". Three artifacts, three characterisations of one population.
- [W2] <severity:med> `thesis/ch03.md` §3.5.3: "an inflation of between **six and nine** times".
  The two measured pairs are 0.0255 → 0.2157 (8.46x) and 0.0333 → 0.1946 (5.84x)
  (`methodology/protocol.md`:825-826). `thesis/ch04.md`:328 states the same fact as "8.5-fold for
  popularity and 5.8-fold for collaborative filtering". "Six" rounds the lower bound the wrong way.
- [W3] <severity:med> `thesis/ch01.md`:200: "The integrity and feasibility criteria are met. …
  C5 finds a main run of 1.014 CPU-hours against a budget of 4.0." Both per-stage verdict files
  read `"verdict": "not met (unchecked conjunct)"` for C5; the `met` verdict is, in Table 5.3's own
  words, "**met** (combined by hand from both receipts)". Chapter 1 states the conclusion without
  the combination. The numbers themselves are right (receipt `cpu_hours` 1.0140075; pilot
  `reproduction_minutes` 0.2378).
- [W4] <severity:low> Licence wording: `thesis/ch02.md`:44 spells it "CC-BY 4.0" once where ch01,
  ch03, `methodology/data_statement.md`, `results/summary.md` and `results/data_manifest.json` all
  say "CC BY 4.0"; `plan.md`:71 still reads "**Licence: `unverified`**" (frozen, human-owned, and
  explained in ch02 and `literature/open_questions.md` item 6); `literature/ledger.csv`'s
  `kuzilek2017oulad` `notes` field still reads "plan.md records the licence as unverified pending
  the human". The substantive status is consistent everywhere and the residual provenance gap (the
  local `oulad.zip` is not traced to the deposit) is named in every place it should be.
- [W5] <severity:low> `thesis/ch02.md`: its two tables (§2.1 terms, §2.8 related work) are
  unnumbered and referenced only as "The table", where ch01 numbers Tables 1.1-1.8 and ch03
  Tables 3.1-3.2. The writing rule asks that every table be referenced in the text before it
  appears; it is, but not by a number the assembled thesis can carry.
- [W6] <severity:low> `thesis/ch02.md` §2.2 and the coverage line at :99: the **context-aware**
  family, a required element of the chapter-2 row in the standards, has no included source — the
  one candidate was excluded at full text. This is disclosed twice and is therefore `unchecked`
  rather than hidden, but the chapter row is not fully satisfied.
- [W7] <severity:low> `thesis/ch01.md` Table 1.2: proposal sub-objective 2 is given the status
  "**In scope**, limited to clustering and the learned blend weight". The clustering feeds no model
  (ch03 §3.1, protocol D14) and RQ2 is unanswerable, so only the learned blend weight is actually
  delivered. The qualification sits in the same cell, but the status word overstates it.
- [W8] <severity:low> `thesis/ch03.md`: neither post-hoc diagnostic (D1 blend-weight distribution,
  D2 behavioural-feature ablation) nor the exploratory random-floor comparison appears anywhere in
  the methodology chapter, although §3.8 does pre-declare an exploratory family F4 that could hold
  them. As drafted they first appear in chapter 4, with no methodological statement behind them.

## Constraint Audit

Hard constraints taken verbatim from `idea.md` (frozen, binding `918162da54511db3`, confirmed
against `idea_provenance.json`).

- [C1] "use the public Open University Learning Analytics Dataset (OULAD) for this pilot … requires
  network access during the pilot to download OULAD once" | status: satisfied | evidence:
  `thesis/ch03.md` §3.2 (OULAD named, licence, population and its limitation stated);
  `thesis/ch03.md` §3.9 "no network access at run time; the dataset tables are already on disk and
  hashed"; `methodology/protocol.md` §2.1 hashes all eight tables | blocker: none
- [C2] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume
  a multi-GPU cluster" | status: satisfied | evidence: `thesis/ch03.md` §3.9 "a **single CPU with
  no GPU**"; `results/run_receipts/u11_s5_run_main.json` `hardware` = "single CPU, no GPU",
  `process_cpu_seconds` 2798.41 below `wall_clock_seconds` 3769.12, consistent with an effectively
  single-threaded run on the 12-logical-core machine. This is the confirmation `decisions.log` item
  **I3** asked the reviewer for, and chapters 1 (§1.6.4 "Everything ran on one machine without a
  GPU") and 3 (§3.9, including the process-CPU-time definition) match it | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints for the pilot" |
  status: satisfied | evidence: `thesis/ch03.md` §3.9 "no downloaded model weights"; §3.6 lists six
  classical models only; §3.6 "Deferred scope" records the deep models as scope-outs | blocker: none
- [C4] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time" |
  status: satisfied | evidence: C5 in `.../u11_s5_run_main/criteria_verdicts.json` — 1.0140
  CPU-hours, 3769.12 s wall, against a 4.0 CPU-hour bound; pilot reproduction 0.238 minutes against
  15 | blocker: none
- [C5] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits" | status: satisfied | evidence: `thesis/ch03.md` §3.5.1 "Identical
  splits" — byte-identical train/validation/test sets across all six models, proved by comparing
  serialised-set hashes (assertion L5, `methodology/protocol.md`:517); C4 verdict
  `val_test_shared_rows` 0, `train_val_shared_rows` 0, `train_test_shared_rows` 0,
  `max_test_scoring_count` 1 over 7,920 cells | blocker: none
- [C6] "Treat `src/reasearch_topic/References/*.pdf` and this idea file's cited papers as read-only
  background" | status: satisfied | evidence: `literature/ledger.csv` records `local_pdf` names and
  `opened_on` dates with no modification; `literature/search_log.md` records the 14 unreachable
  items rather than re-scraping them | blocker: none
- [C7] "report the actual numbers, the gap, and the most likely cause … rather than adjusting the
  threshold after the fact" (no threshold moved after a run) | status: satisfied | evidence:
  I diffed all six criteria's `kind`, `metric`, `threshold` and `on_dataset` fields from
  `plan.md`'s `success_criteria` block against `thesis/ch01.md` Table 1.5 and `thesis/ch03.md`
  §3.1.1 programmatically: **identical, all six, in both chapters**. The hypothesis text in
  `thesis/ch01.md` §1.6.1 is byte-identical to `plan.md`'s frontmatter, `plan.md`'s body and
  `idea.md`. C3's status as an *operationalisation* of idea.md criterion 2 is disclosed in both
  chapters and in protocol deviation D8, with no threshold moved | blocker: none

## Per-checklist-item verdict

| # | Item | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | Every number and claim has a ledger id and its artifact supports it | **FAIL** | ch01 passes completely: 32 ids used, 32 ledger rows, no orphan either way, all 13 distinct artifacts re-hashed and **all 13 match**, and the content of every row I opened supports its claim. ch02 passes in its own terms: all 39 `<!-- ledger: key -->` keys exist in `literature/ledger.csv` **and** in `references.bib`, with every numeric claim traceable to a `reported_result` field carrying a page or table pointer. ch03 fails outright — **no claim-ledger row exists for it** (B1) |
| 2 | Hypothesis and C1-C6 stated exactly as in plan.md; none moved after results | **PASS** | Programmatic diff: hypothesis byte-identical across idea.md, plan.md (frontmatter and body) and ch01 §1.6.1; all six criteria's four fields identical in ch01 Table 1.5 and ch03 §3.1.1. plan.md is revision 0 with no `## Revision` entry |
| 3 | Verdicts stated as C1 met, C2 and C3 not met, C4 C5 C6 met, no softening or inflation | **PASS** | ch01 §1.7.1:196-200 and §1.9:220. Verified against `.../u11_s5_run_main/criteria_verdicts.json`: C1 `met` (+31.20% / +10.68%, p_holm 0.011857 / 0.014095); C2 `not met`; C3 `not met`, 2 of 22 pass all four conjuncts (CCC_2014J, DDD_2013B — I recomputed `all_conjuncts` over the 22 rows); C4 `met`; C6 `met`, `max_abs_diff` 0.0. ch01 does not soften: it says C1 "is met without a wide margin" and names the 0.68-percentage-point margin. See W3 on C5's hand-combined verdict |
| 4 | Corrected facts: +73.12% cold / +190% is warm; warm gain positive in 5 of 7 modules; random floor not below the hybrid on cold start | **PASS** | Neither "+190", "189.54" nor "73.12" appears anywhere in ch01-ch03, so the wrong attribution cannot be carried by them; ch04:116 and ch05:295-298 hold the corrected statement. The "5 of 7 modules" correction lives in ch05:350-351 and `results/summary.md`:162, neither under review here, and ch01-03 make no per-module count. ch01 §1.7.1 states the random floor correctly and completely: 0.0728 CBF, 0.0484 Random, 0.0473 hybrid, 0.0377 CF, 0.0266 MostPop, CF beating Random in 6 of 22 and the hybrid in 10 of 22, all matching `table_5_5_random_floor.md` exactly, and concludes "being ahead of collaborative filtering there is a low bar", explicitly labelled "exploratory and post-hoc … decides no criterion" |
| 5 | Label-collapse explanation withdrawn and absent as a cause | **PASS** | No occurrence in ch01, ch02 or ch03. The only occurrences are in ch05:408 and ch05:532, both stating the withdrawal with the wrong-sign evidence (Spearman +0.434, p = 0.0435) |
| 6 | D1 and D2 post-hoc, decide no criterion; D2 is the blend's use of behavioural features; the behavioural clause unchecked | **PASS (with W8)** | ch01 Table 1.7 K6: "Two disclosed **post-hoc** diagnostics … the distribution of the fitted blend weight and an **ablation of the behavioural features in the blend**, labelled as deciding no criterion". ch01 §1.3.4: "No criterion compares the hybrid with and without its behavioural signal … it is not tested on its own terms". ch03 does not mention them at all (W8) |
| 7 | Different code trees and the prefix hash stated in chapters 3 and 4 | **FAIL** | ch04:268 and ch04:270 state both, fully and correctly. ch03 states neither (B3) |
| 8 | C5 (single CPU) reading matches I3 | **PASS** | See Constraint Audit [C2]. I confirm I3's reading: one machine, one main process plus one fresh-process worker whose wall seconds are counted as CPU (an upper bound), no GPU; process CPU 2,798.41 s below wall-clock 3,769.12 s. ch01 §1.6.4 and ch03 §3.9 both match, and ch03 defines CPU-hours as process CPU time and names the 12 logical cores rather than hiding them |
| 9 | OULAD licence wording consistent everywhere (CC BY 4.0) | **PASS (with W4)** | ch01:175, ch03:112-113 and :722, `data_statement.md` §2, `results/summary.md`:264, `results/data_manifest.json`:7 and `literature/open_questions.md` item 6 all read CC BY 4.0, verified 2026-09-21 at the figshare deposit, with the same residual gap named. Cosmetic residue only (W4) |
| 10 | Dwell time a recorded scope reduction; UI and deep models scope-outs with reason | **PASS** | ch01 §1.3.3 items 1-3; ch03 §3.3.1 (with the six-column `studentVle.csv` header as evidence and the cost stated: "a count cannot distinguish a resource opened once by accident from one studied for an hour") and §3.6 "Deferred scope" and §3.11; ch02 §2.3 "is never called dwell time" and §2.4 "reserved for later work". Both chapters state the reason (no duration field; single-CPU bound and the plan's deferral) and neither claims dwell time was measured |
| 11 | RQ2 / Module D wording matches what was actually done | **PASS** | ch01 §1.3.3 item 4 and Table 1.6 ("RQ2 — none; not answerable by this design"); ch03 §3.1 "**Module D feeds no model** … RQ2, as `plan.md` words it … **is not answerable from this design**". Both name the escalation (rule 8) rather than rewording the frozen question. Corroborated by `review.md`:284-286 and protocol D14/OQ8 |
| 12 | Consistency sweep: data_statement §7 AI disclosure vs literature open question 4; protocol's "cold-start prior" line | **PASS** | `data_statement.md` §7 marks the AI disclosure `unverified` and "a placeholder to be replaced, not a compliant disclosure (OQ2)"; `literature/open_questions.md` item 4 and `search_log.md` both carry it as open; ch01's header, ch01 §1.9 and ch03 §3.10 all say the wording is unsettled. No artifact claims a compliant disclosure exists. `methodology/protocol.md`:203 still carries "cold-start prior" in a Used-how cell, but :209-217 add an explicit qualifying note, and D14 plus OQ8 record it; :241 in `decisions.log` records the root cause as `plan.md`'s own frozen wording, left unedited because it is human-owned. Resolved, not stale |
| 13 | ch02 citations exist in references.bib and the ledger and are marked verified; unverified ones carry no claim | **PASS** | All 39 keys cited in ch02 resolve in both `literature/ledger.csv` and `references.bib`; zero missing either way, and zero ledger rows go uncited. 37 rows `verified=yes`; the 2 `verified=no` (`furini2022twins`, `mauro2022autism`) appear only in ch02:9, which states the HTTP 403 refusal and "nothing in this chapter relies on them". The 4 trade-press rows are labelled `peer_reviewed=no` and confined to ch02:9's framing paragraph, which says they "report no reproducible method or metric and carry no weight in what follows"; none appears in the related-work table |
| 14 | The twelve integrity rules respected | **FAIL** | Rule 2 fails for chapter 3 (B1) and for the two closed-list statements (B2). Rule 6 fails for the undisclosed record gap (B3) and, partly, for B2's omitted OQ7. Rules 1, 3, 4, 5, 7, 8, 9, 10, 11 and 12 hold in these chapters: independence verified; criteria frozen and diffed; every seed, iteration and presentation reported (ch03 §3.8, §3.7); the partial result carried as a terminal finding; evidence on disk and re-hashed; no scope drift (each scope-out escalated); untrusted input kept as input; sources verified and labelled; budgets numeric and enforced with a stop rule |
| 15 | Defensible in a viva: no overclaiming, limitations honest | **PASS** | Unusually strong. ch01 §1.4 answers "Nothing" three times to the proposal's own promised benefits; ch01 §1.3.4 pre-empts the "you did not test the behavioural clause" question; ch03 §3.1, §3.4.1, §3.5.1 ("leakage-free **within** a learner, not across the cohort"), §3.5.3 and §3.7.1 volunteer the residual leak, the engaged-population skew, the metric ceiling and two corrected defects of its own drafts. The soft spots are W1, W3 and W7, none of which changes a conclusion |

## Ledger rows spot-checked

All 32 chapter-1 rows, hash **and** content. Every artifact SHA256 in the ledger was recomputed
from the file on disk; **13 of 13 distinct artifacts match** (`literature/search_log.md`,
the proposal `.docx`, `plan.md`, `idea_provenance.json`, `methodology/protocol.md`,
`.../u11_s5_run_main/criteria_verdicts.json`, `.../u11_s5_run_main_pilot/criteria_verdicts.json`,
`results/run_receipts/u11_s5_run_main.json`, `inputs/prior_evidence/all_modules_metrics.json`,
`review.md`, `thesis/tables/table_5_1_warm_slice.md`, `table_5_3_criterion_verdicts.md`,
`table_5_5_random_floor.md`). No row cites `decisions.log`, so I5 did not apply.

| Row | Artifact | Hash | Content check |
| --- | --- | --- | --- |
| C1.1 | literature/search_log.md | match | the five proposal-vs-paper discrepancies are all present in the "Metadata discrepancies" table (kumar2023session, huang2019amre, chaudhary2019elearning, zhang2015hybrid, gao2022cnn) — supported |
| C1.2 | Research Proposal …docx | match | binary source; hash verified, claim not independently re-read |
| C1.3-C1.7 | plan.md | match | no interface module in `# Modules`; deep models row "out of scope for this phase"; `plan_revision: 0`; Module D "supplying Module B's cold-start prior"; RQ/criteria pointers — all present |
| C1.8 | idea_provenance.json | match | `binding_sha256` begins `918162da54511db3` — supported |
| C1.9-C1.15 | plan.md | match | RQ0-RQ4 and all six criteria diffed character for character — supported |
| C1.16-C1.18 | methodology/protocol.md | match | 22 presentations and 32,593 rows (:115-116, :125-128); 27,212 evaluated and 997 dropped (:177, :299, :334); six models (:517 L5) — supported |
| C1.19 | u11_s5_run_main/criteria_verdicts.json | match | `C1.values.vs_CBF.median_rel_gain` 0.31204, `vs_CF` 0.10685, `p_holm` 0.011857 / 0.014095 — supported |
| C1.20 | table_5_1_warm_slice.md | match | ":55 The vs.-CF conjunct clears the pre-registered threshold by only **0.68 percentage points**" — supported |
| C1.21 | u11_s5_run_main/criteria_verdicts.json | match | `C2.vs_CF` +0.07321, `C2.vs_CBF` −0.30281 — supported |
| C1.22 | u11_s5_run_main/criteria_verdicts.json | match | I recomputed `all_conjuncts` over the 22 per-presentation entries: exactly 2 true — supported |
| C1.23 | inputs/prior_evidence/all_modules_metrics.json | match | hash verified; the 22-of-22 direction is corroborated in table_5_3:16 — supported |
| C1.24 | u11_s5_run_main/criteria_verdicts.json | match | `val_test_shared_rows` 0, `max_test_scoring_count` 1 of 7,920 cells — supported |
| C1.25 | run_receipts/u11_s5_run_main.json | match | `cpu_hours` 1.0140075 — supported (see W3 on the "met" wording) |
| C1.26 | u11_s5_run_main_pilot/criteria_verdicts.json | match | all six `abs_diff_precision_at_10` exactly 0.0, `max_abs_diff` 0.0, tolerance 1e-06, verdict `met` — supported |
| C1.27 | table_5_3_criterion_verdicts.md | match | rows 7-12 give met / not met / not met / met / met / met — supported |
| C1.28 | review.md | match | ":284-286 … the protocol's section 8 compares six models, none segmented … RQ2 as plan.md words it will not be answerable" — supported |
| C1.29 | methodology/protocol.md | match | CC BY 4.0, verified at the figshare deposit — supported |
| C1.30-C1.31 | plan.md | match | refutability sentence and the 22-presentation significance rule — supported |
| C1.32 | table_5_5_random_floor.md | match | all five medians (0.0728 / 0.0484 / 0.0473 / 0.0377 / 0.0266) and both win counts (6 of 22, 10 of 22) match the table exactly — supported |

Ten `literature/ledger.csv` rows additionally spot-checked against the numbers chapter 2 puts on
them: `liang2017profile` (99.6 / 50.0), `huang2019amre` (best on accuracy, last of twelve on
precision), `gao2022cnn` (P@5 0.39 vs 0.23 and 0.26), `chaudhary2019elearning` (98.98%),
`degemmis2004hybrid` (F1 0.839 vs 0.923), `sanguino2022course` (P@5 0.4), `butmeh2024coldstart`
(82%), `kuzilek2017oulad` (22 presentations, 32,593, 10,655,280), `sarwar2001itembased`,
`ferrari2021troubling` (11 of 12). Each row's `reported_result` or `dataset` field carries the
figure with a page or table pointer, and chapter 2's sentence matches it. Total spot-checked: 42.

## Notes

- Chapter 3's numbers are **right** where I could re-derive them, which is what makes B1 a
  missing-ledger finding rather than a wrong-number finding: 32,953 − 32,593 = 360 students;
  402,947 → 47,136 pairs over 1,097 learners; 1,097 − 48 − 31 = 1,018; 1,188 − 1,097 = 91 never
  touching the VLE; 997 of 28,209 (3.53%) leaving 27,212; realised fractions 0.199-0.205 and
  0.102-0.120; ceilings 45.6% / 14.4% / 81.3%; cold cohorts 69 to 426; the 0.0255/0.2157 and
  0.0333/0.1946 exclusion-rule pair; "within 11% of each other" against protocol's 10.8%; CF 31%
  above popularity under the corrected rule (0.0333/0.0255 = 1.306). All confirmed against
  `methodology/protocol.md` and `methodology/threats_to_validity.md`.
- The 5,444 cold-start learner records that D1 is computed over are consistent with 20% of the
  27,212 evaluated learners, and `table_5_5_random_floor.md` states the same figure.
- Chapter 2's "32,593 students" is attributed to the Scientific Data descriptor while chapter 3's
  defect note says `OULAD.names` states 32,953. These are two different documents and both
  chapters name theirs, so this is not a contradiction — but at assembly it would read better if
  chapter 3 said the journal descriptor agrees with the CSVs and only the archive's `.names` file
  does not.
- `decisions.log`:253 left two items open for this gate: "C1.27 cites table_5_3 and C1.20 and
  C4.20 cite table_5_1 so they need re-hash after the analyst finishes" and "ch01 section 1.7.1
  says hybrid is ahead of CF on cold start and needs softening after the Random-floor table".
  Both are now closed: C1.20 and C1.27's hashes match the current tables, and ch01 §1.7.1 carries
  the Random-floor reading with "being ahead of collaborative filtering there is a low bar".
- Writing rules: all three chapters open with a purpose paragraph (§1.0, §2.0, §3.0) and close
  with what they established (§1.9, §2.10, §3.12). Every numbered table in ch01 and ch03 is
  referenced in the text before it appears. Terminology is consistent with ch02's term list,
  including the Precision/الضبط versus Accuracy/الدقة distinction ch01 §1.5 repeats.
- Front matter (Arabic and English title, abstracts, ToC, lists, declaration and AI-assistance
  disclosure) does not exist yet and is blocked on the university regulations (protocol OQ2); it
  belongs to a separate part and is not counted against these three chapters. This is the reviewer
  open question 1 from the skill's project context and remains unresolvable here.

## Overall

Decision: **revise**. Chapters 1 and 2 are gate-ready — chapter 1's claim ledger is complete and
every one of its 32 rows survived a hash recomputation and a content check, the hypothesis and all
six criteria are reproduced character for character from `plan.md`, the verdicts are stated without
softening or inflation, and the corrected cold-start facts are either stated correctly or absent.
Chapter 3 is not, for three reasons: it has **no claim-ledger rows at all**, so none of its 74
numeric sentences is hash-bound (B1); two of its closed lists are contradicted by the protocol
section they name, and the omitted OQ7 is the one open question that could put the cold-start
filter design in doubt (B2); and it states a reproducibility record that does not disclose the two
code trees or the prefix hash that chapter 4 correctly discloses (B3). What would change the
decision: a `C3.*` (and, if the writers prefer, `C2.*`) block in `thesis/claim_ledger.csv` binding
chapter 3's quantitative sentences to `methodology/protocol.md`, `methodology/threats_to_validity.md`
and the receipted artifacts with real SHA256 values; correcting "D3 to D13" to D14 and "Six
questions" to eight with OQ7 and OQ8 carried in §3.11; and a short paragraph in §3.9 stating the
two code trees, the prefix hash and the post-hoc additions. None of the three touches a number, a
threshold or a verdict, and no hard constraint from `idea.md` is violated or unverified. This
verdict was written by hand with no tool validating it, which is a recorded deviation under rule 6.

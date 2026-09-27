# Front matter

Assembled by the Thesis Writer on 2026-09-25 (stage S8, assembly). Every quantitative sentence in
the abstract carries its claim-ledger id in a hidden comment; the rows are `C0.1` to `C0.9` in the
canonical ledger `thesis/claim_ledger.csv`.

**How to read the placeholders.** Everything only the candidate, the supervisor or the university
can supply is marked `[PLACEHOLDER — ...]`. No placeholder is filled with a guess, and none is
silently omitted. The university's thesis regulations are not in this project, so the page order,
the language of each part, the citation style, the page limits, the similarity-check statement and
the required wording of the declaration and the AI-assistance disclosure are all open
(`methodology/protocol.md` OQ2, `literature/open_questions.md` item 1).

---

## 1. Title page

| Field | Value |
| --- | --- |
| Title (English) | A Recommendation System for E-Learning Based on User Behaviour Analysis |
| Title (Arabic) | [PLACEHOLDER — Arabic title exactly as the approved proposal words it] |
| Subtitle, if the regulations allow one | An evidence-bound evaluation on the Open University Learning Analytics Dataset |
| Candidate | [PLACEHOLDER — candidate's full name as registered] |
| Student number | [PLACEHOLDER — registration number] |
| Supervisor | [PLACEHOLDER — supervisor's name and title; the project record names Dr. Bassel Al-Khatib as the proposal's supervisor, to be confirmed by the candidate] |
| Co-supervisor or examiner, if required | [PLACEHOLDER] |
| Degree | [PLACEHOLDER — degree exactly as awarded; the project record says MSc in Web Sciences] |
| Faculty, programme, department | [PLACEHOLDER] |
| University | [PLACEHOLDER — university's official name in both languages; the project record says Syrian Virtual University] |
| Submission date | [PLACEHOLDER — submission date in the calendar the regulations require] |
| Academic year or semester | [PLACEHOLDER] |
| Language of submission | [PLACEHOLDER — this draft is entirely in English; the proposal is Arabic with English terms, and the regulations decide the language of each part] |

---

## 2. Abstract (English)

Hybrid recommenders are expected to help learners with least history most, yet are rarely tested on public learner-behaviour data with an explicit new-learner condition. This thesis asks whether a hybrid of content-based filtering (CBF), item-based collaborative filtering (CF) and a behavioural proxy outranks either technique alone, for learners with history and for new ones.

The data are the Open University Learning Analytics Dataset: 32,593 learner rows, 22 module presentations of 7 modules, 27,212 warm learners. <!-- C0.1 -->
The cold-start slice holds 5,444 learners, simulated by truncating visible history to two items and refitting every quantity without them. <!-- C0.2 -->
The method is pre-registered: identical time-based splits, Precision@10 at K = 10, six binary criteria fixed before any run, and paired exact Wilcoxon tests with Holm correction over the 22 presentations.

C1 is **met**: on warm users the hybrid gains a median +31.20% over CBF and +10.68% over CF, at Holm-corrected p of 0.011857 and 0.014095. <!-- C0.3 -->
C2 and C3 are **not met**: on new learners it loses a median 30.28% to CBF while gaining 7.32% over CF, both at p_holm 0.000241, and 2 of 22 presentations pass all four C3 conjuncts. <!-- C0.4 -->
C4, C5 and C6 are **met**: no leakage conjunct failed, the run cost 1.0140 of 4.0 CPU-hours, and all six phase 1 values reproduced at exactly 0.0 difference. <!-- C0.5 -->
The phase 1 pilot, unreceipted prior evidence, reported the opposite cold-start pattern: a median +73.12% gain over CBF and a median −17.90% loss to CF, in 22 of 22 presentations each. A further exploratory contrast shows that the direction of this inversion tracks the evaluation split, not the cold-start construction: holding the split fixed, changing the construction reverses the sign of no median comparison, while holding the construction fixed, changing the split reverses both. The reproduction on EEE_2014J rules out a difference in the pilot's arithmetic there; the corrected construction still changes the median size of the cold-start gain against CF (+7.32% under the refit condition against +13.34% under the pilot's construction), a difference between medians only — the paired per-presentation shift has a median of about +0.01 percentage points (11 up, 11 down) and can be large in a single presentation (for example AAA_2014J, about −53 percentage points). <!-- C0.6 -->
An exploratory post-hoc check qualifies the half of C2 that passed: on new learners only CBF clearly beats a random floor, and the hybrid is indistinguishable from it. <!-- C0.7 -->

The hypothesis is partially supported: the warm half holds, the cold-start half is refuted against CBF, and the behavioural-signal clause is unchecked, since no dwell time is recorded and no behavioural component was built. <!-- C0.8 -->
Bounds: two filters remove 2,016 of 29,228 logged learners towards engaged learners, cold start is simulated, the 22 presentations are 7 modules, and the cohort is one UK institution's. <!-- C0.9 -->

*Length: 454 words, counted from this section with the hidden ledger ids and this note excluded. The
brief asked for about 250. The excess is the six criterion verdicts, the pilot's own cold-start
result stated before the contrast that bears on it (the abstract must state the inversion itself
before referring to it), the median-only framing of the construction's effect with its paired
caveat, and the random-floor qualification, each of which the gate requires stated exactly, at one
sentence apiece; cutting further means dropping a verdict or a caveat. The regulations may cap the
abstract (`[PLACEHOLDER — abstract length limit]`); if a hard 250 is required, the pilot's
cold-start sentence and its contrast, and the random-floor sentence, are the ones the candidate
should decide about first, and all are in chapter 5.*

## 2a. Abstract (Arabic)

[PLACEHOLDER — Arabic abstract. Not drafted here: the regulations decide whether an Arabic abstract
is required and at what length, and a translation of quantitative claims should be checked by the
candidate against chapter 2's Arabic terminology (Precision = الضبط, Accuracy = الدقة, both proposed
and awaiting the supervisor's confirmation).]

---

## 3. Keywords

**English:** e-learning recommendation; hybrid recommender system; content-based filtering;
collaborative filtering; cold start; learner behaviour analysis; Precision@10; offline evaluation;
OULAD; pre-registered criteria; negative result.

**Arabic:** [PLACEHOLDER — Arabic keywords, to be taken from the proposal's own keyword list and
chapter 2's terms table.]

---

## 4. Declaration and AI-assistance disclosure

### 4.1 Declaration

[PLACEHOLDER — the university's required declaration wording, verbatim. The regulations are not in
this project and no declaration text may be invented.] The candidate's declaration is expected to
cover at least: that the thesis is the candidate's own work; that all sources are acknowledged; that
the work has not been submitted for another degree; and the outcome of the similarity check
`[PLACEHOLDER — similarity tool, threshold and report]`.

### 4.2 AI-assistance disclosure (draft, true to what happened)

Parts of this thesis were produced with the assistance of AI agents working under a fixed set of
project standards that define the stages, the gates, the evidence rules and the review process.
Specifically: the literature search, screening and reference ledger (stage S2); the methodology,
the statistics plan and the threats-to-validity register (stage S3); the experiment code, its
execution and the analysis of its results (stages S4 to S7); and the drafting of the chapters and
this front matter (stage S8) were drafted by AI agents. Every stage was then reviewed at a gate by
an independent reviewer running on a different model identity from the agent that produced the
artifact, and each gate verdict is on file under `reviews/`. Every number in the text is bound to a
file and its SHA256 hash in `thesis/claim_ledger.csv`, and the experiment runs are bound to receipts
under `results/run_receipts/`. The human candidate took and owns every decision about the research
question, the hypothesis, the success thresholds, the dataset, the scope reductions, the ethics and
the submission itself; those decisions are logged with their dates in `decisions.log`. No AI agent
approved its own work, and no criterion or threshold was changed after a result was seen.

[PLACEHOLDER — the university's required AI-use disclosure wording, verbatim, and its required
placement. Until it is supplied this section is a truthful account, not a compliant disclosure.]

**Note for the candidate.** Two project files scope this disclosure differently; the disagreement is
set out in the consistency-sweep section at the end of this file, and it is the candidate's to
resolve, not this document's.

---

## 5. Acknowledgements

[PLACEHOLDER — acknowledgements. Nothing is drafted here: who is thanked, and in what terms, is the
candidate's alone. If the regulations require the supervisor, the institution, a funder or a data
provider to be acknowledged in set words, that wording belongs here; note that the Open University
Learning Analytics Dataset is used under CC BY 4.0 and its attribution requirement is discharged in
chapter 3's data statement rather than here.]

---

## 6. Table of contents

Generated from the chapter files as they stand on 2026-09-25. Page numbers are not shown: this draft
has no fixed pagination until the regulations set the page format
(`[PLACEHOLDER — page numbers]`).

| Section | Title |
| --- | --- |
| — | Title page |
| — | Abstract (English); Abstract (Arabic) `[PLACEHOLDER]` |
| — | Keywords |
| — | Declaration and AI-assistance disclosure |
| — | Acknowledgements `[PLACEHOLDER]` |
| — | Table of contents; List of tables; List of figures; Terms and abbreviations |
| **1** | **Introduction** |
| 1.0 | Purpose of this chapter |
| 1.1 | Introduction |
| 1.2 | Scientific problem and justification (1.2.1 the problem in the proposal's terms; 1.2.2 why it is a research problem; 1.2.3 the problem as this thesis states it) |
| 1.3 | Research objective (1.3.1 the overall objective; 1.3.2 the four sub-objectives; 1.3.3 scope decisions with their reasons; 1.3.4 what the pre-registered criteria can and cannot test) |
| 1.4 | Expected practical results |
| 1.5 | Terms and definitions |
| 1.6 | Research questions, hypothesis and success criteria (1.6.1 the hypothesis; 1.6.2 the research questions; 1.6.3 the success criteria; 1.6.4 the design in brief) |
| 1.7 | Contributions (1.7.1 what the thesis found, in brief) |
| 1.8 | Thesis outline |
| 1.9 | What this chapter established |
| **2** | **Literature review and background** |
| 2.0 | Purpose of this chapter |
| 2.1 | Terms and definitions |
| 2.2 | Recommender foundations |
| 2.3 | Learner behaviour analytics and student profiling |
| 2.4 | Sequence and neural methods |
| 2.5 | E-learning and MOOC recommenders |
| 2.6 | Offline evaluation practice |
| 2.7 | Documented pitfalls |
| 2.8 | Related work |
| 2.9 | The gap this thesis fills |
| 2.10 | What this chapter established |
| **3** | **Methodology** |
| 3.0 | What this chapter establishes |
| 3.1 | Research design (3.1.1 the success criteria, copied from the approved plan) |
| 3.2 | Dataset |
| 3.3 | Variables (3.3.1 recorded scope reduction: the behavioural signal) |
| 3.4 | Preprocessing and the choice of module presentation (3.4.1 who is left, and what that means for every later number) |
| 3.5 | Split rule and cold-start slices (3.5.1 the split; 3.5.2 the cold-start slices; 3.5.3 the task and the candidate set) |
| 3.6 | Models compared and the hybrid's design |
| 3.7 | Metrics (3.7.1 the ceiling on the primary metric) |
| 3.8 | Variance and significance plan |
| 3.9 | Hardware, reproducibility and time budget |
| 3.10 | Ethics and data statement |
| 3.11 | Recorded scope reductions and open questions |
| 3.12 | What this chapter established, and what chapter 4 needs from it |
| **4** | **Implementation and experiments** |
| 4.0 | Purpose of this chapter |
| 4.1 | System architecture |
| 4.2 | Technology stack |
| 4.3 | Code structure and the stage entry contract (4.3.1 files by module; 4.3.2 the stage entry contract; 4.3.3 what one main run does for one presentation) |
| 4.4 | Pilot design and execution history (4.4.1 the phase 1 pilot; 4.4.2 the five weaknesses and the mechanism that answers each; 4.4.3 design and code reviews before any receipted result existed; 4.4.4 the scale-up decision and the phase 2 build) |
| 4.5 | Phase 2 as realised in code (4.5.1 the models and the blend; 4.5.2 defaults chosen where the protocol was silent) |
| 4.6 | Execution and receipts (4.6.1 the three runs; 4.6.2 how the receipts were made, and what that does and does not prove; 4.6.3 the phase 1 reproduction under a receipt; 4.6.4 compute and hardware; 4.6.5 the main run and the evidence about leakage; 4.6.6 two facts a reader who re-hashes will meet) |
| 4.7 | The two post-hoc diagnostics |
| 4.8 | Run environment and reproducibility instructions |
| 4.9 | What this chapter established, and what chapter 5 needs from it |
| **5** | **Results and discussion** |
| 5.0 | What this chapter establishes |
| 5.1 | What was run, and how to read these numbers (5.1.1 the two receipted runs; 5.1.2 the population these numbers describe; 5.1.3 how to read a Precision@10 here; 5.1.4 Module D: the behaviour of the evaluated population, and what RQ1 can be answered from it) |
| 5.2 | The warm-user slice |
| 5.3 | The cold-start-refit slice (5.3.1 criterion C3, conjunct by conjunct; 5.3.2 the random floor, and what the cold-start numbers are worth) |
| 5.4 | The central finding (5.4.1 the phase 1 pilot reported the opposite pattern, and what the receipted cells show) |
| 5.5 | Every success criterion, judged as written |
| 5.6 | How far the result generalises (5.6.1 across the 7 modules; 5.6.2 across alternative splits and filters) |
| 5.7 | Iteration history, and the cause of each change (5.7.1 phase 1, the pilot; 5.7.2 phase 2, the methodology; 5.7.3 phase 2, the code; 5.7.4 phase 2, the runs and the reported numbers; 5.7.5 the post-hoc diagnostics, and one withdrawn explanation) |
| 5.8 | The two post-hoc diagnostics (5.8.1 D1: the fitted blend weight on cold start; 5.8.2 D2: removing the behavioural columns from the blend's feature set; 5.8.3 the exploratory association check) |
| 5.9 | Comparison with the literature, under chapter 2's caveats |
| 5.10 | Threats to validity |
| 5.11 | Limitations |
| 5.12 | What this chapter established |
| **6** | **Conclusions and future work** |
| 6.0 | What this chapter establishes |
| 6.1 | Answers to the research questions (RQ0, RQ1, RQ2, RQ3, RQ4) |
| 6.2 | Contributions, restated against the evidence |
| 6.3 | The hypothesis |
| 6.4 | Practical implications for e-learning platforms |
| 6.5 | Future work |
| 6.6 | What would count as evidence against these conclusions |
| 6.7 | What this chapter established |
| — | References `[PLACEHOLDER — rendered from literature/references.bib in the required citation style]` |
| — | Appendices `[PLACEHOLDER — not yet written: reproducibility appendix, extended result tables, data licence text, code listing pointer]` |

---

## 7. List of tables

**Number-order caveat, stated because the numbers are not in reading order.** Tables 5.1 to 5.5 are
the Results Analyst's tables and keep the numbers they were produced with. Tables 5.6 to 5.12 were
added by chapter 5 afterwards, from the same artifacts, and were numbered in order of their first
appearance so that 5.1 to 5.5 would not move. Table 5.13, the Module D behaviour table, was added
last of all at the critic's request and appears earliest of the chapter's tables, in section 5.1.4.
Table 5.14, the Condition A versus Condition B contrast, was added after cycle 3's review and
appears in section 5.4.1, between Table 5.5 and Table 5.3 in reading order.
The chapter therefore reads 5.13, 5.1, 5.2, 5.6, 5.5, 5.14, 5.3, 5.7, 5.8, 5.9, 5.10, 5.11, 5.12. **This
list is in order of appearance, not in numeric order**, and chapter 5's header states the same
convention. If the regulations require a numeric list, the tables need renumbering in one pass
before submission; Table 5.13 is the strongest argument for doing so.

| Table | Title | Appears in |
| --- | --- | --- |
| 1.1 | Where each section of the approved proposal is carried in this thesis | ch. 1 |
| 1.2 | The four sub-objectives of the proposal, the question that answers each and its status | ch. 1 |
| 1.3 | The proposal's expected practical results and what this thesis measures for each | ch. 1 |
| 1.4 | Terms used in this chapter, with the Arabic used in chapter 2 and the meaning in this thesis | ch. 1 |
| 1.5 | The six pre-registered success criteria, copied from the approved plan | ch. 1 |
| 1.6 | Which criteria answer which research question | ch. 1 |
| 1.7 | Contributions and the chapter that delivers each | ch. 1 |
| 1.8 | Structure of the thesis | ch. 1 |
| 2.1 | Terms and definitions: the proposal's terms with two corrections and one addition | ch. 2 |
| 2.2 | Related work: the nine reviewed papers and later peer-reviewed work, each result with its task | ch. 2 |
| 3.1 | Population per module presentation | ch. 3 |
| 3.2 | What each condition was fitted on, and what it can claim | ch. 3 |
| 4.1 | Technology stack: what was used, for what, and how it compares with the proposal's list | ch. 4 |
| 4.2 | Code structure by module of the plan | ch. 4 |
| 4.3 | The stage entry contract of `code/main.py` | ch. 4 |
| 4.4 | The five named weaknesses of the pilot, the mechanism that replaces each, and the criterion it serves | ch. 4 |
| 4.5 | Independent reviews before the main run, with the blockers each raised | ch. 4 |
| 4.6 | Implementation defaults chosen where the protocol was silent | ch. 4 |
| 4.7 | The three receipted runs | ch. 4 |
| 4.8 | Hash record | ch. 4 |
| 4.9 | The six phase 1 Precision@10 values on EEE_2014J, regenerated by the reproduction | ch. 4 |
| 5.13 | Module D: behavioural feature distributions and k = 4 learner segments, all 22 module presentations (descriptive, decides no criterion) | ch. 5, §5.1.4 |
| 5.1 | Precision@10, warm-user slice, primary time-based split, all 22 module presentations | ch. 5, §5.2 |
| 5.2 | Precision@10, cold-start-refit slice (k = 2), primary time-based split, all 22 module presentations | ch. 5, §5.3 |
| 5.6 | Criterion C3 conjunct by conjunct, cold-start-refit slice (k = 2), all 22 module presentations | ch. 5, §5.3.1 |
| 5.5 | Every model against the random floor, cold-start-refit slice (exploratory) | ch. 5, §5.3.2 |
| 5.14 | Cold-start construction (Condition A refit vs. Condition B shared similarity) crossed with split (primary vs. tertiary), hybrid against CBF and ItemKNN-CF, all 22 module presentations (exploratory, family F4; decides no criterion) | ch. 5, §5.4.1 |
| 5.3 | Every pre-registered success criterion judged as written, with its measured value and artifact | ch. 5, §5.5 |
| 5.7 | Hybrid relative gain per module, both slices, 7 modules | ch. 5, §5.6.1 |
| 5.8 | Median relative gain under each alternative split and item filter (exploratory) | ch. 5, §5.6.2 |
| 5.4 | Post-hoc diagnostics D1 and D2, all 22 module presentations (the Analyst's table; reproduced in chapter 5 as Tables 5.9 to 5.12) | cited in ch. 5, §5.8 |
| 5.9 | Fitted blend weight alpha on the cold-start-refit cell (k = 2), per presentation | ch. 5, §5.8.1 |
| 5.10 | D2 behavioural-feature ablation, warm-user slice | ch. 5, §5.8.2 |
| 5.11 | D2 behavioural-feature ablation, cold-start-refit slice (k = 2) | ch. 5, §5.8.2 |
| 5.12 | Exploratory Spearman associations with the hybrid-versus-CBF cold-start gain | ch. 5, §5.8.3 |

Chapter 6 contains no tables. The Analyst's source files for Tables 5.1 to 5.5 are under
`thesis/tables/`; the figures' captions are in `thesis/figures/captions.md`.

---

## 8. List of figures

| Figure | Title | Appears in | File |
| --- | --- | --- | --- |
| 4.1 | Architecture of the pipeline and the plan module that owns each step | ch. 4, §4.1 | drawn in the text |
| 5.1 | Hybrid Precision@10 relative gain over each baseline on warm users, one point per module presentation | ch. 5, §5.2 | `thesis/figures/figure_5_1_warm_relative_gain_spread.png` |
| 5.2 | Hybrid Precision@10 relative gain over each baseline on cold-start-refit learners, one point per module presentation | ch. 5, §5.3 | `thesis/figures/figure_5_2_coldstart_relative_gain_spread.png` |
| 5.3 | Fitted blend weight alpha on the cold-start-refit cell, per module presentation (post-hoc) | ch. 5, §5.8 | `thesis/figures/figure_5_3_alpha_distribution.png` |

---

## 9. Terms and abbreviations

The Arabic renderings are chapter 2's; the two marked **proposed** await the supervisor's
confirmation. Where a word differs from the approved proposal's, chapter 2 says why.

| Abbreviation or term | Meaning as used in this thesis | Arabic |
| --- | --- | --- |
| CBF | Content-based filtering: ranks items similar to those the learner already used, from item features | التصفية على أساس المحتوى |
| CF | Collaborative filtering; here **ItemKNN-CF**, item-based cosine similarity over the learner–resource matrix | التصفية التعاونية |
| Hybrid | The model under test: a score-level linear blend of CBF and CF whose weight is fitted on validation data | نظام التوصية الهجين |
| MostPop | Global popularity baseline, ranked by the number of distinct training learners who used a resource; C3's popularity floor | — |
| PopWeek | Week-aware popularity baseline; reporting only, decides no criterion | — |
| Random | Uniform random ranker over the candidate set, mean of five seeds 42 to 46; reporting floor, decides no criterion | — |
| P@10, Precision@10 | Proportion of the ten recommended resources that are relevant, at K = 10; the primary metric | الضبط عند 10 (**proposed**) |
| Accuracy | Proportion of correct decisions; used only when quoting a source that reports it, never for Precision | الدقة (**proposed**) |
| Recall@K, NDCG@K, HitRate@K, MRR@K | Additional ranking metrics reported beside Precision@10; they decide no criterion | الاستدعاء (Recall) |
| alpha (α) | The blend weight the hybrid uses: score = α × CF + (1 − α) × CBF, so α is the weight on the collaborative component | — |
| Warm slice, `warm|None` | The held-out slice of learners evaluated with their full training history | — |
| Cold start | A learner with no or very few interactions | البداية الباردة |
| `A|2`, cold-start-refit slice | The primary cold-start condition: visible history truncated to k = 2 items **and** every fitted quantity rebuilt without the held-out learners. Decides C2 and C3 | — |
| Condition B | The secondary cold-start condition: thin visible history on a shared similarity matrix, labelled optimistic; decides nothing | — |
| k | Number of visible items left to a cold-start learner; k = 2 throughout the deciding cell | — |
| K | Cut-off of a ranking metric; K = 10 for the primary metric | — |
| OULAD | Open University Learning Analytics Dataset, the public UK Open University dataset used here, CC BY 4.0 | — |
| Module presentation | One run of one module in one term, for example EEE_2014J; the replication unit, 22 in total over 7 modules | — |
| C1 to C6 | The six pre-registered success criteria, frozen in `plan.md` before any phase 2 run | — |
| G1 to G10 | The project's review gates; G7 is the chapter gate | — |
| F1 to F4 | The four pre-declared families of comparisons; Holm correction is applied within a family, and F4 is exploratory | — |
| Holm correction | Step-down multiple-comparison correction applied within each declared family | — |
| Wilcoxon signed-rank | The pre-registered paired test over the 22 presentations, exact, two-sided | — |
| Ceiling P@10 | The highest Precision@10 any ranker could reach given how few held-out items a learner has | — |
| VLE | Virtual learning environment, the platform whose logs OULAD records | البيئة التعليمية الافتراضية |
| RNN, CNN, RBFNN | Recurrent, convolutional and radial-basis-function neural networks; named in the proposal, deferred scope-outs here, not run | الشبكة العصبية المتكررة، الشبكات العصبونية التلافيفية، الشبكة العصبية ذات الأساس الشعاعي |
| Claim ledger | `thesis/claim_ledger.csv`: one row per quantitative claim, binding it to a file and that file's SHA256 | — |
| Receipt | A JSON record under `results/run_receipts/` carrying a run's command line, code-tree hash, artifact hashes, seeds and timings | — |
| Post-hoc | Measured after the criteria were closed; may not revise a criterion, threshold, model or the protocol | — |

---

## 10. Consistency-sweep leads for the candidate

These are reported, not resolved: the files named belong to other roles or are frozen, and this
document does not edit them.

### Lead 1 — the AI-disclosure scope: `methodology/data_statement.md` §7 versus `literature/open_questions.md` item 4

They disagree in **scope**, in **status** and in **which open question owns it**.

- `methodology/data_statement.md` §7 discloses AI assistance across the **whole research process** —
  it names stage S2 (literature search and ledger), stage S3 (methodology and chapter 3), stages S4
  to S7 (code, execution, results analysis) and stage S8 (the chapter drafts) — states that each
  stage was gate-reviewed by a different model identity, and that the human owns every research
  decision. It then marks itself `unverified` and a **placeholder to be replaced**, attributing the
  open item to **OQ2**, the university-regulations question.
- `literature/open_questions.md` item 4 asks only for "AI-assistance disclosure wording for the
  **references and methods sections**". That scopes the disclosure to two sections of the thesis, it
  asks only about **wording**, and it does not mention the whole-process scope, the gate review, the
  `unverified` status or OQ2.

Read together they could be taken to mean that only the references and the methodology need a
disclosure, which is narrower than what happened: agents drafted chapters 1 and 4 to 6 as well.
The decision is the candidate's, and it has one dependency: the university's regulations fix both
the wording and the placement, so the two files cannot be reconciled definitively until OQ2 is
answered. What can be done now without a ruling is to make item 4 point at §7 and adopt §7's
whole-process scope, so that a reader of either file reaches the same claim. Section 4.2 above is
drafted to §7's scope for that reason.

### Lead 2 — `methodology/protocol.md` line 203, the "cold-start prior" wording

The variables table row "Behavioural session signal" still lists its use as "Module D features,
**cold-start prior**, learned blend features". A cold-start prior fitted from behavioural segments
does not exist in this study: chapter 3 §3.1 and the protocol's own clarifying note immediately
below the table (dated 2026-09-24, cross-artifact fix I1, recorded as deviation D14 and open
question OQ8) state that Module D is descriptive only, that it feeds no model, and that RQ2 as
`plan.md` words it is not answerable from this design. Chapters 5 and 6 say the same.

So the contradiction is already **disclosed and bounded** three lines later, and no number depends
on it. The residual risk is purely one of reading order: an examiner who reads the table cell and
not the note below it will believe a cold-start prior was built. Two options, both the
methodologist's to apply rather than mine: strike "cold-start prior" from the cell and leave the
note as the record of why, or mark the cell "cold-start prior (see the clarifying note below: not
implemented)". The frozen `plan.md` keeps its own wording either way.

### Lead 3 — smaller items already logged, listed so the sweep is complete

- Chapter 1 §1.7.1 previews the cold-start result without the random-floor qualification that
  chapter 5 §5.3.2 and chapter 6 now carry; the two parts read differently on the same finding.
- The G7 review's warning W5 says "six tables" and enumerates seven; all seven are now numbered
  (5.6 to 5.12), so the gate record and the chapter disagree on the count.
- No appendices exist yet, and the reproducibility appendix the standards ask for is the one place
  the receipts, seeds and commands would be gathered for a reader who re-runs the work.

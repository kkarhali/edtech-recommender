---
blockers_count: 0
warnings_count: 4
files_reviewed: n/a (this gate reviews documents: literature/ledger.csv, references.bib,
  search_log.md, screening_records.csv, open_questions.md, literature/notes/ (39 files),
  thesis/ch02.md, plan.md, idea.md, plus the nine source PDFs under
  src/reasearch_topic/References/ and the proposal .docx, opened directly)
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: claude-opus-5
model_identity: claude-opus-5, tier=top for this dispatch. Independence from the producer is
  not assumed: `state.md` `## agents` records `literature_scholar: ... skill=thesis-literature-scholar
  tier=mid` for unit u05_s2_literature and `reviewer: status=running unit=u06_g2_literature_gate
  skill=thesis-reviewer tier=top, model distinct from the scholar's`, and the manager's dispatch
  for this unit states the same. I am that tier=top dispatch and wrote none of the artifacts
  below, so independence is verified from the project's own state file and the dispatch, not
  guessed.
mode: literature_gate
unit: u06_g2_literature_gate
cycle: 0
---

# Review

**Deviation notice (per SKILL.md and rule 6):** the review MCP tool
(`ar-runtime/scripts/ar-gemini-review-mcp.ts`) cannot run on this machine because its
persistence step shells out to `ar-workflow-engine.py`, which imports `fcntl`. This file was
written by hand with `Write`, and `ar-review-contract.ts`'s `validateConstraintAudit` rules were
run against this draft by me rather than by the tool. That is a recorded deviation, not a
silently-passed check.

**What I verified myself, rather than reading the scholar's own summary of it.** I opened all
nine source PDFs under `src/reasearch_topic/References/` with `pdftotext` and checked title,
authors, year, venue, DOI and every number chapter 2 draws from them; I opened the proposal
`.docx` and read its Arabic terms table directly; I recounted `literature/screening_records.csv`;
and I re-ran the scholar's own checker as a cross-check. Result of the checker, run as
instructed (`PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python scripts/check_ledger.py
--project-root <project_root>` inside the `thesis-literature-scholar` skill folder):
`RESULT: PASS (39 ledger rows, 0 errors, 0 warnings)`, exit 0. Zero warnings means every ledger
row is also cited in chapter 2 and every BibTeX key resolves one-to-one.

Ledger rows I opened and confirmed against the source itself (9 of 39, weighted to the rows
carrying the numbers chapter 2 relies on):

| Key | Checked against the PDF | Outcome |
| --- | --- | --- |
| `kumar2023session` | Title, 3 authors, 30Music, Tables 2-4 | Exact. RNN P@5/10/20 = 0.095/0.064/0.042, V-SKNN 0.195/0.159/0.112, IKNN highest on Recall and MRR. The PDF's own text (p.10) claims the RNN "gives better results in terms of precision" at N=5; its Table 2 does not. The ledger's `comparability_note` says exactly this |
| `gao2022cnn` | Front matter, Table 2, section 3.1 | Exact. P@5 0.39 vs Hybrid 0.23 and Ensemble 0.26; 500 crawled CourseTalk learners, 100 test users; DOI 10.1155/2022/9054149, Wireless Communications and Mobile Computing vol. 2022, art. 9054149 |
| `huang2019amre` | Author block, section IV-D, Table 7 | Exact. Qi Huang et al., IEEE Access, DOI 10.1109/ACCESS.2019.2891561. Text: best Accuracy, Recall, F1, "lower in Precision"; Table 7 ML943u(0.2) AMRE 0.8808, rank (12) of 12, best 0.9463 |
| `zhang2015hybrid` | Front page | Exact. Heng-Ru Zhang, Fan Min, Xu He, Yuan-Yuan Xu; Mathematical Problems in Engineering vol. 2015, art. 145636, 11 pp.; DOI 10.1155/2015/145636. Comparator is a random recommender |
| `chaudhary2019elearning` | Front page, abstract, Fig. 7 | Exact. Kamika Chaudhary, Neena Gupta; IJMEMS vol. 4 no. 4, 957-967, 2019; DOI 10.33889/IJMEMS.2019.4.4-076; RF 98.98%, SVM 42%, KNN 63%, NB 66%; task is URL prediction from a keyword |
| `degemmis2004hybrid` | Citation footer, section 4, Table 4, p.8 | Exact. ICEIS 2004 pp. 162-169, DOI 10.5220/0002638201620169; 380 users, 154 products; UPE 0.421/0.066/0.923 vs U(PE)2 1.936/0.099/0.839; 5h47m vs 2h24m total |
| `liang2017profile` | Front page, Table 4 | Exact. Six authors as listed; J. Electrical and Computer Engineering vol. 2017, art. 9720396; accuracy 99.6/99.5/99.7, precision 50.0/65.0/64.3, recall 88.9/76.5/81.8 |
| `sabitha2022uirs` | Front page, sections 4-5 | Exact. Four authors as listed, DOI 10.32604/iasc.2022.018985, IASC; 120 customer samples, TARS and KRS comparators, mean error 0.00755, results in figures only |
| `ansari2016coders` | Front page, section V | Exact. "CodERS: A Hybrid Recommender System for an E-learning System", four authors, ICSPIS 2016 Tehran 14-15 Dec 2016; "12 randomly selected users", results described as satisfactory, no numbers |

Nine of nine agree with the ledger on title, authors, year, venue, DOI and on every number.
I found no row where the ledger overstates its source.

## Blockers (must fix before proceeding)
None.

## Warnings (should fix)
- [W1] <severity:med> `thesis/ch02.md` section 2.6, last sentence: "the splits are random per
  user, last-session or 70:30" citing `kumar2023session`, `chaudhary2019elearning` and
  `liang2017profile`. Two of the three descriptors are right (Kumar holds out each user's last
  session; Chaudhary is 70:30), but "random per user" fits none of the three. Liang's paper says
  "the data set is divided into training set, validation set, and test set randomly; the ratio is
  3 : 1 : 1" (PDF p.6, section 5) — a random split over samples, not per user — and the ledger's
  `dataset`/`method` fields for that row do not record a split at all, so the phrase is not
  traceable to a ledger entry either. Per-user random withholding is what `degemmis2004hybrid`
  does (25% of each test user's ratings, PDF section 4), and that row is not cited here. Fix the
  descriptor or move the citation.
- [W2] <severity:med> `literature/search_log.md:127` and the "Sources that could not be opened"
  table: three different counts of the unopened sources sit in the same stage and none of them
  is reconciled in writing. The table has 15 data rows; `thesis/ch02.md` section 2.8 and
  `literature/open_questions.md:2` both say "14"; the screening block says
  `not_retrievable = 11`, which `screening_records.csv` confirms exactly (438 rows =
  413 excluded_title_abstract + 13 included + 11 full_text_not_retrieved + 1
  excluded_full_text). The reconciliation does exist — 15 rows minus `furini2022twins`,
  `mauro2022autism` and the Adomavicius snowball candidate (none of which entered through the
  search stream) minus the `wired.com` row (which records that no item was ever selected) leaves
  the 11 — but it is nowhere written down, and line 127 points at a counter, `sources_unreachable`,
  that does not exist in the counts block. An examiner who tries to make 15, 14 and 11 agree will
  not be able to. State the reconciliation in the search log and make the table's row count and
  the chapter's "14" refer to the same thing.
- [W3] <severity:med> `thesis/ch02.md` sections 2.8 and 2.9: the chapter names the unopened
  sources as "an OULAD benchmark review and ACM and IEEE items". The two unopened items that
  most directly threaten this particular gap are neither ACM nor IEEE: Bhaskaran et al. 2021,
  "cluster-based hybrid e-learning recommender" (doi 10.3390/math9020197) and Wu et al. 2023,
  "hybrid MOOC recommendation with dynamic preferences" (doi 10.3390/app13095548), both MDPI,
  both HTTP 403 (search log, unreachable table). The gap paragraph is correctly hedged and even
  names its own defeater ("the unopened items in the search log are the first place to look"),
  so this is not a false claim — but naming the OULAD review and "ACM and IEEE items" while
  leaving the two unopened hybrid e-learning recommenders unnamed understates the risk at
  exactly the sentence where a supervisor will press. Name them.
- [W4] <severity:low> `thesis/ch02.md` section 2.7 lists four ways the proposal's summaries
  misread their own papers and fixes each in the text; `literature/search_log.md`'s metadata
  table logs a fifth, `gao2022cnn` ("lower course dropout vs baselines" in the abstract, while
  the experiments score truancy prediction). Chapter 2 handles this one only by omission: it
  never repeats the dropout claim, and the section 2.8 row says "truancy prediction also
  scored", but it never tells the reader the abstract's claim is not what was measured. I
  confirmed the discrepancy in the PDF (abstract claims "lower course dropout rate"; section 4.1
  defines Precision@W/Recall@W over the truancy course sequence). Surface it alongside the other
  four, or the pitfalls list reads as complete when it is not.

## Constraint Audit
- [HC1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not
  assume a multi-GPU cluster." (`idea.md:47-48`) | status: satisfied | evidence: this unit ran
  no compute; `thesis/ch02.md` section 2.4 "What this means here" carries the constraint into the
  review itself — "Phase 2 has a single-CPU budget and no deep model ... RNN, CNN and RBFNN are
  reported as reserved for later work and not as baselines" — so the literature stage narrows
  rather than widens the compute envelope | blocker: none
- [HC2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot."
  (`idea.md:56`) | status: satisfied | evidence: `find data/projects/e_learning_thesis -type f
  -size +5M` returns nothing; the stage's only downloads were open article copies, and every
  ledger row that used one records "(open copy fetched 2026-09-20, not stored in the project)" |
  blocker: none
- [HC3] Network access for the one OULAD download (`idea.md:40-41`, carried as "network limited
  to the one OULAD download") | status: satisfied | evidence: idea.md's sentence is scoped to the
  experiment ("requires network access **during the pilot** to download OULAD once"), and this
  unit downloaded no dataset: `inputs/manifest.json` already hashes the eight OULAD files and no
  new data file entered the project. The stage's web use was bibliographic search, which the
  standards require of S2 and which `literature/search_log.md` logs query by query with its
  refusals (Scopus, ACM DL, ScienceDirect, MDPI, Hindawi/Wiley all HTTP 403). I record this
  scoping reading explicitly rather than leaving it implicit — see Notes | blocker: none
- [HC4] Pilot/time budget: "complete within a few hours of wall-clock time" (`idea.md:54-55`) |
  status: satisfied | evidence: no experiment ran in this unit and no results artifact changed
  (`results/` is empty); `thesis/ch02.md` section 2.10 hands chapter 3 only requirements that
  cost nothing extra to run (time-based split, refitted cold-start slice, popularity baseline,
  stated test unit) | blocker: none
- [HC5] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained
  and evaluated on identical splits so the comparison in success criterion 1 is fair."
  (`idea.md:57-58`) | status: satisfied | evidence: this unit produces no split and no code.
  Nothing in `thesis/ch02.md` or `literature/ledger.csv` weakens or renegotiates the rule; section
  2.6 and section 2.10 hand chapter 3 a stricter version of it (one time-based split rule, a
  cold-start slice built by refitting without the held-out learners, a stated test unit), and
  section 2.2 adds a non-personalised popularity baseline to the comparison set. `code_gate` must
  still re-trace the actual call chain before treating this as satisfied there | blocker: none
- [HC6] "Treat `src/reasearch_topic/References/*.pdf` and this idea file's cited papers as
  read-only background; do not attempt to re-scrape or redistribute their content."
  (`idea.md:59-60`) | status: satisfied | evidence: all nine PDFs still carry their original 2023
  mtimes (`ls -l --time-style=long-iso src/reasearch_topic/References`, dates 2023-10-13 to
  2023-10-22), so nothing was rewritten; `find data/projects/e_learning_thesis -iname "*.pdf"`
  returns nothing, so no copy was made into the project; the 39 files under `literature/notes/`
  are 1.0-2.7 KB each, paraphrase with page locators plus short quoted phrases, which is citation,
  not redistribution | blocker: none
- [HC7] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the
  most likely cause ... rather than adjusting the threshold after the fact." (`idea.md:28-30`,
  rule 3) | status: satisfied | evidence: the literature stage moved no threshold and invented no
  favourable number. The opposite: `thesis/ch02.md` section 2.2 records that the proposal's own
  hybrid "is less accurate than pure CF on all three accuracy measures reported" (I confirmed
  Degemmis Table 4: 0.421/0.066/0.923 for pure CF against 1.936/0.099/0.839 for the hybrid), and
  section 2.9 states outright "Nothing here says the hybrid will win". A literature chapter that
  weakens its own hypothesis where the sources say so is the behaviour rule 3 asks for | blocker: none

## Notes
- **Gate G2, condition by condition.** (1) Every ledger entry opened and its metadata verified:
  37 of 39 rows carry `verified=yes` with an `opened_on` date; the two that do not
  (`furini2022twins`, `mauro2022autism`) are handled below. Nine rows verified by me against the
  source, all exact. (2) Every chapter 2 claim cites a ledger entry: I scanned every non-heading
  line of `ch02.md` carrying a digit and found no attributive or quantitative sentence without a
  `<!-- ledger: ... -->` comment; the only uncited numeric lines are headings and forward-looking
  scope sentences about this thesis ("Every quantity in chapters 4 and 5 called Precision means
  Precision@10", the "What this means here" paragraphs), which are not claims about the
  literature. The checker independently confirms every cited key resolves to a ledger row. (3)
  Coverage: all nine reviewed papers appear in the section 2.8 table by name, and 21 of the 39
  rows are 2021 or later, spread across every theme the chapter uses. (4) Labelling: the four
  trade rows are `type=trade, peer_reviewed=no`, are confined to section 2.0 with "These four
  items report no reproducible method or metric and carry no weight in what follows", and appear
  in no table (checker's trade-in-table test passes; I re-read the tables to confirm). (5) Gap
  statement: section 2.9 closes the chapter, names what it is not, and names its own defeater.
  All five conditions pass.
- **The two unverified rows are handled as unverified everywhere they appear.** `furini2022twins`
  and `mauro2022autism` occur exactly once each in `ch02.md` (I counted), in the one sentence that
  says they could not be opened: "could not be opened (publisher returned HTTP 403 on every
  attempt); nothing in this chapter relies on them." Their ledger rows have `verified=no`, an
  empty `opened_on`, an empty `reported_result` and notes recording the exact 403 timestamps;
  their BibTeX entries carry `note = {Unreachable on 2026-09-20 (HTTP 403); metadata from the
  Crossref record only}`. Keeping an uncitable row with its failed-access record, rather than
  deleting it, is the correct reading of rule 6 — the item is marked `unchecked`, not quietly
  dropped and not quietly passed — so I do not treat the two unopened rows as a failure of the
  "every entry opened" condition.
- **The five proposal-versus-paper discrepancies the scholar reported are real, and chapter 2
  states four of them in the text.** I confirmed each against the PDF: the song RNN's own text
  claims a precision win its Table 2 contradicts (section 2.4 and pitfall 4 say so, with the
  0.095/0.195 pair); AMRE is best on accuracy, recall and F1 and rank 12 of 12 on precision
  (section 2.1 and pitfall 4); Zhang 2015's comparator is a random recommender, not a CBF-CF
  hybrid (section 2.2); Chaudhary and Gupta predict URLs from a keyword at 98.98% accuracy with no
  ranking (pitfall 3). The fifth, Gao's dropout-versus-truancy wording, is logged in the search
  log but not surfaced in the chapter — see [W4]. I also checked the two corrections the chapter
  makes to the proposal's own Arabic table by opening the `.docx` directly: the proposal does
  render Precision as "الدقة", and it does print "الشبكات العصبونية التلافيفية (التكرارية
  المتسلسلة)" for CNN. Both corrections are grounded, not asserted.
- **The gap statement claims only what the opened sources support.** Section 2.9 is scoped four
  separate times ("Among the sources opened", "Work on OULAD that I could open", "none of the
  sources opened evaluates", "The claim is about missing evidence in the sources opened") and
  ends with an explicit defeater plus a pointer to the unopened items. It does not claim novelty
  of hybridisation, CF, CBF, session models or the cold-start problem, and it says the literature
  gives reason to expect the hybrid may lose. [W3] asks only that it name its two nearest unopened
  threats.
- **Scope reading recorded for HC3.** I read idea.md's network sentence as scoped to the pilot's
  dataset access, because that is how idea.md writes it (line 41, "during the pilot") and because
  S2 cannot be performed at all without bibliographic search. I am recording the reading rather
  than leaving it implicit, so that if the coordinator or the human reads the constraint as a
  blanket network limit, this unit is where that disagreement surfaces, not chapter 6.
- **What I could not check, and what that costs.** This role has no web access, so for the 30
  ledger rows with no local PDF (`roy2022review`, `ji2023leakage`, `kuzilek2017oulad`,
  `sanguino2022course` and the rest) I verified internal consistency — ledger against
  `references.bib`, against `literature/notes/`, against the chapter's use of them, against the
  search log's access probes — but not the sources themselves. Their titles, authors, years and
  venues remain the scholar's record, not my finding, and I state that rather than implying I
  checked them. Two things reduce the residual risk: the nine rows I could open agreed exactly,
  including on numbers whose restatement would have been easy to shade; and the rows read at
  abstract level only (`jeevamol2021ontology`, `mohammadi2022rbf`, `dasilva2023educrs`) declare
  it in `notes` and are marked "(abstract)" in the chapter's own table.
- **The screening arithmetic reconciles exactly.** `screening_records.csv` has 438 data rows and
  its `decision` column tallies 413 + 13 + 11 + 1 = 438, matching every number in the search log's
  counts block. `13 + 4 + 7 + 15 = 39` matches the ledger's row count. The one place the numbers
  do not reconcile is the unopened-sources count, [W2].
- Chapter 2's RQ mapping in section 2.9 (RQ0 warm and cold against each single technique, RQ1 and
  RQ2 profiling, RQ3 validation-fitted blend weight, RQ4 significance across 22 presentations)
  matches `plan.md:78-91` question for question. The 22 module-presentations figure the chapter
  attributes to `kuzilek2017oulad` is independently corroborated by the project's own
  `inputs/prior_evidence/summary.md`, which reports 22 pairs.
- `literature/open_questions.md` puts the right six things in front of the human, including the
  OULAD licence (which matches the standing open question 2 in the reviewer's own skill: the
  licence is reported as stated by the descriptor and recorded as unverified, not accepted) and
  the Arabic glossary pair, which is correctly flagged as proposed rather than sourced.

## Overall
Approve. The five conditions of gate G2 all hold, and they hold under checking rather than on the
scholar's word: I opened all nine source PDFs and every one of them agreed with its ledger row on
title, authors, year, venue, DOI and on every number chapter 2 borrows, including the three places
where the honest number is the one that weakens this thesis's own hypothesis. The strongest single
reason to approve is that the chapter's hardest sentences are the correct ones — it reports the
song RNN losing to V-SKNN, AMRE ranking last of twelve on precision, and the proposal's own hybrid
being less accurate than pure CF, each of which I confirmed in the PDF, and it scopes its gap claim
to the sources it actually opened rather than to the literature at large. The two unreachable rows
are marked unverified, carry no result, and are cited exactly once, in the sentence that says they
could not be opened. The four warnings are a misdescribed split in one sentence, an unreconciled
count of unopened sources, two unnamed near-threats in the gap paragraph, and one logged
discrepancy that never reached the chapter; none of them changes what the chapter claims or what
chapter 3 inherits, so none blocks G2. This would change to `revise` if [W1] or [W4] were left for
the writer to inherit into the final chapter 2, where a misattributed split and an incomplete
pitfalls list stop being documentation issues and become claims an examiner can falsify.

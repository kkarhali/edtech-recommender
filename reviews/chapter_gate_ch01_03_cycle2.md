---
blockers_count: 0
warnings_count: 6
files_reviewed: n/a (documents: thesis/ch01.md 901bdeb8, thesis/ch02.md c53f598e, thesis/ch03.md f62a5dd1, thesis/claim_ledger.csv f8d9480b, plus the 14 artifacts the new rows cite)
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Opus 5
model_identity: claude-opus-5 (self-reported; the chapters and the 243 new ledger rows were produced by mid-tier writer/scholar/methodologist agents, so rule 1 independence holds)
mode: chapter_gate
unit: u15_g7_chapter_gate
cycle: 2
decision: approve_with_warnings
decision_vocabulary_note: in the skill's fixed vocabulary this is `approve`, with 6 warnings and 2 open items carried; it is not `revise`
---

# Review

Re-review of cycle 1's three blockers plus the eight warnings, on the chapter hashes the manager
named (all three confirmed by recomputation). Written by hand, no MCP tool validating it — the
recorded Windows deviation, rule 6. Nothing was edited. Rows citing `decisions.log` are exempt
per open item I5; as in cycle 1, no C1/C2/C3 row cites it, so the exemption did not apply.

## Blockers (must fix before proceeding)

None. All three cycle-1 blockers are resolved, and I verified each against the artifacts rather
than against the chapter's own account of itself.

- **B1 resolved.** `thesis/claim_ledger.csv` now holds 541 rows. Chapter 2 uses 73 `C2.*` ids
  against 73 `C2.*` rows; chapter 3 uses 170 `C3.*` ids against 170 `C3.*` rows; **zero orphans in
  either direction for both chapters**. At paragraph level, every paragraph in ch02 and ch03 that
  contains a data number now carries a pointer — the only unpointed matches left are section
  headings whose numbers look like decimals ("3.10"), table captions, and three pure
  cross-reference sentences. All 14 distinct artifacts the new rows cite were re-hashed from disk
  and **14 of 14 match**, with exactly one ledger hash per artifact (no stale duplicates).
- **B2 resolved.** ch03:814 now reads "the full list of deviations from the approved plan, **D3 to
  D14**"; `methodology/protocol.md` §16 holds D3-D14. ch03:778 now reads "**Eight** questions are
  open … (OQ1 to OQ8)" and enumerates all eight; §17 holds OQ1-OQ8. OQ7 is now stated in full at
  ch03:786-792, including the load-bearing clause I said was missing — "the supervisor should say
  whether that criterion is to be read as requiring actual rather than simulated new learners,
  because that reading would put the whole filter design in question and would require a redesign".
  The arithmetic checks: 1,019 + 997 = 2,016 of 29,228.
- **B3 resolved, and independently verified.** ch03 §3.9:699-715 now states both facts with full
  hashes: the G4-approved tree `694c3ea6026939967a6b01ab0698ef7336e77a8dd29f0739157e9f9662b0231c`
  for the pilot and main runs, `5a8f935a8dd05bb2b8428966ae9794a2cfe1bf6b7573b5005698bad267691b21`
  for the diagnostics, and `run_log_after_sha256` as a prefix hash over the first 10,257,030 bytes.
  I did not take this on trust: I hashed `results/run.log`'s first 10,257,030 bytes myself and got
  **d547e943a8e02b9fcc26c807b6072f6fafd4bf1e3ca873815de65bda615c0eac**, exactly the main receipt's
  value; the file is now 10,274,521 bytes (17,491 appended, as claimed) and its whole-file hash is
  `5068dad9…`, which is the diagnostics receipt's `run_log_after_sha256`. The diagnostics receipt
  also carries `main_run_log_prefix_intact: true` and a `w5_inertness_check` of 22 presentations /
  44 cells / 0 differences / max abs difference 0.0, which is what ch03's "all 44 cells checked"
  rests on. Consistent with ch04:268-270 in substance and in every digit.

## Warnings (should fix)

- [W1] <severity:med> **C3.81 is mis-attributed.** The claim is "This replaces the phase 1 design,
  which permuted each learner's resources and held out 20% at random, **ignoring the day column
  entirely**". Its artifact is `inputs/prior_evidence/summary.md`, whose only relevant line (:9) is
  "for each user with ≥5 distinct interacted items, 20% held out as test". The words "random",
  "permuted" and "date" do not occur in that file at all. The load-bearing part of the claim — that
  the holdout was random and ignored `date`, which is why it leaked — is supported by
  `methodology/threats_to_validity.md` T1 ("The pilot's random 20% holdout ignores `date`") and by
  the pilot code, not by the cited artifact. Re-point the row. rule=2
- [W2] <severity:med> **C2.68 and the §2.7 pitfall-1 sentence rest on a finding the ledger does not
  record.** Both attribute to `panda2022coldstart` that the cold-start review "includes no
  experimental benchmark" / that "the reviews report no benchmark of the approaches". That row in
  `literature/ledger.csv` has **no `reported_result` and no `metric` field at all**, `dataset: n/a
  (review)`, and `notes: … full text not opened … claims limited to the abstract`. I searched every
  field of all 39 ledger rows for "benchmark": the only hits are `chaudhary2019elearning`'s
  comparability note and `mohammadi2022rbf`. So an abstract-only source is carrying a negative
  finding that the ledger nowhere records. This does not sink the gap statement — §2.9's gap has an
  independent second pillar ("none of the sources opened evaluates a behaviour-aware hybrid on a
  cold-start slice built by refitting") and is hedged "among the sources opened" throughout — but
  either the abstract's wording should go into that ledger row's `reported_result` or the clause
  should be dropped. rule=11
- [W3] <severity:low-med> **C2.40 is mis-attributed.** "Among the nine proposal papers, none
  reports repeated-run variance or a significance test in the text I read (search of the PDFs,
  `literature/notes`)" cites `literature/ledger.csv`. Only `gao2022cnn`'s comparability note
  mentions variance or significance; for the other eight papers the ledger records nothing about
  the absence. The sentence itself names the right evidence base — `literature/notes` — so the row
  should cite that, not the ledger. rule=2
- [W4] <severity:med> **C3.102 over-states the scope of a one-presentation figure.** "Honest
  cold-start Precision@10 values are small — of the order of **0.025 to 0.033** here". That range
  is `threats_to_validity.md` T27's, and T27 names its presentation: "genuinely small (0.025 to
  0.033 **on EEE_2014J**)". The receipted 22-presentation cold-start medians in
  `thesis/tables/table_5_5_random_floor.md` run from 0.0266 (MostPop) to 0.0728 (CBF), with the
  hybrid at 0.0473 — roughly double the quoted range. As written, chapter 3 tells the reader what
  scale to expect before chapter 5 quotes a cold-start number, and the scale it gives is too low.
  Add "on EEE_2014J", as the source artifact does.
- [W5] <severity:low> **C2.55 drops a qualifier in the direction of the proposal's overclaim.**
  Table 2.2's Zhang et al. 2015 cell reads "Interactive recall above random; diversity **about
  equal**". The ledger's `reported_result` is "hybrid recall higher than the random recommender;
  diversity almost the same, **and lower in the revisit setting**". Chapter 2's own pitfall 4 is
  "reading a paper's summary instead of its table", and its search log records that the proposal
  claims better diversity where the paper shows "about equal or lower". Restore the qualifier.
- [W6] <severity:low> **C3.134's "approved code path" is loose, and ch03's changed-file list is one
  file short of the receipt's.** "run as a separate stage on the approved code path" — the
  diagnostics did not run on the G4-approved *tree* (`5a8f935a…` ≠ `694c3ea6…`); what was approved
  is the entry-point contract (`code/README.md`:144, "fourth `--stage diagnostics` value on the
  existing entry point"). The very next paragraph discloses the two trees, so no reader is misled
  for long, but the phrase should say "entry point" rather than "code path". Separately, C3.143
  lists `code/models.py`, `code/blend.py`, `code/main.py` and new `code/diagnostics.py`; the
  receipt's `changed_files_mtime_after_main_run` also includes `code/README.md`, which ch04:268
  mentions ("modified too but lies outside the hash") and ch03 omits.

## Open items carried (the two warnings writer A declined)

Both declines are **acceptable**, and both must be carried rather than closed:

- **W6 of cycle 1, the context-aware literature gap: acceptable, carry as an open item for the
  supervisor.** The standards' chapter-2 row lists context-aware recommendation as required
  content, and it has no included source. But the scholar's reason holds: the single candidate was
  excluded at full text for stating no method or evaluation, the family is not part of the
  experiments, and the gap is disclosed twice — in §2.2 ("thinly sourced here and is not part of
  the experiments") and in the §2.8 coverage line ("except that context-aware recommendation has no
  included source"). Under rule 6 that makes it `unchecked`, not `passed`, which is the correct
  state for an unobtainable source. It should join `literature/open_questions.md` item 2's database
  access problem as a named gap, so a licensed session can close it later; it must not be left to
  be discovered by an examiner reading the chapter row.
- **W4 of cycle 1, the licence residuals in frozen or scholar-owned files: acceptable, carry as an
  open item for assembly.** ch02 now reads "CC BY 4.0" (the hyphen is gone), so the chapter-level
  inconsistency is closed. The two residuals are `plan.md`:71 "**Licence: `unverified`**" and
  `literature/ledger.csv`'s `kuzilek2017oulad` `notes` field. Declining both is right: `plan.md` is
  frozen and its text is a human-reserved decision, and the ledger's sentence ("plan.md records the
  licence as unverified") is literally true. The item to carry is the appendix: the licence-text
  appendix and the reproducibility appendix must not reproduce a frozen `unverified` beside a
  verified CC BY 4.0 without the one-line explanation ch02 and `literature/open_questions.md`
  item 6 already give.

## Constraint Audit

Unchanged from cycle 1 in substance; re-checked against the revised chapters.

- [C1] "use the public Open University Learning Analytics Dataset (OULAD) … download OULAD once" |
  status: satisfied | evidence: ch03 §3.2; §3.9 "no network access at run time" | blocker: none
- [C2] "Assume a single CPU or a single consumer/cloud GPU … do not assume a multi-GPU cluster" |
  status: satisfied | evidence: ch03 §3.9; `u11_s5_run_main.json` `hardware` "single CPU, no GPU",
  `process_cpu_seconds` 2798.41 < `wall_clock_seconds` 3769.12; the diagnostics receipt records the
  same machine ("12 logical cores, no GPU") with `cpu_hours` 0.1413 — I3's reading holds and ch01
  §1.6.4 and ch03 §3.9 both match it | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints" |
  status: satisfied | evidence: ch03 §3.9; §3.6 six classical models; §3.6 "Deferred scope" | blocker: none
- [C4] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time" |
  status: satisfied | evidence: C5 1.0140 CPU-hours against 4.0; reproduction 0.238 min against 15;
  ch01:200 now discloses that the C5 verdict is combined by hand from the two receipts | blocker: none
- [C5] "Keep the three compared models … trained and evaluated on identical splits" |
  status: satisfied | evidence: ch03 §3.5.1 "Identical splits", byte-identical sets across all six
  models proved by serialised-set hash comparison (L5, protocol:522); C4 verdict's three
  intersection counts all 0, `max_test_scoring_count` 1 over 7,920 cells | blocker: none
- [C6] "Treat `src/reasearch_topic/References/*.pdf` … as read-only background" |
  status: satisfied | evidence: `literature/ledger.csv` `local_pdf`/`opened_on` records; the 14
  unreachable items logged as unreachable rather than re-scraped | blocker: none
- [C7] "report the actual numbers, the gap, and the most likely cause … rather than adjusting the
  threshold after the fact" | status: satisfied | evidence: re-diffed after the revision — all six
  criteria's `kind`, `metric`, `threshold` and `on_dataset` fields are still identical to
  `plan.md`'s `success_criteria` block in both ch01 Table 1.5 and ch03 §3.1.1, and the hypothesis
  in ch01 §1.6.1 is still byte-identical to idea.md and to plan.md's frontmatter and body. The
  post-hoc additions are declared in §3.8 as exploratory family F4 and ch03 §3.12 lists them as the
  fifth thing chapter 4 takes | blocker: none

## Ledger rows sampled by reading the claim against the artifact

**92 rows read, not pattern-matched** — 35 `C2.*` and 57 `C3.*`, against the ledger's artifact in
each case, well above the 40 asked for. I favoured design-commitment sentences in ch03, attributive
prose in ch02, every row whose artifact is `protocol.md` or `literature/ledger.csv`, and all 26
off-pattern rows (those citing anything else), which is where writer A's number-plus-word-overlap
script is weakest.

`C2.*` (35): 1, 3, 4, 5, 8, 11, 12, 17, 19, 21, 22, 23, 27, 28, 29, 32, 34, 38, 39, 40, 42, 46, 48,
51, 55, 57, 59, 61, 64, 67, 68, 69, 70, 72, 73.

`C3.*` (57): 6, 8, 9, 16, 17, 20, 24, 30, 34, 37, 38, 40, 43, 46, 48, 49, 51, 75, 76, 79, 80, 81,
83, 88, 92, 93, 94, 96, 98, 99, 100, 102, 114, 126, 128, 132, 133, 134, 135, 136, 137, 138, 139,
140, 141, 142, 143, 144, 145, 146, 147, 148, 158, 164, 165, 166, 169.

**Not truly supported, mis-attributed or over-stated: 6 rows** — C3.81 (W1), C2.68 (W2), C2.40
(W3), C3.102 (W4), C2.55 (W5), C3.134/C3.143 (W6). The remaining 86 are genuinely supported. Rows
where the weak script could have passed something wrong and did not, checked individually:

- C3.83 — I expected this to fail. The protocol (§5.2:440-445) deliberately distinguishes two
  candidate cut-offs and says which is *not* used: the 80th percentile over interaction **rows**
  (EEE_2014J D = 164) versus over **distinct active days** (211). ch03 says "the day below which
  80% of the presentation's interaction **rows** fall" — the right quantity. Supported.
- C3.96 — Table 3.2's "all **five** learner-dependent fits" against §6.1a's eight rows A1-A8.
  Protocol §6.1a resolves it explicitly: "Rows A1, A2, A3, A6 and A7 are the **five**
  learner-dependent rows", covering **seven** learner-derived fitted objects, with A4 and A5 stated
  as learner-independent with the count that proves it. The chapter's "five", "eight" and "two of
  the eight" all land correctly. Supported.
- C3.126 — the corrected paired-learner range now reads "between **347 and 2,131**", matching
  protocol:1204 ("347 to 2,131"), the population table's AAA_2014J 347 and CCC_2014J 2,131, and
  :606. The old 346/2,118 pair is gone. Supported.
- C3.100 — now "an inflation of between **5.8 and 8.5** times", matching T27's 8.5x and 5.8x and
  ch04:328 exactly; cycle 1's "between six and nine times" is gone. Supported.
- C3.48/C3.49 — "a median of 8 distinct resources … a **handful** of resources in one or two
  sittings", matching protocol:336-339 word for word; cycle 1's "many resources" is gone. Supported.
- C3.51, C3.114 — the 100.0% / 0.2% / 0.3% week-completeness figures and the 45.6% / 14.4% / 81.3%
  ceiling shares are in `threats_to_validity.md` T4 and T10 verbatim, which is the artifact cited.
  Supported.
- C3.128 — "−2.7%" against `all_modules_metrics.json`'s
  `hybrid_vs_cf_relative_gain_warm.median` = −0.026616. Supported.
- C2.59 — I expected the metric names to be unsourced; `jeevamol2021ontology`'s `metric` field does
  read "MAE, precision, recall". Supported.
- C2.4 — the HTTP 403 refusals are timestamped in both `furini2022twins` and `mauro2022autism`
  `notes` fields, with "not relied on for any claim". Supported.
- C3.132-C3.139 — `results/diagnostics_summary.md`:18-22 carries the post-hoc disclosure and the
  no-counter point; :46-47 carries "44 cells … All 44 agree exactly (0 differences, maximum
  absolute difference 0.0)"; `code/README.md`:156 and :161-163 carry D1's alpha logging and D2's
  three dropped columns by name (`n_visible`, `log1p_visible_clicks`, `n_active_days`). Supported.
- C3.142-C3.148 — all six verified against `u13d_diag_run.json` field by field, including
  C3.144's "not under version control and no copy of the earlier tree exists", which is in the
  receipt's `code_tree_difference_note` almost word for word. Supported.

## Notes

- **The row counts in the dispatch do not match the file.** The manager's message says the ledger
  holds "41 C2.* and 202 C3.* rows"; it holds **73 C2.* and 170 C3.***. The total, 243, is right,
  so this looks like a transposition in the hand-off rather than a ledger problem — but the
  coordinator's own record should be corrected, since a later gate that checks the count will trip.
- Writer A's script is as weak as the manager judged, and the six findings above are the shape of
  what it misses: it cannot detect a claim whose *numbers* are all in the artifact while the
  *attribution* or the *scope* is not (C3.81, C3.102), a negative finding no field records
  (C2.68, C2.40), or a dropped qualifier (C2.55). None of the six is a wrong number. Every
  quantitative value I re-derived in either cycle has been correct.
- ch02 now numbers its tables (Table 2.1, Table 2.2) and references each by number before it
  appears — cycle 1's W5 closed.
- ch03 §3.12's "Chapter 4 needs **five** things" enumerates five, and its pointer to "the post-hoc
  additions declared in **3.8**" is right: that paragraph sits at :666, inside §3.8 (:607-684), not
  in §3.9. Checked because a wrong section pointer is exactly what a re-write introduces.
- Nine leakage assertions L1-L9 exist in protocol:518-526, matching ch03 §3.5.1's "Nine leakage
  assertions (L1 to L9)".
- Reviewer open question 1 from the skill's project context still stands: the university
  regulations are absent, so `chapter_gate`'s "matches the university template" line remains
  unverifiable, and front matter does not yet exist. It is not counted against these chapters.

## Overall

Decision: **approve_with_warnings** (`approve` in the skill's fixed vocabulary). All three cycle-1
blockers are genuinely closed, and I confirmed the hardest of them — B3 — by recomputing the prefix
hash of `results/run.log` myself rather than reading the chapter's assurance: the first 10,257,030
bytes do hash to the main receipt's value, and the 17,491 appended bytes are accounted for. Ledger
coverage of chapters 2 and 3 is now complete and orphan-free in both directions, and all 14 cited
artifacts hash-match. Of 92 rows I read against their artifacts, 86 are genuinely supported and 6
have citation or scope defects — a mis-pointed pilot-split row, an abstract-only source carrying a
finding its ledger row does not record, a negative claim pointed at the ledger instead of the
notes, an EEE_2014J range presented as the general cold-start scale, a dropped qualifier in the
related-work table, and one loose phrase about the "approved code path". None changes a number, a
threshold, a verdict or a conclusion, which is why they are warnings and not blockers; the
two declined cycle-1 warnings are acceptable and are carried as open items above. What would turn
this back to `revise`: leaving W2 or W4 unfixed while chapter 5's cold-start argument is assembled
on top of them, since both shape how a reader calibrates the cold-start result.

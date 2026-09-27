---
blockers_count: 0
warnings_count: 2
files_reviewed: fix verification — thesis/ch01.md, thesis/ch05.md, thesis/ch06.md, thesis/tables/table_module_d_behaviour.md, thesis/claim_ledger.csv (rows C5.119 to C5.132, C6.43 to C6.47), code/behaviour.py
reviewer: manual (project engine unavailable on Windows; ar-workflow-engine.py imports fcntl — see thesis-reviewer SKILL.md)
model: Claude Opus 5.5 (self-reported; top-tier reviewer seat)
model_identity: claude-opus-5-5, top tier, reviewer seat. The fixes were produced by writer_B, mid
  tier, sonnet (decisions.log 2026-09-26T08:19:44Z dispatch and 08:23:33Z close of u18c_g7_fix). I
  produced none of the artifacts under review.
mode: chapter_gate
gate: G7 (scoped re-pass, fix verification)
unit: u18b_g7_repass
cycle: 3
scope: verification of the fixes for B1 and W1 to W4 of reviews/chapter_gate_module_d.md (cycle 2,
  left unedited), and confirmation that nothing else in the scoped material changed.
verdict: approve_with_warnings
---

# Review — G7 scoped re-pass, fix verification (cycle 3)

**Manual-write deviation, stated once as rule 6 requires.** The review MCP tool cannot run on this
machine, so no tool validated this file; I ran the validation on my own draft. As in cycle 2, the
dispatch required hashing and running the ledger checker, so I used Bash, read-only.

**Method.** I hashed every changed file. For ch05, ch06, ch01 and the table I then **reversed the
claimed edits byte for byte** and re-hashed the result. If the reconstruction reproduces the
previously recorded hash, the file differs from its gated version by exactly the claimed edits and
nothing else.

| File | Current sha256 (prefix) | Claimed | Claimed edits reversed → | Prior recorded hash | Result |
| --- | --- | --- | --- | --- | --- |
| thesis/ch05.md | 2926442b | 2926442b | 1ca31b4e | 1ca31b4e (u18 close) | only the claimed edits |
| thesis/ch06.md | 1aaa6ec0 | 1aaa6ec0 | 6fe553bc | 6fe553bc (u18 close) | only the claimed edits |
| thesis/ch01.md | 0f9f1b66 | 0f9f1b66 | 901bdeb8 | 901bdeb8 (decisions.log, prior ch01) | only the claimed edit |
| thesis/tables/table_module_d_behaviour.md | 1234d28a | 1234d28a | cfad80d8 | cfad80d8 (cycle 2) | only the one cell |
| thesis/claim_ledger.csv | e6b0d515 | e6b0d515 | 3ef15512 | 4f248439 (u18 close) | not reproduced, see W1 |

## Fix-by-fix

- **B1: resolved.** ch05.md:675 now reads "which answers the first half of RQ1 for three of the four
  families it names — click volume, active-day count and day-ordered sequence; activity type was not
  computed as a learner-level feature — and …", and C5.130 is added to its comment. Ledger C5.129
  (line 525) and C6.45 (line 528) now carry the same qualifier. Neither 5.12 nor any ledger text
  still states RQ1's first half unqualified.
- **W1: resolved.** ch05.md:679 and ch06.md:17 now say "twelve limitations", and section 5.11 has 12
  items.
- **W2: resolved.** A scalar-summary clause appears at ch05.md:134, ch05.md:664 and ch06.md:50-52,
  each tagged C5.132. The new ledger row C5.132 (line 575) describes the two summaries correctly
  against code/behaviour.py:24-27: the distinct first-opening-day count, and the span of
  first-opening days divided by items minus one. Its "0 of 22" monotonicity figure matches my
  recomputation from all 22 results files and the table's D.4. See W2 below for the citation.
- **W3: resolved.** ch01.md:66 now reads "Answered descriptively for three of RQ1's four named
  behaviour families (section 1.3.3, item 4; section 5.1.4)."
- **W4: resolved.** The p25 cell is 12.112 at ch05.md:109 and at table line 48. This matches the
  median of the stored values (12.1125) under the table's half-to-even rule. The table's new hash
  1234d28a appears in exactly 13 ledger rows: C5.119 to C5.127, C5.129 and C6.43 to C6.45. Those are
  all 13 rows that cite the table. No row still carries cfad80d8.

**Nothing else in scope changed.**
- Rows C5.119 to C5.128, C6.43 and C6.44 are byte-identical to their cycle-2 text once the hash is
  reverted.
- Rows C5.130, C5.131, C6.46 and C6.47 are unchanged, and code/behaviour.py still hashes to fa481744.
- Table 5.13 remains cell-identical to the table file.
- Every figure I verified in cycle 2 still stands, because the prose around it is byte-identical,
  as the reconstruction shows.

**Checker:** `check_claim_ledger.py` → `RESULT: PASS (574 ledger rows, 0 errors, 189 warnings)`. In
scope, the warnings are the same "number without a hidden ledger id" lines as in cycle 2. One of
them is ch05.md:679, which is a section reference plus a count word.

## Blockers (must fix before proceeding)
None

## Warnings (should fix)
- [W1] <severity:low> thesis/claim_ledger.csv (whole file): I reverted the claimed ledger edits (13
  hashes back to cfad80d8, the C5.129 and C6.45 text restored to their cycle-2 wording, C5.132
  removed). The result hashes to 3ef15512, not 4f248439, the hash the u18 close recorded. The same
  method reproduced the recorded hash exactly for ch05, ch06, ch01 and the table. Every in-scope row
  is verified row by row. Whether any row **outside** this re-pass's scope changed during u18c
  therefore stays `unchecked`, not passed. The manager should confirm against a copy of the u18
  ledger, if one exists, or record why the logged hash differs.
- [W2] <severity:low> thesis/claim_ledger.csv:575 (C5.132): the row's quantitative clause ("monotonic
  … in 0 of 22 presentations") cites only code/behaviour.py, which cannot carry a result. The number
  is correct, but its artifact is thesis/tables/table_module_d_behaviour.md D.4 (1234d28a). Add that
  artifact, or drop the clause from the code-cited row.

## Constraint Audit
None of the fixes touches a run, a split, a model, a download or a threshold: they are wording, one
rounding cell and ledger rows. The cycle-2 audit therefore carries over unchanged, and I re-state it
here.

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume
  a multi-GPU cluster." | status: satisfied | evidence: no new run; Module D stays inside the
  receipted main run (code/evaluate.py:184; results/run_receipts/u11_s5_run_main.json) | blocker: none
- [C2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." |
  status: satisfied | evidence: code/behaviour.py unchanged (fa481744), imports numpy/pandas/sklearn
  only | blocker: none
- [C3] "requires network access during the pilot to download OULAD once" | status: satisfied |
  evidence: the fixes are text edits only; no code was run and no data was fetched | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits" | status: satisfied | evidence: code/tests/test_evaluate.py:49-51
  unchanged; Module D feeds no model (ch05.md:91 unchanged) | blocker: none
- [C5] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware" | status: satisfied | evidence: no new run | blocker: none
- [C6] "no threshold moved after a run" (idea.md criterion 4; plan.md criteria_frozen) | status:
  satisfied | evidence: the only numeric change is a rounding correction to a descriptive cell that
  decides no criterion; no criterion text or verdict changed (ch05 reconstruction reproduces
  1ca31b4e apart from the claimed edits) | blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background" | status: satisfied | evidence: no reference content in the changed text | blocker: none

## Notes
- The cycle-2 verdict file reviews/chapter_gate_module_d.md was left unedited, as instructed.
- The day-ordered-sequence clause still says that family was answered "affirmatively". With the new
  qualifier (two scalar summaries, no sequence model) this is accurate and no longer a finding.

## Overall
Decision: approve_with_warnings (in the loop vocabulary, `approve`). The blocker and all four
warnings from cycle 2 are fixed. For the four prose and table files, byte-level reconstruction shows
that nothing else changed. The 13 re-hashed ledger rows match the new table hash exactly. The two
remaining warnings concern ledger bookkeeping, not the thesis's claims: an out-of-scope provenance
gap that stays `unchecked`, and an artifact citation on C5.132. Neither changes any number or
conclusion in the Module D material.

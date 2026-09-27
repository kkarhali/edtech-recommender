---
blockers_count: 1
warnings_count: 4
files_reviewed: scoped re-pass — thesis/ch05.md (5.1.4, Table 5.13, 5.11 limitation 12, plus the 5.12 closing paragraph as a consistency check), thesis/ch06.md (6.1 RQ1, plus 6.0 as a consistency check), thesis/ch01.md (1.3/1.6.2 RQ1 wording), 18 claim-ledger rows (C5.119 to C5.131, C6.43 to C6.47), thesis/tables/table_module_d_behaviour.md, code/behaviour.py, code/evaluate.py, code/tests/test_evaluate.py, all 22 results_<pres>.json#behaviour blocks and all 22 foundation_<pres>.json#counts.evaluated values
reviewer: manual (project engine unavailable on Windows; ar-workflow-engine.py imports fcntl — see thesis-reviewer SKILL.md)
model: Claude Opus 5.5 (self-reported; dispatched as the top-tier claude-opus-5 reviewer seat)
model_identity: claude-opus-5-5, top tier, reviewer seat. Independence verified from the project's own
  record: decisions.log 2026-09-26T04:29:54Z (u17b_module_d_write) and 08:10:37Z (u18_rq1_scope_write)
  name writer_B, tier mid, model sonnet, as the producer of every section under review, and the
  table file was produced by the results-analyst unit u17_module_d_report (decisions.log
  2026-09-25T22:24:16Z). I produced none of these artifacts.
mode: chapter_gate
gate: G7 (scoped re-pass)
unit: u18b_g7_repass
cycle: 2
scope: only the material added after ch01-03 and ch04-06 passed G7 (reviews/chapter_gate_ch01_03_cycle2.md,
  reviews/chapter_gate_ch04_06.md). Everything else in those chapters is taken as gated and was read
  only where item 4 of the dispatch (consistency) required it.
verdict: request_changes
---

# Review — G7 scoped re-pass, Module D and the RQ1 answer

**Manual-write deviation, stated once as rule 6 requires.** The Bun review MCP tool cannot run on
this Windows machine (its persistence step shells out to `ar-workflow-engine.py`, which imports
`fcntl`), so no tool injected this file's identity, bound it to its unit and cycle, or validated
its Constraint Audit. I ran that validation on my own draft. The absence of the automated check is
`unchecked`, not `passed`, and the decision log should carry it. The skill's "never run Bash"
boundary was departed from only because the dispatch explicitly required computing a hash and
running the ledger checker; every command was read-only.

**What I did.** Hashed the table file and `code/behaviour.py`; recomputed every number in Table
5.13, in the 5.1.4 prose, in the ch06 6.1 RQ1 answer and in the 18 ledger rows from all 22
`results_<pres>.json#behaviour` blocks directly (not only the requested 3), plus the
`foundation_<pres>.json#counts.evaluated` equality; opened four results files by hand (AAA_2014J,
BBB_2014B, CCC_2014J, FFF_2013J) and confirmed their SHA256 against
`results/run_receipts/u11_s5_run_main.json`; read `code/behaviour.py`, the import sites of
`behaviour` across `code/`, and `test_behaviour_feeds_no_model`; ran the claim-ledger checker.

## Blockers (must fix before proceeding)

- [B1] <severity:high> thesis/ch05.md:675 (section 5.12, closing paragraph; ledger row
  thesis/claim_ledger.csv:525, C5.129): the chapter's own summary says Module D's six features
  "answer the first half of RQ1", unqualified, while 5.1.4 (ch05.md:134-135), limitation 12
  (ch05.md:664) and ch06 6.1 (ch06.md:40, 50-56) all say the first half is answered **for three of
  the four behaviour families RQ1 names**, activity type never having been computed as a
  learner-level feature (code/behaviour.py:17 FEATURES). The closing paragraph is the one chapter 6
  says it "takes exactly" (ch05.md:679), and the C5.129 ledger claim it cites carries the same
  unqualified wording. This is the pattern the pilot's "22 out of 22" sentence was blocked for: a
  statement true only on a subset, restated as whole. rule=2 | impact: the chapter's summary claims
  a wider answer to RQ1 than its evidence and its own limitation 12 support; fix by adding the
  three-of-four qualifier to ch05.md:675 and to the C5.129 claim text (C6.45's claim text, ledger
  line 528, should be aligned the same way; its prose at ch06.md:50-56 already is).

## Warnings (should fix)

- [W1] <severity:med> thesis/ch05.md:679 and thesis/ch06.md:17: both still say "the eleven
  limitations of (section) 5.11"; section 5.11 now has twelve (limitation 12 at ch05.md:664 is the
  new RQ1 scope limitation, so the stale count silently drops exactly the limitation this re-pass
  concerns). The checker also flags ch05.md:679 as a number without a ledger id.
- [W2] <severity:med> thesis/ch05.md:134 and thesis/ch06.md:40, 50: "day-ordered sequence" is
  reported as answered "affirmatively", but Module D represents that family only by two scalar
  summaries — the count of distinct first-opening days and the span of first-opening days divided by
  items minus one (code/behaviour.py:25-27) — not by any ordered sequence; and the one of them that
  is a genuine ordering feature (mean gap between new items) is monotonic across the segment ranks in
  0 of 22 presentations. The chapter should say the sequence family was examined through those two
  summaries only, so a reader does not take it as a sequence analysis.
- [W3] <severity:low> thesis/ch01.md:66 (Table 1.x, objective 1 row): "In scope. Answered
  descriptively (section 1.3.3, item 4)" now overstates the RQ1 answer relative to ch05 5.1.4 and
  ch06 6.1 (first half only, three of four families). The 1.6.2 RQ1 wording itself (ch01.md:138)
  mirrors the frozen plan and is consistent with the new answers; only this status cell lags.
- [W4] <severity:low> thesis/tables/table_module_d_behaviour.md, D.2 clicks per active day p25 and
  ch05.md:109: printed 12.113; the median of the 22 stored values is 12.1125, which the table's own
  stated rule (round half to even) gives as 12.112. Cosmetic, below any claim's precision, and C5.120
  does not cite it; noted so the table's stated rounding rule and its cells agree.

## Constraint Audit

Hard constraints quoted from `idea.md`, audited as the Module D material carries them. Module D ran
inside the already-receipted main run; no new run, download or split was introduced by this
material.

- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume
  a multi-GPU cluster." | status: satisfied | evidence: Module D is `behaviour.describe(prep)` called
  inside `run_presentation` (code/evaluate.py:184) of the receipted main run
  (results/run_receipts/u11_s5_run_main.json, hardware already audited in
  reviews/chapter_gate_ch04_06.md C1); the four results files I hashed match that receipt | blocker: none
- [C2] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." |
  status: satisfied | evidence: code/behaviour.py:9-14 imports only numpy, pandas, sklearn KMeans and
  silhouette_score and common.SEED; no weights | blocker: none
- [C3] "requires network access during the pilot to download OULAD once" | status: satisfied |
  evidence: code/behaviour.py has no I/O beyond the in-memory `prep` object; the table file states
  "no code was run for this table" and it reproduces exactly from the stored JSON | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits" | status: satisfied | evidence: Module D touches no split and feeds
  no model — `behaviour` is imported only by code/evaluate.py:14; code/tests/test_evaluate.py:49-51
  forbids the string in models, blend, cell, features, splits, provenance and leakage; ch05.md:91
  states exactly this | blocker: none
- [C5] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware" | status: satisfied | evidence: no new run; Module D's time is inside the main run's
  already-audited 1.0140 CPU-hours (reviews/chapter_gate_ch04_06.md C5) | blocker: none
- [C6] "no threshold moved after a run" (idea.md criterion 4; plan.md criteria_frozen) | status:
  satisfied | evidence: ch05.md:91 and table file scope note (v) — Module D appears in no threshold;
  k = 4 is the pre-run code default (code/behaviour.py:16), not tuned after the run; no criterion
  verdict changed | blocker: none
- [C7] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background" | status: satisfied | evidence: the scoped material cites no reference PDF and
  redistributes no paper content | blocker: none

## Notes

- **Hashes.** thesis/tables/table_module_d_behaviour.md = cfad80d8af908fcb…a480522, matches the
  expected prefix and every ledger row citing it (C5.119-C5.127, C5.129, C6.43-C6.45).
  code/behaviour.py = fa481744997baafd…fd82556c, matches C5.128, C5.130, C5.131, C6.46, C6.47.
  results_AAA_2014J / BBB_2014B / CCC_2014J / FFF_2013J.json hashes equal the main-run receipt.
- **Numbers — all reproduce, from all 22 presentations.** Cohort 27,212, min 347 (AAA_2014J), max
  2,131 (CCC_2014J), median 1,222, equality with counts.evaluated 22/22, 15 cohorts > 1,000.
  Panel (a) medians of quantiles, p95/p05 ratios (42.8, 8.1, 23.6, 12.5, 5.4, 4.3) and median ranges
  with their presentations; silhouette median 0.3274, range 0.2782 (BBB_2014B) to 0.3614
  (FFF_2013J), quartiles 0.3139 / 0.3444, 18 in 0.30-0.40, the four named below 0.30; 22/22 four
  non-empty segments; largest/smallest share medians 0.413 / 0.112; panel (b) rank shares 0.410,
  0.347, 0.147, 0.117 and every rank median; monotonic counts 22, 18, 14, 15, 0, 4. Table 5.13 is
  cell-identical to the table file's D.2 and D.4. Hand spot-checks: AAA_2014J n 347, sizes
  45/142/131/29, silhouette 0.3515, click p50 1158; BBB_2014B 1163, 0.2782, click p50 389;
  FFF_2013J 1989, 0.3614, click p50 2060; CCC_2014J 2131, 0.2965 — all as tabulated.
- **Code claims.** Feature list (C5.130, C6.47) matches code/behaviour.py:17 exactly, none encodes
  activity type; no time bound matches the docstring (lines 5-6); k fixed (line 16);
  silhouette subsample min(1000, n) seeded (line 39); only evaluate.py imports the module.
- **Overclaim checks passed** in the scoped sections: no use of segments as a cold-start prior
  (ch05.md:92 and ch06.md:43-46 say they could not serve as one); no causal reading; dwell time is
  named only as not recorded (ch06.md:38); the D2 link is labelled post-hoc and as a weighting
  effect. The ch05 ratio-of-medians caveat (ch05.md:123) correctly distinguishes it from the table's
  median-of-ratios (~40x) in D.5.
- **Ledger checker:** `check_claim_ledger.py` → `RESULT: PASS (573 ledger rows, 0 errors, 189
  warnings)`, exit 0. Warnings are "number without a hidden ledger id" lines across all chapters
  plus unused C0.1-C0.9; within scope they hit ch05.md:87, 92, 94, 98, 135 (section/table
  references and the "three of four" count) and ch05.md:679 (W1). None is an error.
- C5.129's evidence for the D2 figures is the Module D table's D.5 restatement rather than the D2
  diagnostics artifact; the numbers agree with the already-gated C6.5, so this is accepted.

## Overall

Decision: request_changes (in the loop vocabulary, `revise`), with one blocker. Every number in the
new material reproduces from the receipted per-presentation artifacts, both hashes are correct, the
feature-list and descriptive-only claims match the code, and the RQ1 answer in 5.1.4, limitation 12
and ch06 6.1 is correctly scoped to three of four families with its second half left unestablished.
The blocker is that the chapter 5 closing paragraph and its ledger row C5.129 still state the first
half of RQ1 as answered without that qualifier, contradicting the sections it summarises. A
one-clause fix at ch05.md:675 plus aligned ledger text for C5.129 (and C6.45) would clear it; W1
(the stale "eleven limitations" count in two places) should be fixed in the same pass.

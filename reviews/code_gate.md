---
blockers_count: 0
warnings_count: 2
files_reviewed: 24
reviewer: manual (project engine unavailable on Windows; see SKILL.md)
model: Opus 5
model_identity: claude-opus-5 (reviewer seat, top tier) — distinct from the experiment engineer's mid-tier sonnet seat that produced code/ (decisions.log, 2026-09-22T06:40:00Z unit_dispatched u10_g4_code_review)
mode: code_gate
unit: u10_g4_code_review
cycle: 0
---

# Review

Gate G4, first half: is `code/` ready for a full review. The two checklist lines of
`references/templates/gate_checklists.md` are the entry-point contract and the module map.
Substantive findings belong to `code_review` and are in `review.md`, not here.

## Blockers (must fix before proceeding)
None.

## Warnings (should fix)
- [W1] <severity:med> code/main.py:43-48: the two path refusals (`--artifact-dir` outside
  `results/run_artifacts/`, `--run-log` not `results/run.log`) exit 1 through `SystemExit(str)`,
  while the missing/duplicated-argument refusals exit 2 through argparse. `code/README.md` line
  "must exit 2 saying `--artifact-dir` is required" is right for the case it names but the two
  exit codes are not documented together; the runner's receipt should record which it saw.
- [W2] <severity:med> code/main.py:72-88: whether the evaluation half runs at all is decided by
  `importlib.util.find_spec("evaluate")`. `evaluate.py` is present, so the gate passes, but a
  deleted or unimportable `evaluate.py` would downgrade a main run to foundation-only with only
  `log.unchecked` lines rather than a hard failure. Rule 6 is honoured (unchecked, never passed),
  so this is a warning, not a blocker.

## Constraint Audit
- [C1] "Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume a multi-GPU cluster." | status: satisfied | evidence: code/common.py:30 `"hardware": "single CPU, no GPU"`; code/common.py:91-101 `environment()` records processor, core count and "no GPU" into `run_manifest.json`; no torch/tensorflow/keras/cuda import anywhere under code/ (grep over all 22 .py files returned only the literal `"downloaded_model_weights": False` in common.py:31) | blocker: none
- [C2] "Pilot (Phase 1) time budget: complete within a few hours of wall-clock time" (plan.md Budget: `max_cpu_hours: 4.0` main, `<= 0.25` reproduction) | status: satisfied | evidence: code/main.py:119-124 measures wall, process CPU and child-worker wall and reports `cpu_hours`; code/verdicts.py:43-53 judges C5 against `common.HARD_CONSTRAINTS` 4.0 / 15.0; code/README.md step 5 makes the runner extrapolate one presentation by 22 and stop above 4.0. The empirical figure is the runner's to establish at G5 | blocker: none
- [C3] "Do not download large model weights or unrelated pretrained checkpoints for the pilot." | status: satisfied | evidence: no `requests`/`urllib`/`http`/`download`/`huggingface`/`transformers` reference in any file under code/ (grep, 22 .py files); the only file reads are the four hashed OULAD CSVs (code/data.py:13, 52-80) | blocker: none
- [C4] "Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and evaluated on identical splits" | status: satisfied | evidence: code/splits.py:100-135 builds the split once per presentation; code/splits.py:90-97 `split_view`/`view_hashes` is the single object handed to every model; code/leakage.py:45-48 `l5` re-hashes it per model against `prep.hashes`; code/variants.py:37 recomputes the triple for every derived split | blocker: none
- [C5] "Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only background" | status: satisfied | evidence: no path under `src/reasearch_topic` appears anywhere in code/; the only configured data root is `data/projects/e_learning_pilot/data/raw` (code/configs/experiments.json:4, code/data.py:14); code/common.py:34 carries the constraint as a literal | blocker: none
- [C6] Network limited to the one OULAD download (idea.md DATASET DECISION: "requires network access during the pilot to download OULAD once") | status: satisfied | evidence: zero network calls in code/; code/data.py:25-40 verifies the already-downloaded copy's SHA256 and byte size against `inputs/manifest.json` and raises `DataIntegrityError` before any use; plan.md Budget `network: none required` | blocker: none
- [C7] "If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most likely cause ... rather than adjusting the threshold after the fact." | status: satisfied | evidence: code/verdicts.py:12-19 re-reads and JSON-decodes `metric`, `threshold` and `on_dataset` out of plan.md's frozen front matter at run time instead of restating them; code/stats.py:12 fixes the four verdict words; code/stats.py:97-109 applies the thresholds as written (C1 `>=` 0.10, C2 `>` 0) | blocker: none
- [C8] "Language/tooling per the thesis: Python, TensorFlow or Keras, scikit-learn. Prefer scikit-learn or a lightweight model for the pilot; reserve deep learning ... for the Phase 2 main experiment" | status: satisfied | evidence: the only estimators are `sklearn.linear_model.LogisticRegression` (code/blend.py:9, 39-44) and `sklearn.cluster.KMeans` (code/behaviour.py:11, 38); plan.md records the deep models as an explicit scope-out | blocker: none

## Notes
- The entry-point contract was verified by execution, not by reading `README.md`. Eight invocations
  were run against `code/main.py` from the project root on `.venv-pilot\Scripts\python.exe` with
  `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUTF8=1`: missing `--artifact-dir` → exit 2; missing
  `--stage` → exit 2; missing `--run-log` → exit 2; `--stage all` → exit 2 ("invalid choice");
  `--stage` twice → exit 2 ("must appear exactly once"); `--artifact-dir` equal to
  `results/run_artifacts` → exit 1; a `--run-log` other than `results/run.log` → exit 1;
  `--stage pilot --only ...` → exit 1. `--dry-run` printed `dry run ok` and exited 0. After all
  nine calls `results/` still did not exist: nothing was created. There is no default for
  `--stage`, no catch-all mode (`STAGES = ("pilot", "main", "iteration")`, code/main.py:23, 29) and
  one stage per process (code/main.py:114).
- Artifact confinement holds: every `write_text` in code/ targets `ctx["artifact_dir"]` or `art`
  (main.py:108, 130, 133; evaluate.py:173, 236; reproduce_phase1.py:194), the only other handle is
  the append-only `results/run.log` the contract requires (common.py:116), and `check_paths`
  (main.py:40-49) refuses a non-empty artifact directory, so one unit cannot write into another's.
- Module map against plan.md: R = `reproduce_phase1.py`; A = `data.py`, `splits.py`, `features.py`,
  `foundation.py`, `provenance.py`, `leakage.py`, `rebuild_worker.py`, `variants.py`; B =
  `models.py`, `blend.py`, `cell.py`; C = `evaluate.py`, `stats.py`, `verdicts.py`, `metrics.py`;
  D = `behaviour.py`; shared = `common.py`, `configs/experiments.json`; tests = three files under
  `tests/`. Every file is accounted for and no file straddles two modules.
- All 22 `.py` files compile under the named interpreter (`py_compile`, doraise) and all 19
  non-test modules import cleanly.

## Overall
`code_gate` is `approve`. The entry point takes `--stage`, `--artifact-dir` and `--run-log`, refuses
to run without any of them, has no default and no `all` mode, runs exactly one stage per process,
and writes measurements only under the artifact directory — all confirmed by running the refusals
rather than by reading the README. The files map cleanly onto plan.md's modules R, A, B, C and D,
and nothing runs the pilot and the main stage from one call. The code is therefore ready for the
full review; what it does once it runs is judged in `review.md`, which is not `approve`. This
verdict would change if the entry point gained a default stage, a combined mode, or a write outside
the artifact directory. Written by hand with Write, not by the review MCP tool, which cannot run on
this machine (`ar-workflow-engine.py` imports `fcntl`); under rule 6 the absence of the tool's
automated Constraint-Audit validation is `unchecked`, not passed, and the decision log must carry
that deviation.

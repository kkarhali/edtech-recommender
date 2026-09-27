#!/usr/bin/env python3
"""Experiment entry point. One stage per process: --stage pilot|main|iteration|diagnostics, --artifact-dir, --run-log, each
exactly once.

pilot       = Module R, the phase 1 reproduction on EEE_2014J (criterion C6).
main        = foundation checks (Module A, L1-L9) over the 22 presentations, then evaluation when parts 2 and 3 exist.
iteration   = the same as main over the presentations named for it in configs/experiments.json.
diagnostics = unit u13b_diag_code: alpha logging on A|2 and the behavioural-signal ablation on warm and A|2, over all 22
              presentations (diagnostics.py); decides no criterion (see criteria_verdicts.json, all UNCHECKED).
Arguments are validated before any file is created or any data is read. See README.md for the commands.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shlex
import sys
import time
import traceback
from pathlib import Path

import common
from common import CODE_DIR, CONFIG, PROJECT_ROOT, RunLog, environment, now

STAGES = ("pilot", "main", "iteration", "diagnostics")
RESULTS = PROJECT_ROOT / "results"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--stage", required=True, choices=STAGES)  # no default and no catch-all mode
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument("--run-log", required=True, type=Path)
    parser.add_argument("--only", default=None, help="one presentation id, e.g. EEE_2014J (main, iteration and diagnostics only)")
    parser.add_argument("--dry-run", action="store_true", help="validate arguments and exit 0, writing nothing")
    for option in ("--stage", "--artifact-dir", "--run-log"):
        if sum(1 for a in argv if a == option or a.startswith(option + "=")) != 1:
            parser.error(f"{option} must appear exactly once")
    return parser.parse_args(argv)


def check_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    art, log = args.artifact_dir.resolve(), args.run_log.resolve()
    root = (RESULTS / "run_artifacts").resolve()
    if art == root or root not in art.parents:
        raise SystemExit(f"error: --artifact-dir must lie under {root}")
    if log != (RESULTS / "run.log").resolve():
        raise SystemExit(f"error: --run-log must be {(RESULTS / 'run.log').resolve()}")
    if art.exists() and any(art.iterdir()):
        raise SystemExit(f"error: {art} already holds files; an artifact directory is immutable once written")
    return art, log


def run_pilot(ctx) -> int:
    import reproduce_phase1
    return reproduce_phase1.run(ctx)


def run_diagnostics(ctx) -> int:
    """D1 (alpha logging) and D2 (behavioural-signal ablation), unit u13b_diag_code: human-approved additions after the
    main run that decide no criterion. See diagnostics.py."""
    import diagnostics
    return diagnostics.run(ctx)


def run_matrix(ctx) -> int:
    """main / iteration: foundation checks per presentation, then the evaluation hook of parts 2 and 3 if it exists."""
    import data
    import foundation
    import provenance
    log = ctx["log"]
    names = CONFIG["stages"][ctx["stage"]]["presentations"]
    import leakage
    oulad = data.load_oulad(log)
    ctx["oulad"], ctx["counter"] = oulad, leakage.ScoreCounter()
    names = names if isinstance(names, list) else sorted(oulad.rows)
    if ctx["only"]:
        if ctx["only"] not in names:
            raise SystemExit(f"error: --only {ctx['only']} is not in this stage's matrix")
        names = [ctx["only"]]
    spec = importlib.util.find_spec("evaluate")
    evaluation = spec is not None and spec.origin is not None and Path(spec.origin).resolve().parent == CODE_DIR
    for pres in names:
        prep = foundation.prepare(oulad, pres, log)
        report = foundation.verify(prep, log)
        (ctx["artifact_dir"] / f"foundation_{pres}.json").write_text(json.dumps(report, indent=2, default=common._jsonable), encoding="utf-8")
        if evaluation:
            import evaluate
            evaluate.run_presentation(prep, ctx)  # parts 2 and 3: models, scoring, metrics; must call the leakage checks
        del prep
    if evaluation:
        evaluate.finalize(ctx)  # L6, C1-C4, reporting tables
    if not evaluation:
        for name in provenance.SEVEN_OBJECTS[3:]:
            log.unchecked(f"L2/L7:{name}", "fitted by code/cell.py, which only evaluate.py (part 3) calls")
        log.unchecked("L6", "no model scores the test split in this build")
        log.unchecked("EVALUATION", "code/evaluate.py (part 3) is not installed; no metric was computed")
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    art, log_path = check_paths(args)
    if args.only and args.stage == "pilot":
        raise SystemExit("error: --only applies to main and iteration")
    if args.dry_run:
        print(f"dry run ok: stage={args.stage} artifact_dir={art} run_log={log_path}")
        return 0
    started, wall0, cpu0 = now(), time.time(), time.process_time()
    art.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {"schema_version": 1, "stage": args.stage, "unit": art.name, "artifact_dir": str(art), "run_log": str(log_path),
                "only": args.only, "argv": sys.argv, "command_line": shlex.join([sys.executable, *sys.argv]), "seed": common.SEED,
                "random_seeds": list(common.RANDOM_SEEDS), "config_sha256": common.sha256_file(CODE_DIR / "configs" / "experiments.json"),
                "code_tree_sha256": common.code_tree_sha256(), "started_at": started, "hard_constraints": common.HARD_CONSTRAINTS,
                **environment()}
    (art / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")  # the first file written
    log = RunLog(log_path, args.stage, art.name)
    log.emit("start", **manifest)
    ctx = {"stage": args.stage, "artifact_dir": art, "log": log, "only": args.only}
    code, status = 1, "failed"
    try:
        if args.stage == "pilot":
            code = run_pilot(ctx)
        elif args.stage == "diagnostics":
            code = run_diagnostics(ctx)
        else:
            code = run_matrix(ctx)
        status = "completed" if code == 0 else "completed_with_failed_criterion"
    except BaseException as exc:  # recorded, then re-raised as a non-zero exit: never a silent partial result
        log.emit("abort", error=f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
    wall, cpu = time.time() - wall0, time.process_time() - cpu0
    import leakage
    import verdicts
    child = leakage.CHILD_SECONDS[0]  # wall seconds of the fresh-process L7 workers: time.process_time() cannot see children
    timing = {"wall_clock_seconds": round(wall, 2), "process_cpu_seconds": round(cpu, 2), "child_worker_wall_seconds": round(child, 2),
              "cpu_hours": (cpu + child) / 3600, "hardware": manifest["hardware"]}
    try:
        crit = verdicts.build(args.stage, ctx, timing, status == "failed")
    except Exception as exc:  # a verdict failure must not hide the run summary
        log.emit("abort", error=f"verdicts: {type(exc).__name__}: {exc}")
        crit, code = {}, 1
    (art / "criteria_verdicts.json").write_text(json.dumps(crit, indent=2, default=common._jsonable), encoding="utf-8")
    summary = {"status": status, "exit_code": code, "started_at": started, "finished_at": now(), **timing,
               "criteria": {c: v["verdict"] for c, v in crit.items()}, "assertions": log.summary()}
    (art / "run_summary.json").write_text(json.dumps(summary, indent=2, default=common._jsonable), encoding="utf-8")
    log.emit("end", **{k: v for k, v in summary.items() if k != "assertions"})
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

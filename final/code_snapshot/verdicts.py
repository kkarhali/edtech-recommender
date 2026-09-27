"""Criteria C1-C6: threshold text copied verbatim from plan.md, one verdict each (met / not met / not met (unchecked conjunct) /
unchecked) with the values behind it, written as criteria_verdicts.json. Each stage decides only what it measured."""
from __future__ import annotations

import json
import re

from common import HARD_CONSTRAINTS, PROJECT_ROOT
from stats import MET, NOT_MET, NOT_MET_UNCHECKED, UNCHECKED


def load_criteria() -> dict:
    """metric / threshold / on_dataset strings of each criterion, verbatim from the frozen plan.md front matter."""
    text = (PROJECT_ROOT / "plan.md").read_text(encoding="utf-8").split("\n---\n")[0]
    out = {}
    for block in re.split(r"\n  - id: ", text)[1:]:
        cid = block.split("\n")[0].strip()
        out[cid] = {f: json.loads(re.search(rf'\n    {f}: ("(?:[^"\\]|\\.)*")', block).group(1)) for f in ("metric", "threshold", "on_dataset")}
    return out


def _combine(parts: dict) -> str:
    """parts: conjunct -> True / False / None (None = not checked by this stage)."""
    if any(v is False for v in parts.values()):
        return NOT_MET
    if any(v is None for v in parts.values()):
        return NOT_MET_UNCHECKED if any(v is True for v in parts.values()) else UNCHECKED
    return MET


def build(stage: str, ctx: dict, timing: dict, failed: bool) -> dict:
    crit = load_criteria()
    out = {c: {**t, "verdict": UNCHECKED, "reason": "run aborted before this criterion was measured" if failed else "not decided by this stage", "values": {}}
           for c, t in crit.items()}
    cpu_h = timing["cpu_hours"]
    if failed:
        return out
    if stage == "pilot":
        c6 = ctx["c6"]
        ok = c6["max_abs_diff"] <= c6["tolerance"] and c6["other_fields_differing"] == 0
        out["C6"].update(verdict=MET if ok else NOT_MET, reason="decided by this reproduction run; the runner adds the receipt hash and command line",
                         values={**c6, "assertions_L1_L9": "not applicable: no bound (protocol 5.5)"})
        repro = ctx["repro_minutes"] <= HARD_CONSTRAINTS["max_minutes_phase1_reproduction"]
        out["C5"].update(verdict=_combine({"reproduction_minutes<=15": repro, "main_run_cpu_hours<=4.0": None}), reason="reproduction conjunct only",
                         values={"reproduction_minutes": ctx["repro_minutes"], "hardware": HARD_CONSTRAINTS["hardware"]})
        return out
    for cid, r in ctx.get("stats", {}).items():
        out[cid].update(r)
    main_ok = cpu_h <= HARD_CONSTRAINTS["max_cpu_hours_main"] if len(ctx.get("acc", {})) == 22 else None
    out["C5"].update(verdict=_combine({"main_run_cpu_hours<=4.0": main_ok, "reproduction_minutes<=15": None}),
                     reason="main-run conjunct only; the reproduction conjunct is decided by the pilot-stage run",
                     values={**timing, "process": "single process plus one fresh-process worker for L7 (wall seconds counted as CPU, an upper bound)",
                             "hardware": HARD_CONSTRAINTS["hardware"], "n_presentations": len(ctx.get("acc", {}))})
    return out

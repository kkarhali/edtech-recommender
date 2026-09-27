"""Shared constants, paths, the append-only run log and canonical hashing.

Every hard constraint of idea.md is a literal in this file (HARD_CONSTRAINTS) so a reviewer can trace it.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np

CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent
REPO_ROOT = PROJECT_ROOT.parents[2]
CONFIG = json.loads((CODE_DIR / "configs" / "experiments.json").read_text(encoding="utf-8"))

SEED = CONFIG["seed"]  # the one seed (protocol s12); used unmodified for the cohort draw, bootstrap, LR random_state
RANDOM_SEEDS = tuple(CONFIG["random_seeds"])  # declared list for the Random baseline (42-46)
KS_COLD = tuple(CONFIG["ks"])
MIN_ITEMS, MIN_DAYS = 5, 3  # filters P4a, P4b
COHORT_FRACTION = 0.20  # protocol 6.1b
TOP_KS, PRIMARY_K = (5, 10, 20), 10
HARD_CONSTRAINTS = {  # idea.md / plan.md: each is a literal here and nowhere else
    "identical_splits_for_all_models": True,
    "hardware": "single CPU, no GPU",
    "downloaded_model_weights": False,
    "max_cpu_hours_main": 4.0,
    "max_minutes_phase1_reproduction": 15.0,
    "reference_pdfs_read_only": True,
}


class LeakageError(RuntimeError):
    """A measured assertion count differed from its required value."""


class DataIntegrityError(RuntimeError):
    """A raw file does not match inputs/manifest.json."""


def _jsonable(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    if isinstance(o, Path):
        return str(o)
    raise TypeError(f"not JSON serialisable: {type(o)}")


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canon_hash(*arrays) -> str:
    """SHA256 over dtype, shape and bytes of each array; callers fix dtype and row order first."""
    h = hashlib.sha256()
    for a in arrays:
        a = np.ascontiguousarray(a)
        h.update(f"{a.dtype.str}{a.shape}".encode())
        h.update(a.tobytes())
    return h.hexdigest()


def code_tree_sha256() -> str:
    h = hashlib.sha256()
    for p in sorted(CODE_DIR.rglob("*")):
        if p.is_file() and p.suffix in (".py", ".json") and "__pycache__" not in p.parts:
            h.update(p.relative_to(CODE_DIR).as_posix().encode())
            h.update(sha256_file(p).encode())
    return h.hexdigest()


def environment() -> dict:
    import pandas
    import scipy
    import sklearn

    return {
        "python": sys.version.split()[0], "executable": sys.executable, "platform": platform.platform(),
        "hardware": f"{platform.processor() or platform.machine()}, {os.cpu_count()} logical cores, no GPU",
        "numpy": np.__version__, "pandas": pandas.__version__,
        "scikit_learn": sklearn.__version__, "scipy": scipy.__version__,
    }


class RunLog:
    """Append-only JSON-lines log. Every assertion is emitted with its measured count, zero included."""

    def __init__(self, path: Path, stage: str, unit: str):
        self.path, self.base = Path(path), {"stage": stage, "unit": unit}
        self.executed: dict[str, list] = {}  # assertion id -> list of (count, required)
        self.unchecked_ids: dict[str, str] = {}
        self.flags: list[dict] = []
        self.provenance: list[dict] = []

    def emit(self, event: str, **kw) -> None:
        rec = {"ts": now(), **self.base, "event": event, **kw}
        with self.path.open("a", encoding="utf-8") as fh:  # append only; the log never shrinks
            fh.write(json.dumps(rec, default=_jsonable) + "\n")

    def measure(self, check_id: str, count, required=0, na: bool = False, **ctx) -> None:
        """Emit a measured count. A count different from `required` is written first and then aborts the run.

        na=True (protocol 5.5): the assertion has no bound to check on this split (currently L2 and L3 on the tertiary split,
        the same treatment L1 and L9 already give it) -- the measured count is still written, as evidence, but with status
        not_applicable, and the run does not abort regardless of the count. Callers elsewhere never pass na, so this changes
        nothing about how L2 and L3 behave on the primary split, the secondary split, or any cold-start condition of section 6,
        where a bound is defined and the count must be zero."""
        count, required = int(count), int(required)
        ok = count == required
        self.executed.setdefault(check_id, []).append((count, required))
        if na:
            self.emit("assert", id=check_id, count=count, required=required, status="not_applicable", **ctx)
            return
        self.emit("assert", id=check_id, count=count, required=required, status="pass" if ok else "FAIL", **ctx)
        if not ok:
            raise LeakageError(f"{check_id}: measured {count}, required {required}, context {ctx}")

    def flag(self, check_id: str, count, required=0, **ctx) -> bool:
        """Like measure but advisory: emits status FLAG instead of aborting. Returns True when count == required."""
        count, required = int(count), int(required)
        ok = count == required
        self.executed.setdefault(check_id, []).append((count, required))
        if not ok:
            self.flags.append({"id": check_id, "count": count, "required": required, **ctx})
        self.emit("assert", id=check_id, count=count, required=required, status="pass" if ok else "FLAG", **ctx)
        return ok

    def unchecked(self, check_id: str, reason: str) -> None:
        """Rule 6: an assertion that did not run is `unchecked`, never `passed`."""
        self.unchecked_ids[check_id] = reason
        self.emit("unchecked", id=check_id, reason=reason)

    def summary(self) -> dict:
        return {"executed": {k: len(v) for k, v in sorted(self.executed.items())},
                "unchecked": dict(self.unchecked_ids), "flags": self.flags}

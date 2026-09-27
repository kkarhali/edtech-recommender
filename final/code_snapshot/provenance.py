"""Provenance records (protocol 5.4): (object_name, n_source_rows, n_rows_outside_allowed, n_learners_used,
n_cold_learners_used) for every fitted object and preprocessing constant, produced by set difference against the
rows the fitting function actually read, and emitted to the run log even when every count is zero."""
from __future__ import annotations

import numpy as np

SEVEN_OBJECTS = ("similarity_matrix", "mostpop_counts", "popweek_counts", "N_selection", "C_selection",
                 "blend_model", "blend_standardiser")
FOUNDATION_OBJECTS = SEVEN_OBJECTS[:3]  # the objects part 1 builds; parts 2 and 3 supply the other four


def record(name: str, read, prep, allowed_ids, roles, cold_ids=()) -> dict:
    """`read` = the frame the function consumed (raw rows or pairs; needs id_student, id_site). Allowed = the pairs of
    `allowed_ids` whose role is in `roles`. Counts come from a merge, not from inspecting the code."""
    ok = prep.pairs[prep.pairs.id_student.isin(np.asarray(allowed_ids)) & prep.pairs.role.isin(roles)][["id_student", "id_site"]].assign(_ok=1)
    merged = read[["id_student", "id_site"]].merge(ok, how="left", on=["id_student", "id_site"])
    used = read.id_student.unique()
    return {"object_name": name, "n_source_rows": int(len(read)), "n_rows_outside_allowed": int(merged["_ok"].isna().sum()),
            "n_learners_used": int(len(used)), "n_cold_learners_used": int(np.isin(used, np.asarray(cold_ids)).sum())}


def emit(log, rec: dict, expected_cold: int = 0, check: str = "L2", **ctx) -> dict:
    """L2 (fitted object) or L3 (constant) on rows outside `allowed`, and L7 on cold learners read. L2 and L3 abort on non-zero,
    except on the tertiary split (protocol 5.5), which has no training bound (variants.tertiary) so a fitted object reading
    every row of a learner's pairs is the split's own design, not a leak; there the measured count is recorded as evidence with
    status not_applicable and the run does not abort -- the same treatment L1 and L9 already give that split. L7 is unaffected
    and still aborts (or reports info for Condition B) on any split, because cold-learner leakage has nothing to do with the
    missing bound."""
    log.provenance.append({**rec, **ctx})
    log.measure(check, rec["n_rows_outside_allowed"], na=(check in ("L2", "L3") and ctx.get("split") == "tertiary"), **rec, **ctx)
    if expected_cold is None:  # Condition B fits on the cohort by design: the count is emitted, not required to be zero
        log.emit("assert", id="L7", count=rec["n_cold_learners_used"], required=None, status="info", object=rec["object_name"], **ctx)
    else:
        log.measure("L7", rec["n_cold_learners_used"], required=expected_cold, object=rec["object_name"], **ctx)
    return rec


def catalogue_constant(log, name: str, n_source_rows: int, **ctx) -> None:
    """L3 for a catalogue-derived constant: it reads no learner row, and the count says so."""
    log.measure("L3", 0, object=name, n_source_rows=n_source_rows, n_learner_rows_used=0, **ctx)


def coverage(log, objects, **ctx) -> None:
    """L2 coverage: every expected object must have a provenance record for this (presentation, condition, k)."""
    have = {r["object_name"] for r in log.provenance if all(r.get(k) == v for k, v in ctx.items())}
    missing = [o for o in objects if o not in have]
    log.measure("L2_objects_without_record", len(missing), missing=missing, **ctx)

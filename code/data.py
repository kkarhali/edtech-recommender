"""Module A, loading: OULAD tables with SHA256 verification, item metadata and the P5 item features."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from common import CONFIG, PROJECT_ROOT, REPO_ROOT, DataIntegrityError, sha256_file

RAW_FILES = ("studentVle.csv", "vle.csv", "courses.csv", "studentRegistration.csv")
RAW_PREFIX = "data/projects/e_learning_pilot/data/raw/"
ACTIVITY_TYPES = (  # the 20 values of vle.csv (protocol 3.1)
    "dataplus", "dualpane", "externalquiz", "folder", "forumng", "glossary", "homepage", "htmlactivity",
    "oucollaborate", "oucontent", "ouelluminate", "ouwiki", "page", "questionnaire", "quiz",
    "repeatactivity", "resource", "sharedsubpage", "subpage", "url")


def raw_dir() -> Path:
    return REPO_ROOT / CONFIG["raw_dir"]


def verify_raw_files(directory: Path, log=None, names=RAW_FILES) -> dict:
    """SHA256 and size of every file used, against inputs/manifest.json. A mismatch raises before any use."""
    manifest = json.loads((PROJECT_ROOT / "inputs" / "manifest.json").read_text(encoding="utf-8"))
    expected = {Path(e["path"]).name: e for e in manifest["inputs"] if e["path"].startswith(RAW_PREFIX)}
    out = {}
    for name in names:
        want, path = expected.get(name), Path(directory) / name
        if want is None or not path.is_file():
            raise DataIntegrityError(f"{name}: missing from manifest or from {directory}")
        size, digest = path.stat().st_size, sha256_file(path)
        if size != want["bytes"] or digest != want["sha256"]:
            raise DataIntegrityError(f"{name}: sha256/size {digest}/{size} != manifest {want['sha256']}/{want['bytes']}")
        out[name] = digest
        if log is not None:
            log.emit("data_sha256", file=name, sha256=digest, bytes=size, manifest_match=True)
    return out


@dataclass
class Oulad:
    rows: dict  # presentation -> DataFrame(id_student, id_site, date, sum_click), raw duplicate rows kept
    items: dict  # presentation -> DataFrame(id_site, activity_type, week_from, week_to) sorted by id_site
    length: dict
    registered: dict
    sha256: dict


def load_oulad(log=None) -> Oulad:
    directory = raw_dir()
    sha = verify_raw_files(directory, log)
    dtypes = {"code_module": str, "code_presentation": str, "id_student": "int64", "id_site": "int64",
              "date": "int64", "sum_click": "int64"}
    sv = pd.read_csv(directory / "studentVle.csv", dtype=dtypes)
    keep = ["id_student", "id_site", "date", "sum_click"]
    rows = {f"{m}_{p}": g[keep].reset_index(drop=True) for (m, p), g in sv.groupby(["code_module", "code_presentation"], sort=True)}
    del sv
    vle = pd.read_csv(directory / "vle.csv", dtype=str)
    unknown = set(vle.activity_type) - set(ACTIVITY_TYPES)
    if unknown:
        raise DataIntegrityError(f"activity types outside the 20 of protocol 3.1: {sorted(unknown)}")
    items = {}
    for (m, p), g in vle.groupby(["code_module", "code_presentation"], sort=True):
        t = pd.DataFrame({
            "id_site": g["id_site"].astype("int64").to_numpy(), "activity_type": g["activity_type"].to_numpy(),
            "week_from": pd.to_numeric(g["week_from"], errors="coerce").to_numpy(dtype=float),  # '?' -> NaN
            "week_to": pd.to_numeric(g["week_to"], errors="coerce").to_numpy(dtype=float)})
        t = t.sort_values("id_site", kind="stable").reset_index(drop=True)
        if not t.id_site.is_unique:
            raise DataIntegrityError(f"duplicate id_site in vle.csv for {m}_{p}")
        items[f"{m}_{p}"] = t
    courses = pd.read_csv(directory / "courses.csv", dtype=str)
    length = {f"{m}_{p}": int(n) for m, p, n in zip(courses.code_module, courses.code_presentation, courses.module_presentation_length)}
    reg = pd.read_csv(directory / "studentRegistration.csv", dtype={"code_module": str, "code_presentation": str, "id_student": "int64"},
                      usecols=["code_module", "code_presentation", "id_student"])
    registered = {f"{m}_{p}": int(n) for (m, p), n in reg.groupby(["code_module", "code_presentation"]).id_student.nunique().items()}
    return Oulad(rows, items, length, registered, sha)


def item_features(items: pd.DataFrame) -> tuple[np.ndarray, dict]:
    """P5 and the protocol-8 CBF item vectors: 20 one-hot activity dims, min-max week_from and week_to, week_missing.

    Reads the catalogue only (no learner row), so assertions A4 and L3 hold by construction and are measured as such.
    A wholly missing week column falls back to 0.0 (the pilot's median of an empty column was NaN).
    """
    def fill(x):
        known = x[~np.isnan(x)]
        med = float(np.median(known)) if known.size else 0.0  # P5 fallback
        return np.where(np.isnan(x), med, x), med, int(known.size)

    def minmax01(x):
        lo, hi = float(x.min()), float(x.max())
        return (x - lo) / (hi - lo) if hi - lo >= 1e-12 else np.zeros_like(x)

    wf, wt = items.week_from.to_numpy(dtype=float), items.week_to.to_numpy(dtype=float)
    wf_f, wf_med, wf_known = fill(wf)
    wt_f, wt_med, wt_known = fill(wt)
    onehot = np.stack([(items.activity_type == a).to_numpy() for a in ACTIVITY_TYPES], axis=1).astype(float)
    mat = np.column_stack([onehot, minmax01(wf_f), minmax01(wt_f), np.isnan(wf).astype(float)])
    if not np.isfinite(mat).all():
        raise DataIntegrityError("non-finite item feature matrix")
    consts = {"week_from_median": wf_med, "week_to_median": wt_med, "week_from_known": wf_known, "week_to_known": wt_known,
              "week_from_min_max": [float(wf_f.min()), float(wf_f.max())], "week_to_min_max": [float(wt_f.min()), float(wt_f.max())],
              "week_missing_share": float(np.isnan(wf).mean()), "n_learner_rows_used": 0,
              "all_missing_columns": [n for n, k in (("week_from", wf_known), ("week_to", wt_known)) if k == 0]}
    return mat, consts

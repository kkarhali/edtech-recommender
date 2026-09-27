"""Fresh-process worker for the section 6.1a rebuild check. Reads a pickled payload on stdin (rows and pairs of the fit
learners only; the cold cohort's rows are physically absent), rebuilds every registered learner-derived object, hashes
inside this process and prints one JSON line. Writes no file."""
from __future__ import annotations

import importlib
import json
import pickle
import sys

import numpy as np

import features


def main() -> int:
    p = pickle.loads(sys.stdin.buffer.read())
    for m in p["modules"]:
        importlib.import_module(m)
    view = features.View(**p["view"])
    cold = np.asarray(p["cold_ids"])
    n_cold = int(view.pairs.id_student.isin(cold).sum() + view.rows.id_student.isin(cold).sum() + view.learners.index.isin(cold).sum())
    hashes = features.build_all(view, p["name"], p["fit_ids"], p["ks"])
    print(json.dumps({"hashes": hashes, "n_cold_rows_in_worker": n_cold}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

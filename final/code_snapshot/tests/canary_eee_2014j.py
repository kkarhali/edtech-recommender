"""Canary for the runner, to execute before any full run:  python code\\tests\\canary_eee_2014j.py
EEE_2014J, Condition A, k = 2, models fitted on the 80% warm learners, scored on the 204-learner cohort drawn in RANK order
(protocol 6.1b, 7.1). It writes no file and prints a table; exit 0 only if all six values match the protocol's four decimals:

                                     no exclusion | exclusion = visible k (adopted) | exclusion = training u validation (discarded)
    MostPop                              0.0137   |            0.0255               |            0.2157
    ItemKNN-CF (N = all, self-sim kept)  0.0279   |            0.0333               |            0.1946

A mismatch in the middle column points at the cohort draw, the exclusion set or the click bound; a low cold-start value is
NOT a bug when this canary passes (cold-start Precision@10 is small by nature)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common  # noqa: E402
import data  # noqa: E402
import models  # noqa: E402
import splits  # noqa: E402
from splits import TEST, TRAIN, VAL  # noqa: E402

PRES = "EEE_2014J"
EXPECTED = {"MostPop": (0.0137, 0.0255, 0.2157), "ItemKNN-CF": (0.0279, 0.0333, 0.1946)}


class Quiet(common.RunLog):
    def __init__(self):
        super().__init__(Path("unused"), "canary", "canary")

    def emit(self, *a, **k):
        pass


def main() -> int:
    log, ou = Quiet(), data.load_oulad(None)
    prep = splits.build_prep(ou, PRES, log)
    cond = splits.make_condition(prep, "A", 2)
    ctx = models.Ctx(prep, cond, ou.length[PRES], 0)
    ids = np.sort(cond.eval_ids)
    assert len(ids) == 204 and len(cond.fit_ids) == 814, (len(ids), len(cond.fit_ids))
    h = models.make_history(prep, ids, True, 2, "M3", "canary")
    truth = models.pair_mask(prep, ids, (TEST,))[0]
    none, visible = np.zeros_like(h.excl), h.excl
    train_val = models.pair_mask(prep, ids, (TRAIN, VAL))[0]  # the discarded revision-1 rule
    rows = {"MostPop": np.tile(ctx.counts.astype(float), (len(ids), 1)), "ItemKNN-CF": models.cf_scores(h.H, ctx.sim_n("all"))}
    bad = 0
    print(f"{'model':12s} {'no exclusion':>13s} {'visible k':>10s} {'train+val':>10s}")
    for name, s in rows.items():
        got = tuple(round(float(models.precision10(s, ex, truth).mean()), 4) for ex in (none, visible, train_val))
        ok = all(abs(g - e) < 5.1e-5 for g, e in zip(got, EXPECTED[name]))
        bad += not ok
        print(f"{name:12s} {got[0]:13.4f} {got[1]:10.4f} {got[2]:10.4f}   expected {EXPECTED[name]}  {'OK' if ok else 'MISMATCH'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

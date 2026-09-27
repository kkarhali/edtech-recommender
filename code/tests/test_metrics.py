"""Hand-computed tests (templates/metric_tests.md plus split and cohort toys). Run: python tests/test_metrics.py (or pytest)."""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import metrics as m  # noqa: E402
import splits  # noqa: E402

RANKED = ["i1", "i2", "i6", "i3", "i4"]  # hits: i2 at rank 2, i3 at rank 4; i5 is never recommended
TRUTH = {"i2", "i3", "i5"}


def close(a, b):
    assert abs(a - b) < 5e-5, (a, b)


def test_precision_divides_by_k():
    close(m.precision_at_k(RANKED, TRUTH, 3), 1 / 3)
    close(m.precision_at_k(RANKED, TRUTH, 5), 0.4)
    close(m.precision_at_k(["i2"], TRUTH, 10), 0.1)  # a short list still divides by K


def test_recall():
    close(m.recall_at_k(RANKED, TRUTH, 3), 1 / 3)
    close(m.recall_at_k(RANKED, TRUTH, 5), 2 / 3)


def test_hitrate_and_mrr():
    assert m.hitrate_at_k(RANKED, TRUTH, 3) == 1 and m.hitrate_at_k(RANKED, TRUTH, 5) == 1
    assert m.hitrate_at_k(["i1"], TRUTH, 5) == 0
    close(m.mrr_at_k(RANKED, TRUTH, 3), 0.5)
    close(m.mrr_at_k(RANKED, TRUTH, 5), 0.5)
    assert m.mrr_at_k(RANKED, TRUTH, 1) == 0


def test_ndcg():
    close(m.ndcg_at_k(RANKED, TRUTH, 3), (1 / math.log2(3)) / (1 + 1 / math.log2(3) + 0.5))  # 0.2961
    close(m.ndcg_at_k(RANKED, TRUTH, 3), 0.2961)
    close(m.ndcg_at_k(RANKED, TRUTH, 5), 0.4982)
    close(m.ndcg_at_k(["i2", "i3", "i5"], TRUTH, 5), 1.0)


def test_rank_order_score_desc_then_id_asc():
    ids = np.array([10, 20, 30, 40, 50])
    assert m.rank_topk([1.0, 3.0, 3.0, 1.0, 2.0], ids, set(), 5) == [20, 30, 50, 10, 40]
    assert m.rank_topk(np.zeros(5), ids, {20}, 3) == [10, 30, 40]  # all equal: id ascending; excluded removed first
    assert m.rank_topk([1.0 + 1e-14, 1.0, 0.0, 0.0, 0.0], ids, set(), 2) == [10, 20]  # 12-decimal rounding makes 10 and 20 tie
    assert m.rank_topk([1.0, 2.0], np.array([1, 2]), set(), 5) == [2, 1]  # fewer than K candidates: short list


def test_nonfinite_scores_raise():
    try:
        m.rank_topk([1.0, float("nan")], np.array([1, 2]), set(), 2)
    except ValueError:
        return
    raise AssertionError("NaN scores must raise")


def test_no_truth_learner_is_excluded_and_counted():
    out = m.aggregate({1: ["a", "b"], 2: ["a"]}, {1: {"a"}, 2: set()}, ks=(5,))
    assert out["n_learners"] == 1 and out["n_excluded_no_truth"] == 1
    close(out["precision@5"]["mean"], 0.2)


def test_split_learner_day_boundary():
    fd = np.repeat([-3, 0, 1, 5, 6, 9, 10, 20], [4, 3, 2, 2, 3, 2, 2, 2])  # n = 20, suffix 20,16,13,11,9,6,4,2
    assert splits.split_learner(fd) == (9, 10)  # test = days 7-8 (4 pairs = 0.20 n), validation = day 6 (2 pairs = 0.10 n)


def test_cohort_quotas_and_rank_order():
    n = 1018
    learners = pd.DataFrame({"n_train": np.arange(n)}, index=pd.Index(np.arange(1000, 1000 + n), name="id_student"))
    cohort = splits.draw_cohort(learners)
    assert len(cohort) == 204 and len(set(cohort)) == 204
    cuts = [0, 204, 407, 611, 814, 1018]
    got = [int(((cohort >= 1000 + cuts[j]) & (cohort < 1000 + cuts[j + 1])).sum()) for j in range(5)]
    assert got == [41, 41, 41, 40, 41], got
    assert (splits.draw_cohort(learners) == cohort).all()  # deterministic


def test_matrix_ranking_agrees_with_rank_topk_and_minmax_rule():
    import models
    ids = np.array([10, 20, 30, 40, 50])
    sc = np.array([[1.0, 3.0, 3.0, 1.0, 2.0], [0.0, 0.0, 0.0, 0.0, 0.0]])
    ex = np.array([[False, False, False, False, False], [False, True, False, False, False]])
    assert models.rank_lists(sc, ex, ids, 5) == [m.rank_topk(sc[0], ids, set(), 5), [10, 30, 40, 50]]
    z = models.minmax_rows(sc, ex)
    assert (z[1] == 0).all() and abs(z[0][1] - 1.0) < 1e-12 and z[0][0] == 0.0  # constant vector -> zeros (k = 0 consequence)
    assert models.a5_mismatches(sc, ex, z) == 0


def test_precision10_masks():
    import models
    sc = np.arange(12, 0, -1, dtype=float)[None, :]  # items 0..11, best first
    truth = np.zeros((1, 12), dtype=bool)
    truth[0, [0, 1, 11]] = True
    ex = np.zeros((1, 12), dtype=bool)
    assert models.precision10(sc, ex, truth)[0] == 0.2  # items 0 and 1 hit, item 11 is outside the top 10
    ex[0, 0] = True  # excluded item leaves the list: top 10 is items 1..10, one hit
    assert models.precision10(sc, ex, truth)[0] == 0.1


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)

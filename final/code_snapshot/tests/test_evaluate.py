"""Tests for evaluate.py, stats.py and the Module D isolation rule. Run: python tests/test_evaluate.py (or pytest)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evaluate  # noqa: E402
import metrics as m  # noqa: E402
import stats  # noqa: E402

CODE = Path(__file__).resolve().parents[1]


def test_vector_metrics_match_list_metrics():
    rng = np.random.default_rng(0)
    names = {"P": "precision", "R": "recall", "HR": "hitrate", "MRR": "mrr", "NDCG": "ndcg"}
    for _ in range(30):
        ranked = rng.permutation(40)[:20].tolist()
        truth = set(rng.choice(40, size=int(rng.integers(1, 15)), replace=False).tolist())
        vm = evaluate.vector_metrics(np.array([[i in truth for i in ranked]]), np.array([len(truth)]))
        ref = m.learner_metrics(ranked, truth)
        for key, v in vm.items():
            short, k = key.split("@")
            assert abs(v[0] - ref[f"{names[short]}@{k}"]) < 1e-12, key


def test_holm():
    assert np.allclose(stats.holm([0.01, 0.04]), [0.02, 0.04])
    assert np.allclose(stats.holm([0.04, 0.01]), [0.04, 0.02])
    assert stats.holm([0.01, None]) == [0.02, None]


def test_wilcoxon_zero_rule_and_inconclusive_wording():
    w = stats.wilcoxon_paired([1, 1, 1, 2, 3, 4], [1, 1, 0, 0, 0, 0])
    assert w["n_eff"] == 4 and w["n_zero_dropped"] == 2
    rows = {"a": {"median_rel_gain": 0.5, "wilcoxon": {"n_eff": 4}, "p_holm": None}}
    assert stats.decide(rows, 0.1, False)[0] == stats.NOT_MET_UNCHECKED  # threshold met, test inconclusive: never "met"
    rows["a"]["median_rel_gain"] = 0.05
    assert stats.decide(rows, 0.1, False)[0] == stats.NOT_MET


def test_rel_gain_excludes_zero_baseline_and_sign_test():
    g, n = stats.rel_gain([1.0, 2.0], [0.0, 1.0])
    assert list(g) == [1.0] and n == 1
    assert abs(stats.sign_test([1, 2, 3], [0, 0, 0])["p"] - 0.25) < 1e-12


def test_behaviour_feeds_no_model():
    for name in ("models.py", "blend.py", "cell.py", "features.py", "splits.py", "provenance.py", "leakage.py"):
        assert "behaviour" not in (CODE / name).read_text(encoding="utf-8"), name


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)

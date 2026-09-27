E-learning recommendation system based on user behavior analysis (MSc thesis pilot experiment)

Source: MSc thesis proposal (Web Sciences, Syrian Virtual University), "A recommendation
system for e-learning based on user behavior analysis." Background, baselines, and pitfalls
are recorded in knowledge_base/e_learning_recommendation.md (9 reviewed papers, all read-only
source PDFs at src/reasearch_topic/References/ for reference only — do not modify).

Hypothesis:
A hybrid recommender that combines (a) content-based filtering over course/content metadata,
(b) collaborative filtering over learner-content interaction history, and (c) a behavioral
session signal (browsing sequence, dwell time, engagement pattern, as used for student
profiling in the reviewed literature) will produce more accurate and more robust
recommendations for e-learning content than either content-based or collaborative filtering
alone, and will specifically outperform them on cold-start learners (users with very little
interaction history), which the reviewed hybrid baselines identify as the main failure mode of
single-technique approaches.

Success criteria (all must be checked and reported numerically, not qualitatively):
1. Primary: the hybrid model's Precision@10 (or equivalent top-K ranking accuracy) on held-out
   warm-user sessions is at least 10% higher (relative) than both a content-based-only baseline
   and a collaborative-filtering-only baseline, trained and evaluated on the same split.
2. Cold-start: on a held-out set of simulated/actual new users (<=2 prior interactions), the
   hybrid model must produce non-degenerate top-K recommendations (not empty, not identical
   for every user) and must not simply fall back to global popularity ranking without at least
   matching the content-based-only baseline's Precision@10 on that same cold-start slice.
3. Anti-cheating / feasibility bound: pilot training + evaluation must complete within the
   compute budget below; report wall-clock time and hardware used.
4. If a numeric target in (1) cannot be met, report the actual numbers, the gap, and the most
   likely cause (data volume, weak behavioral signal, model capacity) rather than adjusting the
   threshold after the fact.

DATASET DECISION (resolved by the operator, recorded here for provenance):
The thesis proposal does not name a dataset already in hand, and none of the 9 reviewed papers
use a shared, off-the-shelf e-learning dataset (they use MovieLens/Kaggle for adjacent domains,
or custom web-mined/institutional data that is not publicly available). Decision: use the
public Open University Learning Analytics Dataset (OULAD) for this pilot. It provides learner
demographics, VLE clickstream/session logs, and assessment results, which map reasonably well
onto this thesis's "user information + user history logs" variables, and it is a real, citable
public dataset rather than a synthetic stand-in — the pilot's accuracy numbers are therefore a
real (if preliminary) research finding, not just a pipeline smoke test. Trade-off accepted:
requires network access during the pilot to download OULAD once (a few hundred MB). Record this
choice and its limitation (OULAD is a UK Open University population, not the thesis's own
institution) explicitly in plan.md and results/summary.md.

Available data and compute:
- No labeled proprietary dataset is provided by the operator at this time.
- Assume a single CPU or a single consumer/cloud GPU is available for the pilot; do not assume
  a multi-GPU cluster. Runner should probe hardware (nvidia-smi) and choose settings that fit.
- Language/tooling per the thesis: Python, TensorFlow or Keras, scikit-learn. Prefer scikit-learn
  or a lightweight model for the pilot; reserve deep learning (RNN/CNN/RBFNN, per the reviewed
  papers) for the Phase 2 main experiment if the pilot shows the hybrid direction is promising.

Constraints:
- Pilot (Phase 1) time budget: complete within a few hours of wall-clock time on the assumed
  hardware, using a data subset if needed to stay within that budget.
- Do not download large model weights or unrelated pretrained checkpoints for the pilot.
- Keep the three compared models (content-based-only, collaborative-only, hybrid) trained and
  evaluated on identical splits so the comparison in success criterion 1 is fair.
- Treat src/reasearch_topic/References/*.pdf and this idea file's cited papers as read-only
  background; do not attempt to re-scrape or redistribute their content.

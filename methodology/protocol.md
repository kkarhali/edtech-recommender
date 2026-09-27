# Evaluation protocol — e-learning recommendation thesis

- Unit: `u07_s3_methodology`
- Cycle: 0
- Mode: draft
- Plan hash: SHA256 `22bb14a20fe7f111bf342aec51a54b7a3b6daf6c8723e1b5d66120d8d8e462d0` (`plan.md`, 15,766 bytes)
- Idea hash: SHA256 `8be52b93fc723207d876ea7d17654fc5102fb27e502db0eb5521864f15bc1b43` (`idea.md`, 4,506 bytes)
- Written: 2026-09-21

This protocol is authoritative. `thesis/ch03.md` is its readable form and never disagrees with it.
Every count below was taken from the CSV file that holds it, using
`.venv-pilot/Scripts/python.exe` with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUTF8=1`, on
2026-09-21. No count is copied from `OULAD.names` or from any summary document.

---

## 1. Research design

This is a quantitative offline comparison of ranking models on logged learner–resource
interactions in a virtual learning environment. The **unit of analysis** is a learner within one
module presentation; the **replication unit** is the 22 OULAD module presentations; the
**population** is UK Open University distance learners registered on those presentations in 2013
and 2014, further narrowed by the filters of section 4 to learners who interacted with at least
five distinct VLE resources.

What this design can conclude: whether a model ranks a learner's held-out future resources higher
than a competing model does, on the same learners, the same candidate sets and the same ground
truth, and whether that difference replicates across 22 presentations.

What this design cannot conclude, stated here and repeated in the limitations: **offline ranking
accuracy is not learning gain.** A click records that a resource was opened, not that it was read,
understood or useful, and `sum_click` is a count with no duration attached. No causal claim about
learning, retention or attainment follows from any number in this thesis. Nor can the design show
what a learner would have done with a resource the platform never surfaced: the log was produced by
the VLE's own navigation, so an item the learner never opened may be an unobserved positive rather
than a true negative <!-- ledger: castells2022offline -->.

Hypothesis, copied character for character from `plan.md`:

> A hybrid recommender that combines (a) content-based filtering over course/content metadata,
> (b) collaborative filtering over learner-content interaction history, and (c) a behavioral
> session signal (browsing sequence, dwell time, engagement pattern, as used for student
> profiling in the reviewed literature) will produce more accurate and more robust
> recommendations for e-learning content than either content-based or collaborative filtering
> alone, and will specifically outperform them on cold-start learners (users with very little
> interaction history), which the reviewed hybrid baselines identify as the main failure mode of
> single-technique approaches.

### 1.1 Success criteria, copied character for character from `plan.md`

| # | `metric` | `threshold` | `on_dataset` |
| --- | --- | --- | --- |
| C1 (primary) | Precision@10 relative gain, hybrid vs. content-based-only AND hybrid vs. collaborative-only, warm-user held-out slice | >= +0.10 relative against BOTH baselines, median over the 22 module-presentations, AND paired Wilcoxon signed-rank p < 0.05 after Holm correction for both comparisons | OULAD, all 22 module-presentations, time-based split, identical splits for all four models |
| C2 (primary) | Precision@10 relative gain, hybrid vs. collaborative-only AND hybrid vs. content-based-only, cold-start slice built by refitting the similarity model without the held-out learners | > 0 relative against BOTH baselines, median over the 22 module-presentations, AND paired Wilcoxon signed-rank p < 0.05 after Holm correction for both comparisons | OULAD, all 22 module-presentations, cold-start-refit condition, identical splits for all four models |
| C3 (primary) | Cold-start Precision@10, hybrid vs. content-based-only and vs. a global-popularity baseline; non-degeneracy of the hybrid's top-10 lists | >= content-based-only Precision@10 AND > popularity-baseline Precision@10 AND == 0 empty top-10 lists AND >= 10% of available items appearing across the slice's top-10 lists, in each of the 22 module-presentations | OULAD, all 22 module-presentations, cold-start-refit condition |
| C4 (anti-cheating) | Tuning-on-test leakage count: rows shared between the validation split and the test split, and hyperparameters (blend weight, K, similarity cut-off) fitted on any data other than the validation split | == 0 shared rows AND == 0 hyperparameters fitted outside the validation split; the test split is scored exactly once per model per module-presentation | OULAD, all 22 module-presentations |
| C5 (feasibility) | Wall-clock time and hardware for the phase 2 main run and for the phase 1 reproduction | <= 4.0 CPU-hours total for the main run over all 22 module-presentations AND <= 15 minutes for the phase 1 reproduction, on a single CPU with no GPU and no downloaded model weights | OULAD, all 22 module-presentations |
| C6 (anti-cheating) | Absolute difference between the reproduced phase 1 Precision@10 values and the recorded prior-evidence values, all three models, warm and cold-start, on EEE_2014J | <= 1e-6 absolute for every one of the 6 values, with a run receipt carrying the SHA256 of the regenerated metrics file and the exact command line | OULAD, module-presentation EEE_2014J, seed 42, deterministic selection rule |

No threshold in this table is changed, reinterpreted downward or supplemented with an alternative
decision rule anywhere in this protocol. Sections 10.3 to 10.5 fix the *units* that `plan.md`
leaves unstated for C1 to C3; each such decision is recorded in section 16 as an operationalisation
and none of them moves a number.

### 1.2 Decision table: which measurement decides which criterion

| Criterion | Slice | Metric | Aggregation | Deciding test | Script-evaluable expression |
| --- | --- | --- | --- | --- | --- |
| C1 | warm test slice, primary time-based split | Precision@10, macro over learners | median of the 22 per-presentation relative gains | paired Wilcoxon signed-rank over the 22 presentation-level pairs, Holm over family F1 | `median(rel_gain_vs_cbf) >= 0.10 and median(rel_gain_vs_cf) >= 0.10 and p_holm_cbf < 0.05 and p_holm_cf < 0.05` |
| C2 | cold-start **refit** slice, k = 2 | Precision@10, macro over learners | median of the 22 per-presentation relative gains | paired Wilcoxon signed-rank over the 22 presentation-level pairs, Holm over family F2 | `median(rel_gain_vs_cf) > 0 and median(rel_gain_vs_cbf) > 0 and p_holm_cf < 0.05 and p_holm_cbf < 0.05` |
| C3 | cold-start **refit** slice, k = 2 | Precision@10, empty-list count, coverage@10 | per presentation, all 22 must hold | none; C3 is a floor, see section 10.5 | `all(p_hyb[i] >= p_cbf[i] and p_hyb[i] > p_pop[i] and n_empty[i] == 0 and coverage10[i] >= 0.10 for i in range(22))` |
| C4 | all splits | row-set intersections, provenance of each fitted value | per presentation | none | `len(val_rows & test_rows) == 0 and n_params_fitted_outside_validation == 0 and max(test_scoring_count) == 1` |
| C5 | whole run | wall-clock seconds | sum over the run | none | `cpu_hours_main <= 4.0 and minutes_repro <= 15.0` |
| C6 | EEE_2014J | Precision@10 | 6 values | none | `all(abs(new[j] - recorded[j]) <= 1e-6 for j in range(6))` |

Every expression above is a boolean a script evaluates; none is prose a reader must interpret.

---

## 2. Data

Dataset: **Open University Learning Analytics Dataset (OULAD)**.

Citation, as printed on the dataset's data descriptor: Kuzilek J., Hlosta M., Zdrahal Z. *Open
University Learning Analytics dataset*, Nature Scientific Data 4:170171,
doi: 10.1038/sdata.2017.171 (2017) <!-- ledger: kuzilek2017oulad -->.

Source URL originally published in the distributed archive (`OULAD.names`, section 4):
`https://analyse.kmi.open.ac.uk/open_dataset`. As of 2026-09-21 that URL returns HTTP 301 to
`https://research.stem.open.ac.uk/ouanalyse/`, which carries no dataset download and no licence
statement (opened 2026-09-21).

Download date of the local copy: **2026-09-14** (filesystem modification time of
`data/projects/e_learning_pilot/data/raw/oulad.zip`; the extracted CSVs carry the archive's own
2015 timestamps). The exact URL the archive was fetched from is **not recorded** anywhere in this
repository — open question OQ1.

Licence: **CC BY 4.0, verified at the authors' own deposit, with a recorded gap** — see
`methodology/data_statement.md` for the quotation, the URLs opened, the dates, and the residual
gap (the licence was verified at the deposit, not at the URL the local bytes came from).

Population: UK Open University distance learners, 7 modules and 22 module presentations starting
in February ("B") and October ("J") of 2013 and 2014. **Not** the candidate's institution, not
on-campus learners, not a non-UK cohort.

### 2.1 Files, verified

SHA256 and byte size recomputed from the files on 2026-09-21; all eight match
`inputs/manifest.json` exactly. Row counts are data rows, header excluded, counted from the file.

| File | Rows | Size (bytes) | SHA256 | Used for |
| --- | --- | --- | --- | --- |
| `studentVle.csv` | 10,655,280 | 453,836,331 | `52668253d876c5becbcb72185977152700cecab2942aca807fecc3dd54b937f0` | interactions: `id_student`, `id_site`, `date`, `sum_click` |
| `vle.csv` | 6,364 | 270,612 | `d7a146497edd0e47ef536144b58796c07b554002d3753e848b8e4cd8a56f4c38` | item metadata: `activity_type`, `week_from`, `week_to` |
| `studentInfo.csv` | 32,593 | 3,462,763 | `815fbc3e2de29f79900bc63f0345a35db62c9146afaa1d86e7107b8b3beffc60` | population counts only; **no column used as a model feature** (section 3.3) |
| `studentRegistration.csv` | 32,593 | 1,132,550 | `bbc87a0de1fe2a9ec6decce1ca6c1a02cf17b54ad3bdcc673fc6413b41c61d47` | denominator "registered learners" per presentation |
| `courses.csv` | 22 | 526 | `4f16eee7454b15e109b0a21a0e43be820e6846ed6f9301bb7feb5ab5ad737a75` | `module_presentation_length`, used to bound the course-week derivation |
| `assessments.csv` | 206 | 8,211 | `9ce92381e4a0ac457f8e251b2eb2c179ed51e023ab30d1d671a0268bd62316ba` | **not used** |
| `studentAssessment.csv` | 173,912 | 5,690,483 | `b1839e17618a5de36b6d189a242d3123f7939a56c8c9ccef0c17b9199c614a6b` | **not used** |
| `OULAD.names` | 213 lines | 12,278 | `e497bc5232f385ece30a7e964b0339bd9b74ba9b9083508b66628fed9dc23ebe` | documentation only; **no count in this thesis is taken from it** |

### 2.2 Two documentation defects, verified against the data

**Defect 1 — the student count.** `OULAD.names` section 5 states `students in courses: 32953` and
`registration entries: 32953`. `studentInfo.csv` and `studentRegistration.csv` each hold **32,593**
data rows, and `OULAD.names`'s own section 9 class distribution totals **32,593**. The
documentation therefore contradicts both the data and itself, by 360 students. **Every count in
this thesis comes from the CSV, and the figure used is 32,593.** Four other figures in the same
section 5 were checked and are correct: VLE pages 6,364 (= `vle.csv` rows), VLE log entries
10,655,280 (= `studentVle.csv` rows), assessments 206, assessment entries 173,912. A third figure,
32,594, appears in a project artifact outside this protocol and is also wrong; it is the row count
including the header line.

**Defect 2 — the granularity of `studentVle.csv`.** `OULAD.names` describes `sum_click` as "the
number of times a student interacts with the material in that day", which implies one row per
(learner, resource, day). The file does not honour that. In EEE_2014J, 402,947 rows reduce to
303,660 distinct (`id_student`, `id_site`, `date`) triples, so **74,972 triples carry more than
one row**, up to 10 rows for a single triple. Across the whole file, 1,614,505 of 8,459,320
distinct triples are duplicated. Consequence for this protocol: any click total must be produced
by an explicit `sum` over all rows of a group, and any *active-day* count must be a count of
**distinct** `date` values, never a row count. Both rules are fixed in section 4.

### 2.3 Completeness and population, per module presentation

Counted 2026-09-21 from `studentVle.csv`, `vle.csv` and `studentRegistration.csv`. "In VLE" counts
learners with at least one interaction with an item in that presentation's own catalogue. The
column "**>= 5 items**" applies filter P4a of section 4 **only**; the final evaluated population,
after P4b's at-least-3-distinct-days filter, is the `Evaluated` column of **section 4.1**, which is
the authoritative population table and is smaller. `week_from` and `week_to`
share the same missingness pattern in every presentation, so one column is shown.

| Presentation | Interactions | Items | `week_*` known (%) | Registered | In VLE | >= 5 items | Distinct items per >= 5-item learner (mean / median / min / max) | `date` range |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AAA_2013J | 180,982 | 211 | 1.4 | 383 | 378 | 377 | 63.9 / 65 / 8 / 133 | -10 .. 268 |
| AAA_2014J | 169,316 | 202 | 1.5 | 365 | 357 | 350 | 57.7 / 56 / 6 / 128 | -24 .. 269 |
| BBB_2013B | 403,266 | 315 | **0.0** | 1,767 | 1,537 | 1,479 | 38.5 / 35 / 5 / 152 | -9 .. 240 |
| BBB_2013J | 452,638 | 321 | 23.7 | 2,237 | 1,870 | 1,788 | 37.6 / 35 / 5 / 182 | -23 .. 268 |
| BBB_2014B | 273,236 | 311 | 24.4 | 1,613 | 1,294 | 1,222 | 36.5 / 33 / 5 / 163 | -9 .. 234 |
| BBB_2014J | 438,424 | 207 | 16.4 | 2,292 | 1,921 | 1,858 | 58.4 / 60 / 5 / 158 | -9 .. 262 |
| CCC_2014B | 496,181 | 196 | 2.6 | 1,936 | 1,681 | 1,610 | 50.6 / 44 / 5 / 158 | -18 .. 241 |
| CCC_2014J | 711,646 | 223 | 2.2 | 2,498 | 2,302 | 2,196 | 52.1 / 47 / 5 / 211 | -18 .. 269 |
| DDD_2013B | 536,837 | 428 | **0.0** | 1,303 | 1,214 | 1,189 | 105.5 / 103 / 5 / 324 | -16 .. 240 |
| DDD_2013J | 680,806 | 462 | **0.0** | 1,938 | 1,768 | 1,724 | 90.3 / 83 / 5 / 360 | -18 .. 261 |
| DDD_2014B | 379,942 | 453 | 0.2 | 1,228 | 1,116 | 1,081 | 85.3 / 74 / 5 / 328 | -18 .. 241 |
| DDD_2014J | 568,901 | 365 | 0.3 | 1,803 | 1,647 | 1,571 | 74.9 / 69 / 5 / 293 | -25 .. 262 |
| EEE_2013J | 356,262 | 112 | 23.2 | 1,052 | 964 | 923 | 45.6 / 49 / 5 / 84 | -11 .. 268 |
| EEE_2014B | 202,224 | 109 | 23.9 | 694 | 624 | 606 | 41.8 / 45 / 5 / 88 | -18 .. 241 |
| **EEE_2014J** | **402,947** | **115** | 23.5 | **1,188** | **1,097** | **1,049** | **44.8 / 49 / 5 / 90** | -18 .. 269 |
| FFF_2013B | 946,765 | 508 | 4.9 | 1,614 | 1,510 | 1,486 | 122.9 / 114 / 5 / 413 | -18 .. 240 |
| FFF_2013J | 1,172,101 | **529** | 53.5 | 2,283 | 2,098 | 2,052 | 111.8 / 103 / 5 / 340 | -18 .. 268 |
| FFF_2014B | 685,274 | 478 | 54.2 | 1,500 | 1,363 | 1,333 | 98.2 / 91 / 5 / 344 | -18 .. 241 |
| FFF_2014J | 1,210,359 | 452 | 57.3 | 2,365 | 2,121 | 2,043 | 105.4 / 102 / 5 / 325 | -18 .. 269 |
| GGG_2013J | 145,995 | 137 | 2.9 | 952 | 895 | 865 | 34.2 / 35 / 5 / 96 | -16 .. 261 |
| GGG_2014B | 123,319 | 124 | 3.2 | 833 | 773 | 740 | 32.5 / 33 / 5 / 72 | -8 .. 241 |
| GGG_2014J | 117,859 | **106** | 3.8 | 749 | 698 | 667 | 34.6 / 36 / 5 / 72 | -16 .. 269 |

Totals: 10,655,280 interactions, 6,364 items, and **27,212 evaluated learners** after the two
filters of section 4 (29,228 learners appear in the logs; see the full breakdown in section 4.1) across the 22
presentations. Catalogue size ranges from 106 (GGG_2014J) to 529 (FFF_2013J); every interaction row
in `studentVle.csv` refers to an `id_site` present in that presentation's `vle.csv` catalogue, so
no interaction is dropped for referring to an unknown item.

**The three all-missing presentations.** `week_from` and `week_to` are `?` for **100%** of items in
BBB_2013B, DDD_2013B and DDD_2013J — confirmed at 0.0% known, exactly the three presentations in
which the pilot's hybrid came out bit-for-bit equal to content-based filtering. DDD_2014B (0.2%)
and DDD_2014J (0.3%) are barely better and must be watched alongside them. Section 4 fixes the
fallback and section 13 fixes the assertion that makes a silent recurrence impossible.

**`date` is negative in real data.** 19,986 of EEE_2014J's 402,947 rows carry a negative `date`,
i.e. activity before the official presentation start. Negative days are kept, ordered normally, and
never clipped to zero; the course-week derivation of section 8 floors at week 0.

---

## 3. Variables

### 3.1 Mapping from the proposal's variables to columns

| Proposal variable | Table and column | Type | Used how | Justification |
| --- | --- | --- | --- | --- |
| User history logs | `studentVle.csv`.`sum_click`, summed per (`id_student`, `id_site`) | count | interaction weight in the learner–item matrix and in the CBF profile | the only interaction-strength signal the dataset carries |
| Time and context | `studentVle.csv`.`date`, days from presentation start, may be negative | integer | ordering key for every split; derivation of the learner's course week | makes a time-based split possible at all; the pilot ignored this column |
| Behavioural session signal | derived: click volume per (learner, item); distinct active days per learner; the day-ordered sequence of a learner's items | count, count, sequence | Module D features, cold-start prior, learned blend features | the recorded proxy for the hypothesis's session signal, see 3.2 |
| Item content | `vle.csv`.`activity_type` (20 values), `week_from`, `week_to` | categorical, numeric | CBF item feature vector; week window for the week-aware popularity baseline | the only item metadata OULAD carries |
| Course length | `courses.csv`.`module_presentation_length` | integer | upper bound on the derived course week | keeps a derived week inside the presentation |
| User information | `studentInfo.csv` | categorical | **population description only**, never a model feature | see 3.3 |

> **Clarifying note (2026-09-24, methodologist, cross-artifact fix I1; no design text above or below
> is changed).** In the row "Behavioural session signal", the entry "cold-start prior" in the
> "Used how" cell must not be read as a use that exists in this study. Module D (`plan.md`, code
> `behaviour.py`) is **descriptive only**: it describes the distributions of the behavioural features
> and clusters learners on them for description, and it feeds no model; no Module D feature, cluster
> or segment label enters any compared model, and no segmented model and no cold-start prior fitted
> from segments exists in the protocol's six models. What does enter a model is separate: the
> learner-activity inputs of the blend weight in section 8.1 step 3 (`n_visible`,
> `log1p_visible_clicks`, `n_active_days`), computed inside the blend from the visible history. `plan.md`
> words Module D as supplying Module B's cold-start prior and RQ2 as asking whether segmentation
> improves that prior; this protocol does not implement that, so **RQ2 as `plan.md` words it is not
> answerable from this design** and RQ1 is addressed descriptively. This is recorded as deviation D14
> and open question OQ8; the research question is not reworded here.

The 20 `activity_type` values, verified from `vle.csv`: `dataplus`, `dualpane`, `externalquiz`,
`folder`, `forumng`, `glossary`, `homepage`, `htmlactivity`, `oucollaborate`, `oucontent`,
`ouelluminate`, `ouwiki`, `page`, `questionnaire`, `quiz`, `repeatactivity`, `resource`,
`sharedsubpage`, `subpage`, `url`.

### 3.2 A signal the hypothesis names and the dataset does not record

| Promised signal | Recorded in OULAD? | Proxy used | Declared where |
| --- | --- | --- | --- |
| Browsing sequence | yes, indirectly | the learner's items ordered by first interaction `date`, ties by `id_site` | section 4 |
| Engagement pattern | yes, indirectly | click volume per (learner, item) and distinct active days per learner | section 4 |
| **Dwell time** | **no** — `studentVle.csv` holds `code_module`, `code_presentation`, `id_student`, `id_site`, `date`, `sum_click` and no duration field anywhere in the dataset | summed `sum_click` per (learner, item), plus distinct active days | chapter 1 and chapter 3 scope reduction; threats table T15; limitations |

This is the human's recorded decision Q2 (`decisions.log`, 2026-09-21): click volume, active days
and click sequence are the behavioural proxy, the substitution is recorded as a scope reduction in
chapters 1 and 3, and **the hypothesis stays frozen**. The word "dwell time" is never used in this
thesis to describe anything that was measured. The cost is stated plainly: a count cannot
distinguish a resource opened once by accident from one studied for an hour.

### 3.3 Demographic attributes: not used as features

No column of `studentInfo.csv` — `gender`, `region`, `highest_education`, `imd_band`, `age_band`,
`num_of_prev_attempts`, `studied_credits`, `disability`, `final_result` — enters any model in this
protocol, as a feature, a filter or a stratifier. Reasons: (i) `plan.md`'s Module B and Module D
specify no demographic feature, so using one is scope drift under rule 8; (ii) whether these
attributes may be used at all is an ethics decision reserved for the human (open question OQ3), and
rule 6 forbids treating an unanswered question as permission; (iii) `final_result` is an outcome
variable whose use as an input would leak the very thing an e-learning recommender is judged on.
`studentInfo.csv` is read only to report how many learners exist. If the human later authorises
demographic features, the fairness check of `methodology/data_statement.md` becomes mandatory and
this protocol is revised, not extended informally.

---

## 4. Preprocessing

The modelling record is the **(learner, item) pair**, not the raw row. For each pair in a
presentation:

- `clicks(u, i | t)` = sum of `sum_click` over the rows of that pair that lie **inside the bound
  `t`**, where "inside" is stated once, per bound, below (defect 2 of section 2.2 makes this an
  explicit sum, not a lookup). **The bound is
  part of the definition** — a click weight with no date bound is never used anywhere in this
  protocol. Two bounds exist, one per information state:
  - **Training bound** `t = the learner's first validation day`; a row is inside it when
    `date < t`, strictly before, so a row dated on the first validation day is excluded. Used for every training-side use of
    a weight: the learner–item engagement matrix and so the item–item similarity, the CBF profile
    weights, and any weight read while scoring at the validation or the warm test boundary.
  - **Cold bound** `t = the first_date of the k-th visible pair`; a row is inside it when
    `date <= t`, inclusive, so the whole day of the k-th interaction counts. Used for the visible
    history in every cold-start condition.

  **Why the bound is part of the definition (G3 cycle 2 blocker B2).** Revisions 0 to 2 summed
  `sum_click` over all rows of a pair while `first_date` alone decided which slice the pair belonged
  to. A pair therefore entered training by its first day but carried the weight of every later
  revisit, including revisits after the test boundary. Measured on EEE_2014J under the section 5.1
  split (2026-09-21): **17.8%** of the clicks on warm training pairs are dated on or after the
  learner's test boundary, affecting 1,014 of 1,018 learners, and **29.8%** are dated on or after
  the first validation day, affecting 1,016; at `k = 2`, **96.9%** of the clicks carried by the two
  visible pairs are dated after the second interaction, affecting 1,015 of 1,018. A "new learner
  with two prior interactions" was thus weighted by that learner's later engagement. Assertion L1
  could not see it, because L1 tests `first_date` and not the rows behind it. The leak was also
  **asymmetric across the compared models**: `MostPop` counts distinct learners and reads no click,
  so the click-weighted models — CBF, CF and therefore the hybrid — were the only ones carrying it,
  which bears directly on C3(b) and on C2.
- `first_date(u, i)` = minimum `date` over all rows for that pair — the ordering key for every
  split in this protocol;
- `active_days(u | t)` = number of **distinct** `date` values for learner `u` among the rows inside
  the same bound `t` as above (a row count would overcount by the duplication of defect 2). The
  blend feature `n_active_days` of section 8.1 step 3 uses this bounded count.

| # | Step | Rule | Reason | Effect, counted | Sensitivity check |
| --- | --- | --- | --- | --- | --- |
| P1 | Presentation selection for the single-presentation reproduction | deterministic: the presentation whose interaction count is closest to 400,000, ties by name | pre-registered before any result; removes selection-on-outcome | picks **EEE_2014J** (402,947; next nearest BBB_2013B at 403,266, |diff| 3,266 vs 2,947) | the main run covers all 22, so the choice affects only the C6 reproduction |
| P2 | Catalogue restriction | keep interactions whose `id_site` is in that presentation's `vle.csv` rows | an item outside the catalogue cannot be ranked | removes 0 rows in all 22 presentations (verified) | none needed |
| P3 | Interaction aggregation | collapse rows to (learner, item) pairs with `clicks` and `first_date` as above | the task ranks items, not days; and the file has duplicate triples | EEE_2014J: 402,947 rows to 47,136 pairs over 1,097 learners | none needed |
| P4a | Learner filter, items | keep learners with >= 5 distinct items (`MIN_ITEMS_FOR_EVAL_USER = 5` in the pilot) | a learner with fewer items cannot fill a 70/10/20 split | EEE_2014J: 1,097 to 1,049, i.e. 48 removed; all 22: 1,019 of 29,228 removed | repeat the whole run at 3 and at 10, reported as a sensitivity table |
| P4b | Learner filter, days | keep learners with >= **3 distinct first-interaction days** | the day-boundary split of section 5.1 assigns whole days and needs three of them to produce a non-empty train, validation and test set. With the `j* >= 3` bound of 5.1 step 2, three distinct days is **sufficient** as well as necessary, so this filter and the split now describe exactly the same learners and the split's own exclusion count is 0 | EEE_2014J: 1,049 to **1,018**, i.e. 31 removed; all 22: **997 of 28,209 removed (3.53%), leaving 27,212 evaluated** | the excluded learners are profiled below, and P4b gets its own sensitivity run (section 12.1) |
| P5 | Missing week values | `?` in `week_from`/`week_to` becomes `NaN`, then: per-column median of the **known** values in that presentation; if the column has **no** known value, fall back to `0.0`; a binary `week_missing` indicator is always a feature | the pilot's `median()` of an all-`NaN` column returned `NaN`, propagated through the L2 norm, evaded the `norm == 0` guard and made the hybrid identical to CBF in three presentations | affects BBB_2013B, DDD_2013B, DDD_2013J (0.0% known) and materially DDD_2014B (0.2%), DDD_2014J (0.3%) | the three all-missing presentations are reported separately in every table |
| P6 | Item filter | none; every catalogue item is a candidate even with zero training interactions | removing cold items would hide exactly the case CBF exists to solve | 0 items removed | new-item coverage reported in section 9 |

### 4.1 Evaluated population, realised split fractions and cold-start cohort, per presentation

Recomputed 2026-09-21 under P4a and P4b and the section 5.1 split. `In log` counts learners with
any interaction with the presentation's own catalogue; `−<5 items` and `−<3 days` are the two
filter drops; `Evaluated` is what remains; `Cohort` is the 20% cold-start cohort of section 6.1;
`test frac` and `val frac` are the **realised** fractions of that presentation's pairs.

| Presentation | In log | −<5 items | −<3 days | Evaluated | Cohort | test frac | val frac |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AAA_2013J | 378 | 1 | 2 | 375 | 75 | 0.199 | 0.102 |
| AAA_2014J | 357 | 7 | 3 | 347 | 69 | 0.199 | 0.105 |
| BBB_2013B | 1,537 | 58 | 75 | 1,404 | 281 | 0.203 | 0.115 |
| BBB_2013J | 1,870 | 82 | 88 | 1,700 | 340 | 0.205 | 0.115 |
| BBB_2014B | 1,294 | 72 | 59 | 1,163 | 233 | 0.205 | 0.118 |
| BBB_2014J | 1,921 | 63 | 85 | 1,773 | 355 | 0.200 | 0.113 |
| CCC_2014B | 1,681 | 71 | 53 | 1,557 | 311 | 0.201 | 0.114 |
| CCC_2014J | 2,302 | 106 | 65 | 2,131 | 426 | 0.202 | 0.116 |
| DDD_2013B | 1,214 | 25 | 39 | 1,150 | 230 | 0.201 | 0.107 |
| DDD_2013J | 1,768 | 44 | 68 | 1,656 | 331 | 0.199 | 0.110 |
| DDD_2014B | 1,116 | 35 | 41 | 1,040 | 208 | 0.202 | 0.112 |
| DDD_2014J | 1,647 | 76 | 48 | 1,523 | 305 | 0.202 | 0.110 |
| EEE_2013J | 964 | 41 | 25 | 898 | 180 | 0.199 | 0.107 |
| EEE_2014B | 624 | 18 | 22 | 584 | 117 | 0.199 | 0.109 |
| **EEE_2014J** | **1,097** | **48** | **31** | **1,018** | **204** | **0.202** | **0.108** |
| FFF_2013B | 1,510 | 24 | 26 | 1,460 | 292 | 0.200 | 0.105 |
| FFF_2013J | 2,098 | 46 | 63 | 1,989 | 398 | 0.201 | 0.106 |
| FFF_2014B | 1,363 | 30 | 52 | 1,281 | 256 | 0.200 | 0.107 |
| FFF_2014J | 2,121 | 78 | 55 | 1,988 | 398 | 0.200 | 0.107 |
| GGG_2013J | 895 | 30 | 30 | 835 | 167 | 0.200 | 0.117 |
| GGG_2014B | 773 | 33 | 35 | 705 | 141 | 0.199 | 0.120 |
| GGG_2014J | 698 | 31 | 32 | 635 | 127 | 0.201 | 0.117 |
| **Total** | **29,228** | **1,019** | **997** | **27,212** | — | 0.199–0.205 | 0.102–0.120 |

**The P4b exclusion is not random, and is described rather than only counted.** Recounted
2026-09-21 after the B1 repair, over the **997** learners P4b now drops: they hold a mean of 10.0
and a median of **8** distinct resources across a mean of 2.66 and a median of **2** distinct
active days, and none has more than 14 active days; the 27,212 retained learners hold a mean of
71.6 and a median of 55 distinct resources across a mean of 66.3 and a median of **52** active
days. The excluded learners are therefore those whose entire recorded activity falls on one or two
days — people who opened a handful of resources in one or two sittings and did not return. They are
a real and interesting population, close to the "actual new users" of `idea.md` criterion 2, and no
result in this thesis speaks for them. This is recorded as threat T22, given its own sensitivity
run in section 12.1, and stated in chapter 3, because an exclusion correlated with the very
behaviour a recommender is meant to change is a limitation, not housekeeping.

*(Revision 1 described this group as holding a median of 9 resources over 2 active days, counted
over 1,103 learners. That count mixed in the 106 learners the split could not serve, whose median
was 5 active days, so the description was wrong for them; the 106 are now kept and the figures
above cover only the learners the filter genuinely removes.)*

**Who is left, and why that matters.** The evaluated population is the *active* one. In EEE_2014J
the 1,018 evaluated learners are drawn from 1,097 who appear in the log at all, and the learners
who do appear hold a median of 49 distinct resources out of a 115-item catalogue — so the skew is
produced by the course and the platform, not by the filters, which together remove 79 of 1,097. Of
1,188 registered learners, 91 never touch the VLE and are invisible to this design from the start.
A mean Precision@10 of 0.5352 is reachable in this setting precisely because a typical learner has
roughly ten held-out items to hit. **Required statement in chapter 3 and chapter 5:** these results
speak about engaged learners and cannot speak about the disengaged learners a recommender is meant
to reach, because those learners are filtered out before measurement begins.

---

## 5. Split rule

### 5.1 Primary split — per-learner day-boundary split, closest achievable to 70 / 10 / 20

**Revision 1 note (G3 blocker B1).** Revision 0 specified a pair-level leave-last-20% split that
then extended the whole tied `first_date` group into test, and again into validation. On OULAD,
where a learner opens several resources on the same day, that rule is destructive: recomputed on
2026-09-21 it empties the training or validation set for **36 of EEE_2014J's 1,049** learners and
for **1,345 of 28,209 (4.8%)** across the 22 presentations, and inflates the realised test set to
between 1.08 and 1.26 times its nominal size. Revision 0's claims that "no learner is expected to
be excluded" and that "the minimum layout is 3 train / 1 validation / 1 test" were therefore
false, and its ceiling table was computed on a *no-tie* construction that the protocol did not
specify. **The rule below replaces it**, and every number this protocol derives from a split has
been recomputed under the new rule. The reason for replacing rather than re-reporting is that the
new rule loses fewer learners (997 rather than 1,345, after the revision 2 repair below), holds
the realised test fraction to
0.199–0.205 instead of inflating it, and still yields a strict day boundary.

Applied independently within each module presentation, to the (learner, item) pairs of section 4.
**Whole days are assigned, never split.** For a learner with `n` pairs and distinct first-interaction
days `d_1 < d_2 < ... < d_m`:

1. Let `suffix(j)` be the number of pairs whose `first_date` is at or after `d_j`.
2. **Test cut.** Choose `j*` in **`3..m`** minimising `|suffix(j) - 0.20n|`; ties are broken toward
   the **larger** `j`, i.e. the smaller test set. The **test** set is every pair on days `d_j*`
   onward. The lower bound is `3`, not `2`: a test cut on the second day leaves no day for
   validation, and the bound is what makes step 3's range non-empty for **every** learner with
   `m >= 3`.
3. **Validation cut.** Among the days strictly before `d_j*`, choose `i*` in `2..j*-1` minimising
   `|(suffix(i) - suffix(j*)) - 0.10n|`, ties again toward the larger `i`. Because `j* >= 3`, this
   range always contains at least `i* = 2`. The **validation** set is every pair on days `d_i*`
   through `d_{j*-1}`; the **training** set is every pair on days before `d_i*`.
4. The construction requires `m >= 3` distinct days **and nothing else**: with the bound of step 2,
   training, validation and test are each non-empty for every such learner, since `i* >= 2` gives a
   non-empty training set, `i* <= j*-1` a non-empty validation set, and `j* <= m` a non-empty test
   set. The `m >= 3` requirement is filter P4b of section 4 and is applied **before** the split, so
   it is a pre-registered population rule and not a silent loss at split time: **no learner is
   excluded at the split itself, and the code asserts that the exclusion count at this step is 0.**
5. Because whole days are assigned, every learner's training and validation days are strictly
   earlier than every test day, which is what makes L1's strict inequality provable without any tie
   extension.

**Revision 2 note (G3 cycle 1 blocker B1).** Revision 1 allowed `j*` to start at `2`. For a learner
whose first day holds roughly four fifths or more of their pairs, the test cut landed on the second
day and step 3's range was empty, so the learner had no validation set although they passed the
`m >= 3` filter. Recomputed 2026-09-21, this affected **106 of 27,212** learners (0.39%, up to 16
in BBB_2013B, 1 in EEE_2014J) — learners the published tables silently dropped while step 4 claimed
an exclusion count of zero, which measured would have been 106 and would have aborted the run. The
bound `j* >= 3` above repairs it **in the split rather than in the filter**, so those 106 learners
are now *kept*: the evaluated population rises from 27,106 to **27,212**, the day-filter drop falls
from 1,103 to **997**, and every table below is regenerated. Verified after the change: **0**
learners with an empty training, validation or test set, and **0** violations of L1, across all
27,212.

Ordering key: `first_date`; `id_site` ascending is the tie-break used only to make the serialised
pair order deterministic, never to place a pair on a different side of a cut. **The split needs no
random seed**, which removes a whole class of "which seed" questions; the only seeded objects in
this protocol are the Random baseline, the bootstrap and the cold-start cohort assignment
(section 6).

**Realised fractions and exclusions, recomputed 2026-09-21.** Because day granularity is coarse,
the realised fractions are close to but not exactly the targets, and they are reported rather than
assumed. Across the 22 presentations the realised **test** fraction runs from **0.199** to
**0.205** and the realised **validation** fraction from **0.102** to **0.120**; the validation
fraction runs highest in the BBB and GGG presentations, whose learners spread their activity over
fewer days. Per-presentation values are in the table of section 4.

The split is built **once per presentation** and handed unchanged to every model. The frozen idea's
hard constraint is honoured in the strongest available form: **every compared model — Random,
MostPop, week-aware popularity, CBF, item-kNN CF and the hybrid — is trained and evaluated on
byte-identical training, validation and test sets**, asserted by comparing the SHA256 of each
serialised pair-set per model before scoring (section 13).

### 5.2 Secondary split — global temporal cut-off, reported as a robustness check

Everything at or before day `D` is training, everything after is test. **`D` is the 80th percentile
of the presentation's `date` values taken over interaction ROWS** — the day at or below which 80%
of that presentation's rows in `studentVle.csv` fall — computed as
`numpy.percentile(rows.date, 80)` and truncated to an integer. This is stated exactly because a
second, different quantity exists and is **not** used: the 80th percentile over the presentation's
**distinct active days** is much later, because early and late days carry few rows each. For
EEE_2014J the row-based `D` is **164** while the distinct-day percentile is **211**; across the 22
presentations the distinct-day percentile runs from 183 to 212 (recomputed 2026-09-21). Every `D`
below is the **row-based** value. The values of `D` are fixed here, before the
run, so they cannot be chosen on results: AAA_2013J 192, AAA_2014J 188, BBB_2013B 159, BBB_2013J
181, BBB_2014B 163, BBB_2014J 179, CCC_2014B 180, CCC_2014J 198, DDD_2013B 148, DDD_2013J 175,
DDD_2014B 156, DDD_2014J 192, EEE_2013J 156, EEE_2014B 150, **EEE_2014J 164**, FFF_2013B 164,
FFF_2013J 170, FFF_2014B 165, FFF_2014J 184, GGG_2013J 201, GGG_2014B 191, GGG_2014J 194. This is
the closest analogue of deployment: at day `D` no model knows anything after `D` for **any**
learner. Its cost is that learners who join late lose their training history; the number of
learners who drop out under this rule is reported per presentation.

**Its validation slice** (G3 cycle 1 warning W2). The secondary split must also carry a validation
set, because `N`, `C` and the `α` model are fitted on validation data in every split and C4 audits
"all splits". Define `D_val` as the largest day such that the pairs whose `first_date` lies in
`(D_val, D]` number no more than 10% of the presentation's pairs; **training** is
`first_date <= D_val`, **validation** is `D_val < first_date <= D`, **test** is `first_date > D`.
This is the same closest-to-target-without-exceeding rule as the primary split, applied at
presentation level rather than per learner. A learner with no training pair under this split is
dropped from the secondary split only, and the count is reported per presentation; the primary
split's population is unaffected.

### 5.3 Tertiary split — the pilot's random 20% holdout, reported for continuity

Each learner's pairs are permuted with `numpy.random.default_rng(42)` and 20% held out, exactly as
the pilot did. **Its validation slice** (G3 cycle 1 warning W2): from the same permutation, the
next 10% of the learner's pairs after the test block form the validation set and the remaining 70%
the training set, so the three slices are disjoint and the hybrid is runnable here on the same
terms as everywhere else. It is
kept **only** so the phase 2 numbers can be read against the phase 1 record and so the cost of the
pilot's temporal leakage can be quantified. **No criterion is judged on it**, and every table that
shows it labels it "random split, temporally leaky". Time-based splits are the standard the
evaluation literature asks for: leakage changes not only the absolute numbers but the relative
order of models <!-- ledger: ji2023leakage -->.

### 5.3a Which split governs, declared in advance

The conclusion of this thesis rests on the **primary** split, and this is pre-declared rather than
settled after the results are seen. **C1, C2 and C3 are judged on the primary split alone**, which
is what `plan.md` C1's `on_dataset` field ("time-based split") and C2's ("cold-start-refit
condition") name. If the secondary global cut-off split **reverses the sign** of a comparison that
decides a criterion, three things happen and none of them is a change of verdict: both results are
reported side by side in chapter 5; the criterion verdict still stands on the primary split; and
the reversal is reported as a **limitation on the robustness of the finding**, in the sentence
chapter 5 uses to state that finding. The tertiary random split decides nothing in any
circumstance. Fixing this rule now is what stops a later reader — or a later author — from
choosing the split that gives the preferred answer.

**A residual the primary split does not remove, and which chapter 3 must carry (threat T1).** The
primary split is leakage-free **within** a learner, not across learners. Every learner shares the
presentation's calendar, so the item–item similarity matrix, the popularity counts and the blend
model are fitted on *other* learners' training and validation pairs, some of which postdate a given
learner's test items. The secondary global cut-off split is the one that removes this, which is
exactly why it is run. Since the evaluation literature's point is that leakage can reorder models
<!-- ledger: ji2023leakage -->, the honest statement — made here, in threat T1 and in chapter 3 —
is that "strictly time-ordered" is true **per learner** and not across the cohort.

### 5.4 Leakage assertions the code must make and the run log must show

| # | Assertion | What it rules out |
| --- | --- | --- |
**The provenance counter that makes L2 and L3 executable.** Revision 0 wrote L2 and L3 as
invariants ("computed from training pairs only") with nothing a run could measure, which rule 6
makes `unchecked`, not `passed` (G3 blocker B3). They are therefore reimplemented as *counted*
tests. Every function that fits a model, selects a hyperparameter or computes a preprocessing
constant takes an explicit `allowed` set as an argument and returns, beside its result, a
provenance record `(object_name, n_source_rows, n_rows_outside_allowed, n_learners_used,
n_cold_learners_used)`. The counts are produced by set difference against the rows the function
actually read, not by inspection of the code. Every record is written to the run log, **including
when every count is zero**, and a non-zero violation count aborts the run.

| # | Assertion | Operational test, emitting a measured count | What it rules out |
| --- | --- | --- | --- |
| L1 | For every learner, `max(first_date over train ∪ validation) < min(first_date over test)` — strict, provable because 5.1 assigns whole days | count of learners violating the strict inequality; must be 0 | temporal leakage inside a learner |
| L2 | Every **fitted** object — the item–item similarity matrix, the `MostPop` counts, the `PopWeek` counts, `N`, `C`, the blend model and its feature standardiser — reads only its declared `allowed` pair set | one provenance record per fitted object, with `n_source_rows` and `n_rows_outside_allowed`; every `n_rows_outside_allowed` must be 0, and the records must cover all **seven** learner-derived objects (section 6.1a) | model-level leakage: a fit that touched validation or test pairs |
| L3 | Every **preprocessing constant** reads only its declared `allowed` source | one provenance record per constant. Learner-derived constants (popularity denominators, the blend model's feature means and standard deviations) record `n_rows_outside_allowed = 0`. Catalogue-derived constants (the P5 week medians, the `week_from`/`week_to` min–max bounds) record `n_learner_rows_used = 0`, which is the positive evidence that they cannot depend on any learner | preprocessing leakage, and the false belief that a catalogue constant is learner-dependent |
| L4 | `train ∩ validation == ∅`, `validation ∩ test == ∅`, `train ∩ test == ∅`, as pair sets | the three intersection sizes; all must be 0. C4 checks the middle one explicitly | split overlap |
| L5 | The SHA256 of the serialised train, validation and test pair sets is identical across all six models within a presentation | count of models whose triple of hashes differs from the reference; must be 0 | a model quietly receiving a different split |
| L6 | Each model scores the test split **exactly once** per presentation | the per-model scoring counter; `max` must be 1 | repeated test scoring |
| L7 | In Condition A, no fitted object read a row belonging to a cold-start learner | for each of the **seven** learner-derived objects, `n_cold_learners_used`; every one must be 0, **and** the independent rebuild-and-hash test of section 6.1a must return seven equal hash pairs. This is the counted form of section 6.1a | a cold-start condition contaminated by the learners it calls new |
| L8 | The candidate exclusion set equals the information set of the **prediction moment**, checked at **both** moments | per learner and per moment: at M1 (warm, validation ground truth) `exclusion == training`; at M2 (warm, test ground truth) `exclusion == training ∪ validation`; at M3 (any cold-start condition, either boundary) `exclusion == visible history`. Emit the count of learners failing each of the three equalities, all required 0 (section 7.1) | a cold-start slice scored after an oracle had removed the learner's future, **and** a validation-time score whose ground truth sits inside its own exclusion set |
| L9 | No click weight or active-day count reads a row dated after its bound | per learner and per fitted or scored object: the number of rows dated at or after the training bound (the learner's first validation day), and after the cold bound (the `k`-th visible pair's `first_date`), that were read while forming a weight. Both required 0, emitted even when zero (section 4) | a pair placed in training or in the visible set by its first day but weighted by the learner's later revisits — the leak L1 cannot see, because L1 tests `first_date` only |

An assertion that is not executed is `unchecked`, never `passed` (rule 6). Each of L1 to L9 emits a
line in the run log with its measured count, including when the count is zero.

### 5.5 Training bound and exclusion moment for the four runs that have no per-learner validation day (G3 cycle 3 warning W4)

Section 4 defines the training bound as "the learner's first validation day". Four runs have no
such day for every learner they score, and the protocol was silent on which bound applies. This
section states it. **It changes no design decision, threshold, criterion, split rule, filter or
number**: it applies the rule of section 4 (a click or day dated at or after a run's own
prediction boundary never reaches a weight or a fitted quantity) and the moments of section 7.1
to runs section 4 did not name. Where a choice existed, the earlier bound was taken, because an
earlier bound can only remove information, never add a leak. The cold bound of section 4 (the
`first_date` of the `k`-th visible pair, inclusive) and moment M3 of section 7.1 are defined from
the learner's own visible pairs, need no day of any split, and apply **unchanged** in every
cold-start condition of the secondary and tertiary splits and of P4b.

| Run | Training bound (a row is inside when) | Exclusion moment | Reason |
| --- | --- | --- | --- |
| Secondary global-cutoff split (5.2), every learner, including learners with no validation pair | the **global day `D_val`** of 5.2: `date <= D_val`, i.e. strictly before `D_val + 1`; used for click weights and for `active_days`, for fitted objects and for scoring alike | M1 at the validation boundary (training only); M2 at the test boundary (training ∪ validation). A learner with no validation pair contributes no validation ground truth, so no row to any selection of `N`, `C` or the blend model, and at M2 their exclusion set is their training pairs | The split's own boundaries are global. `D_val` is earlier than `D`, so it also excludes rows dated in `(D_val, D]`, which postdate the validation boundary and are where validation ground truth lives. A per-learner bound cannot be used because these learners have no first validation day. Using `D_val` for every learner keeps the weight definition identical for learners with and without a validation pair. The cost, disclosed: at the test boundary weights are up to `D - D_val` days stale, the same direction of cost the warm primary split already accepts |
| Tertiary random split (5.3) | **none can be defined, and none is applied.** The split permutes pairs, so a learner's training, validation and test pairs interleave in time and no date separates what the model may know from what it must predict. Clicks and active days are summed over all rows | M1 at the validation slice (training pairs only); M2 at the test slice (training ∪ validation). These are set memberships and need no date | This is the pilot's design, kept for continuity (5.3). It is **temporally leaky and labelled so in every table that shows it**, as section 5.3 already requires. It is **reporting only** and is never read to support a claim about leakage-free performance |
| P4b two-day sensitivity run (12.1) | the learner's **second day `d_2`**, which is that learner's test boundary: `date < d_2`, strictly before, so clicks and active days on `d_2` and later never reach a weight. No validation day exists for them, so the primary rule's first validation day is replaced by the first test day | M2 with an empty validation set, which is **training pairs only** (the pairs first opened on day 1). Excluding day-2 pairs would remove the ground truth | The learner's own test boundary is the earliest date that can be used without a leak, and is the direct analogue of the primary rule with validation absent. The learner's weights are read only to score that learner; their pairs enter **no** fitted object of the main run (similarity, `MostPop` and `PopWeek` counts, `N`, `C`, blend model), because their day-2 pairs are test ground truth in this run |
| C6 phase 1 reproduction (EEE_2014J, C6) | **none, by design.** Click weights are the plain sum of `sum_click` over all of a pair's rows, and any active-day count is over all rows, exactly as the pilot computed them | the pilot's own exclusion: `set(visible_items)`, i.e. the learner's training items in the warm scenario and the pilot's two cold items in the cold scenario, with no validation set (`pilot_recommender.py`, the `exclude = set(visible_items)` line) | C6's threshold is `<= 1e-6` absolute against the recorded pilot values. Reproducing them means reproducing the pilot's **unbounded** behaviour. Applying any bound would change the numbers and make C6 fail for the right reason |

**What C6 therefore does and does not test.** C6 tests the pilot's **arithmetic**: that the
phase 1 code path, run from scratch on EEE_2014J, regenerates the six recorded Precision@10 values.
It does **not** test phase 2's leakage rules. The section 4 bounds, assertions L1 to L9 and the
exclusion moments of 7.1 do not apply to it, and L9 is recorded for this run as "not applicable:
no bound", never as 0. A C6 pass is no evidence that phase 2 is leakage-free, and the C6 numbers
carry the same "temporally leaky" label as the tertiary split and are never compared with primary
split numbers as if they measured the same thing.

**What the tertiary split's L2 and L3 counts therefore mean (G4 cycle 2 blocker B3).** The tertiary
row above already establishes that this split defines no training bound and applies none: "Clicks
and active days are summed over all rows." That absence governs L2 and L3 exactly as it governs L9:
L9 is the per-row bound check on click weights and active-day counts, and L2 and L3 are the same
"reads only its declared `allowed` set" check applied to whole fitted objects and preprocessing
constants — the `allowed` set for both is built from the same, here nonexistent, training bound.
With no bound to build it from, `allowed` cannot be restricted to a training role without inventing
a boundary the split does not have, so every fitted object on this split legitimately reads
validation- and test-role rows by the split's own design, not by a code defect. Measured on
AAA_2013J's tertiary warm cell: `L2: measured 54193, required 0, object_name similarity_matrix,
n_source_rows 180925` — 30% of the rows, exactly the split's 20% test plus 10% validation.
**L2 and L3 are therefore recorded `not_applicable` on the tertiary split, for the same reason and
in the same way as L1 and L9 above: the measured count is written to the run log as evidence of the
leak's size, not compared against a required-zero, and a non-zero L2 or L3 count on this split alone
never aborts the run.** This changes no threshold, criterion or split rule: the tertiary split
decides no criterion (5.3a; C4's expression in section 1.2 tests L4, hyperparameter provenance and
scoring count, none of which is L2 or L3), the split's whole purpose is to reproduce the pilot's
unbounded reads as a quantified point of comparison (5.3), and restricting the fitted objects to
training-role pairs would remove exactly the leak the split exists to measure, contradicting 5.3's
"reported for continuity" design and turning it into a different split. L2 and L3 remain fully
`must be 0`, aborting the run on any violation, on the primary and secondary splits and in every
cold-start condition of section 6, where a bound is defined and a nonzero count is a real leak.

**Which criteria these runs decide.** None of the secondary split, the tertiary split or the P4b
run decides any criterion. **C1, C2 and C3 are judged on the primary split alone** (section 5.3a,
which also fixes that the tertiary split "decides nothing in any circumstance" and that a
secondary-split reversal is reported as a robustness limitation, not a change of verdict); P4b is
a sensitivity run (section 12.1). The C6 reproduction decides **C6 only** (section 1.2), which is a
statement about arithmetic reproduction. C4 still audits the secondary and tertiary splits
("all splits", section 1.2): a hyperparameter fitted outside its own validation slice fails C4 in
either.

---

## 6. Cold-start slices

The human's recorded decision Q1 (`decisions.log`, 2026-09-21): **both conditions are reported; the
refit condition is primary and decides C2; the pilot's thin-history condition stays and is labelled
optimistic; no threshold moves.** This section implements exactly that.

### 6.1 Condition A — held-out new learners, similarity model refitted (primary, decides C2 and C3)

- **Cohort.** Within each presentation, 20% of the evaluated learners are designated cold-start
  learners by a seeded draw (`numpy.random.default_rng(42)`) **stratified by quintile of the
  learner's training-pair count**, so the cold cohort matches the warm cohort's activity
  distribution instead of being accidentally thinner or heavier. The cohort is fixed once per
  presentation and reused for every k and every model. Cohort sizes therefore range from **69**
  (AAA_2014J, 347 evaluated) to **426** (CCC_2014J, 2,131 evaluated), recomputed 2026-09-21 under
  the section 4 filters; the per-presentation cohort size is the `Cohort` column of the section 4.1
  table. The draw itself is specified in 6.1b.
- **Refit.** The learner–item engagement matrix, and therefore the item–item cosine similarity
  matrix, is built from the **remaining 80% of learners' training pairs only**. The cold-start
  learners' rows are removed from the matrix itself, not hidden at scoring time. This is the
  mechanism `plan.md` Module A names, and it is what makes a new-learner claim defensible: a new
  learner did not exist when the model was fitted. **Every other fitted quantity is refitted on the
  same reduced learner set, and section 6.1a names each one and its assertion** — revision 0 stated
  this as a generality and asserted it only for the similarity matrix, which G3 blocker B3
  correctly refused.
- **Visible history.** Each cold-start learner is shown the **earliest `k` of their TRAINING pairs
  by `first_date`**, ties by `id_site` — never a random `k`, and never drawn from the whole pair
  list. The pool is stated because a learner with fewer than `k` training pairs would otherwise
  have a validation or test pair become "visible" and, under section 7.1, excluded from their own
  candidate set, removing a ground-truth item. The visible count is `min(k, |training pairs|)`, and
  the code asserts that the visible set is a subset of the training pairs. Measured 2026-09-21: 168
  of the 27,212 evaluated learners hold fewer than 2 training pairs and 761 fewer than 5, so the
  case is rare at the deciding `k = 2` and commoner at `k = 5`, which decides nothing. The pilot took `train_rows[:2]` from an array it had
  already permuted, so its "first 2 items" were 2 random items and the slice modelled forgetting
  rather than newness. The code must assert that the visible list is sorted ascending by
  `first_date` and emit that assertion's result.
- **k curve.** k ∈ {0, 1, 2, 5}, all four reported. k = 0 is the honest place to show what a
  personalised model can do with nothing, and therefore what popularity alone achieves.
- **Test set.** Each cold-start learner's own time-based test set from section 5.1, **held fixed
  across all k and all models**, so the curve is a paired comparison.
- **Which k decides a criterion.** C2 and C3 are judged at **k = 2**, matching `idea.md`'s
  "<= 2 prior interactions". The other k values are reported and decide nothing.
- **Robustness variant.** The same condition with the cohort chosen as the **latest-arriving 20% of
  learners by first interaction date** instead of a stratified draw, reported once per presentation
  at k = 2. A genuinely new learner arrives late, so this is the more literal construction; it is a
  robustness check and not the deciding one, because late arrivals may be systematically thinner
  and that confound would be baked into C2. The two cohorts' activity distributions are reported
  side by side.

### 6.1b The cohort draw, specified so it can be reproduced (G3 cycle 1 warning W4)

Revision 1 said "a seeded draw stratified by quintile of the training-pair count", which does not
determine a cohort: quintile boundaries over a tie-heavy integer count are ambiguous, per-stratum
rounding can move the total, and the generator's consumption order was unstated. The draw is:

1. **After** filters P4a and P4b and after the section 5.1 split, so the training-pair count is
   defined. Let the evaluated learners of the presentation be `n` and the target cohort size
   `T = round(0.20 n)`.
2. **Strata by rank, not by value**, which removes the tie problem entirely: sort the learners by
   `(training-pair count, id_student)` ascending — a total order, since `id_student` is unique —
   and cut the sorted list at positions `round(j·n/5)` for `j = 0..5`, giving five strata of
   near-equal size.
3. **Apportion `T` across the strata by largest remainder:** each stratum's quota is
   `floor(T · |stratum| / n)`, and the remaining `T − Σ floor(...)` places go to the strata with
   the largest fractional parts, ties by ascending stratum index. This makes the strata sum to `T`
   exactly, so the cohort size is `round(0.20 n)` and not merely near it.
4. **Draw** with a single `numpy.random.default_rng(42)` created **per presentation** and consumed
   by `rng.choice(stratum_ids, size=quota, replace=False)` for strata `0, 1, 2, 3, 4` **in that
   order**, where `stratum_ids` is the array of that stratum's learner ids **in step 2's rank order**
   (training-pair count ascending, then `id_student` ascending), **not** re-sorted by `id_student`.
   The two readings give different cohorts (EEE_2014J, k = 2 cold probe of section 7.1: `MostPop`
   0.0255 under the rank order, 0.0206 if each stratum is re-sorted by `id_student`); the rank
   order is the specified one and is the one the section 7.1 probe table reproduces. The generator is not reused across
   presentations, so adding or reordering presentations cannot change an existing cohort.
5. The cohort is then **fixed** for that presentation and reused for every `k`, every condition and
   every model, which is what makes the `k` curve and the Condition A/B comparison paired.

Verified on 2026-09-21: this procedure yields cohort sizes equal to `round(0.20 × evaluated)` in
all 22 presentations, 69 to 426, matching the `Cohort` column of section 4.1 (EEE_2014J: 204, with
per-stratum quotas 41, 41, 41, 40, 41).

The **A-robustness** cohort replaces steps 2 to 4 with a deterministic rule and no generator: sort
the learners by `(first interaction date, id_student)` ascending and take the **last** `T`.

### 6.1a Every fitted quantity in Condition A, with the learner set it is fitted on and its assertion

G3 blocker B3: a cold-start condition is defined by what the model was fitted on, so naming one
object is not enough. `W` denotes the 80% warm learners of that presentation, `C` the 20%
cold-start cohort. Each row's assertion is the counted form required by L2, L3 and L7, and each
emits its number to the run log even when that number is zero.

| # | Fitted quantity | Decides / feeds | Fitted on, in Condition A | Executable assertion, with its emitted count |
| --- | --- | --- | --- | --- |
| A1 | Learner–item engagement matrix and the item–item cosine similarity derived from it | CF, and the CF half of the hybrid | training pairs of `W` only | the matrix's row-learner set `R`: emit `|R ∩ C|`, must be 0, and emit `|R|` beside `|W|` |
| A2 | `MostPop` counts — distinct learners per item | **C3(b)**, the popularity floor | training pairs of `W` only | emit `|counted learners ∩ C|`, must be 0; emit the count's denominator so `MostPop` is reproducible |
| A3 | `PopWeek` counts | reporting only (D4) | training pairs of `W` only; the week window itself is catalogue-derived | as A2, plus `n_learner_rows_used = 0` for the window |
| A4 | P5 week medians and the `week_from`/`week_to` min–max bounds | CBF item vectors | **the presentation's `vle.csv` catalogue only.** These are item metadata and depend on **no** learner's pairs, so they are bit-identical between the warm condition and Condition A — revision 0's phrase "normalisation constants from training only" wrongly implied learner dependence | emit `n_learner_rows_used = 0`, and assert the item-feature matrix's SHA256 is **equal** to the warm run's; emit the count of differing cells, must be 0 |
| A5 | Per-learner min–max scaling of CF and CBF score vectors inside the blend | hybrid | computed at scoring time from that learner's own candidate-set scores; depends on no other learner | emit `n_other_learner_rows_used = 0` |
| A6 | Selection of the CF neighbourhood `N` and the blend model's `C` | CF and hybrid | validation pairs of `W` only | emit `|selection learner set ∩ C|`, must be 0 |
| A7 | The blend model (logistic regression) and its feature standardiser | hybrid, and therefore C1–C3 | validation pairs of `W` only, **refit for Condition A with visible history truncated to the same k** (section 8.1, step 7) | emit `|training learner set ∩ C|`, must be 0; emit `k` used for the refit |
| A8 | A cold-start learner's own feature vector at scoring time | hybrid | that learner's own earliest `k` visible items — **permitted**, because it is the learner's own visible history, which is what the condition grants them | emit `k` and the visible-item count per learner |

**How many objects, exactly** (G3 cycle 1 warning W3b). Rows A1, A2, A3, A6 and A7 are the five
learner-dependent **rows**, but A6 covers two fitted objects (`N` and `C`) and A7 two more (the
logistic regression and its standardiser), so the provenance counter emits **seven learner-derived
fitted objects** per (presentation, condition, `k`): similarity matrix, `MostPop` counts, `PopWeek`
counts, `N`, `C`, blend model, standardiser. L2 and L7 are stated over those seven; revision 1's
"six" was wrong and is withdrawn. A4 and A5 are stated as learner-independent **with the count that
proves it**, rather than left ambiguous.

**A5's counter, defined** (W3d). `n_other_learner_rows_used` counts rows belonging to a learner
other than the one being scored that were read while computing that learner's min–max score
bounds. It is non-zero if an implementer ever computes the scaling over a pooled score matrix
across learners instead of per learner, which is the realistic way to get this wrong; the assertion
exists to catch exactly that.

**The other cohorts** (W3c). The same eight rows, with the same assertions and counts, are emitted
for the **A-robustness cohort** (the earliest-arriving 80%), substituting that cohort for `W`. Under
the warm condition the eight rows are fitted on all evaluated learners, and under Condition B on
all evaluated learners including `C` — which is exactly what makes Condition B optimistic, and the
Condition B run therefore emits `|R ∩ C| = |C|` rather than 0, recorded as the expected value for
that condition rather than as a violation.

**An independent check, because the counter is self-reported** (W3a). The provenance record is
produced by the very function that does the fitting, so a function that read a module-level frame
instead of its `allowed` argument would report zero while leaking. One check that does not depend
on the function's own bookkeeping is therefore required for every Condition A run: **rebuild all
seven learner-derived objects from a dataframe with the cold cohort's rows physically deleted, and
require the SHA256 of each rebuilt object to equal the SHA256 of the object the run produced.**
The rebuild **runs in a fresh process, reading a data file from which the cold rows were physically
removed, and hashes inside that process**; without that, a function reading a module-level frame
rather than its `allowed` argument would read the same global in both builds and return equal
hashes, so the check would pass while leaking (G3 cycle 2 warning W2). Each hash is taken over a
canonical serialisation — rows sorted by `(id_student, id_site)`, fixed dtypes — so equality does
not depend on row order. The seven hash pairs and their equality verdict go in the run log; any
inequality aborts the run.

### 6.2 Condition B — simulated thin history on the shared matrix (secondary, labelled optimistic)

The pilot's construction, kept for continuity: the **same** learners as the warm slice, the **same**
test sets, one item–item similarity matrix fitted on **every** evaluated learner's full training
history, and the visible history truncated at scoring time. The pilot's `main` builds
`engagement = build_engagement_matrix(splits, item_ids)` over all evaluated learners, derives one
`item_sim = cosine_sim_matrix(engagement)` and passes that same matrix to both the warm and the
cold-start evaluation.

No test interaction enters that matrix, so this construction **passes every leakage check in
section 5.4** — and it still cannot support a new-learner claim, because the learners it calls new
shaped the model that ranks for them. It is a thin-history simulation. Every table, figure and
sentence that reports a Condition B number labels it **"simulated thin history (optimistic)"**, and
no Condition B number is ever used to judge C2 or C3.

### 6.3 Measuring the optimism

Because both conditions run on identical splits with identical test sets and identical k, the
difference `Precision@10(Condition B) − Precision@10(Condition A)` at each k **is** the optimism of
the cheap construction, measured rather than asserted. It is reported per model, per presentation,
per k, with its median and range across the 22. This is a finding in its own right and answers the
committee question "how wrong was the pilot's cold-start number".

### 6.4 What was fitted on what — the table that makes the conditions unambiguous

| Condition | Learners in the similarity fit | Learner's visible history at scoring | Test set | Supports the claim |
| --- | --- | --- | --- | --- |
| Warm | all evaluated learners, training pairs | all training pairs | time-based test set | model quality for an established learner |
| A (primary) | the 80% warm learners only, training pairs | earliest k by `first_date` | same test set, fixed across k | a genuinely new learner |
| A robustness | the 80% earliest-arriving learners, training pairs | earliest k by `first_date` | same test set | a new learner who arrives late in the presentation |
| B (optimistic) | **all** evaluated learners, including the cold ones | earliest k by `first_date` | same test set | thin history, population held constant — **not** a new learner |

---

## 7. Candidate set and task

- **Candidates: the full catalogue of the presentation, 106 to 529 items. No sampled negatives.**
  Full ranking is computationally free at this catalogue size, and sampling negatives can reorder
  models, which would make every comparison in this thesis contingent on the sample. Any sampled
  metric would need a justification here; there is none, because none is used.
- **Already-seen items are excluded** from a learner's candidate list, as the pilot's
  `top_k_excluding` does. The task is therefore *recommend a resource this learner has not opened
  yet*, not *predict the learner's next click*. These are different tasks with different ceilings,
  and the thesis names the one it performs. Under the whole-day split of section 5.1, applied to
  (learner, item) pairs, an item can be in a learner's training, validation or test set but never
  in more than one, so exclusion never removes a ground-truth item — provided the exclusion set is
  the one belonging to that score's prediction moment, which section 7.1 fixes.
### 7.1 The exclusion set: one principle, two conditions (G3 cycle 1 blocker B2)

**The principle.** The exclusion set for a learner is **exactly the resources that learner has
already opened as of the prediction moment that defines the condition** — no more and no less. A
recommender at that moment knows what the learner has opened so far and nothing about what they
will open next. Everything excluded must therefore lie in the learner's *past*; nothing in their
*future* may be used, not to rank and not to filter.

**There are three prediction moments, not two** (G3 cycle 2 blocker B1). A score is computed
either against validation ground truth (when a label, `N` or `C` is being chosen) or against test
ground truth, and the learner's information state differs between the two. Naming all three is the
point:

| # | Prediction moment | Ground truth | Visible history | **Exclusion set** | Why it is not an oracle |
| --- | --- | --- | --- | --- | --- |
| M1 | the **validation** boundary, warm | validation items | training pairs | **training pairs only** | at that moment the learner has opened the training pairs and nothing else. Excluding the validation items here would exclude the ground truth itself |
| M2 | the **test** boundary, warm | test items | training pairs | **training ∪ validation** pairs | every excluded resource was opened *before* the test boundary, so a system deployed then already knows about it. Validation items are excluded but not fitted on, which is the conservative direction: the tuning slice never trains a model |
| M3 | immediately after the learner's `k`-th interaction (Condition A, its robustness variant, and Condition B), at **both** the validation and the test boundary | validation items when fitting, test items when scoring | the earliest `k` training pairs | **the `k` visible pairs only** | the learner has supplied exactly `k` interactions. Their remaining training pairs and their validation pairs lie in the learner's future at that moment and are invisible to a real new learner. The cold information state does not change between the two boundaries, so one rule serves both |

**Revision 3 note (blocker B1).** Revision 2 recognised only M2 and M3 and therefore applied the
test-boundary set at the validation boundary. The consequence was not a small bias but a silent
degeneracy: the ground truth of a validation-time score is a subset of `training ∪ validation`, so
no validation item could be recommended and validation Precision@10 was **0 by construction**.
Measured on EEE_2014J with `MostPop`, on the first 300 warm learners by `id_student` (the warm
learners being the 814 that remain after the Condition A cohort of section 6.1b is set aside, with
the `MostPop` counts fitted on those 814 learners' training pairs only): **0.0000** under
`training ∪ validation` against **0.1883** under training-only. Recomputed 2026-09-21 from the
tables; the neighbouring selections give 0.1887 (first 300 warm by `id_student`, counts fitted on
all 1,018 evaluated learners), 0.1907 (first 300 of all 1,018 evaluated) and 0.1962 (all 814 warm,
counts fitted on all 1,018); 0.0000 under `training ∪ validation` holds for every one of them. Every warm learner would then be all-zero at every `α`,
every one would be dropped by step 2's all-zero rule, step 10's degenerate branch would set `α` to
a constant 0.5 in every presentation, `N` would tie across the grid and resolve to 10, and `C`
would resolve to the smallest — so **C1 would have been judged on a fixed 50/50 blend that is not
the specified model, with no assertion failing.** M1 above repairs it.

**Revision 2 note: this replaces a defect that revision 1 introduced.** Answering cycle 0's warning
W3, revision 1 set the exclusion set to training ∪ validation *in every condition*, and argued it
could not bias a comparison because it applied to all six models. That argument fails for the
cold-start conditions. A learner who is "new" at `k = 2` had roughly 32 further training pairs and
their validation pairs struck from every model's candidate list — information a real new learner
has not supplied — so the condition scored ranking *after an oracle had removed most of the wrong
answers*. It is also not the slice `idea.md` criterion 2 names: a learner whose candidate set
encodes thirty later interactions is not a "new user with <= 2 prior interactions".

**The measured effect, reproduced independently on 2026-09-21** (EEE_2014J, the section 5.1 split,
the section 6.1b cohort draw, cohort n = 204, k = 2, models fitted on the warm 80%):

| Model | no exclusion | **exclusion = visible `k` (adopted)** | exclusion = training ∪ validation (revision 1) |
| --- | --- | --- | --- |
| `MostPop` | 0.0137 | **0.0255** | 0.2157 |
| `ItemKNN-CF` (click-weighted sum, bounded weights, **`N` = all neighbours**; a learner's own visible items **keep self-similarity 1** in the no-exclusion cell) | 0.0279 | **0.0333** | 0.1946 |

**The `ItemKNN-CF` line was re-run at revision 3 and its three values changed** (0.0142 / 0.0250 /
0.2108 → 0.0279 / 0.0333 / 0.1946), for two reasons, both recorded rather than quietly absorbed:
the revision 2 probe summed item–item similarities **unweighted**, where section 8 specifies a
**click-weighted** sum over the visible items; and it used the unbounded click weight that blocker
B2 has now removed. The `MostPop` line is unchanged and was re-verified to the digit, because
`MostPop` counts distinct learners and reads no click weight — which is exactly the asymmetry B2
describes.

The revision 1 exclusion rule inflated cold-start Precision@10 **8.5-fold** for `MostPop` and
**5.8-fold** for item-kNN CF. Two further consequences make it worse than a uniform inflation.
First, the inflation is not a property of non-personalised models: the strongest collaborative
model gains a comparable multiple, because the filter, not the model, is doing much of the ranking.
Second, under that rule the two models converge to within 10.8% of one another (0.2157 against
0.1946), where under the adopted rule CF stands 31% above `MostPop` (0.0333 against 0.0255) on its
own merits — so C3(b), whose whole job is to test the hybrid against `MostPop` on the cold-start
slice, would have been deprived of much of its discriminating power. C2 and C3 are the two criteria
that can refute the hypothesis, and both are judged on this slice.

**No number in sections 4.1, 5.1 or 9.1 changes under either blocker's repair**, and this was
re-verified on 2026-09-21 by regenerating all three from the data: those tables are functions of
`first_date` alone — the population, the split and the test-set sizes — and neither the click bound
nor the exclusion moment touches `first_date`.

**Consistency with the blend model.** Section 8.1 steps 2, 4 and 8 and section 8.0a compute scores
whose ground truth is the **validation** set, so they use moment **M1** in the warm condition
(training pairs only) and **M3** in every cold-start condition (the visible `k` pairs). Test-time
scoring uses **M2** when warm and **M3** when cold. In the cold conditions the exclusion set is
therefore identical at fitting and at scoring time; **in the warm condition it is not**, and that
is a correct consequence of "as of the moment" rather than a defect: the warm candidate set at test
time is smaller than at validation time by that learner's validation items, so the features
`cf_top1`, `cf_top10_mass`, `cbf_top1` and `cbf_top10_mass` shift slightly between fitting and
scoring. **This shift is disclosed, not eliminated** (G3 cycle 2 warning W6): eliminating it would
require applying one exclusion set at both moments, which is precisely the defect B1 removed. The
run log reports the mean absolute shift in each of the four features, per presentation, so its size
is a measured quantity in chapter 5 rather than an assumption, and threat T29 records it.

**What the run log must show.** Per learner, per condition: the visible-history size, the exclusion
set size, and the candidate set size. The assertion is that in every cold-start condition
`exclusion set == visible history` exactly (a set equality, emitting the count of learners for
which it fails, required 0), and that in the warm condition `exclusion set == training pairs` at M1 (validation
ground truth) and `exclusion set == training ∪ validation` at M2 (test ground truth), each on the same
terms. A cold-start candidate set that is smaller than
`catalogue − k` is the signature of this defect returning.
- **Ground truth** for learner `u`: the items in `u`'s test pair set, i.e. items whose first
  interaction with `u` falls after the split boundary.
- **Task, in one sentence:** for each evaluated learner in a module presentation, rank every
  catalogue item that the learner's visible history does not already contain, and measure how many
  of the learner's held-out later items appear in the top K.

---

## 8. Models compared

All six run on the byte-identical splits of section 5. `plan.md` Module B names four
(`ContentBased`, `CollaborativeFiltering`, `PopularityBaseline`, `Hybrid`); the Random floor and
the week-aware popularity variant are **additions recorded in section 16**, present for reporting
and for answering the examiner, and **neither decides any criterion**. C3's "global-popularity
baseline" is `MostPop` and only `MostPop`.

| Model | Specification | Hyperparameters and grid | Fitted on | Deterministic |
| --- | --- | --- | --- | --- |
| `Random` | uniform draw over the learner's candidate set | none; 5 seeds (42, 43, 44, 45, 46) | — | no; mean and SD over the 5 seeds reported |
| `MostPop` | rank by the number of **distinct training learners** who interacted with the item, not by total clicks, so one heavy user cannot manufacture popularity | none | training pairs | yes |
| `PopWeek` | `MostPop` restricted to items whose `[week_from, week_to]` window contains the learner's current course week `w = max(0, floor(d / 7))`, capped at `module_presentation_length / 7`, where `d` is the `first_date` of the learner's **last visible pair** — the last training pair when warm, the `k`-th visible pair when cold, so the week never comes from the learner's future; items with an unknown week are always eligible; **ineligible items are not dropped but appended after every eligible item, in `MostPop` order**, so the ranking is a total order over the whole candidate set and a top-10 is never short | week window rule as stated | training pairs | yes |
| `CBF` | cosine between the learner profile and each item vector; item vector = one-hot `activity_type` (20 dims) + `week_from` and `week_to` min–max normalised over the presentation's **catalogue** + the binary `week_missing` indicator; profile = click-weighted mean of the visible items' vectors, L2-normalised | none tunable in phase 2 | item metadata only; its constants are catalogue-derived and learner-independent (assertion A4) | yes |
| `ItemKNN-CF` | cosine similarity between item columns of the learner–item click matrix; score = click-weighted sum of similarities over visible items; neighbourhood truncated to the top `N` most similar items per item, ties inside the neighbourhood by `id_site` ascending | `N ∈ {10, 25, 50, 100, all}`, selected per section 8.0a | training pairs | yes |
| `Hybrid` | score-level blend `α(u) · minmax(CF) + (1 − α(u)) · minmax(CBF)`, fully specified in **section 8.1** | see section 8.1 | components on training pairs; `α` model on validation pairs | yes |

### 8.0 Ranking, ties and scaling — the rules that decide a Precision@10 (G3 cycle 1 blocker B3)

These four rules were unstated through revision 1. Each of them moves cold-start Precision@10, so
each is fixed here rather than left to whoever writes the code.

**(i) The top-K order, for every model without exception.** Candidates are sorted by **score
descending, then `id_site` ascending**, and the first K are taken. Because CF and CBF scores are
floating-point sums whose last bit depends on summation order, **scores are rounded to 12 decimal
places before ordering** and every score sum is accumulated over its terms in `id_site` ascending
order; without both, two mathematically equal scores could order differently in two
implementations and the order would not in fact be total (G3 cycle 2 warning W4). This is a *total* order on the
candidate set, so it does not depend on the input array's order or on a sort's stability, and two
implementers get the same list. It matters most exactly where the criteria are decided: at
`k ∈ {0, 1, 2}` the item–item CF score is non-zero for at most `k · N` items and CBF is a cosine
over 20 one-hot dimensions plus two week values, so ties spanning the tenth place are the normal
case, not the exception, and `MostPop` ties whenever two resources were opened by the same number
of learners. The tie-break by `id_site` is arbitrary but **pre-registered, identical across all six
models, and independent of any model's score**, so it cannot favour one of them; it is recorded as
a limitation in threat **T28** rather than presented as neutral.

**(ii) `Random` is scored, not shuffled.** For seed `s`, `Random` assigns each candidate a draw
from `numpy.random.default_rng([s, presentation_index, learner_index])` and then applies rule (i).
Ties therefore do not arise, the draw is reproducible from the seed alone, and the five seeds
(42–46) differ only in `s`.

**(iii) Min–max scaling of a constant vector.** `minmax(x)` returns `(x − min) / (max − min)` when
`max − min >= 1e-12`, and **the all-zero vector otherwise** — the pilot's own convention, restated
because it is now load-bearing. Two consequences are stated in advance rather than discovered in
the results. At `k = 0` every personalised model's score vector is constant (CF has no visible item
to sum over, CBF has no profile), so `minmax` returns zeros, the hybrid's blend of two zero vectors
is zero, and **rule (i) then ranks by `id_site` ascending alone**: at `k = 0`, CF, CBF and the
hybrid all emit the same fixed, non-personalised list. That is the correct behaviour — a
personalised model given no history has nothing to say — and it is precisely why `k = 0` is the
honest place to read what `MostPop` achieves. In the same situation the blend features `cf_top1`,
`cf_top10_mass`, `cbf_top1` and `cbf_top10_mass` of section 8.1 step 3 are all 0, which the feature
vector records rather than treats as missing.

**(iv) What `MostPop` counts, restated for ties.** The score is the number of **distinct** learners
in the fitting cohort's training pairs who opened the resource; resources with zero such learners
score 0 and are still candidates, ordered by rule (i).

### 8.0a Selecting the collaborative neighbourhood `N`

- **Criterion:** the macro mean of Precision@10 over the validation learners of the cohort the
  model is being fitted for, scored on those learners' validation items.
- **Tie rule:** the **smallest** `N` among the maximisers, so a tie resolves toward the simpler
  model.
- **The history the selection is scored on:** the same history the model will be applied with. In
  the warm condition that is the learner's full training pairs; **in each cold-start condition it
  is the visible history truncated to that condition's `k`**. Selecting `N` on full histories and
  applying it at `k = 2` would tune the model for a task it is not being judged on.
- **The exclusion set the selection uses:** the score's ground truth is the **validation** set, so
  the prediction moment is **M1** in the warm condition (exclusion = **training pairs only**) and
  **M3** in every cold-start condition (exclusion = the visible `k` pairs). Using M2's
  `training` plus `validation` here would place the ground truth inside the exclusion set and score
  every `N` at 0 (blocker B1).
- **The click weights the selection reads** are bounded by section 4's training bound, and the
  visible history by its cold bound (blocker B2).
- **Re-selected per `k`:** yes. There is **one `N` per (presentation, condition, `k`)**, exactly
  parallel to the one `α` model per (presentation, condition, `k`) of section 8.1 step 11. The
  hybrid inherits the `N` selected for `ItemKNN-CF` under the *same* (presentation, condition, `k`)
  and never selects its own.
- **Reported:** every selected `N` appears in the run log and in chapter 3's appendix table, keyed
  by presentation, condition and `k`, so the reader can see whether the neighbourhood size drifts
  with `k`.

### 8.1 The blend weight, specified so that two implementers build the same object

G3 blocker B2: revision 0 named a logistic regression without its target, level, output mapping,
scaling, solver or feature-construction rule, so the object that decides C1 to C3 could not be
rebuilt and C4's audit had nothing to audit. The full specification follows.

1. **Level.** One row per learner. `α` is a per-learner scalar, constant across that learner's
   candidate items. It is **not** fitted at learner–item pair level.
2. **Target construction (on validation data only).** For each validation learner `u`, sweep the
   fixed grid `A = {0.0, 0.1, 0.2, ..., 1.0}` (11 values), computing `u`'s Precision@10 **on their
   validation items** for each `α ∈ A`, using the exclusion set of the **validation** prediction
   moment from section 7.1 — **training pairs only** in the warm condition (M1), the visible `k`
   pairs in every cold-start condition (M3) — and the date-bounded click weights of section 4.
   Let `A*(u)` be the set of maximising values and `α*(u) = median(A*(u))` (the median of a tied
   set, which is deterministic). The regression target is the binary `y(u) = 1 if α*(u) >= 0.5 else
   0`, i.e. "this learner is better served by a collaborative-leaning blend".
   **All-zero learners are dropped from the fit, not labelled** (G3 cycle 1 warning W1a). If `u`'s
   validation Precision@10 is 0 at every `α ∈ A`, then `A*(u)` is the whole grid and `median = 0.5`
   would silently label the learner `y = 1`, i.e. "collaborative-leaning", purely because no blend
   could serve them. Validation sets hold roughly 4 to 5 items per learner, and the share of
   all-zero learners is large — larger still at `k <= 2`, where a personalised model has almost
   nothing to work with — so this artefact would dominate the label in exactly the condition that
   decides C2 and C3. Such learners are therefore **excluded from the `α` model's training rows**,
   and the **share excluded is reported per presentation, per condition and per `k`** in the run log
   and in chapter 5. They are *not* excluded from evaluation: they still receive an `α` from the
   fitted model at scoring time and still count in every reported metric. If fewer than 20 labelled
   learners remain in a presentation, the degenerate rule of step 10 applies.
3. **Features, eight per learner, in this fixed order.** `n_visible` (count of visible items);
   `log1p(total visible clicks)`; `n_active_days` (distinct `date` values in the visible history);
   `cf_top1` and `cf_top10_mass` (the largest, and the sum of the ten largest, of the min–max
   scaled CF scores over the learner's candidate set); `cbf_top1` and `cbf_top10_mass`, the same
   for CBF; and `week_missing_share` (the share of the presentation's catalogue whose week fields
   are unknown — constant within a presentation, and the feature that lets the model behave
   differently in the three all-missing presentations).
4. **Feature construction, validation time versus test time.** The visible history is whatever the
   condition grants (training pairs when warm, the earliest `k` training pairs when cold), the
   component scores come from models fitted on that condition's cohort with section 4's bounded
   click weights, and **the candidate set uses the exclusion set of the prediction moment**
   (section 7.1): M1 when the ground truth is the validation set and the condition is warm, M2 when
   the ground truth is the test set and the condition is warm, M3 in every cold-start condition at
   either boundary. No feature reads a test item.
   **In the cold conditions the feature definition is therefore identical at fitting and scoring
   time; in the warm condition it is not**, because M1 and M2 differ by the learner's validation
   items. That difference is a correct consequence of "as of the moment" and is disclosed rather
   than removed: `cf_top1`, `cf_top10_mass`, `cbf_top1` and `cbf_top10_mass` are computed over a
   candidate set that is larger at fitting time than at scoring time by those items, the run log
   reports the mean absolute shift in each of the four, and threat T29 carries it. Removing the
   shift would mean applying one exclusion set at both moments, which is the degeneracy blocker B1
   removed.
5. **Scaling.** Z-score standardisation. A feature with zero variance is passed through as a
   constant zero. The standardiser is fitted **twice, on different rows, and this is deliberate**
   (G3 cycle 1 warning W1b): *inside* the cross-validation of step 8 it is refitted on each
   training fold alone and applied to the held-out fold, so no held-out row contributes its own
   feature statistics to the model that scores it; for the final model it is fitted once on all
   labelled validation rows of that presentation, stored, and applied unchanged at test time.
   Neither fit sees a label from a held-out fold or any test data.
6. **Estimator and its settings.** `sklearn.linear_model.LogisticRegression` with `penalty="l2"`,
   `solver="lbfgs"`, `tol=1e-4`, `max_iter=1000`, `fit_intercept=True`, `class_weight=None`,
   `random_state=42`, and `C` selected from `{0.01, 0.1, 1, 10}`. The loss is the standard
   L2-penalised binary cross-entropy; no sample weighting is applied.
7. **From output to α.** `α(u) = P(y = 1 | x(u))`, the estimator's `predict_proba` value for class
   1. It lies in `[0, 1]` by construction, so **no clipping is applied** — revision 0's "clipped to
   [0,1]" is withdrawn as vacuous. `α` is used at full precision, never rounded to the grid `A`,
   which is used only to build the target in step 2.
8. **Selecting `C` without touching test.** `C` is chosen by 5-fold cross-validation over the
   labelled validation learners, using
   `sklearn.model_selection.StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
   stratified on `y`. For each held-out fold the standardiser and the model are fitted on the other
   four folds and the score is the **mean Precision@10 of the resulting hybrid on that fold's
   learners, evaluated against their validation items** under the **validation** moment's exclusion
   set (M1 when warm, M3 when cold). The
   `C` with the highest mean across folds wins, ties going to the **smaller** `C`; the model is
   then refitted on all labelled validation learners with that `C`. Test data enters nowhere in
   this loop.
9. **Which `N` the hybrid's CF component uses.** The hybrid **inherits the `N` selected for the
   standalone `ItemKNN-CF` baseline under the same (presentation, condition, `k`)**, per section
   8.0a, and runs no search of its own. This is stated because it decides the parity count in step
   11 and because the alternative — a separate `N` search inside the hybrid — would give the hybrid
   a larger budget than its own baseline.
10. **Degenerate cases, defined in advance.** Both checks in this step, and the median below, run
    over the **labelled** validation learners of that presentation only — the same population step 2
    builds the fit from, after step 2's all-zero learners are dropped. An all-zero learner's `α*(u)`
    is the tied-grid artefact `median(A) = 0.5`, not a measured preference (step 2), so it is excluded
    here for the identical reason it is excluded from the fit; including it would let learners for
    whom no blend works at all silently pull the constant toward 0.5 in the very presentations —
    small or thin, disproportionately at `k <= 2` — where this rule is reached. If every **labelled**
    validation learner in a presentation has the same `y`, the logistic regression cannot be fitted;
    `α` is then the constant `median{α*(u) : u a labelled validation learner in that presentation}`
    — **all-zero learners dropped by step 2 take no part in this median** — and the run log records
    `alpha_model = constant` with that value. If a presentation has fewer than 10 **labelled**
    validation learners with `y = 1` **or** with `y = 0`, 5-fold stratified cross-validation is not
    possible; `C = 1` is then used without selection and the run log records `C_selection = skipped`.
11. **Refit per condition, including Condition B.** There is exactly **one `α` model per
    (presentation, condition, `k`)**, and every one is built by re-running steps 2 to 8 with that
    condition's cohort, that condition's visible history and that condition's exclusion set:
    - **Warm:** all evaluated learners; visible history = training pairs; the exclusion set is the
      one of the prediction moment (section 7.1): at M1, when a score is computed against validation
      ground truth (steps 2, 4 and 8, and section 8.0a), **training pairs only**; at M2, when a score
      is computed against test ground truth, **training ∪ validation**. One model per presentation.
    - **Condition A** (and its robustness variant, on its own cohort): the **80% warm learners
      only** (assertion A7), visible history truncated to the same `k`, exclusion = the visible `k`
      pairs. One model per (presentation, `k`).
    - **Condition B** (G3 cycle 1 warning W1c): **all evaluated learners**, including the cold
      cohort — which is exactly what makes Condition B optimistic — with visible history truncated
      to the same `k` and exclusion = the visible `k` pairs. One model per (presentation, `k`). It
      is a refit, not a reuse of the warm model; reusing the warm model would confound the
      optimism being measured in 6.3 with a blend fitted for a different history length.

    The truncated refit keeps the model inside its training range: a blend fitted where visible
    history is tens of items and applied at `k = 2` would be extrapolating, and a hybrid losing at
    cold start would then be evidence about a mis-specified blend rather than about the
    architecture (threat T25).

**Tuning parity, counted explicitly.** A *configuration* is one distinct hyperparameter setting
evaluated on validation; a configuration evaluated over several cross-validation folds counts
**once**, not once per fold. On that definition, **per (presentation, condition, `k`)**:
`ItemKNN-CF` 5 (its grid of `N`), `Hybrid` 4 (its grid of `C`, inheriting `N` from `ItemKNN-CF` per
step 9 and section 8.0a), and `CBF`, `MostPop`, `PopWeek` and `Random` 0. The maximum is 5, so the
"at most 5 configurations per model" claim holds within every (presentation, condition, `k`) cell
and the hybrid is the *smaller* of the two tuned budgets. Because both `N` and `α` are re-selected
per `k`, the budget is per cell and not per presentation, and the run log carries the count for
every cell. Disclosed separately rather than
folded in: the 11-point grid `A` of step 2 is a **label-construction** sweep, not a hyperparameter
search — it selects no setting of any model, it is computed on validation items only, and its
result is a regression target. The run log records both numbers, `n_configurations` and
`n_label_grid_points`, per model per presentation, so the parity claim is auditable rather than
asserted <!-- ledger: ferrari2021troubling -->.

**Refit policy after selection, applied identically to every model:** the selected configuration is
**not** refitted on training plus validation. Each model is fitted on training pairs only and
scored on test. Stating this in advance keeps the blend weight — which is fitted on validation —
the only object in the design that has seen validation data, which is exactly what C4 audits.

**What replaces the pilot's hand-picked weight.** The pilot's iteration 2 used
`alpha = min(0.9, 0.2 + 0.05 * n_visible_items)`, written after iteration 1's **test** numbers were
known. Under rule 3 that value is exploratory and supports no criterion in this thesis. It is
reported in chapter 4 as the pilot's value, labelled exploratory, and the phase 2 hybrid uses the
validation-fitted `α` above.

**Deferred by decision, not omitted.** Implicit matrix factorisation and a GRU-based sequence model
are named in the playbook and in the proposal's RNN/CNN plans; the human's recorded decision Q5
defers the deep models (RNN, CNN, RBFNN) and the user interface as **scope-outs**, stated with
their reason in chapter 1 and listed as future work in chapter 6. Phase 2 compares the six models
above and no others.

---

## 9. Metrics

Let `T(u)` be learner `u`'s test item set and `R_K(u)` the top-K list.

| Metric | K | Definition | Why it fits | Known limit |
| --- | --- | --- | --- | --- |
| **Precision@10** | 10 | `|R_10(u) ∩ T(u)| / 10` | **primary; fixed by `plan.md` and decides C1, C2 and C3** | ceiling-bound when `|T(u)| < 10`; see 9.1 |
| Recall@K | 5, 10, 20 | `|R_K(u) ∩ T(u)| / |T(u)|` | normalises on what was actually available, which is what repairs Precision's ceiling | rewards learners with few test items |
| NDCG@K | 5, 10, 20 | `DCG@K / IDCG@K`, `DCG@K = Σ_i rel(i) / log2(i+1)`, **binary relevance** | rank-sensitive; the ideal DCG accounts for `|T(u)| < K` | graded relevance from `sum_click` is **not** used, because it would silently redefine relevance as popularity of effort |
| HitRate@K | 5, 10, 20 | `1[|R_K(u) ∩ T(u)| > 0]` | the "did we help at all" question; meaningful for learners with a single test item | insensitive to how many hits |
| MRR@K | 5, 10, 20 | `1 / rank of the first hit`, else 0 | sensitive to the very top of the list, which is what a learner actually sees | ignores everything after the first hit |
| Catalogue coverage@10 | 10 | distinct items appearing in any top-10 across the slice / catalogue size | **evidence for C3's non-degeneracy conjunct** | a model can be diverse and wrong |
| Intra-list diversity@10 | 10 | mean pairwise Hamming distance over `activity_type` within a list | catches ten near-identical resources, which Precision cannot | needs the `activity_type` vocabulary, which is complete |
| Empty-list count | 10 | learners whose top-10 has fewer than 10 items | **the other C3 non-degeneracy conjunct** | — |
| Popularity agreement | 10 | Kendall τ between the model's full ranking and `MostPop`'s, and `|R_10 ∩ MostPop_10| / 10` | measures `idea.md`'s literal clause "must not simply fall back to global popularity ranking" **directly**, rather than only through an accuracy comparison | diagnostic; decides nothing, see 10.5 |

**Aggregation.** Every metric is computed **per learner and then averaged over learners (macro)**
within a presentation. Micro-averaging over interactions would weight heavy users more and, in a
population this skewed, would change the conclusion. The **median and the full per-learner
distribution are reported beside every mean**, and per-presentation values are always published in
full — this is the lesson of the pilot's `NaN` bug, where the same defect moved the mean gain
against CF to −14.8% while the median stayed near −2.9%.

**Adding metrics is reporting, not threshold-moving.** C1, C2 and C3 remain judged on Precision@10
exactly as `plan.md` states. Recall, NDCG, HitRate and MRR exist so that a conclusion is not an
artefact of one ceiling-bound metric, and no criterion is ever re-decided on them (rule 3).

### 9.1 The Precision@10 ceiling, quantified

A learner with `|T(u)| < 10` **cannot** reach Precision@10 = 1; their maximum is `|T(u)| / 10`.

**Revision 1 note (G3 blocker B1).** Revision 0's table was computed on a plain pair-level
leave-last-20% construction and therefore did not describe the split this protocol specifies. The
table below is recomputed on **the section 5.1 day-boundary split, over the section 4.1 evaluated
population**, and again at revision 2 after blocker B1's repair to the split. The headline figures
have moved twice: EEE_2014J 47.9% (revision 0) → 45.5% (revision 1) → **45.6%**; range across the
22 presentations 15.7%–82.6% → 14.0%–81.1% → **14.4%–81.3%**; learners with exactly one test item
0.0%–4.2% → 0.3%–4.0% → **0.3%–4.3%**.

| Presentation | Test items per learner (mean / median) | Learners with < 10 test items | Learners with 1 test item |
| --- | --- | --- | --- |
| AAA_2013J | 12.8 / 13 | 28.3% | 0.3% |
| AAA_2014J | 11.6 / 12 | 36.3% | 0.3% |
| BBB_2013B | 8.1 / 7 | 67.0% | 2.7% |
| BBB_2013J | 8.0 / 7 | 67.4% | 3.8% |
| BBB_2014B | 7.8 / 7 | 70.9% | 2.8% |
| BBB_2014J | 12.1 / 12 | 37.3% | 2.8% |
| CCC_2014B | 10.4 / 9 | 52.3% | 3.5% |
| CCC_2014J | 10.8 / 9 | 50.4% | 3.3% |
| DDD_2013B | 21.8 / 21 | 20.3% | 1.7% |
| DDD_2013J | 18.6 / 17 | 26.1% | 1.8% |
| DDD_2014B | 17.8 / 16 | 30.1% | 1.5% |
| DDD_2014J | 15.5 / 14 | 32.6% | 3.0% |
| EEE_2013J | 9.3 / 10 | 44.9% | 1.9% |
| EEE_2014B | 8.6 / 9 | 53.1% | 2.4% |
| **EEE_2014J** | **9.3 / 10** | **45.6%** | **2.0%** |
| FFF_2013B | 25.0 / 23 | **14.4%** | 1.0% |
| FFF_2013J | 23.1 / 22 | 18.5% | 0.9% |
| FFF_2014B | 20.3 / 19 | 21.3% | 1.1% |
| FFF_2014J | 21.6 / 21 | 20.8% | 1.7% |
| GGG_2013J | 7.0 / 7 | 78.3% | 3.5% |
| GGG_2014B | 6.7 / 7 | **81.3%** | 4.3% |
| GGG_2014J | 7.2 / 7 | 76.1% | 2.4% |

So in EEE_2014J, **45.6% of evaluated learners are ceiling-bound on the primary metric**, and
across the 22 presentations the share ranges from 14.4% to 81.3%. This is why Recall@K and NDCG@K
are reported alongside, why the distribution of `|T(u)|` is published next to every Precision
table, and why a Precision@10 difference between two presentations is never read as a difference in
model quality. `plan.md` fixed Precision@10 as the primary metric and it stays primary; this
section is the caveat that makes it readable, not a replacement for it.

---

## 10. Statistics plan

### 10.1 Families of comparisons, declared before the run

Holm correction is applied within each declared family and nowhere else. The families are fixed
here, in advance:

- **F1 (decides C1):** {hybrid vs. CBF, hybrid vs. CF} on the warm slice, primary split. Size 2.
- **F2 (decides C2):** {hybrid vs. CF, hybrid vs. CBF} on the cold-start refit slice at k = 2.
  Size 2.
- **F3 (reporting):** the within-presentation per-learner comparisons of a slice: {hybrid vs. CBF,
  hybrid vs. CF, hybrid vs. MostPop, CF vs. CBF, CF vs. MostPop, CBF vs. MostPop}. Size 6.
- **F4 (exploratory):** everything else — other K values, other metrics, the k curve, the secondary
  and tertiary splits, the Condition B comparisons, `PopWeek` and `Random`. Labelled exploratory,
  Holm-corrected within F4, and supporting **no** criterion.

### 10.2 Tests

| Comparison | Test | Unit | n | Correction | Reported with |
| --- | --- | --- | --- | --- | --- |
| C1 and C2 decision | paired Wilcoxon signed-rank, two-sided, on the presentation-level macro Precision@10 pairs | module presentation | 22 | Holm within F1 / F2 | the median relative gain, the per-presentation table, and the sign test below |
| Generalisation companion | exact binomial sign test, two-sided, on the 22 per-presentation signed differences | module presentation | 22 | — | number of presentations favouring each model |
| Within a presentation | paired Wilcoxon signed-rank, two-sided, on per-learner Precision@10 | learner | 347 to 2,131 | Holm within F3 | rank-biserial correlation as effect size, and the median per-learner difference |
| Uncertainty of any reported number | bootstrap percentile 95% CI, 10,000 resamples over learners, `numpy.random.default_rng(42)` | learner | as above | — | reported as `value [lo, hi]`, never as a bare number |
| Stochastic models | 5 seeds (42–46), mean and standard deviation across seeds, every seed in the results | seed | 5 | — | applies to `Random` only; the other five models are deterministic and state so |

### 10.2a Zero differences, zero baselines, and what the test is run on (G3 warning W2)

Exact ties are not hypothetical here: the pilot produced hybrid and CBF Precision@10 values that
were **bit-identical** in BBB_2013B, DDD_2013B and DDD_2013J, the three presentations where the
week fields are 100% missing, and near-ties remain possible there because CBF carries almost no
week information. The rules below are fixed in advance.

1. **What the Wilcoxon is run on.** The deciding test is run on the **paired absolute
   presentation-level macro Precision@10 values** — 22 pairs of the form
   `(P@10_hybrid[i], P@10_baseline[i])` — not on the relative gains. The criterion's *threshold* is
   on the median relative gain, while its *test* asks whether the paired difference is
   distinguishable from zero; these are deliberately two different questions about the same 22
   pairs, and both are reported. Running the test on ratios would also make it undefined wherever
   the baseline is 0.
2. **Zero differences in the Wilcoxon.** `scipy.stats.wilcoxon` with `zero_method="wilcox"`, which
   **discards** zero differences, and `alternative="two-sided"`, `correction=False`,
   `mode="exact"` where scipy permits it. The **effective n after discarding ties is reported
   beside every p-value**, because it can be below 22 and it changes the smallest attainable p. If
   the effective n falls below 6 the two-sided exact test cannot reach p < 0.05 at any effect size;
   in that case the result is reported as **`inconclusive (effective n = <n>)`**, never as "not
   significant", and the criterion's test conjunct is recorded as `unchecked` under rule 6 rather
   than as a failure.
3. **Zero differences in the sign test.** The exact binomial sign test likewise drops zero
   differences; its effective n is reported on the same terms, with the same `inconclusive` rule
   below n = 6.
3a. **How a criterion is worded when a conjunct is `inconclusive`.** A criterion whose threshold
   conjunct is met but whose test conjunct is `inconclusive` for want of effective pairs is
   reported as **"not met (unchecked conjunct)"**, never as "met" and never as a bare "not met".
   The `inconclusive` outcome removes the possibility of a pass; it cannot create one, and it is
   not evidence against the hypothesis either. Chapter 5 states which conjunct was unchecked and
   why.
4. **A baseline Precision@10 of 0.** The relative gain `(hybrid − baseline) / baseline` is
   **undefined** when the baseline is 0. Such a presentation is **excluded from the median** and
   the number excluded is reported beside it; the median is never computed over a silently smaller
   set. For the sign test the same presentation still contributes a sign: `+` if the hybrid is
   above 0, and a zero difference (dropped) if both are 0. A relative gain is never imputed, capped
   or replaced by a large finite number.
5. **Reporting duty.** Every reported test carries: the test name, the effective n, the p-value
   before and after Holm correction, the effect size, and the count of pairs dropped as ties and as
   undefined ratios. A test whose effective n was reduced is never quoted without that n.

### 10.3 Which unit decides C1 and C2, and why — operationalisation D3

`plan.md` writes C1 and C2 as "median over the 22 module-presentations, AND paired Wilcoxon
signed-rank p < 0.05 after Holm correction" without naming the test's unit. Two readings exist:
per-learner within a presentation, or per-presentation across the 22. **This protocol fixes the
per-presentation unit (n = 22) as the deciding test**, for two reasons: the criterion's own
aggregation unit is already the 22 presentations, so using a different unit for the median and for
the test would make the criterion internally inconsistent; and the presentation-level test is the
**less powerful** of the two, so the reading chosen is the conservative one and cannot be
characterised as loosening the bar. The per-learner within-presentation Wilcoxon of F3 is computed
and reported for all 22, with its effect size and bootstrap interval, and decides nothing.

This choice is also what the evaluation literature supports here: Wilcoxon and sign tests show
inflated Type-I error at large sample sizes, and the per-learner tests in this design run at n
between 350 and 2,196 <!-- ledger: ihemelandu2023inference -->. The same source is why **an effect
size accompanies every p-value**: with over a thousand paired learners, a relative gap of a few
percent can be statistically detectable and practically negligible at the same time, and chapter 5
must say both.

### 10.4 Non-independence of the replication unit

The 22 presentations are not fully independent: they are 22 presentations of only 7 modules, and
two presentations of the same module share a catalogue and a syllabus. The across-22 tests are
therefore reported as **indicative of generalisation, not as a random sample of courses**, and a
per-module breakdown (7 modules, 2 to 4 presentations each) is published beside the 22-row table so
a reader can see whether a result is driven by one module.

### 10.5 Resolving the reviewer's two warnings on C3

The G1 verdict (`reviews/plan_gate.md`, W1 and W2) raised two non-blocking issues, carried into S3
by manager decision M4. Both are resolved here; neither resolution changes a number.

**W1 — "verbatim" is an overclaim. Resolved, and corrected in this protocol.** C3's `why` field in
`plan.md` says it carries "idea.md criterion 2 verbatim, including its popularity-fallback clause."
It does not. `idea.md`'s criterion 2 reads:

> on a held-out set of simulated/actual new users (<=2 prior interactions), the hybrid model must
> produce non-degenerate top-K recommendations (not empty, not identical for every user) and must
> not simply fall back to global popularity ranking without at least matching the
> content-based-only baseline's Precision@10 on that same cold-start slice.

That is one qualitative, conditional clause with no numeric bar against popularity and no stated
aggregation. C3's four conjuncts — `>=` CBF, `>` popularity, zero empty lists, `>= 10%` catalogue
coverage, in each of the 22 — are **an operationalisation of that clause, not a quotation of it.**
`plan.md`'s text is frozen and this protocol does not edit it; instead, **chapter 3 and every later
chapter describe C3 as an operationalisation of `idea.md` criterion 2, never as its verbatim
carry-over**, and quote `idea.md`'s sentence next to C3's conjuncts so a reader can see the
distance between them. The operationalisation is necessary and was defensible: the clause could not
be judged in phase 1 at all, because no popularity baseline existed, and rule 6 makes an unbuilt
comparison `unchecked`, never `passed`. **No threshold moves.**

Two additions make the operationalisation honest rather than merely decidable. First, the `>`
against `MostPop` is *stricter* than the literal clause, which asks only that the hybrid not *be* a
popularity ranking; this protocol keeps the stricter conjunct because `plan.md` is frozen, and
records the distance. Second, the **popularity-agreement diagnostic of section 9** (Kendall τ and
top-10 overlap between the hybrid's cold-start ranking and `MostPop`'s) measures the literal clause
directly. It is reported for all 22 presentations and **decides nothing**, so it adds evidence
without touching the criterion.

**W2 — C3's zero-tolerance aggregation against C1/C2's median-plus-significance. Resolved by
recording the asymmetry as a deliberate, named choice, which is the second route the reviewer
itself offered.** The asymmetry is not an oversight; it follows from the conjuncts being two
different kinds of quantity:

- C3's conjuncts (c) *zero empty top-10 lists* and (d) *>= 10% catalogue coverage* are
  **structural invariants of the output**, not noisy estimates of an effect. A degeneracy guarantee
  that holds "on median" is not a guarantee: a model that emits empty lists in three presentations
  has a defect in those three, and averaging it away would hide exactly the failure the conjunct
  exists to catch. A universal quantifier is the **only** correct aggregation for a structural
  floor, so (c) and (d) stay per-presentation, in all 22, unchanged.
- C3's conjuncts (a) *>= CBF's Precision@10* and (b) *> `MostPop`'s Precision@10* are accuracy
  comparisons of the same kind as C1 and C2, so the reviewer's observation bites here. But they sit
  inside C3, whose role in the criterion set is a **floor**, not an effect-size claim: C1 and C2
  assert that the hybrid is *better by a stated margin*, and estimating a margin is what a median
  and a significance test are for; C3 asserts that the hybrid *never falls below* two reference
  points, and a floor is meaningful only where it is checked. Keeping (a) and (b) universal is
  therefore coherent with what C3 is for, and it is also the **stricter** reading.

**Reporting required beside every per-presentation C3 verdict** (G3 cycle 2 warning W7). C3's
conjuncts are strict per-presentation comparisons with no noise allowance, and the deciding number
is noisy: measured on EEE_2014J at `k = 2` with `MostPop` over the 204-learner cohort, the
per-learner standard deviation is 0.059, **81% of cold learners score exactly 0**, and the standard
error of the mean is 0.0041, about 16% of the mean; at the smallest cohort (69 learners) it is
roughly 0.0071, about 28%. Therefore: each per-presentation C3 verdict is printed **beside the
paired bootstrap interval of the difference** (the machinery of section 10.2, no new apparatus),
and it is **pre-declared here** that a shortfall lying inside that interval is still reported as
**not met** — the interval is information for the reader, never a second chance for the criterion.
It is also pre-declared that cold-start Precision@10 values of the order of 0.02 to 0.03 are
**not** evidence that the models failed: the cold target is the set of resources the learner first
opens after the boundary, so resources opened in the middle of their history count as misses for
every model equally, and the attainable ceiling is the one already tabulated in section 9.1 (the
test sets are identical across conditions). Chapter 5 states this before quoting any cold-start
number.

**Named decision M-C3, recorded here and in `thesis/ch03.md`:** C3 is judged exactly as `plan.md`
states it — all four conjuncts, in each of the 22 presentations — and the asymmetry with C1 and C2
is deliberate, because C3 is a floor and a degeneracy guarantee while C1 and C2 are effect claims.
So that the three criteria can still be read against one another, conjuncts (a) and (b) are
**additionally reported** in the C1/C2 style — the median relative difference over the 22 and the
Holm-corrected paired Wilcoxon over the 22, inside exploratory family F4 — as **reporting that
decides nothing**. A reader then sees both the floor result and the effect-size result for the same
comparison.

**What I did not decide, and why it goes to the human.** Replacing C3(a)/(b)'s decision rule with
the median-plus-significance rule would **relax** C3: a hybrid that falls below CBF or below
`MostPop` in one or two presentations would fail the frozen rule and could pass the relaxed one.
That is a change to a frozen criterion and is reserved for the human under rule 3 and standards
decision 1. It is carried as open question **OQ6**, with the protocol running the frozen rule until
and unless the human decides otherwise.

---

## 11. Tuning protocol

1. Every hyperparameter — `ItemKNN-CF`'s neighbourhood `N`, the hybrid's logistic-regression `C`,
   and the blend weight `α` itself — is selected or fitted on the **validation split only**, using
   the grids fixed in section 8 before the run.
2. No value is refitted on training plus validation; the policy is identical for every model
   (section 8).
3. The chosen values are reported per presentation in chapter 3's appendix table and in the run
   receipt, with the search budget (at most 5 configurations per tunable model per presentation).
4. The test split is scored **exactly once** per model per presentation, counted and asserted (L6,
   C4).
5. Any value chosen after a test score was seen is labelled **exploratory** in chapter 5 and
   supports no criterion. The known case is the pilot's iteration 2 `alpha` formula.
6. If a model exceeds the C5 compute budget, the **grid** shrinks, never the seed count or the
   bootstrap resamples: variance reporting is a gate condition and a larger grid is not.

---

## 12. Reproducibility fields

| Field | Value |
| --- | --- |
| Data version and checksums | section 2.1, eight files with SHA256 and byte size, all matching `inputs/manifest.json` |
| Dataset source URL and download date | `https://analyse.kmi.open.ac.uk/open_dataset` as printed in `OULAD.names`; local copy dated 2026-09-14 from the mtime of `oulad.zip`; exact fetch URL not recorded — OQ1 |
| Preprocessing and entry point | `<project_root>/code/`, per `plan.md` Modules R, A, B, C, D; entry point accepts the stage, an artifact directory and a run-log path (G4 condition) |
| Split rule and ordering key | section 5: `first_date` ascending, tie-break `id_site`; 70 / 10 / 20 per learner; **no seed needed for the split** |
| Seeds | 42 for the cold-start cohort draw, the bootstrap and the tertiary random split; 42–46 for the `Random` baseline's 5 runs. Every seed and every run is reported, never the best |
| Code version | git commit SHA of `<project_root>/code/` at run time, recorded in the receipt |
| Python | 3.12.3 (AMD64), `.venv-pilot\Scripts\python.exe`, with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUTF8=1` |
| Library versions | numpy 2.5.3, pandas 3.0.5, scikit-learn 1.9.1, scipy 1.18.1 (verified 2026-09-21 in that interpreter) |
| Hardware | single CPU, Windows 10, 12 logical cores available; **no GPU**, no downloaded model weights, no network access required at run time |
| Wall-clock budget | see section 12.1; C5 is measured as **process CPU time**, and wall-clock is reported beside it |
| Command line per reported number | recorded verbatim in the receipt for each run, together with the SHA256 of every artifact it produced (recorded deviation D2: receipts are written by hand because the workflow engine imports `fcntl` and cannot run on this machine — D1) |

### 12.1 What "CPU-hours" means, and what the C5 budget has to cover (G3 warning W4a)

**Definition.** C5's budget is measured in **process CPU time**: the sum of user and system CPU
time consumed by the run, obtained as `time.process_time()` and divided by 3,600. Verified
2026-09-21: `.venv-pilot` has neither `resource` nor `psutil`, so revision 1's reference to them
was not executable. It is also unnecessary — **the run is single-process by design**, with no
subprocess and no `joblib`/`n_jobs` parallelism anywhere in section 8, so `time.process_time()`
accounts for all of it. If a future change introduces a child process or a threaded BLAS path that
`time.process_time()` would miss, that change must add a measurement that covers it before it is
run, and say so in the receipt. On a 12-logical-core machine
this is **not** wall-clock: a step using four cores for one minute costs about 4 core-minutes of
CPU time and one minute of wall clock. Revision 0 left this ambiguous. **Both numbers are
recorded** in every receipt — `cpu_hours` and `wall_clock_seconds` — and **C5 is judged on
`cpu_hours`**, which is the stricter of the two on multi-core hardware and the one that cannot be
made to look small by parallelising. The idea file's own wording is wall-clock, and the wall-clock
figure is reported beside it so that constraint is checkable too.

**What the budget must cover.** Revision 0's arithmetic named three splits, six models, two
cold-start conditions and four k values, and omitted the P4a sensitivity reruns, which is a real
omission because P4a promises the run be repeated at learner thresholds of 3 and 10. The budget is
therefore itemised:

| Component | Scope | Counted in C5 |
| --- | --- | --- |
| Main run | 22 presentations × 3 splits × 6 models × (warm + Condition A at k ∈ {0,1,2,5} + Condition A robustness at k = 2 + Condition B at k ∈ {0,1,2,5}) | yes |
| Blend-model fits | one `α` model per (presentation, condition, k), each a 4-configuration 5-fold selection over at most ~2,100 learner rows with 8 features | yes |
| Bootstrap | 10,000 resamples over learners per reported number | yes |
| Significance tests | Wilcoxon, sign test, Holm | yes, negligible |
| **P4a sensitivity reruns** | item thresholds 3 and 10, **restricted to the primary split, the warm slice and Condition A at k = 2** — the narrowest run that answers "does the filter choice move the conclusion", not a second full grid | **yes**, and this is the addition revision 0 omitted |
| **P4b sensitivity rerun** | the days filter relaxed from 3 to **2**, same narrow scope (G3 cycle 1 warning W5b). A two-day learner cannot carry a per-learner validation slice, so for this run only, such a learner is split **train/test on their two days** and scored with the presentation-level `N`, `C` and `α` model already fitted on the main run's validation learners — no hyperparameter is refitted, so nothing is tuned on the added learners. It answers the question the filter raises: does including the one-or-two-visit learners, who are the closest thing in this data to `idea.md`'s "actual new users", move the warm and cold-start conclusions? | **yes**, and this is the addition revision 1 omitted |
| C6 reproduction | EEE_2014J, phase 1 configuration | no — it has its own 15-minute bound in C5 |

The training bound and the exclusion moment that the P4b two-day run uses for its two-day learners are fixed in section 5.5.

**Stopping rule.** The runner measures `cpu_hours` for the first completed presentation, projects
the total including the sensitivity reruns above, and **stops for the human** if the projection
exceeds 4.0 CPU-hours, rather than silently overrunning C5. If the budget binds, the **search grid
shrinks first** (section 11 item 6) and the seed count and bootstrap resamples never do. Pilot
reference points for the projection: 29.3 s for one presentation and 140.1 s for all 22 under a
materially simpler phase 1 design.

---

## 13. Verification checks before any result is believed

- [ ] The per-slice completeness table of section 2.3 is regenerated by the run and matches this
      protocol; **no feature column is entirely missing without the documented P5 fallback**, and
      the code asserts it. The three presentations at 0.0% known week data — BBB_2013B, DDD_2013B,
      DDD_2013J — are named in the log by the assertion, not discovered afterwards.
- [ ] No feature matrix, score vector or similarity matrix contains `NaN` or `inf`, asserted after
      construction rather than repaired by a `nan_to_num` safety net alone.
- [ ] Leakage assertions L1 to L9 all executed, each emitting its measured count, all zero — and
      the provenance record of section 5.4 exists for **every** fitted object and every
      preprocessing constant, so L2 and L3 are counted tests rather than claims.
- [ ] The section 4.1 population table is regenerated by the run and matches: 27,212 evaluated
      learners, the per-presentation `−<5 items` and `−<3 days` drops, and the cohort sizes.
- [ ] The split's own exclusion count is **0**, because P4b already removed every learner the
      day-boundary construction cannot serve (section 5.1 step 4).
- [ ] The realised test and validation fractions per presentation fall in the recorded ranges
      (test 0.199–0.205, validation 0.102–0.120); any presentation outside them is investigated
      before its numbers are used.
- [ ] All eight Condition A rows of section 6.1a emit their provenance record, with
      `n_cold_learners_used = 0` for A1, A2, A3, A6 and A7, and `n_learner_rows_used = 0` for A4.
- [ ] The hybrid's run log records `n_configurations`, `n_label_grid_points`, the selected `C`, the
      inherited `N`, and whether `alpha_model = constant` or `C_selection = skipped` was triggered
      (section 8.1 step 10).
- [ ] Every reported test carries its effective n after ties are dropped, and every median relative
      gain carries the count of presentations excluded for an undefined ratio (section 10.2a).
- [ ] Every model received identical splits, proved by comparing the SHA256 of the serialised pair
      sets (L5).
- [ ] The cold-start visible list is sorted ascending by `first_date`, asserted per learner — the
      check that proves the pilot's shuffled-"first-2" defect did not recur.
- [ ] The cold-start refit matrix contains **no** row for any cold-start learner, asserted by set
      difference on learner ids.
- [ ] The test split was scored exactly once per model per presentation (L6).
- [ ] C6: the phase 1 configuration reproduces the six recorded Precision@10 values on EEE_2014J
      (warm CBF 0.11820781696854146, CF 0.5351763584366063, hybrid 0.5207816968541468; cold-start
      CBF 0.10066730219256434, CF 0.16101048617731176, hybrid 0.14022878932316493) to within 1e-6,
      or the difference is explained before any phase 2 number is quoted.
- [ ] `python check_protocol.py <project_root>/methodology/protocol.md` exits 0.

---

## 14. Threats to validity

Full table in `<project_root>/methodology/threats_to_validity.md`. In one line each:

- **Internal.** Temporal leakage, tuning on test data, the all-missing week columns and the `NaN`
  propagation they caused, a cold-start condition whose similarity model saw the cold learners, and
  a shuffled slice presented as an earliest-k slice — each has a mechanism fixed in this protocol
  and an assertion in section 13.
- **External.** One dataset, one country, one institution type, one platform's navigation, and an
  evaluated population of unusually active learners (median 49 distinct resources of 115 in
  EEE_2014J) from which the disengaged learner is absent before measurement begins.
- **Construct.** Clicks as a proxy for learning need, `sum_click` standing in for the dwell time the
  hypothesis names, Precision@10 as a proxy for usefulness, and unobserved items counted as
  negatives.
- **Conclusion.** Differences of a few percent, many pairwise comparisons, Precision@10's ceiling
  for the 14.4% to 81.3% of learners with fewer than 10 test items, and 22 presentations that are
  not independent because they come from 7 modules.

---

## 15. Ethics and data statement

Full statement in `<project_root>/methodology/data_statement.md`. In one line: OULAD is public,
anonymised, secondary data, used under the CC BY 4.0 licence quoted there from the authors' own
deposit with the URL and date opened; no re-identification of any learner is attempted, no
demographic attribute is used as a model feature, all reporting is aggregate, and the residual
licence-provenance gap and the AI-disclosure wording are recorded as open questions rather than
assumed.

---

## 16. Deviations from `plan.md`

| # | Deviation | Reason | Who must approve |
| --- | --- | --- | --- |
| D3 | The unit of C1's and C2's deciding Wilcoxon test is fixed as the module presentation (n = 22), which `plan.md` leaves unstated | keeps the criterion's median and its test on the same unit; it is the less powerful of the two readings, so it cannot loosen the bar (section 10.3) | reviewer at G3; escalate to the human if the reviewer reads it as a change of substance |
| D4 | Two models are added beyond `plan.md` Module B's four: a `Random` floor (5 seeds) and a week-aware popularity variant `PopWeek` | a metric value is unreadable without a floor, and week-aware popularity is the strongest non-personalised competitor in a course setting and the one an e-learning examiner names. Both are reporting only; C3's "global-popularity baseline" remains `MostPop` alone, and neither addition decides any criterion | reviewer at G3 |
| D5 | Metrics are added beyond Precision@10: Recall, NDCG, HitRate, MRR at K = 5, 10, 20, catalogue coverage, intra-list diversity, empty-list count and a popularity-agreement diagnostic | Precision@10 is ceiling-bound for 14.4% to 81.3% of evaluated learners (section 9.1); adding metrics is reporting, and C1 to C3 stay judged on Precision@10 (rule 3) | reviewer at G3 |
| D6 | Three splits are run — primary per-learner time-based, secondary global cut-off, tertiary the pilot's random holdout — where `plan.md` Module A names a time-based split | the secondary is a robustness check on a real design choice, and the tertiary is what makes the phase 1 record comparable and quantifies the cost of the pilot's leakage. The conclusion rests on the primary; the tertiary is labelled temporally leaky wherever it appears | reviewer at G3 |
| D7 | Two cold-start conditions are run where `plan.md` C2 names the refit condition | the human's recorded decision Q1 requires both, with the refit condition primary and deciding C2 and the thin-history condition labelled optimistic | already approved by the human (Q1, `decisions.log` 2026-09-21) |
| D8 | C3's `why` field in `plan.md` calls C3 a verbatim carry-over of `idea.md` criterion 2; this protocol and chapter 3 describe it as an **operationalisation** and quote `idea.md`'s clause beside it | the G1 verdict's W1 is correct: `idea.md`'s clause is conditional and numeric-free, and C3 adds four conjuncts. The wording is corrected; **no threshold moves** and `plan.md` is not edited by this role | reviewer at G3; the human owns any edit to `plan.md`'s text |
| D9 | The asymmetry between C3's universal aggregation and C1/C2's median-plus-significance is recorded as a deliberate, named choice (M-C3) rather than reconciled | reconciling C3's accuracy conjuncts to the C1/C2 rule would relax a frozen criterion, which rule 3 reserves for the human; the degeneracy conjuncts are structural invariants for which a universal rule is the only correct one (section 10.5) | reviewer at G3; the underlying question is OQ6 for the human |
| D10 | No `studentInfo.csv` column is used as a model feature, and `assessments.csv` and `studentAssessment.csv` are not used at all | `plan.md`'s modules specify no demographic or assessment feature, and whether demographics may be used is an unanswered ethics question (OQ3); rule 6 forbids treating silence as permission | reviewer at G3 |
| D11 | The learner filter gains a second, pre-registered condition: at least **3 distinct first-interaction days** (P4b) | the day-boundary split of section 5.1 assigns whole days and needs three to produce a non-empty train, validation and test set. Making it a population filter rather than a split-time casualty is what keeps the evaluated population well defined; it removes **997 of 28,209** learners (3.53%), the excluded group is profiled in section 4.1, it has its own sensitivity rerun in section 12.1, and the exclusion is reported as threat T22 rather than absorbed. The G3 cycle 1 reviewer judged that a learner-inclusion rule changes neither the hypothesis text nor any `on_dataset` field, so it is an operationalisation this role owns; the narrowing of the population toward engaged learners is nevertheless flagged for the supervisor as OQ7 | reviewer at G3 (revision 1, corrected at revision 2 under blocker B1) |
| D12 | The at-least-**5**-distinct-items learner filter (P4a) is a deviation in its own right | G3 cycle 1 warning W5a is correct: `plan.md` contains **no** learner filter, so this rule is inherited from the pilot code (`MIN_ITEMS_FOR_EVAL_USER = 5` in `pilot_recommender.py`), not from the frozen plan. Revision 1's D11 wrongly called it "`plan.md`'s inherited at-least-5-items rule". It is kept because it makes the phase 1 and phase 2 populations comparable, it is varied at 3 and 10 as a sensitivity run, and it is now recorded rather than presented as inherited authority | reviewer at G3 |
| D13 | The deciding Wilcoxon for C1 and C2 is computed on the **paired absolute** presentation-level Precision@10 values, while the criterion's threshold is on the **median relative gain** (section 10.2a item 1) | a further operationalisation of the same kind as D3, and listed here at the G3 cycle 1 reviewer's request (W5c) rather than left inside the statistics section. The threshold asks how large a gain is; the test asks whether the paired difference is distinguishable from zero. Running the test on ratios would additionally make it undefined wherever a baseline scores 0 | reviewer at G3 |
| D14 | Module D is descriptive only: it describes the behavioural feature distributions and clusters learners for description, feeds no model, and supplies no cold-start prior, where `plan.md` Module D says it supplies Module B's cold-start prior and answers RQ1 and RQ2 | no segmented model exists among the six compared models, so nothing can consume a cluster or a prior, and the implemented and receipted Module D is descriptive; RQ1 is addressed descriptively and RQ2 as `plan.md` words it is not answerable from this design. Recorded 2026-09-24 as a clarification of section 3.1 (cross-artifact fix I1), not as a change to any design decision, threshold or criterion | human candidate |

Nothing in this protocol changes a success criterion, a threshold, the hypothesis, the dataset or a
research question.

---

## 17. Open questions for the human

| # | Question | Blocks what | Owner |
| --- | --- | --- | --- |
| OQ1 | The exact URL the local OULAD archive was fetched from, and confirmation that it was the copy carrying the CC BY 4.0 licence. The licence is verified at the authors' figshare deposit (section 2, data statement), but the bytes on disk were extracted from `oulad.zip` whose source URL is recorded nowhere, and the archive itself contains no licence file (8 members, verified). | the data statement's licence claim is sound but its provenance chain has one unverified link; chapter 3 states this rather than hiding it | human candidate |
| OQ2 | University thesis regulations: required format, the language of each part, the citation style, the ethics wording and the AI-assistance disclosure wording. Nothing in this protocol assumes any of them. | chapter 3's language, its citation format, and the ethics and AI-disclosure sections of the data statement | human candidate |
| OQ3 | Whether any demographic attribute (`gender`, `age_band`, `disability`, `imd_band`, `region`) may be used as a model feature at all. Until answered, none is used and none is needed. | Module D's feature set if the answer is yes; a fairness-difference check becomes mandatory in that case | human candidate |
| OQ4 | Confirmation that deferring the user interface and the deep models (RNN, CNN, RBFNN) as scope-outs is acceptable to the supervisor. Recorded decision Q5 defers both; chapter 3 states them as deferred scope-outs and chapter 6 lists them as future work. | the proposal-traceability table's two "out of scope" rows | supervisor, via the human |
| OQ5 | Whether the Arabic rendering of Precision as **الضبط**, distinct from accuracy (**الدقة**), is accepted; chapter 2 proposes the pair and chapter 3 must define the primary metric in both languages. | chapter 3's metric definitions | supervisor, via the human |
| OQ6 | Whether C3's accuracy conjuncts (`>=` CBF and `>` `MostPop`) should stay judged in **each** of the 22 presentations, as `plan.md` freezes them and this protocol runs them, or be relaxed to the median-plus-significance rule of C1 and C2. Relaxing them would let a hybrid that falls below a baseline in one or two presentations still pass C3, so it changes what the criterion demands and is a rule 3 decision the methodologist may not take. | nothing now — the frozen rule runs — but chapter 5's C3 verdict would change if the answer is "relax" | human candidate |
| OQ7 | The evaluated population is narrowed **twice** away from the learners the system is meant to help: by at least 5 distinct resources (D12, inherited from the pilot, absent from `plan.md`) and by at least 3 distinct active days (D11). Together they remove 2,016 of the 29,228 learners in the logs, and the second removes precisely the one- and two-visit learners closest to `idea.md` criterion 2's "actual new users". The G3 reviewer judged the filters to be operationalisations this role may adopt, and they are adopted; **the supervisor should nevertheless see the narrowing and say whether criterion 2 is to be read as requiring actual rather than simulated new users**, because that reading would put the whole filter design in question. | nothing now — both filters run, both have sensitivity reruns, and the limitation is in chapter 3 and threat T22 — but a "actual new users only" reading would require a redesign | human candidate, via the supervisor |
| OQ8 | RQ2 as `plan.md` words it (whether segmenting learners by behavioural profile improves the cold-start prior over a non-segmented hybrid) cannot be answered from this design, because no segmented model is compared; this is decisions.log finding F11. Whether to leave RQ2 unanswered and say so, to reword it (the human's decision, frozen in `plan.md`), or to add a segmented model in a later phase. Until answered, Module D stays descriptive and RQ1 is addressed descriptively | how chapters 3, 5 and 6 state the answer to RQ2 | human candidate |


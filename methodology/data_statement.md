# Data and ethics statement

Companion to `methodology/protocol.md` (unit `u07_s3_methodology`, cycle 0, written 2026-09-21).
Nothing here is written from memory. Each claim is either quoted from a source that was opened,
with its URL and the date it was opened, or marked `unverified`. Rule 6: absence of a check is
`unchecked`, never `passed`.

## 1. Dataset

- **Name:** Open University Learning Analytics Dataset (OULAD)
- **Citation, as printed on the data descriptor:** Kuzilek J., Hlosta M., Zdrahal Z. *Open
  University Learning Analytics dataset*, Nature Scientific Data 4:170171,
  doi: 10.1038/sdata.2017.171 (2017)
- **Deposit of record:** Kuzilek J., Hlosta M., Zdrahal Z., *OULAD: Open University Learning
  Analytics Dataset*, figshare, DOI `10.6084/m9.figshare.5081998.v1`, published
  `2017-06-06T08:06:34Z`
- **Source URL printed in the distributed archive** (`OULAD.names`, section 4):
  `https://analyse.kmi.open.ac.uk/open_dataset`
- **Download date of the local copy:** 2026-09-14, taken from the filesystem modification time of
  `data/projects/e_learning_pilot/data/raw/oulad.zip`. The extracted CSVs carry the archive's own
  2015 timestamps.
- **Files and checksums:** the eight-row table in `methodology/protocol.md` §2.1. All eight SHA256
  values were recomputed from the files on 2026-09-21 and match `inputs/manifest.json` exactly.

## 2. Licence

**Status: quoted, with one recorded gap in the provenance chain.**

The licence was **not** found where it was first looked for, and that is recorded before the
quotation is given:

1. `https://analyse.kmi.open.ac.uk/open_dataset` — the URL the archive itself prints — returned
   HTTP 301 to `https://research.stem.open.ac.uk/ouanalyse/` (opened 2026-09-21). That page
   carries no dataset download and **no licence statement**.
2. The distributed archive contains no licence file. `oulad.zip` holds exactly eight members —
   `assessments.csv`, `courses.csv`, `studentAssessment.csv`, `studentInfo.csv`,
   `studentRegistration.csv`, `studentVle.csv`, `vle.csv`, `OULAD.names` — and a search of
   `OULAD.names` for `licen`, `creative commons`, `CC-BY`, `copyright` and `terms` returns zero
   matches (checked 2026-09-21).
3. The **dataset authors' own deposit** does state a licence. The figshare item
   `10.6084/m9.figshare.5081998.v1`, authored by Jakub Kuzilek, Martin Hlosta and Zdenek Zdrahal —
   the same three authors as the data descriptor — carries the licence field, retrieved verbatim
   from `https://api.figshare.com/v2/articles/5081998` on 2026-09-21:

> ```json
> "license": {
>   "name": "CC BY 4.0",
>   "url": "https://creativecommons.org/licenses/by/4.0/"
> }
> ```

4. Corroboration from a second independent host: the UCI Machine Learning Repository's page for the
   dataset (`https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset`,
   opened 2026-09-21) states: *"This dataset is licensed under a Creative Commons Attribution 4.0
   International (CC BY 4.0) license."* This is a hosting repository's statement and is recorded as
   corroboration, not as the primary source.

The licence text itself, quoted from `https://creativecommons.org/licenses/by/4.0/` (opened
2026-09-21). Title: **Attribution 4.0 International**.

> You are free to:
>
> **Share** — copy and redistribute the material in any medium or format for any purpose, even
> commercially.
>
> **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.
>
> Under the following terms:
>
> **Attribution** — You must give appropriate credit, provide a link to the license, and indicate
> if changes were made. You may do so in any reasonable manner, but not in any way that suggests
> the licensor endorses you or your use.

**Permitted uses under that licence, in one sentence:** the dataset may be used, analysed, adapted
and redistributed, including commercially, provided the authors are credited, a link to the licence
is provided, and any changes are indicated — which this thesis does by citing Kuzilek, Hlosta and
Zdrahal (2017), linking the licence here, and stating that it redistributes no part of the data.

**The recorded gap (open question OQ1).** The licence is verified for *the dataset as deposited by
its authors*. It is **not** traced to *this copy*: the bytes analysed came from `oulad.zip`, whose
fetch URL is recorded nowhere in this repository, and the archive carries no licence file of its
own. The honest statement, which chapter 3 makes rather than hides, is: OULAD is published by its
authors under CC BY 4.0, verified at their deposit on 2026-09-21; the provenance of the local
archive is not documented, and the human candidate is asked to confirm the download URL. No claim
in this thesis depends on the difference, because this work redistributes no part of the dataset
under any licence.

## 3. Provenance and population

- **Collected by:** The Open University, Walton Hall, Milton Keynes, MK7 6AA, United Kingdom, from
  its Virtual Learning Environment. Donors named in `OULAD.names` §2: Jakub Kuzilek (Knowledge
  Media Institute, The Open University; CIIRC, CTU in Prague), Martin Hlosta (KMi) and Zdenek
  Zdrahal (KMi; CIIRC, CTU in Prague). Date received by the archive: December 2015.
- **Population:** UK Open University distance learners on 7 modules across 22 module presentations,
  starting in February ("B") and October ("J") of 2013 and 2014.
- **Size, counted from the tables and not from the documentation:** 32,593 rows in
  `studentInfo.csv` and 32,593 in `studentRegistration.csv`; 10,655,280 interaction rows in
  `studentVle.csv`; 6,364 VLE items in `vle.csv`; 22 presentations in `courses.csv`.
  `OULAD.names` §5 states 32,953 students and 32,953 registration entries, contradicting both the
  CSVs and its own §9 class-distribution total of 32,593. **The figure used throughout this thesis
  is 32,593**, and the discrepancy is stated in chapter 3 rather than silently corrected.
- **Evaluated population after this thesis's filters:** **27,212** learners across the 22
  presentations, ranging from 347 (AAA_2014J) to 2,131 (CCC_2014J). Of the 29,228 learners who
  appear in the VLE logs, 1,019 are removed for holding fewer than 5 distinct resources and a
  further 997 for recording activity on fewer than 3 distinct days; the second group is profiled in
  `protocol.md` §4.1, because an exclusion correlated with disengagement is a limitation and not
  housekeeping, and it is put to the supervisor as open question OQ7. See `protocol.md` §4.1 for
  the per-presentation breakdown.
- **Not representative of:** the candidate's own institution, on-campus learners, non-UK cohorts,
  or disengaged learners. In EEE_2014J, 91 of 1,188 registered learners never touch the VLE at all
  and are invisible to this design; the learners who remain hold a median of 49 distinct resources
  out of 115. This limitation is repeated in chapter 3 and chapter 5.

## 4. Personal data handling

- The dataset is published in anonymised form. Learners appear only as `id_student`, an integer,
  with no name, no contact detail and no free text anywhere in the eight tables.
- **No attempt is made, in code or in analysis, to re-identify any learner**, and no linkage with
  any other dataset is performed. Nothing in this protocol joins OULAD to an external source.
- **All reporting is aggregate**: per model, per slice, per module presentation and per metric. No
  individual learner's history, score, demographic combination or identifier appears in the thesis,
  in a figure, in a table or in an appendix. Where a distribution is published, it is a summary
  statistic or a histogram, never a per-learner listing.
- The data stays inside the project root on the machine that runs the experiment. Nothing is
  uploaded to a third-party service, and the run requires no network access at all — the tables are
  already on disk and hashed in `inputs/manifest.json`.
- This thesis **redistributes no part of OULAD**. Readers are pointed at the citation and the
  deposit DOI.

## 5. Demographic attributes and fairness

`studentInfo.csv` carries `code_module`, `code_presentation`, `id_student`, `gender`, `region`,
`highest_education`, `imd_band`, `age_band`, `num_of_prev_attempts`, `studied_credits`,
`disability` and `final_result` (verified from the file's header, 2026-09-21).

- **Columns used as model features: none.** No demographic attribute enters any model in this
  protocol as a feature, a filter or a stratifier.
- **Columns deliberately excluded, with the reason:** `gender`, `region`, `highest_education`,
  `imd_band`, `age_band` and `disability` are protected or proxy-protected attributes whose use is
  an ethics decision reserved for the human candidate, not a modelling convenience (open question
  OQ3); rule 6 forbids treating an unanswered question as permission. `num_of_prev_attempts` and
  `studied_credits` are excluded because `plan.md`'s modules specify no such feature and adding one
  would be scope drift under rule 8. `final_result` is excluded because it is an **outcome**
  variable: using it as an input would leak the very thing an educational recommender is ultimately
  judged on.
- `studentInfo.csv` is read **only** to count how many learners exist, for the population figures in
  section 3 above.
- **If the human later authorises demographic features**, this protocol is revised rather than
  informally extended, and the revision makes a fairness check mandatory: recommendation quality
  (Precision@10, Recall@10, NDCG@10 and coverage) reported per group for every authorised
  attribute, with the group differences published **whatever they show**, including when they are
  unfavourable to the model this thesis proposes.
- A fairness caveat applies even with no demographic feature in the model: the evaluated population
  is skewed towards highly active learners, so a model tuned on it is tuned on the learners who
  need help least. This is stated in chapter 3 and chapter 5 as a limitation of who the system was
  measured for.

## 6. Ethics approval

- This is a **secondary analysis of a public, anonymised dataset**. No human participants are
  recruited, no new data is collected, no intervention is administered and no learner is contacted.
- Whether the university requires an ethics submission for secondary analysis of public anonymised
  data: **unverified** — the thesis regulations are not in this repository (recorded as a missing
  input in `decisions.log` on 2026-09-20 and as open question OQ2). The required wording, the form
  and the approval route are the human candidate's to supply; nothing is assumed here.

## 7. AI-assistance disclosure

- Parts of this work were produced with the assistance of AI agents operating under the project's
  thesis standards, which fix the stages, the gates, the evidence rules and the independent review
  process. Specifically: the literature search and ledger (stage S2), this methodology and chapter
  3 (stage S3), the experiment code, its execution and the results analysis (stages S4 to S7), and
  the chapter drafts (stage S8) were drafted by AI agents; every stage was reviewed at a gate by a
  reviewer running on a different model identity from the agent that produced the artifact, and the
  human candidate owns every decision about the research question, the hypothesis, the success
  thresholds, the dataset, the ethics and the submission itself.
- **The exact wording, placement and scope of this disclosure follow the university's regulations,
  which are not in this repository.** Until the human supplies them, this section is marked
  `unverified` and is a placeholder to be replaced, not a compliant disclosure (open question OQ2).

## 8. What this data may not be used for

- **Any claim about an individual learner**, their outcomes, their characteristics or their
  identity. The reporting is aggregate and the design cannot support an individual claim.
- **Any causal claim about learning.** This is an offline ranking comparison on logged clicks. It
  measures whether a model ranks a learner's later resources highly, not whether a recommendation
  caused a learner to learn, to persist or to pass. A click is engagement, not understanding, and
  `sum_click` is a count with no duration attached.
- **Any deployment decision at another institution** without re-validation on that institution's
  own data. OULAD is one UK distance-learning population on one platform.
- **Any re-identification attempt**, any linkage to another dataset, and any redistribution of the
  OULAD tables from this project.

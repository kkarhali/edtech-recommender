# ji2023leakage - Ji et al., 2023, A Critical Study on Data Leakage in Recommender System Offline Evaluation

- opened_on: 2026-09-20   source: 10.1145/3569930   type: journal   verified: yes
- Access: access=full text (open copy fetched 2026-09-20, not stored in the project) (arXiv 2010.11060 preprint copy of the published article; published version not opened)
- Problem: Data leakage in offline evaluation.
- Method: Timeline analysis and experiments with four baseline models on four datasets (Abstract).
- Data and domain: See row.
- Metrics and results (with the task each measures): Leakage impacts accuracy and makes relative model order unpredictable; a timeline scheme is proposed (Abstract).
- Limitations stated by the authors and noticed by me: Preprint copy read.
- My reading (what it means for this thesis): A split that ignores time can favour models that learn from the future; use a global timeline.
- Claims I will reuse, each with a locator:
  - Data leakage arises when the train/test split does not follow the global timeline - PDF p.1, abstract
  - Leaked future data makes the relative performance order of models unpredictable - PDF p.1, abstract

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

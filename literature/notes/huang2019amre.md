# huang2019amre - Huang et al., 2019, An Adaptive Mechanism for Recommendation Algorithm Ensemble

- opened_on: 2026-09-20   source: 10.1109/ACCESS.2019.2891561   type: journal   verified: yes
- Access: access=full text (local PDF); on-disk file is the accepted manuscript (banner: accepted for publication in a future issue, not fully edited), so page numbers are of that copy. IEEE Xplore page not opened (empty response); vol. 7, pp. 10331-10342 matched from Crossref and the proposal's bibliography
- Problem: Different CF algorithms suit different situations; choose the recommender adaptively per item.
- Method: Agents each hold a recommender and a reward value; correct recommendations reward, wrong ones punish; a roulette switches agent when the reward falls under a threshold (PDF pp.2-3).
- Data and domain: Two MovieLens subsets, 'leave-item-out': known ratio 20 percent; eleven individual CF algorithms plus two classical ensembles as comparators (PDF pp.3, 8).
- Metrics and results (with the task each measures): Tables 5-8 (PDF pp.8-9); text on PDF p.8: AMRE has the best Accuracy, Recall and F1 but lower Precision.
- Limitations stated by the authors and noticed by me: Noted by me: pointwise classification metrics, no cold-start evaluation, no significance test; the reference to new-user cold start is only in the bibliography (PDF p.11).
- My reading (what it means for this thesis): Shows that a system can top accuracy and recall and still rank last on precision, which is why chapter 5 must name Precision@10 and never 'accuracy'.
- Claims I will reuse, each with a locator:
  - The text states AMRE is best on Accuracy, Recall and F1 and lower on Precision - PDF p.8, section IV-D
  - Table 7: AMRE Precision 0.8808 is rank 12 of 12 on ML943u (0.2) - PDF p.9, Table 7
  - Metric definitions: accuracy (Eq. 12) and precision (Eq. 14) are separate quantities - PDF p.8

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

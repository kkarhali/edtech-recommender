# zhang2015hybrid - Zhang et al., 2015, A Hybrid Recommender System Based on User-Recommender Interaction

- opened_on: 2026-09-20   source: 10.1155/2015/145636   type: journal   verified: yes
- Access: access=full text (local PDF); journal PDF front page carries title, authors, volume, article ID, DOI, dates
- Problem: Real recommenders are interactive; evaluate recall and diversity over rounds in which the user picks items.
- Method: Round 1 random (cold start), then kNN mixed with a fraction of random items (RT = 0.25, TR = 3, k = 45 best) (PDF pp.4-9).
- Data and domain: MovieLens 943 users, 1,682 movies; each approach repeated 10 times because of the random component (PDF p.7).
- Metrics and results (with the task each measures): Conclusions on PDF p.10: random share below 0.25 does not hurt, use kNN early, k about 45, recall grows about linearly with list size, hybrid better than random. Fig. 5 (PDF pp.8-9) shows diversity of hybrid about equal to random.
- Limitations stated by the authors and noticed by me: Noted by me: no pure-kNN baseline is reported; no variance is shown for the 10 repeats; assumptions of fixed interests and fixed item set (PDF p.2).
- My reading (what it means for this thesis): Its 'hybrid' is random plus kNN. Useful as an example of mixing exploration into recommendation, not as a CBF-CF hybrid baseline.
- Claims I will reuse, each with a locator:
  - The hybrid is random plus kNN and uses random recommendations in the initial stage to deal with cold start - PDF pp.1-3
  - Comparison is between random and hybrid; recall of hybrid is higher, diversity about the same - PDF pp.8-9, Fig. 5

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

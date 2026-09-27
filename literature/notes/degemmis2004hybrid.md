# degemmis2004hybrid - Degemmis et al., 2004, A Hybrid Collaborative Recommender System Based on User Profiles

- opened_on: 2026-09-20   source: 10.5220/0002638201620169   type: conference   verified: yes
- Access: access=full text (local PDF); year 2004 read from the PDF footer (PDF p.1) and the SciTePress page (opened 2026-09-20: ICEIS 2004, Vol. 4, 162-169, six authors). The Crossref record for this DOI lists no authors and a different container title, so the PDF and publisher page are treated as authoritative. The proposal gives no year
- Problem: Improve collaborative filtering in e-commerce with knowledge stored in user profiles.
- Method: Profile Extractor infers 11 product-category interests from transactional data; the User Profile Engine's collaborative method then runs on each category's users (PDF pp.2-6).
- Data and domain: 380 users, 154 products, 90/10 train/test, 25 percent of items withheld per test user, 5 repeated test sets; relevant means score above 2.5 (PDF p.6).
- Metrics and results (with the task each measures): Table 4: UPE (pure CF) MAE 0.421, NDPM 0.066, F1 0.923; U(PE)2 MAE 1.936, NDPM 0.099, F1 0.839 (PDF p.7). Time: UPE 5h 47min on 380 users; U(PE)2 57min for recommendations plus 1h 27min for classification, 2h 24min in total (PDF p.8).
- Limitations stated by the authors and noticed by me: Authors: hybrid results are 'satisfactory'; the pure CF is hurt by small groups of poorly correlated users (PDF p.7). Noted by me: no ranking cut-off metric; the conclusion states the goal was scalability (PDF p.8).
- My reading (what it means for this thesis): The paper's own section 2.1 names the 'latency problem' for new items and the 'unusual user' with few ratings as CF weaknesses (PDF p.3), which are the new-item and few-ratings faces of cold start; the terms cold start and sparsity never occur.
- Claims I will reuse, each with a locator:
  - Collaborative filtering weaknesses named: latency problem for new items and unsuitability for an unusual user with few overlapping ratings - PDF p.3, section 2.1
  - Table 4: pure CF is more accurate than the hybrid on MAE, NDPM and F1 - PDF p.7
  - The hybrid's advantage is computation time - PDF p.8, sections 4-5

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

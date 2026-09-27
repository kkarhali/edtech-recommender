# chaudhary2019elearning - Chaudhary et al., 2019, E-Learning Recommender System for Learners: A Machine Learning based Approach

- opened_on: 2026-09-20   source: 10.33889/IJMEMS.2019.4.4-076   type: journal   verified: yes
- Access: access=full text (local PDF); journal PDF carries title, authors, volume, pages, DOI on every page
- Problem: Learners cannot find relevant learning pages by keyword search; predict relevant e-learning URLs.
- Method: Pre-processing phase (keyword collection, cleaning, tokenising, retained keywords per URL) and prediction phase with Random Forest, run in TensorFlow on GPU (PDF pp.4-7).
- Data and domain: Matrix of 0/1 keyword presence per URL; 70:30 split (PDF p.6). Number of URLs and keywords is not given in the text.
- Metrics and results (with the task each measures): Fig. 6 shows accuracy over five runs from 0.9357 to 0.9861 (PDF p.8); Fig. 7 the accuracy comparison, Random Forest 98.98 percent (PDF p.9).
- Limitations stated by the authors and noticed by me: Noted by me: no ranking metric, no recommendation task per learner, no learner data; comparators' provenance unclear; no significance test.
- My reading (what it means for this thesis): A web-mining classification result. The proposal's summary says the system gives personalised recommendations from learner preferences and activity, but the experiment predicts URLs from a keyword.
- Claims I will reuse, each with a locator:
  - Random Forest reaches 98.98 percent accuracy in the reported comparison - PDF p.9, Fig. 7
  - Accuracy is defined from TP, TN, FP, FN - PDF pp.8-9, section 5
  - The prediction task returns URLs for a keyword or URL query - PDF pp.4-6, section 3

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

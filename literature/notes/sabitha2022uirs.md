# sabitha2022uirs - Sabitha et al., 2022, User Interaction Based Recommender System Using Machine Learning

- opened_on: 2026-09-20   source: 10.32604/iasc.2022.018985   type: journal   verified: yes
- Access: access=full text (local PDF); Tech Science Press page opened (title, authors, vol. 31 no. 2, pp. 1037-1049, DOI matched). The knowledge base abbreviates the title to UI-RS
- Problem: Product recommendation in e-commerce from user interaction data gathered from several sources.
- Method: CBF similarity with TF-IDF weights, Dempster-Shafer integration of evidence sources, modified three-layer RBFNN (Gaussian hidden layer, softmax output) to produce the product list (PDF pp.6-8).
- Data and domain: Raw data of www.askboutique.com, 120 customer samples (PDF p.10).
- Metrics and results (with the task each measures): Compared with TARS and KRS on precision, recall, error rate and coverage in figures; mean error rate about 0.00755 (PDF p.10).
- Limitations stated by the authors and noticed by me: Noted by me: no train/test procedure is described, 120 samples, no numeric results table, no significance test. The paper lists CF constraints as data sparsity and cold start and hybrid filtering as the remedy (PDF p.3).
- My reading (what it means for this thesis): Keeps RBFNN in the review as a proposal keyword, but the evidence is small-scale and outside e-learning.
- Claims I will reuse, each with a locator:
  - The authors list collaborative filtering constraints as data sparsity and cold start - PDF p.3, section 1
  - Experiments use 120 customer samples from askboutique.com - PDF p.10, section 4
  - Average error rate about 0.00755 - PDF p.10

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

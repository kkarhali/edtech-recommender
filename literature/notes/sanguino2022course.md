# sanguino2022course - Sanguino Perez et al., 2022, A course hybrid recommender system for limited information scenarios

- opened_on: 2026-09-20   source: 10.5281/zenodo.7304829   type: journal   verified: yes
- Access: access=full text (open copy fetched 2026-09-20, not stored in the project) (Zenodo file 608SanguinoPerez162To188.pdf; running head reads Journal of Educational Data Mining, Volume 14, No 3, 2022, p.162). DOI is the Zenodo deposit DOI used by the journal; DataCite record checked; ERIC also lists the article
- Problem: Recommend courses on an online learning platform when user information is limited.
- Method: Rating estimation from session counts and temporal analysis of Google Analytics logs; rating penalty strategies; text embeddings for CBF (Abstract, PDF p.1).
- Data and domain: GCFGlobal platform (more than 360 courses, 6,400 lessons) (PDF p.2).
- Metrics and results (with the task each measures): Best model by P@5 was CF at 0.4, two of five recommended courses of interest; CBF strategies not significant but mitigate cold start and support a hybrid (Abstract).
- Limitations stated by the authors and noticed by me: Single platform; P@5.
- My reading (what it means for this thesis): A public-log-free but close analogue: session-derived implicit ratings, CF strongest single model, CBF as cold-start support.
- Claims I will reuse, each with a locator:
  - CF was the best model with P@5 = 0.4 on GCFGlobal logs - PDF p.1, abstract
  - Content-based strategies did not yield significant results but help mitigate cold start and validate a hybrid - PDF p.1, abstract

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

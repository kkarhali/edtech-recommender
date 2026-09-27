# liang2017profile - Liang et al., 2017, Online Behavior Analysis-Based Student Profile for Intelligent E-Learning

- opened_on: 2026-09-20   source: 10.1155/2017/9720396   type: journal   verified: yes
- Access: access=full text (local PDF); journal PDF front page carries title, authors, volume, article ID, DOI, dates
- Problem: Low MOOC completion; profile learners from behaviour to guide platform and learner.
- Method: Five age bands (Table 1), 12 preset behaviours (Table 2), duration slots; Jaccard-based similarity matrix (Algorithm 1) and rule labels such as depth-learning type above 60 minutes (PDF pp.2-4).
- Data and domain: Survey-style attitude statistics for 18-24 year-olds (Fig. 3) and course behaviour data for the DSAA course (Table 3, PDF pp.4-5).
- Metrics and results (with the task each measures): Table 4 (PDF p.6): LDA, LR, LSVM accuracy 99.6, 99.5, 99.7; precision 50.0, 65.0, 64.3; recall 88.9, 76.5, 81.8; F-score 64.0, 70.3, 72.0.
- Limitations stated by the authors and noticed by me: Authors give only the algorithm and labelling idea and do not repeat the labelling rules (PDF p.4). Noted by me: no recommender is built or evaluated; data source not named.
- My reading (what it means for this thesis): Duration is part of this profile; OULAD has no duration, only daily click sums, so the behavioural signal here is a reduced version.
- Claims I will reuse, each with a locator:
  - Profile inputs: age band, behaviour type and behaviour duration - PDF pp.2-3
  - Table 4 reports accuracy 99.6 and precision 50.0 for LDA in the same experiment - PDF p.6
  - The authors give only the Jaccard algorithm and the labelling idea - PDF p.4

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

# gao2022cnn - Gao et al., 2022, Online Course Recommendation Using Deep Convolutional Neural Network with Negative Sequenc

- opened_on: 2026-09-20   source: 10.1155/2022/9054149   type: journal   verified: yes
- Access: access=full text (local PDF); publisher page (Wiley) not reachable, HTTP 403; the PDF front page carries the Hindawi citation block, received/accepted/published dates and DOI
- Problem: MOOCs suffer low completion; personalised course recommendation that also warns about courses likely to be mis-selected.
- Method: Course-learning sequence turned into a negative sequence pattern from registration, completion degree and final grade; convolution and max-pooling over embedded windows (L=7, T=2, d=50 best); user embedding concatenated in a fully connected layer (PDF pp.3-6).
- Data and domain: Web-crawled CourseTalk usage of 500 learners with at least 20 courses; positive if completion is at least 50 percent and score above 5, otherwise negative; test users are 100 with truancy records (PDF pp.3, 5).
- Metrics and results (with the task each measures): Table 2 (PDF p.5); text: P@1 improved by 35 percent and 92 percent over the hybrid and ensemble baselines (PDF p.6).
- Limitations stated by the authors and noticed by me: Data available only on formal request (PDF p.6). Noted by me: two baselines only, no popularity or item-kNN baseline, no repeated runs or test; abstract claims lower dropout rate but the reported metrics are precision and recall for predicting truancy.
- My reading (what it means for this thesis): Shows a deep sequence model on e-learning enrolment data, but on a small non-public sample; supports listing CNN sequence work as future work rather than as a baseline here.
- Claims I will reuse, each with a locator:
  - Sample: 500 CourseTalk learners, 100 test users with truancy records, 400 for training - PDF pp.3, 5
  - Table 2 reports P@N and R@N against two baselines; best P@5 is 0.39 - PDF p.5
  - Data are shared only on reasonable request - PDF p.6, Data Availability

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

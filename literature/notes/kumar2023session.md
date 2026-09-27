# kumar2023session - Kumar et al., 2023, Session-Based Song Recommendation Using Recurrent Neural Network

- opened_on: 2026-09-20   source: 10.1007/978-981-99-0085-5_58   type: conference   verified: yes
- Access: access=full text of the ResearchGate 'Conference Paper March 2022' copy (13 PDF pages incl. cover); Springer landing page opened 2026-09-20 (Conference paper, LNEE vol. 997, 2023, pp. 719-728). Year 2022 on the on-disk copy, 2023 in the published record: cite 2023. Published Springer text not opened (paywall), so numbers are from the preprint copy. Proposal summary says a significant Precision boost: see note file.
- Problem: Predict the next song in an ongoing listening session (next-item, session-based recommendation) when user history is absent.
- Method: RNN with 20 layers, batch 16, learning rate 0.1, momentum 0.1, dropout 0.1, session-parallel mini-batches and BPR-max loss (PDF pp.6-7); framed as following Hidasi et al. (GRU4Rec).
- Data and domain: 30Music: 2,764,474 sessions, 31,351,954 events, 4,106,341 users, 210,633 items as printed in Table 1 (PDF p.8). Split: for every user the last session is the test set (PDF p.8).
- Metrics and results (with the task each measures): Precision@5/10/20: RNN 0.095/0.064/0.042; POP 0.003/0.003/0.002; IKNN 0.076/0.045/0.025; SKNN 0.041/0.028/0.015; V-SKNN 0.195/0.159/0.112. Recall@5/10/20: IKNN 0.380/0.454/0.506 vs RNN 0.073/0.087/0.100. MRR: IKNN highest (PDF pp.9-10).
- Limitations stated by the authors and noticed by me: Authors: SBRS ignores long-term preference; future work would combine short and long term (PDF p.10). Noted by me: text on PDF p.10 says RNN is better on precision at length 5 while Table 2 lists V-SKNN at 0.195 against RNN 0.095; no repeated runs or significance test.
- My reading (what it means for this thesis): Useful as the method lead for session sequences; not evidence for e-learning. The proposal's Arabic summary (a significant Precision boost over traditional systems) is only partly supported: RNN beats POP, IKNN and SKNN on precision but not V-SKNN.
- Claims I will reuse, each with a locator:
  - Test protocol: last session of every user held out - PDF p.8, section 4.2
  - Tables 2-4 report Precision, Recall, MRR at N=5, 10, 20 for POP, IKNN, SKNN, V-SKNN and RNN - PDF pp.9-10
  - The authors state that nearest-neighbour methods have proved highly competitive against modern neural methods, and that progress in session-based recommendation still seems limited - PDF p.5, section 2

Locator convention: 'PDF p.N' counts the pages of the file as opened (a ResearchGate cover page counts as page 1); 'Abstract' means the abstract on the publisher page or first page only.

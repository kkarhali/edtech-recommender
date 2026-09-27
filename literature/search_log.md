# Literature search log

Project: e_learning_thesis. Unit u05_s2_literature, cycle 0, mode draft. Date of all searches: 2026-09-20.

## Protocol

This block was written on 2026-09-20 before the first logged query. Three access probes preceded it (table "Access probes" below); they were run only to learn which databases answer at all, and none of the records they returned was screened or used.

- Research question (copied from plan.md, RQ0 main): Does a hybrid of content-based filtering, collaborative filtering and a behavioural engagement signal produce more accurate and more robust top-K e-learning recommendations than either alone, and on cold-start learners? Sub-questions: RQ1 which observable VLE behaviours carry recommendation signal; RQ2 whether segmenting learners by behavioural profile improves the cold-start prior; RQ3 whether a validation-fitted blend weight closes the warm-user gap to pure collaborative filtering; RQ4 whether the hybrid's advantage survives significance testing across 22 module-presentations under a time-based split and a genuine new-learner condition.
- Concept blocks (each research question maps to at least two): C1 e-learning/MOOC; C2 recommender system; C3 learner behaviour/clickstream/profiling; C4 technique (CF, CBF, hybrid, context-aware); C5 cold start/sparsity; C6 sequence and neural models (session-based, RNN, CNN, RBFNN); C7 offline evaluation and statistical inference. Mapping: RQ0 = C1,C2,C4,C5; RQ1 = C1,C3; RQ2 = C3,C5; RQ3 = C2,C4; RQ4 = C1,C5,C7.
- Sources and access level actually available on 2026-09-20 (no institutional or paid subscription was available to this agent):
  - OpenAlex API (open; indexes Crossref, PubMed, arXiv and publisher metadata; used as the primary search engine and for citation links). Access: open.
  - Crossref REST API (open; used for metadata verification by DOI and for bibliographic queries). Access: open.
  - ERIC API (open; education research). Access: open.
  - DOAJ API (open; open-access journals). Access: open.
  - arXiv API (open; preprints, labelled as preprints). Access: open.
  - Semantic Scholar Graph API (open but rate-limited; used for forward citations only where it answered). Access: open, rate-limited.
  - Publisher pages reached through DOI resolution (Springer, IEEE Xplore, Wiley, Tech Science Press, SciTePress, ACM): open only where they answer; each failure is logged in "Sources that could not be opened".
  - Google Scholar, Scopus, Web of Science, IEEE Xplore search, ACM DL search, ScienceDirect search: NOT available (see Access probes). The protocol therefore does not claim them.
- Years covered: no lower bound for the nine proposal papers and for foundations reached by backward snowballing; for new search hits, publication year 2021 to 2026 (the last five years counted from 2026-09-20) so that every theme carries current peer-reviewed work. Foundational older works are admitted only through snowballing or when they define a method or metric the thesis uses.
- Languages: English and Arabic. Arabic-language query rounds are run on Crossref and DOAJ (the two sources that index Arabic-language journals); results are logged even when empty.
- Inclusion criteria: peer-reviewed work on recommender systems in learning contexts; recommender methods (hybrid, CF, CBF, sequence models) in any domain when the method is the reason to include it; learner behaviour analytics and student profiling; offline evaluation and statistical-inference methodology for recommenders; the OULAD data descriptor. Preprints only when they are the primary source for a method used in the thesis, labelled as preprints.
- Exclusion criteria: E1 no method and no evaluation; E2 not about recommendation, learner behaviour, or evaluation methodology (off-topic); E3 trade press or editorial (kept in a separate context list, never in the comparison table); E4 duplicate of the same study; E5 cannot be opened (logged, not cited); E6 short abstract-only items without a full text; E7 dropout or performance prediction with no recommendation or profiling angle relevant to RQ1 or RQ2.
- Screening: two passes, title and abstract first, then full text (or the open full text where reachable; otherwise the item is logged as unreachable at full-text level and is not cited).
- Retrieval rule: for each logged query the top 25 records by the source's relevance ranking are retrieved and screened; "Hits" is the database's own total, "Retrieved" is what was screened. The PRISMA-style counts below use Retrieved, and this is a stated limitation: the review is PRISMA-style lite, not a registered systematic review.
- Snowballing: backward from the reference lists of the nine core papers (screened by title against the criteria), forward through OpenAlex "cites" links (and Semantic Scholar where it answers). Stop when a round adds nothing that passes screening.
- Protocol written on: 2026-09-20 by: literature-scholar, unit u05_s2_literature, cycle 0.

## Access probes and blocked sources

Run on 2026-09-20 (curl and WebFetch from this machine, no credentials, no institutional proxy). The first three probes preceded the protocol block above and only decided which sources to name in it. No attempt was made to bypass a challenge page or a robots block; a source that refused is listed as refused.

| Source | What was tried | Result | Decision |
| --- | --- | --- | --- |
| Google Scholar | scholar.google.com search URL via curl | HTTP 302 to google.com/sorry (automated-query challenge) | Not used; no forward citation counts from it |
| Scopus | Elsevier search API without a key | HTTP 403 | Not available; not claimed |
| Web of Science | Not attempted (no subscription known) | n/a | Not available; not claimed |
| IEEE Xplore | /rest/search; article pages via curl and WebFetch | search HTTP 405; article pages HTTP 202 with an empty body, WebFetch returned no content | Search not usable; IEEE items reached only through local PDFs or DOI registry records |
| ACM Digital Library | search and article pages via curl and WebFetch, repeated 2026-09-21 | HTTP 403 Cloudflare 'Just a moment' challenge every time | Refused; ACM items reached only through open PDF copies where they exist |
| ScienceDirect | search page; article pages via doi.org | search HTTP 403; article pages return a 2.7 kB interstitial with no metadata | Refused |
| MDPI | WebFetch (3 article pages), curl on article, HTML and PDF URLs, repeated 2026-09-21 | HTTP 403 every time | Refused |
| Hindawi / Wiley | downloads.hindawi.com PDF, onlinelibrary.wiley.com pages | HTTP 403 | Refused; the three Hindawi core papers are read from the local PDFs |
| SpringerLink | article pages via curl | HTTP 303 to an identity handshake, then HTTP 200 once the cookie was accepted | Landing pages readable (metadata and abstract); full texts paywalled |
| arXiv API | urllib requests, four attempts over two runs | HTTP 406 Not Acceptable | Answered when called through curl with a browser-style agent string; used for two queries and for open preprint copies |
| Semantic Scholar API | one probe on 2026-09-20, retried 2026-09-21 00:00 | first HTTP 429 (rate limit), retry HTTP 200 | Used only for the forward-citation cross-check |
| OpenAlex, Crossref, ERIC, DOAJ, DataCite | API calls | HTTP 200 | Used |

## Queries

Discovery queries. Hits is the source's own total; Retrieved is the number of records screened (top 25 by relevance, fewer when the source had fewer). OpenAlex queries were run as `title_and_abstract.search:<string>` with `from_publication_date:2021-01-01`, sorted by relevance_score. All on 2026-09-20.

| Query id | Date | Source | Exact query string | Hits | Retrieved | Included | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q01 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("e-learning" OR MOOC OR "online learning") AND ("recommender system" OR "recommendation system") AND ("cold start" OR "new user")` | 118 | 25 | 3 | concept pairs C1+C2+C5 |
| Q02 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("learner behavior" OR "learner behaviour" OR clickstream OR "interaction log") AND ("recommender system" OR "recommendation system") AND (hybrid OR "collaborative filtering")` | 67 | 25 | 0 | C3+C2+C4 |
| Q03 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("session-based" OR sequential) AND recommendation AND (RNN OR LSTM OR GRU OR transformer) AND (course OR MOOC OR learning)` | 742 | 25 | 0 | C6+C2+C1; mostly general sequential-recommendation papers |
| Q04 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("learning analytics" OR OULAD OR "Open University Learning Analytics") AND (recommendation OR recommender)` | 1217 | 25 | 0 | C1/C3 with recommendation; largely learning-analytics dashboards |
| Q05 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("offline evaluation" OR "evaluation protocol" OR "data splitting" OR "data leakage") AND ("recommender system" OR "recommendation") AND (bias OR "sampled metrics" OR reproducibility OR "time-based")` | 316 | 25 | 1 | C7; loose boolean parsing returned bias and fairness papers |
| Q06 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("student profile" OR "learner profile" OR "student profiling") AND (clustering OR segmentation) AND (recommendation OR recommender)` | 82 | 25 | 0 | C3 profiling with clustering |
| Q07 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("hybrid recommender" OR "hybrid recommendation") AND ("content-based" OR "collaborative filtering") AND (e-learning OR education OR course)` | 216 | 25 | 2 | C4 hybrid in education |
| Q08 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("context-aware" OR "context aware") AND (recommender OR recommendation) AND (learning OR education)` | 1588 | 25 | 0 | context-aware (proposal keyword); mostly non-education domains |
| Q09 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("statistical significance" OR "statistical inference" OR "significance test" OR "significance testing") AND ("recommender system" OR "recommendation") AND (evaluation OR experiment)` | 1741 | 25 | 1 | C7 statistics; the source's boolean matching is loose, most hits are non-recommender fields; two relevant records at ranks 1 and 2 |
| Q10 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("radial basis function" OR RBFNN) AND (recommendation OR recommender)` | 284 | 25 | 1 | RBFNN (proposal keyword); mostly engineering uses of RBF networks |
| Q11 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("cold start" OR "cold-start") AND "recommender system" AND (survey OR review OR "systematic literature review")` | 311 | 25 | 2 | C5 reviews |
| Q12 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) ("educational recommender" OR "course recommendation" OR "learning resource recommendation") AND (survey OR review)` | 208 | 25 | 3 | educational recommender reviews |
| Q13 | 2026-09-20 | OpenAlex | `(title_and_abstract.search) OULAD OR "Open University Learning Analytics Dataset"` | 640 | 25 | 1 | OULAD; many hits are place names (Oulad = Moroccan localities), screened out as off-topic |
| Q14 | 2026-09-20 | ERIC | `("recommender system" OR "recommendation system") AND (MOOC OR "e-learning" OR "online learning") AND ("cold start" OR sparsity OR clickstream)` | 4 | 4 | 0 | ERIC, no year filter; 4 hits |
| Q15 | 2026-09-20 | ERIC | `("learning analytics" OR clickstream OR "student behavior") AND (recommender OR recommendation) AND (hybrid OR "collaborative filtering")` | 9 | 9 | 0 | ERIC, no year filter; 9 hits |
| Q16 | 2026-09-20 | DOAJ | `recommender AND (e-learning OR MOOC) AND ("cold start" OR hybrid)` | 62 | 25 | 0 | DOAJ, no year filter |
| Q17 | 2026-09-20 | arXiv | `all:"recommender" AND (all:MOOC OR all:"e-learning" OR all:"online learning") AND all:"cold start"` | 9 | 9 | 0 | arXiv; first two attempts HTTP 406, answered through curl on retry |
| Q18 | 2026-09-20 | arXiv | `all:"session-based" AND all:recommendation AND (all:course OR all:education OR all:learning)` | 172 | 25 | 0 | arXiv; first two attempts HTTP 406, answered through curl on retry |
| Q19 | 2026-09-20 | Crossref | `نظام توصية للتعليم الإلكتروني` | 6210 | 25 | 0 | Arabic string; Crossref bibliographic search, from 2021; results are general Arabic e-learning articles; one recommender-related Arabic record could not be opened |
| Q20 | 2026-09-20 | Crossref | `أنظمة التوصية سلوك المتعلم التعلم الإلكتروني` | 18107 | 25 | 0 | Arabic string; Crossref, from 2015; no recommender-system articles in the top 25 |
| Q21 | 2026-09-20 | DOAJ | `توصية AND (التعليم الإلكتروني OR التعلم عن بعد)` | 0 | 0 | 0 | Arabic string on DOAJ; 0 hits |

Known-item and citation-verification lookups (Crossref bibliographic search, 2026-09-20). These test a lead that came from the knowledge base, the skill's methods list, a core paper's reference list or the field's standard sources; they are not discovery searches and are not counted in the screening totals.

| Query id | Lead | Hits (Crossref total, loose match) | Outcome |
| --- | --- | --- | --- |
| K01 | `Statistical Inference: The Missing Piece of RecSys Experiment Reliability Discourse` | 1,429,794 | Not found: no matching record among the top 4; not pursued and not cited |
| K02 | `A Critical Study on Data Leakage in Recommender System Offline Evaluation` | 15,500,619 | Found: 10.1145/3569930 (ji2023leakage; arXiv copy opened) |
| K03 | `A Troubling Analysis of Reproducibility and Progress in Recommender Systems Research` | 20,104,888 | Found: 10.1145/3434185 (ferrari2021troubling; arXiv copy opened) |
| K04 | `A Survey on Session-based Recommender Systems Wang Cao Wang` | 16,284,932 | Found: 10.1145/3465401 (wang2021session; arXiv v3 copy opened) |
| K05 | `Open University Learning Analytics dataset Kuzilek Hlosta Zdrahal` | 7,037,361 | Found: 10.1038/sdata.2017.171 (kuzilek2017oulad) |
| K06 | `The PRISMA 2020 statement: an updated guideline for reporting systematic reviews` | 10,319,230 | Not found by this string; resolved by direct DOI lookup 10.1136/bmj.n71 (page2021prisma) |
| K07 | `Guidelines for snowballing in systematic literature studies and a replication in software engineering Wohlin` | 12,385,323 | Found: 10.1145/2601248.2601268 (wohlin2014snowballing) |
| K08 | `Analyzing the past to prepare for the future: writing a literature review Webster Watson` | 9,811,162 | Found: 10.2307/4132319 (webster2002review) |
| K09 | `Hybrid Recommender Systems: Survey and Experiments Burke` | 6,199,458 | Found: 10.1023/a:1021240730564 (burke2002hybrid; backward snowball) |
| K10 | `Toward the next generation of recommender systems: a survey of the state-of-the-art and possible extensions Adomavicius Tuzhilin` | 425,584 | Found: 10.1109/tkde.2005.99 (Adomavicius and Tuzhilin 2005); could not be opened, see unreachable table; not in the ledger |
| K11 | `Item-based collaborative filtering recommendation algorithms Sarwar Karypis Konstan Riedl` | 124,222 | Found: 10.1145/371920.372071 (sarwar2001itembased; backward snowball) |
| K12 | `Session-based recommendations with recurrent neural networks Hidasi` | 8,619,133 | Not in Crossref under this title (only later Hidasi papers); resolved through arXiv 1511.06939 (hidasi2016gru4rec; backward snowball) |
| K13 | `Supporting People with Autism Spectrum Disorders in the Exploration of PoIs: An Inclusive Recommender System Mauro Ardissono Cena` | 157,206 | Found: 10.1145/3505267 (mauro2022autism); could not be opened |

## Screening counts

Pass 1 (title and abstract) was assisted by a written keyword rule: a record counted as on-topic only if its title and abstract matched recommender terms together with learning-context, evaluation, sequence, cold-start or profiling terms. Records the rule marked off-topic were not re-read one by one; every record that passed the rule and every included or unreachable candidate was read by title and abstract. The full decision list, one row per unique record with its reason, is `literature/screening_records.csv`. This is PRISMA-style lite (Page et al. 2021, `page2021prisma`); it is not a registered systematic review and the stopping rule (top 25 per query) means that lower-ranked hits were not screened.

```text
identified_total        = 447   (records retrieved and screened across Q01-Q21; database totals are in the Hits column)
duplicates_removed      = 9
screened_title_abstract = 438
excluded_title_abstract = 413   reasons: E2 off-topic 159; E8a on-topic e-learning recommender or profiling record, eligible but not selected 88; E8b on-topic general recommender-methods or evaluation record, eligible but not selected 81; E3 not a peer-reviewed paper (preprint, report, dataset, deposit) 49; outside the 2021-2026 window 18; E7 OULAD prediction with no recommendation or profiling angle 17; retracted 1
full_text_assessed      = 25   (13 included + 11 not retrievable + 1 excluded after opening)
excluded_full_text      = 1    reasons: E1 no method or evaluation stated (Javed et al. 2021, iJET, publisher page opened)
not_retrievable         = 11   search-stream items whose publisher page and full text were refused or paywalled; not cited
sources_unreachable     = 14   = not_retrievable 11 + Furini 2022 + Mauro 2022 + Adomavicius and Tuzhilin 2005 (reconciliation under the unreachable table)
included_from_search    = 13
included_from_snowball  = 4    (3 backward: Burke 2002, Sarwar 2001, Hidasi 2016; 1 forward: Hamim 2021)
included_from_leads     = 7    (known-item lookups and methods sources: Ji 2023, Ferrari Dacrema 2021, Wang 2021, Kuzilek 2017, Page 2021, Wohlin 2014, Webster and Watson 2002)
supplied_by_proposal_or_knowledge_base = 15   (the nine reviewed papers, Furini 2022, Mauro 2022 and four trade-press items)
included_total          = 39   equals the row count of literature/ledger.csv
```

Check: 13 + 4 + 7 + 15 = 39. Of the 39 rows, 37 are verified (opened) and 2 (Furini 2022, Mauro 2022) are kept as unreachable, unverified rows and are not relied on. Four rows are trade press (type=trade, peer_reviewed=no) and are excluded from the related-work table.

Peer-review status was inferred from venue type (journal, or conference proceedings indexed by the publisher); each venue's editorial policy was not opened. Preprint copies (arXiv) were used to read three published articles and one survey; the published versions were not opened and each ledger row says so.

## Snowball rounds

| Round | Direction | Seed keys | Candidates | Included | Stopped because |
| --- | --- | --- | --- | --- | --- |
| 1 | backward | the nine core papers; reference lists hold 241 entries (21, 41, 29, 39, 17, 20, 15, 43, 16 for kumar, gao, sabitha, huang, chaudhary, liang, ansari, zhang, degemmis) | The lists were screened for works the thesis's methods rest on rather than title by title in full (full lists read for chaudhary, ansari, degemmis; the others by targeted extraction). 4 candidates flagged: Burke 2002 (cited by three core papers), Sarwar 2001, Hidasi 2016, Adomavicius and Tuzhilin 2005 | 3 (Burke, Sarwar, Hidasi); Adomavicius could not be opened | A second backward step from these three was not run: they are foundations, and the recent-work requirement is met by forward search |
| 2 | forward citation, OpenAlex (`cites:` filter, from 2021, top 15 by citations per paper) | the nine core papers | 151 citing records since 2021 in total (C01 3; C02 16; C03 9; C04 2; C05 17; C06 51; C07 30; C08 23; C09 0); 89 screened | 1 (Hamim 2021, from liang2017profile; Souabi 2021 was already found by Q07 and is also cited by three core papers) | The other titles were general recommender or learning-analytics items already covered by an included work |
| 3 | forward citation cross-check, Semantic Scholar (2026-09-21 00:00) | the nine core papers | 178 records returned, 119 since 2021 (kumar not indexed, HTTP 404; degemmis 2 since 2021) | 0 | Nothing new that passes screening: the e-learning items returned were reviews of the kind already included (Souabi 2021, Liu 2022, da Silva 2023) or general profiling and prediction studies. Stopped: a full round added nothing |

## Sources that could not be opened

None is cited or summarised. Times are local; each was tried at least twice.

**Reconciliation of the counts (single statement).** The table below has 15 rows. `sources_unreachable` = 14 is the counter cited in the handoff, in chapter 2 section 2.8 and in `open_questions.md`; it counts source items that could not be opened and excludes the wired.com row, because no Wired item was ever selected. Of the 14, 11 entered through the search stream and are the `not_retrievable = 11` line in the screening counts (10 candidates that reached full-text assessment and the Arabic-language article; `screening_records.csv` shows 11 `full_text_not_retrieved`), and 3 did not enter through the search stream: `furini2022twins` and `mauro2022autism` (knowledge-base items, kept in the ledger as verified=no) and Adomavicius and Tuzhilin 2005 (a backward-snowball candidate). So 15 rows - 1 (wired.com) = 14 = 11 + 3.

| Date tried | Source | What was tried | Error or barrier | Decision |
| --- | --- | --- | --- | --- |
| 2026-09-20 22:59:50; 2026-09-21 00:03:51 and 00:04:14 | furini2022twins (Furini et al. 2022, CACM, doi 10.1145/3478281) | curl on dl.acm.org (three times) and the two OpenAlex PDF URLs | HTTP 403 Cloudflare challenge on the landing page; the PDF URLs returned no PDF | Kept in the ledger as verified=no, unreachable; metadata match the Crossref record only |
| 2026-09-20 22:59:44 to 22:59:47; 2026-09-21 00:08:54 to 00:09:10 | mauro2022autism (Mauro et al. 2022, CACM, doi 10.1145/3505267) | cacm.acm.org via WebFetch and curl, dl.acm.org and doi.org via curl | HTTP 403 on every try | Kept in the ledger as verified=no, unreachable |
| 2026-09-20 and 2026-09-21 | Adomavicius and Tuzhilin 2005 (IEEE TKDE, doi 10.1109/tkde.2005.99), backward snowball candidate | ieeexplore.ieee.org document page and two PDF URLs | HTTP 202 empty body / no PDF | Not in the ledger; not cited |
| 2026-09-20 and 2026-09-21 | Uddin et al. 2021, MOOC recommender systems mapping review, IEEE Access, doi 10.1109/access.2021.3101039 | Xplore page; the OpenAlex PDF was fetched (7.9 MB) but has no text layer (pdftotext returned 0 characters) | HTTP 202 empty; PDF unreadable | Not in the ledger; not cited |
| 2026-09-20 and 2026-09-21 | Bhaskaran et al. 2021, cluster-based hybrid e-learning recommender, Mathematics, doi 10.3390/math9020197 | MDPI page (WebFetch, curl), PDF | HTTP 403 | Not in the ledger |
| 2026-09-20 and 2026-09-21 | Wu et al. 2023, hybrid MOOC recommendation with dynamic preferences, Applied Sciences, doi 10.3390/app13095548 | MDPI page (WebFetch), PDF | HTTP 403 | Not in the ledger |
| 2026-09-20 and 2026-09-21 | Liu et al. 2022, student performance from clickstream data (OULAD-type features), Education Sciences, doi 10.3390/educsci13010017 | MDPI page (WebFetch), PDF | HTTP 403 | Not in the ledger |
| 2026-09-20 and 2026-09-21 | Zhang et al. 2023, e-learning behaviour categories on OULAD, Sustainability, doi 10.3390/su15108235 | MDPI page (curl x2), PDF | HTTP 403 | Not in the ledger; RQ1 is supported by qiu2022behaviour and kuzilek2017oulad instead |
| 2026-09-20 and 2026-09-21 | Latifi et al. 2022, sequential recommendation, transformers vs nearest neighbours, Information Sciences, doi 10.1016/j.ins.2022.07.079 | doi.org, ScienceDirect PDF URL; arXiv title search | 2.7 kB interstitial with no metadata; no arXiv copy found | Not in the ledger |
| 2026-09-20 and 2026-09-21 | Zhao et al. 2022, appropriate offline evaluation for top-N recommendation, ACM TOIS, doi 10.1145/3545796 | dl.acm.org; arXiv title search | HTTP 403; no arXiv copy found | Not in the ledger; ji2023leakage and castells2022offline cover the same methodological ground |
| 2026-09-20 and 2026-09-21 | Urbano et al. 2021, metric score distributions and Type I error, ACM ICTIR, doi 10.1145/3471158.3472242 | dl.acm.org, TU Delft repository resolver | HTTP 403; repository resolver returned no PDF | Not in the ledger; ihemelandu2023inference covers significance testing |
| 2026-09-20 and 2026-09-21 | Alhakbani et al. 2022, OULAD benchmark studies review, ACM proceedings, doi 10.1145/3529399.3529413 | dl.acm.org | HTTP 403 | Not in the ledger |
| 2026-09-20 and 2026-09-21 | Lin et al. 2022, context-aware reinforcement learning for course recommendation, Applied Soft Computing, doi 10.1016/j.asoc.2022.109189 | doi.org, ScienceDirect | 2.7 kB interstitial with no metadata | Not in the ledger; context-aware recommendation is therefore thinly sourced, see chapter 2 |
| 2026-09-20 | Arabic-language article 2026, intelligent recommendation system based on learning analytics, International Journal of E-Learning, doi 10.21608/ijel.2026.498278 | doi.org then ijel.journals.ekb.eg | 302 redirect chain ending in an empty response, two tries | Not in the ledger; the Arabic-language part of the search therefore contributes no cited source |
| 2026-09-20 | wired.com (knowledge base item, no Wired article was ever selected) | Not re-tried; the knowledge base already records that wired.com is unreachable by the search tools | n/a | Nothing is attributed to Wired |

## Metadata discrepancies found while opening the sources

| Item | Knowledge base or proposal says | Opened source says | Handling |
| --- | --- | --- | --- |
| kumar2023session | 2023, Springer chapter; the proposal's Arabic summary says a significant Precision boost | The on-disk file is the ResearchGate March 2022 conference-paper copy; its Tables 2-4 show V-SKNN above RNN on Precision | Cite 2023; state the table result; published Springer text not opened |
| sabitha2022uirs | Title given as UI-RS | Title is User Interaction Based Recommender System Using Machine Learning; UI-RS is the model name | Title corrected in the ledger |
| huang2019amre | Outperforms on precision, recall and F1 (knowledge base and proposal) | Best on Accuracy, Recall and F1; lower on Precision | Ledger and chapter follow the paper |
| chaudhary2019elearning | Proposal: personalised recommendations from learner preferences and activity | The experiment predicts URLs from a keyword; no learner data | Comparability note and chapter follow the paper |
| zhang2015hybrid | Better recall and diversity than non-hybrid baselines | Comparison is against a random recommender; diversity about equal or lower | Ledger and chapter follow the paper |
| degemmis2004hybrid | No year, no DOI; addresses cold start, sparsity, new-item problems | Year 2004 (PDF footer, SciTePress page), DOI 10.5220/0002638201620169; the text never says cold start or sparsity (it names a latency problem for new items and the unusual user); the hybrid is less accurate than pure CF and faster | Year and DOI filled from the PDF and the publisher page, not from memory; Crossref lists no authors for this DOI and a different container title, treated as a registry error |
| gao2022cnn | Lower course dropout vs baselines | The abstract says so; the experiments score truancy prediction, not dropout | Noted in the comparability column |
| Panda and Ray 2022 | (my working memory said Panda and Ramesh) | Springer page: Panda, Deepak Kumar; Ray, Sanjog | Ledger follows the page: a name filled from memory would have been wrong |

## Open questions for the human

| Question | Why it blocks or changes the work | Asked on | Answer |
| --- | --- | --- | --- |
| Citation style and thesis language rules | The reference list cannot be finalised and chapter 2 is drafted in English with an Arabic glossary until told otherwise | 2026-09-20 | open |
| Which search databases are licensed for this candidate | Scopus, Web of Science, IEEE Xplore, ACM DL and ScienceDirect were unavailable to this agent; a licensed session could open the 14 unreachable items and re-run the strings | 2026-09-20 | open |
| Are the proposal's nine papers fixed in the review | The nine are kept unchanged; several proposal summaries differ from the papers (see discrepancies above) and the supervisor should confirm wording | 2026-09-20 | open |
| How is AI assistance disclosed | Required by the standards' front-matter row; nothing is asserted here | 2026-09-20 | open |
| The OULAD licence | The data descriptor states CC-BY 4.0 (kuzilek2017oulad, PDF p.1). The licence was unverified when this log was written and plan.md recorded it as such; it has since been verified as CC BY 4.0 by the Methodologist at stage S3 (chapter 3 section 3.2; methodology/data_statement.md section 2). Residual gap named there: the local oulad.zip archive is not traced to the authors' deposit | 2026-09-20 | verified at S3 by the Methodologist (2026-09-21); provenance gap of the local archive open |

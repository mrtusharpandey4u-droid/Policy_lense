# PolicyLens Retrieval Evaluation — Milestone 2B.16

## Evaluation setup

The evaluator, `src/evaluate_retrieval.py`, read
`data/evaluation/evaluation_questions.jsonl` and used the existing
`src.search.retrieve` implementation against each persistent Qdrant collection.
All 25 queries were searched in both strategies, producing 50 query evaluations
at top 10. Exactly 25 query vectors were generated and each was reused for its
two strategy searches. No metadata filters were applied.

Query embeddings used the existing local BGE-M3 model, revision
`5617a9f61b028005a4858fdac845db406aefb181`, and the existing normalized
1,024-dimensional MPS query encoding behavior. One normalized vector was
generated per question and reused for that question in both strategy searches.
Results were judged relevant only
when both `doc_id` matched a gold reference and a result page overlapped its
1-based PDF `gold_pages`. Payload `page_provenance` was preferred; inclusive
`page_start`/`page_end` was the fallback. Printed page numbers and zero-based
PDF indices were not used for Qdrant matching.

## Overall metrics

Recall is question-level hit rate among 25 questions; MRR is the mean
reciprocal rank of the first relevant result, with zero when none appears in
the top 10.

| Metric | Fixed-size | Structure-aware |
|---|---:|---:|
| Recall@3 | 0.80 (80%) | 0.68 (68%) |
| Recall@5 | 0.92 (92%) | 0.84 (84%) |
| Recall@10 | 0.96 (96%) | 0.96 (96%) |
| MRR | 0.6117 (61.17%) | 0.5774 (57.74%) |

## Category-level performance

| Category | Strategy | Questions | Recall@3 | Recall@5 | Recall@10 | MRR |
|---|---|---:|---:|---:|---:|---:|
| Standard | Fixed-size | 15 | 0.7333 (73.33%) | 0.8667 (86.67%) | 0.9333 (93.33%) | 0.5473 (54.73%) |
| Standard | Structure-aware | 15 | 0.5333 (53.33%) | 0.7333 (73.33%) | 0.9333 (93.33%) | 0.4679 (46.79%) |
| Table-value | Fixed-size | 5 | 1.00 (100%) | 1.00 (100%) | 1.00 (100%) | 0.8667 (86.67%) |
| Table-value | Structure-aware | 5 | 1.00 (100%) | 1.00 (100%) | 1.00 (100%) | 0.7333 (73.33%) |
| Paraphrased | Fixed-size | 5 | 0.80 (80%) | 1.00 (100%) | 1.00 (100%) | 0.5500 (55.00%) |
| Paraphrased | Structure-aware | 5 | 0.80 (80%) | 1.00 (100%) | 1.00 (100%) | 0.7500 (75.00%) |

## Question-level comparison

At top 10:

- Retrieved by both strategies: Q001–Q009 and Q011–Q025 (**24 questions**).
- Fixed-size only: **none**.
- Structure-aware only: **none**.
- Missed by both: **Q010**.

First relevant results in ranks 6–10:

- Fixed-size: Q003 at rank 7.
- Structure-aware: Q004 at rank 7, Q005 at rank 6, and Q011 at rank 8.

Other first-relevant ranks and the full top-10 ranked candidates are preserved
in the machine-readable output files.

## Error analysis

- **Q010, missed by both:** The gold page is Shriram Finance's application
  processing provision, which states “approach for gradation of risks” and
  disclosure of the rationale for different rates. The query asks how the
  lender “grades borrower risk.” Neither top-10 list contains doc_016 page 2.
  Instead, top results include other Fair Practice Code passages and interest
  rate material (for example doc_016 pages 1 and 6–7 and doc_003 interest
  provisions). This is consistent with related-topic passages outranking the
  exact provision and a wording variation around “gradation”; it does not prove
  a single cause.
- **Q003, fixed-size rank 7 / structure-aware rank 4:** The gold is the
  vernacular-language communication rule on doc_001 page 4. The fixed-size
  relevant chunk spans pages 3–4 and appears at rank 7, while the
  structure-aware chunk for the loan-application section appears at rank 4.
  Competing Fair Practice Code passages rank above it in both lists.
- **Q004, fixed-size rank 1 / structure-aware rank 7:** The fixed-size top
  result spans doc_001 pages 1–4 and overlaps the gold page; the
  structure-aware top result spans pages 1–3 and therefore does not. Its
  first page-overlapping result is rank 7. The result payloads support a
  chunk-boundary/page-coverage difference, rather than a score-only relevance
  judgment.
- **Q005, fixed-size rank 5 / structure-aware rank 6:** The relevant
  doc_001 pages 4–5 result is rank 5 and 6, respectively. Higher-ranked
  results include other policies' penal-charge or lending passages, which
  share the topic but not the gold document/page.
- **Q011, fixed-size rank 5 / structure-aware rank 8:** The gold board
  responsibility provision is on doc_016 page 5. Earlier results include
  nearby Shriram Finance Fair Practice Code passages on other pages and other
  lenders' related provisions; they match the general policy topic but fail
  the required page-level gold match.

The five table-value questions all have a relevant result within the top 3 in
both strategies. No relevance decision used similarity score alone.

## Interpretation and limitations

Fixed-size performed better on overall Recall@3, Recall@5, and MRR, and tied
structure-aware on Recall@10. Its standard-question and table-value MRRs were
also higher. Structure-aware had higher MRR on the five paraphrased questions,
while both strategies had the same recall at each cutoff for that category.
The results do not establish a universal winner; they are descriptive results
from only 25 questions and should not be interpreted as statistically
significant.

The measured metrics use one verified gold document/page reference per
question, with a binary question-level hit definition. Multiple relevant
chunks from one page do not add extra recall credit. Evaluation reflects the
retrieval results and gold references available in this corpus and dataset;
it does not evaluate answer correctness or answer generation.

## Validation and artifacts

The run produced exactly 50 records: one fixed-size and one structure-aware
result for each of the same 25 question IDs. The independently recalculated
summary matched the detailed result records.

- Results JSON: `data/evaluation/results/retrieval_evaluation_results.json`
- Per-question CSV: `data/evaluation/results/retrieval_evaluation_question_results.csv`
- Evaluator: `src/evaluate_retrieval.py`
- Evaluator tests: `tests/test_evaluate_retrieval.py`

The evaluation queried the existing collections and did not rebuild, upsert,
or otherwise modify Qdrant. It did not modify source PDFs, manifest, chunks, or
embeddings.

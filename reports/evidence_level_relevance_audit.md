# PolicyLens — Evidence-Level Relevance Audit (Milestone 2B.18)

## Executive summary

The existing page-overlap rule is too permissive to establish that a retrieved
chunk contains answer evidence. In the official top 10, the independent
chunk-text audit found 24 DIRECT chunks for each strategy, but these came from
22 fixed-size questions and 21 structure-aware questions. Three questions
(Q001, Q005, Q010) had no DIRECT chunk in either strategy's top 10. The
separate top-20 diagnostic finds Q005 evidence at ranks 19 and 17 (fixed-size
and structure-aware), and Q010 evidence at rank 18 for structure-aware only.

The clearest page-overlap false positive is Q004 fixed-size rank 1: the chunk
spans the cited PDF page and was counted as relevant by the current evaluator,
but does not state the sanction information asked for. Its first DIRECT result
is rank 4. For Q005, page-overlapping rank-5/rank-6 chunks are only PARTIAL;
the chunk containing the exact bold-in-the-loan-agreement instruction is much
lower. For Q010, the source and page are correct, but the evidence is ranked
18th by structure-aware and is absent from fixed-size's top 20.

These are evidence-audit labels, not a replacement benchmark or a recalculation
of official 2B.16 metrics. They were assigned from curated, question-specific
answer components in the retrieved chunk text and table payloads, with
question/source checks for the priority cases. Phrase-based labeling can miss
valid paraphrases and is not a substitute for independent double annotation.
No retrieval, evaluation, source, or production data was changed.

## Existing page-overlap evaluation

`src/evaluate_retrieval.py` defines a hit as a retrieved result whose `doc_id`
matches a gold reference and whose PDF page provenance overlaps a gold PDF
page. If per-page provenance is unavailable, the evaluator falls back to
whether the gold page lies inclusively between `page_start` and `page_end`.
This verifies source/page association, not whether the chunk includes the
answer. A chunk covering several pages can therefore count as a hit when its
text does not contain the cited evidence.

All 25 questions, their gold source/page references, the persisted 2B.16
rankings, both chunk sets, the 2B.17 top-20 diagnostic, and the applicable
original PDF pages and cleaned/table evidence were examined. Gold page values
are PDF-page numbers; printed page labels were not substituted. Table evidence
was checked in its structured representation where it was not present in
cleaned prose. In particular, Q020's 2023–24 value is on PDF page 41 (printed
page 16).

## Evidence-label method

The supporting CSV records all official top-10 results (25 questions × 2
strategies × 10 ranks), plus ranks 11–20 for the five questions in the existing
diagnostic (Q003, Q004, Q005, Q010, Q011): 600 rows total.

- **DIRECT** — the chunk text/table payload contains all curated answer
  components needed for the question, in the cited gold document.
- **PARTIAL** — it contains some required answer evidence but is not sufficient
  alone to answer the question.
- **CONTEXT** — it is on-topic but does not contain the required answer
  evidence.
- **IRRELEVANT** — it does not meaningfully support the question.

These are chunk-level classifications. Separate chunks were not combined to
upgrade PARTIAL chunks to DIRECT. Component phrase checks are conservative and
can miss equivalent wording; they can also require manual interpretation for
tables, negation, exceptions, and scope. Q003 was specifically reviewed for
scope: a microfinance loan-card/loan-agreement language clause is only PARTIAL
for the question about the general borrower-communications rule.

The audit output is
[`data/evaluation/results/evidence_level_relevance_audit.csv`](../data/evaluation/results/evidence_level_relevance_audit.csv).
Each row includes rank, source/page range, page-overlap flag, label,
matched components, and a short reason. The reason is intended to make the
classification inspectable, not to assert an independent reviewer consensus.

## All-question audit

First DIRECT rank is shown within the official top 10; `—` means none. A lower
rank is better. Q001, Q005, and Q010 have no DIRECT result in either top 10;
Q005 and Q010 have evidence in the diagnostic top 20 as discussed below.

| ID | Type | Fixed-size | Structure-aware | Evidence-level result |
|---|---|---:|---:|---|
| Q001 | Standard | — | — | Both have page-overlapping partial/context results, but neither top 10 contains the complete complaint-escalation evidence. |
| Q002 | Standard | 3 | 3 | Both retrieve the acknowledgement/time-frame evidence. |
| Q003 | Standard | 7 | 4 | Both retrieve the general communication-language rule; language clauses in the microfinance section alone are only partial. |
| Q004 | Standard | 4 | 7 | Both retrieve the written-sanction information; fixed-size has a non-evidentiary rank-1 page match. |
| Q005 | Standard | — | — | Top-10 page matches are partial; the exact bold/loan-agreement evidence is only in diagnostic ranks 19/17. |
| Q006 | Standard | 3 | 4 | Both retrieve the loan-term variation and notice evidence. |
| Q007 | Standard | 7 | 4 | Both retrieve release timing and its qualification; structure-aware ranks it earlier. |
| Q008 | Standard | 1 | 2 | Both retrieve the cost information used to compare offers. |
| Q009 | Standard | 2 | 4 | Both retrieve the required customer option for a disadvantageous change. |
| Q010 | Standard | — | — | No top-10 DIRECT result; structure-aware has evidence at diagnostic rank 18, fixed-size has no gold-page match in top 20. |
| Q011 | Standard | 5 | 8 | Both retrieve board governance evidence; structure-aware ranks its complete evidence lower. |
| Q012 | Standard | 4 | 2 | Both retrieve repossession safeguards. |
| Q013 | Standard | 1 | 1 | Both retrieve the pre-contract disclosure evidence. |
| Q014 | Standard | 5 | 2 | Both retrieve collection location and the field-staff exception. |
| Q015 | Standard | 1 | 1 | Both retrieve the stated grievance-policy objectives. |
| Q016 | Table value | 1 | 1 | Both retrieve the benchmark rates and implementation date from the table. |
| Q017 | Table value | 1 | 1 | Both retrieve the incentive-rate and cap evidence; adjacent table rows are often only partial. |
| Q018 | Table value | 1 | 1 | Both retrieve the requested BHIM-UPI rate; table-row boundaries require care. |
| Q019 | Table value | 3 | 3 | Both retrieve the QRC turnaround-time evidence. |
| Q020 | Table value | 2 | 3 | Both retrieve the 2023–24 growth-rate value from the table; value is on PDF page 41. |
| Q021 | Paraphrased | 2 | 1 | Both retrieve the disclosure exceptions. |
| Q022 | Paraphrased | 7 | — | Fixed-size retrieves the restricted calling hours; structure-aware's top 10 are not sufficient. |
| Q023 | Paraphrased | 2 | 2 | Both retrieve the opportunity required before sale/auction. |
| Q024 | Paraphrased | 1 | 1 | Both retrieve consent and fee-disclosure requirements. |
| Q025 | Paraphrased | 2 | 1 | Both retrieve the duplicate-document support and additional-time clause. |

Using earliest DIRECT rank as the comparison rule within top 10: fixed-size is
better on 7 questions, structure-aware on 6, they tie on 9, and both miss on 3.
This is descriptive and does not imply statistical significance. The diagnostic
top-20 results add a DIRECT Q005 result for both strategies and a DIRECT Q010
result for structure-aware; those diagnostic ranks are not official 2B.16
metrics.

## Label distribution and page-overlap behavior

| Result window | Strategy | DIRECT | PARTIAL | CONTEXT | IRRELEVANT | Page-overlap rows not DIRECT |
|---|---|---:|---:|---:|---:|---:|
| Official top 10 (250 chunks) | Fixed-size | 24 | 39 | 128 | 59 | 17 of 41 |
| Official top 10 (250 chunks) | Structure-aware | 24 | 32 | 122 | 72 | 10 of 33 |
| Diagnostic ranks 11–20 (50 chunks) | Fixed-size | 1 | 4 | 34 | 11 | 1 of 2 |
| Diagnostic ranks 11–20 (50 chunks) | Structure-aware | 2 | 5 | 33 | 10 | 1 of 3 |

The counts are chunk labels, not unique questions or unique evidence spans.
In top 10, at least one DIRECT chunk appears for 22/25 fixed-size questions
and 21/25 structure-aware questions. A page-overlap result labeled PARTIAL is
not necessarily useless, but it does not establish a complete answer by itself.
The non-DIRECT page matches are candidates for false positives under the
existing binary hit rule, not all proven false positives in every multi-chunk
answer scenario.

## Priority investigations

### Q004 — sanction information

Gold source: Bajaj Finance Fair Practice Code, `doc_001`, PDF page 4. The
source says the company conveys the sanctioned amount and terms in writing,
including the annualized interest rate and its method of application, in the
sanction letter or otherwise.

- Fixed-size rank 1 (`doc_001_fixed_size_00001_aee405d33739`, PDF pages 1–4,
  score 0.641427) overlaps the gold page and is counted by the old evaluator,
  but contains no complete requested sanction details: **CONTEXT**.
- Fixed-size first DIRECT result is rank 4
  (`doc_001_fixed_size_00003_0bf6f42069fa`, pages 3–4).
- Structure-aware first DIRECT result is rank 7
  (`doc_001_structure_aware_00003_ad7599361f91`, pages 3–4). Its rank-1
  page-spanning chunk is also not sufficient.

The source/page gold reference is accurate. The rank-1 result is a confirmed
page-span false positive. The correct evidence is retrieved but ranked lower.

### Q005 — where penal charges must be stated

Gold source: `doc_001`, PDF page 4. The source requires the penal charge for
late repayment or another default to be stated **in bold in the loan
agreement**.

- Fixed-size rank 5 (`doc_001_fixed_size_00004_785fedf70295`, pages 4–5) and
  structure-aware rank 6 (`doc_001_structure_aware_00004_288632361e39`,
  pages 4–5) overlap the gold page and are official page-level hits, but are
  PARTIAL: they mention related penal-charge/default concepts without the
  complete placement instruction.
- The evidence-bearing chunk is fixed-size rank 19
  (`doc_001_fixed_size_00003_0bf6f42069fa`, pages 3–4) and structure-aware
  rank 17 (`doc_001_structure_aware_00003_ad7599361f91`, pages 3–4) in the
  existing diagnostic.

The gold page is accurate and sufficiently precise. This is a ranking/context
failure in the top 10, not a source extraction failure. The evidence is in a
chunk spanning the prior page and the gold page, so chunk boundaries and
retrieval ranking may contribute; the evidence does not establish which is the
cause.

### Q010 — risk grading and rate rationale

Gold source: Shriram Finance Fair Practices Code, `doc_016`, PDF page 2. The
source requires the loan application and sanction letter to disclose the risk
gradation approach and rationale for different interest rates, with
availability on the company website or relevant newspapers.

- Neither strategy has a DIRECT result in its official top 10. Both top ranks
  retrieve introductory FPC material, not the risk-grading disclosure.
- Structure-aware retrieves a DIRECT evidence chunk at diagnostic rank 18:
  `doc_016_structure_aware_00003_6a9423992e87`, PDF page 2.
- Fixed-size has no matching gold-page result in the available top 20.

The PDF page and evidence snippet were verified. The structure-aware
rank-18 result proves the evidence is present and retrievable under that
strategy, but does not prove why it ranks low. The fixed-size top-20 absence
does not identify whether wording, chunk representation, or embedding/ranking
is the cause. No evidence supports blaming extraction or the gold label.

## Other observed page-match false positives

- **Q001, rank 1, both strategies:** chunks span the gold page and mention
  dissatisfaction, but do not provide the complete way to take the complaint
  forward. Both page-overlap hits are PARTIAL.
- **Q003, fixed-size rank 1 / structure-aware rank 2:** chunks on PDF pages
  10–11 contain microfinance loan-agreement/loan-card language clauses, not
  the general rule that all borrower communications use a language understood
  by the borrower. These were corrected to PARTIAL. The actual general rule
  appears at fixed-size rank 7 and structure-aware rank 4.
- **Q004, fixed-size rank 1:** page range includes PDF page 4 but lacks the
  requested complete sanction particulars; CONTEXT.
- **Q005, fixed-size rank 5 / structure-aware rank 6:** gold-page overlap
  without the bold/loan-agreement instruction; PARTIAL.
- **Q020, fixed-size rank 1:** the chunk includes PDF page 41 but does not
  contain the full table row/value context; PARTIAL. Later results contain
  the requested table value.

Other page-overlap rows not classified DIRECT are enumerated in the CSV,
including cases involving partial answer components, nearby sections, and
adjacent table rows.

## Recommended evidence-level evaluation methodology

For the next evaluation milestone:

1. **Create evidence units per question.** Store source document, PDF page,
   optional table/row or text span, and each required answer facet. Record
   alternatives, exceptions, units, dates, and conditions separately. Keep
   printed page labels distinct from zero-based indices and one-based PDF
   page numbers.
2. **Annotate chunks against those units.** Use DIRECT when a chunk supports
   the complete requested answer on its own; PARTIAL when it supports one or
   more but not all required facets; CONTEXT and IRRELEVANT as defined above.
   The same gold-page match alone must never promote a chunk to DIRECT.
3. **Report complete-answer and facet recall separately.** For a single-facet
   question, Recall@K is 1 if any DIRECT result occurs by K, otherwise 0.
   For multi-facet questions, complete-answer Recall@K is 1 only when the
   retrieved top-K chunks collectively cover all required facets; also report
   per-facet recall so partial retrieval remains visible. PARTIAL alone does
   not count as complete-answer success.
4. **Define MRR completion rank.** For one-chunk-answerable questions, use the
   first DIRECT rank. For multi-facet answers, use the rank at which the last
   required distinct facet first becomes available in the ranked list. The
   reciprocal of that rank is the question's reciprocal rank; use zero if
   the full evidence set is not covered within the cutoff.
5. **Prevent duplicate credit.** Assign stable facet/evidence-span IDs.
   Repeated or overlapping chunks may support the same facet, but count that
   facet only once. Additional chunks must contribute a missing facet to
   complete an answer.
6. **Validate annotations.** Use a written rubric and source citations. Have
   two reviewers independently annotate all questions (or a predeclared
   representative sample), adjudicate disagreements, and report raw agreement
   plus Cohen's kappa for categorical chunk labels. Revisit ambiguous questions
   and preserve adjudication notes. A phrase matcher may assist triage but
   should not silently determine final labels.

## Limitations and unresolved questions

- Labels are evidence-audit judgments assisted by curated answer-component
  checks; they are not blinded, independent double annotations. The CSV's
  short justifications and row-level provenance make individual judgments
  reviewable, but subjective boundary cases remain.
- Phrase/component matching may undercount semantically equivalent
  paraphrases, especially where a table value is encoded across cells, or
  overstate completeness if matching terms occur in a different scope,
  condition, or negation. Q003 demonstrates why scope is essential.
- A chunk-level DIRECT label does not guarantee that its text is sufficient
  to answer every nuanced interpretation. Conversely, an answer may be
  reconstructible from multiple PARTIAL chunks; this audit does not combine
  them into question-level evidence sets.
- The gold set generally identifies pages/snippets rather than exhaustive
  alternative evidence spans. If equivalent evidence elsewhere in a document
  is retrieved, the gold-document constraint can classify it conservatively.
- The Q010 and Q005 ranks beyond 10 come from the existing diagnostic only.
  They are not official evaluation results and do not establish causal
  explanations for ranking differences.
- No new embeddings, searches, Qdrant writes, or production collection checks
  were performed for this audit. No external service was used.

## Recommendation for the next milestone

Implement a versioned evidence-unit/facet annotation format and a deterministic
evidence-level metric evaluator before selecting or changing the primary
chunking strategy. First adjudicate the three top-10 misses (Q001, Q005, Q010),
the Q004 page-span false positive, and table-value questions with two reviewers.
Then recalculate complete-answer and per-facet Recall@3/5/10 and MRR from the
same persisted rankings. Do not treat the current page-overlap metrics or this
phrase-assisted audit as final evidence-level ground truth.

## Validation and integrity

- Audited all 25 questions; reviewed top 10 for both strategies (500 results)
  and existing diagnostic ranks 11–20 for Q003, Q004, Q005, Q010, and Q011
  (100 additional results).
- Verified source/page evidence for the gold references and the priority
  findings against original PDFs and extracted/structured evidence.
- The CSV has 600 data rows; reported label totals reconcile to 250 top-10
  rows per strategy and 50 diagnostic rows per strategy.
- No application code, existing 2B.16 evaluation artifacts, PDFs, manifest,
  extraction/OCR/cleaned-page/chunk data, embeddings, or Qdrant collections
  were modified. No Qdrant write operation or external embedding call occurred.
- `git diff --check` was run after the report was written and passed.

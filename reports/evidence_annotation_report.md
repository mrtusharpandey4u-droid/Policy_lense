# PolicyLens — Evidence Annotation Proposal (Milestone 2B.19)

## Status and scope

This report accompanies the versioned annotation proposal at
[`data/evaluation/evidence_annotations_v1.jsonl`](../data/evaluation/evidence_annotations_v1.jsonl).
It covers all 25 evaluation questions. The records define 63 answer facets,
source citations, excerpts, table/clause constraints, accepted alternate
locations, and a proposed question-level completeness assessment for each
strategy's official top 10. Existing diagnostic top-20 results are separately
noted for Q005 and Q010.

**This is an assistant-produced proposal, not human-adjudicated gold.** No
independent human reviewer participated. Every record remains
`proposed_requires_user_approval` or, for three scope-sensitive questions,
`needs_review`. Do not use the labels or completeness statuses as final
evaluation ground truth until a reviewer approves or corrects them.

## Methodology

1. Read the original 25 questions and gold references, official 2B.16 ranked
   results, previous evidence-audit report/CSV, the relevant chunks for both
   strategies, and source PDFs at the cited pages.
2. Derive facets from the actual source requirement, not from the previous
   audit's automated label. Split independently checkable values, conditions,
   exceptions, channels, and limits into separate facets.
3. Use one-based **PDF page numbers** throughout. Printed page labels are
   retained only as context and are never substituted for PDF pages.
4. For table questions, preserve row/column identity and units, not just
   matching numbers. Check structured table cells when PDF text extraction
   interleaves columns or breaks a row.
5. A chunk label means:
   - **DIRECT:** supports at least one identified required facet directly.
   - **PARTIAL:** supports only part of an answer/facet set, or supports some
     facets but omits others.
   - **CONTEXT:** related background without direct support for a required
     facet.
   - **IRRELEVANT:** no meaningful support.
   Question-level completeness is separate: all required facets must be
   covered by the retrieved evidence. A DIRECT chunk does not, by itself,
   imply a complete multi-facet answer.
6. Count a facet/evidence passage once. Multiple overlapping chunks may each
   be labeled DIRECT, but do not constitute additional unique evidence.

The prior phrase-assisted CSV was used to find questions and ranks to inspect,
not as accepted labels. Candidate matches were checked against actual chunk
text and source pages; prior labels were changed where the evidence did not
support them. No separate exhaustive 600-row chunk-label file is supplied:
unreviewed retrieval rows should not be given apparently final negative
labels. Selected supporting/counterexample chunk IDs and proposed labels are
embedded in the question records.

## Question-by-question proposal

“Complete” means all listed facets are present in at least one or more
top-10 retrieved chunks. Q005/Q010 diagnostic ranks are not official top-10
results. The Q020 assessment requires the explicitly named table row.

| ID | Gold source (PDF page) | Required facets | Fixed-size top 10 | Structure-aware top 10 | Review note |
|---|---|---:|---|---|---|
| Q001 | doc_001 (3) | 1 | Incomplete | Incomplete | Neither top 10 contains the complaint-forwarding commitment. |
| Q002 | doc_001 (4) | 2 | Complete, r3 | Complete, r3 | Acknowledgement receipt and disposal timeframe. |
| Q003 | doc_001 (4) | 1 | Complete, r7 | Complete, r4 | General communications language rule; microfinance-specific language clauses are not substitutes. |
| Q004 | doc_001 (4) | 4 | Complete, r4 | Complete, r7 | Rank-1 fixed-size page-span match is not evidence; complete details occur lower. |
| Q005 | doc_001 (4) | 4 | Incomplete top 10 | Incomplete top 10 | Complete evidence only at diagnostic r19/r17. |
| Q006 | doc_001 (5) | 2 | Complete, r3 | Complete, r4 | Notice of changes and prospective effect. |
| Q007 | doc_001 (5) | 2 | Complete, r7 | Complete, r4 | Release trigger and legitimate-right/lien qualification. |
| Q008 | doc_003 (4) | 2 | Complete, r1 | Complete, r2 | All-in processing/sanction cost, transparency, non-discrimination. |
| Q009 | doc_003 (5) | 3 | Complete, r2 | Complete, r4 | Disadvantage trigger, 60-day close/switch option, no extra charge/interest. |
| Q010 | doc_016 (2) | 2 | Incomplete top 10 | Incomplete top 10 | Structure-aware diagnostic r18 contains both facets; fixed-size has no gold-page hit in top 20. |
| Q011 | doc_016 (5) | 3 | Complete, r5 | Complete, r8 | Mechanism/escalation, periodic review, consolidated report. |
| Q012 | doc_016 (6) | 5 | Complete, r4 | Complete, r2 | Contractual repossession safeguards; five facets cover the enumerated provisions. |
| Q013 | doc_024 (2) | 3 | Complete, r1 | Complete, r1 | KFS, language, explanation, acknowledgement. |
| Q014 | doc_024 (3) | 2 | Complete, r5 | Complete, r2 | Normal collection location and the two-failure home/work exception. |
| Q015 | doc_023 (2) | 3 | Complete, r1 | Complete, r1 | Fairness, courteous/timely resolution, awareness of rights/remedies. |
| Q016 | doc_019 (2) | 1 | Complete, r1 | Complete, r1 | TCL Retail PLR row: current/revised values and date. |
| Q017 | doc_034 (1) | 4 | Complete, r1 | Complete, r1 | Split table cells jointly identify RuPay, outside-programme rate, and cap. |
| Q018 | doc_034 (1) | 3 | Complete, r1 | Complete, r1 | BHIM-UPI P2M threshold, outside-programme category, rate. |
| Q019 | doc_023 (7) | 2 | Complete, r3 | Complete, r3 | QRC-tagging row and T+2 working-day maximum TAT. |
| Q020 | doc_036 (41) | 2 | Incomplete | Incomplete | Top-10 chunks do not contain the Table II.2.1 row/value; structure-aware r5 has alternate narrative evidence. |
| Q021 | doc_016 (3) | 4 | Complete, r2 | Complete, r1 | Three exception categories and marketing limitation; needs scope approval. |
| Q022 | doc_024 (3) | 1 | Complete, r7 | Incomplete | Prohibited before-9 a.m./after-6 p.m. calling. |
| Q023 | doc_016 (6) | 1 | Complete, r2 | Complete, r2 | Final repayment opportunity before sale/auction. |
| Q024 | doc_024 (3) | 2 | Complete, r1 | Complete, r1 | Fixed-size r1 and r10 duplicate the same clause; count its facets once. |
| Q025 | doc_001 (6) | 4 | Complete, r2 | Complete, r1 | Applicability trigger, duplicate copies, costs/compensation, extra 30 days and 60-day penalty boundary; scope needs approval. |

These are proposed question-level assessments, not independently validated
metric results. “Complete” is based on the referenced chunk containing all
the listed facets; “incomplete” does not imply the evidence is absent from the
document.

## Priority-case decisions

### Q004 — complete sanction disclosure

The source on PDF page 4 requires written communication in the vernacular,
by sanction letter or otherwise, of the sanctioned amount, terms and
conditions including annualized interest rate, and the method of applying
that rate. These are four separate facets. Fixed-size rank 1 spans PDF pages
1–4 but does not state the sanction details; it is not relevant merely
because its page range overlaps. The first proposed complete chunks are
fixed-size rank 4 and structure-aware rank 7.

### Q005 — penal charge placement

The source on PDF page 4 says a penal charge for late repayment and/or any
other customer default must be mentioned **in bold in the loan agreement**.
The proposal separates late repayment, other default, bold emphasis, and
agreement location. Official top-10 page matches contain related penal-charge
and agreement material but not the full instruction, so top-10 completeness
is false. The existing diagnostic's fixed-size rank 19 and structure-aware
rank 17 contain the full requirement. Gold page is confirmed.

### Q010 — risk grading and rate rationale

PDF page 2 requires the loan application form and sanction letter to disclose
the risk-gradation approach and rationale for different rates among borrower
categories; the information must also be on the website or published in
relevant newspapers. Generic website mentions and generic interest/risk
language are not direct evidence of this rule. Neither strategy has complete
evidence in top 10. Structure-aware diagnostic rank 18 contains the evidence;
fixed-size has no matching gold-page result in top 20.

### Q017 — split table cells

The actual page-1 table has a row hierarchy: RuPay POS/e-commerce transactions
→ “Other than industry programmes” → 0.40%, capped at ₹100. Both rank-1
chunks contain this relation in the chunk text and structured table cells.
The cells must be interpreted together: token matching against one
contiguous phrase can incorrectly call this row partial. The repeated page-6
claim-submission table is accepted as corroboration, but the stated page-1
scheme table remains the primary citation.

### Q020 — alternate narrative versus requested table

The source table on one-based PDF page 41 was inspected in the PDF's table
cells. Its `Gross Fixed Capital Formation` row across 2019–20 through 2023–24
is `1.1, -7.1, 17.5, 6.6, 10.2`; the requested 2023–24 value is 10.2 per
cent. The cited row is verified despite multi-column PDF text extraction
order. The top-10 chunks previously marked DIRECT by phrase matching do not
contain `10.2` or the table row in their chunk text/table payload. Structure-
aware rank 5 on PDF pages 27–28 does state that GFCF accelerated to 10.2% in
2023–24. This is valid alternate evidence for the numeric fact, but not
retrieval of the question's explicitly named Table II.2.1 row. Whether the
benchmark should accept this alternate location needs reviewer approval.

### Q024 — duplicate retrievals

The fixed-size rank-1 and rank-10 chunks both contain the same PDF-page-3
non-credit-products clause. They can both be DIRECT at the chunk level, but
support the same two facets: full borrower consent and fee statement in the
loan card. Do not count the duplicated span as new evidence or additional
question-level credit. Structure-aware rank 1 contains the same source clause.

## Other source-sensitive decisions

- **Q021:** The confidentiality clause lists three alternative grounds:
  legal/statutory/regulatory requirement; public duty; or company interest
  (including fraud prevention) for disclosure to banks/financial institutions/
  group/associate companies. It then restricts use of that interest rationale
  for marketing. The wording “When can” might ask for an example or the full
  list; this proposal requires the full list and boundary and marks it
  `needs_review`.
- **Q025:** The gold question snippet previously omitted the extra-time
  detail. The source on PDF page 6 says the company assists with duplicate/
  certified copies, bears costs and pays compensation, has an additional 30
  days, and the delayed-period penalty is calculated after 60 days total.
  Whether compensation/penalty are required in an answer to “what support and
  additional time” needs review; the source itself is clear.
- **Q003/Q022:** Scope and conditions matter. The language requirement in
  Q003 is the general borrower-communications clause, not merely the
  microfinance loan-card rule. Q022 prohibits calls before 9 a.m. and after
  6 p.m.; do not add a persistence requirement to the time restriction.
- **Q019:** T+2 is attached to the QRC-tagging row and the table labels TAT in
  working days; a detached `T+2` is not sufficient.

## Annotation and review counts

- Question records: **25**, unique IDs Q001–Q025.
- Proposed evidence facets: **63**.
- Proposed selected chunk references: **54** (46 DIRECT, 3 PARTIAL, 5 CONTEXT);
  every embedded chunk assessment remains pending user adjudication.
- Proposed top-10 completeness: fixed-size **21 complete / 4 incomplete**;
  structure-aware **20 complete / 5 incomplete**. These are provisional
  assistant assessments, not approved scores.
- Records marked `needs_review`: **3** (Q020, Q021, Q025).
- Records marked `proposed_requires_user_approval`: **22**.
- Human-adjudicated question or chunk labels: **0**.
- Existing automated labels accepted as final: **0**.
- Assistant-proposed chunk references are embedded only for source-checked
  positive/partial evidence and selected counterexamples. They are not
  approved labels. A full ranked-result chunk annotation set remains future
  work after review; no CONTEXT/IRRELEVANT labels are being silently inferred
  for unreviewed chunks.

## Unresolved items and validation

1. Obtain user/reviewer decisions for Q020 alternate-page acceptance, Q021
   whether completeness means one exception or the exhaustive list, and Q025
   whether compensation and the post-60-day penalty are required facets.
2. Have a human reviewer validate the 60 facets and quoted excerpts against
   source pages, then adjudicate the selected chunk assessments. In particular
   review exact table-cell association and duplicate chunk treatment.
3. Only after approval, annotate the remaining retrieved chunks with
   DIRECT/PARTIAL/CONTEXT/IRRELEVANT and reviewer status. Keep machine
   suggestions distinct from approved labels.

Validation performed:

- Parsed the annotation JSONL and checked all 25 expected unique question
  IDs, non-empty facet lists, unique facet IDs within each question, source
  document/page references, positive one-based PDF page values, and referenced
  top-10 chunk IDs.
- Compared source excerpts with cited PDF pages; the ordinary text excerpts
  matched after normalization. Q020's table row was verified through the
  original PDF's extracted table cells because text-order normalization does
  not preserve the row.
- Checked the relevant source/chunk passages for Q004, Q005, Q010, Q017,
  Q020, Q024, table questions, paraphrased questions, and the other cited
  top-10 evidence chunks.
- No original question, 2B.16 result, prior audit report/CSV, source PDF,
  manifest, processed data, embeddings, or Qdrant collection was modified.
  No embedding, ingestion, indexing, external API, or metric computation was
  run.

## Recommended next milestone

Request human adjudication of this proposal before treating it as gold.
Resolve the three flagged scope decisions, revise approved facets and excerpts,
then create a separate versioned chunk-annotation set with reviewer identity,
status, and evidence-span/facet IDs. Do not implement metrics or change
retrieval until that approved annotation layer exists.

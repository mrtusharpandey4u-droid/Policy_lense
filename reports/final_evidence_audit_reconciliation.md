# PolicyLens — Final Cross-Artifact Evidence Audit Reconciliation

**Scope:** Milestone 2B.21, read-only cross-artifact review  
**Status:** Proposed evidence annotations remain unapproved

## 1. Executive summary

All 25 evaluation questions were checked against their original question and
gold reference, proposed facets and excerpts, persisted top-10 rankings, the
referenced chunk payloads, and the relevant source PDF pages. Existing evidence
and retrieval artifacts were inspected; no retrieval, metric, embedding, OCR,
or indexing run was performed.

| Question-level reconciliation status | Count |
|---|---:|
| VERIFIED | 22 |
| PARTIALLY_VERIFIED | 1 |
| ISSUE_FOUND | 2 |

Q021 is the single PARTIALLY_VERIFIED case because the source is clear but the
question's completeness criterion needs a reviewer decision. Q020 and Q025 are
the two ISSUE_FOUND cases because persisted completeness/label claims conflict
with their actual chunks.

The proposal is **not ready for approval**. Two objective cross-artifact
corrections are needed:

1. **Q020:** Structure-aware rank 10
   (`doc_036_structure_aware_00080_da6891873a1b`) contains the complete Table
   II.2.1 row and its 2023-24 value, 10.2. The annotation proposal incorrectly
   marks structure-aware top 10 incomplete and says no top-10 chunk contains
   the row/value. The decision sheet is correct on this point. Fixed-size top
   10 does not contain that complete table evidence.
2. **Q025:** Fixed-size rank 2 supports duplicate/certified-copy assistance,
   associated costs, compensation, and the additional 30 days, but does **not**
   state the 60-day total. The annotation JSONL nevertheless marks all four
   facets complete, even though F4 combines the additional 30 days with the
   60-day penalty boundary. The decision sheet correctly identifies the
   missing boundary. The facet scope also needs human adjudication.

Q021's source and three alternative disclosure grounds are supported, but
whether “When can” requires the exhaustive list remains a human decision. The
marketing sentence is a qualification on the company-interest ground, not a
fourth disclosure ground.

The separate “quality review report from Milestone 2B.18B” could not be
identified in this workspace: no report with that milestone designation or
title was found. The closest relevant report present is
[`reports/evidence_level_relevance_audit.md`](evidence_level_relevance_audit.md),
titled Milestone 2B.18; it is not identified as a 2B.18B report. The later
proposal and decision sheet are Milestone 2B.19 artifacts, not substitutes for
a missing 2B.18B report.

No annotation is treated as approved ground truth. All annotation records
remain pending user adjudication, and no existing artifact was changed.

## 2. Files and data sources inspected

- [`reports/evidence_level_relevance_audit.md`](evidence_level_relevance_audit.md)
  — Milestone 2B.18 report, including page-overlap findings and question
  summaries.
- [`data/evaluation/results/evidence_level_relevance_audit.csv`](../data/evaluation/results/evidence_level_relevance_audit.csv)
  — existing 600-row chunk-level audit, including priority-case labels.
- **Milestone 2B.18B quality review:** no matching report was present in
  `reports/` or otherwise identified in the workspace.
- [`reports/evidence_annotation_report.md`](evidence_annotation_report.md)
  and
  [`reports/evidence_annotation_decision_sheet.md`](evidence_annotation_decision_sheet.md)
  — proposal methodology, question summaries, and Q020/Q021/Q025 decisions.
- [`data/evaluation/evidence_annotations_v1.jsonl`](../data/evaluation/evidence_annotations_v1.jsonl)
  and
  [`data/evaluation/evaluation_questions.jsonl`](../data/evaluation/evaluation_questions.jsonl)
  — the 25 proposed records, original question wording, gold page references,
  facets, excerpts, and provisional completeness assessments.
- Persisted retrieval artifacts:
  [`data/evaluation/results/retrieval_evaluation_results.json`](../data/evaluation/results/retrieval_evaluation_results.json),
  [`data/evaluation/results/retrieval_evaluation_question_results.csv`](../data/evaluation/results/retrieval_evaluation_question_results.csv),
  and the existing
  [`data/evaluation/results/retrieval_failure_top20_diagnostic.json`](../data/evaluation/results/retrieval_failure_top20_diagnostic.json).
- Existing chunk sets:
  [`data/processed/chunks/fixed_size.jsonl`](../data/processed/chunks/fixed_size.jsonl)
  and
  [`data/processed/chunks/structure_aware.jsonl`](../data/processed/chunks/structure_aware.jsonl),
  including structured table payloads.
- [`data/manifest.csv`](../data/manifest.csv), cited original PDFs in
  [`data/pdfs/`](../data/pdfs/), and relevant cleaned page records under
  [`data/processed/cleaned/`](../data/processed/cleaned/).
- Related reports consulted for the previous retrieval findings:
  [`reports/retrieval_failure_analysis.md`](retrieval_failure_analysis.md),
  [`reports/retrieval_evaluation_report.md`](retrieval_evaluation_report.md),
  and [`reports/retrieval_evaluation_dataset_report.md`](retrieval_evaluation_dataset_report.md).

### Review method and status meanings

The original question's cited PDF page and excerpt were compared with the
source page (including structured table cells where relevant). Proposed
supporting chunk IDs/ranks were cross-checked against the saved top-10 result
records and both chunk files. Page overlap alone was not treated as evidence.
The existing top-20 diagnostic was used only where it already exists (notably
Q005 and Q010); its ranks are not official top-10 metrics.

- **VERIFIED** means the source, facet interpretation, and stated retrieval
  assessment agree with the inspected evidence. A verified “incomplete” result
  remains an incomplete result.
- **PARTIALLY_VERIFIED** means evidence is present but an interpretation or
  requirement boundary remains unresolved.
- **ISSUE_FOUND** means a concrete claim or completeness status conflicts with
  the inspected source or persisted chunk.
- **REQUIRES_HUMAN_DECISION** marks an interpretation that this audit does not
  silently resolve.

## 3. Twenty-five-question reconciliation

| ID | Original question; gold PDF reference | Source evidence status | Facet accuracy status | Retrieval assessment status | Outstanding issue |
|---|---|---|---|---|---|
| Q001 | What does Bajaj Finance commit to do when a customer remains dissatisfied after raising a complaint? — doc_001, p. 3 | VERIFIED | VERIFIED | VERIFIED | Both top 10s remain incomplete; page-overlapping rank 1 is not the complaint-forwarding commitment. |
| Q002 | What should the lender's acknowledgement tell an applicant about the handling of a loan application? — doc_001, p. 4 | VERIFIED | VERIFIED | VERIFIED | Acknowledgement receipt and disposition timeframe are both supported at rank 3 in each strategy. |
| Q003 | In what language must borrower communications be provided under this fair-practice code? — doc_001, p. 4 | VERIFIED | VERIFIED | VERIFIED | General borrower-language rule is supported at fixed rank 7 and structure-aware rank 4; microfinance-specific language clauses are not substitutes. |
| Q004 | What key loan information must Bajaj Finance convey in writing when a loan is sanctioned? — doc_001, p. 4 | VERIFIED | VERIFIED | VERIFIED | Fixed rank 1 is a page-span false positive; complete evidence is at fixed rank 4 and structure-aware rank 7. |
| Q005 | Where must penal charges for late repayment or another borrower default be highlighted? — doc_001, p. 4 | VERIFIED | VERIFIED | VERIFIED | Top-10 partials do not include the full bold-in-the-loan-agreement instruction; diagnostic evidence is at fixed rank 19 and structure-aware rank 17. |
| Q006 | How must a lender handle changes to loan terms such as the disbursement schedule or interest rate? — doc_001, p. 5 | VERIFIED | VERIFIED | VERIFIED | Notice and prospective-effect facets are supported at fixed rank 3 and structure-aware rank 4. |
| Q007 | When does the code require the lender to release a borrower's securities, and what qualification applies? — doc_001, p. 5 | VERIFIED | VERIFIED | VERIFIED | Release trigger and legitimate-right/lien qualification are supported at fixed rank 7 and structure-aware rank 4. |
| Q008 | What cost information must Tata Capital Housing Finance disclose so a borrower can compare loan offers? — doc_003, p. 4 | VERIFIED | VERIFIED | VERIFIED | All-in cost, transparency, and non-discrimination facets are supported at fixed rank 1 and structure-aware rank 2. |
| Q009 | If a change in loan terms disadvantages the customer, what option does Tata Capital Housing Finance provide? — doc_003, p. 5 | VERIFIED | VERIFIED | VERIFIED | Disadvantage trigger, 60-day close/switch option, and no-extra-charge condition are supported at fixed rank 2 and structure-aware rank 4. |
| Q010 | Where must Shriram Finance explain how it grades borrower risk and why different rates are charged? — doc_016, p. 2 | VERIFIED | VERIFIED | VERIFIED | No complete top-10 result; structure-aware diagnostic rank 18 contains the source evidence, while fixed-size has no gold-page result in the available top 20. |
| Q011 | What governance duties does Shriram Finance's board have for grievance handling and Fair Practice Code compliance? — doc_016, p. 5 | VERIFIED | VERIFIED | VERIFIED | Governance mechanism, review, and reporting facets are supported at fixed rank 5 and structure-aware rank 8. |
| Q012 | What repossession safeguards must Shriram Finance include in a vehicle loan agreement? — doc_016, p. 6 | VERIFIED | VERIFIED | VERIFIED | The five repossession safeguards are supported at fixed rank 4 and structure-aware rank 2. |
| Q013 | What must Tata Capital provide and explain to a prospective microfinance borrower before the loan contract is executed? — doc_024, p. 2 | VERIFIED | VERIFIED | VERIFIED | KFS, language, explanation, and acknowledgement requirements are supported at rank 1 in both strategies. |
| Q014 | Where should microfinance repayments normally be collected, and when may field staff collect at a borrower's home or workplace? — doc_024, p. 3 | VERIFIED | VERIFIED | VERIFIED | Normal collection location and the two-successive-failure home/work exception are supported at fixed rank 5 and structure-aware rank 2. |
| Q015 | What customer protections are objectives of Tata Capital's customer grievance policy? — doc_023, p. 2 | VERIFIED | VERIFIED | VERIFIED | The three stated grievance-policy objectives are supported at rank 1 in both strategies. |
| Q016 | In Tata Capital's benchmark-rate table, what were the current and revised TCL Retail PLR and the earliest implementation date? — doc_019, p. 2 | VERIFIED | VERIFIED | VERIFIED | The TCL Retail PLR row's current/revised values and effective date are supported at rank 1 in both strategies. |
| Q017 | For a RuPay debit-card transaction outside an industry programme, what incentive rate and per-transaction cap does the DFS table specify? — doc_034, p. 1 | VERIFIED | VERIFIED | VERIFIED | Structured table rows support the RuPay category, outside-programme condition, 0.40% rate, and ₹100 cap at rank 1 in both strategies. |
| Q018 | For BHIM-UPI P2M transactions up to ₹2,000 outside industry programmes, what incentive rate is shown in the scheme table? — doc_034, p. 1 | VERIFIED | VERIFIED | VERIFIED | BHIM-UPI P2M threshold, outside-programme category, and 0.25% rate are supported at rank 1 in both strategies. |
| Q019 | In Tata Capital's grievance-handling SOP table, what is the maximum turnaround time for tagging a case as QRC after a customer requirement or concern is identified? — doc_023, p. 7 | VERIFIED | VERIFIED | VERIFIED | The QRC-tagging row and T+2 working-day maximum are supported at rank 3 in both strategies. |
| Q020 | In RBI Annual Report Table II.2.1, what growth rate is listed for Gross Fixed Capital Formation in 2023-24? — doc_036, p. 41 | VERIFIED | VERIFIED | ISSUE_FOUND | Structure-aware rank 10 contains the complete named-table row and value, contrary to the annotation JSONL/report. Fixed-size top 10 has no complete row/year/value evidence. |
| Q021 | When can the finance company disclose a borrower's personal or transaction information without the borrower's authorization? — doc_016, p. 3 | VERIFIED | REQUIRES_HUMAN_DECISION | REQUIRES_HUMAN_DECISION | Both strategies retrieve the three grounds and marketing qualification; decide whether the question requires all grounds or permits one example. |
| Q022 | During microfinance debt collection, which calling hours are prohibited by the fair-practice code? — doc_024, p. 3 | VERIFIED | VERIFIED | VERIFIED | Fixed-size rank 7 contains prohibited calling hours; structure-aware top 10 is incomplete. |
| Q023 | Before selling or auctioning a repossessed vehicle, what opportunity must the lender's process give the borrower? — doc_016, p. 6 | VERIFIED | VERIFIED | VERIFIED | Both strategies support a final repayment opportunity before sale/auction at rank 2. |
| Q024 | May a microfinance lender provide non-credit add-on products without the borrower's agreement, and where must their fees be stated? — doc_024, p. 3 | VERIFIED | VERIFIED | VERIFIED | Both strategies support consent and fee disclosure; fixed-size ranks 1 and 10 repeat the same clause and must not earn duplicate evidence credit. |
| Q025 | If original property papers are lost or damaged after a personal loan is settled, what support and additional time does the code allow? — doc_001, p. 6 | VERIFIED | PARTIALLY_VERIFIED | ISSUE_FOUND | Structure-aware rank 1 includes the 60-day total; fixed-size rank 2 omits it, despite the JSONL marking the combined F4 complete. Decide whether compensation and the 60-day boundary are required or contextual. |

## 4. Priority-case reconciliation

### Q004 — page overlap is not answer evidence

The gold source is `doc_001`, PDF page 4. It requires written disclosure of
the sanctioned amount, terms and conditions (including the annualized interest
rate), and the method of applying that rate. These proposed facets are
supported by the cited source.

Fixed-size rank 1 (`doc_001_fixed_size_00001_aee405d33739`) spans pages 1–4 but
does not state those sanction particulars. The earlier page-overlap evaluator
counted it because the page range covered page 4; the evidence audit correctly
labels it CONTEXT. The first complete evidence is fixed-size rank 4
(`doc_001_fixed_size_00003_0bf6f42069fa`) and structure-aware rank 7
(`doc_001_structure_aware_00003_ad7599361f91`). The proposal incorporates
this correction consistently.

### Q005 — late/default triggers and bold loan-agreement placement

The source on `doc_001`, PDF page 4, covers a penal charge for late repayment
and/or another customer default and requires it to be mentioned in bold in the
loan agreement. The four proposed facets preserve the triggers and placement
requirements. Gold source/page and excerpt are supported.

The page-overlapping fixed-size rank 5 and structure-aware rank 6 chunks
contain related penal-charge/default material but not the complete
instruction. They are partial, not complete evidence. The existing diagnostic
contains the full evidence at fixed-size rank 19 and structure-aware rank 17.
The proposal correctly leaves both official top-10 assessments incomplete;
the diagnostic ranks should remain distinguished from official top-10
results.

### Q010 — generic website language versus risk-grading disclosure

The cited source is `doc_016`, PDF page 2. The source requires the risk-
gradation approach and rationale for different interest rates to be disclosed
in the loan application form and sanction letter, with the information also
available on the company website or in relevant newspapers. The proposed two
facets capture the forms/rationale and the publication channel.

Generic website wording or generic discussion of interest/risk elsewhere
does not establish this requirement. Neither strategy has complete evidence
in the official top 10. Structure-aware rank 18 in the existing diagnostic
contains the evidence; fixed-size has no gold-page chunk in that top 20.
The proposal incorporates the earlier audit finding correctly and does not
claim that the source evidence is absent.

### Q017 — table-cell evidence

The original `doc_034` PDF page 1 and both rank-1 chunk table payloads support
the requested RuPay debit-card POS/e-commerce category, “Other than industry
programmes,” 0.40% incentive, and ₹100 per-transaction cap. The structured
rows preserve the association between category and rate/cap; the values are
not inferred from a neighboring industry-programme row.

The proposal's four facets and rank-1 completeness assessments are supported.
This is the table-cell case that requires reading row/cell structure rather
than relying only on phrase matching over flattened text. Do not treat
adjacent table rows or repeated cell terms as independent evidence.

### Q020 — Table II.2.1 and the actual structure-aware rank 10

The original RBI Annual Report PDF page 41 (printed page 16) has the 2023-24
column heading and the `Gross Fixed Capital Formation` row. The original
table row reads `1.1 | -7.1 | 17.5 | 6.6 | 10.2`; the requested intersecting
value is 10.2 per cent.

The actual structure-aware rank-10 result is
`doc_036_structure_aware_00080_da6891873a1b`, PDF page 41. Its structured
payload contains the year headings and row
`Gross Fixed Capital Formation | 1.1 | -7.1 | 17.5 | 6.6 | 10.2`. It supports
both proposed facets and completes the explicitly named table retrieval
within top 10.

No fixed-size top-10 chunk contains the complete table row/year/value
relation. Fixed-size rank 2
(`doc_036_fixed_size_00070_eb1ac13cadb6`) includes chart/table-related
references to the row and years but no 10.2 in the chunk text or table
payload; the other fixed top-10 chunks likewise do not supply the complete
relation. A similarly named GFCF measure in other chart content is not
sufficient.

Structure-aware rank 5 (`doc_036_structure_aware_00058_627c4c142023`) states
in narrative that GFCF accelerated to 10.2% in 2023-24. It supports the
numeric fact, but does not demonstrate retrieval of the specifically named
Table II.2.1 row. Whether that alternate narrative should count for a
table-specific question remains a human decision; it does not negate the
rank-10 table evidence.

Cross-artifact inconsistencies:

- The annotation JSONL and its report say structure-aware top 10 is
  incomplete and that no top-10 chunk has the row/value. This is contradicted
  by the persisted rank-10 chunk.
- The decision sheet correctly reports the structure-aware rank-10 row and
  should be used for that factual check, but its correction was not propagated
  to the proposal.
- The existing evidence-level CSV labels fixed-size rank 2 and
  structure-aware rank 3 DIRECT based on component-string matches even though
  those chunks lack the complete value relation. Structure-aware rank 5 is
  DIRECT for the narrative number only under a generic fact-answer criterion;
  it is not table-specific evidence. Structure-aware rank 10 is the valid
  table-specific DIRECT result.
- Accordingly, the audit report's first-DIRECT summary for Q020 is not
  reliable under the table-specific criterion. These existing artifacts are
  left unchanged in this read-only audit.

Before approval, the proposal's structure-aware completeness and supporting
chunk citation must be corrected to include rank 10, and its explanatory note
must distinguish that table row from the rank-5 alternate narrative. The
fixed-size assessment remains incomplete for the table-specific criterion.

### Q021 — three alternative grounds and a marketing qualification

The original source is `doc_016`, PDF page 3. It lists three alternative
grounds for disclosure without authorization:

1. A legal, statutory, or regulatory requirement.
2. A duty to the public to reveal the information.
3. Company interest (for example, fraud prevention) for disclosure to banks,
   financial institutions, group, or associate companies.

The following marketing sentence limits use of the company-interest reason:
it is not a fourth ground and should not be detached from that ground in an
answer. The proposed F1–F3 grounds and F4 qualification reflect this source
distinction. Fixed-size rank 2 and structure-aware rank 1 contain the three
grounds and marketing limitation.

The question's “When can” wording does not explicitly require an exhaustive
list. Requiring all three grounds is a defensible reproducible annotation
criterion, but treating one supported example as sufficient is also
linguistically plausible. A reviewer must decide whether completeness means
the exhaustive source list. If the exhaustive criterion is chosen, keep the
marketing limitation as a qualification attached to F3, rather than a fourth
exception.

### Q024 — overlapping chunks are duplicate evidence

The `doc_024` source clause on PDF page 3 requires full borrower consent for
non-credit products and explicit fee-structure communication in the loan
card. Fixed-size rank 1, fixed-size rank 10, and structure-aware rank 1 all
contain that same source clause and support the two facets.

The proposal correctly notes that fixed-size ranks 1 and 10 are overlapping
retrievals of the same evidence. Each chunk may be assessed at chunk level,
but the clause/facets must be counted once at question level. No correction
is needed to the proposed completeness statuses on this point.

### Q025 — required answer versus contextual consequences

The source is `doc_001`, PDF page 6. It states that when original property
documents are lost or damaged, the company assists in obtaining duplicate or
certified copies, bears the associated costs, pays compensation under the
preceding clause, and has an additional 30 days. It further says delayed-
period penalty is calculated after a total period of 60 days.

The question asks what support and additional time the code allows. The core
answer evidence is assistance with duplicate/certified copies, associated
cost responsibility, and the additional 30 days. The total 60-day period is
an important explanation of when the delayed-period penalty starts. The
compensation is a source-stated entitlement, but whether it is required to
answer this narrower question or is contextual/exhaustive detail needs
review. The scenario/applicability facet F1 describes the circumstances and
is not itself a remedy.

Structure-aware rank 1
(`doc_001_structure_aware_00005_33a0e3812a93`) contains all of these
details, including the 60-day total. Fixed-size rank 2
(`doc_001_fixed_size_00005_d577f4089a07`) contains duplicate/certified-copy
assistance, costs, compensation, and 30 additional days, but not the 60-day
total. A similar chunk at fixed-size rank 1 is from `doc_003`, a different
lender, and cannot complete the `doc_001` answer.

The annotation JSONL labels fixed-size rank 2 complete and assigns F4, which
combines the additional 30 days and the 60-day penalty boundary. This is an
unsupported completeness claim: the chunk supports only the first part of
F4. The decision sheet accurately flags that omission. Before approval,
split F3 (costs vs. compensation) and F4 (additional 30 days vs. 60-day
penalty boundary), decide which are essential, and revise fixed-size
completeness accordingly.

## 5. Inconsistencies and required corrections before approval

1. **Correct Q020 in the proposal:** cite structure-aware rank 10 and mark
   structure-aware top 10 complete under the table-specific criterion. Retain
   fixed-size incomplete. Explain that rank 5 is an alternate narrative
   source, not the named table.
2. **Reconcile Q020 labels in the prior CSV/report if they are reused:** the
   prior phrase/component-based DIRECT assignments at fixed rank 2 and
   structure-aware rank 3 do not establish the row/year/value relation.
   Structure-aware rank 5 may support the number but not the specified table;
   rank 10 does contain the complete structured row. Do not let the earlier
   CSV's matched terms override the actual chunk payload.
3. **Correct Q025 fixed-size completeness:** rank 2 does not support the
   60-day half of F4. Either split the facet and classify the top-10 result
   facet-by-facet, or explicitly scope completeness to the core requested
   support/time answer and identify the 60-day total as contextual.
4. **Adjudicate Q021/Q025 scope:** record the human decision for exhaustive
   exception listing and for compensation/60-day penalty treatment; do not
   convert a recommendation in the decision sheet into approved ground truth.
5. **Preserve prior findings consistently:** Q004's page-span false positive,
   Q005's separated evidence/ranks, Q010's generic-website false positive and
   rank-18 evidence, Q017's table-cell associations, and Q024's duplicate
   overlap are all handled consistently by the proposal. Q020 and Q025 are
   the exceptions requiring correction.
6. **Human adjudication remains outstanding for the proposal as a whole:**
   all 25 records are pending user adjudication. This audit checks
   consistency; it does not approve any facet or chunk label.

## 6. Decisions requiring human approval

- **Q020:** Is the benchmark table-specific (require the named Table II.2.1
  row/year/value) or may a narrative passage elsewhere in the same report
  satisfy completeness? Recommended for discussion: preserve table-specific
  retrieval as the primary criterion because the question names the table.
- **Q021:** Does “When can” require all three enumerated grounds or any one
  valid ground? If all three are required, confirm that the marketing limit is
  a qualification on the company-interest ground, not a fourth ground.
- **Q025:** Are compensation and the post-60-day penalty boundary required
  answer facets, contextual consequences, or optional detail for this wording?
  Confirm that the extra 30 days and 60-day total are assessed separately.
- **All questions:** A human reviewer must adjudicate the proposed source
  facets and cited chunks before approval. The proposal's current
  `pending_user_adjudication` state must remain distinct from any future
  approved annotation version.

## 7. Conclusion

The annotation proposal **needs revision before approval**. Q020 has a
verified structure-aware top-10 table row at rank 10 that the proposal
incorrectly omits, and the existing evidence-level CSV also contains
false-positive component matches for other Q020 ranks. Q025 incorrectly marks
fixed-size rank 2 complete against a facet that includes the absent 60-day
boundary. Q021 and Q025 also require explicit human scope decisions.

All other questions' inspected source/page references, proposed facets, and
retrieval completeness claims are consistent with the available artifacts,
including the specified incomplete cases and duplicate-evidence handling.
The 2B.18B quality review report was not found and remains an unavailable
input to this reconciliation.

Only this reconciliation report was created. Original PDFs, manifest,
processed data, chunks, embeddings, vector collections, evaluation questions,
retrieval results, evidence-audit CSV/report, annotation JSONL, annotation
report, and decision sheet were not modified. No commit or push was made.

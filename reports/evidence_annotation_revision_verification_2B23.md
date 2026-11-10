# PolicyLens — Evidence Annotation Revision Verification (Milestone 2B.23)

## 1. Verdict

**VERIFIED_WITH_LIMITATIONS — limited historical-preservation items are not
verifiable.**

The v2 annotation contents, Q020/Q021/Q025 evidence, preserved question
records, report summaries, and pending-review status match the inspected
artifacts and human criteria. No material content discrepancy was found.
However, no reliable pre-revision hash or Git baseline was available for the
top-20 diagnostic or the question-results CSV, so their unchanged status
cannot be independently confirmed. This verdict does not approve any
annotation as ground truth.

## 2. Files inspected

### Versioned proposal and reports

- [`data/evaluation/evidence_annotations_v2.jsonl`](../data/evaluation/evidence_annotations_v2.jsonl)
- [`reports/evidence_annotation_report_v2.md`](evidence_annotation_report_v2.md)
- [`reports/evidence_annotation_decision_sheet_v2.md`](evidence_annotation_decision_sheet_v2.md)
- [`reports/evidence_annotation_revision_2B22.md`](evidence_annotation_revision_2B22.md)
- [`data/evaluation/evidence_annotations_v1.jsonl`](../data/evaluation/evidence_annotations_v1.jsonl)
- [`data/evaluation/evaluation_questions.jsonl`](../data/evaluation/evaluation_questions.jsonl)

### Prior audit and reports

- [`reports/final_evidence_audit_reconciliation.md`](final_evidence_audit_reconciliation.md)
- [`reports/evidence_annotation_report.md`](evidence_annotation_report.md)
- [`reports/evidence_annotation_decision_sheet.md`](evidence_annotation_decision_sheet.md)
- [`reports/evidence_level_relevance_audit.md`](evidence_level_relevance_audit.md)

### Retrieval, chunks, and source pages

- [`data/evaluation/results/retrieval_evaluation_results.json`](../data/evaluation/results/retrieval_evaluation_results.json)
- [`data/evaluation/results/retrieval_evaluation_question_results.csv`](../data/evaluation/results/retrieval_evaluation_question_results.csv)
- [`data/evaluation/results/retrieval_failure_top20_diagnostic.json`](../data/evaluation/results/retrieval_failure_top20_diagnostic.json)
- [`data/evaluation/results/evidence_level_relevance_audit.csv`](../data/evaluation/results/evidence_level_relevance_audit.csv)
- [`data/processed/chunks/fixed_size.jsonl`](../data/processed/chunks/fixed_size.jsonl)
- [`data/processed/chunks/structure_aware.jsonl`](../data/processed/chunks/structure_aware.jsonl)
- Original PDFs: [`doc_036_rbi_annual_report_2023_24.pdf`](../data/pdfs/doc_036_rbi_annual_report_2023_24.pdf), [`doc_016_fair_practice_code_2023.pdf`](../data/pdfs/doc_016_fair_practice_code_2023.pdf), and [`bfl_fair_practice_code.pdf`](../data/pdfs/bfl_fair_practice_code.pdf).

## 3. Validation methodology

- Independently parsed every JSONL record in v1, v2, and the original question
  dataset.
- Compared question IDs, question wording, gold document IDs and gold PDF
  pages; compared v1 and v2 records structurally and semantically.
- Checked all v2 reports against the actual JSONL facets, ranks, status values,
  and complete/incomplete counts.
- Loaded the existing saved retrieval result records and matched cited ranks
  and chunk IDs to the corresponding persisted chunk payloads. No retrieval
  operation was performed.
- Read original PDF pages 41, 3, and 6 using the installed PDF reader;
  inspected the PDF page text and extracted table cells for Q020.
- Compared protected historical artifact SHA-256 values with the pre-revision
  baseline values recorded in the prior session output where available.
- Read the diagnostic JSON and result CSVs for structural validity. Their
  prior hash baselines were not available.

No extraction, OCR, cleaning, chunking, embedding, indexing, retrieval, metric
evaluation, Qdrant operation, or test suite was run.

## 4. Version and preservation audit

### File existence and structure

**VERIFIED:** All four v2 files listed above exist and are readable. The v2
JSONL parses as 25 records with 25 unique IDs (`Q001`–`Q025`). The evaluation
question file also contains 25 unique matching question IDs.

**VERIFIED:** For every ID, the v2 question wording and gold document/page
reference match the original evaluation dataset. The v1 and v2 top-level
record keys are identical; no top-level fields were dropped or renamed.
`schema_version` remains `1.0`.

The optional nested `limitation` property used in Q025's fixed-size supporting
chunk already occurs in the v1 Q020 structure-aware supporting-chunk record.
It is therefore not a new property in the existing proposal format. The
priority facets and completeness values changed only as scoped for Q020,
Q021, and Q025.

**VERIFIED:** Q001–Q019 and Q022–Q024 are semantically identical between v1
and v2. Exactly Q020, Q021, and Q025 differ.

**VERIFIED:** All 25 records retain
`reviewer_status: pending_user_adjudication`. The adjudication-status
distribution is 22 `proposed_requires_user_approval` and 3 `needs_review`.
No record is approved or marked as ground truth.

### All-question preservation checks

For each question below, the original question wording and the stated
`doc_id`/PDF page match between the source evaluation dataset and v2. “Revised
as scoped” means the annotation record changes only for the Milestone 2B.22
decision.

| ID | Original question | Gold source | v1-to-v2 comparison |
|---|---|---|---|
| Q001 | What does Bajaj Finance commit to do when a customer remains dissatisfied after raising a complaint? | doc_001, p. 3 | VERIFIED — unchanged |
| Q002 | What should the lender's acknowledgement tell an applicant about the handling of a loan application? | doc_001, p. 4 | VERIFIED — unchanged |
| Q003 | In what language must borrower communications be provided under this fair-practice code? | doc_001, p. 4 | VERIFIED — unchanged |
| Q004 | What key loan information must Bajaj Finance convey in writing when a loan is sanctioned? | doc_001, p. 4 | VERIFIED — unchanged |
| Q005 | Where must penal charges for late repayment or another borrower default be highlighted? | doc_001, p. 4 | VERIFIED — unchanged |
| Q006 | How must a lender handle changes to loan terms such as the disbursement schedule or interest rate? | doc_001, p. 5 | VERIFIED — unchanged |
| Q007 | When does the code require the lender to release a borrower's securities, and what qualification applies? | doc_001, p. 5 | VERIFIED — unchanged |
| Q008 | What cost information must Tata Capital Housing Finance disclose so a borrower can compare loan offers? | doc_003, p. 4 | VERIFIED — unchanged |
| Q009 | If a change in loan terms disadvantages the customer, what option does Tata Capital Housing Finance provide? | doc_003, p. 5 | VERIFIED — unchanged |
| Q010 | Where must Shriram Finance explain how it grades borrower risk and why different rates are charged? | doc_016, p. 2 | VERIFIED — unchanged |
| Q011 | What governance duties does Shriram Finance's board have for grievance handling and Fair Practice Code compliance? | doc_016, p. 5 | VERIFIED — unchanged |
| Q012 | What repossession safeguards must Shriram Finance include in a vehicle loan agreement? | doc_016, p. 6 | VERIFIED — unchanged |
| Q013 | What must Tata Capital provide and explain to a prospective microfinance borrower before the loan contract is executed? | doc_024, p. 2 | VERIFIED — unchanged |
| Q014 | Where should microfinance repayments normally be collected, and when may field staff collect at a borrower's home or workplace? | doc_024, p. 3 | VERIFIED — unchanged |
| Q015 | What customer protections are objectives of Tata Capital's customer grievance policy? | doc_023, p. 2 | VERIFIED — unchanged |
| Q016 | In Tata Capital's benchmark-rate table, what were the current and revised TCL Retail PLR and the earliest implementation date? | doc_019, p. 2 | VERIFIED — unchanged |
| Q017 | For a RuPay debit-card transaction outside an industry programme, what incentive rate and per-transaction cap does the DFS table specify? | doc_034, p. 1 | VERIFIED — unchanged |
| Q018 | For BHIM-UPI P2M transactions up to ₹2,000 outside industry programmes, what incentive rate is shown in the scheme table? | doc_034, p. 1 | VERIFIED — unchanged |
| Q019 | In Tata Capital's grievance-handling SOP table, what is the maximum turnaround time for tagging a case as QRC after a customer requirement or concern is identified? | doc_023, p. 7 | VERIFIED — unchanged |
| Q020 | In RBI Annual Report Table II.2.1, what growth rate is listed for Gross Fixed Capital Formation in 2023-24? | doc_036, p. 41 | VERIFIED — revised as scoped |
| Q021 | When can the finance company disclose a borrower's personal or transaction information without the borrower's authorization? | doc_016, p. 3 | VERIFIED — revised as scoped |
| Q022 | During microfinance debt collection, which calling hours are prohibited by the fair-practice code? | doc_024, p. 3 | VERIFIED — unchanged |
| Q023 | Before selling or auctioning a repossessed vehicle, what opportunity must the lender's process give the borrower? | doc_016, p. 6 | VERIFIED — unchanged |
| Q024 | May a microfinance lender provide non-credit add-on products without the borrower's agreement, and where must their fees be stated? | doc_024, p. 3 | VERIFIED — unchanged |
| Q025 | If original property papers are lost or damaged after a personal loan is settled, what support and additional time does the code allow? | doc_001, p. 6 | VERIFIED — revised as scoped |

## 5. Q020 — table-specific evidence

**Source evidence — VERIFIED.** On original PDF page 41, the source caption is
“Table II.2.1: Real GDP Growth.” Its year columns include 2023-24, and the
Gross Fixed Capital Formation row is `1.1, -7.1, 17.5, 6.6, 10.2`. The
requested value is 10.2 per cent.

**Retrieved evidence — VERIFIED.** The saved official retrieval result places
`doc_036_structure_aware_00080_da6891873a1b` at structure-aware rank 10. The
chunk is a table payload with page provenance 41. Its structured table
contains the 2019-20 through 2023-24 headings and the complete Gross Fixed
Capital Formation row ending in 10.2. The table caption is visible on the
same source page; the chunk's table rows are linked to that page by their
document/page provenance.

**Completeness — VERIFIED.** The v2 annotation marks structure-aware top 10
complete, covers F1 and F2, and cites rank 10 as DIRECT. Fixed-size top 10 is
incomplete; inspection of its ten saved results found no complete
row/year/value relationship.

**Narrative distinction — VERIFIED.** Structure-aware rank 5,
`doc_036_structure_aware_00058_627c4c142023`, states the 10.2 per cent
figure in narrative text. It is not cited as complete evidence and does not
substitute for retrieval of the named table. Other component-only phrase
matches are likewise insufficient.

The v2 annotation report, decision sheet, and revision report consistently
state this interpretation. No stale claim that structure-aware top 10 lacks
the table row was found in the v2 documents.

## 6. Q021 — disclosure grounds

**Source evidence — VERIFIED.** Original PDF page 3 identifies three
exceptional cases: (1) legal, statutory, or regulatory requirements; (2) a
duty to the public; and (3) company interest, with fraud prevention as an
example and banks, financial institutions, group, or associate companies as
recipients.

The marketing sentence says the company will not use “this reason” to provide
borrower information to anyone else for marketing. In v2 it is attached to
the company-interest ground in F3, not represented as a fourth ground.

**Retrieved evidence — VERIFIED.** Fixed-size rank 2,
`doc_016_fixed_size_00003_d1e3de271923`, and structure-aware rank 1,
`doc_016_structure_aware_00004_15199cc67fa1`, both contain all three grounds,
the stated example/recipients, and the marketing qualification. The v2
completeness records cite those chunks as DIRECT and require F1–F3.

**Cross-artifact consistency — VERIFIED.** The v2 JSONL, annotation report,
decision sheet, and revision report all require three grounds and describe
marketing as a qualification on the third. No fourth ground is introduced.

## 7. Q025 — five independent details

Original PDF page 6 of `doc_001` states assistance with duplicate/certified
copies, associated costs, compensation under clause (i), an additional 30
days, and penalty calculation after 60 days total.

| Facet | Required detail | Fixed-size rank 2 | Structure-aware rank 1 |
|---|---|---|---|
| F1 | Assistance obtaining duplicate/certified copies | VERIFIED — present | VERIFIED — present |
| F2 | Associated costs | VERIFIED — present | VERIFIED — present |
| F3 | Compensation under the preceding clause | VERIFIED — present | VERIFIED — present |
| F4 | Additional 30 days | VERIFIED — present | VERIFIED — present |
| F5 | 60-day total before delayed-period penalty calculation | VERIFIED — absent | VERIFIED — present |

The saved top-10 results place
`doc_001_fixed_size_00005_d577f4089a07` at fixed-size rank 2 and
`doc_001_structure_aware_00005_33a0e3812a93` at structure-aware rank 1.
The fixed-size payload supports F1–F4 but has no 60-day total; the v2 record
marks it PARTIAL and fixed-size top 10 incomplete. The structure-aware payload
contains all five details; the v2 record marks it DIRECT and structure-aware
top 10 complete.

The source loss/damage condition is scenario context, not a counted remedy
facet. Although a similar clause appears in a top-ranked `doc_003` chunk, v2
does not cite that chunk as support for this `doc_001` question. No
cross-issuer evidence is used to establish completeness.

## 8. Report consistency audit

**VERIFIED:** The v2 annotation report's question table agrees with the JSONL:
Q020 fixed-size incomplete/structure-aware complete at rank 10; Q021 complete
at fixed rank 2 and structure-aware rank 1 with three facets; Q025 fixed-size
incomplete with rank 2 partial and structure-aware complete at rank 1.

**VERIFIED:** The report's totals agree with the 25 JSONL records: fixed-size
20 complete/5 incomplete, structure-aware 21 complete/4 incomplete. Its Q025
facet count is five. The decision sheet and revision report agree on the
same ranks, facets, criteria, and pending status.

**VERIFIED:** The revision report's statement that there is no structural
schema change is consistent with the inspection: top-level keys and
`schema_version` are unchanged; the optional `limitation` nested property was
already present in a v1 supporting-chunk record. No unexpected schema key,
field rename, or top-level field deletion was found.

**VERIFIED:** No outdated Q020 incompleteness statement, Q021 fourth-ground
claim, or Q025 combined-facet/fixed-complete claim was found in the three v2
reports. All explicitly distinguish proposal status from approval and
ground-truth status.

## 9. Historical artifact protection

The previous session output recorded pre-revision SHA-256 baselines for the
following files. Each current hash matched that recorded baseline:

| Artifact | Finding |
|---|---|
| `data/evaluation/evidence_annotations_v1.jsonl` | VERIFIED — hash matches |
| `reports/evidence_annotation_report.md` | VERIFIED — hash matches |
| `reports/evidence_annotation_decision_sheet.md` | VERIFIED — hash matches |
| `reports/final_evidence_audit_reconciliation.md` | VERIFIED — hash matches |
| `reports/evidence_level_relevance_audit.md` | VERIFIED — hash matches |
| `data/evaluation/results/evidence_level_relevance_audit.csv` | VERIFIED — hash matches |
| `data/evaluation/results/retrieval_evaluation_results.json` | VERIFIED — hash matches |

No reliable pre-revision hash was recorded for
`data/evaluation/results/retrieval_failure_top20_diagnostic.json` or
`data/evaluation/results/retrieval_evaluation_question_results.csv`, and no
tracked Git baseline was available for those untracked artifacts.
**NOT_VERIFIABLE:** Their current JSON/CSV syntax and readability were
confirmed (five diagnostic question records, 50 retrieval result records,
and 50 question-result CSV rows), but unchanged status cannot be claimed.

## 10. Findings classification and limitations

| Finding area | Classification | Result |
|---|---|---|
| Four v2 files exist and are readable | VERIFIED | All present. |
| JSONL structural validity and record IDs | VERIFIED | 25 valid records, 25 unique IDs Q001–Q025. |
| Question text and gold source/page references | VERIFIED | Match the original evaluation questions for all 25 records. |
| v1-to-v2 scope | VERIFIED | Only Q020, Q021, Q025 differ; other 22 records are semantically unchanged. |
| Q020 source, rank, structured row, and completeness | VERIFIED | Structure-aware r10 complete; fixed-size top 10 incomplete; r5 narrative is not table evidence. |
| Q021 source grounds and retrieval support | VERIFIED | Three grounds required; marketing limitation attached to ground three; both cited chunks support them. |
| Q025 source facets and retrieval support | VERIFIED | Fixed r2 supports F1–F4 only; structure r1 supports F1–F5; other issuer not credited. |
| V2 report/JSONL consistency | VERIFIED | Facets, ranks, counts, and pending-status descriptions agree. |
| V1 and historical files with recorded baselines | VERIFIED | All seven compared hashes match. |
| Top-20 diagnostic and question-results CSV unchanged | NOT_VERIFIABLE | No reliable pre-revision hash or tracked baseline is available. |
| Annotation approval / ground-truth status | VERIFIED | No approval: 25 records remain pending user adjudication. |

The separate Milestone 2B.18B report was previously reported missing; this
verification did not reconstruct or claim to inspect it. No independent second
reviewer adjudicated the proposed labels. Hash equality establishes
byte-for-byte preservation only for the artifacts with recorded baselines;
it does not establish historical preservation for files without baselines.

## 11. Final conclusion

**VERIFIED_WITH_LIMITATIONS.** The actual v2 JSONL, source pages, persisted
ranked results, chunk payloads, and companion reports support the Q020, Q021,
and Q025 human criteria. All 25 question/source references are preserved,
the other 22 records are unchanged, the report summaries agree with the data,
and the annotations remain pending—not approved ground truth.

The limited unresolved preservation finding is that unchanged status cannot
be independently proven for the top-20 diagnostic and question-results CSV
without a pre-revision baseline. No editing or regeneration was performed
during this verification; this report is the only file created.

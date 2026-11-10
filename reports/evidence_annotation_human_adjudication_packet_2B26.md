# Evidence Annotation Human Adjudication Packet — Milestone 2B.26

## Purpose and status

This is a **human decision document**, not an approved dataset or ground truth. The authoritative proposal remains `data/evaluation/evidence_annotations_v3.jsonl`; it is unchanged. The human-approved 2B.24R revision decisions for Q001, Q005, Q009, and Q012 are preserved as revision criteria, not reopened for repetition. Those decisions do not approve any remaining annotations as ground truth. Every question-level disposition and both retrieval-completeness decisions below remain pending explicit human review.

Ranks and chunk quotations below are from saved retrieval results and saved chunk payloads. Quoted snippets are verbatim text/table-payload excerpts. Chunk page spans are stored PDF page numbers/page provenance; v3 source references are PDF page numbers. A rank above 10 is shown as diagnostic evidence only and never counts toward top-10 completeness.

## Reviewer instructions and safeguards

- For each question choose `APPROVE_AS_PROPOSED`, `REVISE`, or `NEEDS_MORE_EVIDENCE`; keep it `PENDING_HUMAN_DECISION` until the human acts.
- Decide separately whether to accept the fixed-size and structure-aware completeness labels. Completeness is aggregate facet coverage across that strategy’s top 10, not a requirement that every cited chunk contain every facet.
- Assess each chunk only for the facet IDs attached to it. Do not infer support from page overlap, a different chunk, or aggregate evidence.
- `DIRECT`, `PARTIAL`, and `CONTEXTUAL` are v3 labels. A `PARTIAL` chunk may support an explicitly listed facet while leaving another required facet uncovered.
- Diagnostic ranks above 10 do not change top-10 completeness. Overlapping excerpts are not independent confirmations.
- Review facets that combine independently assessable elements, repeat prompt context, have unclear excerpt support, or raise source/issuer questions.

## Proposal summary

- Questions: **25** (Q001–Q025).
- Required facets: **62**.
- Fixed-size: **21 complete / 4 incomplete.
- Structure-aware: **22 complete / 3 incomplete.
- V3 reviewer status: 25/25 records are `pending_user_adjudication`.

## Sources inspected

- `data/evaluation/evidence_annotations_v3.jsonl`; `data/evaluation/evaluation_questions.jsonl`.
- `data/processed/chunks/fixed_size.jsonl`; `data/processed/chunks/structure_aware.jsonl`.
- `data/evaluation/results/retrieval_evaluation_results.json`; `data/evaluation/results/retrieval_failure_top20_diagnostic.json`.
- `reports/evidence_annotation_report_v3.md`; `reports/evidence_annotation_decision_sheet_v3.md`; `reports/evidence_annotation_revision_verification_2B24S.md`; `reports/final_evidence_audit_reconciliation_2B25.md`.
- Original PDFs are identified by v3 source references and prior source verification. No extraction/OCR or retrieval was rerun for this packet.

## Q001 — What does Bajaj Finance commit to do when a customer remains dissatisfied after raising a complaint?

- **Canonical gold reference(s):** doc_001 PDF pages [3] (PDF page indices [2]).
- **Facets:** 1. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Tell the customer how to take the complaint forward if still dissatisfied. | doc_001, PDF p. [3]: “Telling customers' how to take their complaint forward if they are still not satisfied.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1.**
- **Rank 1 — `doc_001_fixed_size_00001_aee405d33739`; DIRECT evidence; assigned facets: F1.** Saved result rank: 1; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 1–4; page provenance: 1, 2, 3, 4.
  - **F1 payload excerpt:** “Telling customers' how to take their complaint forward if they are still not satisﬁed iv.”
  - V3 annotation rationale: Contains the page-3 commitment: tell customers how to take the complaint forward if still dissatisfied.

**Structure-aware: `COMPLETE`; v3 covered facets: F1.**
- **Rank 1 — `doc_001_structure_aware_00001_ac782e3816d0`; DIRECT evidence; assigned facets: F1.** Saved result rank: 1; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 1–3; page provenance: 1, 2, 3.
  - **F1 payload excerpt:** “Telling customers' how to take their complaint forward if they are still not satisﬁed iv.”
  - V3 annotation rationale: Contains the page-3 commitment: tell customers how to take the complaint forward if still dissatisfied.

### Known concern / review safeguard

Prior v2 incomplete labels were a false negative. Approved 2B.24R and independent 2B.24S verify both direct rank-1 commitments; confirm the quoted wording and source attribution.

### Previously approved revision criteria retained

Both rank-1 chunks directly support the complaint-forwarding commitment.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q002 — What should the lender's acknowledgement tell an applicant about the handling of a loan application?

- **Canonical gold reference(s):** doc_001 PDF pages [4] (PDF page indices [3]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | The acknowledgement confirms receipt of the loan application. | doc_001, PDF p. [4]: “acknowledgement for receipt of loan applications” |
| F2 | The acknowledgement states the time frame within which the application will be disposed of. | doc_001, PDF p. [4]: “The time frame within which loan applications will be disposed of will be indicated in the acknowledgement.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 3 — `doc_001_fixed_size_00003_0bf6f42069fa`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 3; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “c) The Company will have a system of giving acknowledgement for receipt of loan applications.”
  - **F2 payload excerpt:** “time frame within which loan applications will be disposed of will be indicated in the acknowledgement.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 3 — `doc_001_structure_aware_00003_ad7599361f91`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 3; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “c) The Company will have a system of giving acknowledgement for receipt of loan applications.”
  - **F2 payload excerpt:** “time frame within which loan applications will be disposed of will be indicated in the acknowledgement.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q003 — In what language must borrower communications be provided under this fair-practice code?

- **Canonical gold reference(s):** doc_001 PDF pages [4] (PDF page indices [3]).
- **Facets:** 1. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | All borrower communications must be in the vernacular language or a language the borrower understands. | doc_001, PDF p. [4]: “All communications to the borrower shall be in the vernacular language or a language as understood by the borrower.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1.**
- **Rank 7 — `doc_001_fixed_size_00003_0bf6f42069fa`; DIRECT evidence; assigned facets: F1.** Saved result rank: 7; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “a) All communications to the borrower shall be in the vernacular language or a language as understood by the borrower.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1.**
- **Rank 4 — `doc_001_structure_aware_00003_ad7599361f91`; DIRECT evidence; assigned facets: F1.** Saved result rank: 4; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “a) All communications to the borrower shall be in the vernacular language or a language as understood by the borrower.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q004 — What key loan information must Bajaj Finance convey in writing when a loan is sanctioned?

- **Canonical gold reference(s):** doc_001 PDF pages [4] (PDF page indices [3]).
- **Facets:** 4. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Communicate the information in writing, in the vernacular language, by sanction letter or otherwise. | doc_001, PDF p. [4]: “convey in writing to the borrower in the vernacular language by means of sanction letter or otherwise” |
| F2 | State the amount of loan sanctioned. | doc_001, PDF p. [4]: “the amount of loan sanctioned” |
| F3 | State terms and conditions, including annualized interest rate. | doc_001, PDF p. [4]: “the terms and conditions including annualised rate of interest” |
| F4 | State the method of application of the interest rate. | doc_001, PDF p. [4]: “method of application thereof” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3, F4.**
- **Rank 4 — `doc_001_fixed_size_00003_0bf6f42069fa`; DIRECT evidence; assigned facets: F1, F2, F3, F4.** Saved result rank: 4; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “The Company will convey in writing to the borrower in the vernacular language by means of sanction letter or otherwise, the amount of loan sanctioned along with the terms and conditions including annualised rate”
  - **F2 payload excerpt:** “The Company will convey in writing to the borrower in the vernacular language by means of sanction letter or otherwise, the amount of loan sanctioned along with the terms and conditions including annualised rate”
  - **F3 payload excerpt:** “terms and conditions including annualised rate of interest”
  - **F4 payload excerpt:** “including annualised rate of interest and method of application thereof”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3, F4.**
- **Rank 7 — `doc_001_structure_aware_00003_ad7599361f91`; DIRECT evidence; assigned facets: F1, F2, F3, F4.** Saved result rank: 7; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “The Company will convey in writing to the borrower in the vernacular language by means of sanction letter or otherwise, the amount of loan sanctioned along with the terms and conditions including annualised rate”
  - **F2 payload excerpt:** “The Company will convey in writing to the borrower in the vernacular language by means of sanction letter or otherwise, the amount of loan sanctioned along with the terms and conditions including annualised rate”
  - **F3 payload excerpt:** “terms and conditions including annualised rate of interest”
  - **F4 payload excerpt:** “including annualised rate of interest and method of application thereof”

### Known concern / review safeguard

2B.21 warned of page-overlap false-positive risk and later-rank evidence. Current v3 cites rank 4 in each strategy; assess the actual excerpt, not page overlap.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q005 — Where must penal charges for late repayment or another borrower default be highlighted?

- **Canonical gold reference(s):** doc_001 PDF pages [4] (PDF page indices [3]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F3 | The penal charge must be stated in bold. | doc_001, PDF p. [4]: “in bold” |
| F4 | The penal charge must be stated in the loan agreement. | doc_001, PDF p. [4]: “in bold in the loan agreement” |

### Saved top-10 evidence

**Fixed-size: `INCOMPLETE`; v3 covered facets: F4.**
- **Rank 5 — `doc_001_fixed_size_00004_785fedf70295`; PARTIAL evidence; assigned facets: F4.** Saved result rank: 5; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F4 payload excerpt:** “The quantum and reason for penal charges shall be clearly disclosed by the Company to the customers in the loan agreement and most important terms & conditions / Key Fact Statement (KFS) as applicable.”
  - V3 annotation rationale: Fully supports the loan-agreement location facet through the disclosure-in-the-loan-agreement text; does not state that the charge must be bold, so F3 is not covered.

**Structure-aware: `INCOMPLETE`; v3 covered facets: F4.**
- **Rank 6 — `doc_001_structure_aware_00004_288632361e39`; PARTIAL evidence; assigned facets: F4.** Saved result rank: 6; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F4 payload excerpt:** “The quantum and reason for penal charges shall be clearly disclosed by the Company to the customers in the loan agreement and most important terms & conditions / Key Fact Statement (KFS) as applicable.”
  - V3 annotation rationale: Fully supports the loan-agreement location facet through the disclosure-in-the-loan-agreement text; does not state that the charge must be bold, so F3 is not covered.

### Diagnostic evidence outside top 10 — excluded from completeness

- **Fixed Size rank 19 — `doc_001_fixed_size_00003_0bf6f42069fa`; DIRECT; diagnostic status `complete`; facets F3, F4.**
  - Source `doc_001`, chunk PDF pages 3–4; payload excerpt: “The Company will mention the penal charge which will be charged for late repayment and / or any other default on the part of the customer, in bold in the loan agreement.”
  - Outside top 10; not counted toward completeness.
- **Structure Aware rank 17 — `doc_001_structure_aware_00003_ad7599361f91`; DIRECT; diagnostic status `complete`; facets F3, F4.**
  - Source `doc_001`, chunk PDF pages 3–4; payload excerpt: “The Company will mention the penal charge which will be charged for late repayment and / or any other default on the part of the customer, in bold in the loan agreement.”
  - Outside top 10; not counted toward completeness.

### Known concern / review safeguard

Approved revision: late/default scenario is context, not a required answer facet; bolding and loan-agreement location remain separate. Only F4 is covered in top 10; cited chunks are PARTIAL overall and diagnostic full evidence is outside top 10.

### Previously approved revision criteria retained

Context is excluded; F3 bolding and F4 loan-agreement location are separate; only fully supported facets count as covered.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (incomplete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (incomplete):** `PENDING_HUMAN_DECISION`

## Q006 — How must a lender handle changes to loan terms such as the disbursement schedule or interest rate?

- **Canonical gold reference(s):** doc_001 PDF pages [5] (PDF page indices [4]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Give notice to the borrower, in the vernacular language, of changes to terms including disbursement schedule and interest rates. | doc_001, PDF p. [5]: “give notice to the borrower in the vernacular language of any change in the terms and conditions including disbursement schedule, interest rates” |
| F2 | Changes in interest rates and charges take effect only prospectively. | doc_001, PDF p. [5]: “changes in interest rates and charges are effected only prospectively” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 3 — `doc_001_fixed_size_00004_785fedf70295`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 3; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F1 payload excerpt:** “a) The Company will give notice to the borrower in the vernacular language of any change in the terms and conditions including disbursement schedule, interest rates, service charges, prepayment charges etc.”
  - **F2 payload excerpt:** “The Company will also ensure that changes in interest rates and charges are effected only prospectively.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 4 — `doc_001_structure_aware_00004_288632361e39`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 4; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F1 payload excerpt:** “a) The Company will give notice to the borrower in the vernacular language of any change in the terms and conditions including disbursement schedule, interest rates, service charges, prepayment charges etc.”
  - **F2 payload excerpt:** “The Company will also ensure that changes in interest rates and charges are effected only prospectively.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q007 — When does the code require the lender to release a borrower's securities, and what qualification applies?

- **Canonical gold reference(s):** doc_001 PDF pages [5] (PDF page indices [4]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Release all securities on repayment of all dues or realization of the outstanding loan amount. | doc_001, PDF p. [5]: “release all securities on repayment of all dues or on realisation of the outstanding amount of loan” |
| F2 | Release is subject to any legitimate right or lien for another claim. | doc_001, PDF p. [5]: “subject to any legitimate right or lien for any other claim” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 7 — `doc_001_fixed_size_00004_785fedf70295`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 7; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F1 payload excerpt:** “The Company will release all securities on repayment of all dues or on realisation of the outstanding amount of loan subject to any legitimate right or lien for any other claim the Company may have against borrower.”
  - **F2 payload excerpt:** “The Company will release all securities on repayment of all dues or on realisation of the outstanding amount of loan subject to any legitimate right or lien for any other claim the Company may have against borrower.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 4 — `doc_001_structure_aware_00004_288632361e39`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 4; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F1 payload excerpt:** “The Company will release all securities on repayment of all dues or on realisation of the outstanding amount of loan subject to any legitimate right or lien for any other claim the Company may have against borrower.”
  - **F2 payload excerpt:** “The Company will release all securities on repayment of all dues or on realisation of the outstanding amount of loan subject to any legitimate right or lien for any other claim the Company may have against borrower.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q008 — What cost information must Tata Capital Housing Finance disclose so a borrower can compare loan offers?

- **Canonical gold reference(s):** doc_003 PDF pages [4] (PDF page indices [3]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan. | doc_003, PDF p. [4]: “disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application” |
| F2 | Disclose costs transparently and ensure charges/fees are non-discriminatory. | doc_003, PDF p. [4]: “in a transparent manner. It shall also be ensured that such charges/fees are non-discriminatory.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 1 — `doc_003_fixed_size_00005_96b0d302eff6`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 1; source `doc_003` (Tata Capital Housing Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F1 payload excerpt:** “Thus, we shall disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application in a transparent manner.”
  - **F2 payload excerpt:** “Thus, we shall disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application in a transparent manner. It shall also be ensured that such charges/fees are non-discriminatory.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 2 — `doc_003_structure_aware_00005_a9d262541873`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 2; source `doc_003` (Tata Capital Housing Finance Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “Thus, we shall disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application in a transparent manner.”
  - **F2 payload excerpt:** “Thus, we shall disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application in a transparent manner. It shall also be ensured that such charges/fees are non-discriminatory.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q009 — If a change in loan terms disadvantages the customer, what option does Tata Capital Housing Finance provide?

- **Canonical gold reference(s):** doc_003 PDF pages [5] (PDF page indices [4]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F2 | Within 60 days and without notice, the customer may close the account or switch it. | doc_003, PDF p. [5]: “within 60 days and without notice close his / her account or switch it” |
| F3 | Closing or switching must not require extra charges or interest. | doc_003, PDF p. [5]: “without having to pay any extra charges or interest” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F2, F3.**
- **Rank 2 — `doc_003_fixed_size_00006_8bf99111838c`; DIRECT evidence; assigned facets: F2, F3.** Saved result rank: 2; source `doc_003` (Tata Capital Housing Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F2 payload excerpt:** “If such change is to the disadvantage of the customer, he/she may within 60 days and without notice close his / her account or switch it without having to pay”
  - **F3 payload excerpt:** “without having to pay any extra charges or interest.”

**Structure-aware: `COMPLETE`; v3 covered facets: F2, F3.**
- **Rank 4 — `doc_003_structure_aware_00006_f9c845e0a416`; DIRECT evidence; assigned facets: F2, F3.** Saved result rank: 4; source `doc_003` (Tata Capital Housing Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F2 payload excerpt:** “If such change is to the disadvantage of the customer, he/she may within 60 days and without notice close his / her account or switch it without having to pay”
  - **F3 payload excerpt:** “without having to pay any extra charges or interest.”

### Known concern / review safeguard

Approved revision: disadvantage trigger is question context; answer facets are the 60-day/no-notice close-or-switch option and no extra charges/interest.

### Previously approved revision criteria retained

Disadvantage trigger is context; F2 is the 60-day/no-notice close-or-switch option; F3 is no extra charges/interest.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q010 — Where must Shriram Finance explain how it grades borrower risk and why different rates are charged?

- **Canonical gold reference(s):** doc_016 PDF pages [2] (PDF page indices [1]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | The loan application form and sanction letter disclose the risk-gradation approach and rationale for different interest rates across borrower categories. | doc_016, PDF p. [2]: “The loan application form and the sanction letter issued to the customer shall disclose the approach for gradation of risks and rationale for charging different rates of interest to different categories of borrowers” |
| F2 | The same information is available on the company website or published in relevant newspapers. | doc_016, PDF p. [2]: “made available on the web-site of the Company or published in the relevant newspapers” |

### Saved top-10 evidence

**Fixed-size: `INCOMPLETE`; v3 covered facets: none.**
No chunk is credited for a required facet in the saved v3 top-10 annotation. Same-document/page overlap alone is not answer evidence.

**Structure-aware: `INCOMPLETE`; v3 covered facets: none.**
No chunk is credited for a required facet in the saved v3 top-10 annotation. Same-document/page overlap alone is not answer evidence.

### Diagnostic evidence outside top 10 — excluded from completeness

- **Structure Aware rank 18 — `doc_016_structure_aware_00003_6a9423992e87`; DIRECT; diagnostic status `complete`; facets F1, F2.**
  - Source `doc_016`, chunk PDF pages 2–2; payload excerpt: “The loan application form and the sanction letter issued to the customer shall disclose the approach for gradation of risks and rationale for charging different rates of interest to different categories of borrowers and the same shall also be made available on the web-site of the Company or published in the relevant newspapers.”
  - Outside top 10; not counted toward completeness.

### Known concern / review safeguard

Earlier audit found generic website wording insufficient; structure-aware evidence is rank 18, outside top 10. Both top-10 labels remain incomplete.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (incomplete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (incomplete):** `PENDING_HUMAN_DECISION`

## Q011 — What governance duties does Shriram Finance's board have for grievance handling and Fair Practice Code compliance?

- **Canonical gold reference(s):** doc_016 PDF pages [5] (PDF page indices [4]).
- **Facets:** 3. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level. | doc_016, PDF p. [5]: “lay down the appropriate grievance redressal mechanism ... disputes ... heard and disposed of at least at the next higher level” |
| F2 | Provide for periodic review of FPC compliance and grievance-mechanism functioning at management levels. | doc_016, PDF p. [5]: “periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management” |
| F3 | Submit a consolidated report of reviews to the Board at prescribed regular intervals. | doc_016, PDF p. [5]: “A consolidated report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 5 — `doc_016_fixed_size_00005_92e15d19bd51`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 5; source `doc_016` (Shriram Finance Limited), chunk PDF pages 4–5; page provenance: 4, 5.
  - **F1 payload excerpt:** “The Board of Directors of the Company shall lay down the appropriate grievance redressal mechanism within the organization. Such a mechanism shall ensure that all disputes arising out of the decisions of Company’s functionaries are heard and disposed of at least at the next higher level.”
  - **F2 payload excerpt:** “(b) The Board of Directors shall also provide for periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management.”
  - **F3 payload excerpt:** “report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 8 — `doc_016_structure_aware_00006_d4c341ea43e2`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 8; source `doc_016` (Shriram Finance Limited), chunk PDF pages 5–5; page provenance: 5.
  - **F1 payload excerpt:** “The Board of Directors of the Company shall lay down the appropriate grievance redressal mechanism within the organization. Such a mechanism shall ensure that all disputes arising out of the decisions of Company’s functionaries are heard and disposed of at least at the next higher level.”
  - **F2 payload excerpt:** “(b) The Board of Directors shall also provide for periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management.”
  - **F3 payload excerpt:** “report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q012 — What repossession safeguards must Shriram Finance include in a vehicle loan agreement?

- **Canonical gold reference(s):** doc_016 PDF pages [6] (PDF page indices [5]).
- **Facets:** 7. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | The repossession clause must be legally enforceable and included in the contract/loan agreement. | doc_016, PDF p. [6]: “re-possession clause in the contract/ loan agreement with the borrower which must be legally enforceable” |
| F2 | State the notice period before taking possession. | doc_016, PDF p. [6]: “Notice period before taking possession” |
| F6 | State the circumstances in which the notice period before taking possession may be waived. | doc_016, PDF p. [6]: “Circumstances under which the notice period can be waived” |
| F3 | State the procedure for taking possession of the security. | doc_016, PDF p. [6]: “The procedure for taking possession of the security” |
| F4 | Provide a final opportunity to repay before sale/auction. | doc_016, PDF p. [6]: “final chance to be given to the borrower for repayment of loan before the sale / auction” |
| F5 | State the procedure for returning possession to the borrower. | doc_016, PDF p. [6]: “The procedure for giving repossession to the borrower” |
| F7 | State the procedure for sale or auction of the property. | doc_016, PDF p. [6]: “The procedure for sale / auction of the property” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3, F4, F5, F6, F7.**
- **Rank 4 — `doc_016_fixed_size_00006_5707a2baee10`; DIRECT evidence; assigned facets: F1, F2, F3, F4, F5, F6, F7.** Saved result rank: 4; source `doc_016` (Shriram Finance Limited), chunk PDF pages 5–6; page provenance: 5, 6.
  - **F1 payload excerpt:** “The Company has included re-possession clause in the contract/ loan agreement with the borrower which must be legally enforceable.”
  - **F2 payload excerpt:** “Notice period before taking possession;”
  - **F3 payload excerpt:** “The procedure for taking possession of the security;”
  - **F4 payload excerpt:** “A provision regarding final chance to be given to the borrower for repayment of loan before the sale / auction of the property;”
  - **F5 payload excerpt:** “The procedure for giving repossession to the borrower;”
  - **F6 payload excerpt:** “Circumstances under which the notice period can be waived;”
  - **F7 payload excerpt:** “The procedure for sale / auction of the property.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3, F4, F5, F6, F7.**
- **Rank 2 — `doc_016_structure_aware_00007_3562949c7e7a`; DIRECT evidence; assigned facets: F1, F2, F3, F4, F5, F6, F7.** Saved result rank: 2; source `doc_016` (Shriram Finance Limited), chunk PDF pages 6–6; page provenance: 6.
  - **F1 payload excerpt:** “The Company has included re-possession clause in the contract/ loan agreement with the borrower which must be legally enforceable.”
  - **F2 payload excerpt:** “Notice period before taking possession;”
  - **F3 payload excerpt:** “The procedure for taking possession of the security;”
  - **F4 payload excerpt:** “A provision regarding final chance to be given to the borrower for repayment of loan before the sale / auction of the property;”
  - **F5 payload excerpt:** “The procedure for giving repossession to the borrower;”
  - **F6 payload excerpt:** “Circumstances under which the notice period can be waived;”
  - **F7 payload excerpt:** “The procedure for sale / auction of the property.”

### Previously approved revision criteria retained

Seven distinct safeguards remain separate: enforceable contract clause; notice period; waiver circumstances; taking-possession procedure; final repayment opportunity; return-of-possession procedure; sale/auction procedure.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q013 — What must Tata Capital provide and explain to a prospective microfinance borrower before the loan contract is executed?

- **Canonical gold reference(s):** doc_024 PDF pages [2] (PDF page indices [1]).
- **Facets:** 3. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Provide a standardized Key Facts Statement to all prospective borrowers before contract execution. | doc_024, PDF p. [2]: “provide a Key Facts Statement (KFS) to all prospective borrowers ... before executing the loan contract, as per the standardised format” |
| F2 | Write the KFS in a language understood by the borrower. | doc_024, PDF p. [2]: “The KFS shall be written in a language understood by such borrowers.” |
| F3 | Explain the contents of the KFS and obtain borrower acknowledgement. | doc_024, PDF p. [2]: “Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_024_fixed_size_00002_15bb2fdc5f67`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_024` (Tata Capital Limited), chunk PDF pages 1–2; page provenance: 1, 2.
  - **F1 payload excerpt:** “(b) The Company shall provide a Key Facts Statement (KFS) to all prospective borrowers to help them take an informed view before executing the loan contract, as per the standardised format.”
  - **F2 payload excerpt:** “language understood by such borrowers.”
  - **F3 payload excerpt:** “Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained that he/she has understood the same.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_024_structure_aware_00002_c7c2c87cf73a`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_024` (Tata Capital Limited), chunk PDF pages 1–2; page provenance: 1, 2.
  - **F1 payload excerpt:** “(b) The Company shall provide a Key Facts Statement (KFS) to all prospective borrowers to help them take an informed view before executing the loan contract, as per the standardised format.”
  - **F2 payload excerpt:** “language understood by such borrowers.”
  - **F3 payload excerpt:** “Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained that he/she has understood the same.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q014 — Where should microfinance repayments normally be collected, and when may field staff collect at a borrower's home or workplace?

- **Canonical gold reference(s):** doc_024 PDF pages [3] (PDF page indices [2]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Ordinarily, collect at a designated/central place mutually decided by borrower and company. | doc_024, PDF p. [3]: “Recovery shall be made at a designated/central place decided mutually by the borrower and the Company.” |
| F2 | Field staff may collect at the borrower's residence/work only if the borrower fails to appear at the designated place on two or more successive occasions. | doc_024, PDF p. [3]: “if the borrower fails to appear at the designated/ central designated place on two or more successive occasions ... at the place of residence or work” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 5 — `doc_024_fixed_size_00004_e6145695ee32`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 5; source `doc_024` (Tata Capital Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “(b) Recovery shall be made at a designated/central place decided mutually by the borrower and the Company.”
  - **F2 payload excerpt:** “However, field staff shall be allowed to make recovery at the place of residence or work of the borrower if the borrower fails to appear at the designated/ central designated place on two or more successive occasions.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 2 — `doc_024_structure_aware_00004_ea79c085f5a8`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 2; source `doc_024` (Tata Capital Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “(b) Recovery shall be made at a designated/central place decided mutually by the borrower and the Company.”
  - **F2 payload excerpt:** “However, field staff shall be allowed to make recovery at the place of residence or work of the borrower if the borrower fails to appear at the designated/ central designated place on two or more successive occasions.”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q015 — What customer protections are objectives of Tata Capital's customer grievance policy?

- **Canonical gold reference(s):** doc_023 PDF pages [2] (PDF page indices [1]).
- **Facets:** 3. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Treat all customers fairly and without bias. | doc_023, PDF p. [2]: “All customers are always treated fairly and without bias” |
| F2 | Address customer issues courteously and resolve them on time. | doc_023, PDF p. [2]: “All issues raised by customers are dealt with courtesy and resolved on time” |
| F3 | Make customers aware of their rights and alternative remedies if dissatisfied with the response/resolution. | doc_023, PDF p. [2]: “Customers are made completely aware of their rights so that they can opt for alternative remedies if they are not fully satisfied” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_023_fixed_size_00002_1f9f6e67ac59`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_023` (Tata Capital Limited), chunk PDF pages 1–3; page provenance: 1, 2, 3.
  - **F1 payload excerpt:** “All customers are always treated fairly and without bias •”
  - **F2 payload excerpt:** “All issues raised by customers are dealt with courtesy and resolved on time •”
  - **F3 payload excerpt:** “Customers are made completely aware of their rights so that they can opt for alternative remedies if they are not fully satisfied with our response or resolution to their complaint”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_023_structure_aware_00002_8dc9d4739e5b`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_023` (Tata Capital Limited), chunk PDF pages 1–2; page provenance: 1, 2.
  - **F1 payload excerpt:** “All customers are always treated fairly and without bias •”
  - **F2 payload excerpt:** “All issues raised by customers are dealt with courtesy and resolved on time •”
  - **F3 payload excerpt:** “Customers are made completely aware of their rights so that they can opt for alternative remedies if they are not fully satisfied with our response or resolution to their complaint”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q016 — In Tata Capital's benchmark-rate table, what were the current and revised TCL Retail PLR and the earliest implementation date?

- **Canonical gold reference(s):** doc_019 PDF pages [2] (PDF page indices [1]).
- **Facets:** 1. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Identify the TCL Retail PLR row, current value 11.50%, revised value 11.75%, and earliest implementation date 01-Nov-26. | doc_019, PDF p. [2]: “TCL Retail PLR (“TCL RPLR”) \| 11.50% \| 11.75% \| 01-Nov-26” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1.**
- **Rank 1 — `doc_019_fixed_size_00003_c97da965ff31`; DIRECT evidence; assigned facets: F1.** Saved result rank: 1; source `doc_019` (Tata Capital Limited), chunk PDF pages 2–2; page provenance: 2.
  - **F1 payload excerpt:** “TCL Retail PLR (“TCL RPLR”) | 11.50% | 11.75% | 01-Nov-26”

**Structure-aware: `COMPLETE`; v3 covered facets: F1.**
- **Rank 1 — `doc_019_structure_aware_00003_2fe8e4668967`; DIRECT evidence; assigned facets: F1.** Saved result rank: 1; source `doc_019` (Tata Capital Limited), chunk PDF pages 2–2; page provenance: 2.
  - **F1 payload excerpt:** “TCL Retail PLR (“TCL RPLR”) | 11.50% | 11.75% | 01-Nov-26”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q017 — For a RuPay debit-card transaction outside an industry programme, what incentive rate and per-transaction cap does the DFS table specify?

- **Canonical gold reference(s):** doc_034 PDF pages [1] (PDF page indices [0]).
- **Facets:** 4. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Select the RuPay Debit Card POS/e-commerce transaction row. | doc_034, PDF p. [1]: “Transactions using RuPay Debit Cards at point-of-sale (PoS) and through e-commerce (ecom)” |
| F2 | Select the Other than industry programmes category. | doc_034, PDF p. [1]: “Other than industry programmes” |
| F3 | Report the incentive rate as 0.40%. | doc_034, PDF p. [1]: “0.40%” |
| F4 | Report the cap as ₹100 per transaction. | doc_034, PDF p. [1]: “capped at ₹ 100” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3, F4.**
- **Rank 1 — `doc_034_fixed_size_00001_9402fb448062`; DIRECT evidence; assigned facets: F1, F2, F3, F4.** Saved result rank: 1; source `doc_034` (Department of Financial Services, Ministry of Finance), chunk PDF pages 1–1; page provenance: 1.
  - **F1 payload excerpt:** “Transactions using RuPay Debit Cards at point-of-sale (PoS) and through e-commerce (ecom)”
  - **F2 payload excerpt:** “Other than industry programmes”
  - **F3 payload excerpt:** “0.40%, capped at ₹ 100”
  - **F4 payload excerpt:** “0.40%, capped at ₹ 100”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3, F4.**
- **Rank 1 — `doc_034_structure_aware_00001_edcae9ae118c`; DIRECT evidence; assigned facets: F1, F2, F3, F4.** Saved result rank: 1; source `doc_034` (Department of Financial Services, Ministry of Finance), chunk PDF pages 1–1; page provenance: 1.
  - **F1 payload excerpt:** “Transactions using RuPay Debit Cards at point-of-sale (PoS) and through e-commerce (ecom)”
  - **F2 payload excerpt:** “Other than industry programmes”
  - **F3 payload excerpt:** “0.40%, capped at ₹ 100”
  - **F4 payload excerpt:** “0.40%, capped at ₹ 100”
- **Rank 3 — `doc_034_structure_aware_00008_449aab87e17b`; DIRECT evidence; assigned facets: F1, F2, F3, F4.** Saved result rank: 3; source `doc_034` (Department of Financial Services, Ministry of Finance), chunk PDF pages 6–6; page provenance: 6.
  - **F1 payload excerpt:** “RuPay Debit Card transactions” and, in that table’s left-hand row, “1. | Other than Industry Programme s | 0.40% (Max. ₹ 100 per Txn.)”
  - **F2 payload excerpt:** “1. | Other than Industry Programme s | 0.40% (Max. ₹ 100 per Txn.)” (left-hand RuPay table columns, not the parallel BHIM-UPI columns).
  - **F3 payload excerpt:** “1. | Other than Industry Programme s | 0.40% (Max. ₹ 100 per Txn.)”
  - **F4 payload excerpt:** “1. | Other than Industry Programme s | 0.40% (Max. ₹ 100 per Txn.)”

### Known concern / review safeguard

Earlier phrase-based matching missed structured table-cell evidence. Verify row/category/value alignment, not an isolated phrase.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q018 — For BHIM-UPI P2M transactions up to ₹2,000 outside industry programmes, what incentive rate is shown in the scheme table?

- **Canonical gold reference(s):** doc_034 PDF pages [1] (PDF page indices [0]).
- **Facets:** 3. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Select BHIM-UPI P2M transactions up to ₹2,000. | doc_034, PDF p. [1]: “BHIM-UPI P2M transactions (up to ₹ 2,000)” |
| F2 | Select the Other than industry programmes category. | doc_034, PDF p. [1]: “Other than industry programmes” |
| F3 | Report the incentive rate as 0.25%. | doc_034, PDF p. [1]: “0.25%” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_034_fixed_size_00001_9402fb448062`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_034` (Department of Financial Services, Ministry of Finance), chunk PDF pages 1–1; page provenance: 1.
  - **F1 payload excerpt:** “BHIM-UPI P2M transactions (up to ₹ 2,000)”
  - **F2 payload excerpt:** “Other than industry programmes”
  - **F3 payload excerpt:** “0.25%”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_034_structure_aware_00001_edcae9ae118c`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_034` (Department of Financial Services, Ministry of Finance), chunk PDF pages 1–1; page provenance: 1.
  - **F1 payload excerpt:** “BHIM-UPI P2M transactions (up to ₹ 2,000)”
  - **F2 payload excerpt:** “Other than industry programmes”
  - **F3 payload excerpt:** “0.25%”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q019 — In Tata Capital's grievance-handling SOP table, what is the maximum turnaround time for tagging a case as QRC after a customer requirement or concern is identified?

- **Canonical gold reference(s):** doc_023 PDF pages [7] (PDF page indices [6]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | The specified process row is tagging a case as QRC based on a customer requirement or concern. | doc_023, PDF p. [7]: “Based on the customer requirement or concerns the case is tagged as QRC” |
| F2 | The maximum TAT for that row is T+2 days (working days, per table heading). | doc_023, PDF p. [7]: “Maximum TAT (Working days) ... T+2 days” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 3 — `doc_023_fixed_size_00009_c432e15f15bb`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 3; source `doc_023` (Tata Capital Limited), chunk PDF pages 7–7; page provenance: 7.
  - **F1 payload excerpt:** “Based on the customer requirement or concerns the case is tagged as QRC.”
  - **F2 payload excerpt:** “2 | Based on the customer requirement or concerns the case is tagged as QRC. | T+2 days” under “Maximum TAT (Working days)”.

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 3 — `doc_023_structure_aware_00009_37b714cae638`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 3; source `doc_023` (Tata Capital Limited), chunk PDF pages 7–7; page provenance: 7.
  - **F1 payload excerpt:** “Based on the customer requirement or concerns the case is tagged as QRC.”
  - **F2 payload excerpt:** “2 | Based on the customer requirement or concerns the case is tagged as QRC. | T+2 days” under “Maximum TAT (Working days)”.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q020 — In RBI Annual Report Table II.2.1, what growth rate is listed for Gross Fixed Capital Formation in 2023-24?

- **Canonical gold reference(s):** doc_036 PDF pages [41] (PDF page indices [40]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Identify the Gross Fixed Capital Formation row and 2023-24 column in Table II.2.1. | doc_036, PDF p. [41]: “Table II.2.1; row Gross Fixed Capital Formation; column 2023-24” |
| F2 | Read the intersecting value as 10.2 (per cent). | doc_036, PDF p. [41]: “Gross Fixed Capital Formation \| 1.1 \| -7.1 \| 17.5 \| 6.6 \| 10.2” |

### Saved top-10 evidence

**Fixed-size: `INCOMPLETE`; v3 covered facets: none.**
No chunk is credited for a required facet in the saved v3 top-10 annotation. Same-document/page overlap alone is not answer evidence.

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 10 — `doc_036_structure_aware_00080_da6891873a1b`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 10; source `doc_036` (Reserve Bank of India), chunk PDF pages 41–41; page provenance: 41.
  - **F1 payload excerpt:** “| 2019-20 | 2020-21 | 2021-22 | 2022-23 | 2023-24” (column headings); “Gross Fixed Capital Formation | 1.1 | -7.1 | 17.5 | 6.6 | 10.2” (row).
  - **F2 payload excerpt:** “| 2019-20 | 2020-21 | 2021-22 | 2022-23 | 2023-24”; “Gross Fixed Capital Formation | 1.1 | -7.1 | 17.5 | 6.6 | 10.2”.

### Known concern / review safeguard

Table-specific decision retained: structure-aware rank 10 has the named row/year/value; fixed-size top 10 is incomplete. A narrative 10.2 elsewhere does not prove retrieval of the named table.

### Previously approved revision criteria retained

Named Table II.2.1 row and year, then intersecting value, remain the approved table-specific criteria.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (incomplete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q021 — When can the finance company disclose a borrower's personal or transaction information without the borrower's authorization?

- **Canonical gold reference(s):** doc_016 PDF pages [3] (PDF page indices [2]).
- **Facets:** 3. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Without authorization, disclosure is permitted when required by legal, statutory, or regulatory law. | doc_016, PDF p. [3]: “If the Company has to provide the information by legal, statutory or regulatory laws” |
| F2 | Disclosure is permitted when there is a duty to the public to reveal the information. | doc_016, PDF p. [3]: “If there is a duty to the public to reveal this information” |
| F3 | Disclosure is permitted when company interests require it, such as fraud prevention, to banks/financial institutions/group/associate companies; this company-interest ground must not be used to disclose borrower information to others for marketing. | doc_016, PDF p. [3]: “If the Company’s interest requires to provide this information (e.g., fraud prevention) to Banks / Financial institutions / Group / Associate Companies. The Company will not use this reason for giving information about borrowers to anyone else for marketing purpose.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 2 — `doc_016_fixed_size_00003_d1e3de271923`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 2; source `doc_016` (Shriram Finance Limited), chunk PDF pages 2–3; page provenance: 2, 3.
  - **F1 payload excerpt:** “If the Company has to provide the information by legal, statutory or regulatory laws ”
  - **F2 payload excerpt:** “If there is a duty to the public to reveal this information ”
  - **F3 payload excerpt:** “If the Company’s interest requires to provide this information (e.g., fraud prevention) to Banks / Financial institutions / Group / Associate Companies” followed by “The Company will not use this reason for giving information about borrowers to anyone else for marketing purpose.”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3.**
- **Rank 1 — `doc_016_structure_aware_00004_15199cc67fa1`; DIRECT evidence; assigned facets: F1, F2, F3.** Saved result rank: 1; source `doc_016` (Shriram Finance Limited), chunk PDF pages 2–3; page provenance: 2, 3.
  - **F1 payload excerpt:** “If the Company has to provide the information by legal, statutory or regulatory laws ”
  - **F2 payload excerpt:** “If there is a duty to the public to reveal this information ”
  - **F3 payload excerpt:** “If the Company’s interest requires to provide this information (e.g., fraud prevention) to Banks / Financial institutions / Group / Associate Companies” followed by “The Company will not use this reason for giving information about borrowers to anyone else for marketing purpose.”

### Known concern / review safeguard

Retained v2 criteria: three alternative disclosure grounds; marketing restriction qualifies the company-interest ground and is not a fourth ground.

### Previously approved revision criteria retained

Three grounds; marketing restriction is a qualification on the company-interest ground.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q022 — During microfinance debt collection, which calling hours are prohibited by the fair-practice code?

- **Canonical gold reference(s):** doc_024 PDF pages [3] (PDF page indices [2]).
- **Facets:** 1. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Calling the borrower before 9:00 a.m. or after 6:00 p.m. is prohibited. | doc_024, PDF p. [3]: “calling the borrower before 9:00 a.m. and after 6:00 p.m.” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1.**
- **Rank 7 — `doc_024_fixed_size_00004_e6145695ee32`; DIRECT evidence; assigned facets: F1.** Saved result rank: 7; source `doc_024` (Tata Capital Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “Persistently calling the borrower and/ or calling the borrower before 9:00 a.m. and after 6:00 p.m.”

**Structure-aware: `INCOMPLETE`; v3 covered facets: none.**
No chunk is credited for a required facet in the saved v3 top-10 annotation. Same-document/page overlap alone is not answer evidence.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (incomplete):** `PENDING_HUMAN_DECISION`

## Q023 — Before selling or auctioning a repossessed vehicle, what opportunity must the lender's process give the borrower?

- **Canonical gold reference(s):** doc_016 PDF pages [6] (PDF page indices [5]).
- **Facets:** 1. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Give the borrower a final chance to repay the loan before sale/auction of the property. | doc_016, PDF p. [6]: “final chance to be given to the borrower for repayment of loan before the sale / auction of the property” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1.**
- **Rank 2 — `doc_016_fixed_size_00006_5707a2baee10`; DIRECT evidence; assigned facets: F1.** Saved result rank: 2; source `doc_016` (Shriram Finance Limited), chunk PDF pages 5–6; page provenance: 5, 6.
  - **F1 payload excerpt:** “A provision regarding final chance to be given to the borrower for repayment of loan before”

**Structure-aware: `COMPLETE`; v3 covered facets: F1.**
- **Rank 2 — `doc_016_structure_aware_00007_3562949c7e7a`; DIRECT evidence; assigned facets: F1.** Saved result rank: 2; source `doc_016` (Shriram Finance Limited), chunk PDF pages 6–6; page provenance: 6.
  - **F1 payload excerpt:** “A provision regarding final chance to be given to the borrower for repayment of loan before”

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q024 — May a microfinance lender provide non-credit add-on products without the borrower's agreement, and where must their fees be stated?

- **Canonical gold reference(s):** doc_024 PDF pages [3] (PDF page indices [2]).
- **Facets:** 2. **V3 status:** `pending_user_adjudication`; adjudication `proposed_requires_user_approval`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | No: issuance of non-credit products requires the borrower's full consent. | doc_024, PDF p. [3]: “Issuance of non-credit products shall be with the full consent of the borrowers” |
| F2 | The fee structure must be explicitly communicated in the loan card. | doc_024, PDF p. [3]: “fee structure shall be explicitly communicated to the borrower in the loan card itself” |

### Saved top-10 evidence

**Fixed-size: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 1 — `doc_024_fixed_size_00003_cb861a2996e0`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 1; source `doc_024` (Tata Capital Limited), chunk PDF pages 2–3; page provenance: 2, 3.
  - **F1 payload excerpt:** “(k) Issuance of non-credit products shall be with the full consent of the borrowers and fee structure for such products shall be explicitly communicated to the borrower in the loan card itself;”
  - **F2 payload excerpt:** “(k) Issuance of non-credit products shall be with the full consent of the borrowers and fee structure for such products shall be explicitly communicated to the borrower in the loan card itself;”
- **Rank 10 — `doc_024_fixed_size_00004_e6145695ee32`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 10; source `doc_024` (Tata Capital Limited), chunk PDF pages 3–4; page provenance: 3, 4.
  - **F1 payload excerpt:** “(k) Issuance of non-credit products shall be with the full consent of the borrowers and fee structure for such products shall be explicitly communicated to the borrower in the loan card itself;”
  - **F2 payload excerpt:** “(k) Issuance of non-credit products shall be with the full consent of the borrowers and fee structure for such products shall be explicitly communicated to the borrower in the loan card itself;”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2.**
- **Rank 1 — `doc_024_structure_aware_00003_c9a35a031d1e`; DIRECT evidence; assigned facets: F1, F2.** Saved result rank: 1; source `doc_024` (Tata Capital Limited), chunk PDF pages 2–3; page provenance: 2, 3.
  - **F1 payload excerpt:** “(k) Issuance of non-credit products shall be with the full consent of the borrowers and fee structure for such products shall be explicitly communicated to the borrower in the loan card itself;”
  - **F2 payload excerpt:** “(k) Issuance of non-credit products shall be with the full consent of the borrowers and fee structure for such products shall be explicitly communicated to the borrower in the loan card itself;”

### Known concern / review safeguard

Fixed-size ranks 1 and 10 overlap/repeat the same clause. Do not count them as independent confirmations; the clause itself may support both facets.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (complete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Q025 — If original property papers are lost or damaged after a personal loan is settled, what support and additional time does the code allow?

- **Canonical gold reference(s):** doc_001 PDF pages [6] (PDF page indices [5]).
- **Facets:** 5. **V3 status:** `pending_user_adjudication`; adjudication `needs_review`.
- **Question wording:** MATCHES canonical evaluation dataset.

### Proposed facets

| Facet | Exact proposed requirement | V3 source reference and excerpt |
|---|---|---|
| F1 | Assist the borrower in obtaining duplicate/certified copies of the original property documents. | doc_001, PDF p. [6]: “the Company shall assist the borrower in obtaining duplicate/certified copies of the movable/immovable property documents” |
| F2 | The company bears the associated costs of obtaining the duplicate/certified copies. | doc_001, PDF p. [6]: “shall bear the associated costs” |
| F3 | The company pays compensation as indicated at the preceding clause (i). | doc_001, PDF p. [6]: “in addition to paying compensation as indicated at clause (i) above” |
| F4 | The company has an additional 30 days to complete the procedure. | doc_001, PDF p. [6]: “an additional time of 30 days will be available to the Company to complete this procedure” |
| F5 | The delayed-period penalty is calculated after a total period of 60 days. | doc_001, PDF p. [6]: “the delayed period penalty will be calculated thereafter (i.e., after a total period of 60 days)” |

### Saved top-10 evidence

**Fixed-size: `INCOMPLETE`; v3 covered facets: F1, F2, F3, F4.**
- **Rank 2 — `doc_001_fixed_size_00005_d577f4089a07`; PARTIAL evidence; assigned facets: F1, F2, F3, F4.** Saved result rank: 2; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 5–6; page provenance: 5, 6.
  - **F1 payload excerpt:** “In case of loss/damage to original movable/immovable property documents, either in part or in full, the Company shall assist the borrower in obtaining duplicate/certiﬁed copies of the”
  - **F2 payload excerpt:** “movable/immovable property documents and shall bear the associated costs, in addition to paying compensation as indicated at clause (i) above.”
  - **F3 payload excerpt:** “movable/immovable property documents and shall bear the associated costs, in addition to paying compensation as indicated at clause (i) above.”
  - **F4 payload excerpt:** “of 30 days will be available to the Company”

**Structure-aware: `COMPLETE`; v3 covered facets: F1, F2, F3, F4, F5.**
- **Rank 1 — `doc_001_structure_aware_00005_33a0e3812a93`; DIRECT evidence; assigned facets: F1, F2, F3, F4, F5.** Saved result rank: 1; source `doc_001` (Bajaj Finance Limited), chunk PDF pages 5–6; page provenance: 5, 6.
  - **F1 payload excerpt:** “In case of loss/damage to original movable/immovable property documents, either in part or in full, the Company shall assist the borrower in obtaining duplicate/certiﬁed copies of the”
  - **F2 payload excerpt:** “movable/immovable property documents and shall bear the associated costs, in addition to paying compensation as indicated at clause (i) above.”
  - **F3 payload excerpt:** “movable/immovable property documents and shall bear the associated costs, in addition to paying compensation as indicated at clause (i) above.”
  - **F4 payload excerpt:** “of 30 days will be available to the Company to complete this procedure and the delayed period penalty will be calculated thereafter (i.e., after a total period of 60 days).”
  - **F5 payload excerpt:** “of 30 days will be available to the Company to complete this procedure and the delayed period penalty will be calculated thereafter (i.e., after a total period of 60 days).”

### Known concern / review safeguard

Retained v2 criteria: five answer details (assistance, costs, compensation, additional 30 days, 60-day total); loss/damage is context. Fixed-size lacks F5; structure-aware covers all five.

### Previously approved revision criteria retained

Five separate details; fixed-size and structure-aware top-10 completeness differ.

### Human decision fields

- **Disposition:** `PENDING_HUMAN_DECISION` — select `APPROVE_AS_PROPOSED` / `REVISE` / `NEEDS_MORE_EVIDENCE`.
- **Human rationale:** `PENDING_HUMAN_DECISION`
- **Required correction (if any):** `PENDING_HUMAN_DECISION`
- **Accept fixed-size completeness (incomplete):** `PENDING_HUMAN_DECISION`
- **Accept structure-aware completeness (complete):** `PENDING_HUMAN_DECISION`

## Cross-question review safeguards

- **Prompt context/repetition:** Q009’s disadvantage trigger and Q025’s lost/damaged-paper scenario are contextual. Q017/Q018/Q020 include table row/category/year selectors; consider whether these are necessary to interpret table answers or repeat question content.
- **Compound facets:** Review facets that combine multiple independently assessable requirements, e.g. Q002, Q004, Q006–Q009, Q011–Q014, Q016–Q021, Q024, Q025. The exact proposed facets are listed per question above.
- **Partial support:** Q005 fixed-size rank 5 and structure-aware rank 6 are `PARTIAL` but credited only for F4; F3 is not covered. Q025 fixed-size rank 2 is `PARTIAL`, credited for F1–F4; F5 is not covered.
- **Aggregate vs per-chunk:** Completeness is coverage across a strategy’s top 10. Q012’s cited chunk in each strategy is mapped to seven facets individually; Q024’s overlapping fixed-size chunks are not independent confirmation.
- **Issuer/source identity:** Confirm source issuer/page when material. For Q025, v3’s doc_001 is the gold source; a similar doc_003 passage is explicitly excluded.
- **Historical conflict:** Q001’s previous incomplete label was superseded by approved v3/2B.24S. Q020’s earlier phrase/component matching was superseded by the named-table criterion. These preserved historical differences alone do not invalidate v3.
- **Outside top 10:** Q005 ranks 19/17 and Q010 structure-aware rank 18 are diagnostic only.

## Packet completion and unresolved evidence

- **25 questions and 62 proposed facets are accounted for.**
- Supporting chunk IDs cited in v3 were resolved against saved payloads and top-10 results. Exact excerpts are included for the facets assigned to those chunks; reviewers may consult the full payload where surrounding context matters.
- Particular attention: Q004 (historical overlap false positive); Q005 (partial support and diagnostic-only evidence); Q009 (compound option); Q010 (rank 18 outside top 10); Q012 (seven safeguards); Q017 (table-cell alignment); Q020 (named table vs narrative value); Q021 (three grounds vs marketing qualification); Q024 (overlap); Q025 (five details and fixed-size F5 gap).
- Absence of a cited diagnostic annotation for a question is not evidence that no other relevant result exists. No extra diagnostic rows are promoted to top-10 evidence.
- **Do not change any annotation status or v3 record until the user explicitly authorizes the next step.** This packet does not approve any annotation as ground truth.

## Reviewer decision ledger

| Question | Disposition | Rationale | Required correction | Fixed-size completeness accepted? | Structure-aware completeness accepted? |
|---|---|---|---|---|---|
| Q001 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q002 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q003 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q004 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q005 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q006 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q007 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q008 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q009 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q010 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q011 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q012 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q013 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q014 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q015 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q016 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q017 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q018 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q019 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q020 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q021 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q022 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q023 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q024 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |
| Q025 | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION | PENDING_HUMAN_DECISION |

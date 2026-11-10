# Evidence Annotation Decision Sheet v2 — Q020, Q021, Q025

**Decision criteria:** Human decisions supplied for Milestone 2B.22
**Annotation status:** Proposed; all records remain pending human adjudication

This sheet records the authoritative evaluation criteria for this revision.
It does not approve the annotation dataset or turn assistant-proposed
facets/chunk labels into ground truth. PDF pages below are one-based.

## Q020 — Table II.2.1 GFCF value

**Decision:** Require table-specific evidence.

For completeness, retrieved evidence must connect the named Table II.2.1
table, the Gross Fixed Capital Formation row, the 2023-24 year, and the
intersecting value 10.2 per cent. Isolated component-string matches do not
establish that row/year/value relationship.

The original PDF is `doc_036`, PDF page 41 (printed page 16); the structured
row is `Gross Fixed Capital Formation | 1.1 | -7.1 | 17.5 | 6.6 | 10.2`.
Structure-aware rank 10,
`doc_036_structure_aware_00080_da6891873a1b`, contains the complete structured
row and year headings and satisfies both proposed facets. Structure-aware
top 10 is therefore proposed complete at rank 10.

Fixed-size top 10 remains incomplete: none of its results contains the
complete table row/year/value relation. Structure-aware rank 5,
`doc_036_structure_aware_00058_627c4c142023`, states the numeric value in
narrative, but is not evidence that the explicitly named table row was
retrieved. The prior phrase/component-based Q020 labels in
`data/evaluation/results/evidence_level_relevance_audit.csv` are historical
and are not authoritative under this decision.

**Version-2 annotation status:** Pending user adjudication.

## Q021 — Confidentiality exceptions

**Decision:** Require all three enumerated disclosure grounds.

1. Legal, statutory, or regulatory requirement.
2. Duty to the public to reveal the information.
3. Company interest, including the stated fraud-prevention example and the
   specified bank/financial-institution/group/associate-company recipients.

The marketing limitation is attached to the company-interest ground: the
company must not use that reason to disclose borrower information to others
for marketing. It is not a fourth ground.

Fixed-size rank 2,
`doc_016_fixed_size_00003_d1e3de271923`, and structure-aware rank 1,
`doc_016_structure_aware_00004_15199cc67fa1`, contain all three grounds and
the qualification. Both top-10 assessments remain proposed complete.

**Version-2 annotation status:** Pending user adjudication.

## Q025 — Lost or damaged property documents

**Decision:** Assess five details as separate facets.

1. Assistance obtaining duplicate or certified copies.
2. Responsibility for associated costs.
3. Compensation payable under the preceding clause.
4. An additional 30 days to complete the procedure.
5. The 60-day total period before delayed-period penalty calculation.

The source is `doc_001`, PDF page 6. Structure-aware rank 1,
`doc_001_structure_aware_00005_33a0e3812a93`, supports all five details and
remains proposed complete. Fixed-size rank 2,
`doc_001_fixed_size_00005_d577f4089a07`, supports the first four but omits
the 60-day total; it is PARTIAL and fixed-size top 10 is proposed incomplete.

Do not use the similar `doc_003` passage to complete this `doc_001` question.
The lost/damaged-document trigger is scenario/source context, not an
additional answer facet.

**Version-2 annotation status:** Pending user adjudication.

## Review boundary

These decisions settle the evaluation criteria for Q020, Q021, and Q025, but
do not constitute review or approval of the source citations, all selected
chunk labels, or the remaining 22 questions. The entire v2 proposal remains
`pending_user_adjudication`.

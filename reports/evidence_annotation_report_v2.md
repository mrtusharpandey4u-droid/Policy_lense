# PolicyLens — Evidence Annotation Proposal v2 (Milestone 2B.22)

## Status and scope

This versioned proposal accompanies
[`data/evaluation/evidence_annotations_v2.jsonl`](../data/evaluation/evidence_annotations_v2.jsonl).
It retains the existing JSON schema and the original 25 questions. Only Q020,
Q021, and Q025 were revised in response to the human decisions recorded for
Milestone 2B.22; the other 22 records are retained unchanged from v1.

**This remains a proposal, not approved ground truth.** All records retain
`reviewer_status: pending_user_adjudication`. Q020, Q021, and Q025 also retain
their `needs_review` adjudication state. The human decisions establish the
evaluation criteria for these revisions; they do not approve the annotations
or chunk assessments.

## Version 2 changes

| Question | Revision |
|---|---|
| Q020 | Applied the table-specific criterion. Fixed-size top 10 remains incomplete; structure-aware top 10 is complete from rank 10, which contains Table II.2.1's GFCF row and 2023-24 value. Rank 5's narrative number is retained as an alternate location, not table evidence. |
| Q021 | Required all three enumerated disclosure grounds. The marketing limitation is attached to the company-interest ground in F3; there is no fourth ground. Existing fixed-size rank 2 and structure-aware rank 1 support the three grounds and qualification. |
| Q025 | Replaced the scenario-only answer facet and split the combined details into five required facets: copy assistance, associated costs, compensation, additional 30 days, and the 60-day penalty boundary. Structure-aware rank 1 is complete; fixed-size rank 2 is partial and top-10 completeness is incomplete because it omits the 60-day total. |

The Q020 earlier evidence-level CSV labels were produced by phrase/component
matching and are not authoritative for the newly selected table-specific
criterion. The historical CSV and Milestone 2B.18 report remain unchanged.

## Proposed completeness by question

“Complete” requires all facets in the v2 record to be covered by the official
top-10 retrieval results. Existing diagnostic ranks for Q005 and Q010 are not
counted as top-10 evidence. These are proposed assessments, not approved
metrics or human-adjudicated chunk labels.

| ID | Gold source (PDF page) | Facets | Fixed-size top 10 | Structure-aware top 10 | Note |
|---|---|---:|---|---|---|
| Q001 | doc_001 (3) | 1 | Incomplete | Incomplete | No top-10 evidence contains the complaint-forwarding commitment. |
| Q002 | doc_001 (4) | 2 | Complete, r3 | Complete, r3 | Acknowledgement and disposal timeframe. |
| Q003 | doc_001 (4) | 1 | Complete, r7 | Complete, r4 | General communications language rule. |
| Q004 | doc_001 (4) | 4 | Complete, r4 | Complete, r7 | Fixed-size rank 1 page overlap is not answer evidence. |
| Q005 | doc_001 (4) | 4 | Incomplete | Incomplete | Full instruction is in diagnostic ranks 19/17, outside top 10. |
| Q006 | doc_001 (5) | 2 | Complete, r3 | Complete, r4 | Notice and prospective effect. |
| Q007 | doc_001 (5) | 2 | Complete, r7 | Complete, r4 | Release trigger and lien qualification. |
| Q008 | doc_003 (4) | 2 | Complete, r1 | Complete, r2 | All-in cost, transparency, non-discrimination. |
| Q009 | doc_003 (5) | 3 | Complete, r2 | Complete, r4 | Disadvantage option and conditions. |
| Q010 | doc_016 (2) | 2 | Incomplete | Incomplete | Existing structure-aware rank 18 diagnostic evidence is outside top 10. |
| Q011 | doc_016 (5) | 3 | Complete, r5 | Complete, r8 | Governance duties. |
| Q012 | doc_016 (6) | 5 | Complete, r4 | Complete, r2 | Repossession safeguards. |
| Q013 | doc_024 (2) | 3 | Complete, r1 | Complete, r1 | KFS, language, explanation, acknowledgement. |
| Q014 | doc_024 (3) | 2 | Complete, r5 | Complete, r2 | Collection place and exception. |
| Q015 | doc_023 (2) | 3 | Complete, r1 | Complete, r1 | Grievance-policy objectives. |
| Q016 | doc_019 (2) | 1 | Complete, r1 | Complete, r1 | TCL Retail PLR row and date. |
| Q017 | doc_034 (1) | 4 | Complete, r1 | Complete, r1 | RuPay rate and cap; table-cell association preserved. |
| Q018 | doc_034 (1) | 3 | Complete, r1 | Complete, r1 | BHIM-UPI category, threshold, and rate. |
| Q019 | doc_023 (7) | 2 | Complete, r3 | Complete, r3 | QRC row and T+2 working days. |
| Q020 | doc_036 (41) | 2 | Incomplete | Complete, r10 | Table-specific: rank 10 supplies row/year/value; narrative rank 5 does not. |
| Q021 | doc_016 (3) | 3 | Complete, r2 | Complete, r1 | All three grounds required; marketing limitation qualifies ground three. |
| Q022 | doc_024 (3) | 1 | Complete, r7 | Incomplete | Prohibited calling hours. |
| Q023 | doc_016 (6) | 1 | Complete, r2 | Complete, r2 | Final repayment opportunity. |
| Q024 | doc_024 (3) | 2 | Complete, r1 | Complete, r1 | Overlapping fixed-size rank 10 repeats the same evidence; count once. |
| Q025 | doc_001 (6) | 5 | Incomplete, r2 partial | Complete, r1 | Rank 2 omits the 60-day total; rank 1 includes all five details. |

Across the proposed records, fixed-size has 20 complete and 5 incomplete
questions; structure-aware has 21 complete and 4 incomplete. These counts
reflect only the v2 proposal and are not recomputed performance metrics.

## Priority evidence and interpretation

### Q020 — table-specific evidence

The source is `doc_036`, PDF page 41 (printed page 16). The row
`Gross Fixed Capital Formation | 1.1 | -7.1 | 17.5 | 6.6 | 10.2` and the
2023-24 column identify 10.2 per cent.

Structure-aware rank 10,
`doc_036_structure_aware_00080_da6891873a1b`, includes the structured table
payload with the year headings and complete row; v2 cites it as DIRECT for
both facets. Fixed-size top 10 has no complete row/year/value relation.
Structure-aware rank 5,
`doc_036_structure_aware_00058_627c4c142023`, states the same number in
narrative on PDF pages 27-28, but does not retrieve the specifically named
table. It is an alternate numeric source only and does not satisfy the
table-specific completeness rule. Matching isolated strings for the row,
year, or value in other chunks is not sufficient.

### Q021 — all three disclosure grounds

The v2 facets require, together, (1) a legal/statutory/regulatory
requirement, (2) a duty to the public, and (3) company interest, including the
fraud-prevention example and the specified recipients. The restriction
against using the company-interest reason for marketing disclosure is part of
F3. It is a qualification on that ground, not a fourth ground.

Fixed-size rank 2,
`doc_016_fixed_size_00003_d1e3de271923`, and structure-aware rank 1,
`doc_016_structure_aware_00004_15199cc67fa1`, contain all three grounds and
the marketing limitation. Both remain proposed complete results.

### Q025 — five independently assessed details

The five required facets in v2 are:

1. Assistance obtaining duplicate/certified copies.
2. Responsibility for associated costs.
3. Compensation under the preceding clause.
4. An additional 30 days to complete the procedure.
5. Delayed-period penalty calculation after a total 60-day period.

Structure-aware rank 1,
`doc_001_structure_aware_00005_33a0e3812a93`, includes all five details.
Fixed-size rank 2,
`doc_001_fixed_size_00005_d577f4089a07`, includes details 1-4 but not the
60-day total, so it is PARTIAL and does not make top 10 complete. The
lost/damaged-document condition remains scenario/source context, not a sixth
answer facet. Similar text from `doc_003` is not attributed to this `doc_001`
question.

## Preserved scope and limitations

- Q004 page-overlap handling, Q005's evidence beyond top 10, Q010's rank-18
  diagnostic evidence, Q017's structured table-cell association, and Q024's
  duplicate-evidence handling are unchanged from v1.
- The other 22 question records are unchanged semantically from v1.
- No historical evidence-level audit CSV/report or retrieval artifact was
  revised, and no metrics were recalculated.
- The separate Milestone 2B.18B quality review report was not found and was
  not reconstructed or claimed as inspected.
- No independent second reviewer adjudicated the annotations. All records
  remain pending human adjudication; no label is approved ground truth.

# PolicyLens — Evidence Annotation Revision (Milestone 2B.22)

## Purpose and status

This report documents the v2 proposal revision following the human decisions
for Q020, Q021, and Q025. It is a proposal update, not approval of the
annotations. All 25 records remain pending human adjudication.

## Files created

- [`data/evaluation/evidence_annotations_v2.jsonl`](../data/evaluation/evidence_annotations_v2.jsonl)
- [`reports/evidence_annotation_report_v2.md`](evidence_annotation_report_v2.md)
- [`reports/evidence_annotation_decision_sheet_v2.md`](evidence_annotation_decision_sheet_v2.md)
- [`reports/evidence_annotation_revision_2B22.md`](evidence_annotation_revision_2B22.md)

Version 1 and the Milestone 2B.21 reconciliation report were preserved.
Version 2 uses the existing record schema (`schema_version: 1.0`); there was
no structural schema change. The file version is represented in the filename
and companion reports. Only the Q020, Q021, and Q025 records were changed;
the other 22 records were copied semantically unchanged.

## Changes and rationale

### Q020

The user selected table-specific completeness: evidence must connect Table
II.2.1, the Gross Fixed Capital Formation row, 2023-24, and 10.2 per cent.
Structure-aware rank 10,
`doc_036_structure_aware_00080_da6891873a1b`, contains the complete structured
row and year headings; the v2 proposal now marks structure-aware top 10
complete and cites rank 10 for F1/F2. Fixed-size top 10 remains incomplete.

Structure-aware rank 5,
`doc_036_structure_aware_00058_627c4c142023`, gives an alternate narrative
statement of the number but does not satisfy the named-table retrieval
criterion. Older phrase/component-based labels in
`data/evaluation/results/evidence_level_relevance_audit.csv` remain untouched
and are explicitly non-authoritative for this criterion. Retrieval results
and metrics were not recalculated.

### Q021

The v2 proposal requires all three grounds: legal/statutory/regulatory
requirement, public duty, and company interest with the specified example and
recipients. The marketing limitation is attached to the company-interest
facet, not treated as a fourth ground. Existing fixed-size rank 2 and
structure-aware rank 1 citations and proposed completeness are preserved,
with facet IDs updated to the three-ground form.

### Q025

The v2 proposal has five distinct required facets: duplicate/certified-copy
assistance, associated costs, compensation, additional 30 days, and the
60-day total before penalty calculation. The lost/damaged condition is
retained as scenario/source context rather than a sixth answer detail.

Structure-aware rank 1,
`doc_001_structure_aware_00005_33a0e3812a93`, supports all five and remains
proposed complete. Fixed-size rank 2,
`doc_001_fixed_size_00005_d577f4089a07`, supports the first four but not the
60-day total, so its label is PARTIAL and fixed-size top 10 is incomplete.
The similar passage from `doc_003` is not attributed to the `doc_001`
question.

## Validation performed

Focused validation was run after writing v2; details and results are recorded
in the completion summary. The checks cover JSONL parsing, 25 unique expected
IDs, unchanged question/source references, semantic preservation of the
other 22 records, v2 priority-facet and completeness criteria, pending
adjudication status, rank/ID correspondence to saved retrieval results,
chunk existence and payload evidence, and file hashes for protected v1 and
historical artifacts.

No extraction, OCR, cleaning, chunking, embedding, indexing, retrieval, or
metric evaluation was run. No project code or original source/evaluation
artifact was edited.

## Remaining limitations

- The v2 facet/chunk annotations remain assistant-proposed and pending human
  adjudication. The user's criteria are authoritative for this revision but
  do not mean the annotation dataset is approved or ground truth.
- The separate Milestone 2B.18B quality review report could not be found; it
  was not invented, reconstructed, or treated as inspected.
- Historical Q020 evidence-audit CSV labels remain unchanged. Their
  phrase/component matches should not be used as approved table-specific
  labels.
- No independent second reviewer was involved, and no retrieval metrics were
  recalculated.

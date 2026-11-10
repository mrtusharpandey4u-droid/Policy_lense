# PolicyLens — Evidence Annotation Revision (Milestone 2B.24R)

## Purpose and status

This report documents creation of the v3 evidence annotation proposal after
the human adjudicator approved the five revision decisions for Q001, Q005,
Q009, and Q012. The revision is limited to those four records. The other 21
records, including the already revised Q020, Q021, and Q025, remain
semantically identical to v2.

**The v3 dataset remains a proposal, not approved ground truth.** All 25
records have `reviewer_status: pending_user_adjudication`. No retrieval
metrics, labels in historical artifacts, source files, or saved retrieval
results were changed.

## New artifacts

- [`data/evaluation/evidence_annotations_v3.jsonl`](../data/evaluation/evidence_annotations_v3.jsonl)
- [`reports/evidence_annotation_report_v3.md`](evidence_annotation_report_v3.md)
- [`reports/evidence_annotation_decision_sheet_v3.md`](evidence_annotation_decision_sheet_v3.md)
- [`reports/evidence_annotation_revision_2B24R.md`](evidence_annotation_revision_2B24R.md)

No v1/v2 JSONL, evaluation question, historical report, chunk, PDF, or
retrieval result was edited.

## Human-approved decisions and implementation

| Question | Old v2 facets / status | V3 facets / status | Saved evidence used |
|---|---|---|---|
| Q001 | One F1; fixed-size incomplete, structure-aware incomplete; no cited support. | Same F1; fixed-size complete, structure-aware complete. | Fixed-size r1 `doc_001_fixed_size_00001_aee405d33739` and structure-aware r1 `doc_001_structure_aware_00001_ac782e3816d0`, both DIRECT for F1. Each chunk contains the page-3 complaint-forwarding commitment. |
| Q005 | F1 late repayment, F2 other default, F3 bold, F4 bold statement in loan agreement; both top 10s incomplete, F4 listed as covered despite partial evidence. | F3 bold and F4 loan-agreement location; both top 10s remain incomplete. Only F4 is fully covered. | Fixed-size r5 `doc_001_fixed_size_00004_785fedf70295`; structure-aware r6 `doc_001_structure_aware_00004_288632361e39`. Both support F4 but not F3. Diagnostic r19/r17 is outside top 10. |
| Q009 | F1 disadvantage trigger, F2 60-day/no-notice close-or-switch option, F3 no-extra-charges condition; both complete. | F2 and F3 only; both remain complete. | Fixed-size r2 `doc_003_fixed_size_00006_8bf99111838c` and structure-aware r4 `doc_003_structure_aware_00006_f9c845e0a416`, each DIRECT for both retained facets. |
| Q012 | Five facets, with notice/waiver in F2 and return/sale process in F5; both complete. | Seven facets; notice and waiver separate, as are return-possession and sale/auction procedures; both remain complete. | Fixed-size r4 `doc_016_fixed_size_00006_5707a2baee10` and structure-aware r2 `doc_016_structure_aware_00007_3562949c7e7a`, each DIRECT for all seven v3 facets. |

### Q005 full versus partial evidence

The v3 facets are F3 (“The penal charge must be stated in bold”) and F4 (“The
penal charge must be stated in the loan agreement”), both sourced to doc_001,
PDF page 4. The question's late-repayment and other-default language remains
context; it is not duplicated as required answer detail.

Each cited doc_001 top-10 chunk states that penal-charge quantum and reason
are disclosed in the loan agreement, supporting F4. Neither states the bold
presentation requirement, so neither supports F3. Both chunk references are
therefore `PARTIAL`, with `supported_facet_ids: ["F4"]`; top-10
`covered_facets` also lists only F4 because it is fully supported. Since F3
is missing, both strategies are incomplete.

The existing schema's `label`, `supported_facet_ids`, and `justification`
represent partial chunk evidence without adding a field or changing schema
version. Partial evidence is not credited as full support for F3.

The top-20 diagnostic cites doc_001 fixed-size rank 19
(`doc_001_fixed_size_00003_0bf6f42069fa`) and structure-aware rank 17
(`doc_001_structure_aware_00003_ad7599361f91`) as DIRECT for F3 and F4.
Those ranks do not contribute to official top-10 completeness.

## Facet changes

- **Q001:** F1 is unchanged; added direct rank-1 chunk citations and corrected
  both completeness statuses.
- **Q005:** Removed v2 F1 (late repayment) and F2 (other default) as
  question-context facets. Retained F3 (bold) and narrowed F4 to the
  loan-agreement location requirement.
- **Q009:** Removed v2 F1 (disadvantage trigger) as question context. Retained
  F2 (60 days, without notice, close/switch) and F3 (no extra charges or
  interest).
- **Q012:** Narrowed existing F2 to notice period and F5 to return of
  possession; added F6 for waiver circumstances and F7 for sale/auction
  procedure. Existing F1, F3, and F4 remain unchanged. All seven facets cite
  doc_016, PDF page 6.

## Validation results

Focused read-only validation was run against the original questions, v2
records, both chunk files, the saved top-10 retrieval results, the saved
top-20 diagnostic, and source-page provenance. Results:

1. **JSONL syntax and record count — PASS:** 25 parseable records.
2. **Question IDs — PASS:** exactly 25 unique IDs Q001–Q025.
3. **Question wording and gold references — PASS:** all 25 match the original
   evaluation questions and gold document/page references.
4. **Revision scope — PASS:** only Q001, Q005, Q009, and Q012 differ
   semantically from v2; the other 21 records are unchanged, including Q020,
   Q021, and Q025.
5. **Facet IDs — PASS:** IDs are unique within each record.
6. **Saved ranks and chunks — PASS:** every cited top-10 rank/chunk pair
   resolves to the saved strategy result; source document and page spans match
   the corresponding chunk payload. Q005 diagnostic ranks 19 and 17 also
   match the saved diagnostic.
7. **Coverage/status consistency — PASS:** each `covered_facets` value refers
   only to a fully supported facet; complete/incomplete labels agree with
   required-facet coverage.
8. **Q001 — PASS:** both rank-1 payloads contain the direct sentence and are
   cited DIRECT; both top-10 results are complete.
9. **Q005 — PASS:** no required facet repeats the question's scenario; top-10
   results remain incomplete and only the fully supported F4 is covered.
10. **Q009 — PASS:** no required facet repeats the disadvantage trigger;
    both remaining answer facets are supported in both top-10 strategies.
11. **Q012 — PASS:** seven unique facets separately represent all safeguards;
    both saved cited chunks contain all seven on the gold source page.
12. **Q020, Q021, Q025 — PASS:** records are semantically unchanged from v2.
13. **Pending status — PASS:** all 25 records remain
    `pending_user_adjudication`; no annotation is marked approved ground truth.
14. **Report totals — PASS:** v3 has 62 facets; fixed-size has 21 complete
    and 4 incomplete labels; structure-aware has 22 complete and 3
    incomplete labels. These are counts of proposal labels, not recomputed
    metrics.

No validation failure was found. Retrieval, metric evaluation, OCR,
extraction, chunking, embedding, indexing, and Qdrant access were not
performed.

## Limitations and preservation

- All proposed evidence assessments remain subject to user adjudication.
- The Q005 rank-5/rank-6 chunks fully support the loan-agreement location
  facet, but do not state the bold requirement; incomplete status is retained
  accordingly.
- Top-20 Q005 evidence is diagnostic only and is not included in top-10
  completeness.
- Historical reports remain historical. In particular, the v2 report,
  Milestone 2B.21 reconciliation, Milestone 2B.23 verification, and
  Milestone 2B.24 audit were not retroactively rewritten. Their former
  conclusions remain intact; this revision report notes that Q001's
  false-negative was identified by the 2B.24 audit and corrected only in
  this new proposal.
- No baseline claims are made about protected historical artifacts beyond
  the previously recorded limitations.

## Conclusion

The four new v3 artifacts are internally aligned with the human-approved
revision decisions and with the inspected original sources and saved
retrieval payloads. Version 3 is a revised proposal only; it is not approved
ground truth, and all 25 records remain pending human adjudication.

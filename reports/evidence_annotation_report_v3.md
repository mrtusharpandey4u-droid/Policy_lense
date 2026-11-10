# PolicyLens — Evidence Annotation Proposal v3 (Milestone 2B.24R)

## Status and scope

This proposal accompanies
[`data/evaluation/evidence_annotations_v3.jsonl`](../data/evaluation/evidence_annotations_v3.jsonl).
It retains the 25 original evaluation questions and v1.0 record schema. Only
Q001, Q005, Q009, and Q012 differ semantically from v2, following the five
human-approved decisions for this revision.

**This is still a proposal, not approved ground truth.** All 25 records retain
`reviewer_status: pending_user_adjudication`. The four revised records have
`adjudication_status: needs_review`; the other 21 retain their v2 adjudication
states, including Q020, Q021, and Q025.

## Changes in v3

| Question | Revision |
|---|---|
| Q001 | Corrected the false-negative top-10 assessments. Fixed-size rank 1 and structure-aware rank 1 each contain the direct source-page-3 commitment; both are cited DIRECT and both top-10 assessments are complete. |
| Q005 | Removed late-repayment and other-default context from required facets. F3 requires bold presentation; F4 requires the loan-agreement location. Both top-10 strategies remain incomplete: their cited doc_001 chunks fully support F4, not F3. `covered_facets` lists F4 only; `label: PARTIAL` and the justification preserve the missing F3 evidence. |
| Q009 | Removed the disadvantage trigger, which is already in the question. Retained the 60-day/no-notice close-or-switch option and the no-extra-charges-or-interest condition. Both top-10 strategies remain complete. |
| Q012 | Split the notice-period/waiver pair and the return-possession/sale-auction pair into separate facets. The seven safeguards are all supported by fixed-size rank 4 and structure-aware rank 2; both strategies remain complete. |

No retrieved rank, retrieval result, evaluation metric, source, or question was
changed. Existing Q020, Q021, and Q025 criteria are carried forward unchanged.

## Proposed completeness by question

Completeness is based on the saved official top-10 results and the cited
payloads. Diagnostic ranks beyond top 10 do not contribute to these labels.
These are annotation proposals, not recomputed metrics.

| ID | Gold source (PDF page) | Facets | Fixed-size top 10 | Structure-aware top 10 |
|---|---|---:|---|---|
| Q001 | doc_001 (3) | 1 | Complete, r1 | Complete, r1 |
| Q002 | doc_001 (4) | 2 | Complete, r3 | Complete, r3 |
| Q003 | doc_001 (4) | 1 | Complete, r7 | Complete, r4 |
| Q004 | doc_001 (4) | 4 | Complete, r4 | Complete, r7 |
| Q005 | doc_001 (4) | 2 | Incomplete, r5 partial (F4 only) | Incomplete, r6 partial (F4 only) |
| Q006 | doc_001 (5) | 2 | Complete, r3 | Complete, r4 |
| Q007 | doc_001 (5) | 2 | Complete, r7 | Complete, r4 |
| Q008 | doc_003 (4) | 2 | Complete, r1 | Complete, r2 |
| Q009 | doc_003 (5) | 2 | Complete, r2 | Complete, r4 |
| Q010 | doc_016 (2) | 2 | Incomplete | Incomplete |
| Q011 | doc_016 (5) | 3 | Complete, r5 | Complete, r8 |
| Q012 | doc_016 (6) | 7 | Complete, r4 | Complete, r2 |
| Q013 | doc_024 (2) | 3 | Complete, r1 | Complete, r1 |
| Q014 | doc_024 (3) | 2 | Complete, r5 | Complete, r2 |
| Q015 | doc_023 (2) | 3 | Complete, r1 | Complete, r1 |
| Q016 | doc_019 (2) | 1 | Complete, r1 | Complete, r1 |
| Q017 | doc_034 (1) | 4 | Complete, r1 | Complete, r1 |
| Q018 | doc_034 (1) | 3 | Complete, r1 | Complete, r1 |
| Q019 | doc_023 (7) | 2 | Complete, r3 | Complete, r3 |
| Q020 | doc_036 (41) | 2 | Incomplete | Complete, r10 |
| Q021 | doc_016 (3) | 3 | Complete, r2 | Complete, r1 |
| Q022 | doc_024 (3) | 1 | Complete, r7 | Incomplete |
| Q023 | doc_016 (6) | 1 | Complete, r2 | Complete, r2 |
| Q024 | doc_024 (3) | 2 | Complete, r1 | Complete, r1 |
| Q025 | doc_001 (6) | 5 | Incomplete, r2 partial | Complete, r1 |

Current v3 proposal totals are **21 fixed-size complete / 4 incomplete** and
**22 structure-aware complete / 3 incomplete**. These counts summarize the
annotation labels; they are not retrieval metrics. The v3 JSONL contains 62
required facets.

## Evidence notes for revised questions

### Q001

The fixed-size rank-1 chunk
`doc_001_fixed_size_00001_aee405d33739` and structure-aware rank-1 chunk
`doc_001_structure_aware_00001_ac782e3816d0` both contain: “Telling
customers' how to take their complaint forward if they are still not
satisfied.” The payloads include doc_001 PDF page 3. Each is cited DIRECT for
F1. The correction is based on the sentence itself, not page overlap.

### Q005

The late-repayment/other-default conditions remain in the question wording
and are context, not answer facets. The required facets are F3 (bold) and F4
(loan-agreement location). Fixed-size rank 5,
`doc_001_fixed_size_00004_785fedf70295`, and structure-aware rank 6,
`doc_001_structure_aware_00004_288632361e39`, support the loan-agreement
disclosure location (F4) but do not state that the charge must be bold (F3).
Both references therefore have `label: PARTIAL` and
`supported_facet_ids: ["F4"]`; top-10 `covered_facets` also lists only F4,
which is fully supported. The absent F3 prevents completeness. Direct
doc_001 evidence for both facets occurs at diagnostic fixed-size rank 19 and
structure-aware rank 17, outside top 10.

No new schema field was necessary: the existing `label`, `supported_facet_ids`,
and `justification` distinguish partial chunk evidence from fully covered
facets. No other issuer's evidence is credited.

### Q009

The disadvantage trigger remains supplied by the question and is not a
required facet. F2 retains the 60-day/no-notice close-or-switch option and F3
retains the no-extra-charges-or-interest condition. Fixed-size rank 2,
`doc_003_fixed_size_00006_8bf99111838c`, and structure-aware rank 4,
`doc_003_structure_aware_00006_f9c845e0a416`, each contain both required
details on the cited doc_003 source passage. Both strategies remain complete.

### Q012

The seven facets separately assess: enforceable agreement clause (F1), notice
period (F2), waiver circumstances (F6), taking possession of security (F3),
final repayment chance (F4), return of possession to the borrower (F5), and
sale/auction procedure (F7). Fixed-size rank 4,
`doc_016_fixed_size_00006_5707a2baee10`, and structure-aware rank 2,
`doc_016_structure_aware_00007_3562949c7e7a`, contain each enumerated item
from doc_016 PDF page 6. Both top-10 strategies remain complete.

## Preserved proposal decisions

- Q020 remains table-specific: fixed-size top 10 incomplete; structure-aware
  rank 10 complete for Table II.2.1, the GFCF row, 2023-24, and 10.2.
- Q021 retains exactly three disclosure grounds; the marketing limitation
  remains attached to company interest, not a fourth ground.
- Q025 retains five distinct details; fixed-size rank 2 is incomplete and
  structure-aware rank 1 complete. No doc_003 evidence is credited.

These are pending proposed annotations, not approved ground truth.

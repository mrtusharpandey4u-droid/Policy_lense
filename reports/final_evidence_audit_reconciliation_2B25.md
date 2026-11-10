# PolicyLens — Final Cross-Artifact Evidence Audit Reconciliation (Milestone 2B.25)

## 1. Executive verdict

**VERIFIED_WITH_LIMITATIONS**

`data/evaluation/evidence_annotations_v3.jsonl` is the latest clearly
identified **verified proposal**. Its 25 records match the original
evaluation questions and gold references; only Q001, Q005, Q009, and Q012
differ semantically from v2; all 25 remain pending adjudication. The
human-approved 2B.24 decisions are represented in v3, and the 2B.24S
independent verification confirms the revised per-chunk mappings and totals.

The audit sequence is sufficiently complete to move to a **separate human
adjudication checkpoint**, not to treat these annotations as ground truth or
use them as approved evaluation labels. Two limitations remain:

1. The top-20 diagnostic and retrieval question-results CSV lack reliable
   pre-revision baselines, so their historical unchanged status cannot be
   claimed.
2. Older, milestone-labeled reports retain superseded annotation conclusions
   (notably Q001's former false-negative). They are historical, not current
   authority, but can mislead when read without the later v3/2B.24S reports.

No unversioned runtime consumer of v1/v2 annotation JSONL or current
downstream evaluation artifact presenting v1/v2 completeness labels as
current was found. The v1/v2 reports themselves remain available and
explicitly identify their versions or milestones.

## 2. Scope and read-only method

Inspected:

- `data/evaluation/evidence_annotations_v1.jsonl`,
  `data/evaluation/evidence_annotations_v2.jsonl`, and
  `data/evaluation/evidence_annotations_v3.jsonl`.
- `data/evaluation/evaluation_questions.jsonl`.
- Annotation reports, decision sheets, revision reports, and audits from
  Milestones 2B.21 through 2B.24S.
- Saved `retrieval_evaluation_results.json`, the top-20 diagnostic, the
  question-results CSV, and the evidence-level audit report/CSV.
- Relevant retrieval/chunking reports and source references found by
  repository-wide searches for annotation filenames, status language, and
  the four revised question IDs.
- `src/` for code consuming annotation proposal files.

Record counts, IDs, revisions, pending statuses, facet counts, and
completeness totals were independently calculated from the JSONL. The
2B.24S source/chunk/rank verification was checked for consistency with v3;
the underlying retrieval was not rerun. No retrieval, metric evaluation,
extraction, OCR, embedding, indexing, or Qdrant operation was performed.
No existing file was modified.

## 3. Annotation version authority

| Check | Result |
|---|---|
| Current version | **v3 is the latest verified proposal**, based on the 2B.24R human-approved revision and 2B.24S independent verification. |
| V3 records and IDs | VERIFIED — 25 records with unique IDs Q001–Q025. |
| Original question wording and gold references | VERIFIED — all records match `evaluation_questions.jsonl`. |
| V2-to-v3 semantic changes | VERIFIED — only Q001, Q005, Q009, Q012 changed. |
| Other records | VERIFIED — the other 21 are semantically unchanged from v2. |
| Q020, Q021, Q025 | VERIFIED — all three v2 records and criteria are preserved. |
| Adjudication status | VERIFIED — all 25 records remain `pending_user_adjudication`. |
| V3 totals | VERIFIED — 62 facets; fixed-size 21 complete / 4 incomplete; structure-aware 22 complete / 3 incomplete. |

Version authority follows the evidence chain, not filename ordering alone:
the 2B.24R report records the human-approved changes in v3, and the later
2B.24S report independently verifies v3 and recommends accepting it as a
verified proposal. No report or code was found claiming that v1 or v2 is the
current proposal. The version-specific v1 and v2 reports still accurately
identify themselves as such.

## 4. Human decision traceability

| Approved decision | V3 representation | Reconciliation |
|---|---|---|
| Q001: both rank-1 chunks directly support the complaint-forwarding commitment | Fixed-size r1 `doc_001_fixed_size_00001_aee405d33739` and structure-aware r1 `doc_001_structure_aware_00001_ac782e3816d0` are DIRECT for F1; both top-10 labels are complete. | VERIFIED by the v3 record and 2B.24S payload checks. The direct sentence, not page overlap, supports the facet. |
| Q005: late/default trigger is context; bold and loan-agreement location remain distinct | V3 requires F3 (bold) and F4 (loan-agreement location), both sourced to doc_001 p.4. | VERIFIED. |
| Q005: only fully supported facets count as covered | Fixed-size r5 and structure-aware r6 list only F4 in `covered_facets` and `supported_facet_ids`; both are `PARTIAL` because F3 is absent. | VERIFIED. Diagnostic ranks fixed r19 and structure-aware r17 are recorded separately and do not count toward top-10 completeness. |
| Q009: disadvantage trigger is question context | V3 removes that trigger facet and retains the 60-day/no-notice close-or-switch facet and no-extra-charges-or-interest facet. Both top-10 strategies are complete. | VERIFIED by 2B.24S per-chunk review. |
| Q012: all seven safeguards are separately represented | V3 separately records enforceability, notice period, waiver circumstances, taking-possession procedure, final repayment chance, return-possession procedure, and sale/auction procedure. | VERIFIED by 2B.24S per-chunk review; both strategies are complete. |

No unapproved semantic change was found in the v2-to-v3 comparison.
Q020's table-specific requirement, Q021's three grounds with the marketing
qualification attached to company interest, and Q025's five independently
assessable details remain unchanged from v2.

## 5. Independent verification traceability

The findings in
`reports/evidence_annotation_revision_verification_2B24S.md` are consistent
with v3:

- Q001: both cited rank-1 chunks contain the direct source sentence; both
  strategies are complete.
- Q005: only F4 is fully covered in each top-10 supporting chunk; F3 is
  missing, so both strategies are incomplete. Diagnostic r19/r17 is outside
  top 10.
- Q009: each strategy's cited chunk individually supports both remaining
  facets; aggregate coverage is complete.
- Q012: each strategy's cited chunk individually supports all seven facets;
  aggregate coverage is complete.
- Q020, Q021, and Q025: unchanged from v2.
- Counts: 25 questions, 62 facets, fixed-size 21/4 and structure-aware 22/3.
- Status: all records remain pending user adjudication.

The distinction between per-chunk support and aggregate top-10 coverage is
preserved. Q009 and Q012 do not rely on aggregating unsupported per-chunk
assignments; the cited chunk for each strategy independently supports all
facets assigned to it.

## 6. Historical report reconciliation matrix

Historical conclusions are retained as records of what was assessed at that
milestone. “Superseded” below means that a later human-approved revision or
verification establishes the current position; it does not mean the earlier
report should be rewritten.

| Report | Original purpose and verdict | Historical validity and supersession | Could mislead without later reports? |
|---|---|---|---|
| `reports/final_evidence_audit_reconciliation.md` (2B.21) | Cross-artifact audit; found Q020 and Q025 issues, raised Q021 scope, and said proposal was not ready. It also incorrectly treated Q001 rank-1 evidence as page overlap without the answer. | Valid as a record of the v1-era review; Q020/Q021/Q025 criteria were addressed in 2B.22, and Q001 was identified as a false negative in 2B.24 then corrected in v3. | **Yes.** Its Q001 finding and “not ready” conclusion predate the approved revision. The filename alone does not show the milestone; the report heading does. |
| `reports/evidence_annotation_revision_2B22.md` (2B.22) | Documented human-decision-based creation of v2 for Q020/Q021/Q025. | Valid for v2. Its Q001 incompleteness and Q005/Q009/Q012 facet definitions were inherited from v1 and later revised in 2B.24R. | **Yes, if mistaken for current.** It identifies itself as a version-2 revision but does not incorporate 2B.24R. |
| `reports/evidence_annotation_revision_verification_2B23.md` (2B.23) | Independently verified v2; verdict `VERIFIED_WITH_LIMITATIONS` for missing historical baselines. | Its baseline limitation remains valid. Its conclusion that no material content discrepancy was found was superseded by 2B.24's discovery of Q001's direct rank-1 evidence. | **Yes.** The Q001 defect was missed; the later 2B.24/2B.24R/2B.24S sequence must be consulted. |
| `reports/evidence_annotation_completeness_consistency_audit_2B24.md` (2B.24) | Comprehensive audit of v2; verdict `NOT_VERIFIED`, identifying Q001, Q005, Q009, and Q012 issues/decisions. | Valid for the audited v2 state. Human decisions were authorized in 2B.24R and the resulting v3 was verified in 2B.24S. | **Yes.** Its `NOT_VERIFIED` verdict is not the current v3 verdict. |
| `reports/evidence_annotation_revision_2B24R.md` (2B.24R) | Recorded the human-approved changes and creation of v3. | Current revision record; its evidence and counts agree with the verified v3 proposal. | Low risk when read with its explicit milestone/version status. |
| `reports/evidence_annotation_revision_verification_2B24S.md` (2B.24S) | Independent verification of v3; verdict `VERIFIED`; recommended acceptance as a verified proposal. | Current independent verification, consistent with v3 and this reconciliation. It explicitly does not approve ground truth. | Low risk; it clearly distinguishes proposal verification from annotation approval. |

### Q001 correction trace

The v1 report (`reports/evidence_annotation_report.md`), v2 report
(`reports/evidence_annotation_report_v2.md`), 2B.21 reconciliation, and
Milestone 2B.18 evidence-level audit report/CSV all contain the former
false-negative position: Q001 was described as lacking complete top-10
evidence. The 2B.23 verification of v2 did not detect the direct sentence.
The 2B.24 audit identified it by inspecting the actual rank-1 payloads.
Human-approved decision 1 then updated only the v3 proposal, and 2B.24S
verified both direct rank-1 citations and complete labels. The historical
reports and CSV remain unchanged; **v3 and 2B.24S are the current position**.

## 7. Downstream artifact consistency matrix

| Artifact | Role and current content | Classification |
|---|---|---|
| `data/evaluation/evidence_annotations_v3.jsonl` | Current proposal; 25 records, 62 facets, current completeness totals, all pending. | **Current authority; verified proposal.** |
| `reports/evidence_annotation_report_v3.md` | V3 summary and 25-question table with current totals and Q001/Q005/Q009/Q012 revisions. | **Current; consistent.** |
| `reports/evidence_annotation_decision_sheet_v3.md` | Records the four revised questions and approved criteria. | **Current; consistent.** |
| `reports/evidence_annotation_revision_2B24R.md` | Records the v3 changes, validation, and pending status. | **Current; consistent.** |
| `reports/evidence_annotation_revision_verification_2B24S.md` | Independent v3 verification. | **Current; consistent.** |
| `reports/evidence_annotation_report.md` | Explicitly Milestone 2B.19/v1. Q001 and Q005 old labels, Q009's trigger facet, and Q012's five-facet model remain. | **Historical, superseded; can mislead if presented without its v1 label.** |
| `reports/evidence_annotation_report_v2.md` | Explicit v2 proposal. Shows Q001 incomplete, Q005 with four facets, Q009 with three, and Q012 with five. | **Historical, superseded; not a current report.** |
| `reports/evidence_annotation_decision_sheet_v2.md`, `reports/evidence_annotation_revision_2B22.md` | Decisions and revision scope for Q020/Q021/Q025 only. | **Historical v2 decision record; those three criteria remain unchanged.** |
| `reports/evidence_level_relevance_audit.md` and `data/evaluation/results/evidence_level_relevance_audit.csv` | Earlier chunk-label audit, including Q001 false-negative/component labels. | **Historical evidence audit; not current annotation authority.** |
| `reports/final_evidence_audit_reconciliation.md` and `reports/evidence_annotation_completeness_consistency_audit_2B24.md` | Earlier cross-artifact conclusions about v1/v2, including Q001 error and unresolved Q005/Q009/Q012 decisions. | **Historical milestones; conclusions were acted upon, not retroactively rewritten.** |
| `reports/retrieval_evaluation_report.md`, `reports/chunking_strategy_comparison.md`, `reports/retrieval_failure_analysis.md`, and saved retrieval CSV/JSON | Report original top-10 page/document relevance and retrieval ranking; Q001's rank-1 hit is a page-level metric result. These are not annotation-facet completeness reports. | **No conflicting current annotation claim found.** Their original metric scope remains intact. |
| `src/evaluate_retrieval.py`, `src/evaluate.py`, and searched `src/` code | Retrieval metric evaluator or stub; repository search found no active code importing/consuming v1/v2/v3 annotation JSONL. | **No v1/v2 runtime consumer found.** |

No artifact was found claiming the annotations are approved ground truth.
The historical reports' stale-looking Q001/Q005/Q009/Q012 values are
versioned/milestone-specific, not statements in the v3 report. Nevertheless,
there is no separate project index/manifest designating the current
annotation file; this 2B.25 report, v3 report, and 2B.24S verification now
provide an explicit trace to the current proposal.

## 8. Outstanding limitations

- `data/evaluation/results/retrieval_failure_top20_diagnostic.json` and
  `data/evaluation/results/retrieval_evaluation_question_results.csv` have no
  reliable pre-revision hash or tracked Git baseline documented in 2B.23.
  Their current presence/readability does not establish historical
  preservation; no hash-level unchanged claim is made here.
- All 25 v3 records remain `pending_user_adjudication`. V3 is not approved
  ground truth and must not be used as finalized evidence labels or as an
  adjudicated completeness benchmark before the separate human review.
- Older reports are preserved and retain superseded judgments. Readers must
  follow the milestone/version trace rather than use an older report as the
  current status.
- The standalone 2B.18B quality review report was previously unavailable;
  no missing historical report was reconstructed or assumed in this audit.

## 9. Final recommendation and next authorized step

**VERIFIED_WITH_LIMITATIONS.** The project has a clearly identifiable,
internally consistent, independently verified current proposal:
`data/evaluation/evidence_annotations_v3.jsonl`, with
`reports/evidence_annotation_revision_verification_2B24S.md` as its
independent verification. The Q001 false-negative is explicitly traced from
the historical finding to the corrected v3 position. Historical reports
remain intact and are distinguishable from the current proposal, though
several can mislead when read without their milestone/version context.

The annotation audit sequence is ready for a **separate human adjudication
checkpoint**. That checkpoint must decide whether to approve or revise the
proposed labels; it must not treat this verification verdict as ground-truth
approval. No next implementation milestone or annotation-status change is
authorized by this report.

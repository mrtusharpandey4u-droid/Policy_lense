# Human Adjudication Record — Milestone 2B.28

## Purpose and scope

This report records the user's explicit human decisions for Batch 2, covering Q006–Q010. It is a separate decision record. No annotation status, completeness label, facet, evidence reference, or question wording in v3 is changed by this report.

The user approved Q006, Q007, Q009, and Q010. Q008 is explicitly held for clarification and is neither approved nor rejected. The completeness labels shown for Q008 below are the unchanged proposal values only; no human completeness decision has been finalized for it.

## Source artifacts consulted

- `reports/evidence_annotation_human_adjudication_packet_2B26.md` — prepared evidence and recommendations for all questions.
- `reports/evidence_annotation_human_adjudication_2B27.md` — Batch 1 decision record.
- `data/evaluation/evidence_annotations_v3.jsonl` — current proposal, facet definitions, reviewer statuses, and completeness labels.

Saved retrieval ranks, chunk excerpts, and the rank-18 diagnostic cited below are those recorded in the adjudication packet. No retrieval, evaluation, embedding, indexing, or metric operation was run.

## User-approved decisions and Q008 hold

The following four approvals and one hold were explicitly provided by the user. These are human decisions, not automated inferences.

| Question | Human decision | Fixed-size completeness | Structure-aware completeness |
|---|---|---|---|
| Q006 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q007 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q008 | `HOLD_FOR_CLARIFICATION` | Not finalized; current proposal remains `complete` | Not finalized; current proposal remains `complete` |
| Q009 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q010 | `APPROVE_AS_PROPOSED` | `incomplete` | `incomplete` |

### Evidence-based rationale

- **Q006 — APPROVE_AS_PROPOSED; both strategies complete.** The top-10 fixed-size rank-3 and structure-aware rank-4 chunks directly support both requirements: notifying the borrower in the vernacular language about changes to loan terms, and making interest-rate and charge changes effective only prospectively.
- **Q007 — APPROVE_AS_PROPOSED; both strategies complete.** The fixed-size rank-7 and structure-aware rank-4 chunks support release of securities after repayment of dues or realization of the outstanding loan amount, subject to the lender's legitimate right or lien for another claim.
- **Q008 — HOLD_FOR_CLARIFICATION; no completeness decision finalized.** The existing proposal is preserved unchanged. Its F2 facet combines two independently assessable requirements—disclosure in a transparent manner and ensuring charges/fees are non-discriminatory. Clarification is needed before a final human decision. This hold does not approve or reject Q008, and no facet split or other correction is made here. The proposal's current complete/complete labels remain proposal values only.
- **Q009 — APPROVE_AS_PROPOSED; both strategies complete.** The disadvantage trigger is already in the question and is not a required answer facet. The retained answer facets cover the option to close the account or switch it within 60 days and without notice, and that closing or switching requires no extra charges or interest. The fixed-size rank-2 and structure-aware rank-4 chunks directly support both facets.
- **Q010 — APPROVE_AS_PROPOSED; both strategies incomplete.** Neither strategy has credited supporting evidence in its top 10. The direct evidence for the website/newspaper disclosure requirement appears in the structure-aware diagnostic at rank 18, outside the top 10. That diagnostic evidence is not counted toward top-10 coverage, so both incomplete labels are retained.

## Scope boundary and outstanding work

This batch records exactly four approvals (Q006, Q007, Q009, and Q010) and one hold (Q008). Q008 remains unresolved pending clarification; its proposal data and current completeness labels are preserved. Q011–Q025 have not been adjudicated by this batch and have no approval or rejection recorded here.

All 25 v3 records remain `pending_user_adjudication`; this report does not change those statuses. The approvals in this record do not make v3 or the full dataset approved ground truth. No later adjudication batch is begun by this milestone.

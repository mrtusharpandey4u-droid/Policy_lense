# Human Adjudication Record — Milestone 2B.27

## Purpose and scope

This report records the user's explicit human decisions for adjudication Batch 1, covering Q001–Q005 only. It is a separate decision record; it does not edit the annotation proposal or change any annotation status, completeness label, facet, evidence reference, or question wording.

The decisions approve the five specified question recommendations and their fixed-size and structure-aware top-10 completeness labels. They do **not** approve the entire annotation dataset, do not approve Q006–Q025, and do not make `evidence_annotations_v3.jsonl` approved ground truth.

## Source artifacts consulted

- `reports/evidence_annotation_human_adjudication_packet_2B26.md` — prepared evidence and recommendations for all questions.
- `data/evaluation/evidence_annotations_v3.jsonl` — current proposal and completeness labels.
- `reports/final_evidence_audit_reconciliation_2B25.md` — final audit status and limitations.

The saved ranks and chunk excerpts below are those described in the adjudication packet. No retrieval, evaluation, embedding, indexing, or metric operation was run.

## User-approved decisions

The user explicitly approved all five recommendations below. These are human decisions, not automated inferences.

| Question | Human decision | Fixed-size completeness | Structure-aware completeness |
|---|---|---|---|
| Q001 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q002 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q003 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q004 | `APPROVE_AS_PROPOSED` | `complete` | `complete` |
| Q005 | `APPROVE_AS_PROPOSED` | `incomplete` | `incomplete` |

## Evidence-based rationale

- **Q001 — APPROVE_AS_PROPOSED; both strategies complete.** The adjudication packet identifies the rank-1 fixed-size chunk `doc_001_fixed_size_00001_aee405d33739` and rank-1 structure-aware chunk `doc_001_structure_aware_00001_ac782e3816d0`. Each directly contains the commitment to tell customers how to take their complaint forward if still dissatisfied.
- **Q002 — APPROVE_AS_PROPOSED; both strategies complete.** Each strategy's rank-3 chunk directly supports both required details: acknowledgement of receipt of the loan application and the timeframe for disposing of the application being indicated in that acknowledgement.
- **Q003 — APPROVE_AS_PROPOSED; both strategies complete.** The fixed-size rank-7 and structure-aware rank-4 chunks directly state that borrower communications must be in the vernacular language or a language understood by the borrower.
- **Q004 — APPROVE_AS_PROPOSED; both strategies complete.** The fixed-size rank-4 and structure-aware rank-7 chunks support all four required sanction-communication details: communication in writing and in the vernacular language by sanction letter or otherwise; amount sanctioned; terms and conditions including annualized interest rate; and method of application of the interest rate.
- **Q005 — APPROVE_AS_PROPOSED; both strategies incomplete.** The revised required facets are distinct: the penal charge must be stated in bold and in the loan agreement. The fixed-size rank-5 and structure-aware rank-6 top-10 chunks support only the loan-agreement location facet (F4), not the bolding facet (F3). Therefore, neither strategy's top 10 covers all required facets. The packet's diagnostic evidence at ranks 19 and 17 is outside the top 10 and does not change these completeness decisions.

## Scope boundary and outstanding work

This record contains exactly five approved decisions: Q001–Q005. Questions Q006–Q025 have not been adjudicated by this milestone and remain pending. Approval here is limited to the five recommendations and completeness labels in the decision table; it is not approval of all v3 annotations, the whole evaluation dataset, or ground truth.

The next adjudication batch requires further explicit human instructions. No annotation status or proposal data should be changed as part of this documentation-only record.

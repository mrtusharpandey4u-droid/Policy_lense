# Q011 and Q013 Human Completeness Decision Record — Milestone 2B.39

## Decision authority and scope

On 2026-11-10, the user explicitly approved all four Q011 and Q013 completeness decisions after reviewing the Milestone 2B.38 decision sheet. These are human decisions, not assistant recommendations.

The decisions apply only to the four question/strategy combinations below. They confirm the existing `complete` proposal labels. Following the Q008 Milestone 2B.33 convention, they are recorded separately and do not update v3 or its reviewer/adjudication status fields.

## Human-approved decisions

| Question | Strategy | Human decision | Approved completeness label | Supporting gold-source chunk |
|---|---|---|---|---|
| Q011 | Fixed-size retrieval, top 10 | `APPROVE_AS_PROPOSED` | `complete` | `doc_016_fixed_size_00005_92e15d19bd51` |
| Q011 | Structure-aware retrieval, top 10 | `APPROVE_AS_PROPOSED` | `complete` | `doc_016_structure_aware_00006_d4c341ea43e2` |
| Q013 | Fixed-size retrieval, top 10 | `APPROVE_AS_PROPOSED` | `complete` | `doc_024_fixed_size_00002_15bb2fdc5f67` |
| Q013 | Structure-aware retrieval, top 10 | `APPROVE_AS_PROPOSED` | `complete` | `doc_024_structure_aware_00002_c7c2c87cf73a` |

All four proposed `complete` labels have been human-approved.

## Evidence basis and interpretation

The user-approved rationale is that each strategy's saved top 10 contains at least one gold-source chunk directly supporting every required facet:

- **Q011, fixed-size:** rank 5, `doc_016_fixed_size_00005_92e15d19bd51`, directly supports F1–F4.
- **Q011, structure-aware:** rank 8, `doc_016_structure_aware_00006_d4c341ea43e2`, directly supports F1–F4.
- **Q013, fixed-size:** rank 1, `doc_024_fixed_size_00002_15bb2fdc5f67`, directly supports F1–F3, including the requirement to obtain acknowledgement that the borrower understood the KFS.
- **Q013, structure-aware:** rank 1, `doc_024_structure_aware_00002_c7c2c87cf73a`, directly supports F1–F3, including the borrower-understanding acknowledgement.

The 2B.38 sheet records the distinction between direct support, partial support, and similar evidence from other issuers. For Q011, the fixed-size rank-10 same-source passage is partial for F2–F4 and does not support F1; it is supplementary, while other issuers' similar review/report language is not credited to Shriram Finance. For Q013, the same-source rank-9 fixed-size and rank-6 structure-aware KFS summary-box passages are partial for F1 only; KFS material retrieved from doc_003 concerns another entity and is not substituted for the doc_024 source. Completeness is judged against the direct gold-source support within each saved top 10, not rank alone.

## Current annotation state — observed, not changed

At the start of this milestone, v3 recorded `complete` for both retrieval strategies for Q011 and Q013. It also recorded:

- `reviewer_status`: `pending_user_adjudication`
- `adjudication_status`: `proposed_requires_user_approval`

Those status fields are preserved as-is. The human decisions in this record do not update v3, reviewer status, or adjudication status. This milestone does not claim that v3 was updated.

## Decision boundaries and limitations

These approvals:

- Apply only to Q011 and Q013 fixed-size and structure-aware top-10 completeness decisions listed above.
- Approve the four existing `complete` proposal labels, not the entire v3 dataset as ground truth.
- Do not approve or adjudicate any other question.
- Do not alter any facet definition, evidence mapping, retrieval result, or annotation.
- Do not authorize a change to v3 or to any reviewer/adjudication status.

Completeness conclusions are limited to the saved top-10 result sets inspected for Milestone 2B.38. Partial support and evidence from other issuers are not treated as full gold-source facet coverage.

## Validation record

Inspected:

- [`reports/q011_q013_retrieval_completeness_adjudication_2B38.md`](./q011_q013_retrieval_completeness_adjudication_2B38.md)
- [`reports/q008_human_completeness_decision_record_2B33.md`](./q008_human_completeness_decision_record_2B33.md)
- [`data/evaluation/evidence_annotations_v3.jsonl`](../data/evaluation/evidence_annotations_v3.jsonl)

Validation:

- **PASS:** All four user-approved decisions and labels are recorded exactly.
- **PASS:** Each decision is associated with the corresponding supporting gold-source chunk ID from the 2B.38 sheet.
- **PASS:** Direct, partial, and other-issuer evidence are distinguished.
- **PASS:** v3 was not modified. SHA-256 before this report was created: `32601478d681ca9a33e9ca73f0461f6f33f207b8dfd5025048ed5080930285d2`; size: 61,268 bytes.
- **PASS:** No reviewer or adjudication status was changed.
- **PASS:** This report is the only artifact created for Milestone 2B.39. Other worktree entries were pre-existing and left untouched.

No retrieval, evaluation, indexing, embedding, or metrics operation was run.

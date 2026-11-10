# Q008 Human Completeness Decision Record — Milestone 2B.33

## Decision authority and scope

After reviewing the Milestone 2B.32 decision sheet, the user explicitly supplied the two Q008 completeness decisions recorded below. These are human decisions, not assistant recommendations.

The decisions apply only to Q008's two saved retrieval strategies. They do not adjudicate Q011–Q025 or any other question, approve the complete v3 dataset as ground truth, or authorize a change to v3. No annotation or status was changed in this milestone.

## Human-approved decisions

| Strategy | Human decision | Approved completeness label |
|---|---|---|
| Fixed-size retrieval, top 10 | `APPROVE_AS_PROPOSED` | `complete` |
| Structure-aware retrieval, top 10 | `APPROVE_AS_PROPOSED` | `complete` |

## Approved Q008 facet definitions

These are the approved definitions used to review the saved top-10 evidence:

- **F1:** `Disclose the all-in cost, including charges involved in processing or sanction of the loan.`
- **F2:** `Disclose the all-in cost in a transparent manner.`
- **F3:** `Ensure that charges and fees are non-discriminatory.`

## Evidence basis and interpretation

The source is `doc_003`, [`data/pdfs/tchfl_fair_practices_code.pdf`](../data/pdfs/tchfl_fair_practices_code.pdf), printed page 4 (PDF page index 3), section 5.1(b). It states that the all-in processing/sanction cost is disclosed in a transparent manner and that the charges/fees are non-discriminatory.

The reviewed evidence was the saved top-10 content in [`data/evaluation/results/retrieval_evaluation_question_results.csv`](../data/evaluation/results/retrieval_evaluation_question_results.csv), cross-checked against [`data/evaluation/results/retrieval_evaluation_results.json`](../data/evaluation/results/retrieval_evaluation_results.json). The saved result lists agree:

- **Fixed-size top 10:** Rank 1, `doc_003_fixed_size_00005_96b0d302eff6`, directly supports F1, F2, and F3.
- **Structure-aware top 10:** Rank 2, `doc_003_structure_aware_00005_a9d262541873`, directly supports F1, F2, and F3.

The corresponding saved text was checked in [`data/processed/chunks/fixed_size.jsonl`](../data/processed/chunks/fixed_size.jsonl) and [`data/processed/chunks/structure_aware.jsonl`](../data/processed/chunks/structure_aware.jsonl). Each cited chunk contains the all-in cost and processing/sanction charges, the transparent-disclosure statement, and the separate non-discrimination sentence.

Completeness here is assessed within each strategy's saved top 10. Partial support does not count as full facet coverage. A single retrieved chunk can support multiple distinct facets; that means all those facets are present in the retrieved text, not that they represent independent retrieval events. No outside-top-10 diagnostic evidence was used.

## Current annotation state — observed, not changed

At the start of this task, [`data/evaluation/evidence_annotations_v3.jsonl`](../data/evaluation/evidence_annotations_v3.jsonl) recorded Q008 as follows:

- Exactly three facets with the approved F1/F2/F3 definitions above.
- Fixed-size completeness proposal: `complete`; `covered_facets` is `["F1", "F2", "F3"]`.
- Structure-aware completeness proposal: `complete`; `covered_facets` is `["F1", "F2", "F3"]`.
- `reviewer_status`: `pending_user_adjudication`.
- `adjudication_status`: `proposed_requires_user_approval`.

The human decisions in this report are recorded separately and do not update those JSONL fields. In particular, the v3 status fields remain as observed; this report does not apply either decision to project data.

## Decision boundaries and next authorized step

These decisions:

- Apply only to Q008's fixed-size and structure-aware top-10 completeness labels.
- Do not approve or adjudicate Q011–Q025 or any other question.
- Do not approve the complete v3 dataset as ground truth.
- Do not authorize any modification to v3.

A separate explicit user authorization is required before applying any Q008 annotation, completeness-label, or status update to v3.

## Validation record

Inspected:

- [`reports/q008_completeness_adjudication_decision_sheet_2B32.md`](./q008_completeness_adjudication_decision_sheet_2B32.md)
- [`reports/q008_human_adjudication_revision_2B31.md`](./q008_human_adjudication_revision_2B31.md)
- [`data/evaluation/evidence_annotations_v3.jsonl`](../data/evaluation/evidence_annotations_v3.jsonl)
- [`data/evaluation/results/retrieval_evaluation_question_results.csv`](../data/evaluation/results/retrieval_evaluation_question_results.csv)
- [`data/evaluation/results/retrieval_evaluation_results.json`](../data/evaluation/results/retrieval_evaluation_results.json)
- [`data/processed/chunks/fixed_size.jsonl`](../data/processed/chunks/fixed_size.jsonl)
- [`data/processed/chunks/structure_aware.jsonl`](../data/processed/chunks/structure_aware.jsonl)
- [`data/pdfs/tchfl_fair_practices_code.pdf`](../data/pdfs/tchfl_fair_practices_code.pdf)

The two human decisions and all three facet definitions were checked against the supplied decision and the reviewed decision sheet. The report was created as the only new artifact for this milestone. No existing report, dataset, annotation, evaluation result, chunk, PDF, code, configuration, or other project file was modified. Retrieval, indexing, embeddings, evaluation, and metrics were not run.

No human decision for another question was made. Batch 3 has not started.

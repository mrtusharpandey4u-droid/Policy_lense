# Q008 Human Adjudication Decision and Controlled Revision Plan — Milestone 2B.30

## Scope and explicit human decision

The user explicitly approved **Option B** from Milestone 2B.29: split Q008's combined F2 into two independently assessable facets and retain F1. This is a human-approved facet-structure decision.

The approved facet definitions, reproduced exactly, are:

| Facet ID | Approved requirement |
|---|---|
| F1 | Disclose the all-in cost, including charges involved in processing or sanction of the loan. |
| F2 | Disclose the all-in cost in a transparent manner. |
| F3 | Ensure that charges and fees are non-discriminatory. |

This approval is limited to facet structure and definitions. It does **not** approve either completeness label, complete Q008's overall adjudication, change any reviewer or adjudication status, adjudicate another question, or approve v3 as ground truth. The changes below are a plan only; they have not been applied.

## Starting workspace and record

Before creating this report:

- The proposed report path did not exist.
- `data/evaluation/evidence_annotations_v3.jsonl` SHA-256 was `67ad13f3f4186a601c6f154f96e3f630173d9d323554bc29111d5300c82a58fd`.
- `git status --short` showed pre-existing changes. Tracked modified paths were `README.md`, `data/manifest.csv`, `requirements.txt`, `src/config.py`, `src/extract.py`, `src/ingest.py`, and `src/search.py`. It also showed pre-existing untracked paths, including `data/evaluation/`, numerous reports and source files, and tests. These workspace changes are not part of this milestone and must not be overwritten or cleaned up.

The actual current Q008 record in v3 has two entries in `required_evidence_facets`, with `facet_id` and `requirement` fields and a nested `source` object containing `doc_id`, `pdf_pages`, and `excerpt`. Its `retrieval_completeness` object has `fixed_size_top10` and `structure_aware_top10` entries, each with a `status`, `covered_facets` array, and `supporting_chunks` array. The cited supporting chunk objects contain `rank`, `chunk_id`, `label`, `supported_facet_ids`, `annotation_method`, and `reviewer_status`.

Current Q008 proposal values:

- `reviewer_status`: `pending_user_adjudication`
- `adjudication_status`: `proposed_requires_user_approval`
- `fixed_size_top10.status`: `complete`
- `structure_aware_top10.status`: `complete`
- Current facets: F1 and combined F2

## Before/after facet comparison

| Current facet | Current definition | Proposed facet | Approved definition | Change |
|---|---|---|---|---|
| F1 | Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan. | F1 | Disclose the all-in cost, including charges involved in processing or sanction of the loan. | Retain F1 identity and source reference; use the exact approved requirement wording. |
| F2 | Disclose costs transparently and ensure charges/fees are non-discriminatory. | F2 | Disclose the all-in cost in a transparent manner. | Replace combined F2 with the distinct transparency requirement. |
| — | — | F3 | Ensure that charges and fees are non-discriminatory. | Add a separate non-discrimination requirement. |

The exact three approved definitions above govern the proposed result. F1's ID and current source attribution are retained; its requirement string changes from the current wording to the explicitly approved wording. The current combined F2 definition is removed.

## PROPOSED ONLY — NOT APPLIED

```diff
required_evidence_facets[facet_id="F1"].requirement:
- "Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan."
+ "Disclose the all-in cost, including charges involved in processing or sanction of the loan."

required_evidence_facets[facet_id="F1"].facet_id:
  "F1"  # unchanged
required_evidence_facets[facet_id="F1"].source:
  {"doc_id":"doc_003","pdf_pages":[4],"excerpt":"disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application"}  # unchanged

required_evidence_facets:
- [facet_id="F2", requirement="Disclose costs transparently and ensure charges/fees are non-discriminatory.", source={"doc_id":"doc_003","pdf_pages":[4],"excerpt":"in a transparent manner. It shall also be ensured that such charges/fees are non-discriminatory."}]
+ [facet_id="F2", requirement="Disclose the all-in cost in a transparent manner.", source={"doc_id":"doc_003","pdf_pages":[4],"excerpt":"Thus, we shall disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application in a transparent manner."}]
+ [facet_id="F3", requirement="Ensure that charges and fees are non-discriminatory.", source={"doc_id":"doc_003","pdf_pages":[4],"excerpt":"It shall also be ensured that such charges/fees are non-discriminatory."}]

retrieval_completeness.fixed_size_top10:
  status: "complete"  # unchanged proposal value
- covered_facets: ["F1", "F2"]
+ covered_facets: ["F1", "F2", "F3"]
  supporting_chunks[rank=1, chunk_id=doc_003_fixed_size_00005_96b0d302eff6].supported_facet_ids:
-   supported_facet_ids: ["F1", "F2"]
+   supported_facet_ids: ["F1", "F2", "F3"]

retrieval_completeness.structure_aware_top10:
  status: "complete"  # unchanged proposal value
- covered_facets: ["F1", "F2"]
+ covered_facets: ["F1", "F2", "F3"]
  supporting_chunks[rank=2, chunk_id=doc_003_structure_aware_00005_a9d262541873].supported_facet_ids:
-   supported_facet_ids: ["F1", "F2"]
+   supported_facet_ids: ["F1", "F2", "F3"]
```

The source excerpts proposed above are separate quotations from `doc_003`, PDF page 4, section 5.1(b). The saved fixed-size rank-1 chunk and structure-aware rank-2 chunk both contain the all-in-cost, transparent-disclosure, and non-discrimination statements. Therefore, their `supported_facet_ids` can map separately to F1, F2, and F3 based on the saved chunk contents. This does not claim the retrieval runs produced separate retrieval outcomes for F2 and F3: both obligations appear together in each cited chunk.

The labels `complete` are preserved as existing proposal values; they are not newly approved or inferred from the facet count change. `covered_facets` and `supported_facet_ids` are references to the assessed facets, so those arrays would need to include F3 in a later authorized edit if the cited chunks remain the supporting evidence.

## Fields to keep unchanged

Unless separately authorized, a future edit must preserve:

- `schema_version`, `question_id`, question text, and `question_category`.
- `gold_document_ids` and `gold_pdf_pages`.
- F1's `facet_id` and `source` object; only its `requirement` string is to use the exact approved wording above.
- The source document and page attribution for the new F2 and F3: `doc_003`, PDF page 4.
- Each retrieval strategy's `status` (`complete`) and all support-object values other than the two `supported_facet_ids` arrays described above.
- `table_clause_requirements`, `accepted_alternate_evidence_locations`, `annotation_notes`, `source_verification_status`, `annotation_method`, and any other omitted Q008 fields.
- Q008's `reviewer_status` (`pending_user_adjudication`) and `adjudication_status` (`proposed_requires_user_approval`).
- Every field of all other 24 question records.

No evidence reference is to be copied to a new facet without checking the actual cited chunk. That check was performed for the two current supporting chunks, which contain the source text for both new requirements. If either chunk reference or payload changes before a future authorized edit, re-check support separately for F1, F2, and F3 rather than assuming the current mapping still holds.

## Future authorized-revision validation plan

Perform these checks only after the user separately authorizes editing v3. Do not run them against a modified file as part of this planning milestone:

1. Parse every non-empty JSONL line; confirm the JSONL remains valid.
2. Confirm exactly 25 unique records remain, with IDs Q001–Q025.
3. Confirm Q008 has exactly three facets and the exact approved IDs and requirement strings shown above.
4. Confirm facet IDs are unique within Q008 and all facet references resolve.
5. Confirm `covered_facets` and `supported_facet_ids` contain only valid facet IDs, and verify each supporting chunk directly supports each facet assigned to it.
6. Confirm both completeness `status` values remain `complete` unless a separate human decision explicitly changes them.
7. Confirm Q008 remains `pending_user_adjudication` and its `adjudication_status` remains unchanged unless separately authorized.
8. Compare all non-Q008 records with a pre-edit snapshot; confirm all other 24 records are byte-for-byte or semantically unchanged as appropriate.
9. Confirm Q008's non-authorized fields remain unchanged.
10. Confirm historical reports and all other existing project artifacts remain untouched.
11. Record before/after hashes and inspect the diff to establish that only the specifically authorized Q008 fields changed.

## Risks, limitations, and rollback

- Splitting the combined facet changes the facet denominator from two to three. The two existing `complete` labels remain proposal values; this report does not authorize recomputing metrics or interpreting completeness as independently adjudicated.
- F1's exact approved wording differs slightly from the current requirement string. A future revision must use the exact approved text, not silently preserve the old phrase or introduce a further paraphrase.
- The evidence chunks co-locate the requirements. Their support mappings can identify each facet separately because the text contains each clause, but the saved runs do not show independent retrieval behavior for F2 versus F3.
- If an authorized edit fails validation, restore only the explicitly changed Q008 fields from a preserved pre-edit copy of the v3 file, verify the restored hash, and inspect the diff. Do not revert unrelated worktree changes.

## Milestone boundary

This report documents the explicit facet-structure approval and a controlled plan only. The v3 JSONL was not edited. No completeness or overall adjudication decision was made, no other question was adjudicated, and no retrieval, embeddings, indexing, evaluation, or metrics were run. Batch 3 is not begun.

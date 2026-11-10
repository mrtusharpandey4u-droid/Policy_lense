# Q008 Human Adjudication Annotation Revision — Milestone 2B.31

## Authorization and scope

The human explicitly authorized the exact Q008-only facet and reference changes documented in the Milestone 2B.30 plan. This revision applies only those changes to `data/evaluation/evidence_annotations_v3.jsonl`. No other question, status, completeness label, or project artifact was authorized for modification.

The pre-edit file was untracked within the existing untracked `data/evaluation/` directory. Its prior creation history or integrity before the captured pre-edit state cannot be established from Git. The actual pre-edit bytes were preserved in memory during the update for validation and rollback.

## Pre-edit integrity and worktree

Pre-edit observations:

- SHA-256: `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd`
- File size: `60681` bytes
- Q008 had two facets with the expected supporting references, reviewer status, adjudication status, and completeness proposal statuses.

This pre-edit hash matches the repeated value documented in the 2B.30S investigation. It differs from the value recorded in the older 2B.30 and 2B.30R reports. This revision records the hash actually observed immediately before editing; it does not claim that it establishes the historical creation or integrity of the untracked annotation file.

`git status --short` was captured before editing. It showed these pre-existing tracked modifications: `README.md`, `data/manifest.csv`, `requirements.txt`, `src/config.py`, `src/extract.py`, `src/ingest.py`, and `src/search.py`. It also showed pre-existing untracked paths, including `data/evaluation/`, reports, source files, and tests. No unrelated status entries were cleaned or overwritten.

## Exact Q008 facet changes

| Before | After |
|---|---|
| **F1:** Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan. | **F1:** Disclose the all-in cost, including charges involved in processing or sanction of the loan. |
| **F2:** Disclose costs transparently and ensure charges/fees are non-discriminatory. | **F2:** Disclose the all-in cost in a transparent manner. |
| — | **F3:** Ensure that charges and fees are non-discriminatory. |

F1 retains its existing `source` object unchanged. New sources are recorded for:

- **F2:** `doc_id: doc_003`, `pdf_pages: [4]`, excerpt: “Thus, we shall disclose ‘all in cost’ inclusive of all charges involved in processing/ sanction of loan application in a transparent manner.”
- **F3:** `doc_id: doc_003`, `pdf_pages: [4]`, excerpt: “It shall also be ensured that such charges/fees are non-discriminatory.”

No facet wording was paraphrased from the approved definitions.

## Supporting chunk verification

Before editing, each existing supporting reference was matched to exactly one saved chunk object and its text was inspected:

- Fixed-size, rank 1: `doc_003_fixed_size_00005_96b0d302eff6`, doc_003, pages 4–5. Its saved text contains the all-in cost and processing/sanction charges, the statement that the all-in cost is disclosed “in a transparent manner,” and the separate sentence that charges/fees “are non-discriminatory.”
- Structure-aware, rank 2: `doc_003_structure_aware_00005_a9d262541873`, doc_003, pages 3–4. Its saved text contains the same three source statements in section 5.1(b).

Both actual chunk texts directly support F1, F2, and F3. The mapping separates the facet IDs in the annotation; it does not claim these runs retrieved the two newly separated duties independently.

## Completeness and adjudication values

| Field | Before | After |
|---|---|---|
| `fixed_size_top10.status` | `complete` | `complete` |
| `fixed_size_top10.covered_facets` | `["F1", "F2"]` | `["F1", "F2", "F3"]` |
| Rank-1 `supported_facet_ids` | `["F1", "F2"]` | `["F1", "F2", "F3"]` |
| `structure_aware_top10.status` | `complete` | `complete` |
| `structure_aware_top10.covered_facets` | `["F1", "F2"]` | `["F1", "F2", "F3"]` |
| Rank-2 `supported_facet_ids` | `["F1", "F2"]` | `["F1", "F2", "F3"]` |
| `reviewer_status` | `pending_user_adjudication` | `pending_user_adjudication` |
| `adjudication_status` | `proposed_requires_user_approval` | `proposed_requires_user_approval` |

**Q008 completeness has NOT been newly adjudicated or approved.** The `complete` statuses remain proposal values. Q008's overall adjudication remains pending.

## Validation results

All required post-edit checks passed:

1. Every non-empty JSONL line parsed successfully.
2. Exactly 25 records remain.
3. There are 25 unique question IDs, exactly Q001–Q025.
4. Q008 has exactly three facets.
5. IDs and requirement strings are exactly F1/F2/F3 and the approved wording.
6. F1's source object is unchanged; F2 and F3 source doc/page/excerpt values match the authorized values.
7. Both `covered_facets` arrays are exactly `["F1", "F2", "F3"]`.
8. The specified rank-1 and rank-2 supporting chunk objects reference exactly the authorized facet IDs.
9. Each cited chunk's actual saved text directly supports all three assigned facets.
10. Both completeness statuses remain `complete`.
11. Q008 reviewer and adjudication statuses remain unchanged.
12. All non-authorized Q008 fields compare equal to their pre-edit values.
13. All other 24 question lines are byte-for-byte identical to the pre-edit JSONL lines.
14. The worktree status after editing showed no new or changed path beyond the authorized v3 content; pre-existing unrelated changes remain.

## Diff and post-edit integrity

The JSONL diff is limited to the Q008 record:

- Replace its two-entry `required_evidence_facets` array with the approved three-entry array.
- Update both strategies' `covered_facets` and the existing rank-1/rank-2 `supported_facet_ids` arrays to add F3.
- Preserve all other Q008 fields and all other record bytes.

The Q008 serialized JSONL line changed from 1,977 bytes to 2,232 bytes. Since v3 is untracked, Git does not provide a tracked-file diff against a repository baseline; the before/after byte comparison was performed against the in-memory pre-edit snapshot. No other existing project file was modified.

Post-edit:

- SHA-256: `c2666d5ca4bf37803f12bad333c4707c5b6e9cb8d79c75a2f578a14d4dd14746`
- File size: `60936` bytes

No validation failure occurred; rollback was not needed.

## Milestone boundary

No other question was adjudicated. No retrieval, embeddings, indexing, evaluation, or metrics were run. Batch 3 has **NOT** started. No completeness value, reviewer status, or adjudication status was changed, and v3 is not thereby approved as ground truth.

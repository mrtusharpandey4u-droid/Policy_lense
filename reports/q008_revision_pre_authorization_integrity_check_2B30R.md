# Q008 Revision Pre-Authorization Integrity Check — Milestone 2B.30R

## Scope

This is a read-only integrity check before any Q008 annotation revision is authorized. No completeness decision is made, and no annotation or adjudication status is changed.

## Current v3 file and hash comparison

The current file `data/evaluation/evidence_annotations_v3.jsonl` has SHA-256:

`67ad13f3f4186a601c6f154f96e3f630173d9d323554bc29111d5300c82a58fd`

| Supplied hash | Comparison with current file |
|---|---|
| `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd` | Does not match. |
| `67ad13f3f4186a601c6f154f96e3f630173d9d323554bc29111d5300c82a58fd` | Matches. |

The Milestone 2B.30 plan at `reports/q008_human_adjudication_decision_and_revision_plan_2B30.md` records `67ad13f3f4186a601c6f154f96e3f630173d9d323554bc29111d5300c82a58fd` as the starting v3 hash. That recorded value matches the current file. The two values supplied for comparison disagree at one character (`...c6c154...` versus `...c6f154...`). This check reports the calculated current value and does not infer or reconstruct which earlier transcription introduced the mismatch.

## Current Q008 record

The current JSONL contains 25 records. Q008 has exactly two facets:

| Facet ID | Current definition |
|---|---|
| F1 | Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan. |
| F2 | Disclose costs transparently and ensure charges/fees are non-discriminatory. |

Current statuses:

- `reviewer_status`: `pending_user_adjudication`
- `adjudication_status`: `proposed_requires_user_approval`
- `retrieval_completeness.fixed_size_top10.status`: `complete`
- `retrieval_completeness.structure_aware_top10.status`: `complete`

These are observed proposal values, not newly approved completeness decisions. The proposed three-facet revision has not been applied.

## Worktree status

`git status --short` was captured before creating this report. It showed the pre-existing modified tracked paths `README.md`, `data/manifest.csv`, `requirements.txt`, `src/config.py`, `src/extract.py`, `src/ingest.py`, and `src/search.py`, plus the already-existing untracked paths previously reported, including the 2B.29 clarification and 2B.30 decision/revision plan reports. No other newly detected workspace changes were identified in this check. This report is the only additional path created by this milestone; no pre-existing worktree changes were cleaned, reset, stashed, or overwritten.

## Integrity conclusion

The current v3 file matches the hash recorded in the 2B.30 plan and the second supplied hash. It does not match the first supplied hash. Because the supplied hashes conflict, the discrepancy between reported values remains even though the present file's hash is directly established.

**INTEGRITY_DISCREPANCY_REMAINS**

## Read-only confirmation

The current v3 record and all other pre-existing project files were not modified by this milestone. Only this integrity-check report was created. No retrieval, embeddings, indexing, evaluation, or metrics were run. No Q008 revision was applied; no completeness labels, reviewer statuses, or adjudication statuses were changed. Batch 3 was not begun.

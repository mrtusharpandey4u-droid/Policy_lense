# Q008 Stable Hash Investigation — Milestone 2B.30S

## Scope and timestamp

This read-only investigation checked the present byte-level stability of `data/evaluation/evidence_annotations_v3.jsonl` before any proposed Q008 revision. All timestamps below are UTC.

- Investigation started: `2026-11-10T05:16:14.432591+00:00`
- Git status captured: `2026-11-10T05:16:28Z`
- Investigation ended: `2026-11-10T05:16:14.432964+00:00`

## Sequential hash and metadata observations

The file was hashed three times sequentially. Size and modification-time metadata was recorded immediately before and after the calculations.

| Observation | Timestamp (UTC) | SHA-256 | Size (bytes) | Modification time (UTC) |
|---|---|---|---:|---|
| Before hashes | 2026-11-10T05:16:14.432772+00:00 | — | 60681 | 2026-11-09T15:51:31.035837+00:00 |
| Calculation 1 | 2026-11-10T05:16:14.432779+00:00 | `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd` | — | — |
| Calculation 2 | 2026-11-10T05:16:14.432845+00:00 | `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd` | — | — |
| Calculation 3 | 2026-11-10T05:16:14.432885+00:00 | `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd` | — | — |
| After hashes | 2026-11-10T05:16:14.432952+00:00 | — | 60681 | 2026-11-09T15:51:31.035837+00:00 |

All three hashes are identical. Size and modification time were unchanged during these observations. This confirms a stable hash for the file during this check; it does not establish historical stability outside the observation interval.

## Comparison with previous reports

- The 2B.30 plan, [`q008_human_adjudication_decision_and_revision_plan_2B30.md`](./q008_human_adjudication_decision_and_revision_plan_2B30.md), records `67ad13f3f4186a601c6f154f96e3f630173d9d323554bc29111d5300c82a58fd`.
- The 2B.30R report, [`q008_revision_pre_authorization_integrity_check_2B30R.md`](./q008_revision_pre_authorization_integrity_check_2B30R.md), identifies that same `...c6f154...` value as current and as the matching supplied hash. It lists `...c6c154...` as non-matching.
- The three calculations in this investigation instead all return `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd` (`...c6c154...`).

Thus, both existing reports' recorded current hash differs from the stable value observed here at one character (`c6f` versus `c6c` in that portion of the digest). The earlier execution transcript also records both values at different points. The available evidence establishes the present repeated result and the contents of the reports, but does not establish why the earlier observations or reports differ. No cause is inferred.

## Git status

The captured `git status --short` showed these tracked paths as modified:

- `README.md`
- `data/manifest.csv`
- `requirements.txt`
- `src/config.py`
- `src/extract.py`
- `src/ingest.py`
- `src/search.py`

It also showed the existing untracked project files and directories previously present in the worktree, including numerous reports, source files, tests, and `data/evaluation/`. The v3 file has no tracked modification entry; Git reports its containing `data/evaluation/` directory as untracked. Consequently, this status does not provide a tracked baseline or establish when/how that untracked file was created.

The investigation report target did not exist when checked. This new report is the only file created by this milestone; no existing status entry was cleaned, reset, stashed, or overwritten.

## Current Q008 record

The current JSONL has 25 records. Q008 has exactly two facets:

| Facet ID | Current definition |
|---|---|
| F1 | Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan. |
| F2 | Disclose costs transparently and ensure charges/fees are non-discriminatory. |

Current statuses remain:

- `reviewer_status`: `pending_user_adjudication`
- `adjudication_status`: `proposed_requires_user_approval`
- `retrieval_completeness.fixed_size_top10.status`: `complete`
- `retrieval_completeness.structure_aware_top10.status`: `complete`

No completeness judgment was made. The approved three-facet revision has not been applied.

## Conclusions and unknowns

- **Established:** The three sequential SHA-256 calculations match; the observed file size and modification time are unchanged before and after.
- **Established:** The current repeated hash is `67ad13f3f4186a601c6c154f96e3f630173d9d323554bc29111d5300c82a58fd`.
- **Established:** Both prior reports record a different value, `67ad13f3f4186a601c6f154f96e3f630173d9d323554bc29111d5300c82a58fd`.
- **Unknown:** The available evidence cannot explain why the earlier transcript and reports contain inconsistent hash observations. No attribution or cause can be established from the present file, metadata, report text, and Git status alone.
- **Unknown:** Since the v3 file is untracked, its creation history and any prior committed baseline cannot be established from this Git status.

No existing project file was modified during this milestone. The v3 annotation was not modified; no annotation revision, retrieval, indexing, embedding, evaluation, or metrics were performed. Q008's statuses and proposal completeness values were not changed. Batch 3 was not started.

**STABLE_HASH_CONFIRMED**

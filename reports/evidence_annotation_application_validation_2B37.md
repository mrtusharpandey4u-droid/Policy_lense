# Evidence Annotation Application and Validation — Milestone 2B.37

## Scope and authority

This milestone applies the already-approved Q011 facet split and Q013 F3 wording revision from the [2B.35 human decision record](./evidence_annotation_human_adjudication_decision_record_2B35.md), using the scoped details and source verification in the [2B.36 change report](./evidence_annotation_change_report_2B36.md).

Only Q011 and Q013 were edited in `data/evaluation/evidence_annotations_v3.jsonl`. The completeness decisions for Q012, Q014, and Q015 were explicitly approved by the user; both strategies for each already had `status: complete`, so those labels remain unchanged. As in the Q008 human completeness decision record, the human decisions are distinct from reviewer/adjudication status fields. No status values were invented or changed. Q011/Q013 completeness remains a pending proposal, not a human decision.

## Backup and file integrity

Before editing, an exact byte-for-byte backup was created outside the project at:

`/Users/tusharpandey/.copilot/session-state/90436abe-0bf1-4295-afc2-b07fde62194d/evidence_annotations_v3_pre_2B37.jsonl`

The backup matched the original v3 file exactly.

| Observation | SHA-256 | Bytes |
|---|---|---:|
| Before edit | `c2666d5ca4bf37803f12bad333c4707c5b6e9cb8d79c75a2f578a14d4dd14746` | 60,936 |
| After edit | `32601478d681ca9a33e9ca73f0461f6f33f207b8dfd5025048ed5080930285d2` | 61,268 |

## Exact changes applied

### Q011 — Approved facet split

Before:

| Facet | Requirement |
|---|---|
| F1 | `Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.` |
| F2 | `Provide for periodic review of FPC compliance and grievance-mechanism functioning at management levels.` |
| F3 | `Submit a consolidated report of reviews to the Board at prescribed regular intervals.` |

After:

| Facet | Requirement |
|---|---|
| F1 | `Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.` |
| F2 | `Periodic review of Fair Practices Code compliance at management levels.` |
| F3 | `Periodic review of grievance-mechanism functioning at management levels.` |
| F4 | `Submit a consolidated report of reviews to the Board at prescribed regular intervals.` |

F1 is unchanged. The former reporting facet's wording and source object are unchanged; its ID is now F4. The original F2 source attribution (`doc_016`, PDF page 5) is retained for each of the two split facets, since both are supported by the same source sentence. No source evidence was fabricated or reconstructed.

Both completeness objects were updated consistently:

- `covered_facets`: `["F1", "F2", "F3", "F4"]`
- Each existing direct supporting chunk's `supported_facet_ids`: `["F1", "F2", "F3", "F4"]`

No other Q011 facet-ID reference was present in the annotation structure. The existing direct evidence references remain the fixed-size rank-5 chunk `doc_016_fixed_size_00005_92e15d19bd51` and structure-aware rank-8 chunk `doc_016_structure_aware_00006_d4c341ea43e2`.

### Q013 — Approved F3 wording revision

Before:

`Explain the contents of the KFS and obtain borrower acknowledgement.`

After:

`Explain the contents of the KFS and obtain the borrower's acknowledgement that the borrower has understood it.`

Only the F3 `requirement` value changed. F1, F2, facet IDs, source attribution, and retrieval-evidence mappings are unchanged.

## Evidence mapping validation

**PASS — Q011:** the actual saved fixed-size rank-5 and structure-aware rank-8 chunk objects were inspected. Both contain the FPC-compliance periodic review, the grievance-mechanism-functioning periodic review at management levels, and the consolidated reporting requirement. Each existing supporting chunk directly supports F1–F4. The PDF source passage is `doc_016`, printed page 5 (PDF index 4), §6(b).

**PASS — Q013:** the actual saved fixed-size and structure-aware rank-1 chunk objects were inspected. Both contain the complete requirement to explain the KFS and obtain acknowledgement that the borrower understood it. This matches the source at `doc_024`, printed page 2 (PDF index 1), §1(b).

## Approved completeness decisions and pending decisions

| Question | Fixed-size top 10 | Structure-aware top 10 | Application/status handling |
|---|---|---|---|
| Q011 | Pending; existing `complete` remains a proposal | Pending; existing `complete` remains a proposal | No completeness decision or status change |
| Q012 | Human-approved `complete` | Human-approved `complete` | Existing completeness fields already equal `complete`; no data change required |
| Q013 | Pending; existing `complete` remains a proposal | Pending; existing `complete` remains a proposal | No completeness decision or status change |
| Q014 | Human-approved `complete` | Human-approved `complete` | Existing completeness fields already equal `complete`; no data change required |
| Q015 | Human-approved `complete` | Human-approved `complete` | Existing completeness fields already equal `complete`; no data change required |

The Q008 human completeness decision record kept `reviewer_status` and `adjudication_status` at their observed values and explicitly stated that the decisions were recorded separately without updating v3 status fields. That convention was followed. All reviewer and adjudication status fields for Q011–Q015 remain unchanged, including Q012's `needs_review`; this milestone makes no broader adjudication-status decision.

## Validation results

| Check | Result | Details |
|---|---|---|
| Every non-empty JSONL line parses | **PASS** | All records parse as JSON |
| Record count | **PASS** | Exactly 25 records |
| Question IDs unique | **PASS** | Exactly 25 unique IDs; order unchanged |
| Q011 facets and wording | **PASS** | Exactly F1–F4 with approved wording |
| Q011 facet references | **PASS** | Both coverage arrays and all existing support arrays reference F1–F4 only |
| Q011 evidence support | **PASS** | Actual saved supporting chunks inspected; each directly supports the assigned facets |
| Q013 exact F3 wording | **PASS** | Exact approved wording applied |
| Q013 preservation | **PASS** | No other Q013 value differs from baseline |
| Q012/Q014/Q015 completeness decisions | **PASS** | Both strategy labels for each are `complete`, matching human approvals |
| Q011/Q013 completeness pending | **PASS** | Proposal labels remain `complete`; pending statuses preserved and not represented as approvals |
| Unauthorized records | **PASS** | Q001–Q010 and Q016–Q025 remain byte-for-byte identical to baseline, including record line endings |
| Other fields | **PASS** | Q011 changes are limited to the approved facet split and corresponding facet references; Q013 change is limited to the approved F3 requirement |
| Existing annotation-specific automated tests | **NOT VERIFIED** | No annotation-specific test files or references were found under `tests/` or `src/`; no unrelated tests were substituted |
| New hash and byte count | **PASS** | Recorded above |

The candidate transformation was constructed from the preserved baseline, and only Q011 and Q013 JSONL lines were rewritten. The status/decision interpretation follows the existing Q008 convention. No unresolved evidence-mapping issue remains.

## Scope boundary

No other question was modified. No retrieval code, chunk, embedding, index, Qdrant collection, evaluation metric, source PDF, or unrelated worktree change was modified. This application does not approve the complete v3 dataset as ground truth.

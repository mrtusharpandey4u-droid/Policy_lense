# Controlled Annotation Change Report — Milestone 2B.36

## Scope and interpretation

This report translates the user-approved decisions in the [2B.35 human adjudication decision record](./evidence_annotation_human_adjudication_decision_record_2B35.md) into a controlled annotation change specification.

The instruction “without changing v3 yet” is followed: **no annotation data is changed in this milestone**. The Q011 split and Q013 wording revision below are specified for a later authorized application, not applied to `data/evaluation/evidence_annotations_v3.jsonl`. The approved Q012, Q014, and Q015 completeness decisions are incorporated here as separate human decision records only; their approved labels are not written into v3.

No existing report or other project data/code was modified. No retrieval, indexing, embeddings, evaluation, or metrics were run.

## Approved decision scope

| Question | Decision recorded | v3 action in this milestone |
|---|---|---|
| Q011 | Facet scope `SPLIT`, as explicitly approved by the user | None; specify split below, not applied |
| Q011 | Fixed-size and structure-aware completeness decisions were not supplied | Remain pending |
| Q012 | Both strategies `APPROVE_AS_PROPOSED`, approved label `complete` | Record decision here only; v3 unchanged |
| Q013 | Facet scope `REVISE`, as explicitly approved by the user | None; specify revised F3 below, not applied |
| Q013 | Fixed-size and structure-aware completeness decisions were not supplied | Remain pending |
| Q014 | Both strategies `APPROVE_AS_PROPOSED`, approved label `complete` | Record decision here only; v3 unchanged |
| Q015 | Both strategies `APPROVE_AS_PROPOSED`, approved label `complete` | Record decision here only; v3 unchanged |

These are question- and strategy-specific decisions. They do not approve the complete v3 dataset as ground truth.

## Controlled Q011 facet split specification

### Current v3 facets observed

- **F1:** `Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.`
- **F2:** `Provide for periodic review of FPC compliance and grievance-mechanism functioning at management levels.`
- **F3:** `Submit a consolidated report of reviews to the Board at prescribed regular intervals.`

### Approved split, not applied

The current combined F2 is to be replaced with two independently assessable facets. The former reporting facet moves from F3 to F4. The resulting exact proposed facet set is:

- **F1 — retain unchanged:** `Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.`
- **F2 — new:** `Periodic review of Fair Practices Code compliance at management levels.`
- **F3 — new:** `Periodic review of grievance-mechanism functioning at management levels.`
- **F4 — former F3, ID renumbered:** `Submit a consolidated report of reviews to the Board at prescribed regular intervals.`

The user-approved wording is supported by the complete source passage in `data/pdfs/doc_016_fair_practice_code_2023.pdf`, printed page 5 (PDF page index 4), §6(b):

> “The Board of Directors shall also provide for periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management. A consolidated report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.”

The source separately names FPC-compliance review and grievance-mechanism-functioning review. It applies both at various levels of management, supporting the independent F2 and F3 requirements. The proposed wording uses “Periodic” for “periodical” and “at management levels” for “at various levels of management”; these are concise paraphrases preserving the source meaning. The reporting obligation remains unchanged except for its facet ID.

**Q011 completeness:** both strategy decisions remain pending. The existing v3 `complete` values remain proposal values, not approvals. No `covered_facets` or `supported_facet_ids` remapping is performed here. Those mappings must be addressed in a separately authorized exact application step after this specification is reviewed.

## Controlled Q013 wording revision specification

### Current v3 facets observed

- **F1:** `Provide a standardized Key Facts Statement to all prospective borrowers before contract execution.`
- **F2:** `Write the KFS in a language understood by the borrower.`
- **F3:** `Explain the contents of the KFS and obtain borrower acknowledgement.`

### Approved F3 wording, not applied

The user-approved revised F3 is exactly:

`Explain the contents of the KFS and obtain the borrower's acknowledgement that the borrower has understood it.`

The complete source passage in `data/pdfs/doc_024_fair_practices_code_for_microfinanc.pdf`, printed page 2 (PDF page index 1), §1(b), states:

> “Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained that he/she has understood the same.”

The source directly supports the approved proposed wording. “The borrower has understood it” clarifies the antecedent of “the same” without adding a requirement. F1, F2, facet IDs, and source attribution are outside the approved Q013 scope and must remain unchanged in any later application.

**Q013 completeness:** both strategy decisions remain pending. The existing v3 `complete` values remain proposal values, not approvals. No `covered_facets` or `supported_facet_ids` changes are authorized by this decision.

## Recorded completeness decisions: Q012, Q014, and Q015

These decisions were explicitly supplied by the user and are recorded here as human decisions. They do not change v3.

| Question | Fixed-size top 10 | Structure-aware top 10 | Facet structure |
|---|---|---|---|
| Q012 | `APPROVE_AS_PROPOSED` — approved label `complete` | `APPROVE_AS_PROPOSED` — approved label `complete` | Retain existing seven facets |
| Q014 | `APPROVE_AS_PROPOSED` — approved label `complete` | `APPROVE_AS_PROPOSED` — approved label `complete` | Retain existing facets |
| Q015 | `APPROVE_AS_PROPOSED` — approved label `complete` | `APPROVE_AS_PROPOSED` — approved label `complete` | Retain existing facets |

The Q012, Q014, and Q015 completeness statuses in v3 are left as observed. The record does not update `reviewer_status`, `adjudication_status`, or any facet/evidence mapping.

## Preservation requirements for any future application

Any later authorized edit must be limited to the Q011 facet split and reporting-facet renumbering, Q013 F3 wording, and only the explicitly authorized completeness fields if separately approved for application. In particular:

- Do not infer Q011 or Q013 completeness approval from their facet decisions.
- Keep Q011 and Q013 completeness decisions pending until separately supplied.
- Retain Q012's seven facets and Q014/Q015 facet structures.
- Preserve all existing reviewer and adjudication statuses unless a separate explicit authorization permits a status change.
- Do not alter unrelated records or fields.
- Obtain explicit authorization before changing v3.

## Validation and integrity record

At the start of this milestone:

- `data/evaluation/evidence_annotations_v3.jsonl` contained 25 valid JSONL records.
- The Q011, Q012, Q013, Q014, and Q015 facet wording, statuses, and proposed completeness values were read directly from the file.
- Q011 and Q013 were `pending_user_adjudication` / `proposed_requires_user_approval`; their two strategy labels were still `complete`.
- Q012 was `pending_user_adjudication` / `needs_review`; its two strategy labels were `complete`.
- Q014 and Q015 were `pending_user_adjudication` / `proposed_requires_user_approval`; each strategy label was `complete`.
- The original PDFs and cited saved Q011/Q013 chunk text were checked to confirm the approved wording against the source.
- The target report path was absent.

| Integrity observation | SHA-256 | Byte size |
|---|---|---:|
| v3 before report creation | `c2666d5ca4bf37803f12bad333c4707c5b6e9cb8d79c75a2f578a14d4dd14746` | 60,936 |
| v3 after report creation | `c2666d5ca4bf37803f12bad333c4707c5b6e9cb8d79c75a2f578a14d4dd14746` | 60,936 |

**Validation outcome:** PASS — v3 hash and size are identical before and after; no annotation or status change was applied. The decision record and source wording were inspected. This report is the only project artifact added in this milestone. The pre-existing Git status already contained unrelated modified and untracked files; those paths were left untouched.

## Boundary and next step

This report records the approved Q011/Q013 facet-scope decisions and the approved Q012/Q014/Q015 completeness decisions without implementing them in v3. No other question was adjudicated, and the complete annotation dataset is not approved ground truth.

The next step is human review of this exact change specification. Applying any Q011/Q013 annotation changes or recording completeness/status values in v3 requires a separate explicit authorization. No implementation or subsequent milestone is started here.

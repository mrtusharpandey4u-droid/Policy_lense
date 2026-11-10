# Q011–Q015 Human Adjudication Decision Record — Milestone 2B.35

## Decision authority and scope

After reviewing the [Milestone 2B.34 evidence-preparation report](./evidence_annotation_human_adjudication_batch3_2B34.md), the user explicitly supplied the decisions recorded here. These are human decisions. Facet-scope decisions and retrieval-completeness decisions are recorded separately.

This is a documentation-only decision record. It does not update v3 or apply any facet wording, renumbering, coverage mapping, completeness label, or adjudication status. It does not approve any question beyond the exact decisions listed below and does not approve the complete v3 dataset as ground truth.

## Human decision register

| Question | Facet-scope decision | Fixed-size completeness decision | Structure-aware completeness decision | Current approval status |
|---|---|---|---|---|
| Q011 | `SPLIT` — separate current F2 into two facets; proposed existing reporting facet renumbered to F4 | Pending; no decision supplied | Pending; no decision supplied | Facet-scope approved; both completeness decisions pending |
| Q012 | Retain existing seven-facet structure | `APPROVE_AS_PROPOSED` — `complete` | `APPROVE_AS_PROPOSED` — `complete` | Both completeness decisions approved |
| Q013 | `REVISE` — clarify F3 to include acknowledgement that borrower understood the KFS | Pending; no decision supplied | Pending; no decision supplied | Facet-scope approved; both completeness decisions pending |
| Q014 | Retain existing facet structure | `APPROVE_AS_PROPOSED` — `complete` | `APPROVE_AS_PROPOSED` — `complete` | Both completeness decisions approved |
| Q015 | Retain existing facet structure | `APPROVE_AS_PROPOSED` — `complete` | `APPROVE_AS_PROPOSED` — `complete` | Both completeness decisions approved |

“Pending” means no human completeness decision has been supplied for that strategy. The unchanged `complete` values presently stored in v3 for Q011 and Q013 remain proposal values, not approvals.

## Q011 — Board duties

### Current annotation and human decision

The current Q011 facets in `data/evaluation/evidence_annotations_v3.jsonl` are:

- **F1:** `Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.`
- **F2:** `Provide for periodic review of FPC compliance and grievance-mechanism functioning at management levels.`
- **F3:** `Submit a consolidated report of reviews to the Board at prescribed regular intervals.`

The user decision is **`SPLIT`**. This approves separating the two review duties currently joined in F2. The controlled proposed revised structure is:

- **F1 — unchanged:** `Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.`
- **F2 — proposed:** `Periodic review of Fair Practices Code compliance at management levels.`
- **F3 — proposed:** `Periodic review of grievance-mechanism functioning at management levels.`
- **F4 — proposed renumbering of current F3:** `Submit a consolidated report of reviews to the Board at prescribed regular intervals.`

The proposed F2/F3 wording is a concise rendering of the two objects expressly named in the source; it does not add a different duty. The current report facet's wording is unchanged apart from proposed ID renumbering from F3 to F4. The current F1 is not part of the split.

### Source verification and wording assessment

The original source inspected was `data/pdfs/doc_016_fair_practice_code_2023.pdf`, printed page 5 (PDF page index 4), §6(b). The complete relevant passage states:

> “The Board of Directors shall also provide for periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management. A consolidated report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.”

The source separately names (1) review of FPC compliance and (2) review of grievance-redressal mechanism functioning, and applies both to various management levels. The original source therefore supports the distinction and proposed text. The current F2 wording and the passage in both saved cited chunks—fixed-size rank 5, `doc_016_fixed_size_00005_92e15d19bd51`, and structure-aware rank 8, `doc_016_structure_aware_00006_d4c341ea43e2`—were checked. Each contains the source sentence and subsequent reporting requirement.

**Wording limitation:** the source says “periodical review” and “at various levels of management.” The proposed use of “Periodic” and “at management levels” is a controlled paraphrase preserving those meanings. It is not a verbatim quotation; no further source discrepancy was found. The proposed IDs and wording are a record of the approved scope decision, not an applied v3 revision.

**Completeness boundary:** the user supplied no Q011 completeness decisions. Fixed-size and structure-aware completeness remain pending. Neither current `complete` proposal is human-approved by this record.

## Q012 — Repossession safeguards

The user explicitly approved both saved top-10 completeness proposals:

| Strategy | Human decision | Approved label |
|---|---|---|
| Fixed-size top 10 | `APPROVE_AS_PROPOSED` | `complete` |
| Structure-aware top 10 | `APPROVE_AS_PROPOSED` | `complete` |

The existing seven-facet structure is retained; the prior approved Q012 facet revision is not reopened or reverted. These approvals apply only to Q012's two retrieval strategies. No v3 labels or statuses are updated here.

## Q013 — KFS explanation and acknowledgement

### Current annotation and human decision

The current Q013 F3 wording in `data/evaluation/evidence_annotations_v3.jsonl` is:

`Explain the contents of the KFS and obtain borrower acknowledgement.`

The user decision is **`REVISE`**. The approved proposed revised F3 is exactly:

`Explain the contents of the KFS and obtain the borrower's acknowledgement that the borrower has understood it.`

F1 and F2 are outside this scope decision and remain unchanged.

### Source verification and wording assessment

The original source inspected was `data/pdfs/doc_024_fair_practices_code_for_microfinanc.pdf`, printed page 2 (PDF page index 1), §1(b). The complete relevant text states:

> “Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained that he/she has understood the same.”

This expressly supports both parts of the proposed F3: explain the contents and obtain the borrower's acknowledgement that the borrower understood the KFS. The current wording omits that qualification; the proposed revision restores it without adding a separate requirement. The sentence was also confirmed in the saved fixed-size rank-1 chunk `doc_024_fixed_size_00002_15bb2fdc5f67` and structure-aware rank-1 chunk `doc_024_structure_aware_00002_c7c2c87cf73a`.

**Wording limitation:** the source uses “he/she has understood the same”; the approved proposed text renders this as “the borrower has understood it.” This is a faithful referential clarification. No unresolved source wording issue was found.

**Completeness boundary:** the user supplied no Q013 completeness decisions. Fixed-size and structure-aware completeness remain pending. Neither current `complete` proposal is human-approved by this record.

## Q014 — Repayment collection location

The user explicitly approved both saved top-10 completeness proposals:

| Strategy | Human decision | Approved label |
|---|---|---|
| Fixed-size top 10 | `APPROVE_AS_PROPOSED` | `complete` |
| Structure-aware top 10 | `APPROVE_AS_PROPOSED` | `complete` |

The current facet structure remains unchanged. These approvals apply only to Q014's two retrieval strategies. No v3 labels or statuses are updated here.

## Q015 — Customer grievance-policy objectives

The user explicitly approved both saved top-10 completeness proposals:

| Strategy | Human decision | Approved label |
|---|---|---|
| Fixed-size top 10 | `APPROVE_AS_PROPOSED` | `complete` |
| Structure-aware top 10 | `APPROVE_AS_PROPOSED` | `complete` |

The current facet structure remains unchanged. These approvals apply only to Q015's two retrieval strategies. No v3 labels or statuses are updated here.

## Decision boundaries

- Q011 and Q013 facet-scope decisions are approved as recorded above; their fixed-size and structure-aware completeness decisions remain pending.
- Q012, Q014, and Q015 each have approved `complete` decisions for both retrieval strategies.
- No v3 annotation, completeness status, coverage array, support mapping, reviewer status, or adjudication status has been changed.
- No other question has been adjudicated by this milestone.
- The complete v3 dataset is not approved ground truth.
- A separate explicit authorization is required before any annotation modification.

## Next step

The next step is for the user to review this controlled decision record, followed by preparation of a separate exact annotation-revision plan for user approval. This milestone does not prepare or apply that revision.

## Validation record

Inspected:

- `reports/evidence_annotation_human_adjudication_batch3_2B34.md`
- `reports/evidence_annotation_human_adjudication_packet_2B26.md`
- `reports/evidence_annotation_human_adjudication_2B27.md`
- `reports/evidence_annotation_human_adjudication_2B28.md`
- `reports/q008_human_completeness_decision_record_2B33.md`
- `data/evaluation/evidence_annotations_v3.jsonl`
- `data/pdfs/doc_016_fair_practice_code_2023.pdf`, printed p. 5 / PDF page index 4
- `data/pdfs/doc_024_fair_practices_code_for_microfinanc.pdf`, printed p. 2 / PDF page index 1
- Saved chunk files `data/processed/chunks/fixed_size.jsonl` and `data/processed/chunks/structure_aware.jsonl`, for the cited Q011 and Q013 evidence objects

The user decisions and proposed wording above were checked against the exact task instructions, current v3 wording, original source PDF text, and saved supporting chunk text. Before writing, `data/evaluation/evidence_annotations_v3.jsonl` had SHA-256 `c2666d5ca4bf37803f12bad333c4707c5b6e9cb8d79c75a2f578a14d4dd14746` and size 60,936 bytes. Post-write validation is recorded by the task completion response.

The pre-write Git status contained numerous existing unrelated modifications and untracked project artifacts. This report path was absent at the start. Only this specified Markdown report is created by Milestone 2B.35; unrelated worktree changes are not modified. No retrieval, indexing, embeddings, evaluation, or metrics were run.

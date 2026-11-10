# Q008 Completeness Adjudication Decision Sheet — Milestone 2B.32

## Objective and scope

This source-grounded decision aid evaluates the current proposed Q008 top-10 completeness labels separately for fixed-size and structure-aware retrieval. The human-approved facet structure is:

| Facet | Approved requirement |
|---|---|
| F1 | Disclose the all-in cost, including charges involved in processing or sanction of the loan. |
| F2 | Disclose the all-in cost in a transparent manner. |
| F3 | Ensure that charges and fees are non-discriminatory. |

This report assesses saved evidence only; it does not make the human completeness decision. Q008 is not newly adjudicated, and neither proposed `complete` value is human-approved here.

## Evidence discovery and artifacts inspected

The saved result files were located by listing `data/evaluation/results/` and checking Q008 rows and strategy names, rather than assuming a retrieval-output filename. The exact artifacts used are:

- [`data/evaluation/results/retrieval_evaluation_question_results.csv`](../data/evaluation/results/retrieval_evaluation_question_results.csv) — Q008 row for each strategy, each with a serialized `retrieved_results` top-10 list.
- [`data/evaluation/results/retrieval_evaluation_results.json`](../data/evaluation/results/retrieval_evaluation_results.json) — saved structured Q008 results; its two top-10 lists were compared with the CSV and are identical.
- [`data/processed/chunks/fixed_size.jsonl`](../data/processed/chunks/fixed_size.jsonl) — source text looked up by every fixed-size result chunk ID.
- [`data/processed/chunks/structure_aware.jsonl`](../data/processed/chunks/structure_aware.jsonl) — source text looked up by every structure-aware result chunk ID.
- [`data/evaluation/evidence_annotations_v3.jsonl`](../data/evaluation/evidence_annotations_v3.jsonl) — current Q008 facets, citations, proposal labels, covered-facet arrays, and statuses.
- [`data/pdfs/tchfl_fair_practices_code.pdf`](../data/pdfs/tchfl_fair_practices_code.pdf) — original `doc_003` PDF, printed page 4 (PDF page index 3), section 5.1(b).

Both saved result lists contain exactly ten ranks. Each listed chunk ID was looked up in its corresponding saved chunk JSONL; all 20 IDs resolved to one chunk object, and the text of every listed chunk was inspected. The saved CSV and JSON result payloads agree on rank, chunk ID, document ID, page span, and saved `relevant` flag.

The source states in section 5.1(b) that the lender will disclose the all-in cost, inclusive of processing/sanction charges, “in a transparent manner,” and that “such charges/fees are non-discriminatory.” The source page confirms the three requirements being tested. The rank classifications below rely on actual retrieved text, not a result's relevance flag or chunk ID alone.

**Judgment key:** `Direct` means the retrieved text expressly establishes the facet. `Partial` means it contains relevant cost/disclosure or non-discrimination content but does not establish the full approved requirement. `No` means it does not establish that facet. Partial support is not counted as facet coverage.

## Fixed-size retrieval — full top 10

Evidence inventory (page spans are the saved result fields; chunk text availability records the actual lookup):

| Rank | Chunk ID | Doc ID | Pages | Chunk text | Saved result marked relevant | Inspection note |
|---:|---|---|---|---|---|---|
| 1 | `doc_003_fixed_size_00005_96b0d302eff6` | doc_003 | 4–5 | Retrieved and inspected | Yes | Section 5.1(b) expressly contains all-in processing/sanction cost, transparent disclosure, and non-discriminatory fees. |
| 2 | `doc_003_fixed_size_00023_a8eb1773a020` | doc_003 | 18–19 | Retrieved and inspected | No | Mentions service-charge/interest-rate display and transparency in company operations, but not the all-in processing/sanction cost. |
| 3 | `doc_003_fixed_size_00006_8bf99111838c` | doc_003 | 4–5 | Retrieved and inspected | Yes | Concerns KFS and notice of changes to listed rates/charges; these are related charge disclosures, not the all-in 5.1(b) requirement. |
| 4 | `doc_003_fixed_size_00012_e9c78e5dfd1c` | doc_003 | 9–10 | Retrieved and inspected | No | Transparently disclosed charges for switching loans and related loan information, but not the all-in processing/sanction cost. |
| 5 | `doc_003_fixed_size_00003_dbb2626b5f9e` | doc_003 | 2–3 | Retrieved and inspected | No | Advertisement and general fees/charges disclosure modes; no all-in processing/sanction cost or non-discrimination of charges. |
| 6 | `doc_002_fixed_size_00002_e8bfbf070883` | doc_002 | 2–3 | Retrieved and inspected | No | Another issuer's application and loan-processing policy; it does not establish doc_003's requirements. |
| 7 | `doc_024_fixed_size_00003_cb861a2996e0` | doc_024 | 2–3 | Retrieved and inspected | No | Microfinance loan APR/fee provisions from another issuer and product code; not evidence of doc_003's requirements. |
| 8 | `doc_003_fixed_size_00022_472ad6c21cae` | doc_003 | 17–18 | Retrieved and inspected | No | General non-discrimination in lending and accessibility provisions; does not specifically state non-discriminatory fees. |
| 9 | `doc_003_fixed_size_00007_2c72584c85de` | doc_003 | 5–6 | Retrieved and inspected | No | Property-document return and KFS provisions; no support for the three facets. |
| 10 | `doc_024_fixed_size_00002_15bb2fdc5f67` | doc_024 | 1–2 | Retrieved and inspected | No | Microfinance KFS/APR content from another issuer and product code; not evidence of doc_003's requirements. |

### Fixed-size facet support matrix

| Rank | F1 | F2 | F3 |
|---:|---|---|---|
| 1 | **Direct** | **Direct** | **Direct** |
| 2 | Partial | Partial | No |
| 3 | Partial | Partial | No |
| 4 | Partial | Partial | No |
| 5 | Partial | Partial | No |
| 6 | No | No | No |
| 7 | No | No | No |
| 8 | No | No | Partial |
| 9 | No | No | No |
| 10 | No | No | No |

- **F1 direct support:** rank 1. Partial related charge information occurs at ranks 2–5, but those passages do not state the all-in processing/sanction cost.
- **F2 direct support:** rank 1. Ranks 2–5 concern transparent, general, or changed-fee disclosure but do not establish transparent disclosure of the all-in processing/sanction cost.
- **F3 direct support:** rank 1. Rank 8 prohibits discrimination in lending generally, but does not expressly address charges/fees; it is only partial, not full coverage.
- **Partial/conflicting evidence:** No top-10 passage contradicts section 5.1(b). Several passages discuss related charges or broad non-discrimination, but none substitutes for the express rank-1 requirements. Notably, ranks 3 and 8 have saved `relevant` flags, but the inspected text does not directly establish the Q008 facets. The relevance flag is not treated as a facet decision.
- **Top-10 coverage:** All three facets are directly supported at rank 1. The same source chunk supports multiple facets; that is one retrieved chunk supporting three distinct textual requirements, not three independent retrieval successes.
- **Conclusion:** The saved fixed-size top 10 supports the proposed `complete` label across F1–F3. This is an evidence-based assistant assessment, not human approval.

## Structure-aware retrieval — full top 10

| Rank | Chunk ID | Doc ID | Pages | Chunk text | Saved result marked relevant | Inspection note |
|---:|---|---|---|---|---|---|
| 1 | `doc_003_structure_aware_00003_a8835ade6e1b` | doc_003 | 2–3 | Retrieved and inspected | No | General advertisements and common-fee disclosure modes; no all-in processing/sanction-cost passage. |
| 2 | `doc_003_structure_aware_00005_a9d262541873` | doc_003 | 3–4 | Retrieved and inspected | Yes | Section 5.1(b) expressly contains all-in processing/sanction cost, transparent disclosure, and non-discriminatory fees. |
| 3 | `doc_024_structure_aware_00003_c9a35a031d1e` | doc_024 | 2–3 | Retrieved and inspected | No | Microfinance APR and third-party charges from another issuer/product code; not evidence of doc_003's requirements. |
| 4 | `doc_003_structure_aware_00013_b5e4b30d14fb` | doc_003 | 10–11 | Retrieved and inspected | No | Guarantor and privacy provisions; no Q008 cost-disclosure requirement. |
| 5 | `doc_002_structure_aware_00002_6fcde47d0801` | doc_002 | 2–3 | Retrieved and inspected | No | Another issuer's application and loan-processing policy; it does not establish doc_003's requirements. |
| 6 | `doc_003_structure_aware_00012_0e6b3fb9870f` | doc_003 | 9–10 | Retrieved and inspected | No | Charges for switching loan rates are to be transparently disclosed; not the all-in processing/sanction cost. |
| 7 | `doc_003_structure_aware_00006_f9c845e0a416` | doc_003 | 4–5 | Retrieved and inspected | Yes | Loan appraisal, term-change notices, and charge changes; does not state the three 5.1(b) requirements. |
| 8 | `doc_024_structure_aware_00005_ad192a5e6e82` | doc_024 | 4–4 | Retrieved and inspected | No | Microfinance recovery and grievance provisions from another issuer/product code. |
| 9 | `doc_024_structure_aware_00002_c7c2c87cf73a` | doc_024 | 1–2 | Retrieved and inspected | No | Microfinance KFS/APR and charges from another issuer/product code; not evidence of doc_003's requirements. |
| 10 | `doc_003_structure_aware_00026_37c96e1037b3` | doc_003 | 19–19 | Retrieved and inspected | No | Fair Practices Code publication/display provisions; no express all-in cost or non-discriminatory fee statement. |

### Structure-aware facet support matrix

| Rank | F1 | F2 | F3 |
|---:|---|---|---|
| 1 | Partial | Partial | No |
| 2 | **Direct** | **Direct** | **Direct** |
| 3 | No | No | No |
| 4 | No | No | No |
| 5 | No | No | No |
| 6 | No | Partial | No |
| 7 | Partial | Partial | No |
| 8 | No | No | No |
| 9 | No | No | No |
| 10 | No | No | No |

- **F1 direct support:** rank 2. Ranks 1 and 7 mention fees/charges but do not state the all-in processing/sanction cost.
- **F2 direct support:** rank 2. Ranks 1, 6, and 7 provide related fee or charge disclosure, but do not establish transparent disclosure of the all-in processing/sanction cost. Rank 6 specifically concerns switching-rate charges.
- **F3 direct support:** rank 2. No other top-10 chunk expressly establishes that charges and fees are non-discriminatory.
- **Partial/conflicting evidence:** The result marked relevant at rank 7 discusses fee/charge notices and prospective changes, but does not contain Q008's all-in-cost, transparent-all-in-cost, or non-discriminatory-fees statements. It is therefore partial for F1/F2 at most, not direct coverage. No inspected passage contradicts the gold source.
- **Top-10 coverage:** All three facets are directly supported at rank 2. Other partial results do not count as additional full coverage.
- **Conclusion:** The saved structure-aware top 10 supports the proposed `complete` label across F1–F3. This is an evidence-based assistant assessment, not human approval.

## Annotation consistency checks

The current Q008 record in v3 was inspected and has exactly three facets with the approved wording. These proposal-consistency checks passed:

| Check | Current value | Result |
|---|---|---|
| Fixed-size `covered_facets` | `["F1", "F2", "F3"]` | PASS |
| Structure-aware `covered_facets` | `["F1", "F2", "F3"]` | PASS |
| Fixed-size rank-1 `supported_facet_ids` | `["F1", "F2", "F3"]` | PASS |
| Structure-aware rank-2 `supported_facet_ids` | `["F1", "F2", "F3"]` | PASS |
| Fixed-size completeness status | `complete` | PASS; proposal only |
| Structure-aware completeness status | `complete` | PASS; proposal only |
| `reviewer_status` | `pending_user_adjudication` | PASS |
| `adjudication_status` | `proposed_requires_user_approval` | PASS |

No values were changed.

## Limitations and safeguards

- The saved top-10 list and matching saved chunk text were available for both strategies; no required payload was missing. The CSV and JSON saved result lists match exactly.
- The retrieved chunks often include text spanning multiple printed pages. Their saved page ranges are reported above; the source-grounded Q008 clause itself is printed page 4.
- Each strategy's direct support for all three facets comes from a single rank-1 or rank-2 chunk. The same textual all-in-cost sentence supports F1 and F2, and the adjacent non-discrimination sentence supports F3. The facets are distinct assessment units, not independent retrieval events.
- Some other top-10 chunks contain related fee disclosure or broad non-discrimination language. Those are marked partial only where the text is relevant but lacks the approved facet's full scope. They are not counted as covered.
- `doc_002` and `doc_024` chunks concern other issuers or a separate microfinance product code and are not credited as evidence for doc_003's specific policy requirements.
- No outside-top-10 diagnostic result was used to support either strategy's completeness conclusion. No diagnostic rank is counted toward top-10 coverage.
- Retrieval, indexing, embeddings, evaluation, and metrics were not rerun or recomputed.

## Human decision fields — no decision recorded

No human completeness adjudication has yet occurred. Select a decision independently for each strategy; these fields are intentionally unfilled.

### Decision A — Fixed-size top-10 completeness

- **Current proposed label:** `complete`
- **Evidence:** Rank 1 directly supports F1, F2, and F3; ranks 4 and 5 partially support related cost disclosure, and rank 8 partially supports broader non-discrimination. Partial evidence is not needed to establish top-10 coverage because rank 1 directly supports all three facets.
- **Limitation:** The three facets are co-located in one relevant chunk, so this is not evidence of three independent retrieval events. The saved `relevant` labels at ranks 1 and 3 do not themselves determine facet coverage.
- **Assistant-prepared recommendation (not a human decision):** `APPROVE_AS_PROPOSED`, because one top-10 chunk directly states all three requirements.
- **Human decision:** `PENDING_HUMAN_DECISION — select one: APPROVE_AS_PROPOSED / REJECT_AS_PROPOSED / HOLD_FOR_CLARIFICATION`

### Decision B — Structure-aware top-10 completeness

- **Current proposed label:** `complete`
- **Evidence:** Rank 2 directly supports F1, F2, and F3. Ranks 1, 6, and 7 provide partial related price/charge disclosure but do not independently establish the full all-in-cost requirements.
- **Limitation:** The three facets are co-located in one rank-2 chunk; the result's `relevant` flag at rank 7 does not mean that rank 7 supports the three facets. No outside-top-10 diagnostic was counted.
- **Assistant-prepared recommendation (not a human decision):** `APPROVE_AS_PROPOSED`, because the rank-2 top-10 chunk directly states all three requirements.
- **Human decision:** `PENDING_HUMAN_DECISION — select one: APPROVE_AS_PROPOSED / REJECT_AS_PROPOSED / HOLD_FOR_CLARIFICATION`

`REJECT_AS_PROPOSED` would mean the human does not accept the current `complete` proposal for that strategy. It would not by itself establish an alternative label or authorize a data edit; any replacement label would require a separately explicit decision and authorized change.

## Completion validation

- Both complete saved top-10 lists inspected: **PASS** (10 results per strategy).
- Every listed chunk ID checked against saved chunk text: **PASS** (20 of 20 found and inspected).
- Support judgments grounded in actual text: **PASS**.
- Outside-top-10 evidence excluded: **PASS**.
- Current v3 consistency checks: **PASS**.
- No project data or code modified: **PASS**.
- Only the authorized new Markdown report created by this task: **PASS**.
- Neither proposed completeness label represented as human-approved: **PASS**.

No human adjudication has yet occurred. Q008 remains pending, no other question was adjudicated, and Batch 3 has not begun.

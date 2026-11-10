# Q011 and Q013 Retrieval Completeness Adjudication Decision Sheet

## Milestone 2B.38 — Human review preparation

### Objective and boundaries

This report prepares human completeness decisions for Q011 and Q013 across their saved fixed-size and structure-aware top-10 retrieval results. It applies the established project criterion: every required facet must have direct support somewhere within that strategy's top 10; partial or indirect support does not count as complete coverage. A single retrieved chunk can directly support multiple facets, but this represents one retrieved chunk, not multiple independent retrieval events.

The report does not make a human decision or change v3. Both questions' current `complete` values remain proposal labels. Their reviewer status remains `pending_user_adjudication` and adjudication status remains `proposed_requires_user_approval`.

### Records, evidence discovery, and validation method

Inspected:

- `data/evaluation/evidence_annotations_v3.jsonl`
- `data/evaluation/results/retrieval_evaluation_question_results.csv`
- `data/evaluation/results/retrieval_evaluation_results.json`
- `data/processed/chunks/fixed_size.jsonl`
- `data/processed/chunks/structure_aware.jsonl`
- `data/pdfs/doc_016_fair_practice_code_2023.pdf`
- `data/pdfs/doc_024_fair_practices_code_for_microfinanc.pdf`
- `reports/evidence_annotation_human_adjudication_decision_record_2B35.md`
- `reports/evidence_annotation_change_report_2B36.md`
- `reports/evidence_annotation_application_validation_2B37.md`
- `reports/q008_human_completeness_decision_record_2B33.md`
- `reports/q008_completeness_adjudication_decision_sheet_2B32.md`

The saved CSV and JSON top-10 lists agree on rank, chunk ID, document ID, and page range for all four question/strategy combinations. All 40 result references resolve to actual chunk objects; the object document IDs and page ranges match the saved results. The actual chunk text for every result was inspected. Relevant source PDF passages were inspected directly.

**Evidence status codes:** `D` = direct support; `P` = relevant but partial/indirect support; `—` = no support for a required facet; `N` = text addresses a similar duty but is from an issuer/document other than the gold source and is not credited to the target requirement. Only results at ranks 1–10 are considered.

### Current annotation state

| Question | Existing proposed label | Reviewer status | Adjudication status |
|---|---|---|---|
| Q011 | `complete` for each strategy | `pending_user_adjudication` | `proposed_requires_user_approval` |
| Q013 | `complete` for each strategy | `pending_user_adjudication` | `proposed_requires_user_approval` |

These are observed proposal values, not human approvals.

## Q011 — Board duties for grievance handling and Fair Practices Code compliance

### Current post-2B.37 facets

| Facet | Exact current v3 requirement |
|---|---|
| F1 | Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level. |
| F2 | Periodic review of Fair Practices Code compliance at management levels. |
| F3 | Periodic review of grievance-mechanism functioning at management levels. |
| F4 | Submit a consolidated report of reviews to the Board at prescribed regular intervals. |

**Gold source:** `doc_016`, Shriram Finance Limited, *Fair Practices Code*, printed p. 5 (PDF page index 4), §6(a)–(b). The original PDF states:

> “The Board of Directors of the Company shall lay down the appropriate grievance redressal mechanism within the organization. Such a mechanism shall ensure that all disputes arising out of the decisions of Company’s functionaries are heard and disposed of at least at the next higher level.”
>
> “The Board of Directors shall also provide for periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management. A consolidated report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.”

The source expressly supports all four distinct facets.

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Facet evidence assessment |
|---:|---|---|---|
| 1 | `doc_016_fixed_size_00001_3e76161d41b6` | doc_016, 1–1 | —; introduction and general FPC commitments, no four Board duties |
| 2 | `doc_016_fixed_size_00007_c0b5bc32280d` | doc_016, 6–7 | —; consumer education and complaint/ombudsman assistance, not §6 Board duties |
| 3 | `doc_001_fixed_size_00008_f643700e17c3` | doc_001, 7–8 | N; similar Board review/report language for Bajaj Finance, not Shriram |
| 4 | `doc_001_fixed_size_00011_be30ce0d52cd` | doc_001, 9–10 | —; Bajaj microfinance and gold-loan provisions, no Shriram Board duties |
| 5 | `doc_016_fixed_size_00005_92e15d19bd51` | doc_016, 4–5 | **D F1, F2, F3, F4**; contains §6(a)–(b) source passage |
| 6 | `doc_001_fixed_size_00001_aee405d33739` | doc_001, 1–4 | —; Bajaj Finance introduction and commitments |
| 7 | `doc_003_fixed_size_00002_8432983a1d35` | doc_003, 1–2 | —; Tata Capital Housing Finance opening provisions, no target duties |
| 8 | `doc_002_fixed_size_00005_65b6f505bfff` | doc_002, 5–6 | N; similar review/report duties for Tata Cleantech Capital, not Shriram |
| 9 | `doc_017_fixed_size_00003_01c87f6190f2` | doc_017, 2–3 | N; similar review/report duties for Aditya Birla Finance, not Shriram |
| 10 | `doc_016_fixed_size_00011_c9b767dbd0db` | doc_016, 9–9 | **P F2, F3, F4**; same-issuer monitoring passage, but less specific than §6(b); — F1 |

**Direct rank-5 text, doc_016 p. 5:** “The Board of Directors of the Company shall lay down the appropriate grievance redressal mechanism … [so] all disputes … are heard and disposed of at least at the next higher level.” It continues: “periodical review of the compliance of the FPC and the functioning of the grievances redressal mechanism at various levels of management” and “A consolidated report of such reviews shall be submitted to the Board at regular intervals, as may be prescribed by it.” This directly establishes F1–F4.

**Additional same-source rank-10 text, doc_016 p. 9:** “A review of the compliance of the FPC including the grievances redressal mechanism would be done by the Management regularly and a consolidated report will be submitted to the Board of Directors periodically.” This is relevant to F2 and F3, but less complete than rank 5: it does not state review at various management levels and describes the mechanism inclusively without specifying its functioning. For F4 it gives periodic Board reporting but omits “as may be prescribed.” It does not address F1. These limitations do not remove rank 5's direct support.

Ranks 3, 8, and 9 contain text similar to the Q011 duties, but identify other finance companies. They are not credited as evidence for Shriram's gold-source requirements.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Facet evidence assessment |
|---:|---|---|---|
| 1 | `doc_016_structure_aware_00001_465ed38df1ef` | doc_016, 1–1 | —; introduction, no four Board duties |
| 2 | `doc_016_structure_aware_00008_8909da55ae52` | doc_016, 6–8 | —; complaints and ombudsman responsibilities, not §6 Board duties |
| 3 | `doc_016_structure_aware_00002_1cf9097c9fc7` | doc_016, 1–2 | —; general governance and grievance commitments, not the four specific duties |
| 4 | `doc_003_structure_aware_00018_03fb79a24da9` | doc_003, 13–14 | N; similar Board duties for Tata Capital Housing Finance, not Shriram |
| 5 | `doc_001_structure_aware_00001_ac782e3816d0` | doc_001, 1–3 | —; Bajaj Finance introduction |
| 6 | `doc_001_structure_aware_00011_6d21474d762a` | doc_001, 10–10 | —; Bajaj microfinance and gold-loan provisions |
| 7 | `doc_003_structure_aware_00002_964c980ead5b` | doc_003, 1–2 | —; Tata Capital Housing Finance opening provisions |
| 8 | `doc_016_structure_aware_00006_d4c341ea43e2` | doc_016, 5–5 | **D F1, F2, F3, F4**; contains §6(a)–(b) source passage |
| 9 | `doc_001_structure_aware_00008_bd57eceffcf3` | doc_001, 7–8 | N; similar Board review/report duties for Bajaj Finance, not Shriram |
| 10 | `doc_002_structure_aware_00005_09f53cf3d4e9` | doc_002, 5–5 | N; similar review/report duties for Tata Cleantech Capital, not Shriram |

**Direct rank-8 text, doc_016 p. 5:** contains the same complete §6(a)–(b) passage quoted above and directly supports F1–F4. Ranks 4, 9, and 10 describe similar duties for different issuers; those similarities do not count as Shriram evidence.

### Q011 facet-by-facet top-10 coverage

| Facet | Fixed-size direct rank(s) | Fixed-size partial rank(s) | Structure-aware direct rank(s) | Structure-aware partial rank(s) |
|---|---:|---:|---:|---:|
| F1 | 5 | — | 8 | — |
| F2 | 5 | 10 | 8 | — |
| F3 | 5 | 10 | 8 | — |
| F4 | 5 | 10 | 8 | — |

**Interpretation:** fixed-size rank 5 alone and structure-aware rank 8 alone each directly state all four facets on the gold source. The additional fixed-size rank-10 monitoring passage is partial for F2–F4 and does not provide F1; it is supplementary, not necessary to establish top-10 completeness. Similar text for other issuers is not counted.

**Assistant-prepared recommendation (not a human decision):** `APPROVE_AS_PROPOSED` for both strategies. Consequence: a human approval would affirm the existing `complete` proposal for that strategy; a rejection would reject that proposed label and require a subsequent human-authorized correction; a hold would leave the decision unresolved pending clarification.

**Human decision fields — unfilled**

- Fixed-size top 10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top 10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)

## Q013 — KFS provision, language, explanation, and acknowledgement

### Current post-2B.37 facets

| Facet | Exact current v3 requirement |
|---|---|
| F1 | Provide a standardized Key Facts Statement to all prospective borrowers before contract execution. |
| F2 | Write the KFS in a language understood by the borrower. |
| F3 | Explain the contents of the KFS and obtain the borrower's acknowledgement that the borrower has understood it. |

**Gold source:** `doc_024`, Tata Capital Limited, *Fair Practices Code for Microfinance Loans*, printed p. 2 (PDF page index 1), §1(b). The original PDF states:

> “The Company shall provide a Key Facts Statement (KFS) to all prospective borrowers to help them take an informed view before executing the loan contract, as per the standardised format. The KFS shall be written in a language understood by such borrowers. Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained that he/she has understood the same.”

This passage directly establishes F1, F2, and the complete revised F3, including the understanding qualification.

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Facet evidence assessment |
|---:|---|---|---|
| 1 | `doc_024_fixed_size_00002_15bb2fdc5f67` | doc_024, 1–2 | **D F1, F2, F3**; contains full §1(b), including acknowledgement of understanding |
| 2 | `doc_002_fixed_size_00002_e8bfbf070883` | doc_002, 2–3 | N; another issuer's communications/language and loan-application provisions |
| 3 | `doc_024_fixed_size_00004_e6145695ee32` | doc_024, 3–4 | —; recovery location and collection safeguards |
| 4 | `doc_024_fixed_size_00005_23b340ab4a76` | doc_024, 3–4 | —; recovery-agent and other provisions |
| 5 | `doc_003_fixed_size_00023_a8eb1773a020` | doc_003, 18–19 | N; Tata Capital Housing Finance material, not the target doc_024 provision |
| 6 | `doc_003_fixed_size_00006_8bf99111838c` | doc_003, 4–5 | N; Tata Capital Housing Finance KFS rules for its digital lending products, not doc_024 microfinance borrowers |
| 7 | `doc_003_fixed_size_00022_472ad6c21cae` | doc_003, 17–18 | N; Tata Capital Housing Finance accessibility provisions, not target source |
| 8 | `doc_003_fixed_size_00005_96b0d302eff6` | doc_003, 4–5 | N; Tata Capital Housing Finance loan provisions, not target source |
| 9 | `doc_024_fixed_size_00003_cb861a2996e0` | doc_024, 2–3 | **P F1**; mentions the KFS summary box in the loan agreement, but not the full standardized prospective-borrower/timing requirement; — F2, F3 |
| 10 | `doc_003_fixed_size_00002_8432983a1d35` | doc_003, 1–2 | N; Tata Capital Housing Finance opening provisions, not target source |

**Direct rank-1 text, doc_024 pp. 1–2:** “provide a Key Facts Statement (KFS) to all prospective borrowers … before executing the loan contract, as per the standardised format”; “The KFS shall be written in a language understood by such borrowers”; and “Contents of KFS shall be explained to the borrower and an acknowledgement shall be obtained that he/she has understood the same.” This directly supports F1, F2, and F3 as worded in v3.

**Partial rank-9 text, doc_024 pp. 2–3:** “The KFS shall also be included as a summary box to be exhibited as part of the loan agreement.” The same chunk discusses APR/charges and the loan card. It does not expressly establish that a standardized KFS is supplied to all prospective borrowers before contract execution, nor does it state the language or the explanation-and-understanding acknowledgement. It is partial context for F1 only and cannot independently establish that full facet.

Rank 6 discusses KFS provisions for digital lending products under doc_003 (Tata Capital Housing Finance), a different source document/entity. It is related context only and is not credited to doc_024's requirements.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Facet evidence assessment |
|---:|---|---|---|
| 1 | `doc_024_structure_aware_00002_c7c2c87cf73a` | doc_024, 1–2 | **D F1, F2, F3**; contains full §1(b), including acknowledgement of understanding |
| 2 | `doc_024_structure_aware_00005_ad192a5e6e82` | doc_024, 4–4 | —; recovery-agent, outsourcing, and complaint-mechanism material |
| 3 | `doc_002_structure_aware_00002_6fcde47d0801` | doc_002, 2–3 | N; another issuer's communications and application process |
| 4 | `doc_003_structure_aware_00006_f9c845e0a416` | doc_003, 4–5 | N; Tata Capital Housing Finance's digital lending KFS provision, not target doc_024 |
| 5 | `doc_003_structure_aware_00005_a9d262541873` | doc_003, 3–4 | N; Tata Capital Housing Finance sales-agent provisions |
| 6 | `doc_024_structure_aware_00003_c9a35a031d1e` | doc_024, 2–3 | **P F1**; mentions KFS summary box in loan agreement, not the complete F1; — F2, F3 |
| 7 | `doc_003_structure_aware_00026_37c96e1037b3` | doc_003, 19–19 | N; Tata Capital Housing Finance material |
| 8 | `doc_024_structure_aware_00004_ea79c085f5a8` | doc_024, 3–4 | —; recovery safeguards |
| 9 | `doc_003_structure_aware_00002_964c980ead5b` | doc_003, 1–2 | N; Tata Capital Housing Finance opening provisions |
| 10 | `doc_003_structure_aware_00013_b5e4b30d14fb` | doc_003, 10–11 | N; Tata Capital Housing Finance loan/guarantor material |

**Direct rank-1 text, doc_024 pp. 1–2:** contains the same complete §1(b) text quoted above and directly supports all three facets, including the acknowledgement that the borrower understood the KFS.

**Partial rank-6 text, doc_024 pp. 2–3:** includes the KFS summary-box-in-loan-agreement provision, APR and charges, and loan-card requirements. It does not provide the full F1 timing/prospective-borrower obligation, and it does not contain F2 or the revised F3 understanding acknowledgement. It is partial context for F1 only. The doc_003 KFS result at rank 4 concerns a different Tata entity and digital-lending provisions; it is not credited to doc_024.

### Q013 facet-by-facet top-10 coverage

| Facet | Fixed-size direct rank(s) | Fixed-size partial rank(s) | Structure-aware direct rank(s) | Structure-aware partial rank(s) |
|---|---:|---:|---:|---:|
| F1 | 1 | 9 | 1 | 6 |
| F2 | 1 | — | 1 | — |
| F3 | 1 | — | 1 | — |

**Interpretation:** each strategy's rank-1 chunk directly supports the complete revised F3, not merely KFS explanation or a generic acknowledgement. The actual retrieved text expressly says acknowledgement is obtained that the borrower “has understood the same.” The same chunk also directly supports F1 and F2. Same-source ranks 9 and 6 are partial context for F1 only. Results from doc_003, even where they mention KFS requirements, are not substituted for the doc_024 gold source.

**Assistant-prepared recommendation (not a human decision):** `APPROVE_AS_PROPOSED` for both strategies. Consequence: a human approval would affirm the existing `complete` proposal for that strategy; a rejection would reject that proposal and require a subsequent human-authorized correction; a hold would leave the decision unresolved pending clarification.

**Human decision fields — unfilled**

- Fixed-size top 10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top 10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)

## Consolidated decision comparison

| Question / strategy | Proposed label | Required facets directly supported within top 10 | Partial or non-credited evidence | Assistant-prepared recommendation |
|---|---|---|---|---|
| Q011 fixed-size | `complete` | F1–F4, rank 5 | Rank 10 partially supports F2–F4; similar text at ranks 3, 8, 9 is other issuers | `APPROVE_AS_PROPOSED` |
| Q011 structure-aware | `complete` | F1–F4, rank 8 | Similar duties at rank 4 (doc_003), 9 (doc_001), 10 (doc_002) are other issuers | `APPROVE_AS_PROPOSED` |
| Q013 fixed-size | `complete` | F1–F3, rank 1 | Rank 9 partially supports F1 only; doc_003 KFS material is another entity | `APPROVE_AS_PROPOSED` |
| Q013 structure-aware | `complete` | F1–F3, rank 1 | Rank 6 partially supports F1 only; doc_003 KFS material is another entity | `APPROVE_AS_PROPOSED` |

The decision options follow the Q008 completeness decision sheet precedent: `APPROVE_AS_PROPOSED`, `REJECT_AS_PROPOSED`, or `HOLD_FOR_CLARIFICATION`. Rejecting the proposal means the current `complete` label would not be accepted for that strategy; it does not itself specify a replacement label or alter data. Holding leaves the decision pending further clarification. The assistant recommendations above are not human approvals.

## Human decision record — leave unfilled

| Decision | Human choice | Human rationale |
|---|---|---|
| Q011 fixed-size top 10 | `________________` | `________________` |
| Q011 structure-aware top 10 | `________________` | `________________` |
| Q013 fixed-size top 10 | `________________` | `________________` |
| Q013 structure-aware top 10 | `________________` | `________________` |

No human completeness decision has yet been recorded for Q011 or Q013. No reviewer/adjudication status or v3 completeness field was changed in this milestone.

## Validation and limitations

- **PASS:** v3 contained the post-2B.37 Q011 F1–F4 and Q013 F1–F3 wordings shown above at review start.
- **PASS:** all four saved top-10 result lists contain exactly ten ranks and CSV/JSON rank, chunk, document, and page metadata agree.
- **PASS:** all 40 retrieved chunk IDs resolve to actual saved chunk objects with matching document/page metadata; actual text was inspected.
- **PASS:** supporting claims and partial-support judgments cite actual text, not titles or labels.
- **PASS:** no outside-top-10 results were used.
- **PASS:** cross-issuer similarities were not counted as evidence for the gold-source question.
- **PASS:** decision options and the direct-support completeness threshold follow the Q008 adjudication precedent.
- **PASS:** no human recommendation is represented as a user decision.
- **PASS:** v3 was read-only. Its SHA-256 before and after report creation is `32601478d681ca9a33e9ca73f0461f6f33f207b8dfd5025048ed5080930285d2`; its size before and after is 61,268 bytes.
- **PASS:** the only artifact created by this milestone is this decision sheet. Other modified and untracked worktree entries were already present and were left untouched.

No retrieval, embedding, indexing, evaluation, or metrics operation was run. The decision sheet is for human review only; annotation changes require separate authorization.

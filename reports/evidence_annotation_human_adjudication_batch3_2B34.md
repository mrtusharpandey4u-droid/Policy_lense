# Evidence Annotation Human Adjudication Preparation — Q011–Q015

## Milestone 2B.34: Source-Grounded Decision Sheet

### Objective and scope

This report prepares, but does not make, human adjudication decisions for Q011–Q015. It evaluates each current facet against the original source and the actual saved top-10 chunk text for fixed-size and structure-aware retrieval.

This is a read-only review. No annotation, retrieval, chunk, index, embedding, evaluation, source PDF, code, configuration, or earlier report was modified. No human decision is prefilled. No Q008 decision is revisited, no other question is adjudicated, and Batch 3 is not being started.

### Evidence artifacts and method

Artifacts inspected:

- `data/evaluation/evidence_annotations_v3.jsonl`
- `data/evaluation/evaluation_questions.jsonl`
- `data/evaluation/results/retrieval_evaluation_question_results.csv`
- `data/evaluation/results/retrieval_evaluation_results.json`
- `data/processed/chunks/fixed_size.jsonl`
- `data/processed/chunks/structure_aware.jsonl`
- `data/pdfs/doc_016_fair_practice_code_2023.pdf`
- `data/pdfs/doc_024_fair_practices_code_for_microfinanc.pdf`
- `data/pdfs/doc_023_merged_customer_service_and_grievan.pdf`
- `reports/evidence_annotation_human_adjudication_packet_2B26.md`
- `reports/final_evidence_audit_reconciliation_2B25.md`
- `reports/evidence_annotation_revision_2B24R.md`
- `reports/evidence_annotation_decision_sheet_v3.md`

The packet and earlier reports were used for discovery and history only. Support judgments below are based on the saved chunk objects' text and original source passages, not on packet excerpts, chunk IDs, or the retrieval output's `relevant` flag. The saved per-question CSV lists were compared with the JSON result records: all ten Q011–Q015 strategy lists agree in rank, chunk ID, document ID, and page range. All 100 chunk IDs resolve to actual saved chunk objects; their document IDs and page ranges match the result records, and text was available for all 100.

Only rank 1–10 is counted. Similar wording in another company's policy is not credited to the gold-source question. A result from the correct source that addresses only a related topic is marked partial only where it establishes part of a facet; topical similarity alone is not support. “D” means direct support, “P” partial support, and “—” no support for the question's gold-source requirement. Page numbers below use the saved results' 1-based PDF page convention.

### Source and annotation state

| Question | Gold source and inspected source passage | Current facets / proposed labels | Current reviewer / adjudication status |
|---|---|---|---|
| Q011 | `doc_016`, Shriram Finance Fair Practices Code, printed p. 5 (PDF p. 5; PDF page index 4), §6(b) | F1–F3; both `complete` | `pending_user_adjudication` / `proposed_requires_user_approval` |
| Q012 | `doc_016`, printed p. 6 (PDF p. 6; PDF page index 5), §9 | F1–F7; both `complete` | `pending_user_adjudication` / `needs_review` |
| Q013 | `doc_024`, Tata Capital Fair Practices Code for Microfinance Loans, printed p. 1 (PDF p. 2; PDF page index 1), §1(b) | F1–F3; both `complete` | `pending_user_adjudication` / `proposed_requires_user_approval` |
| Q014 | `doc_024`, printed p. 3 (PDF p. 3; PDF page index 2), §2(b) | F1–F2; both `complete` | `pending_user_adjudication` / `proposed_requires_user_approval` |
| Q015 | `doc_023`, Tata Capital Customer Service and Grievance Handling SOP, printed p. 2 (PDF p. 2; PDF page index 1), §2 | F1–F3; both `complete` | `pending_user_adjudication` / `proposed_requires_user_approval` |

The exact question wording, gold document/page references, facet definitions, coverage arrays, support-chunk references, labels, and statuses were read from v3. All five questions appear in the canonical evaluation dataset with matching wording. The current proposals are consistency-check values only; no field was changed.

## Q011 — Board duties for grievance handling and Fair Practice Code compliance

**Source passage (doc_016, §6(b), p. 5):** the Board lays down a grievance mechanism ensuring disputes over functionaries' decisions are heard and disposed of at least at the next higher level; it provides periodic review of FPC compliance and grievance-mechanism functioning at various management levels; and submits a consolidated report of those reviews to the Board at prescribed regular intervals.

Current facets:

- **F1:** Lay down a grievance-redressal mechanism that escalates disputes from company functionaries to at least the next higher level.
- **F2:** Provide for periodic review of FPC compliance and grievance-mechanism functioning at management levels.
- **F3:** Submit a consolidated report of reviews to the Board at prescribed regular intervals.

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 |
|---:|---|---|---|---|
| 1 | `doc_016_fixed_size_00001_3e76161d41b6` | doc_016, 1–1 | Yes | — / — / — |
| 2 | `doc_016_fixed_size_00007_c0b5bc32280d` | doc_016, 6–7 | Yes | — / — / — |
| 3 | `doc_001_fixed_size_00008_f643700e17c3` | doc_001, 7–8 | Yes | — / — / — (Bajaj Finance, not the gold source) |
| 4 | `doc_001_fixed_size_00011_be30ce0d52cd` | doc_001, 9–10 | Yes | — / — / — (Bajaj Finance, not the gold source) |
| 5 | `doc_016_fixed_size_00005_92e15d19bd51` | doc_016, 4–5 | Yes | D / D / D |
| 6 | `doc_001_fixed_size_00001_aee405d33739` | doc_001, 1–4 | Yes | — / — / — (Bajaj Finance, not the gold source) |
| 7 | `doc_003_fixed_size_00002_8432983a1d35` | doc_003, 1–2 | Yes | — / — / — (Tata Capital Housing Finance, not the gold source) |
| 8 | `doc_002_fixed_size_00005_65b6f505bfff` | doc_002, 5–6 | Yes | — / — / — (Tata Cleantech Capital, not the gold source) |
| 9 | `doc_017_fixed_size_00003_01c87f6190f2` | doc_017, 2–3 | Yes | — / — / — (Aditya Birla Capital, not the gold source) |
| 10 | `doc_016_fixed_size_00011_c9b767dbd0db` | doc_016, 9–9 | Yes | — / P / D |

Rank 5 expressly contains all three Board duties in §6(b). Rank 10, a separate Shriram monitoring passage, says Management regularly reviews FPC compliance including the grievance mechanism and periodically submits a consolidated report to the Board. It partially supports F2 because it does not specify review at the various management levels; it directly supports the reporting element in F3. Other companies' similar Board-review provisions are not Shriram evidence.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 |
|---:|---|---|---|---|
| 1 | `doc_016_structure_aware_00001_465ed38df1ef` | doc_016, 1–1 | Yes | — / — / — |
| 2 | `doc_016_structure_aware_00008_8909da55ae52` | doc_016, 6–8 | Yes | — / — / — |
| 3 | `doc_016_structure_aware_00002_1cf9097c9fc7` | doc_016, 1–2 | Yes | P / P / — |
| 4 | `doc_003_structure_aware_00018_03fb79a24da9` | doc_003, 13–14 | Yes | — / — / — (Tata Capital Housing Finance, not the gold source) |
| 5 | `doc_001_structure_aware_00001_ac782e3816d0` | doc_001, 1–3 | Yes | — / — / — (Bajaj Finance, not the gold source) |
| 6 | `doc_001_structure_aware_00011_6d21474d762a` | doc_001, 10–10 | Yes | — / — / — (Bajaj Finance, not the gold source) |
| 7 | `doc_003_structure_aware_00002_964c980ead5b` | doc_003, 1–2 | Yes | — / — / — (Tata Capital Housing Finance, not the gold source) |
| 8 | `doc_016_structure_aware_00006_d4c341ea43e2` | doc_016, 5–5 | Yes | D / D / D |
| 9 | `doc_001_structure_aware_00008_bd57eceffcf3` | doc_001, 7–8 | Yes | — / — / — (Bajaj Finance, not the gold source) |
| 10 | `doc_002_structure_aware_00005_09f53cf3d4e9` | doc_002, 5–5 | Yes | — / — / — (Tata Cleantech Capital, not the gold source) |

Rank 8 contains the complete §6(b) passage and directly supports F1–F3. Rank 3 describes Shriram's general fair-lending governance, monitoring/auditing, and robust grievance mechanism, but does not state the particular escalation, review, or Board-reporting requirements; it is partial context for F1 and F2 only. The similar Tata Housing passage at rank 4 is not attributable to Shriram.

### Facet matrix and assessment

| Facet | Fixed-size direct ranks | Fixed-size partial ranks | Structure-aware direct ranks | Structure-aware partial ranks |
|---|---:|---:|---:|---:|
| F1 | 5 | — | 8 | 3 |
| F2 | 5 | 10 | 8 | 3 |
| F3 | 5, 10 | — | 8 | — |

All three facets have direct support within each strategy's top 10. Thus, both existing `complete` proposals appear supported by saved top-10 evidence. F2 combines two independently identifiable review subjects—FPC compliance and grievance-mechanism functioning—in one source sentence and one annotation facet. The retrieved direct chunks contain both subjects. Whether to retain that combined facet or split it is a separate source-fidelity/assessment-design decision; no split is made here.

**Assistant-prepared recommendation (not a human decision):** the proposed completeness labels are supported for both strategies. Consider whether F2 should be split before finalizing facet structure; if retained, assess it as requiring evidence for both review subjects.

**Human decision fields — leave blank**

- Fixed-size top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Human rationale: `____________________________________________________________`

## Q012 — Repossession safeguards in Shriram Finance vehicle loan agreements

**Source passage (doc_016, §9, p. 6):** the agreement must contain an enforceable repossession clause and provisions for the notice period; circumstances for waiving it; taking possession of security; a final repayment opportunity before sale/auction; giving repossession back to the borrower; and the sale/auction procedure. The terms must be made available to the borrower.

Current facets are F1 enforceable clause; F2 notice period; F6 waiver circumstances; F3 taking-possession procedure; F4 final repayment opportunity; F5 return-possession procedure; F7 sale/auction procedure. The current F5 paraphrase (“returning possession”) is consistent with the source's “giving repossession to the borrower.”

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 / F4 / F5 / F6 / F7 |
|---:|---|---|---|---|
| 1 | `doc_001_fixed_size_00010_11f6c82db1cd` | doc_001, 9–10 | Yes | — / — / — / — / — / — / — (Bajaj Finance, not Shriram) |
| 2 | `doc_016_fixed_size_00007_c0b5bc32280d` | doc_016, 6–7 | Yes | — / — / — / — / — / — / — |
| 3 | `doc_016_fixed_size_00001_3e76161d41b6` | doc_016, 1–1 | Yes | — / — / — / — / — / — / — |
| 4 | `doc_016_fixed_size_00006_5707a2baee10` | doc_016, 5–6 | Yes | D / D / D / D / D / D / D |
| 5 | `doc_005_fixed_size_00019_e86e69631328` | doc_005, 9–10 | Yes | — / — / — / — / — / — / — |
| 6 | `doc_029_fixed_size_00018_0ece33c1d636` | doc_029, 9–9 | Yes | — / — / — / — / — / — / — |
| 7 | `doc_002_fixed_size_00003_70491da42bd6` | doc_002, 3–4 | Yes | — / — / — / — / — / — / — (Tata Cleantech Capital, not Shriram) |
| 8 | `doc_016_fixed_size_00004_d348f0bac727` | doc_016, 3–4 | Yes | — / — / — / — / — / — / — |
| 9 | `doc_016_fixed_size_00005_92e15d19bd51` | doc_016, 4–5 | Yes | — / — / — / — / — / — / — |
| 10 | `doc_005_fixed_size_00020_2fbf4bf313a5` | doc_005, 10–10 | Yes | — / — / — / — / — / — / — |

Rank 4 contains the complete Shriram §9 list, including all six required agreement provisions and the enforceability clause. Rank 1 contains a similar provision for Bajaj Finance, and rank 7 a similar provision for Tata Cleantech Capital; neither is evidence about Shriram. Other same-source ranks concern different sections (including general recovery conduct, consumer education, or gold collateral), not these vehicle-repossession requirements.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 / F4 / F5 / F6 / F7 |
|---:|---|---|---|---|
| 1 | `doc_001_structure_aware_00010_a2e7e73908b4` | doc_001, 9–9 | Yes | — / — / — / — / — / — / — (Bajaj Finance, not Shriram) |
| 2 | `doc_016_structure_aware_00007_3562949c7e7a` | doc_016, 6–6 | Yes | D / D / D / D / D / D / D |
| 3 | `doc_005_structure_aware_00020_78b838c09623` | doc_005, 9–10 | Yes | — / — / — / — / — / — / — |
| 4 | `doc_027_structure_aware_00016_4763177f33cd` | doc_027, 10–11 | Yes | — / — / — / — / — / — / — |
| 5 | `doc_029_structure_aware_00019_d6821ff704fc` | doc_029, 9–10 | Yes | — / — / — / — / — / — / — |
| 6 | `doc_002_structure_aware_00003_b5b2ec7e1909` | doc_002, 3–4 | Yes | — / — / — / — / — / — / — (Tata Cleantech Capital, not Shriram) |
| 7 | `doc_016_structure_aware_00001_465ed38df1ef` | doc_016, 1–1 | Yes | — / — / — / — / — / — / — |
| 8 | `doc_002_structure_aware_00004_2af833660832` | doc_002, 4–5 | Yes | — / — / — / — / — / — / — (Tata Cleantech Capital, not Shriram) |
| 9 | `doc_001_structure_aware_00011_6d21474d762a` | doc_001, 10–10 | Yes | — / — / — / — / — / — / — (Bajaj Finance, not Shriram) |
| 10 | `doc_001_structure_aware_00008_bd57eceffcf3` | doc_001, 7–8 | Yes | — / — / — / — / — / — / — (Bajaj Finance, not Shriram) |

Rank 2 is the complete Shriram §9 passage and directly supports all seven facets. Parallel clauses in other companies' documents are not credited.

### Facet matrix and assessment

| Facet | Fixed-size direct ranks | Fixed-size partial ranks | Structure-aware direct ranks | Structure-aware partial ranks |
|---|---:|---:|---:|---:|
| F1 | 4 | — | 2 | — |
| F2 | 4 | — | 2 | — |
| F6 | 4 | — | 2 | — |
| F3 | 4 | — | 2 | — |
| F4 | 4 | — | 2 | — |
| F5 | 4 | — | 2 | — |
| F7 | 4 | — | 2 | — |

Every facet has direct top-10 support for each strategy. Both existing `complete` proposals appear supported. The top-10 hit for each strategy is one chunk containing the full list; this is one retrieved chunk supporting multiple facets, not seven independent retrieval events.

**Assistant-prepared recommendation (not a human decision):** both proposed completeness labels appear supported by the saved top-10 evidence.

**Human decision fields — leave blank**

- Fixed-size top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Human rationale: `____________________________________________________________`

## Q013 — KFS provision and explanation before microfinance loan execution

**Source passage (doc_024, §1(b), p. 2):** Tata Capital must give all prospective borrowers a standardized Key Facts Statement before execution so they can take an informed view; write it in a language they understand; explain its contents; and obtain an acknowledgement that the borrower has understood it.

Current facets:

- **F1:** Provide a standardized Key Facts Statement to all prospective borrowers before contract execution.
- **F2:** Write the KFS in a language understood by the borrower.
- **F3:** Explain the contents of the KFS and obtain borrower acknowledgement.

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 |
|---:|---|---|---|---|
| 1 | `doc_024_fixed_size_00002_15bb2fdc5f67` | doc_024, 1–2 | Yes | D / D / D |
| 2 | `doc_002_fixed_size_00002_e8bfbf070883` | doc_002, 2–3 | Yes | — / — / — (Tata Cleantech Capital) |
| 3 | `doc_024_fixed_size_00004_e6145695ee32` | doc_024, 3–4 | Yes | — / — / — |
| 4 | `doc_024_fixed_size_00005_23b340ab4a76` | doc_024, 3–4 | Yes | — / — / — |
| 5 | `doc_003_fixed_size_00023_a8eb1773a020` | doc_003, 18–19 | Yes | — / — / — (Tata Capital Housing Finance) |
| 6 | `doc_003_fixed_size_00006_8bf99111838c` | doc_003, 4–5 | Yes | — / — / — (Tata Capital Housing Finance) |
| 7 | `doc_003_fixed_size_00022_472ad6c21cae` | doc_003, 17–18 | Yes | — / — / — (Tata Capital Housing Finance) |
| 8 | `doc_003_fixed_size_00005_96b0d302eff6` | doc_003, 4–5 | Yes | — / — / — (Tata Capital Housing Finance) |
| 9 | `doc_024_fixed_size_00003_cb861a2996e0` | doc_024, 2–3 | Yes | P / — / — |
| 10 | `doc_003_fixed_size_00002_8432983a1d35` | doc_003, 1–2 | Yes | — / — / — (Tata Capital Housing Finance) |

Rank 1 contains the full §1(b) sentence, including the acknowledgment that the borrower has understood the KFS. Rank 9 contains other KFS-related provisions (APR, charges, and the KFS summary box) but not the complete requirement to provide a standardized KFS to all prospective borrowers before execution; it is partial context for F1 only. Other chunks for Tata Capital's microfinance code concern other sections. The Tata Capital Housing Finance chunks are a different entity and are not credited to Tata Capital Limited.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 |
|---:|---|---|---|---|
| 1 | `doc_024_structure_aware_00002_c7c2c87cf73a` | doc_024, 1–2 | Yes | D / D / D |
| 2 | `doc_024_structure_aware_00005_ad192a5e6e82` | doc_024, 4–4 | Yes | — / — / — |
| 3 | `doc_002_structure_aware_00002_6fcde47d0801` | doc_002, 2–3 | Yes | — / — / — (Tata Cleantech Capital) |
| 4 | `doc_003_structure_aware_00006_f9c845e0a416` | doc_003, 4–5 | Yes | — / — / — (Tata Capital Housing Finance) |
| 5 | `doc_003_structure_aware_00005_a9d262541873` | doc_003, 3–4 | Yes | — / — / — (Tata Capital Housing Finance) |
| 6 | `doc_024_structure_aware_00003_c9a35a031d1e` | doc_024, 2–3 | Yes | P / — / — |
| 7 | `doc_003_structure_aware_00026_37c96e1037b3` | doc_003, 19–19 | Yes | — / — / — (Tata Capital Housing Finance) |
| 8 | `doc_024_structure_aware_00004_ea79c085f5a8` | doc_024, 3–4 | Yes | — / — / — |
| 9 | `doc_003_structure_aware_00002_964c980ead5b` | doc_003, 1–2 | Yes | — / — / — (Tata Capital Housing Finance) |
| 10 | `doc_003_structure_aware_00013_b5e4b30d14fb` | doc_003, 10–11 | Yes | — / — / — (Tata Capital Housing Finance) |

Rank 1 directly supports all three facets with the same full §1(b) sentence. Rank 6 contains additional KFS information but not the full standardized-provision/timing obligation; partial F1 only. The other doc_024 results address recovery procedures. Similar KFS text in doc_003 is not evidence for the gold-source entity.

### Facet matrix and assessment

| Facet | Fixed-size direct ranks | Fixed-size partial ranks | Structure-aware direct ranks | Structure-aware partial ranks |
|---|---:|---:|---:|---:|
| F1 | 1 | 9 | 1 | 6 |
| F2 | 1 | — | 1 | — |
| F3 | 1 | — | 1 | — |

Each strategy has direct support for all currently worded facets within its top 10, so each `complete` proposal appears supported by the saved evidence. There is a source-fidelity caveat: the source requires an acknowledgement **that the borrower has understood** the KFS, whereas F3 only says “obtain borrower acknowledgement.” Rank 1 includes the stronger source language, so retrieval coverage is present, but F3 may understate the requirement. Human review may wish to clarify the facet before treating the annotation wording as final. This caveat does not establish a retrieval miss.

**Assistant-prepared recommendation (not a human decision):** the saved top-10 evidence supports both completeness proposals as currently written. Separately, consider revising F3 to retain the source's “acknowledgement that [the borrower] has understood” qualification before finalizing the facet.

**Human decision fields — leave blank**

- Fixed-size top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Human rationale: `____________________________________________________________`

## Q014 — Normal microfinance repayment collection location and home/work exception

**Source passage (doc_024, §2(b), p. 3):** recovery is normally at a designated/central place mutually decided by borrower and company; field staff may collect at the borrower's residence or work only if the borrower fails to appear at that place on two or more successive occasions.

Current facets:

- **F1:** Ordinarily, collect at a designated/central place mutually decided by borrower and company.
- **F2:** Field staff may collect at the borrower's residence/work only if the borrower fails to appear at the designated place on two or more successive occasions.

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 |
|---:|---|---|---|---|
| 1 | `doc_003_fixed_size_00014_2a0777b91086` | doc_003, 11–12 | Yes | — / — (Tata Capital Housing Finance) |
| 2 | `doc_024_fixed_size_00005_23b340ab4a76` | doc_024, 3–4 | Yes | — / — |
| 3 | `doc_001_fixed_size_00012_9e002cf96917` | doc_001, 10–11 | Yes | — / — (Bajaj Finance, not Tata Capital) |
| 4 | `doc_024_fixed_size_00003_cb861a2996e0` | doc_024, 2–3 | Yes | — / — |
| 5 | `doc_024_fixed_size_00004_e6145695ee32` | doc_024, 3–4 | Yes | D / D |
| 6 | `doc_003_fixed_size_00017_7d8573c40a2a` | doc_003, 13–14 | Yes | — / — (Tata Capital Housing Finance) |
| 7 | `doc_003_fixed_size_00016_71fb70c84b58` | doc_003, 12–13 | Yes | — / — (Tata Capital Housing Finance) |
| 8 | `doc_003_fixed_size_00006_8bf99111838c` | doc_003, 4–5 | Yes | — / — (Tata Capital Housing Finance) |
| 9 | `doc_003_fixed_size_00007_2c72584c85de` | doc_003, 5–6 | Yes | — / — (Tata Capital Housing Finance) |
| 10 | `doc_016_fixed_size_00007_c0b5bc32280d` | doc_016, 6–7 | Yes | — / — (Shriram Finance) |

Rank 5 contains the complete §2(b) location and exception text. The rank 3 Bajaj chunk contains a parallel microfinance rule, but it belongs to a different company. The other retrieved material concerns different issuers or different sections, including recovery-agent procedures, loan terms, and vehicle repossession.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 |
|---:|---|---|---|---|
| 1 | `doc_024_structure_aware_00003_c9a35a031d1e` | doc_024, 2–3 | Yes | — / — |
| 2 | `doc_024_structure_aware_00004_ea79c085f5a8` | doc_024, 3–4 | Yes | D / D |
| 3 | `doc_003_structure_aware_00014_2fe74991cb26` | doc_003, 11–11 | Yes | — / — (Tata Capital Housing Finance) |
| 4 | `doc_024_structure_aware_00005_ad192a5e6e82` | doc_024, 4–4 | Yes | — / — |
| 5 | `doc_003_structure_aware_00017_21db74ec5324` | doc_003, 13–13 | Yes | — / — (Tata Capital Housing Finance) |
| 6 | `doc_003_structure_aware_00006_f9c845e0a416` | doc_003, 4–5 | Yes | — / — (Tata Capital Housing Finance) |
| 7 | `doc_001_structure_aware_00008_bd57eceffcf3` | doc_001, 7–8 | Yes | — / — (Bajaj Finance, not Tata Capital) |
| 8 | `doc_001_structure_aware_00005_33a0e3812a93` | doc_001, 5–6 | Yes | — / — (Bajaj Finance, not Tata Capital) |
| 9 | `doc_017_structure_aware_00003_d48a51798b10` | doc_017, 2–2 | Yes | — / — (Aditya Birla Capital) |
| 10 | `doc_016_structure_aware_00008_8909da55ae52` | doc_016, 6–8 | Yes | — / — (Shriram Finance) |

Rank 2 directly contains both conditions. Rank 1 concerns APR and charges, not the recovery-location provision. Other results do not establish the target-source requirements.

### Facet matrix and assessment

| Facet | Fixed-size direct ranks | Fixed-size partial ranks | Structure-aware direct ranks | Structure-aware partial ranks |
|---|---:|---:|---:|---:|
| F1 | 5 | — | 2 | — |
| F2 | 5 | — | 2 | — |

Both facets have direct support within each top 10; both `complete` proposals appear supported. The qualifying condition is expressly “two or more successive occasions”; no retrieved top-10 evidence was needed from outside the target-source rank.

**Assistant-prepared recommendation (not a human decision):** both proposed completeness labels appear supported by the saved top-10 evidence.

**Human decision fields — leave blank**

- Fixed-size top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Human rationale: `____________________________________________________________`

## Q015 — Customer protections that are objectives of Tata Capital's grievance policy

**Source passage (doc_023, §2, p. 2):** the policy objectives are fair and unbiased treatment; courteous handling and timely resolution; and making customers aware of their rights so they can choose alternative remedies if dissatisfied with the response or resolution. The passage also says the policy applies to Tata Capital Limited customers and recognized interaction channels, excluding sub-judice matters.

Current facets:

- **F1:** Treat all customers fairly and without bias.
- **F2:** Address customer issues courteously and resolve them on time.
- **F3:** Make customers aware of their rights and alternative remedies if dissatisfied with the response/resolution.

### Fixed-size top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 |
|---:|---|---|---|---|
| 1 | `doc_023_fixed_size_00002_1f9f6e67ac59` | doc_023, 1–3 | Yes | D / D / D |
| 2 | `doc_025_fixed_size_00001_e018569bca2f` | doc_025, 1–3 | Yes | — / — / — (Tata Capital Financial Services, not Tata Capital Limited) |
| 3 | `doc_002_fixed_size_00005_65b6f505bfff` | doc_002, 5–6 | Yes | — / — / — (Tata Cleantech Capital) |
| 4 | `doc_003_fixed_size_00017_7d8573c40a2a` | doc_003, 13–14 | Yes | — / — / — (Tata Capital Housing Finance) |
| 5 | `doc_003_fixed_size_00002_8432983a1d35` | doc_003, 1–2 | Yes | — / — / — (Tata Capital Housing Finance) |
| 6 | `doc_025_fixed_size_00003_4bcee1588fcb` | doc_025, 3–4 | Yes | — / — / — (Tata Capital Financial Services) |
| 7 | `doc_023_fixed_size_00004_efc9aaef0071` | doc_023, 3–4 | Yes | — / — / — |
| 8 | `doc_003_fixed_size_00018_38b10f520093` | doc_003, 14–15 | Yes | — / — / — (Tata Capital Housing Finance) |
| 9 | `doc_024_fixed_size_00005_23b340ab4a76` | doc_024, 3–4 | Yes | — / — / — |
| 10 | `doc_026_fixed_size_00003_82ab712771fc` | doc_026, 3–5 | Yes | — / — / — |

Rank 1 directly reproduces the objectives and their dissatisfaction qualifier. Rank 7 describes customer-service registration channels and an escalation matrix for cases not closed within a turnaround time; it does not state the §2 objective of customer rights and alternative remedies. Rank 2 contains similar objective wording in a related but distinct Tata Capital Financial Services policy; it is not evidence for the doc_023 gold-source policy. The remaining results concern other issuers or other policy topics.

### Structure-aware top-10 inventory

| Rank | Chunk ID | Document / pages | Text available | F1 / F2 / F3 |
|---:|---|---|---|---|
| 1 | `doc_023_structure_aware_00002_8dc9d4739e5b` | doc_023, 1–2 | Yes | D / D / D |
| 2 | `doc_025_structure_aware_00001_944a00c98862` | doc_025, 1–2 | Yes | — / — / — (Tata Capital Financial Services, not Tata Capital Limited) |
| 3 | `doc_023_structure_aware_00003_476aa6f90b33` | doc_023, 3–3 | Yes | — / — / — |
| 4 | `doc_024_structure_aware_00005_ad192a5e6e82` | doc_024, 4–4 | Yes | — / — / — |
| 5 | `doc_003_structure_aware_00018_03fb79a24da9` | doc_003, 13–14 | Yes | — / — / — (Tata Capital Housing Finance) |
| 6 | `doc_003_structure_aware_00002_964c980ead5b` | doc_003, 1–2 | Yes | — / — / — (Tata Capital Housing Finance) |
| 7 | `doc_025_structure_aware_00002_c53de051cfa9` | doc_025, 3–3 | Yes | — / — / — (Tata Capital Financial Services) |
| 8 | `doc_002_structure_aware_00005_09f53cf3d4e9` | doc_002, 5–5 | Yes | — / — / — (Tata Cleantech Capital) |
| 9 | `doc_003_structure_aware_00017_21db74ec5324` | doc_003, 13–13 | Yes | — / — / — (Tata Capital Housing Finance) |
| 10 | `doc_003_structure_aware_00019_001eaf2525e2` | doc_003, 14–15 | Yes | — / — / — (Tata Capital Housing Finance) |

Rank 1 directly contains all three objectives. Rank 3 discusses complaint categories, registration channels, and escalation of overdue cases, not the customer-protection objectives in §2. The similar doc_025 policy is for Tata Capital Financial Services Limited and is not substituted for the Tata Capital Limited gold source.

### Facet matrix and assessment

| Facet | Fixed-size direct ranks | Fixed-size partial ranks | Structure-aware direct ranks | Structure-aware partial ranks |
|---|---:|---:|---:|---:|
| F1 | 1 | — | 1 | — |
| F2 | 1 | — | 1 | — |
| F3 | 1 | — | 1 | — |

Each strategy has direct support for all three facets in the target policy at rank 1. Both proposed `complete` labels appear supported. Although the rank-1 chunk spans pages 1–3, the relevant policy-objectives text is on page 2. No outside-top-10 diagnostic result is counted.

**Assistant-prepared recommendation (not a human decision):** both proposed completeness labels appear supported by the saved top-10 evidence.

**Human decision fields — leave blank**

- Fixed-size top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Structure-aware top-10: `________________` (`APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`)
- Human rationale: `____________________________________________________________`

## Cross-question review and decision boundaries

- **Q011:** all current facets have direct coverage in each strategy. F2 groups two independently assessable review subjects; the saved full source sentence and the direct ranks support both.
- **Q012:** the seven previously revised safeguards remain independently represented; each strategy's cited chunk directly contains all seven. This report does not revisit the previously approved facet revision.
- **Q013:** all currently worded facets are directly covered. F3 omits the source's requirement that the acknowledgement confirm borrower understanding; treat that as a facet-fidelity question distinct from top-10 support.
- **Q014:** both the normal collection location and the two-successive-failure exception have direct support in each strategy.
- **Q015:** all three source objectives are directly present in each strategy's rank 1. Similar statements in doc_025 are not credited because that document identifies a different legal entity.

Completeness here means coverage of all current annotation facets within the saved strategy top 10. Partial evidence is not full facet coverage. One chunk may support multiple facets, but this is not multiple independent retrieval events. A `REJECT_AS_PROPOSED` human choice would reject the proposed `complete` label for that strategy; it would not, by itself, change data or specify a replacement label.

## Human decision sheet

No human adjudication has yet occurred for Q011–Q015. The fields below are intentionally unfilled. Assistant-prepared recommendations elsewhere in this report are not human decisions.

| Question | Fixed-size top-10 decision | Structure-aware top-10 decision |
|---|---|---|
| Q011 | `________________` | `________________` |
| Q012 | `________________` | `________________` |
| Q013 | `________________` | `________________` |
| Q014 | `________________` | `________________` |
| Q015 | `________________` | `________________` |

For each strategy, select one: `APPROVE_AS_PROPOSED` / `REJECT_AS_PROPOSED` / `HOLD_FOR_CLARIFICATION`.

Human rationale / requested facet clarification:

`____________________________________________________________________________`

`____________________________________________________________________________`

## Validation and limitations

1. **Both complete top-10 result lists inspected:** PASS — 10 question/strategy lists, 10 ranks each.
2. **Every listed chunk resolved and inspected against saved evidence where available:** PASS — 100/100 chunk objects found; actual text was available for all and reviewed for target facets and relevant borderline cases.
3. **CSV/JSON agreement:** PASS — all 100 rank/chunk/document/page entries match.
4. **Support judgments grounded in actual source and chunk text:** PASS.
5. **No outside-top-10 diagnostic counted:** PASS.
6. **V3 consistency:** PASS — Q011–Q015 have the facets and coverage arrays recorded in the source-of-truth JSONL; each proposed completeness status is `complete`; the support-chunk IDs/ranks listed in v3 resolve to the direct chunks described above. Reviewer/adjudication states are exactly those recorded in the source-state table.
7. **No project data or code modified:** PASS.
8. **Only the authorized new report created by this task:** PASS — comparison with the pre-write Git status shows this report is the only additional project path.
9. **No human decision recorded:** PASS — decision fields are blank.

Limitations and items for human consideration:

- This review assesses retrieval evidence against the current facets; it does not decide whether the facets are the correct final ground truth.
- Q011 F2 may be split for independent facet assessment if a human prefers; no change is applied.
- Q013 F3 should be considered for clarification to preserve the source's “acknowledgement that the borrower has understood” qualification.
- Results from related entities and other issuers were not substituted for the gold-source documents.
- No retrieval was rerun, and no new result was reconstructed.

## Read-only boundary

No completeness label, `covered_facets`, `supported_facet_ids`, reviewer status, or adjudication status was changed. No Q011–Q015 human decision is recorded. No other question was adjudicated, no ground-truth approval is asserted, and Batch 3 has not started.

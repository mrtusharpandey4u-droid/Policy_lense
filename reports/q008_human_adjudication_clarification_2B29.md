# Q008 Human Adjudication Clarification — Milestone 2B.29

## Purpose and scope

This report examines whether Q008's F2 should remain one combined facet or be represented as two independently assessable requirements. It is an assistant-prepared, source-grounded decision aid, not a human adjudication. Q008 is neither approved nor rejected here; no annotation, completeness label, or adjudication status is changed.

## Question and current proposal

**Q008:** “What cost information must Tata Capital Housing Finance disclose so a borrower can compare loan offers?”

The v3 record identifies `doc_003`, PDF page 4, and has two proposed facets:

| Facet | Current proposed requirement |
|---|---|
| F1 | Disclose the all-in cost, inclusive of charges involved in processing or sanction of the loan. |
| F2 | Disclose costs transparently and ensure charges/fees are non-discriminatory. |

The record's reviewer status is `pending_user_adjudication`. Its fixed-size and structure-aware top-10 completeness values are both `complete`, as proposal values only.

## Source examined

The original PDF is [`data/pdfs/tchfl_fair_practices_code.pdf`](../data/pdfs/tchfl_fair_practices_code.pdf), identified as `doc_003` in [`data/manifest.csv`](../data/manifest.csv). Its SHA-256 matches the manifest hash. I inspected the original PDF's printed page 4 (zero-based PDF page index 3), section 5.1(b), rather than relying only on the adjudication packet.

The source paragraph first requires transparent disclosure of interest rates, fees and charges, and other listed information affecting the borrower so offers can be compared. Its concluding sentences state that the all-in processing/sanction cost is to be disclosed “in a transparent manner” and that “such charges/fees are non-discriminatory.”

### Source interpretation

Transparency and non-discrimination are separately expressed and have independently identifiable meanings:

- **Transparency** concerns whether relevant price and fee information—including the all-in processing/sanction cost—is disclosed clearly enough for comparison and an informed decision.
- **Non-discrimination** concerns whether the charges and fees themselves are applied without discrimination.

The requirements can be independently met or missed: transparent disclosure does not itself establish non-discriminatory charges, and non-discriminatory charges do not establish that the borrower received transparent disclosure. The source also states the non-discrimination duty as a separate sentence (“It shall also be ensured”), rather than making it a qualification of transparency.

The current F2 is substantively faithful to the two closing obligations, but compresses them into one conjunctive facet. Its phrase “Disclose costs transparently” is also narrower than the paragraph's earlier transparency requirement, which extends to the listed interest-rate, fee/charge, and other borrower-interest information. F1 already identifies the all-in processing/sanction-cost content; a human-approved revision should make the scope of any transparency facet clear and avoid confusing disclosure manner with cost content.

## Saved top-10 evidence examined

I inspected both complete saved Q008 top-10 result lists in [`data/evaluation/results/retrieval_evaluation_question_results.csv`](../data/evaluation/results/retrieval_evaluation_question_results.csv), cross-checking the saved result records in [`data/evaluation/results/retrieval_evaluation_results.json`](../data/evaluation/results/retrieval_evaluation_results.json). The result records contain rank, document, page, score, and relevance metadata; I matched every listed chunk ID to its already-saved text in [`data/processed/chunks/fixed_size.jsonl`](../data/processed/chunks/fixed_size.jsonl) or [`data/processed/chunks/structure_aware.jsonl`](../data/processed/chunks/structure_aware.jsonl). No retrieval or other processing was run.

| Strategy | Rank | Saved result document/pages | Result marked relevant |
|---|---:|---|---|
| Fixed-size | 1 | doc_003, pp. 4–5 | Yes |
| Fixed-size | 2 | doc_003, pp. 18–19 | No |
| Fixed-size | 3 | doc_003, pp. 4–5 | Yes |
| Fixed-size | 4 | doc_003, pp. 9–10 | No |
| Fixed-size | 5 | doc_003, pp. 2–3 | No |
| Fixed-size | 6 | doc_002, pp. 2–3 | No |
| Fixed-size | 7 | doc_024, pp. 2–3 | No |
| Fixed-size | 8 | doc_003, pp. 17–18 | No |
| Fixed-size | 9 | doc_003, pp. 5–6 | No |
| Fixed-size | 10 | doc_024, pp. 1–2 | No |
| Structure-aware | 1 | doc_003, pp. 2–3 | No |
| Structure-aware | 2 | doc_003, pp. 3–4 | Yes |
| Structure-aware | 3 | doc_024, pp. 2–3 | No |
| Structure-aware | 4 | doc_003, pp. 10–11 | No |
| Structure-aware | 5 | doc_002, pp. 2–3 | No |
| Structure-aware | 6 | doc_003, pp. 9–10 | No |
| Structure-aware | 7 | doc_003, pp. 4–5 | Yes |
| Structure-aware | 8 | doc_024, p. 4 | No |
| Structure-aware | 9 | doc_024, pp. 1–2 | No |
| Structure-aware | 10 | doc_003, p. 19 | No |

The saved fixed-size rank-1 chunk (`doc_003_fixed_size_00005_96b0d302eff6`) contains the relevant section 5.1(b) text, including both the transparent all-in-cost disclosure and the separate non-discrimination sentence. The saved structure-aware rank-2 chunk (`doc_003_structure_aware_00005_a9d262541873`) contains the same source passage and both requirements. These are the direct source-page payloads cited for Q008 in the v3 proposal. Other top-10 payloads do not supply a separate top-10 case where one of these two specific requirements is present and the other absent.

Therefore, the two requirements are independently assessable in meaning, but this query's saved top-10 payloads co-locate both in the relevant source chunks. The saved runs demonstrate support for both together; they do not demonstrate different retrieval outcomes for transparency versus non-discrimination. The retrieval result's `relevant` flag is not, by itself, a facet-level adjudication.

## Decision aid

### Option A — Keep F2 as one combined facet

- **Source fidelity:** Retains both source obligations in a concise representation of the same paragraph, but combines two distinct duties.
- **Assessment clarity:** A reviewer must decide how to score a mixed case where disclosure is transparent but charges are discriminatory, or vice versa. A single covered/not-covered facet can hide which duty is unsupported.
- **Potential impact on completeness:** The combined facet is covered only when evidence supports both parts; evidence for just one may leave the entire facet uncovered, obscuring partial coverage. The denominator remains at two facets, preserving the current granularity.
- **Advantages:** Minimal revision; aligns with the fact that both clauses occur together in the same paragraph and chunk.
- **Disadvantages:** Weakens diagnosis and independent measurement; a missed requirement cannot be isolated cleanly.

### Option B — Split F2 into two independently assessable facets

- **Source fidelity:** Better reflects the source's separate transparency and non-discrimination statements. The transparency facet should clearly identify what information must be disclosed; the source includes the broader listed price information as well as the all-in cost.
- **Assessment clarity:** Allows a reviewer to record transparent disclosure and non-discriminatory charges separately, including partial support or a miss for either one.
- **Potential impact on completeness:** The facet denominator would rise from two to three, so any facet-count-based completeness score or weighting could change. Based on the existing saved rank-1 fixed-size and rank-2 structure-aware chunks, both proposed split requirements have direct source text within each top-10 result, so a split alone does not indicate that either current `complete` proposal should change. The facets and labels would nevertheless need explicit human approval and any subsequent scoring should follow the approved definitions.
- **Advantages:** Separates independent obligations; makes completeness decisions more diagnostic and reproducible.
- **Disadvantages:** Requires a human-approved annotation revision and careful scoping of the transparency facet alongside F1; changes the facet denominator and may affect comparisons with annotations that retain combined facets.

## Assistant / technical recommendation — requires explicit human approval

**Recommend Option B: split F2 into two independently assessable facets.** The source states distinct obligations that can be independently satisfied or violated, and splitting avoids hiding partial evidence. This is a technical recommendation only; it does not revise Q008, alter either proposed `complete` label, or decide Q008's adjudication.

## Validation and boundaries

- Q008 remains `pending_user_adjudication`.
- The existing F1/F2 definitions and both `complete` values remain proposal values and are unchanged.
- No Q001–Q010 annotation or adjudication decision was changed.
- No prior adjudication report or other existing file was changed.
- This milestone creates only this clarification report. No retrieval, embeddings, indexing, evaluation, or metrics were rerun, and Batch 3 is not begun.

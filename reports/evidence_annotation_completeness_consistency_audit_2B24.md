# PolicyLens — Evidence Annotation Completeness and Consistency Audit (Milestone 2B.24)

## 1. Executive verdict

**NOT_VERIFIED**

The v2 proposal is structurally valid and its Q020, Q021, and Q025 revisions
match the specified human criteria. However, a material top-10 completeness
error remains in Q001: both rank-1 chunks contain the exact complaint-forwarding
commitment on the gold source page, while v2 marks both strategies incomplete
and cites no supporting chunk. The same false-negative assessment appears in
the 2B.21 reconciliation and evidence-level audit CSV; the 2B.23 verification
did not detect it. Q005 also includes question-context conditions as required
answer facets, and a few other facet boundaries need human adjudication.

This verdict is about the proposal's auditability and internal accuracy. It
does not approve or reject annotations as ground truth. All 25 records remain
`pending_user_adjudication`.

## 2. Files and evidence inspected

### Annotation, question, and report artifacts

- [Version-2 annotation JSONL](../data/evaluation/evidence_annotations_v2.jsonl)
- [Version-1 annotation JSONL](../data/evaluation/evidence_annotations_v1.jsonl)
- [Original evaluation questions](../data/evaluation/evaluation_questions.jsonl)
- [Version-2 annotation report](evidence_annotation_report_v2.md)
- [Version-2 decision sheet](evidence_annotation_decision_sheet_v2.md)
- [2B.22 revision report](evidence_annotation_revision_2B22.md)
- [2B.23 independent verification report](evidence_annotation_revision_verification_2B23.md)
- [2B.21 reconciliation report](final_evidence_audit_reconciliation.md)
- [Evidence-level relevance audit report](evidence_level_relevance_audit.md)

### Saved retrieval, audit, and chunk data

- [Evidence-level audit CSV](../data/evaluation/results/evidence_level_relevance_audit.csv)
- [Saved retrieval evaluation results](../data/evaluation/results/retrieval_evaluation_results.json)
- [Saved retrieval question-results CSV](../data/evaluation/results/retrieval_evaluation_question_results.csv)
- [Saved top-20 diagnostic](../data/evaluation/results/retrieval_failure_top20_diagnostic.json)
- [Fixed-size chunks](../data/processed/chunks/fixed_size.jsonl)
- [Structure-aware chunks](../data/processed/chunks/structure_aware.jsonl)

### Original source PDFs

- [Bajaj Finance Fair Practice Code](../data/pdfs/bfl_fair_practice_code.pdf) — doc_001
- [Tata Capital Housing Finance Fair Practices Code](../data/pdfs/tchfl_fair_practices_code.pdf) — doc_003
- [Shriram Finance Fair Practice Code 2023](../data/pdfs/doc_016_fair_practice_code_2023.pdf) — doc_016
- [Tata Capital interest-rate policy](../data/pdfs/doc_019_policy_for_determining_interest_rat.pdf) — doc_019
- [Tata Capital customer-service SOP](../data/pdfs/doc_023_merged_customer_service_and_grievan.pdf) — doc_023
- [Tata Capital microfinance code](../data/pdfs/doc_024_fair_practices_code_for_microfinanc.pdf) — doc_024
- [DFS RuPay and BHIM-UPI guidelines](../data/pdfs/doc_034_guidelines_for_promotion_and_incent.pdf) — doc_034
- [RBI Annual Report 2023-24](../data/pdfs/doc_036_rbi_annual_report_2023_24.pdf) — doc_036

All mandatory files listed in the request were present and readable. The
separate Milestone 2B.18B quality review report was not found; the existing
2B.18 evidence-level audit report is not a substitute. No missing report or
historical baseline was reconstructed.

## 3. Methodology

- Parsed v1, v2, and the original question JSONL files; compared record IDs,
  wording, gold source/page references, schema keys, statuses, and the records
  that differ between versions.
- Compared each proposed facet and cited source excerpt with its original
  source PDF page. For table questions, inspected the stored structured table
  payload as well as the original page.
- Matched each cited top-10 chunk ID and rank to the existing retrieval JSON
  and chunk files. Separately inspected relevant uncited top-10 chunks where
  the annotation says incomplete, especially Q001.
- Used only saved retrieval results and the existing diagnostic. No retrieval,
  metric evaluation, OCR, extraction, indexing, or Qdrant operation was run.
- Compared report statements and counts with the records and saved results.
  Historical-preservation statements were treated as unverifiable where no
  reliable baseline is documented.

Finding labels mean:

- `VERIFIED`: the inspected evidence supports the claim.
- `ISSUE_FOUND`: a concrete error or unsupported annotation was identified.
- `NOT_VERIFIABLE`: evidence or a reliable baseline is unavailable.
- `NEEDS_HUMAN_JUDGMENT`: evidence is available, but a facet-scope decision is
  needed.

## 4. Record and schema integrity

| Check | Classification | Result |
|---|---|---|
| V2 record count and IDs | VERIFIED | 25 records, 25 unique IDs Q001–Q025. |
| Facet IDs | VERIFIED | 63 facets; IDs are unique within each question. |
| Question text and gold source/page mapping | VERIFIED | All 25 records match the original evaluation question and its gold document/page references. |
| V1-to-v2 preservation | VERIFIED | Only Q020, Q021, and Q025 differ; the other 22 records are semantically unchanged. |
| Schema | VERIFIED | V1 and v2 top-level field sets match; `schema_version` remains 1.0. No required field or type defect was found. Existing optional nested fields are used consistently with prior records. |
| Adjudication status | VERIFIED | All 25 records have `reviewer_status: pending_user_adjudication`; 22 have `proposed_requires_user_approval`, and Q020/Q021/Q025 have `needs_review`. No record is marked approved ground truth. |
| Cited chunk/rank references | VERIFIED, with Q001 exception below | Cited IDs and ranks resolve to the saved strategy result and corresponding chunk. The defect is that Q001's rank-1 evidence is not cited at all. |

The annotation report's recorded status totals (fixed-size 20 complete / 5
incomplete; structure-aware 21 complete / 4 incomplete) accurately count the
labels in the JSONL. They are not reliable completeness totals, however,
because Q001's two labels conflict with its retrieved chunk contents. No
replacement totals or performance metrics are issued here.

## 5. All-question reconciliation matrix

“Top 10” entries show the current v2 label unless explicitly marked as an
audit finding. The matrix evaluates source, facets, retrieval support, and
attribution for every question.

| ID | Facet quality | Fixed-size top 10 | Structure-aware top 10 | Source attribution | Finding classification |
|---|---|---|---|---|---|
| Q001 | One answer facet is appropriate. | v2: incomplete; **rank 1 directly supports F1**. | v2: incomplete; **rank 1 directly supports F1**. | Correct doc_001, PDF p.3, present in both rank-1 chunks. | ISSUE_FOUND |
| Q002 | Receipt and disposition timeframe are distinct, answer-relevant details. | Complete, r3. | Complete, r3. | VERIFIED; doc_001, p.4. | VERIFIED |
| Q003 | Single language requirement is appropriately scoped. | Complete, r7. | Complete, r4. | VERIFIED; doc_001, p.4. | VERIFIED |
| Q004 | Four facets capture the delivery method and the three requested loan details. | Complete, r4; rank-1 page overlap is not credited. | Complete, r7. | VERIFIED; doc_001, p.4. | VERIFIED |
| Q005 | F1/F2 repeat the late/default scenario already stated in the question; they should not automatically be required answer facets. F3/F4 describe bolding and location. | Incomplete; r5 is partial. | Incomplete; r6 is partial. | VERIFIED; partial chunks are doc_001, pp.4–5; out-of-top-10 direct evidence is from the same source. | ISSUE_FOUND |
| Q006 | Notice and prospective effect are distinct and relevant. | Complete, r3. | Complete, r4. | VERIFIED; doc_001, p.5. | VERIFIED |
| Q007 | Release trigger and lien qualification are both material to “when.” | Complete, r7. | Complete, r4. | VERIFIED; doc_001, p.5. | VERIFIED |
| Q008 | All-in cost and transparent/non-discriminatory charges are relevant disclosure details. | Complete, r1. | Complete, r2. | VERIFIED; doc_003, p.4. | VERIFIED |
| Q009 | F1 repeats the disadvantage trigger already supplied by the question; adjudicate whether it is context rather than a required answer facet. | Complete, r2. | Complete, r4. | VERIFIED; doc_003, p.5. | NEEDS_HUMAN_JUDGMENT |
| Q010 | Two facets represent the risk rationale and its publication locations. | Incomplete. | Incomplete. | VERIFIED; top-10 generic website text is insufficient; direct source evidence occurs at structure-aware diagnostic r18, outside top 10. | VERIFIED |
| Q011 | Three board duties are materially distinct and supported. | Complete, r5. | Complete, r8. | VERIFIED; doc_016, p.5. | VERIFIED |
| Q012 | F2 combines notice period and waiver circumstances; F5 combines return-of-possession and sale/auction procedures. Decide whether to track these independently. | Complete, r4. | Complete, r2. | VERIFIED; doc_016, p.6; cited payloads include the listed safeguards. | NEEDS_HUMAN_JUDGMENT |
| Q013 | KFS provision, language, explanation, and acknowledgement are covered; the final two are a linked but independently checkable pair. | Complete, r1. | Complete, r1. | VERIFIED; doc_024, p.2. | VERIFIED |
| Q014 | Normal collection location and the two-successive-failure exception are separately required. | Complete, r5. | Complete, r2. | VERIFIED; doc_024, p.3. | VERIFIED |
| Q015 | Fair treatment, timely courteous resolution, and alternative-remedy awareness are distinct objectives. | Complete, r1. | Complete, r1. | VERIFIED; doc_023, p.2. | VERIFIED |
| Q016 | One row-bound facet appropriately preserves row, current/revised values, and date. | Complete, r1. | Complete, r1. | VERIFIED; doc_019, p.2; table cells preserve the requested row relationship. | VERIFIED |
| Q017 | Row, category, rate, and cap preserve the table lookup relation. | Complete, r1. | Complete, r1; r3 is noted as repeated, not independent evidence. | VERIFIED; doc_034, p.1 primary table. Same-document p.6 repeated claim row does not inflate completeness. | VERIFIED |
| Q018 | Transaction threshold, category, and rate preserve the table lookup relation. | Complete, r1. | Complete, r1. | VERIFIED; doc_034, p.1. | VERIFIED |
| Q019 | Process row and maximum TAT are correctly tied together. | Complete, r3. | Complete, r3. | VERIFIED; doc_023, p.7; table heading states working days. | VERIFIED |
| Q020 | Two facets preserve the named table, row, year, and value criterion. | Incomplete, correctly. | Complete, r10, correctly. | VERIFIED; doc_036, p.41; r10's structured row/year/value aligns with the original Table II.2.1. | VERIFIED |
| Q021 | Three grounds are required; marketing is a qualification on the company-interest ground, not a fourth ground. | Complete, r2. | Complete, r1. | VERIFIED; doc_016, p.3. | VERIFIED |
| Q022 | Prohibited hours are a single, clear required answer. | Complete, r7. | Incomplete, correctly; top 10 has no hours statement. | VERIFIED; doc_024, p.3; no cross-issuer evidence used. | VERIFIED |
| Q023 | Final repayment opportunity is a single, clear safeguard. | Complete, r2. | Complete, r2. | VERIFIED; doc_016, p.6. | VERIFIED |
| Q024 | Consent and fee disclosure are distinct required details. | Complete, r1; r10 is explicitly a duplicate of r1. | Complete, r1. | VERIFIED; doc_024, p.3; duplicate evidence is not double-counted. | VERIFIED |
| Q025 | Five independent details are appropriately separated; scenario is not counted as a remedy facet. | Incomplete, r2 supports F1–F4 only. | Complete, r1 supports F1–F5. | VERIFIED; doc_001, p.6; the doc_003 top-10 result is a different issuer and is not credited. | VERIFIED |

## 6. Detailed findings

### Q001 — rank-1 direct evidence omitted (ISSUE_FOUND)

The v2 record says both strategies are incomplete, has no supporting chunks,
and states that no top-10 chunk was verified to contain the commitment. That
claim is contradicted by the saved rank-1 payloads:

- Fixed-size r1: `doc_001_fixed_size_00001_aee405d33739`, pages 1–4.
- Structure-aware r1: `doc_001_structure_aware_00001_ac782e3816d0`, pages 1–3.

Both chunks contain the source-page-3 text: “Telling customers' how to take
their complaint forward if they are still not satisfied.” The PDF page
provenance includes doc_001 p.3, and the text itself contains the commitment;
this is not merely page overlap. The original source is [doc_001, PDF p.3](../data/pdfs/bfl_fair_practice_code.pdf).

The finding is echoed in the v2 annotation report, which lists Q001 as
incomplete for both strategies. The 2B.21 matrix likewise says the rank-1
overlap does not contain the commitment. The evidence-level CSV labels each
rank-1 result `PARTIAL` and says a component is missing, although the chunk
contains the complete source sentence. The 2B.23 report then states that no
material content discrepancy was found; this independent verification missed
the same direct payload. These are historical records and remain unchanged.

**Recommended human action:** Re-adjudicate Q001 against both actual chunk
payloads and the source page. If the direct sentence is accepted as evidence,
the v2 citations and both completeness labels require correction. Do not
silently treat the labels as corrected in this report.

### Q005 — scenario conditions and partial facet semantics

The source on [doc_001, PDF p.4](../data/pdfs/bfl_fair_practice_code.pdf)
states that penal charges for late repayment or another customer default are
to be mentioned “in bold in the loan agreement.” The question asks where the
charges must be highlighted; its late/default wording supplies the scope of
the question. Current F1 and F2 make those scenario conditions independently
required facets, even though the question does not ask the reader to restate
them. Human review should decide whether they belong in context/notes rather
than the required answer set.

Fixed-size r5
(`doc_001_fixed_size_00004_785fedf70295`) and structure-aware r6
(`doc_001_structure_aware_00004_288632361e39`) are correctly marked
`PARTIAL` and neither top 10 is complete: the cited chunks contain related
penal-charge/loan-agreement disclosure but not the complete bold-and-location
instruction. The record's `covered_facets: ["F4"]` alongside a `PARTIAL` label
is potentially ambiguous: it must not be interpreted as full coverage of F4.
The top-20 diagnostic's fixed-size r19
(`doc_001_fixed_size_00003_0bf6f42069fa`) and structure-aware r17
(`doc_001_structure_aware_00003_ad7599361f91`) contain the direct instruction;
those ranks are outside top 10.

**Recommended human action:** Decide whether F1/F2 are answer facets or
context; clarify the meaning of `covered_facets` when a chunk is only partial.
The current top-10 incomplete labels remain supported independently of that
scope decision.

### Q009 — scenario condition facet (NEEDS_HUMAN_JUDGMENT)

F1 (“The option is triggered when a change is to the customer's
disadvantage”) repeats the condition already supplied by “If a change in loan
terms disadvantages the customer” in the question. The source on
[doc_003, PDF p.5](../data/pdfs/tchfl_fair_practices_code.pdf) supports it,
and both strategies' complete top-10 chunks support all proposed facets.
The issue is not source accuracy or completeness but whether the condition
should be required answer evidence rather than scenario context.

**Recommended human action:** Confirm whether F1 should remain required, or
whether the answer facets should focus on the close/switch option and its
conditions (time, notice, and charges).

### Q012 — grouped independent safeguards (NEEDS_HUMAN_JUDGMENT)

On [doc_016, PDF p.6](../data/pdfs/doc_016_fair_practice_code_2023.pdf), the
source separately enumerates the notice period and waiver circumstances, and
separately enumerates the procedure for returning possession and the
procedure for sale/auction. V2 combines each pair into F2 and F5. The
fixed-size r4 and structure-aware r2 payloads include the source safeguards,
so both completeness labels are supported. The grouping could nevertheless
hide a missing detail if later chunks support only one item in a pair.

**Recommended human action:** Decide whether the four separately enumerated
subrequirements should be independently assessable facets. No current
completeness correction is indicated.

## 7. Priority-case analysis

### Q004 — page overlap handled correctly in v2

Fixed-size r1 spans pages 1–4 but does not contain the sanction-terms passage
required by Q004. The relevant evidence is present at fixed-size r4
(`doc_001_fixed_size_00003_0bf6f42069fa`) and structure-aware r7
(`doc_001_structure_aware_00003_ad7599361f91`), and supports the four
proposed facets. The later-rank chunks, not page overlap alone, support the
complete labels. The false-positive overlap issue is handled correctly here;
it should not be confused with Q001, where the same fixed-size rank-1 chunk
actually contains the Q001 commitment.

### Q010 — generic website wording not sufficient

The top-10 results include website-related wording but do not establish the
specific risk-gradation approach and rationale for different borrower rates.
Both v2 top-10 labels are incomplete. Structure-aware diagnostic r18,
`doc_016_structure_aware_00003_6a9423992e87`, contains the relevant source
passage but is outside the top 10. The diagnostic rank is not credited toward
top-10 completeness. V2 is consistent with the source and saved ranks.

### Q017 — table cell associations and duplicate evidence

Fixed-size r1, `doc_034_fixed_size_00001_9402fb448062`, and structure-aware r1,
`doc_034_structure_aware_00001_edcae9ae118c`, preserve the RuPay row,
“Other than industry programmes” category, 0.40% rate, and ₹100 cap on
[doc_034, PDF p.1](../data/pdfs/doc_034_guidelines_for_promotion_and_incent.pdf).
Structure-aware r3, `doc_034_structure_aware_00008_449aab87e17b`, is a
same-document repeated claim-submission table row on p.6 with the same facts.
V2 notes that it is not a second evidence unit. Rank 1 alone supports
completeness; the additional row does not inflate the result.

### Q020 — Table II.2.1 row/year/value

The original [RBI Annual Report, PDF p.41](../data/pdfs/doc_036_rbi_annual_report_2023_24.pdf)
identifies Table II.2.1 as “Real GDP Growth.” Structure-aware r10,
`doc_036_structure_aware_00080_da6891873a1b`, has a structured table payload
with the 2023-24 column and the Gross Fixed Capital Formation row ending in
10.2. Although the caption is not repeated in the chunk text, its p.41
provenance ties the row payload to the source page where Table II.2.1 is
identified; the row/year/value relationship is preserved. Structure-aware
top 10 is complete. Structure-aware r5 is narrative and is not credited as
table evidence. Fixed-size top 10 does not contain the complete
table-specific relation and remains incomplete. The v2 facets and decision
sheet reflect the approved criterion.

### Q021 — three confidentiality grounds

The source on [doc_016, PDF p.3](../data/pdfs/doc_016_fair_practice_code_2023.pdf)
lists three alternative grounds: legal/statutory/regulatory requirement,
public duty, and company interest. The company-interest ground includes the
fraud-prevention example and specified recipients. The marketing sentence
limits use of that ground; it is not a fourth ground. Fixed-size r2,
`doc_016_fixed_size_00003_d1e3de271923`, and structure-aware r1,
`doc_016_structure_aware_00004_15199cc67fa1`, support the three grounds and
qualification. Both proposed complete labels are supported.

### Q024 — duplicate overlap

Fixed-size r10 `doc_024_fixed_size_00004_e6145695ee32` repeats the evidence
at fixed-size r1 `doc_024_fixed_size_00003_cb861a2996e0`. V2 explicitly marks
r10 as `duplicate_of_rank: 1`. Counting the repeated chunk does not change
the complete assessment; structure-aware r1 also supports both facets.

### Q025 — five independent details and issuer attribution

The source on [doc_001, PDF p.6](../data/pdfs/bfl_fair_practice_code.pdf)
supports duplicate/certified-copy assistance, associated costs,
compensation, an additional 30 days, and the 60-day total before
delayed-period penalty calculation. Fixed-size r2,
`doc_001_fixed_size_00005_d577f4089a07`, supports F1–F4 but omits F5, so
fixed-size top 10 is incomplete. Structure-aware r1,
`doc_001_structure_aware_00005_33a0e3812a93`, supports F1–F5, so
structure-aware top 10 is complete. Fixed-size r1 from doc_003 is another
issuer and is not credited to the doc_001 question. V2 correctly separates
the five details and does not count the scenario as a facet.

## 8. Cross-artifact consistency

| Claim or artifact | Classification | Audit result |
|---|---|---|
| V2 JSONL record/facet counts and proposal status | VERIFIED | 25 records, 63 facets, all pending; 22 proposed approval states and 3 needs-review states. |
| V2 report and decision sheet for Q020/Q021/Q025 | VERIFIED | Facets, cited ranks, completeness decisions, and human-decision language agree with v2 records and source/rank evidence. |
| 2B.22 revision report | VERIFIED, except it did not identify Q001 | Its stated scope and Q020/Q021/Q025 descriptions match v2. It does not discuss the Q001 false-incomplete label. |
| 2B.23 verification report | ISSUE_FOUND | It concluded no material content discrepancy, but the Q001 rank-1 chunks directly contradict the v2 incomplete labels. |
| 2B.21 reconciliation report | ISSUE_FOUND | Its Q001 matrix says both top 10s are incomplete and rank-1 page overlap is not answer evidence; the actual chunks contain the answer sentence. |
| Evidence-level audit CSV/report | ISSUE_FOUND for Q001; historical criteria otherwise treated as non-authoritative | CSV rank-1 labels for Q001 are `PARTIAL`, despite the direct sentence. The CSV's phrase/component labels do not supersede inspection of the chunk payload. |
| Saved retrieval ranks and cited chunks | VERIFIED, with Q001 omission | Cited rank references resolve; Q001's existing rank-1 evidence was overlooked rather than missing from retrieval. |
| Q020/Q021/Q025 priority decisions | VERIFIED | Current v2 statements match source pages and saved chunks. |
| Historical diagnostics and question-results CSV unchanged status | NOT_VERIFIABLE | The 2B.23 report explicitly records that reliable pre-revision hashes/Git baselines were unavailable for these two files. Their current readability does not prove historical preservation. |
| Separate Milestone 2B.18B report | NOT_VERIFIABLE | No such report was found; the existing 2B.18 report is not reconstructed or substituted. |
| Human approval / ground-truth status | VERIFIED | No artifact changes the pending status or establishes approved ground truth. |

Historical audit reports, JSONL, CSVs, and retrieval artifacts were inspected
read-only and were not altered. The 2B.23 report records hash matches for
several other protected artifacts based on its prior comparison; this audit
does not claim a new independent historical-baseline comparison.

## 9. Decisions requiring human approval

1. Re-adjudicate Q001 using the actual fixed-size and structure-aware rank-1
   payloads and decide whether both top-10 labels should be complete.
2. Decide whether Q005 F1/F2 and Q009 F1 are required answer facets or
   question context.
3. Decide whether Q005's `covered_facets` field may list a partially
   supported facet, or whether the schema/reporting should distinguish
   partial from complete facet coverage.
4. Decide whether Q012's paired safeguards in F2 and F5 need independent
   facet IDs.
5. Retain the already specified Q020 table-specific, Q021 three-ground, and
   Q025 five-detail criteria as pending adjudication; this audit found no
   conflicting evidence for them.

## 10. Final conclusion and recommended next audit step

**NOT_VERIFIED.** Q020, Q021, and Q025 are supported by the actual source
pages and saved evidence, and most records are structurally and
cross-artifact consistent. The direct Q001 rank-1 evidence makes the current
completeness labels and multiple prior audit statements materially
unreliable. Q005 also needs facet-scope adjudication; Q009 and Q012 have
explicit granularity questions.

Recommended next step: have a human adjudicator resolve the five decisions
above, then conduct a focused read-only verification of the resulting
annotations and update any derived summaries only under a separately
authorized milestone. No annotation was edited or approved in this audit.

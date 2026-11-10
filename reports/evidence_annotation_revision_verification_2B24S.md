# PolicyLens — Independent Verification of Annotation Proposal v3

## 1. Executive verdict

**VERIFIED**

The inspected v3 records match the original questions and source references.
Only Q001, Q005, Q009, and Q012 differ semantically from v2; the other 21
records, including Q020, Q021, and Q025, are unchanged. Each cited chunk for
the four revised questions resolves to the stated saved rank and correct
source. Per-chunk facet mappings for Q009 and Q012 are supported by the actual
payloads, and both strategies have complete aggregate top-10 coverage for
those questions. Q001's rank-1 direct support and Q005's partial top-10
support are represented consistently.

This verdict verifies the proposal against the requested evidence. It does
not approve the annotations as ground truth. All 25 records remain
`pending_user_adjudication`.

## 2. Scope and method

Read and compared:

- v2 and v3 annotation JSONL.
- Original evaluation question JSONL.
- The v3 annotation report, decision sheet, and 2B.24R revision report.
- Saved fixed-size and structure-aware top-10 retrieval results.
- Every v3 cited supporting chunk for Q001, Q005, Q009, and Q012.
- Saved Q005 top-20 diagnostic ranks.
- Original PDF source pages for doc_001 pages 3–4, doc_003 page 5, and
  doc_016 page 6.
- The v1/v2 and historical reports to confirm their current presence.

For each chunk citation, I matched question, strategy, rank, and chunk ID
against the saved retrieval result; then matched its document and page span
to the chunk payload and inspected the relevant source text. No retrieval,
metric evaluation, extraction, OCR, embedding, indexing, or Qdrant operation
was run. No file was modified during this verification.

## 3. Structural integrity

| Check | Result |
|---|---|
| V3 JSONL parses | VERIFIED |
| Record count and unique IDs | VERIFIED — 25 records, exactly Q001–Q025 |
| Original question wording | VERIFIED — all 25 match the question dataset |
| Gold document IDs and PDF pages | VERIFIED — all 25 match the original gold references |
| V2-to-v3 semantic changes | VERIFIED — only Q001, Q005, Q009, Q012 differ |
| Other 21 records | VERIFIED — semantically identical to v2 |
| Facet-ID uniqueness | VERIFIED — no duplicate facet IDs within any record |
| Reviewer status | VERIFIED — all 25 are `pending_user_adjudication` |
| Q020, Q021, Q025 | VERIFIED — records are semantically unchanged from v2 and retain their prior criteria |
| Top-10 rank/chunk references for revised cases | VERIFIED — all cited IDs and ranks resolve in the correct saved strategy results |
| Source attribution | VERIFIED — cited chunks have the expected gold document and page provenance |

### Independently counted v3 totals

| Measure | Count from JSONL | Reported value | Result |
|---|---:|---:|---|
| Questions | 25 | 25 | VERIFIED |
| Required facets | 62 | 62 | VERIFIED |
| Fixed-size complete / incomplete | 21 / 4 | 21 / 4 | VERIFIED |
| Structure-aware complete / incomplete | 22 / 3 | 22 / 3 | VERIFIED |
| Pending adjudication | 25 | 25 | VERIFIED |

The totals are counts of proposed labels, not retrieval performance metrics.

## 4. Question-specific findings

### Q001 — direct rank-1 support

The question and gold source are doc_001, PDF page 3. Both actual cited
payloads contain the direct sentence, “Telling customers' how to take their
complaint forward if they are still not satisfied”:

| Strategy | Rank | Chunk ID | Finding |
|---|---:|---|---|
| Fixed-size | 1 | `doc_001_fixed_size_00001_aee405d33739` | DIRECT support for F1; payload contains the sentence and page 3. |
| Structure-aware | 1 | `doc_001_structure_aware_00001_ac782e3816d0` | DIRECT support for F1; payload contains the sentence and page 3. |

Both top-10 labels are complete, with F1 fully covered by the cited rank-1
chunk. This is direct text evidence, not an inference from page overlap.

**Result: VERIFIED. No unsupported assignment found.**

### Q005 — context, full coverage, partial evidence

V3 has no required facet for late repayment or another default; these remain
conditions in the question. The two separate answer facets are:

- F3: the charge must be stated in bold.
- F4: the charge must be stated in the loan agreement.

The fixed-size rank-5 chunk
`doc_001_fixed_size_00004_785fedf70295` and structure-aware rank-6 chunk
`doc_001_structure_aware_00004_288632361e39` are both from doc_001, PDF
pages 4–5. Each contains the clause that the quantum and reason for penal
charges are disclosed to customers in the loan agreement. Each supports the
loan-agreement-location facet F4. Neither contains the requirement to state
the charge in bold, so neither supports F3.

V3 correctly records `label: PARTIAL`, `supported_facet_ids: ["F4"]`, and
`covered_facets: ["F4"]` for each top-10 chunk. The strategy status remains
incomplete because F3 is not covered. Here, `supported_facet_ids` identifies
the facet fully supported by the cited chunk; partial status and its
justification indicate that the chunk does not establish all required facets.

The saved diagnostic confirms fixed-size rank 19
(`doc_001_fixed_size_00003_0bf6f42069fa`) and structure-aware rank 17
(`doc_001_structure_aware_00003_ad7599361f91`) contain direct evidence for
the bold and loan-agreement instructions. These ranks are outside top 10 and
are not credited to top-10 completeness.

**Result: VERIFIED. No unsupported full-coverage assignment found.**

### Q009 — two facets supported by each cited chunk

The original question supplies the disadvantage trigger; v3 does not require
it as an answer facet. The source on doc_003 PDF page 5 supports the two
retained facets:

- F2: within 60 days and without notice, close the account or switch it.
- F3: closing or switching does not require extra charges or interest.

The source states these conditions together. Each cited chunk independently
contains the full clause. The mapping is therefore per-chunk, not borrowed
from the other strategy or inferred from aggregate evidence.

#### Q009 chunk-by-facet evidence matrix

| Strategy | Rank | Chunk ID | Facet | Classification | Payload evidence | Mapping correct? |
|---|---:|---|---|---|---|---|
| Fixed-size | 2 | `doc_003_fixed_size_00006_8bf99111838c` | F2 | DIRECT | “within 60 days and without notice close his / her account or switch it” | Yes |
| Fixed-size | 2 | `doc_003_fixed_size_00006_8bf99111838c` | F3 | DIRECT | “without having to pay any extra charges or interest” | Yes |
| Structure-aware | 4 | `doc_003_structure_aware_00006_f9c845e0a416` | F2 | DIRECT | “within 60 days and without notice close his / her account or switch it” | Yes |
| Structure-aware | 4 | `doc_003_structure_aware_00006_f9c845e0a416` | F3 | DIRECT | “without having to pay any extra charges or interest” | Yes |

Both payloads are doc_003, pages 4–5, and are at the cited ranks in their
respective saved results. Both individually support both assigned facets.

**Aggregate top-10 coverage:** fixed-size `{F2, F3}` / required `{F2, F3}` —
complete; structure-aware `{F2, F3}` / required `{F2, F3}` — complete.

**Result: VERIFIED. No unsupported assignment found.**

### Q012 — seven safeguards and preservation of original requirements

V2 had five facets:

1. F1: legally enforceable clause included in the contract/loan agreement.
2. F2: notice period and circumstances in which notice can be waived.
3. F3: procedure for taking possession of the security.
4. F4: final chance to repay before sale/auction.
5. F5: procedures for returning possession and for sale/auction.

V3 retains all five substantive requirements, narrows F2 to the notice-period
requirement, narrows F5 to return of possession, and adds:

- F6: circumstances in which the notice period can be waived.
- F7: procedure for sale or auction.

This produces seven independently assessable safeguards without dropping or
duplicating a source requirement. The final repayment chance remains F4 and,
as the source says, is before sale/auction; it is not rewritten as an
opportunity before taking possession. F1 is the remaining original
contractual safeguard.

The source on doc_016 PDF page 6 separately lists each contractual provision.
Both cited chunks contain the full list and all seven assignments:

#### Q012 chunk-by-facet evidence matrix

| Strategy | Rank | Chunk ID | Facet | Classification | Payload evidence | Mapping correct? |
|---|---:|---|---|---|---|---|
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F1 | DIRECT | Clause says repossession clause in contract/loan agreement “must be legally enforceable.” | Yes |
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F2 | DIRECT | “Notice period before taking possession.” | Yes |
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F6 | DIRECT | “Circumstances under which the notice period can be waived.” | Yes |
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F3 | DIRECT | “The procedure for taking possession of the security.” | Yes |
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F4 | DIRECT | “final chance … for repayment of loan before the sale / auction.” | Yes |
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F5 | DIRECT | “The procedure for giving repossession to the borrower.” | Yes |
| Fixed-size | 4 | `doc_016_fixed_size_00006_5707a2baee10` | F7 | DIRECT | “The procedure for sale / auction of the property.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F1 | DIRECT | Clause says repossession clause in contract/loan agreement “must be legally enforceable.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F2 | DIRECT | “Notice period before taking possession.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F6 | DIRECT | “Circumstances under which the notice period can be waived.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F3 | DIRECT | “The procedure for taking possession of the security.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F4 | DIRECT | “final chance … for repayment of loan before the sale / auction.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F5 | DIRECT | “The procedure for giving repossession to the borrower.” | Yes |
| Structure-aware | 2 | `doc_016_structure_aware_00007_3562949c7e7a` | F7 | DIRECT | “The procedure for sale / auction of the property.” | Yes |

Both payloads are doc_016, PDF page 6, and their stated ranks match the saved
results. Each chunk individually supports all seven assigned facets.

**Aggregate top-10 coverage:** fixed-size `{F1, F2, F3, F4, F5, F6, F7}` /
required `{F1, F2, F3, F4, F5, F6, F7}` — complete; structure-aware has the
same complete coverage. This result is supported by each cited chunk itself,
not an assumption that evidence is distributed across ranks.

**Result: VERIFIED. No dropped, invented, duplicated, or unsupported facet
assignment found.**

## 5. Per-chunk, aggregate, and completeness distinctions

- **Per-chunk facet support** is the relationship asserted by
  `supporting_chunks[].supported_facet_ids`; it must be justified by that
  exact payload.
- **Aggregate top-10 facet coverage** is the union of facets fully supported
  by relevant chunks in the saved top ten. It may combine multiple chunks if
  the annotation explicitly represents that aggregation.
- **Overall top-10 completeness** is complete only when aggregate full
  coverage includes every required facet. A partial chunk or a diagnostic
  rank outside top 10 cannot fill a top-10 gap.

For Q009, the one cited chunk per strategy individually supports both
required facets. For Q012, the one cited chunk per strategy individually
supports all seven. Thus no unsupported assignment is being excused by
aggregate coverage. Q005 is incomplete: only F4 is fully supported in each
top-10 citation, and F3 is absent. Q001 is complete in both strategies from
direct rank-1 evidence.

## 6. Report consistency

| Artifact claim | Result |
|---|---|
| V3 report lists the actual revised facets and per-strategy ranks/statuses for Q001/Q005/Q009/Q012 | VERIFIED |
| V3 report's 25-question matrix agrees with v3 JSONL | VERIFIED |
| V3 facet and completeness totals agree with independent JSONL counts | VERIFIED |
| Decision sheet's Q005 distinction between F4 full coverage and F3 missing | VERIFIED |
| Decision sheet's Q009 two-facet and Q012 seven-facet mappings | VERIFIED |
| 2B.24R revision report accurately describes changed records, ranks, status changes, validation, and limitations | VERIFIED |
| Reports distinguish proposal status from approval | VERIFIED — no claim that annotations are approved ground truth |
| Historical v1/v2 annotations and earlier reports are present | VERIFIED — the audit did not modify them |

## 7. Unsupported assignments, limitations, and unresolved issues

**Unsupported facet assignments:** None found for Q001, Q005, Q009, or Q012.
In particular, Q009 does not incorrectly assign both facets based on
different chunks, and Q012's all-seven mappings are supported by each
individual cited chunk.

**Limitations:** This was an independent verification of the specified v3
records and evidence, not an adjudication of all 25 questions from scratch.
The existing historical limitation concerning the absence of reliable
pre-revision baselines for the top-20 diagnostic and question-results CSV
remains; their unchanged historical status is not newly established here.
All records remain pending human adjudication.

**Historical preservation:** v1, v2, the v2 companion reports, and prior
2B.21/2B.23/2B.24 reports were present. They were not changed during this
verification. Their presence does not establish any unstated earlier hash
baseline.

## 8. Final recommendation

**Accept v3 as a verified proposal.** The audited chunk-to-facet mappings,
aggregate top-10 coverage, completeness statuses, structural checks, and
companion reports are consistent with the saved evidence and human-approved
revision decisions. This recommendation is not approval of the annotations
as ground truth; all 25 remain pending user adjudication.

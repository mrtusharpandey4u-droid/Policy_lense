# Evidence Annotation Decision Sheet — Q020, Q021, Q025

**Status:** `REQUIRES_USER_APPROVAL`

This is an assistant-prepared, source-grounded decision aid, not human-adjudicated
ground truth. PDF page numbers below are one-based; printed page numbers are
identified separately where verified. The existing annotation proposal remains
unchanged.

## Q020 — Table II.2.1 GFCF value

**Question:** “In RBI Annual Report Table II.2.1, what growth rate is listed for
Gross Fixed Capital Formation in 2023-24?”

**Source:** `doc_036`, [RBI Annual Report 2023-24](../data/pdfs/doc_036_rbi_annual_report_2023_24.pdf),
PDF page 41 (printed page 16). The table row reads:

> Gross Fixed Capital Formation | 1.1 | -7.1 | 17.5 | 6.6 | 10.2

The column headings run from 2019-20 through 2023-24, so the requested value is
**10.2 per cent**. This row and the year headings were verified in the original
PDF's extracted table cells.

**Retrieved evidence checked:** Structure-aware rank 10, chunk
`doc_036_structure_aware_00080_da6891873a1b` (PDF page 41), contains the year
headings and the complete structured row, including `10.2`. Structure-aware
rank 5, chunk `doc_036_structure_aware_00058_627c4c142023` (PDF pages 27-28),
instead states that GFCF accelerated to 10.2 per cent in 2023-24. Fixed-size
rank 2, `doc_036_fixed_size_00070_eb1ac13cadb6` (PDF pages 40-41), includes the
GFCF row name but not `10.2`; no fixed-size top-10 chunk inspected contains
the complete requested row/year/value relation.

**Recommended interpretation:** Because the question names a specific table
and asks what it lists, require evidence of the table row, year column, and
intersecting value for full table-specific completeness. Under that criterion,
the structure-aware rank-10 table payload is relevant and completes the answer;
the existing proposal's “Incomplete” status for structure-aware and its claim
that no top-10 chunk contains the row/value are contradicted by the inspected
data.
The fixed-size strategy remains incomplete for this table-specific question.

**Alternative interpretation:** Accept the page-28 narrative as sufficient
evidence for the numeric fact. This would give credit to a result that answers
“what was the GFCF growth rate?” without retrieving the named table. It may be
appropriate for a fact-answering evaluation, but it does not measure retrieval
of the specified table evidence. The narrative is an acceptable alternate
source for the number, not a substitute for the table in the primary
table-specific criterion.

**Facet decision:** Both proposed facets are needed: identify the GFCF row and
2023-24 column, then read their value. They are jointly covered by the
structure-aware rank-10 table payload on the gold page.

**Decision:** `REQUIRES_USER_APPROVAL`

## Q021 — Exceptions to confidentiality

**Question:** “When can the finance company disclose a borrower's personal or
transaction information without the borrower's authorization?”

**Source:** `doc_016`, [Fair Practice Code 2023](../data/pdfs/doc_016_fair_practice_code_2023.pdf),
PDF page 3. The confidentiality clause introduces “the following exceptional
cases” and lists:

> If the Company has to provide the information by legal, statutory or
> regulatory laws; if there is a duty to the public to reveal this information;
> or if the Company’s interest requires it (e.g., fraud prevention) to Banks /
> Financial institutions / Group / Associate Companies.

It adds:

> The Company will not use this reason for giving information about borrowers
> to anyone else for marketing purpose.

**Retrieved evidence checked:** Fixed-size rank 2,
`doc_016_fixed_size_00003_d1e3de271923`, and structure-aware rank 1,
`doc_016_structure_aware_00004_15199cc67fa1`, both span PDF pages 2-3 and
contain all three grounds and the marketing limitation.

**Recommended interpretation:** For a reproducible, complete answer to this
policy question, require the full enumerated list of three alternative
grounds. The marketing sentence is not a fourth ground; it is a boundary on
the company-interest ground and should be attached to that condition when
reported. The proposed F1-F3 represent the grounds; F4 is best treated as a
qualification to F3, not as an independent exception.

**Alternative interpretation:** The wording “When can” does not expressly say
“list every circumstance.” If the intended task is to provide one valid
example, any single source-supported ground could answer it. That looser
criterion would not detect omission of the other listed exceptions. If the
company-interest ground is the example selected, omitting the marketing
limitation could overstate that ground.

No alternate source location is proposed: the question is grounded in
`doc_016`'s company-specific confidentiality policy, and a similar clause in
another lender's code would not establish this company's terms.

**Decision:** `REQUIRES_USER_APPROVAL`

## Q025 — Lost or damaged property documents

**Question:** “If original property papers are lost or damaged after a personal
loan is settled, what support and additional time does the code allow?”

**Source:** `doc_001`, [Bajaj Finance Fair Practice Code, Version 7.1](../data/pdfs/bfl_fair_practice_code.pdf),
PDF page 6. The section scope says the procedure is for cases due after
December 1, 2023. The loss/damage clause says:

> The Company shall assist the borrower in obtaining duplicate/certified
> copies ... and shall bear the associated costs, in addition to paying
> compensation as indicated at clause (i) above. However, in such cases, an
> additional time of 30 days will be available to the Company to complete this
> procedure and the delayed period penalty will be calculated thereafter
> (i.e., after a total period of 60 days).

**Retrieved evidence checked:** Structure-aware rank 1,
`doc_001_structure_aware_00005_33a0e3812a93` (PDF pages 5-6), contains the
duplicate-copy assistance, costs, compensation cross-reference, 30 additional
days, and 60-day total. Fixed-size rank 2,
`doc_001_fixed_size_00005_d577f4089a07` (PDF pages 5-6), contains the support,
cost/compensation language, and additional 30 days, but not the 60-day total.
A fixed-size rank-1 chunk from `doc_003` contains a similar 60-day clause for a
different lender; it is not evidence for `doc_001` and cannot complete this
source-specific answer.

**Recommended interpretation:** The answer's required content is assistance
with duplicate/certified copies, the company's responsibility for associated
costs, and an additional 30 days. State the 60-day total as an important
qualification to explain when the delayed-period penalty begins; it is not a
separate support item. The scope date (cases due after December 1, 2023) is a
source applicability caveat, not a requested remedy. The proposed F1 merely
repeats the scenario and should not be required as an answer facet. Split
proposed F3: associated costs are required; compensation is an additional
source-stated entitlement but not necessary to answer the specific “support
and additional time” wording. Split proposed F4 so the extra 30 days and the
60-day penalty boundary can be assessed distinctly.

Under this interpretation, structure-aware rank 1 supports the full response.
Fixed-size rank 2 supports the core assistance/cost/extra-time response, but
does not state the 60-day penalty boundary. If the user decides that boundary
is mandatory for completeness, fixed-size is incomplete on the gold-source
chunk. The existing proposal's single combined F4 obscures this distinction.

**Alternative interpretation:** Require both compensation and the post-60-day
penalty boundary as independent answer facets, treating the question as asking
for every consequence of lost documents. This produces a more exhaustive
policy summary, but makes completeness depend on details beyond the question's
explicit request for support and additional time. Conversely, omitting the
60-day qualification from an answer that states the additional 30 days could
leave the deadline ambiguous; it is therefore recommended as a concise
clarification even if not scored as a separate facet.

No alternate source location is proposed: similar text from another lender's
code is not interchangeable with `doc_001`.

**Decision:** `REQUIRES_USER_APPROVAL`

## Review outcome

The source passages and cited retrieved chunks were checked directly. The
decision points above remain unresolved until approved. In particular, the
existing proposal's Q020 completeness note should be corrected after approval,
and Q025's combined facets should be reconsidered. No source, question,
annotation, retrieval result, or other existing project artifact was changed
for this decision sheet.

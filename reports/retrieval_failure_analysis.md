# PolicyLens — Retrieval Failure Analysis (Milestone 2B.17)

## Scope and method

This is a read-only analysis of the five requested questions: Q003, Q004,
Q005, Q010, and Q011. Each gold evidence snippet was checked against its
original PDF page and corresponding cleaned page after Unicode and whitespace
normalization. Source chunks and returned top-10 chunks were inspected in both
chunk files. The top-10 metadata and scores are from the persisted Milestone
2B.16 records; each candidate ID was mapped back to its full chunk text.

The official 2B.16 relevance rule is document ID plus overlap with 1-based PDF
page provenance. A `*` in the candidate lists below marks that page-level
match; it does not assert that the chunk contains the exact gold evidence.
This distinction matters in Q004 and Q005.

A separate read-only diagnostic searched the top 20 in both production
collections for these five queries. It used the existing pinned local BGE-M3
query embedding and `src.search.retrieve`, generated one 1,024-dimensional
query vector per question, reused that vector for both strategies, used cosine
similarity with no metadata filters, and did not update either collection.
The output is
`data/evaluation/results/retrieval_failure_top20_diagnostic.json`. These ranks
are diagnostic only and are not included in Milestone 2B.16 metrics.

## Findings by question

### Q003 — borrower communication language

**Question:** “In what language must borrower communications be provided
under this fair-practice code?”

**Gold:** `doc_001`, PDF page 4. The original PDF and cleaned page both contain
the evidence that communications must be in the vernacular or a language the
borrower understands. The exact evidence is present in fixed-size chunk
`doc_001_fixed_size_00003_0bf6f42069fa` and structure-aware chunk
`doc_001_structure_aware_00003_ad7599361f91`. These source chunks are native
text and have no cleaning-review flag.

The evidence-bearing chunk ranks 7 for fixed-size and 4 for structure-aware.
Fixed-size has another page-overlapping chunk at rank 8, but it does not
contain the evidence sentence. Competing results include Fair Practice Code
passages from `doc_017`, `doc_002`, `doc_003`, and other pages in `doc_001`.
Thus there is a confirmed ranking difference in structure-aware's favor;
the content itself is present and the gold page is correct. The similar
cross-issuer policies are a plausible source of competition, not a proven
single cause.

Top-10 candidates (`rank doc_id pages score`; `*` = page-level gold match):

- Fixed-size: `1 doc_001 p10–11 .683; 2 doc_017 p1 .681; 3 doc_001 p9–10 .654; 4 doc_002 p1–2 .654; 5 doc_003 p18–19 .645; 6 doc_003 p1–2 .644; 7 doc_001 p3–4 .630*; 8 doc_001 p1–4 .621*; 9 doc_024 p1–2 .617; 10 doc_016 p1 .611`
- Structure-aware: `1 doc_017 p1 .679; 2 doc_001 p10–11 .660; 3 doc_003 p1–2 .641; 4 doc_001 p3–4 .634*; 5 doc_003 p19 .631; 6 doc_002 p1–2 .631; 7 doc_001 p10 .621; 8 doc_024 p1–2 .619; 9 doc_017 p3–4 .617; 10 doc_001 p1–3 .617`

### Q004 — information conveyed at sanction

**Question:** “What key loan information must Bajaj Finance convey in
writing when a loan is sanctioned?”

**Gold:** `doc_001`, PDF page 4. The page and cleaned text contain the amount
sanctioned, terms and conditions, annualized interest rate, and rate
application method. Exact evidence is present in fixed-size chunk
`doc_001_fixed_size_00003_0bf6f42069fa` and structure-aware chunk
`doc_001_structure_aware_00003_ad7599361f91`; both match at rank 4 and 7,
respectively.

The fixed-size official first relevant rank is 1, but that result,
`doc_001_fixed_size_00001_aee405d33739` (pages 1–4), does **not** contain the
gold evidence text. Its page provenance includes page 4, so it receives
relevance under the official page-overlap rule. This is a confirmed
page-level over-credit relative to evidence-text retrieval, not a reason to
rewrite the official result. Under a strict evidence-text check the first
fixed-size hit in this question would instead be rank 4. Structure-aware's
first page-level hit is rank 7 and does contain the evidence. The apparent
rank-1 fixed-size result therefore exaggerates its advantage on this
particular question.

Top-10 candidates:

- Fixed-size: `1 doc_001 p1–4 .641*; 2 doc_003 p4–5 .606; 3 doc_002 p2–3 .600; 4 doc_001 p3–4 .597*; 5 doc_016 p1–2 .595; 6 doc_017 p1–2 .594; 7 doc_003 p4–5 .582; 8 doc_016 p2–3 .580; 9 doc_001 p9–10 .575; 10 doc_001 p4–5 .570*`
- Structure-aware: `1 doc_001 p1–3 .636; 2 doc_016 p2 .609; 3 doc_003 p18 .603; 4 doc_003 p4–5 .601; 5 doc_002 p2–3 .591; 6 doc_003 p18 .586; 7 doc_001 p3–4 .575*; 8 doc_001 p4–5 .571*; 9 doc_017 p1–2 .571; 10 doc_001 p9 .566`

### Q005 — where penal charges must be highlighted

**Question:** “Where must penal charges for late repayment or another
borrower default be highlighted?”

**Gold:** `doc_001`, PDF page 4. The source and cleaned page contain the
instruction to mention the penal charge in bold in the loan agreement.
The exact evidence-bearing chunks are
`doc_001_fixed_size_00003_0bf6f42069fa` and
`doc_001_structure_aware_00003_ad7599361f91`; neither is in the official
top 10. In the top-20 diagnostic, they rank 19 and 17, respectively.

The chunks counted by the official page rule at ranks 5 (fixed-size) and 6
(structure-aware) are `doc_001_*_00004_...` page 4–5 chunks. Their text
contains related penal-charge provisions, but not the gold instruction about
late repayment/default being in bold in the loan agreement. The exact source
sentence is present in the adjacent page-3–4 chunk instead. This is confirmed
evidence of a page-level relevance over-credit and of the answer-bearing
chunk being ranked below top 10. The results are consistent with competing
penal-charge passages from other policies and a chunk-boundary/context issue;
the diagnostic does not establish which factor caused the low rank.

Top-10 candidates:

- Fixed-size: `1 doc_003 p7–8 .677; 2 doc_003 p8 .668; 3 doc_003 p4–5 .656; 4 doc_030 p14–15 .639; 5 doc_001 p4–5 .626*; 6 doc_003 p4–5 .625; 7 doc_016 p2–3 .622; 8 doc_007 p11 .621; 9 doc_036 p276 .620; 10 doc_003 p8–9 .619`
- Structure-aware: `1 doc_030 p15 .643; 2 doc_003 p8 .637; 3 doc_003 p7 .635; 4 doc_003 p8–9 .628; 5 doc_036 p276 .620; 6 doc_001 p4–5 .614*; 7 doc_024 p2–3 .611; 8 doc_007 p11 .605; 9 doc_001 p7–8 .597; 10 doc_030 p16 .597`

### Q010 — borrower risk gradation and rate rationale

**Question:** “Where must Shriram Finance explain how it grades borrower
risk and why different rates are charged?”

**Gold:** `doc_016`, PDF page 2. The sentence naming the loan application
form, sanction letter, website, or relevant newspapers appears in both the
original PDF and cleaned page. It is also present in the source chunks:
`doc_016_fixed_size_00002_aac99a7d19b5` and
`doc_016_structure_aware_00003_6a9423992e87`. The source page is native text
and has no cleaning-review flag.

Neither strategy has a page-2 result in the official top 10, so Q010 is
correctly recorded as missed there. In the top-20 diagnostic, the
structure-aware evidence-bearing page-2 chunk appears at rank 18 (score
0.530953). No fixed-size gold-page chunk appears in ranks 1–20. Therefore the
structure-aware miss is a cutoff/ranking issue at top 10; the fixed-size
result is lower than rank 20 or absent from the returned top 20. No exact
cause is established.

The query says “grades borrower risk,” while the source wording is “approach
for gradation of risks.” The top ranks also include related interest-rate
model passages, including `doc_003` pages 7–8, and other lenders' policy
text. These are confirmed lexical/topic competitors and make query wording
or embedding ranking plausible hypotheses, not confirmed root causes.
Source extraction and the gold page are not the problem.

Top-10 candidates:

- Fixed-size: `1 doc_016 p1 .624; 2 doc_016 p6–7 .616; 3 doc_003 p7–8 .602; 4 doc_017 p4 .580; 5 doc_019 p1 .579; 6 doc_019 p1–3 .573; 7 doc_001 p4–5 .562; 8 doc_002 p5–6 .555; 9 doc_016 p4–5 .546; 10 doc_036 p272 .542`
- Structure-aware: `1 doc_016 p1 .620; 2 doc_003 p7 .584; 3 doc_019 p1 .584; 4 doc_001 p4–5 .575; 5 doc_024 p2–3 .558; 6 doc_019 p1–3 .553; 7 doc_027 p10–11 .547; 8 doc_016 p6–8 .545; 9 doc_002 p6 .545; 10 doc_036 p272 .542`

### Q011 — Board duties for grievance handling and FPC compliance

**Question:** “What governance duties does Shriram Finance's board have for
grievance handling and Fair Practice Code compliance?”

**Gold:** `doc_016`, PDF page 5. The PDF and cleaned page contain the Board's
grievance-redressal mechanism, next-level dispute handling, and periodic
review duties. The exact evidence is present in
`doc_016_fixed_size_00005_92e15d19bd51` and
`doc_016_structure_aware_00006_d4c341ea43e2`; both are native and unflagged.
They rank 5 and 8, respectively.

Both top-10 lists rank Shriram's page-1 introduction first (scores 0.720109
and 0.698482); it discusses Board/management responsibility for fair-lending
practices but is not the page-5 governance provision. Other Shriram passages
on pages 6–8 also rank early. This is consistent with related policy context
and a ranking problem. The evidence itself is intact and the gold page is
correct; the specific cause of the ordering is not isolated.

Top-10 candidates:

- Fixed-size: `1 doc_016 p1 .720; 2 doc_016 p6–7 .627; 3 doc_001 p7–8 .563; 4 doc_001 p9–10 .554; 5 doc_016 p4–5 .554*; 6 doc_001 p1–4 .551; 7 doc_003 p1–2 .547; 8 doc_002 p5–6 .546; 9 doc_017 p2–3 .544; 10 doc_016 p9 .540`
- Structure-aware: `1 doc_016 p1 .698; 2 doc_016 p6–8 .618; 3 doc_016 p1–2 .569; 4 doc_003 p13–14 .558; 5 doc_001 p1–3 .554; 6 doc_001 p10 .545; 7 doc_003 p1–2 .545; 8 doc_016 p5 .541*; 9 doc_001 p7–8 .540; 10 doc_002 p5 .525`

## Cross-case interpretation

All five gold evidence snippets were found on the cited original PDF page and
in the corresponding cleaned page. The source chunks containing the evidence
also exist for both strategies. None of these five is an OCR or manual-cleaning
review case. This rules out missing source text as the explanation for these
retrieval outcomes.

Confirmed observations:

- Q003 and Q011 retrieve evidence-bearing chunks in the official top 10, but
  related policy sections outrank them.
- Q010's exact structure-aware gold-page chunk is at diagnostic rank 18;
  fixed-size has no gold-page match in top 20.
- Q005's evidence-bearing source chunks are at diagnostic ranks 19 and 17,
  while the official page-level top-10 hits are adjacent penal-charge text
  without the queried bold/loan-agreement instruction.
- Q004's fixed-size rank-1 page-level match does not contain the gold passage;
  an evidence-bearing fixed-size chunk is rank 4.

These observations support a weakness in **page-only chunk relevance**:
provenance may include a page while the chunk text omits the particular
evidence. The official evaluation results are left unchanged. A future
evaluation should retain document/page validation but also inspect the
retrieved chunk's evidence span or use reviewed chunk-level gold labels. A
future chunking experiment could test tighter paragraph/section boundaries
around adjacent instructions while preserving enough context and intact
table rows. No implementation or evaluation labels were changed here.

## Limitations

- The top-20 diagnostic covers only the five specified questions and is not a
  new benchmark or statistical test.
- Fixed-size gold-page chunks not returned in its top 20 are reported as
  absent from that diagnostic window; their exact later rank was not
  established.
- Exact normalized snippet containment is a useful audit signal but is not a
  complete semantic relevance measure. Where the exact text is absent, the
  retrieved text was inspected to distinguish a related provision from the
  specific requested instruction.
- Scores describe cosine retrieval order only; they do not prove why the
  model ranked candidates as it did.

# Retrieval Evaluation Dataset Report

## Dataset composition

The dataset at `data/evaluation/evaluation_questions.jsonl` contains exactly
25 questions:

| Category | Count | Question IDs |
|---|---:|---|
| Standard | 15 | Q001–Q015 |
| Table-value | 5 | Q016–Q020 |
| Paraphrased | 5 | Q021–Q025 |

Each question has one gold reference with document ID, manifest title and
issuer, a 1-based PDF page number, the corresponding zero-based PDF page index,
section title, concise evidence snippet, and reference notes. Printed page
numbers are recorded separately when applicable.

## Gold document and page coverage

The 25 references cover eight verified corpus documents:

| Document ID | Gold PDF pages |
|---|---|
| doc_001 | 3, 4, 5, 6 |
| doc_003 | 4, 5 |
| doc_016 | 2, 3, 5, 6 |
| doc_019 | 2 |
| doc_023 | 2, 7 |
| doc_024 | 2, 3 |
| doc_034 | 1 |
| doc_036 | 41 |

Gold pages use the same 1-based PDF-page convention as the search/index
payloads. For RBI Annual Report Table II.2.1, the cited page is PDF page 41;
the printed page number is 16 and is stored separately.

## Source verification method

The validator, `src/validate_evaluation_dataset.py`, checks that every
reference:

- Resolves to a verified manifest entry and matches its title and issuer.
- Falls within the manifest page count and has the corresponding PDF index.
- Points to a readable source PDF whose SHA-256 matches the manifest.
- Has evidence found on the cited source page. For table questions, evidence is
  checked against PyMuPDF-extracted table rows rather than requiring a table row
  to appear as one contiguous ordinary-text string.
- Maps to at least one indexed chunk covering the gold page in each strategy.

The eight referenced source PDFs were opened and hash-checked. All 25 gold page
references passed the source and page checks. Q020’s printed-page/PDF-page
difference is explicitly represented; no other page-number convention issue
was found.

## Table-value verification

The five table-value questions use values from the original PDF tables:

- **Q016:** TCL Retail PLR, 11.50% current and 11.75% revised, effective
  01-Nov-26.
- **Q017:** 0.40% incentive, capped at ₹100, for the applicable RuPay debit
  card category.
- **Q018:** 0.25% incentive for BHIM-UPI P2M transactions up to ₹2,000 outside
  industry programmes.
- **Q019:** T+2 working days to tag a case as QRC.
- **Q020:** 10.2 per cent growth for Gross Fixed Capital Formation in 2023-24.

Each value and its conditions were checked against the source PDF table and
the corresponding structured table record. All five questions also have their
evidence in table-bearing payloads in both indexed strategies. The validator
found no explicit split-table fragment markers (`part_count > 1`) on these
gold references.

## Paraphrased questions

Q021–Q025 paraphrase source provisions on confidentiality exceptions,
borrower contact hours, lender grievance handling, consent for microfinance
add-on products, and recovery-agent conduct. Their evidence snippets were
checked against the cited source pages. The maximum lexical similarity between
a paraphrased question and its evidence snippet is 0.372; this is a screening
signal only, not a semantic-equivalence measure.

## Indexed-chunk readiness

| Strategy | Collection | Collection points | Questions with all gold references mapped | Table-value evidence in table payloads |
|---|---|---:|---:|---:|
| Fixed-size | `policylens_fixed_size_bge_m3` | 1,370 | 25/25 | 5/5 |
| Structure-aware | `policylens_structure_aware_bge_m3` | 1,478 | 25/25 | 5/5 |

All 25 references mapped to indexed chunks in both collections. No gold
reference was unmappable. No table-value question was found to have an explicit
split-table fragment marker in the matching payloads.

## Validation results and limitations

Command run:

```bash
.venv/bin/python -m src.validate_evaluation_dataset
```

Result: **passed** — 25 records; category counts 15/5/5; 25 verified gold page
references; eight source PDF hashes checked; all questions mapped in both
collections; all table values verified in original and cleaned structured
tables and present in both strategies' table payloads; zero validation
warnings or errors. PyMuPDF may print its optional
`pymupdf_layout` layout-analysis recommendation during table extraction; it does
not affect the validation result.

This milestone establishes a source-grounded retrieval evaluation set only.
It does not calculate Recall@K, MRR, or any other retrieval-quality metric,
and does not establish that retrieved results are relevant.

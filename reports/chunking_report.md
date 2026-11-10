# Milestone 2B.7 — Chunking Report

## Result

The chunking pipeline processed all **31 cleaned documents and 814 page
records** using the cleaned JSONL files as read-only inputs. It generated
separate fixed-size and structure-aware outputs under
`data/processed/chunks/`. No input record failed, and the chunking summary
reports no errors.

| Measure | Fixed-size | Structure-aware |
|---|---:|---:|
| Chunks generated | 1,370 | 1,478 |
| Minimum / median / average / maximum tokens | 3 / 500 / 405.94 / 1,107 | 3 / 414.5 / 348.81 / 1,107 |
| Chunks in the 300–800 token range | 1,052 (76.79%) | 1,016 (68.74%) |
| Text chunks | 930 | 1,038 |
| Text chunks in the target range | 915 (98.39%) | 879 (84.68%) |
| Structured table chunks | 440 | 440 |
| Chunks carrying cleaning-review flags | 154 | 153 |
| Chunks carrying OCR provenance | 65 | 72 |
| Chunks missing title, issuer, issue date, or source hash | 0 | 0 |

The overall size distribution includes table chunks, which are kept separate
from prose and are often much shorter than 300 tokens. The six chunks marked
as exceeding the configured 500-token target are table fragments whose rows
could not be divided safely; two exceed 800 tokens. Such rows remain intact
and are explicitly marked rather than being split mid-row.

## Configuration and Tokenizer

The run used a **500-token target** and **50-token overlap**, with the
assignment's 300–800 token range as the preferred target. Counts use
`PolicyLens Unicode lexical tokenizer v1`: the regex `\w+|[^\w\s]` counts
Unicode word/number runs and individual punctuation characters. This is a
deterministic lexical measure, not a count from a particular language model
tokenizer. In particular, punctuation inside dates, amounts, and percentages
can increase this count.

Fixed-size chunking forms a sliding window over each document and preserves
intentional overlap. Structure-aware chunking builds units from detected
headings, clause-like lines, and paragraph boundaries, preferring a heading
boundary when the current chunk is near its target. Oversized sections are
split with overlap. Both strategies keep documents separate and record the
source page range and per-page provenance.

## Tables, Metadata, and Provenance

- The inputs contained **370 structured tables**. Both outputs contain all
  370 table groups as **440 table chunks**; 63 source tables were split at
  row boundaries. Reassembly validation found every original row, in order,
  and confirmed that each split fragment repeats the first extracted row.
- Table chunks retain the source table structure and extraction metadata.
  The six over-target fragments were retained intact and marked.
- All **71 cleaning-review pages** and all **37 OCR-selected pages** remain
  identifiable in chunk page provenance. Review flags were not used to drop
  content.
- Every output chunk has a unique deterministic ID. All chunks have
  `doc_id`, page range, title, issuer, issue date, and source hash. The source
  hashes agree with the verified manifest rows.
- A token-sequence comparison against canonical source text found no loss or
  duplication beyond the configured overlap in either strategy. Table-only
  fallback text is represented by the separate structured table chunk, not
  emitted a second time as prose.
- Six empty pages with no structured table and no cleaning-review flag do not
  produce empty chunks. All other pages are represented by chunk page
  provenance.

## Representative Corpus Examples

These are real generated records; page numbers are the original 1-based PDF
page numbers.

| Strategy / content | Document | Page range | Example |
|---|---|---:|---|
| Fixed-size text | `doc_001` | 1–4 | Fair Practice Code, 500 tokens |
| Structure-aware text | `doc_001` | 1–3 | Fair Practice Code, 475 tokens |
| Structured table | `doc_036` | 41 | RBI Annual Report consumption table; 300 tokens |
| OCR-derived text | `doc_004` | 1 | OCR selection and provenance carried on the chunk |

The structure-aware chunk records the detected section title and preserves
source headings and text in the chunk body. A chunk may span more than one
short section when combining them is needed to approach the configured target.

## Validation and Reproducibility

- Chunk-specific tests: **12 passed**.
- Full project test suite: **53 passed**.
- Compilation: `.venv/bin/python -m compileall -q src tests` passed.
- `git diff --check` passed.
- Output validation: zero duplicate IDs, invalid page ranges, missing review
  or OCR provenance, missing source metadata, missing tables, or changed table
  rows.
- Text-token reconstruction: exact for both strategies after removing only
  the intentional overlap.
- Idempotency: a second full run produced byte-identical hashes for
  `fixed_size.jsonl`, `structure_aware.jsonl`, and `chunking_summary.json`.
- Run summary: `data/processed/chunks/chunking_summary.json`.

The test run emitted six third-party deprecation warnings from PyMuPDF/SWIG;
there were no test failures.

## Limitations

1. The existing table schema provides extracted rows but does not identify
   multi-row header boundaries. The chunker conservatively repeats the first
   extracted row as the header for split fragments; additional header rows
   remain in the original first fragment but cannot be reliably inferred for
   repetition. Multi-level headers in split tables may therefore need review.
2. The lexical tokenizer is reproducible and transparent but does not
   estimate any embedding model's token count. Chunk sizes should be revisited
   if a specific downstream model is selected.
3. Six table fragments exceed the 500-token target because their indivisible
   row content cannot be split safely. Rows were kept intact to avoid
   damaging table meaning.
4. OCR-derived text and pages marked for cleaning review retain their
   provenance and flags; chunking does not correct or validate OCR text.
5. No embeddings, indexing, search, retrieval, evaluation, or answer
   generation were implemented.

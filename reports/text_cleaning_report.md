# Milestone 2B.6 — Conservative Text Cleaning and Normalization

## Executive Summary

The new cleaning stage processed **814 pages across 31 documents** and wrote
cleaned copies to `data/processed/cleaned/`. The source extraction/OCR JSONL
files were not modified. No document failed.

| Measure | Result |
|---|---:|
| Pages processed | 814 |
| Pages whose canonical text changed | 724 |
| Native text selected | 777 |
| OCR text selected | 37 |
| Repeating edge-line candidates identified | 12 |
| Repeating edge lines removed | 0 |
| Repeating standalone page numbers removed | 47 |
| Native wrapped lines joined with a space | 11,540 |
| Native hyphen-wrapped lines joined, retaining the hyphen | 77 |
| Repeated blank lines collapsed | 300 |
| Soft hyphen characters removed | 0 |
| Pages flagged for manual review | 71 |
| Errors | 0 |

The 12 repeated edge-line candidates were retained because they matched
document-cover content, detected headings, or policy/version/date/legal
information. This conservative result avoids removing meaningful document
titles or regulatory metadata. The 47 removed page numbers were standalone
numbers equal to the physical PDF page number, in a page-edge position, and
repeated on at least 60% of the document's pages (minimum three pages).

## Architecture and Output

`src/clean.py` reads only top-level `data/processed/doc_*.jsonl` inputs and
writes one JSONL per document under `data/processed/cleaned/`. Each output
record is a copy of the input record with two additive fields:

- `canonical_text`: selected and conservatively normalized page text.
- `cleaning`: selection reason, native text quality assessment, OCR
  provenance where selected, operations applied, repeated-edge candidates,
  page-number removal, and review flags.

Original `text`, `native_text`, `ocr`, blocks, headings, tables, document ID,
source filename/hash, and page number are retained unchanged in the cleaned
copy. The raw input JSONL remains the source of record. The JSON summary is
written separately to `data/processed/cleaning_summary.json`.

## Cleaning Rules

### Whitespace and line breaks

- `CRLF`/`CR` line endings are normalized to `LF`.
- Leading/trailing whitespace on each line and runs of ordinary spaces are
  normalized; tabs and pipe delimiters are preserved.
- Repeated blank lines are reduced to one blank line. Paragraph boundaries
  are retained.
- Native lines are joined only when their adjacent lines belong to the same
  extracted text block and their positions are consistent with line wrapping.
  Bullet/list markers, separate blocks, table blocks, and OCR-only lines are
  not joined by this rule.
- Structured `tables` are never rewritten. Any pipe-delimited table fallback
  already present in native text keeps its row/column delimiters.

### Repeating headers, footers, and page numbers

A repeated edge line is a candidate only if it occurs in the first or last
two nonblank lines on at least three pages and on at least 60% of pages in the
same document. Titles, cover text, detected headings, digits, and lines
containing policy/legal/financial terms are protected. The 12 detected
candidates were recorded in page-level `cleaning.repeating_edge_line_candidates`;
all were retained under these safeguards.

A standalone page number is removed only when it equals the page record's
1-based PDF page number, occurs at the page edge, and satisfies the same
document repetition threshold. Clause numbers and page references inside
content are unchanged. The page number in record metadata is never changed.

### Hyphenation and OCR

- A native line break is repaired only when the two adjacent lines are
  supported by consecutive lines in the same native text block.
- The printed hyphen is retained: `re-` + line break + `verification` becomes
  `re-verification`. The cleaner does not guess whether a visible hyphen was
  typographic or lexical.
- Ambiguous visible-hyphen line breaks without sufficient block evidence are
  preserved and flagged; this includes OCR text, for which line-position
  metadata is not available in the existing OCR schema.
- Soft hyphens are deterministically removed if encountered; none were found
  in this run.
- OCR is selected only when successful OCR provenance is present and the
  separate native text is absent or fails the extractor's documented
  threshold (fewer than 30 non-whitespace characters or alphanumeric ratio
  below 0.35). The cleaner selects OCR text alone in that case; it does not
  concatenate it with the native/OCR merged `text` field.
- If an OCR record lacks a separate native snapshot, its combined `text` is
  not trusted as native input; the separate successful `ocr.text` field is
  selected instead.
- No financial values, percentages, dates, names, legal terms, or citations
  are automatically corrected.

## Before-and-After Examples

Examples below are taken from the raw page records and the generated cleaned
records. The original source fields remain in the cleaned copy.

### Normal native text and table-heavy page — `doc_036`, page 41

**Before:**

```text
II.2.4<TAB>
Private final consumption expenditure 
(PFCE) – the mainstay of domestic aggregate 
demand – slackened in 2023-24.
```

**After:**

```text
II.2.4
Private final consumption expenditure (PFCE) – the mainstay of domestic aggregate
demand – slackened in 2023-24.
```

The block-internal line wraps were joined, while the `II.2.4` section label
remained separate. The page's extracted table rows (including the `2019-20`
through `2023-24` column labels) are byte-for-byte equivalent as JSON values
to the source record. Paragraph content and numerical values were not
corrected.

### Repeating header candidate — `doc_003`, page 3

`TATA CAPITAL HOUSING FINANCE LIMITED` is detected at the top edge across 19
pages. It is also title/heading-like content, so it remains in canonical text.
Likewise, repeated footer candidates such as the Fair Practices Code version
and Board approval date in `doc_002` are retained. The candidate and retention
reason are recorded in each applicable page's `cleaning` metadata.

### Hyphenation — `doc_003`, page 12

**Before:** `... at which re-` followed by a line break and `verification of antecedents ...`

**After:** `... at which re-verification of antecedents ...`

The line break was supported by adjacent lines in the same native text block.
The printed hyphen was kept rather than silently changing the lexical form.
For contrast, `time-` followed by `to-time` on `doc_002` page 2 lacked
sufficient same-block evidence and remains split/flagged for review.

### OCR-derived page — `doc_009`, page 48

The native text snapshot is empty, while `ocr.text` begins
`EXPORT-IMPORT BANK OF INDIA / HEAD OFFICE / Centre One Building...`. The
canonical source is the OCR field alone (`selected_source: "ocr"`), not the
merged page `text`. The OCR language and engine/source provenance are copied
into `cleaning.ocr_provenance`; names and contact numbers remain flagged for
verification under the OCR quality audit.

### Table-heavy OCR page — `doc_029`, page 17

OCR text containing values such as `0.00%` and `30.00%` is preserved without
numeric correction or fabricated cells. The source `tables` array remains
unchanged (this page's image-backed tables were not structured by extraction),
and the page is flagged because OCR is selected and its mean confidence is
below 90. Manual comparison with the original remains necessary.

### Standalone page number — `doc_016`, page 2

The raw page text ends with a standalone `2`; the canonical text omits that
edge line. The record's `page_number` remains `2`, and clause numbering and
references in the body remain unchanged.

## Source Selection and Review Flags

- **777 pages** use native text. A reliable native extraction is never
  replaced by OCR, including records that happen to contain OCR metadata.
- **37 pages** use OCR because the separate native snapshot is below the
  extraction threshold. OCR text is not appended to native text.
- **71 pages** are marked `cleaning.needs_manual_review`: all 37 OCR-derived
  pages, plus pages with ambiguous visible-hyphen line breaks (36 such pages,
  with overlap between categories). Five OCR pages also have mean confidence
  below 90; these are a subset of the OCR-derived pages.
- Tables and layout metadata remain available separately for downstream
  review.

## Validation and Tests

- Complete project test suite: **41 passed**.
- Cleaning-specific tests: **14 passed**.
- Compilation: `.venv/bin/python -m compileall -q src tests` passed.
- All 814 raw/cleaned page pairs were checked for identical document ID, page
  number, source filename/hash, raw text, OCR object, blocks, headings, and
  table data.
- All 37 OCR-derived canonical records were checked for source hash, source
  filename, language, and original page-number provenance.
- Idempotency was checked by rerunning the cleaner and comparing cleaned-file
  hashes; repeated processing does not add duplicate text or change output.
- `git diff --check` passed.

## Limitations

1. OCR remains a transcription aid, not authoritative text; the 37 OCR pages
   are explicitly reviewable, and financial/legal details require source
   checking.
2. The current OCR output does not retain per-word positions. Its line breaks
   are therefore not reflowed, and ambiguous visible-hyphen candidates are
   preserved rather than guessed.
3. Some repeated headers/footers remain because the available evidence cannot
   distinguish page furniture from titles, legal notices, and version/date
   metadata with sufficient confidence.
4. Existing image-backed tables remain unstructured OCR text. Table extraction
   quality is unchanged by this milestone.
5. Cleaning is normalization only; it performs no OCR correction, language
   rewriting, chunking, embedding, indexing, search, or answer generation.

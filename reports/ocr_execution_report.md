# Milestone 2B.5B — OCR Execution and Quality Report

## Executive Summary

The targeted OCR run completed for all **37 unique selected pages**: **32 pages
confirmed as scanned/image-only** plus **5 pages with material extraction
gaps**. No target remains failed or blocked. The **11 excluded candidate pages**
(4 blank/nearly blank, 2 sparse-text, and 5 formatting-driven) were not OCRed.
No PDF or manifest metadata was changed.

The final page records contain OCR output, language, Tesseract confidence,
processing duration, source filename/hash, and original PDF page number. Native
text and existing table data remain in place; OCR did not generate table cells.
The output is useful for document discovery, but low-confidence text, Hindi
content, legal citations, contact details, and dense numeric tables require
source verification before they are relied upon.

## Preflight and Target Reconciliation

- Project interpreter: `.venv/bin/python`, Python 3.15.2.
- PyMuPDF: 1.28.2.
- OCR engine: Tesseract 5.5.4, available to the project process.
- Languages verified by `tesseract --list-langs`: `eng` and `hin` (the local
  installation also lists other languages).
- Rendering resolution: 300 DPI.
- Inventory reconciliation: 48 distinct audited candidates; 37 selected and
  11 excluded. The five material-gap pages were checked against the 32
  confirmed image-only pages and did not duplicate those targets.
- Language assignment: 29 `eng`, 7 `eng+hin`, and 1 `hin`. The page-specific
  language selections reflect visual review of bilingual Gazette pages, not
  only the original candidate classification.

## Execution Results

| Measure | Result |
|---|---:|
| Unique OCR targets | 37 |
| Unique target pages with successful OCR output | 37 |
| Unresolved target failures | 0 |
| Excluded pages OCRed | 0 |
| Excluded candidate pages | 11 |
| Successful OCR invocations across initial run and targeted retries | 53 |
| Initial source-resolution failures | 2, both resolved on retry |
| OCR characters in final target outputs | 99,071 |

The two initial failures were source-file resolution errors for `doc_004` pages
1–2, not Tesseract recognition failures. The source resolver was corrected to
use the source filename recorded in the page record and to verify its SHA-256;
both pages subsequently succeeded. Later targeted retries corrected language
selection on visually confirmed bilingual pages and repaired TSV parsing on
nine affected pages. The final OCR error file has no unresolved page errors.

The current inventory marks 28 targets `already_processed` and 9 targets
`processed` by the latest repair batch. This is inventory state, not a count of
successful unique pages: all 37 have successful, validated OCR provenance.
`data/processed/ocr_processing_summary.json` describes the latest nine-page
repair batch (9 succeeded, 39 skipped, 0 failed), rather than the cumulative
run history. The cumulative counts above are reconciled from the execution
history and final page records. The existing `logs/ocr.log` retains an earlier
preflight-blocked entry and is not a cumulative success log; successful
processing is evidenced by the page-level JSONL provenance and the summary
files.

### Language and Confidence

| Language | Unique pages | Result |
|---|---:|---|
| `eng` | 29 | Successful |
| `eng+hin` | 7 | Successful |
| `hin` | 1 | Successful |

Across 37 pages, the mean of per-page mean word-confidence scores is **93.04**
and the median is **94.32**. Page means range from **78.66** to **96.22**. The
lowest individual nonnegative word-confidence score is **0.00**. These are
Tesseract word-confidence measures, not calibrated character accuracy or
probabilities that a page is correct. A high page mean does not rule out a
wrong digit or legal reference.

The sum of the latest stored per-page OCR durations is **57.460 seconds**
(mean **1.553 seconds/page**). The four OCR-producing batches took a combined
**77.533 seconds** of command wall time; that sum includes OCR process overhead
and targeted reprocessing, and excludes visual review, preflight, and
zero-recognition idempotency checks.

## Page-Level Quality Review

All 37 original target pages were visually reviewed against their OCR output.
The five material-gap pages received focused review; representative English,
Hindi/bilingual, legal-text, directory, and table-heavy pages were checked for
reading order, names, dates, numeric values, and obvious omissions. The
page-level assessments and actions are in
[`ocr_page_quality_audit.csv`](./ocr_page_quality_audit.csv).

### Representative comparisons

- **English scanned Gazette, `doc_010` p10 (`eng`):** The output begins with
  the Gazette heading and continues into the provision on lending/investing.
  Printed legal text is discoverable, but exact citations and marginal-heading
  order should be checked when used.
- **`doc_007` p66 (`eng`):** OCR recovered the report heading and text from two
  visible audit tables. The content is not represented as reliable rows and
  columns; numeric alignment and table values require manual comparison.
- **`doc_029` p17 (`eng`):** OCR returned annexure text from two dense percentage
  grids. The page has the lowest mean confidence (78.66); the output is
  unsuitable as a faithful numeric table without manual verification.
- **`doc_009` p48 (`eng`):** The two-column directory is readable, beginning
  with “EXPORT-IMPORT BANK OF INDIA / HEAD OFFICE”. Names, telephone numbers,
  fax numbers, and cross-column order still require checking.
- **`doc_009` p49 (`eng+hin`):** Hindi directory text is present, beginning
  “भारतीय निर्यात-आयात बैंक मुख्यालय”. The OCR emits `HH परेड` where the
  original reads `कफ परेड`, and the fax label is recognized as `tee`; contact
  details require manual verification.
- **`doc_036` p4 (`eng`):** The RBI Governor transmittal letter is recovered.
  The handwritten signature is not recognized, and the Hindi footer is noisy;
  reference/date details should be checked against the page.

Other page-level warnings include a suspicious `3%` token in the date on
`doc_014` p2 and a truncated-looking legal-year fragment (`989`) in the Hindi
OCR on `doc_014` p3. These are flagged for source checking in the CSV; the OCR
text has not been silently corrected.

## Output Integrity and Idempotency

For each of the 37 target records, validation confirmed:

- Exactly one record for each `(doc_id, PDF page number)` target.
- The source PDF exists and its SHA-256 matches the page record.
- OCR provenance carries the same source filename/hash and original page
  number.
- The recorded language matches the reconciled inventory.
- OCR status is successful and the OCR text is non-empty.
- No tab contamination remains from Tesseract TSV output.
- Native extracted text and existing table fields are preserved; OCR text is
  separately identified as OCR-derived.

A safe second-run check used a temporary copy of the inventory and temporary
summary/error paths. It made **0 Tesseract recognition calls**, reported 0
successes, 48 skips (37 existing OCR results plus 11 exclusions), and 0
failures. SHA-256 digests of all affected processed JSONL files were identical
before and after. The production inventory was not used for this check.

## Tests and Validation

- Complete test suite: **27 passed**.
- Python compilation (`.venv/bin/python -m compileall -q src tests`): passed.
- `git diff --check`: passed.
- Output schema, target uniqueness, page number, source hash/provenance,
  language, non-empty OCR, and TSV-contamination checks: passed.
- Idempotency check: passed; no OCR call and no processed-output changes.

## Limitations and Readiness

OCR is ready as a **fallback for discovery and retrieval preparation**, not as
authoritative transcription. Important limitations:

1. Tesseract confidence is not a guarantee of accuracy; numbers, dates,
   percentages, names, and statutory references need source checking.
2. The two table-heavy pages remain unstructured OCR text. No cells or table
   values were fabricated.
3. Hindi mixed-script recognition is usable for discovery but noisy for some
   names, address fragments, and footers.
4. Two-column directories and Gazette marginal headings may not retain exact
   visual reading order.
5. Handwriting and signature marks are not transcribed.
6. OCR output has not been manually corrected. The suspicious date/year and
   other page-level cautions are documented in the audit CSV.

No OCR text cleaning, chunking, embeddings, vector database, search, or answer
generation was started.

## Related Files

- [`ocr_target_inventory.csv`](./ocr_target_inventory.csv)
- [`ocr_page_quality_audit.csv`](./ocr_page_quality_audit.csv)
- [`ocr_processing_summary.csv`](./ocr_processing_summary.csv)
- [`../data/processed/ocr_processing_summary.json`](../data/processed/ocr_processing_summary.json)
- [`../data/processed/ocr_errors.jsonl`](../data/processed/ocr_errors.jsonl)

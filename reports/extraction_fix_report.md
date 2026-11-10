# Milestone 2B.4 — Targeted Extraction Defect Investigation and Fixes

## 1. Executive Summary

The five reported pages were checked against their original PDFs and current page-level JSONL. All five are genuine text-recovery gaps, but none has ordinary selectable text or tables that the current PyMuPDF text/table path can recover:

- `doc_007` p66 and `doc_029` p17 contain table content as embedded images.
- `doc_009` pp48–49 render the directory as vector outlines, with no text blocks or image objects.
- `doc_036` p4 is an image-based letter with no extractable text.

These pages remain flagged for OCR/recovery; no OCR or page-specific workaround was added.

Two other defects were reproducible and fixed:

1. The source PDF text mapping emits BEL (`U+0007`) inside otherwise visible words and labels. The extractor now removes only this known character from extracted spans, block text, and table cells.
2. The heading heuristic treated chart/table-sized text as the page's typical font size, causing body lines to be reported as headings. It now estimates typical size from longer prose blocks, recognizes same-size bold and standalone italic labels, and filters same-size running headers/footers.

The revised heading heuristic changed heading metadata in 23 of the 31 document outputs. Those 23 JSONL files (777 pages total) were regenerated; the other eight outputs were left untouched. Corpus totals remain 31 documents, 814 pages, 766 successfully extracted pages, 48 OCR candidates, and 370 tables. The complete test suite passes.

## 2. Investigation of All Five Material Extraction Gaps

### `doc_007`, page 66 — table extraction gap

- **Original:** Two populated audit-report tables are visible on the page.
- **Before:** The record contained only “Annual Report”, “2024-2025”, and printed page number “286”; 24 non-whitespace characters, no extracted tables, and an OCR-candidate flag.
- **Evidence/root cause:** The PDF page contains 28 image objects and five vector drawings. PyMuPDF's `find_tables()` detects zero tables. The visible table content is image content rather than selectable text or vector table lines.
- **Decision:** Genuine extraction gap, but not fixable by the current text/table extractor. Recovering cell values requires OCR or a separate image-table workflow, neither in scope.
- **After:** Still 0 tables and 24 non-whitespace characters; page remains flagged for OCR. This is an explicitly unresolved issue, not a claimed fix.

### `doc_029`, page 17 — table extraction gap

- **Original:** Two dense annexure tables contain numerical percentage grids.
- **Before:** Only “ANNEXURE - 4” and “ANNEXURE -5” were extractable (24 text characters, 20 non-whitespace); no detected tables, and an OCR-candidate flag.
- **Evidence/root cause:** The page contains three embedded image objects holding the grids. PyMuPDF's table detector finds zero tables because the cell values are in images.
- **Decision:** Genuine extraction gap, not recoverable through the current text/table path. OCR or image-table recovery is required.
- **After:** No table values were recovered; the page remains flagged. Its containing JSONL was regenerated as part of the document's heading-output refresh, but this image-table gap remains unresolved.

### `doc_009`, page 48 — directory extraction gap

- **Original:** A two-column English office directory with addresses and contact details.
- **Before:** No text, blocks, or tables; OCR-candidate flag set.
- **Evidence/root cause:** The rendered page is composed of vector drawing paths (2,821 drawing objects), with no text spans or image objects. The visible letters are outlines, not selectable characters.
- **Decision:** Genuine extraction gap. PyMuPDF text extraction cannot recover outlined glyphs as characters; OCR/vector recognition is needed.
- **After:** The page still has no extracted text or tables and remains flagged. Its containing JSONL was regenerated for heading metadata on other pages, without recovering this directory content.

### `doc_009`, page 49 — directory extraction gap

- **Original:** A two-column Hindi office directory with office names, addresses, and contact details.
- **Before:** No text, blocks, or tables; OCR-candidate flag set.
- **Evidence/root cause:** The page contains 2,733 vector drawing objects and no text spans or image objects. As on page 48, the rendered glyphs are outlines.
- **Decision:** Genuine extraction gap, not fixable through text/table extraction without OCR or vector recognition.
- **After:** The page still has no extracted text or tables and remains flagged. Its containing JSONL was regenerated for heading metadata on other pages, without recovering this directory content.

### `doc_036`, page 4 — letter extraction gap

- **Original:** A legible RBI Governor's transmittal letter with date, addressee, statutory reference, and signature.
- **Before:** No usable text or table; OCR-candidate flag set.
- **Evidence/root cause:** A page-sized embedded image covers the letter. The page has three image objects (the letter page and logos), but no extractable text layer.
- **Decision:** Genuine image-based page; OCR is required. The extraction code correctly did not fabricate text.
- **After:** Still no text or table and remains flagged. The page was regenerated with the rest of `doc_036`; no recovery is claimed.

## 3. Control Character Investigation

The RBI Annual Report's page 41 contains table labels such as “Total Consumption Expenditure”, “Gross Capital Formation”, and “Gross Fixed Capital Formation”. The rendered source labels contain ordinary letters, but PyMuPDF's direct `page.get_text()` and `table.extract()` results include `U+0007` (BEL), for example `E\x07xpenditure` and `Form\x07a\x07tion`. Thus the artifact comes from the PDF's text mapping as exposed by PyMuPDF; it is not visible on the page and was not introduced by JSONL serialization.

The same BEL mapping artifact appeared in output strings on 13 pages of `doc_036` (105 stored string appearances across text, spans, and table fields). The fix removes **only** `U+0007` during extraction. It does not normalize other characters, whitespace, or text. Across regenerated `doc_036.jsonl`, BEL appearances changed from 105 to 0; page 41's GDP table remains present and its numeric alignment is unchanged.

## 4. Heading Detection Findings

### `doc_007`

On pages 5 and 7, prose and section headings share the same 10.08-point size. The section labels use bold spans, but the prior rule required bold text to be at least 1.1 times the page median, so same-size headings such as “Regional Rural Banks (RRB)” and “Industrial Finance-II (IF-II)” were missed. Page 5 had zero detected headings; page 7 detected only “NHB,” and “RBI”.

### `doc_036`

On page 41, narrative text is 11 points while chart and ancillary labels are mostly 6.5 points. The all-page median was 6.5 points, making the 1.25-times size threshold only 8.125 points. As a result, ordinary 11-point paragraph lines were marked as headings; 50 candidates were emitted, including body lines.

### Decision

These were heuristic defects, not evidence that the source layouts were unreadable. The targeted change uses longer prose blocks for the baseline, recognizes same-size bold and standalone italic lines, and excludes same-size style candidates at the page's top/bottom margins and digit-only page numbers. This improves the reported cases but does not constitute a complete heading redesign.

## 5. Root Causes

1. **Image-backed tables/letter:** No selectable text/table structure exists on the source pages.
2. **Outlined directory glyphs:** The glyphs are vector paths, so the PDF has no text spans for extraction.
3. **BEL characters:** A PDF text mapping returns a control character for visible glyphs.
4. **Heading baseline contamination:** A single page-wide font median included small chart/ancillary text, and the previous bold threshold excluded same-size bold headings.

## 6. Code Changes Made

In [src/extract.py](../src/extract.py):

- Added exact BEL removal at extracted text-span, block-text, and table-cell boundaries. No general text cleaning was added.
- Changed heading-size estimation to prefer longer prose text blocks instead of small labels.
- Lowered the same-size bold threshold to the body font size, added a narrowly scoped standalone-italic case, and filtered same-size header/footer candidates and digit-only page numbers.
- Preserved the existing JSONL schema and page/document metadata.

No changes were made to OCR, source PDFs, manifest metadata, chunking, embeddings, vector storage, search, or answer generation.

## 7. Before-and-After Comparisons

| Record | Before | After | Result |
|---|---|---|---|
| `doc_007` p5 headings | 0 | 3 | Detected the three bold section labels; page header/footer excluded. |
| `doc_007` p7 headings | 2 | 5 | Detected the bold “Industrial Finance-II” and “Cybersecurity and FinTech” labels in addition to existing headings. |
| `doc_007` p66 tables / OCR flag | 0 / yes | 0 / yes | Image-based tables remain unresolved and correctly flagged. |
| `doc_036` p41 headings | 50 | 5 | Paragraph lines no longer treated as headings; section labels/markers retained. |
| `doc_036` p41 tables | 1 | 1 | GDP table retained; four BEL characters in its three affected labels removed. |
| `doc_036` BEL appearances across records | 105 | 0 | Exact control-character artifact removed throughout this regenerated PDF. |
| Corpus documents/pages/OCR candidates/tables | 31 / 814 / 48 / 370 | 31 / 814 / 48 / 370 | No counts, page numbers, document IDs, or source metadata changed. |

The affected heading outputs were found by comparing the new extraction result with all existing page records in memory. Only PDFs with changed heading metadata were persisted; other outputs were not rewritten. Regenerated files (page count):

| Processed JSONL | Pages | Processed JSONL | Pages |
|---|---:|---|---:|
| `doc_001.jsonl` | 11 | `doc_019.jsonl` | 3 |
| `doc_002.jsonl` | 6 | `doc_023.jsonl` | 10 |
| `doc_003.jsonl` | 19 | `doc_024.jsonl` | 4 |
| `doc_005.jsonl` | 18 | `doc_025.jsonl` | 8 |
| `doc_006.jsonl` | 68 | `doc_026.jsonl` | 41 |
| `doc_007.jsonl` | 66 | `doc_027.jsonl` | 21 |
| `doc_009.jsonl` | 49 | `doc_028.jsonl` | 17 |
| `doc_016.jsonl` | 9 | `doc_029.jsonl` | 17 |
| `doc_030.jsonl` | 17 | `doc_031.jsonl` | 36 |
| `doc_032.jsonl` | 21 | `doc_033.jsonl` | 10 |
| `doc_034.jsonl` | 11 | `doc_035.jsonl` | 5 |
| `doc_036.jsonl` | 310 |  |  |

The 23 files contain 777 pages total. Metadata fields (`doc_id`, title, source filename/hash, and page number), table-presence status, and OCR-candidate status were checked page-by-page and preserved.

## 8. Regression Tests Added

Four tests were added in [tests/test_extract.py](../tests/test_extract.py):

- Page 41 integration check that extracted output contains no BEL and retains the “Expenditure” table label (skips when the local corpus PDF is absent).
- Exact BEL-only removal check.
- Heading baseline check with small chart labels, a paragraph, and a standalone italic section label.
- Same-size bold heading detection check.

## 9. Test Results

- Pre-change extraction tests: **7 passed**.
- Post-change targeted extraction tests: **11 passed**.
- Post-change complete test suite (`.venv/bin/python -m pytest tests/ -v`): **11 passed**, with six upstream PyMuPDF/Python deprecation warnings.
- Processed corpus validation: 31 JSONL documents, 814 pages, 766 successfully extracted pages, 48 OCR candidates, 370 tables, zero page/table errors, and zero remaining BEL appearances in the corpus outputs.
- Regenerated pages retained sequential 1-based page numbers and unchanged document/source metadata.

## 10. Known Unresolved Limitations

- The five material page gaps remain unresolved without OCR or vector-glyph recognition.
- Image-table recognition can require specialized OCR/layout processing to recover accurate cell values; it is not guaranteed by OCR alone.
- Heading detection remains heuristic. It can still miss headings with unusual typography and may identify some short styled labels that are not semantic section headings.
- The table sample and page review do not establish that all corpus tables or pages are error-free.

## 11. Extraction Readiness Assessment

The targeted fixes are verified, but the corpus is **not yet fully ready for dependable retrieval**. The extractor now avoids the confirmed BEL artifact and produces more reasonable headings on the audited examples. The five content gaps still require OCR or another image/vector recovery method, and complex table/heading behavior remains imperfect. Preserve those pages as explicitly incomplete until their text is recovered or they are excluded from retrieval.

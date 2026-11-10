# Milestone 2B.5 — OCR Implementation and Quality Report

> **Superseded status:** This report records the earlier implementation phase,
> when Tesseract was unavailable and corpus OCR had not run. OCR was later
> executed and validated; use
> [`ocr_execution_report.md`](./ocr_execution_report.md) and
> [`ocr_page_quality_audit.csv`](./ocr_page_quality_audit.csv) for the current
> environment, page results, and quality findings. The historical statements
> below describe the earlier blocked run, not the current OCR status.

## Executive Summary

The targeted OCR pipeline, inventory, and mocked integration tests are implemented. The corpus reconciliation selected **37 unique pages**: all 32 pages previously visually classified as image-only, plus the five material content gaps. The other 11 audited candidates (four blank/nearly blank, two sparse-text, and five formatting-driven) are excluded.

OCR did **not** run on any source page. The current environment has Python 3.14.6 and PyMuPDF 2.1, but no `tesseract` executable. Consequently the engine version and availability of its `eng` and `hin` language data cannot be verified. The run recorded 37 pages blocked by this prerequisite, 11 excluded/skipped, zero OCR attempts, and zero page-processing failures. No source PDF, manifest, or existing extraction JSONL record was modified by the blocked run.

## Validation Methodology

- Read the existing extraction implementation, configuration, JSONL records, candidate audit, previous quality and fix reports, and dependency list before integrating OCR.
- Reconciled the existing 48-row audit with the per-page extraction records. A page is selected only when the audit identifies a confirmed image-only page or a material extraction-quality problem and its current record still needs OCR.
- Checked the five previously reported gaps against the original-page findings recorded in the Milestone 2B.4 report. These remain separate from the 32 confirmed scanned/image-only pages.
- Exercised page targeting, English/Hindi language forwarding, confidence TSV parsing, preservation of native text and tables, error isolation, empty output, and repeat-run behavior with temporary PDFs and a mocked backend.
- Ran the full existing test suite. OCR accuracy comparisons against the originals could not be performed because no OCR engine was available.

## OCR Engine and Prerequisites

The implementation uses the **Tesseract command-line interface** and renders only selected pages through PyMuPDF at **300 DPI**. Tesseract TSV word output provides word-level confidence; the pipeline records the mean, minimum, and count of valid word confidences. This avoids replacing the existing native extractor and does not require the Python `pytesseract` wrapper or Pillow at runtime.

| Environment check | Result |
|---|---|
| Python | 3.14.6 |
| PyMuPDF | 2.1 |
| Tesseract executable | Not found (`tesseract` is not on PATH) |
| Tesseract version | Unavailable |
| `eng` language data | Unverified; engine unavailable |
| `hin` language data | Unverified; engine unavailable |
| Required language codes | `eng`; `hin+eng` for `doc_009`, page 49 |

Install Tesseract and the English and Hindi traineddata using the operating-system package manager or the official Tesseract distribution, then verify both codes with `tesseract --list-langs`. Platform guidance and the invocation command are in [README.md](../README.md). No system software or language pack was installed for this milestone.

## Target Inventory and Processing Results

The generated [ocr_target_inventory.csv](./ocr_target_inventory.csv) contains one row per audited candidate:

| Audit classification | Candidate pages | OCR decision |
|---|---:|---|
| Genuine scanned/image-only page | 32 | Include |
| Extraction-quality problem | 5 | Include |
| Blank or nearly blank page | 4 | Exclude |
| Sparse text page | 2 | Exclude |
| Other / uncertain (formatting-driven) | 5 | Exclude |
| **Total audited** | **48** | **37 selected / 11 excluded** |

The five extraction-quality pages are `doc_007` p66, `doc_029` p17, `doc_009` pp48–49, and `doc_036` p4. They do not overlap with the 32 confirmed scanned pages. `doc_009` p49 uses `hin+eng`; the other 36 selected pages use `eng`.

| Processing outcome | Pages |
|---|---:|
| Successfully OCR-processed | 0 |
| Excluded/skipped from OCR | 11 |
| Blocked because Tesseract is unavailable | 37 |
| OCR-attempt failures | 0 |

The run summary is in [ocr_processing_summary.json](../data/processed/ocr_processing_summary.json); page-level prerequisite records are in [ocr_errors.jsonl](../data/processed/ocr_errors.jsonl), and the CLI warning is in [ocr.log](../logs/ocr.log). The summary distinguishes blocked pages from OCR failures. The 36 English pages and one Hindi-plus-English page are all blocked; neither language was actually exercised on a source page.

## Integration, Provenance, and Idempotency

The new [ocr.py](../src/ocr.py) module reads the existing audit/inventory, opens each matching PDF once, and renders only selected pages. For successful fallback OCR it keeps document ID, filename, source hash, page number, existing blocks, headings, layout, and table structures. It preserves prior native text in `native_text`, records recognized text and confidence under `ocr`, and makes the combined fallback text available in the existing `text` field. Native text is not replaced when its page record no longer needs OCR, and OCR is never converted into table cells.

A repeated run skips a record already marked with successful OCR unless `--force` is given. Failed or empty pages remain retryable and are separately recorded. Synthetic integration tests confirmed one successful page was not duplicated on a second run and that a failed page did not stop a later page. Corpus-level idempotency could not be exercised without Tesseract.

## Requested Source-Page Checks

Prior to OCR, these are the actual extracted-record contents and the prior visual audit findings. Since no engine was available, the “OCR result” is **not available** for every row; no accuracy claim is made.

| Page | Source-page finding from prior visual audit | Existing extracted text | OCR comparison |
|---|---|---|---|
| `doc_010` p10 (representative English scan) | Previously classified as a rasterized image-only page. | No usable text. | Not run; recognition, names, values, and confidence unverified. |
| `doc_007` p66 | Two dense image-backed tables. | `Annual Report`, `2024-2025`, and printed page `286`; no structured tables. | Not run; numeric recovery and alignment unverified. |
| `doc_029` p17 | Two dense annexure tables embedded as images. | Only `ANNEXURE - 4` and `ANNEXURE -5`; no structured tables. | Not run; values and cell alignment unverified. |
| `doc_009` p48 | English directory rendered as vector outlines. | Empty text and no text blocks or tables. | Not run; names and contact details unverified. |
| `doc_009` p49 | Hindi directory rendered as vector outlines. | Empty text and no text blocks or tables. | Not run; Hindi recognition unverified. |
| `doc_036` p4 | Image-based RBI transmittal letter. | Empty text and no tables. | Not run; date, addressee, statutory reference, and signature text unverified. |

The scan and material-gap descriptions above are the findings documented in [extraction_quality_report.md](./extraction_quality_report.md) and [extraction_fix_report.md](./extraction_fix_report.md); they are not new OCR observations.

## Confidence and Limitations

- The TSV parser calculates confidence only for recognized words with valid, non-negative confidence values. No corpus confidence values exist because no page was processed.
- The mock test verifies TSV confidence parsing, not Tesseract recognition quality or any source-page numerical value.
- OCR text does not include word-position blocks in this milestone; existing native positional blocks remain unchanged.
- Image-backed tables may yield OCR text but not reliable row/column structure. Their table fields remain untouched and must not be interpreted as recovered cells.
- The five formatting-driven candidates and blank/sparse candidates remain excluded according to the completed audit. Their statuses are explicit in the inventory.
- A quality review against originals, including Hindi quality, dates, names, numerical values, and OCR confidence, remains mandatory after the engine and both language datasets are installed.

## Tests and Readiness Assessment

- `python -m pytest tests/test_ocr.py -q`: **11 passed**.
- `python -m compileall -q src/ocr.py src/config.py`: **passed**.
- `python -m pytest tests/ -q`: **21 passed, 1 failed**. The failing pre-existing test is `test_detects_tables_and_preserves_structured_cells` in `tests/test_extract.py`; on the active PyMuPDF 2.1 environment it expects `Loan Policy One` but receives `LoanPolicyOne` from table extraction. The OCR changes do not modify that extractor or its test, and no unrelated table normalization was introduced.
- OCR command: correctly returned blocked status (exit code 2), with 37 pages blocked and no source-page attempts.

**Assessment:** The implementation and mocked integration behavior are ready for a real OCR run once Tesseract and both language packs are installed. This milestone is not complete as a corpus OCR/quality-validation run: zero source pages were OCR-processed, the five gaps remain unresolved, and the full test suite has the noted existing table-spacing failure.

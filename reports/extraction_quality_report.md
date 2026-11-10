# Extraction Quality Report

## 1. Executive Summary

The existing extraction run covers 31 PDFs and 814 PDF pages. Its summary reports 766 pages successfully extracted, 48 OCR candidates, 370 extracted tables, and zero recorded document/page failures. The 48 candidates were reviewed against the original PDF pages:

| Classification | Pages | Share of candidates |
|---|---:|---:|
| Genuine scanned/image-only page | 32 | 66.7% |
| Blank or nearly blank page | 4 | 8.3% |
| Sparse text page | 2 | 4.2% |
| Extraction-quality problem | 5 | 10.4% |
| Other / uncertain (formatting-driven threshold flag) | 5 | 10.4% |
| **Total** | **48** | **100%** |

Twelve extracted tables from twelve different PDFs were compared with their source pages: 4 were Good (33.3%), 8 Acceptable (66.7%), and 0 Poor. This is a representative sample of 12/370 tables (3.2%), not a quality certification of every table.

**Assessment:** Page-level records, page numbering, and ordinary text extraction provide a useful base, but the corpus is not yet ready for dependable retrieval. Scanned pages and five material extraction gaps need later OCR or targeted recovery. Complex forms remain layout-sensitive, and one table contains a confirmed control-character artifact.

## 2. Validation Methodology

- Reviewed the existing extractor/configuration, extraction summary, logs, and per-document JSONL records. The existing schema includes document ID, source filename, 1-based PDF page number, text, positioned blocks, headings, tables, OCR-candidate status/reason, layout metadata, text-quality metrics, and page/table errors.
- Reconciled all 48 `needs_ocr` records against the original PDF pages. Every candidate was visually reviewed in rendered-page contact sheets; ambiguous or material cases were inspected at higher resolution.
- The candidate audit's “extracted character count” is the extractor's **non-whitespace character count**, and the ratio is the stored alphanumeric ratio.
- Compared 12 tables from 12 PDFs with rendered original pages and their corresponding extracted table cells, dimensions, and headers. The sample prioritizes lending values, financial schedules, complex forms, and irregular layouts.
- Reviewed layout and reading order on `doc_007` pages 5, 7, and 66; `doc_036` pages 30, 31, and 41; table-heavy `doc_006` page 41; normal text-native `doc_001` page 2; and scanned `doc_010` page 10.
- No source PDF, processed JSONL, manifest, or extraction code was modified.

## 3. OCR Candidate Audit

The page-level classifications and recommended actions are recorded in [ocr_candidate_audit.csv](./ocr_candidate_audit.csv).

**Confirmed findings**

- **32 genuine scanned/image-only pages (66.7%)** have no meaningful extractable text layer and need OCR in a later milestone.
- **4 blank/nearly blank pages (8.3%)** do not need OCR: `doc_031` p36 and `doc_036` pp3, 5, and 25.
- **2 sparse pages (4.2%)** are the `doc_036` front and back covers; their artwork contains little text and should not be treated as body content.
- **5 formatting-driven candidates (10.4%)** contain legible contents/directory text: `doc_026` p14 and `doc_036` pp7–10. Dot leaders and page-number formatting depress their alphanumeric ratios, despite useful extracted text. These are threshold false positives for OCR.
- **5 extraction-quality problems (10.4%)** warrant targeted recovery:
  - `doc_007` p66: two visible data tables, but only 24 non-whitespace characters were extracted.
  - `doc_009` pp48–49: visible directory pages with no usable extracted text.
  - `doc_029` p17: two dense annexure tables are visible, but only sparse labels were retained.
  - `doc_036` p4: a visible transmittal letter has no usable extracted text.

The original threshold remains a candidate detector, not a scan classifier: it flags fewer than 30 non-whitespace characters **or** an alphanumeric ratio below 0.35. This audit confirms that the threshold also flags blank pages, sparse covers, and contents pages dominated by dot leaders.

## 4. Table Extraction Quality

The full sample and per-table observations are in [table_quality_audit.csv](./table_quality_audit.csv).

| Overall quality | Tables | Share of sample |
|---|---:|---:|
| Good | 4 | 33.3% |
| Acceptable | 8 | 66.7% |
| Poor | 0 | 0% |

The Good samples (`doc_007` p19, `doc_016` p7, `doc_019` p2, and `doc_034` p5) preserve the reviewed row/column relationships. The Acceptable samples are primarily merged-cell policy forms, grievance matrices, and multirow financial headers. Their content is generally represented, but flattened cell grids do not fully express the source geometry; blank fields on sample forms are intentional and were not treated as missing values.

On `doc_036` p41, the GDP growth table's year/value alignment is retained, but the extracted label “Total Consumption Expenditure” contains an unexpected control character (`E\x07xpenditure`), while the rendered source label is normal. This is a confirmed text artifact; no numeric value loss was observed in the sampled rows.

## 5. Reading Order and Layout Validation

**Confirmed findings**

- `doc_007` pp5 and 7 are visually two-column pages. The output declares two columns and `left_column_then_right_column`; the reviewed text follows the left column before the right, rather than alternating across columns.
- `doc_036` pp30–31 are also genuine two-column pages. Their text proceeds column by column, and section markers `I.16`–`I.20` and `I.21`–`I.25` are retained in sequence.
- `doc_001` p2 is a normal text-native index page. Its entries and referenced page numbers are retained in reading order, with positioned blocks.
- `doc_006` p41 is a table-heavy Gazette page. Four table objects are represented separately from ordinary page text; visual comparison shows the principal schedules and their grouped headers. Most amount cells are blank in the source template.
- `doc_036` p41 keeps the GDP table as a separate table object beside narrative text and charts. Its section marker and printed page information are retained.
- `doc_010` p10 is visibly image-only and has no extracted text; it is correctly marked as needing OCR.

**Issues observed**

- On `doc_007` p5, visually prominent section labels were not detected as headings. On p7, heading detection returned only a small subset of visible section labels. Heading detection is therefore inconsistent even when body-text reading order is reasonable.
- On `doc_036` p41, the heading list includes fragmented paragraph/chart text as heading candidates. Heading metadata should not be treated as authoritative without later evaluation.
- `doc_007` p66 demonstrates that table/layout content may be visually clear but absent from the extracted text/table representation.

## 6. Issues Identified

1. **OCR dependency:** 32 confirmed image-only pages have no text layer; they require OCR for text retrieval.
2. **Material page gaps:** Five pages have visible, retrieval-relevant content that is absent or severely incomplete in the current extraction.
3. **Candidate-threshold false positives:** 11 candidates (4 blank, 2 sparse, 5 formatting-driven) do not call for OCR as classified here.
4. **Table geometry:** Eight of the 12 sampled tables are Acceptable rather than Good, chiefly because merged or spanning cells are represented as sparse rectangular grids.
5. **Text artifact:** A control character appears in a table label on `doc_036` p41.
6. **Heading metadata:** Heading detection both misses visible headings and over-identifies some non-heading text.
7. **Error counts are not quality guarantees:** The recorded zero page/document failures means no exception was logged; it does not mean every visible page element was extracted.

## 7. Recommended Fixes

- In the OCR milestone, prioritize the 32 confirmed image-only pages and the five material extraction-quality pages; keep OCR explicitly separate from the current text extraction.
- Do not OCR the 11 blank, sparse, or formatting-driven pages solely because they crossed the current threshold. Retain their metadata or existing readable text as appropriate.
- Preserve table geometry and merged-cell context for the complex forms; avoid interpreting empty sample-form cells as missing source values.
- Normalize or reject control characters in a later text-cleaning stage, after preserving the original extraction as evidence.
- Evaluate heading detection separately before relying on headings for retrieval segmentation.
- Expand table review beyond this 12-table sample before making corpus-wide table quality claims.

These are recommendations for later milestones; no OCR, cleaning, chunking, embeddings, vector database, search, or answer generation was implemented here.

## 8. Extraction Readiness Assessment

**Conditionally useful, not retrieval-ready.** The current JSONL records preserve page identity, positioned text blocks, layout metadata, and separate table objects. The reviewed two-column pages show a sensible column order, and the sample's standard tables retain useful data.

However, 32 image-only pages remain unreadable without OCR, five other pages have material extraction gaps, and complex table/heading metadata has known limitations. These issues must be addressed or explicitly excluded before dependable retrieval is built on the corpus.

## 9. Limitations

- The table audit covers 12 selected tables, not all 370 extracted tables; results should not be generalized to the entire inventory.
- Visual comparison is a quality sample, not exhaustive cell-by-cell verification of every extracted table value in the corpus.
- This audit classifies OCR candidates and identifies pages for later recovery; it does not perform OCR or confirm the exact text that OCR would produce.
- No extraction code was changed, so the existing test suite was not rerun for this audit. The earlier extraction milestone reported seven passing tests; that prior result is not a new test run for this report.

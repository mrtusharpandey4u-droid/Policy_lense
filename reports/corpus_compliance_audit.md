# PolicyLens Corpus Compliance Audit

**Audit date:** 2026-11-09  
**PDF library:** PyMuPDF 2.1  
**Scope:** All 31 PDF files present in `data/pdfs/`. The five manifest entries with `pending` status and no local PDF were not counted or modified.

## Executive result

The corpus contains 31 PDFs, and all 31 opened successfully. Their page counts were compared with the manifest, and their SHA-256 values were checked. Rechecking all 30 original PDFs confirmed their recorded page counts and hashes. One official RBI Annual Report (2023-24) was added as `doc_036`; it has 310 pages, contains meaningful tables, and has a visually verified genuine two-column text layout.

The corpus now meets the total-document, long-document, and two-column targets:

| Requirement from the original assignment | Target | Verified result | Status |
|---|---:|---:|---|
| Total PDFs | 30–50 | 31 | Meets |
| Text-native | ~60% (about 19) | 25/31 (80.6%) | Above target by 6 documents |
| Scanned / OCR-needed | ~20% (about 6) | 6/31 (19.4%) | Meets target |
| Table-bearing | ~20% (about 6) | 12/31 (38.7%) | Above target by 6 documents |
| Longer than 50 pages | At least 3 | 3 | Meets |
| Two-column layouts | At least 2 | 2 | Meets |

Table-bearing is a feature that can overlap with text-native PDFs, not a mutually exclusive extraction type. Counts therefore should not be summed. The 60/20/20 proportions do not match as measured: the corpus is text-native-heavy, scanned is on target, and meaningful tables are more prevalent than the target.

## Page-count and classification inventory

“Text-native” means the document has a usable selectable text layer; documents with a small number of image-only pages remain text-native overall. “Scanned” means no selectable text was present across the PDF. Table and column flags indicate substantive tables and a genuine two-column text layout, respectively; small revision/contents tables and ordinary table cells are not counted as two-column layouts.

| Doc ID | PDF filename | Pages | Type | Meaningful tables | Two-column |
|---|---|---:|---|---|---|
| doc_001 | `bfl_fair_practice_code.pdf` | 11 | Text-native | No | No |
| doc_002 | `tccl_fair_practice_code.pdf` | 6 | Text-native | No | No |
| doc_003 | `tchfl_fair_practices_code.pdf` | 19 | Text-native | No | No |
| doc_004 | `dfs_banking_gazette_2022.pdf` | 2 | Scanned | No | No |
| doc_005 | `lic_jeevan_tarun_policy_doc.pdf` | 18 | Text-native | Yes | No |
| doc_006 | `doc_006_nabfid_general_amendment_rules_2022.pdf` | 68 | Text-native | Yes | No |
| doc_007 | `doc_007_department_of_financial_services_an.pdf` | 66 | Text-native | Yes | Yes |
| doc_009 | `doc_009_export_import_bank_of_india_act_198.pdf` | 49 | Text-native | No | No |
| doc_010 | `doc_010_national_bank_for_financing_infrast.pdf` | 22 | Scanned | No | No |
| doc_011 | `doc_011_financial_services_institutions_bur.pdf` | 2 | Scanned | No | No |
| doc_012 | `doc_012_gazetted_notification_appointment_o.pdf` | 1 | Scanned | No | No |
| doc_014 | `doc_014_notification_on_debts_recovery_trib.pdf` | 3 | Scanned | No | No |
| doc_015 | `doc_015_vigilance_clearance_and_public_sect.pdf` | 2 | Scanned | No | No |
| doc_016 | `doc_016_fair_practice_code_2023.pdf` | 9 | Text-native | Yes | No |
| doc_017 | `doc_017_fair_practice_code_policy.pdf` | 4 | Text-native | No | No |
| doc_019 | `doc_019_policy_for_determining_interest_rat.pdf` | 3 | Text-native | Yes | No |
| doc_022 | `doc_022_know_your_customer_guidelines.pdf` | 1 | Text-native | No | No |
| doc_023 | `doc_023_merged_customer_service_and_grievan.pdf` | 10 | Text-native | Yes | No |
| doc_024 | `doc_024_fair_practices_code_for_microfinanc.pdf` | 4 | Text-native | No | No |
| doc_025 | `doc_025_grievance_redressal_policy.pdf` | 8 | Text-native | Yes | No |
| doc_026 | `doc_026_internal_corporate_governance_guide.pdf` | 41 | Text-native | No | No |
| doc_027 | `doc_027_sample_policy_document_lic_new_jeev.pdf` | 21 | Text-native | Yes | No |
| doc_028 | `doc_028_policy_document_lic_digi_term_uin_5.pdf` | 17 | Text-native | Yes | No |
| doc_029 | `doc_029_final_policy_document_lic_new_endow.pdf` | 17 | Text-native | Yes | No |
| doc_030 | `doc_030_payment_and_settlement_systems_act_.pdf` | 17 | Text-native | No | No |
| doc_031 | `doc_031_insurance_regulatory_and_developmen.pdf` | 36 | Text-native | No | No |
| doc_032 | `doc_032_general_insurance_business_national.pdf` | 21 | Text-native | No | No |
| doc_033 | `doc_033_bankers_books_evidence_act_1891_as_.pdf` | 10 | Text-native | No | No |
| doc_034 | `doc_034_guidelines_for_promotion_and_incent.pdf` | 11 | Text-native | Yes | No |
| doc_035 | `doc_035_accessibility_standards_and_guideli.pdf` | 5 | Text-native | No | No |
| doc_036 | `doc_036_rbi_annual_report_2023_24.pdf` | 310 | Text-native | Yes | Yes |

## Documents with meaningful tables

The following 12 documents contain substantive data tables, schedules, or structured forms. Representative page evidence from visual review:

| Doc ID | Evidence |
|---|---|
| doc_005 | LIC Jeevan Tarun policy schedule/form, p. 4 |
| doc_006 | Financial statement schedules and structured forms, pp. 2, 41, 45, 48, 51, 64 |
| doc_007 | Annual-report financial figures and review tables, p. 19 |
| doc_016 | Grievance/contact-level matrix, p. 7 |
| doc_019 | Interest-rate comparison table, p. 2 |
| doc_023 | Customer-service process / service-level table, p. 3 |
| doc_025 | Grievance-service process table, p. 3 |
| doc_027 | LIC New Jeevan Shanti policy schedule, p. 4 |
| doc_028 | LIC Digi Term policy schedule, p. 4 |
| doc_029 | LIC New Endowment policy schedule, p. 4 |
| doc_034 | RuPay/BHIM-UPI incentive claim tables, p. 5 |
| doc_036 | Real GDP growth and macroeconomic indicator tables, e.g. Table II.2.1, PDF p. 41 |

Automated table detection was used to find candidate pages, and representative candidates were visually reviewed. Contents lists, revision-history blocks, and prose mistakenly split into cells by automated detection were not counted as meaningful tables.

## Long documents and column layouts

Three PDFs exceed 50 pages:

- `doc_006` — 68 pages.
- `doc_007` — 66 pages.
- `doc_036` — 310 pages.

`doc_009` has 49 pages, so it does not meet the “more than 50 pages” threshold.

Two PDFs were verified to have genuine two-column text layouts: `doc_007` (visibly present on PDF pp. 5–7) and `doc_036` (visibly present on PDF pp. 30–34 and 39–40, among others). In the RBI report, prose flows independently down left and right columns; table/chart layouts were not used as column evidence. The review re-opened every original PDF, checked all page counts and hashes, and screened page text-block geometry for possible columns. Visual review of candidate pages in `doc_005`, `doc_006`, `doc_027`–`doc_029`, and `doc_034` confirmed that their apparent columns are policy forms or table cells, not two-column prose. `doc_004` is a scanned bilingual gazette, but its Hindi and English sections are arranged sequentially rather than as side-by-side text columns; it does not count.

## Method and manifest updates

- Opened all 31 local PDFs with PyMuPDF 2.1 and checked page counts; reviewed selectable text page by page.
- Used page text, image presence, and table-detection results to identify scan and table candidates; visually reviewed representative candidate pages and suspected column layouts, including the newly added report.
- Rechecked all 30 original PDFs and confirmed that their page counts and hashes match the manifest. Verified `doc_036` at 310 pages, with SHA-256 `9a1c7e0266e0ce578ca5055b25c06808e0ff57283efb1912e88d1fd9da84c925`.
- Added `doc_036` from the official Reserve Bank of India annual report archive (publication date 2024-05-30): [official PDF](https://rbidocs.rbi.org.in/rdocs/AnnualReport/PDFs/0ANNUALREPORT202324_FULLDF549205FA214F62A2441C5320D64A29.PDF).
- Preserved existing manifest metadata and fields, and added `has_meaningful_tables` and `has_two_column_layout`. These fields are blank for pending manifest records without a local PDF.
- No OCR, chunking, embeddings, or vector database work was performed.

# PolicyLens — Corpus Collection Report (Milestone 2A: Pilot Ingestion)

> **Document Research & Data Engineering Specialist Report**  
> **Status:** Completed & Verified  
> **Scope:** Pilot collection of 5 authentic, publicly available financial/lending/insurance regulatory policy documents.

---

## 1. Executive Summary

In Milestone 2A, we identified, downloaded, verified, and registered a pilot set of 5 official regulatory policy documents spanning the lending, housing finance, banking regulation, and life insurance sectors in India.

The documents were sourced exclusively from verified official government repositories (Ministry of Finance Department of Financial Services), premier statutory financial institutions (Life Insurance Corporation of India), and major systemic public Non-Banking Financial Companies (Bajaj Finance Limited, Tata Capital Limited, and Tata Capital Housing Finance Limited).

No placeholder files, simulated data, or unverified secondary aggregators were used. Every document was downloaded, byte-verified (`%PDF` header), opened and parsed with PDF tooling, and cataloged with a SHA-256 cryptographic checksum.

---

## 2. Document Inventory & Detailed Profiles

### Document 1: `doc_001`
- **Document Title:** Fair Practice Code (Version 7.1)
- **Issuer:** Bajaj Finance Limited (BFL)
- **Official Source URL:** [https://cms-assets.bajajfinserv.in/is/content/bajajfinance/fair-practice-code-ver-7-1-jan-2026-english?scl=1&fmt=pdf](https://cms-assets.bajajfinserv.in/is/content/bajajfinance/fair-practice-code-ver-7-1-jan-2026-english?scl=1&fmt=pdf)
- **Local Filename:** `data/pdfs/bfl_fair_practice_code.pdf`
- **Issue / Approval Date:** January 2026 (Version 7.1)
- **Page Count:** 11
- **File Size:** 280,778 bytes (~274 KB)
- **SHA-256 Hash:** `7651c9ebdfdd9da0217180eeb0081211c2b7ab6ce1b6f08476555b1fe606950f`
- **Document Type:** Text-native (27,682 extracted characters, ~2,516 chars/page)
- **Table Presence:** Yes. Contains structured turnaround time tables, grievance redressal hierarchy, and escalation matrices.
- **Two-Column Layout Presence:** No (single-column structured document).
- **Download Verification Status:** Verified. Magic bytes `%PDF-1.3`, parsed without errors.
- **Source Reliability & Sharing:** Highly reliable. Statutory disclosure required under RBI Master Directions on Fair Practices Code for NBFCs, publicly hosted on Bajaj Finserv's official CDN.

---

### Document 2: `doc_002`
- **Document Title:** Fair Practices Code (Version 3.0)
- **Issuer:** Tata Cleantech Capital Limited (TCCL / Tata Capital)
- **Official Source URL:** [https://www.tatacapital.com/content/dam/tata-capital/tccl/Fair%20Practice%20Code.pdf](https://www.tatacapital.com/content/dam/tata-capital/tccl/Fair%20Practice%20Code.pdf)
- **Local Filename:** `data/pdfs/tccl_fair_practice_code.pdf`
- **Issue / Approval Date:** 2023-01-19 (Board approval date)
- **Page Count:** 6
- **File Size:** 253,232 bytes (~247 KB)
- **SHA-256 Hash:** `d9d84cad49fe834317ab948949180b33a94a87d7fcbb2e8ef484e53efa2e6a9a`
- **Document Type:** Text-native (13,453 extracted characters, ~2,242 chars/page)
- **Table Presence:** Yes. Includes structured contact details for Principal Nodal Officers, Grievance Redressal Officers, and RBI Ombudsman escalation stages.
- **Two-Column Layout Presence:** No (single-column layout).
- **Download Verification Status:** Verified. Magic bytes `%PDF-1.5`, parsed without errors.
- **Source Reliability & Sharing:** Highly reliable. Official regulatory policy document published on Tata Capital's compliance portal under RBI directives.

---

### Document 3: `doc_003`
- **Document Title:** Fair Practices Code (Version 3.0)
- **Issuer:** Tata Capital Housing Finance Limited (TCHFL)
- **Official Source URL:** [https://www.tatacapital.com/content/dam/tata-capital/tchfl/fpc/Fair%20Practices%20Code-English.pdf](https://www.tatacapital.com/content/dam/tata-capital/tchfl/fpc/Fair%20Practices%20Code-English.pdf)
- **Local Filename:** `data/pdfs/tchfl_fair_practices_code.pdf`
- **Issue / Approval Date:** 2026-01-19 (Current Revision Date, Version 3.0)
- **Page Count:** 19
- **File Size:** 322,534 bytes (~315 KB)
- **SHA-256 Hash:** `71954c69a0d091f985148771b92d02ea8330581e16b114eee9668c7a7b9bedcf`
- **Document Type:** Text-native (53,790 extracted characters, ~2,831 chars/page)
- **Table Presence:** Yes (Heavy). Multiple comprehensive tables detailing loan application processing stages, turnaround times (TAT), grievance redressal levels (GRO, Chief Grievance Redressal Officer, National Housing Bank / RBI Ombudsman), and fees/charges disclosures.
- **Two-Column Layout Presence:** No (single-column structured sections).
- **Download Verification Status:** Verified. Magic bytes `%PDF-1.6`, parsed cleanly.
- **Source Reliability & Sharing:** Highly reliable. Formal regulatory code under National Housing Bank (NHB) and RBI guidelines for Housing Finance Companies (HFCs).

---

### Document 4: `doc_004`
- **Document Title:** Notification under Section 53(1) of Banking Regulation Act 1949
- **Issuer:** Department of Financial Services, Ministry of Finance, Government of India
- **Official Source URL:** [https://financialservices.gov.in/sites/default/files/order-notices/Gazette.pdf](https://financialservices.gov.in/sites/default/files/order-notices/Gazette.pdf)
- **Local Filename:** `data/pdfs/dfs_banking_gazette_2022.pdf`
- **Issue / Approval Date:** 2022-05-27
- **Page Count:** 2
- **File Size:** 597,120 bytes (~583 KB)
- **SHA-256 Hash:** `a640feb146831a6e8c74786fb5b3f3d02111ae6c571106e676274b4ff1fa7ebd`
- **Document Type:** Scanned PDF (0 selectable/extractable text characters across both pages).
- **Table Presence:** No.
- **Two-Column Layout Presence:** Yes. Official bilingual gazette format with side-by-side or dual-block structure (Hindi on one segment, English on the other), published as an official printed scanned page.
- **Download Verification Status:** Verified. Magic bytes `%PDF-1.4`. Confirmed to contain 2 full-page scanned raster images (1653 x 2338 pixels each, 8-bit grayscale) embedded in the PDF stream. Ideal benchmark for Tesseract OCR pipeline testing.
- **Source Reliability & Sharing:** Official Government Gazette document published on the Central Government Department of Financial Services portal (`financialservices.gov.in`). Public record under Government of India open publishing.

---

### Document 5: `doc_005`
- **Document Title:** LIC's Jeevan Tarun Policy Document (UIN 512N299V02)
- **Issuer:** Life Insurance Corporation of India (LIC)
- **Official Source URL:** [https://licindia.in/documents/20121/106020/Final-Policy-doc-LIC-s-Jeevan-Tarun.pdf/580b8637-a8c4-4be2-a067-1c16f8f1a732?t=1681125305022](https://licindia.in/documents/20121/106020/Final-Policy-doc-LIC-s-Jeevan-Tarun.pdf/580b8637-a8c4-4be2-a067-1c16f8f1a732?t=1681125305022)
- **Local Filename:** `data/pdfs/lic_jeevan_tarun_policy_doc.pdf`
- **Issue / Approval Date:** 2023-04-10
- **Page Count:** 18
- **File Size:** 219,821 bytes (~215 KB)
- **SHA-256 Hash:** `1b05f8fb587452e5cf70d763406f990650a3100a99b1ee9cca4bbf855a0e7cce`
- **Document Type:** Text-native (72,282 extracted characters, ~4,015 chars/page)
- **Table Presence:** Yes. Multiple structured schedules, benefit option tables (survival benefit percentages), guaranteed surrender value factor tables, and statutory grievance escalation matrices.
- **Two-Column Layout Presence:** No (standard multi-part structured contract document divided into Parts A through G).
- **Download Verification Status:** Verified. Magic bytes `%PDF-1.3`, parsed cleanly.
- **Source Reliability & Sharing:** Highly reliable. Formal statutory policy conditions document published by India's largest public insurer (LIC) under IRDAI Product Regulations.

---

## 3. Pilot Corpus Characteristics & Requirement Alignment

| Criterion | Target Requirement (Full Corpus) | Pilot Status (Milestone 2A) | Validation Notes |
|---|---|---|---|
| **Total Documents** | 30–50 documents | **5 documents** | Pilot stage complete |
| **Text-Native PDFs** | ~60% | **4 documents (80%)** | `doc_001`, `doc_002`, `doc_003`, `doc_005` |
| **Scanned PDFs** | ~20% | **1 document (20%)** | `doc_004` (0 text layer, 100% scanned raster) |
| **Table Presence** | ~20% containing important tables | **4 documents (80%)** | `doc_001`, `doc_002`, `doc_003`, `doc_005` have tables |
| **Two-Column / Complex Layout** | At least 2 two-column PDFs | **1 document (20%)** | `doc_004` (official gazette format) |
| **Long / Multi-Section PDF** | Multi-page complex documents | **`doc_003` (19 pgs), `doc_005` (18 pgs)** | Substantial legal/contractual documents |
| **Public Sharing Reliability** | Official, public domain or statutory disclosures | **100% compliant** | Sourced directly from official regulatory portals |

---

## 4. Observations & Recommendations for Milestone 2B (Expansion to 30–50 PDFs)

1. **WAF & CDN Handling:**  
   Some Indian central regulatory endpoints (such as `rbi.org.in` notifications and `irdai.gov.in`) employ web application firewalls that return session challenge pages for automated CLI requests. In contrast:
   - Public NBFCs (Bajaj Finance, Tata Capital, Muthoot, HDBFS, L&T Finance) host static, clean PDFs on standard enterprise CDNs (`cms-assets.bajajfinserv.in`, `tatacapital.com/content/dam/`).
   - Public financial institutions (LIC, SIDBI, NABARD, NHB) and Ministry of Finance portals (`financialservices.gov.in`) reliably host direct static PDFs.
   - For expanding to 30–50 PDFs, the automated ingestion script (`ingest.py`) should use browser-like headers (`User-Agent`, `Accept: application/pdf`, redirect following, and retry logic with timeouts).

2. **Deduplication:**  
   SHA-256 calculation for each file is now confirmed and recorded in `manifest.csv`. Re-running ingestion in subsequent milestones will check `source_hash` to ensure zero duplicates are added.

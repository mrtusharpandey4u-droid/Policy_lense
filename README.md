# PolicyLens

> **Case Study 2 — Applied LLM Engineering Assignment**
>
> A retrieval-focused policy-document search system built on sentence-transformer embeddings and ChromaDB.

---

## What is PolicyLens?

PolicyLens ingests publicly available policy PDF documents, chunks them into semantically meaningful passages, embeds each passage with a sentence-transformer model, and stores them in a local ChromaDB vector database.

Given a free-text question, PolicyLens retrieves the most relevant passages and reports which document and page they came from — enabling analysts, researchers, and citizens to quickly locate specific policy provisions without reading entire documents.

---

## The Problem it Solves

Policy documents are:

- **Long** — budgets, legislation, and regulatory frameworks routinely exceed 100 pages.
- **Dense** — relevant answers are buried in subsections and appendices.
- **Heterogeneous** — some are text-native PDFs, others are scanned images, and many contain complex tables.

Keyword search misses paraphrase matches. Reading everything manually is impractical. PolicyLens bridges the gap with semantic retrieval.

---

## Folder Structure

```
CS2_PolicyLens/
├── src/                # Pipeline source code
│   ├── __init__.py     # Package initialisation
│   ├── config.py       # Centralised, env-driven settings
│   ├── ingest.py       # PDF download, hashing, manifest management
│   ├── extract.py      # Text and table extraction (PyMuPDF + Tesseract)
│   ├── chunking.py     # Fixed-size and structure-aware chunking
│   ├── embeddings.py   # Sentence-transformer encoding helpers
│   ├── search.py       # ChromaDB indexing and retrieval
│   └── evaluate.py     # Recall@k and MRR evaluation
│
├── data/
│   ├── pdfs/           # Raw downloaded PDFs (git-ignored)
│   ├── processed/      # Extracted page-level JSON files (git-ignored)
│   └── manifest.csv    # Document registry (doc_id, url, hash, status, …)
│
├── eval/
│   └── questions.csv   # Hand-labelled evaluation questions with gold answers
│
├── logs/               # Runtime logs (git-ignored)
├── vector_store/       # ChromaDB persistent storage (git-ignored)
├── reports/            # Evaluation metric reports (git-ignored)
├── tests/              # pytest test suite
│
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template (copy → .env)
└── .gitignore
```

---

## Planned Technology Stack

| Concern | Library / Tool | Notes |
|---|---|---|
| PDF text extraction | PyMuPDF (`fitz`) | Fast, accurate for text-native PDFs |
| OCR for scanned pages | Tesseract + `pytesseract` | Handles image-only pages |
| Embeddings | `sentence-transformers` | Default: `all-MiniLM-L6-v2` |
| Vector store | ChromaDB | Local persistent storage |
| Data manipulation | Pandas | Manifest and question-set management |
| Testing | pytest | Unit and integration tests |
| Config | `python-dotenv` | Secrets and tunable parameters in `.env` |

> **Modular design:** every technology is isolated behind a single module in `src/`. Swapping a component (e.g. replacing ChromaDB with FAISS) requires changes only in the relevant module, not across the codebase.

---

## Planned Document Corpus Requirements

- **30–50** publicly shareable policy PDFs
- **~60 %** text-native, **~20 %** scanned (OCR), **~20 %** table-heavy
- **At least 3** PDFs longer than 50 pages
- **At least 2** two-column layout PDFs
- Document types: government policy, legislation, regulatory frameworks, international agreements

---

## Planned Chunking Requirements

- Chunk size: **300–800 tokens**
- **Strategy A — Fixed-size with overlap:** sliding window of 800 tokens, 50-token overlap
- **Strategy B — Structure-aware:** respects headings, paragraphs, and table boundaries
- Comparison: Recall@k and MRR are reported for each strategy separately

### Chunk metadata fields

| Field | Description |
|---|---|
| `chunk_id` | Unique identifier (`doc_id_chunk_NNNN`) |
| `doc_id` | Parent document identifier |
| `title` | Document title |
| `issuer` | Issuing organisation |
| `issue_date` | ISO-8601 publication date |
| `page_start` | First page of this chunk (1-based) |
| `page_end` | Last page of this chunk (1-based) |
| `section_title` | Nearest detected section heading |
| `source_hash` | SHA-256 of the source PDF file |

---

## Planned Evaluation Requirements

Metrics computed over `eval/questions.csv`:

| Metric | Description |
|---|---|
| **Recall@3** | Gold document in top-3 retrieved chunks |
| **Recall@5** | Gold document in top-5 retrieved chunks |
| **Recall@10** | Gold document in top-10 retrieved chunks |
| **MRR** | Mean Reciprocal Rank across all questions |

- Evaluation questions are hand-labelled — no synthetic answers.
- Each question has a `gold_document` and `gold_page` from `manifest.csv`.
- A second ingestion run must produce **no duplicate records** (idempotency test).

---

## Planned Development Milestones

| # | Milestone | Deliverable |
|---|---|---|
| **1** | Project initialisation ✅ | Folder structure, stubs, config, README |
| **2** | Document corpus & ingestion | 30–50 PDFs downloaded, manifest complete, deduplication verified |
| **3** | Extraction, chunking & indexing | PyMuPDF + OCR pipeline, two chunking strategies, ChromaDB indexed |
| **4** | Retrieval evaluation | questions.csv labelled, Recall@k and MRR reported |
| **5** | Chunking strategy comparison | Side-by-side metric report, analysis write-up |

---

## Environment Setup

### Prerequisites

- Python 3.10 or later
- Tesseract OCR installed on the system:
  - **macOS:** `brew install tesseract`
  - **Ubuntu/Debian:** `sudo apt install tesseract-ocr`
  - **Windows:** download the installer from the [official repo](https://github.com/UB-Mannheim/tesseract/wiki)

### Create a virtual environment and install dependencies

```bash
# From the CS2_PolicyLens directory
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### Configure the environment

```bash
cp .env.example .env
# Edit .env to override any defaults (see comments inside the file)
```

### Run the test suite

```bash
pytest tests/ -v
```

---

## Safety Notes

- **No secrets in Git.** `.env` is listed in `.gitignore`. Only `.env.example` is committed.
- **No paid API calls.** All models run locally.
- **No frontend.** This is a retrieval pipeline, not a web application.
- **No answer generation.** PolicyLens retrieves passages; it does not generate answers.
- **Relative paths only.** The project is portable across machines.

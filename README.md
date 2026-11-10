# PolicyLens

> **Case Study 2 — Applied LLM Engineering Assignment**
>
> A retrieval-focused policy-document search system built on local sentence-transformer embeddings and Qdrant.

---

## What is PolicyLens?

PolicyLens ingests publicly available policy PDF documents, chunks them into semantically meaningful passages, embeds each passage with a sentence-transformer model, and stores them in a local Qdrant database.

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
│   ├── config.py       # Paths and optional runtime settings
│   ├── ingest.py       # PDF download, hashing, manifest management
│   ├── extract.py      # Page-level text, layout, and table extraction (PyMuPDF)
│   ├── ocr.py          # Targeted page-level OCR fallback (Tesseract CLI)
│   ├── clean.py        # Conservative canonical-text preparation
│   ├── chunk.py        # Fixed-size and structure-aware chunk CLI
│   ├── chunking.py     # Chunking helpers
│   ├── embed.py        # Pinned local BGE-M3 embedding CLI
│   ├── embeddings.py   # Embedding helper module
│   ├── index.py        # Persistent Qdrant indexing
│   ├── search.py       # Local semantic search implementation
│   ├── evaluate.py     # Evaluation helpers
│   ├── evaluate_retrieval.py # Recall@k and MRR evaluation CLI
│   └── validate_evaluation_dataset.py # Gold-source/index validation CLI
│
├── data/
│   ├── pdfs/           # Raw downloaded PDFs (git-ignored)
│   ├── processed/      # Extraction, OCR, cleaned text, chunks, embeddings (git-ignored)
│   ├── evaluation/
│   │   ├── evaluation_questions.jsonl # Canonical 25-question dataset
│   │   └── results/    # Saved JSON/CSV evaluation outputs
│   └── manifest.csv    # Document registry (doc_id, url, hash, status, …)
│
├── logs/               # Runtime logs (git-ignored)
├── vector_store/       # Qdrant persistent storage (git-ignored)
├── reports/            # Methodology, results, audits, and final report
├── tests/              # pytest test suite
│
├── requirements.txt    # Python dependencies
├── ingest.py           # Root-level PDF ingestion CLI
├── search.py           # Root-level semantic search CLI
├── .env.example        # Environment variable template (copy → .env)
└── .gitignore
```

`eval/questions.csv` is a legacy placeholder and is not read by the current
evaluation or dataset-validation commands.

---

## Planned Technology Stack

| Concern | Library / Tool | Notes |
|---|---|---|
| PDF text extraction | PyMuPDF (`fitz`) | Fast, accurate for text-native PDFs |
| OCR for scanned pages | Tesseract CLI + PyMuPDF | Targeted page-level fallback; English and Hindi |
| Embeddings | `sentence-transformers` | Local BGE-M3, pinned revision; see execution report |
| Vector store | Qdrant local | Persistent local collections with cosine similarity |
| Data manipulation | Pandas | Manifest and question-set management |
| Testing | pytest | Unit and integration tests |
| Config | `python-dotenv` | Secrets and tunable parameters in `.env` |

The Milestone 2B.11 assessment recommended Qdrant local mode. The 2B.12
runtime preflight and 2B.13 production indexing have since passed; both
embedding strategies are stored in separate persistent collections. Search,
semantic retrieval, and the 25-question retrieval evaluation are implemented.
Answer generation is not implemented.
See
[reports/vector_database_assessment.md](reports/vector_database_assessment.md)
for the original assessment and
[reports/qdrant_indexing_report.md](reports/qdrant_indexing_report.md) for the
production indexing results. The gold-reference validation details are in
[reports/retrieval_evaluation_dataset_report.md](reports/retrieval_evaluation_dataset_report.md).

The Milestone 2B.8 model assessment recommended BGE-M3 as the local primary
candidate and OpenAI `text-embedding-3-small` as an API alternative. The
Milestone 2B.10 pipeline uses the pinned local BGE-M3 checkpoint; it does not
send document text to an API. See
[reports/embedding_model_assessment.md](reports/embedding_model_assessment.md)
for measured model-token counts, cost assumptions, and limitations.

### BGE-M3 local embedding pipeline

On the assessed Apple Silicon/Python 3.15.2 environment, the following
embedding runtime versions are installed in the project virtual environment
and verified with MPS:

```bash
.venv/bin/python -m pip install \
  "torch==2.15.0" \
  "sentence-transformers==6.2.0"

.venv/bin/python - <<'PY'
import torch
print("PyTorch:", torch.__version__)
print("MPS built:", torch.backends.mps.is_built())
print("MPS available:", torch.backends.mps.is_available())
if not torch.backends.mps.is_available():
    raise SystemExit("MPS is unavailable; do not silently fall back to CPU.")
PY
```

The first BGE-M3 load requires approximately 2.27 GB of model weights. The
checkpoint is pinned to revision
`5617a9f61b028005a4858fdac845db406aefb181`; the embedding pipeline loads that
revision from the local cache only and explicitly requires MPS (no CPU
fallback). The controlled eight-chunk smoke-test results are in
[reports/embedding_smoke_test_report.md](reports/embedding_smoke_test_report.md).

Generate embeddings for both existing chunk strategies with:

```bash
.venv/bin/python -m src.embed
```

By default, this writes resumable JSONL files and provenance sidecars under
`data/processed/embeddings/`. It uses batch size 1, normalized 1,024-dimensional
vectors, and validates source correspondence, metadata, dimensions, finite
values, and vector norms before reporting completion. Existing valid outputs
are skipped on reruns; changed inputs or model configuration are rejected
rather than silently overwritten. Search is implemented separately from
embedding generation; answer generation is not implemented. See
[reports/embedding_execution_report.md](reports/embedding_execution_report.md)
for the verified corpus-run results and limitations.

### Qdrant production indexing

Milestone 2B.13 indexes the already-generated embedding records without
re-embedding:

```bash
.venv/bin/python -m src.index
```

The fixed-size and structure-aware strategies are stored in separate cosine
collections under `vector_store/qdrant_local/`. The indexer validates source
hashes and payload/vector correspondence, resumes only from matching records,
and reopens the persistent store for full ID and metadata validation. No query
or answer generation was part of that indexing milestone.

### Milestone 2B.14 — Semantic search

Search one strategy collection with the pinned local BGE-M3 model and Qdrant.
The query encoder uses the same normalization, model revision, local MPS
device, and no query instruction as corpus embeddings. It never downloads a
model or sends text to an external service.

From the project root:

```bash
.venv/bin/python search.py "cash disbursement limit for secured loans" --top_k 5 --filter issuer=RBI
```

By default, the CLI searches the fixed-size collection. Select the other
strategy explicitly with `--strategy structure_aware`; use
`--strategy fixed_size` to select fixed-size. `--top_k` accepts positive
integers, and `--top-k` is an equivalent spelling. The currently supported
metadata filter is an exact issuer match; `issuer=RBI` resolves to the corpus's
stored issuer value `Reserve Bank of India`. Results are JSON with the original
chunk payload, including document and page metadata, and a cosine similarity
score. Use `--help` for options.

### Retrieval evaluation

The hand-curated retrieval evaluation set is
[`data/evaluation/evaluation_questions.jsonl`](data/evaluation/evaluation_questions.jsonl).
It contains 25 source-verified questions (15 standard, 5 table-value, and 5
paraphrased) with gold document/page evidence. Validate its page citations and
coverage in both indexed strategies with:

```bash
.venv/bin/python -m src.validate_evaluation_dataset
```

Run the top-10 Recall@3/5/10 and MRR comparison against both collections with:

```bash
.venv/bin/python -m src.evaluate_retrieval
```

The evaluator reads the JSONL dataset, queries both Qdrant collections at
top 10, and writes `retrieval_evaluation_results.json` and
`retrieval_evaluation_question_results.csv` under
`data/evaluation/results/` by default. A run using the current saved results is
also preserved at
`data/evaluation/results/final_run.FNAvNf/`; it contains 25 questions and 50
strategy evaluations. This run reports fixed-size Recall@3/5/10 of
0.80/0.92/0.96 and MRR 0.6117, and structure-aware Recall@3/5/10 of
0.68/0.84/0.96 and MRR 0.5774. Running the evaluator with its default output
directory replaces the default JSON and CSV files; use `--output-dir` to
preserve them when performing another evaluation.

The metrics and question-level error analysis are documented in
[`reports/retrieval_evaluation_report.md`](reports/retrieval_evaluation_report.md).
This small evaluation is descriptive and does not establish statistical
significance or evaluate answer generation.

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
- **Strategy A — Fixed-size with overlap:** 500-token target, 50-token overlap
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

Metrics are computed over the canonical
`data/evaluation/evaluation_questions.jsonl` dataset:

| Metric | Description |
|---|---|
| **Recall@3** | Gold document in top-3 retrieved chunks |
| **Recall@5** | Gold document in top-5 retrieved chunks |
| **Recall@10** | Gold document in top-10 retrieved chunks |
| **MRR** | Mean Reciprocal Rank across all questions |

- Evaluation questions are hand-labelled — no synthetic answers.
- Each question has gold document and PDF page references in `gold_references`.
- A second ingestion run must produce **no duplicate records** (idempotency test).

---

## Planned Development Milestones

| # | Milestone | Deliverable |
|---|---|---|
| **1** | Project initialisation ✅ | Folder structure, stubs, config, README |
| **2A** | Document corpus & ingestion | 31 verified local PDFs; 5 manifest entries remain pending |
| **2B.2** | PDF document extraction ✅ | Page-level JSONL, layout metadata, tables, OCR-candidate flags |
| **2B.5B** | Corpus OCR execution ✅ | Targeted OCR with provenance, page audit, and quality report |
| **2B.6** | Conservative text cleaning ✅ | Separate canonical-text JSONL with source-selection and cleaning metadata |
| **2B.7** | Chunking engine ✅ | Fixed-size and structure-aware chunks with provenance and table preservation |
| **3** | Embeddings, indexing & semantic search ✅ | BGE-M3 embeddings, separate Qdrant collections, local search CLI |
| **4** | Retrieval evaluation ✅ | 25 gold questions evaluated against both strategies; Recall@k and MRR report |
| **5** | Chunking strategy comparison ✅ | Side-by-side metric report and analysis in `reports/chunking_strategy_comparison.md` |

### Milestone 2A — PDF ingestion

The root-level ingestion CLI downloads and verifies PDFs listed in the manifest:

```bash
.venv/bin/python ingest.py --input data/pdfs --manifest data/manifest.csv
```

It updates `data/manifest.csv` with download status, page count, and source
hashes. It processes every manifest row, so rows marked pending may trigger
network downloads. The `--force` option re-downloads existing files and should
not be used for a routine run. Ingestion does not run extraction, OCR, or
Qdrant indexing; those are separate stages.

### Milestone 2B.2 — PDF document extraction

Extract verified local PDFs into one JSONL record per page:

```bash
.venv/bin/python -m src.extract
# Optional paths:
.venv/bin/python -m src.extract --pdf-dir data/pdfs --manifest data/manifest.csv \
  --output-dir data/processed
```

Each page record contains its document ID, source filename, 1-based page number,
selectable text, positioned text/image blocks, likely headings, structured
tables (when PyMuPDF can detect them), text-quality results, and a layout
reading-order estimate. Two-column pages use a documented left-column-then-
right-column block-order heuristic. Pages with fewer than 30 non-whitespace
characters or an alphanumeric ratio below 0.35 are flagged as OCR candidates;
this threshold can also flag blank or unusual pages for review. OCR is not run.
The run writes `extraction_summary.json`, `extraction_errors.jsonl`, and one
`<doc_id>.jsonl` file per matched document beneath `data/processed/`.

Run the extraction tests with:

```bash
.venv/bin/python -m pytest tests/test_extract.py -v
```

### Milestone 2B.5 — Targeted OCR fallback

The OCR pipeline uses the local Tesseract executable and PyMuPDF. It reads the
audited page inventory, renders only selected pages at 300 DPI, and stores OCR
text, language, confidence, and provenance on the existing page-level JSONL
record. Native text and structured table data are retained. OCR output is not
used to fabricate table cells.

Install Tesseract separately from Python dependencies. On macOS:

```bash
brew install tesseract
brew install tesseract-lang
tesseract --version
tesseract --list-langs
```

The base Homebrew formula includes English (`eng`); `tesseract-lang` adds
additional language data, including Hindi (`hin`). Verify that both `eng` and
`hin` appear in the language listing before running the OCR pipeline. On Apple
Silicon, if the executable is not on `PATH`, set
`TESSERACT_CMD=/opt/homebrew/bin/tesseract` in `.env` (on Intel Homebrew, check
`brew --prefix tesseract` for the executable path).

On Debian/Ubuntu, install the engine and both language data packages:

```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-hin
tesseract --list-langs
```

The language listing must include `eng` and `hin`; pages containing Hindi use
`eng+hin` (or `hin` for a Hindi-only page), including `doc_009`, page 49. Other
English pages use `eng`. On systems
where a language is not included by the package manager, install the matching
official Tesseract traineddata file (for example, `eng.traineddata` or
`hin.traineddata`) from the [Tesseract traineddata repository](https://github.com/tesseract-ocr/tessdata_fast),
place it in the active tessdata directory, and set `TESSDATA_PREFIX` to that
directory if needed. The exact directory is platform/package dependent. Do not
start an OCR run until both required languages are listed.

Run OCR after the candidate audit and page-level extraction are available:

```bash
.venv/bin/python -m src.ocr
# Reprocess successful OCR pages only when explicitly required:
.venv/bin/python -m src.ocr --force
```

The default audit is `reports/ocr_candidate_audit.csv`. The target inventory
is written to `reports/ocr_target_inventory.csv`; processing totals and
page-level errors are written to `data/processed/ocr_processing_summary.json`
and `data/processed/ocr_errors.jsonl`. A missing engine or language pack is
recorded as blocked rather than treated as a successful OCR run.

### Milestone 2B.5B — Corpus OCR execution

The verified local run used Tesseract 5.5.4 with `eng` and `hin` installed,
Python 3.15.2, and PyMuPDF 1.28.2 from `.venv`. It processed 37 selected pages
and excluded 11 blank, sparse, or formatting-driven candidates. All 37 unique
targets have successful OCR output, with zero unresolved page failures (two
initial source-resolution errors were corrected and retried). Final language
counts are 29 `eng`, 7 `eng+hin`, and 1 `hin`; targeted retries brought the
successful OCR invocation count to 53. A safe idempotency rerun made no OCR
calls and changed no processed JSONL data. OCR confidence is not a guarantee of
correct transcription; dense tables, Hindi contact details, legal citations,
and numeric values still require source verification. The complete test suite
passes (27 tests). See
`reports/ocr_execution_report.md`, `reports/ocr_page_quality_audit.csv`, and
`reports/ocr_processing_summary.csv` for results and limitations.

### Milestone 2B.6 — Conservative text cleaning and normalization

Run the cleaning stage after extraction and OCR:

```bash
.venv/bin/python -m src.clean
# Optional input/output paths:
.venv/bin/python -m src.clean --input-dir data/processed \
  --output-dir data/processed/cleaned \
  --summary data/processed/cleaning_summary.json
```

The cleaner reads the top-level page JSONL files and writes separate cleaned
copies under `data/processed/cleaned/`; it does not modify the source PDFs,
manifest, or raw extraction/OCR JSONL. The cleaned copies retain raw fields and
add `canonical_text` plus `cleaning` metadata identifying whether native or
OCR text was selected and why. OCR is used only when the separate native text
is missing or fails the extraction text-quality threshold; the two sources
are not blindly concatenated. Tables and OCR provenance remain separate.

Whitespace and native block-internal line wraps are normalized conservatively.
Visible hyphens are retained when joining a proven native line wrap; ambiguous
hyphen breaks and all OCR-derived pages are flagged for review as appropriate.
Repeating page-edge lines are removed only with document-level repetition and
content safeguards; standalone physical page numbers are removed only when
they match the page record and repeat across the document. The run summary is
`data/processed/cleaning_summary.json`; the detailed methodology, examples,
counts, and limitations are in `reports/text_cleaning_report.md`.

### Milestone 2B.7 — Chunking

Generate both chunking strategies from the cleaned page-level records:

```bash
.venv/bin/python -m src.chunk \
  --input-dir data/processed/cleaned \
  --manifest data/manifest.csv \
  --output-dir data/processed/chunks \
  --chunk-size 500 \
  --overlap 50 \
  --strategy both
```

The CLI also accepts `--strategy fixed_size` or
`--strategy structure_aware` to generate one output independently. The chunk
size must be within the configured 300-800 token range; the default target is
500 tokens and the default overlap is 50. These values can be overridden with
the corresponding CLI options or `CHUNK_TARGET_TOKENS` and
`CHUNK_OVERLAP_TOKENS` environment variables.

Outputs are written separately to
`data/processed/chunks/fixed_size.jsonl` and
`data/processed/chunks/structure_aware.jsonl`, with corpus statistics in
`data/processed/chunks/chunking_summary.json`. Chunk IDs are deterministic for
identical inputs and settings, so rerunning safely replaces the generated
chunk files with equivalent records. The inputs in `data/processed/cleaned/`,
raw extraction/OCR files, PDFs, and manifest are not changed.

Token counts use the named PolicyLens Unicode lexical tokenizer: Unicode
letter/number runs and individual punctuation marks are counted as tokens.
This is an explicit reproducible lexical measure, not a count from a specific
language-model tokenizer. Fixed-size chunks use a sliding window with overlap.
Structure-aware chunks use detected heading, clause, and paragraph boundaries
as preferred breakpoints near the target size. Extracted tables are emitted as
separate structured table chunks; oversized tables are split at row boundaries
with their first row repeated as the header. OCR source/provenance and all
cleaning-review flags are retained on the corresponding chunks. Review flags
on otherwise empty pages are also retained in review-only chunks.

Run the chunking tests with:

```bash
.venv/bin/python -m pytest tests/test_chunk.py -v
```

The measured corpus results, validation, examples, and known limitations are
in `reports/chunking_report.md`.

---

## Environment Setup

### Prerequisites

- Python 3.10 or later
- Tesseract OCR is optional for native PDF extraction. It is required to run
  the targeted OCR milestone described above.

### Create a virtual environment and install dependencies

```bash
# From the CS2_PolicyLens directory
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### Configure the environment (optional)

```bash
cp .env.example .env
# Edit .env only when you need to override a supported setting.
```

The embedding pipeline is pinned in code to local BAAI/bge-m3 revision
`5617a9f61b028005a4858fdac845db406aefb181` and requires its snapshot to be
cached locally and Apple MPS to be available. `HF_HOME` or `HF_HUB_CACHE` may
select the Hugging Face cache location. Qdrant uses local persistent storage;
no separate Qdrant service or API key is required.

### Run the test suite

```bash
.venv/bin/python -m pytest tests/ -v
```

---

## Safety Notes

- **No secrets in Git.** `.env` is listed in `.gitignore`. Only `.env.example` is committed.
- **No paid API calls.** All models run locally.
- **No frontend.** This is a retrieval pipeline, not a web application.
- **No answer generation.** PolicyLens retrieves passages; it does not generate answers.
- **Relative paths only.** The project is portable across machines.

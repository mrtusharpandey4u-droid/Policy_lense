# Milestone 2B.10 — Embedding Execution Report

## Result

Generated and validated embeddings for both existing chunk strategies using
local BGE-M3 on Apple MPS. The output files contain 2,848 records in total.
Original chunk JSONL files were not modified.

| Strategy | Source chunks | Valid embedding records | Failed | Missing / duplicate |
|---|---:|---:|---:|---:|
| Fixed-size | 1,370 | 1,370 | 0 | 0 / 0 |
| Structure-aware | 1,478 | 1,478 | 0 | 0 / 0 |
| **Total** | **2,848** | **2,848** | **0** | **0 / 0** |

Outputs:

- `data/processed/embeddings/fixed_size.jsonl`
- `data/processed/embeddings/structure_aware.jsonl`
- Per-output `.meta.json` provenance sidecars and
  `data/processed/embeddings/embedding_summary.json`

These are generated files under the repository's ignored
`data/processed/` directory.

## Model and Configuration

- Model: `BAAI/bge-m3`
- Exact revision: `5617a9f61b028005a4858fdac845db406aefb181`
- Dimensions: 1,024
- Device: Apple MPS (`mps:0`)
- Batch size: 1
- Precision: float32
- Normalization: enabled; L2 norm tolerance `1e-4`
- Model loading: pinned snapshot directory from the local Hugging Face cache;
  Hub offline mode enabled
- Prompt: none

Runtime versions from `.venv`:

| Component | Version |
|---|---|
| Python | 3.15.2 |
| PyTorch | 2.15.0 |
| Sentence Transformers | 6.2.0 |
| Transformers | 5.22.2 |
| Tokenizers | 0.23.3 |
| NumPy | 2.5.4 |

## Execution and Resume

An initial run loaded the named model from cache but still attempted Hugging
Face metadata GET/HEAD requests. It was stopped after 1,062 fixed-size vectors
had been durably appended. The requests concerned model metadata and references;
chunk text was not sent to an external embedding endpoint. The loader was then
changed to use the exact cached revision directory with Hub offline mode
enabled. The resumed completion and the idempotency run emitted no Hub network
requests.

The successful completing invocation resumed the 1,062 valid fixed-size
records, generated 308 additional fixed-size vectors, then generated all 1,478
structure-aware vectors:

| Strategy | Newly embedded in completing invocation | Reused valid records | Strategy elapsed | Mean measured inference per new chunk |
|---|---:|---:|---:|---:|
| Fixed-size | 308 | 1,062 | 45.819 s | 0.1481 s |
| Structure-aware | 1,478 | 0 | 237.612 s | 0.1600 s |

The completing invocation took 288.797 seconds total, including the 4.351
second model load and output validation. Its measured mean model-inference time
across the 1,786 newly generated vectors was approximately 0.158 seconds per
chunk. The first interrupted invocation's duration was not captured, so an
end-to-end wall time for all 2,848 vectors is not claimed.

A subsequent idempotency run completed in 5.666 seconds, generated zero
vectors, and skipped all 1,370 fixed-size and 1,478 structure-aware records
after validating them.

## Integrity and Validation

Independent validation confirmed:

- Exactly one output for every source chunk; no missing or duplicate IDs.
- `chunk_id` and `source_chunk_id` match.
- All 2,848 vectors have 1,024 finite, non-zero values and normalized L2 norm
  within `1e-4` of 1.
- Model name, pinned revision, embedding configuration, and strategy match the
  run metadata.
- Every source chunk's text and metadata—including document ID, page range,
  OCR provenance, cleaning-review flags, and table data—match its recorded
  source hash.
- No invalid or empty-text source chunks and no failed embeddings.

Source chunk file SHA-256 values were unchanged:

| Input | SHA-256 |
|---|---|
| `fixed_size.jsonl` | `375b1a6961d56bfffc1e85b402e638b6b94454c0f69ae4cec441f08af777aedf` |
| `structure_aware.jsonl` | `b719052434f7b7dca8dbebf19f5ea72faa9918f21393c61de7cd404a6ead8fd3` |

| Output | Size |
|---|---:|
| Fixed-size JSONL | 34,642,296 bytes |
| Structure-aware JSONL | 36,962,241 bytes |

## Resource Observations

- Machine memory: 16 GiB unified memory.
- Maximum observed MPS driver-allocated memory: 3,208,314,880 bytes
  (structure-aware run).
- Process peak RSS reported by `resource.getrusage`: 980,287,488 bytes.
  RSS and MPS driver allocation are separate measurements and are not added.
- MPS synchronization and memory measurements were taken during inference.
- PyTorch emitted its informational warning that distributed output redirects
  are unsupported on macOS. No inference errors occurred.

No hosted or paid embedding API was used, and no provider API charge was
incurred. Local compute and energy costs are not estimated. These results only
establish successful generation and integrity; retrieval quality has not yet
been evaluated.

## Tests

- Targeted embedding tests: 11 passed.
- Complete test suite: 64 passed, with 6 pre-existing dependency deprecation
  warnings.
- Python compilation (`compileall`) and `git diff --check`: passed.

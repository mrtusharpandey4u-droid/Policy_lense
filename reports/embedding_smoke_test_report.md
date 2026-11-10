# Milestone 2B.9 — BGE-M3 Controlled Smoke Test

**Result: Smoke test passed on MPS.** Eight representative chunks were
embedded locally with batch size 1. This was a smoke test only; no
production embeddings, index, or vector database were created.

## Environment and Installed Runtime

The test ran from the PolicyLens `.venv`, not the system/Anaconda Python:

| Component | Verified version / result |
|---|---|
| Python executable | `/Users/tusharpandey/Documents/CS2_PolicyLens/.venv/bin/python` |
| Python | 3.15.2 |
| macOS / hardware | macOS 27.2, arm64 MacBook Air with Apple M5, 16 GiB unified memory |
| PyTorch | 2.15.0; import successful |
| Sentence Transformers | 6.2.0 |
| Transformers | 5.22.2 |
| Tokenizers | 0.23.3 |
| Safetensors | 0.8.0 |
| NumPy | 2.5.4 |
| SciPy | 1.18.1 |
| scikit-learn | 1.9.1 |
| MPS built / available | `True` / `True` |
| CUDA | Unavailable (not applicable on this Mac) |

Only the embedding runtime and its resolved dependencies were installed into
`.venv`: `torch==2.15.0` and `sentence-transformers==6.2.0` were the
requested top-level packages. Other project dependencies and configuration
files were not changed. This environment setup is separate from changing
`requirements.txt`.

The first runtime installation completed successfully. PyTorch imported,
reported an MPS-enabled build, and completed a small MPS tensor operation
before model download. MPS was therefore verified at runtime, not inferred
from package metadata alone.

## Model and Smoke-Test Scope

- Model: `BAAI/bge-m3`
- Hugging Face revision: `5617a9f61b028005a4858fdac845db406aefb181`
- Expected output dimension: 1,024
- Device passed explicitly at load: `mps`
- Actual model and parameter device: `mps:0`
- Batch size: 1
- Unique chunks embedded: 8 (four from each strategy)
- Dataset files read only:
  - `data/processed/chunks/fixed_size.jsonl` — 1,370 records
  - `data/processed/chunks/structure_aware.jsonl` — 1,478 records

Each strategy contributed ordinary native text, a structured-table chunk, a
chunk with English/Hindi OCR provenance, and a native chunk carrying a
cleaning-review flag. No source text or vectors were written to a file.

| Strategy | Sample category | Chunk ID | Result |
|---|---|---|---|
| Fixed-size | Native text | `doc_001_fixed_size_00001_aee405d33739` | Passed |
| Fixed-size | Structured table | `doc_001_fixed_size_00002_c5426065a28b` | Passed |
| Fixed-size | English/Hindi OCR | `doc_004_fixed_size_00001_9b8b675cc272` | Passed |
| Fixed-size | Native cleaning-review page | `doc_001_fixed_size_00007_4a17edd59695` | Passed |
| Structure-aware | Native text | `doc_001_structure_aware_00001_ac782e3816d0` | Passed |
| Structure-aware | Structured table | `doc_001_structure_aware_00002_8f73405fe12b` | Passed |
| Structure-aware | English/Hindi OCR | `doc_004_structure_aware_00001_d155e9332d76` | Passed |
| Structure-aware | Native cleaning-review page | `doc_001_structure_aware_00007_0c1f6297db2c` | Passed |

## Results

- **Model load:** successful at the pinned revision on `mps:0`.
- **Embedding generation:** 8/8 succeeded on MPS; there was no CPU fallback.
- **Dimension validation:** all eight vectors had shape `(1024,)`.
- **Finite-value validation:** all vector values were finite; no NaN or
  infinity was found.
- **Non-zero validation:** all vectors had non-zero L2 norms (approximately
  1.0; the model returned normalized embeddings).
- **Similarity:** cosine similarity between the first two sample vectors
  computed successfully and was finite: **0.62867385**.
- **Inference duration:** eight sequential batch-size-1 encodes took
  approximately **1.77 seconds** in the successful run. Individual measured
  times ranged from about 0.10 to 0.79 seconds. This is a tiny sample, not a
  corpus throughput benchmark.
- **Model load duration:** the first load, which included fetching/cache
  population and initialization, took approximately **278 seconds**.
  A subsequent cached load took approximately **3.1 seconds**. These
  measurements are environment- and network-specific.
- **Model checkpoint:** `pytorch_model.bin` is 2,271,145,830 bytes (about
  2.12 GiB). The pinned snapshot occupies about 2.1 GiB in the Hugging Face
  cache. The repository cache currently reports about 4.3 GiB across stored
  blobs/snapshots; not all of that total can be attributed to this run because
  the cache was not inventoried before download. No cache cleanup was done.

### Memory observations

PyTorch's MPS memory counters in a separate cached-load/one-sample run
reported:

- Current MPS allocated memory after model load and after the sample:
  **2,288,370,176 bytes** (about 2.13 GiB).
- MPS driver-allocated memory after load: **3,196,534,784 bytes** (about
  2.98 GiB); after one sample: **3,196,780,544 bytes**.
- Python process peak RSS high-water mark in the eight-sample process:
  **989,528,064 bytes** (about 0.92 GiB).
- macOS system-wide free-memory percentage after the test: **61%**.

The process RSS does not account for all MPS driver allocations. The MPS
values above are current allocation counters, not a measured peak during the
eight-sample run. No system memory pressure failure or swap activity was
observed in the recorded snapshots. These values support feasibility for a
small batch, but do not establish safe maximum batch size.

## Failures and Warnings

The first smoke-test process loaded the model successfully on `mps:0`, but
stopped before generating embeddings because the test guard compared the
device string literally to `"mps"` and rejected PyTorch's valid `"mps:0"`
representation. This was a test-guard issue, not a model/device failure.
The guard was corrected to check `torch.device(device).type == "mps"` and the
same eight selected chunks were then embedded successfully. No CPU fallback
was attempted.

Observed notices:

- PyTorch emitted its macOS note that distributed elastic multiprocessing
  redirects are not supported. Distributed multiprocessing was not used.
- Hugging Face Hub emitted an unauthenticated-request warning during public
  model retrieval. The public model download succeeded; no token or API
  credential was accessed, requested, or printed.
- No Python warnings were captured during the successful model load.

## Readiness

**Ready for a controlled full-corpus embedding run, with safeguards.** The
model loads successfully and all eight representative embeddings passed on
MPS. Before processing all chunks, implementation should still:

1. Process in small batches (start with batch size 1 or a similarly
   conservative value) and preserve explicit MPS selection.
2. Fail clearly if MPS is unavailable rather than silently switching device.
3. Keep the two chunking strategies as separate outputs/experiments.
4. Persist embeddings only in a dedicated generated artifact, retaining
   source chunk IDs and metadata; do not overwrite chunk JSONL.
5. Add resumability, duplicate checks, finite/dimension validation, and
   progress/error summaries before corpus execution.
6. Measure throughput and memory on a larger but still bounded batch before
   choosing production batch settings.

This conclusion approves only a future controlled full-corpus embedding
milestone; indexing, vector storage, retrieval, and answer generation remain
out of scope.

## Validation and Integrity

- Test suite: **53 passed**.
- Compilation: `.venv/bin/python -m compileall -q src tests` passed.
- `git diff --check` passed.
- SHA-256 values for both chunk JSONL files and `chunking_summary.json`
  matched their pre-smoke-test values. The files were not modified.
- No PDFs, manifest data, raw extraction, cleaning outputs, or chunk outputs
  were changed.

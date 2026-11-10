# Milestone 2B.13 — Production Qdrant Indexing Report

## Result

Both existing embedding datasets were indexed into separate persistent local
Qdrant collections. The indexer closed and reopened the store, then compared
every stored point against its source embedding record. A second full run
validated all existing points, inserted none, and left both collection counts
unchanged.

| Strategy | Collection | Expected | Actual | IDs validated | Missing / extra |
|---|---|---:|---:|---:|---:|
| Fixed-size | `policylens_fixed_size_bge_m3` | 1,370 | 1,370 | 1,370 | 0 / 0 |
| Structure-aware | `policylens_structure_aware_bge_m3` | 1,478 | 1,478 | 1,478 | 0 / 0 |
| **Total** | Two independent collections | **2,848** | **2,848** | **2,848** | **0 / 0** |

No input records failed or were skipped as invalid during the production
indexing run.

## Configuration and environment

- Database: Qdrant local persistent mode, `qdrant-client==1.20.0`.
- Runtime: Python 3.15.2 on macOS Apple Silicon.
- Storage: `vector_store/qdrant_local/` (approximately 37 MB after indexing;
  excluded from Git).
- Vector size: 1,024; distance: cosine.
- Embedding model: `BAAI/bge-m3`, revision
  `5617a9f61b028005a4858fdac845db406aefb181`.
- Batch size: 32 points.
- Indexing batches: 43 fixed-size batches and 47 structure-aware batches.
- First production indexing duration: 2.595 seconds, including the indexer's
  post-write close/reopen validation. Embeddings were not regenerated.
- No monetary API or provider compute charge was incurred. This was local
  indexing of existing vectors; memory usage was not separately measured.

The collection configuration and source-file hashes are recorded in Qdrant
collection metadata. The input chunk and embedding files were not modified:

| Input | SHA-256 |
|---|---|
| `data/processed/chunks/fixed_size.jsonl` | `375b1a6961d56bfffc1e85b402e638b6b94454c0f69ae4cec441f08af777aedf` |
| `data/processed/embeddings/fixed_size.jsonl` | `6e5ceb850daa362318cde184a3de359f0ffd6f2108d64f717176c707e4ad6d62` |
| `data/processed/chunks/structure_aware.jsonl` | `b719052434f7b7dca8dbebf19f5ea72faa9918f21393c61de7cd404a6ead8fd3` |
| `data/processed/embeddings/structure_aware.jsonl` | `fc055df6217b43e655903fbf13884f2224c8ac6713637f3191ebc486b0af4c6a` |

## Record IDs and payload

Each stable source `chunk_id` is mapped deterministically to a UUIDv5 Qdrant
point ID. The original chunk ID remains in the payload. The vector is stored
in Qdrant's vector field; all other source embedding-record fields are retained
in its JSON payload, including:

- Chunk text, chunk ID, document ID, title, issuer, and issue date.
- Page start/end and section title.
- Source hash, OCR provenance, and cleaning-review fields when present.
- Chunking strategy, embedding model, model revision, dimensions, and
  embedding configuration/status.
- Source chunk ID and source chunk/file hashes.

Issuer is stored as a top-level payload field to support exact issuer filters.
The strategies use separate collections and cannot be mixed accidentally by a
collection-level query.

## Validation and idempotency

The first indexing run wrote 1,370 fixed-size and 1,478 structure-aware points.
After closing and reopening the persistent client, validation checked every
point ID and payload against the prepared source inventory, checked vector
dimension, finiteness, normalization (norm tolerance `1e-4`) and direction
against the source vector,
and checked document/page/text fields and strategy. Both collections had
exactly the expected count and no missing, duplicate, or extra IDs.

Cosine collection configuration and issuer-filtered queries were verified for
both collections. The issuer-filter checks returned the expected matching
sample and matching issuer/citation payload (sample issuer: `Bajaj Finance
Limited`).

The second full invocation completed successfully:

| Strategy | Existing points verified/skipped | Added | Count before | Count after |
|---|---:|---:|---:|---:|
| Fixed-size | 1,370 | 0 | 1,370 | 1,370 |
| Structure-aware | 1,478 | 0 | 1,478 | 1,478 |

It again closed and reopened the database and validated all 2,848 point IDs.
The second invocation took 2.088 seconds end-to-end.

## Dependency decision

`qdrant-client==1.20.0` is now pinned in `requirements.txt`. ChromaDB was
removed after checking project imports/usages: it had no active implementation
or imports, only the previous dependency/configuration and an unimplemented
search stub. The Qdrant backend configuration and stub references were updated.
No unrelated packages were upgraded or downgraded.

## Checks run

- `.venv/bin/python -m pytest -q` — **70 passed**.
- `.venv/bin/python -m compileall -q src tests` — passed.
- `.venv/bin/python -m pip check` — no broken requirements.
- `git diff --check` — passed.
- Independent persisted-collection inspection — both exact counts,
1,024-dimensional vectors, and cosine configuration confirmed.

Pytest emitted six deprecation warnings from PyMuPDF/SWIG bindings. They did
not fail tests and are unrelated to Qdrant indexing.

## Limitations and safe update behavior

- Qdrant local mode is suitable for this local corpus but is not a Qdrant
  server. Local payload-index creation is unsupported/ineffective, so no
  payload indexes were created; issuer filtering was exercised against the
  local collections and may require scanning as the corpus grows.
- Changed source files or embedding configuration are rejected rather than
  silently replacing a collection. The current safe rebuild procedure is to
  preserve the existing store and build/validate into a new versioned storage
  path and collection names, then explicitly switch configuration after
  review. The indexer does not delete collections automatically.
- No CLI search, retrieval evaluation, answer generation, or chatbot behavior
  was added in this milestone.

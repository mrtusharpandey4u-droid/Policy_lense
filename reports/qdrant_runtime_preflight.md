# Milestone 2B.12 — Qdrant Local Runtime Preflight

## Result

**Qdrant local mode passed the synthetic runtime preflight** in the existing
project `.venv` on Python 3.15.2 / macOS Apple Silicon ARM64.

No actual PolicyLens embedding records, chunk text, PDFs, or manifest data were
read by the smoke test. The test used two synthetic points and a temporary
database directory, which was removed after the test. No Qdrant store was
created under the project `vector_store/` directory.

## Environment and installation

- Python executable:
  `.venv/bin/python` → `.../CS2_PolicyLens/.venv/bin/python`
- Python: 3.15.2
- Platform: macOS 27.2, `arm64`
- Installed Qdrant client: `qdrant-client==1.20.0`
- Installation command:

  ```bash
  .venv/bin/pip install --no-input 'qdrant-client==1.20.0'
  ```

The client installed successfully. Runtime dependencies that were absent before
installation were installed to satisfy the client's declared requirements:

| Package | Version |
|---|---:|
| grpcio | 1.85.1 |
| httpx | 0.28.1 |
| portalocker | 4.4.2 |
| protobuf | 7.36.2 |
| pydantic | 2.14.3 |
| urllib3 | 2.8.0 |
| NumPy (already present) | 2.5.4 |

`pip check` result: **No broken requirements found.**

No dependency manifest was changed. `requirements.txt` still declares ChromaDB,
not Qdrant; making Qdrant a project dependency is a decision for an approved
implementation milestone.

## Synthetic runtime checks

The test created a temporary persistent local collection with a 1,024-element
unit vector and cosine distance. It inserted two synthetic points with the
same vector but different issuers, so the issuer filter's behavior was
observable even for a tied unfiltered similarity result.

| Check | Result |
|---|---|
| Local Qdrant client starts and creates a collection | Passed |
| Collection vector size | 1,024 |
| Collection distance | Cosine |
| Similarity query for inserted vector | Passed; target score approximately 1.0 |
| Exact issuer filter | Passed; returned only the matching synthetic point |
| Nested JSON payload round-trip | Passed; nested page provenance and table data preserved |
| Close and reopen persistent local database | Passed |
| Vector config and records after reopen | Passed |
| Repeat upsert with same UUID point ID | Passed; count remained 2 and payload updated |

The isolated smoke operation took **0.0103 seconds** (measured around local
collection creation, insert, query, close/reopen, and checks). The dedicated
Python process peak RSS was **111,525,888 bytes**. This is a tiny synthetic
preflight, not a throughput or resource estimate for indexing all 2,848
PolicyLens vectors.

No Qdrant runtime warnings or errors were emitted during the smoke test.

## Test and validation commands

- `.venv/bin/python -m pytest -q tests/test_qdrant_preflight.py -s` — **1 passed**
- `.venv/bin/python -m pip check` — **passed**
- `.venv/bin/python -m pytest -q` — **65 passed**, 6 dependency deprecation
  warnings from existing PyMuPDF/SWIG code
- `.venv/bin/python -m compileall -q src tests` — **passed**
- `git diff --check` — **passed**

The new test uses synthetic vectors and metadata, isolates persistence under
pytest's temporary directory, closes/reopens the client, checks filtered
similarity and nested payload round-tripping, and confirms repeated upserts do
not add duplicate points. It skips if `qdrant-client` is not installed.

## Scope and remaining concerns

- **Compatibility:** basic local persistence and the tested API work on this
  exact Python 3.15.2/macOS ARM64 environment.
- **Not tested:** indexing actual PolicyLens data, larger-scale performance,
  concurrent writers, crash recovery under load, filters over the corpus, or
  any retrieval-quality metric.
- No production collection, database adapter, semantic retrieval, or
  answer-generation feature was implemented.
- `requirements.txt` was not changed; a future approved implementation should
  decide how to declare/pin Qdrant and reconcile the existing Chroma dependency
  and configuration.

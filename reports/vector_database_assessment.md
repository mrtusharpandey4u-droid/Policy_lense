# Milestone 2B.11 — Vector Database Selection and Compatibility Assessment

**Assessment date:** 2026-11-09

## Executive summary

**Recommendation: Qdrant local mode**, using `qdrant-client` with its persistent
`path=` configuration and two separate collections. The recommendation is
conditional: the current `.venv` is Python 3.15.2 on Apple Silicon, but
`qdrant-client` is not installed and has not been run in this environment.
PyPI metadata explicitly lists Python 3.15 support for the client; a small
install-and-runtime preflight is still required in the next milestone.

The corpus is modest (2,848 vectors, 1,024 dimensions) and all vectors are
already computed and normalized. Qdrant's persistent local client, cosine
metric, exact payload filters, and JSON payloads align with the needs without
requiring a separate server. Separate collections preserve the fixed-size and
structure-aware comparison.

This is an assessment only. No packages, vectors, indexes, or source data were
changed, and no search or retrieval was implemented or evaluated.

## Workspace evidence

Inspected the project dependency file, configuration, embedding implementation,
embedding execution report, tests, and both generated embedding JSONL files.
The relevant paths are `requirements.txt`, `src/config.py`, `src/embed.py`,
`tests/test_embed.py`, and `reports/embedding_execution_report.md`.

The `.venv` reports Python 3.15.2 on macOS 27.2 `arm64`. Runtime package
inspection found:

| Database package | Installed in `.venv`? | Evidence |
|---|---:|---|
| `chromadb` | No | `importlib.metadata` reports not installed; import module unavailable |
| `qdrant-client` | No | `importlib.metadata` reports not installed; import module unavailable |
| `faiss-cpu` / `faiss` | No | Distribution and import module unavailable |

`requirements.txt` currently declares `chromadb>=0.5.0`, and `src/config.py`
defaults `VECTOR_STORE_BACKEND` to `chromadb` with one `CHROMA_COLLECTION_NAME`.
These are existing project intentions, not evidence that Chroma is installed
or works on this interpreter.

The embedding outputs are
`data/processed/embeddings/fixed_size.jsonl` (1,370 records) and
`data/processed/embeddings/structure_aware.jsonl` (1,478 records). A
streaming inspection confirmed 1,024 vector values per record, unique chunk
IDs, matching `chunk_id` and `source_chunk_id`, and matching strategy names.
Both sets include document ID, issuer, title, issue date, page range, source
hash, text, tables, page provenance, OCR and cleaning-review fields, and
embedding provenance. `issuer` is a non-null string on all records (11 distinct
issuer values across each set). `section_title` is optional and is omitted on
288 fixed-size and 236 structure-aware records. `tables`, `page_provenance`,
and `review_pages` are structured list values.

The embedding report records the full vector validation and successful
idempotent rerun. No retrieval-quality results exist yet.

## Comparison

| Criterion | ChromaDB | Qdrant local (`qdrant-client`) | FAISS CPU |
|---|---|---|---|
| Python 3.15.2 | PyPI's current package metadata says `Requires-Python >=3.9`, but its classifiers only state generic Python 3; transitive/runtime compatibility on 3.15 is not established. Not installed here. | PyPI project metadata explicitly lists Python 3.15 among its classifiers. Strongest declared match, but not installed or runtime-tested here. | PyPI `faiss-cpu` metadata lists Python classifiers through 3.14, not 3.15. Compatibility with 3.15 is unverified. |
| Apple Silicon | PyPI calls the package OS-independent; this does not prove that the package's native/transitive dependencies work in this `.venv`. Not tested here. | The client has a local Python mode and current NumPy is installed in this ARM64 environment. The Qdrant client itself has not been installed/tested on this machine; do not infer a successful runtime from metadata alone. | PyPI metadata classifies the package for macOS generally, but this does not establish a compatible CPython 3.15 ARM64 wheel. No compatible wheel was verified. |
| Local persistence | Official `PersistentClient(path=...)` persists to and reloads from a local path. | Official Python client supports `QdrantClient(path=...)` for persistent local mode, without a separate server. | Index files can be written/read, but index persistence is not a complete database with managed metadata. Application must manage all sidecars and lifecycle. |
| Cosine similarity | Native HNSW `space="cosine"` collection configuration. | Native collection metric `Distance.COSINE`. | Cosine can be computed as inner product after normalizing both stored and query vectors; this project's stored vectors are normalized. |
| Issuer filtering | Native `where` metadata filter. | Native payload filter, e.g. exact match on `issuer`; payload indexes can be added if needed. | No database-level metadata filter. Application must filter IDs/vectors itself, use per-issuer indexes, or over-fetch and risk losing correct top-k results. |
| Document/page metadata | Store searchable scalar metadata and text as the document. Metadata supports scalar values and homogeneous arrays; nested table/page-provenance objects need flattening, JSON serialization, or an external sidecar. | Payload supports JSON objects, arrays, and scalar values, fitting nested tables and page provenance more directly. Store chunk text and citation fields in payload. | Requires an external ID-to-record mapping and metadata store. |
| Stable chunk IDs | Accepts unique string IDs directly. | Point IDs are unsigned 64-bit integers or UUIDs, not arbitrary PolicyLens strings. Derive a stable UUID (for example UUIDv5) from each `chunk_id`, and retain the original string in payload and mapping. | FAISS indexes use integer positions/IDs; a deterministic string-to-integer mapping and metadata sidecar are required. |
| Two strategies | Straightforward: two named collections. | Straightforward: two named collections in one persistent local database. | Two index files, each paired with its own ID/metadata sidecar. |
| Implementation / maintenance | Simple client API and already declared in the requirements, but has a more extensive dependency tree and its Python 3.15 runtime remains unverified. | Moderate implementation effort; rich payload model and local-persistence API fit the corpus. Local mode is positioned for development/prototyping/testing, so concurrency and growth limits need a later operational decision. | Fast and compact for nearest-neighbor math, but most database behavior (filtering, metadata, persistence consistency, and IDs) becomes custom project code. |
| Assignment fit | Strong conceptual fit; existing requirements/configuration are Chroma-oriented. Nested metadata and Python 3.15 package compatibility are concerns. | Best overall fit for this corpus and current interpreter evidence, provided the required preflight succeeds. | Weaker fit because the assignment needs issuer filtering and document/page citations as first-class data, not only vector math. |
| Dependency/runtime risk | No installed package; `chromadb` metadata lists dependencies including ONNX Runtime, gRPC, and tokenizers. Resolver/runtime validation is needed on Python 3.15. | No installed package; package metadata declares Python 3.15. Local storage and ARM64 runtime still need an actual import/reopen/filter test. | No installed package; no Python 3.15 classifier and ARM64 wheel availability not confirmed. Native binary/BLAS packaging adds risk. |

All three are local/open-source options with no required vector-provider API
charge. This assessment does not compare hosted services or attach a monetary
cost to local compute.

## Recommendation and compatibility conclusion

Choose **Qdrant local mode** for the next implementation milestone, subject to
the preflight below. It offers the most directly evidenced Python-version fit
for Python 3.15, stores nested JSON payloads without reducing the page/table
provenance to opaque strings, and provides cosine collections and issuer
filters in one local persistent interface. The full dataset has only 2,848
vectors; the local-client scope is appropriate to evaluate for this
single-machine assignment, though it is not a claim about production
concurrency or deployment scale.

Compatibility status:

- **Verified in this workspace:** Python 3.15.2, macOS ARM64, NumPy 2.5.4,
  stored vector dimension and metadata shape, and that none of the three
  database packages is installed.
- **Verified from current package metadata:** Qdrant client classifiers include
  Python 3.15; Chroma's current PyPI metadata declares Python >=3.9 but has no
  minor-version classifier beyond generic Python 3; FAISS CPU classifiers end
  at Python 3.14.
- **Not verified:** importing or using Qdrant local mode on this exact
  Python/macOS/ARM64 runtime, persistence across reopening, cosine behavior,
  issuer filters, and all nested payload values. No installation was attempted
  because this milestone prohibits changing dependencies.

Do not treat Chroma's `Requires-Python >=3.9` as proof that its full dependency
tree supports Python 3.15. Conversely, package classifiers are published
compatibility declarations, not substitutes for a runtime test. If the
Qdrant preflight fails, stop and reassess Chroma/FAISS or the Python runtime
with approval; do not silently change the project's Python version.

## Proposed architecture for the next milestone

1. Add a modular `src/vector_store.py` adapter. Keep database operations
   separate from embedding generation, chunking, and any future retrieval
   orchestration.
2. Use a single local persistent database directory under the existing ignored
   `vector_store/` directory, with independent collections such as
   `policylens_fixed_size` and `policylens_structure_aware`.
3. Configure each collection for 1,024 dimensions and cosine distance. Pass the
   already-generated vector directly; do not invoke an embedding function or
   change/recompute embeddings. The future query vector must use the same BGE-M3
   revision/configuration and be normalized consistently.
4. Map each string `chunk_id` deterministically to a UUIDv5 point ID. Preserve
   the original `chunk_id` and `source_chunk_id` in payload. Check mapping
   collisions and ensure every source ID appears exactly once.
5. Store citation and filter fields in the payload: `doc_id`, `title`, `issuer`,
   `issue_date`, `page_start`, `page_end`, `section_title` when present,
   `source_hash`, `chunking_strategy`, `text`, tables, page provenance, OCR
   provenance, cleaning-review flags, and embedding model/revision. Do not
   store the 1,024-float vector a second time in the payload.
6. Query-time issuer filtering should be a Qdrant exact payload match on
   `issuer`. Add a keyword payload index if needed; retain the exact issuer
   value from each source record. Returned payload must include document and
   page range for citations. Do not implement answer generation.
7. Record source-file SHA-256, model revision, dimensions, strategy, collection
   name, and expected record count in a small index manifest. Reuse an existing
   collection only when its manifest and source hashes match.
8. Use deterministic IDs and upsert semantics to prevent duplicate points, but
   do not use destructive collection recreation on an active index. For changed
   inputs, build a versioned staging collection, validate it, and switch the
   active collection names/manifest only after success. Keep the prior
   collection until the replacement is verified; make removal an explicit
   operation.
9. Validate counts and ID coverage after indexing: 1,370 fixed-size and 1,478
   structure-aware points, no extra or missing source IDs, 1,024-dimensional
   vectors, expected collection metric, and representative issuer-filtered
   payloads. Test persistence by closing and reopening the local path.

The exact staging/switch procedure should be confirmed against the installed
Qdrant client's local-mode API before implementation; this assessment has not
run the client and does not assume server-only alias behavior exists in local
mode.

## Risks and limitations

- The Qdrant recommendation is not yet a tested install/runtime result.
- Local mode is positioned for development, prototyping, and testing;
  concurrent-writer behavior has not been verified, and production serving may
  warrant a Qdrant server instead.
- Qdrant's UUID point-ID requirement adds a deterministic mapping layer for
  existing string IDs.
- Missing `section_title` is normal in the current data; payload construction
  must omit absent optional values rather than inventing titles.
- Validate nested table/page-provenance payload shapes and record-size behavior
  with actual rows before indexing the full corpus.
- `requirements.txt` and `src/config.py` currently select/name Chroma. Changing
  them is a next-milestone decision, not part of this assessment.
- Retrieval quality has not been evaluated; database selection says nothing
  about ranking quality.

## Exact next implementation steps

1. Ask for approval to use Qdrant and add a compatible `qdrant-client`
   dependency; do not install it before approval.
2. In the approved implementation milestone, install only into `.venv`, then
   record the resolved package/dependency versions and verify imports on
   Python 3.15.2/macOS ARM64.
3. Run a tiny local-path preflight using representative existing records from
   both strategies: create two cosine collections, write/reopen them, check
   1,024 dimensions, test exact issuer filtering, and round-trip nested
   provenance/table payloads.
4. Resolve and test deterministic UUIDv5 mapping, including duplicate/collision
   checks and preservation of the original string IDs.
5. Implement the adapter and tests for idempotent indexing, changed-input
   rejection/staging, strategy separation, record-count validation, persistence,
   payload citations, and issuer filters.
6. Only after the preflight and tests pass, index all 2,848 existing vectors
   without modifying the source embedding JSONL files.
7. Report indexed counts and validation. Keep retrieval evaluation and all
   answer-generation functionality out of this database milestone.

## Sources

Official documentation and package metadata consulted on the assessment date:

- [Chroma persistent and in-memory clients](https://docs.trychroma.com/docs/run-chroma/clients)
- [Chroma collection index configuration and cosine space](https://docs.trychroma.com/docs/collections/configure)
- [Chroma adding data and metadata value types](https://docs.trychroma.com/docs/collections/add-data)
- [Chroma metadata filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering)
- [ChromaDB PyPI metadata](https://pypi.org/project/chromadb/)
- [Qdrant Python client: local mode, persistent path, and package metadata](https://pypi.org/project/qdrant-client/)
- [Qdrant collections and vector distance configuration](https://qdrant.tech/documentation/manage-data/collections/)
- [Qdrant payload JSON and filtering](https://qdrant.tech/documentation/manage-data/payload/)
- [Qdrant point IDs](https://qdrant.tech/documentation/manage-data/points/)
- [Qdrant local server quickstart](https://qdrant.tech/documentation/quickstart/)
- [FAISS CPU PyPI metadata](https://pypi.org/project/faiss-cpu/)
- [FAISS cosine similarity with normalized inner product](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)
- [FAISS project README and documentation entry points](https://github.com/facebookresearch/faiss)

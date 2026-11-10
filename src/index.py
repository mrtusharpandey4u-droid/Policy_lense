"""Build and validate persistent Qdrant indexes from existing embeddings."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import logging
import math
import os
import struct
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from qdrant_client import QdrantClient, models

from src.config import (
    LOGS_DIR,
    QDRANT_FIXED_COLLECTION_NAME,
    QDRANT_STORAGE_DIR,
    QDRANT_STRUCTURE_COLLECTION_NAME,
)
from src.embed import (
    EmbeddingError,
    EMBEDDING_DIMENSIONS,
    MODEL_NAME,
    MODEL_REVISION,
    STRATEGIES,
    _canonical_sha256,
    _file_sha256,
    _read_jsonl,
    validate_embedding,
)

logger = logging.getLogger("policylens.index")

DEFAULT_EMBEDDING_DIR = Path(__file__).resolve().parents[1] / "data/processed/embeddings"
DEFAULT_CHUNK_DIR = Path(__file__).resolve().parents[1] / "data/processed/chunks"
BATCH_SIZE = 32
SCROLL_PAGE_SIZE = 128
VECTOR_NORM_TOLERANCE = 1e-4
MIN_VECTOR_COSINE = 1.0 - 1e-6
STORE_MARKER_NAME = ".policylens_qdrant_store.json"
STORE_MARKER = {
    "format_version": 1,
    "store": "policylens_qdrant_local",
}
POINT_ID_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL, "https://policylens.local/qdrant/point-id/v1"
)

EXPECTED_COUNTS = {
    "fixed_size": 1370,
    "structure_aware": 1478,
}
COLLECTION_NAMES = {
    "fixed_size": QDRANT_FIXED_COLLECTION_NAME,
    "structure_aware": QDRANT_STRUCTURE_COLLECTION_NAME,
}


class IndexingError(RuntimeError):
    """Raised when indexing cannot safely proceed or validate."""


@dataclass(frozen=True)
class ExpectedPoint:
    chunk_id: str
    payload_sha256: str
    vector_bytes: bytes


@dataclass(frozen=True)
class PreparedStrategy:
    strategy: str
    embedding_path: Path
    chunk_path: Path
    collection_name: str
    embedding_sha256: str
    chunk_sha256: str
    run_metadata: dict[str, Any]
    collection_metadata: dict[str, Any]
    expected_points: dict[str, ExpectedPoint]
    sample_point_id: str
    sample_vector: list[float]
    sample_issuer: str


def _sha256_file(path: Path) -> str:
    return _file_sha256(path)


def deterministic_point_id(chunk_id: str) -> str:
    """Map the stable string chunk ID to Qdrant's accepted UUID ID format."""
    if not isinstance(chunk_id, str) or not chunk_id:
        raise IndexingError("chunk_id must be a non-empty string.")
    return str(uuid.uuid5(POINT_ID_NAMESPACE, chunk_id))


def _read_sidecar(path: Path) -> dict[str, Any]:
    try:
        metadata = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IndexingError(f"Cannot read embedding metadata {path}: {exc}") from exc
    if not isinstance(metadata, dict):
        raise IndexingError(f"Embedding metadata must be an object: {path}")
    return metadata


def _source_chunk_inventory(
    chunk_path: Path, strategy: str
) -> tuple[str, dict[str, str]]:
    if not chunk_path.is_file():
        raise FileNotFoundError(f"Source chunk file not found: {chunk_path}")
    file_hash = _sha256_file(chunk_path)
    source_hashes: dict[str, str] = {}
    errors: list[str] = []
    for line_number, record in enumerate(_read_jsonl(chunk_path), 1):
        chunk_id = record.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            errors.append(f"line {line_number}: missing chunk_id")
            continue
        if chunk_id in source_hashes:
            errors.append(f"line {line_number}: duplicate chunk_id {chunk_id}")
        if record.get("chunking_strategy") != strategy:
            errors.append(
                f"line {line_number} ({chunk_id}): strategy is "
                f"{record.get('chunking_strategy')!r}, expected {strategy!r}"
            )
        source_hashes[chunk_id] = _canonical_sha256(record)
    if errors:
        raise IndexingError(
            f"Chunk source validation failed for {chunk_path}: "
            + "; ".join(errors[:10])
        )
    if not source_hashes:
        raise IndexingError(f"No source chunks found in {chunk_path}.")
    if _sha256_file(chunk_path) != file_hash:
        raise IndexingError(f"Source chunks changed during validation: {chunk_path}")
    return file_hash, source_hashes


def _collection_metadata(
    strategy: str,
    embedding_sha256: str,
    chunk_sha256: str,
    count: int,
    run_metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "policylens_schema_version": 1,
        "chunking_strategy": strategy,
        "source_embedding_sha256": embedding_sha256,
        "source_chunk_sha256": chunk_sha256,
        "expected_point_count": count,
        "embedding_model": run_metadata["embedding_model"],
        "model_revision": run_metadata["model_revision"],
        "embedding_dimensions": run_metadata["embedding_dimensions"],
        "embedding_config_sha256": _canonical_sha256(
            run_metadata["embedding_config"]
        ),
    }


def _prepare_strategy(
    embedding_path: Path,
    chunk_path: Path,
    strategy: str,
    collection_name: str,
) -> PreparedStrategy:
    if strategy not in STRATEGIES:
        raise IndexingError(f"Unsupported strategy: {strategy!r}")
    if not embedding_path.is_file():
        raise FileNotFoundError(f"Embedding file not found: {embedding_path}")

    embedding_sha256 = _sha256_file(embedding_path)
    chunk_sha256, source_hashes = _source_chunk_inventory(chunk_path, strategy)
    sidecar_path = embedding_path.with_suffix(embedding_path.suffix + ".meta.json")
    run_metadata = _read_sidecar(sidecar_path)
    if run_metadata.get("chunking_strategy") != strategy:
        raise IndexingError(
            f"{sidecar_path} strategy does not match {strategy!r}."
        )
    if run_metadata.get("source_input_sha256") != chunk_sha256:
        raise IndexingError(
            f"Original chunk hash does not match embedding provenance for "
            f"{strategy}: {chunk_path}"
        )
    if run_metadata.get("embedding_model") != MODEL_NAME:
        raise IndexingError(
            f"Unexpected embedding model in {sidecar_path}: "
            f"{run_metadata.get('embedding_model')!r}"
        )
    if run_metadata.get("model_revision") != MODEL_REVISION:
        raise IndexingError(
            f"Unexpected model revision in {sidecar_path}: "
            f"{run_metadata.get('model_revision')!r}"
        )
    if run_metadata.get("embedding_dimensions") != EMBEDDING_DIMENSIONS:
        raise IndexingError(
            f"Unexpected embedding dimensions in {sidecar_path}: "
            f"{run_metadata.get('embedding_dimensions')!r}"
        )
    embedding_config = run_metadata.get("embedding_config")
    if not isinstance(embedding_config, dict):
        raise IndexingError(f"Missing embedding configuration in {sidecar_path}.")

    expected_points: dict[str, ExpectedPoint] = {}
    seen_chunk_ids: set[str] = set()
    seen_point_ids: set[str] = set()
    sample_point_id = ""
    sample_vector: list[float] = []
    sample_issuer = ""
    errors: list[str] = []

    for line_number, record in enumerate(_read_jsonl(embedding_path), 1):
        chunk_id = record.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            errors.append(f"line {line_number}: missing chunk_id")
            continue
        if chunk_id in seen_chunk_ids:
            errors.append(f"line {line_number}: duplicate chunk_id {chunk_id}")
        seen_chunk_ids.add(chunk_id)
        if chunk_id not in source_hashes:
            errors.append(f"line {line_number}: no source chunk for {chunk_id}")
            continue
        point_id = deterministic_point_id(chunk_id)
        if point_id in seen_point_ids:
            errors.append(f"line {line_number}: point ID collision for {chunk_id}")
        seen_point_ids.add(point_id)
        vector = record.get("embedding")
        try:
            valid_vector = validate_embedding(vector)
        except (EmbeddingError, TypeError, ValueError) as exc:
            errors.append(f"line {line_number} ({chunk_id}): invalid vector: {exc}")
            continue
        if record.get("source_chunk_id") != chunk_id:
            errors.append(f"line {line_number} ({chunk_id}): source ID mismatch")
        if record.get("source_chunk_sha256") != source_hashes[chunk_id]:
            errors.append(
                f"line {line_number} ({chunk_id}): source chunk hash mismatch"
            )
        if record.get("source_input_sha256") != chunk_sha256:
            errors.append(
                f"line {line_number} ({chunk_id}): source input hash mismatch"
            )
        if record.get("chunking_strategy") != strategy:
            errors.append(
                f"line {line_number} ({chunk_id}): strategy mismatch"
            )
        if record.get("embedding_model") != MODEL_NAME:
            errors.append(
                f"line {line_number} ({chunk_id}): embedding model mismatch"
            )
        if record.get("model_revision") != MODEL_REVISION:
            errors.append(
                f"line {line_number} ({chunk_id}): model revision mismatch"
            )
        if record.get("embedding_dimensions") != EMBEDDING_DIMENSIONS:
            errors.append(
                f"line {line_number} ({chunk_id}): dimension metadata mismatch"
            )
        if record.get("embedding_status") != "completed":
            errors.append(f"line {line_number} ({chunk_id}): not completed")
        if record.get("normalized") is not True:
            errors.append(f"line {line_number} ({chunk_id}): not normalized")
        if record.get("embedding_config") != embedding_config:
            errors.append(f"line {line_number} ({chunk_id}): config mismatch")
        if not isinstance(record.get("doc_id"), str) or not record["doc_id"]:
            errors.append(f"line {line_number} ({chunk_id}): missing doc_id")
        if not isinstance(record.get("text"), str) or not record["text"].strip():
            errors.append(f"line {line_number} ({chunk_id}): missing chunk text")
        issuer = record.get("issuer")
        if not isinstance(issuer, str) or not issuer.strip():
            errors.append(f"line {line_number} ({chunk_id}): missing issuer")
        page_start = record.get("page_start")
        page_end = record.get("page_end")
        if (
            not isinstance(page_start, int)
            or             not isinstance(page_end, int)
            or page_start < 1
            or page_end < page_start
        ):
            errors.append(f"line {line_number} ({chunk_id}): invalid page range")

        payload = {key: value for key, value in record.items() if key != "embedding"}
        try:
            payload_sha256 = _canonical_sha256(payload)
        except (TypeError, ValueError) as exc:
            errors.append(f"line {line_number} ({chunk_id}): invalid payload: {exc}")
            continue
        expected_points[point_id] = ExpectedPoint(
            chunk_id=chunk_id,
            payload_sha256=payload_sha256,
            vector_bytes=struct.pack(f"<{len(valid_vector)}f", *valid_vector),
        )
        if not sample_point_id:
            sample_point_id = point_id
            sample_vector = valid_vector
            sample_issuer = issuer if isinstance(issuer, str) else ""

    missing_embeddings = set(source_hashes).difference(seen_chunk_ids)
    if missing_embeddings:
        errors.append(
            f"{len(missing_embeddings)} source chunk IDs have no embedding"
        )
    if len(seen_chunk_ids) != len(source_hashes):
        errors.append(
            f"chunk/embedding record count differs: {len(source_hashes)} chunks, "
            f"{len(seen_chunk_ids)} embedding IDs"
        )
    if _sha256_file(embedding_path) != embedding_sha256:
        errors.append(f"embedding file changed during validation: {embedding_path}")
    if errors:
        raise IndexingError(
            f"Embedding preflight failed for {strategy}: "
            + "; ".join(errors[:20])
        )

    collection_metadata = _collection_metadata(
        strategy,
        embedding_sha256,
        chunk_sha256,
        len(expected_points),
        run_metadata,
    )
    return PreparedStrategy(
        strategy=strategy,
        embedding_path=embedding_path,
        chunk_path=chunk_path,
        collection_name=collection_name,
        embedding_sha256=embedding_sha256,
        chunk_sha256=chunk_sha256,
        run_metadata=run_metadata,
        collection_metadata=collection_metadata,
        expected_points=expected_points,
        sample_point_id=sample_point_id,
        sample_vector=sample_vector,
        sample_issuer=sample_issuer,
    )


def _ensure_store_marker(storage_dir: Path) -> None:
    storage_dir.mkdir(parents=True, exist_ok=True)
    marker_path = storage_dir / STORE_MARKER_NAME
    if marker_path.exists():
        try:
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise IndexingError(
                f"Cannot read Qdrant store marker {marker_path}: {exc}"
            ) from exc
        if marker != STORE_MARKER:
            raise IndexingError(
                f"Qdrant storage path has an unexpected marker: {marker_path}"
            )
        return
    existing = [path.name for path in storage_dir.iterdir()]
    if existing:
        raise IndexingError(
            f"Refusing to use non-empty Qdrant path without a PolicyLens marker: "
            f"{storage_dir} ({', '.join(existing[:10])})"
        )
    try:
        with marker_path.open("x", encoding="utf-8") as marker_file:
            json.dump(STORE_MARKER, marker_file, sort_keys=True)
            marker_file.write("\n")
            marker_file.flush()
            os.fsync(marker_file.fileno())
    except OSError as exc:
        raise IndexingError(
            f"Cannot create PolicyLens Qdrant marker {marker_path}: {exc}"
        ) from exc


def _assert_collection(
    client: QdrantClient, prepared: PreparedStrategy, create: bool
) -> None:
    names = {item.name for item in client.get_collections().collections}
    if prepared.collection_name not in names:
        if not create:
            raise IndexingError(
                f"Missing Qdrant collection {prepared.collection_name!r}."
            )
        client.create_collection(
            collection_name=prepared.collection_name,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIMENSIONS,
                distance=models.Distance.COSINE,
            ),
            metadata=prepared.collection_metadata,
        )

    info = client.get_collection(prepared.collection_name)
    if info.config.metadata != prepared.collection_metadata:
        raise IndexingError(
            f"Collection {prepared.collection_name!r} has unexpected or stale "
            f"metadata. It is preserved; use a new versioned storage path for "
            "changed source data."
        )
    vector_config = info.config.params.vectors
    if not isinstance(vector_config, models.VectorParams):
        raise IndexingError(
            f"Collection {prepared.collection_name!r} has unexpected named "
            "vector configuration."
        )
    if (
        vector_config.size != EMBEDDING_DIMENSIONS
        or vector_config.distance != models.Distance.COSINE
    ):
        raise IndexingError(
            f"Collection {prepared.collection_name!r} must use "
            f"{EMBEDDING_DIMENSIONS}-dimensional cosine vectors."
        )

def _validate_point(
    point: Any, prepared: PreparedStrategy
) -> str:
    point_id = str(point.id)
    expected = prepared.expected_points.get(point_id)
    if expected is None:
        raise IndexingError(
            f"Unexpected point ID {point_id} in {prepared.collection_name}."
        )
    payload = point.payload
    if not isinstance(payload, dict):
        raise IndexingError(f"Point {point_id} has no metadata payload.")
    if _canonical_sha256(payload) != expected.payload_sha256:
        raise IndexingError(
            f"Payload mismatch for chunk {expected.chunk_id} in "
            f"{prepared.collection_name}."
        )
    if payload.get("chunk_id") != expected.chunk_id:
        raise IndexingError(f"Chunk ID mismatch in payload for point {point_id}.")
    if payload.get("chunking_strategy") != prepared.strategy:
        raise IndexingError(f"Strategy mismatch in payload for point {point_id}.")
    if not isinstance(payload.get("text"), str) or not payload["text"].strip():
        raise IndexingError(f"Missing source text in payload for point {point_id}.")
    if not isinstance(payload.get("doc_id"), str) or not payload["doc_id"]:
        raise IndexingError(f"Missing doc_id in payload for point {point_id}.")
    if not isinstance(payload.get("issuer"), str) or not payload["issuer"]:
        raise IndexingError(f"Missing issuer in payload for point {point_id}.")
    if not isinstance(payload.get("page_start"), int) or not isinstance(
        payload.get("page_end"), int
    ) or payload["page_start"] < 1 or payload["page_end"] < payload["page_start"]:
        raise IndexingError(f"Missing page range in payload for point {point_id}.")
    vector = point.vector
    if not isinstance(vector, list) or len(vector) != EMBEDDING_DIMENSIONS:
        raise IndexingError(
            f"Point {point_id} does not contain a {EMBEDDING_DIMENSIONS}-dimensional vector."
        )
    if not all(math.isfinite(float(value)) for value in vector):
        raise IndexingError(f"Point {point_id} has non-finite vector values.")
    norm = math.sqrt(sum(float(value) ** 2 for value in vector))
    if abs(norm - 1.0) > VECTOR_NORM_TOLERANCE:
        raise IndexingError(
            f"Point {point_id} vector norm {norm:.8f} is not normalized."
        )
    source_vector = struct.unpack(
        f"<{EMBEDDING_DIMENSIONS}f", expected.vector_bytes
    )
    dot_product = sum(
        float(stored) * float(source)
        for stored, source in zip(vector, source_vector, strict=True)
    )
    source_norm = math.sqrt(sum(float(value) ** 2 for value in source_vector))
    if dot_product / source_norm < MIN_VECTOR_COSINE:
        raise IndexingError(
            f"Stored vector direction differs from source embedding for "
            f"{expected.chunk_id}."
        )
    return point_id


def _scroll_points(
    client: QdrantClient, collection_name: str
) -> Iterator[Any]:
    offset: Any = None
    while True:
        points, offset = client.scroll(
            collection_name=collection_name,
            limit=SCROLL_PAGE_SIZE,
            offset=offset,
            with_payload=True,
            with_vectors=True,
        )
        yield from points
        if offset is None:
            break


def _audit_existing_points(
    client: QdrantClient, prepared: PreparedStrategy
) -> set[str]:
    existing_ids: set[str] = set()
    for point in _scroll_points(client, prepared.collection_name):
        point_id = _validate_point(point, prepared)
        if point_id in existing_ids:
            raise IndexingError(
                f"Duplicate point ID {point_id} in {prepared.collection_name}."
            )
        existing_ids.add(point_id)
    return existing_ids


def _iter_batches(
    records: Iterator[dict[str, Any]],
    prepared: PreparedStrategy,
    existing_ids: set[str],
    batch_size: int,
) -> Iterator[tuple[list[models.PointStruct], int]]:
    batch: list[models.PointStruct] = []
    skipped = 0
    for record in records:
        point_id = deterministic_point_id(record["chunk_id"])
        if point_id in existing_ids:
            skipped += 1
            continue
        vector = validate_embedding(record["embedding"])
        payload = {
            key: value for key, value in record.items() if key != "embedding"
        }
        batch.append(
            models.PointStruct(id=point_id, vector=vector, payload=payload)
        )
        if len(batch) >= batch_size:
            yield batch, skipped
            batch = []
            skipped = 0
    if batch or skipped:
        yield batch, skipped


def _validate_collection(
    client: QdrantClient, prepared: PreparedStrategy
) -> dict[str, Any]:
    _assert_collection(client, prepared, create=False)
    info = client.get_collection(prepared.collection_name)
    expected_count = len(prepared.expected_points)
    actual_count = client.count(
        collection_name=prepared.collection_name, exact=True
    ).count
    if actual_count != expected_count:
        raise IndexingError(
            f"{prepared.collection_name} has {actual_count} points; "
            f"expected {expected_count}."
        )
    seen_ids = _audit_existing_points(client, prepared)
    expected_ids = set(prepared.expected_points)
    missing_ids = expected_ids.difference(seen_ids)
    extra_ids = seen_ids.difference(expected_ids)
    if missing_ids or extra_ids or len(seen_ids) != expected_count:
        raise IndexingError(
            f"Point ID validation failed for {prepared.collection_name}: "
            f"{len(missing_ids)} missing, {len(extra_ids)} extra."
        )

    filtered = client.query_points(
        collection_name=prepared.collection_name,
        query=prepared.sample_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="issuer",
                    match=models.MatchValue(value=prepared.sample_issuer),
                )
            ]
        ),
        with_payload=True,
        limit=min(10, expected_count),
    ).points
    if not filtered or all(
        point.id != prepared.sample_point_id for point in filtered
    ):
        raise IndexingError(
            f"Issuer filter did not return the expected sample in "
            f"{prepared.collection_name}."
        )
    if any(point.payload.get("issuer") != prepared.sample_issuer for point in filtered):
        raise IndexingError(
            f"Issuer filter returned a mismatched payload in "
            f"{prepared.collection_name}."
        )
    if any(
        not point.payload.get("doc_id")
        or point.payload.get("page_start") is None
        or point.payload.get("page_end") is None
        for point in filtered
    ):
        raise IndexingError(
            f"Filtered citation metadata is incomplete in "
            f"{prepared.collection_name}."
        )

    return {
        "collection_name": prepared.collection_name,
        "expected_points": expected_count,
        "actual_points": actual_count,
        "validated_point_ids": len(seen_ids),
        "missing_point_ids": 0,
        "extra_point_ids": 0,
        "embedding_dimensions": info.config.params.vectors.size,
        "distance": info.config.params.vectors.distance.value,
        "strategy": prepared.strategy,
        "issuer_filter_sample_count": len(filtered),
        "issuer_filter_sample_issuer": prepared.sample_issuer,
    }


def _index_prepared(
    client: QdrantClient,
    prepared: PreparedStrategy,
    batch_size: int,
) -> dict[str, Any]:
    _assert_collection(client, prepared, create=True)
    existing_ids = _audit_existing_points(client, prepared)
    embedded_count = 0
    skipped_count = 0
    started = time.perf_counter()
    batch_number = 0
    for batch, skipped in _iter_batches(
        _read_jsonl(prepared.embedding_path),
        prepared,
        existing_ids,
        batch_size,
    ):
        skipped_count += skipped
        if batch:
            client.upsert(
                collection_name=prepared.collection_name,
                points=batch,
                wait=True,
            )
            embedded_count += len(batch)
            batch_number += 1
            logger.info(
                "%s: indexed %d/%d points in %d batches",
                prepared.strategy,
                embedded_count,
                len(prepared.expected_points) - len(existing_ids),
                batch_number,
            )
    if _sha256_file(prepared.embedding_path) != prepared.embedding_sha256:
        raise IndexingError(
            f"Embedding file changed while indexing {prepared.strategy}."
        )
    if _sha256_file(prepared.chunk_path) != prepared.chunk_sha256:
        raise IndexingError(
            f"Chunk source changed while indexing {prepared.strategy}."
        )
    actual_count = client.count(
        collection_name=prepared.collection_name, exact=True
    ).count
    if actual_count != len(prepared.expected_points):
        raise IndexingError(
            f"After indexing {prepared.strategy}, collection has {actual_count} "
            f"points; expected {len(prepared.expected_points)}."
        )
    return {
        "strategy": prepared.strategy,
        "collection_name": prepared.collection_name,
        "expected_points": len(prepared.expected_points),
        "indexed_this_run": embedded_count,
        "skipped_valid_existing": skipped_count,
        "points_before_run": len(existing_ids),
        "points_after_run": actual_count,
        "batch_size": batch_size,
        "batch_count": batch_number,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "embedding_file_sha256": prepared.embedding_sha256,
        "chunk_file_sha256": prepared.chunk_sha256,
    }


def _prepare_corpus(
    embedding_dir: Path, chunk_dir: Path
) -> dict[str, PreparedStrategy]:
    prepared: dict[str, PreparedStrategy] = {}
    if len(set(COLLECTION_NAMES.values())) != len(COLLECTION_NAMES):
        raise IndexingError("Qdrant collection names must be distinct.")
    for strategy in STRATEGIES:
        prepared[strategy] = _prepare_strategy(
            embedding_dir / f"{strategy}.jsonl",
            chunk_dir / f"{strategy}.jsonl",
            strategy,
            COLLECTION_NAMES[strategy],
        )
        expected = EXPECTED_COUNTS[strategy]
        if len(prepared[strategy].expected_points) != expected:
            raise IndexingError(
                f"{strategy} has {len(prepared[strategy].expected_points)} valid "
                f"records; expected exactly {expected}."
            )
    return prepared


def index_corpus(
    embedding_dir: Path = DEFAULT_EMBEDDING_DIR,
    chunk_dir: Path = DEFAULT_CHUNK_DIR,
    storage_dir: Path = QDRANT_STORAGE_DIR,
    batch_size: int = BATCH_SIZE,
) -> dict[str, Any]:
    """Index both strategies, then close, reopen, and independently validate."""
    if batch_size < 1 or batch_size > 256:
        raise ValueError("batch_size must be between 1 and 256.")
    embedding_dir = Path(embedding_dir)
    chunk_dir = Path(chunk_dir)
    storage_dir = Path(storage_dir)
    prepared = _prepare_corpus(embedding_dir, chunk_dir)
    _ensure_store_marker(storage_dir)

    summary: dict[str, Any] = {
        "status": "indexing",
        "storage_dir": str(storage_dir),
        "qdrant_client_version": importlib.metadata.version("qdrant-client"),
        "embedding_model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "distance": "Cosine",
        "batch_size": batch_size,
        "expected_total_points": sum(
            len(item.expected_points) for item in prepared.values()
        ),
        "strategies": {},
        "validation": {},
        "persistence_reopened": False,
    }
    started = time.perf_counter()
    client: QdrantClient | None = None
    try:
        client = QdrantClient(path=str(storage_dir))
        for strategy in STRATEGIES:
            summary["strategies"][strategy] = _index_prepared(
                client, prepared[strategy], batch_size
            )
    except Exception as exc:
        summary["status"] = "failed"
        summary["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        if client is not None:
            client.close()

    reopened = QdrantClient(path=str(storage_dir))
    try:
        summary["persistence_reopened"] = True
        for strategy in STRATEGIES:
            summary["validation"][strategy] = _validate_collection(
                reopened, prepared[strategy]
            )
    finally:
        reopened.close()

    for strategy in STRATEGIES:
        if _sha256_file(prepared[strategy].embedding_path) != prepared[
            strategy
        ].embedding_sha256:
            raise IndexingError(
                f"Embedding input changed during post-index validation: {strategy}"
            )
        if _sha256_file(prepared[strategy].chunk_path) != prepared[
            strategy
        ].chunk_sha256:
            raise IndexingError(
                f"Chunk input changed during post-index validation: {strategy}"
            )
    summary["status"] = "completed"
    summary["total_elapsed_seconds"] = round(time.perf_counter() - started, 3)
    return summary


def index_strategy(
    embedding_path: Path,
    chunk_path: Path,
    storage_dir: Path,
    strategy: str,
    collection_name: str,
    batch_size: int = BATCH_SIZE,
) -> dict[str, Any]:
    """Index and independently validate one strategy; useful for isolated tests."""
    if batch_size < 1 or batch_size > 256:
        raise ValueError("batch_size must be between 1 and 256.")
    prepared = _prepare_strategy(
        Path(embedding_path),
        Path(chunk_path),
        strategy,
        collection_name,
    )
    storage_dir = Path(storage_dir)
    _ensure_store_marker(storage_dir)
    client = QdrantClient(path=str(storage_dir))
    try:
        result = _index_prepared(client, prepared, batch_size)
    finally:
        client.close()
    reopened = QdrantClient(path=str(storage_dir))
    try:
        result["validation"] = _validate_collection(reopened, prepared)
        result["persistence_reopened"] = True
    finally:
        reopened.close()
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Index existing PolicyLens embedding JSONL files into Qdrant."
    )
    parser.add_argument("--embedding-dir", type=Path, default=DEFAULT_EMBEDDING_DIR)
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--storage-dir", type=Path, default=QDRANT_STORAGE_DIR)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = parser.parse_args(argv)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(LOGS_DIR / "qdrant_indexing.log", encoding="utf-8"),
        ],
    )
    try:
        summary = index_corpus(
            args.embedding_dir,
            args.chunk_dir,
            args.storage_dir,
            args.batch_size,
        )
    except (IndexingError, FileNotFoundError, OSError, ValueError) as exc:
        logger.error("%s", exc)
        return 1
    for strategy, validation in summary["validation"].items():
        logger.info(
            "%s: %d/%d points validated in %s",
            strategy,
            validation["actual_points"],
            validation["expected_points"],
            validation["collection_name"],
        )
    logger.info(
        "Qdrant indexing completed in %.3f seconds.",
        summary["total_elapsed_seconds"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

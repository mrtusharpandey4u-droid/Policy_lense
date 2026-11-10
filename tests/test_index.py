from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path
from typing import Any

import pytest
from qdrant_client import QdrantClient, models

from src import index
from src.embed import EMBEDDING_DIMENSIONS, MODEL_NAME, MODEL_REVISION, _canonical_sha256


EMBEDDING_CONFIG = {
    "device": "mps",
    "batch_size": 1,
    "precision": "float32",
    "normalize_embeddings": True,
    "normalization_tolerance": 1e-4,
    "prompt": None,
}


def _source_chunk(strategy: str, position: int) -> dict[str, Any]:
    return {
        "chunk_id": f"synthetic_{strategy}_{position:04d}",
        "doc_id": f"synthetic_doc_{position:04d}",
        "title": "Synthetic lending policy",
        "issuer": "Synthetic Regulator" if position == 1 else "Other Regulator",
        "issue_date": "2025-01-01",
        "page_start": position,
        "page_end": position + 1,
        "section_title": "Lending",
        "source_hash": "source-pdf-hash",
        "chunking_strategy": strategy,
        "text": f"Synthetic text for {strategy} chunk {position}.",
        "tables": [
            {
                "headers": ["Policy", "Value"],
                "rows": [[f"Requirement {position}", "synthetic"]],
            }
        ],
        "page_provenance": [
            {
                "page_number": position,
                "text_source": "native",
                "cleaning_review": position == 1,
                "ocr_provenance": {"language": "eng+hin"},
            }
        ],
        "contains_ocr": False,
        "has_cleaning_review": position == 1,
        "review_pages": [position] if position == 1 else [],
    }


def _write_inputs(
    root: Path, strategy: str, count: int = 2
) -> tuple[Path, Path, list[dict[str, Any]]]:
    chunk_dir = root / "chunks"
    embedding_dir = root / "embeddings"
    chunk_dir.mkdir(parents=True)
    embedding_dir.mkdir(parents=True)
    chunk_path = chunk_dir / f"{strategy}.jsonl"
    embedding_path = embedding_dir / f"{strategy}.jsonl"
    chunks = [_source_chunk(strategy, position + 1) for position in range(count)]
    chunk_text = "".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
        for record in chunks
    )
    chunk_path.write_text(chunk_text, encoding="utf-8")
    chunk_sha256 = hashlib.sha256(chunk_path.read_bytes()).hexdigest()

    records = []
    for position, chunk in enumerate(chunks):
        vector = [0.0] * EMBEDDING_DIMENSIONS
        vector[position] = 1.0
        record = {
            **chunk,
            "embedding": vector,
            "embedding_model": MODEL_NAME,
            "model_revision": MODEL_REVISION,
            "embedding_dimensions": EMBEDDING_DIMENSIONS,
            "normalized": True,
            "embedding_config": EMBEDDING_CONFIG,
            "embedding_status": "completed",
            "source_chunk_id": chunk["chunk_id"],
            "source_chunk_sha256": _canonical_sha256(chunk),
            "source_input_sha256": chunk_sha256,
        }
        records.append(record)
    embedding_path.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            for record in records
        ),
        encoding="utf-8",
    )
    sidecar = {
        "schema_version": 1,
        "chunking_strategy": strategy,
        "source_input_sha256": chunk_sha256,
        "embedding_model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "embedding_config": EMBEDDING_CONFIG,
    }
    embedding_path.with_suffix(embedding_path.suffix + ".meta.json").write_text(
        json.dumps(sidecar), encoding="utf-8"
    )
    return embedding_path, chunk_path, records


def test_point_ids_are_stable_and_derived_from_chunk_ids():
    chunk_id = "doc_001_fixed_size_00001_hash"
    point_id = index.deterministic_point_id(chunk_id)

    assert point_id == index.deterministic_point_id(chunk_id)
    assert uuid.UUID(point_id).version == 5
    assert point_id != index.deterministic_point_id(chunk_id + "_different")
    with pytest.raises(index.IndexingError, match="non-empty string"):
        index.deterministic_point_id("")


@pytest.mark.parametrize("strategy", ["fixed_size", "structure_aware"])
def test_index_creation_payload_filter_and_idempotent_resume(tmp_path, strategy):
    embedding_path, chunk_path, source_records = _write_inputs(tmp_path, strategy)
    storage_dir = tmp_path / "vector-store"
    collection_name = f"synthetic_{strategy}"

    first = index.index_strategy(
        embedding_path, chunk_path, storage_dir, strategy, collection_name
    )
    assert first["indexed_this_run"] == 2
    assert first["points_after_run"] == 2
    assert first["persistence_reopened"] is True
    assert first["validation"]["distance"] == "Cosine"
    assert first["validation"]["embedding_dimensions"] == EMBEDDING_DIMENSIONS
    assert first["validation"]["issuer_filter_sample_count"] >= 1

    client = QdrantClient(path=str(storage_dir))
    try:
        info = client.get_collection(collection_name)
        assert info.config.params.vectors.size == EMBEDDING_DIMENSIONS
        assert info.config.params.vectors.distance == models.Distance.COSINE
        assert client.count(collection_name, exact=True).count == 2
        target = index.deterministic_point_id(source_records[0]["chunk_id"])
        stored = client.retrieve(
            collection_name,
            ids=[target],
            with_payload=True,
            with_vectors=True,
        )[0]
        expected_payload = {
            key: value
            for key, value in source_records[0].items()
            if key != "embedding"
        }
        assert stored.payload == expected_payload
        assert stored.vector == source_records[0]["embedding"]
    finally:
        client.close()

    second = index.index_strategy(
        embedding_path, chunk_path, storage_dir, strategy, collection_name
    )
    assert second["indexed_this_run"] == 0
    assert second["skipped_valid_existing"] == 2
    assert second["points_before_run"] == 2
    assert second["points_after_run"] == 2


def test_changed_source_is_rejected_without_overwriting_existing_index(tmp_path):
    embedding_path, chunk_path, _ = _write_inputs(tmp_path, "fixed_size")
    storage_dir = tmp_path / "vector-store"
    collection_name = "synthetic_fixed_size"
    index.index_strategy(
        embedding_path, chunk_path, storage_dir, "fixed_size", collection_name
    )

    chunks = [
        json.loads(line)
        for line in chunk_path.read_text(encoding="utf-8").splitlines()
    ]
    chunks[0]["text"] += " changed"
    chunk_path.write_text(
        "".join(json.dumps(item) + "\n" for item in chunks), encoding="utf-8"
    )
    with pytest.raises(index.IndexingError, match="Original chunk hash"):
        index.index_strategy(
            embedding_path, chunk_path, storage_dir, "fixed_size", collection_name
        )

    client = QdrantClient(path=str(storage_dir))
    try:
        assert client.count(collection_name, exact=True).count == 2
    finally:
        client.close()


def test_unmarked_nonempty_storage_is_not_reused(tmp_path):
    storage_dir = tmp_path / "vector-store"
    storage_dir.mkdir()
    (storage_dir / "unrelated.txt").write_text("keep", encoding="utf-8")
    with pytest.raises(index.IndexingError, match="non-empty Qdrant path"):
        index._ensure_store_marker(storage_dir)
    assert (storage_dir / "unrelated.txt").read_text(encoding="utf-8") == "keep"

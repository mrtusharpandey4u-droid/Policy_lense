from __future__ import annotations

import importlib.metadata
import time
from pathlib import Path
from typing import Any

import pytest

qdrant_client = pytest.importorskip("qdrant_client")

from qdrant_client import QdrantClient, models


COLLECTION_NAME = "policylens_synthetic_preflight"
VECTOR_SIZE = 1024
TARGET_ID = "54c3888b-7863-5d4c-9a7e-3c9f12002002"
OTHER_ID = "54c3888b-7863-5d4c-9a7e-3c9f12002003"


def _unit_vector(position: int) -> list[float]:
    vector = [0.0] * VECTOR_SIZE
    vector[position] = 1.0
    return vector


def _run_synthetic_preflight(storage_path: Path) -> dict[str, Any]:
    target_vector = _unit_vector(0)
    target_payload = {
        "chunk_id": "synthetic-policy-chunk-001",
        "doc_id": "synthetic-doc-001",
        "issuer": "Synthetic Financial Regulator",
        "page_start": 4,
        "page_end": 5,
        "page_provenance": [
            {
                "page_number": 4,
                "text_source": "synthetic",
                "ocr_provenance": {"languages": ["eng", "hin"]},
            }
        ],
        "tables": [
            {
                "headers": ["Requirement", "Threshold"],
                "rows": [["Synthetic lending test", "42"]],
            }
        ],
    }

    started = time.perf_counter()
    client = QdrantClient(path=str(storage_path))
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=TARGET_ID,
                    vector=target_vector,
                    payload=target_payload,
                ),
                models.PointStruct(
                    id=OTHER_ID,
                    vector=target_vector,
                    payload={
                        "chunk_id": "synthetic-policy-chunk-002",
                        "doc_id": "synthetic-doc-002",
                        "issuer": "Another Synthetic Issuer",
                        "page_start": 1,
                        "page_end": 1,
                    },
                ),
            ],
            wait=True,
        )

        collection_info = client.get_collection(COLLECTION_NAME)
        vector_config = collection_info.config.params.vectors
        assert vector_config.size == VECTOR_SIZE
        assert vector_config.distance == models.Distance.COSINE
        assert client.count(COLLECTION_NAME, exact=True).count == 2

        filtered = client.query_points(
            collection_name=COLLECTION_NAME,
            query=target_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="issuer",
                        match=models.MatchValue(
                            value="Synthetic Financial Regulator"
                        ),
                    )
                ]
            ),
            with_payload=True,
            limit=5,
        ).points
        assert len(filtered) == 1
        assert filtered[0].id == TARGET_ID
        assert filtered[0].score == pytest.approx(1.0, abs=1e-6)
        assert filtered[0].payload == target_payload

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=TARGET_ID,
                    vector=target_vector,
                    payload={**target_payload, "upsert_marker": "updated"},
                )
            ],
            wait=True,
        )
        assert client.count(COLLECTION_NAME, exact=True).count == 2
    finally:
        client.close()

    reopened_client = QdrantClient(path=str(storage_path))
    try:
        reopened_info = reopened_client.get_collection(COLLECTION_NAME)
        reopened_config = reopened_info.config.params.vectors
        assert reopened_config.size == VECTOR_SIZE
        assert reopened_config.distance == models.Distance.COSINE
        assert reopened_client.count(COLLECTION_NAME, exact=True).count == 2

        persisted = reopened_client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[TARGET_ID],
            with_payload=True,
            with_vectors=True,
        )
        assert len(persisted) == 1
        point = persisted[0]
        assert point.payload == {**target_payload, "upsert_marker": "updated"}
        assert len(point.vector) == VECTOR_SIZE
        assert point.vector == target_vector

        filtered_after_reopen = reopened_client.query_points(
            collection_name=COLLECTION_NAME,
            query=target_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="issuer",
                        match=models.MatchValue(
                            value="Synthetic Financial Regulator"
                        ),
                    )
                ]
            ),
            with_payload=True,
            limit=5,
        ).points
        assert [result.id for result in filtered_after_reopen] == [TARGET_ID]
    finally:
        reopened_client.close()

    return {
        "qdrant_client_version": importlib.metadata.version("qdrant-client"),
        "collection_name": COLLECTION_NAME,
        "vector_dimensions": VECTOR_SIZE,
        "distance": "Cosine",
        "point_count_after_repeated_upsert": 2,
        "issuer_filter_result_count": len(filtered_after_reopen),
        "nested_payload_round_trip": True,
        "persistence_reopen": True,
        "elapsed_seconds": time.perf_counter() - started,
    }


def test_persistent_local_collection_cosine_filter_and_nested_payload(
    tmp_path: Path,
) -> None:
    result = _run_synthetic_preflight(tmp_path / "qdrant-local")

    assert result["qdrant_client_version"] == "1.20.0"
    assert result["vector_dimensions"] == 1024
    assert result["distance"] == "Cosine"
    assert result["point_count_after_repeated_upsert"] == 2
    assert result["issuer_filter_result_count"] == 1
    assert result["nested_payload_round_trip"] is True
    assert result["persistence_reopen"] is True

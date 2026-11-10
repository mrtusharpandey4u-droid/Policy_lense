from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from qdrant_client import QdrantClient, models

from src import search
from src.config import QDRANT_FIXED_COLLECTION_NAME
from src.embed import EMBEDDING_DIMENSIONS, MODEL_NAME, MODEL_REVISION


class SyntheticModel:
    device = "mps"

    def __init__(self, vector: list[float] | None = None) -> None:
        self.vector = _unit_vector(0) if vector is None else vector
        self.calls: list[tuple[list[str], dict[str, Any]]] = []

    def encode(self, texts: list[str], **kwargs: Any) -> list[list[float]]:
        self.calls.append((texts, kwargs))
        return [self.vector]


def _unit_vector(position: int) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSIONS
    vector[position] = 1.0
    return vector


def _make_store(
    storage_dir: Path,
    collection: str = QDRANT_FIXED_COLLECTION_NAME,
    strategy: str = "fixed_size",
) -> None:
    storage_dir.mkdir(parents=True)
    (storage_dir / search.STORE_MARKER_NAME).write_text(
        json.dumps(search.STORE_MARKER), encoding="utf-8"
    )
    client = QdrantClient(path=str(storage_dir))
    try:
        client.create_collection(
            collection_name=collection,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIMENSIONS,
                distance=models.Distance.COSINE,
            ),
            metadata={
                "chunking_strategy": strategy,
                "embedding_model": MODEL_NAME,
                "model_revision": MODEL_REVISION,
                "embedding_dimensions": EMBEDDING_DIMENSIONS,
            },
        )
        client.upsert(
            collection_name=collection,
            points=[
                models.PointStruct(
                    id="00000000-0000-0000-0000-000000000001",
                    vector=_unit_vector(0),
                    payload={
                        "chunk_id": "rbi-chunk-1",
                        "doc_id": "rbi-doc",
                        "issuer": "Reserve Bank of India",
                        "page_start": 4,
                        "page_end": 5,
                        "chunking_strategy": strategy,
                        "text": "Policy about secured lending.",
                    },
                ),
                models.PointStruct(
                    id="00000000-0000-0000-0000-000000000002",
                    vector=_unit_vector(1),
                    payload={
                        "chunk_id": "other-chunk",
                        "doc_id": "other-doc",
                        "issuer": "Other Regulator",
                        "page_start": 9,
                        "page_end": 9,
                        "chunking_strategy": strategy,
                        "text": "Unrelated synthetic policy.",
                    },
                ),
            ],
            wait=True,
        )
    finally:
        client.close()


def test_query_embedding_matches_corpus_configuration() -> None:
    model = SyntheticModel()

    vector = search.embed_query(" secured loan limits ", model=model)

    assert vector == _unit_vector(0)
    assert model.calls == [
        (
            ["secured loan limits"],
            {
                "batch_size": 1,
                "show_progress_bar": False,
                "convert_to_numpy": True,
                "normalize_embeddings": True,
                "precision": "float32",
                "prompt": None,
            },
        )
    ]


@pytest.mark.parametrize(
    "vector",
    [
        [0.0] * EMBEDDING_DIMENSIONS,
        [float("nan")] + [0.0] * (EMBEDDING_DIMENSIONS - 1),
        [1.0],
        [2.0] + [0.0] * (EMBEDDING_DIMENSIONS - 1),
    ],
)
def test_query_embedding_rejects_invalid_vectors(vector: list[float]) -> None:
    with pytest.raises(search.SearchError, match="embedding validation"):
        search.embed_query("policy query", model=SyntheticModel(vector))


def test_retrieve_filters_rbi_alias_and_preserves_citation_metadata(
    tmp_path: Path,
) -> None:
    storage_dir = tmp_path / "qdrant"
    _make_store(storage_dir)

    results = search.retrieve(
        "secured loan limits",
        top_k=5,
        filters=search.parse_filters(["issuer=RBI"]),
        model=SyntheticModel(),
        storage_dir=storage_dir,
    )

    assert len(results) == 1
    assert results[0]["issuer"] == "Reserve Bank of India"
    assert results[0]["doc_id"] == "rbi-doc"
    assert results[0]["page_start"] == 4
    assert results[0]["page_end"] == 5
    assert results[0]["score"] == pytest.approx(1.0)


def test_retrieve_uses_structure_aware_collection_independently(
    tmp_path: Path,
) -> None:
    storage_dir = tmp_path / "qdrant"
    _make_store(
        storage_dir,
        collection=search.STRATEGY_COLLECTIONS["structure_aware"],
        strategy="structure_aware",
    )

    results = search.retrieve(
        "secured loan limits",
        top_k=1,
        strategy="structure_aware",
        model=SyntheticModel(),
        storage_dir=storage_dir,
    )

    assert len(results) == 1
    assert results[0]["chunking_strategy"] == "structure_aware"
    assert results[0]["chunk_id"] == "rbi-chunk-1"


def test_retrieve_accepts_a_validated_precomputed_query_vector(
    tmp_path: Path,
) -> None:
    storage_dir = tmp_path / "qdrant"
    _make_store(storage_dir)

    results = search.retrieve(
        "secured loan limits",
        top_k=1,
        query_vector=_unit_vector(0),
        storage_dir=storage_dir,
    )

    assert len(results) == 1
    assert results[0]["chunk_id"] == "rbi-chunk-1"
    with pytest.raises(search.SearchError, match="embedding validation"):
        search.retrieve(
            "secured loan limits",
            query_vector=[0.0] * EMBEDDING_DIMENSIONS,
            storage_dir=storage_dir,
        )


def test_pinned_query_model_is_loaded_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model = SyntheticModel()
    load_count = 0

    def load_model() -> SyntheticModel:
        nonlocal load_count
        load_count += 1
        return model

    monkeypatch.setattr(search, "_QUERY_MODEL", None)
    monkeypatch.setattr(search, "_load_model", load_model)

    search.embed_query("first query")
    search.embed_query("second query")

    assert load_count == 1
    assert len(model.calls) == 2


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ("issuer", "field=value"),
        ("issuer=", "must not be empty"),
        ("=RBI", "must not be empty"),
        ("title=policy", "Unsupported filter field"),
        ("issuer=RBI=extra", "field=value"),
    ],
)
def test_parse_filters_reports_invalid_syntax_and_fields(
    raw: str, message: str
) -> None:
    with pytest.raises(search.SearchError, match=message):
        search.parse_filters([raw])


def test_invalid_query_top_k_and_strategy_are_rejected_before_io(tmp_path: Path) -> None:
    with pytest.raises(search.SearchError, match="must not be empty"):
        search.retrieve("  ", storage_dir=tmp_path / "missing")
    with pytest.raises(search.SearchError, match="positive integer"):
        search.retrieve("query", top_k=0, storage_dir=tmp_path / "missing")
    with pytest.raises(search.SearchError, match="Invalid strategy"):
        search.retrieve("query", strategy="both", storage_dir=tmp_path / "missing")


def test_missing_database_and_collection_have_friendly_errors(tmp_path: Path) -> None:
    with pytest.raises(search.SearchError, match="database is missing"):
        search.retrieve("query", storage_dir=tmp_path / "missing")

    storage_dir = tmp_path / "empty-qdrant"
    _make_store(storage_dir, collection="not-the-fixed-collection")
    with pytest.raises(search.SearchError, match="collection .* is missing"):
        search.retrieve(
            "query",
            model=SyntheticModel(),
            storage_dir=storage_dir,
        )


def test_non_mps_model_is_rejected_without_fallback() -> None:
    model = SyntheticModel()
    model.device = "cpu"
    with pytest.raises(search.SearchError, match="requires the explicitly configured MPS"):
        search.embed_query("query", model=model)


def test_cli_help_is_available(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        search.main(["--help"])

    assert exc_info.value.code == 0
    assert "FIELD=VALUE" in capsys.readouterr().out

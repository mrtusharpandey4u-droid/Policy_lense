"""Local semantic search over the PolicyLens Qdrant collections."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping

from qdrant_client import QdrantClient, models

from src.config import (
    QDRANT_FIXED_COLLECTION_NAME,
    QDRANT_STORAGE_DIR,
    QDRANT_STRUCTURE_COLLECTION_NAME,
    RETRIEVE_TOP_K,
)
from src.embed import (
    EMBEDDING_DIMENSIONS,
    MODEL_NAME,
    MODEL_REVISION,
    EmbeddingError,
    _load_model,
    validate_embedding,
)

STRATEGY_COLLECTIONS = {
    "fixed_size": QDRANT_FIXED_COLLECTION_NAME,
    "structure_aware": QDRANT_STRUCTURE_COLLECTION_NAME,
}
STORE_MARKER_NAME = ".policylens_qdrant_store.json"
STORE_MARKER = {"format_version": 1, "store": "policylens_qdrant_local"}
FILTER_FIELDS = {"issuer"}
FILTER_ALIASES = {"rbi": "Reserve Bank of India"}

_QUERY_MODEL: Any | None = None


class SearchError(RuntimeError):
    """Raised when a local search cannot safely complete."""


def _validate_query(query: str) -> str:
    if not isinstance(query, str) or not query.strip():
        raise SearchError("Search query must not be empty.")
    return query.strip()


def _validate_top_k(top_k: int) -> int:
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
        raise SearchError("top_k must be a positive integer.")
    return top_k


def parse_filters(values: list[str] | None) -> dict[str, str]:
    """Parse supported exact-match filters from ``field=value`` arguments."""
    filters: dict[str, str] = {}
    for value in values or []:
        if not isinstance(value, str) or value.count("=") != 1:
            raise SearchError(
                f"Invalid filter {value!r}; use the form field=value, "
                "for example issuer=RBI."
            )
        field, filter_value = (part.strip() for part in value.split("=", 1))
        if not field or not filter_value:
            raise SearchError(
                f"Invalid filter {value!r}; field and value must not be empty."
            )
        if field not in FILTER_FIELDS:
            supported = ", ".join(sorted(FILTER_FIELDS))
            raise SearchError(
                f"Unsupported filter field {field!r}. Supported fields: {supported}."
            )
        normalized_value = FILTER_ALIASES.get(filter_value.casefold(), filter_value)
        if field in filters and filters[field] != normalized_value:
            raise SearchError(f"Conflicting values supplied for filter {field!r}.")
        filters[field] = normalized_value
    return filters


def _get_query_model() -> Any:
    global _QUERY_MODEL
    if _QUERY_MODEL is None:
        try:
            _QUERY_MODEL = _load_model()
        except EmbeddingError as exc:
            raise SearchError(f"Local BGE-M3 model is unavailable: {exc}") from exc
        except (ImportError, OSError, RuntimeError, ValueError) as exc:
            raise SearchError(f"Could not load the pinned local BGE-M3 model: {exc}") from exc
    return _QUERY_MODEL


def embed_query(query: str, model: Any | None = None) -> list[float]:
    """Encode a query with the corpus BGE-M3 snapshot and normalization."""
    query = _validate_query(query)
    active_model = model if model is not None else _get_query_model()
    device = str(getattr(active_model, "device", "")).split(
        ":", maxsplit=1
    )[0].lower()
    if device != "mps":
        raise SearchError(
            f"Query model is on {getattr(active_model, 'device', None)!r}; "
            "PolicyLens requires the explicitly configured MPS device."
        )
    try:
        encoded = active_model.encode(
            [query],
            batch_size=1,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
            precision="float32",
            prompt=None,
        )
        vector = validate_embedding(encoded[0])
    except EmbeddingError as exc:
        raise SearchError(f"Query embedding validation failed: {exc}") from exc
    except (IndexError, TypeError, ValueError, RuntimeError, OSError) as exc:
        raise SearchError(
            f"Could not encode the query with the pinned local BGE-M3 model: {exc}"
        ) from exc
    return vector


def _validate_storage(storage_dir: Path) -> None:
    marker_path = storage_dir / STORE_MARKER_NAME
    if not storage_dir.is_dir() or not marker_path.is_file():
        raise SearchError(
            f"Qdrant database is missing at {storage_dir}. Run "
            "`.venv/bin/python -m src.index` before searching."
        )
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SearchError(
            f"Cannot read Qdrant database marker {marker_path}: {exc}"
        ) from exc
    if marker != STORE_MARKER:
        raise SearchError(f"Unrecognized Qdrant database marker at {marker_path}.")


def _validate_collection(
    client: QdrantClient, collection_name: str, strategy: str
) -> None:
    names = {item.name for item in client.get_collections().collections}
    if collection_name not in names:
        raise SearchError(
            f"Qdrant collection {collection_name!r} is missing. Run "
            "`.venv/bin/python -m src.index` to build the indexes."
        )
    info = client.get_collection(collection_name)
    metadata = info.config.metadata or {}
    if (
        metadata.get("chunking_strategy") != strategy
        or metadata.get("embedding_model") != MODEL_NAME
        or metadata.get("model_revision") != MODEL_REVISION
        or metadata.get("embedding_dimensions") != EMBEDDING_DIMENSIONS
    ):
        raise SearchError(
            f"Collection {collection_name!r} does not match the pinned "
            "PolicyLens model, dimensions, or strategy."
        )
    vectors = info.config.params.vectors
    if (
        not isinstance(vectors, models.VectorParams)
        or vectors.size != EMBEDDING_DIMENSIONS
        or vectors.distance != models.Distance.COSINE
    ):
        raise SearchError(
            f"Collection {collection_name!r} must use "
            f"{EMBEDDING_DIMENSIONS}-dimensional cosine vectors."
        )


def retrieve(
    query: str,
    top_k: int = RETRIEVE_TOP_K,
    strategy: str = "fixed_size",
    filters: Mapping[str, str] | None = None,
    *,
    model: Any | None = None,
    query_vector: list[float] | None = None,
    storage_dir: Path = QDRANT_STORAGE_DIR,
) -> list[dict[str, Any]]:
    """Return cosine-ranked chunk payloads from one strategy collection."""
    query = _validate_query(query)
    top_k = _validate_top_k(top_k)
    if strategy not in STRATEGY_COLLECTIONS:
        raise SearchError(
            f"Invalid strategy {strategy!r}; choose fixed_size or structure_aware."
        )
    parsed_filters = parse_filters(
        [f"{field}={value}" for field, value in (filters or {}).items()]
    )
    storage_dir = Path(storage_dir)
    _validate_storage(storage_dir)
    collection_name = STRATEGY_COLLECTIONS[strategy]

    try:
        client = QdrantClient(path=str(storage_dir))
    except (OSError, RuntimeError, ValueError) as exc:
        raise SearchError(f"Could not open the local Qdrant database: {exc}") from exc
    try:
        _validate_collection(client, collection_name, strategy)
        if query_vector is None:
            query_vector = embed_query(query, model=model)
        else:
            if model is not None:
                raise SearchError("Provide either model or query_vector, not both.")
            try:
                query_vector = validate_embedding(query_vector)
            except (EmbeddingError, TypeError, ValueError) as exc:
                raise SearchError(f"Query embedding validation failed: {exc}") from exc
        query_filter = None
        if parsed_filters:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key=field,
                        match=models.MatchValue(value=value),
                    )
                    for field, value in parsed_filters.items()
                ]
            )
        points = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        ).points
    except SearchError:
        raise
    except (OSError, RuntimeError, ValueError) as exc:
        raise SearchError(f"Qdrant search failed: {exc}") from exc
    finally:
        client.close()

    results: list[dict[str, Any]] = []
    for point in points:
        payload = point.payload
        if not isinstance(payload, dict):
            raise SearchError(f"Search result {point.id} has no payload metadata.")
        if point.score is None or not math.isfinite(float(point.score)):
            raise SearchError(
                f"Search result {point.id} has an invalid similarity score."
            )
        result = dict(payload)
        result["score"] = float(point.score)
        results.append(result)
    results.sort(key=lambda result: result["score"], reverse=True)
    return results


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search PolicyLens policy chunks using local BGE-M3 and Qdrant."
    )
    parser.add_argument("query", help="Free-text policy search query")
    parser.add_argument(
        "--top_k",
        "--top-k",
        dest="top_k",
        type=_positive_int,
        default=RETRIEVE_TOP_K,
        help=f"Maximum results to return (default: {RETRIEVE_TOP_K})",
    )
    parser.add_argument(
        "--strategy",
        choices=sorted(STRATEGY_COLLECTIONS),
        default="fixed_size",
        help="Embedding/chunk strategy collection to search (default: fixed_size)",
    )
    parser.add_argument(
        "--filter",
        action="append",
        default=[],
        metavar="FIELD=VALUE",
        help="Exact metadata filter; currently supports issuer (repeatable)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        filters = parse_filters(args.filter)
        results = retrieve(
            args.query,
            top_k=args.top_k,
            strategy=args.strategy,
            filters=filters,
        )
    except SearchError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

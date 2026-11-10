"""Resumable local BGE-M3 embeddings for PolicyLens chunk JSONL files."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import logging
import math
import os
import resource
import sys
import time
from pathlib import Path
from statistics import mean
from typing import Any, Iterator

from src.config import LOGS_DIR, PROCESSED_DIR

logger = logging.getLogger("policylens.embed")

MODEL_NAME = "BAAI/bge-m3"
MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
EMBEDDING_DIMENSIONS = 1024
DEVICE = "mps"
BATCH_SIZE = 1
NORMALIZATION_TOLERANCE = 1e-4
STRATEGIES = ("fixed_size", "structure_aware")
DEFAULT_INPUT_DIR = PROCESSED_DIR / "chunks"
DEFAULT_OUTPUT_DIR = PROCESSED_DIR / "embeddings"

_EMBEDDING_FIELDS = {
    "embedding",
    "embedding_model",
    "model_revision",
    "embedding_dimensions",
    "normalized",
    "embedding_config",
    "embedding_status",
    "source_chunk_id",
    "source_chunk_sha256",
    "source_input_sha256",
}


class EmbeddingError(RuntimeError):
    """Raised when an embedding run cannot safely complete or resume."""


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as input_file:
        for block in iter(lambda: input_file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise EmbeddingError(
                    f"Invalid JSON at {path}:{line_number}: {exc}"
                ) from exc
            if not isinstance(record, dict):
                raise EmbeddingError(
                    f"Expected a chunk object at {path}:{line_number}."
                )
            yield record


def _source_inventory(
    input_path: Path, strategy: str
) -> tuple[str, dict[str, str], int]:
    if not input_path.is_file():
        raise FileNotFoundError(f"Chunk input not found: {input_path}")
    input_hash = _file_sha256(input_path)
    source_hashes: dict[str, str] = {}
    invalid: list[str] = []
    for line_number, record in enumerate(_read_jsonl(input_path), 1):
        chunk_id = record.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            invalid.append(f"line {line_number}: missing chunk_id")
            continue
        if chunk_id in source_hashes:
            invalid.append(f"line {line_number}: duplicate chunk_id {chunk_id}")
        if record.get("chunking_strategy") != strategy:
            invalid.append(
                f"line {line_number} ({chunk_id}): expected strategy "
                f"{strategy}, got {record.get('chunking_strategy')!r}"
            )
        text = record.get("text")
        if not isinstance(text, str) or not text.strip():
            invalid.append(f"line {line_number} ({chunk_id}): empty or invalid text")
        if not isinstance(record.get("doc_id"), str) or not record.get("doc_id"):
            invalid.append(f"line {line_number} ({chunk_id}): missing doc_id")
        page_start = record.get("page_start")
        page_end = record.get("page_end")
        if (
            not isinstance(page_start, int)
            or not isinstance(page_end, int)
            or page_start < 1
            or page_end < page_start
        ):
            invalid.append(f"line {line_number} ({chunk_id}): invalid page range")
        source_hashes[chunk_id] = _canonical_sha256(record)
    if invalid:
        preview = "; ".join(invalid[:10])
        extra = f"; and {len(invalid) - 10} more" if len(invalid) > 10 else ""
        raise EmbeddingError(
            f"Chunk preflight failed for {input_path}: {preview}{extra}"
        )
    if not source_hashes:
        raise EmbeddingError(f"No chunks found in {input_path}.")
    if _file_sha256(input_path) != input_hash:
        raise EmbeddingError(f"Chunk input changed during preflight: {input_path}")
    return input_hash, source_hashes, len(source_hashes)


def _embedding_config() -> dict[str, Any]:
    return {
        "device": DEVICE,
        "batch_size": BATCH_SIZE,
        "precision": "float32",
        "normalize_embeddings": True,
        "normalization_tolerance": NORMALIZATION_TOLERANCE,
        "prompt": None,
    }


def _run_metadata(strategy: str, input_hash: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "chunking_strategy": strategy,
        "source_input_sha256": input_hash,
        "embedding_model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "embedding_config": _embedding_config(),
    }


def _read_metadata(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EmbeddingError(f"Cannot read run metadata {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EmbeddingError(f"Run metadata must be a JSON object: {path}")
    return value


def _write_metadata(path: Path, metadata: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as output_file:
            json.dump(metadata, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")
            output_file.flush()
            os.fsync(output_file.fileno())
        temporary.replace(path)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise


def validate_embedding(
    vector: Any, tolerance: float = NORMALIZATION_TOLERANCE
) -> list[float]:
    """Validate a normalized 1,024-value vector and return JSON-safe floats."""
    try:
        values = [float(value) for value in vector]
    except (TypeError, ValueError) as exc:
        raise EmbeddingError(f"Embedding is not a numeric vector: {exc}") from exc
    if len(values) != EMBEDDING_DIMENSIONS:
        raise EmbeddingError(
            f"Expected {EMBEDDING_DIMENSIONS} dimensions, got {len(values)}."
        )
    if not all(math.isfinite(value) for value in values):
        raise EmbeddingError("Embedding contains NaN or infinity.")
    norm = math.sqrt(sum(value * value for value in values))
    if norm == 0.0:
        raise EmbeddingError("Embedding is an all-zero vector.")
    if abs(norm - 1.0) > tolerance:
        raise EmbeddingError(
            f"Embedding L2 norm {norm:.8f} is outside tolerance {tolerance}."
        )
    return values


def _repair_incomplete_tail(path: Path) -> int:
    """Drop only a non-newline-terminated final append interrupted mid-write."""
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open("r+b") as output_file:
        output_file.seek(-1, os.SEEK_END)
        if output_file.read(1) == b"\n":
            return 0
        end = output_file.tell()
        block_size = 64 * 1024
        while end:
            start = max(0, end - block_size)
            output_file.seek(start)
            block = output_file.read(end - start)
            newline = block.rfind(b"\n")
            if newline >= 0:
                valid_end = start + newline + 1
                break
            end = start
        else:
            valid_end = 0
        discarded = path.stat().st_size - valid_end
        output_file.truncate(valid_end)
        output_file.flush()
        os.fsync(output_file.fileno())
    return discarded


def _validate_output_record(
    record: dict[str, Any],
    expected_source_hashes: dict[str, str],
    metadata: dict[str, Any],
) -> str:
    chunk_id = record.get("source_chunk_id")
    if not isinstance(chunk_id, str) or not chunk_id:
        raise EmbeddingError("Embedding output is missing source_chunk_id.")
    if record.get("chunk_id") != chunk_id:
        raise EmbeddingError(f"chunk_id/source_chunk_id mismatch: {chunk_id}")
    expected_hash = expected_source_hashes.get(chunk_id)
    if expected_hash is None:
        raise EmbeddingError(f"Unexpected output chunk ID: {chunk_id}")
    if record.get("source_chunk_sha256") != expected_hash:
        raise EmbeddingError(f"Source chunk changed for output ID {chunk_id}.")
    source_record = {
        key: value for key, value in record.items() if key not in _EMBEDDING_FIELDS
    }
    if _canonical_sha256(source_record) != expected_hash:
        raise EmbeddingError(f"Source metadata/text changed for output ID {chunk_id}.")
    for key in ("embedding_model", "model_revision", "embedding_dimensions"):
        if record.get(key) != metadata.get(key):
            raise EmbeddingError(f"{key} mismatch in output ID {chunk_id}.")
    for key in ("chunking_strategy", "source_input_sha256"):
        if record.get(key) != metadata.get(
            "chunking_strategy" if key == "chunking_strategy" else "source_input_sha256"
        ):
            raise EmbeddingError(f"{key} mismatch in output ID {chunk_id}.")
    if record.get("embedding_status") != "completed":
        raise EmbeddingError(f"Output ID {chunk_id} is not completed.")
    if record.get("normalized") is not True:
        raise EmbeddingError(f"Output ID {chunk_id} is not marked normalized.")
    if record.get("embedding_config") != metadata.get("embedding_config"):
        raise EmbeddingError(f"Embedding configuration mismatch for {chunk_id}.")
    validate_embedding(record.get("embedding"))
    return chunk_id


def _resume_records(
    output_path: Path,
    metadata_path: Path,
    expected_metadata: dict[str, Any],
    source_hashes: dict[str, str],
) -> tuple[set[str], int]:
    if metadata_path.exists():
        actual_metadata = _read_metadata(metadata_path)
        if actual_metadata != expected_metadata:
            raise EmbeddingError(
                f"Input/model/configuration changed for existing output "
                f"{output_path}. Preserve this output and use a new output "
                f"directory for changed inputs."
            )
    elif output_path.exists() and output_path.stat().st_size:
        raise EmbeddingError(
            f"Output exists without resumability metadata: {output_path}. "
            "Refusing to overwrite or guess its provenance."
        )
    else:
        _write_metadata(metadata_path, expected_metadata)

    discarded_tail_bytes = _repair_incomplete_tail(output_path)
    completed: set[str] = set()
    if not output_path.exists():
        return completed, discarded_tail_bytes
    with output_path.open("r", encoding="utf-8") as output_file:
        for line_number, line in enumerate(output_file, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise EmbeddingError(
                    f"Invalid complete output record at {output_path}:{line_number}: {exc}"
                ) from exc
            if not isinstance(record, dict):
                raise EmbeddingError(
                    f"Expected an output object at {output_path}:{line_number}."
                )
            chunk_id = _validate_output_record(
                record, source_hashes, expected_metadata
            )
            if chunk_id in completed:
                raise EmbeddingError(
                    f"Duplicate embedding record for {chunk_id} in {output_path}."
                )
            completed.add(chunk_id)
    return completed, discarded_tail_bytes


def _device_type(device: Any) -> str:
    return str(device).split(":", maxsplit=1)[0].lower()


def _load_model() -> Any:
    """Load only the already-cached pinned model; never download or fall back."""
    cache_root = os.environ.get("HF_HUB_CACHE")
    if cache_root is None:
        cache_root = str(
            Path(os.environ.get("HF_HOME", Path.home() / ".cache/huggingface"))
            / "hub"
        )
    snapshot_path = (
        Path(cache_root)
        / "models--BAAI--bge-m3"
        / "snapshots"
        / MODEL_REVISION
    )
    if not snapshot_path.is_dir() or not (snapshot_path / "modules.json").is_file():
        raise EmbeddingError(
            f"Pinned BGE-M3 snapshot is not available locally: {snapshot_path}"
        )
    os.environ["HF_HUB_OFFLINE"] = "1"
    from sentence_transformers import SentenceTransformer

    _require_mps()
    model = SentenceTransformer(
        str(snapshot_path),
        device=DEVICE,
        local_files_only=True,
    )
    if _device_type(model.device) != DEVICE:
        raise EmbeddingError(
            f"Model loaded on {model.device}, expected explicit {DEVICE}."
        )
    parameter = next(model.parameters(), None)
    if parameter is None or _device_type(parameter.device) != DEVICE:
        raise EmbeddingError("Model parameters are not resident on the MPS device.")
    return model


def _require_mps() -> Any:
    import torch

    if not torch.backends.mps.is_built() or not torch.backends.mps.is_available():
        raise EmbeddingError(
            "Apple MPS is unavailable. Refusing to fall back to another device."
        )
    return torch


def _make_output_record(
    source: dict[str, Any], vector: Any, input_hash: str
) -> dict[str, Any]:
    chunk_id = source["chunk_id"]
    result = copy.deepcopy(source)
    result.update(
        {
            "embedding": validate_embedding(vector),
            "embedding_model": MODEL_NAME,
            "model_revision": MODEL_REVISION,
            "embedding_dimensions": EMBEDDING_DIMENSIONS,
            "normalized": True,
            "embedding_config": _embedding_config(),
            "embedding_status": "completed",
            "source_chunk_id": chunk_id,
            "source_chunk_sha256": _canonical_sha256(source),
            "source_input_sha256": input_hash,
        }
    )
    return result


def embed_strategy(
    input_path: Path,
    output_path: Path,
    model: Any,
) -> dict[str, Any]:
    """Embed one strategy, appending each validated result durably for resume."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    strategy = input_path.stem
    if strategy not in STRATEGIES:
        raise EmbeddingError(f"Unsupported chunking strategy input: {input_path}")
    if _device_type(getattr(model, "device", "")) != DEVICE:
        raise EmbeddingError(
            f"Refusing model device {getattr(model, 'device', None)!r}; "
            f"expected {DEVICE}."
        )
    input_hash, source_hashes, source_count = _source_inventory(
        input_path, strategy
    )
    metadata = _run_metadata(strategy, input_hash)
    metadata_path = output_path.with_suffix(output_path.suffix + ".meta.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed, discarded_tail_bytes = _resume_records(
        output_path, metadata_path, metadata, source_hashes
    )
    if not completed.issubset(source_hashes):
        raise EmbeddingError(f"Output contains unexpected IDs: {output_path}")

    embedded_now = 0
    inference_seconds: list[float] = []
    start_time = time.perf_counter()
    rss_peak_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_mps_driver_bytes = 0
    torch = _require_mps()

    try:
        with input_path.open("r", encoding="utf-8") as input_file, output_path.open(
            "a", encoding="utf-8"
        ) as output_file:
            for line_number, line in enumerate(input_file, 1):
                if not line.strip():
                    continue
                source = json.loads(line)
                chunk_id = source["chunk_id"]
                if chunk_id in completed:
                    continue
                try:
                    torch.mps.synchronize()
                    inference_start = time.perf_counter()
                    vector = model.encode(
                        [source["text"]],
                        batch_size=BATCH_SIZE,
                        show_progress_bar=False,
                        convert_to_numpy=True,
                        normalize_embeddings=True,
                        precision="float32",
                    )[0]
                    torch.mps.synchronize()
                    inference_seconds.append(time.perf_counter() - inference_start)
                    result = _make_output_record(source, vector, input_hash)
                    output_file.write(
                        json.dumps(
                            result,
                            ensure_ascii=False,
                            separators=(",", ":"),
                            allow_nan=False,
                        )
                        + "\n"
                    )
                    output_file.flush()
                    os.fsync(output_file.fileno())
                    completed.add(chunk_id)
                    embedded_now += 1
                    max_mps_driver_bytes = max(
                        max_mps_driver_bytes, torch.mps.driver_allocated_memory()
                    )
                except Exception as exc:
                    raise EmbeddingError(
                        f"Embedding failed for {strategy} chunk {chunk_id} "
                        f"at source line {line_number}; completed records are "
                        f"preserved and the run can resume: "
                        f"{type(exc).__name__}: {exc}"
                    ) from exc
    except OSError as exc:
        raise EmbeddingError(
            f"I/O failure while embedding {strategy}; completed records remain "
            f"available for resume: {exc}"
        ) from exc

    if _file_sha256(input_path) != input_hash:
        raise EmbeddingError(
            f"Source chunk file changed during embedding: {input_path}. "
            "Output is retained but must not be used until resolved."
        )
    if len(completed) != source_count:
        raise EmbeddingError(
            f"Output count mismatch for {strategy}: {len(completed)} of "
            f"{source_count} source chunks completed."
        )
    elapsed = time.perf_counter() - start_time
    rss_peak_end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {
        "strategy": strategy,
        "input_file": str(input_path),
        "input_sha256": input_hash,
        "output_file": str(output_path),
        "metadata_file": str(metadata_path),
        "source_chunks": source_count,
        "embedded_this_run": embedded_now,
        "skipped_valid_on_resume": len(completed) - embedded_now,
        "completed_embeddings": len(completed),
        "failed_chunks": 0,
        "elapsed_seconds": round(elapsed, 3),
        "average_inference_seconds_per_embedded_chunk": round(
            mean(inference_seconds), 4
        )
        if inference_seconds
        else 0,
        "batch_size": BATCH_SIZE,
        "device": DEVICE,
        "max_mps_driver_allocated_bytes_observed": max_mps_driver_bytes,
        "process_peak_rss_bytes": max(rss_peak_start, rss_peak_end),
        "discarded_incomplete_tail_bytes": discarded_tail_bytes,
        "output_size_bytes": output_path.stat().st_size,
    }


def validate_strategy_output(
    input_path: Path, output_path: Path
) -> dict[str, Any]:
    strategy = Path(input_path).stem
    input_hash, source_hashes, source_count = _source_inventory(
        Path(input_path), strategy
    )
    metadata = _run_metadata(strategy, input_hash)
    metadata_path = Path(output_path).with_suffix(
        Path(output_path).suffix + ".meta.json"
    )
    completed, discarded_tail = _resume_records(
        Path(output_path), metadata_path, metadata, source_hashes
    )
    if discarded_tail:
        raise EmbeddingError(
            f"Unexpected incomplete output tail in completed file {output_path}."
        )
    if len(completed) != source_count:
        missing = source_count - len(completed)
        raise EmbeddingError(
            f"{strategy} output has {len(completed)} of {source_count} records; "
            f"{missing} source chunks are missing."
        )
    return {
        "strategy": strategy,
        "source_chunks": source_count,
        "embedding_records": len(completed),
        "missing_source_chunks": 0,
        "duplicate_ids": 0,
        "input_sha256": input_hash,
    }


def _write_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as output_file:
            json.dump(summary, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")
            output_file.flush()
            os.fsync(output_file.fileno())
        temporary.replace(path)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise


def embed_corpus(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    model: Any | None = None,
) -> dict[str, Any]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    for strategy in STRATEGIES:
        input_path = input_dir / f"{strategy}.jsonl"
        if not input_path.is_file():
            raise FileNotFoundError(f"Required chunk input not found: {input_path}")
    summary: dict[str, Any] = {
        "stage": "local_bge_m3_embedding",
        "schema_version": 1,
        "embedding_model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "embedding_config": _embedding_config(),
        "device": DEVICE,
        "batch_size": BATCH_SIZE,
        "strategies": {},
        "validation": {},
        "errors": [],
    }
    run_started = time.perf_counter()
    try:
        model_load_started = time.perf_counter()
        active_model = model if model is not None else _load_model()
        model_load_seconds = time.perf_counter() - model_load_started
        summary["model_load_seconds"] = round(model_load_seconds, 3)
        for strategy in STRATEGIES:
            input_path = input_dir / f"{strategy}.jsonl"
            output_path = output_dir / f"{strategy}.jsonl"
            summary["strategies"][strategy] = embed_strategy(
                input_path, output_path, active_model
            )
            _write_summary(output_dir / "embedding_summary.json", summary)
        for strategy in STRATEGIES:
            summary["validation"][strategy] = validate_strategy_output(
                input_dir / f"{strategy}.jsonl",
                output_dir / f"{strategy}.jsonl",
            )
        summary["status"] = "completed"
        summary["total_elapsed_seconds"] = round(
            time.perf_counter() - run_started, 3
        )
        _write_summary(output_dir / "embedding_summary.json", summary)
        return summary
    except Exception as exc:
        summary["status"] = "failed"
        summary["total_elapsed_seconds"] = round(
            time.perf_counter() - run_started, 3
        )
        summary["errors"].append(
            {"error_type": type(exc).__name__, "error": str(exc)}
        )
        _write_summary(output_dir / "embedding_summary.json", summary)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate resumable, local BGE-M3 embeddings for both chunk sets."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(LOGS_DIR / "embedding.log", encoding="utf-8"),
        ],
    )
    try:
        summary = embed_corpus(args.input_dir, args.output_dir)
    except (EmbeddingError, FileNotFoundError, OSError, ValueError) as exc:
        logger.error("%s", exc)
        return 1
    for strategy, details in summary["strategies"].items():
        logger.info(
            "%s: %d/%d embeddings complete; %d embedded this run",
            strategy,
            details["completed_embeddings"],
            details["source_chunks"],
            details["embedded_this_run"],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

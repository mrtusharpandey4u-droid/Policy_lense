"""Deterministic fixed-size and structure-aware page-level chunking."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

from src.config import (
    CHUNK_MAX_TOKENS,
    CHUNK_MIN_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    CHUNK_TARGET_TOKENS,
    LOGS_DIR,
    MANIFEST_PATH,
    PROCESSED_DIR,
)

logger = logging.getLogger("policylens.chunk")

TOKENIZER_NAME = "PolicyLens Unicode lexical tokenizer v1 (regex)"
_TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)
_HEADING_PREFIX = re.compile(
    r"^\s*(?:\d+(?:\.\d+)*(?:\([A-Za-z0-9]+\))*[.)]?|"
    r"[A-Z][.)]|\([a-z]\)|[ivxlcdm]+[.)])\s+\S",
    re.IGNORECASE,
)
_WHITESPACE = re.compile(r"\s+")


def _tokens(text: str) -> list[re.Match[str]]:
    """Tokenize Unicode word/number runs and individual punctuation marks."""
    return list(_TOKEN_PATTERN.finditer(text))


def _normalized(text: str) -> str:
    return _WHITESPACE.sub(" ", text).strip().casefold()


def _table_text(table: dict[str, Any]) -> str:
    rows = table.get("rows", [])
    rendered = [
        " | ".join(str(cell).replace("\n", " ").strip() for cell in row)
        for row in rows
    ]
    return "\n".join(row for row in rendered if row.strip())


def _table_signature(table: dict[str, Any]) -> str:
    identity = {
        "table_number": table.get("table_number"),
        "bbox": table.get("bbox"),
        "rows": table.get("rows", []),
    }
    return json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _page_text(record: dict[str, Any]) -> str:
    text = record.get("canonical_text", "")
    if not isinstance(text, str):
        return ""
    # Table-only extraction already has a readable table fallback in canonical_text.
    rendered_tables = "\n".join(
        _table_text(table)
        for table in record.get("tables", [])
        if isinstance(table, dict) and table.get("rows")
    )
    if rendered_tables and _normalized(text) == _normalized(rendered_tables):
        return ""
    return text


def _heading_lines(record: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for heading in record.get("headings", []):
        if isinstance(heading, dict) and isinstance(heading.get("text"), str):
            title = heading["text"].strip()
            if title:
                result[_normalized(title)] = title
    return result


def _page_units(
    record: dict[str, Any], inherited_section: str | None
) -> tuple[list[dict[str, Any]], str | None]:
    text = _page_text(record)
    if not text.strip():
        return [], inherited_section
    heading_lines = _heading_lines(record)
    lines = text.splitlines()
    units: list[dict[str, Any]] = []
    current_lines: list[str] = []
    current_section = inherited_section

    def flush() -> None:
        content = "\n".join(current_lines).strip()
        if content:
            units.append(
                {
                    "text": content,
                    "page_number": record["page_number"],
                    "section_title": current_section,
                    "kind": "text",
                }
            )
        current_lines.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        heading = heading_lines.get(_normalized(stripped))
        clause = (
            stripped
            if len(stripped) <= 160 and _HEADING_PREFIX.match(stripped)
            else None
        )
        detected_title = heading or clause
        if detected_title:
            flush()
            current_section = detected_title
        current_lines.append(line)
    flush()
    if not units:
        units.append(
            {
                "text": text.strip(),
                "page_number": record["page_number"],
                "section_title": current_section,
                "kind": "text",
            }
        )
    return units, current_section


def _page_provenance(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_page: dict[int, dict[str, Any]] = {}
    for record in records:
        page_number = record["page_number"]
        cleaning = record.get("cleaning", {})
        source = cleaning.get("selected_source", "native")
        entry = {
            "page_number": page_number,
            "text_source": source,
            "cleaning_review": bool(cleaning.get("needs_manual_review", False)),
            "review_reasons": list(cleaning.get("review_reasons", [])),
        }
        if source == "ocr":
            entry["ocr_provenance"] = copy.deepcopy(
                cleaning.get("ocr_provenance")
                or record.get("ocr", {})
            )
        by_page[page_number] = entry
    return [by_page[number] for number in sorted(by_page)]


def _metadata(
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
) -> dict[str, Any]:
    first = records[0]
    title = manifest_row.get("title", "").strip() or first.get("document_title")
    values: dict[str, Any] = {
        "doc_id": doc_id,
        "page_start": min(record["page_number"] for record in records),
        "page_end": max(record["page_number"] for record in records),
    }
    if first.get("source_hash"):
        values["source_hash"] = first["source_hash"]
    if title:
        values["title"] = title
    for key in ("issuer", "issue_date"):
        value = manifest_row.get(key, "").strip()
        if value:
            values[key] = value
    return values


def _make_chunk(
    *,
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    strategy: str,
    chunk_size: int,
    overlap: int,
    ordinal: int,
    text: str,
    section_title: str | None,
    content_type: str,
    tables: list[dict[str, Any]] | None = None,
    continuation: bool = False,
    oversize: bool = False,
) -> dict[str, Any]:
    pages = sorted({record["page_number"] for record in records})
    base = _metadata(doc_id, records, manifest_row)
    base["page_start"] = min(pages)
    base["page_end"] = max(pages)
    if section_title:
        base["section_title"] = section_title
    base.update(
        {
            "chunk_id": "",
            "chunking_strategy": strategy,
            "chunk_index": ordinal,
            "text": text,
            "token_count": len(_tokens(text)),
            "content_type": content_type,
            "tables": copy.deepcopy(tables or []),
            "page_provenance": _page_provenance(records),
            "contains_ocr": any(
                record["cleaning"].get("selected_source") == "ocr"
                for record in records
            ),
            "has_cleaning_review": any(
                record["cleaning"].get("needs_manual_review", False)
                for record in records
            ),
            "review_pages": [
                record["page_number"]
                for record in records
                if record["cleaning"].get("needs_manual_review", False)
            ],
            "is_continuation": continuation,
            "exceeds_target_size": oversize,
        }
    )
    signature = {
        "doc_id": doc_id,
        "strategy": strategy,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "ordinal": ordinal,
        "pages": pages,
        "text": text,
        "tables": [
            _table_signature(table)
            for table in (tables or [])
        ],
    }
    digest = hashlib.sha256(
        json.dumps(signature, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:12]
    base["chunk_id"] = f"{doc_id}_{strategy}_{ordinal:05d}_{digest}"
    return base


def _text_chunks(
    *,
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    strategy: str,
    chunk_size: int,
    overlap: int,
    ordinal: int,
    text: str,
    page_for_token: list[int],
    section_title: str | None,
    section_for_token: list[str | None] | None = None,
) -> list[dict[str, Any]]:
    tokens = _tokens(text)
    if not tokens:
        return []
    chunks: list[dict[str, Any]] = []
    step = chunk_size - overlap
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        char_start = tokens[start].start()
        char_end = tokens[end - 1].end()
        chunk_text = text[char_start:char_end]
        chunk_pages = set(page_for_token[start:end])
        chunk_records = [
            record for record in records if record["page_number"] in chunk_pages
        ]
        chunks.append(
            _make_chunk(
                doc_id=doc_id,
                records=chunk_records,
                manifest_row=manifest_row,
                strategy=strategy,
                chunk_size=chunk_size,
                overlap=overlap,
                ordinal=ordinal + len(chunks),
                text=chunk_text,
                section_title=(
                    section_for_token[start]
                    if section_for_token and section_for_token[start]
                    else section_title
                ),
                content_type="text",
                continuation=start > 0,
            )
        )
        if end == len(tokens):
            break
        start += step
    return chunks


def _fixed_text_chunks(
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    chunk_size: int,
    overlap: int,
) -> list[dict[str, Any]]:
    page_for_token: list[int] = []
    section_for_token: list[str | None] = []
    all_text = ""
    current_section: str | None = None
    for record in records:
        page_text = _page_text(record)
        if not page_text.strip():
            continue
        if all_text:
            all_text += "\n\n"
        all_text += page_text
        heading_lines = _heading_lines(record)
        line_offsets: list[tuple[int, str]] = []
        cursor = 0
        for line in page_text.splitlines(keepends=True):
            title = heading_lines.get(_normalized(line.strip()))
            if title:
                line_offsets.append((cursor, title))
            cursor += len(line)
        heading_index = 0
        for token in _tokens(page_text):
            while (
                heading_index < len(line_offsets)
                and line_offsets[heading_index][0] <= token.start()
            ):
                current_section = line_offsets[heading_index][1]
                heading_index += 1
            page_for_token.append(record["page_number"])
            section_for_token.append(current_section)
    if not _tokens(all_text):
        return []
    return _text_chunks(
        doc_id=doc_id,
        records=records,
        manifest_row=manifest_row,
        strategy="fixed_size",
        chunk_size=chunk_size,
        overlap=overlap,
        ordinal=1,
        text=all_text,
        page_for_token=page_for_token,
        section_title=None,
        section_for_token=section_for_token,
    )


def _structure_text_chunks(
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    chunk_size: int,
    overlap: int,
) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    buffer: list[dict[str, Any]] = []
    buffered_tokens = 0
    inherited_section: str | None = None

    def flush_buffer() -> None:
        nonlocal buffer, buffered_tokens
        if not buffer:
            return
        joined_text = "\n\n".join(unit["text"] for unit in buffer)
        pages = sorted({unit["page_number"] for unit in buffer})
        page_records = [r for r in records if r["page_number"] in pages]
        token_pages = [
            unit["page_number"]
            for unit in buffer
            for _ in _tokens(unit["text"])
        ]
        token_sections = [
            unit["section_title"]
            for unit in buffer
            for _ in _tokens(unit["text"])
        ]
        section = next(
            (unit["section_title"] for unit in buffer if unit["section_title"]),
            None,
        )
        if len(_tokens(joined_text)) <= chunk_size:
            chunks.append(
                _make_chunk(
                    doc_id=doc_id,
                    records=page_records,
                    manifest_row=manifest_row,
                    strategy="structure_aware",
                    chunk_size=chunk_size,
                    overlap=overlap,
                    ordinal=len(chunks) + 1,
                    text=joined_text,
                    section_title=section,
                    content_type="text",
                )
            )
        else:
            chunks.extend(
                _text_chunks(
                    doc_id=doc_id,
                    records=page_records,
                    manifest_row=manifest_row,
                    strategy="structure_aware",
                    chunk_size=chunk_size,
                    overlap=overlap,
                    ordinal=len(chunks) + 1,
                    text=joined_text,
                    page_for_token=token_pages,
                    section_title=section,
                    section_for_token=token_sections,
                )
            )
        buffer = []
        buffered_tokens = 0

    for record in records:
        units, inherited_section = _page_units(record, inherited_section)
        for unit in units:
            unit_tokens = len(_tokens(unit["text"]))
            if unit_tokens > chunk_size:
                flush_buffer()
                chunks.extend(
                    _text_chunks(
                        doc_id=doc_id,
                        records=[record],
                        manifest_row=manifest_row,
                        strategy="structure_aware",
                        chunk_size=chunk_size,
                        overlap=overlap,
                        ordinal=len(chunks) + 1,
                        text=unit["text"],
                        page_for_token=[record["page_number"]] * unit_tokens,
                        section_title=unit["section_title"],
                    )
                )
                continue
            if (
                buffer
                and unit["section_title"] != buffer[-1]["section_title"]
                and buffered_tokens >= chunk_size - overlap
            ):
                flush_buffer()
            if buffer and buffered_tokens + unit_tokens > chunk_size:
                flush_buffer()
            buffer.append(unit)
            buffered_tokens += unit_tokens
    flush_buffer()
    return chunks


def _split_table_rows(
    table: dict[str, Any], chunk_size: int
) -> list[tuple[list[list[Any]], bool]]:
    rows = table.get("rows", [])
    if not rows:
        return []
    whole_text = _table_text(table)
    if len(_tokens(whole_text)) <= chunk_size:
        return [(copy.deepcopy(rows), False)]
    header = copy.deepcopy(rows[0])
    fragments: list[tuple[list[list[Any]], bool]] = []
    data_rows = rows[1:]
    current = [header]
    for row in data_rows:
        candidate = current + [copy.deepcopy(row)]
        if len(_tokens(_table_text({"rows": candidate}))) <= chunk_size:
            current.append(copy.deepcopy(row))
            continue
        if len(current) > 1:
            fragments.append(
                (current, len(_tokens(_table_text({"rows": current}))) > chunk_size)
            )
        current = [header]
        single_row_fragment = [header, copy.deepcopy(row)]
        if len(_tokens(_table_text({"rows": single_row_fragment}))) > chunk_size:
            fragments.append((single_row_fragment, True))
        else:
            current.append(copy.deepcopy(row))
    if len(current) > 1 or not fragments:
        fragments.append(
            (current, len(_tokens(_table_text({"rows": current}))) > chunk_size)
        )
    return fragments


def _table_chunks(
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    strategy: str,
    chunk_size: int,
    overlap: int,
) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for record in records:
        tables = [
            table
            for table in record.get("tables", [])
            if isinstance(table, dict) and table.get("rows")
        ]
        for table in tables:
            fragments = _split_table_rows(table, chunk_size)
            for part_index, (rows, oversize) in enumerate(fragments, start=1):
                fragment = copy.deepcopy(table)
                fragment["rows"] = rows
                fragment["original_table_number"] = table.get("table_number")
                fragment["part_index"] = part_index
                fragment["part_count"] = len(fragments)
                fragment["header_repeated"] = part_index > 1
                text = _table_text({"rows": rows})
                heading_candidates = [
                    heading
                    for heading in record.get("headings", [])
                    if isinstance(heading, dict)
                    and isinstance(heading.get("bbox"), list)
                    and isinstance(table.get("bbox"), list)
                    and len(heading["bbox"]) == 4
                    and heading["bbox"][1] <= table["bbox"][1]
                ]
                section = (
                    max(heading_candidates, key=lambda item: item["bbox"][1])["text"]
                    if heading_candidates
                    else None
                )
                chunks.append(
                    _make_chunk(
                        doc_id=doc_id,
                        records=[record],
                        manifest_row=manifest_row,
                        strategy=strategy,
                        chunk_size=chunk_size,
                        overlap=overlap,
                        ordinal=0,
                        text=text,
                        section_title=section,
                        content_type="table",
                        tables=[fragment],
                        continuation=part_index > 1,
                        oversize=oversize,
                    )
                )
    return chunks


def _review_only_chunks(
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    strategy: str,
    chunk_size: int,
    overlap: int,
) -> list[dict[str, Any]]:
    chunks = []
    for record in records:
        if (
            not _page_text(record).strip()
            and not any(
                isinstance(table, dict) and table.get("rows")
                for table in record.get("tables", [])
            )
            and record.get("cleaning", {}).get("needs_manual_review")
        ):
            chunks.append(
                _make_chunk(
                    doc_id=doc_id,
                    records=[record],
                    manifest_row=manifest_row,
                    strategy=strategy,
                    chunk_size=chunk_size,
                    overlap=overlap,
                    ordinal=0,
                    text="",
                    section_title=None,
                    content_type="review_only",
                )
            )
    return chunks


def _finalize_ids(
    chunks: list[dict[str, Any]], strategy: str, chunk_size: int, overlap: int
) -> list[dict[str, Any]]:
    chunks.sort(
        key=lambda chunk: (
            chunk["doc_id"],
            chunk["page_start"],
            chunk["page_end"],
            {"text": 0, "table": 1, "review_only": 2}[chunk["content_type"]],
            chunk.get("chunk_index", 0),
        )
    )
    counters: Counter[str] = Counter()
    for chunk in chunks:
        doc_id = chunk["doc_id"]
        counters[doc_id] += 1
        signature = {
            "doc_id": doc_id,
            "strategy": strategy,
            "chunk_size": chunk_size,
            "overlap": overlap,
            "index": counters[doc_id],
            "page_start": chunk["page_start"],
            "page_end": chunk["page_end"],
            "text": chunk["text"],
            "tables": [
                _table_signature(table)
                for table in chunk.get("tables", [])
            ],
        }
        digest = hashlib.sha256(
            json.dumps(signature, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:12]
        chunk["chunk_index"] = counters[doc_id]
        chunk["chunk_id"] = (
            f"{doc_id}_{strategy}_{counters[doc_id]:05d}_{digest}"
        )
    return chunks


def chunk_document(
    doc_id: str,
    records: list[dict[str, Any]],
    manifest_row: dict[str, str],
    strategy: str,
    chunk_size: int,
    overlap: int,
) -> list[dict[str, Any]]:
    if strategy not in {"fixed_size", "structure_aware"}:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap smaller than it.")
    records = sorted(records, key=lambda record: record["page_number"])
    if not records:
        return []
    if any(record.get("doc_id") != doc_id for record in records):
        raise ValueError("All chunk input records must belong to the requested document.")

    if strategy == "fixed_size":
        chunks = _fixed_text_chunks(
            doc_id, records, manifest_row, chunk_size, overlap
        )
    else:
        chunks = _structure_text_chunks(
            doc_id, records, manifest_row, chunk_size, overlap
        )
    chunks.extend(
        _table_chunks(
            doc_id, records, manifest_row, strategy, chunk_size, overlap
        )
    )
    chunks.extend(
        _review_only_chunks(
            doc_id, records, manifest_row, strategy, chunk_size, overlap
        )
    )
    return _finalize_ids(chunks, strategy, chunk_size, overlap)


def _read_manifest(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Manifest not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as input_file:
        reader = csv.DictReader(input_file)
        required = {"doc_id", "title", "issuer", "issue_date", "source_hash", "download_status"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Manifest missing chunk metadata columns: {sorted(required)}")
        return {
            row["doc_id"]: row
            for row in reader
            if row.get("doc_id") and row.get("download_status") == "verified"
        }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, 1):
            if line.strip():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON at {path}:{line_number}: {exc}") from exc
                if not isinstance(value, dict):
                    raise ValueError(f"Expected page object at {path}:{line_number}.")
                records.append(value)
    return records


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as output_file:
            for record in records:
                output_file.write(
                    json.dumps(record, ensure_ascii=False, separators=(",", ":"))
                    + "\n"
                )
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _size_stats(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    sizes = [chunk["token_count"] for chunk in chunks]
    return {
        "chunk_count": len(chunks),
        "minimum_tokens": min(sizes) if sizes else 0,
        "median_tokens": median(sizes) if sizes else 0,
        "average_tokens": round(mean(sizes), 2) if sizes else 0,
        "maximum_tokens": max(sizes) if sizes else 0,
        "chunks_300_to_800_tokens": sum(
            300 <= size <= 800 for size in sizes
        ),
        "percent_300_to_800_tokens": round(
            100 * sum(300 <= size <= 800 for size in sizes) / len(sizes), 2
        )
        if sizes
        else 0,
        "table_chunks": sum(chunk["content_type"] == "table" for chunk in chunks),
        "review_only_chunks": sum(
            chunk["content_type"] == "review_only" for chunk in chunks
        ),
        "chunks_with_cleaning_review": sum(
            chunk["has_cleaning_review"] for chunk in chunks
        ),
        "chunks_with_ocr": sum(chunk["contains_ocr"] for chunk in chunks),
        "oversize_chunks": sum(chunk["exceeds_target_size"] for chunk in chunks),
    }


def chunk_corpus(
    input_dir: Path = PROCESSED_DIR / "cleaned",
    manifest_path: Path = MANIFEST_PATH,
    output_dir: Path = PROCESSED_DIR / "chunks",
    chunk_size: int = CHUNK_TARGET_TOKENS,
    overlap: int = CHUNK_OVERLAP_TOKENS,
    strategy: str = "both",
) -> dict[str, Any]:
    if not CHUNK_MIN_TOKENS <= chunk_size <= CHUNK_MAX_TOKENS:
        raise ValueError(
            f"chunk_size must be in the configured range "
            f"{CHUNK_MIN_TOKENS}-{CHUNK_MAX_TOKENS}."
        )
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size.")
    if strategy not in {"fixed_size", "structure_aware", "both"}:
        raise ValueError(f"Unknown strategy selection: {strategy}")
    input_paths = sorted(Path(input_dir).glob("doc_*.jsonl"))
    if not input_paths:
        raise FileNotFoundError(f"No cleaned per-document JSONL found in {input_dir}.")
    manifest = _read_manifest(Path(manifest_path))
    selected_strategies = (
        ["fixed_size", "structure_aware"]
        if strategy == "both"
        else [strategy]
    )
    summary: dict[str, Any] = {
        "stage": "page_level_chunking",
        "schema_version": 1,
        "input_directory": str(input_dir),
        "output_directory": str(output_dir),
        "tokenizer": TOKENIZER_NAME,
        "chunk_size_tokens": chunk_size,
        "overlap_tokens": overlap,
        "target_range_tokens": [CHUNK_MIN_TOKENS, CHUNK_MAX_TOKENS],
        "documents_discovered": len(input_paths),
        "documents_processed": 0,
        "pages_processed": 0,
        "pages_with_cleaning_review": 0,
        "pages_without_text": 0,
        "errors": [],
        "strategies": {},
    }
    strategy_chunks: dict[str, list[dict[str, Any]]] = {
        selected: [] for selected in selected_strategies
    }
    for path in input_paths:
        try:
            records = _read_jsonl(path)
            if not records:
                continue
            doc_id = records[0].get("doc_id")
            if not isinstance(doc_id, str) or not doc_id:
                raise ValueError(f"Missing doc_id in {path}.")
            if any(record.get("doc_id") != doc_id for record in records):
                raise ValueError(f"Mixed document IDs in {path}.")
            manifest_row = manifest.get(doc_id, {})
            summary["documents_processed"] += 1
            summary["pages_processed"] += len(records)
            summary["pages_with_cleaning_review"] += sum(
                bool(record.get("cleaning", {}).get("needs_manual_review"))
                for record in records
            )
            summary["pages_without_text"] += sum(
                not _page_text(record).strip()
                and not any(table.get("rows") for table in record.get("tables", []))
                for record in records
            )
            for selected in selected_strategies:
                strategy_chunks[selected].extend(
                    chunk_document(
                        doc_id,
                        records,
                        manifest_row,
                        selected,
                        chunk_size,
                        overlap,
                    )
                )
        except (OSError, ValueError, TypeError) as exc:
            logger.exception("Could not chunk %s", path)
            summary["errors"].append(
                {"source_file": path.name, "error": f"{type(exc).__name__}: {exc}"}
            )

    output_root = Path(output_dir)
    for selected, chunks in strategy_chunks.items():
        output_path = output_root / f"{selected}.jsonl"
        _write_jsonl(output_path, chunks)
        stats = _size_stats(chunks)
        stats["output_file"] = str(output_path)
        stats["unique_chunk_ids"] = len({chunk["chunk_id"] for chunk in chunks})
        stats["chunks_missing_source_hash"] = sum(
            not chunk.get("source_hash") for chunk in chunks
        )
        stats["chunks_missing_title"] = sum(not chunk.get("title") for chunk in chunks)
        stats["chunks_missing_issuer"] = sum(not chunk.get("issuer") for chunk in chunks)
        stats["chunks_missing_issue_date"] = sum(
            not chunk.get("issue_date") for chunk in chunks
        )
        summary["strategies"][selected] = stats
    summary_path = output_root / "chunking_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate fixed-size and structure-aware document chunks."
    )
    parser.add_argument("--input-dir", type=Path, default=PROCESSED_DIR / "cleaned")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output-dir", type=Path, default=PROCESSED_DIR / "chunks")
    parser.add_argument(
        "--strategy",
        choices=["fixed_size", "structure_aware", "both"],
        default="both",
    )
    parser.add_argument("--chunk-size", type=int, default=CHUNK_TARGET_TOKENS)
    parser.add_argument("--overlap", type=int, default=CHUNK_OVERLAP_TOKENS)
    args = parser.parse_args(argv)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(LOGS_DIR / "chunking.log", encoding="utf-8"),
        ],
    )
    try:
        summary = chunk_corpus(
            args.input_dir,
            args.manifest,
            args.output_dir,
            args.chunk_size,
            args.overlap,
            args.strategy,
        )
    except (OSError, ValueError) as exc:
        logger.error("Chunking could not start: %s", exc)
        return 1
    for name, stats in summary["strategies"].items():
        logger.info(
            "%s: %d chunks; %.2f%% within 300-800 tokens",
            name,
            stats["chunk_count"],
            stats["percent_300_to_800_tokens"],
        )
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

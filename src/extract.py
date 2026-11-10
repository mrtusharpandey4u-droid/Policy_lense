"""
Page-level PDF text and layout extraction for PolicyLens.

PyMuPDF extracts text, positioned blocks, headings, and supported tables.
Pages with fewer than 30 non-whitespace characters or an alphanumeric ratio
below 0.35 are flagged for OCR review; OCR is deliberately not run here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict

import pymupdf

from src.config import LOGS_DIR, MANIFEST_PATH, PDF_DIR, PROCESSED_DIR

logger = logging.getLogger("policylens.extract")

MIN_TEXT_CHARACTERS = 30
MIN_ALPHANUMERIC_RATIO = 0.35
_COLUMN_GUTTER_TOLERANCE = 0.03
_MIN_COLUMN_BLOCK_CHARACTERS = 40
_MIN_COLUMN_CHARACTERS = 180


class PageData(TypedDict):
    """JSON-serializable extraction result for one PDF page."""

    doc_id: str
    document_title: str
    source_filename: str
    source_hash: str
    page_number: int
    text: str
    blocks: list[dict[str, Any]]
    headings: list[dict[str, Any]]
    tables: list[dict[str, Any]]
    needs_ocr: bool
    ocr_reason: str | None
    is_ocr: bool
    has_table: bool
    layout_columns: int
    layout: dict[str, Any]
    text_quality: dict[str, Any]
    page_error: str | None
    table_errors: list[str]


@dataclass(frozen=True)
class DocumentSource:
    """A local PDF matched to its verified manifest metadata."""

    doc_id: str
    path: Path
    metadata: dict[str, str]


class PDFExtractionError(RuntimeError):
    """Raised when a PDF cannot be opened or enumerated."""


def _text_quality(text: str) -> dict[str, Any]:
    """Measure selectable-text quality using the documented extraction threshold."""
    compact_text = "".join(character for character in text if not character.isspace())
    alphanumeric_count = sum(character.isalnum() for character in compact_text)
    ratio = alphanumeric_count / len(compact_text) if compact_text else 0.0
    character_count = len(compact_text)
    needs_ocr = (
        character_count < MIN_TEXT_CHARACTERS
        or ratio < MIN_ALPHANUMERIC_RATIO
    )
    if not compact_text:
        reason = "no_extractable_text"
    elif character_count < MIN_TEXT_CHARACTERS:
        reason = "below_minimum_text_characters"
    elif ratio < MIN_ALPHANUMERIC_RATIO:
        reason = "below_minimum_alphanumeric_ratio"
    else:
        reason = None
    return {
        "non_whitespace_characters": character_count,
        "alphanumeric_ratio": round(ratio, 4),
        "minimum_characters": MIN_TEXT_CHARACTERS,
        "minimum_alphanumeric_ratio": MIN_ALPHANUMERIC_RATIO,
        "needs_ocr": needs_ocr,
        "reason": reason,
    }


def is_scanned_page(page: pymupdf.Page) -> bool:
    """Return whether a page falls below the selectable-text quality threshold.

    This is an OCR-candidate check, not proof that the page is scanned: a blank
    page or an unusual form may also fall below the threshold.
    """
    try:
        return bool(_text_quality(page.get_text("text"))["needs_ocr"])
    except Exception:
        logger.exception("Could not assess selectable text on PDF page %s", page.number + 1)
        return True


def _bbox(raw_bbox: Any) -> list[float]:
    return [round(float(value), 2) for value in raw_bbox]


def _remove_bell_character_artifact(text: str) -> str:
    """Remove BEL emitted for visible glyphs by malformed PDF text mappings."""
    return text.replace("\x07", "")


def _block_text(raw_block: dict[str, Any]) -> str:
    text = "\n".join(
        "".join(span.get("text", "") for span in line.get("spans", []))
        for line in raw_block.get("lines", [])
    ).strip()
    return _remove_bell_character_artifact(text)


def _table_data(page: pymupdf.Page) -> tuple[list[dict[str, Any]], list[str]]:
    tables: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        found_tables = page.find_tables()
    except Exception as exc:
        message = f"Table detection failed: {type(exc).__name__}: {exc}"
        logger.warning("Page %s: %s", page.number + 1, message)
        return tables, [message]

    for table_index, table in enumerate(found_tables.tables, start=1):
        try:
            rows = [
                [
                    _remove_bell_character_artifact(cell).strip()
                    if isinstance(cell, str)
                    else ""
                    for cell in row
                ]
                for row in table.extract()
            ]
            if not any(cell for row in rows for cell in row):
                continue
            tables.append(
                {
                    "table_number": table_index,
                    "bbox": _bbox(table.bbox),
                    "row_count": len(rows),
                    "column_count": max((len(row) for row in rows), default=0),
                    "rows": rows,
                    "extraction_method": "pymupdf_find_tables",
                }
            )
        except Exception as exc:
            message = (
                f"Table {table_index} extraction failed: "
                f"{type(exc).__name__}: {exc}"
            )
            logger.warning("Page %s: %s", page.number + 1, message)
            errors.append(message)
    return tables, errors


def _block_is_in_table(block: dict[str, Any], tables: list[dict[str, Any]]) -> bool:
    box = block["bbox"]
    center_x = (box[0] + box[2]) / 2
    center_y = (box[1] + box[3]) / 2
    return any(
        table_box[0] <= center_x <= table_box[2]
        and table_box[1] <= center_y <= table_box[3]
        for table_box in (table["bbox"] for table in tables)
    )


def _is_two_column_layout(
    blocks: list[dict[str, Any]],
    page_width: float,
    page_height: float,
    tables: list[dict[str, Any]],
) -> bool:
    """Recognize two prose columns, excluding blocks inside detected tables."""
    midpoint = page_width / 2
    gutter = page_width * _COLUMN_GUTTER_TOLERANCE
    left: list[dict[str, Any]] = []
    right: list[dict[str, Any]] = []

    for block in blocks:
        text = block["text"]
        box = block["bbox"]
        if (
            block["block_type"] != "text"
            or len(text) < _MIN_COLUMN_BLOCK_CHARACTERS
            or _block_is_in_table(block, tables)
            or box[2] - box[0] > page_width * 0.72
        ):
            continue
        if box[2] <= midpoint + gutter:
            left.append(block)
        elif box[0] >= midpoint - gutter:
            right.append(block)

    if len(left) < 2 or len(right) < 2:
        return False
    if sum(len(block["text"]) for block in left) < _MIN_COLUMN_CHARACTERS:
        return False
    if sum(len(block["text"]) for block in right) < _MIN_COLUMN_CHARACTERS:
        return False

    left_top = min(block["bbox"][1] for block in left)
    left_bottom = max(block["bbox"][3] for block in left)
    right_top = min(block["bbox"][1] for block in right)
    right_bottom = max(block["bbox"][3] for block in right)
    vertical_overlap = min(left_bottom, right_bottom) - max(left_top, right_top)
    return vertical_overlap >= page_height * 0.25


def _order_blocks(
    blocks: list[dict[str, Any]],
    page_width: float,
    page_height: float,
    columns: int,
) -> list[dict[str, Any]]:
    if columns != 2:
        return sorted(blocks, key=lambda block: (block["bbox"][1], block["bbox"][0]))

    midpoint = page_width / 2
    tolerance = page_width * _COLUMN_GUTTER_TOLERANCE
    column_blocks = [
        block
        for block in blocks
        if block["block_type"] == "text"
        and block["bbox"][2] - block["bbox"][0] <= page_width * 0.72
    ]
    if not column_blocks:
        return sorted(blocks, key=lambda block: (block["bbox"][1], block["bbox"][0]))
    body_top = min(block["bbox"][1] for block in column_blocks)
    body_bottom = max(block["bbox"][3] for block in column_blocks)

    headers: list[dict[str, Any]] = []
    footers: list[dict[str, Any]] = []
    middle: list[dict[str, Any]] = []
    left: list[dict[str, Any]] = []
    right: list[dict[str, Any]] = []
    for block in blocks:
        box = block["bbox"]
        width = box[2] - box[0]
        if width > page_width * 0.72:
            if box[3] <= body_top + page_height * 0.03:
                headers.append(block)
            elif box[1] >= body_bottom - page_height * 0.03:
                footers.append(block)
            else:
                middle.append(block)
        elif block["block_type"] != "text":
            middle.append(block)
        elif box[2] <= midpoint + tolerance:
            left.append(block)
        elif box[0] >= midpoint - tolerance:
            right.append(block)
        elif box[3] <= body_top + page_height * 0.03:
            headers.append(block)
        elif box[1] >= body_bottom - page_height * 0.03:
            footers.append(block)
        else:
            middle.append(block)

    by_position = lambda block: (block["bbox"][1], block["bbox"][0])
    ordered = (
        sorted(headers, key=by_position)
        + sorted(left, key=by_position)
        + sorted(middle, key=by_position)
        + sorted(right, key=by_position)
        + sorted(footers, key=by_position)
    )
    return ordered


def _find_headings(
    blocks: list[dict[str, Any]], page_height: float
) -> list[dict[str, Any]]:
    text_blocks = [
        block for block in blocks if block["block_type"] == "text"
    ]
    body_font_sizes = [
        float(span["size"])
        for block in text_blocks
        if len(block["text"].strip()) >= 80
        for line in block["lines"]
        for span in line["spans"]
        if span["text"].strip()
    ]
    font_sizes = body_font_sizes or [
        float(span["size"])
        for block in text_blocks
        for line in block["lines"]
        for span in line["spans"]
        if span["text"].strip()
    ]
    if not font_sizes:
        return []
    typical_size = statistics.median(font_sizes)
    headings: list[dict[str, Any]] = []

    for block in text_blocks:
        for line in block["lines"]:
            text = "".join(span["text"] for span in line["spans"]).strip()
            if not text or len(text) > 180:
                continue
            sizes = [span["size"] for span in line["spans"] if span["text"].strip()]
            if not sizes:
                continue
            max_size = max(sizes)
            is_bold = any(span["flags"] & 16 for span in line["spans"])
            is_uppercase = text.isupper() and any(
                character.isalpha() for character in text
            )
            is_in_body = (
                line["bbox"][1] >= page_height * 0.08
                and line["bbox"][3] <= page_height * 0.90
            )
            is_standalone_italic = (
                len(block["lines"]) == 1
                and all(
                    span["flags"] & 2
                    for span in line["spans"]
                    if span["text"].strip()
                )
                and is_in_body
            )
            if (
                max_size >= typical_size * 1.25
                or (
                    is_bold
                    and max_size >= typical_size
                    and is_in_body
                    and not text.isdigit()
                )
                or (
                    is_uppercase
                    and max_size >= typical_size
                    and is_in_body
                )
                or (is_standalone_italic and max_size >= typical_size)
            ):
                headings.append(
                    {
                        "text": text,
                        "bbox": line["bbox"],
                        "font_size": round(max_size, 2),
                    }
                )
    return headings


def _readable_table_text(tables: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for table in tables:
        for row in table["rows"]:
            cells = [cell.replace("\n", " ").strip() for cell in row]
            if any(cells):
                lines.append(" | ".join(cells))
    return "\n".join(lines)


def _failed_page_data(
    doc_id: str,
    page_number: int,
    source_filename: str,
    source_hash: str,
    document_title: str,
    error: Exception,
) -> PageData:
    message = f"{type(error).__name__}: {error}"
    return {
        "doc_id": doc_id,
        "document_title": document_title,
        "source_filename": source_filename,
        "source_hash": source_hash,
        "page_number": page_number,
        "text": "",
        "blocks": [],
        "headings": [],
        "tables": [],
        "needs_ocr": True,
        "ocr_reason": "page_extraction_error",
        "is_ocr": False,
        "has_table": False,
        "layout_columns": 1,
        "layout": {
            "column_count": 1,
            "reading_order": "unavailable",
            "reading_order_heuristic": (
                "Page-level extraction failed; no reading order is available."
            ),
        },
        "text_quality": _text_quality(""),
        "page_error": message,
        "table_errors": [],
    }


def extract_page_text(
    page: pymupdf.Page,
    doc_id: str,
    page_number: int,
    source_filename: str = "",
    source_hash: str = "",
    document_title: str = "",
) -> PageData:
    """Extract text, positional blocks, headings, and tables from one page.

    Table text is retained in structured ``tables``. When a page contains only
    tables, ``text`` includes a readable pipe-delimited fallback rather than
    flattening rows into an unstructured paragraph.
    """
    try:
        raw_blocks = page.get_text("dict", sort=False).get("blocks", [])
        tables, table_errors = _table_data(page)
        blocks: list[dict[str, Any]] = []
        for raw_block in raw_blocks:
            block_type = "text" if raw_block.get("type") == 0 else "image"
            lines: list[dict[str, Any]] = []
            if block_type == "text":
                for raw_line in raw_block.get("lines", []):
                    spans = [
                        {
                            "text": _remove_bell_character_artifact(
                                span.get("text", "")
                            ),
                            "bbox": _bbox(span["bbox"]) if span.get("bbox") else [],
                            "font": span.get("font", ""),
                            "size": round(float(span.get("size", 0.0)), 2),
                            "flags": int(span.get("flags", 0)),
                        }
                        for span in raw_line.get("spans", [])
                    ]
                    lines.append(
                        {
                            "bbox": (
                                _bbox(raw_line["bbox"])
                                if raw_line.get("bbox")
                                else []
                            ),
                            "spans": spans,
                        }
                    )
            bbox = _bbox(raw_block.get("bbox", (0, 0, 0, 0)))
            block = {
                "block_type": block_type,
                "bbox": bbox,
                "text": _block_text(raw_block) if block_type == "text" else "",
                "lines": lines,
            }
            if block_type == "text" and _block_is_in_table(block, tables):
                block["block_type"] = "table"
            blocks.append(block)

        page_width = float(page.rect.width)
        page_height = float(page.rect.height)
        columns = (
            2
            if _is_two_column_layout(blocks, page_width, page_height, tables)
            else 1
        )
        ordered_blocks = _order_blocks(blocks, page_width, page_height, columns)
        for order, block in enumerate(ordered_blocks):
            block["reading_order"] = order

        paragraph_text = "\n".join(
            block["text"]
            for block in ordered_blocks
            if block["block_type"] == "text" and block["text"]
        )
        text = paragraph_text or _readable_table_text(tables)
        table_text = _readable_table_text(tables)
        quality = _text_quality("\n".join(part for part in (paragraph_text, table_text) if part))
        needs_ocr = bool(quality["needs_ocr"])
        layout = {
            "column_count": columns,
            "reading_order": (
                "left_column_then_right_column"
                if columns == 2
                else "top_to_bottom_then_left_to_right"
            ),
            "reading_order_heuristic": (
                "For two-column pages, positioned text blocks are read down the "
                "left column before the right; full-width blocks are kept at "
                "the page edges where their coordinates indicate headers or footers."
                if columns == 2
                else "Text blocks are sorted by vertical position, then horizontal position."
            ),
            "page_width": round(page_width, 2),
            "page_height": round(page_height, 2),
        }
        return {
            "doc_id": doc_id,
            "document_title": document_title,
            "source_filename": source_filename or page.parent.name,
            "source_hash": source_hash,
            "page_number": page_number,
            "text": text,
            "blocks": ordered_blocks,
            "headings": _find_headings(ordered_blocks, page_height),
            "tables": tables,
            "needs_ocr": needs_ocr,
            "ocr_reason": quality["reason"],
            "is_ocr": False,
            "has_table": bool(tables),
            "layout_columns": columns,
            "layout": layout,
            "text_quality": quality,
            "page_error": None,
            "table_errors": table_errors,
        }
    except Exception as exc:
        logger.exception(
            "Page extraction failed for %s page %d", doc_id, page_number
        )
        return _failed_page_data(
            doc_id,
            page_number,
            source_filename,
            source_hash,
            document_title,
            exc,
        )


def extract_pdf(
    pdf_path: Path,
    doc_id: str,
    source_hash: str = "",
    document_title: str = "",
) -> list[PageData]:
    """Extract every page from a PDF, continuing after page-level failures."""
    pdf_path = Path(pdf_path)
    try:
        document = pymupdf.open(pdf_path)
    except Exception as exc:
        logger.exception("Could not open PDF %s", pdf_path)
        raise PDFExtractionError(
            f"Could not open PDF {pdf_path}: {type(exc).__name__}: {exc}"
        ) from exc

    pages: list[PageData] = []
    try:
        for page_index in range(document.page_count):
            page_number = page_index + 1
            try:
                page = document.load_page(page_index)
                page_data = extract_page_text(
                    page,
                    doc_id,
                    page_number,
                    source_filename=pdf_path.name,
                    source_hash=source_hash,
                    document_title=document_title,
                )
            except Exception as exc:
                logger.exception(
                    "Could not load %s page %d", pdf_path.name, page_number
                )
                page_data = _failed_page_data(
                    doc_id,
                    page_number,
                    pdf_path.name,
                    source_hash,
                    document_title,
                    exc,
                )
            pages.append(page_data)
    finally:
        document.close()
    return pages


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_documents(
    pdf_dir: Path = PDF_DIR,
    manifest_path: Path = MANIFEST_PATH,
) -> tuple[list[DocumentSource], list[dict[str, str]]]:
    """Match local PDFs to verified manifest rows without changing the manifest."""
    pdf_dir = Path(pdf_dir)
    manifest_path = Path(manifest_path)
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    if not pdf_dir.is_dir():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    with manifest_path.open("r", encoding="utf-8", newline="") as manifest_file:
        reader = csv.DictReader(manifest_file)
        if not reader.fieldnames or not {"doc_id", "download_status"} <= set(reader.fieldnames):
            raise ValueError(f"Manifest has invalid headers: {manifest_path}")
        rows = list(reader)

    pdf_paths = sorted(path for path in pdf_dir.glob("*.pdf") if path.is_file())
    unassigned = set(pdf_paths)
    sources: list[DocumentSource] = []
    errors: list[dict[str, str]] = []

    for row in rows:
        if row.get("download_status", "").strip().lower() != "verified":
            continue
        doc_id = row.get("doc_id", "").strip()
        if not doc_id:
            errors.append(
                {"kind": "manifest_error", "message": "Verified manifest row has no doc_id."}
            )
            continue
        prefix_matches = sorted(
            path
            for path in unassigned
            if path.stem == doc_id or path.stem.startswith(f"{doc_id}_")
        )
        match: Path | None = None
        if len(prefix_matches) == 1:
            match = prefix_matches[0]
        elif len(prefix_matches) > 1:
            errors.append(
                {
                    "kind": "ambiguous_pdf",
                    "doc_id": doc_id,
                    "message": "Multiple local PDFs use this document ID prefix.",
                }
            )
            continue
        else:
            source_hash = row.get("source_hash", "").strip().lower()
            if source_hash:
                hash_matches: list[Path] = []
                for path in sorted(unassigned):
                    try:
                        if _sha256(path) == source_hash:
                            hash_matches.append(path)
                    except OSError as exc:
                        errors.append(
                            {
                                "kind": "file_error",
                                "source_filename": path.name,
                                "message": f"{type(exc).__name__}: {exc}",
                            }
                        )
                if len(hash_matches) == 1:
                    match = hash_matches[0]
                elif len(hash_matches) > 1:
                    errors.append(
                        {
                            "kind": "ambiguous_hash",
                            "doc_id": doc_id,
                            "message": "Multiple local PDFs match this manifest SHA-256.",
                        }
                    )
                    continue
        if match is None:
            errors.append(
                {
                    "kind": "missing_pdf",
                    "doc_id": doc_id,
                    "message": "No local PDF matches this verified manifest row.",
                }
            )
            continue
        unassigned.remove(match)
        sources.append(
            DocumentSource(
                doc_id=doc_id,
                path=match,
                metadata={key: value or "" for key, value in row.items()},
            )
        )

    for path in sorted(unassigned):
        errors.append(
            {
                "kind": "unmatched_pdf",
                "source_filename": path.name,
                "message": "Local PDF is not linked to a verified manifest row.",
            }
        )
    return sources, errors


def _write_jsonl(path: Path, pages: list[PageData]) -> None:
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as output_file:
            for page in pages:
                output_file.write(
                    json.dumps(page, ensure_ascii=False, separators=(",", ":"))
                    + "\n"
                )
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def extract_corpus(
    pdf_dir: Path = PDF_DIR,
    manifest_path: Path = MANIFEST_PATH,
    output_dir: Path = PROCESSED_DIR,
) -> dict[str, Any]:
    """Extract all verified local PDFs, writing one JSONL record per page."""
    pdf_dir = Path(pdf_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    local_pdf_count = len(
        [path for path in pdf_dir.glob("*.pdf") if path.is_file()]
    )
    sources, discovery_errors = discover_documents(pdf_dir, manifest_path)
    errors: list[dict[str, Any]] = list(discovery_errors)
    all_pages: list[PageData] = []
    processed_documents = 0
    failed_documents = 0
    table_extraction_failures = 0

    for source in sources:
        try:
            pages = extract_pdf(
                source.path,
                source.doc_id,
                source_hash=source.metadata.get("source_hash", ""),
                document_title=source.metadata.get("title", ""),
            )
            _write_jsonl(output_dir / f"{source.doc_id}.jsonl", pages)
            processed_documents += 1
            all_pages.extend(pages)
            for page in pages:
                for message in page["table_errors"]:
                    table_extraction_failures += 1
                    errors.append(
                        {
                            "kind": "table_extraction_error",
                            "doc_id": source.doc_id,
                            "source_filename": source.path.name,
                            "page_number": page["page_number"],
                            "message": message,
                        }
                    )
                if page["page_error"]:
                    errors.append(
                        {
                            "kind": "page_extraction_error",
                            "doc_id": source.doc_id,
                            "source_filename": source.path.name,
                            "page_number": page["page_number"],
                            "message": page["page_error"],
                        }
                    )
        except Exception as exc:
            failed_documents += 1
            message = f"{type(exc).__name__}: {exc}"
            logger.exception("Document extraction failed for %s", source.path)
            errors.append(
                {
                    "kind": "document_extraction_error",
                    "doc_id": source.doc_id,
                    "source_filename": source.path.name,
                    "message": message,
                }
            )

    for error in errors:
        if error.get("kind") in {
            "missing_pdf",
            "ambiguous_pdf",
            "ambiguous_hash",
            "unmatched_pdf",
            "file_error",
            "manifest_error",
        }:
            logger.error("Document discovery issue: %s", error)
        elif error.get("kind") in {"page_extraction_error", "table_extraction_error"}:
            logger.error("Extraction issue: %s", error)

    summary: dict[str, Any] = {
        "documents_discovered": local_pdf_count,
        "documents_matched": len(sources),
        "documents_processed": processed_documents,
        "documents_failed": failed_documents,
        "pages_processed": len(all_pages),
        "pages_successfully_extracted": sum(
            page["page_error"] is None and not page["needs_ocr"]
            for page in all_pages
        ),
        "pages_flagged_for_ocr": sum(
            page["page_error"] is None and page["needs_ocr"]
            for page in all_pages
        ),
        "pages_failed": sum(page["page_error"] is not None for page in all_pages),
        "tables_extracted": sum(len(page["tables"]) for page in all_pages),
        "table_extraction_failures": table_extraction_failures,
        "extraction_failures": failed_documents
        + sum(page["page_error"] is not None for page in all_pages)
        + sum(
            error.get("kind")
            in {
                "missing_pdf",
                "ambiguous_pdf",
                "ambiguous_hash",
                "unmatched_pdf",
                "file_error",
                "manifest_error",
            }
            for error in discovery_errors
        ),
        "errors": errors,
    }
    (output_dir / "extraction_errors.jsonl").write_text(
        "".join(
            json.dumps(error, ensure_ascii=False, separators=(",", ":")) + "\n"
            for error in errors
        ),
        encoding="utf-8",
    )
    (output_dir / "extraction_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    logger.info(
        "Extraction complete: %d/%d documents, %d/%d pages extracted, "
        "%d OCR candidates, %d page/document failures, %d tables.",
        processed_documents,
        local_pdf_count,
        summary["pages_successfully_extracted"],
        summary["pages_processed"],
        summary["pages_flagged_for_ocr"],
        summary["extraction_failures"],
        summary["tables_extracted"],
    )
    return summary


def _configure_logging() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "extraction.log", encoding="utf-8"),
        ],
        force=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract page-level text and layout metadata from PolicyLens PDFs."
    )
    parser.add_argument("--pdf-dir", type=Path, default=PDF_DIR)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output-dir", type=Path, default=PROCESSED_DIR)
    args = parser.parse_args(argv)
    _configure_logging()

    try:
        summary = extract_corpus(args.pdf_dir, args.manifest, args.output_dir)
    except (OSError, ValueError, csv.Error) as exc:
        logger.exception("Extraction could not start: %s", exc)
        return 1
    print(json.dumps({key: value for key, value in summary.items() if key != "errors"}, indent=2))
    return 0 if summary["extraction_failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

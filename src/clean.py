"""Conservative, traceable text normalization for page-level PDF records.

Raw extraction and OCR JSONL files are read-only inputs. Cleaned records are
written separately under ``data/processed/cleaned`` and retain the original
record fields alongside a canonical text and cleaning provenance.
"""

from __future__ import annotations

import argparse
import copy
import json
import logging
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.config import LOGS_DIR, PROCESSED_DIR
from src.extract import _text_quality

logger = logging.getLogger("policylens.clean")

_REPEATED_EDGE_FRACTION = 0.6
_MIN_REPEATED_EDGE_PAGES = 3
_MAX_EDGE_LINE_LENGTH = 120
_LINE_WRAP_HYPHEN = re.compile(r"([A-Za-z]{2,})-$")
_LINE_WRAP_SUFFIX = re.compile(r"^[a-z][A-Za-z]{1,}(?:\b|$)")
_STANDALONE_SECTION_LABEL = re.compile(
    r"(?:(?:[ivxlcdm]+|\d+)(?:\.(?:[ivxlcdm]+|\d+))*[.)]?|\(?[a-zA-Z][.)])",
    re.IGNORECASE,
)
_VISIBLE_HYPHEN_BREAK = re.compile(
    r"([A-Za-z]{2,})-\n([a-z][A-Za-z]{1,}(?:\b|$))"
)
_PAGE_NUMBER = re.compile(r"\d{1,4}")
_PROTECTED_EDGE_TERMS = re.compile(
    r"\b(?:act|acts|rule|rules|regulation|regulations|section|schedule|"
    r"notification|circular|policy|policies|code|loan|interest|rate|rates|"
    r"reserve bank|rbi|government|gazette|inr|rupees?)\b|₹|%",
    re.IGNORECASE,
)


def _normalize_line_key(text: str) -> str:
    return " ".join(text.split()).casefold()


def _source_text(record: dict[str, Any]) -> tuple[str, str, str, dict[str, Any]]:
    has_separate_native_text = "native_text" in record
    native_text = record.get("native_text", record.get("text", ""))
    if not isinstance(native_text, str):
        native_text = ""
    native_quality = _text_quality(native_text)
    ocr = record.get("ocr")
    if (
        record.get("is_ocr") is True
        and isinstance(ocr, dict)
        and ocr.get("status") == "success"
        and isinstance(ocr.get("text"), str)
        and ocr["text"].strip()
        and (not has_separate_native_text or native_quality["needs_ocr"])
    ):
        return (
            ocr["text"],
            "ocr",
            (
                "native_text_missing_and_combined_text_not_trusted"
                if not has_separate_native_text
                else "native_text_below_extraction_quality_threshold"
            ),
            native_quality,
        )
    if native_text.strip():
        reason = (
            "native_text_meets_extraction_quality_threshold"
            if not native_quality["needs_ocr"]
            else "no_valid_ocr_fallback"
        )
        return native_text, "native", reason, native_quality
    return native_text, "native", "no_usable_text_source", native_quality


def _edge_lines(text: str) -> dict[str, set[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return {"top": set(), "bottom": set()}
    bottom_start = max(2, len(lines) - 2)
    return {
        "top": {line for line in lines[:2] if len(line) <= _MAX_EDGE_LINE_LENGTH},
        "bottom": {
            line
            for line in lines[bottom_start:]
            if len(line) <= _MAX_EDGE_LINE_LENGTH
        },
    }


def _protected_edge_line(
    line: str,
    document_title_keys: set[str],
    heading_keys: set[str],
    cover_line_keys: set[str],
) -> bool:
    key = _normalize_line_key(line)
    title_match = any(
        key == title
        or (
            len(key) >= 12
            and len(title) >= 12
            and (title in key or key in title)
        )
        for title in document_title_keys
    )
    return (
        title_match
        or key in heading_keys
        or key in cover_line_keys
        or bool(_PROTECTED_EDGE_TERMS.search(line))
        or bool(re.search(r"\d", line))
    )


def _document_furniture(
    records: list[dict[str, Any]], source_texts: list[tuple[str, str, str, dict[str, Any]]]
) -> tuple[
    dict[str, set[str]],
    dict[str, set[str]],
    list[dict[str, Any]],
]:
    edge_pages: dict[tuple[str, str], set[int]] = defaultdict(set)
    page_number_pages: dict[str, set[int]] = defaultdict(set)
    document_title_keys = {
        _normalize_line_key(record.get("document_title", ""))
        for record in records
        if record.get("document_title")
    }
    heading_keys = {
        _normalize_line_key(heading.get("text", ""))
        for record in records
        for heading in record.get("headings", [])
        if isinstance(heading, dict) and heading.get("text")
    }
    cover_line_keys = {
        _normalize_line_key(line)
        for line in source_texts[0][0].splitlines()
        if line.strip()
    }
    for record, (text, _source, _reason, _quality) in zip(
        records, source_texts, strict=True
    ):
        page_number = record.get("page_number")
        for edge, lines in _edge_lines(text).items():
            for line in lines:
                edge_pages[(edge, _normalize_line_key(line))].add(page_number)
        for edge, lines in _edge_lines(text).items():
            for line in lines:
                if (
                    _PAGE_NUMBER.fullmatch(line)
                    and line == str(page_number)
                ):
                    page_number_pages[edge].add(page_number)

    required_pages = max(
        _MIN_REPEATED_EDGE_PAGES,
        math.ceil(len(records) * _REPEATED_EDGE_FRACTION),
    )
    removable_headers: dict[str, set[str]] = {"top": set(), "bottom": set()}
    candidates: list[dict[str, Any]] = []
    for (edge, line_key), pages in sorted(edge_pages.items()):
        if len(pages) < required_pages:
            continue
        example = next(
            line
            for text, _source, _reason, _quality in source_texts
            for edge_lines in _edge_lines(text).values()
            for line in edge_lines
            if _normalize_line_key(line) == line_key
        )
        if _protected_edge_line(
            example, document_title_keys, heading_keys, cover_line_keys
        ):
            action = "retained_title_heading_or_substantive_edge_text"
        else:
            removable_headers[edge].add(line_key)
            action = "removed_repeating_edge_line"
        candidates.append(
            {
                "edge": edge,
                "text": example,
                "pages": len(pages),
                "action": action,
            }
        )

    removable_page_numbers = {
        edge
        for edge, pages in page_number_pages.items()
        if len(pages) >= required_pages
    }
    return removable_headers, removable_page_numbers, candidates


def _native_line_wrap_pairs(
    record: dict[str, Any], source: str
) -> dict[tuple[str, str], str]:
    if source != "native":
        return {}
    pairs: dict[tuple[str, str], str] = {}
    for block in record.get("blocks", []):
        if not isinstance(block, dict) or block.get("block_type") != "text":
            continue
        block_lines = block.get("lines", [])
        rendered_lines = []
        for line in block_lines:
            if not isinstance(line, dict):
                continue
            line_text = "".join(
                span.get("text", "")
                for span in line.get("spans", [])
                if isinstance(span, dict)
            ).strip()
            rendered_lines.append((line_text, line.get("bbox", [])))
        for (previous, previous_bbox), (following, following_bbox) in zip(
            rendered_lines, rendered_lines[1:]
        ):
            if not previous or not following:
                continue
            if (
                previous in {"•", "·", "\uf0b7", "-", "–", "—"}
                or _STANDALONE_SECTION_LABEL.fullmatch(previous.strip())
                or re.match(
                    r"^(?:[•·\uf0b7]|[-–—]|\(?\d+[.)]|\(?[a-zA-Z][.)])\s",
                    following,
                )
            ):
                continue
            if len(previous_bbox) == 4 and len(following_bbox) == 4:
                previous_height = previous_bbox[3] - previous_bbox[1]
                following_gap = following_bbox[1] - previous_bbox[3]
                if following_gap > max(2.0, previous_height * 0.8):
                    continue
            previous_key = " ".join(previous.split())
            following_key = " ".join(following.split())
            joiner = (
                ""
                if _LINE_WRAP_HYPHEN.search(previous)
                and _LINE_WRAP_SUFFIX.match(following)
                else " "
            )
            pairs[(previous_key, following_key)] = joiner
    return pairs


def _normalize_whitespace(
    text: str, line_wrap_pairs: dict[tuple[str, str], str]
) -> tuple[str, dict[str, int], list[str]]:
    operations = {
        "soft_hyphens_removed": text.count("\u00ad"),
        "hyphenation_line_joins": 0,
        "wrapped_line_joins": 0,
        "repeated_blank_lines_collapsed": 0,
    }
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00ad", "")
    lines = [re.sub(r"[ ]{2,}", " ", line.strip()) for line in text.split("\n")]
    joined: list[str] = []
    index = 0
    unresolved: list[str] = []
    while index < len(lines):
        current = lines[index]
        if index + 1 < len(lines) and current and lines[index + 1]:
            following = lines[index + 1]
            matching_joiner = next(
                (
                    joiner
                    for (previous_block_line, next_block_line), joiner
                    in line_wrap_pairs.items()
                    if current.endswith(previous_block_line)
                    and following.startswith(next_block_line)
                ),
                None,
            )
            if matching_joiner is not None:
                joined.append(current + matching_joiner + following)
                if matching_joiner == "":
                    operations["hyphenation_line_joins"] += 1
                else:
                    operations["wrapped_line_joins"] += 1
                index += 2
                continue
            if _VISIBLE_HYPHEN_BREAK.search(current + "\n" + following):
                unresolved.append(f"{current}\n{following}")
        joined.append(current)
        index += 1

    collapsed: list[str] = []
    blank_count = 0
    for line in joined:
        if line:
            blank_count = 0
            collapsed.append(line)
        else:
            blank_count += 1
            if blank_count <= 1:
                collapsed.append("")
            else:
                operations["repeated_blank_lines_collapsed"] += 1
    return "\n".join(collapsed).strip(), operations, unresolved


def _remove_edge_lines(
    text: str,
    record: dict[str, Any],
    removable_headers: dict[str, set[str]],
    removable_page_numbers: set[str],
) -> tuple[str, list[str], bool]:
    lines = text.splitlines()
    nonempty_indices = [index for index, line in enumerate(lines) if line.strip()]
    if not nonempty_indices:
        return text, [], False
    top_indices = set(nonempty_indices[:2])
    bottom_start = max(2, len(nonempty_indices) - 2)
    bottom_indices = set(nonempty_indices[bottom_start:])
    removed_headers: list[str] = []
    page_number_removed = False
    for index in sorted(top_indices | bottom_indices):
        line = lines[index].strip()
        key = _normalize_line_key(line)
        edge = "top" if index in top_indices else "bottom"
        if key in removable_headers.get(edge, set()):
            removed_headers.append(line)
            lines[index] = ""
        elif (
            edge in removable_page_numbers
            and _PAGE_NUMBER.fullmatch(line)
            and line == str(record.get("page_number"))
        ):
            lines[index] = ""
            page_number_removed = True
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return cleaned, removed_headers, page_number_removed


def clean_document_records(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Return cleaned copies of one document's page records and run counts."""
    if not records:
        return [], {
            "pages_processed": 0,
            "pages_changed": 0,
            "native_selected_pages": 0,
            "ocr_selected_pages": 0,
            "repeating_header_footer_candidates": 0,
            "repeating_header_footer_lines_removed": 0,
            "page_numbers_removed": 0,
            "hyphenation_line_joins": 0,
            "wrapped_line_joins": 0,
            "pages_needing_review": 0,
        }
    doc_ids = {record.get("doc_id") for record in records}
    page_numbers = [record.get("page_number") for record in records]
    if len(doc_ids) != 1 or None in doc_ids:
        raise ValueError("A cleaning input file must contain one non-empty doc_id.")
    if len(page_numbers) != len(set(page_numbers)) or any(
        not isinstance(number, int) or number < 1 for number in page_numbers
    ):
        raise ValueError("Page numbers must be unique positive integers.")

    sources = [_source_text(record) for record in records]
    removable_headers, removable_page_numbers, edge_candidates = (
        _document_furniture(records, sources)
    )
    output: list[dict[str, Any]] = []
    pages_changed = native_selected = ocr_selected = header_removed = 0
    page_numbers_removed = hyphenation_joins = pages_needing_review = 0
    for record, (source_text, selected_source, selection_reason, native_quality) in zip(
        records, sources, strict=True
    ):
        line_wrap_pairs = _native_line_wrap_pairs(record, selected_source)
        normalized, operations, unresolved_hyphenation = _normalize_whitespace(
            source_text, line_wrap_pairs
        )
        current_edges = _edge_lines(normalized)
        page_edge_candidates = [
            candidate
            for candidate in edge_candidates
            if _normalize_line_key(candidate["text"])
            in {
                _normalize_line_key(line)
                for line in current_edges[candidate["edge"]]
            }
        ]
        canonical_text, removed_headers, removed_page_number = _remove_edge_lines(
            normalized,
            record,
            removable_headers,
            removable_page_numbers,
        )
        review_reasons: list[str] = []
        if selected_source == "ocr":
            review_reasons.append("canonical text is OCR-derived")
        if unresolved_hyphenation:
            review_reasons.append("ambiguous visible-hyphen line break preserved")
        if record.get("page_error"):
            review_reasons.append("source page has an extraction error")
        if record.get("has_table") and selected_source == "ocr":
            review_reasons.append("OCR table content is not structured table data")
        ocr = record.get("ocr")
        if (
            selected_source == "ocr"
            and isinstance(ocr, dict)
            and isinstance(ocr.get("confidence_mean"), (int, float))
            and ocr["confidence_mean"] < 90
        ):
            review_reasons.append("OCR mean confidence is below 90")

        cleaned_record = copy.deepcopy(record)
        cleaned_record["canonical_text"] = canonical_text
        cleaned_record["cleaning"] = {
            "schema_version": 1,
            "selected_source": selected_source,
            "selection_reason": selection_reason,
            "native_text_quality": native_quality,
            "ocr_provenance": (
                {
                    key: ocr[key]
                    for key in (
                        "engine",
                        "engine_version",
                        "language",
                        "source_filename",
                        "source_hash",
                        "source_page_number",
                        "confidence_mean",
                        "confidence_min",
                    )
                    if key in ocr
                }
                if selected_source == "ocr" and isinstance(ocr, dict)
                else None
            ),
            "whitespace_operations": operations,
            "repeating_edge_line_candidates": page_edge_candidates,
            "repeating_edge_lines_removed": removed_headers,
            "page_number_removed": removed_page_number,
            "hyphenation_line_joins": operations["hyphenation_line_joins"],
            "wrapped_line_joins": operations["wrapped_line_joins"],
            "unresolved_hyphenation_candidates": unresolved_hyphenation,
            "needs_manual_review": bool(review_reasons),
            "review_reasons": review_reasons,
        }
        output.append(cleaned_record)
        pages_changed += canonical_text != source_text
        native_selected += selected_source == "native"
        ocr_selected += selected_source == "ocr"
        header_removed += len(removed_headers)
        page_numbers_removed += removed_page_number
        hyphenation_joins += operations["hyphenation_line_joins"]
        pages_needing_review += bool(review_reasons)

    counts = {
        "pages_processed": len(records),
        "pages_changed": pages_changed,
        "native_selected_pages": native_selected,
        "ocr_selected_pages": ocr_selected,
        "repeating_header_footer_candidates": len(edge_candidates),
        "repeating_header_footer_lines_removed": header_removed,
        "page_numbers_removed": page_numbers_removed,
        "hyphenation_line_joins": hyphenation_joins,
        "wrapped_line_joins": sum(
            page["cleaning"]["whitespace_operations"]["wrapped_line_joins"]
            for page in output
        ),
        "pages_needing_review": pages_needing_review,
    }
    return output, counts


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path} line {line_number}: {exc}"
                ) from exc
            if not isinstance(record, dict):
                raise ValueError(f"Expected a JSON object in {path} line {line_number}.")
            records.append(record)
    return records


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as output_file:
            for record in records:
                output_file.write(
                    json.dumps(record, ensure_ascii=False, separators=(",", ":"))
                    + "\n"
                )
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _write_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        temporary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def clean_corpus(
    input_dir: Path = PROCESSED_DIR,
    output_dir: Path = PROCESSED_DIR / "cleaned",
    summary_path: Path = PROCESSED_DIR / "cleaning_summary.json",
) -> dict[str, Any]:
    """Clean every top-level per-document JSONL without changing raw inputs."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    summary_path = Path(summary_path)
    if input_dir.resolve() == output_dir.resolve():
        raise ValueError("Cleaned output directory must differ from the raw input directory.")
    input_paths = sorted(
        path for path in input_dir.glob("doc_*.jsonl") if path.is_file()
    )
    if not input_paths:
        raise FileNotFoundError(f"No per-document JSONL files found in {input_dir}.")

    totals = {
        "pages_processed": 0,
        "pages_changed": 0,
        "native_selected_pages": 0,
        "ocr_selected_pages": 0,
        "repeating_header_footer_candidates": 0,
        "repeating_header_footer_lines_removed": 0,
        "page_numbers_removed": 0,
        "hyphenation_line_joins": 0,
        "wrapped_line_joins": 0,
        "pages_needing_review": 0,
    }
    errors: list[dict[str, str]] = []
    documents_processed = 0
    for input_path in input_paths:
        try:
            records = _read_jsonl(input_path)
            cleaned, counts = clean_document_records(records)
            _write_jsonl(output_dir / input_path.name, cleaned)
            documents_processed += 1
            for key, value in counts.items():
                totals[key] += value
        except (OSError, ValueError, TypeError) as exc:
            logger.exception("Could not clean document output %s", input_path)
            errors.append(
                {
                    "source_file": input_path.name,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    summary = {
        "stage": "conservative_text_cleaning",
        "schema_version": 1,
        "input_directory": str(input_dir),
        "output_directory": str(output_dir),
        "documents_discovered": len(input_paths),
        "documents_processed": documents_processed,
        "documents_failed": len(errors),
        **totals,
        "errors": errors,
    }
    _write_summary(summary_path, summary)
    logger.info(
        "Cleaning complete: %d documents, %d pages, %d changed, %d failures",
        documents_processed,
        totals["pages_processed"],
        totals["pages_changed"],
        len(errors),
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create conservative cleaned copies of page-level JSONL records."
    )
    parser.add_argument("--input-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--output-dir", type=Path, default=PROCESSED_DIR / "cleaned")
    parser.add_argument(
        "--summary",
        type=Path,
        default=PROCESSED_DIR / "cleaning_summary.json",
    )
    args = parser.parse_args(argv)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(LOGS_DIR / "cleaning.log", encoding="utf-8"),
        ],
    )
    try:
        summary = clean_corpus(args.input_dir, args.output_dir, args.summary)
    except (OSError, ValueError) as exc:
        logger.error("Cleaning could not start: %s", exc)
        return 1
    return 1 if summary["documents_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

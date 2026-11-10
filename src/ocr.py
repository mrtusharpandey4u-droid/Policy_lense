"""Targeted, page-level OCR fallback for PolicyLens extraction outputs.

The Tesseract command-line interface is used directly so OCR does not require
Pillow or a Python wrapper. OCR text is applied only to pages whose native
extraction is insufficient; original native text and table data are retained.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import pymupdf

from src.config import (
    LOGS_DIR,
    OCR_DPI,
    OCR_LANGUAGE,
    OCR_PAGE_SEGMENTATION_MODE,
    OCR_TIMEOUT_SECONDS,
    PDF_DIR,
    PROCESSED_DIR,
    REPORTS_DIR,
    TESSERACT_CMD,
)
from src.extract import _text_quality, _write_jsonl

logger = logging.getLogger("policylens.ocr")

LANGUAGE_OVERRIDES = {
    ("doc_004", 1): "eng+hin",
    ("doc_004", 2): "eng+hin",
    ("doc_009", 49): "eng+hin",
    ("doc_010", 1): "eng+hin",
    ("doc_011", 1): "eng+hin",
    ("doc_014", 3): "hin",
    ("doc_015", 1): "eng+hin",
    ("doc_015", 2): "eng+hin",
}
OCR_TARGET_INVENTORY_PATH = REPORTS_DIR / "ocr_target_inventory.csv"

INVENTORY_FIELDS = [
    "doc_id",
    "PDF page number",
    "original OCR classification",
    "reason for inclusion/exclusion",
    "overlaps with previously reported extraction gap",
    "OCR language required",
    "processing status",
]


class OCRPrerequisiteError(RuntimeError):
    """Raised when Tesseract or required language data is unavailable."""


class OCRProcessingError(RuntimeError):
    """Raised for a page-level OCR failure."""


@dataclass(frozen=True)
class OCRResult:
    """Text and confidence summary returned by the OCR engine."""

    text: str
    confidence_mean: float | None
    confidence_min: float | None
    confidence_word_count: int


@dataclass(frozen=True)
class EngineInfo:
    """Installed Tesseract version and language data."""

    version: str
    languages: frozenset[str]


class OCRBackend(Protocol):
    """Interface that allows the page pipeline to be tested without Tesseract."""

    def inspect(self) -> EngineInfo:
        """Return engine version and installed language codes."""

    def recognize(self, page: pymupdf.Page, language: str) -> OCRResult:
        """OCR one already-selected page."""


def _parse_tsv(tsv_text: str) -> OCRResult:
    reader = csv.DictReader(
        tsv_text.splitlines(),
        delimiter="\t",
        quoting=csv.QUOTE_NONE,
    )
    required = {"text", "conf", "block_num", "par_num", "line_num", "level"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise OCRProcessingError("Tesseract returned malformed TSV output.")

    lines: dict[tuple[str, str, str], list[str]] = {}
    confidences: list[float] = []
    for row in reader:
        if row.get("level") != "5":
            continue
        word = (row.get("text") or "").strip()
        if not word:
            continue
        key = (row["block_num"], row["par_num"], row["line_num"])
        lines.setdefault(key, []).append(word)
        try:
            confidence = float(row["conf"])
        except (TypeError, ValueError):
            continue
        if confidence >= 0:
            confidences.append(confidence)

    text = "\n".join(" ".join(words) for words in lines.values()).strip()
    return OCRResult(
        text=text,
        confidence_mean=(
            round(sum(confidences) / len(confidences), 2)
            if confidences
            else None
        ),
        confidence_min=round(min(confidences), 2) if confidences else None,
        confidence_word_count=len(confidences),
    )


class TesseractBackend:
    """Run the local Tesseract executable on PyMuPDF-rendered page images."""

    def __init__(
        self,
        command: str = TESSERACT_CMD,
        dpi: int = OCR_DPI,
        timeout_seconds: int = OCR_TIMEOUT_SECONDS,
        page_segmentation_mode: int = OCR_PAGE_SEGMENTATION_MODE,
    ) -> None:
        if dpi < 150:
            raise ValueError("OCR resolution must be at least 150 DPI.")
        if timeout_seconds <= 0:
            raise ValueError("OCR timeout must be greater than zero.")
        self.command = command
        self.dpi = dpi
        self.timeout_seconds = timeout_seconds
        self.page_segmentation_mode = page_segmentation_mode

    def inspect(self) -> EngineInfo:
        executable = shutil.which(self.command)
        if executable is None and not Path(self.command).is_file():
            raise OCRPrerequisiteError(
                f"Tesseract executable not found: {self.command}. "
                "Install Tesseract and set TESSERACT_CMD if it is not on PATH."
            )
        try:
            version_result = subprocess.run(
                [self.command, "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            language_result = subprocess.run(
                [self.command, "--list-langs"],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise OCRPrerequisiteError(
                f"Could not inspect Tesseract: {type(exc).__name__}: {exc}"
            ) from exc

        if version_result.returncode != 0:
            raise OCRPrerequisiteError(
                f"Tesseract version check failed: {version_result.stderr.strip()}"
            )
        if language_result.returncode != 0:
            raise OCRPrerequisiteError(
                f"Tesseract language check failed: {language_result.stderr.strip()}"
            )

        version = (version_result.stdout or version_result.stderr).splitlines()
        version = version[0].strip() if version else "unknown"
        language_lines = language_result.stdout.splitlines()
        languages = frozenset(
            line.strip()
            for line in language_lines[1:]
            if line.strip()
        )
        return EngineInfo(version=version, languages=languages)

    def recognize(self, page: pymupdf.Page, language: str) -> OCRResult:
        try:
            png = page.get_pixmap(dpi=self.dpi, alpha=False).tobytes("png")
            result = subprocess.run(
                [
                    self.command,
                    "stdin",
                    "stdout",
                    "-l",
                    language,
                    "--psm",
                    str(self.page_segmentation_mode),
                    "tsv",
                ],
                input=png,
                check=False,
                capture_output=True,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            raise OCRProcessingError(
                f"Tesseract timed out after {self.timeout_seconds} seconds."
            ) from exc
        except OSError as exc:
            raise OCRProcessingError(
                f"Could not run Tesseract: {type(exc).__name__}: {exc}"
            ) from exc

        if result.returncode != 0:
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise OCRProcessingError(
                f"Tesseract exited with status {result.returncode}: {detail}"
            )
        output = result.stdout.decode("utf-8", errors="replace")
        return _parse_tsv(output)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _classification_decision(
    classification: str, reason: str
) -> tuple[bool, str]:
    if classification == "Genuine scanned/image-only page":
        return True, "Confirmed image-only page with no meaningful native text; OCR is required."
    if classification == "Extraction-quality problem":
        return True, f"Visually confirmed retrieval-relevant content is missing or materially incomplete: {reason}"
    if classification == "Blank or nearly blank page":
        return False, "Visually confirmed blank/nearly blank page; OCR would not recover meaningful body text."
    if classification == "Sparse text page":
        return False, "Sparse cover/separator content is not a useful OCR target."
    if classification == "Other / uncertain":
        return False, "Existing text is readable; the candidate flag is caused by formatting/low alphanumeric ratio."
    return False, f"Unrecognized audit classification {classification!r}; excluded pending manual review."


def build_target_inventory(
    audit_path: Path,
    processed_dir: Path = PROCESSED_DIR,
) -> list[dict[str, str]]:
    """Reconcile the OCR audit with current page records and deduplicate keys."""
    audit_path = Path(audit_path)
    processed_dir = Path(processed_dir)
    reconciled: dict[tuple[str, int], dict[str, str]] = {}
    records_by_document: dict[str, dict[int, dict[str, Any]]] = {}

    with audit_path.open(encoding="utf-8-sig", newline="") as audit_file:
        reader = csv.DictReader(audit_file)
        required = {
            "doc_id",
            "PDF page number",
            "classification",
            "reason for classification",
        }
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"OCR audit has missing columns: {audit_path}")

        for row in reader:
            doc_id = row["doc_id"].strip()
            page_number = int(row["PDF page number"])
            key = (doc_id, page_number)
            classification = row["classification"].strip()
            reason = row["reason for classification"].strip()
            include, decision = _classification_decision(
                classification, reason
            )
            overlaps = key in MATERIAL_EXTRACTION_GAPS

            output_path = processed_dir / f"{doc_id}.jsonl"
            if doc_id not in records_by_document:
                page_records = (
                    _read_jsonl(output_path) if output_path.is_file() else []
                )
                records_by_document[doc_id] = {
                    page["page_number"]: page for page in page_records
                }
            record = records_by_document[doc_id].get(page_number)
            prior_ocr = record.get("ocr", {}) if record else {}
            has_successful_ocr = record is not None and _has_ocr_result(record)
            language = LANGUAGE_OVERRIDES.get(key, OCR_LANGUAGE)
            already_processed = (
                record is not None
                and _valid_ocr_output(record)
                and prior_ocr.get("language") == language
            )
            if record is None:
                include = False
                decision = f"Excluded because page-level extraction record is missing: {output_path.name}."
            elif (
                include
                and not already_processed
                and not has_successful_ocr
                and not record.get("needs_ocr", False)
            ):
                include = False
                decision = "Excluded because current page record has sufficient native text."

            if include and already_processed:
                status = "already_processed"
            else:
                status = "pending" if include else "excluded"

            inventory_row = {
                "doc_id": doc_id,
                "PDF page number": str(page_number),
                "original OCR classification": classification,
                "reason for inclusion/exclusion": decision,
                "overlaps with previously reported extraction gap": (
                    "yes" if overlaps else "no"
                ),
                "OCR language required": language if include else "",
                "processing status": status,
            }
            if key in reconciled:
                if reconciled[key] != inventory_row:
                    raise ValueError(f"Conflicting duplicate OCR audit page: {key}")
                continue
            reconciled[key] = inventory_row

    return sorted(
        reconciled.values(),
        key=lambda row: (row["doc_id"], int(row["PDF page number"])),
    )


def _write_inventory(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=INVENTORY_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        temporary_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _write_errors(path: Path, errors: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as output_file:
            for error in errors:
                output_file.write(
                    json.dumps(error, ensure_ascii=False, separators=(",", ":"))
                    + "\n"
                )
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _valid_ocr_output(record: dict[str, Any]) -> bool:
    return _has_ocr_result(record) and "\t" not in record["ocr"]["text"]


def _has_ocr_result(record: dict[str, Any]) -> bool:
    return (
        record.get("is_ocr") is True
        and record.get("ocr", {}).get("status") == "success"
        and bool(record.get("ocr", {}).get("text", "").strip())
    )


def _apply_ocr_result(
    record: dict[str, Any],
    result: OCRResult,
    language: str,
    engine_version: str,
    dpi: int,
    page_segmentation_mode: int,
    force: bool = False,
    processing_time_seconds: float = 0.0,
) -> bool:
    """Apply OCR only as fallback and preserve the original native text."""
    ocr_metadata = {
        "status": "success" if result.text.strip() else "empty",
        "engine": "Tesseract",
        "engine_version": engine_version,
        "language": language,
        "text": result.text,
        "source_filename": record.get("source_filename"),
        "source_hash": record.get("source_hash"),
        "source_page_number": record.get("page_number"),
        "dpi": dpi,
        "page_segmentation_mode": page_segmentation_mode,
        "processing_time_seconds": round(processing_time_seconds, 3),
        "confidence_mean": result.confidence_mean,
        "confidence_min": result.confidence_min,
        "confidence_word_count": result.confidence_word_count,
    }
    if not result.text.strip():
        ocr_metadata["error"] = "Tesseract returned no recognized words."
        record["ocr"] = ocr_metadata
        return False

    native_text = record.get("native_text", record.get("text", ""))
    if (
        not record.get("needs_ocr", False)
        and not _has_ocr_result(record)
        and not force
    ):
        logger.info(
            "OCR result not applied to %s page %s because native text is sufficient",
            record.get("doc_id"),
            record.get("page_number"),
        )
        return False

    record["native_text"] = native_text
    record["text"] = _merge_native_and_ocr_text(native_text, result.text)
    record["ocr"] = ocr_metadata
    record["is_ocr"] = True
    quality_text = "\n".join(
        (record["text"], _table_text(record.get("tables", [])))
    )
    quality = _text_quality(quality_text)
    record["text_quality"] = quality
    record["needs_ocr"] = quality["needs_ocr"]
    record["ocr_reason"] = quality["reason"]
    return True


def _merge_native_and_ocr_text(native_text: str, ocr_text: str) -> str:
    """Keep useful native fragments while avoiding repeating recognized text."""
    native_text = native_text.strip()
    ocr_text = ocr_text.strip()
    if not native_text:
        return ocr_text
    if native_text.casefold() in ocr_text.casefold():
        return ocr_text
    if ocr_text.casefold() in native_text.casefold():
        return native_text
    return f"{native_text}\n{ocr_text}"


def _table_text(tables: list[dict[str, Any]]) -> str:
    return "\n".join(
        " | ".join(
            cell.replace("\n", " ").strip() if isinstance(cell, str) else ""
            for cell in row
        )
        for table in tables
        for row in table.get("rows", [])
        if any(cell for cell in row)
    )


def run_ocr_inventory(
    inventory_path: Path,
    pdf_dir: Path = PDF_DIR,
    processed_dir: Path = PROCESSED_DIR,
    backend: OCRBackend | None = None,
    force: bool = False,
    summary_path: Path | None = None,
    errors_path: Path | None = None,
) -> dict[str, Any]:
    """OCR only included inventory pages and update their existing JSONL records."""
    inventory_path = Path(inventory_path)
    pdf_dir = Path(pdf_dir)
    processed_dir = Path(processed_dir)
    summary_path = Path(summary_path or processed_dir / "ocr_processing_summary.json")
    errors_path = Path(errors_path or processed_dir / "ocr_errors.jsonl")
    backend = backend or TesseractBackend()

    with inventory_path.open(encoding="utf-8-sig", newline="") as inventory_file:
        reader = csv.DictReader(inventory_file)
        if not reader.fieldnames or not set(INVENTORY_FIELDS).issubset(reader.fieldnames):
            raise ValueError(f"OCR target inventory has missing columns: {inventory_path}")
        rows = list(reader)

    errors: list[dict[str, Any]] = []
    included = [row for row in rows if row["processing status"] != "excluded"]
    pending = [
        row for row in included
        if force or row["processing status"] != "already_processed"
    ]

    engine_info: EngineInfo | None = None
    if pending:
        try:
            engine_info = backend.inspect()
        except OCRPrerequisiteError as exc:
            language_results: dict[str, dict[str, int]] = defaultdict(
                lambda: {"succeeded": 0, "failed": 0, "blocked": 0, "skipped": 0}
            )
            for row in pending:
                row["processing status"] = "blocked_prerequisite"
                language_results[row["OCR language required"]]["blocked"] += 1
                errors.append(
                    {
                        "kind": "prerequisite_missing",
                        "doc_id": row["doc_id"],
                        "page_number": int(row["PDF page number"]),
                        "language": row["OCR language required"],
                        "message": str(exc),
                    }
                )
            logger.warning(
                "OCR prerequisite unavailable; %d selected pages blocked: %s",
                len(pending),
                exc,
            )
            _write_inventory(inventory_path, rows)
            _write_errors(errors_path, errors)
            summary = {
                "ocr_engine": "Tesseract CLI",
                "engine_version": None,
                "dpi": OCR_DPI,
                "selected_unique_pages": len(included),
                "pages_succeeded": 0,
                "pages_skipped": len(rows) - len(included)
                + sum(row["processing status"] == "already_processed" for row in rows),
                "pages_failed": 0,
                "pages_blocked": len(pending),
                "language_results": dict(language_results),
                "errors": errors,
            }
            _write_json(summary_path, summary)
            return summary

    pages_succeeded = 0
    run_started = time.monotonic()
    pages_skipped = len(rows) - len(included)
    pages_failed = 0
    pages_blocked = 0
    language_results: dict[str, dict[str, int]] = defaultdict(
        lambda: {"succeeded": 0, "failed": 0, "blocked": 0, "skipped": 0}
    )
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in included:
        status = row["processing status"]
        if status == "already_processed" and not force:
            pages_skipped += 1
            language_results[row["OCR language required"]]["skipped"] += 1
            continue
        language = row["OCR language required"]
        missing_languages = set(language.split("+")) - engine_info.languages
        if missing_languages:
            message = (
                "Missing Tesseract language data: "
                + ", ".join(sorted(missing_languages))
            )
            row["processing status"] = "blocked_missing_language_data"
            pages_blocked += 1
            language_results[language]["blocked"] += 1
            errors.append(
                {
                    "kind": "language_data_missing",
                    "doc_id": row["doc_id"],
                    "page_number": int(row["PDF page number"]),
                    "language": language,
                    "message": message,
                }
            )
            continue
        grouped[row["doc_id"]].append(row)

    for doc_id, target_rows in grouped.items():
        output_path = processed_dir / f"{doc_id}.jsonl"
        try:
            records = _read_jsonl(output_path)
            records_by_page = {record["page_number"]: record for record in records}
        except Exception as exc:
            message = f"Could not read page records: {type(exc).__name__}: {exc}"
            for row in target_rows:
                row["processing status"] = "failed"
                pages_failed += 1
                language_results[row["OCR language required"]]["failed"] += 1
                errors.append(
                    {
                        "kind": "page_records_unavailable",
                        "doc_id": doc_id,
                        "page_number": int(row["PDF page number"]),
                        "message": message,
                    }
                )
            continue

        source_records = [
            records_by_page.get(int(row["PDF page number"]))
            for row in target_rows
        ]
        source_names = {
            record.get("source_filename")
            for record in source_records
            if record and record.get("source_filename")
        }
        source_hashes = {
            record.get("source_hash")
            for record in source_records
            if record and record.get("source_hash")
        }
        pdf_path: Path | None = None
        source_error: dict[str, str] | None = None
        if len(source_names) == 1:
            source_name = next(iter(source_names))
            candidate = pdf_dir / source_name
            if candidate.is_file():
                pdf_path = candidate
            else:
                source_error = {
                    "kind": "source_pdf_missing",
                    "message": f"Recorded source PDF is missing: {source_name}",
                }
        elif not source_names:
            candidates = [
                path for path in pdf_dir.glob("*.pdf")
                if path.stem == doc_id or path.stem.startswith(f"{doc_id}_")
            ]
            if len(candidates) == 1:
                pdf_path = candidates[0]
            else:
                source_error = {
                    "kind": "source_pdf_missing",
                    "message": (
                        "No unique source PDF filename was available from page "
                        "metadata or document ID."
                    ),
                }
        else:
            source_error = {
                "kind": "source_pdf_ambiguous",
                "message": f"Target records reference multiple source PDFs: {sorted(source_names)}",
            }

        if pdf_path is not None and len(source_hashes) > 1:
            source_error = {
                "kind": "source_hash_ambiguous",
                "message": "Target page records contain inconsistent source hashes.",
            }
        elif pdf_path is not None and source_hashes:
            expected_hash = next(iter(source_hashes))
            try:
                actual_hash = _sha256(pdf_path)
            except OSError as exc:
                source_error = {
                    "kind": "source_hash_unavailable",
                    "message": f"Could not verify source PDF hash: {type(exc).__name__}: {exc}",
                }
            else:
                if actual_hash.lower() != expected_hash.lower():
                    source_error = {
                        "kind": "source_hash_mismatch",
                        "message": (
                            f"Source PDF SHA-256 mismatch for {pdf_path.name}: "
                            f"expected {expected_hash}, found {actual_hash}."
                        ),
                    }

        if pdf_path is None or source_error:
            error = source_error or {
                "kind": "source_pdf_missing",
                "message": "Could not resolve a source PDF from page metadata.",
            }
            for row in target_rows:
                row["processing status"] = "failed"
                pages_failed += 1
                language_results[row["OCR language required"]]["failed"] += 1
                errors.append(
                    {
                        **error,
                        "doc_id": doc_id,
                        "page_number": int(row["PDF page number"]),
                    }
                )
            continue
        try:
            document = pymupdf.open(pdf_path)
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            for row in target_rows:
                row["processing status"] = "failed"
                pages_failed += 1
                language_results[row["OCR language required"]]["failed"] += 1
                errors.append(
                    {
                        "kind": "document_open_failed",
                        "doc_id": doc_id,
                        "page_number": int(row["PDF page number"]),
                        "message": message,
                    }
                )
            continue

        changed = False
        try:
            for row in target_rows:
                page_number = int(row["PDF page number"])
                language = row["OCR language required"]
                record = records_by_page.get(page_number)
                if record is None or page_number > document.page_count:
                    row["processing status"] = "failed"
                    pages_failed += 1
                    language_results[language]["failed"] += 1
                    errors.append(
                        {
                            "kind": "page_record_missing",
                            "doc_id": doc_id,
                            "page_number": page_number,
                            "message": "PDF page or page-level JSONL record is missing.",
                        }
                    )
                    continue
                if (
                    _valid_ocr_output(record)
                    and record.get("ocr", {}).get("language") == language
                    and not force
                ):
                    row["processing status"] = "already_processed"
                    pages_skipped += 1
                    language_results[language]["skipped"] += 1
                    continue
                if (
                    not record.get("needs_ocr", False)
                    and not _has_ocr_result(record)
                    and not force
                ):
                    row["processing status"] = "skipped_native_text_sufficient"
                    pages_skipped += 1
                    language_results[language]["skipped"] += 1
                    continue

                try:
                    page_started = time.monotonic()
                    page = document.load_page(page_number - 1)
                    result = backend.recognize(page, language)
                    processing_time_seconds = time.monotonic() - page_started
                    applied = _apply_ocr_result(
                        record,
                        result,
                        language,
                        engine_info.version,
                        getattr(backend, "dpi", OCR_DPI),
                        getattr(backend, "page_segmentation_mode", OCR_PAGE_SEGMENTATION_MODE),
                        force=(
                            force
                            or (
                                _has_ocr_result(record)
                                and (
                                    record.get("ocr", {}).get("language")
                                    != language
                                    or "\t" in record.get("ocr", {}).get("text", "")
                                )
                            )
                        ),
                        processing_time_seconds=processing_time_seconds,
                    )
                    if applied:
                        row["processing status"] = "processed"
                        pages_succeeded += 1
                        language_results[language]["succeeded"] += 1
                        changed = True
                    else:
                        status = record.get("ocr", {}).get("status")
                        if status == "success":
                            row["processing status"] = "skipped_native_text_sufficient"
                            pages_skipped += 1
                            language_results[language]["skipped"] += 1
                        else:
                            row["processing status"] = "failed_empty_result"
                            pages_failed += 1
                            language_results[language]["failed"] += 1
                            errors.append(
                                {
                                    "kind": "empty_ocr_result",
                                    "doc_id": doc_id,
                                    "page_number": page_number,
                                    "language": language,
                                    "message": record.get("ocr", {}).get("error"),
                                }
                            )
                        changed = True
                except Exception as exc:
                    message = f"{type(exc).__name__}: {exc}"
                    record["ocr"] = {
                        "status": "failed",
                        "engine": "Tesseract",
                        "engine_version": engine_info.version,
                        "language": language,
                        "source_filename": record.get("source_filename"),
                        "source_hash": record.get("source_hash"),
                        "source_page_number": page_number,
                        "dpi": getattr(backend, "dpi", OCR_DPI),
                        "processing_time_seconds": round(
                            time.monotonic() - page_started, 3
                        ),
                        "error": message,
                    }
                    row["processing status"] = "failed"
                    pages_failed += 1
                    language_results[language]["failed"] += 1
                    errors.append(
                        {
                            "kind": "page_ocr_failed",
                            "doc_id": doc_id,
                            "page_number": page_number,
                            "language": language,
                            "processing_time_seconds": round(
                                time.monotonic() - page_started, 3
                            ),
                            "message": message,
                        }
                    )
                    changed = True
                    logger.exception("OCR failed for %s page %d", doc_id, page_number)
        finally:
            document.close()
        if changed:
            _write_jsonl(output_path, records)

    _write_inventory(inventory_path, rows)
    _write_errors(errors_path, errors)
    summary = {
        "ocr_engine": "Tesseract CLI",
        "engine_version": engine_info.version if engine_info else None,
        "dpi": OCR_DPI,
        "selected_unique_pages": len(included),
        "pages_succeeded": pages_succeeded,
        "pages_skipped": pages_skipped,
        "pages_failed": pages_failed,
        "pages_blocked": pages_blocked,
        "processing_time_seconds": round(time.monotonic() - run_started, 3),
        "language_results": dict(language_results),
        "errors": errors,
    }
    _write_json(summary_path, summary)
    return summary


def _configure_logging() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "ocr.log", encoding="utf-8"),
        ],
        force=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run OCR on audited pages that lack sufficient native text."
    )
    parser.add_argument(
        "--audit",
        type=Path,
        default=REPORTS_DIR / "ocr_candidate_audit.csv",
        help="Audited OCR-candidate CSV.",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=OCR_TARGET_INVENTORY_PATH,
        help="Target inventory CSV path.",
    )
    parser.add_argument("--pdf-dir", type=Path, default=PDF_DIR)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--force", action="store_true", help="Re-OCR successful pages.")
    args = parser.parse_args(argv)
    _configure_logging()

    try:
        inventory = build_target_inventory(args.audit, args.processed_dir)
        _write_inventory(args.inventory, inventory)
        summary = run_ocr_inventory(
            args.inventory, args.pdf_dir, args.processed_dir, force=args.force
        )
    except (OSError, ValueError, csv.Error) as exc:
        logger.exception("OCR could not start: %s", exc)
        return 1
    print(json.dumps({key: value for key, value in summary.items() if key != "errors"}, indent=2))
    if summary["pages_failed"]:
        return 1
    if summary["pages_blocked"]:
        return 2
    return 0


MATERIAL_EXTRACTION_GAPS = {
    ("doc_007", 66),
    ("doc_029", 17),
    ("doc_009", 48),
    ("doc_009", 49),
    ("doc_036", 4),
}


if __name__ == "__main__":
    raise SystemExit(main())

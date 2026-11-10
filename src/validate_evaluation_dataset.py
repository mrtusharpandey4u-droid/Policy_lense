"""Read-only validation for the hand-curated retrieval evaluation dataset."""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pymupdf
from qdrant_client import QdrantClient

from src.config import (
    MANIFEST_PATH,
    QDRANT_FIXED_COLLECTION_NAME,
    QDRANT_STORAGE_DIR,
    QDRANT_STRUCTURE_COLLECTION_NAME,
    PROJECT_ROOT,
)

DEFAULT_DATASET = PROJECT_ROOT / "data/evaluation/evaluation_questions.jsonl"
CHUNK_FILES = {
    "fixed_size": PROJECT_ROOT / "data/processed/chunks/fixed_size.jsonl",
    "structure_aware": PROJECT_ROOT / "data/processed/chunks/structure_aware.jsonl",
}
COLLECTIONS = {
    "fixed_size": QDRANT_FIXED_COLLECTION_NAME,
    "structure_aware": QDRANT_STRUCTURE_COLLECTION_NAME,
}
EXPECTED_COUNTS = {"fixed_size": 1370, "structure_aware": 1478}
EXPECTED_TYPES = {"standard": 15, "table_value": 5, "paraphrased": 5}
DATASET_SIZE = 25
_NON_WORD = re.compile(r"[^\w]+", re.UNICODE)


class DatasetValidationError(RuntimeError):
    """Raised when an evaluation dataset integrity check fails."""


def _normalized(text: str) -> str:
    normalized_characters = []
    for character in unicodedata.normalize("NFKC", text).casefold():
        if character.isspace():
            normalized_characters.append(" ")
        elif not unicodedata.category(character).startswith("C"):
            normalized_characters.append(character)
    normalized = "".join(normalized_characters)
    return " ".join(_NON_WORD.sub(" ", normalized).split())


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise DatasetValidationError(f"Cannot read {path}: {exc}") from exc
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DatasetValidationError(
                f"Invalid JSON at {path}:{line_number}: {exc}"
            ) from exc
        if not isinstance(record, dict):
            raise DatasetValidationError(
                f"Expected an object at {path}:{line_number}."
            )
        records.append(record)
    return records


def _manifest(path: Path) -> dict[str, dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
    except OSError as exc:
        raise DatasetValidationError(f"Cannot read manifest {path}: {exc}") from exc
    return {
        row["doc_id"]: row
        for row in rows
        if row.get("doc_id") and row.get("download_status") == "verified"
    }


def _table_text(page_record: dict[str, Any]) -> str:
    rows = []
    for table in page_record.get("tables", []):
        for row in table.get("rows", []):
            rows.append(" | ".join(str(cell or "") for cell in row))
    return "\n".join(rows)


def _pdf_table_text(page: pymupdf.Page) -> str:
    rows = []
    for table in page.find_tables().tables:
        for row in table.extract() or []:
            rows.append(" | ".join(str(cell or "") for cell in row))
    return "\n".join(rows)


def _chunk_pages(chunk: dict[str, Any]) -> set[int]:
    provenance = chunk.get("page_provenance")
    if isinstance(provenance, list):
        pages = {
            entry.get("page_number")
            for entry in provenance
            if isinstance(entry, dict)
            and isinstance(entry.get("page_number"), int)
        }
        if pages:
            return pages
    start, end = chunk.get("page_start"), chunk.get("page_end")
    if isinstance(start, int) and isinstance(end, int) and start <= end:
        return set(range(start, end + 1))
    return set()


def _load_indexed_chunks(
    client: QdrantClient, strategy: str
) -> tuple[dict[str, list[dict[str, Any]]], int]:
    collection_name = COLLECTIONS[strategy]
    count = client.count(collection_name=collection_name, exact=True).count
    if count != EXPECTED_COUNTS[strategy]:
        raise DatasetValidationError(
            f"{collection_name} contains {count} points; expected "
            f"{EXPECTED_COUNTS[strategy]}."
        )
    chunks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    offset: Any = None
    seen_ids: set[str] = set()
    while True:
        points, offset = client.scroll(
            collection_name=collection_name,
            limit=128,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for point in points:
            payload = point.payload
            if not isinstance(payload, dict):
                raise DatasetValidationError(
                    f"Missing payload in {collection_name} point {point.id}."
                )
            chunk_id = payload.get("chunk_id")
            doc_id = payload.get("doc_id")
            if not isinstance(chunk_id, str) or not isinstance(doc_id, str):
                raise DatasetValidationError(
                    f"Missing chunk/document ID in {collection_name} point {point.id}."
                )
            if str(point.id) in seen_ids:
                raise DatasetValidationError(
                    f"Duplicate point ID {point.id} in {collection_name}."
                )
            seen_ids.add(str(point.id))
            chunks[doc_id].append(
                {
                    "chunk_id": chunk_id,
                    "page_numbers": _chunk_pages(payload),
                    "content_type": payload.get("content_type"),
                    "tables": payload.get("tables", []),
                }
            )
        if offset is None:
            break
    if len(seen_ids) != count:
        raise DatasetValidationError(
            f"Scroll found {len(seen_ids)} points in {collection_name}, "
            f"but count reports {count}."
        )
    return chunks, count


def validate_dataset(
    dataset_path: Path = DEFAULT_DATASET,
    manifest_path: Path = MANIFEST_PATH,
    pdf_dir: Path = PROJECT_ROOT / "data/pdfs",
    cleaned_dir: Path = PROJECT_ROOT / "data/processed/cleaned",
    chunk_files: dict[str, Path] | None = None,
    storage_dir: Path = QDRANT_STORAGE_DIR,
) -> dict[str, Any]:
    """Validate sources, pages, table evidence, and indexed-chunk coverage."""
    manifest = _manifest(Path(manifest_path))
    records = _read_jsonl(Path(dataset_path))
    errors: list[str] = []
    warnings: list[str] = []
    expected_ids = [f"Q{number:03d}" for number in range(1, DATASET_SIZE + 1)]
    actual_ids = [record.get("question_id") for record in records]
    if len(records) != DATASET_SIZE:
        errors.append(f"Expected {DATASET_SIZE} questions, found {len(records)}.")
    if actual_ids != expected_ids:
        errors.append("Question IDs must be unique and sequential from Q001 to Q025.")

    type_counts = Counter(record.get("question_type") for record in records)
    if dict(type_counts) != EXPECTED_TYPES:
        errors.append(
            f"Question type counts are {dict(type_counts)}, expected {EXPECTED_TYPES}."
        )
    normalized_questions = [_normalized(record.get("question", "")) for record in records]
    for index, question in enumerate(normalized_questions):
        if not question:
            errors.append(f"{expected_ids[index]} has an empty question.")
        for prior in range(index):
            similarity = difflib.SequenceMatcher(
                None, question, normalized_questions[prior]
            ).ratio()
            if similarity >= 0.82:
                errors.append(
                    f"{expected_ids[prior]} and {expected_ids[index]} are near-duplicates "
                    f"(similarity {similarity:.2f})."
                )

    page_cache: dict[str, dict[int, dict[str, Any]]] = {}
    pdf_cache: dict[str, pymupdf.Document] = {}
    report_by_question: dict[str, dict[str, Any]] = {}
    verified_pages = 0
    table_questions_verified = 0
    table_payload_questions = {strategy: set() for strategy in EXPECTED_COUNTS}
    paraphrase_checks: list[float] = []
    source_hashes_checked: set[str] = set()
    prepared_chunk_files = chunk_files or CHUNK_FILES
    source_chunks: dict[str, dict[str, list[dict[str, Any]]]] = {}
    source_chunk_ids: dict[str, set[str]] = {}

    for strategy, path in prepared_chunk_files.items():
        records_for_strategy = _read_jsonl(Path(path))
        ids = [chunk.get("chunk_id") for chunk in records_for_strategy]
        if len(ids) != len(set(ids)):
            errors.append(f"Duplicate chunk IDs in {strategy} source chunk file.")
        if len(records_for_strategy) != EXPECTED_COUNTS.get(strategy):
            errors.append(
                f"{strategy} source chunk file has {len(records_for_strategy)} "
                f"records; expected {EXPECTED_COUNTS.get(strategy)}."
            )
        source_chunk_ids[strategy] = {str(chunk_id) for chunk_id in ids}
        source_chunks[strategy] = defaultdict(list)
        for chunk in records_for_strategy:
            source_chunks[strategy][str(chunk.get("doc_id"))].append(
                {
                    "chunk_id": chunk.get("chunk_id"),
                    "page_numbers": _chunk_pages(chunk),
                    "content_type": chunk.get("content_type"),
                    "tables": chunk.get("tables", []),
                }
            )

    client: QdrantClient | None = None
    indexed_chunks: dict[str, dict[str, list[dict[str, Any]]]] = {}
    qdrant_counts: dict[str, int] = {}
    try:
        client = QdrantClient(path=str(storage_dir))
        for strategy in EXPECTED_COUNTS:
            indexed_chunks[strategy], qdrant_counts[strategy] = _load_indexed_chunks(
                client, strategy
            )
            indexed_chunk_ids = {
                chunk["chunk_id"]
                for doc_chunks in indexed_chunks[strategy].values()
                for chunk in doc_chunks
            }
            if indexed_chunk_ids != source_chunk_ids[strategy]:
                missing = len(source_chunk_ids[strategy] - indexed_chunk_ids)
                extra = len(indexed_chunk_ids - source_chunk_ids[strategy])
                errors.append(
                    f"{strategy} Qdrant payload IDs differ from source chunks: "
                    f"{missing} missing, {extra} extra."
                )

        for record in records:
            question_id = record.get("question_id", "<missing ID>")
            question = record.get("question")
            question_type = record.get("question_type")
            if not isinstance(question, str) or not question.strip():
                errors.append(f"{question_id} has no question text.")
            if question_type not in EXPECTED_TYPES:
                errors.append(f"{question_id} has unsupported question_type.")
            if not isinstance(record.get("expected_information"), str) or not record[
                "expected_information"
            ].strip():
                errors.append(f"{question_id} has no expected_information.")
            if record.get("difficulty") not in {"easy", "medium", "hard"}:
                errors.append(f"{question_id} has invalid difficulty.")
            references = record.get("gold_references")
            if not isinstance(references, list) or not references:
                errors.append(f"{question_id} has no gold reference.")
                continue
            question_status = {
                "references": len(references),
                "mapped_references": {"fixed_size": 0, "structure_aware": 0},
                "table_chunks": {"fixed_size": 0, "structure_aware": 0},
            }
            for reference_number, reference in enumerate(references, 1):
                ref_label = f"{question_id} reference {reference_number}"
                required = (
                    "doc_id",
                    "title",
                    "issuer",
                    "gold_pages",
                    "section_title",
                    "evidence_snippet",
                    "reference_notes",
                )
                missing = [field for field in required if field not in reference]
                if missing:
                    errors.append(f"{ref_label} is missing {', '.join(missing)}.")
                    continue
                doc_id = reference["doc_id"]
                row = manifest.get(doc_id)
                if row is None:
                    errors.append(f"{ref_label} uses unknown/unverified doc_id {doc_id}.")
                    continue
                if reference["title"] != row["title"] or reference["issuer"] != row["issuer"]:
                    errors.append(f"{ref_label} title/issuer differs from the manifest.")
                try:
                    page_count = int(row["page_count"])
                except (TypeError, ValueError):
                    errors.append(f"{ref_label} manifest page count is invalid.")
                    continue

                gold_pages = reference.get("gold_pages")
                pdf_indices = reference.get("pdf_page_indices")
                if (
                    not isinstance(gold_pages, list)
                    or not gold_pages
                    or any(not isinstance(page, int) for page in gold_pages)
                ):
                    errors.append(f"{ref_label} has invalid gold_pages.")
                    continue
                if not isinstance(pdf_indices, list) or pdf_indices != [
                    page - 1 for page in gold_pages
                ]:
                    errors.append(
                        f"{ref_label} pdf_page_indices must be the corresponding "
                        "zero-based PDF indices."
                    )
                if len(set(gold_pages)) != len(gold_pages):
                    errors.append(f"{ref_label} contains duplicate gold pages.")
                printed_pages = reference.get("printed_page_numbers", [])
                if (
                    not isinstance(printed_pages, list)
                    or any(
                        not isinstance(page, int) or page < 1
                        for page in printed_pages
                    )
                ):
                    errors.append(f"{ref_label} has invalid printed_page_numbers.")

                if doc_id not in page_cache:
                    cleaned_path = Path(cleaned_dir) / f"{doc_id}.jsonl"
                    cleaned_records = _read_jsonl(cleaned_path)
                    page_cache[doc_id] = {
                        item["page_number"]: item for item in cleaned_records
                    }
                    first = cleaned_records[0] if cleaned_records else {}
                    filename = first.get("source_filename")
                    if not isinstance(filename, str) or not filename:
                        errors.append(f"{doc_id} has no source filename in cleaned data.")
                        continue
                    pdf_path = Path(pdf_dir) / filename
                    if not pdf_path.is_file():
                        errors.append(f"Source PDF is missing: {pdf_path}.")
                        continue
                    pdf_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
                    if pdf_hash != row.get("source_hash"):
                        errors.append(f"Source PDF hash differs from manifest for {doc_id}.")
                    source_hashes_checked.add(doc_id)
                    try:
                        pdf_cache[doc_id] = pymupdf.open(pdf_path)
                    except (OSError, RuntimeError) as exc:
                        errors.append(f"Cannot open source PDF for {doc_id}: {exc}")
                        continue
                    if len(pdf_cache[doc_id]) != page_count:
                        errors.append(
                            f"{doc_id} PDF has {len(pdf_cache[doc_id])} pages; "
                            f"manifest says {page_count}."
                        )

                pdf = pdf_cache.get(doc_id)
                if pdf is None:
                    continue
                page_matches = {"fixed_size": [], "structure_aware": []}
                for page_offset, page_number in enumerate(gold_pages):
                    if page_number < 1 or page_number > page_count or page_number > len(pdf):
                        errors.append(
                            f"{ref_label} page {page_number} is outside 1..{page_count}."
                        )
                        continue
                    page_record = page_cache[doc_id].get(page_number)
                    if page_record is None:
                        errors.append(
                            f"{ref_label} has no cleaned page record for page {page_number}."
                        )
                        continue
                    source_page = pdf[page_number - 1]
                    source_text = source_page.get_text("text")
                    if page_offset < len(printed_pages) and str(
                        printed_pages[page_offset]
                    ) not in source_text:
                        errors.append(
                            f"{ref_label} printed page {printed_pages[page_offset]} "
                            f"is not visible on PDF page {page_number}."
                        )
                    snippet = reference.get("evidence_snippet")
                    normalized_snippet = _normalized(snippet)
                    is_table_question = record.get("question_type") == "table_value"
                    if is_table_question:
                        original_table_text = _pdf_table_text(source_page)
                        if (
                            not normalized_snippet
                            or normalized_snippet
                            not in _normalized(original_table_text)
                        ):
                            errors.append(
                                f"{ref_label} evidence snippet is not found in "
                                f"PyMuPDF-extracted tables on original PDF page "
                                f"{page_number}."
                            )
                    elif not normalized_snippet or normalized_snippet not in _normalized(
                        source_text
                    ):
                        errors.append(
                            f"{ref_label} evidence snippet is not found on original "
                            f"PDF page {page_number}."
                        )
                    section = reference.get("section_title")
                    nearby_text = source_text + " " + " ".join(
                        heading.get("text", "")
                        for heading in page_record.get("headings", [])
                        if isinstance(heading, dict)
                    )
                    for adjacent_index in (page_number - 2, page_number):
                        if 0 <= adjacent_index < len(pdf):
                            nearby_text += " " + pdf[adjacent_index].get_text("text")
                    if section and _normalized(section) not in _normalized(nearby_text):
                        warnings.append(
                            f"{ref_label} section title is not a literal page heading "
                            f"on or adjacent to PDF page {page_number}; verify it is "
                            "a concise table/section label."
                        )
                    if is_table_question:
                        table_text = _normalized(_table_text(page_record))
                        if not page_record.get("tables"):
                            errors.append(
                                f"{ref_label} is table_value but no structured table "
                                f"exists on PDF page {page_number}."
                            )
                        if not _pdf_table_text(source_page):
                            errors.append(
                                f"{ref_label} is table_value but PyMuPDF found no "
                                f"table on original PDF page {page_number}."
                            )
                        if not normalized_snippet or normalized_snippet not in table_text:
                            errors.append(
                                f"{ref_label} table evidence is not present in the "
                                f"structured table rows for page {page_number}."
                            )
                        table_questions_verified += 1
                    verified_pages += 1
                    for strategy in EXPECTED_COUNTS:
                        matches = [
                            chunk
                            for chunk in indexed_chunks[strategy].get(doc_id, [])
                            if page_number in chunk["page_numbers"]
                        ]
                        if not matches:
                            errors.append(
                                f"{ref_label} page {page_number} has no indexed "
                                f"{strategy} chunk."
                            )
                            page_matches[strategy].append(False)
                        else:
                            page_matches[strategy].append(True)
                        table_chunk_matches = [
                            chunk
                            for chunk in matches
                            if chunk.get("content_type") == "table"
                            or chunk.get("tables")
                        ]
                        question_status["table_chunks"][strategy] += len(
                            table_chunk_matches
                        )
                        if question_type == "table_value":
                            if not table_chunk_matches:
                                errors.append(
                                    f"{ref_label} page {page_number} has no "
                                    f"table-bearing {strategy} chunk."
                                )
                            else:
                                chunk_table_text = _normalized(
                                    _table_text(
                                        {
                                            "tables": [
                                                table
                                                for chunk in table_chunk_matches
                                                for table in chunk.get("tables", [])
                                            ]
                                        }
                                    )
                                )
                                if normalized_snippet not in chunk_table_text:
                                    errors.append(
                                        f"{ref_label} evidence is missing from "
                                        f"{strategy} indexed table payloads on "
                                        f"page {page_number}."
                                    )
                                else:
                                    table_payload_questions[strategy].add(
                                        question_id
                                    )
                for strategy, page_coverage in page_matches.items():
                    if page_coverage and all(page_coverage):
                        question_status["mapped_references"][strategy] += 1
            if question_type == "paraphrased":
                for reference in references:
                    evidence = _normalized(reference.get("evidence_snippet", ""))
                    normalized_question = _normalized(question or "")
                    paraphrase_checks.append(
                        difflib.SequenceMatcher(
                            None, normalized_question, evidence
                        ).ratio()
                    )
            report_by_question[question_id] = question_status
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(f"Could not validate persisted Qdrant collections: {exc}")
    finally:
        if client is not None:
            client.close()
        for pdf in pdf_cache.values():
            pdf.close()

    matching_questions = {
        strategy: sum(
            status["mapped_references"][strategy] == status["references"]
            for status in report_by_question.values()
        )
        for strategy in EXPECTED_COUNTS
    }
    table_fragmentation: list[dict[str, Any]] = []
    for record in records:
        if record.get("question_type") != "table_value":
            continue
        question_id = record.get("question_id")
        status = report_by_question.get(question_id, {})
        fragmented = False
        fragment_details = []
        for strategy in EXPECTED_COUNTS:
            for reference in record.get("gold_references", []):
                doc_id = reference.get("doc_id")
                for page_number in reference.get("gold_pages", []):
                    matches = [
                        chunk
                        for chunk in indexed_chunks.get(strategy, {}).get(doc_id, [])
                        if page_number in chunk["page_numbers"]
                        and (
                            chunk.get("content_type") == "table"
                            or chunk.get("tables")
                        )
                    ]
                    for chunk in matches:
                        for table in chunk.get("tables", []):
                            if isinstance(table, dict) and table.get("part_count", 1) > 1:
                                fragmented = True
                                fragment_details.append(
                                    {
                                        "strategy": strategy,
                                        "chunk_id": chunk["chunk_id"],
                                        "part_index": table.get("part_index"),
                                        "part_count": table.get("part_count"),
                                    }
                                )
        if fragmented:
            table_fragmentation.append(
                {"question_id": question_id, "fragments": fragment_details}
            )

    result = {
        "status": "failed" if errors else "passed",
        "question_count": len(records),
        "question_type_counts": dict(type_counts),
        "unique_verified_gold_documents": len(
            {
                reference.get("doc_id")
                for record in records
                for reference in record.get("gold_references", [])
            }
        ),
        "verified_gold_page_references": verified_pages,
        "source_pdf_hashes_checked": len(source_hashes_checked),
        "table_value_questions_with_verified_table_evidence": sum(
            record.get("question_type") == "table_value"
            and bool(report_by_question.get(record.get("question_id")))
            for record in records
        ),
        "table_value_questions_with_indexed_table_evidence": {
            strategy: len(question_ids)
            for strategy, question_ids in table_payload_questions.items()
        },
        "question_coverage_with_indexed_chunks": matching_questions,
        "qdrant_collection_counts": qdrant_counts,
        "table_references_with_split_table_fragments": table_fragmentation,
        "maximum_paraphrase_question_to_source_similarity": max(
            paraphrase_checks, default=0.0
        ),
        "warnings": warnings,
        "errors": errors,
    }
    if errors:
        raise DatasetValidationError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate PolicyLens evaluation questions against source PDFs and indexes."
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args(argv)
    try:
        result = validate_dataset(args.dataset)
    except DatasetValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

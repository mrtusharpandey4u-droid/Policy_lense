import csv
import hashlib
import json
from pathlib import Path

import pymupdf
import pytest

from src.ocr import (
    EngineInfo,
    OCRProcessingError,
    OCRPrerequisiteError,
    OCRResult,
    _apply_ocr_result,
    _parse_tsv,
    build_target_inventory,
    run_ocr_inventory,
)


def _write_pdf(path: Path, page_count: int = 1) -> None:
    document = pymupdf.open()
    for _ in range(page_count):
        document.new_page()
    document.save(path)
    document.close()


def _write_page_records(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )


def _set_pdf_provenance(record: dict, pdf_path: Path) -> None:
    record["source_filename"] = pdf_path.name
    record["source_hash"] = hashlib.sha256(pdf_path.read_bytes()).hexdigest()


def _record(page_number: int, text: str = "", needs_ocr: bool = True) -> dict:
    return {
        "doc_id": "doc_test",
        "document_title": "Test Policy",
        "source_filename": "doc_test.pdf",
        "source_hash": "abc123",
        "page_number": page_number,
        "text": text,
        "blocks": [],
        "headings": [],
        "tables": [],
        "needs_ocr": needs_ocr,
        "ocr_reason": "no_extractable_text" if needs_ocr else None,
        "is_ocr": False,
        "has_table": False,
        "layout_columns": 1,
        "layout": {"column_count": 1},
        "text_quality": {},
        "page_error": None,
        "table_errors": [],
    }


def _write_inventory(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "doc_id",
        "PDF page number",
        "original OCR classification",
        "reason for inclusion/exclusion",
        "overlaps with previously reported extraction gap",
        "OCR language required",
        "processing status",
    ]
    with path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _target_row(
    page_number: int, language: str = "eng", doc_id: str = "doc_test"
) -> dict[str, str]:
    return {
        "doc_id": doc_id,
        "PDF page number": str(page_number),
        "original OCR classification": "Genuine scanned/image-only page",
        "reason for inclusion/exclusion": "Image-only page.",
        "overlaps with previously reported extraction gap": "no",
        "OCR language required": language,
        "processing status": "pending",
    }


class FakeBackend:
    dpi = 300
    page_segmentation_mode = 3

    def __init__(self, results: dict[int, OCRResult] | None = None) -> None:
        self.results = results or {}
        self.calls: list[tuple[int, str]] = []
        self.inspect_calls = 0

    def inspect(self) -> EngineInfo:
        self.inspect_calls += 1
        return EngineInfo("Tesseract test", frozenset({"eng", "hin"}))

    def recognize(self, page: pymupdf.Page, language: str) -> OCRResult:
        page_number = page.number + 1
        self.calls.append((page_number, language))
        return self.results[page_number]


def test_target_inventory_selects_scans_and_material_gaps(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    processed.mkdir()
    _write_page_records(
        processed / "doc_009.jsonl",
        [_record(48), _record(49)],
    )
    audit = tmp_path / "audit.csv"
    rows = [
        {
            "doc_id": "doc_009",
            "PDF page number": "48",
            "extracted character count": "0",
            "alphanumeric ratio": "0",
            "classification": "Extraction-quality problem",
            "reason for classification": "Vector directory text is missing.",
            "recommended action": "OCR",
        },
        {
            "doc_id": "doc_009",
            "PDF page number": "49",
            "extracted character count": "0",
            "alphanumeric ratio": "0",
            "classification": "Extraction-quality problem",
            "reason for classification": "Hindi vector directory text is missing.",
            "recommended action": "OCR",
        },
        {
            "doc_id": "doc_009",
            "PDF page number": "50",
            "extracted character count": "2",
            "alphanumeric ratio": "0",
            "classification": "Blank or nearly blank page",
            "reason for classification": "Blank page.",
            "recommended action": "Do not OCR",
        },
    ]
    with audit.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    inventory = build_target_inventory(audit, processed)

    assert len(inventory) == 3
    by_page = {int(row["PDF page number"]): row for row in inventory}
    assert by_page[48]["processing status"] == "pending"
    assert by_page[49]["OCR language required"] == "eng+hin"
    assert by_page[50]["processing status"] == "excluded"


def test_inventory_deduplicates_audit_page(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    processed.mkdir()
    _write_page_records(processed / "doc_test.jsonl", [_record(1)])
    audit = tmp_path / "audit.csv"
    row = {
        "doc_id": "doc_test",
        "PDF page number": "1",
        "extracted character count": "0",
        "alphanumeric ratio": "0",
        "classification": "Genuine scanned/image-only page",
        "reason for classification": "Scanned image.",
        "recommended action": "OCR",
    }
    with audit.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=row.keys())
        writer.writeheader()
        writer.writerows([row, row])

    inventory = build_target_inventory(audit, processed)

    assert len(inventory) == 1


def test_tsv_parser_returns_text_and_confidence() -> None:
    tsv = (
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop"
        "\twidth\theight\tconf\ttext\n"
        "5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t92.5\tLoan\n"
        "5\t1\t1\t1\t1\t2\t11\t0\t20\t10\t88.5\tpolicy\n"
    )

    result = _parse_tsv(tsv)

    assert result.text == "Loan policy"
    assert result.confidence_mean == 90.5
    assert result.confidence_min == 88.5
    assert result.confidence_word_count == 2


def test_tsv_parser_reports_malformed_output() -> None:
    with pytest.raises(OCRProcessingError, match="malformed TSV"):
        _parse_tsv("not a TSV response")


def test_tsv_parser_keeps_quoted_ocr_words_without_merging_rows() -> None:
    tsv = (
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop"
        "\twidth\theight\tconf\ttext\n"
        '5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t92.5\t"Includes\n'
        '5\t1\t1\t1\t2\t1\t0\t12\t10\t10\t88.5\t"Report\n'
    )

    result = _parse_tsv(tsv)

    assert result.text == '"Includes\n"Report'
    assert result.confidence_word_count == 2


def test_ocr_preserves_native_text_and_metadata_without_replacing_tables() -> None:
    page = _record(1, text="Annual Report 2024", needs_ocr=True)
    page["tables"] = [{"rows": [["Policy", "Value"]]}]

    applied = _apply_ocr_result(
        page,
        OCRResult("Loan policy eligibility", 89.2, 70.0, 3),
        "eng",
        "Tesseract test",
        300,
        3,
    )

    assert applied
    assert page["native_text"] == "Annual Report 2024"
    assert page["text"] == "Annual Report 2024\nLoan policy eligibility"
    assert page["ocr"]["text"] == "Loan policy eligibility"
    assert page["ocr"]["confidence_mean"] == 89.2
    assert page["source_hash"] == "abc123"
    assert page["page_number"] == 1
    assert page["tables"] == [{"rows": [["Policy", "Value"]]}]
    assert page["is_ocr"] is True


def test_sufficient_native_text_is_not_overwritten() -> None:
    page = _record(1, text="This is reliable native text.", needs_ocr=False)

    applied = _apply_ocr_result(
        page,
        OCRResult("wrong OCR", 10.0, 10.0, 1),
        "eng",
        "Tesseract test",
        300,
        3,
    )

    assert not applied
    assert page["text"] == "This is reliable native text."
    assert "native_text" not in page
    assert page["is_ocr"] is False


def test_run_ocr_uses_language_and_is_idempotent(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "notice.pdf"
    _write_pdf(pdf_path)
    record = _record(1)
    _set_pdf_provenance(record, pdf_path)
    _write_page_records(processed / "doc_test.jsonl", [record])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1, "eng+hin")])
    backend = FakeBackend(
        {1: OCRResult("ऋण नीति", 91.0, 80.0, 2)}
    )

    first = run_ocr_inventory(
        inventory, pdf_dir, processed, backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )
    second = run_ocr_inventory(
        inventory, pdf_dir, processed, backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert first["pages_succeeded"] == 1
    assert second["pages_succeeded"] == 0
    assert second["pages_skipped"] == 1
    assert backend.calls == [(1, "eng+hin")]
    output = json.loads((processed / "doc_test.jsonl").read_text().splitlines()[0])
    assert output["text"] == "ऋण नीति"
    assert output["ocr"]["language"] == "eng+hin"
    assert output["ocr"]["source_filename"] == "notice.pdf"
    assert output["ocr"]["source_hash"] == record["source_hash"]
    assert output["ocr"]["source_page_number"] == 1
    assert output["ocr"]["processing_time_seconds"] >= 0


def test_source_pdf_is_resolved_and_hash_checked_using_page_provenance(
    tmp_path: Path,
) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "gazette_notice.pdf"
    _write_pdf(pdf_path)
    page = _record(1)
    _set_pdf_provenance(page, pdf_path)
    _write_page_records(processed / "doc_004.jsonl", [page])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1, doc_id="doc_004")])
    backend = FakeBackend({1: OCRResult("Gazette notice text", 92.0, 85.0, 3)})

    summary = run_ocr_inventory(
        inventory,
        pdf_dir,
        processed,
        backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_succeeded"] == 1
    assert summary["pages_failed"] == 0
    output = json.loads((processed / "doc_004.jsonl").read_text().splitlines()[0])
    assert output["ocr"]["source_filename"] == pdf_path.name
    assert output["ocr"]["source_hash"] == page["source_hash"]


def test_source_hash_mismatch_prevents_ocr(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "doc_test.pdf"
    _write_pdf(pdf_path)
    page = _record(1)
    _set_pdf_provenance(page, pdf_path)
    page["source_hash"] = "0" * 64
    _write_page_records(processed / "doc_test.jsonl", [page])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1)])
    backend = FakeBackend({1: OCRResult("Should not run", 90.0, 90.0, 3)})

    summary = run_ocr_inventory(
        inventory,
        pdf_dir,
        processed,
        backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_failed"] == 1
    assert backend.calls == []
    assert json.loads((tmp_path / "errors.jsonl").read_text())["kind"] == "source_hash_mismatch"


def test_force_reprocesses_an_already_successful_page(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "doc_test.pdf"
    _write_pdf(pdf_path)
    page = _record(1)
    _set_pdf_provenance(page, pdf_path)
    _apply_ocr_result(
        page,
        OCRResult("Initial OCR result", 90.0, 90.0, 3),
        "eng",
        "Tesseract test",
        300,
        3,
    )
    _write_page_records(processed / "doc_test.jsonl", [page])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1)])
    backend = FakeBackend({1: OCRResult("Updated OCR result", 88.0, 80.0, 3)})

    summary = run_ocr_inventory(
        inventory,
        pdf_dir,
        processed,
        backend,
        force=True,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_succeeded"] == 1
    output = json.loads((processed / "doc_test.jsonl").read_text().splitlines()[0])
    assert output["text"] == "Updated OCR result"
    assert output["native_text"] == ""


def test_language_change_reprocesses_successful_ocr_without_force(
    tmp_path: Path,
) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "doc_test.pdf"
    _write_pdf(pdf_path)
    page = _record(1)
    _set_pdf_provenance(page, pdf_path)
    _apply_ocr_result(
        page,
        OCRResult("Old English result", 70.0, 60.0, 3),
        "eng",
        "Tesseract test",
        300,
        3,
    )
    _write_page_records(processed / "doc_test.jsonl", [page])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1, "eng+hin")])
    backend = FakeBackend({1: OCRResult("Updated bilingual text", 90.0, 80.0, 3)})

    summary = run_ocr_inventory(
        inventory,
        pdf_dir,
        processed,
        backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_succeeded"] == 1
    assert backend.calls == [(1, "eng+hin")]
    output = json.loads((processed / "doc_test.jsonl").read_text().splitlines()[0])
    assert output["text"] == "Updated bilingual text"
    assert output["ocr"]["language"] == "eng+hin"


def test_tsv_contaminated_ocr_is_reprocessed_without_force(
    tmp_path: Path,
) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "doc_test.pdf"
    _write_pdf(pdf_path)
    page = _record(1)
    _set_pdf_provenance(page, pdf_path)
    _apply_ocr_result(
        page,
        OCRResult("Contaminated\tTSV\tfields", 70.0, 60.0, 3),
        "eng",
        "Tesseract test",
        300,
        3,
    )
    _write_page_records(processed / "doc_test.jsonl", [page])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1)])
    backend = FakeBackend({1: OCRResult("Clean OCR result", 91.0, 82.0, 3)})

    summary = run_ocr_inventory(
        inventory,
        pdf_dir,
        processed,
        backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_succeeded"] == 1
    assert backend.calls == [(1, "eng")]
    output = json.loads((processed / "doc_test.jsonl").read_text().splitlines()[0])
    assert output["ocr"]["text"] == "Clean OCR result"


def test_empty_ocr_output_is_reported_as_failure(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "doc_test.pdf"
    _write_pdf(pdf_path)
    page = _record(1)
    _set_pdf_provenance(page, pdf_path)
    _write_page_records(processed / "doc_test.jsonl", [page])
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1)])
    backend = FakeBackend({1: OCRResult("", None, None, 0)})

    summary = run_ocr_inventory(
        inventory, pdf_dir, processed, backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_failed"] == 1
    assert json.loads((tmp_path / "errors.jsonl").read_text())["kind"] == "empty_ocr_result"


def test_page_failure_does_not_stop_later_pages(tmp_path: Path) -> None:
    class OnePageFails(FakeBackend):
        def recognize(self, page: pymupdf.Page, language: str) -> OCRResult:
            if page.number == 0:
                raise OCRProcessingError("synthetic page failure")
            return super().recognize(page, language)

    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    pdf_path = pdf_dir / "doc_test.pdf"
    _write_pdf(pdf_path, page_count=2)
    pages = [_record(1), _record(2)]
    for page in pages:
        _set_pdf_provenance(page, pdf_path)
    _write_page_records(processed / "doc_test.jsonl", pages)
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1), _target_row(2)])
    backend = OnePageFails({2: OCRResult("Page two text", 90.0, 90.0, 3)})

    summary = run_ocr_inventory(
        inventory, pdf_dir, processed, backend,
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_failed"] == 1
    assert summary["pages_succeeded"] == 1
    records = [
        json.loads(line)
        for line in (processed / "doc_test.jsonl").read_text().splitlines()
    ]
    assert records[0]["ocr"]["status"] == "failed"
    assert records[1]["text"] == "Page two text"


def test_missing_engine_is_reported_without_claiming_page_failures(
    tmp_path: Path,
) -> None:
    class MissingBackend(FakeBackend):
        def inspect(self) -> EngineInfo:
            raise OCRPrerequisiteError("Tesseract is not installed")

    pdf_dir = tmp_path / "pdfs"
    processed = tmp_path / "processed"
    pdf_dir.mkdir()
    processed.mkdir()
    inventory = tmp_path / "inventory.csv"
    _write_inventory(inventory, [_target_row(1)])

    summary = run_ocr_inventory(
        inventory,
        pdf_dir,
        processed,
        MissingBackend(),
        summary_path=tmp_path / "summary.json",
        errors_path=tmp_path / "errors.jsonl",
    )

    assert summary["pages_blocked"] == 1
    assert summary["pages_failed"] == 0
    assert summary["engine_version"] is None

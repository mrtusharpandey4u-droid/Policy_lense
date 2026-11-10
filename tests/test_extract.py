import csv
import json
from pathlib import Path

import pymupdf
import pytest

from src.config import MANIFEST_PATH, PDF_DIR, PROCESSED_DIR
from src.extract import (
    MIN_ALPHANUMERIC_RATIO,
    MIN_TEXT_CHARACTERS,
    _find_headings,
    _remove_bell_character_artifact,
    discover_documents,
    extract_corpus,
    extract_page_text,
)


def _create_text_pdf(
    path: Path,
    text: str = "A sufficiently long policy text for extraction.",
) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(path)
    document.close()


def _text_block(
    text: str,
    font_size: float,
    flags: int = 0,
    block_type: str = "text",
) -> dict:
    span = {
        "text": text,
        "bbox": [40, 40, 300, 55],
        "font": "Helvetica",
        "size": font_size,
        "flags": flags,
    }
    line = {"bbox": [40, 40, 300, 55], "spans": [span]}
    return {
        "block_type": block_type,
        "bbox": [40, 40, 300, 55],
        "text": text,
        "lines": [line],
    }


def test_extracts_text_positions_and_headings(tmp_path: Path) -> None:
    pdf_path = tmp_path / "doc_900_test.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Loan Policy", fontsize=22)
    page.insert_text((72, 110), "This is a sufficiently long body paragraph about loan policy terms.", fontsize=11)
    document.save(pdf_path)
    document.close()

    document = pymupdf.open(pdf_path)
    extracted = extract_page_text(
        document[0], "doc_900", 1, source_filename=pdf_path.name
    )
    document.close()

    assert extracted["page_number"] == 1
    assert extracted["source_filename"] == pdf_path.name
    assert "loan policy terms" in extracted["text"].lower()
    assert extracted["blocks"]
    assert all(len(block["bbox"]) == 4 for block in extracted["blocks"])
    assert any("Loan Policy" in heading["text"] for heading in extracted["headings"])
    assert not extracted["needs_ocr"]


def test_heading_detection_uses_body_text_size_and_standalone_style() -> None:
    body = _text_block(
        "This paragraph describes lending policy requirements in sufficient "
        "detail and explains the supporting compliance procedures.",
        11,
    )
    section_heading = _text_block("Consumption", 11, flags=2)
    chart_labels = [
        _text_block(f"Chart label {index}", 6.5)
        for index in range(20)
    ]
    table_label = _text_block(
        "E\x07xpenditure", 6.5, block_type="table"
    )

    headings = _find_headings(
        [*chart_labels, body, section_heading, table_label], 500
    )

    assert [heading["text"] for heading in headings] == ["Consumption"]


def test_heading_detection_accepts_bold_heading_at_body_font_size() -> None:
    body = _text_block(
        "This paragraph describes lending policy requirements in sufficient detail.",
        10,
    )
    bold_heading = _text_block("Regional Rural Banks", 10, flags=16)

    headings = _find_headings([body, bold_heading], 500)

    assert [heading["text"] for heading in headings] == [
        "Regional Rural Banks"
    ]


def test_removes_only_the_bell_control_character_artifact() -> None:
    assert (
        _remove_bell_character_artifact("E\x07xpenditure\tvalue")
        == "Expenditure\tvalue"
    )


def test_rbi_page_41_has_no_bell_artifacts_when_corpus_is_available() -> None:
    pdf_paths = list(PDF_DIR.glob("doc_036*.pdf"))
    if not pdf_paths:
        pytest.skip("Local corpus PDFs are not present in this checkout.")

    document = pymupdf.open(pdf_paths[0])
    extracted = extract_page_text(document[40], "doc_036", 41)
    document.close()

    def contains_bell(value: object) -> bool:
        if isinstance(value, str):
            return "\x07" in value
        if isinstance(value, list):
            return any(contains_bell(item) for item in value)
        if isinstance(value, dict):
            return any(contains_bell(item) for item in value.values())
        return False

    assert not contains_bell(extracted)
    assert any(
        "Expenditure" in cell
        for table in extracted["tables"]
        for row in table["rows"]
        for cell in row
    )


def test_flags_image_only_page_for_ocr_without_running_ocr(tmp_path: Path) -> None:
    pdf_path = tmp_path / "scanned.pdf"
    document = pymupdf.open()
    page = document.new_page()
    pixmap = pymupdf.Pixmap(
        pymupdf.csRGB, pymupdf.IRect(0, 0, 100, 100), False
    )
    pixmap.clear_with(245)
    page.insert_image(page.rect, stream=pixmap.tobytes("png"))
    document.save(pdf_path)
    document.close()

    document = pymupdf.open(pdf_path)
    extracted = extract_page_text(document[0], "doc_scan", 1)
    document.close()

    assert extracted["needs_ocr"]
    assert extracted["ocr_reason"] == "no_extractable_text"
    assert extracted["is_ocr"] is False
    assert any(block["block_type"] == "image" for block in extracted["blocks"])
    assert MIN_TEXT_CHARACTERS == 30
    assert MIN_ALPHANUMERIC_RATIO == 0.35


def test_detects_tables_and_preserves_structured_cells(tmp_path: Path) -> None:
    pdf_path = tmp_path / "table.pdf"
    document = pymupdf.open()
    page = document.new_page()
    x_positions = [50, 220, 390, 560]
    y_positions = [100, 145, 190, 235]
    for x in x_positions:
        page.draw_line((x, y_positions[0]), (x, y_positions[-1]))
    for y in y_positions:
        page.draw_line((x_positions[0], y), (x_positions[-1], y))
    values = [
        ["Document ID", "Issue Date", "Status"],
        ["Loan Policy One", "2024-01-02", "approved"],
        ["Loan Policy Two", "2024-02-03", "reviewed"],
    ]
    for row_index, row in enumerate(values):
        for column_index, value in enumerate(row):
            page.insert_text(
                (x_positions[column_index] + 5, y_positions[row_index] + 20),
                value,
                fontsize=10,
            )
    document.save(pdf_path)
    document.close()

    document = pymupdf.open(pdf_path)
    extracted = extract_page_text(document[0], "doc_table", 1)
    document.close()

    assert extracted["has_table"]
    assert "Loan Policy One" in extracted["tables"][0]["rows"][1][0]
    assert " | " in extracted["text"]
    assert not extracted["needs_ocr"]


def test_two_column_reading_order_is_left_column_then_right(tmp_path: Path) -> None:
    pdf_path = tmp_path / "two_columns.pdf"
    document = pymupdf.open()
    page = document.new_page()
    for y, prefix in [(80, "left one"), (230, "left two"), (380, "left three")]:
        page.insert_textbox(
            pymupdf.Rect(40, y, 285, y + 100),
            f"{prefix}. " + ("This paragraph describes lending policy requirements. " * 3),
            fontsize=11,
        )
    for y, prefix in [(80, "right one"), (230, "right two"), (380, "right three")]:
        page.insert_textbox(
            pymupdf.Rect(325, y, 570, y + 100),
            f"{prefix}. " + ("This paragraph describes compliance review requirements. " * 3),
            fontsize=11,
        )
    document.save(pdf_path)
    document.close()

    document = pymupdf.open(pdf_path)
    extracted = extract_page_text(document[0], "doc_columns", 1)
    document.close()

    assert extracted["layout_columns"] == 2
    assert extracted["layout"]["reading_order"] == "left_column_then_right_column"
    assert extracted["text"].index("left three") < extracted["text"].index("right one")


def test_discovery_matches_all_local_verified_pdfs() -> None:
    local_pdfs = list(PDF_DIR.glob("*.pdf"))
    if not local_pdfs:
        pytest.skip("Local corpus PDFs are not present in this checkout.")

    sources, errors = discover_documents(PDF_DIR, MANIFEST_PATH)

    assert len(local_pdfs) == 31
    assert len(sources) == 31
    assert not errors


def test_extracted_corpus_outputs_preserve_pages_and_flags() -> None:
    sources, _ = discover_documents(PDF_DIR, MANIFEST_PATH)
    if not sources or not all(
        (PROCESSED_DIR / f"{source.doc_id}.jsonl").is_file()
        for source in sources
    ):
        pytest.skip("Run `python -m src.extract` before validating corpus outputs.")

    text_native_pages = 0
    ocr_candidates = 0
    pages_with_tables = 0
    two_column_pages = 0
    for source in sources:
        output_path = PROCESSED_DIR / f"{source.doc_id}.jsonl"
        records = [
            json.loads(line)
            for line in output_path.read_text(encoding="utf-8").splitlines()
        ]
        assert len(records) == int(source.metadata["page_count"])
        assert [page["page_number"] for page in records] == list(
            range(1, len(records) + 1)
        )
        for page in records:
            assert page["doc_id"] == source.doc_id
            assert page["source_filename"] == source.path.name
            assert isinstance(page["blocks"], list)
            assert isinstance(page["layout"], dict)
            assert isinstance(page["tables"], list)
            assert page["page_error"] is None
            if source.metadata.get("document_type") == "text_native":
                text_native_pages += 1
                if not page["text"].strip():
                    assert page["needs_ocr"]
            ocr_candidates += page["needs_ocr"]
            pages_with_tables += page["has_table"]
            two_column_pages += page["layout_columns"] == 2

    assert text_native_pages > 0
    assert ocr_candidates > 0
    assert pages_with_tables > 0
    assert two_column_pages > 0
    assert (PROCESSED_DIR / "extraction_errors.jsonl").is_file()
    summary = json.loads(
        (PROCESSED_DIR / "extraction_summary.json").read_text(encoding="utf-8")
    )
    assert summary["documents_processed"] == 31
    assert summary["pages_failed"] == 0


def test_corrupt_document_is_reported_without_stopping_other_documents(
    tmp_path: Path,
) -> None:
    pdf_dir = tmp_path / "pdfs"
    output_dir = tmp_path / "processed"
    pdf_dir.mkdir()
    valid_pdf = pdf_dir / "doc_901_valid.pdf"
    corrupt_pdf = pdf_dir / "doc_902_corrupt.pdf"
    _create_text_pdf(valid_pdf)
    corrupt_pdf.write_bytes(b"not a PDF")
    manifest_path = tmp_path / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as manifest_file:
        writer = csv.DictWriter(
            manifest_file,
            fieldnames=[
                "doc_id",
                "title",
                "source_hash",
                "download_status",
            ],
        )
        writer.writeheader()
        writer.writerows(
            [
                {
                    "doc_id": "doc_901",
                    "title": "Valid policy",
                    "source_hash": "",
                    "download_status": "verified",
                },
                {
                    "doc_id": "doc_902",
                    "title": "Corrupt policy",
                    "source_hash": "",
                    "download_status": "verified",
                },
            ]
        )

    summary = extract_corpus(pdf_dir, manifest_path, output_dir)

    assert summary["documents_discovered"] == 2
    assert summary["documents_processed"] == 1
    assert summary["documents_failed"] == 1
    assert summary["pages_successfully_extracted"] == 1
    assert summary["extraction_failures"] == 1
    assert (output_dir / "doc_901.jsonl").is_file()
    errors = [
        json.loads(line)
        for line in (output_dir / "extraction_errors.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    assert errors[0]["kind"] == "document_extraction_error"

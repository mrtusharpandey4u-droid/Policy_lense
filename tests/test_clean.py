import copy
import json
from pathlib import Path

import pytest

from src.clean import clean_corpus, clean_document_records


def _record(
    page_number: int,
    text: str,
    *,
    doc_id: str = "doc_test",
    title: str = "Test lending policy",
    blocks: list[dict] | None = None,
    headings: list[dict] | None = None,
    tables: list[dict] | None = None,
    needs_ocr: bool = False,
) -> dict:
    return {
        "doc_id": doc_id,
        "document_title": title,
        "source_filename": "doc_test.pdf",
        "source_hash": "source-hash",
        "page_number": page_number,
        "text": text,
        "blocks": blocks or [],
        "headings": headings or [],
        "tables": tables or [],
        "has_table": bool(tables),
        "needs_ocr": needs_ocr,
        "is_ocr": False,
        "page_error": None,
    }


def _block_with_wrapped_lines(first: str, second: str) -> list[dict]:
    return [
        {
            "block_type": "text",
            "lines": [
                {"spans": [{"text": first}]},
                {"spans": [{"text": second}]},
            ],
        }
    ]


def test_normalizes_whitespace_but_preserves_paragraph_and_table_separators() -> None:
    table = {"rows": [["Product", "Amount"], ["Loan", "₹ 1,00,000"]]}
    page = _record(
        1,
        "Policy   terms\r\n\r\n\r\nRate\t|   Amount\n5%  |  ₹ 1,00,000",
        tables=[table],
    )

    cleaned, _ = clean_document_records([page])

    assert cleaned[0]["canonical_text"] == (
        "Policy terms\n\nRate\t| Amount\n5% | ₹ 1,00,000"
    )
    assert cleaned[0]["tables"] == [table]


def test_removes_only_high_confidence_repeating_edge_furniture() -> None:
    pages = [_record(1, "Cover title\nSection 1 applies.")]
    pages.extend(
        _record(n, f"INTERNAL COPY\nSection {n} applies.")
        for n in range(2, 6)
    )

    cleaned, stats = clean_document_records(pages)

    assert cleaned[0]["canonical_text"] == "Cover title\nSection 1 applies."
    assert all(
        page["canonical_text"] == f"Section {page['page_number']} applies."
        for page in cleaned[1:]
    )
    assert stats["repeating_header_footer_lines_removed"] == 4
    assert cleaned[1]["cleaning"]["repeating_edge_line_candidates"] == [
        {
            "edge": "top",
            "text": "INTERNAL COPY",
            "pages": 4,
            "action": "removed_repeating_edge_line",
        }
    ]


def test_preserves_repeated_titles_headings_and_legal_notices() -> None:
    pages = [
        _record(
            n,
            "Test lending policy\nGovernment notification under section 4",
            headings=[{"text": "Test lending policy"}],
        )
        for n in range(1, 5)
    ]

    cleaned, stats = clean_document_records(pages)

    assert all(
        "Test lending policy\nGovernment notification under section 4"
        == page["canonical_text"]
        for page in cleaned
    )
    assert stats["repeating_header_footer_lines_removed"] == 0
    assert stats["repeating_header_footer_candidates"] >= 1


def test_preserves_repeated_title_line_found_on_document_cover() -> None:
    title_line = "Customer Service and Grievance Handling - Standard"
    pages = [
        _record(n, f"{title_line}\nPage content {n}.", title="Grievance Redressal Policy")
        for n in range(1, 6)
    ]

    cleaned, stats = clean_document_records(pages)

    assert all(title_line in page["canonical_text"] for page in cleaned)
    assert stats["repeating_header_footer_lines_removed"] == 0
    assert all(
        page["cleaning"]["repeating_edge_line_candidates"][0]["action"]
        == "retained_title_heading_or_substantive_edge_text"
        for page in cleaned
    )


def test_removes_repeating_standalone_page_numbers_but_not_clause_numbers() -> None:
    pages = [
        _record(n, f"{n}\nClause {n}. This applies to every loan.")
        for n in range(1, 6)
    ]

    cleaned, stats = clean_document_records(pages)

    assert all(
        page["canonical_text"] == (
            f"Clause {page['page_number']}. This applies to every loan."
        )
        for page in cleaned
    )
    assert stats["page_numbers_removed"] == 5


def test_joins_native_wrapped_hyphens_without_removing_hyphen_or_values() -> None:
    source = "The rate is 7.25% and repayment is time-\nto-time."
    page = _record(
        1,
        source,
        blocks=_block_with_wrapped_lines("repayment is time-", "to-time."),
    )

    cleaned, stats = clean_document_records([page])

    assert cleaned[0]["canonical_text"] == (
        "The rate is 7.25% and repayment is time-to-time."
    )
    assert cleaned[0]["text"] == source
    assert stats["hyphenation_line_joins"] == 1


def test_joins_wrapped_native_lines_but_keeps_paragraph_boundaries() -> None:
    source = "The borrower must provide\nfinancial statements annually.\n\nA separate paragraph follows."
    page = _record(
        1,
        source,
        blocks=_block_with_wrapped_lines(
            "The borrower must provide",
            "financial statements annually.",
        ),
    )

    cleaned, stats = clean_document_records([page])

    assert cleaned[0]["canonical_text"] == (
        "The borrower must provide financial statements annually.\n\n"
        "A separate paragraph follows."
    )
    assert stats["wrapped_line_joins"] == 1


def test_preserves_standalone_section_labels_inside_text_blocks() -> None:
    source = "II.2.4\nPrivate final consumption expenditure begins here."
    page = _record(
        1,
        source,
        blocks=_block_with_wrapped_lines(
            "II.2.4",
            "Private final consumption expenditure begins here.",
        ),
    )

    cleaned, stats = clean_document_records([page])

    assert cleaned[0]["canonical_text"] == source
    assert stats["wrapped_line_joins"] == 0


def test_preserves_legal_terms_financial_values_and_ambiguous_hyphens() -> None:
    text = "Section 17(2), non-\nperforming assets, ₹ 1,25,000, 8.5%, 2024-25."
    page = _record(1, text)

    cleaned, _ = clean_document_records([page])

    assert cleaned[0]["canonical_text"] == text
    assert cleaned[0]["cleaning"]["needs_manual_review"]
    assert cleaned[0]["cleaning"]["unresolved_hyphenation_candidates"]


def test_uses_ocr_only_when_native_text_fails_documented_quality_threshold() -> None:
    poor_native = _record(1, "NABARD 2024", needs_ocr=True)
    poor_native.update(
        {
            "is_ocr": True,
            "native_text": "NABARD 2024",
            "ocr": {
                "status": "success",
                "text": "A complete OCR recovery of this scanned lending policy page.",
                "engine": "Tesseract",
                "engine_version": "test",
                "language": "eng",
                "source_filename": "doc_test.pdf",
                "source_hash": "source-hash",
                "source_page_number": 1,
                "confidence_mean": 91.0,
            },
        }
    )
    good_native = _record(
        2, "This is a sufficiently long reliable native text extraction."
    )
    good_native.update(
        {
            "is_ocr": True,
            "native_text": good_native["text"],
            "ocr": {"status": "success", "text": "wrong duplicate OCR text"},
        }
    )

    cleaned, stats = clean_document_records([poor_native, good_native])

    assert cleaned[0]["canonical_text"].startswith("A complete OCR recovery")
    assert cleaned[0]["cleaning"]["selected_source"] == "ocr"
    assert cleaned[0]["cleaning"]["ocr_provenance"]["language"] == "eng"
    assert cleaned[1]["canonical_text"] == good_native["native_text"]
    assert cleaned[1]["cleaning"]["selected_source"] == "native"
    assert "wrong duplicate OCR text" not in cleaned[1]["canonical_text"]
    assert stats["ocr_selected_pages"] == 1
    assert stats["native_selected_pages"] == 1


def test_uses_separate_ocr_field_when_native_snapshot_is_missing() -> None:
    page = _record(1, "This field may already contain merged output.")
    page.update(
        {
            "is_ocr": True,
            "ocr": {
                "status": "success",
                "text": "The original OCR-only fallback text.",
                "language": "eng",
            },
        }
    )

    cleaned, _ = clean_document_records([page])

    assert cleaned[0]["canonical_text"] == "The original OCR-only fallback text."
    assert cleaned[0]["cleaning"]["selected_source"] == "ocr"
    assert cleaned[0]["cleaning"]["selection_reason"] == (
        "native_text_missing_and_combined_text_not_trusted"
    )


def test_preserves_source_fields_tables_identifiers_and_page_numbers() -> None:
    page = _record(
        7,
        "Native policy content, with a table.",
        tables=[{"rows": [["Limit", "Value"], ["Daily", "₹ 25,000"]]}],
    )
    original = copy.deepcopy(page)

    cleaned, _ = clean_document_records([page])

    assert page == original
    assert cleaned[0]["doc_id"] == original["doc_id"]
    assert cleaned[0]["page_number"] == 7
    assert cleaned[0]["source_hash"] == original["source_hash"]
    assert cleaned[0]["text"] == original["text"]
    assert cleaned[0]["tables"] == original["tables"]


def test_cleaning_is_idempotent_and_output_is_separate_from_raw(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    clean_dir = tmp_path / "cleaned"
    raw_dir.mkdir()
    source = _record(1, "Policy   text")
    raw_path = raw_dir / "doc_test.jsonl"
    raw_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
    raw_before = raw_path.read_bytes()

    first = clean_corpus(raw_dir, clean_dir, tmp_path / "summary.json")
    first_bytes = (clean_dir / "doc_test.jsonl").read_bytes()
    second = clean_corpus(raw_dir, clean_dir, tmp_path / "summary.json")
    second_bytes = (clean_dir / "doc_test.jsonl").read_bytes()
    result = json.loads(second_bytes.decode("utf-8").splitlines()[0])

    assert first["pages_processed"] == second["pages_processed"] == 1
    assert first["pages_changed"] == second["pages_changed"] == 1
    assert first_bytes == second_bytes
    assert raw_path.read_bytes() == raw_before
    assert result["canonical_text"] == "Policy text"
    assert result["text"] == source["text"]


def test_rejects_duplicate_or_invalid_page_numbers() -> None:
    with pytest.raises(ValueError, match="unique positive integers"):
        clean_document_records([_record(1, "A page."), _record(1, "Another page.")])

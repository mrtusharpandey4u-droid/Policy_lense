import copy

from src.chunk import (
    _split_table_rows,
    _tokens,
    chunk_document,
)


def _page(
    page_number: int,
    text: str,
    *,
    doc_id: str = "doc_test",
    headings: list[dict] | None = None,
    tables: list[dict] | None = None,
    selected_source: str = "native",
    review: bool = False,
) -> dict:
    return {
        "doc_id": doc_id,
        "document_title": "Test Lending Policy",
        "source_filename": "doc_test.pdf",
        "source_hash": "source-hash",
        "page_number": page_number,
        "canonical_text": text,
        "headings": headings or [],
        "tables": tables or [],
        "cleaning": {
            "selected_source": selected_source,
            "needs_manual_review": review,
            "review_reasons": ["review required"] if review else [],
            "ocr_provenance": (
                {
                    "engine": "Tesseract",
                    "language": "hin",
                    "source_filename": "doc_test.pdf",
                    "source_hash": "source-hash",
                    "source_page_number": page_number,
                }
                if selected_source == "ocr"
                else None
            ),
        },
    }


def _manifest() -> dict[str, str]:
    return {
        "title": "Test Lending Policy",
        "issuer": "Test Financial Regulator",
        "issue_date": "2025-02-03",
        "source_hash": "source-hash",
    }


def test_fixed_size_chunking_respects_size_overlap_and_page_ranges() -> None:
    words = [f"word{index}" for index in range(31)]
    records = [
        _page(1, " ".join(words[:15])),
        _page(2, " ".join(words[15:])),
    ]

    chunks = chunk_document(
        "doc_test", records, _manifest(), "fixed_size", chunk_size=10, overlap=2
    )
    text_chunks = [chunk for chunk in chunks if chunk["content_type"] == "text"]

    assert len(text_chunks) == 4
    assert all(chunk["token_count"] <= 10 for chunk in text_chunks)
    assert text_chunks[0]["page_start"] == text_chunks[0]["page_end"] == 1
    assert any(
        chunk["page_start"] == 1 and chunk["page_end"] == 2
        for chunk in text_chunks
    )
    assert text_chunks[-1]["page_start"] == text_chunks[-1]["page_end"] == 2
    for left, right in zip(text_chunks, text_chunks[1:]):
        assert [match.group() for match in _tokens(left["text"])[-2:]] == [
            match.group() for match in _tokens(right["text"])[:2]
        ]
    covered = [match.group() for match in _tokens(text_chunks[0]["text"])]
    for chunk in text_chunks[1:]:
        covered.extend(match.group() for match in _tokens(chunk["text"])[2:])
    assert covered == words


def test_chunk_metadata_is_from_manifest_and_source_pages() -> None:
    records = [
        _page(4, "This page contains enough words for a small test chunk.", review=True)
    ]
    chunks = chunk_document(
        "doc_test", records, _manifest(), "fixed_size", chunk_size=20, overlap=3
    )

    chunk = chunks[0]
    assert chunk["doc_id"] == "doc_test"
    assert chunk["title"] == "Test Lending Policy"
    assert chunk["issuer"] == "Test Financial Regulator"
    assert chunk["issue_date"] == "2025-02-03"
    assert chunk["source_hash"] == "source-hash"
    assert chunk["page_start"] == chunk["page_end"] == 4
    assert chunk["chunking_strategy"] == "fixed_size"
    assert chunk["has_cleaning_review"]
    assert chunk["review_pages"] == [4]
    assert chunk["page_provenance"][0]["cleaning_review"]


def test_chunk_ids_are_deterministic_for_identical_inputs_and_config() -> None:
    records = [_page(1, "Stable chunk identifiers preserve reproducibility.")]
    first = chunk_document(
        "doc_test", records, _manifest(), "fixed_size", chunk_size=12, overlap=2
    )
    second = chunk_document(
        "doc_test", copy.deepcopy(records), _manifest(), "fixed_size", 12, 2
    )

    assert [chunk["chunk_id"] for chunk in first] == [
        chunk["chunk_id"] for chunk in second
    ]
    assert len({chunk["chunk_id"] for chunk in first}) == len(first)


def test_structure_aware_uses_headings_and_keeps_sections_together() -> None:
    text = (
        "1. Eligibility\nBorrowers must meet the stated lending criteria.\n\n"
        "2. Interest Rate\nThe annual rate is 8.5% and applies to the loan."
    )
    records = [
        _page(
            1,
            text,
            headings=[
                {"text": "1. Eligibility"},
                {"text": "2. Interest Rate"},
            ],
        )
    ]

    chunks = chunk_document(
        "doc_test",
        records,
        _manifest(),
        "structure_aware",
        chunk_size=20,
        overlap=4,
    )
    text_chunks = [chunk for chunk in chunks if chunk["content_type"] == "text"]

    assert len(text_chunks) == 2
    assert text_chunks[0]["section_title"] == "1. Eligibility"
    assert text_chunks[1]["section_title"] == "2. Interest Rate"
    assert "8.5%" in text_chunks[1]["text"]


def test_long_structure_section_splits_with_overlap_and_continuity() -> None:
    words = [f"term{index}" for index in range(31)]
    record = _page(3, "Section A\n" + " ".join(words), headings=[{"text": "Section A"}])

    chunks = chunk_document(
        "doc_test", [record], _manifest(), "structure_aware", 10, 2
    )
    text_chunks = [chunk for chunk in chunks if chunk["content_type"] == "text"]

    assert len(text_chunks) >= 4
    assert all(chunk["section_title"] == "Section A" for chunk in text_chunks)
    assert all(chunk["token_count"] <= 10 for chunk in text_chunks)
    assert any(chunk["is_continuation"] for chunk in text_chunks[1:])
    reconstructed = []
    for chunk in text_chunks:
        tokens = [match.group() for match in _tokens(chunk["text"])]
        if chunk["is_continuation"]:
            tokens = tokens[2:]
        reconstructed.extend(tokens)
    assert reconstructed == [
        match.group() for match in _tokens(record["canonical_text"])
    ]


def test_ocr_and_cleaning_review_provenance_are_preserved() -> None:
    record = _page(9, "यह OCR text is retained with source provenance.", selected_source="ocr", review=True)

    chunks = chunk_document(
        "doc_test", [record], _manifest(), "structure_aware", 20, 2
    )
    chunk = next(chunk for chunk in chunks if chunk["content_type"] == "text")

    assert chunk["contains_ocr"]
    assert chunk["has_cleaning_review"]
    provenance = chunk["page_provenance"][0]
    assert provenance["text_source"] == "ocr"
    assert provenance["ocr_provenance"]["language"] == "hin"
    assert provenance["ocr_provenance"]["source_page_number"] == 9


def test_table_is_preserved_and_large_tables_split_at_rows_with_header() -> None:
    table = {
        "table_number": 2,
        "bbox": [10, 20, 300, 400],
        "row_count": 8,
        "column_count": 2,
        "rows": [["Year", "Amount"], *[[str(year), f"₹ {year * 100}"] for year in range(1, 8)]],
        "extraction_method": "pymupdf_find_tables",
    }
    original_rows = copy.deepcopy(table["rows"])
    records = [_page(6, "Financial summary.", tables=[table])]

    chunks = chunk_document(
        "doc_test", records, _manifest(), "fixed_size", chunk_size=12, overlap=2
    )
    table_chunks = [chunk for chunk in chunks if chunk["content_type"] == "table"]

    assert len(table_chunks) > 1
    assert all(chunk["tables"][0]["rows"][0] == table["rows"][0] for chunk in table_chunks)
    assert all(
        chunk["tables"][0]["original_table_number"] == 2
        for chunk in table_chunks
    )
    assert all(
        chunk["tables"][0]["part_count"] == len(table_chunks)
        for chunk in table_chunks
    )
    data_rows = [
        row
        for chunk in table_chunks
        for row in chunk["tables"][0]["rows"][1:]
    ]
    assert data_rows == original_rows[1:]
    assert table["rows"] == original_rows
    assert all(chunk["page_start"] == chunk["page_end"] == 6 for chunk in table_chunks)


def test_single_oversize_table_row_is_kept_intact_and_marked() -> None:
    table = {
        "table_number": 1,
        "rows": [
            ["Label", "Value"],
            ["Long label " * 8, "₹ 1,25,000"],
        ],
    }
    fragments = _split_table_rows(table, 8)

    assert len(fragments) == 1
    assert fragments[0][0] == table["rows"]
    assert fragments[0][1]


def test_empty_review_page_gets_review_only_chunk() -> None:
    chunks = chunk_document(
        "doc_test",
        [_page(11, "", selected_source="ocr", review=True)],
        _manifest(),
        "fixed_size",
        10,
        2,
    )

    assert len(chunks) == 1
    assert chunks[0]["content_type"] == "review_only"
    assert chunks[0]["token_count"] == 0
    assert chunks[0]["review_pages"] == [11]


def test_empty_page_without_review_is_not_emitted_as_empty_chunk() -> None:
    chunks = chunk_document(
        "doc_test",
        [_page(1, ""), _page(2, "Useful policy content remains.")],
        _manifest(),
        "structure_aware",
        20,
        2,
    )

    assert chunks
    assert all(chunk["content_type"] != "review_only" for chunk in chunks)
    assert all(chunk["token_count"] > 0 for chunk in chunks)


def test_table_only_canonical_fallback_is_not_duplicated_as_text() -> None:
    table = {
        "table_number": 1,
        "rows": [["Loan", "Limit"], ["Personal", "₹ 25,000"]],
    }
    fallback = "Loan | Limit\nPersonal | ₹ 25,000"
    chunks = chunk_document(
        "doc_test",
        [_page(1, fallback, tables=[table])],
        _manifest(),
        "fixed_size",
        20,
        2,
    )

    assert [chunk["content_type"] for chunk in chunks] == ["table"]


def test_manifest_metadata_is_not_fabricated_when_absent() -> None:
    chunks = chunk_document(
        "doc_test",
        [_page(1, "Some source text.")],
        {},
        "fixed_size",
        20,
        2,
    )

    chunk = chunks[0]
    assert chunk["title"] == "Test Lending Policy"
    assert "issuer" not in chunk
    assert "issue_date" not in chunk

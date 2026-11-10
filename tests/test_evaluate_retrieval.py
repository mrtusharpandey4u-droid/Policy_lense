from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import evaluate_retrieval as evaluation


def _gold(doc_id: str = "doc_a", pages: list[int] | None = None) -> list[dict]:
    return [{"doc_id": doc_id, "gold_pages": [1] if pages is None else pages}]


def _result(
    doc_id: str = "doc_a",
    *,
    pages: list[int] | None = None,
    page_start: int | None = None,
    page_end: int | None = None,
) -> dict:
    result = {"doc_id": doc_id}
    if pages is not None:
        result["page_provenance"] = [{"page_number": page} for page in pages]
    if page_start is not None:
        result["page_start"] = page_start
    if page_end is not None:
        result["page_end"] = page_end
    return result


def test_relevant_at_rank_one() -> None:
    assert evaluation.first_relevant_rank([_result(pages=[1])], _gold()) == 1


def test_relevant_at_rank_three() -> None:
    results = [_result("other", pages=[1]), _result("other", pages=[1]), _result(pages=[1])]
    assert evaluation.first_relevant_rank(results, _gold()) == 3


def test_relevant_at_rank_five() -> None:
    results = [_result("other", pages=[1]) for _ in range(4)] + [_result(pages=[1])]
    assert evaluation.first_relevant_rank(results, _gold()) == 5


def test_relevant_at_rank_ten() -> None:
    results = [_result("other", pages=[1]) for _ in range(9)] + [_result(pages=[1])]
    assert evaluation.first_relevant_rank(results, _gold()) == 10


def test_no_relevant_result_in_top_ten() -> None:
    results = [_result("other", pages=[1]) for _ in range(10)]
    assert evaluation.first_relevant_rank(results, _gold()) is None


def test_matching_document_with_wrong_page_is_not_relevant() -> None:
    assert not evaluation.is_relevant(_result(pages=[2]), _gold(pages=[1]))


def test_matching_page_with_wrong_document_is_not_relevant() -> None:
    assert not evaluation.is_relevant(_result("other", pages=[1]), _gold())


def test_multiple_gold_references_match_either_document_and_page() -> None:
    references = _gold("doc_a", [2]) + _gold("doc_b", [5])
    assert evaluation.is_relevant(_result("doc_b", pages=[5]), references)
    assert not evaluation.is_relevant(_result("doc_b", pages=[4]), references)


def test_multiple_chunks_from_same_gold_page_use_first_rank() -> None:
    results = [_result(pages=[1]), _result(pages=[1])]
    assert evaluation.first_relevant_rank(results, _gold()) == 1


def test_inclusive_page_range_overlap() -> None:
    assert evaluation.is_relevant(
        _result(page_start=4, page_end=6), _gold(pages=[6])
    )
    assert not evaluation.is_relevant(
        _result(page_start=4, page_end=5), _gold(pages=[6])
    )


def test_printed_page_number_is_not_used_for_qdrant_matching() -> None:
    result = {
        "doc_id": "doc_a",
        "page_provenance": [{"page_number": 41}],
        "page_start": 41,
        "page_end": 41,
        "printed_page_numbers": [16],
        "pdf_page_indices": [40],
    }
    assert evaluation.is_relevant(result, _gold(pages=[41]))
    assert not evaluation.is_relevant(result, _gold(pages=[16]))


def test_known_question_level_recall_and_mrr() -> None:
    results = [
        {"first_relevant_rank": 1, "reciprocal_rank": 1.0},
        {"first_relevant_rank": 3, "reciprocal_rank": 1 / 3},
        {"first_relevant_rank": 5, "reciprocal_rank": 1 / 5},
        {"first_relevant_rank": 10, "reciprocal_rank": 1 / 10},
        {"first_relevant_rank": None, "reciprocal_rank": 0.0},
    ]

    metrics = evaluation.calculate_metrics(results)

    assert metrics["recall_at_k"]["3"] == {
        "hits": 2,
        "denominator": 5,
        "value": 0.4,
        "percentage": 40.0,
    }
    assert metrics["recall_at_k"]["5"]["value"] == 0.6
    assert metrics["recall_at_k"]["10"]["value"] == 0.8
    assert metrics["mrr"]["value"] == (1 + 1 / 3 + 1 / 5 + 1 / 10) / 5


def test_run_evaluation_reuses_one_query_vector_for_both_strategies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dataset = tmp_path / "questions.jsonl"
    questions = []
    for number in range(1, 26):
        question_type = (
            "standard"
            if number <= 15
            else "table_value"
            if number <= 20
            else "paraphrased"
        )
        questions.append(
            {
                "question_id": f"Q{number:03d}",
                "question": f"Question {number}",
                "question_type": question_type,
                "gold_references": _gold(),
            }
        )
    dataset.write_text(
        "".join(json.dumps(question) + "\n" for question in questions),
        encoding="utf-8",
    )

    encoded_queries: list[str] = []
    vectors: list[list[float]] = []
    retrieval_calls: list[dict] = []

    def fake_embed(query: str) -> list[float]:
        encoded_queries.append(query)
        vector = [float(len(encoded_queries))]
        vectors.append(vector)
        return vector

    def fake_retrieve(query: str, **kwargs: object) -> list[dict]:
        retrieval_calls.append({"query": query, **kwargs})
        return []

    monkeypatch.setattr(evaluation.search, "embed_query", fake_embed)
    monkeypatch.setattr(evaluation.search, "retrieve", fake_retrieve)

    result = evaluation.run_evaluation(
        dataset,
        tmp_path / "results",
        tmp_path / "unused-storage",
    )

    assert len(encoded_queries) == 25
    assert len(retrieval_calls) == 50
    assert result["query_evaluation_count"] == 50
    for index, vector in enumerate(vectors):
        fixed_call, structure_call = retrieval_calls[index * 2 : index * 2 + 2]
        assert fixed_call["query"] == structure_call["query"] == encoded_queries[index]
        assert fixed_call["query_vector"] is vector
        assert structure_call["query_vector"] is vector
        assert fixed_call["filters"] is structure_call["filters"] is None
        assert fixed_call["top_k"] == structure_call["top_k"] == 10
    saved = json.loads(
        (tmp_path / "results/retrieval_evaluation_results.json").read_text(
            encoding="utf-8"
        )
    )
    assert saved["query_embeddings_generated"] == 25
    assert len(saved["results"]) == 50

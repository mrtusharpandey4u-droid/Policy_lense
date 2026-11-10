"""Evaluate PolicyLens retrieval against the hand-curated gold references."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from src import search
from src.config import QDRANT_STORAGE_DIR, PROJECT_ROOT
from src.embed import DEVICE, EMBEDDING_DIMENSIONS, MODEL_NAME, MODEL_REVISION

DEFAULT_DATASET = PROJECT_ROOT / "data/evaluation/evaluation_questions.jsonl"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data/evaluation/results"
STRATEGIES = ("fixed_size", "structure_aware")
TOP_K = 10
RECALL_CUTOFFS = (3, 5, 10)


class EvaluationError(RuntimeError):
    """Raised when an evaluation input or retrieval result is invalid."""


def _read_dataset(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise EvaluationError(f"Cannot read evaluation dataset {path}: {exc}") from exc
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvaluationError(
                f"Invalid JSON at {path}:{line_number}: {exc}"
            ) from exc
        if not isinstance(record, dict):
            raise EvaluationError(
                f"Expected an object at {path}:{line_number}."
            )
        if not isinstance(record.get("question"), str) or not record["question"].strip():
            raise EvaluationError(f"Question at {path}:{line_number} is empty.")
        if not isinstance(record.get("gold_references"), list) or not record[
            "gold_references"
        ]:
            raise EvaluationError(
                f"Question at {path}:{line_number} has no gold references."
            )
        records.append(record)
    if not records:
        raise EvaluationError(f"Evaluation dataset is empty: {path}")
    return records


def _result_pages(result: dict[str, Any]) -> set[int]:
    provenance = result.get("page_provenance")
    if isinstance(provenance, list):
        pages = {
            entry["page_number"]
            for entry in provenance
            if isinstance(entry, dict)
            and isinstance(entry.get("page_number"), int)
            and not isinstance(entry.get("page_number"), bool)
        }
        if pages:
            return pages
    page_start, page_end = result.get("page_start"), result.get("page_end")
    if (
        isinstance(page_start, int)
        and not isinstance(page_start, bool)
        and isinstance(page_end, int)
        and not isinstance(page_end, bool)
        and page_start >= 1
        and page_end >= page_start
    ):
        return set(range(page_start, page_end + 1))
    return set()


def is_relevant(
    result: dict[str, Any], gold_references: list[dict[str, Any]]
) -> bool:
    """Match document ID and 1-based PDF page provenance, never printed pages."""
    doc_id = result.get("doc_id")
    pages = _result_pages(result)
    if not isinstance(doc_id, str) or not pages:
        return False
    return any(
        doc_id == reference.get("doc_id")
        and bool(pages.intersection(reference.get("gold_pages", [])))
        for reference in gold_references
        if isinstance(reference, dict)
        and isinstance(reference.get("gold_pages"), list)
    )


def first_relevant_rank(
    results: list[dict[str, Any]], gold_references: list[dict[str, Any]]
) -> int | None:
    for rank, result in enumerate(results, 1):
        if is_relevant(result, gold_references):
            return rank
    return None


def _result_record(
    question: dict[str, Any], strategy: str, retrieved: list[dict[str, Any]]
) -> dict[str, Any]:
    gold_references = question["gold_references"]
    ranking: list[dict[str, Any]] = []
    for rank, result in enumerate(retrieved[:TOP_K], 1):
        if not isinstance(result.get("doc_id"), str):
            raise EvaluationError(
                f"{question['question_id']} {strategy} rank {rank} has no doc_id."
            )
        score = result.get("score")
        if isinstance(score, bool) or not isinstance(score, (float, int)) or not math.isfinite(score):
            raise EvaluationError(
                f"{question['question_id']} {strategy} rank {rank} has an invalid score."
            )
        ranking.append(
            {
                "rank": rank,
                "chunk_id": result.get("chunk_id"),
                "doc_id": result["doc_id"],
                "page_start": result.get("page_start"),
                "page_end": result.get("page_end"),
                "page_provenance": result.get("page_provenance", []),
                "score": float(score),
                "relevant": is_relevant(result, gold_references),
            }
        )
    rank = first_relevant_rank(retrieved[:TOP_K], gold_references)
    return {
        "question_id": question["question_id"],
        "question_type": question.get("question_type"),
        "strategy": strategy,
        "question": question["question"],
        "gold_references": gold_references,
        "retrieved_results": ranking,
        "first_relevant_rank": rank,
        "reciprocal_rank": 1.0 / rank if rank is not None else 0.0,
        "hit_at_3": rank is not None and rank <= 3,
        "hit_at_5": rank is not None and rank <= 5,
        "hit_at_10": rank is not None and rank <= 10,
    }


def calculate_metrics(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calculate question-level Recall@K and MRR for one result group."""
    if not results:
        raise EvaluationError("Cannot calculate metrics for an empty result set.")
    count = len(results)
    recall: dict[str, dict[str, float | int]] = {}
    for cutoff in RECALL_CUTOFFS:
        hits = sum(
            result.get("first_relevant_rank") is not None
            and result["first_relevant_rank"] <= cutoff
            for result in results
        )
        recall[str(cutoff)] = {
            "hits": hits,
            "denominator": count,
            "value": hits / count,
            "percentage": 100.0 * hits / count,
        }
    mrr = sum(float(result["reciprocal_rank"]) for result in results) / count
    return {
        "question_count": count,
        "recall_at_k": recall,
        "mrr": {"value": mrr, "percentage": 100.0 * mrr},
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_strategy: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_category: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for result in results:
        by_strategy[result["strategy"]].append(result)
        by_category[result["question_type"]][result["strategy"]].append(result)

    metrics = {
        strategy: calculate_metrics(by_strategy[strategy])
        for strategy in STRATEGIES
    }
    category_metrics = {
        category: {
            strategy: calculate_metrics(by_category[category][strategy])
            for strategy in STRATEGIES
        }
        for category in ("standard", "table_value", "paraphrased")
    }

    top10_hits = {
        strategy: {
            result["question_id"]: result["hit_at_10"]
            for result in by_strategy[strategy]
        }
        for strategy in STRATEGIES
    }
    fixed_hits = top10_hits["fixed_size"]
    structure_hits = top10_hits["structure_aware"]
    question_comparison = {
        "both": sorted(qid for qid in fixed_hits if fixed_hits[qid] and structure_hits[qid]),
        "fixed_size_only": sorted(
            qid for qid in fixed_hits if fixed_hits[qid] and not structure_hits[qid]
        ),
        "structure_aware_only": sorted(
            qid for qid in fixed_hits if structure_hits[qid] and not fixed_hits[qid]
        ),
        "missed_by_both": sorted(
            qid for qid in fixed_hits if not fixed_hits[qid] and not structure_hits[qid]
        ),
    }
    low_rank = {
        strategy: [
            {
                "question_id": result["question_id"],
                "first_relevant_rank": result["first_relevant_rank"],
            }
            for result in by_strategy[strategy]
            if result["first_relevant_rank"] is not None
            and result["first_relevant_rank"] >= 6
        ]
        for strategy in STRATEGIES
    }
    return {
        "overall": metrics,
        "by_category": category_metrics,
        "question_comparison": question_comparison,
        "first_relevant_ranks_6_to_10": low_rank,
    }


def _write_outputs(output_dir: Path, metadata: dict[str, Any], results: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "retrieval_evaluation_results.json"
    csv_path = output_dir / "retrieval_evaluation_question_results.csv"
    output = {**metadata, "summary": summarize(results), "results": results}
    try:
        result_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        with csv_path.open("w", encoding="utf-8", newline="") as stream:
            fieldnames = [
                "question_id",
                "question_type",
                "strategy",
                "question",
                "gold_references",
                "retrieved_results",
                "first_relevant_rank",
                "reciprocal_rank",
                "hit_at_3",
                "hit_at_5",
                "hit_at_10",
            ]
            writer = csv.DictWriter(stream, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(
                    {
                        **result,
                        "gold_references": json.dumps(
                            result["gold_references"], ensure_ascii=False
                        ),
                        "retrieved_results": json.dumps(
                            result["retrieved_results"], ensure_ascii=False
                        ),
                    }
                )
    except OSError as exc:
        raise EvaluationError(f"Cannot write evaluation outputs to {output_dir}: {exc}") from exc


def run_evaluation(
    dataset_path: Path = DEFAULT_DATASET,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    storage_dir: Path = QDRANT_STORAGE_DIR,
) -> dict[str, Any]:
    questions = _read_dataset(Path(dataset_path))
    if len(questions) != 25:
        raise EvaluationError(f"Expected 25 evaluation questions, found {len(questions)}.")
    question_ids = [record.get("question_id") for record in questions]
    if question_ids != [f"Q{number:03d}" for number in range(1, 26)]:
        raise EvaluationError("Question IDs must be sequential from Q001 to Q025.")

    results: list[dict[str, Any]] = []
    for question in questions:
        query_vector = search.embed_query(question["question"])
        for strategy in STRATEGIES:
            retrieved = search.retrieve(
                question["question"],
                top_k=TOP_K,
                strategy=strategy,
                filters=None,
                query_vector=query_vector,
                storage_dir=Path(storage_dir),
            )
            if len(retrieved) > TOP_K:
                raise EvaluationError(
                    f"{question['question_id']} {strategy} returned more than {TOP_K} results."
                )
            results.append(_result_record(question, strategy, retrieved))

    metadata = {
        "dataset_path": str(Path(dataset_path).resolve()),
        "question_count": len(questions),
        "query_evaluation_count": len(results),
        "top_k": TOP_K,
        "strategies": {
            strategy: search.STRATEGY_COLLECTIONS[strategy]
            for strategy in STRATEGIES
        },
        "embedding_model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "embedding_device": DEVICE,
        "normalized_embeddings": True,
        "query_prompt": None,
        "distance_metric": "cosine",
        "query_embeddings_generated": len(questions),
        "page_convention": "1-based PDF page numbers from page_provenance or inclusive page_start/page_end",
        "filters": None,
    }
    _write_outputs(Path(output_dir), metadata, results)
    return {**metadata, "summary": summarize(results)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate PolicyLens retrieval using gold document/page references."
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--storage-dir", type=Path, default=QDRANT_STORAGE_DIR)
    args = parser.parse_args(argv)
    try:
        result = run_evaluation(args.dataset, args.output_dir, args.storage_dir)
    except (EvaluationError, search.SearchError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
evaluate.py — Retrieval evaluation metrics for PolicyLens.

Metrics to be computed (to be implemented in later milestones):
  - Recall@3   : fraction of questions where gold chunk appears in top 3
  - Recall@5   : fraction of questions where gold chunk appears in top 5
  - Recall@10  : fraction of questions where gold chunk appears in top 10
  - MRR        : Mean Reciprocal Rank across all questions

Evaluation workflow:
  1. Load questions from eval/questions.csv.
  2. For each question, call search.retrieve() with top_k = 10.
  3. Check whether the gold_document / gold_page appears in the retrieved set.
  4. Compute and log all metrics.
  5. Write a timestamped report to reports/.

Planned evaluation data:
  - questions.csv contains hand-labelled question–answer pairs.
  - Each row has a gold_document (doc_id) and gold_page so ground truth can be
    checked at the chunk level.
  - No synthetic or auto-generated answers are used.
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.config import QUESTIONS_PATH, RECALL_K_VALUES, REPORTS_DIR

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API (stubs — to be implemented)
# ---------------------------------------------------------------------------

def recall_at_k(retrieved_doc_ids: list[str], gold_doc_id: str, k: int) -> float:
    """Return 1.0 if gold_doc_id appears in the first k results, else 0.0.

    Parameters
    ----------
    retrieved_doc_ids:
        Ordered list of doc_ids returned by the retrieval system.
    gold_doc_id:
        The correct document id from questions.csv.
    k:
        Cut-off rank.
    """
    raise NotImplementedError("recall_at_k will be implemented in Milestone 4.")


def reciprocal_rank(retrieved_doc_ids: list[str], gold_doc_id: str) -> float:
    """Return 1/rank if gold_doc_id is found, else 0.0.

    Parameters
    ----------
    retrieved_doc_ids:
        Ordered list of doc_ids returned by the retrieval system.
    gold_doc_id:
        The correct document id from questions.csv.
    """
    raise NotImplementedError("reciprocal_rank will be implemented in Milestone 4.")


def run_evaluation(
    questions_path: Path = QUESTIONS_PATH,
    report_dir: Path = REPORTS_DIR,
) -> dict:
    """Run the full retrieval evaluation over all labelled questions.

    Parameters
    ----------
    questions_path:
        Path to eval/questions.csv.
    report_dir:
        Directory where the timestamped JSON report is written.

    Returns
    -------
    dict
        Keys: ``"recall@3"``, ``"recall@5"``, ``"recall@10"``, ``"mrr"``.
    """
    raise NotImplementedError("run_evaluation will be implemented in Milestone 4.")

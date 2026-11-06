"""
chunking.py — Text chunking strategies for PolicyLens.

Two strategies are planned (to be implemented in later milestones):

1. Fixed-size chunking with overlap
   - Split text into windows of CHUNK_MAX_TOKENS tokens.
   - Slide by (CHUNK_MAX_TOKENS - CHUNK_OVERLAP_TOKENS) tokens per step.
   - Guarantees every chunk is within [CHUNK_MIN_TOKENS, CHUNK_MAX_TOKENS].

2. Structure-aware chunking
   - Detect section headings, paragraph breaks, and table boundaries.
   - Create chunks that respect document structure (no heading orphans).
   - Falls back to fixed-size splitting for oversized sections.

Both strategies attach the same metadata envelope to every chunk so that
downstream retrieval and evaluation code is strategy-agnostic.

Chunk metadata fields:
  chunk_id, doc_id, title, issuer, issue_date,
  page_start, page_end, section_title, source_hash,
  token_count, strategy
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from src.config import (
    CHUNK_MAX_TOKENS,
    CHUNK_MIN_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    CHUNKING_STRATEGY,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    """A single text chunk with its metadata envelope."""

    chunk_id: str           # e.g. "doc_001_chunk_0042"
    doc_id: str
    title: str
    issuer: str
    issue_date: str         # ISO-8601 string, e.g. "2023-04-01"
    page_start: int         # 1-based
    page_end: int           # 1-based
    section_title: str
    source_hash: str        # SHA-256 of the source PDF
    token_count: int
    strategy: str           # "fixed" | "structure_aware"
    text: str
    extra: dict = field(default_factory=dict)  # for future metadata fields


# ---------------------------------------------------------------------------
# Public API (stubs — to be implemented)
# ---------------------------------------------------------------------------

def fixed_size_chunks(
    pages: list[dict],
    doc_meta: dict,
    max_tokens: int = CHUNK_MAX_TOKENS,
    overlap_tokens: int = CHUNK_OVERLAP_TOKENS,
) -> list[Chunk]:
    """Split page text into fixed-size overlapping chunks.

    Parameters
    ----------
    pages:
        List of PageData dicts from extract.py.
    doc_meta:
        Document metadata row from manifest.csv (title, issuer, etc.).
    max_tokens:
        Target maximum tokens per chunk.
    overlap_tokens:
        Number of tokens to repeat between consecutive chunks.

    Returns
    -------
    list[Chunk]
        Chunks with strategy="fixed".
    """
    raise NotImplementedError("fixed_size_chunks will be implemented in Milestone 3.")


def structure_aware_chunks(
    pages: list[dict],
    doc_meta: dict,
    max_tokens: int = CHUNK_MAX_TOKENS,
) -> list[Chunk]:
    """Split page text into chunks that respect document structure.

    Parameters
    ----------
    pages:
        List of PageData dicts from extract.py.
    doc_meta:
        Document metadata row from manifest.csv.
    max_tokens:
        Maximum tokens per chunk before forced splitting.

    Returns
    -------
    list[Chunk]
        Chunks with strategy="structure_aware".
    """
    raise NotImplementedError(
        "structure_aware_chunks will be implemented in Milestone 3."
    )


def chunk_document(pages: list[dict], doc_meta: dict) -> list[Chunk]:
    """Dispatch to the configured chunking strategy.

    Reads ``CHUNKING_STRATEGY`` from config to decide which function to call.
    Swapping the strategy requires only changing the environment variable.

    Parameters
    ----------
    pages:
        List of PageData dicts from extract.py.
    doc_meta:
        Document metadata row from manifest.csv.
    """
    if CHUNKING_STRATEGY == "fixed":
        return fixed_size_chunks(pages, doc_meta)
    elif CHUNKING_STRATEGY == "structure_aware":
        return structure_aware_chunks(pages, doc_meta)
    else:
        raise ValueError(
            f"Unknown CHUNKING_STRATEGY '{CHUNKING_STRATEGY}'. "
            "Valid options: 'fixed', 'structure_aware'."
        )

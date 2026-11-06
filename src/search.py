"""
search.py — Vector-store retrieval via ChromaDB.

Responsibilities (to be implemented in later milestones):
  1. Connect to (or create) a ChromaDB collection backed by VECTOR_STORE_DIR.
  2. Index a list of Chunk objects: embed text, upsert vectors + metadata.
  3. Query the collection by embedding a user question and returning the top-k
     most similar chunks with their metadata.
  4. Provide a deduplication guard so re-indexing the same chunk_id is a no-op.

The vector-store backend is isolated behind this module. Swapping ChromaDB for
another backend (e.g. FAISS, Pinecone) requires changes only here.
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.config import (
    CHROMA_COLLECTION_NAME,
    RETRIEVE_TOP_K,
    VECTOR_STORE_DIR,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API (stubs — to be implemented)
# ---------------------------------------------------------------------------

def get_collection():
    """Return (or create) the ChromaDB collection for policy chunks.

    Uses a persistent client so the vector store survives process restarts.
    The collection is stored under VECTOR_STORE_DIR.

    Returns
    -------
    chromadb.Collection
        The named collection ready for upsert / query.
    """
    raise NotImplementedError("get_collection will be implemented in Milestone 3.")


def index_chunks(chunks: list) -> int:
    """Embed and upsert a list of Chunk objects into the vector store.

    Already-indexed chunk_ids are skipped (idempotent).

    Parameters
    ----------
    chunks:
        List of ``Chunk`` dataclass instances from chunking.py.

    Returns
    -------
    int
        Number of new chunks actually written (skipped ones excluded).
    """
    raise NotImplementedError("index_chunks will be implemented in Milestone 3.")


def retrieve(query: str, top_k: int = RETRIEVE_TOP_K) -> list[dict]:
    """Retrieve the top-k most relevant chunks for a query.

    Parameters
    ----------
    query:
        Free-text search question.
    top_k:
        Number of results to return.

    Returns
    -------
    list[dict]
        Each dict contains chunk metadata and a ``score`` key (cosine
        similarity, higher is better).
    """
    raise NotImplementedError("retrieve will be implemented in Milestone 3.")

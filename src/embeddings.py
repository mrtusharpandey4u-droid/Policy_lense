"""
embeddings.py — Sentence-Transformer embedding helpers.

Responsibilities (to be implemented in later milestones):
  1. Load a sentence-transformers model from EMBEDDING_MODEL config.
  2. Encode a list of text strings into float32 numpy arrays.
  3. Provide a batch-encoding helper with progress reporting.
  4. Cache the loaded model so it is not reloaded for every call.

The embedding backend is intentionally isolated behind this module so that
swapping from sentence-transformers to another provider (e.g. a hosted API)
requires changes only here.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.config import EMBEDDING_MODEL

if TYPE_CHECKING:
    import numpy as np  # only needed for type hints

logger = logging.getLogger(__name__)

# Module-level model cache — avoids reloading the model on every call.
_model = None


def get_model():
    """Return the loaded SentenceTransformer model (cached after first call).

    The model name is read from ``EMBEDDING_MODEL`` in config.py so it can be
    changed via the ``.env`` file without touching this module.

    Returns
    -------
    SentenceTransformer
        A loaded model ready for encoding.
    """
    raise NotImplementedError("get_model will be implemented in Milestone 3.")


def embed_texts(texts: list[str], batch_size: int = 32) -> "np.ndarray":
    """Encode a list of strings into embedding vectors.

    Parameters
    ----------
    texts:
        Input strings to embed.
    batch_size:
        Number of strings to encode per forward pass.

    Returns
    -------
    np.ndarray
        Shape ``(len(texts), embedding_dim)`` float32 array.
    """
    raise NotImplementedError("embed_texts will be implemented in Milestone 3.")


def embed_query(query: str) -> "np.ndarray":
    """Encode a single query string into an embedding vector.

    Parameters
    ----------
    query:
        The search query text.

    Returns
    -------
    np.ndarray
        Shape ``(embedding_dim,)`` float32 array.
    """
    raise NotImplementedError("embed_query will be implemented in Milestone 3.")

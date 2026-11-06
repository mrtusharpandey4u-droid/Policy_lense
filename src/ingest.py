"""
ingest.py — PDF ingestion and manifest management.

Responsibilities (to be implemented in later milestones):
  1. Read manifest.csv and identify PDFs pending download.
  2. Download each PDF from its URL with retry logic.
  3. Compute a SHA-256 hash of the raw bytes for deduplication.
  4. Validate that the file is a real PDF (magic bytes check).
  5. Update manifest.csv with page_count, source_hash, and download_status.
  6. Skip documents that are already present and hash-verified (idempotent run).

Deduplication guarantee: a second ingestion run must not create duplicate
records in the manifest or the vector store.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

# Placeholder imports — will be uncommented when dependencies are installed.
# import pandas as pd
# import fitz  # PyMuPDF
# import requests

from src.config import MANIFEST_PATH, PDF_DIR

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API (stubs — to be implemented)
# ---------------------------------------------------------------------------

def compute_sha256(file_path: Path) -> str:
    """Return the hex SHA-256 digest of a file.

    Parameters
    ----------
    file_path:
        Path to the file to hash.

    Returns
    -------
    str
        64-character lowercase hex string.
    """
    raise NotImplementedError("compute_sha256 will be implemented in Milestone 2.")


def download_pdf(url: str, dest_path: Path, timeout: int = 30) -> bool:
    """Download a PDF from *url* to *dest_path*.

    Parameters
    ----------
    url:
        Public URL of the policy document.
    dest_path:
        Local path where the file should be saved.
    timeout:
        Request timeout in seconds.

    Returns
    -------
    bool
        True if the download succeeded, False otherwise.
    """
    raise NotImplementedError("download_pdf will be implemented in Milestone 2.")


def ingest_manifest(manifest_path: Path = MANIFEST_PATH) -> None:
    """Read the manifest and download any PDFs not yet present locally.

    This function is idempotent — running it twice must not produce
    duplicate records.

    Parameters
    ----------
    manifest_path:
        Path to manifest.csv.
    """
    raise NotImplementedError("ingest_manifest will be implemented in Milestone 2.")

"""
config.py — Centralised configuration for PolicyLens.

All project-wide settings are read from environment variables (via .env)
so that the technology stack can be swapped without touching pipeline code.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Base paths — everything is relative to the project root so the project is
# portable across machines.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

# ---------------------------------------------------------------------------
# Directory paths
# ---------------------------------------------------------------------------
DATA_DIR        = PROJECT_ROOT / "data"
PDF_DIR         = DATA_DIR / "pdfs"
PROCESSED_DIR   = DATA_DIR / "processed"
EVAL_DIR        = PROJECT_ROOT / "eval"
LOGS_DIR        = PROJECT_ROOT / "logs"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"
REPORTS_DIR     = PROJECT_ROOT / "reports"

MANIFEST_PATH   = DATA_DIR / "manifest.csv"
QUESTIONS_PATH  = EVAL_DIR / "questions.csv"

# ---------------------------------------------------------------------------
# Chunking settings
# ---------------------------------------------------------------------------
CHUNK_MIN_TOKENS: int = int(os.getenv("CHUNK_MIN_TOKENS", "300"))
CHUNK_MAX_TOKENS: int = int(os.getenv("CHUNK_MAX_TOKENS", "800"))
CHUNK_OVERLAP_TOKENS: int = int(os.getenv("CHUNK_OVERLAP_TOKENS", "50"))

# Chunking strategy: "fixed" | "structure_aware"
CHUNKING_STRATEGY: str = os.getenv("CHUNKING_STRATEGY", "fixed")

# ---------------------------------------------------------------------------
# Embedding settings
# ---------------------------------------------------------------------------
EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL", "all-MiniLM-L6-v2"
)  # any sentence-transformers model name

# ---------------------------------------------------------------------------
# Vector store settings
# ---------------------------------------------------------------------------
VECTOR_STORE_BACKEND: str = os.getenv("VECTOR_STORE_BACKEND", "chromadb")
CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "policy_chunks")

# ---------------------------------------------------------------------------
# OCR settings
# ---------------------------------------------------------------------------
TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", "tesseract")  # path or command name
OCR_LANGUAGE: str = os.getenv("OCR_LANGUAGE", "eng")

# ---------------------------------------------------------------------------
# Retrieval / evaluation settings
# ---------------------------------------------------------------------------
RETRIEVE_TOP_K: int = int(os.getenv("RETRIEVE_TOP_K", "10"))
RECALL_K_VALUES: list[int] = [3, 5, 10]  # Recall@k values to report

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: Path = LOGS_DIR / "policylens.log"


def ensure_dirs() -> None:
    """Create all required directories if they do not already exist."""
    for d in [PDF_DIR, PROCESSED_DIR, EVAL_DIR, LOGS_DIR, VECTOR_STORE_DIR, REPORTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

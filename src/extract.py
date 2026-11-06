"""
extract.py — PDF text and table extraction.

Responsibilities (to be implemented in later milestones):
  1. Open a PDF with PyMuPDF (fitz).
  2. For each page, detect whether it is text-native or scanned.
  3. Extract text from text-native pages using PyMuPDF's getText().
  4. Run Tesseract OCR on scanned / image-only pages.
  5. Detect and extract tables (two-column layouts, structured grids).
  6. Return a list of per-page dictionaries ready for chunking.

Document categories to handle:
  - ~60 % text-native PDFs
  - ~20 % scanned (OCR required)
  - ~20 % containing important tables
  - At least 2 two-column layout PDFs
  - At least 3 PDFs longer than 50 pages
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TypedDict

from src.config import OCR_LANGUAGE, TESSERACT_CMD

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class PageData(TypedDict):
    """Structured output for a single extracted page."""

    doc_id: str
    page_number: int          # 1-based
    text: str                 # Extracted / OCR'd text
    is_ocr: bool              # True if Tesseract was used
    has_table: bool           # True if a table was detected
    layout_columns: int       # Estimated number of text columns


# ---------------------------------------------------------------------------
# Public API (stubs — to be implemented)
# ---------------------------------------------------------------------------

def is_scanned_page(page) -> bool:  # page: fitz.Page
    """Return True if the page has no selectable text (image-only).

    Parameters
    ----------
    page:
        A PyMuPDF Page object.
    """
    raise NotImplementedError("is_scanned_page will be implemented in Milestone 2.")


def extract_page_text(page, doc_id: str, page_number: int) -> PageData:
    """Extract text from a single PyMuPDF page, using OCR if necessary.

    Parameters
    ----------
    page:
        A PyMuPDF Page object.
    doc_id:
        Identifier from manifest.csv (e.g. ``"doc_001"``).
    page_number:
        1-based page index.
    """
    raise NotImplementedError("extract_page_text will be implemented in Milestone 2.")


def extract_pdf(pdf_path: Path, doc_id: str) -> list[PageData]:
    """Extract all pages from a PDF file.

    Parameters
    ----------
    pdf_path:
        Path to the PDF file.
    doc_id:
        Identifier from manifest.csv.

    Returns
    -------
    list[PageData]
        One entry per page in reading order.
    """
    raise NotImplementedError("extract_pdf will be implemented in Milestone 2.")

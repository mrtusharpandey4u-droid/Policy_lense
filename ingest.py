#!/usr/bin/env python3
"""
ingest.py — Root-level CLI entrypoint for PolicyLens PDF Ingestion.

Supports the assignment command:
    python ingest.py --input data/pdfs --manifest data/manifest.csv --collection policylens_v1
"""

import sys
from pathlib import Path

# Ensure project root and src/ are in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingest import main

if __name__ == "__main__":
    sys.exit(main())

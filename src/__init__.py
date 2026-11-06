"""
PolicyLens — src package.

This package contains all pipeline modules:
  config     – centralised settings and environment loading
  ingest     – PDF download, validation, and manifest management
  chunking   – fixed-size and structure-aware text chunking strategies
  embeddings – sentence-transformer embedding helpers
  search     – vector-store retrieval (ChromaDB)
  extract    – PDF text and table extraction (PyMuPDF + Tesseract OCR)
  evaluate   – retrieval evaluation metrics (Recall@k, MRR)
"""

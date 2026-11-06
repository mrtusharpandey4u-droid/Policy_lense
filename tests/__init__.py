"""
tests/ — PolicyLens pytest test suite.

Test modules to be added in later milestones:

  test_config.py       – verify all config values load from env correctly
  test_ingest.py       – SHA-256 hashing, download stub, deduplication
  test_extract.py      – page extraction, OCR fallback detection
  test_chunking.py     – fixed-size chunk sizes/overlap, structure-aware splits
  test_embeddings.py   – embed_texts output shape and dtype
  test_search.py       – index → retrieve round-trip, idempotency
  test_evaluate.py     – recall_at_k, reciprocal_rank unit tests
"""

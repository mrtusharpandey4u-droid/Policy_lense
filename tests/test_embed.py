import json
from pathlib import Path

import numpy as np
import pytest

import src.embed as embed


class _FakeMps:
    @staticmethod
    def synchronize() -> None:
        return None

    @staticmethod
    def driver_allocated_memory() -> int:
        return 1234


class _FakeTorch:
    mps = _FakeMps()


class _FakeModel:
    device = "mps:0"

    def __init__(self, fail_on_call: int | None = None) -> None:
        self.calls = 0
        self.fail_on_call = fail_on_call

    def encode(self, texts, **kwargs):
        assert len(texts) == 1
        assert kwargs["batch_size"] == 1
        assert kwargs["normalize_embeddings"] is True
        self.calls += 1
        if self.calls == self.fail_on_call:
            raise RuntimeError("simulated transient failure")
        vector = np.zeros(embed.EMBEDDING_DIMENSIONS, dtype=np.float32)
        vector[0] = 1.0
        return vector.reshape(1, -1)


@pytest.fixture(autouse=True)
def fake_mps(monkeypatch):
    monkeypatch.setattr(embed, "_require_mps", lambda: _FakeTorch())


def _chunk(strategy: str, index: int, text: str | None = None) -> dict:
    return {
        "chunk_id": f"doc_{strategy}_{index:03d}",
        "doc_id": "doc_test",
        "title": "Test Policy",
        "issuer": "Test Regulator",
        "issue_date": "2025-01-02",
        "page_start": index,
        "page_end": index + 1,
        "section_title": "Lending",
        "source_hash": "source-hash",
        "chunking_strategy": strategy,
        "chunk_index": index,
        "text": text if text is not None else f"Policy text {index}",
        "token_count": 3,
        "content_type": "text",
        "tables": [],
        "page_provenance": [
            {
                "page_number": index,
                "text_source": "ocr",
                "cleaning_review": True,
                "review_reasons": ["OCR review"],
                "ocr_provenance": {"language": "eng+hin"},
            }
        ],
        "contains_ocr": True,
        "has_cleaning_review": True,
        "review_pages": [index],
        "is_continuation": False,
        "exceeds_target_size": False,
    }


def _write_chunks(path: Path, strategy: str, count: int = 2) -> list[dict]:
    records = [_chunk(strategy, index + 1) for index in range(count)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    return records


def test_validate_embedding_requires_dimension_finite_nonzero_and_normalized():
    vector = [0.0] * embed.EMBEDDING_DIMENSIONS
    vector[0] = 1.0
    assert embed.validate_embedding(vector) == vector

    with pytest.raises(embed.EmbeddingError, match="Expected 1024"):
        embed.validate_embedding([1.0])
    with pytest.raises(embed.EmbeddingError, match="NaN or infinity"):
        embed.validate_embedding([float("nan")] + [0.0] * 1023)
    with pytest.raises(embed.EmbeddingError, match="all-zero"):
        embed.validate_embedding([0.0] * 1024)
    with pytest.raises(embed.EmbeddingError, match="outside tolerance"):
        embed.validate_embedding([0.5] + [0.0] * 1023)


@pytest.mark.parametrize("strategy", ["fixed_size", "structure_aware"])
def test_embedding_preserves_metadata_and_records_model_revision(tmp_path, strategy):
    input_path = tmp_path / f"{strategy}.jsonl"
    output_path = tmp_path / "embeddings" / f"{strategy}.jsonl"
    source = _write_chunks(input_path, strategy)[0]

    result = embed.embed_strategy(input_path, output_path, _FakeModel())
    output = json.loads(output_path.read_text(encoding="utf-8").splitlines()[0])

    for key, value in source.items():
        assert output[key] == value
    assert output["embedding_dimensions"] == 1024
    assert output["embedding_model"] == embed.MODEL_NAME
    assert output["model_revision"] == embed.MODEL_REVISION
    assert output["normalized"] is True
    assert output["embedding_status"] == "completed"
    assert output["source_chunk_id"] == source["chunk_id"]
    assert output["chunking_strategy"] == strategy
    assert len(output["embedding"]) == 1024
    assert result["embedded_this_run"] == 2
    assert embed.validate_strategy_output(input_path, output_path)["missing_source_chunks"] == 0


def test_interrupted_run_resumes_without_regenerating_completed_chunks(tmp_path):
    input_path = tmp_path / "fixed_size.jsonl"
    output_path = tmp_path / "out" / "fixed_size.jsonl"
    _write_chunks(input_path, "fixed_size", count=3)
    model = _FakeModel(fail_on_call=2)

    with pytest.raises(embed.EmbeddingError, match="completed records are preserved"):
        embed.embed_strategy(input_path, output_path, model)
    assert len(output_path.read_text(encoding="utf-8").splitlines()) == 1

    resumed = embed.embed_strategy(input_path, output_path, _FakeModel())
    assert resumed["embedded_this_run"] == 2
    assert resumed["skipped_valid_on_resume"] == 1
    assert resumed["completed_embeddings"] == 3
    assert len(output_path.read_text(encoding="utf-8").splitlines()) == 3
    assert embed.validate_strategy_output(input_path, output_path)["embedding_records"] == 3


def test_resume_repairs_only_an_incomplete_last_line(tmp_path):
    input_path = tmp_path / "fixed_size.jsonl"
    output_path = tmp_path / "out" / "fixed_size.jsonl"
    _write_chunks(input_path, "fixed_size", count=2)
    embed.embed_strategy(input_path, output_path, _FakeModel())
    with output_path.open("ab") as output_file:
        output_file.write(b'{"interrupted":')

    resumed = embed.embed_strategy(input_path, output_path, _FakeModel())
    assert resumed["discarded_incomplete_tail_bytes"] == len(b'{"interrupted":')
    assert resumed["embedded_this_run"] == 0
    assert resumed["skipped_valid_on_resume"] == 2
    assert len(output_path.read_text(encoding="utf-8").splitlines()) == 2


def test_changed_input_hash_is_rejected_for_existing_output(tmp_path):
    input_path = tmp_path / "fixed_size.jsonl"
    output_path = tmp_path / "out" / "fixed_size.jsonl"
    records = _write_chunks(input_path, "fixed_size", count=1)
    embed.embed_strategy(input_path, output_path, _FakeModel())
    records[0]["text"] += " changed"
    input_path.write_text(json.dumps(records[0]) + "\n", encoding="utf-8")

    with pytest.raises(embed.EmbeddingError, match="Input/model/configuration changed"):
        embed.embed_strategy(input_path, output_path, _FakeModel())


def test_duplicate_ids_and_empty_text_are_reported_not_skipped(tmp_path):
    duplicate_path = tmp_path / "fixed_size.jsonl"
    records = [_chunk("fixed_size", 1), _chunk("fixed_size", 1)]
    duplicate_path.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )
    with pytest.raises(embed.EmbeddingError, match="duplicate chunk_id"):
        embed._source_inventory(duplicate_path, "fixed_size")

    empty_path = tmp_path / "structure_aware.jsonl"
    _write_chunks(empty_path, "structure_aware", count=1)
    record = _chunk("structure_aware", 1, text="   ")
    empty_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(embed.EmbeddingError, match="empty or invalid text"):
        embed._source_inventory(empty_path, "structure_aware")


def test_duplicate_embedding_records_are_rejected(tmp_path):
    input_path = tmp_path / "fixed_size.jsonl"
    output_path = tmp_path / "out" / "fixed_size.jsonl"
    _write_chunks(input_path, "fixed_size", count=1)
    embed.embed_strategy(input_path, output_path, _FakeModel())
    completed_record = output_path.read_text(encoding="utf-8")
    with output_path.open("a", encoding="utf-8") as output_file:
        output_file.write(completed_record)

    with pytest.raises(embed.EmbeddingError, match="Duplicate embedding record"):
        embed.embed_strategy(input_path, output_path, _FakeModel())


def test_output_record_source_hash_covers_all_original_metadata(tmp_path):
    input_path = tmp_path / "fixed_size.jsonl"
    output_path = tmp_path / "out" / "fixed_size.jsonl"
    source = _write_chunks(input_path, "fixed_size", count=1)[0]
    embed.embed_strategy(input_path, output_path, _FakeModel())

    record = json.loads(output_path.read_text(encoding="utf-8"))
    record["page_provenance"][0]["review_reasons"] = ["changed"]
    output_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(embed.EmbeddingError, match="Source metadata/text changed"):
        embed.validate_strategy_output(input_path, output_path)
    assert source["page_provenance"][0]["review_reasons"] == ["OCR review"]


def test_model_device_must_be_mps(tmp_path):
    input_path = tmp_path / "fixed_size.jsonl"
    output_path = tmp_path / "out" / "fixed_size.jsonl"
    _write_chunks(input_path, "fixed_size", count=1)

    class CpuModel(_FakeModel):
        device = "cpu"

    with pytest.raises(embed.EmbeddingError, match="expected mps"):
        embed.embed_strategy(input_path, output_path, CpuModel())


def test_both_strategy_corpus_uses_separate_outputs(tmp_path):
    inputs = tmp_path / "chunks"
    outputs = tmp_path / "embeddings"
    _write_chunks(inputs / "fixed_size.jsonl", "fixed_size", count=1)
    _write_chunks(inputs / "structure_aware.jsonl", "structure_aware", count=1)

    summary = embed.embed_corpus(inputs, outputs, model=_FakeModel())
    assert set(summary["strategies"]) == {"fixed_size", "structure_aware"}
    assert summary["validation"]["fixed_size"]["embedding_records"] == 1
    assert summary["validation"]["structure_aware"]["embedding_records"] == 1
    assert (outputs / "fixed_size.jsonl").is_file()
    assert (outputs / "structure_aware.jsonl").is_file()

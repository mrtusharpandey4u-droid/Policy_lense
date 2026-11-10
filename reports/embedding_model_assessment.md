# Milestone 2B.8 — Embedding Model Assessment and Selection

**Assessment date:** 2026-11-09

## Executive Summary

**Primary candidate: `BAAI/bge-m3`, run locally.** Its multilingual coverage,
1024-dimensional dense vector, and 8192-token input limit suit the existing
English/Hindi chunks without truncation. Local execution avoids per-request
fees and transmitting public-policy text to an API. This recommendation is
conditional on providing local compute and must be confirmed by retrieval
evaluation on PolicyLens questions; no model was run or benchmarked for
PolicyLens relevance in this assessment.

**Alternative: OpenAI `text-embedding-3-small`, hosted.** It also fits every
current chunk, has a low published input price, and avoids managing model
weights and local inference. Use only if an API account is available and the
project's data-handling rules permit sending document text to the provider.
No credentials were inspected and no API request was made.

The local `intfloat/multilingual-e5-large` candidate is multilingual, but its
512-token input length is a poor match for the current chunks: **62.55%** of
fixed-size chunks and **40.60%** of structure-aware chunks exceed that limit.
Do not embed with default truncation without first revising chunking or
explicitly handling long chunks.

## Project Inputs Inspected

- `requirements.txt` already declares `sentence-transformers` and `torch`;
  neither `sentence_transformers`, `torch`, nor model-tokenizer libraries
  were installed in the project's `.venv` at assessment time.
- `src/config.py` still defaults `EMBEDDING_MODEL` to `all-MiniLM-L6-v2`.
  That existing value was not changed; the assessment below focuses on
  multilingual candidates appropriate to the Hindi-containing corpus.
- `src/chunk.py` defines the current lexical tokenizer as
  `\w+|[^\w\s]` (Unicode word/number runs plus individual punctuation).
  Chunk configuration defaults to 500 lexical tokens with 50-token overlap
  and a preferred 300–800 range.
- The generated files are `data/processed/chunks/fixed_size.jsonl`
  (**1,370** records) and `data/processed/chunks/structure_aware.jsonl`
  (**1,478** records).
- Each record has `text`, lexical `token_count`, `content_type`, `doc_id`,
  source/title/issuer/date fields, page range, `section_title`,
  `chunking_strategy`, table data, and OCR/review metadata including
  `contains_ocr`, `has_cleaning_review`, `review_pages`, and
  `page_provenance`.
- Table chunks' `text` is the pipe-delimited rendering used for chunking;
  structured table rows remain separately available in `tables`. Token
  comparisons below use each record's `text`, not its metadata or serialized
  `tables` object.

## Candidate Comparison

| Model | Runtime / dimensions | Language and retrieval fit | Input context | Estimated cost per 1,000 chunk inputs | Advantages | Disadvantages |
|---|---|---|---:|---:|---|---|
| **BAAI/bge-m3** | Local Hugging Face model; 1,024 dimensions | Model card reports more than 100 working languages; includes multilingual dense retrieval. Good candidate for mixed English/Hindi policy text. | 8,192 tokens | **$0 provider fee**; local hardware, energy, and setup are additional and not estimated. | Fits all current chunks; avoids sending text to a third party; no API rate limit or per-token charge; one model supports dense, sparse, and multi-vector modes, though this assessment concerns dense embeddings only. MIT-licensed model card. | Approximately 2.27 GB FP32 checkpoint weights before runtime/activation memory; requires downloading model weights before implementation. CPU inference may be slow. Hardware cost and throughput were not measured. |
| **intfloat/multilingual-e5-large** | Local Hugging Face model; 1,024 dimensions | Model card reports support for 100 XLM-R languages, including Hindi coverage through that multilingual base. Passage embeddings should use the `passage: ` prefix. | 512 tokens (model-card inference setting) | **$0 provider fee**; local hardware, energy, and setup are additional and not estimated. | MIT license; multilingual; local/private execution; model card gives a clear passage/query usage convention. Approximately 2.24 GB FP32 checkpoint weights before runtime/activation memory. | 512-token input limit is materially shorter than current chunks: 857 fixed-size and 600 structure-aware chunks exceed it after the required passage prefix. Default truncation could discard meaningful text and table values. |
| **OpenAI `text-embedding-3-small`** | Hosted OpenAI embeddings API; 1,536 dimensions by default (API supports a dimensions option) | Multilingual retrieval is supported; OpenAI reports results on the multilingual MIRACL benchmark. This is general benchmark evidence, not lending-compliance validation. | 8,192 tokens | **About $0.0102** fixed-size or **$0.0087** structure-aware, using measured model-token counts and the published **$0.02 / 1M input tokens** rate. | Every current chunk fits; no local model-weight storage or inference runtime; low measured one-time corpus cost at the published rate. | Requires an API account/key and network access; sends chunk text to a hosted provider; tier-dependent rate limits; hosted alias introduces an external dependency. No key was assumed or used. |

**Cost assumptions:** Figures are provider charges for one embedding pass over
1,000 chunks of the indicated strategy, excluding retries, query embeddings,
taxes, discounts, storage, and any local infrastructure. The OpenAI estimate
uses the measured mean of 507.78 model tokens per fixed-size chunk and 437.18
per structure-aware chunk. The two strategies are alternatives; embedding
both for a comparison incurs the cost of each set. Local “$0” means no
per-request provider charge, not zero total operating cost.

**Hardware estimate:** Public Hugging Face repository metadata lists one
FP32 checkpoint of 2,271,145,830 bytes for BGE-M3 and 2,239,611,368 bytes
for E5-large. This is checkpoint size, not a measured runtime minimum.
Budget additional memory for the framework, activations, batching, and the
operating system. The model weights were not downloaded, and inference speed
was not tested.

**Rate limits:** OpenAI's current model page lists tier-dependent API limits;
the listed Free tier is 100 requests/minute and 40,000 tokens/minute, with
higher tiers available. Actual limits depend on the account and can change.
Batching, retries, and rate-limit handling would be required in a future
implementation. No hosted request was made.

## Actual Tokenizer Validation

The existing lexical `token_count` was compared with each candidate's
tokenizer for every chunk in both outputs:

- BGE-M3: Hugging Face `tokenizer.json`, with special tokens enabled.
- Multilingual E5-large: its Hugging Face `tokenizer.json`, with the model's
  required `passage: ` prefix and special tokens enabled.
- OpenAI text-embedding-3-small: `cl100k_base` via `tiktoken`, the encoding
  mapped to that model.

Only public tokenizer assets were retrieved; **no embedding model weights
were downloaded, no chunk text was sent externally, and no paid API or
embedding endpoint was called**. Tokenizer packages were installed into a
temporary, isolated assessment directory and were not added to project
dependencies. Tokenization was run with the available system Python 3.14.6
because the temporary `tiktoken` wheel was incompatible with the project's
Python 3.15.2 environment. The tokenizer assets and inputs were the actual
model and project files; no tokenizer validation result is inferred from
lexical counts.

Percentages below are over **all chunks**, including short standalone table
chunks. Counts in the 300–800 column use the model tokenizer's count, not the
stored lexical count.

### Fixed-size output — 1,370 chunks

| Count method | Minimum | Median | Mean | Maximum | Chunks at 300–800 | Percentage at 300–800 | Above model context |
|---|---:|---:|---:|---:|---:|---:|---:|
| Existing lexical counter | 3 | 500 | 405.94 | 1,107 | 1,052 | 76.79% | — |
| BGE-M3 tokenizer | 8 | 571 | 480.41 | 1,248 | 965 | 70.44% | 0 / 1,370 |
| Multilingual E5-large tokenizer, including passage prefix | 9 | 573 | 482.22 | 1,250 | 967 | 70.58% | **857 / 1,370 (62.55%)** |
| OpenAI tokenizer | 5 | 554 | 507.78 | 1,554 | 977 | 71.31% | 0 / 1,370 |

### Structure-aware output — 1,478 chunks

| Count method | Minimum | Median | Mean | Maximum | Chunks at 300–800 | Percentage at 300–800 | Above model context |
|---|---:|---:|---:|---:|---:|---:|---:|
| Existing lexical counter | 3 | 414.5 | 348.81 | 1,107 | 1,016 | 68.74% | — |
| BGE-M3 tokenizer | 7 | 468.5 | 412.58 | 1,233 | 983 | 66.51% | 0 / 1,478 |
| Multilingual E5-large tokenizer, including passage prefix | 9 | 470.5 | 414.40 | 1,235 | 987 | 66.78% | **600 / 1,478 (40.60%)** |
| OpenAI tokenizer | 4 | 477 | 437.18 | 1,524 | 1,010 | 68.34% | 0 / 1,478 |

No chunk exceeds the BGE-M3 or OpenAI context limit. For E5-large, the
over-limit counts mean the current input would need splitting or another
explicit strategy before inference; they must not be silently truncated.
Measured token counts also show that lexical counts are not interchangeable
with model-token counts. Under BGE-M3, 70.44% and 66.51% of the two sets fall
in the 300–800 range; OpenAI's figures are 71.31% and 68.34%. These sizes are
practical for both candidates, with no context-driven chunk adjustment
required.

The chunks flagged as OCR-containing are included in these counts. There
were 65 such fixed-size chunks and 72 structure-aware chunks; all fit the
BGE-M3 and OpenAI limits. E5's limit was exceeded by 35 OCR-containing
fixed-size chunks and 20 OCR-containing structure-aware chunks. Hindi and
English/Hindi support is supported by the model cards, but this count
validation does not measure Hindi embedding quality or OCR correctness.

## Recommendation and Next Validation

Select **BGE-M3 as the primary model candidate**, conditional on local memory
and acceptable CPU/GPU throughput. It is the strongest fit to the current
architecture when reproducibility, multilingual policy text, and keeping
document text local are priorities. Its context length accommodates all
existing fixed-size and structure-aware chunks, and its per-call provider
cost is zero. Pin a specific model revision and runtime/library versions in
any future implementation.

Keep **OpenAI text-embedding-3-small as the alternative** when local inference
capacity is insufficient and hosted processing is approved. It meets the
same context-fit requirement at a very small measured cost for this corpus.
Availability of an API account and approval to transmit source-derived text
remain prerequisites; neither was assumed.

Before implementation, evaluate the primary and alternative using the
project's labeled retrieval questions, with separate fixed-size and
structure-aware results. Include English, Hindi/bilingual OCR, table-heavy
documents, and exact numeric/regulatory queries. This milestone did not
create embeddings, call either model, compare retrieval metrics, select an
API account, or change chunking.

## Sources

Official model/provider sources checked on 2026-11-09:

1. [BAAI BGE-M3 model card](https://huggingface.co/BAAI/bge-m3) — 100+
   languages, 8,192-token length, 1,024 dimensions, and retrieval modes.
2. [BGE-M3 model repository metadata](https://huggingface.co/api/models/BAAI/bge-m3?blobs=true)
   — MIT license and published checkpoint file size.
3. [Multilingual E5-large model card](https://huggingface.co/intfloat/multilingual-e5-large)
   — 1,024 dimensions, 512-token inference example, passage prefix, and
   100-language coverage.
4. [E5 model repository metadata](https://huggingface.co/api/models/intfloat/multilingual-e5-large?blobs=true)
   — MIT license and checkpoint file sizes.
5. [OpenAI text-embedding-3-small model page](https://developers.openai.com/api/docs/models/text-embedding-3-small)
   — 1,536 default dimensions, 8,192 context, $0.02 / million-token pricing,
   and tier-dependent rate limits.
6. [OpenAI embedding guide](https://developers.openai.com/api/docs/guides/embeddings)
   and [embedding model announcement](https://openai.com/index/new-embedding-models-and-api-updates/)
   — dimensions controls and published multilingual benchmark context.
7. [OpenAI tiktoken repository](https://github.com/openai/tiktoken) and
   [cl100k tokenizer data](https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken)
   — tokenizer implementation and public encoding data.

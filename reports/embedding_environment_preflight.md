# Milestone 2B.9 — BGE-M3 Environment Preflight

**Assessment date:** 2026-11-09  
**Outcome: READY WITH LIMITATIONS**

The hardware and currently published Python wheels make local BGE-M3
implementation reasonable on this machine, preferably using Apple's MPS
backend. The project `.venv` currently has none of the required embedding
runtime packages installed, so neither MPS availability nor real inference
memory/throughput has been tested. Do not treat this preflight as an
embedding execution test.

## Environment Facts

| Item | Observed |
|---|---|
| Operating system | macOS 27.2 (Darwin 27.2.0) |
| Architecture / chip | `arm64`; MacBook Air, Apple M5 |
| Physical memory | 16 GiB unified memory |
| Current memory snapshot | `memory_pressure -Q` reported 65% system-wide free. This is a point-in-time OS figure, not a guarantee of memory available throughout inference. |
| Swap snapshot | `memory_pressure` reported zero swap-ins and zero swap-outs at inspection time. |
| Free disk | 358 GiB available on the workspace volume (`df -h`). |
| Project Python | `.venv/bin/python`, Python 3.15.2; the executable resolves inside this PolicyLens workspace's `.venv`. |
| Project pip | pip 26.3, running through `.venv/bin/python -m pip`. |

These are observations from this machine, not assumptions based on the base
Python installation. System `python3` is a different Python 3.14.6 and was
not used to report the project's interpreter or installed packages.

## Runtime and Compatibility

The following were **not installed** in `.venv` during inspection:

- `torch`
- `sentence-transformers`
- `transformers`
- `tokenizers`
- `safetensors`
- `accelerate`
- `numpy`
- `scipy`
- `scikit-learn`

`requirements.txt` already declares `sentence-transformers>=3.0.0` and
`torch>=2.2.0`, but declaring them does not mean they are installed in the
active environment.

Public package-index metadata was checked without installing or downloading
packages. At the time of this assessment it showed:

- PyTorch 2.15.0 publishes a regular-GIL Python 3.15 wheel for Apple Silicon:
  `macosx_14_0_arm64` (about 139 MB). Its `Requires-Python` is `>=3.11`.
- Sentence Transformers 6.2.0 is a universal Python wheel and requires
  Python `>=3.10`; it depends on PyTorch `>=2.2`, Transformers `>=5,<6`,
  Tokenizers `>=0.19`, NumPy, SciPy, and scikit-learn.
- Transformers 5.22.2 and the current NumPy, SciPy, and scikit-learn releases
  publish Python 3.15-compatible packages/wheels.
- Tokenizers 0.23.3 and safetensors 0.8.0 publish `cp310-abi3` Apple Silicon
  wheels, which are ABI-compatible with this regular-GIL CPython 3.15
  interpreter.

This indicates a compatible dependency route exists; it does not verify a
successful dependency resolution or runtime import in `.venv`. No packages
were installed as part of this assessment.

### Acceleration and CPU

The M5 Apple Silicon hardware and macOS version are suitable for PyTorch's
Metal Performance Shaders (MPS) backend. PyTorch's MPS documentation says to
confirm runtime support with `torch.backends.mps.is_available()` and
`torch.backends.mps.is_built()`. Since PyTorch is absent, those checks could
not be run. MPS support is therefore **hardware/package-compatible but not
yet runtime-verified**.

CPU inference is also available in principle through PyTorch on macOS ARM.
The estimated workload is modest for a one-time local corpus pass, but
CPU throughput was not benchmarked. It is not possible to promise a run time
or decide from this inspection alone whether CPU would feel slow. Prefer
MPS if the installed PyTorch build reports it available; retain CPU as a
fallback and use small batches.

## BGE-M3 Resource Estimate

| Resource | Assessment |
|---|---|
| Model download | Approximately 2.27 GB for the FP32 checkpoint, based on the public Hugging Face repository file metadata recorded in the prior model assessment. This is the weight file size, not the complete installed/cache footprint. |
| Runtime memory | **Estimate, not measured:** budget roughly 4–8 GB for the checkpoint plus framework, temporary tensors/activations, and a modest batch. Actual use depends on dtype, backend, sequence length, and batch size. A larger batch or long inputs can raise use substantially. |
| Available physical memory | 16 GiB unified memory; 65% free in the observed OS snapshot. The 4–8 GB estimate is within physical capacity, but other running applications share that memory. |
| Disk | 358 GiB free, ample for the checkpoint, environment packages, and cache. |
| Practicality | Reasonable to attempt locally with MPS and a conservative batch size. Confirm with a small smoke run, measure peak memory and throughput, and only then process the corpus. |

The BGE-M3 checkpoint is about 567 million FP32 parameters by the rough
calculation `2.27 GB / 4 bytes per parameter`; this is consistent with the
checkpoint-size estimate, not a separate runtime measurement. Reduced
precision may lower weight memory but has not been tested or assumed here.

## Corpus Workload

The existing `data/processed/chunks/chunking_summary.json` was read without
changing it. Its stored counts use the PolicyLens lexical tokenizer, not a
model tokenizer.

| Strategy | Chunks | Approx. total lexical tokens from recorded mean |
|---|---:|---:|
| Fixed-size | 1,370 | 556,000 |
| Structure-aware | 1,478 | 516,000 |
| Both alternative outputs, if each is embedded separately | 2,848 | 1,072,000 |

The previous model-tokenizer assessment measured approximately 658,000
BGE-M3 tokens for fixed-size chunks and 609,000 for structure-aware chunks
(about **1.27 million tokens** if embedding both alternatives). Each strategy
is a separate experiment; the normal workload would embed one strategy, not
both. All measured chunks were below BGE-M3's 8,192-token context limit.
The longest measured chunk was 1,248 BGE-M3 tokens for fixed-size and 1,233
for structure-aware.

At this scale, memory use is driven chiefly by model/runtime/batch rather
than by the total corpus token count, because chunks can be processed in
batches. MPS with small batches should be practical; larger batches may
increase throughput but need measurement against the shared 16 GiB memory.

## Recommendation

**READY WITH LIMITATIONS — proceed with a local BGE-M3 implementation only
after a small runtime smoke test.**

Reasons:

1. The machine is an Apple M5 Mac with 16 GiB unified memory and substantial
   free disk; these resources are compatible with the approximately 2.27 GB
   model checkpoint and a conservative inference setup.
2. Current package metadata provides a compatible PyTorch 2.15.0 wheel for
   Python 3.15 on Apple Silicon, plus compatible current dependencies.
3. MPS should be the preferred accelerator, but actual availability cannot be
   confirmed until PyTorch is installed and queried in `.venv`.
4. The total BGE token workload is approximately 0.61–0.66 million tokens
   for either chunking strategy, or 1.27 million if both are embedded for
   comparison. CPU-only processing may be feasible at that scale but its
   speed is unknown and should not be assumed adequate without benchmarking.
5. If the smoke test shows MPS unavailable or memory pressure is excessive,
   test CPU with a small batch before considering a smaller model or the
   hosted alternative. No model selection or implementation change is made
   here.

Before any corpus-wide embedding run, verify in the project environment:
`torch.__version__`, `torch.backends.mps.is_built()`,
`torch.backends.mps.is_available()`, a single representative BGE-M3
embedding, output dimension 1,024, peak memory, and measured throughput.
Keep batch size low initially and retain CPU fallback behavior.

## Restrictions and Validation

- No model weights were downloaded.
- No packages were installed.
- No embedding API, vector store, or model inference was invoked.
- No chunk outputs, source PDFs, manifest, or source code were modified.
- The chunk summary was read only.

## Sources

- Local system commands: `uname`, `sw_vers`, `sysctl hw.memsize`,
  `memory_pressure`, `vm_stat`, `df -h`, `.venv/bin/python`, and
  `.venv/bin/python -m pip`.
- [PyTorch MPS backend documentation](https://docs.pytorch.org/docs/2.15/notes/mps.html)
  — MPS runtime checks and device requirements.
- [PyPI torch metadata](https://pypi.org/project/torch/) and
  [sentence-transformers metadata](https://pypi.org/project/sentence-transformers/)
  — current Python requirements and available distributions.
- [Transformers metadata](https://pypi.org/project/transformers/),
  [Tokenizers metadata](https://pypi.org/project/tokenizers/),
  [safetensors metadata](https://pypi.org/project/safetensors/),
  [NumPy metadata](https://pypi.org/project/numpy/),
  [SciPy metadata](https://pypi.org/project/scipy/), and
  [scikit-learn metadata](https://pypi.org/project/scikit-learn/) — runtime
  dependency Python requirements and wheel compatibility.
- [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3) and its public
  [repository metadata](https://huggingface.co/api/models/BAAI/bge-m3?blobs=true)
  — model context, dimensions, and checkpoint file size.
- [Chunking summary](../data/processed/chunks/chunking_summary.json) and
  [prior tokenizer assessment](./embedding_model_assessment.md) — corpus
  workload and measured BGE-M3 token counts.

# PolicyLens — Chunking Strategy Comparison (Milestone 2B.17)

## Executive summary

The fixed-size strategy had higher question-level Recall@3, Recall@5, and MRR
on the 25-question Milestone 2B.16 evaluation; both strategies tied at
Recall@10. Fixed-size was better by reciprocal rank on 7 questions,
structure-aware on 4, tied on 13, and both missed Q010. These are descriptive
results, not evidence of statistical significance.

The comparison does **not** justify discarding structure-aware chunking:
structure-aware had higher MRR on the five paraphrased questions, several
individual questions ranked better, and both strategies preserved the same
structured table fragments. In addition, the page-overlap relevance rule
appears to over-credit some retrieved chunks that do not contain the
question's evidence text. **Recommendation: retain both strategies for further
evaluation, and improve evidence-level relevance checks before selecting a
primary strategy.**

## Methodology and sources

Read-only inputs:

- `data/evaluation/evaluation_questions.jsonl`
- `data/evaluation/results/retrieval_evaluation_results.json`
- `data/evaluation/results/retrieval_evaluation_question_results.csv`
- `data/processed/chunks/fixed_size.jsonl`
- `data/processed/chunks/structure_aware.jsonl`
- `data/processed/cleaned/*.jsonl` and the referenced PDFs for Q003, Q004,
  Q005, Q010, and Q011
- `src/chunk.py`, `src/search.py`, and `src/embed.py`
- `reports/chunking_report.md`, `reports/embedding_model_assessment.md`,
  `reports/embedding_execution_report.md`, and
  `reports/retrieval_evaluation_report.md`

Chunk sizes were independently tokenized from the `text` field using the
locally cached BGE-M3 tokenizer at revision
`5617a9f61b028005a4858fdac845db406aefb181` (`XLMRobertaTokenizer`, vocabulary
size 250,002). Token counts include the tokenizer's default special tokens and
disable truncation. No remote model or embedding service was used. The existing
`token_count` field is **not** this count: it was produced by the chunker's
documented Unicode lexical regex tokenizer. The BGE counts below are a
measurement only; no source chunk or stored count was changed.

Retrieval comparisons use the existing 25 questions, top-10 ranked records,
and Milestone 2B.16 relevance definition: a matching document ID plus
overlapping 1-based PDF page provenance. `Y/N` in the question table indicates
whether that strategy has a relevant result by ranks 3, 5, and 10,
respectively. The full machine-readable comparison is in
`data/evaluation/results/chunking_strategy_question_comparison.csv`.

## Chunk-size comparison

Counts are over all chunk records, including separate table chunks.

| Measure (BGE-M3 tokens) | Fixed-size | Structure-aware |
|---|---:|---:|
| Total chunks | 1,370 | 1,478 |
| Average | 480.22 | 412.40 |
| Median | 571 | 468.5 |
| Minimum | 7 | 7 |
| Maximum | 1,248 | 1,233 |
| 300–800 tokens | 965 (70.44%) | 983 (66.51%) |
| Below 300 tokens | 346 (25.26%) | 451 (30.51%) |
| Above 800 tokens | 59 (4.31%) | 44 (2.98%) |

The target-range percentages differ from the earlier chunking report because
that report's counts use the lexical tokenizer. Here the BGE tokenizer is used
for every reported size statistic. The configured 300–800 range is a target,
not a claim that every chunk should be forced into that range.

Text and table records have different size profiles:

| Content type | Strategy | Chunks | Average | Median | Min–max | 300–800 |
|---|---|---:|---:|---:|---:|---:|
| Text | Fixed-size | 930 | 584.58 | 598 | 32–1,248 | 811 (87.20%) |
| Text | Structure-aware | 1,038 | 477.16 | 517 | 7–1,233 | 829 (79.87%) |
| Table | Fixed-size | 440 | 259.63 | 204 | 7–955 | 154 (35.00%) |
| Table | Structure-aware | 440 | 259.63 | 204 | 7–955 | 154 (35.00%) |

Fixed-size produces 108 fewer chunks and larger text chunks on average.
Structure-aware produces more text chunks and a lower text-chunk mean; its
logical boundaries can leave short units, while long units are still split.
Neither shape is inherently better: larger context may help with related
provisions but can dilute a passage or broaden page provenance; shorter,
section-aligned context may sharpen topical matching but can separate a
question from nearby context.

## Tables, page provenance, and section context

- Both strategies contain **440 separate table chunks** representing the same
  **370 source tables** found in cleaned pages. There are 63 split source
  tables: 57 into two parts, 5 into three, and 1 into four. The resulting 440
  table objects, including rows and split-part metadata, match exactly between
  the two outputs.
- Tables remain `content_type="table"` and retain structured `tables` rows in
  addition to rendered chunk text. Splits are row-based and later parts mark
  the repeated first row as a header. Two table chunks exceed 800 BGE tokens
  in each strategy; intact long rows are a likely constraint, not evidence
  that one strategy handles tables better.
- The retrieved table-value questions Q016–Q020 all have a page-level relevant
  result by rank 3 in both strategies. Q020 ranks at 1 for fixed-size and 3
  for structure-aware; the other four table-value questions tie at their first
  relevant rank. This is a small sample and does not establish a general table
  advantage.
- Both chunk sets represent the same **808 document-page pairs**, including
  all 37 OCR-selected pages and all 71 cleaning-review pages. The chunk-level
  flag totals differ because the strategies create different overlapping
  chunks: fixed-size has 65 chunks with OCR and 154 with review flags;
  structure-aware has 72 and 153, respectively. These are not counts of
  unique OCR/review pages.
- `section_title` is populated on 1,082 fixed-size chunks (78.98%) and 1,242
  structure-aware chunks (84.03%). Structure-aware has a modestly higher
  metadata coverage. The field is not a guaranteed clean hierarchy: detected
  clause-like lines, noisy OCR text, or ordinary short labels can appear as
  titles.
- Fixed-size has 663 multi-page chunks; structure-aware has 487. Both preserve
  `page_provenance`; most chunks have single-page ranges, while fixed-size
  more often carries text across page boundaries. In two Annual Report chunks
  per strategy, the `page_start`–`page_end` envelope includes empty pages not
  listed in `page_provenance`. Use provenance rather than treating every page
  in the envelope as represented.

The chunker implementation explains the observed trade-off: fixed-size uses
sliding lexical-token windows with overlap; structure-aware forms paragraph
and heading/clause units, combines units toward its target, and splits long
units. Both retain title/context metadata and table content; the table
pipeline is shared in outcome rather than being a distinguishing retrieval
feature here.

## Retrieval metrics

### Overall

| Metric | Fixed-size | Structure-aware |
|---|---:|---:|
| Recall@3 | 0.8000 (80%) | 0.6800 (68%) |
| Recall@5 | 0.9200 (92%) | 0.8400 (84%) |
| Recall@10 | 0.9600 (96%) | 0.9600 (96%) |
| MRR | 0.6117 | 0.5774 |

### By question category

| Category | Strategy | N | Recall@3 | Recall@5 | Recall@10 | MRR |
|---|---|---:|---:|---:|---:|---:|
| Standard | Fixed-size | 15 | 0.7333 | 0.8667 | 0.9333 | 0.5473 |
| Standard | Structure-aware | 15 | 0.5333 | 0.7333 | 0.9333 | 0.4679 |
| Table-value | Fixed-size | 5 | 1.0000 | 1.0000 | 1.0000 | 0.8667 |
| Table-value | Structure-aware | 5 | 1.0000 | 1.0000 | 1.0000 | 0.7333 |
| Paraphrased | Fixed-size | 5 | 0.8000 | 1.0000 | 1.0000 | 0.5500 |
| Paraphrased | Structure-aware | 5 | 0.8000 | 1.0000 | 1.0000 | 0.7500 |

Both strategies retrieve the same 24 questions in the official top 10; neither
has a strategy-exclusive top-10 success. Q010 is missed by both at that
cutoff. Fixed-size's
aggregate lead comes mainly from the standard category and Q020's earlier
table-value hit; structure-aware is better on several paraphrased questions.
The evaluation is only 25 questions and should not be read as a significant
or universal strategy difference.

## Per-question comparison

`Hits` lists Recall@3, @5, and @10 in order. Chunk identifiers and their
page-range provenance are the relevant results in the official top 10. For
complete question text, flags, and CSV-safe values, see the linked CSV.

| ID | Type | Fixed: rank / RR / hits | Structure: rank / RR / hits | ΔRR (structure − fixed) | Classification | Relevant chunk IDs and page ranges (fixed / structure) |
|---|---|---|---|---:|---|---|
| Q001 | standard | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_001_fixed_size_00001_aee405d33739` p1–4 / `doc_001_structure_aware_00001_ac782e3816d0` p1–3 |
| Q002 | standard | 3 / 0.333 / YYY | 3 / 0.333 / YYY | +0.000 | Tie | `doc_001_fixed_size_00003_0bf6f42069fa` p3–4 / `doc_001_structure_aware_00003_ad7599361f91` p3–4 |
| Q003 | standard | 7 / 0.143 / NNY | 4 / 0.250 / NYY | +0.107 | Structure-aware better | `doc_001_fixed_size_00003_0bf6f42069fa` p3–4; `doc_001_fixed_size_00001_aee405d33739` p1–4 / `doc_001_structure_aware_00003_ad7599361f91` p3–4 |
| Q004 | standard | 1 / 1.000 / YYY | 7 / 0.143 / NNY | −0.857 | Fixed-size better* | `doc_001_fixed_size_00001_aee405d33739` p1–4; `doc_001_fixed_size_00003_0bf6f42069fa` p3–4; `doc_001_fixed_size_00004_785fedf70295` p4–5 / `doc_001_structure_aware_00003_ad7599361f91` p3–4; `doc_001_structure_aware_00004_288632361e39` p4–5 |
| Q005 | standard | 5 / 0.200 / NYY | 6 / 0.167 / NNY | −0.033 | Fixed-size better* | `doc_001_fixed_size_00004_785fedf70295` p4–5 / `doc_001_structure_aware_00004_288632361e39` p4–5 |
| Q006 | standard | 3 / 0.333 / YYY | 4 / 0.250 / NYY | −0.083 | Fixed-size better | `doc_001_fixed_size_00004_785fedf70295` p4–5 / `doc_001_structure_aware_00004_288632361e39` p4–5 |
| Q007 | standard | 2 / 0.500 / YYY | 2 / 0.500 / YYY | +0.000 | Tie | `doc_001_fixed_size_00005_d577f4089a07` p5–6; `doc_001_fixed_size_00004_785fedf70295` p4–5 / `doc_001_structure_aware_00005_33a0e3812a93` p5–6; `doc_001_structure_aware_00004_288632361e39` p4–5 |
| Q008 | standard | 1 / 1.000 / YYY | 2 / 0.500 / YYY | −0.500 | Fixed-size better | `doc_003_fixed_size_00005_96b0d302eff6` p4–5; `doc_003_fixed_size_00006_8bf99111838c` p4–5 / `doc_003_structure_aware_00005_a9d262541873` p3–4; `doc_003_structure_aware_00006_f9c845e0a416` p4–5 |
| Q009 | standard | 2 / 0.500 / YYY | 4 / 0.250 / NYY | −0.250 | Fixed-size better | `doc_003_fixed_size_00006_8bf99111838c` p4–5; `doc_003_fixed_size_00005_96b0d302eff6` p4–5; `doc_003_fixed_size_00007_2c72584c85de` p5–6 / `doc_003_structure_aware_00006_f9c845e0a416` p4–5 |
| Q010 | standard | — / 0.000 / NNN | — / 0.000 / NNN | +0.000 | Both missed | none / none in official top 10 |
| Q011 | standard | 5 / 0.200 / NYY | 8 / 0.125 / NNY | −0.075 | Fixed-size better | `doc_016_fixed_size_00005_92e15d19bd51` p4–5 / `doc_016_structure_aware_00006_d4c341ea43e2` p5 |
| Q012 | standard | 2 / 0.500 / YYY | 2 / 0.500 / YYY | +0.000 | Tie | `doc_016_fixed_size_00007_c0b5bc32280d` p6–7; `doc_016_fixed_size_00006_5707a2baee10` p5–6 / `doc_016_structure_aware_00007_3562949c7e7a` p6 |
| Q013 | standard | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_024_fixed_size_00002_15bb2fdc5f67` p1–2; `doc_024_fixed_size_00003_cb861a2996e0` p2–3 / `doc_024_structure_aware_00002_c7c2c87cf73a` p1–2; `doc_024_structure_aware_00003_c9a35a031d1e` p2–3 |
| Q014 | standard | 2 / 0.500 / YYY | 1 / 1.000 / YYY | +0.500 | Structure-aware better | `doc_024_fixed_size_00005_23b340ab4a76` p3–4; `doc_024_fixed_size_00003_cb861a2996e0` p2–3; `doc_024_fixed_size_00004_e6145695ee32` p3–4 / `doc_024_structure_aware_00003_c9a35a031d1e` p2–3; `doc_024_structure_aware_00004_ea79c085f5a8` p3–4 |
| Q015 | standard | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_023_fixed_size_00002_1f9f6e67ac59` p1–3 / `doc_023_structure_aware_00002_8dc9d4739e5b` p1–2 |
| Q016 | table_value | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_019_fixed_size_00003_c97da965ff31` p2 / `doc_019_structure_aware_00003_2fe8e4668967` p2 |
| Q017 | table_value | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_034_fixed_size_00001_9402fb448062` p1; `doc_034_fixed_size_00002_c622db067f0e` p1–2 / `doc_034_structure_aware_00001_edcae9ae118c` p1; `doc_034_structure_aware_00002_c45648b6c424` p1–2 |
| Q018 | table_value | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_034_fixed_size_00001_9402fb448062` p1; `doc_034_fixed_size_00002_c622db067f0e` p1–2 / `doc_034_structure_aware_00001_edcae9ae118c` p1; `doc_034_structure_aware_00002_c45648b6c424` p1–2 |
| Q019 | table_value | 3 / 0.333 / YYY | 3 / 0.333 / YYY | +0.000 | Tie | `doc_023_fixed_size_00009_c432e15f15bb` p7; `doc_023_fixed_size_00010_a7d7b91a7eb1` p7–10 / `doc_023_structure_aware_00009_37b714cae638` p7; `doc_023_structure_aware_00010_087fc5b6e931` p7–9 |
| Q020 | table_value | 1 / 1.000 / YYY | 3 / 0.333 / YYY | −0.667 | Fixed-size better | `doc_036_fixed_size_00072_29979ea5ed7c` p41–43; `doc_036_fixed_size_00070_eb1ac13cadb6` p40–41 / `doc_036_structure_aware_00079_31c3eb9905da` p41; `doc_036_structure_aware_00080_da6891873a1b` p41 |
| Q021 | paraphrased | 2 / 0.500 / YYY | 1 / 1.000 / YYY | +0.500 | Structure-aware better | `doc_016_fixed_size_00003_d1e3de271923` p2–3 / `doc_016_structure_aware_00004_15199cc67fa1` p2–3 |
| Q022 | paraphrased | 4 / 0.250 / NYY | 4 / 0.250 / NYY | +0.000 | Tie | `doc_024_fixed_size_00005_23b340ab4a76` p3–4; `doc_024_fixed_size_00004_e6145695ee32` p3–4 / `doc_024_structure_aware_00003_c9a35a031d1e` p2–3 |
| Q023 | paraphrased | 2 / 0.500 / YYY | 2 / 0.500 / YYY | +0.000 | Tie | `doc_016_fixed_size_00006_5707a2baee10` p5–6 / `doc_016_structure_aware_00007_3562949c7e7a` p6 |
| Q024 | paraphrased | 1 / 1.000 / YYY | 1 / 1.000 / YYY | +0.000 | Tie | `doc_024_fixed_size_00003_cb861a2996e0` p2–3; `doc_024_fixed_size_00004_e6145695ee32` p3–4 / `doc_024_structure_aware_00003_c9a35a031d1e` p2–3 |
| Q025 | paraphrased | 2 / 0.500 / YYY | 1 / 1.000 / YYY | +0.500 | Structure-aware better | `doc_001_fixed_size_00005_d577f4089a07` p5–6 / `doc_001_structure_aware_00005_33a0e3812a93` p5–6 |

*Q004 and Q005 illustrate a potential page-overlap over-credit; see
`reports/retrieval_failure_analysis.md`. The official rank labels above are
preserved unchanged.

## Interpretation, limitations, and recommendation

The observed fixed-size advantage is primarily a **ranking outcome** in this
dataset, especially among standard questions. Its text chunks are larger on
average under BGE tokenization and retain overlap across page boundaries, which
can keep nearby context together. Structure-aware more often produces
section-aligned context and smaller text chunks, which is consistent with its
wins on Q003, Q014, Q021, and Q025. These are plausible mechanisms, not
causally isolated findings: there was no controlled experiment changing only
one chunking variable.

Table handling is not a differentiator in these outputs: both strategies have
identical structured table chunks and all five table questions hit by rank 3.
Section-title coverage is higher for structure-aware, but the field can be
noisy. Fixed-size's broad page ranges can also produce a page-level match even
when the matching chunk does not contain the gold evidence passage. This is
the most important current evaluation caveat.

**Recommendation — retain both for further evaluation.** Continue comparing
both under a larger and more representative question set, but first add a
future evidence-level audit that checks whether retrieved chunk text contains
or substantively covers the gold passage. Keep page provenance as a necessary
condition, not the sole relevance condition. For chunking experiments,
specifically compare narrower page/section-boundary chunks against the current
overlap windows while preserving table rows and nearby heading context. No
implementation changes are made in this milestone.

### Limitations

1. The 25 questions are a small, category-balanced evaluation set; metrics are
   descriptive and question-level, not statistically significant.
2. The official evaluator counts a result as relevant on document and page
   overlap. It does not require the exact gold evidence to be present in the
   returned chunk text. The Q004 and Q005 inspection demonstrates why this
   can overstate evidence retrieval.
3. BGE-tokenizer measurements include special tokens and should be compared
   consistently if future chunking changes are evaluated.
4. No chunking, extraction, search, or embedding implementation was changed.
   The top-20 results are separately labeled diagnostics and do not alter
   Milestone 2B.16 metrics.

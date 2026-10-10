# Data and results

These files describe the AIMS at COLM 2026 workshop camera-ready benchmark.
This directory contains benchmark metadata, individual scores and two worked
examples. The complete 276 case prompts, matching scoring references and 7,728
case model responses are available on
[Hugging Face](https://huggingface.co/datasets/Hongyu801/LegalScope).
The source judgments, full exam input and response collections, and raw review
sheets are excluded. See the [release guide](../docs/USING_THE_RELEASE.md).

| File | Purpose |
| --- | --- |
| `metadata/dataset_summary.json` | Version, counts, endpoints, and current/historical audit scope. |
| `metadata/model_groups.csv` | 28 model groups; indices match Figure 3. |
| `metadata/model_performance.csv` | Paper Table 3, rounded to one decimal on the 0-100 scale. |
| `metadata/source_composition.csv` | Country, U.S. source, and legal-category composition. |
| `metadata/exam_source_locations.jsonl` | PDF page links for all 78 released Victorian Bar source records. |
| `metadata/case_release_manifest.json` | Case release counts, field definitions and file hashes. |
| `results/answer_scores.csv.gz` | 34,636 automatic and human score records; reproduces all 252 published aggregate values. |
| `examples/` | Complete stored inputs, model answers, scores and sources for the website examples. |

The benchmark has 861 exam items and 276 case prompts (1,137 total). Across 28
models this gives 31,836 responses. Human validation covers 2,520 unique answers;
case answers are each rated by two lawyers.

Source-composition percentages use the matching split/dimension denominator.
The public-exam category residual is derived by subtracting the paper's displayed
categories (at least 20 items each) from 861. It contains 107 items. Model names
follow Appendix A.1, with the table's short LLaMA label expanded to `Instruct`.

In `model_performance.csv`, exam human scores use the 80-item validation subset;
case human scores use the pooled lawyers on the 10-prompt subset. Automatic scores
cover the full tracks. Overall columns average the two corresponding track means
and are descriptive, not equated ability scales. Rounded aggregates can differ
from averages calculated from other rounded columns. Use individual scores for
[reproduction](../docs/REPRODUCIBILITY.md).

Current clustered analyses use all 276 prompts and 56 judgments. Historical
controls and the fixed 200-answer stability audits have separate denominators in
the JSON. See [results](../docs/RESULTS_SUMMARY.md).

`sample/` documents the optional legacy workbook utility. Published records are
listed in the release guide above.

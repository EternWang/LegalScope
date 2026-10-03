# Data Preview

These files describe the AIMS at COLM 2026 workshop camera-ready benchmark.
The full workbook, prompts, references, model outputs, and review sheets are not included.

| File | Purpose |
| --- | --- |
| `metadata/dataset_summary.json` | Version, counts, endpoints, and current/historical audit scope. |
| `metadata/model_groups.csv` | 28 model groups; indices match Figure 3. |
| `metadata/model_performance.csv` | Paper Table 3, rounded to one decimal on the 0-100 scale. |
| `metadata/source_composition.csv` | Country, U.S. source, and legal-category composition. |

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
and are descriptive, not equated ability scales. Rounding can prevent exact
reconstruction of means, differences, or rank order.

Current clustered analyses use all 276 prompts and 56 judgments. Historical
controls and the fixed 200-answer stability audits have separate denominators in
the JSON. See [results](../docs/RESULTS_SUMMARY.md).

`sample/` contains only a README. The legacy sample generator produces a different
workbook-derived metadata format; use a separate output directory and complete
release review before publishing generated rows.

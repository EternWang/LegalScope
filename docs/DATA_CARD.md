# Data Card

## Purpose and Version

LegalScope measures the relationship between public legal-exam performance and
closed book reasoning over curated summaries of deidentified Chinese judgments.
This card follows the AIMS at COLM 2026 workshop camera-ready version.

For the downloadable subset, its complete field dictionary, a runnable loading
example, answer types, and current case-release status, see
[Using the public release](USING_THE_RELEASE.md). The six Hub configurations total 716 rows: 276 case prompts, 276 matching
scoring references, 78 exam source records and 86 metadata rows. This means
354 prompt/source records, not 716 questions. See the [case fields and provenance](CASE_RELEASE.md).

## Benchmark Composition

| Component | Count |
| --- | ---: |
| Public legal-exam items | 861 |
| Real-case issue-stance prompts | 276 |
| Total dataset items | 1,137 |
| Model groups | 28 |
| Public-exam responses | 24,108 |
| Real-case responses | 7,728 |
| Total dataset responses | 31,836 |
| Exam validation items / responses | 80 / 2,240 |
| Case validation prompts / unique responses | 10 / 280 |
| Total validation items / unique responses | 90 / 2,520 |
| De-identified Chinese judgments | 56 |
| Real-case legal issues | 138 |

See [dataset summary](../data/metadata/dataset_summary.json) for machine-readable
counts. Human-validation counts refer to unique answers, not lawyer-rating events.

## Splits

The exam split covers the United States (603), China (94), the United Kingdom (86),
and Australia (78). One duplicate and six items with unverifiable shared context
were excluded from the earlier split. Reported exam responses and scores predate
prompt and reference-text repairs (paper Sections 3.1 and 5.1).

The case split has 80 Tort, 72 Contract, 54 Criminal, 34 Intellectual Property,
22 Administrative, 8 Civil Procedure, and 6 Property prompts. Each of 138 issues
has one supporting and one opposing prompt. Real-case provenance refers to
concluded judgments, not access to complete case files. Names, institutions,
addresses, and original file paths are removed or masked during deidentification.

Human validation covers all 28 groups. Exam human scores are reviewed and
confirmed against the reference answers. Two practicing Chinese lawyers independently score the same
case answer set, with Lawyer 2 held out from rubric calibration. Their case scores
are pooled with equal weights.

## Audit Scope

The current clustered dimension analysis covers all 276 case prompts and 56
judgments. Historical controls and the 200-answer, five-run fixed-answer audits
retain their own pools. See [results](RESULTS_SUMMARY.md) for the distinction.

## Metadata Provenance

Country, U.S. source, and category counts follow Sections 3.1-3.2 and Tables 5,
15-16. Public-exam categories below the paper's 20-item display threshold are
grouped into an explicitly derived residual (107 items). Percentages are calculated
within the relevant split/dimension and rounded to one decimal place.

The model roster follows Appendix A.1; indices follow Figure 3. The shortened
figure/table label `LLaMA 3.1 8B` is normalized to `LLaMA 3.1 8B Instruct` in CSVs.
Table 3 performance values retain the paper's one decimal precision and order.

## Public Release and Intended Use

The repository exposes documentation, figures, aggregate statistics, and workbook
helpers. It supports inspection of benchmark design and evaluation methodology,
and helper reuse with authorized local data. The project page includes one
attributed Victorian Bar question-and-answer excerpt under CC BY-NC-ND 4.0;
see [third party notices](../THIRD_PARTY_NOTICES.txt).

The [Hugging Face release](https://huggingface.co/datasets/Hongyu801/LegalScope)
includes all 276 deidentified case prompts and their scoring references in
separate configurations, plus 78 Victorian Bar source excerpts. Six configurations
use Parquet; original CSV/JSONL downloads remain available. The case input and
reference fields match the current workbook. Updated citations and their
[official sources](CASE_REFERENCE_NOTES.md) are included in the reference configuration.

The exam subset retains source-specific attribution and CC BY-NC-ND 4.0 notices;
it is not an exact replacement for the original exam evaluation inputs.
The paper's scores are unchanged. The [reproducibility files](REPRODUCIBILITY.md)
include 7,728 stored case responses, 34,636 individual scores and page locations
for all 78 exam source records. Remaining exam inputs, exam response text, raw
lawyer sheets, original judgments and private workbooks are excluded.
See [case sources](CASE_RELEASE.md#case-publication-status) for provenance,
deidentification, and the scope of the released annotations.

## Limitations

- Case tasks concern Chinese judgments and curated, closed book summaries; they
  do not represent every jurisdiction or the full legal workflow.
- Exam materials may occur in pretraining data; exam scores are comparative
  signals rather than clean generalization tests.
- Tracks and rubric dimensions are not equated difficulty scales.
- Human validation is a subset, not manual relabeling of the full matrix.
- The automatic evaluator alias is not date-pinned, decoding settings are not
  fully specified, and historical scores remain where no update was run.
- Source redistribution and privacy constraints limit public artifact release.

These materials are not intended for legal advice, ranking legal professionals or
institutions, or deploying legal decision systems.

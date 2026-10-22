# Data Card

## Purpose

LegalScope measures the relationship between public legal-exam performance and
closed book reasoning over curated summaries of deidentified Chinese judgments.

The [loading guide](USING_THE_RELEASE.md) covers downloads, field definitions and
examples. The six Hub configurations contain 354 prompt/source records, 276
matching references and 86 metadata rows (716 rows total).

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
and Australia (78). Curation excluded one duplicate and six items whose shared
context could not be verified. The [reproducibility guide](REPRODUCIBILITY.md#scoring-provenance)
documents the inputs used for reported scores.

The case split has 80 Tort, 72 Contract, 54 Criminal, 34 Intellectual Property,
22 Administrative, 8 Civil Procedure, and 6 Property prompts. Each of 138 issues
has one supporting and one opposing prompt. The tasks use summaries of concluded
judgments. Names, institutions,
addresses, and original file paths are removed or masked during deidentification.

Human validation covers all 28 groups. Exam human scores are reviewed and
confirmed against the reference answers. Two practicing Chinese lawyers independently score the same
case answer set, with Lawyer 2 held out from rubric calibration. Their case scores
are pooled with equal weights.

## Audit Scope

The clustered dimension analysis covers all 276 case prompts and 56 judgments.
Repeatability analyses use 200 fixed, blinded answers from 10 prompts and 20 model
configurations, with five repetitions per dimension. The Tort control
uses 243 exam items, 76 case prompts from 15 judgments, and 20 model configurations.
See the [results summary](RESULTS_SUMMARY.md#reliability-analyses-and-supplementary-controls)
for the supplementary analyses.

## Metadata Provenance

Country, U.S. source, and category counts follow the paper's benchmark composition
and category analyses. Public-exam categories below its 20-item display threshold are
grouped into an explicitly derived residual (107 items). Percentages are calculated
within the relevant split/dimension and rounded to one decimal place.

The model roster follows the paper's model list; indices follow the transfer plots. The shortened
figure/table label `LLaMA 3.1 8B` is normalized to `LLaMA 3.1 8B Instruct` in CSVs.
Model performance values retain the paper's one decimal precision and order.

## Public Release and Intended Use

The release supports research on legal reasoning and evaluation. GitHub provides
documentation, figures, worked examples, individual and aggregate scores, and
generation/scoring code. [Hugging Face](https://huggingface.co/datasets/Hongyu801/LegalScope)
hosts 276 case prompts, 276 scoring references, 7,728
[English case responses](SCORING_RUBRIC.md#evaluation-workflow) and
78 Victorian Bar source records. [Reproducibility files](REPRODUCIBILITY.md)
include 34,636 individual scores and PDF page locations for all 78 source records.

Case prompts preserve the evaluation inputs. Ten scoring references have
[citation updates](CASE_REFERENCE_NOTES.md) made after evaluation. The exam
source excerpts reproduce publisher text and differ from the original evaluation
inputs. Original judgments, identifying mappings, the remaining 783 exam inputs,
exam response text and raw human review sheets are outside the release.

To respect third-party copyright, we release only the 78 Victorian Bar exam
excerpts licensed under CC BY-NC-ND 4.0. Project-authored code, documentation,
metadata and case annotations use MIT. The excerpts retain their
[source notices](../THIRD_PARTY_NOTICES.txt). See the [case sources](CASE_RELEASE.md#case-sources)
for provenance and deidentification.

## Limitations

- Case tasks cover curated Chinese judgment summaries and assigned stances.
- Exam materials may occur in pretraining data, affecting generalization claims.
- Track and dimension scores measure different properties and difficulty levels.
- Human validation covers 80 exam questions and 10 case prompts.
- New scoring runs depend on evaluator settings and reference versions; see the
  [scoring provenance notes](REPRODUCIBILITY.md#scoring-provenance).

The benchmark is intended for research, not legal advice or operational legal decisions.

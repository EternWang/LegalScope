# Data Card

## Purpose and Version

LegalScope measures the relationship between public legal-exam performance and
closed book reasoning over curated summaries of deidentified Chinese judgments.
This card follows the AIMS at COLM 2026 workshop camera-ready version.

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
and Australia (78). One duplicate and six items with unverifiable shared context
were excluded from the earlier split. Reported exam responses and scores predate
prompt and reference-text repairs (paper Sections 3.1 and 5.1).

The case split has 80 Tort, 72 Contract, 54 Criminal, 34 Intellectual Property,
22 Administrative, 8 Civil Procedure, and 6 Property prompts. Each of 138 issues
has one supporting and one opposing prompt. The tasks use summaries of concluded
judgments. Names, institutions,
addresses, and original file paths are removed or masked during deidentification.

Researchers handled source selection, deidentification, legal review and
interpretation. AI tools supported data processing, answer generation and scoring.

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

Project-authored code, documentation, metadata and case annotations use MIT.
Victorian Bar text retains CC BY-NC-ND 4.0 and its
[source notices](../THIRD_PARTY_NOTICES.txt). See the [case sources](CASE_RELEASE.md#case-sources)
for provenance and deidentification.

## Limitations

- Case tasks cover curated Chinese judgment summaries and assigned stances.
- Exam materials may occur in pretraining data, affecting generalization claims.
- Track and dimension scores measure different properties and difficulty levels.
- Human validation covers 80 exam questions and 10 case prompts.
- Evaluator aliases, unspecified decoding settings and retained historical scores
  limit exact reproduction of new scoring runs; see the [scoring protocol](SCORING_RUBRIC.md).

The benchmark is intended for research, not legal advice or operational legal decisions.

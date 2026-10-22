# Releases

## Current release

The public dataset is hosted at
[Hongyu801/LegalScope](https://huggingface.co/datasets/Hongyu801/LegalScope).
It accompanies the [AIMS at COLM 2026 workshop paper](https://openreview.net/forum?id=BNx62Wx1ej).

| Component | Public contents |
| --- | --- |
| Case prompts | 276 evaluation inputs from 56 judgments and 138 issues |
| Case scoring references | 276 matching records, joined by `review_id` |
| Victorian Bar source excerpts | 78 records with selected candidate answers and source notices |
| Model results and roster | 28 model groups, including 252 aggregate score values |
| Source composition | 30 rows describing overlapping source and category breakdowns |
| Case model responses | 7,728 stored responses across 276 prompts and 28 models |
| Individual scores | 34,636 numeric score records, including human scores |
| Exam source locations | 78 records with 213 excerpt locations in the original PDFs |
| Evaluation code | Score aggregation, response generation, anonymous scoring and archived rubrics |

The six configurations contain 716 rows. There are 354 prompt or source records;
matching references and metadata are not additional questions. Case prompts are
the default view. All configurations support Parquet loading; CSV and JSONL
downloads are also available. Response, individual score and page-location files
are additional downloads outside the six viewer configurations.

[Loading guide](USING_THE_RELEASE.md) · [Case fields and sources](CASE_RELEASE.md) ·
[Reference sources](CASE_REFERENCE_NOTES.md)

## October 22, 2026

Unified the project page and dataset guides around the workshop version and the
Chinese-answer → GPT-5.5 English-translation → scoring workflow. Examples now show
short summaries and scores, with full inputs, answers and rules expandable.
Updated the sample-data guide, aligned the exam scoring description with the
released rubric, and shortened download and methodology documentation.

## October 10, 2026

The project website now separates the home overview, task examples, results,
and data/citation pages. Both worked examples show the complete stored input
and answer with their scoring rules and recorded scores.

Case metadata uses standardized deidentification descriptions and reference status
labels, with identical records in JSONL and Parquet.

## October 9, 2026

Released all 276 case prompts and their scoring references. Ten reference
records include citation corrections made after scoring and links to official
legal sources. The reference source index lists the
affected record IDs and cited provisions.

Published individual scores reproduce all 252 main-table values. The release adds
case response text, exam PDF page links, archived scoring rubrics and runnable
evaluation utilities. See the [reproducibility guide](REPRODUCIBILITY.md).

## October 8, 2026

Released 78 Victorian Bar source excerpts with selected candidate answers,
attribution, license notices, and source manifests. Model results, the roster,
and source composition are available in both CSV and Parquet.

The website includes worked exam and case examples. Its results table identifies
the best displayed value in bold and the second best with an underline, including
ties. These annotations describe displayed values, not statistical significance.

## October 3, 2026

Updated benchmark documentation, results, model names, and figures to the workshop
paper: 861 exam items, 276 case prompts, 56 judgments, 138 legal issues, and 28
model groups. The benchmark contains 31,836 model responses and 2,520 unique
human validation answers.

Earlier versions remain in [Git history](https://github.com/EternWang/LegalScope/commits/main).

## Availability and use

See the [data card](DATA_CARD.md) for release scope, licenses and intended use.
Report loading or data errors in a [GitHub issue](https://github.com/EternWang/LegalScope/issues)
with the record ID and dataset revision.

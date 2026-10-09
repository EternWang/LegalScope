# Project Brief

This summary follows the AIMS at COLM 2026 workshop camera-ready version of
[LegalScope](https://openreview.net/forum?id=BNx62Wx1ej).

## Research Question

Public legal exams are standardized, scalable, and often paired with reference
answers. Real-case analysis instead requires selecting responsive authorities,
respecting a bounded factual record, and constructing an argument under a specified
stance. LegalScope studies the association between independently scored exam and
case tracks over a common model roster.

## Benchmark Design

<img src="../assets/figures/paper_collection_pipeline.png" alt="LegalScope benchmark construction pipeline" width="920">

| Track | Task | Scale |
| --- | --- | ---: |
| Public legal exams | Reference-aware legal-exam answering | 861 questions |
| Chinese real cases | Closed-book, stance-aware analysis of curated judgment summaries | 276 prompts |

The exam track covers the United States (603), China (94), the United Kingdom (86),
and Australia (78). The case track covers seven legal categories and derives 138
issues from 56 deidentified Chinese judgments. Each issue has supporting and
opposing prompts. Models must construct arguments rather than only predict the
court's outcome. Real-case provenance does not mean access to complete case files.

## Evaluation Protocol

Exam answers receive reference-matching scores from 0 to 4. Case answers receive
three separate 0-4 scores: citation relevance, constraint extraction, and argument
validity. Constraint extraction assesses the assigned stance, factual boundaries,
requested subtasks, and format. Case totals average these three dimensions; scores
are mapped to 0-100 without equating the difficulty of the two tracks.

Across 28 model groups, the benchmark contains 24,108 exam responses and 7,728 case
responses. Independent review covers 2,240 exam answers and 280 case answers, with
two practicing lawyers independently scoring the same case set.

## Findings and Interpretation

Exam and case means correlate at `r = 0.817` and `rho = 0.708`, but rankings and
variant gains can change. Citation relevance has a lower mean than argument
validity under automatic and lawyer evaluation. The pooled lawyer contrast remains
descriptive because its confidence interval includes zero.

Automatic-human answer-level agreement falls from `r = 0.910` on exams to
`r = 0.312` on cases, motivating expert-grounded case evaluation. The workshop
version does not retain the earlier claim that constraint extraction is the main
automatic-scoring bottleneck. See [results](RESULTS_SUMMARY.md) for exact endpoints,
uncertainty, and historical-audit distinctions.

## Public Repository

Documentation, figures, aggregate results, metadata, and workbook helpers are
available here. Hugging Face provides 276 case prompts with separately packaged
historical scoring references and 78 Victorian Bar source records. See the
[case release](CASE_RELEASE.md) and [official reference sources](CASE_REFERENCE_NOTES.md).
Remaining exam inputs, full model responses, human review sheets and original
judgment files are not included.

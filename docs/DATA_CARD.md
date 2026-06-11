# Data Card

## Dataset Name

LegalScope.

## Purpose

LegalScope evaluates whether LLM performance on public legal-exam tasks transfers to
practice-oriented legal reasoning over de-identified Chinese civil judgments. The
benchmark separates reference-answer scoring from case-based rubric scoring so that
exam performance, real-case performance, human validation, and transfer can be
studied separately.

## Benchmark Composition

| Component | Count |
| --- | ---: |
| Public legal-exam items | 868 |
| Real-case issue-stance prompts | 76 |
| Total dataset items | 944 |
| Model groups | 20 |
| Public-exam model responses | 17,360 |
| Real-case model responses | 1,520 |
| Total dataset model responses | 18,880 |
| Human-scored public-exam items | 80 |
| Human-scored real-case prompts | 10 |
| Human-validation responses | 1,800 |
| De-identified Chinese civil judgments | 15 |
| Real-case legal issues | 38 |

See `data/metadata/dataset_summary.json` for the machine-readable summary.

## Splits

### Public Legal-Exam Split

The public-exam split contains open-ended questions from public legal-exam materials.
It is scored with a reference-aware 0-4 answer-match protocol. The split covers U.S.,
China, U.K., and Australia sources.

### Chinese Real-Case Split

The real-case split contains issue-stance prompts derived from de-identified Chinese
civil judgments. Each prompt asks the model to reason from a structured case setting
under a specified stance. It is scored across citation relevance, constraint
extraction, and argument validity.

### Human Validation

The human-validation subset covers 80 public-exam items and 10 real-case prompts
across the same 20 model groups. It is used to compare automated/model-judge scores
with human legal review.

## Public Release Boundary

The repository exposes only high-level metadata, documentation, selected paper figures,
and lightweight workbook utilities. It does not include the full workbook, full prompts,
reference answers, model-output matrices, human review sheets, or private source
documents.

## Intended Uses

- Studying legal benchmark design.
- Inspecting how exam and real-case evaluation settings differ.
- Reviewing documentation for high-stakes LLM evaluation workflows.
- Reusing lightweight workbook helpers in a private, properly licensed workspace.

## Out-of-Scope Uses

- Legal advice.
- Ranking lawyers, courts, litigants, institutions, or jurisdictions.
- Training or deploying legal decision systems from these materials.
- Redistributing source documents, full prompts, or model outputs without release
  review.

## Known Limitations

- The real-case split is focused on Chinese civil judgments and is not a general legal
  practice benchmark.
- Public-exam and real-case tasks use different scoring regimes.
- Some source materials may have licensing or redistribution constraints.
- Human validation is a subset of the full evaluation matrix, not a complete manual
  relabeling of all model responses.

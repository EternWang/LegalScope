# Data Card

## Dataset Name

LegalScope.

## Summary

LegalScope evaluates whether public legal-exam performance transfers to
practice-oriented legal reasoning over de-identified Chinese civil judgments.
The benchmark has two coordinated tracks:

- a public legal-exam track with reference-aware open-ended scoring;
- a real-case legal-analysis track with stance-aware, closed-record prompts
  derived from de-identified Chinese civil judgments.

The public repository is a metadata and documentation preview. It intentionally
does not publish the full workbook, row-level prompt matrix, model outputs,
human review sheets, or private legal source documents.

## Benchmark Composition

| Component | Count |
| --- | ---: |
| Public legal-exam items | 868 |
| Real-case issue-stance prompts | 76 |
| Total benchmark items | 944 |
| Model groups | 20 |
| Public-exam model responses | 17,360 |
| Real-case model responses | 1,520 |
| Total model responses | 18,880 |
| Human-scored public-exam items | 80 |
| Human-scored real-case prompts | 10 |
| Human-validation responses | 1,800 |
| De-identified Chinese civil judgments | 15 |
| Real-case legal issues | 38 |

See [`data/metadata/dataset_summary.json`](../data/metadata/dataset_summary.json)
for a machine-readable summary.

## Data Structure

### Public Legal-Exam Track

The public-exam track contains open-ended questions drawn from public legal-exam
materials across multiple jurisdictions. Answers are scored against reference
answers with a 0-4 protocol that rewards issue recognition, rule identification,
application, and conclusion alignment.

The public repository exposes only aggregate metadata for this track. Full
question text, reference answers, and model answers are withheld pending source
redistribution review.

### Real-Case Legal-Analysis Track

The real-case track contains issue-stance prompts derived from 15 de-identified
Chinese civil judgments and 38 legal issues. Many issues are paired into
support/opposition prompts so that the same bounded factual context can be used
to test whether models can construct statute-grounded arguments under an
assigned stance.

The track is scored on:

- citation relevance;
- constraint extraction;
- argument validity.

The public repository does not include non-de-identified judgments, full
prompts, hidden legal references, row-level model answers, or review notes.

### Human Validation

Human validation covers 80 public-exam items and 10 real-case prompts across the
same 20 model groups, for 1,800 human-validation responses. Human review is used
to calibrate and audit automated scoring, especially for real-case legal
analysis where expert judgment remains important.

## Source Composition

Public metadata includes:

- jurisdiction and domain counts for the public-exam track;
- legal-domain counts for the real-case track;
- model-group names used in the evaluation tables;
- aggregate transfer and human-validation metrics.

See [`data/metadata/source_composition.csv`](../data/metadata/source_composition.csv)
and [`data/metadata/model_groups.csv`](../data/metadata/model_groups.csv).

## Intended Uses

- Studying legal benchmark design.
- Comparing public-exam and real-case evaluation settings.
- Auditing release boundaries for high-stakes legal NLP datasets.
- Reusing public helper utilities with authorized local workbooks.
- Preparing a later full artifact release after privacy, license, and review
  checks.

## Out-of-Scope Uses

- Legal advice or legal decision support.
- Ranking courts, lawyers, litigants, institutions, or jurisdictions.
- Training or deploying legal decision systems from the public preview.
- Reconstructing private workbooks, source documents, model outputs, or human
  review sheets.
- Redistributing source materials without independent license and privacy
  review.

## Privacy and De-identification

Real-case materials are derived from de-identified Chinese civil judgments.
Non-de-identified judgments and private source files are excluded from the
public repository. Any row-level release should pass a separate review for
personal names, institution names, addresses, identifiers, case-specific
re-identification risk, and hidden evidence references.

## Known Limitations

- The real-case track is focused on Chinese civil judgments, not all legal
  practice settings.
- Public-exam and real-case tracks use different scoring regimes.
- The public preview documents aggregate results but does not expose all
  row-level evidence needed for independent replication.
- Human validation covers a subset of responses rather than a full manual
  relabeling of the entire model-output matrix.
- Source redistribution rights may differ across public-exam sources and
  judgment-derived materials.

## Version

This card describes the paper-submission benchmark snapshot represented by the
public LegalScope repository.

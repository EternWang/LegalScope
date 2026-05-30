# Scoring Rubric

This document summarizes the LegalScope scoring protocol used in the benchmark.

## Public Legal-Exam Scoring

Public-exam answers receive one reference-aware score from 0 to 4.

| Score | Anchor |
| ---: | --- |
| 0 | Nonresponsive, legally irrelevant, or opposite to the reference answer. |
| 1 | Captures roughly one core unit such as issue, rule, application, or conclusion. |
| 2 | Captures about two core units but misses major substance. |
| 3 | Mostly matches the reference answer with limited gaps. |
| 4 | Matches the core issue, rule/test, application, and conclusion without substantive conflict. |

## Real-Case A/B/C Rubric

Real-case answers receive three 0-4 scores.

### A. Citation Relevance

Checks whether the answer identifies legally responsive authority and connects it to a
usable legal proposition.

### B. Constraint Extraction

Checks whether the answer follows the assigned stance, extracts operative constraints,
avoids invented facts, respects the prompt boundary, and covers the requested issue.

### C. Argument Validity

Checks whether the answer states a defensible conclusion, applies rules to facts,
handles counterpoints, and avoids unsupported reasoning.

## Calibration Notes

The calibrated rubric keeps strict high-score thresholds while reducing over-penalty
for ordinary incompleteness. Severe failures such as stance reversal, non-answer,
refusal, major truncation, or unusable output remain capped at very low scores. If an
answer lacks a responsive legal basis, citation relevance can be zero while argument
or constraint dimensions may still receive limited credit for substantive reasoning.

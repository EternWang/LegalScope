# Scoring Rubric

LegalScope uses different scoring protocols for public legal exams and
real-case legal analysis because the two tracks test different forms of legal
reasoning.

## Public Legal-Exam Scoring

Public-exam answers receive one reference-aware score from 0 to 4.

| Score | Anchor |
| ---: | --- |
| 0 | Nonresponsive, legally irrelevant, or opposite to the reference answer. |
| 1 | Captures roughly one core unit such as issue, rule, application, or conclusion. |
| 2 | Captures about two core units but misses major substance. |
| 3 | Mostly matches the reference answer with limited gaps. |
| 4 | Matches the core issue, rule or test, application, and conclusion without substantive conflict. |

The public-exam score is intended to measure reference-answer alignment, not
general legal usefulness.

## Real-Case A/B/C Rubric

Real-case answers receive three independent 0-4 scores.

### A. Citation Relevance

Checks whether the answer identifies legally responsive authority and connects
that authority to a usable legal proposition.

High-scoring answers cite or name the controlling legal basis and explain why it
matters for the assigned issue. Low-scoring answers cite irrelevant rules, cite
rules that do not support the conclusion, omit legal authority, or rely on
generic legal language without a usable legal proposition.

### B. Constraint Extraction

Checks whether the answer recovers and respects the operative constraints in
the prompt:

- assigned support or opposition stance;
- given factual record;
- issue boundary;
- legal and evidentiary conditions;
- required output format;
- de-identification and closed-record restrictions.

High-scoring answers reason within the supplied record. Low-scoring answers
reverse the stance, invent facts, add hidden evidence, ignore key conditions, or
miss the issue being tested.

### C. Argument Validity

Checks whether the legal conclusion follows from the cited law and the supplied
facts under the assigned stance.

High-scoring answers connect rule conditions to the facts, handle important
counterpoints, and reach a defensible conclusion. Low-scoring answers are
conclusory, internally inconsistent, unsupported by the cited rules, or
misaligned with the core legal question.

## V2 Calibration

The current V2 rubric keeps strict high-score thresholds while reducing
over-penalty for ordinary incompleteness.

Key calibration principles:

- A score of 4 is reserved for answers with no meaningful substantive defect in
  that dimension.
- Severe failures such as stance reversal, non-answer, refusal, major
  truncation, or unusable output remain capped at very low scores.
- If an answer lacks a responsive legal basis, citation relevance can be zero;
  constraint extraction and argument validity may still receive limited credit
  when there is substantive reasoning.
- Missing hidden evidence, hidden appraisal material, or unshown contract
  detail should not be treated as a failure unless the prompt itself provided
  that material.
- Long or fluent writing should not raise a score unless it improves legal
  relevance, constraint recovery, or rule-to-fact reasoning.

The calibration goal is to reduce generator-evaluator bias while preserving the
distinction between fluent legal prose and legally controlled analysis.

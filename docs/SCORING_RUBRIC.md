# Scoring Rubric

LegalScope uses reference-answer matching for exams and a three-dimensional
rubric for case analysis, as described in the paper's evaluation protocol.
The [evaluation directory](../evaluation/README.md) provides machine-readable
rubrics, prompt construction and an executable scorer.

## Evaluation Workflow

Models received only the exam question or case prompt. For cases, models answered
English prompts in Chinese; GPT-5.5 translated the answers into English before
scoring. The evaluator received the prompt, translated answer and scoring
references. The downloadable case responses contain these English translations.

Automatic scores were compared with [human ratings](ANNOTATION_PROTOCOL.md).
The [results analysis](RESULTS_SUMMARY.md) covers exam-to-case association,
score dimensions and evaluator reliability.

## Public-Exam Scoring

Exam answers receive 0–4 points for substantive consistency with the reference
answer, considering the legal issues, governing rules, application and conclusion.

| Score | Assessment |
| ---: | --- |
| 0 | Wrong, irrelevant or not evaluable |
| 1 | Generic or weakly related legal statements |
| 2 | Relevant legal content with incomplete application |
| 3 | Correct core direction with some elements missing |
| 4 | Decisive legal points covered with a compatible conclusion |

The [released exam scorer](../evaluation/rubrics/exam_aug2026.json) implements
reference matching with four components: issue, governing rule, application or
exception, and conclusion or remedy. Each substantive match earns one point;
refusals and structurally damaged answers score at most 1. The linked rubric
provides the complete scoring instructions.

## Real-Case Rubric

Responses are evaluated against the supplied case facts, court outcome and
assigned stance. Each answer receives three integer scores from 0 to 4:

- **A, citation relevance:** whether the selected authority responds to the issue
  and its supporting proposition is explicit.
- **B, constraint extraction:** compliance with the assigned stance, factual
  boundaries, requested subtasks, and format.
- **C, argument validity:** whether the conclusion follows from the cited law and
  facts under the assigned stance.

The case score averages A/B/C. Raw scores are multiplied by 25 for the 0-100 scale;
normalization does not equate difficulty across tracks.

## Scoring Rules and Calibration

The calibrated rubric gives partial credit with score caps: missing legal
authority gives A=0 and caps B/C at 2; B=0 also caps C at 2.

English translations satisfy the language requirement. A wrong stance gives B=0;
serious factual fabrication caps B at 1.

| Stage | Full mean | Share of dimension scores at 3/4 | Lawyer 1 overlap: automatic / human |
| --- | ---: | ---: | --- |
| Initial checklist | 77.3 | 79.8% | 76.8 / 75.5 |
| Strict regrade | 58.0 | 40.0% | 56.3 / 75.5 |
| Calibrated scores | 73.0 | 70.2% | 71.3 / 75.5 |

Full means and score shares describe each stage's evaluated pool; the calibrated
row covers 276 prompts and 28 model configurations. The overlap column compares
the same 200 answers rated by Lawyer 1 across all three stages.

## Automatic Evaluator

Rescoring uses GPT-5.5 (`gpt-5.5`) through the Codex CLI. The evaluator
scores one anonymized answer using the prompt and criteria in a closed-book
setting. Model identity, prior scores and review notes are withheld.

The [reproducibility guide](REPRODUCIBILITY.md#scoring-provenance) records scoring
batches, reference corrections and evaluator settings. Five-run repeatability
analyses are reported in the [results summary](RESULTS_SUMMARY.md#reliability-analyses-and-supplementary-controls).

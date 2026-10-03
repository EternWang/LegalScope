# Scoring Rubric

This document follows Sections 4 and A.5 of the workshop camera-ready paper.

## Public-Exam Scoring

| Score | Anchor |
| ---: | --- |
| 0 | Wrong, irrelevant, or not evaluable. |
| 1 | Generic or only weakly related legal statements. |
| 2 | Relevant legal content applied incompletely. |
| 3 | Correct core direction with some missing elements. |
| 4 | Decisive legal points covered and a compatible conclusion. |

## Real-Case Rubric

Each answer receives three integer scores from 0 to 4:

- **A, citation relevance:** whether the selected authority responds to the issue
  and its supporting proposition is explicit.
- **B, constraint extraction:** compliance with the assigned stance, factual
  boundaries, requested subtasks, and format.
- **C, argument validity:** whether the conclusion follows from the cited law and
  facts under the assigned stance.

The case score averages A/B/C. Raw scores are multiplied by 25 for the 0-100 scale;
normalization does not equate difficulty across tracks.

## Calibration and B-Only Update

The calibrated rubric allows partial credit for usable analysis while retaining
caps for severe failures. No legal authority gives A=0, while B/C may retain
limited credit. B=0 caps C at 2 rather than forcing C to zero.

The B-only update treats English answers as language-compliant. Missing
identifiable authority caps B at 2; a wrong stance gives B=0; serious fabrication
caps B at 1. The B=0 rule required two C corrections. Historical review notes were
not regenerated with B, and lawyer scores remain unchanged; B comparisons remain
subject to rubric-version and language differences.

| Stage | Full mean | Share of dimension scores at 3/4 | Original Lawyer 1 overlap: automatic / human |
| --- | ---: | ---: | --- |
| Initial checklist | 77.3 | 79.8% | 76.8 / 75.5 |
| Strict regrade | 58.0 | 40.0% | 56.3 / 75.5 |
| Calibrated scores | 73.0 | 70.2% | 71.3 / 75.5 |

Historical stages retain their original pools; only the current row covers 276
prompts and 28 models. The overlap column uses the original 200 answers. This table
is not a fixed-sample comparison of rubric changes.

## Automatic Evaluator

Scoring updates use Codex 5.5 through the `gpt-5.5` alias. The evaluator receives
one anonymized answer with the prompt and scoring criteria, without model identity,
prior scores, or review notes, and does not conduct independent legal research.

The alias is not date-pinned; temperature, top-p, and seed are not explicitly set.
Batch configurations differ, and historical scores remain where no update was run.
Updated scores use the first valid result after execution/parsing/schema retries.
Repeated judgments are not averaged into headline scores. Blinding does not rule
out stylistic self-preference; independent human validation remains necessary.

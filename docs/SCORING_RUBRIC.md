# Scoring Rubric

This document follows Sections 4 and A.5 of the workshop camera-ready paper.
The [evaluation directory](../evaluation/README.md) provides machine-readable
rubrics, prompt construction and an executable scorer.

## Public-Exam Scoring

The [released exam scorer](../evaluation/rubrics/exam_aug2026.json) compares
the answer with four reference components: issue, governing rule, application
or exception, and conclusion or remedy. Each substantive match earns one point.

| Score | Reference components matched |
| ---: | --- |
| 0 | None, a clearly opposite core conclusion, or a non-responsive answer |
| 1 | One |
| 2 | Two |
| 3 | Three |
| 4 | All four, with no substantive conflict |

Refusals and structurally damaged answers score at most 1. Matching concerns
substance rather than wording, length or fluency.

## Real-Case Rubric

Models answered the case prompts in Chinese. GPT-5.5 translated their answers into English for scoring; the release contains these English translations.

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

The calibrated rubric gives partial credit with score caps: missing legal
authority gives A=0 and caps B/C at 2; B=0 also caps C at 2.

The B-only update accepts English answers as language-compliant. A wrong stance
gives B=0; serious factual fabrication caps B at 1. Applying the B=0 cap required
two C corrections. Review notes and lawyer ratings retain their earlier versions,
so comparisons across stages depend on rubric and language differences.

| Stage | Full mean | Share of dimension scores at 3/4 | Original Lawyer 1 overlap: automatic / human |
| --- | ---: | ---: | --- |
| Initial checklist | 77.3 | 79.8% | 76.8 / 75.5 |
| Strict regrade | 58.0 | 40.0% | 56.3 / 75.5 |
| Calibrated scores | 73.0 | 70.2% | 71.3 / 75.5 |

Historical stages retain their original pools; only the current row covers 276
prompts and 28 models. The overlap column uses the original 200 answers. This table
is not a fixed-sample comparison of rubric changes.

## Automatic Evaluator

Scoring updates use GPT-5.5 (`gpt-5.5`) through the Codex CLI. The evaluator
scores one anonymized answer using the prompt and criteria in a closed-book
setting. Model identity, prior scores and review notes are withheld.

The alias is not date-pinned; temperature, top-p and seed are unspecified.
Batch configurations differ, and earlier scores remain for answers not rescored.
Updates retain the first valid result after execution or validation retries.
The five-run stability audits are reported separately from headline scores.

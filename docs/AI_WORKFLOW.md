# AI-Assisted Research Workflow

## Pipeline

1. Collect public legal-exam sources and concluded Chinese judgment materials.
2. Parse, normalize, redact, deduplicate, and audit source records.
3. Build exam tasks and paired, closed-book case prompts with human case review.
4. Generate answers across 28 model groups.
5. Score exam answers against references and case answers with the calibrated A/B/C rubric.
6. Validate 2,240 exam answers using human scores and 280 case answers using two lawyers' independent scores.
7. Analyze exam-case association, dimension contrasts, and automatic-human agreement.
8. Audit the current citation-argument contrast with prompt/judgment clusters over
   all 276 prompts, while retaining historical controls and fixed-answer audits as
   separate evidence.

AI tools assist transformation code, normalization, prompt preparation, answer
generation, scoring, and candidate error analysis. Source selection, legal review,
de-identification, interpretation, and release decisions remain human responsibilities.

## Version and Reproducibility

The workshop scoring updates use the non-date-pinned `gpt-5.5` alias, with batch
configuration differences and retained historical scores. See the
[scoring rubric](SCORING_RUBRIC.md) for reproducibility limits. The historical A/C
audit and updated B-only audit each rescore the same 200 fixed answers five times;
they are not a single joint rerun.

## Public Boundary

GitHub provides research documentation, paper figures, aggregate performance,
metadata, and data utilities. Hugging Face provides all 276 case prompts and
matching scoring references, plus 78 Victorian Bar source excerpts. Original
judgments, private workbooks, remaining exam inputs and exam model response text
are not included. The [results release](REPRODUCIBILITY.md) adds case responses,
individual numeric scores, source page locations and evaluation code. See the
[loading guide](USING_THE_RELEASE.md) for the available files and formats.

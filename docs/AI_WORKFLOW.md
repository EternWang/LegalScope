# AI-Assisted Research Workflow

## Pipeline

1. Collect public legal-exam sources and concluded Chinese judgment materials.
2. Parse, normalize, redact, deduplicate, and audit source records.
3. Build exam tasks and paired, closed-book case prompts with human case review.
4. Generate answers across 28 model groups.
5. Score exam answers against references and case answers with the calibrated A/B/C rubric.
6. Validate 2,240 exam answers and 280 case answers against independent review.
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

Documentation, paper figures, high-level metadata, aggregate performance, and
workbook helpers are public. Full workbooks, prompts, model outputs, and human
review sheets remain outside this repository. Generating a local sample does not
establish that its source rights or de-identification permit publication.

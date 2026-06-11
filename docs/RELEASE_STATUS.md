# Release Status

LegalScope is represented here as a public research repository, not a full
artifact release.

## Included

- Benchmark design and evaluation counts.
- Public-safe metadata about sources, rows, model groups, and response counts.
- Selected figures rendered from paper figure sources.
- Public-facing result summaries.
- Scoring, annotation, data-card, provenance, and AI-workflow documentation.
- Lightweight workbook helper utilities.
- A Hugging Face dataset-card release plan.

## Not Included

- Paper draft, review PDF, or LaTeX source files.
- Full benchmark workbook.
- Full prompt matrix.
- Complete reference answers.
- Complete model outputs.
- Human review sheets or adjudication notes.
- Non-de-identified judgments or private source documents.
- Internal API keys, provider logs, or local absolute-path artifacts.

## Recommended Public Release Strategy

1. Keep this GitHub repository as the project and reproducibility scaffold.
2. Publish a Hugging Face dataset repository as a metadata-only public preview.
3. Link the GitHub repository and Hugging Face dataset card after the Hub page is
   live.
4. Add row-level samples only after a separate release review confirms source
   redistribution rights, de-identification quality, and review anonymity.

## Before Any Full Dataset Release

Check:

- source redistribution rights for public-exam materials;
- de-identification and re-identification risk for judgment-derived prompts;
- provider terms for redistributing model outputs;
- whether the review version requires anonymous artifact paths;
- whether repository text, commit history, file names, or public URLs could
  identify a submission during review;
- whether human review sheets contain private notes, names, or hidden evidence
  references.

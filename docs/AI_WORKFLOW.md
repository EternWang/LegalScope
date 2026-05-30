# AI-Assisted Research Workflow

LegalScope uses LLMs as research tools while keeping source selection, legal review,
release decisions, and paper claims under human control.

## Pipeline Overview

1. Collect public legal-exam sources and de-identified civil-judgment materials.
2. Parse, normalize, redact, deduplicate, and audit source records.
3. Build standardized public-exam and real-case prompt templates.
4. Generate model answers across 20 model groups.
5. Score public-exam answers with reference-aware scoring.
6. Score real-case answers with the A/B/C legal-reasoning rubric.
7. Validate selected rows against human legal review.
8. Analyze transfer, human agreement, length effects, and error patterns.

## Where AI Assistance Is Used

AI tools may help draft transformation code, normalize text, prepare prompt templates,
generate model answers under controlled settings, and identify candidate failure modes
for inspection.

AI tools do not replace source-selection decisions, de-identification review, final
legal judgment, manuscript claims, licensing review, or release decisions.

## Safeguards

- De-identification before public release.
- Separate scorer-side references and prompt-facing text.
- Stance and closed-book constraints for real-case prompts.
- Human validation for selected public-exam and real-case rows.
- Public release boundary for full prompts, model outputs, and review sheets.

## Public Repository Boundary

This repository keeps documentation, V2 figure exports, high-level metadata, and small
workbook utilities. Full data and review artifacts remain private until privacy,
licensing, and review constraints are resolved.

# AI-Assisted Research Workflow

LegalScope uses AI systems as research tools while keeping dataset design,
source selection, de-identification, legal review, scoring decisions, release
decisions, and paper claims under human control.

## Pipeline Overview

1. Collect public legal-exam sources and candidate Chinese civil-judgment
   materials.
2. Parse, normalize, redact, deduplicate, and audit source records.
3. Construct public-exam prompts and real-case issue-stance prompts.
4. Generate model answers across 20 model groups.
5. Score public-exam answers with reference-aware 0-4 scoring.
6. Score real-case answers with the citation, constraint, and argument rubric.
7. Calibrate the real-case rubric against human legal review.
8. Analyze exam-to-case transfer, human agreement, score distributions, length
   effects, and error patterns.
9. Prepare public documentation and metadata while withholding sensitive
   artifacts.

## Public-Safe Script Provenance

The Drive public-material folder documents 78 copied and annotated pipeline
scripts grouped into five stages:

| Stage | Scripts | Public-safe description |
| --- | ---: | --- |
| Public bar source collection and cleaning | 16 | Collection, parsing, normalization, duplicate repair, reference repair, and source-audit scripts. |
| Chinese real-case prompt construction | 7 | Judgment preview, issue/stance prompt construction, repair, rerun, and workbook writeback scripts. |
| Model answer generation | 17 | Model catalog, provider runners, batch launchers, answer merge, and answer writeback scripts. |
| Scoring and regrading | 29 | Public-exam scoring, real-case rubric calibration, blind packets, V2 scoring, and validation utilities. |
| Final conversion, translation, and release | 9 | Workbook-to-JSON conversion, English cleanup, metadata repair, and public release packaging. |

Some internal scripts retain absolute paths or require provider credentials.
They should be treated as provenance records and rerun only after path,
credential, privacy, and redistribution checks.

## Where AI Assistance Is Used

AI tools may help:

- draft transformation code;
- normalize and translate text;
- prepare prompt templates;
- generate model answers under controlled settings;
- score answers according to documented rubrics;
- identify candidate failure modes for human inspection;
- prepare release documentation.

## Human-Controlled Steps

AI tools do not replace:

- source-selection decisions;
- privacy and de-identification review;
- legal-domain review;
- final scoring policy;
- human-validation judgments;
- licensing and redistribution decisions;
- paper claims and release decisions.

## Safeguards

- Separate public prompt-facing text from scorer-side references.
- Keep real-case prompts closed-record and stance-constrained.
- Mask names, institutions, identifiers, and other sensitive details before
  public release.
- Validate selected rows with human legal review.
- Preserve a clear public/private release boundary.
- Withhold full prompts, model outputs, human review sheets, and non-de-identified
  source documents until a later release review.

## Public Repository Boundary

This repository includes documentation, selected figures, high-level metadata,
and lightweight helper code. The full data workflow remains private until
privacy, licensing, and review constraints are resolved.

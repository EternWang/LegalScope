# Project Brief

This is a public, application-facing version of the paper introduction. It is written
to explain the project without releasing the full manuscript, full data, model-output
matrix, human review sheets, or private legal materials.

## Motivation

Public legal exams are widely used to evaluate legal reasoning in language models
because they are standardized, scalable, and often come with reference answers. But
real legal work is different: it involves incomplete records, contested facts,
jurisdiction-specific authorities, procedural constraints, and arguments made from a
particular position.

LegalScope asks whether public-exam performance is a good proxy for real-case legal
reasoning, or whether exam success hides failures that appear only when a model must
reason from a controlled case record.

## Benchmark Design

LegalScope has two connected tracks.

| Track | What It Tests | Scale |
| --- | --- | ---: |
| Public legal exams | Reference-aware open-ended legal-exam answering | 868 questions |
| Chinese real cases | Stance-aware legal reasoning over de-identified civil judgments | 76 prompts |

The real-case track is built from 15 de-identified Chinese civil judgments and 38
legal issues. Many issues are converted into paired support/opposition prompts so that
models must reason under an assigned legal stance rather than merely predict the
observed judgment outcome.

## Evaluation

The public-exam track is scored with a reference-aware 0-4 answer-match rubric.

The real-case track is scored on three dimensions:

- citation relevance: whether the cited authority responds to the issue;
- constraint extraction: whether the answer recovers the operative rule conditions and
  factual boundaries;
- argument validity: whether the legal conclusion follows from the cited law and case
  facts under the assigned stance.

The scoring protocol is validated against human legal review on overlapping subsets.

## My Role

I initiated and led the benchmark design, data organization, scoring-protocol design,
evaluation workflow, public repository packaging, and paper framing. The project also
involved weekly research collaboration and legal-domain review for real-case scoring
and validation.

## Main Takeaway

LegalScope shows that public-exam performance partially transfers to real-case legal
analysis, but does not fully predict it. The dominant real-case weakness is not legal
fluency; it is constraint extraction. Models can write plausible legal arguments while
missing the operative facts, procedural conditions, evidence boundaries, or assigned
stance that make the argument legally controlled.

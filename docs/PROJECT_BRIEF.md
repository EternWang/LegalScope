# Project Brief

This is a public, application-facing summary of the paper structure. It explains the
research question, benchmark design, evaluation protocol, and main findings without
releasing the full manuscript, full workbook, model-output matrix, human review sheets,
or private legal materials.

## Introduction

Public legal exams are useful for large-scale model evaluation because they are
standardized, repeatable, and often paired with reference answers. Real legal analysis
is harder to reduce to exam-style scoring: a useful answer must identify controlling
legal conditions, connect them to a bounded fact record, and argue from a specified
stance.

LegalScope asks whether public-exam performance transfers to real-case legal reasoning,
or whether exam success hides failures that only appear when a model must reason from
de-identified civil judgments.

## Benchmark Design

<img src="../assets/figures/paper_collection_pipeline.png" alt="LegalScope benchmark construction pipeline" width="920">

LegalScope has two connected tracks.

| Track | What It Tests | Scale |
| --- | --- | ---: |
| Public legal exams | Reference-aware open-ended legal-exam answering | 868 questions |
| Chinese real cases | Stance-aware legal reasoning over de-identified civil judgments | 76 prompts |

The real-case track is built from 15 de-identified Chinese civil judgments and 38
legal issues. Many issues are converted into paired support/opposition prompts so that
models must construct statute-grounded arguments under an assigned stance rather than
imitate the observed judgment outcome.

## Evaluation Protocol

The public-exam track is scored with a reference-aware 0-4 answer-match rubric.

The real-case track is scored on three dimensions:

- citation relevance: whether the cited authority responds to the issue;
- constraint extraction: whether the answer recovers the operative rule conditions and
  factual boundaries;
- argument validity: whether the legal conclusion follows from the cited law and case
  facts under the assigned stance.

The scoring protocol is validated against human legal review on overlapping subsets.

## Experiments and Results

Across 20 model groups, LegalScope evaluates 17,360 public-exam responses and 1,520
real-case responses. Public-exam scores correlate with real-case scores, but they do
not fully predict real-case performance, ranking changes, or reasoning-mode gains.

See [Results Summary](RESULTS_SUMMARY.md) for the public-facing figures.

## Analysis

The main real-case bottleneck is constraint extraction. Models can often write fluent
legal arguments while missing the operative facts, procedural conditions, evidence
boundaries, or assigned stance that makes the answer legally controlled.

Automated evaluation is more reliable on public-exam answers than on case-based legal
analysis, which is why the benchmark keeps expert-grounded validation in the loop.

## Public Release Boundary

This repository is a public research scaffold. It documents the project clearly enough
for readers to understand the benchmark, but it does not release the full paper,
private workbook, complete prompts, model outputs, human review sheets, or
non-de-identified legal source materials.

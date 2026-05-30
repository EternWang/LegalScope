# Annotation Protocol

## Purpose

The human-validation protocol checks whether automated and model-judge scores align
with human legal review, and whether the failure modes found in real cases differ from
public-exam scoring.

## Human-Scored Subset

| Subset | Items | Model groups | Human-validation responses |
| --- | ---: | ---: | ---: |
| Public legal exams | 80 | 20 | 1,600 |
| Chinese real cases | 10 | 20 | 200 |
| Total | 90 | 20 | 1,800 |

## Review Focus

Human review checks:

- source and reference-answer alignment for public-exam rows;
- issue and stance consistency for real-case rows;
- privacy and de-identification constraints;
- citation relevance;
- constraint extraction;
- argument validity;
- cases where automated scores appear too generous or too punitive.

## Preferred Review Notes

Review notes should be brief and audit-friendly. Useful tags include:

- opposite stance;
- invented facts;
- missing operative constraint;
- weak citation linkage;
- wrong legal domain;
- missed key issue;
- thin rule-to-fact analysis;
- mostly aligned with minor gaps.

## Reliability Reporting

A full public release should report reviewer training, double-coded subset size,
agreement statistics, and adjudication procedure. The public repository does not
include raw human review sheets.

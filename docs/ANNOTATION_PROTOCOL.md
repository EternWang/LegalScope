# Annotation Protocol

## Human-Scored Subset

| Subset | Items | Model groups | Unique answers |
| --- | ---: | ---: | ---: |
| Public legal exams | 80 | 28 | 2,240 |
| Chinese real cases | 10 | 28 | 280 |
| Total | 90 | 28 | 2,520 |

Exam human scores are reviewed and confirmed against the reference answers. For cases, two
practicing Chinese lawyers independently score the same randomized answer set.
Model identities, automatic scores, and the other lawyer's ratings are hidden.
Case reviewers are excluded from benchmark construction; Lawyer 2 is held out from
rubric calibration. The case human endpoint is the equal-weight mean of both
lawyers. Unique-answer counts do not count the two lawyers' ratings separately.

## Review Focus

Review assesses reference alignment for exams, and citation relevance, constraint
extraction, and argument validity for cases. Case curation also checks issue/stance
consistency and de-identification. Useful error-note categories include citation
mismatch, condition omission, fact extrapolation, stance drift, and conclusion jump.
Historical notes were not regenerated with the B-only scoring update and should
not be used as explanations of updated B scores.

## Reliability Reporting

| Endpoint | Answer-level r / rho | Model-level r / rho |
| --- | --- | --- |
| Automatic vs. exam review | 0.910 / 0.898 | 0.948 / 0.963 |
| Automatic vs. pooled case lawyers | 0.312 / 0.235 | 0.703 / 0.459 |

The lawyers' quadratic-weighted kappa is `0.676`, `0.560`, and `0.559` for citation,
constraint, and argument, respectively. Their model-level means correlate at
`r = 0.841`, `rho = 0.711` (paper Section 6.5).

Pooled dimension means are `71.65`, `73.35`, and `76.79`. Argument minus citation
is reported as `5.13` points, with prompt-cluster 95% CI `[-0.94, 11.07]` from
10,000 draws. Both lawyers show the same direction, but the pooled and Lawyer 2
intervals cross zero. The lawyer-scored contrast is descriptive; no consistent
ordering for constraint extraction is claimed.

Individual numeric ratings are included in the [score release](REPRODUCIBILITY.md).
Raw review sheets and adjudication notes are not included.

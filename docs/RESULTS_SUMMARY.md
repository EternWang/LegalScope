# Results Summary

This summary covers the paper's model comparisons and validation analyses.
The main model results are available as [rounded aggregates](../data/metadata/model_performance.csv)
and can be recomputed from [individual scores](REPRODUCIBILITY.md).

## Headline Performance

Across 28 model configurations, the public-exam mean is `72.6` and the real-case
mean is `73.0` on the 0-100 scale.

| Real-case dimension | Mean |
| --- | ---: |
| Citation relevance | 66.9 |
| Constraint extraction | 79.3 |
| Argument validity | 72.6 |

Citation relevance receives a lower mean than argument validity. Tracks and
dimensions use different scoring criteria, so their means are descriptive
comparisons rather than a common difficulty scale.

## Score Distribution

<img src="../assets/figures/paper_score_distribution.png" alt="Scores for all 28 model groups: 861 exam prompts and 276 case prompts per model" width="920">

Constraint extraction has `11.9%` of scores at 2 and `48.9%` at 4; argument validity
has `45.0%` at 3 and `24.7%` at 4. Figure 2 shows these per-answer
score distributions.

## Exam-to-Case Association

<img src="../assets/figures/paper_transfer_model_judge.png" alt="Automatic exam-to-case association, Pearson 0.817 and Spearman 0.708 over 28 groups" width="920">

| Scoring endpoint | Model groups | Pearson | Spearman |
| --- | ---: | ---: | ---: |
| Automatic exam and case means | 28 | 0.817 | 0.708 |
| Human exam and pooled lawyer case means on validation subsets | 28 | 0.696 | 0.690 |

<img src="../assets/figures/paper_transfer_human.png" alt="Human exam and pooled-lawyer case association, Pearson 0.696 and Spearman 0.690 over 28 groups" width="920">

Figure 3 compares exam and case performance, with the diagonal marking equal
normalized scores. The human panel averages the two lawyers' case scores.

The Chinese exam subset gives `r = 0.788`, `rho = 0.704`; the English aggregate
gives `r = 0.813`, `rho = 0.670`. Source and task composition prevent
isolating language or legal-system effects from these comparisons.

Variant differences do not transfer uniformly: GPT-5.5 High exceeds GPT-5.4 Mini by
`2.4` exam points and `9.9` case points, while DeepSeek R1 exceeds DeepSeek V3.2 by
`5.7` exam points but scores `1.5` case points lower. These comparisons mix
checkpoint, size, and reasoning-mode differences; they do not isolate reasoning effort.

## Source and Case Categories

<img src="../assets/figures/paper_jurisdiction_means.png" alt="Exam means: United Kingdom 82.5, United States 74.0, Australia 65.7, China 60.2" width="700">

| Public-exam group | N | Mean |
| --- | ---: | ---: |
| United Kingdom | 86 | 82.5 |
| United States | 603 | 74.0 |
| Australia | 78 | 65.7 |
| China | 94 | 60.2 |

These means describe the sampled sources and formats in each jurisdiction.

| Real-case category | Prompts | Mean |
| --- | ---: | ---: |
| Tort | 80 | 71.9 |
| Contract | 72 | 73.4 |
| Criminal | 54 | 74.0 |
| Intellectual Property | 34 | 73.7 |
| Administrative | 22 | 70.9 |
| Civil Procedure | 8 | 70.3 |
| Property | 6 | 77.7 |

Mean citation relevance is lower than argument validity in all seven
categories. Tort is 29.0% of case prompts; medical-malpractice prompts are 18.1%.

## Human Validation

| Validation set | Answer-level Pearson | Answer-level Spearman | Model-level Pearson | Model-level Spearman |
| --- | ---: | ---: | ---: | ---: |
| Public exams | 0.910 | 0.898 | 0.948 | 0.963 |
| Real cases, pooled lawyers | 0.312 | 0.235 | 0.703 | 0.459 |

The 80-item exam subset contains 2,240 answers; the 10-prompt case subset contains
280 answers. The case human score is the equal-weight mean
of two independent lawyers; Lawyer 2 was held out from rubric calibration.

Pooled lawyer means for citation, constraint, and argument are `71.65`, `73.35`, and
`76.79`. Argument minus citation has a reported gap of `5.13` points and a
prompt-cluster 95% interval of `[-0.94, 11.07]`. Both lawyers show a positive point
estimate; the pooled and Lawyer 2 intervals include zero.

## Reliability Analyses and Supplementary Controls

The citation-argument analysis uses all 276 prompts, 56 judgments, and 28
model configurations (7,728 answers), with 10,000 cluster-bootstrap draws.
The automatic gap is `5.69`, with prompt-cluster 95% CI `[4.51, 6.83]` and
judgment-cluster CI `[4.44, 6.92]`. Giving judgments equal weight yields `6.02`,
CI `[4.84, 7.17]`. Human resampling retains both lawyers and all 28 models within
each of the 10 prompt clusters. Transfer intervals separately resample model
groups and are conditional on the roster, without accounting for family dependence.

The T1 analysis covers 76 case prompts and 20 model configurations. The Tort
control compares 243 exam items with 76 case prompts from 15 judgments across
20 model configurations; its exam–case correlations are `r = 0.807` and
`rho = 0.554`. The 861-item exam benchmark contains 242 Tort items.

The paper also reports supplementary language comparisons, a C-Eval comparison
on 14 model groups, and a nearby-version sensitivity analysis on 10 groups.
Their evaluation scope is documented in the paper's bootstrap analysis and
the [scoring provenance notes](REPRODUCIBILITY.md#scoring-provenance).

The repeatability analyses score the same 200 fixed answers five times. Citation
relevance and argument validity come from joint scoring; constraint extraction
comes from a separate B-only batch. Constraint extraction has `45.0%` exact
agreement, `75.5%` range-at-most-one, mean pairwise QWK `0.802`, and mean answer SD
`0.372`. These analyses estimate scoring variability on fixed answers. Repeated
scores do not enter the headline results.

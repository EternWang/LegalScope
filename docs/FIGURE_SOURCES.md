# Figure Sources

The five figures show the paper's benchmark pipeline and result analyses.
The original exports come from the AIMS at COLM 2026 workshop paper; its PDF
checksum is recorded in
[`dataset_summary.json`](../data/metadata/dataset_summary.json).

| Repository file | Original source |
| --- | --- |
| `assets/figures/paper_collection_pipeline.svg`, `.pdf`, `.png` | Figure 1, page 3. |
| `assets/figures/paper_score_distribution.png` | Figure 2, page 7. |
| `assets/figures/paper_transfer_model_judge.png` | Figure 3(a), page 19. |
| `assets/figures/paper_transfer_human.png` | Figure 3(b), page 19. |
| `assets/figures/paper_jurisdiction_means.png` | Figure 4, page 20. |

Figure 1 is available as SVG, PDF and PNG. Model marks and icon attribution are
listed in [Figure icon sources](FIGURE_ICON_SOURCES.md).

The human transfer plot uses human exam scores and the pooled scores of both lawyers on the
validation subsets to show exam–case association. The 243-item Tort control in
Figure 1 compares 76 case prompts from 15 judgments across 20 model configurations.
The repeatability analyses use 200 fixed, blinded answers from 10 prompts and
20 model configurations, with five repetitions per dimension.
See the [results summary](RESULTS_SUMMARY.md#reliability-analyses-and-supplementary-controls)
for the evaluation scope of each analysis.

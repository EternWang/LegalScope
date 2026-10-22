# LegalScope: Measuring Exam-to-Case Transfer in LLM Legal Reasoning

**AI Measurement Science (AIMS) Workshop at COLM 2026**

[Project page](https://eternwang.github.io/LegalScope/) ·
[Workshop paper](https://openreview.net/forum?id=BNx62Wx1ej) ·
[Hugging Face](https://huggingface.co/datasets/Hongyu801/LegalScope) ·
[Task examples](https://eternwang.github.io/LegalScope/examples.html) ·
[Citation](#citation)

LegalScope evaluates how performance on legal exams relates to reasoning about
real cases. It compares 28 model configurations on 861 exam questions from four
jurisdictions and 276 paired prompts drawn from 56 Chinese judgments.

## Benchmark

<a href="assets/figures/paper_collection_pipeline.png"><img src="assets/figures/paper_collection_pipeline.png" alt="LegalScope benchmark construction, model evaluation and human validation" width="760"></a>

| Component | Count |
| --- | ---: |
| Legal-exam questions | 861 |
| Case prompts: 138 issues × supporting and opposing stances | 276 |
| Deidentified Chinese judgments | 56 |
| Model configurations, including reasoning-effort variants | 28 |

Human validation covers 80 exam questions and 10 case prompts across all 28
configurations. Two lawyers independently score the same 280 case answers.

## Main findings

- Exam and case scores correlate across models: Pearson `r = 0.817`,
  Spearman `rho = 0.708`. Rankings and gains from model variants differ between tracks.
- Mean automatic citation relevance is `66.9`, compared with `72.6` for
  argument validity on a 0–100 scale.
- Automatic and human scores correlate more strongly on exam answers
  (`r = 0.910`) than on case answers (`r = 0.312`, averaging two lawyers).

See the [results](https://eternwang.github.io/LegalScope/results.html) and
[statistical analysis](docs/RESULTS_SUMMARY.md).

## Downloads

| Material | Records | Access |
| --- | ---: | --- |
| Case prompts and matching scoring references | 276 each | [Case data](https://huggingface.co/datasets/Hongyu801/LegalScope/tree/main/data/cases) |
| Victorian Bar source excerpts and selected candidate answers | 78 | [Exam sources](https://huggingface.co/datasets/Hongyu801/LegalScope/tree/main/data/victorian_bar) |
| Case model responses | 7,728 | [Responses](https://huggingface.co/datasets/Hongyu801/LegalScope/tree/main/data/results) |
| Individual automatic and human score records | 34,636 | [Scores](data/results/answer_scores.csv.gz) |
| Aggregate performance and model roster | 28 each | [Metadata](data/metadata) |

The downloadable exam source subset covers 78 of the 861 evaluation items.
Case prompts and references are separate tables joined by `review_id`.

Case models answered in Chinese. GPT-5.5 translated the answers into English, and the English translations were scored. The released case responses are these English translations.

Start with the [loading guide](docs/USING_THE_RELEASE.md) for dataset examples,
field definitions and version pinning.

## Reproduce and evaluate

```sh
python -m pip install -e .
python -m legalscope.results \
  --scores data/results/answer_scores.csv.gz \
  --roster data/metadata/model_groups.csv \
  --published data/metadata/model_performance.csv
```

This recomputes all 252 values in workshop Table 3 from individual scores.

| Topic | Guide |
| --- | --- |
| Counts, sources and intended use | [Data card](docs/DATA_CARD.md) |
| Response and score fields | [Reproducibility](docs/REPRODUCIBILITY.md) |
| New generation and scoring runs | [Evaluation](evaluation/README.md) |
| Scoring dimensions and human validation | [Rubric](docs/SCORING_RUBRIC.md), [annotation protocol](docs/ANNOTATION_PROTOCOL.md) |
| Model configurations | [Model settings](docs/MODEL_SETTINGS.md) |
| Case fields and legal reference sources | [Case data](docs/CASE_RELEASE.md), [reference sources](docs/CASE_REFERENCE_NOTES.md) |

## Licenses

Project-authored code, documentation, metadata and case annotations use
[MIT](LICENSE). Victorian Bar excerpts retain **CC BY-NC-ND 4.0**, with their
attribution and notices; see [third-party notices](THIRD_PARTY_NOTICES.txt).
Original judgments and the remaining 783 exam inputs are outside the data release.

## Citation


```bibtex
@inproceedings{wang2026legalscope,
  title = {{LegalScope}: Measuring Exam-to-Case Transfer in {LLM} Legal Reasoning},
  author = {Wang, Hongyu and Han, Rilyn R. and Zhao, Yilun and Zhao, Xuandong and Cohan, Arman},
  booktitle = {AI Measurement Science Workshop at COLM 2026},
  year = {2026},
  url = {https://openreview.net/forum?id=BNx62Wx1ej}
}
```

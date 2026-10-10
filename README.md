# LegalScope: Measuring Exam-to-Case Transfer in LLM Legal Reasoning

**AI Measurement Science (AIMS) Workshop at COLM 2026**

[Project page](https://eternwang.github.io/LegalScope/) ·
[Paper (PDF)](https://drive.google.com/file/d/1I3nfb16wuCmj-i2bo6rM5MU0A9sJ-FZx/view) ·
[Workshop record](https://openreview.net/forum?id=BNx62Wx1ej) ·
[Hugging Face](https://huggingface.co/datasets/Hongyu801/LegalScope) ·
[Results](docs/RESULTS_SUMMARY.md) · [Data card](docs/DATA_CARD.md) ·
[Version notes](docs/RELEASE_STATUS.md) · [Citation](#citation)

LegalScope asks whether strong public legal-exam scores transfer to real-case legal
reasoning. It pairs public exams from four jurisdictions with supporting and
opposing prompts derived from deidentified Chinese judgments and reviewed by lawyers.

This repository accompanies the **AIMS at COLM 2026 workshop paper**. It provides
documentation, figures, individual and aggregate scores, model responses, and evaluation code.
Reported scores cover 28 model groups; the data release does not change them.
The PDF link opens the current manuscript; the workshop record and citation
identify the published AIMS version.

**Downloadable now:** all 276 deidentified case prompts with 276 separately
packaged scoring references, 78 Victorian Bar source excerpt records
with selected candidate answers, and benchmark metadata. Start with the
[case dataset](https://huggingface.co/datasets/Hongyu801/LegalScope/viewer/case_prompts/test)
and the [loading and field guide](docs/USING_THE_RELEASE.md).
[Official reference sources](docs/CASE_REFERENCE_NOTES.md) accompany the updated citations.
The release also includes **7,728 case model responses**, **34,636 individual score records**,
and [code to reproduce the main results](docs/REPRODUCIBILITY.md).

## Benchmark at a Glance

<a href="assets/figures/paper_collection_pipeline.png"><img src="assets/figures/paper_collection_pipeline.png" alt="LegalScope construction, evaluation, human validation, and reliability audit pipeline for 28 model groups" width="760"></a>

| Component | Count |
| --- | ---: |
| Public legal-exam questions | 861 |
| Real-case issue-stance prompts | 276 |
| De-identified Chinese judgments | 56 |
| Legal issues, each with support and opposition prompts | 138 |
| Model groups evaluated | 28 |
| Public-exam model responses | 24,108 |
| Real-case model responses | 7,728 |
| Total dataset model responses | 31,836 |
| Unique human-validation responses | 2,520 |

Human validation covers 80 exam items (2,240 answers) and 10 case prompts (280
answers). Two lawyers score the same case answers; their ratings do not double the
unique-answer count. Historical controls and fixed-answer audits in the pipeline
are separate from the full benchmark; see the [results](docs/RESULTS_SUMMARY.md).

## Main Findings

- Exam and case scores are associated across the 28 model groups: Pearson
  `r = 0.817`, Spearman `rho = 0.708`. Rankings and variant gains do not transfer
  uniformly between the tracks.
- Mean scores are `72.6` for public exams and `73.0` for real cases on the 0-100
  scale. The tracks use different scoring protocols; these means do not equate
  their difficulty.
- Citation relevance averages `66.9`, below argument validity at `72.6`.
  Lawyers show the same direction descriptively, but the pooled lawyer gap's
  95% interval crosses zero. This is not evidence of a universal dimension ordering.
- Automatic scoring agrees more strongly with human review on exam answers
  (`r = 0.910`) than case answers (`r = 0.312`, pooled lawyers).

## Explore the Project

| Topic | Resource |
| --- | --- |
| Research question and benchmark design | [Project brief](docs/PROJECT_BRIEF.md) |
| Findings, figures, and uncertainty | [Results summary](docs/RESULTS_SUMMARY.md) |
| Counts, sources, and intended use | [Data card](docs/DATA_CARD.md) |
| Downloads, field meanings, answer types, and examples | [Using the release](docs/USING_THE_RELEASE.md) |
| Reference-answer scoring and calibrated case rubric | [Scoring rubric](docs/SCORING_RUBRIC.md) |
| Reproduce Table 3 or run a new evaluation | [Results reproduction](docs/REPRODUCIBILITY.md), [evaluation code](evaluation/README.md) |
| Human scores and lawyer agreement | [Annotation protocol](docs/ANNOTATION_PROTOCOL.md) |
| Model roster and paper Table 3 | [Model groups](data/metadata/model_groups.csv), [aggregate performance](data/metadata/model_performance.csv) |
| Machine-readable composition | [Dataset summary](data/metadata/dataset_summary.json), [source composition](data/metadata/source_composition.csv) |
| Figure provenance and version history | [Figure sources](docs/FIGURE_SOURCES.md), [release status](docs/RELEASE_STATUS.md) |

## Code and Reproducibility

Start with the [loading guide](docs/USING_THE_RELEASE.md) to download case
prompts, join their scoring references, or analyze published scores.

The repository provides score aggregation, response generation, anonymous scoring,
data conversion, website generation, and reference comparison utilities. The workbook inspector and legacy sample
extractor support local spreadsheet exploration; their preview outputs are
separate from the published benchmark files.

Install the utilities and run the checks:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

For the reviewed public Hugging Face package, `scripts/prepare_hf_tables.py`
creates lossless Parquet loader tables from the original CSV/JSONL files. Install
`python -m pip install -e ".[release]"`, then run
`python scripts/prepare_hf_tables.py --package-dir /path/to/reviewed-package`.
The utility verifies source/case manifests, case-reference joins and paired
stances, and round-trips every converted value;
it does not extract new data from a private workbook or clear new source rights.

The [reproduction command](docs/REPRODUCIBILITY.md) recalculates all 252 main-table
values from the released individual scores. The [evaluation guide](evaluation/README.md)
provides runnable generation and scoring examples, archived rubrics and available
run configurations. Original provider transcripts, remaining exam inputs and the
complete historical execution environment are outside the release.

The [model settings reference](docs/MODEL_SETTINGS.md) covers all 28 groups,
with current provider defaults, model release configurations and official sources.

## Public Release Boundary

The complete benchmark is larger than the downloadable release. The repository
contains metadata and aggregate results; the project page also shows an attributed
Victorian Bar question-and-answer excerpt under **CC BY-NC-ND 4.0**. That excerpt
is not covered by this repository's MIT license. See
[third party notices](THIRD_PARTY_NOTICES.txt).

The [Hugging Face release](https://huggingface.co/datasets/Hongyu801/LegalScope)
provides six separate Parquet configurations: case prompts, case
references, exam source excerpts, model scores, the roster, and source composition.
Original CSV/JSONL files remain downloadable. The 276 case prompts match the
final workbook; scoring references include updated citations and official source links. See the [case release](docs/CASE_RELEASE.md).

The 78 Victorian Bar excerpts retain their CC BY-NC-ND 4.0 license and notices;
the other 783 exam records are not cleared for this source-text release.
Project authored case annotations retain MIT, without granting rights to the
excluded source judgments. Additional response, score and PDF page-location files
are available alongside the six viewer configurations.

Case model responses and individual numeric scores are available. Exam model
outputs, raw lawyer review sheets, source judgments, private workbooks and the
manuscript source package are not published. The paper is linked
above. See [release status](docs/RELEASE_STATUS.md) for details.

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

LegalScope is a research benchmark, not legal advice or a substitute for
jurisdiction-specific legal review.

For a new reference comparison, use the [offline preparation and validation guide](docs/REFERENCE_REVIEW.md).

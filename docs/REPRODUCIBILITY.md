# Results and reproducibility

The release contains the individual scores needed to reproduce all 252 values
in the paper's main model table. It also provides the 7,728 stored case responses,
evaluator rubrics, a scoring runner, and response generation utilities.

## Reproduce the model table

From the repository root:

```sh
python -m pip install -e .
python -m legalscope.results \
  --scores data/results/answer_scores.csv.gz \
  --roster data/metadata/model_groups.csv \
  --published data/metadata/model_performance.csv
```

The command checks item coverage, model identities, duplicate records, score
ranges, the two lawyers' shared subset and all nine metrics for each model.
Its output reports `models: 28`, `values_checked: 252`, and `differences: []`.
No model calls are needed.

## Individual score records

[answer_scores.csv.gz](../data/results/answer_scores.csv.gz) is a compressed CSV
with 34,636 rows. The same file is available on
[Hugging Face](https://huggingface.co/datasets/Hongyu801/LegalScope/tree/main/data/results).

| Track | Evaluation | Rows | Coverage |
| --- | --- | ---: | --- |
| `exam` | `automatic` | 24,108 | 861 items × 28 models |
| `case` | `automatic` | 7,728 | 276 prompts × 28 models |
| `exam` | `exam_review` | 2,240 | Human scores for 80 items × 28 models |
| `case` | `lawyer_1` | 280 | Human scores for 10 prompts × 28 models |
| `case` | `lawyer_2` | 280 | Human scores for the same case subset |

Each row is identified by `track`, `evaluation`, `item_id`, and `model_group`.
Exam rows use integer `score`; case rows use integer `A`, `B`, and `C`.
All values are on the original 0–4 scale. Fields for the other track are empty.
`answer_sha256` identifies the stored answer text in the corresponding score
sheet. Text versions used in automatic and human evaluation can have different
hashes, including translated or formatted versions; the hash is not an item ID.
Join score endpoints by item ID and model, retaining the evaluation label.

Exam means and each case dimension are multiplied by 25. The case mean gives
equal weight to A, B and C. Human case means give equal weight to the two lawyers.
Overall means give equal weight to the exam and case tracks, rather than weighting
by their different numbers of questions. Comparison with the paper allows its
one decimal rounding. These averages do not equate difficulty across tracks.

## Case model responses

[case_model_responses.parquet](https://huggingface.co/datasets/Hongyu801/LegalScope/resolve/main/data/results/case_model_responses.parquet)
contains one stored answer for every case prompt and model group.
Fields are `item_id`, `model_group`, `response`, and `answer_sha256`.
Join `item_id` to `review_id` in the case prompt and reference configurations.
The response and individual score files were published at Hugging Face revision
`ae2090d802ee887f972e0e983103fef8c6339722`.

```python
import pandas as pd

scores = pd.read_csv("data/results/answer_scores.csv.gz")
answers = pd.read_parquet("case_model_responses.parquet")
case_scores = scores.query("track == 'case' and evaluation == 'automatic'")
joined = answers.merge(case_scores, on=["item_id", "model_group", "answer_sha256"],
                       validate="one_to_one")
assert len(joined) == 7728
```

The `response` field contains the English translation used for scoring;
see the [translation protocol](SCORING_RUBRIC.md#evaluation-workflow).

These are evaluated model outputs and can contain legal or factual errors.
Every released answer hash matches its automatic score record.

## Reading the results table

The website shows seven track and dimension columns; CSV and Parquet also include
the two equal-weight overall means. Scores use a 0–100 scale. Automatic scores
cover all items; human scores cover 80 exam questions and 10 case prompts, with
case ratings averaged across two lawyers.

Bold and underlined values mark the highest and second-highest displayed values
within each column across all 28 groups. Ties share a mark, and filtering keeps
those full-roster ranks. The initial row order follows the paper's main model table.
These highlights describe the displayed scores, not statistical significance;
the two tracks use different scoring protocols and difficulty scales.
See the [results analysis](RESULTS_SUMMARY.md) for confidence intervals, including
the lawyer-rated citation–argument difference.

## Source locations

[exam_source_locations.jsonl](../data/metadata/exam_source_locations.jsonl)
locates all 78 Victorian Bar records in their original PDFs. Its 213 entries
cover background segments, separately transcribed questions where present,
and selected candidate answer excerpts. Pages are one-based PDF page numbers,
which may differ from printed page labels. Each entry links directly to the
relevant page. Use this index for source page locations and dataset document
IDs for record grouping.

## Scoring provenance

Reported exam responses and scores were produced before subsequent prompt and
reference-text repairs. The 78 released Victorian Bar records reproduce publisher
excerpts rather than those evaluation inputs.

Published case results combine A/C scores with separately scored B values. The
B-only rubric treats English translations as language-compliant. Applying its
B=0 cap required two corrections to C. Review notes were not regenerated with B,
and lawyer ratings were unchanged; the notes therefore do not explain the B-only
scores. Comparisons across scoring stages reflect both rubric and language
differences.

Rescoring uses GPT-5.5 through the `gpt-5.5` alias, which is not date-pinned.
Temperature, top-p and seed were not explicitly set. Batch configurations differ,
and answers without a rescoring run retain their recorded scores. Each rescore is
the first valid result after execution, parsing or validation retries. Repeated
judgments are not averaged into headline results.

The five-run repeatability analyses use the same 200 fixed answers. A/C values
come from a joint-scoring batch and B values from a separate B-only batch. Their
execution settings do not reproduce every benchmark scoring batch. The Tort
control uses 243 exam items and 76 case prompts from 15 judgments across 20 model
configurations. The supplementary language and C-Eval controls use a case endpoint
separate from the full 276-prompt, 28-model evaluation.

Ten public case references contain [citation corrections](CASE_REFERENCE_NOTES.md)
added after evaluation. Re-evaluating answers with those references can change
scores. The released individual scores preserve the results reported in the paper.

## New evaluations

The [evaluation guide](../evaluation/README.md) explains response generation,
anonymous task preparation and scoring. The three rubric files cover
joint A/B/C scoring, B-only scoring and exam answer matching. Generation
settings are available for the eight groups in the August model expansion.
The [model settings reference](MODEL_SETTINGS.md) records provider defaults
checked on 9 October 2026 for all 28 model groups.

For a new run, record the dataset revision, translation and evaluator settings,
provider route and execution date. Model aliases and reference revisions can
change outputs. See [release scope](DATA_CARD.md#public-release-and-intended-use)
for available inputs and responses.

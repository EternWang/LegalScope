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

These are model responses, not reference answers. They may contain incorrect
law, unsupported facts, refusals or other errors. Text is preserved from the
final evaluation workbook, including translated versions; it is not a collection
of original provider transcripts. Every released answer hash matches its
automatic score record. Original judgments, identifying source mappings and
the full exam response collection are not included.

## Source locations

[exam_source_locations.jsonl](../data/metadata/exam_source_locations.jsonl)
locates all 78 Victorian Bar records in their original PDFs. Its 213 entries
cover background segments, separately transcribed questions where present,
and selected candidate answer excerpts. Pages are one-based PDF page numbers,
which may differ from printed page labels. Each entry links directly to the
relevant page. An empty question field does not receive an invented location.
Dataset document IDs are not original exam question numbers.

## New evaluations

The [evaluation guide](../evaluation/README.md) explains response generation,
anonymous task preparation and scoring. The three archived rubric files cover
joint A/B/C scoring, the B-only update and exam answer matching. Recovered
generation settings cover the eight groups in the August model expansion.
The [model settings reference](MODEL_SETTINGS.md) provides current provider
defaults and official sources for the full 28-group roster.

Recomputing stored scores reproduces the published model table. New generation
or scoring runs use their own dataset revision and evaluator configuration;
provider aliases, translated text, updated references and retained historical
scores prevent a promise of identical new outputs. The remaining 783 exam inputs,
the complete historical provider environment and raw human review documents are
outside this release. Numeric human scores are included.

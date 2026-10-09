# Using the public release

## Start with the material you need

| Material | Downloadable now | Relation to the paper |
| --- | ---: | --- |
| Victorian Bar source excerpts and selected candidate answers | 78 records | Source material for part of the 861-item exam track; not the exact evaluation inputs |
| Model performance | 28 rows | Nine rounded scores per model, including two descriptive overall means |
| Model roster | 28 rows | Display names and paper indices |
| Source composition | 30 rows | Overlapping breakdowns of the full benchmark, not additional examples |
| Case prompts | 276 records | Full prompt text preserved from the final workbook |
| Case scoring references | 276 records | Join by `review_id`; authorities/propositions/constraints, not unique gold answers; see official source links |

The Hub may report **716 rows** across six configurations: 276 case prompts,
276 matching references, 78 source records and 86 metadata rows. There are 354
prompt/source records, not 716 questions. Case configurations use `test` for
evaluation; no train/development partitions are supplied. The source subset uses
`source`. Metadata uses `train` as a loader convention, not a training set.

## Load case prompts

```python
from datasets import load_dataset

revision = "3f2126c5c4b0842872311c2e71c00e300a9ae776"
prompts = load_dataset("Hongyu801/LegalScope", "case_prompts", split="test", revision=revision)
references = load_dataset("Hongyu801/LegalScope", "case_scoring_references", split="test", revision=revision)
by_id = {r["review_id"]: r for r in references}
assert len(prompts) == len(by_id) == 276
print(prompts[0]["prompt"])
print(by_id[prompts[0]["review_id"]]["reference_status"])
```

Read the [complete case field guide](CASE_RELEASE.md) and
[reference notes](CASE_REFERENCE_NOTES.md) before running a new evaluation.
The reference table is not part of the model input.

For a new evaluation, submit each record's complete `prompt` and retain its
`review_id` alongside the model response. Use the same pinned revision for the
prompts and references. Record your generation and evaluator settings, and report
new scores separately from the paper's results. The
[offline comparison utility](REFERENCE_REVIEW.md) prepares responses and
validates returned scores; it does not generate or judge answers.

Prompts from the same judgment share facts, and each issue has two assigned
stances. If creating your own training, development, or test partitions, keep
all records with the same `document_id` together to avoid overlap between
partitions. No such partitions are supplied by this release.

## Load and inspect a source record

Install `datasets`, then explicitly select the source configuration. This example
pins a dataset version so a later update does not change
the files used in an analysis.

```python
from datasets import load_dataset

revision = "3f2126c5c4b0842872311c2e71c00e300a9ae776"
excerpts = load_dataset(
    "Hongyu801/LegalScope", "victorian_bar_source_excerpts",
    split="source", revision=revision,
)
assert len(excerpts) == 78
record = excerpts[0]
print(record["item_id"], record["source_url"])
for part in record["source_background_excerpts"]:
    print(part)
if record["source_question_excerpt"]:
    print(record["source_question_excerpt"])
print(record["source_reference_answer_excerpt"])
print(record["excerpt_note"])
```

For scores use `"model_performance", split="train"`; for the roster use
`"model_roster", split="train"`; for composition use
`"source_composition", split="train"`. Keep the same revision when comparing
files. Record the revision in your own results. Original CSV and JSONL downloads
remain in the Hub Files tab, alongside lossless Parquet copies.

## Source-record fields

All fields are strings except `source_background_excerpts`, which is a list of
strings in source order.

| Field | Meaning |
| --- | --- |
| `item_id` | Unique LegalScope item ID; retained for reporting corrections |
| `document_id` | Dataset document grouping; not a PDF page or question number. The 78 records have 74 such IDs but come from only three publications |
| `jurisdiction` | Source jurisdiction, Australia for this subset |
| `exam_date` | Source exam date in `YYYY-MM-DD` format |
| `publisher`, `source_url` | Original publisher and full source publication |
| `source_background_excerpts` | Original context excerpts; may also contain the question |
| `source_question_excerpt` | Separately transcribed original question, where available; intentionally empty in 22 records |
| `source_reference_answer_excerpt` | Selected candidate answer excerpt reproduced by the publisher; not a model-generated answer or guaranteed error-free gold answer |
| `reference_answer_type` | Explicit statement of that answer's origin and limitations |
| `source_license`, `license_url`, `copyright_notice` | License, license link, and attribution that accompany the source text |
| `excerpt_note`, `transcription_note` | Omitted context, non-contiguous excerpts, and technical transcription information |
| `endorsement_note`, `warranty_notice` | Publisher non-endorsement and warranty notices |

The 22 empty question fields are intentional: the workbook field was an editorial
summary, while the original question is already present in the background
excerpts. Do not discard these records as unanswered or fill them with generated
text. EXTVICBAR04B contains two non-contiguous background excerpts; consult its
note and source publication instead of treating them as a continuous passage.
Per-record PDF page and original question-number fields are not yet supplied.

## Keep three kinds of answers separate

- **Source candidate answer:** the Victorian Bar's selected exam response. It can
  contain errors or omissions and is reproduced with its original wording.
- **Evaluator reference:** legal authorities, propositions, and task constraints
  used to assess a case response. It is not necessarily a single ideal answer.
- **Model response:** what an evaluated model produced. The website's RV038
  excerpt is one such response and illustrates unsupported factual additions;
  the full model response matrix is not included in this release.

Case prompts ask for support or opposition on a legal issue. The task is to argue
within the supplied facts and assigned stance, not simply predict the court's
decision. A response may receive different citation, constraint, and argument
scores; those dimensions should not be collapsed into a claim of legal accuracy.

## Scores and reproducibility

All published scores are normalized to 0–100. `public_exam_auto` covers 861 items;
`real_case_auto` covers 276 prompts and averages `citation`, `constraint`, and
`argument`. Human columns cover 80 exam items and 10 case prompts, respectively;
the case endpoint averages the two lawyers. `overall_auto` and `overall_human`
are descriptive equal-weight means of the two tracks, not equated ability scales.
They are included in CSV/Parquet; the website shows the seven track/dimension
columns. Values retain one decimal rounding, so averaging displayed values may
differ by 0.1 from a published aggregate.

The model table contains the 252 score values from Table 3 in the linked
workshop paper.

You can inspect sources, analyze the published aggregate scores, and build the
website with this release. Reproducing the paper's complete evaluation also
requires the exact evaluation inputs, model responses, scoring implementation
and run settings, and human-review data that are not supplied here. New results
on the source excerpt subset must be labeled as a separate evaluation; the
paper's scores were not rerun on this package.

## Case publication status

All 276 case prompts and 276 matching scoring references are available.
See [case sources and fields](CASE_RELEASE.md) and the
[official reference sources](CASE_REFERENCE_NOTES.md). Prompt text and reported
scores are unchanged; reference citations include the supplied source links. Original
judgments, identifying mappings and the full model response matrix are excluded.

## Licenses and corrections

Project authored code, documentation, metadata, and case prompt/reference annotations retain MIT; rights in excluded original judgments are not granted. The Victorian Bar
source text retains CC BY-NC-ND 4.0, including its noncommercial and no-derivatives
conditions; the MIT license does not override it. Keep the per record notices.

For data or loading errors, open a
[GitHub issue](https://github.com/EternWang/LegalScope/issues) with the item ID,
configuration, revision, and a description. Do not include private case files or
identifying personal information in a public issue.

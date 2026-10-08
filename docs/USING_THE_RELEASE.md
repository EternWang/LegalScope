# Using the public release

## Start with the material you need

| Material | Downloadable now | Relation to the paper |
| --- | ---: | --- |
| Victorian Bar source excerpts and selected candidate answers | 78 records | Source material for part of the 861-item exam track; not the exact evaluation inputs |
| Model performance | 28 rows | Nine rounded scores per model, including two descriptive overall means |
| Model roster | 28 rows | Display names and paper indices |
| Source composition | 30 rows | Overlapping breakdowns of the full benchmark, not additional examples |
| Full case prompt/answer dataset | 0 of 276 prompts | Not released as a dataset; RV038 on the website is an abbreviated worked example |

The Hub may report **164 total rows** across its four configurations. This adds
78 source records to 86 metadata rows; it does not mean 164 questions. The paper
evaluates 861 exam items and 276 case prompts. Metadata configurations use the
loader split name `train`, but contain no training examples. The source subset
uses `source`; no train/validation/test partition is supplied for it.

## Load and inspect a source record

Install `datasets`, then explicitly select the source configuration. This example
pins the verified data release so a later documentation update does not change
the files used in an analysis.

```python
from datasets import load_dataset

revision = "2d09713c9e3440226f0db079694d82016fa15b9e"
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
| `document_id` | Internal workbook document grouping; not a PDF page or question number. The 78 records have 74 such IDs but come from only three publications |
| `jurisdiction` | Source jurisdiction, Australia for this subset |
| `exam_date` | Source exam date in `YYYY-MM-DD` format |
| `publisher`, `source_url` | Original publisher and full source publication |
| `source_background_excerpts` | Original context excerpts; may also contain the question |
| `source_question_excerpt` | Separately transcribed original question, where available; intentionally empty in 22 records |
| `source_reference_answer_excerpt` | Selected candidate-answer excerpt reproduced by the publisher; not a model-generated answer or guaranteed error-free gold answer |
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
  the full model-response matrix is not included in this release.

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
columns. Values retain one-decimal rounding, so averaging displayed values may
differ by 0.1 from a published aggregate.

The model table is Table 3 in the linked workshop paper and Table 4 in the
manuscript checked on October 8, 2026. The 252 displayed values agree. The public
citation remains the workshop record.

You can inspect sources, analyze the published aggregate scores, and build the
website with this release. Reproducing the paper's complete evaluation also
requires the exact evaluation inputs, model responses, scoring implementation
and run settings, and human-review data that are not supplied here. New results
on the source-excerpt subset must be labeled as a separate evaluation; the
paper's scores were not rerun on this package.

## Case publication status

The 276 case prompts are **not yet released**, rather than categorically barred
from publication. Original court decisions, project-authored prompts/references,
third-party commentary, and model outputs have different publication questions.
The lack of a Creative Commons label on an original judgment is not by itself a
reason to withhold a project-authored case prompt. See Article 5 of the
[Copyright Law](https://www.ncac.gov.cn/xxfb/flfg/flfg_532/202103/t20210309_50530.html).

The remaining review checks each proposed prompt **and answer** for source
provenance, direct identifiers and combinations of facts that could identify a
person; output-provider terms must also be checked for any model-response release.
Removing names is evidence of de-identification, not proof of anonymization.
Dates or medical facts are review signals, not automatic exclusion rules. The
[Personal Information Protection Law, Articles 4 and 73](https://www.miit.gov.cn/zwgk/zcwj/flfg/art/2022/art_04a0f1fb5df244e39688fd5372623a8d.html)
distinguishes these concepts.

A future case release should record decisions per item, publish cleared items,
and identify the concrete unresolved issue for any withheld item. The present
release does not claim that this full review is complete. If anonymization
changes an evaluated prompt or answer, preserve the original privately and
identify the changed public version; do not silently associate historical scores
with modified inputs. Legally relevant facts and score explanations should not
be removed merely to make a screening rule pass.

## Licenses and corrections

Project-authored code, documentation, and metadata retain MIT. The Victorian Bar
source text retains CC BY-NC-ND 4.0, including its noncommercial and no-derivatives
conditions; the MIT license does not override it. Keep the per-record notices.

For data or loading errors, open a
[GitHub issue](https://github.com/EternWang/LegalScope/issues) with the item ID,
configuration, revision, and a description. Do not include private case files or
identifying personal information in a public issue.

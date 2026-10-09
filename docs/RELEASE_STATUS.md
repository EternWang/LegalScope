# Release Status

## Case data: October 9, 2026

This release adds 276 case prompts and 276 matching historical scoring references
on Hugging Face. They cover 56 judgments and 138 issues with paired supporting
and opposing positions. Case prompts are the default dataset view.

Six configurations contain 716 rows: 276 prompts, 276 references, 78 exam source
records and 86 metadata rows. Reference and metadata rows are not extra questions.
Original input and reference text, the 78 exam source records and all 252 reported
score values are unchanged. Version and reference issue fields are added.

RV025 has an unspecified statute edition; RV026 also has a nursing fee article
mismatch. The [reference notes](CASE_REFERENCE_NOTES.md) explain both. Scores have
not been rerun, and the effect of this issue on scoring has not been measured.

[Case sources and fields](CASE_RELEASE.md) · [Loading guide](USING_THE_RELEASE.md) ·
[File hashes](../data/metadata/case_release_manifest.json)

Earlier entries describe the release available on each date.

## Release Documentation Clarification: October 8, 2026

The website and dataset card now distinguish the 78 downloadable source records
from the full benchmark and the 86 metadata rows. The Hub's default configuration
is the source-excerpt subset; explicit configuration names and all data files
remain unchanged. The [release guide](USING_THE_RELEASE.md) documents all source
fields, the 22 intentionally empty question fields, candidate versus model
answers, pinned loading, and what the public package can reproduce.

Case publication is described as an item-level review, not a blanket prohibition
or a requirement to find a Creative Commons license for each original judgment.
No new case prompts, answers, or other source records are published by this
documentation update. Per-record PDF-page/question locators and a dedicated
private feedback channel are not supplied by this update.

## Public Package and Code Checks: October 8, 2026

The canonical Hugging Face repository is now
[Hongyu801/LegalScope](https://huggingface.co/datasets/Hongyu801/LegalScope).
The reviewed release is commit
[`2d09713`](https://huggingface.co/datasets/Hongyu801/LegalScope/commit/2d09713c9e3440226f0db079694d82016fa15b9e).
The earlier Hongyu513 repository is retained as a historical metadata preview;
active project links and loading examples use Hongyu801.

This release contains 78 Victorian Bar source-excerpt records, selected candidate
answers, per-record notices, a source manifest, and benchmark metadata. All four
Hub configurations use Parquet: 28 model results, 28 roster records, 30 composition
rows, and 78 source records. The original CSV/JSONL files remain available. The
storage conversion was checked field-for-field and does not change source text.
Using one loader format fixes the failure caused by mixing CSV and JSONL configs.

Code checks also found and fixed unsafe legacy export defaults, a zero-size
sample exporting every row, and build output paths overlapping source/data
directories. Export previews now stay in a private or external empty directory;
the site builder validates finite score values and the complete model roster.
Fresh-clone installation includes the local helper package. CI now builds the
site and checks JavaScript syntax as well as running Python tests.

The checks concern the public utilities, website, and reviewed release package.
They do not rerun the private generation/scoring pipeline or reproduce all paper
experiments. Unreviewed exam sources, case records, and private workbooks remain
outside this release.

## Content and Project Page Review: October 8, 2026

The subsequent presentation update adds worked exam/case examples, including
RV038's given facts, assigned task, stored model-answer excerpt and recorded
4/1/3 rubric scores. Model results now have grouped automatic/human headings,
per-column best (bold) / second-best (underlined) emphasis, with shared marks
for tied displayed scores. Table/card shadows, diagonal patterns and score-cell
color fills have been removed following presentation review. All reported score values are unchanged. The
Hugging Face source-excerpt package is now published after the checks above.

The current manuscript and the final source workbook were checked. The benchmark
still contains **861 exam items, 276 case prompts, 56 judgments, 138 issues and
28 model groups**. All 252 published aggregate score values match the current
manuscript. This is a content check, not a new experiment or a claim of a new
publication venue; the public citation remains the workshop record below.

A final check also re-aggregated the stored automatic scores and both lawyers'
case scores from the final workbook. All 252 displayed values agree within the
paper's one-decimal rounding precision. Workbook model blocks were aligned with
the paper roster; legacy header labels were recorded, and the additional model
block outside that roster was excluded. This verifies the stored-score summaries,
not the identity of past API calls or a rerun of the scoring process. The model
performance table is Table 3 in the workshop paper and Table 4 in the current
manuscript; documentation references retain the public workshop numbering.

The project page now uses a centered academic heading, a narrower text column,
consistent section headings and lighter section backgrounds. Figure 1 retains its
original content and aspect ratio; its display width is capped at 760 pixels and
links to the full-resolution image. The current abstract is used. The unverified
exam excerpt was replaced with an attributed Victorian Bar excerpt.

Layout references inspected: [CourtReasoner, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1787/)
(paper page 3 and [repository](https://github.com/Yale-NLP/CourtReasoner)),
[LEXam](https://lexam-benchmark.github.io/) and
[LegalBench](https://hazyresearch.stanford.edu/legalbench/). CourtReasoner's paper
and repository were inspected directly; no separate project website was linked
in those inspected sources. These references inform layout, not LegalScope's
data permissions or reported findings.

### Source-specific data release

| Material | Current status |
| --- | --- |
| Benchmark metadata, aggregate scores and research documentation | Public on GitHub and Hugging Face |
| Victorian Bar source excerpts and selected candidate answers, 78 items | Published on Hongyu801/LegalScope under CC BY-NC-ND 4.0 |
| Remaining exam items, 783 | Source-text redistribution not cleared for this release |
| Derived case prompts and historical scoring references | Published October 9: 276 prompts + 276 matching references; see known-issue notes above |
| Original judgment files and private workbooks | Not included in the public release |
| Model responses and individual review sheets | Not included; aggregate scores remain public |

The 78-item package comes from three Victorian Bar publications, which state
CC BY-NC-ND 4.0. Source text is kept separate from LegalScope's editorial fields.
Twenty-two workbook question fields are editorial summaries; these are omitted
from the original-text package, with the original questions retained in the
background excerpts. One record explicitly marks its non-contiguous excerpts.
Selected candidate answers may contain errors; they are not described as perfect
official model answers. See [third-party notices](../THIRD_PARTY_NOTICES.txt).

“Publicly accessible” does not describe a universal redistribution license. A
source with unconfirmed permissions is recorded as pending, not as permanently
prohibited. Dataset size and release size are reported separately.

## Workshop Camera-Ready Synchronization: October 3, 2026

This repository now follows **LegalScope: Measuring Exam-to-Case Transfer in LLM
Legal Reasoning**, AI Measurement Science Workshop at COLM 2026.
[Paper record](https://openreview.net/forum?id=BNx62Wx1ej).

| Component | Earlier repository snapshot | Workshop snapshot |
| --- | ---: | ---: |
| Exam questions | 868 | 861 |
| Case prompts | 256 | 276 |
| Judgments / legal issues | 54 / 128 | 56 / 138 |
| Model groups | 20 | 28 |
| Dataset responses | 22,480 | 31,836 |
| Unique human-validation responses | 1,800 | 2,520 |

The exam split excludes one duplicate and six items with unverifiable shared
context. The case split now spans seven legal categories. Model display names,
calibrated rubric, all five figures, correlations, and human-validation statistics
are synchronized with the workshop version. The main dimension comparison now
concerns citation relevance versus argument validity; the former
constraint-extraction-bottleneck claim is superseded.

The earlier snapshot remains accessible in Git history at
[`a84b8a6`](https://github.com/EternWang/LegalScope/tree/a84b8a6e641ba0b1e09c5c67ea68848eb5092f39).
Historical controls explicitly retained by the paper remain labeled historical.
They are not silently rescaled to 28 models.

## Included

- README with workshop paper link and citation.
- Benchmark metadata, 28-model roster, source/category counts, and rounded Table 3 results.
- Five workshop figures and provenance notes.
- Scoring, annotation, data-card, results, and AI-workflow documentation.
- Workbook helper code and consistency tests.

This update transcribes the workshop paper and its figure assets. It does not rerun
models, rescore private answers, or claim reproduction from the private workbook.
The legacy sample extractor has not been validated on the workshop workbook;
its generated files should not overwrite this versioned paper metadata.

## Not Included

The repository is a public research preview, not a full artifact release. It does
not contain the full workbook, prompt/reference matrix, model outputs, human review
sheets, non-de-identified judgments, private source documents, or the paper source
package. The paper is linked rather than committed as a PDF.

## Before a Full Data Release

Confirm source redistribution rights, de-identification and re-identification risk,
provider terms for outputs, and any applicable review/anonymity requirements.
No row-level data was added in this synchronization.

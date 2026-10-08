# Release Status

## Content and Project Page Review: October 8, 2026

The current manuscript and the final source workbook were checked. The benchmark
still contains **861 exam items, 276 case prompts, 56 judgments, 138 issues and
28 model groups**. All 252 published aggregate score values match the current
manuscript. This is a content check, not a new experiment or a claim of a new
publication venue; the public citation remains the workshop record below.

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
| Victorian Bar source excerpts and selected candidate answers, 78 items | Prepared for Hugging Face; not yet published as a dataset |
| Remaining exam items, 783 | Source-text redistribution not cleared for this release |
| Derived case prompts and scoring packets, 276 | Pending per-case source and privacy review |
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

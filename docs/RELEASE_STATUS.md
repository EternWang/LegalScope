# Release Status

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

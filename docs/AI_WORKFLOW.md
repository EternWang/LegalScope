# Research workflow

1. Collect legal-exam sources and concluded Chinese judgments.
2. Normalize, deidentify, deduplicate and review the source records.
3. Build exam tasks and paired case prompts with lawyer review.
4. Generate answers across 28 model configurations.
5. Translate Chinese case answers into English with GPT-5.5.
6. Score exam answers against references and translated case answers on citation relevance, constraint extraction and argument validity.
7. Compare automatic scores with human scores on 2,240 exam answers and 280 case answers; two lawyers independently rate the case set.
8. Analyze exam–case association, score dimensions and automatic–human agreement.

AI tools support data processing, generation and scoring. Researchers handle
source selection, deidentification, legal review and interpretation.

The citation–argument analysis covers 276 prompts and 56 judgments. Historical
controls and the two five-run audits of 200 fixed answers retain their own
samples and scoring versions. See [results](RESULTS_SUMMARY.md) for these
analyses and [scoring](SCORING_RUBRIC.md) for evaluator settings.

[Loading guide](USING_THE_RELEASE.md) · [Reproduce the results](REPRODUCIBILITY.md)

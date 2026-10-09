# Comparing reference versions

The offline review utility prepares case responses for a **new experiment** and
checks returned scores. It is not the historical evaluator and does not reproduce
the paper's full experiment. It makes no API calls. Existing scores are retained.

## Prepare a comparison

Install this repository with `pip install -e .`. Supply the published prompt and
reference JSONL files and your own response JSONL. Each response needs
`review_id`, `model` and `response`. Supply a JSON array of model names and a JSON
array of selected review IDs. Every selected prompt must have one response per
listed model. IDs, case and issue joins, duplicate responses, and missing values
are checked before output is written.

```sh
python -m legalscope.review prepare \
  --prompts data/private/case_prompts.jsonl \
  --references data/private/case_scoring_references.jsonl \
  --responses data/private/responses.jsonl \
  --models data/private/models.json \
  --selection data/private/selection.json \
  --run-id reference-comparison-v1 --variant historical \
  --out-dir data/private/comparison-historical
```

For a second variant, add `--citation-patch path/to/patch.jsonl`, change the
variant name, and choose a fresh output directory. Each patch contains
`review_id`, `before` and `after`, where `before` must exactly match the historical
`citation_basis`. The original files are never overwritten. Article corrections
do not establish that a reference is complete or legally applicable to the case.
Read the [reference notes](CASE_REFERENCE_NOTES.md) when defining a comparison.

`packets.jsonl` includes only an opaque response ID, the original model prompt,
the unchanged model response, and four reference fields. The separate
`identity_map.private.jsonl` connects the response ID to its model and case.
Previous scores and model identity metadata are excluded from packets. Any
self-identification already present in an answer is preserved. Keep both outputs
private unless their release has been separately reviewed.

The manifest records input and output hashes, selected cases, the model roster,
and coverage. Select and archive the evaluator instructions before scoring.
`scoring_prompt` in the reference file is an issue label, not a complete rubric.
Record the evaluator model or snapshot, reasoning setting, sampling parameters,
tool availability, retry policy, instruction hash, and execution dates. An
unrecorded historical parameter must not be reconstructed by assumption.

## Validate scores

Each result must contain `response_id`, integer `A`, `B`, `C` values from 0 to 4,
and nonempty `notes`. After scoring all packets in one bundle:

```sh
python -m legalscope.review validate \
  --bundle data/private/comparison-historical \
  --results data/private/results.jsonl \
  --output data/private/comparison-summary.json
```

The utility rejects missing, duplicate and unknown IDs, invalid score values and
changed bundle files. It reports each dimension as its mean multiplied by 25,
plus an equal-weight case mean. These are scores for the selected subset, not
the paper's full 276-prompt case result. Variants are never pooled. Semantic
quality, compliance with the rubric and correct legal reasoning still require
evaluation; schema validation cannot establish them.

For a controlled reference comparison, reuse the same responses and run both
reference variants with the same evaluator settings. Report paired differences
and the selected sample size. Do not replace historical scores with new scores
without identifying the new reference and evaluator versions.

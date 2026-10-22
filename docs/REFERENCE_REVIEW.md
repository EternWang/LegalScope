# Comparing reference versions

The offline utility prepares anonymized case-answer packets and validates scores
returned by an evaluator. Use it to compare reference versions on the same
answers. For the published results, see the [reproduction guide](REPRODUCIBILITY.md).

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
`review_id`, `before` and `after`, where `before` must exactly match the supplied
`citation_basis`. Each variant writes to its own directory. Use the
[reference notes](CASE_REFERENCE_NOTES.md) to select citation changes for comparison.

`packets.jsonl` includes only an opaque response ID, the original model prompt,
the unchanged model response, and four reference fields. The separate
`identity_map.private.jsonl` connects the response ID to its model and case.
Previous scores and model identity metadata are excluded from packets. Any
self-identification already present in an answer is preserved.

The manifest records input and output hashes, selected cases, the model roster,
and coverage. Select and archive the evaluator instructions before scoring.
`scoring_prompt` in the reference file is an issue label, not a complete rubric.
Record the evaluator model or snapshot, reasoning setting, sampling parameters,
tool availability, retry policy, instruction hash, and execution dates. Mark
unrecorded settings as unknown.

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
plus an equal-weight case mean for each variant on the selected subset.
Validation checks record structure and coverage; the chosen evaluator assesses
the answers against the rubric.

For a controlled reference comparison, reuse the same responses and run both
reference variants with the same evaluator settings. Report paired differences
and the selected sample size, identifying the reference and evaluator versions
used for each result.

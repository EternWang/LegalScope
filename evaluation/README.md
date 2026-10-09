# Evaluation

This directory provides response generation, anonymous scoring, and the scoring
rubrics used in the August 2026 model expansion. For the published results, use
the stored scores and [aggregation guide](../docs/REPRODUCIBILITY.md).

## Generate case answers

Download `data/cases/case_prompts.jsonl` and
`data/cases/case_scoring_references.jsonl` from
[Hugging Face](https://huggingface.co/datasets/Hongyu801/LegalScope/tree/main/data/cases)
into `data/private/`. Only the `prompt` field is sent to the answering model.

```sh
python evaluation/generate.py \
  --prompts data/private/case_prompts.jsonl \
  --model "Qwen3.5-9B" --limit 1 --out data/private/generation
```

The command validates a request without making a model call. Add `--execute`
to generate responses. Set `OPENROUTER_API_KEY` for OpenRouter configurations or
`GEMINI_API_KEY` for Google. Results go to a new directory, with input and runtime
hashes and the request configuration. The output `responses.jsonl` contains
`item_id`, `model_group`, `response`, `answer_sha256`, and execution metadata.

[generation_configs.json](generation_configs.json) records settings recovered
from the eight model groups added in August 2026. It includes model aliases,
provider routing, reasoning settings, output budgets, and source code hashes.
Null parameters were not set explicitly. Configurations for the other 20 groups
are not represented by this file. Provider aliases and routing may change over
time, so a new run is a new experiment.

The [model settings reference](../docs/MODEL_SETTINGS.md) and
[provider default catalog](provider_defaults.json) cover all 28 groups. They
document current provider defaults separately from the recorded run settings.

The generation adapter preserves the recorded request parameters. It uses
sequential requests and bounded execution retries; it increases the output budget
after truncation, up to the recorded maximum. Incomplete responses are rejected.
It does not reproduce historical parallel scheduling or provider state.

## Prepare anonymous scoring tasks

Use generated responses or convert the released case response Parquet to JSONL:

```python
import json
import pyarrow.parquet as pq

rows = pq.read_table("case_model_responses.parquet").to_pylist()
with open("data/private/responses.jsonl", "w", encoding="utf-8") as out:
    for row in rows:
        out.write(json.dumps(row, ensure_ascii=False) + "\n")
```

Prepare one model and one prompt as a small example:

```sh
python evaluation/prepare.py \
  --prompts data/private/case_prompts.jsonl \
  --references data/private/case_scoring_references.jsonl \
  --responses data/private/responses.jsonl \
  --models "Qwen3.5-9B" --review-ids RV001 \
  --mode joint --out data/private/scoring-input
```

Omit `--review-ids` to select all 276 prompts. Supply multiple names after
`--models` to evaluate more model groups. The preparer checks input joins, answer
hashes and coverage. Scoring inputs contain one answer and its references;
model identity and prior scores remain outside the evaluator prompt. The separate
`identity_map.jsonl` joins task IDs back to the selected model and prompt.

## Run the scorer

```sh
python evaluation/score.py \
  --scoring-dir data/private/scoring-input \
  --output-dir data/private/scoring-output --dry-run
```

After validating inputs, omit `--dry-run` to run a compatible Codex CLI. The
default evaluator is `gpt-5.5` with high reasoning effort. Use
`--codex-executable` to select a CLI installation. Each answer is evaluated in
a separate ephemeral process in an empty, read-only workspace. Tool activity is
rejected. The first result satisfying the schema and score caps is retained,
with up to three execution or validation attempts by default.

The portable runner retains the original prompt builders and score validators.
It adds configurable paths, a separate output directory, input/runtime hash
checks and a tool-use guard. [provenance.json](provenance.json) identifies the
source runtime and rubric files. The runner reports the requested alias; it does
not claim an immutable backend model snapshot. Temperature, top-p and seed are
not set by this scorer.

Use `--mode b` in the preparation step for the archived B-only rubric. This is
a separate scoring run, not an average with the joint A/B/C result. The B-only
rubric includes the English-language policy used in that batch. Historical
dimension scores and subsequent B updates should not be replaced by a single
new joint run when comparing with the paper.

The public references contain citation updates. Scoring them again can produce
different results from the historical scores. Report the dataset revision,
rubric hash, evaluator configuration, execution date, and selected items with
new results. Schema checks establish valid score records, not the legal
correctness of a model's reasoning.

## Runtime requirements

Generation and input preparation use Python 3.10+ and the standard library.
Reading the case response Parquet requires `pyarrow`. Model generation requires
the relevant provider account; scoring requires an authenticated Codex CLI with
the flags used by the runner, targeting Codex CLI `0.147.0-alpha.6.5`.
Dry runs and the repository tests make no model
calls. The full historical generation and scoring environment is not bundled.

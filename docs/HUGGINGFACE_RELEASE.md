# Hugging Face Release Plan

This document describes the recommended Hugging Face public preview for
LegalScope.

## Recommended Repository

- Repository type: dataset
- Suggested repo id: `EternWang/LegalScope`
- Public title: `LegalScope`
- Release mode: metadata-only public preview

The first Hub release should mirror the public GitHub release boundary. It
should include the dataset card and public metadata files, not the full
workbook, prompts, model outputs, human review sheets, or private legal source
documents.

## Files to Upload

```text
README.md
data/metadata/dataset_summary.json
data/metadata/model_groups.csv
data/metadata/source_composition.csv
```

Optional after review:

```text
data/sample/public_preview.jsonl
data/sample/README.md
```

## Dataset Card Requirements

The Hugging Face `README.md` should include:

- YAML metadata for discoverability;
- a concise dataset summary;
- benchmark composition counts;
- data structure and release boundary;
- intended and out-of-scope uses;
- privacy, de-identification, and licensing notes;
- citation instructions;
- links back to GitHub and the paper once available.

## Suggested Metadata

```yaml
---
language:
- en
- zh
license: mit
pretty_name: LegalScope
task_categories:
- question-answering
- text-generation
tags:
- legal
- legal-reasoning
- benchmark
- llm-evaluation
- exam-to-case-transfer
- chinese-civil-judgments
- text
size_categories:
- n<1K
---
```

The `n<1K` value reflects the public metadata preview files, not the withheld
full model-output matrix.

## Upload Workflow

Create the dataset repository on the Hub, then upload the prepared files. A CLI
flow may look like:

```bash
hf auth login
hf repo create EternWang/LegalScope --type dataset
hf upload EternWang/LegalScope ./huggingface_dataset_repo . --repo-type dataset
```

After upload, verify:

1. the dataset card renders correctly;
2. YAML metadata appears as Hub tags;
3. public metadata files are visible under `data/metadata/`;
4. no withheld workbook, prompt, model-output, human-review, or non-de-identified
   source files were uploaded;
5. GitHub and Hugging Face links point to each other.

## Full Release Gate

Before adding row-level samples or full artifacts, confirm:

- source redistribution rights;
- de-identification quality;
- model-output provider terms;
- paper review anonymity;
- human review privacy;
- final paper citation and artifact policy.

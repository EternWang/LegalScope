# LegalScope

**LegalScope** is a benchmark for measuring whether large language model
performance on public legal exams transfers to real-case legal analysis.

The project pairs a scalable public-exam track with a lawyer-reviewed,
de-identified Chinese civil-judgment track. The public repository is a
research release scaffold: it documents the benchmark design, evaluation
counts, scoring protocol, public figures, metadata, and helper utilities while
withholding private workbooks, full prompts, model outputs, human review
sheets, and non-de-identified legal materials.

## Snapshot

| Component | Count |
| --- | ---: |
| Public legal-exam questions | 868 |
| Real-case issue-stance prompts | 76 |
| De-identified Chinese civil judgments | 15 |
| Legal issues extracted from judgments | 38 |
| Model groups evaluated | 20 |
| Public-exam model responses | 17,360 |
| Real-case model responses | 1,520 |
| Total model responses | 18,880 |
| Human-validation responses | 1,800 |

<img src="assets/figures/paper_collection_pipeline.png" alt="LegalScope benchmark construction pipeline" width="920">

## What LegalScope Tests

LegalScope asks whether exam performance is a reliable proxy for applied legal
reasoning. The public-exam track uses reference-aware open-ended legal-exam
questions. The real-case track asks models to write stance-aware Chinese legal
analysis over de-identified civil-judgment materials under closed-record
constraints.

The benchmark separates three questions that are often blurred together:

1. How well do models answer public legal-exam questions?
2. How well do the same models reason over bounded real-case legal facts?
3. Do rankings, reasoning-mode gains, and evaluator agreement transfer across
   those settings?

## Main Findings

- Public-exam scores correlate with Chinese real-case scores at the model level
  (Pearson `r = 0.835`, Spearman `rho = 0.661`), but the transfer is incomplete.
- Real-case legal reasoning exposes a constraint-extraction bottleneck: models
  often produce fluent legal prose while missing operative rule conditions,
  factual boundaries, stance requirements, or evidence limits.
- Automated evaluation aligns strongly with human review on public-exam answers
  (answer-level Pearson `r = 0.925`) but weakens on real-case analysis
  (`r = 0.450`), motivating expert-grounded validation for high-stakes legal
  evaluation.

## Repository Map

| Path | Purpose |
| --- | --- |
| `assets/figures/` | Public-safe figures rendered from paper figure sources. |
| `data/metadata/` | Machine-readable counts, model groups, and source composition. |
| `data/sample/` | Reserved for public row-level samples after release review. |
| `docs/PROJECT_BRIEF.md` | Research question, benchmark design, and paper-facing summary. |
| `docs/RESULTS_SUMMARY.md` | Public-facing result figures and transfer metrics. |
| `docs/DATA_CARD.md` | Dataset scope, intended use, limitations, and release boundary. |
| `docs/SCORING_RUBRIC.md` | Public-exam and real-case scoring protocols. |
| `docs/ANNOTATION_PROTOCOL.md` | Human-validation protocol and review focus. |
| `docs/AI_WORKFLOW.md` | AI-assisted workflow and human-control safeguards. |
| `docs/PROVENANCE.md` | Public-safe construction and processing provenance. |
| `docs/HUGGINGFACE_RELEASE.md` | Hugging Face dataset-card release plan. |
| `scripts/` | Lightweight public helper scripts. |
| `src/legalscope/` | Small Python utilities for authorized local workbooks. |
| `tests/` | Unit tests for public helpers. |

## Quickstart

Install the public helper package from a local checkout:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Inspect the public metadata:

```bash
python - <<'PY'
import json
from pathlib import Path

summary = json.loads(Path("data/metadata/dataset_summary.json").read_text())
print(summary["project"])
print(summary["counts"]["dataset_model_responses_total"])
PY
```

Use the workbook helpers only with authorized local workbooks:

```python
from legalscope.workbook import summarize_workbook

for sheet in summarize_workbook("private_authorized_workbook.xlsx"):
    print(sheet.title, sheet.data_rows, sheet.model_count)
```

## Public Release Boundary

This repository does not publish:

- the paper draft, review PDF, or LaTeX source;
- the full benchmark workbook;
- complete prompt matrices, reference answers, model answers, or row-level
  model-output tables;
- human review sheets, adjudication notes, or reviewer annotations;
- non-de-identified judgments or private source documents.

The public materials are sufficient to understand the research design, scope,
counts, release boundary, and public-facing results. They are not sufficient to
reconstruct the full benchmark.

## Hugging Face Release

A Hugging Face dataset-card-ready public preview is described in
[`docs/HUGGINGFACE_RELEASE.md`](docs/HUGGINGFACE_RELEASE.md). The recommended
first Hub release is a metadata-only preview containing this README-style
dataset card plus the public metadata files. Row-level samples should be added
only after source redistribution, privacy, and review constraints are cleared.

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). The final paper
citation should replace the placeholder citation once the paper has a stable
public identifier.

## License

Code and public documentation in this repository are released under the MIT
License unless otherwise noted. This license does not grant redistribution
rights for withheld source documents, full workbooks, model outputs, or private
review materials.

## Disclaimer

LegalScope is a research benchmark for model evaluation. It is not legal advice,
a legal research product, or a substitute for jurisdiction-specific legal
review.

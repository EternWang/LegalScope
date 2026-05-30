# Data Preview

This folder contains only public-safe LegalScope metadata. The full workbook, prompt
matrix, model outputs, reference answers, and human review sheets are not included in
this repository.

## Metadata Files

| File | Purpose |
| --- | --- |
| `metadata/dataset_summary.json` | Machine-readable counts and release boundary. |
| `metadata/model_groups.csv` | The 20 model groups used in the evaluation tables. |
| `metadata/source_composition.csv` | Public-exam and real-case source composition. |

## Snapshot Counts

| Component | Count |
| --- | ---: |
| Public legal-exam items | 868 |
| Real-case issue-stance prompts | 76 |
| Total dataset items | 944 |
| Model groups | 20 |
| Dataset model responses | 18,880 |
| Human-validation responses | 1,800 |

## Release Boundary

`data/sample/` intentionally contains only a README. Public row-level samples should
be regenerated only after source-distribution, privacy, and review constraints are
cleared.

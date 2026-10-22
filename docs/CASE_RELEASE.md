# Case data

## Case prompts and scoring references

The `case_prompts` configuration contains 276 prompt records (`test` split),
covering 56 judgments and 138 issues. Each issue has one supporting and one
opposing prompt. The `case_scoring_references` configuration contains 276 matching
reference records (`test` split). Join them by `review_id`, never by row position.
The split name denotes evaluation use; no train/development split is supplied.

The released prompts are in English and request Chinese answers. GPT-5.5
translated the model answers into English for scoring; the response release
contains these English translations.

Send only `prompt` to the answering model. The separate reference table supplies
authorities, propositions and constraints for evaluation; opposing stances may
share an authority or court proposition. `scoring_prompt` labels the issue and
stance. See the [scoring guide](SCORING_RUBRIC.md) for the complete protocol.

```python
from datasets import load_dataset

# Pin the same revision for prompts and references.
revision = "e4444c9755072ed2255ad11fa304e4a446121b40"
prompts = load_dataset("Hongyu801/LegalScope", "case_prompts", split="test", revision=revision)
references = load_dataset("Hongyu801/LegalScope", "case_scoring_references", split="test", revision=revision)
by_id = {r["review_id"]: r for r in references}
assert len(prompts) == len(by_id) == 276
row = prompts[0]
print(row["review_id"], row["stance"], row["prompt"])
print(by_id[row["review_id"]]["reference_status"])
```

| Prompt field | Meaning |
| --- | --- |
| `review_id` | Unique prompt/reference join key, RV001–RV276 |
| `document_id` | Dataset case ID; 56 distinct values, with numbering gaps retained |
| `case_theme` | Curated case topic |
| `issue_id`, `issue_title`, `core_issue` | Issue grouping, title and issue statement |
| `position_original` | Original stance wording |
| `stance` | Normalized `support` or `oppose`; original wording is retained separately |
| `prompt` | Full supplied model input text; unmodified |
| `judgment_level`, `case_type` | Case descriptors |
| `law_category`, `law_category_detail` | Legal category descriptors |
| `deidentification_note` | Description of identifier removal; separate from the model input |
| `release_version`, `license` | Release version and applicable license |

| Reference field | Meaning |
| --- | --- |
| `review_id`, `document_id`, `issue_id` | Join keys and case/issue grouping |
| `scoring_prompt` | Issue and stance label; the full scoring protocol is documented separately |
| `citation_basis` | Legal authorities and cited provisions |
| `supported_proposition` | Proposition or authority explanation used for benchmark scoring |
| `review_constraints` | Constraints supplied for evaluation |
| `answer_type` | Identifies the record as a scoring reference |
| `reference_status`, `reference_note` | Reference type and citation notes; see the status definitions below |
| `reference_sources` | Official authority titles, provisions and source URLs where supplied |
| `release_version`, `license` | Release version and applicable license |

[Official reference sources](CASE_REFERENCE_NOTES.md) are also supplied in
`reference_sources`. An empty list means no source link is supplied for that
record. Cited authorities are listed in `citation_basis`.

`benchmark_reference` identifies a released scoring annotation.
`citation_sources_updated` identifies the ten records with corrected citation
text and official source links.
The status and deidentification metadata are separate from model inputs and
evaluator reference text.

## Case sources

The case track draws on 15 judgments provided by a handling lawyer (76 prompts)
and 41 judgments attributed to China Judgments Online (200 prompts). All prompts
were deidentified and checked by a practicing lawyer.

The release provides the evaluation prompts, scoring references and
[model responses and scores](REPRODUCIBILITY.md). Ten reference records include
citation corrections made after scoring, indexed in the
[reference notes](CASE_REFERENCE_NOTES.md). Provenance is documented at
collection level; original judgments and identifying source mappings are excluded.

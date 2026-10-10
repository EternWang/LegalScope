# Case data

## Case prompts and scoring references

The `case_prompts` configuration contains 276 prompt records (`test` split),
covering 56 judgments and 138 issues. Each issue has one supporting and one
opposing prompt. The `case_scoring_references` configuration contains 276 matching
reference records (`test` split). Join them by `review_id`, never by row position.
The split name denotes evaluation use; no train/development split is supplied.

The prompts are in English and request answers in Chinese. The released text
preserves the final dataset inputs. Do not feed
the reference table to the model as part of the closed book input. References for
opposing stances may share a court proposition or legal authority. They do not
provide an ideal answer for each stance. `scoring_prompt` is an issue and stance
label, **not the complete evaluator prompt or executable scoring code**.

```python
from datasets import load_dataset

# Pin the dataset revision when reporting an experiment.
prompts = load_dataset("Hongyu801/LegalScope", "case_prompts", split="test")
references = load_dataset("Hongyu801/LegalScope", "case_scoring_references", split="test")
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
| `deidentification_note` | Description of identifier removal and the release boundary; not part of the model input |
| `release_version`, `license` | Release version and applicable license |

| Reference field | Meaning |
| --- | --- |
| `review_id`, `document_id`, `issue_id` | Join keys and case/issue grouping |
| `scoring_prompt` | Issue and stance label; the full scoring protocol is documented separately |
| `citation_basis` | Legal authorities and cited provisions |
| `supported_proposition` | Proposition or authority explanation used for benchmark scoring |
| `review_constraints` | Constraints supplied for evaluation |
| `answer_type` | Explicitly identifies a scoring reference, not model output or unique gold answer |
| `reference_status`, `reference_note` | Reference type and citation notes; see the status definitions below |
| `reference_sources` | Official authority titles, provisions and source URLs where supplied |
| `release_version`, `license` | Release version and applicable license |

[Official reference sources](CASE_REFERENCE_NOTES.md) are also supplied in
`reference_sources`. An empty list means no source link is supplied for that
record; it does not mean the record has no cited authority. Published scores
are unchanged.

`benchmark_reference` identifies a released scoring annotation.
`citation_sources_updated` identifies the ten records with corrected citation
text and official source links. Neither status certifies every reference's
legal applicability to its case; scoring annotations are not legal opinions.
The status and deidentification metadata are separate from model inputs and
evaluator reference text.

## Case publication status

The case track draws on 15 judgments provided by a handling lawyer (76 prompts)
and 41 judgments attributed to China Judgments Online (200 prompts). The first
76 prompts were derived from the lawyer supplied judgments and reviewed after
deidentification. All prompts were
deidentified and checked by a practicing lawyer. The 276 records cover 56 cases
and 138 issues, each with supporting and opposing positions.

The release contains the final prompt text and reference annotations with updated
citations and official source links. A separate [results release](REPRODUCIBILITY.md)
contains all case model responses and individual numeric scores. Original
judgments and identifying source mappings are excluded. Sources are documented at collection
level; links to individual judgments are not included.

# Contributing

LegalScope is currently a public research preview with a strict release boundary.
Contributions are welcome for documentation, metadata cleanup, public helper
code, tests, and release-process improvements.

Please do not submit:

- private workbooks;
- full prompts or reference answers;
- model-output matrices;
- human review sheets or adjudication notes;
- non-de-identified legal source documents;
- provider credentials, local paths, logs, or API keys.

## Development

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Documentation Changes

Keep public files aligned with the project name `LegalScope`. Historical
internal names should not be introduced into public documentation.

## Privacy Review

Any proposed row-level data release should be reviewed for source licensing,
de-identification, re-identification risk, provider terms, and paper review
requirements before it is merged.

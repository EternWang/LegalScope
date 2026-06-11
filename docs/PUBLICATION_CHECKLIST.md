# Publication Checklist

Use this checklist before making GitHub or Hugging Face materials public.

## Naming

- [ ] The public name is `LegalScope`.
- [ ] Historical internal project names do not appear in public files.
- [ ] Figure labels and captions use the public name where applicable.

## GitHub

- [ ] README explains what the project does, why it matters, and how to start.
- [ ] Repository map points to data card, results, scoring, annotation, and
  release-boundary docs.
- [ ] `CITATION.cff` is up to date.
- [ ] License text applies only to code and public documentation unless a data
  license is explicitly added.
- [ ] CI passes on the public helper code.
- [ ] No private workbook, prompt matrix, model output, review sheet, API key,
  provider log, or non-de-identified source file is committed.

## Hugging Face

- [ ] Dataset card has valid YAML metadata.
- [ ] Dataset card states that this is a metadata-only public preview.
- [ ] Public metadata files are uploaded under `data/metadata/`.
- [ ] Full prompts, model outputs, reference answers, human review sheets, and
  non-de-identified sources are absent.
- [ ] Hub page links back to GitHub.
- [ ] GitHub README links to the Hub page after it is live.

## Full Dataset Expansion

- [ ] Source redistribution rights checked.
- [ ] De-identification reviewed.
- [ ] Re-identification risk reviewed.
- [ ] Provider terms for model-output redistribution checked.
- [ ] Human review notes cleaned or excluded.
- [ ] Review anonymity requirements checked.
- [ ] Final paper citation added.

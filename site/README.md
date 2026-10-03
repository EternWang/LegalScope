# Project page

The site is published at https://eternwang.github.io/LegalScope/.

Run `python scripts/build_site.py` from the repository root, then preview
`_site/` with any static HTTP server. The build copies paper figures and metadata
from the repository and derives the interactive table from
`data/metadata/model_performance.csv`.

GitHub Actions builds and deploys changes to `main` through the Pages workflow.
Update the paper, GitHub and Hugging Face links together when a release changes.
Do not mark benchmark records as available until the linked repository contains
that release. Paper results and new experiments should remain distinguishable.

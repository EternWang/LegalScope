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

The result table marks the highest and second-highest **distinct displayed
values per column** across the full 28-model roster. Equal one-decimal scores
share a mark. Search and sorting never recompute ranks within the visible rows.
Solid shading and bold text mark the best value; diagonal hatching and an
underline mark the second. These marks do not establish statistical significance.

Worked examples separate source facts, task instructions, reference/model answers
and presentation commentary. RV038's answer excerpt and 4/1/3 scores follow the
current manuscript. The Victorian Bar source text retains its source license;
the 0–4 display is a scoring scale, not a measured model score for that excerpt.

The build versions CSS, JavaScript and generated result URLs by content hash so
returning visitors do not receive old table behavior with new page content.

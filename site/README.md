# Project page

The site is published at https://eternwang.github.io/LegalScope/.

The homepage introduces the paper, retains the benchmark overview and pipeline,
and links to three dedicated pages: `examples.html`, `results.html` and
`resources.html`.
Page content lives in the corresponding `site/*.html` fragments. The build
wraps them in `site/layout.html`, with shared navigation and a current-page
indicator. Legacy homepage section links redirect to the matching page.
Examples support direct `#exam` and `#case` links and browser back/forward.

Run `python scripts/build_site.py` from the repository root, then preview
`_site/` with any static HTTP server. The build copies paper figures and metadata
from the repository and derives the interactive table from
`data/metadata/model_performance.csv`.

GitHub Actions builds and deploys changes to `main` through the Pages workflow.
The resources page links to the paper, released data and reproduction guides.

The result table marks the highest and second-highest **distinct displayed
values per column** across the full 28-model roster. Equal one-decimal scores
share a mark. Search and sorting never recompute ranks within the visible rows.
Bold text marks the best value; an underline marks the second. A subtle background
groups the human-evaluation columns. These marks do not establish statistical significance.

Worked examples contain the complete model input, stored model answer, scoring
rules and recorded score in bounded reading panels. RV038 uses the recorded
4/1/3 scores; the Victorian Bar example uses Gemini 2.5 Flash's recorded 1/4.
Highlights are presentation annotations. Source text retains its source license.

The build versions CSS, JavaScript and generated result URLs by content hash so
returning visitors do not receive old table behavior with new page content.

Before writing output, the build checks the model roster and finite 0–100 score
values. It refuses source directories as output, publishes only the listed
website assets and metadata, and rejects unexpected files left in the build
directory. This prevents an old local preview from silently entering a release.

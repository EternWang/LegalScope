# Project page

The site is published at https://eternwang.github.io/LegalScope/.
It has four pages: the overview, task examples, results, and data/citation.

## Build and deploy

Run `python scripts/build_site.py` from the repository root and serve `_site/`
with a static HTTP server. GitHub Actions builds and deploys changes to `main`
through the Pages workflow.

Content lives in `site/*.html`, wrapped by `site/layout.html`. The build copies
figures and metadata and creates the results table from
`data/metadata/model_performance.csv`. Asset URLs include content hashes for
cache refresh. The build validates the roster, score ranges and output files.

## Navigation and examples

Legacy homepage section links redirect to the corresponding page. Examples
support direct `#exam` and `#case` links and browser back/forward navigation.
Each example shows a task summary, answer summary and score; expandable sections
contain the complete input, model answer and scoring rules.

RV038 shows its recorded 4/1/3 case scores. The Victorian Bar example shows
Gemini 2.5 Flash's recorded 1/4 exam score. Highlights explain the displayed
answers; quoted source text retains its source license.

The results table marks the highest and second-highest distinct displayed
values across the full roster, including ties. Filtering preserves those ranks.
See [table details](../docs/REPRODUCIBILITY.md#reading-the-results-table).

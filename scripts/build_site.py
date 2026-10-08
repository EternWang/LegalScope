"""Build the static project page from versioned paper metadata and figures."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output).resolve()
    if not output.is_relative_to(root) or output == root:
        parser.error("Build output must be a subdirectory of this repository.")
    output.mkdir(parents=True, exist_ok=True)
    for source in (root / "site").iterdir():
        if source.is_file():
            shutil.copy2(source, output / source.name)
    shutil.copytree(root / "assets/figures", output / "assets", dirs_exist_ok=True)
    data = output / "data"
    data.mkdir(exist_ok=True)
    metadata = root / "data/metadata"
    for source in metadata.iterdir():
        if source.suffix in {".csv", ".json"}:
            shutil.copy2(source, data / source.name)
    with (metadata / "model_performance.csv").open(encoding="utf-8", newline="") as handle:
        results = []
        for index, row in enumerate(csv.DictReader(handle)):
            results.append({key: value if key == "model_group" else float(value) for key, value in row.items()} | {"paper_order": index})
    counts = json.loads((metadata / "dataset_summary.json").read_text(encoding="utf-8"))["counts"]
    if len(results) != counts["model_groups"]:
        raise ValueError("Model result count differs from the benchmark snapshot.")
    (data / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    # Keep returning visitors on matching HTML, styling, code, and score data.
    result_version = hashlib.sha256((data / "results.json").read_bytes()).hexdigest()[:12]
    script = output / "app.js"
    script.write_text(script.read_text(encoding="utf-8").replace(
        "'data/results.json'", f"'data/results.json?v={result_version}'"
    ), encoding="utf-8")
    page = (output / "index.html").read_text(encoding="utf-8")
    for name, attribute in (("style.css", "href"), ("app.js", "src")):
        version = hashlib.sha256((output / name).read_bytes()).hexdigest()[:12]
        page = page.replace(f'{attribute}="{name}"', f'{attribute}="{name}?v={version}"')
    (output / "index.html").write_text(page, encoding="utf-8")
    (output / ".nojekyll").touch()
    print(f"Built project page with {len(results)} model groups: {output}")


if __name__ == "__main__":
    main()

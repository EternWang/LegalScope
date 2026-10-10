"""Build the static project page from versioned paper metadata and figures."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import re
import shutil
from pathlib import Path


SCORE_COLUMNS = {"public_exam_auto", "public_exam_human", "citation", "constraint", "argument", "real_case_auto", "real_case_human", "overall_auto", "overall_human"}
METADATA_FILES = ("model_performance.csv", "model_groups.csv", "source_composition.csv", "dataset_summary.json")
PAGES = {
    "index": ("Home", "LegalScope studies exam-to-case transfer in LLM legal reasoning: 861 legal-exam questions, 276 case prompts and 28 model groups."),
    "examples": ("Task examples", "Follow complete LegalScope prompts through model answers, scoring rules and recorded scores."),
    "results": ("Results", "Compare the published LegalScope results for all 28 model groups and explore exam-to-case transfer."),
    "resources": ("Data & citation", "Download LegalScope data, read the documentation and cite the workshop paper."),
}


def validate_output_path(root: Path, output: Path) -> None:
    root, output = root.resolve(), output.resolve()
    protected = ("site", "assets", "data", "docs", "scripts", "src", "tests", ".git", ".github", ".venv")
    if not output.is_relative_to(root) or output == root:
        raise ValueError("Build output must be a subdirectory of this repository.")
    if any(output.is_relative_to((root / name).resolve()) for name in protected):
        raise ValueError("Build output must not overwrite repository source, data, or configuration directories.")


def load_results(metadata: Path) -> list[dict]:
    with (metadata / "model_performance.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(reader.fieldnames) != 10 or set(reader.fieldnames) != SCORE_COLUMNS | {"model_group"}:
            raise ValueError("Unexpected model-performance columns.")
        results = []
        for index, row in enumerate(reader):
            if None in row or not row["model_group"] or not row["model_group"].strip():
                raise ValueError("Malformed score row or missing model name.")
            scores = {key: float(row[key]) for key in SCORE_COLUMNS}
            if not all(math.isfinite(value) and 0 <= value <= 100 for value in scores.values()):
                raise ValueError("All scores must be finite values in [0, 100].")
            results.append({"model_group": row["model_group"], **scores, "paper_order": index})
    counts = json.loads((metadata / "dataset_summary.json").read_text(encoding="utf-8"))["counts"]
    with (metadata / "model_groups.csv").open(encoding="utf-8", newline="") as handle:
        roster = [row["model_group"] for row in csv.DictReader(handle)]
    names = [row["model_group"] for row in results]
    if len(names) != counts["model_groups"] or len(set(names)) != len(names) or len(roster) != len(names) or set(names) != set(roster):
        raise ValueError("Model results must match the unique benchmark roster and count.")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output).resolve()
    try:
        validate_output_path(root, output)
        metadata = root / "data/metadata"
        results = load_results(metadata)
        example_inputs = {}
        for track, name in (("exam", "exam_confidentiality"), ("case", "case_reappraisal")):
            example = json.loads((root / f"data/examples/{name}.json").read_text(encoding="utf-8"))
            prompt = example["prompt"]
            if not isinstance(prompt, str) or not prompt.strip() or hashlib.sha256(prompt.encode("utf-8")).hexdigest() != example["prompt_sha256"]:
                raise ValueError(f"Invalid {track} example prompt or content hash.")
            example_inputs[track] = prompt
    except (ValueError, TypeError) as error:
        parser.error(str(error))
    # Publish only explicit assets. Reject leftovers rather than accidentally
    # deploying stale examples or unrelated local files from an old build.
    site_files = [root / "site" / name for name in ("style.css", "app.js", "favicon.svg")]
    figure_files = sorted((root / "assets/figures").glob("*.png"))
    figure_files += [root / "assets/figures" / name for name in (
        "paper_collection_pipeline.svg", "paper_collection_pipeline.pdf",
        "MODEL_ICONS_LICENSE.txt", "DIAGRAM_ICONS_LICENSE.txt",
    )]
    icon_files = [root / "site/icons" / name for name in ("github-white.svg", "github-black.svg", "huggingface.svg")]
    allowed = {Path(source.name) for source in site_files} | {Path("assets") / source.name for source in figure_files}
    allowed |= {Path(f"{key}.html") for key in PAGES}
    allowed |= {Path("icons") / source.name for source in icon_files}
    allowed |= {Path("data") / name for name in METADATA_FILES} | {Path("data/results.json"), Path(".nojekyll")}
    # Earlier builds copied this developer note; it is safe to keep, but no
    # longer copied into new builds.
    allowed.add(Path("README.md"))
    if output.exists() and any(path.is_file() and path.relative_to(output) not in allowed for path in output.rglob("*")):
        parser.error("Build output contains unexpected files. Choose an empty output directory.")
    output.mkdir(parents=True, exist_ok=True)
    for source in site_files:
        shutil.copy2(source, output / source.name)
    (output / "assets").mkdir(exist_ok=True)
    for source in figure_files:
        shutil.copy2(source, output / "assets" / source.name)
    (output / "icons").mkdir(exist_ok=True)
    for source in icon_files:
        shutil.copy2(source, output / "icons" / source.name)
    data = output / "data"
    data.mkdir(exist_ok=True)
    for name in METADATA_FILES:
        shutil.copy2(metadata / name, data / name)
    (data / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    # Keep returning visitors on matching HTML, styling, code, and score data.
    result_version = hashlib.sha256((data / "results.json").read_bytes()).hexdigest()[:12]
    script = output / "app.js"
    script.write_text(script.read_text(encoding="utf-8").replace(
        "'data/results.json'", f"'data/results.json?v={result_version}'"
    ), encoding="utf-8")
    layout = (root / "site/layout.html").read_text(encoding="utf-8")
    pages = {key: (root / f"site/{key}.html").read_text(encoding="utf-8") for key in PAGES}
    for track, prompt in example_inputs.items():
        marker = f"<!-- {track.upper()}_MODEL_INPUT -->"
        if sum(content.count(marker) for content in pages.values()) != 1 or pages["examples"].count(marker) != 1:
            parser.error(f"Expected one {track} prompt placeholder.")
        formatted = re.sub(r"^(\[[^\n]+\])$", r'<span class="prompt-label">\1</span>', html.escape(prompt), flags=re.MULTILINE)
        pages["examples"] = pages["examples"].replace(marker, formatted)
    for name, attribute in (("style.css", "href"), ("app.js", "src")):
        version = hashlib.sha256((output / name).read_bytes()).hexdigest()[:12]
        layout = layout.replace(f'{attribute}="{name}"', f'{attribute}="{name}?v={version}"')
    for key, (label, description) in PAGES.items():
        title = "LegalScope · Exam-to-Case Legal Reasoning" if key == "index" else f"{label} · LegalScope"
        navigation = "\n".join(
            f'<a href="{target}.html"' + (' aria-current="page"' if target == key else '') + f'>{html.escape(name)}</a>'
            for target, (name, _) in PAGES.items()
        )
        page = layout.replace("{{PAGE_TITLE}}", html.escape(title)).replace("{{PAGE_DESCRIPTION}}", html.escape(description))
        page = page.replace("{{PAGE_KEY}}", key).replace("<!-- MAIN_NAV -->", navigation).replace("<!-- PAGE_CONTENT -->", pages[key])
        (output / f"{key}.html").write_text(page, encoding="utf-8")
    (output / ".nojekyll").touch()
    print(f"Built {len(PAGES)} project pages with {len(results)} model groups: {output}")


if __name__ == "__main__":
    main()

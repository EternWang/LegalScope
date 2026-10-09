"""Create lossless Hub loader tables from an already reviewed public package.

This converts storage formats only; it does not clear source redistribution
rights, select new records, or reconstruct private evaluation prompts.
Install the optional `release` dependencies before running.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

def read_case_tables(package: Path) -> tuple[dict, dict | None]:
    """Accept only the reviewed case JSONL files and verify their joins before conversion."""
    cases = package / "data/cases"
    if not cases.exists():
        return {}, None
    manifest = json.loads((cases / "manifest.json").read_text(encoding="utf-8"))
    tables = {}
    for name, count_key in (("case_prompts", "case_prompts"),
                            ("case_scoring_references", "scoring_references")):
        source = cases / f"{name}.jsonl"
        expected = manifest["files"][source.name]
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected["sha256"]:
            raise ValueError(f"Case content differs from the reviewed manifest: {source.name}")
        rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(rows) != expected["rows"] or len(rows) != manifest[count_key]:
            raise ValueError(f"Case row count differs from the reviewed manifest: {source.name}")
        if len({r["review_id"] for r in rows}) != len(rows):
            raise ValueError(f"Duplicate case review IDs: {source.name}")
        tables[cases / f"{name}.parquet"] = rows
    prompts = tables[cases / "case_prompts.parquet"]
    references = tables[cases / "case_scoring_references.parquet"]
    by_id = {r["review_id"]: r for r in references}
    if set(by_id) != {p["review_id"] for p in prompts}:
        raise ValueError("Prompt and reference review IDs do not match.")
    for prompt in prompts:
        if any(prompt[k] != by_id[prompt["review_id"]][k] for k in ("document_id", "issue_id")):
            raise ValueError("Prompt and reference case/issue joins do not match.")
    pairs = Counter((p["document_id"], p["issue_id"], p["stance"]) for p in prompts)
    issues = {(p["document_id"], p["issue_id"]) for p in prompts}
    if (len(issues) != manifest["issues"] or
            len({p["document_id"] for p in prompts}) != manifest["judgments"] or
            Counter(p["stance"] for p in prompts) != manifest["stance_counts"] or
            any(pairs[(doc, issue, stance)] != 1 for doc, issue in issues for stance in ("support", "oppose"))):
        raise ValueError("Case grouping or paired stances differ from the reviewed manifest.")
    return tables, manifest


def prepare(package: Path) -> dict:
    import pyarrow as pa
    import pyarrow.parquet as pq

    metadata = package / "data/metadata"
    tables = {}
    for name in ("model_performance", "model_groups", "source_composition"):
        with (metadata / f"{name}.csv").open(encoding="utf-8-sig", newline="") as handle:
            records = list(csv.DictReader(handle))
        for row in records:
            for key in row:
                if (name == "model_performance" and key != "model_group") or key == "percent":
                    row[key] = float(row[key])
                elif key in ("model_index", "count"):
                    row[key] = int(row[key])
        tables[metadata / f"{name}.parquet"] = records

    sources = package / "data/victorian_bar"
    source_file = sources / "source_excerpts.jsonl"
    manifest_path = sources / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if hashlib.sha256(source_file.read_bytes()).hexdigest() != manifest["sha256"]:
        raise ValueError("Source excerpt content differs from the reviewed manifest.")
    records = [json.loads(line) for line in source_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(records) != manifest["rows"] or len({row["item_id"] for row in records}) != len(records):
        raise ValueError("Source count or item identity differs from the reviewed manifest.")
    tables[sources / "source_excerpts.parquet"] = records
    case_tables, case_manifest = read_case_tables(package)
    tables.update(case_tables)
    written = {}
    for path, records in tables.items():
        pq.write_table(pa.Table.from_pylist(records), path, compression="zstd", write_page_index=True)
        if pq.read_table(path).to_pylist() != records:
            raise ValueError(f"Parquet round-trip changed values: {path.name}")
        written[path.relative_to(package).as_posix()] = {"rows": len(records), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    manifest["parquet_sha256"] = written["data/victorian_bar/source_excerpts.parquet"]["sha256"]
    manifest["parquet_note"] = "Lossless storage conversion of source_excerpts.jsonl; identical fields, source wording and license notices."
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if case_manifest is not None:
        for path in case_tables:
            case_manifest["files"][path.name] = written[path.relative_to(package).as_posix()]
        (package / "data/cases/manifest.json").write_text(
            json.dumps(case_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.package_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()

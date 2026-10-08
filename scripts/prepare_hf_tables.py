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
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


def prepare(package: Path) -> dict:
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
    written = {}
    for path, records in tables.items():
        pq.write_table(pa.Table.from_pylist(records), path, compression="zstd", write_page_index=True)
        if pq.read_table(path).to_pylist() != records:
            raise ValueError(f"Parquet round-trip changed values: {path.name}")
        written[path.relative_to(package).as_posix()] = {"rows": len(records), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    manifest["parquet_sha256"] = written["data/victorian_bar/source_excerpts.parquet"]["sha256"]
    manifest["parquet_note"] = "Lossless storage conversion of source_excerpts.jsonl; identical fields, source wording and license notices."
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.package_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()

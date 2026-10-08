"""Regression checks for accidental export and publication failures."""
from __future__ import annotations

import csv
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = script("build_site")
extract = script("extract_public_sample")


class ReleaseSafetyTests(unittest.TestCase):
    def test_build_cannot_target_source_or_escape_repository(self):
        for path in (ROOT, ROOT.parent / "elsewhere", ROOT / "site", ROOT / "data/metadata", ROOT / "assets/build", ROOT / ".git/build"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                build.validate_output_path(ROOT, path)
        build.validate_output_path(ROOT, ROOT / "_site")

    def test_legacy_export_cannot_replace_published_files(self):
        for path in ("data", "data/metadata", "site", ".", ".."):
            with self.subTest(path=path), self.assertRaises(ValueError):
                extract.private_output_path(path)
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "new-preview"
            self.assertEqual(extract.private_output_path(str(output)), output.resolve())
            output.mkdir()
            (output / "keep.txt").write_text("existing work", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract.private_output_path(str(output))
            self.assertEqual((output / "keep.txt").read_text(), "existing work")

    def test_zero_sample_does_not_export_all_rows(self):
        rows = [{"group": "a"}, {"group": "b"}]
        self.assertEqual(extract.stratified_sample(rows, ("group",), 0), [])
        with self.assertRaises(ValueError):
            extract.stratified_sample(rows, ("group",), -1)
        self.assertEqual(len(extract.stratified_sample(rows, ("group",), 1)), 1)

    def test_build_rejects_invalid_scores_and_duplicate_models(self):
        with tempfile.TemporaryDirectory() as folder:
            metadata = Path(folder)
            for name in build.METADATA_FILES:
                shutil.copy2(ROOT / "data/metadata" / name, metadata / name)
            path = metadata / "model_performance.csv"
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                fields, original = reader.fieldnames, list(reader)
            self.assertEqual(len(build.load_results(metadata)), 28)
            for column, value in [("citation", "NaN"), ("citation", "inf"), ("citation", "-1"), ("citation", "101"), ("citation", ""), ("model_group", original[1]["model_group"])]:
                rows = [dict(row) for row in original]
                rows[0][column] = value
                with path.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                    build.load_results(metadata)


if __name__ == "__main__":
    unittest.main()

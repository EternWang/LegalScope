from __future__ import annotations

import csv
import json
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata"


def read_csv(name: str) -> list[dict[str, str]]:
    with (METADATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class MetadataConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = json.loads(
            (METADATA / "dataset_summary.json").read_text(encoding="utf-8")
        )

    def test_dataset_and_validation_response_counts(self) -> None:
        counts = self.summary["counts"]
        for item_key, response_key in [
            ("public_exam_items", "public_exam_model_responses"),
            ("real_case_issue_stance_prompts", "real_case_model_responses"),
            ("human_public_exam_items", "human_public_exam_responses"),
            ("human_real_case_prompts", "human_real_case_responses"),
        ]:
            with self.subTest(response_key=response_key):
                self.assertEqual(
                    counts[response_key], counts[item_key] * counts["model_groups"]
                )
        for total, first, second in [
            ("dataset_items_total", "public_exam_items", "real_case_issue_stance_prompts"),
            ("dataset_model_responses_total", "public_exam_model_responses", "real_case_model_responses"),
            ("human_validation_items_total", "human_public_exam_items", "human_real_case_prompts"),
            ("human_validation_responses_total", "human_public_exam_responses", "human_real_case_responses"),
        ]:
            self.assertEqual(counts[total], counts[first] + counts[second])
        self.assertEqual(counts["real_case_issue_stance_prompts"], 2 * counts["real_case_legal_issues"])
        for module in self.summary["dataset_modules"]:
            self.assertEqual(module["model_groups"], counts["model_groups"])
            self.assertEqual(module["evaluations"], module["rows"] * module["model_groups"])

    def test_current_and_historical_audits_keep_separate_pools(self) -> None:
        audits = self.summary["robustness_audit"]
        current = audits["current_dimension_contrast"]
        counts = self.summary["counts"]
        self.assertEqual(current["prompts"], counts["real_case_issue_stance_prompts"])
        self.assertEqual(current["judgments"], counts["deidentified_chinese_judgments"])
        self.assertEqual(current["model_responses"], counts["real_case_model_responses"])
        self.assertEqual(current["human_responses"], counts["human_real_case_responses"])
        historical = audits["historical_t1"]
        self.assertEqual(historical["model_responses"], historical["prompts"] * historical["model_groups"])
        self.assertEqual(historical["model_groups"], 20)
        self.assertEqual(historical["model_responses"], 1520)
        fixed = audits["fixed_answer_stability"]
        self.assertEqual(fixed["responses"], fixed["prompts"] * fixed["model_groups"])
        self.assertEqual(fixed["responses"], 200)
        self.assertEqual(fixed["independent_rescoring_runs"], 5)

    def test_source_composition_counts_and_percentages(self) -> None:
        groups = defaultdict(list)
        for row in read_csv("source_composition.csv"):
            groups[(row["split"], row["dimension"])].append(row)
        # Workshop paper Sections 3.1-3.2 and Tables 5, 15-16.
        expected = {
            ("public_exam", "country"): 861,
            ("public_exam", "legal_category"): 861,
            ("public_exam_us_source", "source"): 603,
            ("real_case", "legal_category"): 276,
        }
        self.assertEqual(set(groups), set(expected))
        for group, total in expected.items():
            with self.subTest(group=group):
                rows = groups[group]
                self.assertEqual(sum(int(row["count"]) for row in rows), total)
                self.assertEqual(len(rows), len({row["value"] for row in rows}))
                for row in rows:
                    self.assertAlmostEqual(
                        float(row["percent"]), int(row["count"]) / total * 100, delta=0.051
                    )
        self.assertEqual(
            {r["value"] for r in groups[("real_case", "legal_category")]},
            {"Tort", "Contract", "Criminal", "Intellectual Property", "Administrative", "Civil Procedure", "Property"},
        )

    def test_model_roster_and_performance_cover_same_groups(self) -> None:
        models = read_csv("model_groups.csv")
        names = {row["model_group"] for row in models}
        self.assertEqual(len(models), 28)
        self.assertEqual(len(names), 28)
        self.assertEqual([int(row["model_index"]) for row in models], list(range(1, 29)))
        for name in ("GPT-5.5 High", "GPT-5.5 Medium", "GLM-5 low", "DeepSeek-V4-Pro", "Gemini-3.5-Flash"):
            self.assertIn(name, names)
        results = read_csv("model_performance.csv")
        self.assertEqual(len(results), 28)
        self.assertEqual({row["model_group"] for row in results}, names)
        for row in results:
            values = {k: float(v) for k, v in row.items() if k != "model_group"}
            self.assertTrue(all(0 <= v <= 100 for v in values.values()))
            # Table 3 publishes rounded values; derived means can differ by 0.1.
            self.assertAlmostEqual(values["real_case_auto"], sum(values[k] for k in ("citation", "constraint", "argument")) / 3, delta=0.101)
            for endpoint in ("auto", "human"):
                self.assertAlmostEqual(values[f"overall_{endpoint}"], (values[f"public_exam_{endpoint}"] + values[f"real_case_{endpoint}"]) / 2, delta=0.101)
        # Checks against the workshop's headline means, not rerun scores.
        for column, expected in [("public_exam_auto", 72.6), ("real_case_auto", 73.0), ("citation", 66.9), ("constraint", 79.3), ("argument", 72.6)]:
            self.assertAlmostEqual(sum(float(r[column]) for r in results) / 28, expected, delta=0.1)


if __name__ == "__main__":
    unittest.main()

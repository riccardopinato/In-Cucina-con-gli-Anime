"""Portable R1 v2 regression: discovery, evidence, fail-closed and read-only behavior."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_v2 import scan, scan_python, scan_dart, scan_workflow, scan_recipe_catalog


class QualityV2Tests(unittest.TestCase):
    def test_python_ast_findings_are_source_anchored(self):
        result = scan_python("lib/a.py", "def x():\n    eval('1 + 1')\n    try:\n        pass\n    except:\n        pass\n")
        self.assertEqual({x["ruleId"] for x in result},
                         {"PY_DYNAMIC_EXECUTION", "PY_BARE_EXCEPT"})
        self.assertEqual({x["line"] for x in result}, {2, 5})
        self.assertTrue(all(x["humanReviewEvidence"] is None for x in result))
        self.assertEqual(scan_python("lib/a.py", "def f():\n    pass\n"), [])
        self.assertEqual(scan_python("lib/a.py", "def (:\n")[0]["ruleId"],
                         "PY_PARSE_ERROR")

    def test_dart_and_workflow_review_heuristics(self):
        dart = scan_dart("lib/app.dart", '// print("skip");\nprint("test");\nfinal x = Uri.parse("http://host");')
        self.assertEqual([x["ruleId"] for x in dart],
                         ["DART_DEBUG_OUTPUT", "DART_PLAINTEXT_HTTP"])
        yml = ("name: test\n"
               "on:\n  pull_request_target:\n"
               "permissions: write-all\n"
               "jobs:\n  test:\n    steps:\n"
               "      - uses: actions/checkout@v4\n"
               "      - uses: actions/setup-python@"
               + "a" * 40 + "\n")
        found = scan_workflow(".github/workflows/a.yml", yml)
        self.assertEqual({f["ruleId"] for f in found},
                         {"GHA_PRIVILEGED_PR_EVENT", "GHA_WRITE_ALL", "GHA_ACTION_UNPINNED"})
        self.assertNotIn("a" * 40, json.dumps(found))

    def test_dynamic_content_finds_new_issues_without_fixed_id_list(self):
        data = {
            "recipes": [
                {"id": "new_recipe", "title": "Test", "description": "Example",
                 "times": {"prepMinutes": 20, "sourceCookMinutes": 20, "totalElapsedMinutes": 10},
                 "ingredients": [
                     {"id": "egg", "componentRef": "long_prep"},
                     {"id": "egg", "componentRef": "missing"},
                 ],
                 "steps": [{"instruction": "Servi con tuorlo d'uovo fresco."}]},
                {"id": "new_recipe", "title": "", "description": "",
                 "ingredients": [], "steps": []},
            ],
            "reusableComponents": {"long_prep": {"totalElapsedMinutes": 180}},
        }
        found = scan_recipe_catalog("authoring/test.json", json.dumps(data))
        rules = {f["ruleId"] for f in found}
        self.assertTrue({"CONTENT_DUPLICATE_RECIPE", "CONTENT_DUPLICATE_INGREDIENT",
                         "CONTENT_MISSING_COMPONENT", "CONTENT_TIME_INCONSISTENCY",
                         "CONTENT_MISSING_STEPS", "CULINARY_RAW_YOLK_REVIEW",
                         "CULINARY_PREMADE_DEPENDENCY"}.issubset(rules))
        self.assertFalse(any("Servi con tuorlo" in json.dumps(f) for f in found))
        self.assertEqual(scan_recipe_catalog("x.json", "{}")[0]["ruleId"],
                         "CONTENT_SCHEMA")

    def test_three_parallel_modes_generate_independent_noncertifying_reports(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for d in ["tool", "lib", ".github/workflows", "authoring"]:
                (root / d).mkdir(parents=True)
            (root / "tool/sample.py").write_text("eval('1')\n", encoding="utf-8")
            (root / "lib/a.dart").write_text('print("hi");\n', encoding="utf-8")
            (root / ".github/workflows/scan.yml").write_text(
                "- uses: actions/checkout@v4\n", encoding="utf-8")
            (root / "authoring/content.json").write_text('{"recipes": []}', encoding="utf-8")
            cfg = {"schemaVersion": 1, "profile": "fixture",
                   "paths": {"code": ["tool/**/*.py", "lib/**/*.dart"],
                             "content": ["authoring/*.json"],
                             "workflows": [".github/workflows/*.yml"]}}
            before = sorted((p.relative_to(root).as_posix(), p.read_bytes())
                            for p in root.rglob("*") if p.is_file())
            reports = [scan(root, cfg, mode, "fixed-commit") for mode in
                       ("code", "content", "workflows")]
            after = sorted((p.relative_to(root).as_posix(), p.read_bytes())
                           for p in root.rglob("*") if p.is_file())
            self.assertEqual(before, after)
            self.assertEqual([x["filesScanned"] for x in reports], [2, 1, 1])
            self.assertTrue(all(x["readOnly"] and not x["selfRepairEnabled"]
                                and x["certification"] == "NOT_CERTIFIED"
                                and x["humanApprovals"] == 0 for x in reports))
            self.assertTrue(all(x["sourceSha"] == "fixed-commit" for x in reports))
            self.assertEqual(reports[0], scan(root, cfg, "code", "fixed-commit"))
            self.assertEqual([x["mode"] for x in reports],
                             ["code", "content", "workflows"])

    def test_invalid_scope_fail_closed_and_secret_values_not_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "code.py").write_text("eval('TOP-SECRET-UNIQUE-VALUE')\n",
                                          encoding="utf-8")
            cfg = {"schemaVersion": 1, "paths": {"code": ["*.py"]}}
            report = scan(root, cfg, "code")
            self.assertEqual(report["counts"]["high"], 1)
            self.assertNotIn("TOP-SECRET-UNIQUE-VALUE", json.dumps(report))
            cfg["paths"]["code"] = ["../outside/*.py"]
            with self.assertRaisesRegex(ValueError, "unsafe"):
                scan(root, cfg, "code")
            cfg["paths"]["code"] = ["/etc/**/*.py"]
            with self.assertRaisesRegex(ValueError, "unsafe"):
                scan(root, cfg, "code")
            cfg["paths"]["code"] = ["*.py"]
            cfg["schemaVersion"] = 99
            with self.assertRaisesRegex(ValueError, "configuration"):
                scan(root, cfg, "code")


if __name__ == "__main__":
    unittest.main()

"""v2.4-B official Dart JSON adapter: source and SDK provenance validation."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_v24b_official import (
    EXPECTED_FLUTTER, normalize, path_in_checkout, validate_version,
)

SHA = "a" * 40
TOOL = {
    "frameworkVersion": EXPECTED_FLUTTER,
    "dartSdkVersion": "3.13.1",
    "frameworkRevision": "a" * 40,
}
EMPTY = {"version": 1, "diagnostics": []}


def diagnostic(file: str, *, code="unused_local_variable", severity="WARNING",
               line=5, offset=42, message="private secret should not leak"):
    return {
        "code": code, "severity": severity, "type": "STATIC_WARNING",
        "location": {"file": file, "range": {
            "start": {"offset": offset, "line": line, "column": 3},
            "end": {"offset": offset + 6, "line": line, "column": 9},
        }},
        "problemMessage": message,
        "correctionMessage": "DANGEROUS SECRET",
        "documentation": "https://example.invalid/private",
    }


class OfficialDartEvidenceTests(unittest.TestCase):
    def test_clean_output_is_not_project_certification(self):
        with tempfile.TemporaryDirectory() as d:
            out = normalize(EMPTY, TOOL, root=Path(d), source_sha=SHA, exit_code=0)
            self.assertEqual(out["status"], "ANALYZED_CLEAN")
            self.assertEqual(out["qualityGate"], "CLEAN")
            self.assertEqual(out["counts"], {"ERROR": 0, "WARNING": 0, "INFO": 0})
            self.assertTrue(out["readOnly"])
            self.assertFalse(out["selfRepairEnabled"])
            self.assertEqual(out["certification"], "NOT_CERTIFIED")
            self.assertEqual(out["toolVersions"]["flutter"], EXPECTED_FLUTTER)

    def test_machine_evidence_uses_real_rule_location_not_messages(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            file = root / "lib/demo.dart"
            file.parent.mkdir()
            file.write_text("test", encoding="utf-8")
            data = {"version": 1, "diagnostics": [
                diagnostic(str(file)),
                diagnostic("lib/demo.dart", code="undefined_method",
                           severity="ERROR", line=10, offset=110),
            ]}
            before = copy.deepcopy(data)
            report = normalize(data, TOOL, root=root, source_sha=SHA, exit_code=3)
            self.assertEqual(report["status"], "ANALYZED_WITH_FINDINGS")
            self.assertEqual(report["qualityGate"], "BLOCKING_FINDINGS")
            self.assertEqual(report["counts"]["ERROR"], 1)
            self.assertEqual(report["counts"]["WARNING"], 1)
            self.assertEqual(report["findings"][0]["path"], "lib/demo.dart")
            self.assertEqual(len({x["id"] for x in report["findings"]}), 2)
            serialized = json.dumps(report)
            for secret in ("private secret", "DANGEROUS SECRET", "example.invalid"):
                self.assertNotIn(secret, serialized)
            self.assertEqual(data, before)

    def test_info_level_diagnostic_is_review_not_silent_clean(self):
        with tempfile.TemporaryDirectory() as d:
            data = {"version": 1, "diagnostics": [
                diagnostic("lib/a.dart", code="avoid_print", severity="INFO")]}
            report = normalize(data, TOOL, root=Path(d),
                               source_sha=SHA, exit_code=0)
            self.assertEqual(report["qualityGate"], "REVIEW_ONLY")
            self.assertEqual(report["counts"]["INFO"], 1)
            self.assertEqual(report["findings"][0]["severity"], "info")

    def test_nonzero_exit_without_diagnostics_is_tool_failure(self):
        with tempfile.TemporaryDirectory() as d:
            report = normalize(EMPTY, TOOL, root=Path(d), source_sha=SHA, exit_code=2)
            self.assertEqual(report["status"], "TOOL_FAILURE")
            self.assertEqual(report["qualityGate"], "INCOMPLETE")

    def test_wrong_or_unverifiable_sdk_version_fails_closed(self):
        for patch in (
            {"frameworkVersion": "3.42.0"},
            {"dartSdkVersion": None},
            {"frameworkRevision": "invalid"},
        ):
            version = {**TOOL, **patch}
            with self.assertRaisesRegex(ValueError, "version"):
                validate_version(version)

    def test_analyzer_json_schema_and_unknown_severity_rejected(self):
        for data in (
            [], {"version": 2, "diagnostics": []}, {"version": 1, "diagnostics": "x"},
            {"version": 1, "diagnostics": [diagnostic("lib/x.dart", severity="CRITICAL")]},
            {"version": 1, "diagnostics": [diagnostic("lib/x.dart", code="../bad")]},
        ):
            with tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError):
                    normalize(data, TOOL, root=Path(d), source_sha=SHA, exit_code=0)

    def test_outside_paths_and_source_snippets_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for value in ("../outside.dart", "/etc/passwd", "test/not_lib.dart",
                          "lib/../secret.dart", "lib\\backslash.dart"):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    path_in_checkout(value, root)
            self.assertEqual(path_in_checkout("lib/sample.dart", root),
                             "lib/sample.dart")

    def test_duplicate_finding_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            x = diagnostic("lib/test.dart")
            with self.assertRaisesRegex(ValueError, "Ambiguous repeated"):
                normalize({"version": 1, "diagnostics": [x, copy.deepcopy(x)]},
                          TOOL, root=Path(d), source_sha=SHA, exit_code=0)

    def test_invalid_line_range_and_bool_exit_code_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            x = diagnostic("lib/test.dart")
            x["location"]["range"]["start"]["line"] = 0
            with self.assertRaisesRegex(ValueError, "location"):
                normalize({"version": 1, "diagnostics": [x]},
                          TOOL, root=Path(d), source_sha=SHA, exit_code=0)
            with self.assertRaisesRegex(ValueError, "exit code"):
                normalize(EMPTY, TOOL, root=Path(d), source_sha=SHA, exit_code=True)

    def test_fixture_is_deterministic_and_machine_generated(self):
        with tempfile.TemporaryDirectory() as d:
            data = {"version": 1, "diagnostics": [diagnostic("lib/sample.dart")]}
            left = normalize(data, TOOL, root=Path(d), source_sha=SHA, exit_code=3)
            right = normalize(data, TOOL, root=Path(d), source_sha=SHA, exit_code=3)
            self.assertEqual(left, right)
            self.assertEqual(left["sourceSha"], SHA)

    def test_workflow_pins_same_flutter_as_development(self):
        official = Path(".github/workflows/quality-engine-v24b-official.yml").read_text()
        dev = Path(".github/workflows/dev-checks.yml").read_text()
        self.assertIn('flutter-version: "3.47.3"', official)
        self.assertIn('flutter-version: "3.47.3"', dev)
        self.assertIn("dart analyze --format=json lib", official)
        self.assertIn("flutter --version --machine", official)
        self.assertIn("quality-v24b-dart-evidence", official)
        self.assertIn("contents: read", official)
        self.assertNotIn("contents: write", official)
        self.assertNotIn("pull_request_target:", official)


if __name__ == "__main__":
    unittest.main()

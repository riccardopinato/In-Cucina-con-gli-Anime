"""v2.4-A: isolated, grounded, no-network/static review leads."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_v24_static import (
    dart, kotlin, android_manifest, gradle, scan,
)

SHA = "a" * 40
CONFIG = {
    "schemaVersion": 1, "profile": "test",
    "paths": {
        "dart": ["lib/**/*.dart"], "kotlin": ["android/**/*.kt"],
        "android_manifest": ["android/**/AndroidManifest.xml"],
        "gradle": ["android/**/*.gradle", "android/**/*.gradle.kts"],
    },
}


class StaticAdapterTests(unittest.TestCase):
    def test_01_dart_tls_and_release_logging_are_review_leads(self):
        code = 'x.badCertificateCallback = (a,b,c) => true;\ndebugPrint("debug");'
        findings = dart("lib/net.dart", code)
        self.assertEqual({f["ruleId"] for f in findings},
                         {"DART_TLS_CERT_BYPASS_CANDIDATE", "DART_RELEASE_LOGGING"})
        self.assertTrue(all(f["humanReviewEvidence"] is None for f in findings))
        self.assertTrue(any(f["severity"] == "high" for f in findings))

    def test_02_dart_sensitive_storage_and_suppressed_lints(self):
        source = '// ignore_for_file: unnecessary_cast\nprefs.setString("refresh_token", value);\n'
        rules = {f["ruleId"] for f in dart("lib/a.dart", source)}
        self.assertEqual(rules, {"DART_SENSITIVE_PREF_KEY_CANDIDATE",
                                 "DART_FILE_LINT_SUPPRESSION"})

    def test_03_dart_comments_are_not_reported_as_code(self):
        src = '// debugPrint("do not report");\n/* badCertificateCallback = true */\n'
        self.assertEqual(dart("lib/a.dart", src), [])

    def test_04_kotlin_log_and_hostname_bypass_are_candidates(self):
        src = "Log.d(TAG, value)\nval hv = ALLOW_ALL_HOSTNAME_VERIFIER"
        rules = [f["ruleId"] for f in kotlin("Main.kt", src)]
        self.assertEqual(rules, ["KOTLIN_RUNTIME_LOGGING", "KOTLIN_TLS_HOSTNAME_BYPASS"])

    def test_05_gradle_flags_dynamic_dependencies_and_http_repo(self):
        src = 'implementation("org.example:example:+")\nmaven { url "http://repo.example" }'
        rules = {f["ruleId"] for f in gradle("app/build.gradle", src)}
        self.assertEqual(rules, {"GRADLE_DYNAMIC_DEPENDENCY",
                                 "GRADLE_PLAINTEXT_REPOSITORY"})

    def test_06_manifest_flags_cleartext_debug_and_multiple_exported(self):
        xml = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
          <application android:usesCleartextTraffic="true" android:debuggable="true">
            <activity android:name=".A" android:exported="true"/>
            <activity android:name=".B" android:exported="true"/>
          </application></manifest>'''
        issues = android_manifest("android/app/src/main/AndroidManifest.xml", xml)
        self.assertEqual(len(issues), 4)
        self.assertEqual(len({i["id"] for i in issues}), 4)
        self.assertIn("ANDROID_DEBUGGABLE_MANIFEST", {i["ruleId"] for i in issues})

    def test_07_malformed_manifest_fails_to_parse_without_network(self):
        issues = android_manifest("AndroidManifest.xml", "<manifest")
        self.assertEqual(issues[0]["ruleId"], "ANDROID_MANIFEST_PARSE")

    def test_08_no_matching_android_kotlin_is_not_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "lib").mkdir()
            (root / "lib/app.dart").write_text("void main() {}", encoding="utf-8")
            result = scan(root, CONFIG, SHA)
            self.assertEqual(result["coverage"]["dart"]["filesScanned"], 1)
            for mode in ("kotlin", "android_manifest", "gradle"):
                self.assertEqual(result["coverage"][mode]["coverageStatus"],
                                 "NO_MATCHING_FILES")
            self.assertEqual(result["counts"]["high"], 0)
            self.assertFalse(result["selfRepairEnabled"])
            self.assertEqual(result["certification"], "NOT_CERTIFIED")

    def test_09_missing_rules_do_not_leak_any_source_values(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file = root / "lib/a.dart"
            file.parent.mkdir(parents=True)
            file.write_text('debugPrint("SECRET_TOKEN_123456");\n', encoding="utf-8")
            report = scan(root, CONFIG, SHA)
            self.assertNotIn("SECRET_TOKEN_123456", json.dumps(report))
            self.assertEqual(report["counts"]["info"], 1)

    def test_10_untrusted_paths_and_invalid_sha_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg = json.loads(json.dumps(CONFIG))
            cfg["paths"]["dart"] = ["../other/**/*"]
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                scan(root, cfg, SHA)
            with self.assertRaisesRegex(ValueError, "Invalid scan"):
                scan(root, CONFIG, "invalid")

    def test_11_symlinked_file_is_skipped_and_reported_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file = root / "lib/a.dart"
            file.parent.mkdir()
            outside = root / "b.dart"
            outside.write_text("debugPrint('secret');", encoding="utf-8")
            file.symlink_to(outside)
            result = scan(root, CONFIG, SHA)
            self.assertEqual(result["coverage"]["dart"]["filesScanned"], 0)
            self.assertEqual(result["filesSkipped"][0]["reason"], "unsafe_path")

    def test_12_fixture_reports_are_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file = root / "lib/a.dart"
            file.parent.mkdir()
            file.write_text("debugPrint('hello');\n", encoding="utf-8")
            a = scan(root, CONFIG, SHA)
            b = scan(root, CONFIG, SHA)
            self.assertEqual(a, b)
            self.assertEqual(a["sourceSha"], SHA)

    def test_13_independent_v24_workflow_is_read_only(self):
        file = Path(".github/workflows/quality-engine-v24-static.yml")
        txt = file.read_text(encoding="utf-8")
        self.assertIn("quality_engine_v24_static.py", txt)
        self.assertIn("contents: read", txt)
        self.assertIn("quality-v24a-static-analysis", txt)
        self.assertNotIn("contents: write", txt)
        self.assertNotIn("pull_request_target:", txt)


if __name__ == "__main__":
    unittest.main()

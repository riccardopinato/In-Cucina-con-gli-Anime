"""Quality v2.2: provenance-bound diagnostic plans never mutate or approve content."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_v21_history import compare
from quality_engine_v22_diagnose import RULEBOOK, diagnose

CONFIG = {
    "schemaVersion": 1, "profile": "sample",
    "paths": {"code": ["tool/**/*.py"], "content": ["authoring/*.json"],
              "workflows": [".github/workflows/*.yml"]},
    "policy": {"mode": "READ_ONLY_OBSERVATION", "autoFix": False,
               "autoMerge": False, "humanReviewRequired": True},
}


def item(rule: str, ident: str, *, path: str = "tool/app.py", line: int = 3,
         severity: str = "high", entity=None, message: str = "Original scanner message"):
    return {"id": ident, "ruleId": rule, "severity": severity,
            "path": path, "line": line, "entityId": entity, "message": message,
            "state": "REVIEW_REQUIRED", "humanReviewEvidence": None}


def scan(*found, mode="code", sha="a"*40, profile="sample"):
    return {"schemaVersion": 1, "engine": "R1_QUALITY_ENGINE_V2",
            "version": "2.0.0-pilot", "mode": mode, "sourceSha": sha,
            "profile": profile, "readOnly": True, "selfRepairEnabled": False,
            "certification": "NOT_CERTIFIED", "humanApprovals": 0,
            "filesScanned": 1, "filesSkipped": [], "findings": list(found)}


def package(report, previous=None, run="1"):
    delta, state = compare(report, CONFIG, previous,
                           repository="owner/repo", run_id=run, event="push")
    return diagnose(report, delta, CONFIG), state, delta


class DiagnoserTests(unittest.TestCase):
    def test_known_security_finding_has_safe_specific_investigation(self):
        original = scan(item("PY_SHELL_TRUE", "id001"))
        preserved = copy.deepcopy(original)
        plan, _, delta = package(original)
        self.assertEqual(plan["counts"]["active"], 1)
        self.assertEqual(plan["counts"]["priorityP0Candidates"], 1)
        self.assertEqual(plan["baselineStatus"], "ABSENT")
        self.assertEqual(plan["proposals"][0]["transition"], "UNBASELINED")
        self.assertEqual(plan["proposals"][0]["riskClass"], "security")
        self.assertEqual(plan["proposals"][0]["requiredReviewerRole"], "security_reviewer")
        self.assertEqual(plan["proposals"][0]["reviewDecision"], "PENDING_HUMAN_REVIEW")
        self.assertFalse(plan["proposals"][0]["autoFixEligible"])
        self.assertIsNone(plan["proposals"][0]["patch"])
        self.assertFalse(plan["selfRepairEnabled"])
        self.assertFalse(plan["automaticPrEnabled"])
        self.assertFalse(plan["automaticMergeEnabled"])
        self.assertEqual(plan["certification"], "NOT_CERTIFIED")
        self.assertEqual(plan["humanApprovals"], 0)
        self.assertEqual(original, preserved)
        self.assertEqual(plan["sourceSha"], delta["sourceSha"])

    def test_content_specific_human_safety_review_never_certifies(self):
        f = item("CULINARY_RAW_YOLK_REVIEW", "egg-id", path="authoring/f3k.json",
                 severity="review", entity="recipe_000153")
        plan, _, _ = package(scan(f, mode="content"))
        p = plan["proposals"][0]
        self.assertEqual(p["domain"], "content")
        self.assertEqual(p["source"]["entityRef"], "recipe_000153")
        self.assertEqual(p["requiredReviewerRole"], "qualified_food_safety_reviewer")
        self.assertEqual(p["diagnosisStatus"], "HYPOTHESIS_NOT_VALIDATED")
        self.assertEqual(p["priorityCandidate"], "P0")
        self.assertNotIn("Original scanner message", json.dumps(plan))
        self.assertNotIn("recipe safe", json.dumps(plan).lower())

    def test_lifecycle_new_persisting_and_resolved_are_not_misreported(self):
        first = scan(item("PY_BARE_EXCEPT", "a", severity="review"))
        _, baseline, _ = package(first)
        second = scan(item("PY_BARE_EXCEPT", "a", severity="review"),
                      item("PY_DYNAMIC_EXECUTION", "b"), sha="b"*40)
        plan, state, _ = package(second, baseline, "2")
        self.assertEqual(plan["counts"]["active"], 2)
        self.assertEqual({a["transition"] for a in plan["proposals"]},
                         {"NEW", "PERSISTING"})
        third = scan(item("PY_DYNAMIC_EXECUTION", "b"), sha="c"*40)
        final, _, _ = package(third, state, "3")
        self.assertEqual(final["counts"]["resolvedSinceBaseline"], 1)
        self.assertEqual(final["counts"]["active"], 1)
        self.assertEqual([a["transition"] for a in final["proposals"]], ["PERSISTING"])
        self.assertNotIn("PY_BARE_EXCEPT", [p["ruleId"] for p in final["proposals"]])

    def test_relocated_identity_binds_to_current_scanner(self):
        a = scan(item("PY_BARE_EXCEPT", "line3", line=3, severity="review"))
        _, baseline, _ = package(a)
        b = scan(item("PY_BARE_EXCEPT", "line5", line=5, severity="review"), sha="b"*40)
        plan, _, _ = package(b, baseline)
        self.assertEqual(plan["proposals"][0]["findingId"], "line3")
        self.assertEqual(plan["proposals"][0]["scannerId"], "line5")
        self.assertEqual(plan["proposals"][0]["transition"], "PERSISTING")

    def test_unsupported_new_rule_has_no_fabricated_repair(self):
        plan, _, _ = package(scan(item("NEW_RULE_ADDED_LATER", "future")))
        p = plan["proposals"][0]
        self.assertEqual(p["adapterStatus"], "UNSUPPORTED_RULE")
        self.assertEqual(p["priorityCandidate"], "P3")
        self.assertFalse(p["autoFixEligible"])
        self.assertEqual(plan["counts"]["unsupportedRules"], 1)

    def test_wrong_sha_scope_and_forged_history_fail_closed(self):
        original = scan(item("PY_SHELL_TRUE", "x"))
        _, _, delta = package(original)
        bad = copy.deepcopy(delta)
        bad["sourceSha"] = "b"*40
        with self.assertRaisesRegex(ValueError, "provenance"):
            diagnose(original, bad, CONFIG)
        bad = copy.deepcopy(delta)
        bad["scopeDigest"] = "evil"
        with self.assertRaisesRegex(ValueError, "provenance"):
            diagnose(original, bad, CONFIG)
        bad = copy.deepcopy(delta)
        bad["findings"][0]["severity"] = "info"
        with self.assertRaisesRegex(ValueError, "scanner evidence"):
            diagnose(original, bad, CONFIG)
        bad = copy.deepcopy(delta)
        bad["counts"]["UNBASELINED"] = 2
        with self.assertRaisesRegex(ValueError, "counts"):
            diagnose(original, bad, CONFIG)
        bad = copy.deepcopy(delta)
        bad["findings"] = []
        with self.assertRaisesRegex(ValueError, "omits current"):
            diagnose(original, bad, CONFIG)

    def test_malformed_paths_privacy_and_unsafe_policy(self):
        s = scan(item("PY_SHELL_TRUE", "x", path="../secrets.txt"))
        # Build a valid historical delta first; the diagnoser itself must
        # reject the unsafe relative path when invoked under the assertion.
        d, _ = compare(s, CONFIG, None, repository="owner/repo",
                       run_id="1", event="push")
        with self.assertRaisesRegex(ValueError, "finding path"):
            diagnose(s, d, CONFIG)
        s = scan(item("PY_DYNAMIC_EXECUTION", "x", entity="SECRET USER STRING; DON'T LEAK"))
        plan, _, _ = package(s)
        dumped = json.dumps(plan)
        self.assertNotIn("SECRET USER STRING", dumped)
        self.assertTrue(plan["proposals"][0]["source"]["entityRef"].startswith("sha256:"))
        for name in ("autoFix", "autoMerge", "humanReviewRequired"):
            unsafe = copy.deepcopy(CONFIG)
            unsafe["policy"][name] = not unsafe["policy"][name]
            with self.assertRaisesRegex(ValueError, "Unsafe write"):
                _, _, d = package(scan())
                diagnose(scan(), d, unsafe)

    def test_rulebook_is_non_executable_and_no_input_message_spills(self):
        self.assertTrue({"PY_DYNAMIC_EXECUTION", "DART_PLAINTEXT_HTTP",
                         "GHA_WRITE_ALL", "CULINARY_PREMADE_DEPENDENCY"}.issubset(RULEBOOK))
        report = scan(item("PY_DYNAMIC_EXECUTION", "bad", message="API_KEY=TOP-SECRET"))
        plan, _, _ = package(report)
        serialized = json.dumps(plan)
        self.assertNotIn("TOP-SECRET", serialized)
        self.assertNotIn("API_KEY=", serialized)
        for proposal in plan["proposals"]:
            self.assertIsNone(proposal["approvalEvidence"])
            self.assertIsNone(proposal["patch"])
            self.assertFalse(proposal["autoFixEligible"])

    def test_workflow_invokes_diagnosis_after_valid_history(self):
        text = Path(".github/workflows/quality-engine-v2.yml").read_text(encoding="utf-8")
        self.assertIn("tool/quality_engine_v22_diagnose.py", text)
        self.assertIn("quality-v22-proposals-", text)
        self.assertIn("actions: read", text)
        self.assertNotIn("contents: write", text)


if __name__ == "__main__":
    unittest.main()

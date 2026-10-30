"""R1 v2.1: historical comparison, provenance, missing baseline and privacy."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_v21_history import compare, digest, scope_digest, validate_report, load_json

CONFIG = {
    "schemaVersion": 1, "profile": "fixture",
    "paths": {
        "code": ["lib/**/*.dart"], "content": ["authoring/*.json"],
        "workflows": [".github/workflows/*.yml"],
    },
}


def f(key: str, line: int = 1) -> dict:
    return {
        "id": key, "ruleId": "CODE_REVIEW", "severity": "review",
        "path": "lib/app.dart", "line": line, "entityId": None,
        "message": "Check for potential issue", "humanReviewEvidence": None,
    }


def report(*issues: dict, sha: str = "a" * 40, mode: str = "code") -> dict:
    return {
        "schemaVersion": 1, "engine": "R1_QUALITY_ENGINE_V2",
        "version": "2.0.0-pilot", "profile": "fixture", "mode": mode,
        "sourceSha": sha, "filesScanned": 1, "filesSkipped": [],
        "readOnly": True, "selfRepairEnabled": False,
        "certification": "NOT_CERTIFIED", "humanApprovals": 0,
        "findings": list(issues),
    }


def evaluate(source, old=None, run="1"):
    return compare(source, CONFIG, old, repository="owner/project",
                   run_id=run, event="schedule")


class QualityV21HistoryTests(unittest.TestCase):
    def test_unbaselined_is_not_falsely_new(self):
        delta, state = evaluate(report(f("aa")))
        self.assertEqual(delta["baselineStatus"], "ABSENT")
        self.assertEqual(delta["counts"]["UNBASELINED"], 1)
        self.assertEqual(delta["counts"]["NEW"], 0)
        self.assertIsNone(delta["previousSha"])
        self.assertEqual(state["records"]["aa"]["state"], "ACTIVE")
        self.assertEqual(state["records"]["aa"]["observations"], 1)
        self.assertTrue(delta["readOnly"])
        self.assertFalse(delta["selfRepairEnabled"])
        self.assertEqual(delta["certification"], "NOT_CERTIFIED")

    def test_new_persisting_resolved_reopened_and_no_duplicate_resolution(self):
        _, a = evaluate(report(f("a")), run="1")
        b_delta, b = evaluate(report(f("a"), f("b"), sha="b"*40), a, run="2")
        self.assertEqual(b_delta["counts"]["PERSISTING"], 1)
        self.assertEqual(b_delta["counts"]["NEW"], 1)
        self.assertEqual(b["records"]["a"]["observations"], 2)
        c_delta, c = evaluate(report(f("b"), sha="c"*40), b, run="3")
        self.assertEqual(c_delta["counts"]["RESOLVED"], 1)
        self.assertEqual(c["records"]["a"]["state"], "RESOLVED")
        self.assertEqual(c["records"]["b"]["observations"], 2)
        d_delta, d = evaluate(report(f("b"), sha="d"*40), c, run="4")
        self.assertEqual(d_delta["counts"]["RESOLVED"], 0)
        self.assertEqual(d_delta["counts"]["PERSISTING"], 1)
        self.assertEqual(d["records"]["a"], c["records"]["a"])
        e_delta, e = evaluate(report(f("a"), sha="e"*40), d, run="5")
        self.assertEqual(e_delta["counts"]["REOPENED"], 1)
        self.assertEqual(e_delta["counts"]["RESOLVED"], 1)
        self.assertEqual(e["records"]["a"]["firstSeenSha"], "a"*40)
        self.assertEqual(e["records"]["a"]["observations"], 3)

    def test_same_sha_scheduled_repeat_is_persisting(self):
        a, state = evaluate(report(f("x")), run="100")
        delta, updated = evaluate(report(f("x")), state, run="101")
        self.assertEqual(delta["counts"]["PERSISTING"], 1)
        self.assertEqual(updated["records"]["x"]["observations"], 2)
        self.assertEqual(delta["sourceSha"], delta["previousSha"])

    def test_scope_engine_profile_and_repo_mismatch_fail_closed(self):
        _, baseline = evaluate(report(f("x")), run="1")
        for mutation, kwargs in (
            (lambda x: x.update({"scopeDigest": "wrong"}), {}),
            (lambda x: x.update({"repository": "other/repo"}), {}),
            (lambda x: x.update({"profile": "fake"}), {}),
            (lambda x: x.update({"certification": "CERTIFIED"}), {}),
            (lambda x: x.update({"humanApprovals": 1}), {}),
        ):
            corrupt = copy.deepcopy(baseline)
            mutation(corrupt)
            with self.assertRaisesRegex(ValueError, "Baseline provenance"):
                evaluate(report(f("x")), corrupt, run="2")
        changed = report(f("x"))
        changed["version"] = "2.2.0"
        with self.assertRaisesRegex(ValueError, "Baseline provenance"):
            evaluate(changed, baseline)
        self.assertEqual(scope_digest(CONFIG, report()), baseline["scopeDigest"])

    def test_incomplete_scan_and_untrusted_finding_are_rejected(self):
        _, baseline = evaluate(report(f("a")))
        skipped = report(sha="b"*40)
        skipped["filesSkipped"] = [{"path": "lib/app.dart", "reason": "file_exceeds_size_limit"}]
        with self.assertRaisesRegex(ValueError, "Incomplete scan"):
            evaluate(skipped, baseline)
        duplicated = report(f("a"), f("a"))
        with self.assertRaisesRegex(ValueError, "Duplicate finding IDs"):
            evaluate(duplicated, baseline)
        unverified = report(f("a"))
        unverified["humanApprovals"] = 1
        with self.assertRaisesRegex(ValueError, "Untrusted"):
            evaluate(unverified)
        invalid = report(f("a"))
        invalid["findings"][0]["line"] = 0
        with self.assertRaisesRegex(ValueError, "finding line"):
            evaluate(invalid)

    def test_outputs_do_not_leak_extra_fields_or_mutate_sources(self):
        src = report(f("a"))
        src["findings"][0]["rawSnippet"] = "SECRET VALUE SHOULD NEVER APPEAR"
        before = copy.deepcopy(src)
        delta, state = evaluate(src)
        self.assertEqual(src, before)
        self.assertNotIn("SECRET VALUE SHOULD NEVER APPEAR", json.dumps(delta))
        self.assertNotIn("SECRET VALUE SHOULD NEVER APPEAR", json.dumps(state))
        self.assertIsNone(state["records"]["a"]["entityId"])

    def test_missing_unsafe_json_and_bad_history_are_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "state.json"
            p.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must be an object"):
                load_json(p)
        _, baseline = evaluate(report(f("a")))
        baseline["records"]["a"]["observations"] = -1
        with self.assertRaisesRegex(ValueError, "Malformed prior history"):
            evaluate(report(f("a")), baseline)

    def test_cumulative_state_is_json_serializable_and_deterministic(self):
        _, b = evaluate(report(f("a"), f("b")), run="1")
        left = evaluate(report(f("b"), f("c"), sha="b"*40), b, run="2")
        right = evaluate(report(f("b"), f("c"), sha="b"*40), b, run="2")
        self.assertEqual(digest(left), digest(right))
        self.assertEqual(json.loads(json.dumps(left)), json.loads(json.dumps(right)))


if __name__ == "__main__":
    unittest.main()

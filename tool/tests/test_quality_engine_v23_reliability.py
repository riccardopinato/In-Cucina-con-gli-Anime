"""v2.3 reliability: scheduled proof, duplicate draft guards, and local Git E2E."""
from __future__ import annotations

import copy
import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_l2_draft import FIXED_ALLOWLIST, plan, apply
from quality_engine_v23_reliability import (
    REPO, build_report, check_duplicate, inspect, parse_utc,
)

NOW = dt.datetime(2026, 10, 30, 12, 0, tzinfo=dt.timezone.utc)
CONFIG = {
    "schemaVersion": 1, "enabled": True, "riskTier": "LOW_FORMAT_ONLY",
    "draftOnly": True, "autoMerge": False, "autoPublish": False,
    "allowedRule": "MD_BLANK_LINE_WHITESPACE",
    "eligiblePaths": sorted(FIXED_ALLOWLIST),
}


def run(run_id=101, *, when="2026-10-30T11:00:00Z", conclusion="success",
        event="schedule", status="completed", branch="main"):
    return {
        "id": run_id, "created_at": when, "conclusion": conclusion,
        "event": event, "status": status, "head_branch": branch,
    }


def payload(*records):
    return {"total_count": len(records), "workflow_runs": list(records)}


def workspace(root: Path, content=b"Header\n \t\nBody\n"):
    for name in FIXED_ALLOWLIST:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


class ReliabilityTests(unittest.TestCase):
    def test_01_missing_schedule_is_not_reported_as_healthy(self):
        report = build_report({
            "quality-engine-v2.yml": payload(run(event="push")),
            "quality-engine-l2-draft.yml": payload(),
        }, NOW, REPO)
        self.assertEqual(report["overall"], "ATTENTION_REQUIRED")
        self.assertTrue(all(v["status"] == "NOT_YET_VERIFIED" for v in report["checks"]))
        self.assertTrue(report["readOnly"])
        self.assertFalse(report["autoMerge"])

    def test_02_hourly_and_daily_schedule_proven_with_real_event(self):
        report = build_report({
            "quality-engine-v2.yml": payload(run(1, when="2026-10-30T11:00:00Z")),
            "quality-engine-l2-draft.yml": payload(run(2, when="2026-10-30T06:00:00Z")),
        }, NOW, REPO)
        self.assertEqual(report["overall"], "HEALTHY")
        self.assertTrue(all(c["status"] == "SCHEDULE_OBSERVED" for c in report["checks"]))

    def test_03_schedule_failure_is_not_hidden_by_successful_push(self):
        res = inspect("quality-engine-v2.yml", payload(
            run(1, when="2026-10-30T11:30:00Z", conclusion="failure"),
            run(2, when="2026-10-30T11:50:00Z", event="push")), NOW)
        self.assertEqual(res["status"], "LAST_SCHEDULE_FAILED")
        self.assertEqual(res["lastScheduledRunId"], 1)

    def test_04_old_schedule_is_stale_even_if_green(self):
        a = inspect("quality-engine-v2.yml", payload(
            run(1, when="2026-10-30T02:00:00Z")), NOW)
        b = inspect("quality-engine-l2-draft.yml", payload(
            run(2, when="2026-10-25T06:00:00Z")), NOW)
        self.assertEqual((a["status"], b["status"]), ("SCHEDULE_STALE", "SCHEDULE_STALE"))

    def test_05_queued_schedule_is_distinguished_from_success(self):
        a = inspect("quality-engine-v2.yml", payload(
            run(5, when="2026-10-30T11:55:00Z",
                status="in_progress", conclusion=None)), NOW)
        self.assertEqual(a["status"], "RUNNING_OR_QUEUED")

    def test_06_malformed_future_and_untrusted_workflow_fail_closed(self):
        cases = [
            ("quality-engine-v2.yml", payload(run(1, when="2026-10-30T12:10:00Z"))),
            ("quality-engine-v2.yml", payload(run(1, when="no timestamp"))),
            ("quality-engine-v2.yml", payload(run(1, status="nonsense"))),
            ("not-a-real-workflow.yml", payload(run(1))),
        ]
        for name, value in cases:
            with self.subTest(name=name, value=value):
                with self.assertRaises(ValueError):
                    inspect(name, value, NOW)
        with self.assertRaises(ValueError):
            parse_utc("2026-10-30T11:00:00")

    def test_07_plan_repair_identity_survives_unrelated_commit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace(root)
            p1 = plan(root, CONFIG, source_sha="a"*40, repository=REPO)
            p2 = plan(root, CONFIG, source_sha="b"*40, repository=REPO)
            self.assertNotEqual(p1["sourceSha"], p2["sourceSha"])
            self.assertEqual(p1["repairKey"], p2["repairKey"])
            self.assertEqual(len(p1["repairKey"]), 24)
            self.assertEqual(check_duplicate(p2, [], REPO)["decision"], "DRAFT_ALLOWED")

    def test_08_already_open_or_closed_draft_repair_is_not_proposed_twice(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace(root)
            p = plan(root, CONFIG, source_sha="a"*40, repository=REPO)
            allowed = check_duplicate(p, [], REPO)
            self.assertTrue(allowed["branch"].startswith("quality-l2/repair-"))
            self.assertEqual(check_duplicate(p, ["unrelated", allowed["branch"]], REPO),
                             {"decision": "ALREADY_PROPOSED", "branch": allowed["branch"]})

    def test_09_empty_plan_never_creates_draft(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace(root, b"Header\n\nContent\n")
            p = plan(root, CONFIG, source_sha="a"*40, repository=REPO)
            self.assertEqual(check_duplicate(p, [], REPO),
                             {"decision": "NO_CANDIDATE", "branch": None})

    def test_10_tampered_or_foreign_plan_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace(root)
            p = plan(root, CONFIG, source_sha="a"*40, repository=REPO)
            for key, value in (
                ("repository", "some/other"), ("draftPrOnly", False),
                ("autoMergeEnabled", True), ("humanApprovals", 1),
                ("repairKey", "../../unsafe"), ("repairKey", None),
            ):
                altered = copy.deepcopy(p)
                altered[key] = value
                with self.assertRaises(ValueError, msg=key):
                    check_duplicate(altered, [], REPO)

    def test_11_bounded_history_and_wrong_repo_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace(root)
            p = plan(root, CONFIG, source_sha="a"*40, repository=REPO)
            with self.assertRaises(ValueError):
                check_duplicate(p, ["x"]*10001, REPO)
            with self.assertRaises(ValueError):
                check_duplicate(p, [], "another/repo")
        with self.assertRaises(ValueError):
            build_report({"quality-engine-v2.yml": payload()}, NOW, REPO)

    def test_12_local_git_branch_patch_and_duplicate_stop(self):
        # Exercises plan -> authorization -> git branch -> apply -> diff ->
        # commit -> duplicate suppression; never contacts GitHub or mutates main.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace(root)
            def git(*args):
                return subprocess.check_output(
                    ["git", "-C", str(root), *args], text=True).strip()
            git("init", "-q", "-b", "main")
            git("add", "--", *sorted(FIXED_ALLOWLIST))
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "commit", "-qm", "baseline")
            sha = git("rev-parse", "HEAD")
            result = plan(root, CONFIG, source_sha=sha, repository=REPO)
            decision = check_duplicate(result, [], REPO)
            self.assertEqual(decision["decision"], "DRAFT_ALLOWED")
            git("switch", "-q", "-c", decision["branch"])
            changed = apply(root, CONFIG, result, source_sha=sha, repository=REPO)
            self.assertEqual(sorted(git("diff", "--name-only").splitlines()),
                             sorted(changed))
            git("add", "--", *changed)
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "commit", "-qm", "synthetic draft candidate")
            git("switch", "-q", "main")
            for name in FIXED_ALLOWLIST:
                self.assertEqual((root / name).read_bytes(), b"Header\n \t\nBody\n")
            same = plan(root, CONFIG, source_sha=sha, repository=REPO)
            self.assertEqual(check_duplicate(same, [decision["branch"]], REPO)["decision"],
                             "ALREADY_PROPOSED")

    def test_13_workflow_uses_history_guard_before_git_mutation(self):
        source = Path(".github/workflows/quality-engine-l2-draft.yml").read_text()
        self.assertIn("quality_engine_v23_reliability.py dedupe", source)
        self.assertIn("gh api --paginate", source)
        self.assertIn("ALREADY_PROPOSED", source)
        self.assertIn("repair-", source)
        self.assertLess(source.index("quality_engine_v23_reliability.py dedupe"),
                        source.index("git switch --create"))
        self.assertNotIn("gh pr merge", source)

    def test_14_reliability_workflow_observer_remains_read_only(self):
        source = Path(".github/workflows/quality-engine-v23-reliability.yml").read_text()
        self.assertIn("actions: read", source)
        self.assertIn("contents: read", source)
        self.assertIn("workflow_dispatch:", source)
        self.assertNotIn("pull_request_target:", source)
        self.assertNotIn("pull-requests: write", source)
        self.assertNotIn("contents: write", source)
        self.assertIn("quality_engine_v23_reliability.py", source)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Quality Engine v2.3: independently inspect scheduler proof and repair de-duplication.

Stdlib-only, read-only. Workflow collects GitHub metadata via a token with
actions:read. This module never contacts GitHub, grants approvals, or writes
to repositories. Scheduled execution is best effort; absence is NOT_VERIFIED.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO = "riccardopinato/In-Cucina-con-gli-Anime"
SCHEMA = 1
WORKFLOWS = {
    "quality-engine-v2.yml": 60,
    "quality-engine-l2-draft.yml": 1440,
}
HEX_KEY = re.compile(r"^[a-f0-9]{24}$")
STATUSES = {"completed", "queued", "in_progress", "pending", "requested", "waiting"}
CONCLUSIONS = {
    "success", "failure", "cancelled", "skipped", "timed_out",
    "action_required", "neutral", "stale", "startup_failure",
}


def parse_utc(value: str) -> dt.datetime:
    if not isinstance(value, str):
        raise ValueError("Run timestamp must be a string")
    try:
        obj = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Malformed workflow timestamp") from exc
    if obj.tzinfo is None:
        raise ValueError("Workflow timestamp must include UTC offset")
    return obj.astimezone(dt.timezone.utc)


def check_duplicate(plan: dict, head_refs: list[str], repository: str) -> dict:
    """Decision must be made before any authenticated remote mutation."""
    if (repository != REPO or not isinstance(plan, dict)
            or plan.get("schemaVersion") != 1
            or plan.get("engine") != "QUALITY_ENGINE_L2_DRAFT_REPAIR"
            or plan.get("repository") != REPO
            or plan.get("draftPrOnly") is not True
            or plan.get("autoMergeEnabled") is not False
            or plan.get("contentCertification") != "NOT_CERTIFIED"
            or plan.get("humanApprovals") != 0):
        raise ValueError("Unauthorized draft plan")
    changes = plan.get("changes")
    key = plan.get("repairKey")
    if not isinstance(changes, list):
        raise ValueError("Invalid repair changes")
    if not changes:
        if key is not None:
            raise ValueError("Empty repair has nonempty identity")
        return {"decision": "NO_CANDIDATE", "branch": None}
    if len(changes) > 3 or not isinstance(key, str) or not HEX_KEY.fullmatch(key):
        raise ValueError("Invalid bounded repair identity")
    if (not isinstance(head_refs, list)
            or len(head_refs) > 10000
            or any(not isinstance(v, str) or len(v) > 300 for v in head_refs)):
        raise ValueError("Untrusted pull request history")
    branch = "quality-l2/repair-" + key
    return {
        "decision": "ALREADY_PROPOSED" if branch in head_refs else "DRAFT_ALLOWED",
        "branch": branch,
    }


def inspect(name: str, data: dict, now: dt.datetime, *,
            repository: str = REPO) -> dict:
    if name not in WORKFLOWS or repository != REPO:
        raise ValueError("Unknown workflow/repository")
    if not isinstance(data, dict) or not isinstance(data.get("workflow_runs"), list):
        raise ValueError("Untrusted GitHub Actions response")
    runs = data["workflow_runs"]
    if len(runs) > 100:
        raise ValueError("Too many workflow records")
    eligible = []
    for run in runs:
        if not isinstance(run, dict):
            raise ValueError("Invalid workflow run record")
        if run.get("head_branch") != "main" or run.get("event") != "schedule":
            continue
        if (not isinstance(run.get("id"), int) or isinstance(run["id"], bool)
                or run["id"] <= 0
                or run.get("status") not in STATUSES
                or (run.get("conclusion") is not None
                    and run["conclusion"] not in CONCLUSIONS)):
            raise ValueError("Invalid scheduled workflow run")
        started = parse_utc(run.get("created_at"))
        if started > now + dt.timedelta(minutes=5):
            raise ValueError("Future workflow run timestamp")
        eligible.append((started, run))
    eligible.sort(key=lambda q: (q[0], q[1]["id"]), reverse=True)
    every = WORKFLOWS[name]
    # GitHub schedule isn't a guaranteed timer. Warn on missing/delayed evidence
    # without inventing runs, successful repair PRs or 24/7 operation.
    threshold = every * 3
    if not eligible:
        health = "NOT_YET_VERIFIED"
        last_id = None
        last_seen = None
        age = None
    else:
        date, latest = eligible[0]
        last_id = latest["id"]
        last_seen = date.isoformat()
        age = round((now - date).total_seconds() / 60)
        if latest["status"] != "completed":
            health = "RUNNING_OR_QUEUED"
        elif latest["conclusion"] != "success":
            health = "LAST_SCHEDULE_FAILED"
        elif age > threshold:
            health = "SCHEDULE_STALE"
        else:
            health = "SCHEDULE_OBSERVED"
    return {
        "workflow": name, "expectedIntervalMinutes": every,
        "graceMinutes": threshold,
        "status": health,
        "lastScheduledRunId": last_id,
        "lastScheduledStart": last_seen,
        "minutesSinceScheduledStart": age,
        "scheduledEvidenceCountInWindow": len(eligible),
    }


def build_report(runs: dict[str, dict], now: dt.datetime, repository: str) -> dict:
    if now.tzinfo is None:
        raise ValueError("Audit timestamp must be timezone aware")
    now = now.astimezone(dt.timezone.utc)
    if set(runs) != set(WORKFLOWS):
        raise ValueError("Both workflows must be audited")
    checks = [inspect(name, runs[name], now, repository=repository)
              for name in sorted(WORKFLOWS)]
    return {
        "schemaVersion": SCHEMA, "engine": "QUALITY_ENGINE_V23_RELIABILITY",
        "repository": repository, "asOf": now.isoformat(),
        "readOnly": True, "certification": "NOT_CERTIFIED",
        "humanApprovals": 0, "autoMerge": False,
        "checks": checks,
        "overall": ("HEALTHY" if all(x["status"] == "SCHEDULE_OBSERVED" for x in checks)
                    else "ATTENTION_REQUIRED"),
        "limitations": [
            "GitHub scheduled jobs are best effort, not continuous operation",
            "Schedules verified only by actual schedule event metadata",
            "This report does not prove an autonomous draft PR was created",
        ],
    }


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "dedupe":
        cli = argparse.ArgumentParser(description="Validate autonomous draft uniqueness")
        cli.add_argument("dedupe")
        cli.add_argument("--plan", required=True, type=Path)
        cli.add_argument("--refs", required=True, type=Path)
        cli.add_argument("--repository", required=True)
        cli.add_argument("--output", required=True, type=Path)
        args = cli.parse_args()
        refs = args.refs.read_text(encoding="utf-8").splitlines()
        answer = check_duplicate(json.loads(args.plan.read_text(encoding="utf-8")),
                                 refs, args.repository)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(answer, sort_keys=True) + "\n",
                               encoding="utf-8")
        print("L2 draft decision: " + answer["decision"])
        return 0
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--v2-runs", type=Path, required=True)
    cli.add_argument("--l2-runs", type=Path, required=True)
    cli.add_argument("--repository", required=True)
    cli.add_argument("--as-of", required=True,
                     help="ISO 8601 offset-aware audit timestamp")
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    report = build_report({
        "quality-engine-v2.yml": json.loads(args.v2_runs.read_text()),
        "quality-engine-l2-draft.yml": json.loads(args.l2_runs.read_text()),
    }, parse_utc(args.as_of), args.repository)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for item in report["checks"]:
        print(f"{item['workflow']}: {item['status']}, run={item['lastScheduledRunId']}")
    print(f"R1 v2.3 reliability: {report['overall']} (audit only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

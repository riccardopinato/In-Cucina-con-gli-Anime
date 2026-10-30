#!/usr/bin/env python3
"""R1 Quality Engine v2.1: source-bound, read-only longitudinal finding state.

Input: v2 JSON report and optional previous, independently retrieved state.
Output: deterministic, inspectable delta + cumulative state; no repository edits.
The GitHub Actions wrapper retrieves previous *successful main* artifacts, not
this module. Never promotes a finding to a human-verified fact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCHEMA_VERSION = 1
MAX_RECORDS = 12000
MAX_BYTES = 12_000_000
TRANSITIONS = ("NEW", "PERSISTING", "RESOLVED", "REOPENED", "UNBASELINED")
SAFE_SEVERITIES = {"info", "review", "high"}
ALLOWED_MODES = {"code", "content", "workflows"}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("History input exceeds bounded size")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("History input must be an object")
    return data


def scope_digest(config: dict, report: dict) -> str:
    mode = report["mode"]
    if config.get("schemaVersion") != 1 or not isinstance(config.get("paths"), dict):
        raise ValueError("Invalid configuration")
    paths = config["paths"].get(mode)
    if not isinstance(paths, list) or not paths or not all(isinstance(x, str) for x in paths):
        raise ValueError("Invalid mode patterns")
    # Include the ruleset version: changing rules should never be silently
    # interpreted as fixing or introducing a source defect.
    return digest({
        "profile": report["profile"], "mode": mode,
        "engine": report["engine"], "version": report["version"],
        "paths": paths,
    })


def safe_finding(f: dict) -> dict:
    keys = ("id", "ruleId", "severity", "path", "line", "entityId", "message")
    if not isinstance(f, dict) or any(key not in f for key in keys):
        raise ValueError("Incomplete finding")
    if any(not isinstance(f[k], str) for k in ("id", "ruleId", "severity", "path", "message")):
        raise ValueError("Invalid finding fields")
    if not f["id"] or not f["ruleId"] or f["severity"] not in SAFE_SEVERITIES:
        raise ValueError("Invalid finding identity or severity")
    if not isinstance(f["line"], int) or isinstance(f["line"], bool) or f["line"] < 1:
        raise ValueError("Invalid finding line")
    if f["entityId"] is not None and not isinstance(f["entityId"], str):
        raise ValueError("Invalid finding entity")
    # Never serialize extra fields, e.g. accidental raw snippets or secrets.
    return {key: f[key] for key in keys}


def validate_report(report: dict) -> list[dict]:
    if (report.get("schemaVersion") != 1
            or report.get("engine") != "R1_QUALITY_ENGINE_V2"
            or report.get("mode") not in ALLOWED_MODES
            or report.get("readOnly") is not True
            or report.get("selfRepairEnabled") is not False
            or report.get("certification") != "NOT_CERTIFIED"
            or report.get("humanApprovals") != 0
            or not isinstance(report.get("sourceSha"), str)
            or not isinstance(report.get("profile"), str)
            or not isinstance(report.get("version"), str)
            or not isinstance(report.get("findings"), list)
            or not isinstance(report.get("filesSkipped"), list)
            or not isinstance(report.get("filesScanned"), int)
            or report["filesScanned"] < 0):
        raise ValueError("Untrusted or incompatible scan report")
    findings = [safe_finding(f) for f in report["findings"]]
    ids = [f["id"] for f in findings]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate finding IDs: cannot calculate trustworthy history")
    return findings


def signature(row: dict) -> tuple:
    """Conservative relocation key; only unique, unambiguous pairs may migrate."""
    return (row.get("ruleId"), row.get("path"), row.get("entityId"),
            row.get("message"), row.get("severity"))


def compare(report: dict, config: dict, previous: dict | None, *,
            repository: str, run_id: str, event: str) -> tuple[dict, dict]:
    current_findings = validate_report(report)
    if not repository or "/" not in repository or not run_id or not event:
        raise ValueError("Missing observation provenance")
    mode = report["mode"]
    scope = scope_digest(config, report)
    if report["filesSkipped"]:
        raise ValueError("Incomplete scan: skipped files prevent safe lifecycle comparison")
    current = {f["id"]: f for f in current_findings}
    baseline_status = "AVAILABLE" if previous is not None else "ABSENT"
    old_records = {}
    previous_sha = None
    if previous is not None:
        if (previous.get("schemaVersion") != SCHEMA_VERSION
                or previous.get("engine") != "R1_QUALITY_ENGINE_V21_HISTORY"
                or previous.get("repository") != repository
                or previous.get("mode") != mode
                or previous.get("profile") != report["profile"]
                or previous.get("scopeDigest") != scope
                or previous.get("readOnly") is not True
                or previous.get("certification") != "NOT_CERTIFIED"
                or previous.get("humanApprovals") != 0):
            raise ValueError("Baseline provenance/schema/scope mismatch; refuse false resolved claims")
        old_records = previous.get("records")
        if not isinstance(old_records, dict):
            raise ValueError("Invalid historical records")
        if len(old_records) > MAX_RECORDS:
            raise ValueError("History exceeds bounded record count")
        previous_sha = previous.get("sourceSha")
        if not isinstance(previous_sha, str) or not previous_sha:
            raise ValueError("Invalid baseline commit")
        scanner_ids = set()
        for fid, row in old_records.items():
            if (not isinstance(fid, str) or not isinstance(row, dict)
                    or row.get("id") != fid
                    or row.get("state") not in {"ACTIVE", "RESOLVED"}
                    or not isinstance(row.get("firstSeenSha"), str)
                    or not isinstance(row.get("lastSeenSha"), str)
                    or not isinstance(row.get("observations"), int)
                    or row["observations"] < 1
                    or not isinstance(row.get("scannerId", fid), str)
                    or not row.get("scannerId", fid)):
                raise ValueError("Malformed prior history row")
            # A current scanner fingerprint may only belong to one historical
            # record: otherwise no deterministic identity comparison is safe.
            scanner_id = row.get("scannerId", fid)
            if scanner_id in scanner_ids:
                raise ValueError("Duplicate historical scanner fingerprints")
            scanner_ids.add(scanner_id)

    # First reconcile exact observed fingerprints (including a previously
    # relocated scannerId). Then pair *only unique* shifts of line number
    # within the same rule/path/entity/message/severity.
    matches: dict[str, str] = {}  # current scannerId -> stable history ID
    used_old: set[str] = set()
    prior_by_scanner = {
        row.get("scannerId", fid): fid for fid, row in old_records.items()
    }
    for scanner_id in sorted(current):
        historical_id = prior_by_scanner.get(scanner_id)
        if historical_id is not None:
            matches[scanner_id] = historical_id
            used_old.add(historical_id)

    groups_old: dict[tuple, list[str]] = {}
    groups_new: dict[tuple, list[str]] = {}
    for fid, old in old_records.items():
        if fid not in used_old and old["state"] == "ACTIVE":
            groups_old.setdefault(signature(old), []).append(fid)
    for scanner_id, finding in current.items():
        if scanner_id not in matches:
            groups_new.setdefault(signature(finding), []).append(scanner_id)
    for sig in sorted(set(groups_new) & set(groups_old), key=repr):
        old_ids, new_ids = groups_old[sig], groups_new[sig]
        if len(old_ids) == 1 and len(new_ids) == 1:
            matches[new_ids[0]] = old_ids[0]
            used_old.add(old_ids[0])
        else:
            # Without excerpts or AST anchors, multiple equivalent findings
            # cannot be paired after line movement. Avoid false NEW/RESOLVED.
            raise ValueError("Ambiguous finding relocation: review source locations")

    result_rows = []
    updated = {}
    for scanner_id in sorted(current):
        finding = current[scanner_id]
        historical_id = matches.get(scanner_id, scanner_id)
        old = old_records.get(historical_id)
        if old is None:
            transition = "NEW" if previous is not None else "UNBASELINED"
            record = {
                **finding, "state": "ACTIVE", "scannerId": scanner_id,
                "firstSeenSha": report["sourceSha"],
                "lastSeenSha": report["sourceSha"], "resolvedAtSha": None,
                "observations": 1,
            }
        else:
            transition = "REOPENED" if old["state"] == "RESOLVED" else "PERSISTING"
            record = {
                **finding, "id": historical_id, "scannerId": scanner_id,
                "state": "ACTIVE",
                "firstSeenSha": old["firstSeenSha"],
                "lastSeenSha": report["sourceSha"], "resolvedAtSha": None,
                "observations": old["observations"] + 1,
            }
        updated[historical_id] = record
        result_rows.append({
            **{k: record.get(k) for k in
               ("id", "ruleId", "severity", "path", "line", "entityId", "message")},
            "scannerId": scanner_id, "transition": transition, "state": "ACTIVE",
        })

    for fid in sorted(old_records):
        old = old_records[fid]
        if fid not in updated:
            # Keep the last SHA where the problem was actually *detected*.
            record = dict(old)
            if old["state"] == "ACTIVE":
                record["state"] = "RESOLVED"
                record["resolvedAtSha"] = report["sourceSha"]
                result_rows.append({
                    **{k: record.get(k) for k in
                       ("id", "ruleId", "severity", "path", "line", "entityId", "message")},
                    "scannerId": record.get("scannerId", fid),
                    "transition": "RESOLVED", "state": "RESOLVED",
                })
            updated[fid] = record
    if len(updated) > MAX_RECORDS:
        raise ValueError("History exceeds max records: needs explicit retention policy")
    result_rows.sort(key=lambda r: (r["path"], r["line"], r["ruleId"], r["id"]))
    tallies = {key: sum(row["transition"] == key for row in result_rows)
               for key in TRANSITIONS}
    delta = {
        "schemaVersion": SCHEMA_VERSION, "engine": "R1_QUALITY_ENGINE_V21_DELTA",
        "mode": mode, "profile": report["profile"], "repository": repository,
        "sourceSha": report["sourceSha"], "previousSha": previous_sha,
        "runId": run_id, "event": event, "scopeDigest": scope,
        "baselineStatus": baseline_status, "completeScan": True,
        "counts": tallies, "readOnly": True, "selfRepairEnabled": False,
        "certification": "NOT_CERTIFIED", "humanApprovals": 0,
        "findings": result_rows,
    }
    state = {
        "schemaVersion": SCHEMA_VERSION, "engine": "R1_QUALITY_ENGINE_V21_HISTORY",
        "mode": mode, "profile": report["profile"], "repository": repository,
        "sourceSha": report["sourceSha"], "runId": run_id,
        "scopeDigest": scope, "readOnly": True,
        "certification": "NOT_CERTIFIED", "humanApprovals": 0,
        "records": updated,
    }
    return delta, state


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--report", required=True, type=Path)
    cli.add_argument("--config", required=True, type=Path)
    cli.add_argument("--previous", type=Path)
    cli.add_argument("--repository", required=True)
    cli.add_argument("--run-id", required=True)
    cli.add_argument("--event", required=True)
    cli.add_argument("--out-delta", required=True, type=Path)
    cli.add_argument("--out-state", required=True, type=Path)
    args = cli.parse_args()
    if args.previous is not None and not args.previous.is_file():
        raise ValueError("Baseline path supplied but missing: fail closed")
    report = load_json(args.report)
    config = load_json(args.config)
    previous = load_json(args.previous) if args.previous else None
    delta, state = compare(report, config, previous, repository=args.repository,
                           run_id=args.run_id, event=args.event)
    args.out_delta.parent.mkdir(parents=True, exist_ok=True)
    args.out_state.parent.mkdir(parents=True, exist_ok=True)
    args.out_delta.write_text(json.dumps(delta, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    args.out_state.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    print(f"R1 v2.1 {delta['mode']}: {delta['baselineStatus']} "
          f"{delta['counts']}; source={delta['sourceSha']} previous={delta['previousSha']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

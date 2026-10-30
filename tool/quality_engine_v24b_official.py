#!/usr/bin/env python3
"""Quality Engine v2.4-B: normalize the official Dart analyzer JSON evidence.

Input from pinned separate invocation of dart analyze --format=json lib.
This module does not execute analyzed code, fetch packages, mutate files,
expose analyzer messages/snippets, certify safety, or authorize a repair.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ENGINE = "QUALITY_ENGINE_V24B_DART_EVIDENCE"
SCHEMA = 1
MAX_INPUT_BYTES = 8_000_000
MAX_DIAGNOSTICS = 5000
EXPECTED_FLUTTER = "3.47.3"
SHA = re.compile(r"^[a-f0-9]{40}$")
RULE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,127}$")
SEVERITIES = {"ERROR": "high", "WARNING": "review", "INFO": "info"}


def read_bounded(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("Missing or oversized tool evidence")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Tool evidence must be a JSON object")
    return data


def path_in_checkout(raw: str, root: Path) -> str:
    if (not isinstance(raw, str) or not raw or len(raw) > 1600
            or any(ord(x) < 32 for x in raw) or "\\" in raw):
        raise ValueError("Untrusted analyzer source path")
    base = root.resolve(strict=True)
    source = Path(raw)
    candidate = source if source.is_absolute() else base / source
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(base):
        raise ValueError("Analyzer path escapes checkout")
    relative = resolved.relative_to(base)
    if (len(relative.parts) < 2 or relative.parts[0] != "lib"
            or relative.suffix != ".dart" or any(p.startswith(".") for p in relative.parts)):
        raise ValueError("Analyzer returned a path outside lib/ scope")
    if source.is_symlink() or (base / relative).is_symlink():
        raise ValueError("Analyzer source is a symlink")
    return relative.as_posix()


def validate_version(version: dict) -> dict:
    if not isinstance(version, dict):
        raise ValueError("Flutter version evidence must be JSON object")
    flutter = version.get("frameworkVersion")
    dart = version.get("dartSdkVersion")
    revision = version.get("frameworkRevision")
    if (flutter != EXPECTED_FLUTTER or not isinstance(dart, str)
            or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+.\w]*)?", dart)
            or not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{7,40}", revision)):
        raise ValueError("Unpinned or malformed Flutter/Dart tool version")
    return {"flutter": flutter, "dartSdk": dart, "flutterRevision": revision}


def normalize(raw: dict, version: dict, *, root: Path,
              source_sha: str, exit_code: int) -> dict:
    if not SHA.fullmatch(source_sha):
        raise ValueError("Invalid analyzer source SHA")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool) or not 0 <= exit_code <= 255:
        raise ValueError("Invalid analyzer exit code")
    tool = validate_version(version)
    if (not isinstance(raw, dict) or raw.get("version") != 1
            or not isinstance(raw.get("diagnostics"), list)
            or len(raw["diagnostics"]) > MAX_DIAGNOSTICS):
        raise ValueError("Unrecognized official Dart analyzer output")
    findings = []
    used_ids = set()
    for diag in raw["diagnostics"]:
        if not isinstance(diag, dict):
            raise ValueError("Malformed analyzer diagnostic")
        severity, rule = diag.get("severity"), diag.get("code")
        kind = diag.get("type")
        if (severity not in SEVERITIES or not isinstance(rule, str)
                or not RULE.fullmatch(rule)
                or not isinstance(kind, str) or len(kind) > 70):
            raise ValueError("Invalid severity or analyzer rule identity")
        location = diag.get("location")
        if not isinstance(location, dict) or not isinstance(location.get("range"), dict):
            raise ValueError("Missing analyzer location")
        loc_range = location["range"]
        start, end = loc_range.get("start"), loc_range.get("end")
        if not isinstance(start, dict) or not isinstance(end, dict):
            raise ValueError("Malformed analyzer range")
        line, col, start_offset, end_offset = (start.get("line"), start.get("column"),
                                               start.get("offset"), end.get("offset"))
        if (any(not isinstance(n, int) or isinstance(n, bool) for n in
                (line, col, start_offset, end_offset))
                or line < 1 or col < 1 or start_offset < 0 or end_offset < start_offset):
            raise ValueError("Invalid analyzer location offset")
        file = path_in_checkout(location.get("file"), root)
        identity = "\x1f".join((rule, file, str(start_offset), str(end_offset)))
        digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
        if digest in used_ids:
            raise ValueError("Ambiguous repeated analyzer diagnostic identity")
        used_ids.add(digest)
        findings.append({
            "id": digest, "ruleId": rule, "severity": SEVERITIES[severity],
            "analyzerSeverity": severity, "analyzerType": kind,
            "path": file, "line": line, "column": col,
            "offset": start_offset, "length": end_offset - start_offset,
            "state": "REVIEW_REQUIRED", "reviewerRole": "code_reviewer",
            "humanReviewEvidence": None,
        })
    findings.sort(key=lambda f: (f["path"], f["line"], f["column"], f["ruleId"], f["id"]))
    counts = Counter(f["analyzerSeverity"] for f in findings)
    if exit_code != 0 and not findings:
        state = "TOOL_FAILURE"
        gate = "INCOMPLETE"
    else:
        state = "ANALYZED_WITH_FINDINGS" if findings else "ANALYZED_CLEAN"
        gate = "BLOCKING_FINDINGS" if counts["ERROR"] or counts["WARNING"] else (
            "REVIEW_ONLY" if counts["INFO"] else "CLEAN")
    return {
        "schemaVersion": SCHEMA, "engine": ENGINE,
        "profile": "cooking-anime-v24b-official-dart", "sourceSha": source_sha,
        "tool": "dart analyze --format=json lib", "toolVersions": tool,
        "exitCode": exit_code, "status": state, "qualityGate": gate,
        "scope": ["lib/**/*.dart"],
        "readOnly": True, "selfRepairEnabled": False,
        "certification": "NOT_CERTIFIED", "humanApprovals": 0,
        "counts": {s: counts[s] for s in ("ERROR", "WARNING", "INFO")},
        "findings": findings,
    }


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--analyzer-json", type=Path, required=True)
    cli.add_argument("--flutter-version-json", type=Path, required=True)
    cli.add_argument("--root", type=Path, default=Path("."))
    cli.add_argument("--source-sha", required=True)
    cli.add_argument("--exit-code", type=int, required=True)
    cli.add_argument("--output", type=Path, required=True)
    a = cli.parse_args()
    result = normalize(read_bounded(a.analyzer_json),
                       read_bounded(a.flutter_version_json), root=a.root,
                       source_sha=a.source_sha, exit_code=a.exit_code)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"Dart official analyzer: {result['status']} {result['qualityGate']} "
          f"{result['counts']} at {result['sourceSha']}")
    return 1 if result["status"] == "TOOL_FAILURE" else 0


if __name__ == "__main__":
    raise SystemExit(main())

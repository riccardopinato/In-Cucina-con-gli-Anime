#!/usr/bin/env python3
"""Quality Engine v2.4-A: portable read-only Flutter/Android source checks.

Heuristic review leads only; NOT a Dart/Kotlin compiler, security certificate,
manifest merger or full static analysis substitute. No network/API/writes.
V2.1 history is intentionally not modified by these new unbaselined rules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

VERSION = "2.4.0-a"
SCHEMA = 1
MAX_BYTES = 2_000_000
ANDROID = "{http://schemas.android.com/apk/res/android}"
MODES = {"dart", "kotlin", "android_manifest", "gradle"}


def finding(rule: str, severity: str, path: str, line: int, explanation: str,
            anchor: str = "") -> dict:
    if severity not in ("info", "review", "high") or line < 1:
        raise ValueError("Invalid finding")
    key = "\x1f".join((rule, path, str(line), anchor))
    return {
        "id": hashlib.sha256(key.encode("utf-8")).hexdigest()[:20],
        "ruleId": rule, "severity": severity, "path": path, "line": line,
        "message": explanation, "state": "REVIEW_REQUIRED",
        "reviewerRole": "security_reviewer" if severity == "high" else "code_reviewer",
        "humanReviewEvidence": None,
    }


def lines_without_obvious_comments(src: str):
    # Conservative line-based heuristics: never call them semantic proof.
    for num, line in enumerate(src.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(("//", "/*", "*", "#")):
            continue
        yield num, line


def dart(path: str, src: str) -> list[dict]:
    findings = []
    for num, line in enumerate(src.splitlines(), 1):
        if re.search(r"^\s*//\s*ignore_for_file\s*:", line):
            findings.append(finding("DART_FILE_LINT_SUPPRESSION", "review", path, num,
                                    "Whole-file lint suppression requires scope justification"))
    for num, line in lines_without_obvious_comments(src):
        if re.search(r"\bbadCertificateCallback\b", line) and (
                "true" in line or "=>" in line):
            findings.append(finding("DART_TLS_CERT_BYPASS_CANDIDATE", "high", path, num,
                                    "TLS certificate callback requires independent security review"))
        if re.search(r"\b(?:print|debugPrint)\s*\(", line):
            findings.append(finding("DART_RELEASE_LOGGING", "info", path, num,
                                    "Check whether diagnostic output is disabled or redacted in release"))
        if re.search(r"\bsetString\s*\(\s*['\"](?:access_?token|refresh_?token|password|api_?key|secret)['\"]", line, re.I):
            findings.append(finding("DART_SENSITIVE_PREF_KEY_CANDIDATE", "review", path, num,
                                    "Sensitive-key literal in generic storage call needs privacy review"))
    return findings


def kotlin(path: str, src: str) -> list[dict]:
    findings = []
    for num, line in lines_without_obvious_comments(src):
        if re.search(r"\bLog\.(?:d|v|i|e|w)\s*\(", line):
            findings.append(finding("KOTLIN_RUNTIME_LOGGING", "info", path, num,
                                    "Verify Android logging does not disclose sensitive values"))
        if re.search(r"\b(?:allowAllHostnameVerifier|ALLOW_ALL_HOSTNAME_VERIFIER)\b", line):
            findings.append(finding("KOTLIN_TLS_HOSTNAME_BYPASS", "high", path, num,
                                    "All-hostname TLS verifier needs security review"))
    return findings


def gradle(path: str, src: str) -> list[dict]:
    findings = []
    for num, line in lines_without_obvious_comments(src):
        if re.search(r"\b(?:implementation|api|classpath)\s*(?:\(\s*)?['\"][^'\"\n]+:[^'\"\n]+:\+['\"]", line):
            findings.append(finding("GRADLE_DYNAMIC_DEPENDENCY", "review", path, num,
                                    "Dynamic dependency version may cause unreviewed resolution"))
        if re.search(r"\burl\s*(?:=|\s)\s*(?:uri\s*\(\s*)?['\"]http://", line):
            findings.append(finding("GRADLE_PLAINTEXT_REPOSITORY", "high", path, num,
                                    "Plaintext dependency repository requires supply-chain review"))
    return findings


def android_manifest(path: str, src: str) -> list[dict]:
    try:
        root = ET.fromstring(src)
    except ET.ParseError:
        return [finding("ANDROID_MANIFEST_PARSE", "high", path, 1,
                        "AndroidManifest.xml could not be parsed")]
    if root.tag != "manifest":
        return [finding("ANDROID_MANIFEST_ROOT", "high", path, 1,
                        "Manifest XML has unexpected root")]
    findings = []
    application = root.find("application")
    if application is not None:
        if application.get(ANDROID + "usesCleartextTraffic") == "true":
            findings.append(finding("ANDROID_CLEARTEXT_ENABLED", "review", path, 1,
                                    "Cleartext network traffic explicitly permitted"))
        if application.get(ANDROID + "debuggable") == "true":
            findings.append(finding("ANDROID_DEBUGGABLE_MANIFEST", "high", path, 1,
                                    "Manifest explicitly enables debugging; verify release override"))
        for tag in ("activity", "service", "receiver", "provider"):
            for index, element in enumerate(application.findall(tag), 1):
                if element.get(ANDROID + "exported") == "true" and element.get(ANDROID + "permission") is None:
                    findings.append(finding("ANDROID_EXPORTED_COMPONENT_REVIEW", "review", path, 1,
                                            "Exported component without local permission needs intent/exposure review",
                                            anchor=f"{tag}:{index}"))
    return findings


SCANNERS = {"dart": dart, "kotlin": kotlin,
            "android_manifest": android_manifest, "gradle": gradle}


def scan(root: Path, config: dict, sha: str) -> dict:
    if (config.get("schemaVersion") != 1 or config.get("profile") is None
            or not isinstance(config.get("paths"), dict) or set(config["paths"]) != MODES
            or not re.fullmatch("[0-9a-f]{40}", sha)):
        raise ValueError("Invalid scan configuration/commit")
    root_real = root.resolve(strict=True)
    issues = []
    coverage = {}
    skipped = []
    for mode in sorted(MODES):
        globs = config["paths"][mode]
        if not isinstance(globs, list) or not globs:
            raise ValueError("Missing analyzer scope")
        candidates = set()
        for pattern in globs:
            if (not isinstance(pattern, str) or not pattern
                    or Path(pattern).is_absolute() or ".." in Path(pattern).parts):
                raise ValueError("Unsafe analyzer scope")
            candidates.update(root.glob(pattern))
        analyzed = 0
        for path in sorted(candidates):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if (path.is_symlink() or not path.resolve().is_relative_to(root_real)
                    or any(part.startswith(".") for part in path.relative_to(root).parts)):
                skipped.append({"path": rel, "reason": "unsafe_path"})
                continue
            if path.stat().st_size > MAX_BYTES:
                skipped.append({"path": rel, "reason": "size_limit"})
                continue
            if mode == "dart" and path.suffix != ".dart":
                continue
            if mode == "kotlin" and path.suffix != ".kt":
                continue
            if mode == "android_manifest" and path.name != "AndroidManifest.xml":
                continue
            if mode == "gradle" and path.suffix not in (".gradle", ".kts"):
                continue
            source = path.read_text(encoding="utf-8", errors="strict")
            issues.extend(SCANNERS[mode](rel, source))
            analyzed += 1
        coverage[mode] = {"filesScanned": analyzed,
                          "coverageStatus": "SCANNED" if analyzed else "NO_MATCHING_FILES"}
    issues.sort(key=lambda x: (x["path"], x["line"], x["ruleId"], x["id"]))
    tally = Counter(x["severity"] for x in issues)
    return {
        "schemaVersion": SCHEMA, "engine": "QUALITY_ENGINE_V24A_STATIC",
        "version": VERSION, "profile": config["profile"], "sourceSha": sha,
        "readOnly": True, "selfRepairEnabled": False, "certification": "NOT_CERTIFIED",
        "humanApprovals": 0, "coverage": coverage, "filesSkipped": skipped,
        "counts": {k: tally[k] for k in ("info", "review", "high")},
        "findings": issues,
    }


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=Path("."))
    cli.add_argument("--config", type=Path, default=Path(".quality-engine-v24.json"))
    cli.add_argument("--source-sha", required=True)
    cli.add_argument("--output", type=Path, required=True)
    a = cli.parse_args()
    result = scan(a.root, json.loads(a.config.read_text(encoding="utf-8")),
                  a.source_sha)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"Quality Engine v2.4-A: coverage={result['coverage']} counts={result['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

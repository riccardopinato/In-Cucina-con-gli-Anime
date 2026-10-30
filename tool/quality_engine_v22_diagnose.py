#!/usr/bin/env python3
"""R1 Quality Engine v2.2: read-only, deterministic diagnostic proposals.

Consumes the complete v2 scan and corresponding v2.1 delta from exactly the
same run/commit. Outputs review plans, never patches, commands, approvals,
certifications or instructions that an automatic writer may execute.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path, PurePosixPath

from quality_engine_v21_history import load_json, scope_digest, validate_report

ENGINE_VERSION = "2.2.0-diagnoser"
ACTIVE = {"NEW", "PERSISTING", "REOPENED", "UNBASELINED"}
ALL_TRANSITIONS = ACTIVE | {"RESOLVED"}
MAX_PROPOSALS = 12000

# Domain, candidate priority, risk, cause hypothesis, suggested investigation,
# evidence gate, and qualified human decision needed. No auto-applied changes.
RULEBOOK: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "PY_PARSE_ERROR": ("code", "P1", "compatibility", "Python syntax cannot be parsed",
        "Locate the parser error and correct only the relevant statement.",
        "Python compile and repository unit tests at exact commit.", "code_reviewer"),
    "PY_DYNAMIC_EXECUTION": ("code", "P0", "security", "Dynamic execution can process unsafe input",
        "Evaluate replacing dynamic execution with an explicit allowlisted operation.",
        "Security review, adversarial-input tests and regression suite.", "security_reviewer"),
    "PY_BARE_EXCEPT": ("code", "P2", "reliability", "Unexpected exceptions may be hidden",
        "Identify expected exceptions and preserve explicit error handling.",
        "Exercise success/error cases and Python regression tests.", "code_reviewer"),
    "PY_SHELL_TRUE": ("code", "P0", "security", "Shell execution may introduce injection exposure",
        "Review argument provenance and prefer a structured command argument vector.",
        "Threat-model review, hostile-input tests and Python regression suite.", "security_reviewer"),
    "DART_PLAINTEXT_HTTP": ("code", "P1", "security", "The URL literal may use unencrypted HTTP",
        "Check transport requirements and a supported authenticated HTTPS endpoint.",
        "Flutter tests, networking integration and security review.", "code_reviewer"),
    "DART_DEBUG_OUTPUT": ("code", "P2", "privacy", "Diagnostic logging may expose runtime values",
        "Check logging redaction, build-mode gating and release visibility.",
        "Flutter analyze/test and release logging review.", "code_reviewer"),
    "GHA_ACTION_UNPINNED": ("workflows", "P1", "supply_chain", "Action reference may move over time",
        "Identify trusted upstream release and pin it to a verified immutable commit.",
        "Action provenance, least privileges and workflow CI.", "security_reviewer"),
    "GHA_PRIVILEGED_PR_EVENT": ("workflows", "P0", "security", "Privileged PR event may execute untrusted inputs",
        "Threat-model workflow triggers, checkout and permission boundaries.",
        "Workflow security review and protected-branch checks.", "security_reviewer"),
    "GHA_WRITE_ALL": ("workflows", "P0", "security", "Broad write-all permissions may exceed minimum need",
        "Replace broad privilege with documented job-level minimum permissions.",
        "Permission review, workflow tests and protected-branch checks.", "security_reviewer"),
    "CONTENT_JSON_PARSE": ("content", "P1", "data_integrity", "JSON source may be malformed",
        "Inspect the source JSON syntax without editing generated runtime artifacts.",
        "Authoring parser, full catalog validation and editorial review.", "editorial_reviewer"),
    "CONTENT_SCHEMA": ("content", "P1", "data_integrity", "Catalog root does not meet expected shape",
        "Verify the source schema and required recipe collection.",
        "Authoring/schema tests and versioned catalog gate.", "editorial_reviewer"),
    "CONTENT_COMPONENT_SCHEMA": ("content", "P1", "data_integrity", "Reusable component registry is malformed",
        "Validate the component registry against the authoring contract.",
        "Component and dependent-recipe regression checks.", "editorial_reviewer"),
    "CONTENT_RECIPE_SCHEMA": ("content", "P1", "data_integrity", "A recipe item has an unexpected type",
        "Inspect the offending source item and its schema identity.",
        "Authoring parser and stable-ID regression tests.", "editorial_reviewer"),
    "CONTENT_MISSING_ID": ("content", "P1", "data_integrity", "Stable recipe identity is missing",
        "Restore a valid durable recipe ID without remapping user-owned references.",
        "ID compatibility, favorites and catalog regression tests.", "editorial_reviewer"),
    "CONTENT_DUPLICATE_RECIPE": ("content", "P1", "data_integrity", "A recipe ID may be duplicated",
        "Investigate source identity and duplicate handling; never auto-delete a recipe.",
        "Duplicate-review evidence and user-data compatibility tests.", "editorial_reviewer"),
    "CONTENT_EMPTY_TITLE": ("content", "P2", "editorial", "Required recipe title is empty",
        "Prepare dish-specific title text for editorial approval.",
        "Editorial review and localization alignment checks.", "editorial_reviewer"),
    "CONTENT_EMPTY_DESCRIPTION": ("content", "P2", "editorial", "Required description is missing",
        "Draft original recipe-specific copy; do not insert generic boilerplate.",
        "Editorial quality and localization completeness checks.", "editorial_reviewer"),
    "CONTENT_TIME_INCONSISTENCY": ("content", "P1", "timing", "Declared durations may not add up",
        "Reconcile preparation/cooking/elapsed durations with real workflow steps.",
        "Culinary timing verification and catalog regression tests.", "culinary_reviewer"),
    "CONTENT_INGREDIENT_SCHEMA": ("content", "P1", "data_integrity", "An ingredient record is malformed",
        "Verify quantities, identity and reference fields against source schema.",
        "Ingredient/schema and recipe regression checks.", "editorial_reviewer"),
    "CONTENT_DUPLICATE_INGREDIENT": ("content", "P2", "data_integrity", "Ingredient identity may repeat",
        "Determine if intentional repetition or accidental duplicate; preserve quantities.",
        "Editorial review plus ingredient identity and quantity tests.", "editorial_reviewer"),
    "CONTENT_COMPONENT_REF_SCHEMA": ("content", "P1", "data_integrity", "A component reference is malformed",
        "Validate that the component reference is a nonempty registered identifier.",
        "Dependency validation and stable-ID regression tests.", "editorial_reviewer"),
    "CONTENT_MISSING_COMPONENT": ("content", "P1", "data_integrity", "Ingredient refers to absent component",
        "Investigate the missing registry entry and affected dependent recipes.",
        "Component dependency matrix and catalog compiler tests.", "editorial_reviewer"),
    "CONTENT_MISSING_STEPS": ("content", "P1", "editorial", "Recipe has no valid procedure steps",
        "Restore recipe-specific ordered instructions in the canonical source.",
        "Culinary process review and editorial quality gate.", "culinary_reviewer"),
    "CONTENT_EMPTY_STEP": ("content", "P1", "editorial", "Procedure step is empty or malformed",
        "Review ordered preparation instructions without inventing culinary facts.",
        "Source-specific culinary review and localization consistency.", "culinary_reviewer"),
    "CULINARY_RAW_YOLK_REVIEW": ("content", "P0", "food_safety", "Raw/soft egg service may need additional controls",
        "Have a qualified reviewer assess pasteurization, supply chain and cooked alternatives.",
        "Qualified food-safety review with locale-specific source evidence.", "qualified_food_safety_reviewer"),
    "CULINARY_PREMADE_DEPENDENCY": ("content", "P1", "timing", "Reusable component may exceed listed recipe duration",
        "Check the advance-preparation assumption and storage/time semantics.",
        "Dependency duration QA, culinary review and localization checks.", "culinary_reviewer"),
}

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
TRANSITION_ORDER = {"REOPENED": 0, "NEW": 1, "PERSISTING": 2, "UNBASELINED": 3}
SAFE_REF = re.compile(r"^[a-zA-Z0-9_./:@-]{1,200}$")


def short_ref(value: str | None) -> str | None:
    if value is None:
        return None
    if SAFE_REF.fullmatch(value):
        return value
    # Do not expose arbitrary source-content strings in report identifiers.
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def check_path(path: str) -> str:
    if (not isinstance(path, str) or not path or len(path) > 300
            or "\\" in path or any(ord(ch) < 32 for ch in path)
            or PurePosixPath(path).is_absolute()
            or ".." in PurePosixPath(path).parts):
        raise ValueError("Untrusted finding path")
    return path


def diagnose(scan: dict, delta: dict, config: dict) -> dict:
    original = validate_report(scan)
    if len(original) > MAX_PROPOSALS or scan.get("filesSkipped"):
        raise ValueError("Incomplete/oversized scanner input")
    if (not isinstance(config, dict)
            or config.get("policy", {}).get("autoFix") is not False
            or config.get("policy", {}).get("autoMerge") is not False
            or config.get("policy", {}).get("humanReviewRequired") is not True):
        raise ValueError("Unsafe write or approval policy")
    if (not isinstance(delta, dict) or delta.get("schemaVersion") != 1
            or delta.get("engine") != "R1_QUALITY_ENGINE_V21_DELTA"
            or delta.get("mode") != scan["mode"]
            or delta.get("profile") != scan["profile"]
            or delta.get("sourceSha") != scan["sourceSha"]
            or delta.get("scopeDigest") != scope_digest(config, scan)
            or delta.get("readOnly") is not True
            or delta.get("selfRepairEnabled") is not False
            or delta.get("certification") != "NOT_CERTIFIED"
            or delta.get("humanApprovals") != 0
            or delta.get("completeScan") is not True
            or delta.get("baselineStatus") not in ("ABSENT", "AVAILABLE")
            or not isinstance(delta.get("repository"), str)
            or "/" not in delta["repository"]
            or not isinstance(delta.get("runId"), str)
            or not delta["runId"]
            or not isinstance(delta.get("findings"), list)
            or not isinstance(delta.get("counts"), dict)):
        raise ValueError("Incompatible scanner/history provenance")
    current = {f["id"]: f for f in original}
    observed: set[str] = set()
    ids = set()
    actual_counts = Counter()
    actions = []
    resolved = 0
    for row in delta["findings"]:
        if (not isinstance(row, dict)
                or row.get("transition") not in ACTIVE | {"RESOLVED"}
                or not isinstance(row.get("id"), str)
                or row["id"] in ids
                or not isinstance(row.get("scannerId"), str)):
            raise ValueError("Untrusted or duplicated historical finding")
        ids.add(row["id"])
        actual_counts[row["transition"]] += 1
        if row["transition"] == "RESOLVED":
            if row["scannerId"] in current:
                raise ValueError("A resolved finding is still in the scanner report")
            resolved += 1
            continue
        source = current.get(row["scannerId"])
        if source is None or row["scannerId"] in observed:
            raise ValueError("Missing/duplicated current scanner evidence")
        for key in ("ruleId", "severity", "path", "line", "entityId", "message"):
            if row.get(key) != source[key]:
                raise ValueError("History record disagrees with scanner evidence")
        observed.add(row["scannerId"])
        path = check_path(source["path"])
        spec = RULEBOOK.get(source["ruleId"])
        if spec is None or spec[0] != scan["mode"]:
            # Unknown rules remain visible but do not receive invented advice.
            domain, priority, risk = scan["mode"], "P3", "unknown_rule"
            cause = "The scanner reported a rule without a reviewed diagnostic adapter"
            proposal = "Register and independently review a diagnostic adapter before suggesting changes."
            gate = "Manual rule-definition review and exact-head regression suite."
            reviewer = "code_reviewer"
            adapter_state = "UNSUPPORTED_RULE"
        else:
            domain, priority, risk, cause, proposal, gate, reviewer = spec
            adapter_state = "RULE_ADAPTER_AVAILABLE"
        actions.append({
            "findingId": row["id"],
            "scannerId": row["scannerId"],
            "ruleId": source["ruleId"],
            "source": {
                "path": path, "line": source["line"],
                "entityRef": short_ref(source["entityId"]),
            },
            "transition": row["transition"], "severity": source["severity"],
            "priorityCandidate": priority,
            "domain": domain, "riskClass": risk,
            "diagnosisStatus": "HYPOTHESIS_NOT_VALIDATED",
            "adapterStatus": adapter_state,
            "possibleCause": cause,
            "proposedInvestigation": proposal,
            "requiredValidation": gate,
            "requiredReviewerRole": reviewer,
            "reviewDecision": "PENDING_HUMAN_REVIEW",
            "approvalEvidence": None,
            "autoFixEligible": False,
            "patch": None,
        })
    if observed != set(current):
        raise ValueError("Historical delta omits current evidence")
    if any(delta["counts"].get(k) != actual_counts[k]
           for k in ("NEW", "PERSISTING", "RESOLVED", "REOPENED", "UNBASELINED")):
        raise ValueError("Historical summary counts do not match findings")
    if delta["baselineStatus"] == "ABSENT" and any(
            row["transition"] != "UNBASELINED" for row in delta["findings"]):
        raise ValueError("No baseline can claim NEW/RESOLVED/PERSISTING")
    actions.sort(key=lambda a: (PRIORITY_ORDER[a["priorityCandidate"]],
                               TRANSITION_ORDER[a["transition"]],
                               a["source"]["path"], a["source"]["line"],
                               a["ruleId"], a["findingId"]))
    summary = [
        {"ruleId": rule, "findings": count}
        for rule, count in sorted(Counter(a["ruleId"] for a in actions).items(),
                                  key=lambda pair: (-pair[1], pair[0]))
    ]
    return {
        "schemaVersion": 1, "engine": "R1_QUALITY_ENGINE_V22_DIAGNOSIS",
        "version": ENGINE_VERSION,
        "repository": delta["repository"], "mode": scan["mode"],
        "profile": scan["profile"], "sourceSha": scan["sourceSha"],
        "scopeDigest": delta["scopeDigest"], "runId": delta["runId"],
        "baselineStatus": delta["baselineStatus"],
        "readOnly": True, "selfRepairEnabled": False,
        "automaticPrEnabled": False, "automaticMergeEnabled": False,
        "certification": "NOT_CERTIFIED", "humanApprovals": 0,
        "diagnosticsAreHypotheses": True,
        "counts": {
            "active": len(actions), "resolvedSinceBaseline": resolved,
            "priorityP0Candidates": sum(a["priorityCandidate"] == "P0" for a in actions),
            "unsupportedRules": sum(a["adapterStatus"] == "UNSUPPORTED_RULE" for a in actions),
        },
        "ruleSummary": summary, "proposals": actions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = diagnose(load_json(args.scan), load_json(args.delta), load_json(args.config))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"Quality v2.2 {result['mode']} {result['sourceSha']}: "
          f"{result['counts']} (review-only; no code changes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

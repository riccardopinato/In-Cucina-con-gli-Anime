#!/usr/bin/env python3
"""Portable read-only repository quality monitor (R1 v2 pilot).

Python standard library only. Findings are hypotheses / review leads, not
professional certifications, security attestations, or authorization to edit.
No API keys, network requests, git writes or automatic source modifications.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path

ENGINE_VERSION = "2.0.0-pilot"
MODES = ("code", "content", "workflows")
MAX_INPUT_BYTES = 3_000_000
SEVERITIES = {"info": 0, "review": 1, "high": 2}


def fingerprint(*parts: str) -> str:
    raw = "\x1f".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def issue(rule: str, severity: str, path: str, message: str, *,
          line: int = 1, entity: str = "") -> dict:
    if severity not in SEVERITIES:
        raise ValueError("Unsupported severity")
    return {
        "id": fingerprint(rule, path, entity, str(line)),
        "ruleId": rule,
        "severity": severity,
        "path": path,
        "line": line,
        "entityId": entity or None,
        "message": message,
        "state": "REVIEW_REQUIRED",
        "humanReviewEvidence": None,
    }


def scan_python(path: str, code: str) -> list[dict]:
    findings = []
    try:
        tree = ast.parse(code, filename=path)
    except SyntaxError as exc:
        return [issue("PY_PARSE_ERROR", "high", path,
                      "Python source cannot be parsed", line=exc.lineno or 1)]
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(issue("PY_BARE_EXCEPT", "review", path,
                                  "Bare except can hide unexpected failures",
                                  line=node.lineno))
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in ("eval", "exec"):
            findings.append(issue("PY_DYNAMIC_EXECUTION", "high", path,
                                  "Dynamic evaluation/execution requires security review",
                                  line=node.lineno))
        if isinstance(func, ast.Attribute) and func.attr in ("run", "Popen", "call", "check_output", "check_call"):
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    findings.append(issue("PY_SHELL_TRUE", "high", path,
                                          "Subprocess shell=True requires injection review",
                                          line=node.lineno))
    return findings


def scan_dart(path: str, code: str) -> list[dict]:
    findings = []
    for line_no, line in enumerate(code.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
            continue
        if re.search(r"\bUri\.parse\(\s*['\"]http://", line):
            findings.append(issue("DART_PLAINTEXT_HTTP", "review", path,
                                  "Plaintext HTTP URL requires transport review", line=line_no))
        if re.search(r"^\s*(?:print|debugPrint)\s*\(", line):
            findings.append(issue("DART_DEBUG_OUTPUT", "info", path,
                                  "Check whether debug output should remain", line=line_no))
    return findings


def scan_workflow(path: str, source: str) -> list[dict]:
    findings = []
    for line_no, line in enumerate(source.splitlines(), 1):
        match = re.match(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)", line)
        if match:
            action = match.group(1).strip("'\"")
            if not action.startswith(("./", "docker://")):
                if not re.fullmatch(r"[^@\s]+@[0-9a-fA-F]{40}", action):
                    findings.append(issue("GHA_ACTION_UNPINNED", "high", path,
                                          "External action must use immutable 40-character commit SHA",
                                          line=line_no))
        if re.match(r"^\s*pull_request_target\s*:", line):
            findings.append(issue("GHA_PRIVILEGED_PR_EVENT", "high", path,
                                  "Privileged pull_request_target event needs explicit threat review",
                                  line=line_no))
        if re.match(r"^\s*permissions:\s*write-all\s*(?:#.*)?$", line):
            findings.append(issue("GHA_WRITE_ALL", "high", path,
                                  "Broad write-all workflow permissions need least-privilege review",
                                  line=line_no))
    return findings


def scan_recipe_catalog(path: str, source: str) -> list[dict]:
    findings = []
    try:
        doc = json.loads(source)
    except json.JSONDecodeError as exc:
        return [issue("CONTENT_JSON_PARSE", "high", path,
                      "Content file is not valid JSON", line=exc.lineno)]
    if not isinstance(doc, dict) or not isinstance(doc.get("recipes"), list):
        return [issue("CONTENT_SCHEMA", "high", path,
                      "Expected a JSON object with a recipes list")]
    recipes = doc["recipes"]
    components = doc.get("reusableComponents", {})
    if not isinstance(components, dict):
        findings.append(issue("CONTENT_COMPONENT_SCHEMA", "high", path,
                              "Reusable component registry is not an object"))
        components = {}
    seen = set()
    for index, recipe in enumerate(recipes):
        if not isinstance(recipe, dict):
            findings.append(issue("CONTENT_RECIPE_SCHEMA", "high", path,
                                  "Recipe entry is not an object", entity=f"index:{index}"))
            continue
        rid = str(recipe.get("id", ""))
        entity = rid or f"index:{index}"
        if not rid:
            findings.append(issue("CONTENT_MISSING_ID", "high", path,
                                  "Recipe identity is missing", entity=entity))
        elif rid in seen:
            findings.append(issue("CONTENT_DUPLICATE_RECIPE", "high", path,
                                  "Duplicate recipe ID in source",
                                  entity=f"{entity}/entry:{index + 1}"))
        seen.add(rid)
        if not isinstance(recipe.get("title"), str) or not recipe["title"].strip():
            findings.append(issue("CONTENT_EMPTY_TITLE", "high", path,
                                  "Recipe title is empty", entity=entity))
        if not isinstance(recipe.get("description"), str) or not recipe["description"].strip():
            findings.append(issue("CONTENT_EMPTY_DESCRIPTION", "review", path,
                                  "Recipe description is missing", entity=entity))
        times = recipe.get("times", {})
        if isinstance(times, dict):
            prep, cook, total = (times.get(k) for k in
                                 ("prepMinutes", "sourceCookMinutes", "totalElapsedMinutes"))
            if all(isinstance(x, (float, int)) and not isinstance(x, bool)
                   for x in (prep, cook, total)) and total < prep + cook:
                findings.append(issue("CONTENT_TIME_INCONSISTENCY", "high", path,
                                      "Total elapsed time is below prep plus cooking time", entity=entity))
        ingredients = recipe.get("ingredients", [])
        if not isinstance(ingredients, list):
            findings.append(issue("CONTENT_INGREDIENT_SCHEMA", "high", path,
                                  "Ingredients must be a list", entity=entity))
            ingredients = []
        ing_ids = set()
        deps = set()
        for ingredient_index, ingredient in enumerate(ingredients, 1):
            location = f"{entity}/ingredient:{ingredient_index}"
            if not isinstance(ingredient, dict):
                findings.append(issue("CONTENT_INGREDIENT_SCHEMA", "high", path,
                                      "Ingredient is not an object", entity=location))
                continue
            iid = str(ingredient.get("id", ""))
            if iid and iid in ing_ids:
                findings.append(issue("CONTENT_DUPLICATE_INGREDIENT", "high", path,
                                      "Repeated ingredient ID in one recipe", entity=location))
            ing_ids.add(iid)
            ref = ingredient.get("componentRef")
            if ref is not None and ref != "":
                if not isinstance(ref, str) or not ref.strip():
                    findings.append(issue("CONTENT_COMPONENT_REF_SCHEMA", "high", path,
                                          "Component reference must be a nonempty string",
                                          entity=location))
                else:
                    deps.add(ref)
                    if ref not in components:
                        findings.append(issue("CONTENT_MISSING_COMPONENT", "high", path,
                                              "Ingredient references missing reusable component",
                                              entity=location))
        steps = recipe.get("steps", [])
        if not isinstance(steps, list) or not steps:
            findings.append(issue("CONTENT_MISSING_STEPS", "high", path,
                                  "Recipe has no preparation steps", entity=entity))
            steps = []
        full_steps = []
        for step_index, step in enumerate(steps, 1):
            location = f"{entity}/step:{step_index}"
            if (not isinstance(step, dict)
                    or not isinstance(step.get("instruction"), str)
                    or not step["instruction"].strip()):
                findings.append(issue("CONTENT_EMPTY_STEP", "high", path,
                                      "A recipe instruction is empty or malformed", entity=location))
            else:
                full_steps.append(step["instruction"])
        operations = " ".join(full_steps).casefold()
        if re.search(r"tuorlo\s+d['’]uovo\s+fresco", operations) and not re.search(
                r"tuorlo\s+(?:da\s+uovo\s+)?pastorizzat", operations):
            findings.append(issue("CULINARY_RAW_YOLK_REVIEW", "review", path,
                                  "Fresh yolk served in steps: confirm safe/pasteurized alternative",
                                  entity=entity))
        for ref in sorted(deps):
            component = components.get(ref)
            if not isinstance(component, dict):
                continue
            component_time = component.get("totalElapsedMinutes")
            total = times.get("totalElapsedMinutes") if isinstance(times, dict) else None
            if all(isinstance(x, (int, float)) and not isinstance(x, bool)
                   for x in (component_time, total)) and component_time > total:
                findings.append(issue("CULINARY_PREMADE_DEPENDENCY", "review", path,
                                      "Reusable component takes longer than stated recipe time; verify pre-made assumption",
                                      entity=entity + "->" + ref))
    return findings


SCANNERS = {
    "code": {".py": scan_python, ".dart": scan_dart},
    "content": {".json": scan_recipe_catalog},
    "workflows": {".yml": scan_workflow, ".yaml": scan_workflow},
}


def scan(root: Path, config: dict, mode: str, source_sha: str = "unknown") -> dict:
    if mode not in MODES:
        raise ValueError("Unknown scan mode")
    if config.get("schemaVersion") != 1 or not isinstance(config.get("paths"), dict):
        raise ValueError("Invalid quality engine configuration")
    patterns = config["paths"].get(mode)
    if not isinstance(patterns, list) or not patterns or not all(
            isinstance(x, str) and x and not Path(x).is_absolute() and ".." not in Path(x).parts
            for x in patterns):
        raise ValueError(f"Missing or unsafe {mode} path patterns")
    findings = []
    scanned = []
    skipped = []
    targets = set()
    for pattern in patterns:
        targets.update(root.glob(pattern))
    root_real = root.resolve()
    for target in sorted(targets):
        if not target.is_file() or target.is_symlink() or target.suffix not in SCANNERS[mode]:
            continue
        resolved = target.resolve()
        if not resolved.is_relative_to(root_real):
            continue
        rel = target.relative_to(root).as_posix()
        if any(part.startswith(".") and part != ".github" for part in target.relative_to(root).parts):
            continue
        if target.stat().st_size > MAX_INPUT_BYTES:
            skipped.append({"path": rel, "reason": "file_exceeds_size_limit"})
            continue
        source = target.read_text(encoding="utf-8", errors="replace")
        scanned.append(rel)
        findings.extend(SCANNERS[mode][target.suffix](rel, source))
    findings.sort(key=lambda x: (x["path"], x["line"], x["ruleId"], x["entityId"] or ""))
    counts = Counter(x["severity"] for x in findings)
    return {
        "schemaVersion": 1,
        "engine": "R1_QUALITY_ENGINE_V2",
        "version": ENGINE_VERSION,
        "mode": mode,
        "sourceSha": source_sha,
        "profile": str(config.get("profile", "unspecified")),
        "readOnly": True,
        "selfRepairEnabled": False,
        "certification": "NOT_CERTIFIED",
        "humanApprovals": 0,
        "filesScanned": len(scanned),
        "filesSkipped": skipped,
        "counts": {"info": counts["info"], "review": counts["review"], "high": counts["high"]},
        "findings": findings,
    }


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=Path("."))
    cli.add_argument("--config", type=Path, default=Path(".quality-engine-v2.json"))
    cli.add_argument("--mode", choices=MODES, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--source-sha", default=os.environ.get("GITHUB_SHA", "unknown"))
    args = cli.parse_args()
    report = scan(args.root, json.loads(args.config.read_text(encoding="utf-8")),
                  args.mode, args.source_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"R1 v2 {args.mode}: {report['filesScanned']} files; {report['counts']}; "
          f"SHA {report['sourceSha']}; report={args.output}")
    # Always nonblocking in pilot: report and review, never fake certification.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

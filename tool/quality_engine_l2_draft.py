#!/usr/bin/env python3
"""Quality Engine L2 pilot: a strictly bounded, reversible Markdown formatter.

Only remove whitespace from *otherwise blank lines* in three fixed, non-product
Quality Engine documentation files. Never touch application code, culinary
content, workflow definitions, secrets, signing, assets or Factory Core.
A separate CI job may use the verified plan on an isolated Git branch and open
a DRAFT pull request. This script has no Git/network/API/merge operations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = "2.3.0-l2-pilot"
RULE_ID = "MD_BLANK_LINE_WHITESPACE"
FIXED_ALLOWLIST = frozenset({
    "docs/R1_QUALITY_ENGINE_V2_PILOT.md",
    "docs/R1_QUALITY_ENGINE_V21_HISTORY.md",
    "docs/R1_QUALITY_ENGINE_V22_DIAGNOSER.md",
})
MAX_FILE_SIZE = 256 * 1024
MAX_CHANGED_LINES = 40
MAX_CHANGED_FILES = 3
MAX_REMOVED_BYTES = 1024
HEX_SHA = re.compile(r"^[0-9a-f]{40}$")


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def as_json(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def validate_policy(cfg: dict) -> list[str]:
    if not isinstance(cfg, dict) or cfg.get("schemaVersion") != 1:
        raise ValueError("Invalid L2 policy version")
    if (cfg.get("enabled") is not True
            or cfg.get("riskTier") != "LOW_FORMAT_ONLY"
            or cfg.get("draftOnly") is not True
            or cfg.get("autoMerge") is not False
            or cfg.get("autoPublish") is not False
            or cfg.get("allowedRule") != RULE_ID):
        raise ValueError("L2 policy does not permit safe draft-only formatting")
    paths = cfg.get("eligiblePaths")
    if (not isinstance(paths, list) or not paths
            or len(paths) != len(set(paths))
            or not all(isinstance(p, str) and p in FIXED_ALLOWLIST for p in paths)):
        raise ValueError("L2 targets must be explicit fixed safe documentation files")
    return sorted(paths)


def transform(source: bytes) -> tuple[bytes, tuple[int, ...], int]:
    # Reject binary and invalid UTF-8, even though transformation is byte-only.
    source.decode("utf-8")
    if len(source) > MAX_FILE_SIZE:
        raise ValueError("Target file exceeds maximum size")
    output: list[bytes] = []
    changed: list[int] = []
    removed = 0
    fence_kind: bytes | None = None
    fence_width = 0
    for index, line in enumerate(source.splitlines(keepends=True), start=1):
        # A conservative Markdown fence tracker protects blank lines within
        # fenced code blocks, including examples where spaces are meaningful.
        fence = re.match(rb"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)
            if fence_kind is None:
                fence_kind, fence_width = marker[:1], len(marker)
            elif (marker[:1] == fence_kind and len(marker) >= fence_width
                    and not line[fence.end():].strip(b" \t\r\n")):
                # Closing fences must have *only* optional whitespace after
                # the marker. A line like ```example is not a closing fence.
                fence_kind, fence_width = None, 0
            output.append(line)
            continue
        if fence_kind is not None:
            output.append(line)
            continue
        # Only whitespace-only lines are editable. Content-bearing lines and
        # intentional Markdown hard breaks remain byte-identical.
        match = re.fullmatch(rb"[ \t]+(\r\n|\n|\r)?", line)
        if match:
            clean = match.group(1) or b""
            output.append(clean)
            changed.append(index)
            removed += len(line) - len(clean)
        else:
            output.append(line)
    if len(changed) > MAX_CHANGED_LINES or removed > MAX_REMOVED_BYTES:
        raise ValueError("L2 diff exceeds bounded budget")
    return b"".join(output), tuple(changed), removed


def safe_target(root: Path, name: str) -> Path:
    if name not in FIXED_ALLOWLIST:
        raise ValueError("L2 path is not in immutable code allowlist")
    root_real = root.resolve(strict=True)
    if root.is_symlink():
        raise ValueError("Checkout root may not be a symlink")
    relative = Path(name)
    cursor = root
    for segment in relative.parts[:-1]:
        cursor = cursor / segment
        if cursor.is_symlink():
            raise ValueError("Symlinked parent directory is forbidden")
        if not cursor.is_dir():
            raise ValueError("Missing expected checkout directory")
    path = root / relative
    if not path.is_file() or path.is_symlink():
        raise ValueError("Target must be existing regular file, never symlink")
    if not path.resolve(strict=True).is_relative_to(root_real):
        raise ValueError("L2 target escapes checkout")
    return path


def plan(root: Path, cfg: dict, *, source_sha: str, repository: str) -> dict:
    if not HEX_SHA.fullmatch(source_sha):
        raise ValueError("L2 needs an immutable 40-hex source SHA")
    if repository != "riccardopinato/In-Cucina-con-gli-Anime":
        raise ValueError("L2 writer pilot restricted to one explicitly authorized repository")
    paths = validate_policy(cfg)
    changes = []
    for name in paths:
        path = safe_target(root, name)
        before = path.read_bytes()
        after, lines, nbytes = transform(before)
        if lines:
            changes.append({
                "ruleId": RULE_ID,
                "path": name,
                "beforeSha256": hash_bytes(before),
                "afterSha256": hash_bytes(after),
                "changedLineNumbers": list(lines),
                "linesChanged": len(lines),
                "bytesRemoved": nbytes,
                "riskTier": "LOW_FORMAT_ONLY",
            })
    if len(changes) > MAX_CHANGED_FILES:
        raise ValueError("Too many L2 files")
    return {
        "schemaVersion": 1, "engine": "QUALITY_ENGINE_L2_DRAFT_REPAIR",
        "version": VERSION, "repository": repository, "sourceSha": source_sha,
        "policySha256": hash_bytes(as_json(cfg).encode("utf-8")),
        "ruleId": RULE_ID, "readOnlyPlan": True,
        "draftPrOnly": True, "autoMergeEnabled": False,
        "contentCertification": "NOT_CERTIFIED",
        "humanApprovals": 0, "changes": changes,
        "counts": {"files": len(changes),
                   "lines": sum(x["linesChanged"] for x in changes),
                   "bytesRemoved": sum(x["bytesRemoved"] for x in changes)},
    }


def apply(root: Path, cfg: dict, signed_plan: dict, *,
          source_sha: str, repository: str) -> list[str]:
    # This "plan" is not a digital signature. Recompute every bit from
    # checked-out trusted source so a tampered artifact cannot target new files.
    current = plan(root, cfg, source_sha=source_sha, repository=repository)
    if as_json(signed_plan) != as_json(current):
        raise ValueError("Plan drift or tampered plan: no modifications allowed")
    prepared = []
    for record in current["changes"]:
        path = safe_target(root, record["path"])
        before = path.read_bytes()
        after, lines, removed = transform(before)
        if (hash_bytes(before) != record["beforeSha256"]
                or hash_bytes(after) != record["afterSha256"]
                or list(lines) != record["changedLineNumbers"]
                or removed != record["bytesRemoved"]):
            raise ValueError("Source drift during preparation")
        prepared.append((path, after))
    for path, after in prepared:
        path.write_bytes(after)
    return [record["path"] for record in current["changes"]]


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("command", choices=("plan", "apply"))
    cli.add_argument("--root", type=Path, default=Path("."))
    cli.add_argument("--config", type=Path, default=Path(".quality-engine-l2.json"))
    cli.add_argument("--source-sha", required=True)
    cli.add_argument("--repository", required=True)
    cli.add_argument("--plan", type=Path, default=Path("build/quality-l2/plan.json"))
    args = cli.parse_args()
    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    if args.command == "plan":
        result = plan(args.root, cfg, source_sha=args.source_sha,
                      repository=args.repository)
        args.plan.parent.mkdir(parents=True, exist_ok=True)
        args.plan.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
        print(f"L2 plan on {result['sourceSha']}: {result['counts']} (no writes)")
    else:
        signed_plan = json.loads(args.plan.read_text(encoding="utf-8"))
        changed = apply(args.root, cfg, signed_plan, source_sha=args.source_sha,
                        repository=args.repository)
        print(f"L2 isolated checkout: {len(changed)} allowlisted documentation files formatted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

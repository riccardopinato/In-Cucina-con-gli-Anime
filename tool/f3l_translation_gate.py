#!/usr/bin/env python3
"""F3L strict structural gate; never treats MT output as editorial sign-off."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LOCALES = ("en", "es", "fr", "de", "pt")
FORBIDDEN = (
    "[translation", "[traduzione", "lorem ipsum", "todo:", "insert text",
    "cook the main component", "prepare all ingredients before applying heat",
    "cuoci l'elemento principale", "cocina el elemento principal",
)


def canonical_json(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj):
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def source_recipes(source):
    recipes = source["recipes"]
    expected = [f"recipe_{n:06d}" for n in range(51, 163)]
    if source.get("count") != 112 or [r["id"] for r in recipes] != expected:
        raise ValueError("F3K source baseline identity/count mismatch")
    return recipes


def inspect(source, pack, *, require_review=False):
    issues = []
    try:
        source_rows = source_recipes(source)
    except (KeyError, ValueError, TypeError) as exc:
        return [f"Invalid Italian source: {exc}"]
    locale = pack.get("locale")
    if locale not in LOCALES:
        issues.append(f"Unsupported locale: {locale!r}")
    if pack.get("sourceLocale") != "it":
        issues.append("Source locale must be it")
    if pack.get("sourceBaselineSha256") != digest(source):
        issues.append("Italian baseline fingerprint mismatch: translations stale")
    translated = pack.get("recipes")
    if not isinstance(translated, list):
        return issues + ["recipes is not a list"]
    if len(translated) != 112:
        issues.append(f"Coverage is {len(translated)}/112")
    if [r.get("id") for r in translated] != [r["id"] for r in source_rows]:
        issues.append("Sequence of stable recipe IDs differs from Italian baseline")
    source_by_id = {r["id"]: r for r in source_rows}
    seen = set()
    for r in translated:
        rid = r.get("id")
        if rid not in source_by_id:
            issues.append(f"Extra/unknown recipe {rid}")
            continue
        if rid in seen:
            issues.append(f"Duplicate recipe {rid}")
        seen.add(rid)
        it = source_by_id[rid]
        if r.get("sourceRecipeSha256") != digest(it):
            issues.append(f"{rid}: stale per-recipe fingerprint")
        if r.get("sourceContentVersion") != it["targetContentVersion"]:
            issues.append(f"{rid}: source content version mismatch")
        if r.get("servings") != it["servings"] or r.get("difficulty") != it["difficulty"]:
            issues.append(f"{rid}: canonical servings/difficulty drift")
        source_time={k:v for k,v in it["times"].items() if k!="note"}
        target_time={k:v for k,v in r.get("times",{}).items() if k!="note"}
        if source_time != target_time:
            issues.append(f"{rid}: canonical time data drift")
        if not r.get("times",{}).get("note") or r["times"]["note"] == it["times"].get("note"):
            issues.append(f"{rid}: elapsed-time note not translated")
        if len(r.get("equipment",[])) != len(it.get("equipment",[])):
            issues.append(f"{rid}: equipment count mismatch")
        for f in ("title", "description", "animeContext"):
            s = r.get(f)
            if not isinstance(s, str) or not s.strip():
                issues.append(f"{rid}: empty {f}")
            elif any(x in s.lower() for x in FORBIDDEN):
                issues.append(f"{rid}: placeholder/filler detected in {f}")
        ing = r.get("ingredients", [])
        if not isinstance(ing, list) or len(ing) != len(it["ingredients"]):
            issues.append(f"{rid}: ingredient count mismatch")
        else:
            for ii, (src, dst) in enumerate(zip(it["ingredients"], ing)):
                if src["id"] != dst.get("id"):
                    issues.append(f"{rid}: ingredient ID mismatch {ii}")
                for canonical in ("quantity", "unit", "amountMode", "componentRef"):
                    if src.get(canonical) != dst.get(canonical):
                        issues.append(f"{rid}: ingredient {ii} canonical {canonical} changed")
                if bool(src.get("note")) != bool(dst.get("note")):
                    issues.append(f"{rid}: ingredient {ii} note lost/added")
                if not isinstance(dst.get("name"), str) or not dst["name"].strip():
                    issues.append(f"{rid}: ingredient {ii} name empty")
                if not isinstance(dst.get("amountText"), str) or not dst["amountText"].strip():
                    issues.append(f"{rid}: ingredient {ii} amountText empty")
                if dst.get("name") == src["name"] and len(src["name"].split()) > 5:
                    issues.append(f"{rid}: ingredient {ii} long Italian source unchanged")
        steps = r.get("steps", [])
        if not isinstance(steps, list) or len(steps) != len(it["steps"]):
            issues.append(f"{rid}: recipe steps collapsed/expanded")
        else:
            for si, (src, dst) in enumerate(zip(it["steps"], steps)):
                if src["id"] != dst.get("id") or src.get("timerSeconds") != dst.get("timerSeconds"):
                    issues.append(f"{rid}: step identity/timer mismatch {si}")
                translated_text = dst.get("instruction", "")
                if not isinstance(translated_text, str) or not translated_text.strip():
                    issues.append(f"{rid}: empty step {si}")
                    continue
                if any(x in translated_text.lower() for x in FORBIDDEN):
                    issues.append(f"{rid}: filler in step {si}")
                if translated_text.strip() == src["instruction"].strip():
                    issues.append(f"{rid}: untranslated step {si}")
                source_len = len(src["instruction"].strip())
                length_ratio = len(translated_text.strip()) / max(1, source_len)
                if not .3 <= length_ratio <= 3.1:
                    issues.append(f"{rid}: suspicious truncation/expansion in step {si} ({length_ratio:.2f})")
        if r.get("reviewStatus") not in ("machine_draft", "human_reviewed"):
            issues.append(f"{rid}: invalid review status")
        if require_review and r.get("reviewStatus") != "human_reviewed":
            issues.append(f"{rid}: human editorial review missing")
        if require_review and not r.get("reviewEvidence"):
            issues.append(f"{rid}: human review evidence missing")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="authoring/f3k_it_hardening_51_162.json")
    ap.add_argument("--pack", required=True)
    ap.add_argument("--release-ready", action="store_true")
    ap.add_argument("--report")
    ns = ap.parse_args()
    source = json.loads(Path(ns.source).read_text(encoding="utf-8"))
    pack = json.loads(Path(ns.pack).read_text(encoding="utf-8"))
    issues = inspect(source, pack, require_review=ns.release_ready)
    report = {"locale": pack.get("locale"), "sourceCount":112, "translatedCount":len(pack.get("recipes",[])), "reviewedCount":sum(r.get("reviewStatus")=="human_reviewed" for r in pack.get("recipes",[])), "releaseReady":bool(ns.release_ready and not issues), "errorCount":len(issues), "issues":issues[:300]}
    if ns.report:
        Path(ns.report).parent.mkdir(parents=True,exist_ok=True)
        Path(ns.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="issues"},ensure_ascii=False))
    for issue in issues[:30]:
        print("ERROR:",issue,file=sys.stderr)
    if issues: sys.exit(1)

if __name__ == "__main__": main()
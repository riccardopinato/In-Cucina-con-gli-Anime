#!/usr/bin/env python3
"""F3K Italian editorial hardening quality gate for recipes 51-162.

This gate intentionally validates only the Italian staging package. Translation
locales are blocked until this gate passes for all 112 recipes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "authoring" / "f3k_it_hardening_51_162.json"
EXPECTED_IDS = {f"recipe_{i:06d}" for i in range(51, 163)}
BANNED = [
    r"Controlla consistenza e cottura",
    r"elemento principale",
    r"componenti restanti",
    r"guarnizioni previste",
    r"porta in tavolar",
    r"aggiungire",
    r"porta a temperatur",
    r"Prosegui così",
    r"Nella fase successiva",
    r"Per completare",
]
STOPWORDS = {
    "il", "lo", "la", "i", "gli", "le", "un", "una", "uno", "di", "a",
    "da", "in", "con", "su", "per", "tra", "fra", "e", "o", "ma", "che",
    "del", "della", "dello", "dei", "delle", "degli", "al", "allo", "alla",
    "ai", "alle", "agli", "nel", "nello", "nella", "nei", "nelle", "negli",
    "è", "sono", "viene", "vengono", "questa", "questo", "versione",
    "preparazione", "giapponese", "ricetta", "piatto", "ottenere", "risultato",
}

def words(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ'-]+\b", text, flags=re.UNICODE))

def tokens(text: str) -> set[str]:
    return {
        t for t in re.findall(r"[a-zà-ù0-9]+", text.lower())
        if len(t) > 2 and t not in STOPWORDS
    }

def main() -> int:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors: list[str] = []

    if data.get("count") != 112:
        errors.append(f"count must be 112, got {data.get('count')}")
    ids = {r["id"] for r in data.get("recipes", [])}
    if ids != EXPECTED_IDS:
        errors.append("recipe ID set must be exactly recipe_000051..recipe_000162")

    translation = data.get("translationPolicy", {})
    if translation.get("status") != "BLOCKED":
        errors.append("translationPolicy.status must remain BLOCKED during F3K")
    if sorted(translation.get("locales", [])) != sorted(["en", "es", "fr", "de", "pt"]):
        errors.append("translationPolicy.locales must be EN/ES/FR/DE/PT excluding IT")

    components = data.get("reusableComponents", {})
    descriptions: list[tuple[str, set[str]]] = []

    for recipe in data.get("recipes", []):
        rid = recipe["id"]
        if recipe.get("translationState") != "BLOCKED_UNTIL_IT_100_PERCENT":
            errors.append(f"{rid}: translations are not locked")
        if recipe.get("status") != "it_reviewed_translation_blocked":
            errors.append(f"{rid}: unexpected staging status")

        desc = recipe.get("description", "")
        if words(desc) < 35:
            errors.append(f"{rid}: description too short ({words(desc)} words)")
        descriptions.append((rid, tokens(desc)))

        steps = recipe.get("steps", [])
        step_text = " ".join(s.get("instruction", "") for s in steps)
        if len(steps) < 6:
            errors.append(f"{rid}: fewer than 6 meaningful steps")
        if words(step_text) < 100:
            errors.append(f"{rid}: procedure too short ({words(step_text)} words)")
        for pattern in BANNED:
            if re.search(pattern, step_text, flags=re.I):
                errors.append(f"{rid}: banned filler/grammar pattern: {pattern}")

        ingredients = recipe.get("ingredients", [])
        if len(ingredients) < 3 and not recipe.get("completenessException"):
            errors.append(f"{rid}: too few ingredients without explicit completeness exception")
        for ingredient in ingredients:
            if ingredient.get("amountMode") not in {"measured", "q.b."}:
                errors.append(f"{rid}: ingredient amount mode missing: {ingredient.get('name')}")
            component_ref = ingredient.get("componentRef")
            if component_ref and component_ref not in components:
                errors.append(f"{rid}: unresolved componentRef {component_ref}")

        times = recipe.get("times", {})
        if times.get("totalElapsedMinutes", 0) < times.get("prepMinutes", 0) + times.get("sourceCookMinutes", 0):
            errors.append(f"{rid}: total elapsed time is lower than source prep+cook")

        anime = recipe.get("animeReview", {})
        if anime.get("status") != "complete":
            errors.append(f"{rid}: anime review incomplete")
        refs = anime.get("references", [])
        if not refs:
            errors.append(f"{rid}: anime reference list empty")
        for ref in refs:
            if ref.get("reviewStatus") != "reviewed":
                errors.append(f"{rid}: anime association not reviewed: {ref.get('workTitle')}")
            if ref.get("relation") == "unverified":
                errors.append(f"{rid}: unverified anime relation remains: {ref.get('workTitle')}")
            if ref.get("relation") in {"verified_appearance", "recurring_association"} and not ref.get("evidenceSource"):
                errors.append(f"{rid}: factual anime relation lacks evidence source: {ref.get('workTitle')}")

    # Descriptions may share culinary vocabulary, but near-duplicate editorial copy is blocked.
    for i, (rid_a, tok_a) in enumerate(descriptions):
        for rid_b, tok_b in descriptions[i + 1:]:
            union = tok_a | tok_b
            score = len(tok_a & tok_b) / len(union) if union else 0.0
            if score >= 0.75:
                errors.append(f"{rid_a}/{rid_b}: description similarity too high ({score:.3f})")

    if errors:
        print(f"F3K IT QUALITY GATE: FAIL ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1

    print("F3K IT QUALITY GATE: PASS")
    print("- 112/112 recipes present")
    print("- Italian descriptions/procedures meet completeness thresholds")
    print("- ingredient/component references resolve")
    print("- elapsed-time contract is coherent")
    print("- anime associations have no unreviewed state")
    print("- EN/ES/FR/DE/PT remain blocked until this Italian baseline is frozen")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
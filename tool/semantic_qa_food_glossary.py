#!/usr/bin/env python3
"""Italian-source culinary term triage: cipollotto != chives or mature onion.

Read only, stdlib, exact canonical ingredient-ID alignment. Neither this script
nor a zero-finding result can certify whole-recipe translation or food safety.
No external model, API key, private user content or network access.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "it"
TARGETS = ("en", "es", "fr", "de", "pt")
LEAK = {
    "en": re.compile(r"^(?:onion|onions)$|\bchives\b", re.I),
    "es": re.compile(r"cipollott|cebollino", re.I),
    "fr": re.compile(r"ciboulett", re.I),
    "de": re.compile(r"\b(?:Zwiebeln?|Schnittlauch|Unterlegscheiben)\b", re.I),
    "pt": re.compile(r"\bcebolinho\b|\bcebola\b(?!\s+de rama)|cipollott", re.I),
}

def is_mistranslation(locale: str, name: str) -> bool:
    """Narrow witnessed false-friend/undertranslation evidence, not an LLM."""
    if locale not in LEAK:
        raise ValueError(f"Unsupported translation locale: {locale}")
    if locale == "de" and "Frühlingszwiebel" in name:
        return False
    return bool(LEAK[locale].search(name))

def load_packs(root: Path = ROOT) -> dict:
    packs = {}
    for locale in (SOURCE, *TARGETS):
        path = root / "assets/catalog/locales" / f"{locale}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("locale") != locale or not isinstance(data.get("recipes"), dict):
            raise ValueError(f"Invalid locale pack: {locale}")
        packs[locale] = data["recipes"]
    return packs

def scan(root: Path = ROOT) -> dict:
    packs = load_packs(root)
    recipe_ids = sorted(packs[SOURCE])
    if len(recipe_ids) != 162:
        raise ValueError(f"Expected 162 published recipes, got {len(recipe_ids)}")
    for locale in TARGETS:
        if set(packs[locale]) != set(recipe_ids):
            raise ValueError(f"Missing/mismatched recipe IDs in {locale}")
    findings = []
    source_ingredients = 0
    for rid in recipe_ids:
        for ingredient_id, data in packs[SOURCE][rid]["ingredientTexts"].items():
            original = data.get("name", "")
            # The ID of a compound ingredient may include cipollotto even when
            # this *specific* row names sesame, egg or another component.
            if "cipollott" not in original.casefold():
                continue
            source_ingredients += 1
            for locale in TARGETS:
                item = packs[locale][rid]["ingredientTexts"].get(ingredient_id)
                if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                    raise ValueError(f"Missing aligned ingredient: {rid}/{locale}/{ingredient_id}")
                if is_mistranslation(locale, item["name"]):
                    findings.append({
                        "id": rid, "locale": locale, "ingredientId": ingredient_id,
                        "code": "CIPOLLOTTO_MISTRANSLATED",
                        "severity": "HOLD_EDITORIAL",
                        "sourceName": original, "targetName": item["name"],
                    })
    findings.sort(key=lambda x: (x["id"], x["locale"], x["ingredientId"]))
    return {
        "schemaVersion": 1, "reviewType": "DETERMINISTIC_SOURCE_BOUND_GLOSSARY",
        "mode": "OFFLINE", "semanticModelActuallyUsed": False,
        "paidAiApiCalls": 0, "certification": "NOT_CERTIFIED",
        "recipeCount": len(recipe_ids), "sourceIngredientCount": source_ingredients,
        "comparisonCount": source_ingredients * len(TARGETS),
        "findingsCount": len(findings),
        "affectedRecordCount": len({f["id"] for f in findings}),
        "findings": findings,
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build/semantic_qa/food_glossary.json")
    args = parser.parse_args()
    report = scan(ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "findings"},
                     ensure_ascii=False))
    if report["findingsCount"]:
        raise SystemExit("Culinary glossary triage: unresolved published ingredient names")
if __name__ == "__main__":
    main()

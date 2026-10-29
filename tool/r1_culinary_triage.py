#!/usr/bin/env python3
"""R1 source-bound culinary review queue; deterministic triage, NOT food-safety approval.

Reads the quarantined F3K Italian source only. Never alters source/locale/runtime
records and never creates human sign-offs. Review leads are literal-source
observations, not an exhaustive or professional safety determination.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from f3l_translation_gate import digest

SOURCE = Path("authoring/f3k_it_hardening_51_162.json")
SOURCE_SHA = "deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67"
RECIPE_IDS = [f"recipe_{n:06d}" for n in range(51, 163)]
EXPECTED_COMPONENTS = {
    "component_chashu", "component_ajitama", "component_dashi",
    "component_tonkatsu", "component_chocolate_custard",
    "component_brioche_cornet", "component_karaage_ref",
    "component_japanese_curry_ref", "component_kakuni_ref",
    "component_yakisoba_ref",
}

# (finding ID, priority, entity ID, verbatim source needle, review question)
# P0/P1 indicates review priority only: no validated hazard classification.
LEADS = (
    ("R1-001", "P0_CANDIDATE", "recipe_000056", "salmone fresco per sashimi",
     "Confirm documented raw-fish suitability, parasite controls, refrigeration and higher-risk consumers."),
    ("R1-002", "P0_CANDIDATE", "component_ajitama", "6 minuti e 30 secondi",
     "Review soft-cooked egg sourcing, pasteurized/fully cooked alternatives and cold storage."),
    ("R1-003", "P0_CANDIDATE", "recipe_000110", "trippa o frattaglie",
     "Verify the specific offal kind, safe pre-treatment and fully cooked endpoint; do not assume a universal cook time."),
    ("R1-004", "P0_CANDIDATE", "recipe_000150", "Gira il petto d'anatra",
     "Validate a measured fully cooked poultry endpoint rather than relying on fixed minutes alone."),
    ("R1-005", "P1_CANDIDATE", "recipe_000051", "maiale Chashu",
     "Explain pre-prepared chashu/ajitama timing; component durations are not included in a fresh 45-minute meal."),
    ("R1-006", "P1_CANDIDATE", "recipe_000059", "Cuoci per 3-4 minuti",
     "Review shellfish sourcing, refrigerated handling, cooking process and discard rules."),
    ("R1-007", "P1_CANDIDATE", "recipe_000080", "lasciandoli interi",
     "Review handling and cooking of whole fish with viscera, including objective doneness criteria."),
    ("R1-008", "P1_CANDIDATE", "recipe_000124", "espressamente idoneo al consumo crudo",
     "Verify already-present raw-uni safety precautions with qualified sourcing and market-specific criteria."),
    ("R1-009", "P1_CANDIDATE", "recipe_000146", "La marinatura non rende sicuro",
     "Verify already-present raw-tuna controls, supplier evidence, cold chain and histamine risk."),
    ("R1-010", "P1_CANDIDATE", "recipe_000134", "tuorlo da uovo pastorizzato",
     "Verify actual pasteurized yolk and already-cooked shirasu status, without weakening source safeguards."),
    ("R1-011", "P1_CANDIDATE", "recipe_000162", "albume d'uovo pastorizzato",
     "Check handling and cold chain of pasteurized egg whites in uncooked frozen dessert."),
    ("R1-012", "P1_CANDIDATE", "component_chashu", "Raffredda almeno 1 ora",
     "Verify pork cooking endpoint, cooling/refrigeration and dependent recipe preparation."),
    ("R1-013", "P0_CANDIDATE", "recipe_000153", "tuorlo d'uovo fresco",
     "Raw yolk offered as a dipping sauce; verify pasteurized alternative and vulnerable-consumer controls."),
    ("R1-014", "P0_CANDIDATE", "recipe_000133", "15-20 minuti",
     "Rolled chicken thigh uses time-only instructions; validate a poultry core temperature check."),
    ("R1-015", "P0_CANDIDATE", "recipe_000054", "carne macinata mista",
     "Mixed ground beef/pork cooking has no measured core temperature; validate safe ground-meat doneness."),
    ("R1-016", "P0_CANDIDATE", "recipe_000064", "carne macinata mista",
     "Ground-meat cutlet uses browning/timing; verify a measured safe internal cooking endpoint."),
    ("R1-017", "P1_CANDIDATE", "recipe_000149", "riso cotto del giorno prima",
     "Confirm rapid cooling, uninterrupted refrigeration, safe reheating and Bacillus cereus risk."),
    ("R1-018", "P1_CANDIDATE", "recipe_000117", "sovracosce di pollo disossate",
     "Review measured poultry endpoint and handling of cold tartar-style mayonnaise topping."),
    ("R1-019", "P1_CANDIDATE", "recipe_000096", "vongole asari (o veraci)",
     "Check shellfish sourcing, opening/cooking verification, broth filtration and cold-chain management."),
    ("R1-020", "P1_CANDIDATE", "recipe_000156", "vongole veraci spurgate",
     "Check shellfish sourcing and doneness; source does not explicitly require discarding unopened clams."),
)


def evidence(entity: dict, needle: str) -> dict:
    """Return a verbatim source field: no generated text is called evidence."""
    fields = [("title", entity.get("title", "")),
              ("description", entity.get("description", ""))]
    fields.extend(
        (f"ingredient_{n}", ingredient.get("name", ""))
        for n, ingredient in enumerate(entity.get("ingredients", []), 1)
    )
    for n, step in enumerate(entity.get("steps", []), 1):
        fields.append((f"step_{n}", step if isinstance(step, str) else step.get("instruction", "")))
    for field, value in fields:
        if isinstance(value, str) and needle.casefold() in value.casefold():
            return {"field": field, "verbatim": value}
    raise ValueError(f"Missing witnessed source phrase {needle!r}")


def build(source: dict) -> dict:
    """Fail closed if source changes or review queue does not cover 112+10."""
    if digest(source) != SOURCE_SHA:
        raise ValueError("Italian source fingerprint drift: re-triage against reviewed source")
    recipes = source.get("recipes", [])
    components = source.get("reusableComponents", {})
    if source.get("count") != 112 or [r.get("id") for r in recipes] != RECIPE_IDS:
        raise ValueError("R1 recipe coverage/order must be 51..162, 112 unique")
    if not isinstance(components, dict) or set(components) != EXPECTED_COMPONENTS:
        raise ValueError("R1 component coverage must be exactly 10 known identities")
    if source.get("translationPolicy", {}).get("status") != "BLOCKED":
        raise ValueError("R1 must not release locked translation candidates")

    records = {r["id"]: r for r in recipes}
    for recipe in recipes:
        if recipe.get("translationState") != "BLOCKED_UNTIL_IT_100_PERCENT":
            raise ValueError(f"{recipe['id']}: translation embargo changed")
        if recipe.get("status") != "it_reviewed_translation_blocked":
            raise ValueError(f"{recipe['id']}: unexpected Italian staging state")
        for ingredient in recipe.get("ingredients", []):
            ref = ingredient.get("componentRef")
            if ref and ref not in components:
                raise ValueError(f"{recipe['id']}: missing referenced component {ref}")
    candidate_rows = []
    for key, priority, entity_id, needle, question in LEADS:
        entity = records.get(entity_id) if entity_id.startswith("recipe_") else components.get(entity_id)
        if entity is None:
            raise ValueError(f"Missing R1 evidence entity {entity_id}")
        candidate_rows.append({
            "findingId": key, "priority": priority, "entityId": entity_id,
            "sourceEvidence": evidence(entity, needle),
            "reviewQuestion": question,
            "status": "PENDING_QUALIFIED_REVIEW",
            "humanDecisionEvidence": None,
        })
    by_entity = {}
    for finding in candidate_rows:
        by_entity.setdefault(finding["entityId"], []).append(finding["findingId"])
    recipe_queue = []
    for recipe in recipes:
        refs = sorted({
            ingredient["componentRef"]
            for ingredient in recipe["ingredients"] if ingredient.get("componentRef")
        })
        recipe_queue.append({
            "id": recipe["id"],
            "titleIT": recipe["title"],
            "sourceEntitySha256": digest(recipe),
            "contentVersion": recipe["targetContentVersion"],
            "componentDependencies": refs,
            "priorityFindings": by_entity.get(recipe["id"], []),
            "status": "PENDING_QUALIFIED_CULINARY_REVIEW",
            "humanDecisionEvidence": None,
        })
    component_queue = [
        {"id": key, "titleIT": value["title"], "sourceEntitySha256": digest(value),
         "priorityFindings": by_entity.get(key, []),
         "status": "PENDING_QUALIFIED_CULINARY_REVIEW",
         "humanDecisionEvidence": None}
        for key, value in sorted(components.items())
    ]
    return {
        "schemaVersion": 1,
        "phase": "R1_SOURCE_TRIAGE_NOT_CERTIFICATION",
        "sourceCatalogSha256": digest(source),
        "stagingOnly": True,
        "noAutomaticPublication": True,
        "humanSignoffs": 0,
        "releaseApproved": False,
        "sourceModified": False,
        "coverage": {
            "recipes": len(recipe_queue), "components": len(component_queue),
            "priorityReviewLeads": len(candidate_rows),
            "unreviewedEntities": len(recipe_queue) + len(component_queue),
        },
        "priorityCandidates": candidate_rows,
        "recipes": recipe_queue,
        "components": component_queue,
        "reviewNotice": "All entries pending qualified human review; automated evidence is not safety certification.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=Path("build/r1/culinary_triage.json"))
    args = parser.parse_args()
    report = build(json.loads(args.source.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"R1 pending: {report['coverage']} — no human approvals; {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

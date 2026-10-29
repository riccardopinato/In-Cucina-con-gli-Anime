#!/usr/bin/env python3
"""Generate source-locked F3L B2 bilingual review dossiers. Never certify content.

This is a review aid, not a translation engine or a publication pipeline.
Outputs contain candidate prose only; they are never runtime catalog assets.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from f3l_translation_gate import digest, inspect, source_recipes

LOCALES = ("en", "es", "fr", "de", "pt")
SOURCE_PATH = Path("authoring/f3k_it_hardening_51_162.json")
DRAFT_DIR = Path("authoring/f3l_review_drafts")

# These are observable conflicts in existing source descriptions, not approvals
# to rewrite them automatically. Check the complete method before editing.
# The following observed conflicts were corrected in versioned source migration B2-1.
# Keep the historical observations in docs, not as open blockers on revised text.
RESOLVED_ITALIAN_COPY_CONFLICTS = ("recipe_000059", "recipe_000073", "recipe_000074",
                                   "recipe_000081", "recipe_000088", "recipe_000124")
KNOWN_ITALIAN_COPY_ISSUES = {}

GENERIC_COPY_MARKERS = (
    ("generic_sequence", r"secondo una sequenza precisa"),
    ("generic_techniques", r"(?:le tecniche previste|le tecniche principali|la sequenza include le lavorazioni previste)"),
    ("generic_dessert", r"(?:struttura del dolce|impasto o crema, temperatura e tempi di riposo)"),
    ("generic_assembly", r"gli elementi che richiedono cottura o raffreddamento vengono preparati prima"),
    ("generic_method", r"il procedimento (?:distingue chiaramente|separa le fasi)"),
)


def italian_triage(source: dict) -> dict:
    """Create a complete *unapproved* 112-item Italian source-review queue."""
    recipes = []
    for row in source_recipes(source):
        description = row["description"]
        flags = [
            {"code": code, "basis": "heuristic", "excerpt": match.group(0)}
            for code, regex in GENERIC_COPY_MARKERS
            if (match := re.search(regex, description, re.IGNORECASE))
        ]
        if row["id"] in KNOWN_ITALIAN_COPY_ISSUES:
            flags.insert(0, {
                "code": "observed_source_copy_conflict",
                "basis": "manual_triage_required",
                "observation": KNOWN_ITALIAN_COPY_ISSUES[row["id"]],
            })
        recipes.append({
            "recipeId": row["id"],
            "sourceContentVersion": row["targetContentVersion"],
            "sourceRecipeSha256": digest(row),
            "titleIT": row["title"],
            "descriptionIT": description,
            "sourceReviewStatus": "PENDING_EDITORIAL_REVIEW",
            "priority": "HIGH" if row["id"] in KNOWN_ITALIAN_COPY_ISSUES else ("NORMAL" if flags else "ROUTINE"),
            "triageFlags": flags,
        })
    return {
        "schemaVersion": 1,
        "sourceLocale": "it",
        "sourceBaselineSha256": digest(source),
        "scope": "F3K recipes 51-162 only; NOT the 50 previously published recipes",
        "editorialReviewComplete": False,
        "reviewedByQualifiedHuman": 0,
        "pendingRecipeCount": len(recipes),
        "flaggedRecipeCount": sum(bool(r["triageFlags"]) for r in recipes),
        "observedConflictCount": len(KNOWN_ITALIAN_COPY_ISSUES),
        "disclaimer": "Heuristics identify candidates for contextual review. They do not prove or exhaust errors.",
        "recipes": recipes,
    }


def paired_ingredient(source: dict, translated: dict) -> dict:
    return {
        "stableIngredientId": source["id"],
        "sourceNameIT": source["name"],
        "candidateName": translated["name"],
        "sourceNoteIT": source.get("note"),
        "candidateNote": translated.get("note"),
        "sourceAmountTextIT": source.get("amountText"),
        "candidateAmountText": translated.get("amountText"),
        "quantity": source.get("quantity"),
        "unit": source.get("unit"),
        "amountMode": source.get("amountMode"),
        "componentRef": translated.get("componentRef"),
    }


def paired_recipe(source: dict, translated: dict, triage: dict) -> dict:
    return {
        "recipeId": source["id"],
        "sourceRecipeSha256": digest(source),
        "sourceContentVersion": source["targetContentVersion"],
        "reviewStatus": "PENDING_QUALIFIED_BILINGUAL_REVIEW",
        "humanReviewEvidence": None,
        "italianSourceTriageFlags": triage["triageFlags"],
        "servings": {"it": source["servings"], "candidate": translated["servings"]},
        "numericTimes": {
            "it": {k: v for k, v in source["times"].items() if k != "note"},
            "candidate": {k: v for k, v in translated["times"].items() if k != "note"},
        },
        "fields": {
            "title": {"it": source["title"], "candidate": translated["title"]},
            "description": {"it": source["description"], "candidate": translated["description"]},
            "animeContext": {
                "canonicalAnimeReview": source.get("animeReview"),
                "candidate": translated.get("animeContext"),
            },
            "elapsedTimeNote": {
                "it": source["times"].get("note"),
                "candidate": translated["times"].get("note"),
            },
        },
        "equipment": [
            {"index": n + 1, "it": it, "candidate": candidate}
            for n, (it, candidate) in enumerate(zip(source.get("equipment", []), translated.get("equipment", [])))
        ],
        "ingredients": [
            paired_ingredient(it, candidate)
            for it, candidate in zip(source["ingredients"], translated["ingredients"])
        ],
        "steps": [
            {
                "stableStepId": it["id"],
                "it": it["instruction"],
                "candidate": candidate["instruction"],
                "timerSeconds": it.get("timerSeconds"),
            }
            for it, candidate in zip(source["steps"], translated["steps"])
        ],
    }


def paired_component(component_id: str, source: dict, translated: dict) -> dict:
    return {
        "componentId": component_id,
        "reviewStatus": "PENDING_QUALIFIED_BILINGUAL_REVIEW",
        "humanReviewEvidence": None,
        "sourceTitleIT": source["title"],
        "candidateTitle": translated["title"],
        "servings": source.get("servings"),
        "totalElapsedMinutes": source.get("totalElapsedMinutes"),
        "recipeRef": source.get("recipeRef"),
        "ingredients": [
            {
                "index": n + 1,
                "it": it["name"],
                "candidate": candidate["name"],
                "quantity": it.get("quantity"),
                "unit": it.get("unit"),
            }
            for n, (it, candidate) in enumerate(zip(source.get("ingredients", []), translated.get("ingredients", [])))
        ],
        "steps": [
            {"index": n + 1, "it": it, "candidate": candidate}
            for n, (it, candidate) in enumerate(zip(source.get("steps", []), translated.get("steps", [])))
        ],
    }


def build_dossier(source: dict, pack: dict, *, recipe_id: str | None = None) -> dict:
    locale = pack.get("locale")
    if locale not in LOCALES:
        raise ValueError(f"unsupported locale: {locale}")
    if pack.get("sourceBaselineSha256") != digest(source):
        raise ValueError(f"{locale}: stale Italian fingerprint; review cannot proceed")
    if pack.get("reviewStatus") != "machine_draft_not_publishable":
        raise ValueError(f"{locale}: candidate is no longer a quarantined machine draft")
    if pack.get("editorialStaging", {}).get("noAutomaticPublication") is not True:
        raise ValueError(f"{locale}: non-publication lock missing")
    if any(r.get("reviewStatus") != "machine_draft" or r.get("reviewEvidence")
           for r in pack["recipes"]):
        raise ValueError(f"{locale}: unexpected human sign-off claim in staging pack")
    issues = inspect(source, pack)
    if issues:
        raise ValueError(f"{locale}: structural mismatch: {issues[:5]}")
    source_rows = source_recipes(source)
    if recipe_id and recipe_id not in {row["id"] for row in source_rows}:
        raise ValueError(f"unknown recipe id: {recipe_id}")
    candidates = {row["id"]: row for row in pack["recipes"]}
    triage = {row["recipeId"]: row for row in italian_triage(source)["recipes"]}
    selected = [row for row in source_rows if recipe_id is None or row["id"] == recipe_id]
    components = [] if recipe_id is not None else [
        paired_component(cid, it, pack["reusableComponents"][cid])
        for cid, it in source["reusableComponents"].items()
    ]
    return {
        "schemaVersion": 1,
        "phase": "F3L_B2_HUMAN_REVIEW_PACKET",
        "locale": locale,
        "sourceLocale": "it",
        "sourceBaselineSha256": digest(source),
        "machineDraftOnly": True,
        "noAutomaticPublication": True,
        "publishable": False,
        "nativeRecipeSignoffs": 0,
        "humanReviewedReusableComponents": 0,
        "candidateRecipeCount": len(selected),
        "candidateComponentCount": len(components),
        "selection": recipe_id or "recipe_000051..recipe_000162",
        "reviewInstructions": (
            "Compare every title, description, equipment item, ingredient/amount/note, "
            "instruction, duration, anime reference and reusable component against Italian. "
            "Escalate food-safety/rights issues to qualified reviewers. Do not infer approval "
            "from machine QA or write reviewEvidence automatically."
        ),
        "recipes": [paired_recipe(it, candidates[it["id"]], triage[it["id"]]) for it in selected],
        "reusableComponents": components,
    }


def load_inputs(source_path: Path, draft_dir: Path) -> tuple[dict, dict]:
    source = json.loads(source_path.read_text(encoding="utf-8"))
    packs = {}
    for loc in LOCALES:
        path = draft_dir / f"f3l_{loc}_51_162_review_draft.json"
        pack = json.loads(path.read_text(encoding="utf-8"))
        if pack.get("locale") != loc:
            raise ValueError(f"{path}: embedded locale mismatch; expected {loc!r}, got {pack.get('locale')!r}")
        packs[loc] = pack
    return source, packs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_PATH)
    parser.add_argument("--draft-dir", type=Path, default=DRAFT_DIR)
    parser.add_argument("--locale", choices=("all",) + LOCALES, default="all")
    parser.add_argument("--recipe-id", help="Optional stable recipe ID for focused review")
    parser.add_argument("--out-dir", type=Path, help="Write review artifacts only here; never runtime assets")
    args = parser.parse_args()
    source, packs = load_inputs(args.source, args.draft_dir)
    languages = LOCALES if args.locale == "all" else (args.locale,)
    dossiers = {
        locale: build_dossier(source, packs[locale], recipe_id=args.recipe_id)
        for locale in languages
    }
    triage = italian_triage(source)
    if args.out_dir is not None:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "F3L_B2_IT_SOURCE_TRIAGE.json").write_text(
            json.dumps(triage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        for locale, dossier in dossiers.items():
            (args.out_dir / f"F3L_B2_{locale.upper()}_REVIEW_DOSSIER.json").write_text(
                json.dumps(dossier, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    print(json.dumps({
        "sourceSha256": digest(source),
        "italianRecipesPendingReview": triage["pendingRecipeCount"],
        "italianObservedCopyConflicts": triage["observedConflictCount"],
        "italianCopyTriageCandidates": triage["flaggedRecipeCount"],
        "locales": list(dossiers),
        "bilingualRecipes": sum(x["candidateRecipeCount"] for x in dossiers.values()),
        "bilingualComponents": sum(x["candidateComponentCount"] for x in dossiers.values()),
        "humanSignoffs": 0,
        "releaseEligible": False,
        "filesWritten": args.out_dir is not None,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

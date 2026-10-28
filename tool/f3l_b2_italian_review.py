#!/usr/bin/env python3
"""F3L B2: source-locked Italian editorial candidates, never silent publishing.

112 source-specific AI-assisted description proposals, plus a contextual
review queue. This is a staging artifact, NOT culinary/human certification.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from f3l_translation_gate import digest, source_recipes

EXPECTED_SOURCE_SHA = "954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c"
PROPOSALS_DIR = Path("docs/f3l_editorial/italian_proposals")
PARTS = ((51, 78), (79, 106), (107, 134), (135, 162))
LOCALES = ("en", "es", "fr", "de", "pt")

# These are *pending investigations*; evidence is captured from the Italian
# source below. Never equate this list with all possible unsafe instructions.
OBSERVED_REVIEW_LEADS = {
    52: ("method_wording", "Stendi ogni pallina forma un disco"),
    54: ("method_wording", "In una padella rosoli la cipolla"),
    56: ("raw_seafood_qualified_review", "salmone fresco per sashimi"),
    59: ("shellfish_handling_qualified_review", "vongole fresche (fatte spurgare"),
    60: ("split_instruction", "Finché il composto diventa chiaro"),
    61: ("method_wording", "In una pentola, capiente"),
    73: ("incorrect_meat_method_description", "struttura dell’impasto"),
    74: ("article_and_boilerplate", "Nel Oden Invernale"),
    80: ("species_name_and_fish_handling", "Luccio di mare/Costardella"),
    81: ("incorrect_sandwich_method_description", "struttura all’impasto"),
    88: ("split_instruction_and_dough_description", "(es."),
    96: ("shellfish_handling_qualified_review", "vongole asari (o veraci)"),
    104: ("method_typo", "cuocerela"),
    110: ("offal_qualified_review", "trippa o frattaglie"),
    117: ("poultry_qualified_review", "sovracosce di pollo"),
    124: ("raw_sea_urchin_qualified_review", "Assaggia una piccola quantità di uni"),
    133: ("poultry_qualified_review", "sovracosce di pollo disossate con pelle"),
    146: ("raw_tuna_qualified_review", "idoneo al consumo crudo"),
    149: ("cooked_rice_storage_qualified_review", "riso cotto del giorno prima"),
    150: ("duck_cooking_qualified_review", "Gira il petto d'anatra"),
    153: ("raw_egg_yolk_qualified_review", "tuorlo d'uovo fresco"),
    156: ("shellfish_handling_qualified_review", "vongole veraci spurgate"),
}
# Some observations are in title, ingredient names, description or steps.
def matched_source_excerpt(recipe: dict, needle: str) -> dict:
    corpus = [
        ("title", recipe["title"]),
        ("description", recipe["description"]),
        *[(f"ingredient_{i+1}", x["name"]) for i, x in enumerate(recipe["ingredients"])],
        *[(f"step_{i+1}", x["instruction"]) for i, x in enumerate(recipe["steps"])],
    ]
    for field, text in corpus:
        if needle.casefold() in text.casefold():
            return {"field": field, "excerpt": text}
    raise ValueError(f"{recipe['id']}: observed lead without source evidence: {needle!r}")


def load_proposals(folder: Path = PROPOSALS_DIR) -> dict:
    proposals = {}
    for start, end in PARTS:
        path = folder / f"{start:03d}_{end:03d}.json"
        part = json.loads(path.read_text(encoding="utf-8"))
        if (part.get("schemaVersion") != 1 or part.get("locale") != "it"
                or part.get("sourceBaselineSha256") != EXPECTED_SOURCE_SHA
                or part.get("range") != [start, end]
                or part.get("reviewKind")
                != "AI_ASSISTED_SOURCE_LOCKED_DESCRIPTION_PROPOSALS_NOT_APPLIED"):
            raise ValueError(f"{path}: unsafe or stale proposal envelope")
        records = part.get("proposals", [])
        if len(records) != end - start + 1:
            raise ValueError(f"{path}: incomplete proposal coverage")
        for n, row in enumerate(records, start):
            rid = f"recipe_{n:06d}"
            if row.get("recipeId") != rid or rid in proposals:
                raise ValueError(f"{path}: missing, reordered or duplicate recipe {rid}")
            if row.get("reviewStatus") != "CANDIDATE_NOT_APPROVED":
                raise ValueError(f"{rid}: candidate must not claim approval")
            description = row.get("proposedDescriptionIT")
            if (not isinstance(description, str) or len(description.strip()) < 75
                    or re.search(r"\b(?:TODO|lorem ipsum|placeholder)\b", description, re.I)):
                raise ValueError(f"{rid}: missing/placeholder Italian candidate")
            proposals[rid] = description
    if len(proposals) != 112:
        raise ValueError("112 source-specific proposals required")
    return proposals


def build(source: dict, proposals: dict) -> dict:
    rows = source_recipes(source)
    if digest(source) != EXPECTED_SOURCE_SHA:
        raise ValueError("Italian source changed: proposals are stale; migrate and re-review")
    if set(proposals) != {r["id"] for r in rows}:
        raise ValueError("proposal IDs must equal the 112 canonical recipe IDs")
    review_rows = []
    for recipe in rows:
        n = int(recipe["id"].split("_")[1])
        lead = OBSERVED_REVIEW_LEADS.get(n)
        findings = []
        if lead:
            label, needle = lead
            findings.append({
                "kind": label,
                "certainty": "source_text_observed_review_needed",
                **matched_source_excerpt(recipe, needle),
            })
        time = recipe.get("times", {})
        prep, cook, total = (
            time.get("prepMinutes"), time.get("sourceCookMinutes"),
            time.get("totalElapsedMinutes")
        )
        if all(isinstance(v, (int, float)) for v in (prep, cook, total)):
            # Only flag; resting and other elapsed time make simple sum unreliable.
            if prep + cook != total:
                findings.append({
                    "kind": "elapsed_time_arithmetic_requires_context",
                    "certainty": "heuristic_not_a_confirmed_error",
                    "prepMinutes": prep, "sourceCookMinutes": cook,
                    "totalElapsedMinutes": total,
                })
        review_rows.append({
            "recipeId": recipe["id"],
            "sourceRecipeSha256": digest(recipe),
            "sourceContentVersion": recipe["targetContentVersion"],
            "titleIT": recipe["title"],
            "originalDescriptionIT": recipe["description"],
            "proposedDescriptionIT": proposals[recipe["id"]],
            "descriptionChangedInProposal": proposals[recipe["id"]] != recipe["description"],
            "status": "PENDING_ITALIAN_HUMAN_EDITORIAL_ACCEPTANCE_AND_ATOMIC_LOCALE_MIGRATION",
            "reviewEvidence": None,
            "qualificationsVerified": False,
            "findingsRequiringReview": findings,
        })
    return {
        "schemaVersion": 1,
        "phase": "F3L_B2_ITALIAN_AI_ASSISTED_COPY_REVIEW",
        "sourceBaselineSha256": digest(source),
        "canonicalSourceModified": False,
        "stagingOnly": True,
        "noAutomaticPublication": True,
        "machineDraftLocalesUnaffected": list(LOCALES),
        "sourceRecipeCount": 112,
        "descriptionProposalCount": len(review_rows),
        "descriptionChangeCandidates": sum(r["descriptionChangedInProposal"] for r in review_rows),
        "observedSourceLeads": sum(bool(OBSERVED_REVIEW_LEADS.get(int(r["recipeId"][-6:]))) for r in review_rows),
        "timingReviewLeads": sum(any(f["kind"] == "elapsed_time_arithmetic_requires_context"
                                     for f in r["findingsRequiringReview"]) for r in review_rows),
        "humanEditorialSignoffs": 0,
        "sourceApprovedForPromotion": False,
        "releaseApproved": False,
        "reviewNotice": (
            "112/112 AI-assisted proposals are available for line-by-line editorial decisions. "
            "No human/culinary/food-safety review is attested. To apply any accepted change, "
            "update canonical source versions and FIVE translated packs atomically, "
            "including their recipe fingerprints and source-dependent tools; "
            "never merely rebind unchanged translation prose to a new source hash."
        ),
        "recipes": review_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path,
                        default=Path("authoring/f3k_it_hardening_51_162.json"))
    parser.add_argument("--proposals-dir", type=Path, default=PROPOSALS_DIR)
    parser.add_argument("--out-dir", type=Path,
                        default=Path("build/f3l-b2-italian-review"))
    args = parser.parse_args()
    # Never let this review tool write into canonical authoring or runtime paths.
    root = (Path.cwd() / "build").resolve()
    output = args.out_dir.resolve()
    if not output.is_relative_to(root) or output == root:
        raise ValueError("review output must be a subdirectory under build/")
    source = json.loads(args.source.read_text(encoding="utf-8"))
    report = build(source, load_proposals(args.proposals_dir))
    output.mkdir(parents=True, exist_ok=True)
    (output / "F3L_B2_ITALIAN_REVIEW_CANDIDATES.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "recipes"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

from recipe_authoring_lib import (
    load_asset_manifest,
    load_json,
    load_recipe_files,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "authoring" / "catalog.json"


def build_queue(
    recipes: list[dict],
    assets: dict[str, dict],
    *,
    default_locale: str,
    ids: set[str] | None = None,
    missing_only: bool = False,
) -> list[dict]:
    queue: list[dict] = []
    for recipe in sorted(recipes, key=lambda item: str(item["id"])):
        recipe_id = str(recipe["id"])
        if ids is not None and recipe_id not in ids:
            continue

        asset_id = recipe.get("imageAssetId")
        asset = assets.get(asset_id, {}) if asset_id else {}
        review = asset.get("semanticReview", {})
        approved = (
            asset_id is not None
            and review.get("status") == "approved"
            and review.get("reviewedContentVersion")
            == recipe.get("contentVersion")
        )
        if missing_only and approved:
            continue

        localized = recipe["locales"][default_locale]
        queue.append(
            {
                "recipeId": recipe_id,
                "contentVersion": recipe["contentVersion"],
                "title": localized["title"],
                "inspirationTitle": recipe["inspirationTitle"],
                "difficulty": recipe["difficulty"],
                "prepMinutes": recipe["prepMinutes"],
                "cookMinutes": recipe["cookMinutes"],
                "ingredients": [
                    {
                        "id": item["id"],
                        "name": localized["ingredients"][item["id"]]["name"],
                        "quantity": item.get("quantity"),
                        "unit": item.get("unit"),
                    }
                    for item in recipe["ingredients"]
                ],
                "steps": [
                    localized["steps"][step["id"]]
                    for step in recipe["steps"]
                ],
                "currentAssetId": asset_id,
                "artworkApproved": approved,
                "expectedAssetId": f"{recipe_id}_artwork",
                "expectedPath": (
                    f"assets/recipe_artwork/{recipe_id}.jpg"
                ),
                "renderingContract": {
                    "singleAsset": True,
                    "card": "same asset cropped by UI with BoxFit.cover",
                    "detail": "same asset shown uncropped with BoxFit.contain",
                },
                "semanticReviewRequired": True,
            }
        )
    return queue


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a deterministic batch queue for recipe artwork."
    )
    parser.add_argument("--ids", nargs="*")
    parser.add_argument("--missing-only", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "authoring" / "artwork_queue.json",
    )
    args = parser.parse_args()

    config = load_json(CONFIG)
    recipes = [
        recipe
        for _, recipe in load_recipe_files(
            [ROOT / str(config["productionSource"])]
        )
    ]
    assets = load_asset_manifest(
        ROOT / str(config["assetManifest"])
    )
    queue = build_queue(
        recipes,
        assets,
        default_locale=str(config["defaultLocale"]),
        ids=set(args.ids) if args.ids else None,
        missing_only=args.missing_only,
    )
    output = args.output.resolve()
    write_json(
        output,
        {
            "schemaVersion": 1,
            "recipeCount": len(queue),
            "recipes": queue,
        },
    )
    print(f"Artwork queue: {len(queue)} recipe(s) -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_DIR))

from build_recipe_artwork_queue import build_queue  # noqa: E402
from recipe_authoring_lib import (  # noqa: E402
    validate_asset_usage,
    validate_authoring_recipe,
)

ROOT = TOOL_DIR.parents[0]
CONFIG = json.loads(
    (ROOT / "authoring" / "catalog.json").read_text(encoding="utf-8")
)
FIXTURE = json.loads(
    (
        ROOT
        / "authoring"
        / "fixtures"
        / "fixture_noodles.json"
    ).read_text(encoding="utf-8")
)


def _asset(*, recipe_id: str, version: int, status: str = "approved"):
    return {
        "id": f"{recipe_id}_artwork",
        "path": f"assets/recipe_artwork/{recipe_id}.jpg",
        "rights": "original",
        "recipeId": recipe_id,
        "semanticReview": {
            "status": status,
            "reviewedContentVersion": version,
            "reviewedAt": "2026-10-23",
            "note": "Test semantic review.",
        },
    }


class RecipeArtworkPipelineTest(unittest.TestCase):
    def test_published_recipe_accepts_current_approved_artwork(self):
        recipe = copy.deepcopy(FIXTURE)
        asset = _asset(
            recipe_id=recipe["id"],
            version=recipe["contentVersion"],
        )
        recipe["imageAssetId"] = asset["id"]

        errors, _ = validate_authoring_recipe(
            recipe,
            CONFIG,
            {asset["id"]: asset},
        )

        self.assertEqual(errors, [])

    def test_published_recipe_rejects_artwork_for_another_recipe(self):
        recipe = copy.deepcopy(FIXTURE)
        asset = _asset(recipe_id="other_recipe", version=1)
        recipe["imageAssetId"] = asset["id"]

        errors, _ = validate_authoring_recipe(
            recipe,
            CONFIG,
            {asset["id"]: asset},
        )

        self.assertTrue(
            any("belongs to another recipe" in error for error in errors)
        )

    def test_published_recipe_rejects_stale_semantic_review(self):
        recipe = copy.deepcopy(FIXTURE)
        recipe["contentVersion"] = 2
        asset = _asset(recipe_id=recipe["id"], version=1)
        recipe["imageAssetId"] = asset["id"]

        errors, _ = validate_authoring_recipe(
            recipe,
            CONFIG,
            {asset["id"]: asset},
        )

        self.assertTrue(
            any("semantic review is stale" in error for error in errors)
        )

    def test_asset_usage_rejects_orphan_artwork(self):
        assets = {
            "unused_artwork": _asset(
                recipe_id="unused",
                version=1,
            )
        }
        errors = validate_asset_usage([FIXTURE], assets)
        self.assertEqual(
            errors,
            ["Unused recipe artwork asset: unused_artwork"],
        )

    def test_batch_queue_marks_missing_artwork(self):
        queue = build_queue(
            [FIXTURE],
            {},
            default_locale="en",
            missing_only=True,
        )
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["recipeId"], FIXTURE["id"])
        self.assertFalse(queue[0]["artworkApproved"])
        self.assertTrue(queue[0]["semanticReviewRequired"])


if __name__ == "__main__":
    unittest.main()

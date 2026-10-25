from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tool"))

from f3g_editorial_gate import validate_f3g_recipe


CONFIG = {
    "supportedLocales": ["en", "it"],
}

BASE = {
    "id": "recipe_test",
    "status": "published",
    "animeReferences": [
        {
            "workTitle": "Synthetic Series",
            "relation": "inspired",
            "season": None,
            "episode": None,
            "chapter": None,
        }
    ],
    "editorialVerification": {
        "culinaryStatus": "verified",
        "culinaryNote": "Synthetic culinary verification note used by the unit test.",
        "animeStatus": "unverified",
        "animeNote": "Synthetic inspiration only; no factual appearance is claimed.",
    },
    "locales": {
        locale: {
            "description": (
                "A sufficiently complete synthetic recipe description used only "
                "to validate the F3G editorial publication contract in tests."
            ),
            "animeContext": (
                "Synthetic inspiration context that is deliberately long enough "
                "for the F3G publication gate."
            ),
            "steps": {
                "step_1": (
                    "Prepare the synthetic ingredient carefully and observe the "
                    "texture before moving to the next operation."
                ),
                "step_2": (
                    "Cook over controlled heat for the stated time, checking the "
                    "visual doneness cue before removing it."
                ),
                "step_3": (
                    "Rest briefly, make the final seasoning adjustment and serve "
                    "while the intended texture is still at its best."
                ),
            },
        }
        for locale in CONFIG["supportedLocales"]
    },
}


class F3GEditorialGateTest(unittest.TestCase):
    def test_complete_published_recipe_passes(self) -> None:
        self.assertEqual(validate_f3g_recipe(BASE, CONFIG), [])

    def test_published_recipe_rejects_missing_description(self) -> None:
        recipe = copy.deepcopy(BASE)
        del recipe["locales"]["it"]["description"]
        errors = validate_f3g_recipe(recipe, CONFIG)
        self.assertTrue(any("description" in error for error in errors))

    def test_unverified_relation_cannot_ship_as_fact(self) -> None:
        recipe = copy.deepcopy(BASE)
        recipe["animeReferences"][0]["relation"] = "unverified"
        errors = validate_f3g_recipe(recipe, CONFIG)
        self.assertTrue(any("unverified" in error for error in errors))

    def test_forbidden_editorial_token_is_rejected(self) -> None:
        recipe = copy.deepcopy(BASE)
        recipe["locales"]["it"]["steps"]["step_2"] += " undefined"
        errors = validate_f3g_recipe(recipe, CONFIG)
        self.assertTrue(any("forbidden editorial token" in error for error in errors))

    def test_forbidden_token_in_ingredient_copy_is_rejected(self) -> None:
        recipe = copy.deepcopy(BASE)
        recipe["locales"]["it"]["ingredients"] = {
            "synthetic": {"name": "Ingredient placeholder", "note": None}
        }
        errors = validate_f3g_recipe(recipe, CONFIG)
        self.assertTrue(any("ingredient synthetic" in error for error in errors))

    def test_verified_appearance_requires_verified_anime_status(self) -> None:
        recipe = copy.deepcopy(BASE)
        recipe["animeReferences"][0]["relation"] = "verified_appearance"
        errors = validate_f3g_recipe(recipe, CONFIG)
        self.assertTrue(any("animeStatus=verified" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_DIR))

from recipe_authoring_lib import (  # noqa: E402
    attach_review_decision,
    build_similarity_report,
    compare_recipes,
    compile_runtime_catalog,
    load_policy,
    validate_authoring_recipe,
)

ROOT = TOOL_DIR.parents[0]
CONFIG = json.loads(
    (
        ROOT / "authoring" / "catalog.json"
    ).read_text(encoding="utf-8")
)
POLICY = load_policy(
    ROOT
    / "authoring"
    / "config"
    / "similarity_policy.json"
)
FIXTURE = json.loads(
    (
        ROOT
        / "authoring"
        / "fixtures"
        / "fixture_noodles.json"
    ).read_text(encoding="utf-8")
)


class RecipeAuthoringTest(unittest.TestCase):
    def test_fixture_validates_and_compiles_to_f1_contract(
        self,
    ) -> None:
        errors, completeness = (
            validate_authoring_recipe(
                FIXTURE, CONFIG, {}
            )
        )
        self.assertEqual(errors, [])
        self.assertTrue(
            completeness["complete"]
        )

        compiled = compile_runtime_catalog(
            [FIXTURE], CONFIG, {}
        )
        self.assertEqual(
            compiled["recipes.json"]["recipes"][
                0
            ]["id"],
            "fixture_noodles",
        )
        self.assertEqual(
            compiled["locales/it.json"][
                "recipes"
            ]["fixture_noodles"]["title"],
            "Noodles di prova",
        )

    def test_same_id_same_fingerprint_is_idempotent_duplicate(
        self,
    ) -> None:
        result = compare_recipes(
            FIXTURE,
            copy.deepcopy(FIXTURE),
            CONFIG,
            POLICY,
        )

        self.assertEqual(
            result["classification"],
            "idempotent_duplicate",
        )
        self.assertEqual(
            result["recommendedAction"],
            "SKIP",
        )

    def test_same_id_changed_content_is_same_entity_update(
        self,
    ) -> None:
        changed = copy.deepcopy(FIXTURE)
        changed["contentVersion"] = 2
        changed["cookMinutes"] = 9

        result = compare_recipes(
            FIXTURE,
            changed,
            CONFIG,
            POLICY,
        )

        self.assertEqual(
            result["classification"],
            "same_entity_update",
        )
        self.assertEqual(
            result["recommendedAction"],
            "UPDATE_OR_REVIEW",
        )

    def test_unit_conversion_and_aliases_detect_equivalent_recipe(
        self,
    ) -> None:
        other = copy.deepcopy(FIXTURE)
        other["id"] = "fixture_noodles_alt"
        other["ingredients"][1]["id"] = "shoyu"
        other["ingredients"][1]["quantity"] = 3
        other["ingredients"][1]["unit"] = "tsp"
        for locale in other["locales"].values():
            soy = locale["ingredients"].pop(
                "soy_sauce"
            )
            locale["ingredients"]["shoyu"] = soy
        other["locales"]["en"]["ingredients"][
            "shoyu"
        ]["name"] = "Shoyu"

        result = compare_recipes(
            FIXTURE, other, CONFIG, POLICY
        )

        self.assertGreaterEqual(
            result["dimensions"]["ingredients"],
            0.99,
        )
        self.assertGreaterEqual(
            result["dimensions"]["quantities"],
            0.99,
        )
        self.assertEqual(
            result["classification"],
            "probable_duplicate",
        )

    def test_same_title_with_materially_different_recipe_avoids_false_duplicate(
        self,
    ) -> None:
        other = copy.deepcopy(FIXTURE)
        other["id"] = "fixture_rice"
        other["ingredients"] = [
            {
                "id": "rice",
                "quantity": 200,
                "unit": "g",
            }
        ]
        other["steps"] = [
            {
                "id": "bake",
                "timerSeconds": 1800,
            }
        ]
        other["prepMinutes"] = 20
        other["cookMinutes"] = 30
        for localized in other["locales"].values():
            localized["ingredients"] = {
                "rice": {
                    "name": "Rice",
                    "note": None,
                }
            }
            localized["steps"] = {
                "bake": (
                    "Bake the rice casserole "
                    "until browned."
                )
            }

        result = compare_recipes(
            FIXTURE, other, CONFIG, POLICY
        )

        self.assertNotIn(
            result["classification"],
            {
                "probable_duplicate",
                "review_required",
            },
        )

    def test_review_memory_is_invalidated_when_content_fingerprint_changes(
        self,
    ) -> None:
        other = copy.deepcopy(FIXTURE)
        other["id"] = (
            "fixture_noodles_variant"
        )
        comparison = compare_recipes(
            FIXTURE, other, CONFIG, POLICY
        )
        decision = {
            "leftId": comparison["leftId"],
            "rightId": comparison["rightId"],
            "leftFingerprint": comparison[
                "leftFingerprint"
            ],
            "rightFingerprint": comparison[
                "rightFingerprint"
            ],
            "normalizerVersion": comparison[
                "normalizerVersion"
            ],
            "decision": "keep_variant",
            "reviewedAt": "2026-10-22",
        }

        resolved = attach_review_decision(
            comparison, [decision]
        )
        self.assertTrue(
            resolved["reviewResolved"]
        )

        changed = copy.deepcopy(other)
        changed["cookMinutes"] = 99
        stale = attach_review_decision(
            compare_recipes(
                FIXTURE,
                changed,
                CONFIG,
                POLICY,
            ),
            [decision],
        )
        self.assertFalse(
            stale["reviewResolved"]
        )

    def test_published_recipe_requires_all_supported_locales(
        self,
    ) -> None:
        other = copy.deepcopy(FIXTURE)
        del other["locales"]["de"]

        errors, report = (
            validate_authoring_recipe(
                other, CONFIG, {}
            )
        )

        self.assertTrue(
            any(
                "missing locales" in error
                for error in errors
            )
        )
        self.assertIn(
            "de", report["missingLocales"]
        )

    def test_similarity_report_is_deterministic_and_blocks_unreviewed_match(
        self,
    ) -> None:
        other = copy.deepcopy(FIXTURE)
        other["id"] = (
            "fixture_noodles_variant"
        )

        first = build_similarity_report(
            [FIXTURE, other],
            CONFIG,
            POLICY,
            [],
        )
        second = build_similarity_report(
            [FIXTURE, other],
            CONFIG,
            POLICY,
            [],
        )

        self.assertEqual(first, second)
        self.assertEqual(
            first["summary"][
                "unresolvedBlocking"
            ],
            1,
        )


if __name__ == "__main__":
    unittest.main()

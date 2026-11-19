"""Zero-paid-AI regression for 28 source-bound recipe fixes and their runtime."""
from pathlib import Path
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tool/semantic_qa_food_glossary.py"
spec = importlib.util.spec_from_file_location("qa_food_glossary", SCRIPT)
glossary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(glossary)

REVIEWED_IDS = tuple(f"recipe_{i:06d}" for i in (
    55, 61, 63, 66, 71, 73, 75, 76, 78, 82, 83, 90, 92, 98,
    100, 108, 112, 114, 118, 123, 130, 131, 133, 134, 138, 147, 151, 156
))
ALL_LOCALES = ("it", "en", "es", "fr", "de", "pt")

def read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class CulinaryGlossaryRegression(unittest.TestCase):
    def test_source_bound_wrong_ingredient_examples_and_valid_ones(self):
        for locale, bad, good in (
            ("en", "onions", "spring onions"),
            ("es", "cipollotto fresco picado", "cebolleta fresca picada"),
            ("fr", "ciboulette", "cébette fraîche émincée"),
            ("de", "gehackte Zwiebel", "gehackte Frühlingszwiebel"),
            ("de", "Schnittlauch", "Frühlingszwiebeln"),
            ("pt", "cebolinho", "cebola de rama"),
            ("pt", "cebola cortada em lavadoras", "cebola de rama às rodelas"),
        ):
            with self.subTest(locale=locale, target=bad):
                self.assertTrue(glossary.is_mistranslation(locale, bad))
                self.assertFalse(glossary.is_mistranslation(locale, good))

    def test_all_162_published_recipes_have_no_known_scallion_errors(self):
        result = glossary.scan(ROOT)
        self.assertEqual(result["recipeCount"], 162)
        self.assertEqual(result["sourceIngredientCount"], 40)
        self.assertEqual(result["comparisonCount"], 200)
        self.assertEqual(result["findingsCount"], 0)
        self.assertEqual(result["affectedRecordCount"], 0)
        self.assertEqual(result["paidAiApiCalls"], 0)
        self.assertEqual(result["certification"], "NOT_CERTIFIED")

    def test_all_28_updated_authoring_versions_match_materialized_runtime(self):
        packs = {locale: read(f"assets/catalog/locales/{locale}.json")["recipes"]
                 for locale in ALL_LOCALES}
        canonical = {r["id"]: r for r in read("assets/catalog/recipes.json")["recipes"]}
        self.assertEqual(len(REVIEWED_IDS), 28)
        for rid in REVIEWED_IDS:
            with self.subTest(recipe=rid):
                source = read(f"authoring/recipes/{rid}.json")
                self.assertEqual(source["status"], "published")
                self.assertIsNone(source["imageAssetId"])
                self.assertEqual(canonical[rid]["contentVersion"],
                                 source["contentVersion"])
                self.assertEqual(
                    [(x["id"], x["quantity"], x["unit"]) for x in canonical[rid]["ingredients"]],
                    [(x["id"], x["quantity"], x["unit"]) for x in source["ingredients"]])
                self.assertEqual(canonical[rid]["steps"], source["steps"])
                for locale in ALL_LOCALES:
                    original = source["locales"][locale]
                    item = packs[locale][rid]
                    self.assertEqual(item["description"], original["description"])
                    self.assertEqual(item["ingredientTexts"], original["ingredients"])
                    self.assertEqual(item["stepTexts"], original["steps"])
                    self.assertEqual(item["title"], original["title"])
                    self.assertEqual(item["animeContext"], original["animeContext"])

    def test_tsukemen_seven_steps_and_real_dipping_actions(self):
        tsukemen = read("authoring/recipes/recipe_000083.json")
        self.assertEqual(tsukemen["contentVersion"], 5)
        self.assertEqual(len(tsukemen["steps"]), 7)
        self.assertIn("katsuobushi", tsukemen["locales"]["it"]["ingredients"]
                      ["polvere_di_pesce"]["name"].lower())
        for locale in ALL_LOCALES:
            with self.subTest(locale=locale):
                v = tsukemen["locales"][locale]
                self.assertEqual(len(v["steps"]), 7)
                self.assertTrue(all(v["steps"][f"step_{i}"].strip()
                                    for i in range(1, 8)))
                self.assertIn("5", v["steps"]["step_3"])
                self.assertIn("6", v["steps"]["step_3"])
                self.assertNotIn("intingol", v["description"].lower() if locale != "it" else "")
                for invalid in ("poor katsuobushi", "katsuobushi pauvre",
                                "arme katsuobushi", "pobre katsuobushi",
                                "brodo de porco", "guárdalo ahora",
                                "concentre- se", "se teñi"):
                    self.assertNotIn(invalid, (
                        v["description"] + " " + " ".join(v["steps"].values()) + " " +
                        " ".join(x["name"] for x in v["ingredients"].values())
                    ).lower())
if __name__ == "__main__":
    unittest.main()

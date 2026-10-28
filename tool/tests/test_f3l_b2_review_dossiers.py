"""F3L B2 must generate inspectable work, not editorial certification."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from f3l_b2_review_dossiers import (
    KNOWN_ITALIAN_COPY_ISSUES,
    LOCALES,
    build_dossier,
    italian_triage,
    load_inputs,
)


class F3LB2ReviewDossiersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source, cls.packs = load_inputs(
            Path("authoring/f3k_it_hardening_51_162.json"),
            Path("authoring/f3l_review_drafts"),
        )

    def test_italian_source_triage_is_complete_and_unapproved(self):
        report = italian_triage(self.source)
        self.assertEqual(report["pendingRecipeCount"], 112)
        self.assertFalse(report["editorialReviewComplete"])
        self.assertEqual(report["reviewedByQualifiedHuman"], 0)
        self.assertEqual(len(report["recipes"]), 112)
        flagged = {r["recipeId"] for r in report["recipes"] if r["priority"] == "HIGH"}
        self.assertEqual(flagged, set(KNOWN_ITALIAN_COPY_ISSUES))
        self.assertEqual(
            {r["recipeId"] for r in report["recipes"]},
            {f"recipe_{i:06d}" for i in range(51, 163)},
        )

    def test_five_full_bilingual_packets_cover_every_field_and_component(self):
        totals = []
        for locale in LOCALES:
            with self.subTest(locale=locale):
                packet = build_dossier(self.source, self.packs[locale])
                self.assertFalse(packet["publishable"])
                self.assertTrue(packet["noAutomaticPublication"])
                self.assertTrue(packet["machineDraftOnly"])
                self.assertEqual(packet["nativeRecipeSignoffs"], 0)
                self.assertEqual(packet["candidateRecipeCount"], 112)
                self.assertEqual(packet["candidateComponentCount"], 10)
                self.assertEqual(len(packet["reusableComponents"]), 10)
                self.assertEqual(
                    [r["recipeId"] for r in packet["recipes"]],
                    [r["id"] for r in self.source["recipes"]],
                )
                for raw, paired in zip(self.source["recipes"], packet["recipes"]):
                    self.assertEqual(len(paired["ingredients"]), len(raw["ingredients"]))
                    self.assertEqual(len(paired["steps"]), len(raw["steps"]))
                    self.assertEqual(len(paired["equipment"]), len(raw["equipment"]))
                    self.assertIsNone(paired["humanReviewEvidence"])
                    self.assertEqual(paired["servings"], {
                        "it": raw["servings"],
                        "candidate": self.packs[locale]["recipes"][self.source["recipes"].index(raw)]["servings"],
                    })
                    self.assertEqual(paired["numericTimes"]["it"], {
                        key: value for key, value in raw["times"].items() if key != "note"
                    })
                    self.assertEqual(paired["numericTimes"]["candidate"], {
                        key: value for key, value in self.packs[locale]["recipes"][self.source["recipes"].index(raw)]["times"].items() if key != "note"
                    })
                    for src, dst in zip(raw["steps"], paired["steps"]):
                        self.assertEqual(dst["stableStepId"], src["id"])
                        self.assertEqual(dst["timerSeconds"], src.get("timerSeconds"))
                    for src, dst in zip(raw["ingredients"], paired["ingredients"]):
                        self.assertEqual(dst["stableIngredientId"], src["id"])
                        self.assertEqual(dst["quantity"], src.get("quantity"))
                        self.assertEqual(dst["unit"], src.get("unit"))
                totals.append((packet["candidateRecipeCount"], packet["candidateComponentCount"]))
        self.assertEqual(sum(x for x, _ in totals), 560)
        self.assertEqual(sum(y for _, y in totals), 50)

    def test_single_recipe_selection_still_unapproved(self):
        packet = build_dossier(
            self.source, self.packs["fr"], recipe_id="recipe_000073"
        )
        self.assertEqual(packet["candidateRecipeCount"], 1)
        self.assertEqual(packet["candidateComponentCount"], 0)
        self.assertIn(
            "observed_source_copy_conflict",
            [x["code"] for x in packet["recipes"][0]["italianSourceTriageFlags"]],
        )
        self.assertFalse(packet["publishable"])

    def test_stale_source_and_missing_lock_fail_closed(self):
        changed_source = copy.deepcopy(self.source)
        changed_source["recipes"][0]["description"] += " Revisione senza versione."
        with self.assertRaisesRegex(ValueError, "stale Italian fingerprint"):
            build_dossier(changed_source, self.packs["en"])
        changed_pack = copy.deepcopy(self.packs["de"])
        changed_pack["editorialStaging"]["noAutomaticPublication"] = False
        with self.assertRaisesRegex(ValueError, "non-publication lock"):
            build_dossier(self.source, changed_pack)

    def test_fabricated_signoff_or_structural_edit_rejected(self):
        changed = copy.deepcopy(self.packs["es"])
        changed["recipes"][0]["reviewStatus"] = "human_reviewed"
        changed["recipes"][0]["reviewEvidence"] = {"reviewer": "fake"}
        with self.assertRaisesRegex(ValueError, "unexpected human sign-off"):
            build_dossier(self.source, changed)
        changed = copy.deepcopy(self.packs["pt"])
        changed["recipes"][0]["ingredients"][0]["quantity"] = 9999
        with self.assertRaisesRegex(ValueError, "structural mismatch"):
            build_dossier(self.source, changed)

    def test_mislabeled_locale_pack_rejected_before_review(self):
        with TemporaryDirectory() as temp_dir:
            draft_dir = Path(temp_dir)
            (draft_dir / "f3l_en_51_162_review_draft.json").write_text(
                json.dumps(self.packs["fr"]), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "embedded locale mismatch"):
                load_inputs(Path("authoring/f3k_it_hardening_51_162.json"), draft_dir)

    def test_unknown_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown recipe"):
            build_dossier(self.source, self.packs["en"], recipe_id="recipe_999999")


if __name__ == "__main__":
    unittest.main()

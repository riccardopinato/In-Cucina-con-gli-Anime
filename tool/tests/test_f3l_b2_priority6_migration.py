"""Bounded F3L B2-1 migration regression: six source revisions, five quarantined drafts."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tool"))
from f3l_translation_gate import digest, inspect, source_recipes
from f3l_semantic_safety_gate import check


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def immutable_fields(recipe):
    filtered = copy.deepcopy(recipe)
    filtered.pop("description")
    filtered.pop("targetContentVersion")
    for step in filtered["steps"]:
        step.pop("instruction")
    return filtered


class PrioritySixMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load("authoring/f3k_it_hardening_51_162.json")
        cls.baseline = load("tool/f3l_b2_priority6_migration_baseline.json")
        cls.payload = load("tool/f3l_b2_priority6_migration_payload.json")
        cls.bulk = load("tool/f3l_b2_2_106_migration_baseline.json")
        cls.enriched = load("tool/f3l_b2_2_101_enrichment_baseline.json")
        cls.packs = {
            loc: load(f"authoring/f3l_review_drafts/f3l_{loc}_51_162_review_draft.json")
            for loc in ("en", "es", "fr", "de", "pt")
        }

    def test_six_historical_source_revisions_survive_following_bulk_migration(self):
        expected = set(self.baseline["changedRecipeIds"])
        self.assertEqual(len(expected), 6)
        self.assertEqual(set(self.payload["ids"]), expected)
        self.assertEqual(
            self.baseline["postMigrationSourceSha256"],
            self.bulk["preMigrationSourceSha256"],
        )
        self.assertEqual(
            self.payload["preMigrationSourceSha256"],
            self.baseline["preMigrationSourceSha256"],
        )
        self.assertEqual(
            digest(self.source), self.enriched["postMigrationSourceSha256"]
        )
        self.assertEqual(
            set(self.baseline["oldRecipeFingerprints"]),
            {r["id"] for r in source_recipes(self.source)},
        )
        self.assertEqual(
            digest(self.source["reusableComponents"]),
            self.baseline["oldReuseComponentsFingerprint"],
        )
        for row in self.source["recipes"]:
            rid = row["id"]
            if rid not in expected:
                continue  # B2-2 changes are verified by its separate regression test.
            self.assertNotEqual(
                digest(row), self.baseline["oldRecipeFingerprints"][rid]
            )
            self.assertEqual(
                digest(row), self.bulk["oldRecipeSha256"][rid]
            )
            self.assertEqual(
                row["targetContentVersion"],
                self.baseline["oldVersions"][rid] + 1,
            )
            self.assertEqual(
                digest(immutable_fields(row)),
                self.baseline["unchangedFieldsFingerprints"][rid],
            )

    def test_five_language_packs_match_new_source_without_false_approvals(self):
        self.assertTrue(self.payload["noAutomaticPublication"])
        for loc, pack in self.packs.items():
            with self.subTest(locale=loc):
                self.assertEqual(pack["locale"], loc)
                self.assertEqual(
                    pack["sourceBaselineSha256"], digest(self.source)
                )
                self.assertEqual(
                    pack["reviewStatus"], "machine_draft_not_publishable"
                )
                self.assertIs(pack["editorialStaging"]["noAutomaticPublication"], True)
                b2 = pack["editorialStaging"]["b2Priority6"]
                self.assertEqual(b2["sourceSha256"], self.baseline["postMigrationSourceSha256"])
                self.assertEqual(pack["editorialStaging"]["b2BulkItalianDescriptions"]["sourceSha256"], self.bulk["postMigrationSourceSha256"])
                self.assertEqual(set(b2["updatedRecipeIds"]), set(self.payload["ids"]))
                self.assertEqual(b2["editedDescriptionCount"], 6)
                self.assertEqual(b2["editedStepCount"], 5)
                self.assertEqual(len(pack["recipes"]), 112)
                self.assertEqual(len(pack["reusableComponents"]), 10)
                self.assertEqual(inspect(self.source, pack), [])
                self.assertTrue(
                    all(
                        r["reviewStatus"] == "machine_draft" and not r.get("reviewEvidence")
                        for r in pack["recipes"]
                    )
                )
                translations = {r["id"]: r for r in pack["recipes"]}
                for source_row in self.source["recipes"]:
                    translated = translations[source_row["id"]]
                    self.assertEqual(
                        translated["sourceRecipeSha256"],
                        digest(source_row),
                    )
                    self.assertEqual(
                        translated["sourceContentVersion"],
                        source_row["targetContentVersion"],
                    )
                    n = int(source_row["id"][-6:])
                    if source_row["id"] not in self.payload["ids"]:
                        continue
                    self.assertEqual(
                        translated["description"],
                        self.payload["localizedDescriptions"][loc][str(n)],
                    )
                    for step_id, prose in self.payload[
                        "localizedStepEdits"
                    ][loc].get(str(n), {}).items():
                        self.assertEqual(
                            next(s["instruction"] for s in translated["steps"]
                                 if s["id"] == step_id),
                            prose,
                        )
        self.assertEqual(check(self.source, self.packs), [])

    def test_unsafe_tasting_instruction_removed_in_all_languages(self):
        src = next(
            r for r in self.source["recipes"] if r["id"] == "recipe_000124"
        )["steps"][2]["instruction"].lower()
        self.assertNotIn("assaggia una piccola quantità", src)
        self.assertIn("non assaggiarlo", src)
        self.assertIn("idoneo al consumo crudo", src)
        forbidden = {
            "en": "taste a small amount",
            "es": "prueba una pequeña cantidad",
            "fr": "goûtez une petite quantité",
            "de": "probieren sie eine kleine",
            "pt": "prove uma pequena quantidade",
        }
        for locale, pack in self.packs.items():
            row = next(
                r for r in pack["recipes"] if r["id"] == "recipe_000124"
            )
            self.assertNotIn(
                forbidden[locale], row["steps"][2]["instruction"].lower()
            )

    def test_canonical_drift_or_fabricated_approval_fails(self):
        broken = copy.deepcopy(self.source)
        broken["recipes"][0]["steps"][0]["instruction"] += " changed"
        self.assertNotEqual(
            digest(broken),
            self.enriched["postMigrationSourceSha256"],
        )
        pack = copy.deepcopy(self.packs["en"])
        pack["recipes"][0]["reviewStatus"] = "human_reviewed"
        pack["recipes"][0]["reviewEvidence"] = {"fake": True}
        self.assertTrue(
            any("fingerprint" in issue or "stale" in issue
                for issue in check(broken, self.packs))
        )
        self.assertTrue(
            any("human editorial review missing" in issue
                for issue in inspect(self.source, pack, require_review=True))
        )


if __name__ == "__main__":
    unittest.main()

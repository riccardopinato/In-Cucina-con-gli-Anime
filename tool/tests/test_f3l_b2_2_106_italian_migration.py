"""F3L B2-2: 106 remaining Italian editorial decisions, 105 actual content edits.

Verify exactly 105 versioned description edits and five source-bound machine-draft
translations; zero simulated human reviews and absolutely no auto publication.
"""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tool"))
from f3l_translation_gate import digest, inspect, source_recipes
from f3l_editorial_audit import audit

LOCALES = ("en", "es", "fr", "de", "pt")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def invariant(row):
    value = copy.deepcopy(row)
    value.pop("description")
    value.pop("targetContentVersion")
    return value


class BulkItalianEditorialMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read("authoring/f3k_it_hardening_51_162.json")
        cls.baseline = read("tool/f3l_b2_2_106_migration_baseline.json")
        cls.packs = {loc: read(
            f"authoring/f3l_review_drafts/f3l_{loc}_51_162_review_draft.json"
        ) for loc in LOCALES}

    def test_105_changed_and_seven_unmodified(self):
        source, baseline = self.source, self.baseline
        self.assertEqual(digest(source), baseline["postMigrationSourceSha256"])
        self.assertEqual(len(source_recipes(source)), 112)
        modified = set(baseline["changedRecipeIds"])
        unchanged = set(baseline["unchangedRecipeIds"])
        self.assertEqual(len(modified), 105)
        self.assertEqual(len(unchanged), 7)
        self.assertEqual(modified | unchanged, {r["id"] for r in source["recipes"]})
        self.assertEqual(modified & unchanged, set())
        self.assertIn("recipe_000055", unchanged)
        self.assertEqual(
            digest(source["reusableComponents"]),
            baseline["reusableComponentsSha256"],
        )
        for row in source["recipes"]:
            rid = row["id"]
            if rid in unchanged:
                self.assertEqual(
                    digest(row), baseline["oldRecipeSha256"][rid], rid
                )
                continue
            self.assertNotEqual(
                digest(row), baseline["oldRecipeSha256"][rid], rid
            )
            self.assertEqual(
                row["targetContentVersion"],
                baseline["oldContentVersions"][rid] + 1,
            )
            self.assertEqual(
                digest(invariant(row)),
                baseline["unchangedFieldsSha256"][rid],
                f"Ingredient amounts, IDs, steps, timers, anime provenance or metadata changed: {rid}",
            )
            self.assertGreaterEqual(len(row["description"].strip()), 75)

    def test_five_full_non_publishable_translated_packs(self):
        src = {x["id"]: x for x in self.source["recipes"]}
        for locale, pack in self.packs.items():
            with self.subTest(locale=locale):
                self.assertEqual(pack["locale"], locale)
                self.assertEqual(pack["sourceLocale"], "it")
                self.assertEqual(pack["sourceBaselineSha256"], digest(self.source))
                self.assertEqual(pack["reviewStatus"], "machine_draft_not_publishable")
                self.assertTrue(pack["editorialStaging"]["noAutomaticPublication"])
                self.assertEqual(
                    pack["editorialStaging"]["b2BulkItalianDescriptions"]["status"],
                    "AI_ASSISTED_MACHINE_TRANSLATION_NOT_NATIVE_APPROVED",
                )
                self.assertEqual(
                    pack["editorialStaging"]["b2BulkItalianDescriptions"]["migratedRecipeCount"],
                    105,
                )
                self.assertEqual(len(pack["recipes"]), 112)
                self.assertEqual(len(pack["reusableComponents"]), 10)
                self.assertEqual(inspect(self.source, pack), [])
                self.assertEqual(
                    [r["id"] for r in pack["recipes"]],
                    [r["id"] for r in self.source["recipes"]],
                )
                for row in pack["recipes"]:
                    rid = row["id"]
                    it = src[rid]
                    self.assertEqual(row["sourceRecipeSha256"], digest(it))
                    self.assertEqual(row["sourceContentVersion"], it["targetContentVersion"])
                    self.assertEqual(row["reviewStatus"], "machine_draft")
                    self.assertFalse(row.get("reviewEvidence"))
                    self.assertTrue(row["description"].strip())
                    self.assertNotEqual(
                        row["description"].strip(), it["description"].strip(), rid
                    )
                report = audit(self.source, pack)
                self.assertEqual(report["humanReviewedCount"], 0)
                self.assertFalse(report["releaseApproved"])
                self.assertTrue(any("human editorial review missing" in x for x in
                    inspect(self.source, pack, require_review=True)))

    def test_malformed_source_is_rejected_even_if_target_hashes_are_changed(self):
        src = copy.deepcopy(self.source)
        src["recipes"][0]["description"] += " una nuova modifica non versionata"
        self.assertNotEqual(digest(src), self.baseline["postMigrationSourceSha256"])
        for locale, pack in self.packs.items():
            self.assertTrue(any("fingerprint" in x or "stale" in x
                for x in inspect(src, pack)), locale)


if __name__ == "__main__":
    unittest.main()

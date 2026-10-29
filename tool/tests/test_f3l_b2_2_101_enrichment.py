"""F3L B2-2 follow-up: 101 contextual descriptions and five quarantined language packs."""
from __future__ import annotations
import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tool"))
from f3l_translation_gate import digest, inspect
from f3l_editorial_audit import audit

LOCALES = ("en", "es", "fr", "de", "pt")


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def invariant(row):
    value = copy.deepcopy(row)
    value.pop("description")
    value.pop("targetContentVersion")
    return value


class ContextualItalianDescriptionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load("authoring/f3k_it_hardening_51_162.json")
        cls.previous = load("tool/f3l_b2_2_106_migration_baseline.json")
        cls.baseline = load("tool/f3l_b2_2_101_enrichment_baseline.json")
        cls.ledger = load("tool/f3l_b2_2_101_description_enrichment.json")
        cls.packs = {
            locale: load(f"authoring/f3l_review_drafts/f3l_{locale}_51_162_review_draft.json")
            for locale in LOCALES
        }

    def test_exact_101_italian_edits_and_no_undocumented_facts_drift(self):
        self.assertEqual(digest(self.source), self.baseline["postMigrationSourceSha256"])
        self.assertEqual(
            self.baseline["preMigrationSourceSha256"],
            self.previous["postMigrationSourceSha256"],
        )
        expected = set(self.baseline["modifiedRecipeIds"])
        self.assertEqual(expected, set(self.ledger["appendItalianByRecipeId"]))
        self.assertEqual(len(expected), 101)
        self.assertEqual(len(self.source["recipes"]), 112)
        self.assertEqual(
            digest(self.source["reusableComponents"]),
            self.baseline["reusableComponentsSha256"],
        )
        for row in self.source["recipes"]:
            rid = row["id"]
            before = self.baseline["oldRecipeSha256"][rid]
            if rid not in expected:
                self.assertEqual(digest(row), before, rid)
                continue
            self.assertNotEqual(digest(row), before, rid)
            self.assertEqual(row["targetContentVersion"], self.baseline["oldVersions"][rid] + 1)
            self.assertEqual(
                digest(invariant(row)), self.baseline["immutableFieldsSha256"][rid], rid
            )
            self.assertTrue(
                row["description"].endswith(self.ledger["appendItalianByRecipeId"][rid]), rid
            )
            self.assertGreaterEqual(
                len(re.findall(r"\b[\wÀ-ÿ'-]+\b", row["description"])), 45, rid
            )

    def test_five_pack_identity_quarantine_and_semantic_audit(self):
        source_by_id = {row["id"]: row for row in self.source["recipes"]}
        for locale, pack in self.packs.items():
            with self.subTest(locale=locale):
                self.assertEqual(pack["sourceBaselineSha256"], digest(self.source))
                self.assertEqual(len(pack["recipes"]), 112)
                self.assertEqual(len(pack["reusableComponents"]), 10)
                self.assertEqual(pack["reviewStatus"], "machine_draft_not_publishable")
                self.assertTrue(pack["editorialStaging"]["noAutomaticPublication"])
                stage = pack["editorialStaging"]["b2QualityCompletion101"]
                self.assertEqual(stage["sourceSha256"], digest(self.source))
                self.assertEqual(stage["migratedRecipeCount"], 101)
                self.assertTrue(stage["noAutomaticPublication"])
                self.assertEqual(stage["status"], "AI_ASSISTED_MACHINE_DRAFT_NOT_NATIVE_APPROVED")
                self.assertEqual(inspect(self.source, pack), [])
                self.assertEqual(audit(self.source, pack)["warningCount"], 0)
                for row in pack["recipes"]:
                    src = source_by_id[row["id"]]
                    self.assertEqual(row["sourceRecipeSha256"], digest(src))
                    self.assertEqual(row["sourceContentVersion"], src["targetContentVersion"])
                    self.assertEqual(row["reviewStatus"], "machine_draft")
                    self.assertFalse(row.get("reviewEvidence"))
                self.assertFalse(audit(self.source, pack)["releaseApproved"])
                self.assertTrue(any("human editorial review missing" in msg
                    for msg in inspect(self.source, pack, require_review=True)))

    def test_known_mistranslations_corrected_without_false_signoffs(self):
        checks = {
            "fr": {110: "cuisinier", 139: "cuisinier"},
            "pt": {95: "macarrãoes", 147: "macarrãoes", 154: "macarrãoes", 156: "macarrãoes"},
            "en": {162: "expected album"},
            "de": {162: "geplante Album"},
            "fr": {162: "albume prévu"},
        }
        for locale, rows in checks.items():
            translations = {int(r["id"][-6:]): r for r in self.packs[locale]["recipes"]}
            for n, forbidden in rows.items():
                self.assertNotIn(forbidden.casefold(), translations[n]["description"].casefold())
        for locale, pack in self.packs.items():
            r = next(item for item in pack["recipes"] if item["id"] == "recipe_000162")
            self.assertIn("pasteur", r["description"].lower())

    def test_guard_against_source_and_fake_approval(self):
        modified = copy.deepcopy(self.source)
        modified["recipes"][0]["description"] += " cambio invisibile"
        self.assertNotEqual(digest(modified), self.baseline["postMigrationSourceSha256"])
        for locale, pack in self.packs.items():
            self.assertTrue(any("fingerprint" in issue or "stale" in issue
                                for issue in inspect(modified, pack)), locale)


if __name__ == "__main__":
    unittest.main()

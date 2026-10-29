"""Regression contract: F3L source migration 000089 cannot change recipes or publish drafts."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_translation_gate import digest, inspect
from f3l_editorial_audit import audit

ROOT=Path(__file__).resolve().parents[2]
OLD_SOURCE="4d736cfa431025fdd8c6baa9725adf2525cdf0bcbf2be8508941f5dd68c3710f"
NEW_SOURCE="deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67"
OLD_RECIPE="485c7ba4a19db4b71b5455b990a8b73cbc32ac38c226df989a338c704409cd5e"
NEW_RECIPE="56992a2f75b2eb4e0c5935cd9397be9249519bdce10a72323e5af45b655f6f8b"
OLD_TEXT="Cuoci nel lascia cuocereriso o in pentola con 280ml d'acqua per 15 minuti dal bollore."
NEW_TEXT="Cuoci nel cuociriso o in pentola con 280 ml d'acqua per 15 minuti dal bollore."
LOCALES=("en","es","fr","de","pt")

class SourceMigration000089Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads((ROOT/"authoring/f3k_it_hardening_51_162.json").read_text(encoding="utf-8"))

    def test_exact_versioned_source_delta(self):
        now=self.source
        self.assertEqual(digest(now),NEW_SOURCE)
        self.assertEqual(len(now["recipes"]),112)
        row=next(x for x in now["recipes"] if x["id"]=="recipe_000089")
        self.assertEqual(row["steps"][1]["instruction"],NEW_TEXT)
        self.assertEqual(row["steps"][1]["timerSeconds"],900)
        self.assertEqual(row["targetContentVersion"],5)
        # Legacy rice-cooker repair stays in force after the later B2 description update.
        prior=json.loads((ROOT/"tool/f3l_b2_2_106_migration_baseline.json").read_text(encoding="utf-8"))
        self.assertEqual(prior["oldRecipeSha256"]["recipe_000089"],NEW_RECIPE)
        self.assertNotEqual(digest(row),NEW_RECIPE)
        self.assertEqual(row["targetContentVersion"],prior["oldContentVersions"]["recipe_000089"]+2)

    def test_five_packs_still_frozen_non_publishable(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                path=ROOT/"authoring/f3l_review_drafts"/f"f3l_{locale}_51_162_review_draft.json"
                pack=json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(pack["sourceBaselineSha256"],NEW_SOURCE)
                self.assertEqual(len(pack["recipes"]),112)
                self.assertEqual(inspect(self.source,pack),[])
                row=next(r for r in pack["recipes"] if r["id"]=="recipe_000089")
                self.assertEqual(row["sourceRecipeSha256"],digest(next(x for x in self.source["recipes"] if x["id"]=="recipe_000089")))
                self.assertEqual(row["sourceContentVersion"],5)
                self.assertIn("280",row["steps"][1]["instruction"])
                self.assertIn("15",row["steps"][1]["instruction"])
                self.assertEqual(pack["reviewStatus"],"machine_draft_not_publishable")
                self.assertTrue(pack["editorialStaging"]["noAutomaticPublication"])
                self.assertTrue(all(r["reviewStatus"]=="machine_draft" for r in pack["recipes"]))
                report=audit(self.source,pack)
                self.assertEqual(report["sourceSha256"],NEW_SOURCE)
                self.assertEqual(report["structuralErrorCount"],0)
                self.assertEqual(report["humanReviewedCount"],0)
                self.assertFalse(report["releaseApproved"])
                self.assertTrue(any("human editorial review missing" in e for e in inspect(self.source,pack,require_review=True)))

if __name__=="__main__":
    unittest.main()

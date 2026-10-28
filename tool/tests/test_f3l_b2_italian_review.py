"""Regression and negative-path tests: 112 Italian candidate descriptions, zero approvals."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from f3l_b2_italian_review import (
    EXPECTED_SOURCE_SHA, OBSERVED_REVIEW_LEADS, PARTS, PROPOSALS_DIR,
    build, load_proposals,
)
from f3l_translation_gate import digest


class F3LB2ItalianReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            Path("authoring/f3k_it_hardening_51_162.json").read_text(encoding="utf-8")
        )
        cls.proposals = load_proposals()

    def test_source_bound_112_unique_candidates_no_fake_approval(self):
        self.assertEqual(digest(self.source), EXPECTED_SOURCE_SHA)
        self.assertEqual(len(self.proposals), 112)
        self.assertEqual(list(self.proposals), [
            f"recipe_{n:06d}" for n in range(51, 163)
        ])
        report = build(self.source, self.proposals)
        self.assertEqual(report["sourceRecipeCount"], 112)
        self.assertEqual(report["descriptionProposalCount"], 112)
        self.assertEqual(report["observedSourceLeads"], len(OBSERVED_REVIEW_LEADS))
        self.assertEqual(report["italianReusableComponentCount"], 10)
        self.assertEqual(len(report["italianReusableComponents"]), 10)
        self.assertEqual(report["humanEditorialSignoffs"], 0)
        self.assertFalse(report["canonicalSourceModified"])
        self.assertFalse(report["releaseApproved"])
        self.assertFalse(report["sourceApprovedForPromotion"])
        self.assertTrue(report["noAutomaticPublication"])
        self.assertEqual(report["machineDraftLocalesUnaffected"],
                         ["en", "es", "fr", "de", "pt"])
        self.assertTrue(all(r["reviewEvidence"] is None and
                            r["status"].startswith("PENDING_")
                            for r in report["recipes"]))
        for source, packet in zip(self.source["recipes"], report["recipes"]):
            self.assertEqual(packet["stepsIT"], source["steps"])
            self.assertEqual(packet["ingredientsIT"], source["ingredients"])
            self.assertEqual(packet["times"], source["times"])
            self.assertEqual(packet["servings"], source["servings"])
            self.assertEqual(packet["animeReviewSource"], source["animeReview"])
            self.assertEqual(packet["equipmentIT"], source.get("equipment", []))
        self.assertTrue(all(c["reviewEvidence"] is None and
                            c["status"].startswith("PENDING_")
                            for c in report["italianReusableComponents"]))

    def test_observed_finding_excerpts_are_verbatim_from_source(self):
        report = build(self.source, self.proposals)
        by_id = {r["recipeId"]: r for r in report["recipes"]}
        for n, (kind, _) in OBSERVED_REVIEW_LEADS.items():
            with self.subTest(recipe=n):
                candidate = by_id[f"recipe_{n:06d}"]
                issues = [x for x in candidate["findingsRequiringReview"]
                          if x["kind"] == kind]
                self.assertEqual(len(issues), 1)
                self.assertTrue(issues[0]["excerpt"])

    def test_source_change_relocks_all_112_proposals(self):
        source = copy.deepcopy(self.source)
        source["recipes"][0]["description"] += " fonte mutata"
        with self.assertRaisesRegex(ValueError, "source changed"):
            build(source, self.proposals)

    def test_no_missing_or_duplicate_or_fake_approved_proposals(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for start, end in PARTS:
                name = f"{start:03d}_{end:03d}.json"
                part = json.loads((PROPOSALS_DIR / name).read_text(encoding="utf-8"))
                if start == 51:
                    part["proposals"][0]["reviewStatus"] = "human_reviewed"
                (folder / name).write_text(
                    json.dumps(part, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must not claim approval"):
                load_proposals(folder)
            part = json.loads((PROPOSALS_DIR / "051_078.json").read_text(encoding="utf-8"))
            part["proposals"].pop(2)
            (folder / "051_078.json").write_text(json.dumps(part), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete"):
                load_proposals(folder)

    def test_missing_recipe_candidate_is_rejected(self):
        shorter = dict(self.proposals)
        shorter.pop("recipe_000088")
        with self.assertRaisesRegex(ValueError, "proposal IDs"):
            build(self.source, shorter)


if __name__ == "__main__":
    unittest.main()

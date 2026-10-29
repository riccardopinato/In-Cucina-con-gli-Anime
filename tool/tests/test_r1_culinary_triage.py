"""R1 source triage: exact source, source-grounded evidence, 122 pending items."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from r1_culinary_triage import (
    EXPECTED_COMPONENTS, LEADS, RECIPE_IDS, SOURCE_SHA, build, evidence
)
from f3l_translation_gate import digest


class R1CulinaryTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            Path("authoring/f3k_it_hardening_51_162.json").read_text(encoding="utf-8")
        )

    def test_all_entities_pending_with_witnessed_findings(self):
        report = build(self.source)
        self.assertEqual(report["sourceCatalogSha256"], SOURCE_SHA)
        self.assertEqual(report["coverage"], {
            "recipes": 112, "components": 10, "priorityReviewLeads": 12,
            "unreviewedEntities": 122,
        })
        self.assertEqual([x["id"] for x in report["recipes"]], RECIPE_IDS)
        self.assertEqual({x["id"] for x in report["components"]}, EXPECTED_COMPONENTS)
        self.assertTrue(report["stagingOnly"])
        self.assertTrue(report["noAutomaticPublication"])
        self.assertFalse(report["releaseApproved"])
        self.assertFalse(report["sourceModified"])
        self.assertEqual(report["humanSignoffs"], 0)
        self.assertTrue(all(x["humanDecisionEvidence"] is None for x in
                            report["priorityCandidates"] + report["recipes"] + report["components"]))
        self.assertTrue(all(x["status"].startswith("PENDING_") for x in
                            report["priorityCandidates"] + report["recipes"] + report["components"]))
        self.assertEqual([x["findingId"] for x in report["priorityCandidates"]],
                         [row[0] for row in LEADS])
        entities = {x["id"]: x for x in self.source["recipes"]}
        entities.update(self.source["reusableComponents"])
        for finding in report["priorityCandidates"]:
            entity = entities[finding["entityId"]]
            ev = finding["sourceEvidence"]
            self.assertTrue(ev["verbatim"])
            self.assertIn(ev, [evidence(entity, row[3]) for row in LEADS
                               if row[2] == finding["entityId"]])
        self.assertEqual(digest(self.source), SOURCE_SHA)

    def test_component_dependency_edges_unchanged(self):
        report = build(self.source)
        r = next(x for x in report["recipes"] if x["id"] == "recipe_000051")
        self.assertEqual(r["componentDependencies"],
                         ["component_ajitama", "component_chashu", "component_dashi"])
        self.assertIn("R1-005", r["priorityFindings"])

    def test_stale_source_and_quarantine_change_fail_closed(self):
        mutated = copy.deepcopy(self.source)
        mutated["recipes"][0]["description"] += " changed"
        with self.assertRaisesRegex(ValueError, "fingerprint drift"):
            build(mutated)
        mutated = copy.deepcopy(self.source)
        mutated["translationPolicy"]["status"] = "APPROVED"
        with self.assertRaisesRegex(ValueError, "fingerprint drift"):
            build(mutated)

    def test_bad_evidence_needle_is_rejected(self):
        recipe = self.source["recipes"][5]
        with self.assertRaisesRegex(ValueError, "Missing witnessed source phrase"):
            evidence(recipe, "THIS TEXT IS NOT PRESENT IN THE SOURCE")

    def test_no_mutation_of_source_by_triage(self):
        before = json.dumps(self.source, sort_keys=True, ensure_ascii=False)
        build(self.source)
        self.assertEqual(json.dumps(self.source, sort_keys=True, ensure_ascii=False), before)


if __name__ == "__main__":
    unittest.main()

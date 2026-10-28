"""F3L editorial repair must preserve 560 draft records and block release."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_semantic_safety_gate import check,load,EXPECTED_SOURCE,LOCALES
from f3l_translation_gate import digest,inspect

class EditorialRepairTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.source,cls.packs=load(Path(__file__).resolve().parents[2])
 def test_exact_source_and_no_witnessed_errors(self):
  self.assertEqual(digest(self.source),EXPECTED_SOURCE)
  self.assertEqual(check(self.source,self.packs),[])
 def test_five_complete_packs_not_approved(self):
  for loc in LOCALES:
   with self.subTest(loc=loc):
    p=self.packs[loc]
    self.assertEqual(len(p["recipes"]),112)
    self.assertEqual(sum(len(r["steps"]) for r in p["recipes"]),900)
    self.assertEqual(sum(len(r["ingredients"]) for r in p["recipes"]),936)
    self.assertEqual(len(p["reusableComponents"]),10)
    self.assertEqual(inspect(self.source,p),[])
    self.assertTrue(p["editorialStaging"]["noAutomaticPublication"])
    self.assertEqual(p["reviewStatus"],"machine_draft_not_publishable")
    self.assertTrue(any("human editorial review missing" in e for e in inspect(self.source,p,require_review=True)))
 def test_detect_regressed_mistranslation(self):
  p=copy.deepcopy(self.packs)
  p["fr"]["recipes"][0]["steps"][0]["instruction"]="Préparez les joints."
  self.assertTrue(any("witnessed false friend" in e for e in check(self.source,p)))
 def test_source_change_fails_closed(self):
  other=copy.deepcopy(self.source)
  other["recipes"][0]["steps"][0]["instruction"]+=" Riscrittura."
  self.assertTrue(any("fingerprint drift" in e for e in check(other,self.packs)))

if __name__=="__main__":unittest.main()

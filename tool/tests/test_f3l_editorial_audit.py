"""Regression coverage for F3L editorial non-certification."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_editorial_audit import audit
from test_f3l_translation_gate import data

class EditorialAuditTest(unittest.TestCase):
    def test_structural_pass_is_not_editorial_approval(self):
        source,pack=data()
        report=audit(source,pack)
        self.assertEqual(report['structuralErrorCount'],0)
        self.assertFalse(report['releaseApproved'])
        self.assertEqual(report['unreviewedCount'],112)
    def test_catches_italian_title_bleed(self):
        source,pack=data()
        pack['recipes'][0]['title']='Shio Ramen al Sale con Chashu'
        report=audit(source,pack)
        self.assertIn('untranslated_italian_title_fragment',report['warningReasons'])
    def test_catches_culinary_semantic_corruption(self):
        source,pack=data()
        pack['locale']='de'
        pack['recipes'][0]['steps'][0]['instruction']='Legen Sie alles in den Kupfer.'
        report=audit(source,pack)
        self.assertIn('witnessed_semantic_mistranslation',report['warningReasons'])

if __name__=='__main__':unittest.main()
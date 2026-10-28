import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_witnessed_wording_repairs import apply
from f3l_review_report import normalized_numbers
ROOT=Path(__file__).resolve().parents[2]
class WordingsTests(unittest.TestCase):
 def test_attached_units_are_whole_numbers(self):
  self.assertEqual(normalized_numbers('400ml e 20g'),['400','20'])
 def test_spelled_out_numbers_equal_digits(self):
  self.assertIn('2',normalized_numbers('durante dos minutos','es'))
  self.assertIn('8',normalized_numbers('en huit portions','fr'))
 def test_glossary_fix_keeps_source_identity(self):
  source=json.loads((ROOT/'authoring/f3k_it_hardening_51_162.json').read_text())
  p=json.loads((ROOT/'authoring/f3l_review_drafts/f3l_de_51_162_review_draft.json').read_text())
  p['recipes'][0]['ingredients'][0]['name']='Nudeln für Kupfer'
  count=apply(source,p)
  self.assertGreaterEqual(count,1)
  self.assertEqual(p['recipes'][0]['ingredients'][0]['name'],'Ramen-Nudeln')
  self.assertEqual(p['sourceLocale'],'it')
if __name__=='__main__':unittest.main()
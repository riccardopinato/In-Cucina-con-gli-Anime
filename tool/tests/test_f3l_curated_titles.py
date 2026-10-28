import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_curated_titles import titles, apply_titles
SRC=Path(__file__).resolve().parents[2]/'authoring/f3k_it_hardening_51_162.json'
class TitleReviewTests(unittest.TestCase):
 def test_exact_112_titles_per_locale(self):
  m=titles();self.assertEqual(set(m),set(('en','es','fr','de','pt')))
  for l,rows in m.items():
   with self.subTest(l=l):self.assertEqual(len(rows),112)
 def test_source_changed_invalidates_title_copyedit(self):
  src=json.loads(SRC.read_text(encoding='utf-8'))
  pack={'locale':'en','sourceBaselineSha256':'invalid','recipes':[]}
  with self.assertRaises(ValueError):apply_titles(src,pack)
if __name__=='__main__':unittest.main()
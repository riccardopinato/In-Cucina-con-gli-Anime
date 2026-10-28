import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_check_review_drafts import check
ROOT=Path(__file__).resolve().parents[2]
class PackIntegrationTests(unittest.TestCase):
 def test_all_five_quarantined_packs_structurally_valid(self):
  source=json.loads((ROOT/'authoring/f3k_it_hardening_51_162.json').read_text(encoding='utf-8'))
  result=check(source,ROOT/'authoring/f3l_review_drafts')
  self.assertEqual(len(result),5)
  self.assertTrue(all(not row['releaseApproved'] for row in result))
 def test_release_gate_rejects_unreviewed_candidates(self):
  source=json.loads((ROOT/'authoring/f3k_it_hardening_51_162.json').read_text(encoding='utf-8'))
  with self.assertRaisesRegex(ValueError,'human editorial review missing'):
   check(source,ROOT/'authoring/f3l_review_drafts',strict_release=True)
if __name__=='__main__':unittest.main()
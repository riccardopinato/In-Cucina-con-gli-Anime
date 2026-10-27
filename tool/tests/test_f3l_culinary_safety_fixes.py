import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_culinary_safety_fixes import apply
SRC=Path(__file__).resolve().parents[2]/'authoring/f3k_it_hardening_51_162.json'
class SafetyFixTests(unittest.TestCase):
 def test_preserves_canonical_id_and_step_structure(self):
  s=json.loads(SRC.read_text())
  for l in ('en','es','fr','de','pt'):
   for rid in (53,59,107,150):
    src=s['recipes'][rid-51]
    candidate={'id':src['id'],'ingredients':[dict(i) for i in src['ingredients']],'steps':[dict(x) for x in src['steps']],'title':src['title'],'description':src['description']}
    apply(src,candidate,l)
    self.assertEqual([v['id'] for v in src['ingredients']],[v['id'] for v in candidate['ingredients']])
    self.assertEqual([v['id'] for v in src['steps']],[v['id'] for v in candidate['steps']])
    self.assertEqual([v['timerSeconds'] for v in src['steps']],[v['timerSeconds'] for v in candidate['steps']])
if __name__=='__main__':unittest.main()
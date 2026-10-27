import json,sys,unittest,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_curated_components import COPY,apply
from f3l_translation_gate import inspect,digest
ROOT=Path(__file__).resolve().parents[2]
class ComponentCopyeditTests(unittest.TestCase):
 def test_full_component_translation_preserves_steps_quantities_and_references(self):
  source=json.loads((ROOT/'authoring/f3k_it_hardening_51_162.json').read_text())
  for l in ('en','es','fr','de','pt'):
   with self.subTest(l=l):
    pack=json.loads((ROOT/f'authoring/f3l_review_drafts/f3l_{l}_51_162_review_draft.json').read_text())
    src_c=source['reusableComponents']
    before=copy.deepcopy(pack['reusableComponents'])
    apply(source,pack)
    self.assertEqual(len(pack['reusableComponents']),10)
    for id,a in src_c.items():
     b=pack['reusableComponents'][id]
     self.assertEqual(a.get('recipeRef'),b.get('recipeRef'))
     self.assertEqual([v.get('quantity') for v in a.get('ingredients',[])],[v.get('quantity') for v in b.get('ingredients',[])])
     self.assertEqual(len(a.get('steps',[])),len(b.get('steps',[])))
    self.assertEqual(inspect(source,pack),[])
 def test_rejects_changed_source(self):
  source=json.loads((ROOT/'authoring/f3k_it_hardening_51_162.json').read_text())
  pack=json.loads((ROOT/'authoring/f3l_review_drafts/f3l_en_51_162_review_draft.json').read_text())
  source['reusableComponents']['component_chashu']['steps'][0]+=' revised'
  with self.assertRaisesRegex(ValueError,'source changed'):apply(source,pack)
if __name__=='__main__':unittest.main()
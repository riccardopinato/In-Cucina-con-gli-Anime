"""Protect the specific human-written French Kuri Manju translation repair."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from f3l_french_recipe_159 import apply_french_recipe_159, DESCRIPTION, INGREDIENT_NAMES, STEPS

SOURCE_FILE = Path(__file__).resolve().parents[2] / 'authoring' / 'f3k_it_hardening_51_162.json'


class FrenchRecipe159Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = json.loads(SOURCE_FILE.read_text(encoding='utf-8'))
        cls.recipe = next(r for r in src['recipes'] if r['id']=='recipe_000159')

    def test_full_nine_step_revision_keeps_canonical_content(self):
        r=copy.deepcopy(self.recipe)
        candidate={
            'id':r['id'],
            'ingredients':[{'id':i['id'],'quantity':i['quantity'],'unit':i['unit'],'amountMode':i['amountMode']} for i in r['ingredients']],
            'steps':[{'id':s['id'],'timerSeconds':s['timerSeconds'],'instruction':'Untranslated placeholder'} for s in r['steps']],
            'reviewStatus':'machine_draft',
        }
        before=copy.deepcopy(candidate)
        fixed=apply_french_recipe_159(r,candidate)
        self.assertEqual(len(fixed['steps']),9)
        self.assertEqual([s['instruction'] for s in fixed['steps']],[STEPS[s['id']] for s in r['steps']])
        self.assertEqual([i['name'] for i in fixed['ingredients']],[INGREDIENT_NAMES[i['id']] for i in r['ingredients']])
        self.assertIn('châtaigne',DESCRIPTION)
        for original,modified in zip(before['ingredients'],fixed['ingredients']):
            for key in ('id','quantity','unit','amountMode'): self.assertEqual(original[key],modified[key])
        for original,modified in zip(before['steps'],fixed['steps']):
            for key in ('id','timerSeconds'): self.assertEqual(original[key],modified[key])
        self.assertEqual(fixed['reviewStatus'],'machine_draft')

    def test_italian_change_invalidates_rewrite(self):
        bad=copy.deepcopy(self.recipe)
        bad['steps'][6]['instruction']='Changed source instruction'
        with self.assertRaisesRegex(ValueError,'source recipe_000159 changed'):
            apply_french_recipe_159(bad,{'id':bad['id']})

    def test_another_recipe_cannot_receive_rewrite(self):
        with self.assertRaisesRegex(ValueError,'only for recipe_000159'):
            apply_french_recipe_159({'id':'recipe_000160'},{'id':'recipe_000160'})

if __name__=='__main__': unittest.main()
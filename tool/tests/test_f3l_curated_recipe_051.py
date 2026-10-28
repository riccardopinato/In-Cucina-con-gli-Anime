import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_curated_recipe_051 import COPY, apply
from f3l_translation_gate import digest

SOURCE=Path(__file__).resolve().parents[2]/'authoring/f3k_it_hardening_51_162.json'
class Curated051Test(unittest.TestCase):
    def test_locales_source_locked_and_cardinality(self):
        source=json.loads(SOURCE.read_text())['recipes'][0]
        for locale in COPY:
            with self.subTest(locale=locale):
                candidate={'id':source['id'],'ingredients':[{'id':i['id'],'name':i['name']} for i in source['ingredients']], 'steps':[{'id':s['id'],'instruction':s['instruction']} for s in source['steps']]}
                fixed=apply(source,candidate,locale)
                self.assertEqual(len(fixed['ingredients']),len(source['ingredients']))
                self.assertEqual(len(fixed['steps']),len(source['steps']))
                self.assertTrue(all(s['instruction']!=r['instruction'] for s,r in zip(fixed['steps'],source['steps'])))
    def test_source_drift_fails_closed(self):
        source=json.loads(SOURCE.read_text())['recipes'][0]
        candidate={'id':source['id'],'ingredients':[{'id':i['id'],'name':i['name']} for i in source['ingredients']], 'steps':[{'id':s['id'],'instruction':s['instruction']} for s in source['steps']]}
        source['steps'][0]['instruction']+=' change'
        with self.assertRaisesRegex(ValueError,'source changed'):apply(source,candidate,'en')
if __name__=='__main__':unittest.main()
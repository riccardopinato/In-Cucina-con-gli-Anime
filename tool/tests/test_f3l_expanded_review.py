"""Regression checks for F3L edits without inventing native sign-off."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_expanded_review import apply,SOURCE_SHA
from f3l_translation_gate import digest,inspect
from f3l_editorial_audit import audit

ROOT=Path(__file__).resolve().parents[2]
class ExpandedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads((ROOT/'authoring/f3k_it_hardening_51_162.json').read_text(encoding='utf-8'))
    def pack(self,l):
        return json.loads((ROOT/'authoring/f3l_review_drafts'/f'f3l_{l}_51_162_review_draft.json').read_text(encoding='utf-8'))
    def test_persisted_five_locale_structure_and_non_publication(self):
        self.assertEqual(digest(self.source),SOURCE_SHA)
        for l in ('en','es','fr','de','pt'):
            p=self.pack(l)
            self.assertEqual(inspect(self.source,p),[])
            self.assertEqual(audit(self.source,p)['warningCount'],0)
            self.assertTrue(p['editorialStaging']['noAutomaticPublication'])
            self.assertGreater(p['editorialStaging']['expandedReviewFieldEdits'],0)
            self.assertTrue(all(r['reviewStatus']=='machine_draft' and not r['reviewEvidence'] for r in p['recipes']))
    def test_edit_is_idempotent(self):
        for l in ('en','es','fr','de','pt'):
            p=self.pack(l);before=json.dumps(p,ensure_ascii=False,sort_keys=True)
            edits=apply(self.source,p)
            self.assertEqual(edits['editCount'],0,l)
            self.assertEqual(json.dumps(p,ensure_ascii=False,sort_keys=True),before,l)
    def test_italian_source_change_fails_closed(self):
        changed=copy.deepcopy(self.source)
        changed['recipes'][0]['steps'][0]['instruction']+=' Correzione.'
        with self.assertRaisesRegex(ValueError,'fingerprint'):
            apply(changed,self.pack('fr'))
    def test_rice_cooker_erratum_rendering_keeps_units(self):
        for l in ('en','es','fr','de','pt'):
            s=next(r for r in self.pack(l)['recipes'] if r['id']=='recipe_000089')['steps'][1]['instruction']
            self.assertIn('280',s);self.assertIn('15',s)
            self.assertNotIn('cuocereriso',s)
    def test_source_culinary_terms_retained_and_false_friends_removed(self):
        en=self.pack('en');en137=next(r for r in en['recipes'] if r['id']=='recipe_000137')
        self.assertIn('stir-fry',en137['steps'][4]['instruction'])
        fr=self.pack('fr');fr110=next(r for r in fr['recipes'] if r['id']=='recipe_000110')
        self.assertIn('dashi',fr110['steps'][2]['instruction'])
        de=self.pack('de');de136=next(r for r in de['recipes'] if r['id']=='recipe_000136')
        self.assertIn('Miso',de136['ingredients'][1]['name'])
        pt=self.pack('pt');pt055=next(r for r in pt['recipes'] if r['id']=='recipe_000055')
        self.assertIn('concha',pt055['steps'][2]['instruction'])
    def test_release_is_explicitly_blocked(self):
        for l in ('en','es','fr','de','pt'):
            p=self.pack(l)
            self.assertTrue(any('human editorial review missing' in issue for issue in inspect(self.source,p,require_review=True)))

if __name__=='__main__':unittest.main()
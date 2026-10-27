"""Negative-path regression tests for F3L translation invariants."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from f3l_translation_gate import inspect,digest


def data():
    recipes=[]
    for n in range(51,163):
        recipes.append({"id":f"recipe_{n:06d}","targetContentVersion":2,"servings":2,"difficulty":"easy","times":{"prepMinutes":5,"totalElapsedMinutes":20,"note":"La durata comprende le attese."},"ingredients":[{"id":"rice","name":"riso da sushi bianco ben lavato e scolato","note":None,"quantity":100,"unit":"g","amountMode":"measured"}],"steps":[{"id":"step_1","instruction":"Cuoci il riso per dieci minuti mescolando e lascia riposare coperto.","timerSeconds":600}]})
    src={"count":112,"recipes":recipes,"reusableComponents":{}}
    pack={"locale":"en","sourceLocale":"it","sourceBaselineSha256":digest(src),"reusableComponents":{},"recipes":[{"id":r["id"],"sourceRecipeSha256":digest(r),"sourceContentVersion":2,"reviewStatus":"machine_draft","title":"Sushi rice","description":"A complete recipe for a simple Japanese rice dish.","animeContext":"The dish is thematically inspired by works of fiction.","servings":2,"difficulty":"easy","times":{**r["times"],"note":"Total duration includes the waiting time."},"ingredients":[{"id":"rice","name":"washed and drained white sushi rice","note":None,"quantity":100,"unit":"g","amountMode":"measured","amountText":"100 g"}],"steps":[{"id":"step_1","instruction":"Cook the rice for ten minutes, stirring, then let it rest covered.","timerSeconds":600}]} for r in recipes]}
    return src,pack

class GateTest(unittest.TestCase):
    def test_draft_can_be_structurally_valid(self):
        s,p=data();self.assertEqual(inspect(s,p),[])
    def test_unreviewed_draft_cannot_be_released(self):
        s,p=data();self.assertIn("human editorial review missing"," ".join(inspect(s,p,require_review=True)))
    def test_step_is_never_collapsed(self):
        s,p=data();p["recipes"][7]["steps"]=[];self.assertIn("steps collapsed"," ".join(inspect(s,p)))
    def test_canonical_quantity_is_not_translated(self):
        s,p=data();p["recipes"][0]["ingredients"][0]["quantity"]=200;self.assertIn("canonical quantity changed"," ".join(inspect(s,p)))
    def test_source_fingerprint_invalidates_old_translations(self):
        s,p=data();s["recipes"][0]["steps"][0]["instruction"]+=" Correzione.";self.assertIn("baseline fingerprint mismatch"," ".join(inspect(s,p)))
    def test_subrecipes_cannot_be_omitted(self):
        s,p=data();s["reusableComponents"]={"component_test":{"title":"brodo","servings":1,"totalElapsedMinutes":25,"ingredients":[],"steps":["Bolli per 20 minuti."]}}
        p["sourceBaselineSha256"]=digest(s)
        self.assertIn("Reusable component IDs differ", " ".join(inspect(s,p)))
    def test_component_reference_must_be_preserved(self):
        s,p=data()
        s["reusableComponents"]={"component_ref":{"title":"curry di base","recipeRef":"recipe_000013"}}
        p["sourceBaselineSha256"]=digest(s)
        p["reusableComponents"]={"component_ref":{"title":"Base curry","recipeRef":"recipe_000019"}}
        self.assertIn("canonical recipeRef mismatch"," ".join(inspect(s,p)))
    def test_boilerplate_rejected(self):
        s,p=data();p["recipes"][0]["steps"][0]["instruction"]="cook the main component";self.assertIn("filler"," ".join(inspect(s,p)))

if __name__=="__main__":unittest.main()
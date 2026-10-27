#!/usr/bin/env python3
"""Generate never-publishable 1:1 MarianMT draft translations from frozen F3K Italian.

Requires transformers, torch and sentencepiece at AUTHORING time only. Downloads
Apache-2.0 model weights only in the CI environment. All output is review-required.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

from f3l_translation_gate import digest, inspect, source_recipes

MODEL_MAP = {
    "en": ("Helsinki-NLP/opus-mt-it-en",),
    "es": ("Helsinki-NLP/opus-mt-it-es",),
    "fr": ("Helsinki-NLP/opus-mt-it-fr",),
    "de": ("Helsinki-NLP/opus-mt-it-de",),
    "pt": ("Helsinki-NLP/opus-mt-it-en", "Helsinki-NLP/opus-mt-en-ROMANCE"),
}
# Preserve identity, avoid hallucinated canonical appearances.
ANIME_CONTEXT = {
    "en": "This recipe is thematically inspired by {names}. These are editorial associations, not claims of appearances in specific episodes or chapters.",
    "es": "Esta receta está inspirada temáticamente en {names}. Son asociaciones editoriales, no afirmaciones de apariciones en episodios o capítulos concretos.",
    "fr": "Cette recette s'inspire librement de {names}. Il s'agit de rapprochements éditoriaux, et non d'affirmations sur une apparition dans un épisode ou un chapitre précis.",
    "de": "Dieses Rezept ist thematisch von {names} inspiriert. Es handelt sich um redaktionelle Bezüge, nicht um Behauptungen über Auftritte in bestimmten Folgen oder Kapiteln.",
    "pt": "Esta receita inspira-se tematicamente em {names}. São associações editoriais, não alegações de aparições em episódios ou capítulos específicos.",
}
ELAPSED_NOTE = {
    "en": "Total elapsed time includes the resting, proofing, marinating, cooling or freezing steps explicitly described in the method.",
    "es": "El tiempo total incluye los reposos, las fermentaciones, los marinados, el enfriamiento o la congelación indicados en la preparación.",
    "fr": "La durée totale comprend les temps de repos, de levée, de marinade, de refroidissement ou de congélation indiqués dans la préparation.",
    "de": "Die Gesamtzeit umfasst die im Rezept angegebenen Ruhe-, Geh-, Marinier-, Abkühl- oder Gefrierzeiten.",
    "pt": "O tempo total inclui os períodos de repouso, levedação, marinada, arrefecimento ou congelação indicados no modo de preparação.",
}
TO_TASTE = {"en":"to taste", "es":"al gusto", "fr":"selon le goût", "de":"nach Geschmack", "pt":"a gosto"}
UNITS = {
    "portion":{"en":("serving","servings"),"es":("ración","raciones"),"fr":("portion","portions"),"de":("Portion","Portionen"),"pt":("porção","porções")},
    "piece":{"en":("piece","pieces"),"es":("unidad","unidades"),"fr":("pièce","pièces"),"de":("Stück","Stück"),"pt":("unidade","unidades")},
    "slice":{"en":("slice","slices"),"es":("loncha","lonchas"),"fr":("tranche","tranches"),"de":("Scheibe","Scheiben"),"pt":("fatia","fatias")},
    "tbsp":{"en":("tbsp","tbsp"),"es":("cda.","cdas."),"fr":("c. à soupe","c. à soupe"),"de":("EL","EL"),"pt":("colher de sopa","colheres de sopa")},
    "tsp":{"en":("tsp","tsp"),"es":("cdta.","cdtas."),"fr":("c. à café","c. à café"),"de":("TL","TL"),"pt":("colher de chá","colheres de chá")}
}

def amounts(ingredient, locale):
    if ingredient.get("amountMode") == "q.b.": return TO_TASTE[locale]
    q = ingredient.get("quantity")
    if q is None: return TO_TASTE[locale]
    n = f"{q:g}" if isinstance(q,(int,float)) else str(q)
    unit=ingredient.get("unit")
    if not unit: return n
    table=UNITS.get(unit,{}).get(locale)
    if table:
        singular,plural=table
        return f"{n} {singular if q==1 else plural}"
    if unit in ("g","kg","ml","l","cm"):
        return f"{n} {unit}"
    return f"{n} {unit}"  # Unknown unit: preserve, never invent.


def translate_all(texts, model_name, *, batch_size, max_length, prefix=""):
    from transformers import MarianMTModel, MarianTokenizer
    import torch
    torch.set_num_threads(2)
    tokenizer=MarianTokenizer.from_pretrained(model_name)
    model=MarianMTModel.from_pretrained(model_name).eval()
    unique=list(dict.fromkeys(t.strip() for t in texts if isinstance(t,str) and t.strip()))
    result={}
    for i in range(0,len(unique),batch_size):
        batch=unique[i:i+batch_size]
        # Check for truncation rather than silently chopping real cooking instructions.
        enc=tokenizer([prefix + text for text in batch],return_tensors="pt",padding=True,truncation=False)
        if enc["input_ids"].shape[1] > max_length:
            raise ValueError(f"Source token overflow: {enc['input_ids'].shape[1]} > {max_length}; split explicitly")
        with torch.no_grad():
            target=model.generate(**enc,num_beams=3,max_new_tokens=max_length+32)
        decoded=tokenizer.batch_decode(target,skip_special_tokens=True)
        for old,new in zip(batch,decoded):
            if not new.strip(): raise ValueError(f"Empty MT output for {old[:60]!r}")
            result[old]=new.strip()
        if i%200==0 or i+batch_size>=len(unique): print(f"model={model_name} translated {min(i+batch_size,len(unique))}/{len(unique)}",flush=True)
    del model
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--locale",choices=MODEL_MAP,required=True)
    ap.add_argument("--source",default="authoring/f3k_it_hardening_51_162.json")
    ap.add_argument("--output",required=True)
    ap.add_argument("--batch-size",type=int,default=12)
    ap.add_argument("--max-length",type=int,default=256)
    ns=ap.parse_args()
    source=json.loads(Path(ns.source).read_text(encoding="utf-8"))
    rows=source_recipes(source)
    texts=[]
    for component in source["reusableComponents"].values():
        texts.append(component["title"])
        texts += [i["name"] for i in component.get("ingredients",[])]
        texts += list(component.get("steps",[]))
    for r in rows:
        texts += [r["title"],r["description"]]
        texts += [i["name"] for i in r["ingredients"]]
        texts += [i["note"] for i in r["ingredients"] if i.get("note")]
        texts += [s["instruction"] for s in r["steps"]]
        texts += [e for e in r.get("equipment",[]) if isinstance(e,str)]
    translated=None
    for model_index, model in enumerate(MODEL_MAP[ns.locale]):
        prefix = ">>pt_BR<< " if ns.locale == "pt" and model_index == 1 else ""
        output=translate_all(texts if translated is None else translated.values(),model,batch_size=ns.batch_size,max_length=ns.max_length,prefix=prefix)
        translated=output if translated is None else {src:output[target] for src,target in translated.items()}
    def t(s):return translated[s.strip()] if isinstance(s,str) and s.strip() else s
    components={}
    for comp_id, comp in source["reusableComponents"].items():
        components[comp_id]={
            "title":t(comp["title"]),
            **({"recipeRef":comp["recipeRef"]} if "recipeRef" in comp else {}),
            **({"servings":comp["servings"]} if "servings" in comp else {}),
            **({"totalElapsedMinutes":comp["totalElapsedMinutes"]} if "totalElapsedMinutes" in comp else {}),
            **({"ingredients":[{"name":t(i["name"]),"quantity":i.get("quantity"),"unit":i.get("unit")}
                             for i in comp["ingredients"]]} if "ingredients" in comp else {}),
            **({"steps":[t(x) for x in comp["steps"]]} if "steps" in comp else {}),
        }
    output=[]
    for r in rows:
        names=", ".join(x["workTitle"] for x in r.get("animeReview",{}).get("references",[]))
        out={
            "id":r["id"], "sourceRecipeSha256":digest(r), "sourceContentVersion":r["targetContentVersion"],
            "reviewStatus":"machine_draft", "reviewEvidence":None,
            "title":t(r["title"]), "description":t(r["description"]),
            "animeContext":ANIME_CONTEXT[ns.locale].format(names=names),
            "servings":r["servings"],"difficulty":r["difficulty"],
            "times":{**r["times"],"note":ELAPSED_NOTE[ns.locale]},
            "equipment":[t(e) for e in r.get("equipment",[])],
            "ingredients":[{
                "id":i["id"],"name":t(i["name"]),"note":t(i.get("note")),
                "quantity":i.get("quantity"),"unit":i.get("unit"),"amountMode":i.get("amountMode"),
                "amountText":amounts(i,ns.locale),"componentRef":i.get("componentRef")
            } for i in r["ingredients"]],
            "steps":[{"id":s["id"],"instruction":t(s["instruction"]),"timerSeconds":s.get("timerSeconds")} for s in r["steps"]]
        }
        output.append(out)
    pack={"schemaVersion":1,"phase":"F3L_TRANSLATIONS","locale":ns.locale,"sourceLocale":"it",
          "sourceBaselineSha256":digest(source),"modelChain":list(MODEL_MAP[ns.locale]),
          "copyrightPolicy":"Apache-2.0 MT model weights; translation candidates need editorial QA",
          "reviewStatus":"machine_draft_not_publishable","recipeCount":112,"reusableComponentCount":len(components),
          "reusableComponents":components,"recipes":output}
    issues=inspect(source,pack)
    path=Path(ns.output); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"F3L {ns.locale}: {len(output)}/112, structural issues={len(issues)}, HUMAN_REVIEW_PENDING",flush=True)
    for issue in issues[:20]:print("ERROR",issue,flush=True)
    if issues:raise SystemExit(1)

if __name__=="__main__":main()
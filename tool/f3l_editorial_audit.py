#!/usr/bin/env python3
"""Conservative editorial QA for five F3L draft locales.

This is a triage report, NOT a human language/cuisine certification. It checks
fidelity risks that 1:1 schema validation cannot see. Never auto-approve drafts.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
import re
from pathlib import Path

from f3l_translation_gate import digest, inspect, source_recipes
from f3l_review_report import inspect_copy

# Each of these is a witnessed bad output, not a heuristic assumption that a
# legitimate culinary term never appears in another language.
WITNESSED_MISTRANSLATIONS = {
    'en': (r'\b(?:Sexam|Ginger Pig Lumbat|dust dashes|Black Sexam|jump|spatolines|candy slightly)\b',),
    'es': (r'\b(?:Temporada de Gambas|en el diente|zuca|Lombarda de Cerdo|únete|acaricia|pañuelo|dispar(?:e|en|a|o))\b',),
    'fr': (r'\b(?:pangratté|Escolez|Miso Nikumi|Strufato|Couette cruciforme|man et porc|écoutez|taureau|cuisinier|surbouches)\b',),
    'de': (r'\b(?:Kupfer|Krebshomelette|Bierhefe|Vogel zum Vapore|Manzo|Sexam|streicheln|Peitsche|Mist)\b',),
    'pt': (r'\b(?:lagartos frescos|traço de poeira|Sexam|Lumbat|macarrãoes|pule|colchão)\b',),
}
# Italian fragments unsuitable as translated display titles. Some words can be
# legitimate in Italian, but these are only applied to non-Italian locales.
ITALIAN_IN_TITLES = (
    r'\b(?:al Sale|con Chashu|di Gamberi|Panino|Croccante|Cottoletta|Sofficissimo|Stufati|Vongole|Zenzero|Agrodolce|Salsa Tentsuyu|al Vapore|Macinata|Fritto|al Sesamo|al Formaggio|al Burro)\b',
)


def audit(source: dict, pack: dict) -> dict:
    locale=pack.get('locale')
    structural=inspect(source,pack)
    warnings=[]
    rows=source_recipes(source)
    targeted={r['id']:r for r in rows}
    for issue in inspect_copy(source,pack):
        warnings.append({**issue,'origin':'source_vs_translation'})
    for translated in pack.get('recipes',[]):
        rid=translated.get('id')
        if rid not in targeted: continue
        for field,value in [('title',translated.get('title','')),('description',translated.get('description',''))]:
            if not isinstance(value,str): continue
            for expr in WITNESSED_MISTRANSLATIONS.get(locale,()):
                if m:=re.search(expr,value,re.I):
                    warnings.append({'severity':'high','recipe':rid,'field':field,'reason':'witnessed_semantic_mistranslation','excerpt':m.group()})
            if field=='title':
                for expr in ITALIAN_IN_TITLES:
                    if m:=re.search(expr,value,re.I):
                        if locale=='es' and m.group().lower() in ('con chashu','salsa tentsuyu'):
                            continue  # Both are grammatical Spanish culinary phrases.
                        warnings.append({'severity':'medium','recipe':rid,'field':field,'reason':'untranslated_italian_title_fragment','excerpt':m.group()})
        for index,step in enumerate(translated.get('steps',[]),1):
            text=step.get('instruction','')
            for expr in WITNESSED_MISTRANSLATIONS.get(locale,()):
                if m:=re.search(expr,text,re.I):
                    warnings.append({'severity':'high','recipe':rid,'field':f'step_{index}','reason':'witnessed_semantic_mistranslation','excerpt':m.group()})
        for index,ingredient in enumerate(translated.get('ingredients',[]),1):
            text=ingredient.get('name','')
            for expr in WITNESSED_MISTRANSLATIONS.get(locale,()):
                if m:=re.search(expr,text,re.I):
                    warnings.append({'severity':'high','recipe':rid,'field':f'ingredient_{index}','reason':'witnessed_semantic_mistranslation','excerpt':m.group()})
    reviewed=[x['id'] for x in pack.get('recipes',[]) if x.get('reviewStatus')=='human_reviewed' and x.get('reviewEvidence')]
    reasons=Counter(x['reason'] for x in warnings)
    return {
        'locale':locale,'sourceSha256':digest(source),
        'recipeCount':len(pack.get('recipes',[])),'structuralErrorCount':len(structural),
        'structuralErrors':structural,
        'humanReviewedCount':len(reviewed),'humanReviewRequiredCount':112,
        'unreviewedCount':112-len(reviewed),
        'warningCount':len(warnings),
        'highSeverityCount':sum(x['severity']=='high' for x in warnings),
        'warningReasons':dict(sorted(reasons.items())),
        'warnings':warnings,
        'releaseApproved':len(structural)==0 and len(warnings)==0 and len(reviewed)==112,
        'editorialNotice':'Machine draft; advisory lexical checks do not replace contextual linguistic and culinary review.'
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--pack',required=True)
    p.add_argument('--report',required=True)
    p.add_argument('--strict-release',action='store_true')
    args=p.parse_args()
    source=json.loads(Path(args.source).read_text(encoding='utf-8'))
    pack=json.loads(Path(args.pack).read_text(encoding='utf-8'))
    result=audit(source,pack)
    Path(args.report).parent.mkdir(parents=True,exist_ok=True)
    Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('warnings','structuralErrors')},ensure_ascii=False))
    if result['structuralErrorCount'] or (args.strict_release and not result['releaseApproved']):
        raise SystemExit(1)

if __name__=='__main__':main()
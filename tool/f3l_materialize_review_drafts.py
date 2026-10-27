#!/usr/bin/env python3
"""Persist source-locked edited candidate packs for review; never publish them."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from f3l_translation_gate import inspect, digest, source_recipes
from f3l_editorial_audit import audit
from f3l_curated_recipe_051 import apply as curate_051
from f3l_culinary_safety_fixes import apply as culinary_fixes

LOCALES=('en','es','fr','de','pt')
def generate(source,pack):
    locale=pack['locale']
    if locale not in LOCALES:raise ValueError('unsupported target locale')
    by_id={r['id']:r for r in source_recipes(source)}
    if pack.get('sourceBaselineSha256')!=digest(source):raise ValueError('Italian source fingerprint changed')
    if pack.get('reviewStatus')!='machine_draft_not_publishable':raise ValueError('only quarantined MT drafts accepted')
    before=inspect(source,pack)
    if before:raise ValueError('invalid unedited input: '+str(before[:4]))
    for translated in pack['recipes']:
        rid=translated['id'];it=by_id[rid]
        if rid=='recipe_000051':curate_051(it,translated,locale)
        culinary_fixes(it,translated,locale)
        if translated['reviewStatus']!='machine_draft':raise ValueError('must never mark edits human_reviewed')
    # Explicit provenance distinguishes this human-guided copy edit from locale sign-off.
    pack['editorialStaging']={
        'status':'PARTIAL_COPYEDIT_UNAPPROVED',
        'comprehensivelyEditedRecipeIds':['recipe_000051'],
        'partiallyEditedRecipeIds':['recipe_000053','recipe_000059','recipe_000107','recipe_000150'],
        'noAutomaticPublication':True,
        'copyeditScope':'Machine drafts are not native-speaker certified or cooking-tested.'
    }
    issues=inspect(source,pack)
    if issues:raise ValueError('Post-edit structural issues: '+str(issues[:20]))
    return pack

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',default='authoring/f3k_it_hardening_51_162.json')
    ap.add_argument('--input-dir',required=True)
    ap.add_argument('--output-dir',default='authoring/f3l_review_drafts')
    ap.add_argument('--reports-dir',default='docs/f3l_editorial')
    ns=ap.parse_args()
    src=json.loads(Path(ns.source).read_text(encoding='utf-8'))
    out=Path(ns.output_dir);reports=Path(ns.reports_dir)
    out.mkdir(parents=True,exist_ok=True);reports.mkdir(parents=True,exist_ok=True)
    summary=[]
    for locale in LOCALES:
        candidate=Path(ns.input_dir)/locale/f'f3l_{locale}_51_162_draft.json'
        pack=generate(src,json.loads(candidate.read_text(encoding='utf-8')))
        filename=f'f3l_{locale}_51_162_review_draft.json'
        (out/filename).write_text(json.dumps(pack,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        report=audit(src,pack)
        (reports/f'f3l_{locale}_editorial_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        summary.append({k:report[k] for k in ('locale','recipeCount','structuralErrorCount','warningCount','highSeverityCount','humanReviewedCount','releaseApproved')})
        print(f'{locale}: {report["recipeCount"]}/112, structural={report["structuralErrorCount"]}, editorial warnings={report["warningCount"]}, high={report["highSeverityCount"]}, release={report["releaseApproved"]}')
    (reports/'f3l_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
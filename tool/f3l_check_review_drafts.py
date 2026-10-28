#!/usr/bin/env python3
"""Fast CI gate for persisted quarantined F3L five-locale candidate packs."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from f3l_translation_gate import inspect, digest
from f3l_editorial_audit import audit

LOCALES=('en','es','fr','de','pt')
def check(source,root,strict_release=False):
    results=[]
    for loc in LOCALES:
        path=root/f'f3l_{loc}_51_162_review_draft.json'
        pack=json.loads(path.read_text(encoding='utf-8'))
        if pack.get('locale')!=loc:raise ValueError(f'{loc}: locale mismatch')
        if pack.get('sourceBaselineSha256')!=digest(source):raise ValueError(f'{loc}: source changed')
        if pack.get('reviewStatus')!='machine_draft_not_publishable':raise ValueError(f'{loc}: missing non-publishable status')
        if not pack.get('editorialStaging',{}).get('noAutomaticPublication'):raise ValueError(f'{loc}: unsafe promotion marker')
        errors=inspect(source,pack,require_review=strict_release)
        if errors:raise ValueError(f'{loc}: '+str(errors[:10]))
        report=audit(source,pack)
        if strict_release and not report['releaseApproved']:
            raise ValueError(f'{loc}: native editorial review incomplete')
        results.append({k:report[k] for k in ('locale','recipeCount','structuralErrorCount','warningCount','highSeverityCount','humanReviewedCount','releaseApproved')})
    return results

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',default='authoring/f3k_it_hardening_51_162.json')
    ap.add_argument('--draft-dir',default='authoring/f3l_review_drafts')
    ap.add_argument('--strict-release',action='store_true')
    args=ap.parse_args()
    source=json.loads(Path(args.source).read_text(encoding='utf-8'))
    results=check(source,Path(args.draft_dir),args.strict_release)
    print(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
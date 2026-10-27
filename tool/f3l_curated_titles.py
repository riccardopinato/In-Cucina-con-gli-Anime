"""Source-bound 112x5 culinary title copy-edit, stored in UTF-8 PSV for review.

Titles are prepared with bilingual culinary terminology, but they are AI-generated
editorial candidates, not independently certified native translations.
"""
from __future__ import annotations
from pathlib import Path
from f3l_translation_gate import digest,source_recipes
SOURCE_SHA256='4d736cfa431025fdd8c6baa9725adf2525cdf0bcbf2be8508941f5dd68c3710f'
LOCALES=('en','es','fr','de','pt')
TITLE_FILE=Path(__file__).with_suffix('.psv')

def titles():
    lines=TITLE_FILE.read_text(encoding='utf-8').splitlines()
    data=[row.split('|') for row in lines]
    if data[0]!=['id',*LOCALES]:raise ValueError('Unexpected title translation columns')
    if len(data)!=113 or any(len(row)!=6 for row in data):
        raise ValueError('112 five-locale titles required')
    expected=[f'recipe_{i:06d}' for i in range(51,163)]
    if [row[0] for row in data[1:]]!=expected:raise ValueError('Recipe title list/order drift')
    if any(not x.strip() for row in data[1:] for x in row[1:]):raise ValueError('Blank localized title')
    return {l:{row[0]:row[i] for row in data[1:]} for i,l in enumerate(LOCALES,1)}

def apply_titles(source,pack):
    if digest(source)!=SOURCE_SHA256 or pack.get('sourceBaselineSha256')!=SOURCE_SHA256:
        raise ValueError('Italian source changed: re-review every title')
    locales=titles();loc=pack['locale'];mapping=locales[loc]
    source_recipes(source)
    for row in pack['recipes']:
        row['title']=mapping[row['id']]
    return pack
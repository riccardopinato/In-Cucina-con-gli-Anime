"""Conservative glossary corrections to *witnessed* MT mistranslations.

This does not auto-certify or suggest that the surrounding prose is native-quality.
Every replacement is an exact known harmful substring under a frozen IT hash.
"""
from f3l_translation_gate import digest
SOURCE_SHA256='905e4faa5253bc2968477836657abc6068e2961768008707f83b3b4b6f17431e'
REPLACEMENTS={
 'en':[],
 'es':[
   ('Zuca Japonesa Stufata','calabaza japonesa estofada'),
   ('Zuca','calabaza'),
 ],
 'fr':[
   ('pangratté','chapelure'),
   ('Pangratté','chapelure'),
   ('Escolez','Égouttez'),
   ('Miso Nikumi','Miso Nikomi'),
   ('Udon Stufati al Miso','udon mijotés au miso'),
   ('man et porc','bœuf et porc'),
 ],
 'de':[
   ('Nudeln, frisch für Kupfer','frische Ramen-Nudeln'),
   ('Nudeln für Kupfer, frisch','frische Ramen-Nudeln'),
   ('Nudeln für Kupfer','Ramen-Nudeln'),
   ('Kupferschüsseln','Ramen-Schalen'),
   ('Kupfer','Ramen'),
   ('Bierhefe','Trockenhefe'),
   ('Manzo','Rind'),
 ],
 'pt':[
   ('macarrãoes','fios de massa'),
   ('Macarrãoes','fios de massa'),
 ],
}

def apply(source,pack):
    if digest(source)!=SOURCE_SHA256 or pack.get('sourceBaselineSha256')!=SOURCE_SHA256:
        raise ValueError('Italian source changed: witnessed glossary repairs need re-review')
    locale=pack['locale']; replacements=REPLACEMENTS[locale]
    fields_changed=0
    def fix(s):
        nonlocal fields_changed
        if not isinstance(s,str):return s
        out=s
        for wrong,right in replacements:out=out.replace(wrong,right)
        if out!=s:fields_changed+=1
        return out
    for r in pack['recipes']:
        r['title']=fix(r['title']);r['description']=fix(r['description'])
        for ingredient in r['ingredients']:
            ingredient['name']=fix(ingredient['name'])
            if ingredient.get('note'):ingredient['note']=fix(ingredient['note'])
        for step in r['steps']:step['instruction']=fix(step['instruction'])
        for i,e in enumerate(r.get('equipment',[])):r['equipment'][i]=fix(e)
    for c in pack['reusableComponents'].values():
        c['title']=fix(c['title'])
        for i in c.get('ingredients',[]):i['name']=fix(i['name'])
        if 'steps' in c:c['steps']=[fix(x) for x in c['steps']]
    return fields_changed
"""Limited source-bound semantic corrections that prevent cooking mistakes.

Applied to editorial *drafts* only. Unmodified recipes remain unreviewed.
"""
from f3l_translation_gate import digest

# Change is rejected if the Italian operation changes.
FIXES={
 ('es','recipe_000059','step_3'): ('19c3b0a5','Deja que el ajo y el jengibre se doren a fuego suave durante 1 minuto.'),
 ('de','recipe_000059','step_3'): ('19c3b0a5','Knoblauch und Ingwer bei schwacher Hitze 1 Minute lang leicht goldbraun anbraten.'),
 ('es','recipe_000107','step_1'): ('19c3b0a5','Corta dos rebanadas de shokupan de unos 2–3 cm de grosor. Deja que el ogura-an alcance la temperatura ambiente o caliéntalo ligeramente sin que se reseque.'),
 ('fr','recipe_000107','step_1'): ('19c3b0a5','Coupez deux tranches de shokupan d’environ 2 à 3 cm d’épaisseur. Laissez l’ogura-an revenir à température ambiante ou réchauffez-le doucement sans le dessécher.'),
 ('de','recipe_000107','step_1'): ('19c3b0a5','Zwei etwa 2–3 cm dicke Scheiben Shokupan abschneiden. Das Ogura-An auf Zimmertemperatur bringen oder kurz und behutsam erwärmen, ohne es auszutrocknen.'),
 ('es','recipe_000150','step_3'): ('19c3b0a5','Da la vuelta a la pechuga de pato y cocínala durante otros 2 minutos.'),
}

# Titles and descriptive copy are amended independently of culinary operations.
TITLES_053={
 'en':'Ebi Tendon — shrimp and vegetable tempura over rice with tentsuyu sauce',
 'es':'Ebi Tendon — tempura de gambas y verduras sobre arroz con salsa tentsuyu',
 'fr':'Ebi Tendon — tempura de crevettes et légumes sur riz, sauce tentsuyu',
 'de':'Ebi Tendon – Garnelen- und Gemüse-Tempura auf Reis mit Tentsuyu-Sauce',
 'pt':'Ebi Tendon — tempura de camarão e legumes sobre arroz com molho tentsuyu',
}
DESCRIPTIONS_053={
 'en':('Ebi tendon is a Japanese rice bowl topped with crisp shrimp and vegetable tempura. Keep the batter icy cold and mix it only briefly: a few lumps help create a delicate, airy crust. The shrimp are scored so they stay straight when fried, while a warm tentsuyu sauce of dashi, soy sauce, mirin and sugar seasons the rice. Arrange everything just before serving to preserve the contrast between hot rice and crunchy tempura.'),
 'es':('El ebi tendon es un cuenco de arroz japonés coronado con tempura crujiente de gambas y verduras. Mantén la masa de rebozado muy fría y mézclala lo justo para que quede ligera, incluso con algunos grumos. Haz pequeñas incisiones en las gambas para evitar que se curven al freírse. La salsa tentsuyu, preparada con dashi, soja, mirin y azúcar, se vierte sobre el arroz justo antes de disponer la tempura para conservar su textura.'),
 'fr':('L’ebi tendon associe du riz chaud à des crevettes et des légumes en tempura croustillante. Travaillez la pâte à beignet aussi peu que possible et gardez-la glacée : quelques grumeaux favorisent une croûte légère. Pratiquez de petites incisions sur la face ventrale des crevettes pour qu’elles restent droites à la friture. La sauce tentsuyu, préparée avec du dashi, de la sauce soja, du mirin et du sucre, parfume le riz ; disposez la tempura au dernier moment pour préserver son croustillant.'),
 'de':('Ebi Tendon ist eine japanische Reisschale mit knusprig frittierten Garnelen und Gemüse in Tempura-Teig. Der Teig bleibt besonders leicht, wenn er eiskalt ist und nur kurz verrührt wird; kleine Klümpchen sind erwünscht. Durch flache Einschnitte an der Bauchseite bleiben die Garnelen beim Frittieren möglichst gerade. Die warme Tentsuyu-Sauce aus Dashi, Sojasauce, Mirin und Zucker würzt den Reis. Tempura erst unmittelbar vor dem Servieren darauflegen, damit sie knusprig bleibt.'),
 'pt':('O ebi tendon é uma tigela japonesa de arroz quente coberto com tempura crocante de camarão e legumes. A massa deve estar muito fria e ser mexida apenas o necessário; pequenos grumos ajudam a obter uma crosta leve. Faça cortes superficiais na parte de baixo dos camarões para evitar que enrolem durante a fritura. O molho tentsuyu, preparado com dashi, molho de soja, mirin e açúcar, tempera o arroz. Disponha a tempura no último momento para conservar a textura estaladiça.'),
}
INGREDIENT_053={
 'en':{'gamberone_freschi_sgusciati':'fresh peeled shrimp, tails left on','verdure_a_scelta':'vegetables of your choice (pumpkin, eggplant or shiso leaves)','riso_bianco_per_sushi_o_riso_originario_cotto_al_v':'steamed white rice (sushi rice or another short-grain rice)'},
 'es':{'gamberone_freschi_sgusciati':'gambas frescas peladas, con la cola intacta','verdure_a_scelta':'verduras al gusto (calabaza, berenjena u hojas de shiso)','riso_bianco_per_sushi_o_riso_originario_cotto_al_v':'arroz blanco cocido al vapor, de sushi u otra variedad de grano corto'},
 'fr':{'gamberone_freschi_sgusciati':'crevettes fraîches décortiquées, queue conservée','verdure_a_scelta':'légumes au choix (courge, aubergine ou feuilles de shiso)','riso_bianco_per_sushi_o_riso_originario_cotto_al_v':'riz blanc cuit à la vapeur, de type riz à sushi ou autre riz rond'},
 'de':{'gamberone_freschi_sgusciati':'frische, geschälte Garnelen mit Schwanzflosse','verdure_a_scelta':'Gemüse nach Wahl (Kürbis, Aubergine oder Shiso-Blätter)','riso_bianco_per_sushi_o_riso_originario_cotto_al_v':'gedämpfter weißer Reis, z. B. Sushi-Reis oder anderer Rundkornreis'},
 'pt':{'gamberone_freschi_sgusciati':'camarões frescos descascados, com a cauda intacta','verdure_a_scelta':'legumes à escolha (abóbora, beringela ou folhas de shiso)','riso_bianco_per_sushi_o_riso_originario_cotto_al_v':'arroz branco cozido a vapor, de sushi ou outro arroz de grão curto'},
}


def apply(source_recipe, target_recipe, locale):
    rid=source_recipe['id']
    if rid!=target_recipe['id']:raise ValueError('source and target recipe IDs mismatch')
    if rid=='recipe_000053':
        if digest(source_recipe)!='144316766446fb70f77715d858cc2a8ae4c19587c2a8e8db5b0fb7e39c78653d':
            raise ValueError('Italian Ebi Tendon source changed')
        target_recipe['title']=TITLES_053[locale]
        target_recipe['description']=DESCRIPTIONS_053[locale]
        for ingredient in target_recipe['ingredients']:
            if ingredient['id'] in INGREDIENT_053[locale]:
                ingredient['name']=INGREDIENT_053[locale][ingredient['id']]
    for (code,fixrid,stepid),(_,newtext) in FIXES.items():
        if code==locale and fixrid==rid:
            if digest(source_recipe)!=DIGESTS[fixrid]:raise ValueError(f'Italian {fixrid} source changed')
            dst=next((s for s in target_recipe['steps'] if s['id']==stepid),None)
            if dst is None:raise ValueError(f'Missing {rid} {stepid}')
            dst['instruction']=newtext
    return target_recipe

DIGESTS={
    # Immutable exact source fingerprints; verified against F3K Italian baseline.
    'recipe_000059':'99e7c1a025a4e61c53698266dfa42669bc9d14b0fce753fd95209f070f6918be', 'recipe_000107':'88e10b92a35afee9868971b87e71d436bb3ecd3884fa4f973ba60f637ed57ed8','recipe_000150':'fac38660770a0602c0ee2bbcb2d02606567fea065c5933d748d3ef4b82904bf7'
}
"""Targeted French editorial repair for Kuri Manju, bound to an exact Italian revision.

All nine Italian preparation operations and nine canonical ingredient records remain
intact. This repair changes only localized wording; it is not a full human review
of the other 111 French recipes or of the complete French locale pack.
"""
from __future__ import annotations

from f3l_translation_gate import digest

RECIPE_ID = "recipe_000159"
SOURCE_SHA256 = "fd8800bb21bf7ad3adae4619c178aa5e8853b840d19667f155d46582cc6ca7cd"
TITLE = "Kuri Manju — petits gâteaux japonais fourrés à la châtaigne"
DESCRIPTION = (
    "Ces kuri manju sont de petits gâteaux japonais cuits au four, façonnés en forme "
    "de châtaigne. Chaque pièce renferme une châtaigne entière enveloppée de shiro-an, "
    "une pâte sucrée de haricots blancs. La pâte extérieure associe farine, lait "
    "concentré et jaune d’œuf. Après 20 minutes de repos au réfrigérateur, les "
    "gâteaux sont façonnés, dorés au jaune d’œuf et à la sauce soja, puis décorés "
    "de sésame noir. Une cuisson de 12 à 15 minutes à 170 °C leur donne une surface "
    "dorée et brillante. La recette permet de préparer huit petits gâteaux."
)
INGREDIENT_NAMES = {
    "farina_per_dolci": "farine pâtissière",
    "latte_condensato": "lait concentré",
    "lievito_per_dolci": "levure chimique",
    "tuorlo_d_uovo": "jaune d’œuf",
    "pasta_di_fagioli_bianchi": "pâte sucrée de haricots blancs (shiro-an)",
    "castagne_sciroppate_o_lesse_intatte": "châtaignes entières au sirop ou cuites à l’eau",
    "tuorlo_per_spennellatura": "jaune d’œuf pour la dorure",
    "salsa_di_soia_per_spennellatura": "sauce soja pour la dorure",
    "semi_di_sesamo_nero": "graines de sésame noir",
}
STEPS = {
    "step_1": "Dans un saladier, mélangez le lait concentré avec le jaune d’œuf.",
    "step_2": "Tamisez la farine avec la levure chimique, puis incorporez-les au mélange. Pétrissez jusqu’à obtenir une pâte souple.",
    "step_3": "Laissez reposer la pâte au réfrigérateur pendant 20 minutes.",
    "step_4": "Enrobez chacune des huit châtaignes entières de 20 g de shiro-an, en formant une boule régulière.",
    "step_5": "Divisez la pâte en huit portions et aplatissez-les en disques. Enveloppez chaque boule de châtaigne et de shiro-an dans un disque de pâte, puis soudez soigneusement les bords et façonnez une forme de châtaigne.",
    "step_6": "Déposez les huit gâteaux sur une plaque recouverte de papier cuisson.",
    "step_7": "Mélangez le jaune d’œuf réservé à la dorure avec la sauce soja. Badigeonnez uniquement le dessus des manju.",
    "step_8": "Trempez la pointe de chaque manju dans les graines de sésame noir.",
    "step_9": "Faites cuire dans un four à chaleur tournante préchauffé à 170 °C pendant 12 à 15 minutes, jusqu’à ce que le dessus soit bien doré et brillant.",
}


def apply_french_recipe_159(source_recipe: dict, translated_recipe: dict) -> dict:
    """Correct only matching source revision; never mutate canonical fields."""
    if source_recipe.get("id") != RECIPE_ID or translated_recipe.get("id") != RECIPE_ID:
        raise ValueError("French editorial override is only for recipe_000159")
    if digest(source_recipe) != SOURCE_SHA256:
        raise ValueError("Italian source recipe_000159 changed; French repair must be reviewed again")
    if [i["id"] for i in source_recipe["ingredients"]] != list(INGREDIENT_NAMES):
        raise ValueError("Italian ingredient order changed; French repair is stale")
    if [s["id"] for s in source_recipe["steps"]] != list(STEPS):
        raise ValueError("Italian step order changed; French repair is stale")
    if [i["id"] for i in translated_recipe["ingredients"]] != list(INGREDIENT_NAMES):
        raise ValueError("French ingredient IDs do not match frozen source")
    if [s["id"] for s in translated_recipe["steps"]] != list(STEPS):
        raise ValueError("French step IDs do not match frozen source")
    translated_recipe["title"] = TITLE
    translated_recipe["description"] = DESCRIPTION
    for ingredient in translated_recipe["ingredients"]:
        ingredient["name"] = INGREDIENT_NAMES[ingredient["id"]]
    for step in translated_recipe["steps"]:
        step["instruction"] = STEPS[step["id"]]
    # Keep reviewStatus=machine_draft: a single repaired recipe is not review
    # evidence for the complete 112-recipe French language pack.
    return translated_recipe
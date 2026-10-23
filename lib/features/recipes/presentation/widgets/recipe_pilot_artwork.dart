const Map<String, String> pilotRecipeArtwork = {
  'recipe_000002': 'assets/recipe_artwork/recipe_000002.webp',
  'recipe_000003': 'assets/recipe_artwork/recipe_000003.webp',
  'recipe_000009': 'assets/recipe_artwork/recipe_000009.webp',
};

String? pilotRecipeArtworkFor(String recipeId) {
  return pilotRecipeArtwork[recipeId];
}

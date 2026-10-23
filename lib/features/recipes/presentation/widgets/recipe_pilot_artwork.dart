const Map<String, String> pilotRecipeArtwork = {
  'recipe_000002': 'assets/recipe_artwork/recipe_000002.jpg',
  'recipe_000003': 'assets/recipe_artwork/recipe_000003.jpg',
  'recipe_000009': 'assets/recipe_artwork/recipe_000009.jpg',
};

String? pilotRecipeArtworkFor(String recipeId) {
  return pilotRecipeArtwork[recipeId];
}

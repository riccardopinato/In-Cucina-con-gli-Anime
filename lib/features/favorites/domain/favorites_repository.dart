abstract interface class FavoritesRepository {
  Set<String> loadFavoriteIds();
  Future<void> saveFavoriteIds(Set<String> recipeIds);
}

import 'package:shared_preferences/shared_preferences.dart';

import '../domain/favorites_repository.dart';

class SharedPreferencesFavoritesRepository implements FavoritesRepository {
  SharedPreferencesFavoritesRepository(this._prefs);

  static const _key = 'favorite_recipe_ids_v1';

  final SharedPreferences _prefs;

  @override
  Set<String> loadFavoriteIds() {
    return (_prefs.getStringList(_key) ?? const <String>[]).toSet();
  }

  @override
  Future<void> saveFavoriteIds(Set<String> recipeIds) async {
    final sorted = recipeIds.toList()..sort();
    await _prefs.setStringList(_key, sorted);
  }
}

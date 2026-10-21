import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/persistence/shared_preferences_provider.dart';
import '../data/shared_preferences_favorites_repository.dart';
import '../domain/favorites_repository.dart';

final favoritesRepositoryProvider = Provider<FavoritesRepository>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SharedPreferencesFavoritesRepository(prefs);
});

class FavoritesNotifier extends Notifier<Set<String>> {
  @override
  Set<String> build() {
    return ref.watch(favoritesRepositoryProvider).loadFavoriteIds();
  }

  void toggle(String recipeId) {
    final next = {...state};
    if (!next.add(recipeId)) {
      next.remove(recipeId);
    }
    state = next;
    unawaited(
      ref.read(favoritesRepositoryProvider).saveFavoriteIds(state),
    );
  }
}

final favoritesProvider = NotifierProvider<FavoritesNotifier, Set<String>>(
  FavoritesNotifier.new,
);

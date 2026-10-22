import 'dart:ui' show PlatformDispatcher;

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/preferences/preferences_providers.dart';
import '../data/recipe_catalog_source.dart';
import '../data/versioned_recipe_catalog_repository.dart';
import '../domain/recipe.dart';
import '../domain/recipe_catalog_repository.dart';

final recipeLocaleCodeProvider = Provider<String>((ref) {
  final preference = ref.watch(localePreferenceProvider);
  return preference.locale?.languageCode ??
      PlatformDispatcher.instance.locale.languageCode;
});

final recipeCatalogRepositoryProvider = Provider<RecipeCatalogRepository>((ref) {
  return VersionedRecipeCatalogRepository(
    source: AssetRecipeCatalogSource(rootBundle),
    localeCode: ref.watch(recipeLocaleCodeProvider),
  );
});

final allRecipesProvider = FutureProvider<List<Recipe>>((ref) {
  return ref.watch(recipeCatalogRepositoryProvider).loadPublishedRecipes();
});

class SearchQueryNotifier extends Notifier<String> {
  @override
  String build() => '';

  void setQuery(String value) => state = value;
  void reset() => state = '';
}

final searchQueryProvider = NotifierProvider<SearchQueryNotifier, String>(
  SearchQueryNotifier.new,
);

class SelectedAnimeNotifier extends Notifier<String?> {
  @override
  String? build() => null;

  void select(String? value) => state = value;
}

final selectedAnimeProvider = NotifierProvider<SelectedAnimeNotifier, String?>(
  SelectedAnimeNotifier.new,
);

class SelectedDifficultyNotifier extends Notifier<RecipeDifficulty?> {
  @override
  RecipeDifficulty? build() => null;

  void select(RecipeDifficulty? value) => state = value;
}

final selectedDifficultyProvider =
    NotifierProvider<SelectedDifficultyNotifier, RecipeDifficulty?>(
  SelectedDifficultyNotifier.new,
);

final filteredRecipesProvider = Provider<AsyncValue<List<Recipe>>>((ref) {
  final recipes = ref.watch(allRecipesProvider);
  final query = ref.watch(searchQueryProvider).trim().toLowerCase();
  final selectedAnime = ref.watch(selectedAnimeProvider);
  final selectedDifficulty = ref.watch(selectedDifficultyProvider);

  return recipes.whenData((items) {
    return items.where((recipe) {
      final matchesQuery = query.isEmpty ||
          recipe.title.toLowerCase().contains(query) ||
          recipe.animeSource.toLowerCase().contains(query);
      final matchesAnime =
          selectedAnime == null || recipe.animeSource == selectedAnime;
      final matchesDifficulty = selectedDifficulty == null ||
          recipe.difficulty == selectedDifficulty;
      return matchesQuery && matchesAnime && matchesDifficulty;
    }).toList(growable: false);
  });
});

final animeSourcesProvider = Provider<AsyncValue<List<String>>>((ref) {
  return ref.watch(allRecipesProvider).whenData((recipes) {
    final sources = recipes.map((recipe) => recipe.animeSource).toSet().toList()
      ..sort();
    return sources;
  });
});

final hasActiveRecipeFiltersProvider = Provider<bool>((ref) {
  return ref.watch(searchQueryProvider).trim().isNotEmpty ||
      ref.watch(selectedAnimeProvider) != null ||
      ref.watch(selectedDifficultyProvider) != null;
});

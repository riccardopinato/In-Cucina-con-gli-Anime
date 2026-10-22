import 'dart:convert';

import 'package:animekitchen/features/recipes/data/recipe_catalog_source.dart';
import 'package:animekitchen/features/recipes/data/versioned_recipe_catalog_repository.dart';
import 'package:animekitchen/features/recipes/domain/recipe.dart';
import 'package:flutter_test/flutter_test.dart';

class MemoryCatalogSource implements RecipeCatalogSource {
  const MemoryCatalogSource(this.files);

  final Map<String, String> files;

  @override
  Future<String> loadString(String path) async {
    final value = files[path];
    if (value == null) {
      throw StateError('Missing test asset $path');
    }
    return value;
  }
}

Map<String, String> fixtureCatalog({
  int schemaVersion = 1,
  int contentVersion = 1,
  bool includeItalianRecipe = true,
  bool duplicateRecipe = false,
}) {
  final recipe = {
    'id': 'fixture_noodles',
    'contentVersion': contentVersion,
    'status': 'published',
    'inspirationTitle': 'Synthetic Series',
    'prepMinutes': 5,
    'cookMinutes': 8,
    'servings': 2,
    'difficulty': 'easy',
    'imageAsset': null,
    'contentOrigin': 'original',
    'sourceNote': null,
    'ingredients': [
      {'id': 'noodles', 'quantity': 100, 'unit': 'g'},
    ],
    'steps': [
      {'id': 'cook', 'timerSeconds': 480},
    ],
  };

  Map<String, Object?> localized(String title, String ingredient, String step) {
    return {
      'title': title,
      'ingredientTexts': {
        'noodles': {'name': ingredient, 'note': null},
      },
      'stepTexts': {'cook': step},
    };
  }

  final manifest = {
    'schemaVersion': schemaVersion,
    'catalogVersion': '1.0.0',
    'defaultLocale': 'en',
    'supportedLocales': ['en', 'it'],
    'contentAsset': 'content.json',
    'localeAssets': {
      'en': 'en.json',
      'it': 'it.json',
    },
  };

  return {
    'manifest.json': jsonEncode(manifest),
    'content.json': jsonEncode({
      'schemaVersion': 1,
      'recipes': duplicateRecipe ? [recipe, recipe] : [recipe],
    }),
    'en.json': jsonEncode({
      'schemaVersion': 1,
      'locale': 'en',
      'recipes': {
        'fixture_noodles': localized(
          'Fixture noodles',
          'Noodles',
          'Cook the noodles.',
        ),
      },
    }),
    'it.json': jsonEncode({
      'schemaVersion': 1,
      'locale': 'it',
      'recipes': includeItalianRecipe
          ? {
              'fixture_noodles': localized(
                'Noodles di prova',
                'Noodles',
                'Cuoci i noodles.',
              ),
            }
          : <String, Object?>{},
    }),
  };
}

void main() {
  test('loads requested locale and structured canonical data', () async {
    final repository = VersionedRecipeCatalogRepository(
      source: MemoryCatalogSource(fixtureCatalog()),
      localeCode: 'it-IT',
      manifestAsset: 'manifest.json',
    );

    final recipes = await repository.loadPublishedRecipes();

    expect(recipes, hasLength(1));
    expect(recipes.single.id, 'fixture_noodles');
    expect(recipes.single.title, 'Noodles di prova');
    expect(recipes.single.contentVersion, 1);
    expect(recipes.single.contentOrigin, RecipeContentOrigin.original);
    expect(recipes.single.ingredients.single.displayText, '100 g Noodles');
    expect(recipes.single.steps.single.timerSeconds, 480);
  });

  test('falls back to default locale when translation is absent', () async {
    final repository = VersionedRecipeCatalogRepository(
      source: MemoryCatalogSource(
        fixtureCatalog(includeItalianRecipe: false),
      ),
      localeCode: 'it',
      manifestAsset: 'manifest.json',
    );

    final recipes = await repository.loadPublishedRecipes();

    expect(recipes.single.title, 'Fixture noodles');
    expect(recipes.single.steps.single.text, 'Cook the noodles.');
  });

  test('rejects unsupported schema version without partial loading', () async {
    final repository = VersionedRecipeCatalogRepository(
      source: MemoryCatalogSource(fixtureCatalog(schemaVersion: 2)),
      localeCode: 'en',
      manifestAsset: 'manifest.json',
    );

    expect(
      repository.loadPublishedRecipes(),
      throwsA(isA<RecipeCatalogException>()),
    );
  });

  test('rejects duplicate stable recipe ids', () async {
    final repository = VersionedRecipeCatalogRepository(
      source: MemoryCatalogSource(fixtureCatalog(duplicateRecipe: true)),
      localeCode: 'en',
      manifestAsset: 'manifest.json',
    );

    expect(
      repository.loadPublishedRecipes(),
      throwsA(isA<RecipeCatalogException>()),
    );
  });

  test('stable id survives content revision', () async {
    final first = VersionedRecipeCatalogRepository(
      source: MemoryCatalogSource(fixtureCatalog(contentVersion: 1)),
      localeCode: 'en',
      manifestAsset: 'manifest.json',
    );
    final second = VersionedRecipeCatalogRepository(
      source: MemoryCatalogSource(fixtureCatalog(contentVersion: 2)),
      localeCode: 'en',
      manifestAsset: 'manifest.json',
    );

    final firstRecipe = (await first.loadPublishedRecipes()).single;
    final secondRecipe = (await second.loadPublishedRecipes()).single;

    expect(firstRecipe.id, secondRecipe.id);
    expect(firstRecipe.contentVersion, 1);
    expect(secondRecipe.contentVersion, 2);
  });
}

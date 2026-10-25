import 'package:animekitchen/features/recipes/data/recipe_catalog_source.dart';
import 'package:animekitchen/features/recipes/data/versioned_recipe_catalog_repository.dart';
import 'package:animekitchen/features/recipes/domain/recipe.dart';
import 'package:flutter_test/flutter_test.dart';

class _MemorySource implements RecipeCatalogSource {
  const _MemorySource(this.files);

  final Map<String, String> files;

  @override
  Future<String> loadString(String path) async {
    final value = files[path];
    if (value == null) {
      throw StateError('Missing test asset: $path');
    }
    return value;
  }
}

void main() {
  test('F3G rich editorial fields parse without breaking stable recipe identity', () async {
    const source = _MemorySource({
      'assets/catalog/manifest.json': '''
{
  "schemaVersion": 1,
  "catalogVersion": "0.7.0",
  "defaultLocale": "en",
  "supportedLocales": ["en"],
  "contentAsset": "assets/catalog/recipes.json",
  "localeAssets": {"en": "assets/catalog/locales/en.json"}
}
''',
      'assets/catalog/recipes.json': '''
{
  "schemaVersion": 1,
  "recipes": [
    {
      "id": "recipe_000041",
      "contentVersion": 1,
      "status": "published",
      "inspirationTitle": "Food Wars! Shokugeki no Soma",
      "animeReferences": [
        {
          "workTitle": "Food Wars! Shokugeki no Soma",
          "relation": "verified_appearance",
          "season": 1,
          "episode": "13–14",
          "chapter": null
        }
      ],
      "prepMinutes": 15,
      "cookMinutes": 15,
      "servings": 2,
      "difficulty": "medium",
      "imageAsset": null,
      "contentOrigin": "adapted",
      "sourceNote": "test",
      "ingredients": [
        {"id": "eggs", "quantity": 4, "unit": null}
      ],
      "steps": [
        {"id": "whip", "timerSeconds": 300}
      ]
    }
  ]
}
''',
      'assets/catalog/locales/en.json': '''
{
  "schemaVersion": 1,
  "locale": "en",
  "recipes": {
    "recipe_000041": {
      "title": "Food Wars-style Soufflé Omelette",
      "description": "A deliberately complete rich editorial description for the F3G parser regression test.",
      "animeContext": "Direct Food Wars reference used to verify the structured anime context parser.",
      "ingredientTexts": {
        "eggs": {"name": "Fresh eggs", "note": null}
      },
      "stepTexts": {
        "whip": "Whip the egg whites to firm glossy peaks while keeping the bowl completely clean and dry."
      }
    }
  }
}
'''
    });

    final repository = VersionedRecipeCatalogRepository(
      source: source,
      localeCode: 'en',
    );

    final recipes = await repository.loadPublishedRecipes();
    expect(recipes, hasLength(1));

    final recipe = recipes.single;
    expect(recipe.id, 'recipe_000041');
    expect(recipe.description, contains('rich editorial description'));
    expect(recipe.animeContext, contains('Direct Food Wars reference'));
    expect(recipe.animeReferences, hasLength(1));

    final reference = recipe.animeReferences.single;
    expect(reference.workTitle, 'Food Wars! Shokugeki no Soma');
    expect(reference.relation, RecipeAnimeRelation.verifiedAppearance);
    expect(reference.season, 1);
    expect(reference.episode, '13–14');
    expect(reference.chapter, isNull);
  });
}

import 'package:flutter_test/flutter_test.dart';
import 'package:animekitchen/features/recipes/data/empty_recipe_catalog_repository.dart';

void main() {
  test('bootstrap catalog deliberately contains no recipes', () async {
    const repository = EmptyRecipeCatalogRepository();

    final recipes = await repository.loadPublishedRecipes();

    expect(recipes, isEmpty);
  });
}

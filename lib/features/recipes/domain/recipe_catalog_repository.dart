import 'recipe.dart';

abstract interface class RecipeCatalogRepository {
  Future<List<Recipe>> loadPublishedRecipes();
}

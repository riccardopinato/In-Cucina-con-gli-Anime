import '../domain/recipe.dart';
import '../domain/recipe_catalog_repository.dart';

class EmptyRecipeCatalogRepository implements RecipeCatalogRepository {
  const EmptyRecipeCatalogRepository();

  @override
  Future<List<Recipe>> loadPublishedRecipes() async => const [];
}

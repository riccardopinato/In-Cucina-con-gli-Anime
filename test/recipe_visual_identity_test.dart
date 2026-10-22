import 'package:animekitchen/features/recipes/domain/recipe.dart';
import 'package:animekitchen/features/recipes/presentation/widgets/recipe_artwork.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'procedural artwork renders all ten production recipe ids',
    (tester) async {
      final recipes = List.generate(
        10,
        (index) => Recipe(
          id: 'recipe_${(index + 1).toString().padLeft(6, '0')}',
          contentVersion: 1,
          contentOrigin: RecipeContentOrigin.adapted,
          title: 'Recipe ${index + 1}',
          animeSource: 'Reference ${index + 1}',
          prepMinutes: 10,
          cookMinutes: 15,
          servings: 2,
          difficulty: RecipeDifficulty.easy,
          ingredients: const [],
          steps: const [],
        ),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ListView(
              children: [
                for (final recipe in recipes)
                  SizedBox(
                    height: 180,
                    child: RecipeArtwork(
                      recipe: recipe,
                      showReference: true,
                    ),
                  ),
              ],
            ),
          ),
        ),
      );

      expect(find.byType(RecipeArtwork), findsNWidgets(10));
      expect(tester.takeException(), isNull);
    },
  );
}

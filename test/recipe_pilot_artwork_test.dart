import 'package:animekitchen/features/recipes/presentation/widgets/recipe_pilot_artwork.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('pilot artwork maps only the three review recipes', () {
    expect(
      pilotRecipeArtworkFor('recipe_000002'),
      'assets/recipe_artwork/recipe_000002.webp',
    );
    expect(
      pilotRecipeArtworkFor('recipe_000003'),
      'assets/recipe_artwork/recipe_000003.webp',
    );
    expect(
      pilotRecipeArtworkFor('recipe_000009'),
      'assets/recipe_artwork/recipe_000009.webp',
    );
    expect(pilotRecipeArtworkFor('recipe_000001'), isNull);
    expect(pilotRecipeArtwork.length, 3);
  });
}

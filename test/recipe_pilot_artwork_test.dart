import 'dart:ui' as ui;

import 'package:animekitchen/features/recipes/presentation/widgets/recipe_pilot_artwork.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('pilot artwork maps only the three review recipes', () {
    expect(
      pilotRecipeArtworkFor('recipe_000002'),
      'assets/recipe_artwork/recipe_000002.jpg',
    );
    expect(
      pilotRecipeArtworkFor('recipe_000003'),
      'assets/recipe_artwork/recipe_000003.jpg',
    );
    expect(
      pilotRecipeArtworkFor('recipe_000009'),
      'assets/recipe_artwork/recipe_000009.jpg',
    );
    expect(pilotRecipeArtworkFor('recipe_000001'), isNull);
    expect(pilotRecipeArtwork.length, 3);
  });

  test('all pilot artwork assets decode through Flutter image codec', () async {
    for (final assetPath in pilotRecipeArtwork.values) {
      final data = await rootBundle.load(assetPath);
      expect(data.lengthInBytes, greaterThan(0), reason: assetPath);

      final codec = await ui.instantiateImageCodec(
        data.buffer.asUint8List(
          data.offsetInBytes,
          data.lengthInBytes,
        ),
      );
      final frame = await codec.getNextFrame();

      expect(frame.image.width, greaterThanOrEqualTo(512), reason: assetPath);
      expect(frame.image.height, greaterThanOrEqualTo(512), reason: assetPath);

      frame.image.dispose();
      codec.dispose();
    }
  });
}

import 'dart:convert';
import 'dart:ui' as ui;

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('published recipe artwork decodes through Flutter', () async {
    final raw = await rootBundle.loadString('assets/catalog/recipes.json');
    final payload = jsonDecode(raw) as Map<String, dynamic>;
    final recipes = (payload['recipes'] as List<dynamic>)
        .cast<Map<String, dynamic>>();
    final paths = recipes
        .map((recipe) => recipe['imageAsset'])
        .whereType<String>()
        .toSet();

    expect(paths, isNotEmpty);

    for (final assetPath in paths) {
      final data = await rootBundle.load(assetPath);
      final codec = await ui.instantiateImageCodec(
        data.buffer.asUint8List(
          data.offsetInBytes,
          data.lengthInBytes,
        ),
      );
      final frame = await codec.getNextFrame();

      expect(frame.image.width, greaterThanOrEqualTo(720), reason: assetPath);
      expect(frame.image.height, greaterThanOrEqualTo(720), reason: assetPath);

      frame.image.dispose();
      codec.dispose();
    }
  });
}

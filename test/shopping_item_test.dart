import 'package:flutter_test/flutter_test.dart';
import 'package:animekitchen/features/shopping/domain/shopping_item.dart';

void main() {
  test('shopping item JSON round trip preserves user state', () {
    const original = ShoppingItem(
      id: 'item-1',
      name: 'Soy sauce',
      recipeSource: 'Manual',
      isBought: true,
    );

    final restored = ShoppingItem.fromJson(original.toJson());

    expect(restored.id, original.id);
    expect(restored.name, original.name);
    expect(restored.recipeSource, original.recipeSource);
    expect(restored.isBought, isTrue);
  });
}

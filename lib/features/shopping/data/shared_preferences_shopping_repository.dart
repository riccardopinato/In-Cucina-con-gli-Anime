import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../domain/shopping_item.dart';
import '../domain/shopping_repository.dart';

class SharedPreferencesShoppingRepository implements ShoppingRepository {
  SharedPreferencesShoppingRepository(this._prefs);

  static const _key = 'shopping_list_items_v1';

  final SharedPreferences _prefs;

  @override
  List<ShoppingItem> loadItems() {
    final encoded = _prefs.getStringList(_key) ?? const <String>[];
    final items = <ShoppingItem>[];

    for (final value in encoded) {
      try {
        final decoded = jsonDecode(value);
        if (decoded is Map<String, dynamic>) {
          items.add(ShoppingItem.fromJson(decoded));
        }
      } on FormatException {
        continue;
      }
    }

    return items;
  }

  @override
  Future<void> saveItems(List<ShoppingItem> items) async {
    final encoded = items
        .map((item) => jsonEncode(item.toJson()))
        .toList(growable: false);
    await _prefs.setStringList(_key, encoded);
  }
}

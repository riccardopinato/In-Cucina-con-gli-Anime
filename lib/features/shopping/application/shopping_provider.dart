import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/persistence/shared_preferences_provider.dart';
import '../data/shared_preferences_shopping_repository.dart';
import '../domain/shopping_item.dart';
import '../domain/shopping_repository.dart';

final shoppingRepositoryProvider = Provider<ShoppingRepository>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SharedPreferencesShoppingRepository(prefs);
});

class ShoppingNotifier extends Notifier<List<ShoppingItem>> {
  @override
  List<ShoppingItem> build() {
    return ref.watch(shoppingRepositoryProvider).loadItems();
  }

  void addManual(String name, String sourceLabel) {
    final trimmed = name.trim();
    if (trimmed.isEmpty) return;

    final item = ShoppingItem(
      id: DateTime.now().microsecondsSinceEpoch.toString(),
      name: trimmed,
      recipeSource: sourceLabel,
    );
    state = [...state, item];
    _persist();
  }

  void toggle(String id) {
    state = [
      for (final item in state)
        if (item.id == id)
          item.copyWith(isBought: !item.isBought)
        else
          item,
    ];
    _persist();
  }

  void remove(String id) {
    state = state.where((item) => item.id != id).toList(growable: false);
    _persist();
  }

  void clearBought() {
    state = state.where((item) => !item.isBought).toList(growable: false);
    _persist();
  }

  void _persist() {
    unawaited(ref.read(shoppingRepositoryProvider).saveItems(state));
  }
}

final shoppingProvider =
    NotifierProvider<ShoppingNotifier, List<ShoppingItem>>(
  ShoppingNotifier.new,
);

import 'shopping_item.dart';

abstract interface class ShoppingRepository {
  List<ShoppingItem> loadItems();
  Future<void> saveItems(List<ShoppingItem> items);
}

class ShoppingItem {
  const ShoppingItem({
    required this.id,
    required this.name,
    required this.recipeSource,
    this.isBought = false,
  });

  final String id;
  final String name;
  final String recipeSource;
  final bool isBought;

  ShoppingItem copyWith({
    String? id,
    String? name,
    String? recipeSource,
    bool? isBought,
  }) {
    return ShoppingItem(
      id: id ?? this.id,
      name: name ?? this.name,
      recipeSource: recipeSource ?? this.recipeSource,
      isBought: isBought ?? this.isBought,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'recipeSource': recipeSource,
        'isBought': isBought,
      };

  factory ShoppingItem.fromJson(Map<String, dynamic> json) {
    return ShoppingItem(
      id: json['id'] as String,
      name: json['name'] as String,
      recipeSource: json['recipeSource'] as String,
      isBought: json['isBought'] as bool? ?? false,
    );
  }
}

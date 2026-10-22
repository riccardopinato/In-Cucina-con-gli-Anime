enum RecipeDifficulty {
  easy,
  medium,
  hard,
}

enum RecipeContentOrigin {
  original,
  inspired,
  adapted,
}

class RecipeIngredient {
  const RecipeIngredient({
    required this.id,
    required this.name,
    this.quantity,
    this.unit,
    this.note,
  });

  final String id;
  final String name;
  final double? quantity;
  final String? unit;
  final String? note;

  String get displayText {
    final parts = <String>[
      if (quantity != null) _formatQuantity(quantity!),
      if (unit != null && unit!.trim().isNotEmpty) unit!.trim(),
      name.trim(),
      if (note != null && note!.trim().isNotEmpty) '(${note!.trim()})',
    ];
    return parts.join(' ');
  }

  static String _formatQuantity(double value) {
    if (value == value.roundToDouble()) {
      return value.toInt().toString();
    }
    return value
        .toStringAsFixed(2)
        .replaceFirst(RegExp(r'0+$'), '')
        .replaceFirst(RegExp(r'\.$'), '');
  }
}

class RecipeStep {
  const RecipeStep({
    required this.id,
    required this.text,
    this.timerSeconds,
  });

  final String id;
  final String text;
  final int? timerSeconds;
}

class Recipe {
  const Recipe({
    required this.id,
    required this.contentVersion,
    required this.contentOrigin,
    required this.title,
    required this.animeSource,
    required this.prepMinutes,
    required this.cookMinutes,
    required this.servings,
    required this.difficulty,
    required this.ingredients,
    required this.steps,
    this.sourceNote,
    this.imageAsset,
  });

  final String id;
  final int contentVersion;
  final RecipeContentOrigin contentOrigin;
  final String? sourceNote;
  final String title;
  final String animeSource;
  final int prepMinutes;
  final int cookMinutes;
  final int servings;
  final RecipeDifficulty difficulty;
  final String? imageAsset;
  final List<RecipeIngredient> ingredients;
  final List<RecipeStep> steps;
}

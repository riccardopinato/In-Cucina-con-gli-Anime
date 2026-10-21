enum RecipeDifficulty {
  easy,
  medium,
  hard,
}

class Recipe {
  const Recipe({
    required this.id,
    required this.title,
    required this.animeSource,
    required this.prepMinutes,
    required this.cookMinutes,
    required this.difficulty,
    required this.ingredients,
    required this.steps,
    this.imageAsset,
  });

  final String id;
  final String title;
  final String animeSource;
  final int prepMinutes;
  final int cookMinutes;
  final RecipeDifficulty difficulty;
  final String? imageAsset;
  final List<String> ingredients;
  final List<String> steps;
}

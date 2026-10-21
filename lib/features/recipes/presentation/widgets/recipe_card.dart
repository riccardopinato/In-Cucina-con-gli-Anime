import 'package:flutter/material.dart';

import '../../../../l10n/app_localizations.dart';
import '../../domain/recipe.dart';
import 'animated_favorite_button.dart';

class RecipeCard extends StatelessWidget {
  const RecipeCard({
    super.key,
    required this.recipe,
    required this.isFavorite,
    required this.onFavoritePressed,
    required this.onTap,
  });

  final Recipe recipe;
  final bool isFavorite;
  final VoidCallback onFavoritePressed;
  final VoidCallback onTap;

  String _difficultyLabel(AppLocalizations l10n) {
    return switch (recipe.difficulty) {
      RecipeDifficulty.easy => l10n.difficultyEasy,
      RecipeDifficulty.medium => l10n.difficultyMedium,
      RecipeDifficulty.hard => l10n.difficultyHard,
    };
  }

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final l10n = AppLocalizations.of(context)!;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AspectRatio(
              aspectRatio: 16 / 10,
              child: Hero(
                tag: 'recipe-image-${recipe.id}',
                child: recipe.imageAsset == null
                    ? DecoratedBox(
                        decoration: BoxDecoration(
                          color: colors.tertiaryContainer,
                        ),
                        child: Icon(
                          Icons.ramen_dining,
                          size: 56,
                          color: colors.onTertiaryContainer,
                        ),
                      )
                    : Image.asset(recipe.imageAsset!, fit: BoxFit.cover),
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 14, 8, 14),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          recipe.title,
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          recipe.animeSource,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '${recipe.prepMinutes + recipe.cookMinutes} min · '
                          '${_difficultyLabel(l10n)}',
                          style: Theme.of(context).textTheme.labelMedium,
                        ),
                      ],
                    ),
                  ),
                  AnimatedFavoriteButton(
                    isFavorite: isFavorite,
                    onPressed: onFavoritePressed,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

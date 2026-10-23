import 'package:flutter/material.dart';

import '../../../../core/theme/app_design_tokens.dart';
import '../../../../l10n/app_localizations.dart';
import '../../domain/recipe.dart';
import 'animated_favorite_button.dart';
import 'recipe_artwork.dart';
import 'recipe_pilot_artwork.dart';

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
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final l10n = AppLocalizations.of(context)!;
    final pilotAsset = pilotRecipeArtworkFor(recipe.id);
    final imageAsset = recipe.imageAsset ?? pilotAsset;

    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadii.container),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              height: 178,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Hero(
                    tag: 'recipe-image-${recipe.id}',
                    child: imageAsset == null
                        ? RecipeArtwork(
                            recipe: recipe,
                            showReference: true,
                            borderRadius: const BorderRadius.vertical(
                              top: Radius.circular(AppRadii.container),
                            ),
                          )
                        : _PhotoCardArtwork(
                            recipe: recipe,
                            assetPath: imageAsset,
                          ),
                  ),
                  Positioned(
                    right: AppSpacing.small,
                    top: AppSpacing.small,
                    child: DecoratedBox(
                      decoration: BoxDecoration(
                        color: colors.surface.withValues(alpha: 0.88),
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.08),
                            blurRadius: 14,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: AnimatedFavoriteButton(
                        isFavorite: isFavorite,
                        onPressed: onFavoritePressed,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(
                  AppSpacing.medium,
                  14,
                  AppSpacing.medium,
                  AppSpacing.medium,
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      recipe.title,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: theme.textTheme.titleLarge,
                    ),
                    const Spacer(),
                    Wrap(
                      spacing: AppSpacing.small,
                      runSpacing: AppSpacing.xSmall,
                      children: [
                        _MetaPill(
                          icon: Icons.schedule_rounded,
                          label:
                              '${recipe.prepMinutes + recipe.cookMinutes} min',
                        ),
                        _MetaPill(
                          icon: Icons.signal_cellular_alt_rounded,
                          label: _difficultyLabel(l10n),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _MetaPill extends StatelessWidget {
  const _MetaPill({
    required this.icon,
    required this.label,
  });

  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 10,
        vertical: 6,
      ),
      decoration: BoxDecoration(
        color: colors.surfaceContainer,
        borderRadius: BorderRadius.circular(AppRadii.pill),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 15, color: colors.primary),
          const SizedBox(width: 5),
          Text(
            label,
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  fontWeight: FontWeight.w700,
                ),
          ),
        ],
      ),
    );
  }
}


class _PhotoCardArtwork extends StatelessWidget {
  const _PhotoCardArtwork({
    required this.recipe,
    required this.assetPath,
  });

  final Recipe recipe;
  final String assetPath;

  @override
  Widget build(BuildContext context) {
    final match = RegExp(r'(\d+)$').firstMatch(recipe.id);
    final ordinal = int.tryParse(match?.group(1) ?? '') ?? 1;

    return ClipRRect(
      borderRadius: const BorderRadius.vertical(
        top: Radius.circular(AppRadii.container),
      ),
      child: Stack(
        fit: StackFit.expand,
        children: [
          Image.asset(
            assetPath,
            fit: BoxFit.cover,
            alignment: Alignment.center,
          ),
          Positioned(
            left: 22,
            top: 18,
            child: Text(
              ordinal.toString().padLeft(2, '0'),
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 2.2,
                    shadows: const [
                      Shadow(
                        color: Colors.black54,
                        blurRadius: 8,
                      ),
                    ],
                  ),
            ),
          ),
          Positioned(
            left: 20,
            right: 72,
            bottom: 18,
            child: Align(
              alignment: Alignment.bottomLeft,
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 7,
                ),
                decoration: BoxDecoration(
                  color: Colors.black.withValues(alpha: 0.58),
                  borderRadius: BorderRadius.circular(AppRadii.pill),
                ),
                child: Text(
                  recipe.animeSource,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                      ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/theme/app_design_tokens.dart';
import '../../../core/widgets/app_empty_state.dart';
import '../../../core/widgets/app_error_state.dart';
import '../../../l10n/app_localizations.dart';
import '../application/favorites_provider.dart';
import '../../recipes/application/recipe_providers.dart';
import '../../recipes/presentation/screens/recipe_detail_screen.dart';
import '../../recipes/presentation/widgets/recipe_card.dart';

class FavoritesScreen extends ConsumerWidget {
  const FavoritesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final favorites = ref.watch(favoritesProvider);
    final recipes = ref.watch(allRecipesProvider);

    return recipes.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (_, _) => AppErrorState(
        title: l10n.errorTitle,
        retryLabel: l10n.retry,
        onRetry: () => ref.invalidate(allRecipesProvider),
      ),
      data: (allRecipes) {
        final saved = allRecipes
            .where((recipe) => favorites.contains(recipe.id))
            .toList(growable: false);

        if (saved.isEmpty) {
          return AppEmptyState(
            icon: Icons.favorite_border,
            title: l10n.emptyFavoritesTitle,
            body: l10n.emptyFavoritesBody,
          );
        }

        return GridView.builder(
          padding: const EdgeInsets.all(AppSpacing.medium),
          gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
            maxCrossAxisExtent: 420,
            mainAxisExtent: 310,
            crossAxisSpacing: AppSpacing.medium,
            mainAxisSpacing: AppSpacing.medium,
          ),
          itemCount: saved.length,
          itemBuilder: (context, index) {
            final recipe = saved[index];
            return RecipeCard(
              recipe: recipe,
              isFavorite: true,
              onFavoritePressed: () {
                ref.read(favoritesProvider.notifier).toggle(recipe.id);
              },
              onTap: () {
                Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (_) => RecipeDetailScreen(recipe: recipe),
                  ),
                );
              },
            );
          },
        );
      },
    );
  }
}

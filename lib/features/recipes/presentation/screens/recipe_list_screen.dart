import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_staggered_animations/flutter_staggered_animations.dart';

import '../../../../core/theme/app_design_tokens.dart';
import '../../../../core/widgets/app_empty_state.dart';
import '../../../../core/widgets/app_error_state.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../favorites/application/favorites_provider.dart';
import '../../application/recipe_providers.dart';
import '../../domain/recipe.dart';
import '../widgets/recipe_card.dart';
import 'recipe_detail_screen.dart';

class RecipeListScreen extends ConsumerStatefulWidget {
  const RecipeListScreen({super.key});

  @override
  ConsumerState<RecipeListScreen> createState() => _RecipeListScreenState();
}

class _RecipeListScreenState extends ConsumerState<RecipeListScreen> {
  final _searchController = TextEditingController();

  void _resetFilters() {
    _searchController.clear();
    ref.read(searchQueryProvider.notifier).reset();
    ref.read(selectedAnimeProvider.notifier).select(null);
    ref.read(selectedDifficultyProvider.notifier).select(null);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  String _difficultyLabel(
    AppLocalizations l10n,
    RecipeDifficulty difficulty,
  ) {
    return switch (difficulty) {
      RecipeDifficulty.easy => l10n.difficultyEasy,
      RecipeDifficulty.medium => l10n.difficultyMedium,
      RecipeDifficulty.hard => l10n.difficultyHard,
    };
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final filtered = ref.watch(filteredRecipesProvider);
    final animeSources = ref.watch(animeSourcesProvider);
    final selectedAnime = ref.watch(selectedAnimeProvider);
    final selectedDifficulty = ref.watch(selectedDifficultyProvider);
    final hasActiveFilters = ref.watch(hasActiveRecipeFiltersProvider);
    final favorites = ref.watch(favoritesProvider);

    return SafeArea(
      top: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(
          AppSpacing.medium,
          AppSpacing.small,
          AppSpacing.medium,
          0,
        ),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    onChanged: ref.read(searchQueryProvider.notifier).setQuery,
                    textInputAction: TextInputAction.search,
                    decoration: InputDecoration(
                      hintText: l10n.searchHint,
                      prefixIcon: const Icon(Icons.search),
                    ),
                  ),
                ),
                if (hasActiveFilters) ...[
                  const SizedBox(width: AppSpacing.small),
                  IconButton(
                    onPressed: _resetFilters,
                    tooltip: l10n.resetFilters,
                    icon: const Icon(Icons.filter_alt_off),
                  ),
                ],
              ],
            ),
            const SizedBox(height: AppSpacing.small),
            SizedBox(
              height: 44,
              child: animeSources.when(
                data: (items) => ListView(
                  scrollDirection: Axis.horizontal,
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(right: AppSpacing.small),
                      child: FilterChip(
                        selected: selectedAnime == null,
                        label: Text(l10n.filterAllAnime),
                        onSelected: (_) {
                          ref.read(selectedAnimeProvider.notifier).select(null);
                        },
                      ),
                    ),
                    for (final source in items)
                      Padding(
                        padding: const EdgeInsets.only(right: AppSpacing.small),
                        child: FilterChip(
                          selected: selectedAnime == source,
                          label: Text(source),
                          onSelected: (_) {
                            ref
                                .read(selectedAnimeProvider.notifier)
                                .select(source);
                          },
                        ),
                      ),
                  ],
                ),
                loading: () => const SizedBox.shrink(),
                error: (_, _) => const SizedBox.shrink(),
              ),
            ),
            const SizedBox(height: AppSpacing.small),
            SizedBox(
              height: 44,
              child: ListView(
                scrollDirection: Axis.horizontal,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(right: AppSpacing.small),
                    child: FilterChip(
                      selected: selectedDifficulty == null,
                      label: Text(l10n.filterAllDifficulty),
                      onSelected: (_) {
                        ref
                            .read(selectedDifficultyProvider.notifier)
                            .select(null);
                      },
                    ),
                  ),
                  for (final difficulty in RecipeDifficulty.values)
                    Padding(
                      padding: const EdgeInsets.only(right: AppSpacing.small),
                      child: FilterChip(
                        selected: selectedDifficulty == difficulty,
                        label: Text(_difficultyLabel(l10n, difficulty)),
                        onSelected: (_) {
                          ref
                              .read(selectedDifficultyProvider.notifier)
                              .select(difficulty);
                        },
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.medium),
            Expanded(
              child: filtered.when(
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),
                error: (_, _) => AppErrorState(
                  title: l10n.errorTitle,
                  retryLabel: l10n.retry,
                  onRetry: () => ref.invalidate(allRecipesProvider),
                ),
                data: (recipes) {
                  if (recipes.isEmpty) {
                    return AppEmptyState(
                      icon: hasActiveFilters
                          ? Icons.search_off
                          : Icons.menu_book_outlined,
                      title: hasActiveFilters
                          ? l10n.noResultsTitle
                          : l10n.emptyCatalogTitle,
                      body: hasActiveFilters
                          ? l10n.noResultsBody
                          : l10n.emptyCatalogBody,
                    );
                  }

                  return AnimationLimiter(
                    child: GridView.builder(
                      padding: const EdgeInsets.only(
                        bottom: AppSpacing.xLarge,
                      ),
                      gridDelegate:
                          const SliverGridDelegateWithMaxCrossAxisExtent(
                        maxCrossAxisExtent: 420,
                        mainAxisExtent: 310,
                        crossAxisSpacing: AppSpacing.medium,
                        mainAxisSpacing: AppSpacing.medium,
                      ),
                      itemCount: recipes.length,
                      itemBuilder: (context, index) {
                        final recipe = recipes[index];
                        return AnimationConfiguration.staggeredGrid(
                          position: index,
                          columnCount: 2,
                          duration: const Duration(milliseconds: 360),
                          child: SlideAnimation(
                            verticalOffset: 28,
                            child: FadeInAnimation(
                              child: RecipeCard(
                                recipe: recipe,
                                isFavorite: favorites.contains(recipe.id),
                                onFavoritePressed: () {
                                  ref
                                      .read(favoritesProvider.notifier)
                                      .toggle(recipe.id);
                                },
                                onTap: () {
                                  Navigator.of(context).push(
                                    MaterialPageRoute<void>(
                                      builder: (_) => RecipeDetailScreen(
                                        recipe: recipe,
                                      ),
                                    ),
                                  );
                                },
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

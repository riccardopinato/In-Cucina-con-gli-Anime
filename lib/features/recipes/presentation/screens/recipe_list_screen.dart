import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/decorative_characters/decorative_character_registry.dart';
import '../../../../core/decorative_characters/decorative_character_stage.dart';
import '../../../../core/theme/app_design_tokens.dart';
import '../../../../core/theme/app_palette.dart';
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
    final colors = Theme.of(context).colorScheme;

    return SafeArea(
      top: false,
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              colors.surface,
              colors.surfaceContainerLowest,
            ],
          ),
        ),
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(
                    maxWidth: AppLayout.contentMaxWidth,
                  ),
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(
                      AppSpacing.medium,
                      AppSpacing.large,
                      AppSpacing.medium,
                      AppSpacing.medium,
                    ),
                    child: _ExploreHeader(l10n: l10n),
                  ),
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(
                    maxWidth: AppLayout.contentMaxWidth,
                  ),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.medium,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: _searchController,
                                onChanged: ref
                                    .read(searchQueryProvider.notifier)
                                    .setQuery,
                                textInputAction: TextInputAction.search,
                                decoration: InputDecoration(
                                  hintText: l10n.searchHint,
                                  prefixIcon:
                                      const Icon(Icons.search_rounded),
                                ),
                              ),
                            ),
                            if (hasActiveFilters) ...[
                              const SizedBox(width: AppSpacing.small),
                              IconButton.filledTonal(
                                onPressed: _resetFilters,
                                tooltip: l10n.resetFilters,
                                icon:
                                    const Icon(Icons.filter_alt_off_rounded),
                              ),
                            ],
                          ],
                        ),
                        const SizedBox(height: AppSpacing.medium),
                        _FilterRail(
                          children: [
                            FilterChip(
                              selected: selectedAnime == null,
                              label: Text(l10n.filterAllAnime),
                              onSelected: (_) {
                                ref
                                    .read(selectedAnimeProvider.notifier)
                                    .select(null);
                              },
                            ),
                            ...animeSources.maybeWhen(
                              data: (items) => [
                                for (final source in items)
                                  FilterChip(
                                    selected: selectedAnime == source,
                                    label: Text(source),
                                    onSelected: (_) {
                                      ref
                                          .read(
                                            selectedAnimeProvider.notifier,
                                          )
                                          .select(source);
                                    },
                                  ),
                              ],
                              orElse: () => const <Widget>[],
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.small),
                        _FilterRail(
                          children: [
                            FilterChip(
                              selected: selectedDifficulty == null,
                              label: Text(l10n.filterAllDifficulty),
                              onSelected: (_) {
                                ref
                                    .read(
                                      selectedDifficultyProvider.notifier,
                                    )
                                    .select(null);
                              },
                            ),
                            for (final difficulty
                                in RecipeDifficulty.values)
                              FilterChip(
                                selected:
                                    selectedDifficulty == difficulty,
                                label: Text(
                                  _difficultyLabel(l10n, difficulty),
                                ),
                                onSelected: (_) {
                                  ref
                                      .read(
                                        selectedDifficultyProvider.notifier,
                                      )
                                      .select(difficulty);
                                },
                              ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.large),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            filtered.when(
              loading: () => const SliverFillRemaining(
                hasScrollBody: false,
                child: Center(child: CircularProgressIndicator()),
              ),
              error: (_, _) => SliverFillRemaining(
                hasScrollBody: false,
                child: AppErrorState(
                  title: l10n.errorTitle,
                  retryLabel: l10n.retry,
                  onRetry: () => ref.invalidate(allRecipesProvider),
                ),
              ),
              data: (recipes) {
                if (recipes.isEmpty) {
                  return SliverFillRemaining(
                    hasScrollBody: false,
                    child: AppEmptyState(
                      icon: hasActiveFilters
                          ? Icons.search_off_rounded
                          : Icons.menu_book_outlined,
                      title: hasActiveFilters
                          ? l10n.noResultsTitle
                          : l10n.emptyCatalogTitle,
                      body: hasActiveFilters
                          ? l10n.noResultsBody
                          : l10n.emptyCatalogBody,
                    ),
                  );
                }

                return SliverPadding(
                  padding: const EdgeInsets.fromLTRB(
                    AppSpacing.medium,
                    0,
                    AppSpacing.medium,
                    AppSpacing.xxxLarge,
                  ),
                  sliver: SliverGrid(
                    gridDelegate:
                        const SliverGridDelegateWithMaxCrossAxisExtent(
                      maxCrossAxisExtent: 390,
                      mainAxisExtent: 322,
                      crossAxisSpacing: AppSpacing.medium,
                      mainAxisSpacing: AppSpacing.medium,
                    ),
                    delegate: SliverChildBuilderDelegate(
                      (context, index) {
                        final recipe = recipes[index];
                        return Center(
                          child: ConstrainedBox(
                            constraints: const BoxConstraints(
                              maxWidth: 390,
                            ),
                            child: RecipeCard(
                              recipe: recipe,
                              isFavorite:
                                  favorites.contains(recipe.id),
                              onFavoritePressed: () {
                                ref
                                    .read(favoritesProvider.notifier)
                                    .toggle(recipe.id);
                              },
                              onTap: () {
                                Navigator.of(context).push(
                                  MaterialPageRoute<void>(
                                    builder: (_) =>
                                        RecipeDetailScreen(
                                      recipe: recipe,
                                    ),
                                  ),
                                );
                              },
                            ),
                          ),
                        );
                      },
                      childCount: recipes.length,
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _ExploreHeader extends StatelessWidget {
  const _ExploreHeader({required this.l10n});

  final AppLocalizations l10n;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.xLarge),
      decoration: BoxDecoration(
        color: colors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(AppRadii.hero),
        border: Border.all(
          color: colors.outlineVariant.withValues(alpha: 0.62),
        ),
      ),
      child: Stack(
        children: [
          Positioned(
            right: -26,
            top: -42,
            child: Container(
              width: 156,
              height: 156,
              decoration: BoxDecoration(
                color: (isDark
                        ? colors.primaryContainer
                        : AppPalette.apricot)
                    .withValues(alpha: 0.62),
                shape: BoxShape.circle,
              ),
            ),
          ),
          Positioned(
            right: 42,
            bottom: -74,
            child: Container(
              width: 128,
              height: 128,
              decoration: BoxDecoration(
                border: Border.all(
                  color: colors.primary.withValues(alpha: 0.14),
                  width: 18,
                ),
                shape: BoxShape.circle,
              ),
            ),
          ),
          LayoutBuilder(
            builder: (context, constraints) {
              final wide = constraints.maxWidth >= 620;

              if (wide) {
                return Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                      child: _ExploreHeaderCopy(
                        l10n: l10n,
                        colors: colors,
                      ),
                    ),
                    const SizedBox(width: AppSpacing.large),
                    const DecorativeCharacterStage(
                      slot: DecorativeSlot.exploreHero,
                      size: 142,
                    ),
                  ],
                );
              }

              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        child: _BrandPill(
                          label: l10n.appName,
                          colors: colors,
                        ),
                      ),
                      const SizedBox(width: AppSpacing.small),
                      const DecorativeCharacterStage(
                        slot: DecorativeSlot.exploreHero,
                        size: 78,
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.medium),
                  Text(
                    l10n.exploreTagline,
                    style: theme.textTheme.displayMedium,
                  ),
                  const SizedBox(height: AppSpacing.small),
                  Text(
                    l10n.exploreIntro,
                    style: theme.textTheme.bodyLarge?.copyWith(
                      color: colors.onSurfaceVariant,
                      height: 1.45,
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}

class _ExploreHeaderCopy extends StatelessWidget {
  const _ExploreHeaderCopy({
    required this.l10n,
    required this.colors,
  });

  final AppLocalizations l10n;
  final ColorScheme colors;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 720),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _BrandPill(
            label: l10n.appName,
            colors: colors,
          ),
          const SizedBox(height: AppSpacing.large),
          Text(
            l10n.exploreTagline,
            style: theme.textTheme.displayMedium,
          ),
          const SizedBox(height: AppSpacing.small),
          Text(
            l10n.exploreIntro,
            style: theme.textTheme.bodyLarge?.copyWith(
              color: colors.onSurfaceVariant,
              height: 1.45,
            ),
          ),
        ],
      ),
    );
  }
}

class _BrandPill extends StatelessWidget {
  const _BrandPill({
    required this.label,
    required this.colors,
  });

  final String label;
  final ColorScheme colors;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 12,
        vertical: 7,
      ),
      decoration: BoxDecoration(
        color: colors.primary.withValues(alpha: 0.10),
        borderRadius: BorderRadius.circular(AppRadii.pill),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.restaurant_menu_rounded,
            size: 17,
            color: colors.primary,
          ),
          const SizedBox(width: 7),
          Flexible(
            child: Text(
              label,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                    color: colors.primary,
                  ),
            ),
          ),
        ],
      ),
    );
  }
}

class _FilterRail extends StatelessWidget {
  const _FilterRail({required this.children});

  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 42,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: children.length,
        separatorBuilder: (_, _) =>
            const SizedBox(width: AppSpacing.small),
        itemBuilder: (_, index) => children[index],
      ),
    );
  }
}

import 'package:flutter/material.dart';

import '../../../../core/theme/app_design_tokens.dart';
import '../../../../l10n/app_localizations.dart';
import '../../domain/recipe.dart';
import '../widgets/cooking_timer_widget.dart';

class RecipeDetailScreen extends StatefulWidget {
  const RecipeDetailScreen({
    super.key,
    required this.recipe,
  });

  final Recipe recipe;

  @override
  State<RecipeDetailScreen> createState() => _RecipeDetailScreenState();
}

class _RecipeDetailScreenState extends State<RecipeDetailScreen> {
  late List<bool> _checkedIngredients;

  @override
  void initState() {
    super.initState();
    _checkedIngredients = List<bool>.filled(
      widget.recipe.ingredients.length,
      false,
    );
  }

  String _difficultyLabel(AppLocalizations l10n) {
    return switch (widget.recipe.difficulty) {
      RecipeDifficulty.easy => l10n.difficultyEasy,
      RecipeDifficulty.medium => l10n.difficultyMedium,
      RecipeDifficulty.hard => l10n.difficultyHard,
    };
  }

  @override
  Widget build(BuildContext context) {
    final recipe = widget.recipe;
    final l10n = AppLocalizations.of(context)!;
    final colors = Theme.of(context).colorScheme;

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar.large(
            pinned: true,
            expandedHeight: 320,
            flexibleSpace: FlexibleSpaceBar(
              title: Text(
                recipe.title,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              background: Hero(
                tag: 'recipe-image-${recipe.id}',
                child: recipe.imageAsset == null
                    ? DecoratedBox(
                        decoration: BoxDecoration(
                          color: colors.tertiaryContainer,
                        ),
                        child: Icon(
                          Icons.ramen_dining,
                          size: 96,
                          color: colors.onTertiaryContainer,
                        ),
                      )
                    : Image.asset(recipe.imageAsset!, fit: BoxFit.cover),
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
                  padding: const EdgeInsets.all(AppSpacing.medium),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Wrap(
                        spacing: AppSpacing.small,
                        runSpacing: AppSpacing.small,
                        children: [
                          Chip(
                            avatar: const Icon(Icons.movie_outlined, size: 18),
                            label: Text(recipe.animeSource),
                          ),
                          Chip(
                            avatar: const Icon(Icons.schedule, size: 18),
                            label: Text(
                              '${recipe.prepMinutes + recipe.cookMinutes} min',
                            ),
                          ),
                          Chip(
                            avatar: const Icon(Icons.bar_chart, size: 18),
                            label: Text(_difficultyLabel(l10n)),
                          ),
                        ],
                      ),
                      if (recipe.cookMinutes > 0) ...[
                        const SizedBox(height: AppSpacing.large),
                        CookingTimerWidget(minutes: recipe.cookMinutes),
                      ],
                      const SizedBox(height: AppSpacing.xLarge),
                      Text(
                        l10n.ingredientsTitle,
                        style: Theme.of(context).textTheme.headlineMedium,
                      ),
                      const SizedBox(height: AppSpacing.small),
                      ...List.generate(recipe.ingredients.length, (index) {
                        return CheckboxListTile(
                          value: _checkedIngredients[index],
                          contentPadding: EdgeInsets.zero,
                          title: Text(recipe.ingredients[index]),
                          controlAffinity: ListTileControlAffinity.leading,
                          onChanged: (value) {
                            setState(() {
                              _checkedIngredients[index] = value ?? false;
                            });
                          },
                        );
                      }),
                      const SizedBox(height: AppSpacing.xLarge),
                      Text(
                        l10n.stepsTitle,
                        style: Theme.of(context).textTheme.headlineMedium,
                      ),
                      const SizedBox(height: AppSpacing.medium),
                      ...List.generate(recipe.steps.length, (index) {
                        return Padding(
                          padding: const EdgeInsets.only(
                            bottom: AppSpacing.medium,
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              CircleAvatar(
                                radius: 18,
                                backgroundColor: colors.secondaryContainer,
                                foregroundColor: colors.onSecondaryContainer,
                                child: Text('${index + 1}'),
                              ),
                              const SizedBox(width: AppSpacing.medium),
                              Expanded(
                                child: Text(
                                  recipe.steps[index],
                                  style: Theme.of(context).textTheme.bodyLarge,
                                ),
                              ),
                            ],
                          ),
                        );
                      }),
                      const SizedBox(height: AppSpacing.xxLarge),
                    ],
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

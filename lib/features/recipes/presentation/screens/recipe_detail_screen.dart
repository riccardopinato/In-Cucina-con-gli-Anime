import 'package:flutter/material.dart';

import '../../../../core/theme/app_design_tokens.dart';
import '../../../../l10n/app_localizations.dart';
import '../../domain/recipe.dart';
import '../widgets/cooking_timer_widget.dart';
import '../widgets/recipe_artwork.dart';
import '../widgets/recipe_pilot_artwork.dart';

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
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final pilotAsset = pilotRecipeArtworkFor(recipe.id);
    final imageAsset = recipe.imageAsset ?? pilotAsset;

    final ingredients = _IngredientsPanel(
      recipe: recipe,
      checked: _checkedIngredients,
      onChanged: (index, value) {
        setState(() {
          _checkedIngredients[index] = value;
        });
      },
    );

    final steps = _StepsPanel(recipe: recipe);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            pinned: true,
            stretch: true,
            expandedHeight: imageAsset == null ? 390 : 520,
            title: Text(
              recipe.title,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            flexibleSpace: FlexibleSpaceBar(
              collapseMode: CollapseMode.parallax,
              background: Hero(
                tag: 'recipe-image-${recipe.id}',
                child: imageAsset == null
                    ? RecipeArtwork(
                        recipe: recipe,
                        showReference: true,
                      )
                    : ColoredBox(
                        color: colors.surface,
                        child: Center(
                          child: Image.asset(
                            imageAsset,
                            fit: BoxFit.contain,
                            alignment: Alignment.center,
                          ),
                        ),
                      ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(
                  maxWidth: AppLayout.detailMaxWidth,
                ),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(
                    AppSpacing.medium,
                    AppSpacing.xLarge,
                    AppSpacing.medium,
                    AppSpacing.xxxLarge,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(
                        recipe.title,
                        style: theme.textTheme.headlineLarge,
                      ),
                      const SizedBox(height: AppSpacing.small),
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Icon(
                            Icons.auto_awesome_rounded,
                            size: 19,
                            color: colors.secondary,
                          ),
                          const SizedBox(width: AppSpacing.small),
                          Expanded(
                            child: Text(
                              '${l10n.animeReferenceLabel}: '
                              '${recipe.animeSource}',
                              style: theme.textTheme.bodyLarge?.copyWith(
                                color: colors.onSurfaceVariant,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.xLarge),
                      Wrap(
                        spacing: AppSpacing.small,
                        runSpacing: AppSpacing.small,
                        children: [
                          _FactTile(
                            icon: Icons.timer_outlined,
                            label: l10n.prepTimeLabel,
                            value: '${recipe.prepMinutes} min',
                          ),
                          _FactTile(
                            icon: Icons.local_fire_department_outlined,
                            label: l10n.cookTimeLabel,
                            value: '${recipe.cookMinutes} min',
                          ),
                          _FactTile(
                            icon: Icons.signal_cellular_alt_rounded,
                            label: l10n.difficultyLabel,
                            value: _difficultyLabel(l10n),
                          ),
                          _FactTile(
                            icon: Icons.people_alt_outlined,
                            label: l10n.servingsLabel,
                            value: '${recipe.servings}',
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.xLarge),
                      LayoutBuilder(
                        builder: (context, constraints) {
                          final wide = constraints.maxWidth >= 820;
                          final timer = recipe.cookMinutes > 0
                              ? CookingTimerWidget(
                                  minutes: recipe.cookMinutes,
                                )
                              : null;

                          if (!wide) {
                            return Column(
                              crossAxisAlignment:
                                  CrossAxisAlignment.stretch,
                              children: [
                                if (timer != null) ...[
                                  timer,
                                  const SizedBox(
                                    height: AppSpacing.large,
                                  ),
                                ],
                                ingredients,
                                const SizedBox(
                                  height: AppSpacing.large,
                                ),
                                steps,
                              ],
                            );
                          }

                          return Row(
                            crossAxisAlignment:
                                CrossAxisAlignment.start,
                            children: [
                              Expanded(
                                flex: 4,
                                child: Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                  children: [
                                    if (timer != null) ...[
                                      timer,
                                      const SizedBox(
                                        height: AppSpacing.large,
                                      ),
                                    ],
                                    ingredients,
                                  ],
                                ),
                              ),
                              const SizedBox(
                                width: AppSpacing.large,
                              ),
                              Expanded(
                                flex: 6,
                                child: steps,
                              ),
                            ],
                          );
                        },
                      ),
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

class _FactTile extends StatelessWidget {
  const _FactTile({
    required this.icon,
    required this.label,
    required this.value,
  });

  final IconData icon;
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Container(
      constraints: const BoxConstraints(minWidth: 132),
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.medium,
        vertical: 13,
      ),
      decoration: BoxDecoration(
        color: colors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(
          color: colors.outlineVariant.withValues(alpha: 0.70),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 20, color: colors.primary),
          const SizedBox(width: AppSpacing.small),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: theme.textTheme.labelSmall?.copyWith(
                  color: colors.onSurfaceVariant,
                ),
              ),
              Text(
                value,
                style: theme.textTheme.titleSmall?.copyWith(
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _IngredientsPanel extends StatelessWidget {
  const _IngredientsPanel({
    required this.recipe,
    required this.checked,
    required this.onChanged,
  });

  final Recipe recipe;
  final List<bool> checked;
  final void Function(int index, bool value) onChanged;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.large),
      decoration: BoxDecoration(
        color: colors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(AppRadii.container),
        border: Border.all(
          color: colors.outlineVariant.withValues(alpha: 0.70),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _SectionHeading(
            icon: Icons.shopping_basket_outlined,
            title: l10n.ingredientsTitle,
          ),
          const SizedBox(height: AppSpacing.medium),
          for (var index = 0;
              index < recipe.ingredients.length;
              index++) ...[
            _IngredientRow(
              text: recipe.ingredients[index].displayText,
              checked: checked[index],
              onChanged: (value) => onChanged(index, value),
            ),
            if (index != recipe.ingredients.length - 1)
              Divider(
                height: 1,
                indent: 48,
                color: colors.outlineVariant.withValues(alpha: 0.55),
              ),
          ],
        ],
      ),
    );
  }
}

class _IngredientRow extends StatelessWidget {
  const _IngredientRow({
    required this.text,
    required this.checked,
    required this.onChanged,
  });

  final String text;
  final bool checked;
  final ValueChanged<bool> onChanged;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return InkWell(
      borderRadius: BorderRadius.circular(AppRadii.small),
      onTap: () => onChanged(!checked),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 7),
        child: Row(
          children: [
            Checkbox(
              value: checked,
              onChanged: (value) => onChanged(value ?? false),
            ),
            const SizedBox(width: AppSpacing.small),
            Expanded(
              child: AnimatedDefaultTextStyle(
                duration: AppMotion.feedback,
                style: theme.textTheme.bodyMedium!.copyWith(
                  color: checked
                      ? colors.onSurfaceVariant
                      : colors.onSurface,
                  decoration:
                      checked ? TextDecoration.lineThrough : null,
                ),
                child: Text(text),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StepsPanel extends StatelessWidget {
  const _StepsPanel({required this.recipe});

  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final colors = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.large),
      decoration: BoxDecoration(
        color: colors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(AppRadii.container),
        border: Border.all(
          color: colors.outlineVariant.withValues(alpha: 0.70),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _SectionHeading(
            icon: Icons.menu_book_outlined,
            title: l10n.stepsTitle,
          ),
          const SizedBox(height: AppSpacing.large),
          for (var index = 0;
              index < recipe.steps.length;
              index++)
            Padding(
              padding: EdgeInsets.only(
                bottom: index == recipe.steps.length - 1
                    ? 0
                    : AppSpacing.medium,
              ),
              child: _StepCard(
                number: index + 1,
                step: recipe.steps[index],
              ),
            ),
        ],
      ),
    );
  }
}

class _StepCard extends StatelessWidget {
  const _StepCard({
    required this.number,
    required this.step,
  });

  final int number;
  final RecipeStep step;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final minutes = step.timerSeconds == null
        ? null
        : (step.timerSeconds! / 60).ceil();

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 42,
          height: 42,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: colors.secondary.withValues(alpha: 0.14),
            shape: BoxShape.circle,
          ),
          child: Text(
            number.toString().padLeft(2, '0'),
            style: theme.textTheme.labelLarge?.copyWith(
              color: colors.secondary,
              fontWeight: FontWeight.w900,
            ),
          ),
        ),
        const SizedBox(width: AppSpacing.medium),
        Expanded(
          child: Container(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.medium,
              13,
              AppSpacing.medium,
              AppSpacing.medium,
            ),
            decoration: BoxDecoration(
              color: colors.surfaceContainerLow,
              borderRadius: BorderRadius.circular(AppRadii.card),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (minutes != null && minutes > 0) ...[
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 9,
                      vertical: 5,
                    ),
                    decoration: BoxDecoration(
                      color: colors.primary.withValues(alpha: 0.09),
                      borderRadius:
                          BorderRadius.circular(AppRadii.pill),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.timer_outlined,
                          size: 15,
                          color: colors.primary,
                        ),
                        const SizedBox(width: 5),
                        Text(
                          '$minutes min',
                          style: theme.textTheme.labelSmall?.copyWith(
                            color: colors.primary,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.small),
                ],
                Text(
                  step.text,
                  style: theme.textTheme.bodyLarge?.copyWith(
                    height: 1.48,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _SectionHeading extends StatelessWidget {
  const _SectionHeading({
    required this.icon,
    required this.title,
  });

  final IconData icon;
  final String title;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Row(
      children: [
        Container(
          width: 38,
          height: 38,
          decoration: BoxDecoration(
            color: colors.primary.withValues(alpha: 0.10),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, size: 20, color: colors.primary),
        ),
        const SizedBox(width: AppSpacing.small),
        Expanded(
          child: Text(
            title,
            style: theme.textTheme.headlineMedium,
          ),
        ),
      ],
    );
  }
}

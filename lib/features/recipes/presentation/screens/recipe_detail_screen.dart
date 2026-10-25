import 'package:flutter/material.dart';

import '../../../../core/theme/app_design_tokens.dart';
import '../../../../core/widgets/motion_entrance.dart';
import '../../../../l10n/app_localizations.dart';
import '../../domain/recipe.dart';
import '../widgets/cooking_timer_widget.dart';
import '../widgets/recipe_artwork.dart';

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

  String _animeRelationLabel(
    AppLocalizations l10n,
    RecipeAnimeRelation relation,
  ) {
    return switch (relation) {
      RecipeAnimeRelation.verifiedAppearance => l10n.animeRelationVerified,
      RecipeAnimeRelation.recurringAssociation => l10n.animeRelationRecurring,
      RecipeAnimeRelation.inspired => l10n.animeRelationInspired,
      RecipeAnimeRelation.unverified => l10n.animeReferenceLabel,
    };
  }

  String? _animeLocation(
    AppLocalizations l10n,
    RecipeAnimeReference reference,
  ) {
    final parts = <String>[
      if (reference.season != null)
        '${l10n.animeSeasonLabel} ${reference.season}',
      if (reference.episode != null && reference.episode!.trim().isNotEmpty)
        '${l10n.animeEpisodeLabel} ${reference.episode!.trim()}',
      if (reference.chapter != null && reference.chapter!.trim().isNotEmpty)
        '${l10n.animeChapterLabel} ${reference.chapter!.trim()}',
    ];
    return parts.isEmpty ? null : parts.join(' · ');
  }

  @override
  Widget build(BuildContext context) {
    final recipe = widget.recipe;
    final l10n = AppLocalizations.of(context)!;
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final imageAsset = recipe.imageAsset;
    final primaryAnimeReference = recipe.animeReferences.isEmpty
        ? null
        : recipe.animeReferences.first;

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
            child: MotionEntrance(
              child: ${expr},
            ),
          ),
        ],
      ),
    );
  }
}

class _AnimeContextPanel extends StatelessWidget {
  const _AnimeContextPanel({
    required this.title,
    required this.contextText,
    required this.reference,
    required this.relationLabel,
    required this.location,
  });

  final String title;
  final String? contextText;
  final RecipeAnimeReference? reference;
  final String relationLabel;
  final String? location;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.large),
      decoration: BoxDecoration(
        color: colors.secondaryContainer.withValues(alpha: 0.34),
        borderRadius: BorderRadius.circular(AppRadii.container),
        border: Border.all(
          color: colors.secondary.withValues(alpha: 0.22),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _SectionHeading(
            icon: Icons.movie_filter_outlined,
            title: title,
          ),
          if (reference != null) ...[
            const SizedBox(height: AppSpacing.medium),
            Text(
              reference!.workTitle,
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: AppSpacing.xSmall),
            Wrap(
              spacing: AppSpacing.small,
              runSpacing: AppSpacing.xSmall,
              children: [
                Chip(
                  label: Text(relationLabel),
                  visualDensity: VisualDensity.compact,
                ),
                if (location != null)
                  Chip(
                    label: Text(location!),
                    visualDensity: VisualDensity.compact,
                  ),
              ],
            ),
          ],
          if (contextText != null && contextText!.trim().isNotEmpty) ...[
            const SizedBox(height: AppSpacing.medium),
            Text(
              contextText!,
              style: theme.textTheme.bodyMedium?.copyWith(
                height: 1.5,
                color: colors.onSurfaceVariant,
              ),
            ),
          ],
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

class _IngredientRow extends StatefulWidget {
  const _IngredientRow({
    required this.text,
    required this.checked,
    required this.onChanged,
  });

  final String text;
  final bool checked;
  final ValueChanged<bool> onChanged;

  @override
  State<_IngredientRow> createState() => _IngredientRowState();
}

class _IngredientRowState extends State<_IngredientRow>
    with SingleTickerProviderStateMixin {
  late final AnimationController _checkController;
  late final Animation<double> _checkScale;

  @override
  void initState() {
    super.initState();
    _checkController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 240),
    );
    _checkScale = TweenSequence<double>([
      TweenSequenceItem(
        tween: Tween<double>(begin: 1, end: 1.16)
            .chain(CurveTween(curve: Curves.easeOutCubic)),
        weight: 45,
      ),
      TweenSequenceItem(
        tween: Tween<double>(begin: 1.16, end: 1)
            .chain(CurveTween(curve: Curves.easeOutBack)),
        weight: 55,
      ),
    ]).animate(_checkController);
  }

  @override
  void didUpdateWidget(covariant _IngredientRow oldWidget) {
    super.didUpdateWidget(oldWidget);
    final reduceMotion =
        MediaQuery.maybeOf(context)?.disableAnimations ?? false;

    if (!reduceMotion && !oldWidget.checked && widget.checked) {
      _checkController.forward(from: 0);
    }
  }

  @override
  void dispose() {
    _checkController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final reduceMotion =
        MediaQuery.maybeOf(context)?.disableAnimations ?? false;

    return InkWell(
      borderRadius: BorderRadius.circular(AppRadii.small),
      onTap: () => widget.onChanged(!widget.checked),
      child: AnimatedContainer(
        duration: reduceMotion ? Duration.zero : AppMotion.feedback,
        curve: AppMotion.standardCurve,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.xSmall,
          vertical: 7,
        ),
        decoration: BoxDecoration(
          color: widget.checked
              ? colors.primary.withValues(alpha: 0.055)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(AppRadii.small),
        ),
        child: Row(
          children: [
            ScaleTransition(
              scale: reduceMotion
                  ? const AlwaysStoppedAnimation<double>(1)
                  : _checkScale,
              child: Checkbox(
                value: widget.checked,
                onChanged: (value) =>
                    widget.onChanged(value ?? false),
              ),
            ),
            const SizedBox(width: AppSpacing.small),
            Expanded(
              child: AnimatedDefaultTextStyle(
                duration:
                    reduceMotion ? Duration.zero : AppMotion.feedback,
                style: theme.textTheme.bodyMedium!.copyWith(
                  color: widget.checked
                      ? colors.onSurfaceVariant
                      : colors.onSurface,
                  decoration: widget.checked
                      ? TextDecoration.lineThrough
                      : null,
                ),
                child: Text(widget.text),
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

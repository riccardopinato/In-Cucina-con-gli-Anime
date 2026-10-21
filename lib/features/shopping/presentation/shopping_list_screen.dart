import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/theme/app_design_tokens.dart';
import '../../../../core/widgets/app_empty_state.dart';
import '../../../../l10n/app_localizations.dart';
import '../../application/shopping_provider.dart';

class ShoppingListScreen extends ConsumerWidget {
  const ShoppingListScreen({super.key});

  Future<void> _showAddDialog(
    BuildContext context,
    WidgetRef ref,
  ) async {
    final l10n = AppLocalizations.of(context)!;
    final controller = TextEditingController();

    await showDialog<void>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text(l10n.addIngredientTitle),
        content: TextField(
          controller: controller,
          autofocus: true,
          textInputAction: TextInputAction.done,
          decoration: InputDecoration(hintText: l10n.addIngredientHint),
          onSubmitted: (value) {
            if (value.trim().isEmpty) return;
            ref
                .read(shoppingProvider.notifier)
                .addManual(value, l10n.manualItemSource);
            Navigator.of(dialogContext).pop();
          },
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(dialogContext).pop(),
            child: Text(l10n.cancel),
          ),
          FilledButton(
            onPressed: () {
              final value = controller.text;
              if (value.trim().isEmpty) return;
              ref
                  .read(shoppingProvider.notifier)
                  .addManual(value, l10n.manualItemSource);
              Navigator.of(dialogContext).pop();
            },
            child: Text(l10n.addItem),
          ),
        ],
      ),
    );

    controller.dispose();
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final items = ref.watch(shoppingProvider);
    final hasBought = items.any((item) => item.isBought);

    return Scaffold(
      backgroundColor: Colors.transparent,
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAddDialog(context, ref),
        icon: const Icon(Icons.add),
        label: Text(l10n.addItem),
      ),
      body: items.isEmpty
          ? AppEmptyState(
              icon: Icons.shopping_basket_outlined,
              title: l10n.shoppingEmptyTitle,
              body: l10n.shoppingEmptyBody,
            )
          : Column(
              children: [
                if (hasBought)
                  Align(
                    alignment: Alignment.centerRight,
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(
                        AppSpacing.medium,
                        AppSpacing.small,
                        AppSpacing.medium,
                        0,
                      ),
                      child: TextButton.icon(
                        onPressed: () {
                          ref.read(shoppingProvider.notifier).clearBought();
                        },
                        icon: const Icon(Icons.delete_sweep_outlined),
                        label: Text(l10n.clearBought),
                      ),
                    ),
                  ),
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.fromLTRB(
                      AppSpacing.medium,
                      AppSpacing.small,
                      AppSpacing.medium,
                      96,
                    ),
                    itemCount: items.length,
                    itemBuilder: (context, index) {
                      final item = items[index];
                      return Padding(
                        padding: const EdgeInsets.only(
                          bottom: AppSpacing.small,
                        ),
                        child: Dismissible(
                          key: ValueKey(item.id),
                          direction: DismissDirection.endToStart,
                          onDismissed: (_) {
                            ref.read(shoppingProvider.notifier).remove(item.id);
                          },
                          background: Container(
                            alignment: Alignment.centerRight,
                            padding: const EdgeInsets.only(
                              right: AppSpacing.large,
                            ),
                            decoration: BoxDecoration(
                              color: Theme.of(context).colorScheme.errorContainer,
                              borderRadius: BorderRadius.circular(
                                AppRadii.container,
                              ),
                            ),
                            child: Icon(
                              Icons.delete_outline,
                              color: Theme.of(context)
                                  .colorScheme
                                  .onErrorContainer,
                            ),
                          ),
                          child: Card(
                            child: CheckboxListTile(
                              value: item.isBought,
                              controlAffinity: ListTileControlAffinity.leading,
                              title: Text(
                                item.name,
                                style: TextStyle(
                                  decoration: item.isBought
                                      ? TextDecoration.lineThrough
                                      : null,
                                ),
                              ),
                              subtitle: Text(item.recipeSource),
                              onChanged: (_) {
                                ref
                                    .read(shoppingProvider.notifier)
                                    .toggle(item.id);
                              },
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
    );
  }
}

import 'package:flutter/material.dart';

import '../theme/app_design_tokens.dart';

class AppEmptyState extends StatelessWidget {
  const AppEmptyState({
    super.key,
    required this.icon,
    required this.title,
    required this.body,
    this.action,
    this.decoration,
  });

  final IconData icon;
  final String title;
  final String body;
  final Widget? action;
  final Widget? decoration;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 480),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.xLarge),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              decoration ?? Icon(icon, size: 64, color: colors.primary),
              const SizedBox(height: AppSpacing.medium),
              Text(
                title,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              const SizedBox(height: AppSpacing.small),
              Text(
                body,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              if (action != null) ...[
                const SizedBox(height: AppSpacing.large),
                action!,
              ],
            ],
          ),
        ),
      ),
    );
  }
}

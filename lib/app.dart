import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/monetization/purchase_provider.dart';
import 'core/preferences/preferences_providers.dart';
import 'core/preferences/preferences_repository.dart';
import 'core/theme/app_theme.dart';
import 'features/navigation/presentation/main_navigation_screen.dart';
import 'l10n/app_localizations.dart';

class AnimeKitchenApp extends ConsumerWidget {
  const AnimeKitchenApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final localePreference = ref.watch(localePreferenceProvider);
    final themePreference = ref.watch(themePreferenceProvider);
    ref.watch(purchaseControllerProvider);

    final themeMode = switch (themePreference) {
      AppThemePreference.system => ThemeMode.system,
      AppThemePreference.light => ThemeMode.light,
      AppThemePreference.dark => ThemeMode.dark,
    };

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      onGenerateTitle: (context) => AppLocalizations.of(context)!.appName,
      locale: localePreference.locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: themeMode,
      home: const MainNavigationScreen(),
    );
  }
}

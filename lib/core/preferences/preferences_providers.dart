import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/locale_preference.dart';
import '../persistence/shared_preferences_provider.dart';
import 'preferences_repository.dart';
import 'shared_preferences_preferences_repository.dart';

final preferencesRepositoryProvider = Provider<PreferencesRepository>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SharedPreferencesPreferencesRepository(prefs);
});

class LocalePreferenceNotifier extends Notifier<LocalePreference> {
  @override
  LocalePreference build() {
    return ref.watch(preferencesRepositoryProvider).loadLocalePreference();
  }

  void setPreference(LocalePreference preference) {
    state = preference;
    unawaited(
      ref.read(preferencesRepositoryProvider).saveLocalePreference(preference),
    );
  }
}

final localePreferenceProvider =
    NotifierProvider<LocalePreferenceNotifier, LocalePreference>(
  LocalePreferenceNotifier.new,
);

class ThemePreferenceNotifier extends Notifier<AppThemePreference> {
  @override
  AppThemePreference build() {
    return ref.watch(preferencesRepositoryProvider).loadThemePreference();
  }

  void setPreference(AppThemePreference preference) {
    state = preference;
    unawaited(
      ref.read(preferencesRepositoryProvider).saveThemePreference(preference),
    );
  }
}

final themePreferenceProvider =
    NotifierProvider<ThemePreferenceNotifier, AppThemePreference>(
  ThemePreferenceNotifier.new,
);

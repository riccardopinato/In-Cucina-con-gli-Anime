import '../localization/locale_preference.dart';

enum AppThemePreference {
  system,
  light,
  dark,
}

abstract interface class PreferencesRepository {
  LocalePreference loadLocalePreference();
  Future<void> saveLocalePreference(LocalePreference preference);

  AppThemePreference loadThemePreference();
  Future<void> saveThemePreference(AppThemePreference preference);
}

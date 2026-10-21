import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../localization/locale_preference.dart';
import 'preferences_repository.dart';

class SharedPreferencesPreferencesRepository
    implements PreferencesRepository {
  SharedPreferencesPreferencesRepository(this._prefs);

  static const _localeKey = 'app_locale_preference_v1';
  static const _themeKey = 'app_theme_preference_v1';

  final SharedPreferences _prefs;

  @override
  LocalePreference loadLocalePreference() {
    final encoded = _prefs.getString(_localeKey);
    if (encoded == null) return const LocalePreference();

    try {
      final decoded = jsonDecode(encoded);
      if (decoded is! Map<String, dynamic>) {
        return const LocalePreference();
      }
      return LocalePreference.fromJson(decoded);
    } on FormatException {
      return const LocalePreference();
    }
  }

  @override
  Future<void> saveLocalePreference(LocalePreference preference) async {
    await _prefs.setString(_localeKey, jsonEncode(preference.toJson()));
  }

  @override
  AppThemePreference loadThemePreference() {
    final stored = _prefs.getString(_themeKey);
    return AppThemePreference.values.firstWhere(
      (value) => value.name == stored,
      orElse: () => AppThemePreference.system,
    );
  }

  @override
  Future<void> saveThemePreference(AppThemePreference preference) async {
    await _prefs.setString(_themeKey, preference.name);
  }
}

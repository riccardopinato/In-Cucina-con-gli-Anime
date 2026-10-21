import 'package:flutter/widgets.dart';

enum LanguageMode {
  device,
  manual,
}

enum AppLanguage {
  english('en', 'English'),
  italian('it', 'Italiano'),
  spanish('es', 'Español'),
  french('fr', 'Français'),
  german('de', 'Deutsch'),
  portuguese('pt', 'Português');

  const AppLanguage(this.code, this.nativeLabel);

  final String code;
  final String nativeLabel;

  Locale get locale => Locale(code);

  static AppLanguage? fromCode(String? code) {
    if (code == null) return null;
    for (final value in values) {
      if (value.code == code.toLowerCase()) return value;
    }
    return null;
  }
}

import 'package:flutter/widgets.dart';

import 'app_language.dart';

class LocalePreference {
  const LocalePreference({
    this.mode = LanguageMode.device,
    this.language,
  });

  final LanguageMode mode;
  final AppLanguage? language;

  Locale? get locale {
    if (mode == LanguageMode.device) return null;
    return language?.locale ?? const Locale('en');
  }

  Map<String, dynamic> toJson() => {
        'mode': mode.name,
        'language': language?.code,
      };

  factory LocalePreference.fromJson(Map<String, dynamic> json) {
    final mode = LanguageMode.values.firstWhere(
      (value) => value.name == json['mode'],
      orElse: () => LanguageMode.device,
    );

    return LocalePreference(
      mode: mode,
      language: AppLanguage.fromCode(json['language']?.toString()),
    );
  }
}

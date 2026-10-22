import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/localization/app_language.dart';
import '../../../core/localization/locale_preference.dart';
import '../../../core/monetization/consent.dart';
import '../../../core/monetization/consent_provider.dart';
import '../../../core/preferences/preferences_providers.dart';
import '../../../core/preferences/preferences_repository.dart';
import '../../../core/theme/app_design_tokens.dart';
import '../../../l10n/app_localizations.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  String _languageLabel(AppLocalizations l10n, AppLanguage language) {
    return switch (language) {
      AppLanguage.english => l10n.languageEnglish,
      AppLanguage.italian => l10n.languageItalian,
      AppLanguage.spanish => l10n.languageSpanish,
      AppLanguage.french => l10n.languageFrench,
      AppLanguage.german => l10n.languageGerman,
      AppLanguage.portuguese => l10n.languagePortuguese,
    };
  }

  String _themeLabel(
    AppLocalizations l10n,
    AppThemePreference preference,
  ) {
    return switch (preference) {
      AppThemePreference.system => l10n.themeSystem,
      AppThemePreference.light => l10n.themeLight,
      AppThemePreference.dark => l10n.themeDark,
    };
  }

  String _privacyStatusLabel(
    AppLocalizations l10n,
    AdPrivacyPreference preference,
  ) {
    return switch (preference) {
      AdPrivacyPreference.unresolved => l10n.privacyStatusUnresolved,
      AdPrivacyPreference.allowAds => l10n.privacyStatusAllow,
      AdPrivacyPreference.blockAds => l10n.privacyStatusBlock,
    };
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final localePreference = ref.watch(localePreferenceProvider);
    final themePreference = ref.watch(themePreferenceProvider);
    final consentState = ref.watch(consentProvider);

    final selectedPrivacy = consentState.hasLocalChoice
        ? <AdPrivacyPreference>{consentState.localPreference}
        : <AdPrivacyPreference>{};

    return Scaffold(
      appBar: AppBar(title: Text(l10n.settingsTitle)),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.medium),
        children: [
          Text(
            l10n.settingsLanguage,
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppSpacing.small),
          SegmentedButton<LanguageMode>(
            segments: [
              ButtonSegment(
                value: LanguageMode.device,
                icon: const Icon(Icons.phone_android),
                label: Text(l10n.languageDevice),
              ),
              ButtonSegment(
                value: LanguageMode.manual,
                icon: const Icon(Icons.language),
                label: Text(l10n.languageManual),
              ),
            ],
            selected: {localePreference.mode},
            onSelectionChanged: (selection) {
              final mode = selection.single;
              ref.read(localePreferenceProvider.notifier).setPreference(
                    LocalePreference(
                      mode: mode,
                      language: localePreference.language ??
                          AppLanguage.english,
                    ),
                  );
            },
          ),
          if (localePreference.mode == LanguageMode.manual) ...[
            const SizedBox(height: AppSpacing.medium),
            DropdownButtonFormField<AppLanguage>(
              initialValue:
                  localePreference.language ?? AppLanguage.english,
              decoration: InputDecoration(labelText: l10n.settingsLanguage),
              items: AppLanguage.values
                  .map(
                    (language) => DropdownMenuItem(
                      value: language,
                      child: Text(_languageLabel(l10n, language)),
                    ),
                  )
                  .toList(growable: false),
              onChanged: (language) {
                if (language == null) return;
                ref.read(localePreferenceProvider.notifier).setPreference(
                      LocalePreference(
                        mode: LanguageMode.manual,
                        language: language,
                      ),
                    );
              },
            ),
          ],
          const SizedBox(height: AppSpacing.xLarge),
          Text(
            l10n.settingsTheme,
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppSpacing.small),
          SegmentedButton<AppThemePreference>(
            segments: AppThemePreference.values
                .map(
                  (preference) => ButtonSegment(
                    value: preference,
                    label: Text(_themeLabel(l10n, preference)),
                  ),
                )
                .toList(growable: false),
            selected: {themePreference},
            onSelectionChanged: (selection) {
              ref
                  .read(themePreferenceProvider.notifier)
                  .setPreference(selection.single);
            },
          ),
          const SizedBox(height: AppSpacing.xLarge),
          Text(
            l10n.settingsPrivacyAds,
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppSpacing.small),
          Text(
            l10n.privacyAdsDescription,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: AppSpacing.medium),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.privacy_tip_outlined),
            title: Text(l10n.privacyStatusLabel),
            subtitle: Text(
              _privacyStatusLabel(l10n, consentState.localPreference),
            ),
          ),
          SegmentedButton<AdPrivacyPreference>(
            emptySelectionAllowed: true,
            segments: [
              ButtonSegment(
                value: AdPrivacyPreference.allowAds,
                icon: const Icon(Icons.check_circle_outline),
                label: Text(l10n.privacyAllowAds),
              ),
              ButtonSegment(
                value: AdPrivacyPreference.blockAds,
                icon: const Icon(Icons.block_outlined),
                label: Text(l10n.privacyBlockAds),
              ),
            ],
            selected: selectedPrivacy,
            onSelectionChanged: (selection) {
              if (selection.isEmpty) return;
              ref
                  .read(consentProvider.notifier)
                  .setLocalPreference(selection.single);
            },
          ),
          if (consentState.hasLocalChoice)
            Align(
              alignment: Alignment.centerLeft,
              child: TextButton(
                onPressed: () {
                  ref
                      .read(consentProvider.notifier)
                      .resetLocalPreference();
                },
                child: Text(l10n.privacyResetChoice),
              ),
            ),
        ],
      ),
    );
  }
}

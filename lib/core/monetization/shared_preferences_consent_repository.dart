import 'package:shared_preferences/shared_preferences.dart';

import 'consent.dart';
import 'consent_repository.dart';

class SharedPreferencesConsentRepository implements ConsentRepository {
  SharedPreferencesConsentRepository(this._prefs);

  static const _preferenceKey = 'ad_privacy_preference_v1';
  static const _updatedAtKey = 'ad_privacy_preference_updated_at_v1';

  final SharedPreferences _prefs;

  @override
  ConsentState load() {
    final stored = _prefs.getString(_preferenceKey);
    final preference = AdPrivacyPreference.values.firstWhere(
      (value) =>
          value != AdPrivacyPreference.unresolved && value.name == stored,
      orElse: () => AdPrivacyPreference.unresolved,
    );

    if (preference == AdPrivacyPreference.unresolved) {
      return ConsentState.initial;
    }

    final updatedAt = DateTime.tryParse(
      _prefs.getString(_updatedAtKey) ?? '',
    );

    return ConsentState(
      localPreference: preference,
      localUpdatedAt: updatedAt,
      provider: ProviderConsentSnapshot.unresolved,
    );
  }

  @override
  Future<void> saveLocalPreference(AdPrivacyPreference preference) async {
    if (preference == AdPrivacyPreference.unresolved) {
      await clearLocalPreference();
      return;
    }

    await _prefs.setString(_preferenceKey, preference.name);
    await _prefs.setString(
      _updatedAtKey,
      DateTime.now().toUtc().toIso8601String(),
    );
  }

  @override
  Future<void> clearLocalPreference() async {
    await _prefs.remove(_preferenceKey);
    await _prefs.remove(_updatedAtKey);
  }
}

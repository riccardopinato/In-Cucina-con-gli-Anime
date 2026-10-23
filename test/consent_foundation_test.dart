import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:animekitchen/core/monetization/consent.dart';
import 'package:animekitchen/core/monetization/shared_preferences_consent_repository.dart';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test('privacy preference defaults to unresolved and fail-closed', () async {
    final prefs = await SharedPreferences.getInstance();
    final repository = SharedPreferencesConsentRepository(prefs);

    final state = repository.load();

    expect(state.localPreference, AdPrivacyPreference.unresolved);
    expect(state.provider.status, ConsentProviderStatus.unresolved);
    expect(state.canRequestAds, isFalse);
  });

  test('local privacy choice persists without provider eligibility', () async {
    final prefs = await SharedPreferences.getInstance();
    final repository = SharedPreferencesConsentRepository(prefs);

    await repository.saveLocalPreference(AdPrivacyPreference.allowAds);

    final state = repository.load();

    expect(state.localPreference, AdPrivacyPreference.allowAds);
    expect(state.localUpdatedAt, isNotNull);
    expect(state.provider.status, ConsentProviderStatus.unresolved);
    expect(state.canRequestAds, isFalse);
  });

  test('clearing the choice returns to unresolved state', () async {
    final prefs = await SharedPreferences.getInstance();
    final repository = SharedPreferencesConsentRepository(prefs);

    await repository.saveLocalPreference(AdPrivacyPreference.blockAds);
    await repository.clearLocalPreference();

    expect(repository.load().localPreference, AdPrivacyPreference.unresolved);
  });
}

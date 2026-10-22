import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../persistence/shared_preferences_provider.dart';
import 'consent.dart';
import 'consent_repository.dart';
import 'shared_preferences_consent_repository.dart';

final consentRepositoryProvider = Provider<ConsentRepository>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SharedPreferencesConsentRepository(prefs);
});

class ConsentNotifier extends Notifier<ConsentState> {
  @override
  ConsentState build() {
    return ref.watch(consentRepositoryProvider).load();
  }

  void setLocalPreference(AdPrivacyPreference preference) {
    if (preference == AdPrivacyPreference.unresolved) {
      resetLocalPreference();
      return;
    }

    state = ConsentState(
      localPreference: preference,
      localUpdatedAt: DateTime.now().toUtc(),
      provider: state.provider,
    );

    unawaited(
      ref.read(consentRepositoryProvider).saveLocalPreference(preference),
    );
  }

  void resetLocalPreference() {
    state = ConsentState(
      localPreference: AdPrivacyPreference.unresolved,
      localUpdatedAt: null,
      provider: state.provider,
    );

    unawaited(
      ref.read(consentRepositoryProvider).clearLocalPreference(),
    );
  }

  void applyProviderResolution(ProviderConsentSnapshot provider) {
    if (provider.source == ConsentProviderSource.none &&
        provider.status != ConsentProviderStatus.unresolved) {
      throw ArgumentError(
        'Resolved consent provider state requires a trusted source.',
      );
    }

    state = ConsentState(
      localPreference: state.localPreference,
      localUpdatedAt: state.localUpdatedAt,
      provider: provider,
    );
  }

  void clearProviderResolution() {
    state = ConsentState(
      localPreference: state.localPreference,
      localUpdatedAt: state.localUpdatedAt,
      provider: ProviderConsentSnapshot.unresolved,
    );
  }
}

final consentProvider =
    NotifierProvider<ConsentNotifier, ConsentState>(ConsentNotifier.new);

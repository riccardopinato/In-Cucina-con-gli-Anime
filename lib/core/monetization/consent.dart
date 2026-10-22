enum AdPrivacyPreference {
  unresolved,
  allowAds,
  blockAds,
}

enum ConsentProviderStatus {
  unresolved,
  blocked,
  eligible,
}

enum ConsentProviderSource {
  none,
  providerVerified,
  qaOverride,
}

class ProviderConsentSnapshot {
  const ProviderConsentSnapshot({
    required this.status,
    required this.source,
    required this.resolvedAt,
    this.privacyOptionsRequired = false,
  });

  final ConsentProviderStatus status;
  final ConsentProviderSource source;
  final DateTime? resolvedAt;
  final bool privacyOptionsRequired;

  bool get canRequestAds =>
      status == ConsentProviderStatus.eligible &&
      source != ConsentProviderSource.none;

  static const unresolved = ProviderConsentSnapshot(
    status: ConsentProviderStatus.unresolved,
    source: ConsentProviderSource.none,
    resolvedAt: null,
  );
}

class ConsentState {
  const ConsentState({
    required this.localPreference,
    required this.localUpdatedAt,
    required this.provider,
  });

  final AdPrivacyPreference localPreference;
  final DateTime? localUpdatedAt;
  final ProviderConsentSnapshot provider;

  bool get hasLocalChoice =>
      localPreference != AdPrivacyPreference.unresolved;

  bool get canRequestAds =>
      localPreference == AdPrivacyPreference.allowAds &&
      provider.canRequestAds;

  static const initial = ConsentState(
    localPreference: AdPrivacyPreference.unresolved,
    localUpdatedAt: null,
    provider: ProviderConsentSnapshot.unresolved,
  );
}

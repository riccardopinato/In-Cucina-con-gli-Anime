import 'package:flutter_test/flutter_test.dart';
import 'package:animekitchen/core/monetization/consent.dart';
import 'package:animekitchen/core/monetization/entitlement.dart';
import 'package:animekitchen/core/monetization/product_limits.dart';

void main() {
  const providerEligible = ProviderConsentSnapshot(
    status: ConsentProviderStatus.eligible,
    source: ConsentProviderSource.providerVerified,
    resolvedAt: null,
  );

  test('free plan cannot request ads while consent is unresolved', () {
    const limits = ProductLimits(
      EntitlementSnapshot.free,
      ConsentState.initial,
    );

    expect(limits.adsSuppressed, isFalse);
    expect(limits.canRequestAds, isFalse);
  });

  test('local allow preference alone cannot unlock ad requests', () {
    const consent = ConsentState(
      localPreference: AdPrivacyPreference.allowAds,
      localUpdatedAt: null,
      provider: ProviderConsentSnapshot.unresolved,
    );
    const limits = ProductLimits(EntitlementSnapshot.free, consent);

    expect(limits.canRequestAds, isFalse);
  });

  test('free plan can request ads only after both gates allow it', () {
    const consent = ConsentState(
      localPreference: AdPrivacyPreference.allowAds,
      localUpdatedAt: null,
      provider: providerEligible,
    );
    const limits = ProductLimits(EntitlementSnapshot.free, consent);

    expect(limits.canRequestAds, isTrue);
  });

  test('local block preference wins over provider eligibility', () {
    const consent = ConsentState(
      localPreference: AdPrivacyPreference.blockAds,
      localUpdatedAt: null,
      provider: providerEligible,
    );
    const limits = ProductLimits(EntitlementSnapshot.free, consent);

    expect(limits.canRequestAds, isFalse);
  });

  test('lifetime plan suppresses ad requests after consent resolution', () {
    const consent = ConsentState(
      localPreference: AdPrivacyPreference.allowAds,
      localUpdatedAt: null,
      provider: providerEligible,
    );
    final limits = ProductLimits(
      EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: DateTime.utc(2026, 10, 21),
      ),
      consent,
    );

    expect(limits.adsSuppressed, isTrue);
    expect(limits.canRequestAds, isFalse);
  });
}

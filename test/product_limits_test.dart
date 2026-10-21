import 'package:flutter_test/flutter_test.dart';
import 'package:animekitchen/core/monetization/entitlement.dart';
import 'package:animekitchen/core/monetization/product_limits.dart';

void main() {
  test('free plan can request ads', () {
    const limits = ProductLimits(EntitlementSnapshot.free);

    expect(limits.adsSuppressed, isFalse);
    expect(limits.canRequestAds, isTrue);
  });

  test('lifetime plan suppresses ad requests', () {
    final limits = ProductLimits(
      EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: DateTime.utc(2026, 10, 21),
      ),
    );

    expect(limits.adsSuppressed, isTrue);
    expect(limits.canRequestAds, isFalse);
  });
}

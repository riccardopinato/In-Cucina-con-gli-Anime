import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'consent_provider.dart';
import 'entitlement.dart';
import 'product_limits.dart';

final entitlementProvider = Provider<EntitlementSnapshot>((ref) {
  return EntitlementSnapshot.free;
});

final productLimitsProvider = Provider<ProductLimits>((ref) {
  return ProductLimits(
    ref.watch(entitlementProvider),
    ref.watch(consentProvider),
  );
});

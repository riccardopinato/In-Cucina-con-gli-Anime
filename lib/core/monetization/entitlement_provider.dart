import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../persistence/shared_preferences_provider.dart';
import 'consent_provider.dart';
import 'entitlement.dart';
import 'entitlement_repository.dart';
import 'product_limits.dart';
import 'shared_preferences_entitlement_repository.dart';

final entitlementRepositoryProvider = Provider<EntitlementRepository>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SharedPreferencesEntitlementRepository(prefs);
});

class EntitlementNotifier extends Notifier<EntitlementSnapshot> {
  @override
  EntitlementSnapshot build() {
    return ref.watch(entitlementRepositoryProvider).loadCached();
  }

  Future<void> grantVerifiedLifetime({
    required DateTime verifiedAt,
  }) async {
    final snapshot = EntitlementSnapshot(
      plan: AppPlan.lifetime,
      source: EntitlementSource.providerVerified,
      verifiedAt: verifiedAt.toUtc(),
    );

    await ref.read(entitlementRepositoryProvider).cacheLifetime(snapshot);
    state = snapshot;
  }

  Future<void> clearCachedForQa() async {
    await ref.read(entitlementRepositoryProvider).clearCached();
    state = EntitlementSnapshot.free;
  }
}

final entitlementProvider =
    NotifierProvider<EntitlementNotifier, EntitlementSnapshot>(
  EntitlementNotifier.new,
);

final productLimitsProvider = Provider<ProductLimits>((ref) {
  return ProductLimits(
    ref.watch(entitlementProvider),
    ref.watch(consentProvider),
  );
});

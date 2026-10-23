import 'entitlement.dart';

abstract interface class EntitlementRepository {
  EntitlementSnapshot loadCached();

  Future<void> cacheLifetime(EntitlementSnapshot snapshot);

  Future<void> clearCached();
}

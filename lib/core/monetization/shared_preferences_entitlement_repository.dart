import 'package:shared_preferences/shared_preferences.dart';

import 'entitlement.dart';
import 'entitlement_repository.dart';

class SharedPreferencesEntitlementRepository
    implements EntitlementRepository {
  SharedPreferencesEntitlementRepository(this._prefs);

  static const _lifetimeKey = 'lifetime_entitlement_v1';
  static const _verifiedAtKey = 'lifetime_entitlement_verified_at_v1';

  final SharedPreferences _prefs;

  @override
  EntitlementSnapshot loadCached() {
    if (!(_prefs.getBool(_lifetimeKey) ?? false)) {
      return EntitlementSnapshot.free;
    }

    return EntitlementSnapshot(
      plan: AppPlan.lifetime,
      source: EntitlementSource.offlineCache,
      verifiedAt: DateTime.tryParse(
        _prefs.getString(_verifiedAtKey) ?? '',
      ),
    );
  }

  @override
  Future<void> cacheLifetime(EntitlementSnapshot snapshot) async {
    if (snapshot.plan != AppPlan.lifetime) {
      throw ArgumentError('Only lifetime entitlement may be cached here.');
    }

    await _prefs.setBool(_lifetimeKey, true);
    final verifiedAt = snapshot.verifiedAt;
    if (verifiedAt == null) {
      await _prefs.remove(_verifiedAtKey);
    } else {
      await _prefs.setString(
        _verifiedAtKey,
        verifiedAt.toUtc().toIso8601String(),
      );
    }
  }

  @override
  Future<void> clearCached() async {
    await _prefs.remove(_lifetimeKey);
    await _prefs.remove(_verifiedAtKey);
  }
}

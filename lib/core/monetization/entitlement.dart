enum AppPlan {
  free,
  premium,
  lifetime,
}

enum EntitlementSource {
  localDefault,
  providerVerified,
  offlineCache,
  qaOverride,
  unknown,
}

class EntitlementSnapshot {
  const EntitlementSnapshot({
    required this.plan,
    required this.source,
    required this.verifiedAt,
    this.expiresAt,
    this.graceUntil,
  });

  final AppPlan plan;
  final EntitlementSource source;
  final DateTime? verifiedAt;
  final DateTime? expiresAt;
  final DateTime? graceUntil;

  static const free = EntitlementSnapshot(
    plan: AppPlan.free,
    source: EntitlementSource.localDefault,
    verifiedAt: null,
  );
}

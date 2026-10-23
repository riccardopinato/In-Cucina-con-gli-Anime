import 'consent.dart';
import 'entitlement.dart';

class ProductLimits {
  const ProductLimits(this.entitlement, this.consent);

  final EntitlementSnapshot entitlement;
  final ConsentState consent;

  bool get adsSuppressed => entitlement.plan != AppPlan.free;

  bool get canRequestAds =>
      !adsSuppressed && consent.canRequestAds;
}

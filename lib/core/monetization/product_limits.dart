import 'entitlement.dart';

class ProductLimits {
  const ProductLimits(this.entitlement);

  final EntitlementSnapshot entitlement;

  bool get adsSuppressed => entitlement.plan != AppPlan.free;

  bool get canRequestAds => !adsSuppressed;
}

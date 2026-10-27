class PurchaseRuntimeConfig {
  const PurchaseRuntimeConfig({
    required this.billingEnabled,
    required this.sandboxVerification,
    required this.lifetimeProductId,
  });

  factory PurchaseRuntimeConfig.environment() {
    return const PurchaseRuntimeConfig(
      billingEnabled: bool.fromEnvironment(
        'ANIME_KITCHEN_BILLING_ENABLED',
        defaultValue: false,
      ),
      sandboxVerification: bool.fromEnvironment(
        'ANIME_KITCHEN_BILLING_SANDBOX',
        defaultValue: false,
      ),
      lifetimeProductId: String.fromEnvironment(
        'ANIME_KITCHEN_LIFETIME_PRODUCT_ID',
        defaultValue: 'remove_ads_lifetime',
      ),
    );
  }

  final bool billingEnabled;
  final bool sandboxVerification;
  final String lifetimeProductId;
}

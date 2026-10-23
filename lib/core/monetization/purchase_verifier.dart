import 'purchase_gateway.dart';

abstract interface class PurchaseVerifier {
  Future<bool> verify(StorePurchaseEvent event);
}

class SandboxPurchaseVerifier implements PurchaseVerifier {
  const SandboxPurchaseVerifier({
    required this.enabled,
    required this.expectedProductId,
  });

  final bool enabled;
  final String expectedProductId;

  @override
  Future<bool> verify(StorePurchaseEvent event) async {
    if (!enabled || event.productId != expectedProductId) {
      return false;
    }

    final isOwned = event.status == StorePurchaseStatus.purchased ||
        event.status == StorePurchaseStatus.restored;

    return isOwned &&
        event.verificationData.trim().isNotEmpty &&
        event.verificationSource.trim().isNotEmpty;
  }
}

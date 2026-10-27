enum StorePurchaseStatus {
  pending,
  purchased,
  restored,
  canceled,
  error,
}

class StoreOffer {
  const StoreOffer({
    required this.productId,
    required this.title,
    required this.description,
    required this.price,
  });

  final String productId;
  final String title;
  final String description;
  final String price;
}

class StorePurchaseEvent {
  const StorePurchaseEvent({
    required this.transactionKey,
    required this.productId,
    required this.status,
    required this.verificationData,
    required this.verificationSource,
    required this.needsCompletion,
    this.errorMessage,
  });

  final String transactionKey;
  final String productId;
  final StorePurchaseStatus status;
  final String verificationData;
  final String verificationSource;
  final bool needsCompletion;
  final String? errorMessage;
}

abstract interface class PurchaseGateway {
  bool get isSupported;

  Stream<StorePurchaseEvent> get events;

  Future<StoreOffer?> loadOffer(String productId);

  Future<bool> buyNonConsumable();

  Future<void> restorePurchases();

  Future<void> completePurchase(String transactionKey);

  Future<void> dispose();
}

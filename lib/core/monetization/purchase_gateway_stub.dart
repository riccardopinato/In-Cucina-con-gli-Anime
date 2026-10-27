import 'purchase_gateway.dart';

PurchaseGateway createPurchaseGateway() => _UnsupportedPurchaseGateway();

class _UnsupportedPurchaseGateway implements PurchaseGateway {
  @override
  bool get isSupported => false;

  @override
  Stream<StorePurchaseEvent> get events =>
      const Stream<StorePurchaseEvent>.empty();

  @override
  Future<StoreOffer?> loadOffer(String productId) async => null;

  @override
  Future<bool> buyNonConsumable() async => false;

  @override
  Future<void> restorePurchases() async {}

  @override
  Future<void> completePurchase(String transactionKey) async {}

  @override
  Future<void> dispose() async {}
}

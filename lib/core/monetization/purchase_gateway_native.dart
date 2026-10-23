import 'dart:async';

import 'package:in_app_purchase/in_app_purchase.dart';

import 'purchase_gateway.dart';

PurchaseGateway createPurchaseGateway() => NativePurchaseGateway();

class NativePurchaseGateway implements PurchaseGateway {
  NativePurchaseGateway() {
    _subscription = _iap.purchaseStream.listen(
      _handlePurchases,
      onError: (Object error, StackTrace stackTrace) {
        _events.addError(error, stackTrace);
      },
    );
  }

  final InAppPurchase _iap = InAppPurchase.instance;
  final StreamController<StorePurchaseEvent> _events =
      StreamController<StorePurchaseEvent>.broadcast();
  final Map<String, PurchaseDetails> _pendingCompletion = {};

  StreamSubscription<List<PurchaseDetails>>? _subscription;
  ProductDetails? _loadedProduct;

  @override
  bool get isSupported => true;

  @override
  Stream<StorePurchaseEvent> get events => _events.stream;

  @override
  Future<StoreOffer?> loadOffer(String productId) async {
    if (productId.trim().isEmpty || !await _iap.isAvailable()) {
      return null;
    }

    final response = await _iap.queryProductDetails({productId});
    ProductDetails? product;
    for (final candidate in response.productDetails) {
      if (candidate.id == productId) {
        product = candidate;
        break;
      }
    }

    _loadedProduct = product;
    if (product == null) {
      return null;
    }

    return StoreOffer(
      productId: product.id,
      title: product.title,
      description: product.description,
      price: product.price,
    );
  }

  @override
  Future<bool> buyNonConsumable() async {
    final product = _loadedProduct;
    if (product == null) {
      return false;
    }

    return _iap.buyNonConsumable(
      purchaseParam: PurchaseParam(productDetails: product),
    );
  }

  @override
  Future<void> restorePurchases() {
    return _iap.restorePurchases();
  }

  @override
  Future<void> completePurchase(String transactionKey) async {
    final purchase = _pendingCompletion.remove(transactionKey);
    if (purchase != null && purchase.pendingCompletePurchase) {
      await _iap.completePurchase(purchase);
    }
  }

  void _handlePurchases(List<PurchaseDetails> purchases) {
    for (final purchase in purchases) {
      final key = purchase.purchaseID ??
          '${purchase.productID}:${purchase.transactionDate ?? 'no-date'}:'
              '${identityHashCode(purchase)}';

      if (purchase.pendingCompletePurchase) {
        _pendingCompletion[key] = purchase;
      }

      _events.add(
        StorePurchaseEvent(
          transactionKey: key,
          productId: purchase.productID,
          status: switch (purchase.status) {
            PurchaseStatus.pending => StorePurchaseStatus.pending,
            PurchaseStatus.purchased => StorePurchaseStatus.purchased,
            PurchaseStatus.restored => StorePurchaseStatus.restored,
            PurchaseStatus.canceled => StorePurchaseStatus.canceled,
            PurchaseStatus.error => StorePurchaseStatus.error,
          },
          verificationData:
              purchase.verificationData.serverVerificationData,
          verificationSource: purchase.verificationData.source,
          needsCompletion: purchase.pendingCompletePurchase,
          errorMessage: purchase.error?.message,
        ),
      );
    }
  }

  @override
  Future<void> dispose() async {
    await _subscription?.cancel();
    await _events.close();
    _pendingCompletion.clear();
  }
}

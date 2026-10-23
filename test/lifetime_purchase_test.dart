import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:animekitchen/core/monetization/entitlement.dart';
import 'package:animekitchen/core/monetization/entitlement_provider.dart';
import 'package:animekitchen/core/monetization/purchase_config.dart';
import 'package:animekitchen/core/monetization/purchase_gateway.dart';
import 'package:animekitchen/core/monetization/purchase_provider.dart';
import 'package:animekitchen/core/persistence/shared_preferences_provider.dart';

const _productId = 'remove_ads_lifetime';

Future<void> _flushAsyncWork() async {
  for (var i = 0; i < 6; i++) {
    await Future<void>.delayed(Duration.zero);
  }
}

class _FakePurchaseGateway implements PurchaseGateway {
  final _events =
      StreamController<StorePurchaseEvent>.broadcast(sync: true);

  int completions = 0;
  bool emitRestore = true;
  bool validReceipt = true;

  @override
  bool get isSupported => true;

  @override
  Stream<StorePurchaseEvent> get events => _events.stream;

  @override
  Future<StoreOffer?> loadOffer(String productId) async {
    return const StoreOffer(
      productId: _productId,
      title: 'Lifetime',
      description: 'Remove ads forever',
      price: '€4.99',
    );
  }

  @override
  Future<bool> buyNonConsumable() async {
    _events.add(
      StorePurchaseEvent(
        transactionKey: 'purchase-1',
        productId: _productId,
        status: StorePurchaseStatus.purchased,
        verificationData: validReceipt ? 'sandbox-receipt' : '',
        verificationSource: 'sandbox',
        needsCompletion: true,
      ),
    );
    return true;
  }

  @override
  Future<void> restorePurchases() async {
    if (emitRestore) {
      _events.add(
        const StorePurchaseEvent(
          transactionKey: 'restore-1',
          productId: _productId,
          status: StorePurchaseStatus.restored,
          verificationData: 'sandbox-restore',
          verificationSource: 'sandbox',
          needsCompletion: true,
        ),
      );
    }
  }

  @override
  Future<void> completePurchase(String transactionKey) async {
    completions++;
  }

  @override
  Future<void> dispose() async {
    await _events.close();
  }
}

ProviderContainer _container({
  required SharedPreferences prefs,
  required PurchaseGateway gateway,
  required bool sandboxVerification,
}) {
  return ProviderContainer(
    overrides: [
      sharedPreferencesProvider.overrideWithValue(prefs),
      purchaseGatewayProvider.overrideWithValue(gateway),
      purchaseConfigProvider.overrideWithValue(
        PurchaseRuntimeConfig(
          billingEnabled: true,
          sandboxVerification: sandboxVerification,
          lifetimeProductId: _productId,
        ),
      ),
    ],
  );
}

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test('verified sandbox purchase grants and caches lifetime', () async {
    final prefs = await SharedPreferences.getInstance();
    final gateway = _FakePurchaseGateway();
    final container = _container(
      prefs: prefs,
      gateway: gateway,
      sandboxVerification: true,
    );
    addTearDown(container.dispose);

    container.read(purchaseControllerProvider);
    await _flushAsyncWork();

    expect(
      container.read(purchaseControllerProvider).availability,
      PurchaseAvailability.ready,
    );
    expect(container.read(entitlementProvider).plan, AppPlan.free);

    await container
        .read(purchaseControllerProvider.notifier)
        .buyLifetime();
    await _flushAsyncWork();

    final entitlement = container.read(entitlementProvider);
    expect(entitlement.plan, AppPlan.lifetime);
    expect(entitlement.source, EntitlementSource.providerVerified);
    expect(gateway.completions, 1);
    expect(prefs.getBool('lifetime_entitlement_v1'), isTrue);

    final restarted = ProviderContainer(
      overrides: [
        sharedPreferencesProvider.overrideWithValue(prefs),
        purchaseConfigProvider.overrideWithValue(
          const PurchaseRuntimeConfig(
            billingEnabled: false,
            sandboxVerification: false,
            lifetimeProductId: _productId,
          ),
        ),
      ],
    );
    addTearDown(restarted.dispose);

    final cached = restarted.read(entitlementProvider);
    expect(cached.plan, AppPlan.lifetime);
    expect(cached.source, EntitlementSource.offlineCache);
  });

  test('verified restore grants lifetime', () async {
    final prefs = await SharedPreferences.getInstance();
    final gateway = _FakePurchaseGateway();
    final container = _container(
      prefs: prefs,
      gateway: gateway,
      sandboxVerification: true,
    );
    addTearDown(container.dispose);

    container.read(purchaseControllerProvider);
    await _flushAsyncWork();

    await container.read(purchaseControllerProvider.notifier).restore();
    await _flushAsyncWork();

    expect(container.read(entitlementProvider).plan, AppPlan.lifetime);
    expect(
      container.read(purchaseControllerProvider).flowStatus,
      PurchaseFlowStatus.restored,
    );
    expect(gateway.completions, 1);
  });

  test('billing stays locked when no purchase verifier is ready', () async {
    final prefs = await SharedPreferences.getInstance();
    final gateway = _FakePurchaseGateway();
    final container = _container(
      prefs: prefs,
      gateway: gateway,
      sandboxVerification: false,
    );
    addTearDown(container.dispose);

    final purchase = container.read(purchaseControllerProvider);

    expect(
      purchase.availability,
      PurchaseAvailability.verificationUnavailable,
    );

    await container
        .read(purchaseControllerProvider.notifier)
        .buyLifetime();

    expect(container.read(entitlementProvider).plan, AppPlan.free);
    expect(gateway.completions, 0);
  });

  test('invalid sandbox receipt cannot grant entitlement', () async {
    final prefs = await SharedPreferences.getInstance();
    final gateway = _FakePurchaseGateway()..validReceipt = false;
    final container = _container(
      prefs: prefs,
      gateway: gateway,
      sandboxVerification: true,
    );
    addTearDown(container.dispose);

    container.read(purchaseControllerProvider);
    await _flushAsyncWork();

    await container
        .read(purchaseControllerProvider.notifier)
        .buyLifetime();
    await _flushAsyncWork();

    expect(container.read(entitlementProvider).plan, AppPlan.free);
    expect(
      container.read(purchaseControllerProvider).flowStatus,
      PurchaseFlowStatus.verificationFailed,
    );
    expect(gateway.completions, 1);
  });
}

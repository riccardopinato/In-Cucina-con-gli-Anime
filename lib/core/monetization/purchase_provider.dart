import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'entitlement_provider.dart';
import 'purchase_config.dart';
import 'purchase_gateway.dart';
import 'purchase_gateway_factory.dart';
import 'purchase_verifier.dart';

enum PurchaseAvailability {
  disabled,
  loading,
  unavailable,
  ready,
}

enum PurchaseFlowStatus {
  idle,
  pending,
  purchased,
  restored,
  canceled,
  verificationFailed,
  error,
}

class PurchaseState {
  const PurchaseState({
    required this.availability,
    required this.flowStatus,
    this.offer,
    this.message,
  });

  final PurchaseAvailability availability;
  final PurchaseFlowStatus flowStatus;
  final StoreOffer? offer;
  final String? message;

  static const disabled = PurchaseState(
    availability: PurchaseAvailability.disabled,
    flowStatus: PurchaseFlowStatus.idle,
  );

  static const loading = PurchaseState(
    availability: PurchaseAvailability.loading,
    flowStatus: PurchaseFlowStatus.idle,
  );

  PurchaseState copyWith({
    PurchaseAvailability? availability,
    PurchaseFlowStatus? flowStatus,
    StoreOffer? offer,
    bool clearOffer = false,
    String? message,
    bool clearMessage = false,
  }) {
    return PurchaseState(
      availability: availability ?? this.availability,
      flowStatus: flowStatus ?? this.flowStatus,
      offer: clearOffer ? null : (offer ?? this.offer),
      message: clearMessage ? null : (message ?? this.message),
    );
  }
}

final purchaseConfigProvider = Provider<PurchaseRuntimeConfig>((ref) {
  return PurchaseRuntimeConfig.environment();
});

final purchaseGatewayProvider = Provider<PurchaseGateway>((ref) {
  final gateway = createPurchaseGateway();
  ref.onDispose(() {
    unawaited(gateway.dispose());
  });
  return gateway;
});

final purchaseVerifierProvider = Provider<PurchaseVerifier>((ref) {
  final config = ref.watch(purchaseConfigProvider);
  return SandboxPurchaseVerifier(
    enabled: config.sandboxVerification,
    expectedProductId: config.lifetimeProductId,
  );
});

class PurchaseController extends Notifier<PurchaseState> {
  StreamSubscription<StorePurchaseEvent>? _subscription;
  PurchaseGateway? _gateway;
  PurchaseRuntimeConfig? _config;

  @override
  PurchaseState build() {
    final config = ref.watch(purchaseConfigProvider);
    _config = config;

    if (!config.billingEnabled) {
      return PurchaseState.disabled;
    }

    final gateway = ref.watch(purchaseGatewayProvider);
    _gateway = gateway;

    if (!gateway.isSupported) {
      return const PurchaseState(
        availability: PurchaseAvailability.unavailable,
        flowStatus: PurchaseFlowStatus.idle,
      );
    }

    _subscription = gateway.events.listen(
      _handleEvent,
      onError: (Object error, StackTrace stackTrace) {
        state = state.copyWith(
          flowStatus: PurchaseFlowStatus.error,
          message: error.toString(),
        );
      },
    );

    ref.onDispose(() {
      unawaited(_subscription?.cancel());
    });

    unawaited(_loadOffer(gateway, config));
    return PurchaseState.loading;
  }

  Future<void> _loadOffer(
    PurchaseGateway gateway,
    PurchaseRuntimeConfig config,
  ) async {
    try {
      final offer = await gateway.loadOffer(config.lifetimeProductId);
      state = PurchaseState(
        availability: offer == null
            ? PurchaseAvailability.unavailable
            : PurchaseAvailability.ready,
        flowStatus: PurchaseFlowStatus.idle,
        offer: offer,
      );
    } catch (error) {
      state = PurchaseState(
        availability: PurchaseAvailability.unavailable,
        flowStatus: PurchaseFlowStatus.error,
        message: error.toString(),
      );
    }
  }

  Future<void> buyLifetime() async {
    final gateway = _gateway;
    if (gateway == null ||
        state.availability != PurchaseAvailability.ready ||
        state.offer == null) {
      return;
    }

    state = state.copyWith(
      flowStatus: PurchaseFlowStatus.pending,
      clearMessage: true,
    );

    try {
      final started = await gateway.buyNonConsumable();
      if (!started) {
        state = state.copyWith(
          flowStatus: PurchaseFlowStatus.error,
          message: 'purchase_not_started',
        );
      }
    } catch (error) {
      state = state.copyWith(
        flowStatus: PurchaseFlowStatus.error,
        message: error.toString(),
      );
    }
  }

  Future<void> restore() async {
    final gateway = _gateway;
    if (gateway == null ||
        state.availability == PurchaseAvailability.disabled) {
      return;
    }

    state = state.copyWith(
      flowStatus: PurchaseFlowStatus.pending,
      clearMessage: true,
    );

    try {
      await gateway.restorePurchases();
      if (state.flowStatus == PurchaseFlowStatus.pending) {
        state = state.copyWith(flowStatus: PurchaseFlowStatus.idle);
      }
    } catch (error) {
      state = state.copyWith(
        flowStatus: PurchaseFlowStatus.error,
        message: error.toString(),
      );
    }
  }

  Future<void> _handleEvent(StorePurchaseEvent event) async {
    final config = _config;
    final gateway = _gateway;
    if (config == null ||
        gateway == null ||
        event.productId != config.lifetimeProductId) {
      return;
    }

    switch (event.status) {
      case StorePurchaseStatus.pending:
        state = state.copyWith(
          flowStatus: PurchaseFlowStatus.pending,
          clearMessage: true,
        );
        return;
      case StorePurchaseStatus.canceled:
        state = state.copyWith(
          flowStatus: PurchaseFlowStatus.canceled,
          clearMessage: true,
        );
        return;
      case StorePurchaseStatus.error:
        state = state.copyWith(
          flowStatus: PurchaseFlowStatus.error,
          message: event.errorMessage ?? 'store_error',
        );
        return;
      case StorePurchaseStatus.purchased:
      case StorePurchaseStatus.restored:
        final verifier = ref.read(purchaseVerifierProvider);
        final verified = await verifier.verify(event);

        if (verified) {
          await ref.read(entitlementProvider.notifier).grantVerifiedLifetime(
                verifiedAt: DateTime.now().toUtc(),
              );
        }

        if (event.needsCompletion) {
          await gateway.completePurchase(event.transactionKey);
        }

        state = state.copyWith(
          flowStatus: verified
              ? (event.status == StorePurchaseStatus.restored
                  ? PurchaseFlowStatus.restored
                  : PurchaseFlowStatus.purchased)
              : PurchaseFlowStatus.verificationFailed,
          clearMessage: true,
        );
        return;
    }
  }
}

final purchaseControllerProvider =
    NotifierProvider<PurchaseController, PurchaseState>(
  PurchaseController.new,
);

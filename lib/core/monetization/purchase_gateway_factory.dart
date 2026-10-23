import 'purchase_gateway.dart';
import 'purchase_gateway_stub.dart'
    if (dart.library.io) 'purchase_gateway_native.dart' as implementation;

PurchaseGateway createPurchaseGateway() =>
    implementation.createPurchaseGateway();

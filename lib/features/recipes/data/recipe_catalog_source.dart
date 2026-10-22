import 'package:flutter/services.dart';

abstract interface class RecipeCatalogSource {
  Future<String> loadString(String path);
}

class AssetRecipeCatalogSource implements RecipeCatalogSource {
  const AssetRecipeCatalogSource(this.bundle);

  final AssetBundle bundle;

  @override
  Future<String> loadString(String path) => bundle.loadString(path);
}

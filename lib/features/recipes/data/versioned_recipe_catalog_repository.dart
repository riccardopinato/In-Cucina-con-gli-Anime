import 'dart:convert';

import '../domain/recipe.dart';
import '../domain/recipe_catalog_repository.dart';
import 'recipe_catalogsource.dart';

class RecipeCatalogException implements Exception {
  const RecipeCatalogException(this.message);

  final String message;

  @override
  String toString() => 'RecipeCatalogException: $message';
}

class VersionedRecipeCatalogRepository implements RecipeCatalogRepository {
  const VersionedRecipeCatalogRepository({
    required this.source,
    required this.localeCode,
    this.manifestAsset = 'assets/catalog/manifest.json',
  });

  static const supportedSchemaVersion = 1;

  final RecipeCatalogSource source;
  final String localeCode;
  final String manifestAsset;

  @override
  Future<List<Recipe>> loadPublishedRecipes() async {
    try {
      final manifest = _decodeObject(
        await source.loadString(manifestAsset),
        manifestAsset,
      );
      _requireSchema(manifest, manifestAsset);

      final catalogVersion =
          _string(manifest, 'catalogVersion', manifestAsset);
      if (!RegExp(r'^\d+\.\d+\.\d+$').hasMatch(catalogVersion)) {
        throw const RecipeCatalogException(
          'catalogVersion must use x.y.z semantic versioning',
        );
      }

      final defaultLocale =
          _normalize(_string(manifest, 'defaultLocale', manifestAsset));
      final supportedLocales = _stringList(
        manifest,
        'supportedLocales',
        manifestAsset,
      ).map(_normalize).toList(growable: false);
      if (supportedLocales.toSet().length != supportedLocales.length) {
        throw const RecipeCatalogException(
          'supportedLocales contains duplicates',
        );
      }
      if (!supportedLocales.contains(defaultLocale)) {
        throw const RecipeCatalogException(
          'defaultLocale must be supported',
        );
      }

      final contentAsset = _string(manifest, 'contentAsset', manifestAsset);
      final localeAssets = _stringMap(
        manifest,
        'localeAssets',
        manifestAsset,
      );
      if (localeAssets.keys.toSet().difference(supportedLocales.toSet()).isNotEmpty ||
          supportedLocales.toSet().difference(localeAssets.keys.toSet()).isNotEmpty) {
        throw const RecipeCatalogException(
          'localeAssets keys must match supportedLocales',
        );
      }

      final normalizedRequested = _normalize(localeCode);
      final requestedLocale = supportedLocales.contains(normalizedRequested)
          ? normalizedRequested
          : defaultLocale;

      final content = _decodeObject(
        await source.loadString(contentAsset),
        contentAsset,
      );
      _requireSchema(content, contentAsset);

      final defaultAsset = localeAssets[defaultLocale]!;
      final defaultPayload = _decodeObject(
        await source.loadString(defaultAsset),
        defaultAsset,
      );
      _validateLocaleEnvelope(defaultPayload, defaultLocale, defaultAsset);

      final requestedAsset = localeAssets[requestedLocale]!;
      final requestedPayload = requestedLocale == defaultLocale
          ? defaultPayload
          : _decodeObject(
              await source.loadString(requestedAsset),
              requestedAsset,
            );
      if (requestedLocale != defaultLocale) {
        _validateLocaleEnvelope(
          requestedPayload,
          requestedLocale,
          requestedAsset,
        );
      }

      final rawRecipes = _list(content, 'recipes', contentAsset);
      final canonical = <String, Map<String, dynamic>>{};
      for (var index = 0; index < rawRecipes.length; index++) {
        final recipe = _object(
          rawRecipes[index],
          '$contentAsset recipes[$index]',
        );
        _validateCanonical(recipe);
        final id = _string(recipe, 'id', 'recipe');
        if (canonical.containsKey(id)) {
          throw RecipeCatalogException('Duplicate recipe id: $id');
        }
        canonical[id] = recipe;
      }

      final fallbackTexts = _localizedRecipes(defaultPayload, defaultAsset);
      final requestedTexts =
          _localizedRecipes(requestedPayload, requestedAsset);

      _validateLocalized(fallbackTexts, canonical, defaultAsset);
      if (requestedLocale != defaultLocale) {
        _validateLocalized(requestedTexts, canonical, requestedAsset);
      }

      final output = <Recipe>[];
      for (final entry in canonical.entries) {
        final metadata = entry.value;
        if (_string(metadata, 'status', 'recipe') != 'published') {
          continue;
        }
        final fallback = fallbackTexts[entry.key];
        if (fallback == null) {
          throw RecipeCatalogException(
            'Published recipe ${entry.key} has no default translation',
          );
        }
        output.add(
          _toRecipe(metadata, requestedTexts[entry.key] ?? fallback),
        );
      }
      return List<Recipe>.unmodifiable(output);
    } on RecipeCatalogException {
      rethrow;
    } catch (error) {
      throw RecipeCatalogException('Catalog rejected: $error');
    }
  }

  static Recipe _toRecipe(
    Map<String, dynamic> metadata,
    Map<String, dynamic> localized,
  ) {
    final id = _string(metadata, 'id', 'recipe');
    final ingredientTexts =
        _object(localized['ingredientTexts'], 'ingredientTexts');
    final ingredients = _list(metadata, 'ingredients', 'recipe').map((raw) {
      final item = _object(raw, 'ingredient');
      final itemId = _string(item, 'id', 'ingredient');
      final text = _object(ingredientTexts[itemId], 'ingredient text');
      return RecipeIngredient(
        id: itemId,
        name: _string(text, 'name', 'ingredient text'),
        quantity: _optionalNumber(item['quantity']),
        unit: _optionalString(item['unit']),
        note: _optionalString(text['note']),
      );
    }).toList(growable: false);

    final stepTexts = _object(localized['stepTexts'], 'stepTexts');
    final steps = _list(metadata, 'steps', 'recipe').map((raw) {
      final step = _object(raw, 'step');
      final stepId = _string(step, 'id', 'step');
      final stepText = stepTexts[stepId];
      if (stepText is! String || stepText.trim().isEmpty) {
        throw RecipeCatalogException('Missing step text: $stepId');
      }
      return RecipeStep(
        id: stepId,
        text: stepText.trim(),
        timerSeconds: _optionalInt(step['timerSeconds']),
      );
    }).toList(growable: false);

    return Recipe(
      id: id,
      contentVersion: _int(metadata, 'contentVersion', 'recipe'),
      contentOrigin: switch (_string(metadata, 'contentOrigin', 'recipe')) {
        'original' => RecipeContentOrigin.original,
        'inspired' => RecipeContentOrigin.inspired,
        'adapted' => RecipeContentOrigin.adapted,
        _ => throw const RecipeCatalogException('Unsupported contentOrigin'),
      },
      sourceNote: _optionalString(metadata['sourceNote']),
      title: _string(localized, 'title', 'localized recipe'),
      animeSource: _string(metadata, 'inspirationTitle', 'recipe'),
      prepMinutes: _int(metadata, 'prepMinutes', 'recipe'),
      cookMinutes: _int(metadata, 'cookMinutes', 'recipe'),
      servings: _int(metadata, 'servings', 'recipe'),
      difficulty: switch (_string(metadata, 'difficulty', 'recipe')) {
        'easy' => RecipeDifficulty.easy,
        'medium' => RecipeDifficulty.medium,
        'hard' => RecipeDifficulty.hard,
        _ => throw const RecipeCatalogException('Unsupported difficulty'),
      },
      imageAsset: _optionalString(metadata['imageAsset']),
      ingredients: ingredients,
      steps: steps,
    );
  }

  static void _validateCanonical(Map<String, dynamic> recipe) {
    final id = _string(recipe, 'id', 'recipe');
    final idPattern = RegExp(r'^[a-z0-9]+(?:_[a-z0-9]+)*$');
    if (!idPattern.hasMatch(id)) {
      throw RecipeCatalogException('Invalid stable recipe id: $id');
    }
    if (_int(recipe, 'contentVersion', id) < 1) {
      throw RecipeCatalogException('$id contentVersion must be >= 1');
    }
    if (!{'draft', 'published', 'archived'}
        .contains(_string(recipe, 'status', id))) {
      throw RecipeCatalogException('$id has invalid status');
    }
    _string(recipe, 'inspirationTitle', id);
    if (_int(recipe, 'prepMinutes', id) < 0 ||
        _int(recipe, 'cookMinutes', id) < 0) {
      throw RecipeCatalogException('$id minutes cannot be negative');
    }
    if (_int(recipe, 'servings', id) < 1) {
      throw RecipeCatalogException('$id servings must be >= 1');
    }
    if (!{'easy', 'medium', 'hard'}
        .contains(_string(recipe, 'difficulty', id))) {
      throw RecipeCatalogException('$id has invalid difficulty');
    }
    if (!{'original', 'inspired', 'adapted'}
        .contains(_string(recipe, 'contentOrigin', id))) {
      throw RecipeCatalogException('$id has invalid contentOrigin');
    }
    _nullableString(recipe['sourceNote'], '$id sourceNote');
    _nullableString(recipe['imageAsset'], '$id imageAsset');

    final ingredientIds = <String>{};
    final ingredients = _list(recipe, 'ingredients', id);
    if (ingredients.isEmpty) {
      throw RecipeCatalogException('$id must contain ingredients');
    }
    for (final raw in ingredients) {
      final ingredient = _object(raw, '$id ingredient');
      final ingredientId = _string(ingredient, 'id', '$id ingredient');
      if (!idPattern.hasMatch(ingredientId) ||
          !ingredientIds.add(ingredientId)) {
        throw RecipeCatalogException(
          '$id has invalid or duplicate ingredient ids',
        );
      }
      final quantity = _optionalNumber(ingredient['quantity']);
      if (quantity != null && quantity <= 0) {
        throw RecipeCatalogException('$id ingredient quantity must be > 0');
      }
      _nullableString(ingredient['unit'], '$id ingredient unit');
    }

    final stepIds = <String>{};
    final steps = _list(recipe, 'steps', id);
    if (steps.isEmpty) {
      throw RecipeCatalogException('$id must contain steps');
    }
    for (final raw in steps) {
      final step = _object(raw, '$id step');
      final stepId = _string(step, 'id', '$id step');
      if (!idPattern.hasMatch(stepId) || !stepIds.add(stepId)) {
        throw RecipeCatalogException('$id has invalid or duplicate step ids');
      }
      final timer = _optionalInt(step['timerSeconds']);
      if (timer != null && timer < 0) {
        throw RecipeCatalogException('$id timerSeconds cannot be negative');
      }
    }
  }

  static void _validateLocalized(
    Map<String, Map<String, dynamic>> localized,
    Map<String, Map<String, dynamic>> canonical,
    String label,
  ) {
    for (final entry in localized.entries) {
      final metadata = canonical[entry.key];
      if (metadata == null) {
        throw RecipeCatalogException(
          '$label contains orphan recipe id ${entry.key}',
        );
      }
      final value = entry.value;
      _string(value, 'title', label);

      final expectedIngredients = _list(
        metadata,
        'ingredients',
        entry.key,
      ).map((raw) => _string(_object(raw, 'ingredient'), 'id', 'ingredient')).toSet();
      final ingredientTexts =
          _object(value['ingredientTexts'], 'ingredientTexts');
      if (ingredientTexts.keys.toSet().difference(expectedIngredients).isNotEmpty ||
          expectedIngredients.difference(ingredientTexts.keys.toSet()).isNotEmpty) {
        throw RecipeCatalogException(
          '$label ingredient ids do not match ${entry.key}',
        );
      }
      for (final rawText in ingredientTexts.values) {
        final ingredientText = _object(rawText, 'ingredient text');
        _string(ingredientText, 'name', 'ingredient text');
        _nullableString(ingredientText['note'], 'ingredient note');
      }

      final expectedSteps = _list(
        metadata,
        'steps',
        entry.key,
      ).map((raw) => _string(_object(raw, 'step'), 'id', 'step')).toSet();
      final stepTexts = _object(value['stepTexts'], 'stepTexts');
      if (stepTexts.keys.toSet().difference(expectedSteps).isNotEmpty ||
          expectedSteps.difference(stepTexts.keys.toSet()).isNotEmpty) {
        throw RecipeCatalogException(
          '$label step ids do not match ${entry.key}',
        );
      }
      for (final stepId in expectedSteps) {
        final text = stepTexts[stepId];
        if (text is! String || text.trim().isEmpty) {
          throw RecipeCatalogException(
            '$label has invalid step text $stepId',
          );
        }
      }
    }
  }

  static void _validateLocaleEnvelope(
    Map<String, dynamic> payload,
    String expectedLocale,
    String label,
  ) {
    _requireSchema(payload, label);
    if (_normalize(_string(payload, 'locale', label)) != expectedLocale) {
      throw RecipeCatalogException('$label declares the wrong locale');
    }
    _object(payload['recipes'], '$label recipes');
  }

  static Map<String, Map<String, dynamic>> _localizedRecipes(
    Map<String, dynamic> payload,
    String label,
  ) {
    final raw = _object(payload['recipes'], '$label recipes');
    return raw.map(
      (key, value) => MapEntry(key, _object(value, '$label recipe')),
    );
  }

  static void _requireSchema(
    Map<String, dynamic> payload,
    String label,
  ) {
    final version = _int(payload, 'schemaVersion', label);
    if (version != supportedSchemaVersion) {
      throw RecipeCatalogException(
        '$label uses unsupported schemaVersion $version',
      );
    }
  }

  static Map<String, dynamic> _decodeObject(String raw, String label) {
    return _object(jsonDecode(raw), label);
  }

  static Map<String, dynamic> _object(Object? value, String label) {
    if (value is! Map) {
      throw RecipeCatalogException('$label must be a JSON object');
    }
    return value.map((key, item) => MapEntry(key.toString(), item));
  }

  static List<dynamic> _list(
    Map<String, dynamic> object,
    String key,
    String label,
  ) {
    final value = object[key];
    if (value is! List) {
      throw RecipeCatalogException('$label.$key must be an array');
    }
    return value;
  }

  static String _string(
    Map<String, dynamic> object,
    String key,
    String label,
  ) {
    final value = object[key];
    if (value is! String || value.trim().isEmpty) {
      throw RecipeCatalogException('$label.$key must be a non-empty string');
    }
    return value.trim();
  }

  static int _int(
    Map<String, dynamic> object,
    String key,
    String label,
  ) {
    final value = object[key];
    if (value is! int) {
      throw RecipeCatalogException('$label.$key must be an integer');
    }
    return value;
  }

  static int? _optionalInt(Object? value) {
    if (value == null) return null;
    if (value is! int) {
      throw const RecipeCatalogException('Expected optional integer');
    }
    return value;
  }

  static double? _optionalNumber(Object? value) {
    if (value == null) return null;
    if (value is! num) {
      throw const RecipeCatalogException('Expected optional number');
    }
    return value.toDouble();
  }

  static String? _optionalString(Object? value) {
    if (value == null) return null;
    if (value is! String) {
      throw const RecipeCatalogException('Expected optional string');
    }
    return value.trim().isEmpty ? null : value.trim();
  }

  static void _nullableString(Object? value, String label) {
    if (value != null && value is! String) {
      throw RecipeCatalogException('$label must be null or a string');
    }
  }

  static List<String> _stringList(
    Map<String, dynamic> object,
    String key,
    String label,
  ) {
    return _list(object, key, label).map((value) {
      if (value is! String || value.trim().isEmpty) {
        throw RecipeCatalogException('$label.$key must contain strings');
      }
      return value.trim();
    }).toList(growable: false);
  }

  static Map<String, String> _stringMap(
    Map<String, dynamic> object,
    String key,
    String label,
  ) {
    return _object(object[key], '$label.$key').map((mapKey, value) {
      if (value is! String || value.trim().isEmpty) {
        throw RecipeCatalogException('$label.$key values must be strings');
      }
      return MapEntry(_normalize(mapKey), value.trim());
    });
  }

  static String _normalize(String value) {
    return value.trim().toLowerCase().split(RegExp('[-_]')).first;
  }
}

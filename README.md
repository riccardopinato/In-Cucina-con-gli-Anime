# In Cucina con gli Anime

Flutter app for original/adapted editorial recipes inspired by food seen in anime, built as a local-first, multilingual and monetization-ready product.

## Current state

**v0.2 — F1 versioned recipe catalog contract complete. Production catalog intentionally contains zero recipes.**

The app now loads a deterministic JSON catalog contract with stable recipe IDs, schema/catalog/content versioning, structured ingredients/steps, locale fallback and fail-closed validation. Real recipe authoring starts in F2.

## Stack

- Flutter / Dart
- Riverpod
- SharedPreferences for small user-owned state
- Flutter gen_l10n: EN / IT / ES / FR / DE / PT
- JSON-only versioned recipe catalog
- Material 3 foundation with custom brand tokens
- Android / iOS / Web scaffold generated deterministically

## First setup

```bash
./tool/bootstrap_platforms.sh
flutter pub get
flutter gen-l10n
dart run launcher_icons
flutter run
```

## Validation

```bash
python3 tool/validate_structure.py
python3 tool/validate_recipe_catalog.py
flutter analyze
flutter test
flutter build web --release
```

## Product and execution truth

- Product: `docs/PRODUCT_BIBLE.md`
- Roadmap: `ROADMAP.md`
- Architecture: `docs/ARCHITECTURE.md`
- Catalog contract: `docs/RECIPE_CATALOG_CONTRACT.md`
- Rights/editorial policy: `docs/CONTENT_RIGHTS_POLICY.md`
- Agent contract: `AGENTS.md`
- Golden reuse: `docs/GOLDEN_REUSE_MANIFEST.txt`

Factory baseline: App-Factory-Core Master 26.6 / Golden Index 18 @ `47c47f49a7b46812e3bd6f1231c3524f2b52b826`.

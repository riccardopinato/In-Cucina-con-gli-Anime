# In Cucina con gli Anime

Flutter app for original recipes inspired by food seen in anime, built as a local-first, multilingual and monetization-ready product.

## Current state

**v0.1 foundation bootstrap — no recipes imported yet.**

The attached planning PDF is used only for product context. Recipe content will be implemented later through a versioned editorial catalog with explicit provenance/rights rules.

## Stack

- Flutter / Dart
- Riverpod
- SharedPreferences for small user-owned state
- Flutter gen_l10n: EN / IT / ES / FR / DE / PT
- Material 3 with custom watercolor-inspired brand
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
flutter analyze
flutter test
flutter build web --release
```

## Product and execution truth

- Product: `docs/PRODUCT_BIBLE.md`
- Roadmap: `ROADMAP.md`
- Architecture: `docs/ARCHITECTURE.md`
- Rights: `docs/CONTENT_RIGHTS_POLICY.md`
- Agent contract: `AGENTS.md`
- Golden reuse: `docs/GOLDEN_REUSE_MANIFEST.txt`

Factory baseline: App-Factory-Core Master 26.6 / Golden Index 18 @ `47c47f49a7b46812e3bd6f1231c3524f2b52b826`.

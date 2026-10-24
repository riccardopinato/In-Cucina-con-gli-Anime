# In Cucina con gli Anime

Flutter app for original/adapted editorial recipes inspired by food seen in anime, built as a local-first, multilingual and monetization-ready product.

## Current state

**v0.9 — F3F complete: twenty audited recipes with one optimized original artwork per recipe; F4A remains complete and monetization wiring is unchanged.**

F1 remains the runtime contract and F2 remains the authoring/build layer. F3D/F3E established the artwork system; F3F expands the catalog to twenty recipes, fills every recipe artwork slot, audits culinary semantics and hardens batch CI. F4A consent/privacy remains complete, but this editorial batch does not add ad or billing SDKs.

## Stack

- Flutter / Dart
- Riverpod
- SharedPreferences for small user-owned state
- Flutter gen_l10n: EN / IT / ES / FR / DE / PT
- JSON-only versioned runtime recipe catalog
- JSON-only build-time recipe authoring pipeline
- deterministic duplicate/similarity review
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

## Recipe authoring

Production records belong in `authoring/recipes/`. Raw copied source material should remain transient and uncommitted.

```bash
python3 tool/compile_recipe_catalog.py --check
python3 tool/review_recipe_similarity.py path/to/candidate.json
python3 tool/build_recipe_preview.py
```

See `docs/RECIPE_AUTHORING_PIPELINE.md`.

## Validation

```bash
python3 tool/validate_structure.py
python3 tool/compile_recipe_catalog.py --check
python3 -m unittest discover -s tool/tests -p 'test_*.py'
python3 tool/validate_recipe_catalog.py
flutter analyze
flutter test
python3 tool/build_recipe_preview.py
flutter build web --release
```

## Product and execution truth

- Product: `docs/PRODUCT_BIBLE.md`
- Roadmap: `ROADMAP.md`
- Architecture: `docs/ARCHITECTURE.md`
- Catalog contract: `docs/RECIPE_CATALOG_CONTRACT.md`
- Authoring pipeline: `docs/RECIPE_AUTHORING_PIPELINE.md`
- Rights/editorial policy: `docs/CONTENT_RIGHTS_POLICY.md`
- Agent contract: `AGENTS.md`
- Golden reuse: `docs/GOLDEN_REUSE_MANIFEST.txt`

Factory baseline: App-Factory-Core Master 26.6 / Golden Index 19 @ `4cc0b94467b94ab6fabe2c927fcc58afff49e39a`.


## Recipe artwork pipeline

F3E stores one optimized JPEG per approved recipe. The same asset is cropped in cards and shown full in recipe detail. Run `python3 tool/build_recipe_artwork_queue.py --missing-only` to prepare a batch; semantic approval is explicit and CI enforces the 140 KiB / 720–960 px asset budget.


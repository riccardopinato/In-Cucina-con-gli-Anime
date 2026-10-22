# Architecture

## Runtime flow

```text
Presentation (Flutter widgets + Riverpod)
        |
        v
Application state / use-oriented notifiers
        |
        v
Domain interfaces
        |
        +--> RecipeCatalogRepository
        +--> FavoritesRepository
        +--> ShoppingRepository
        +--> PreferencesRepository
        +--> Entitlement state
        |
        v
Local adapters
```

The Flutter runtime does not know about the authoring pipeline.

## Build-time editorial flow

```text
transient user/reference input
        |
        v
editorial normalization + fresh app wording
        |
        v
authoring/recipes/*.json
        |
        +--> authoring validation
        +--> localization completeness
        +--> asset manifest resolution
        +--> Duplicate / Similarity Review Gate
        |
        v
tool/compile_recipe_catalog.py
        |
        v
assets/catalog/*.json
        |
        +--> tool/validate_recipe_catalog.py
        |
        v
VersionedRecipeCatalogRepository
        |
        v
Flutter UI
```

This is intentionally a build pipeline, not a second runtime content engine.

## Authoring ownership

`authoring/recipes/*.json` is the editable production content source.

`assets/catalog/*` is generated runtime content and must match authoring output. CI enforces this with `compile_recipe_catalog.py --check`.

Synthetic records live under `authoring/fixtures/` and are included only when explicitly requested for preview/tests.

Raw copied source prose is not committed to the authoring source. The committed records contain normalized culinary facts and fresh app editorial wording.

## Recipe catalog runtime seam

The UI knows one interface: obtain currently published recipes.

`VersionedRecipeCatalogRepository` consumes the F1 package through `RecipeCatalogSource`, allowing tests to use in-memory assets while production uses Flutter `rootBundle`.

Runtime flow:

```text
manifest.json
-> schema/catalog/locale contract
recipes.json
-> canonical recipe metadata
requested locale + default locale
-> localized editorial text
-> Recipe domain objects
```

Unsupported or malformed input fails closed with `RecipeCatalogException`; no partial recipe list is returned.

## Duplicate / Similarity Review Gate

Similarity is a build-time review seam, not runtime business logic.

The comparator:
- normalizes explicit ingredient aliases;
- converts configured compatible units;
- compares inspiration/reference, ingredient set, quantities, ordered procedure text and total timing;
- emits explainable per-dimension scores and differences;
- distinguishes idempotent same-ID re-import, same-entity update, probable duplicate, review-required, possible variant and distinct content.

Blocking semantic collisions require a fingerprint-bound decision. A decision ceases to match if either recipe changes.

The system never maps a similarity score directly to destructive mutation.

## Asset manifest

Authoring records reference stable `imageAssetId` values. The build-time manifest resolves IDs to repository-owned asset paths and records a minimal rights class.

Flutter receives only the resolved runtime path.

## User state

Favorites store stable recipe IDs only. Shopping items are user-owned and independent from catalog replacement. Catalog generation/update is never user-data migration.

## Preferences

Theme and locale are small local preferences. The recipe repository follows manual locale preference when set, otherwise the device language, then the catalog default fallback.

## Entitlements

UI asks ProductLimits/capabilities, not a store SDK. Billing/RevenueCat/Play/StoreKit remain future adapters behind the entitlement seam.

## Presentation

- NavigationBar on compact width;
- NavigationRail on wide width;
- Explore, Favorites, Shopping primary destinations;
- Settings secondary;
- recipe detail pushed route;
- F3B presentation tokens sit above Material 3 so visual identity can evolve without changing domain/application seams;
- `RecipeArtwork` is a lightweight procedural no-photo fallback keyed by stable recipe ID;
- the artwork layer contains no recipe business data and can be replaced by an original/licensed `imageAsset` without changing cards or detail navigation;
- recipe detail switches from a single-column phone layout to a two-column ingredients/timer + preparation composition on wider surfaces;
- F3C decorative characters live under `core/decorative_characters`, not in recipe domain/catalog data;
- `DecorativeCharacterRegistry` owns archetype metadata, culture, motion type, compatible presentation slots and session anti-repetition memory;
- `DecorativeCharacterStage` owns native motion and reduced-motion handling, while `DecorativeCharacterArtwork` paints the original procedural archetype;
- presentation surfaces request a semantic slot such as Explore/Favorites/Shopping rather than naming a specific mascot, allowing rotation and future artwork replacement without screen rewrites;
- the current implementation permits one primary decorative mascot per screen and adds no image-animation package dependency.

## Preview boundary

`tool/build_recipe_preview.py` temporarily swaps in a compiled synthetic catalog, validates it, builds the same Flutter Web app, and restores production catalog bytes in a `finally` path.

The preview proves authoring/content wiring and shared UI buildability; it does not certify native/store behaviour.

## No architecture for architecture's sake

No backend, database engine, Markdown parser, AI SDK, vector store, ad SDK or billing SDK is introduced for F2. Deterministic Python tooling is sufficient for the current catalog size and review requirements.

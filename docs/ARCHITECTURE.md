# Architecture

## Top-level flow

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
Local adapters now / provider adapters later
```

## Deep seams

### Recipe catalog

The UI knows one interface: obtain the currently published recipes.

F1 replaces the bootstrap empty adapter with `VersionedRecipeCatalogRepository`. The adapter consumes a compact JSON runtime package through `RecipeCatalogSource`, so tests can inject in-memory assets while production uses Flutter `rootBundle`.

Runtime flow:

```text
manifest.json
  -> schema/catalog/locale contract
recipes.json
  -> canonical recipe metadata
requested locale + default locale
  -> localized editorial text
deterministic validation
  -> published Recipe domain objects
```

Unsupported or malformed input fails closed with `RecipeCatalogException`; no partial recipe list is returned.

Canonical quantities, timings, servings, ingredient IDs and step IDs are stored once. Localized files contain only user-facing title/ingredient/step wording.

### User state

Favorites store stable recipe IDs only. Shopping items are user-owned and independent from catalog replacement. Catalog update is never user-data migration.

### Preferences

Theme and locale are small local preferences. They do not need a database or account.

The recipe repository follows the manual locale preference when set, otherwise the device language, then applies the catalog default-locale fallback.

### Entitlements

UI asks ProductLimits/capabilities, not a store SDK. Billing/RevenueCat/Play/StoreKit remain future adapters behind the entitlement seam.

## Presentation

- one adaptive app shell;
- NavigationBar on compact width;
- NavigationRail on wide width;
- Explore, Favorites, Shopping primary destinations;
- Settings as a secondary action;
- recipe detail as a pushed route.

## Catalog evolution

```text
F2 authoring input
-> editorial normalization
-> compiled JSON runtime package
-> deterministic validator
-> VersionedRecipeCatalogRepository
-> published domain recipes
-> search/filter UI
```

F2 can optimize authoring ergonomics without changing the F1 runtime contract.

## No architecture for architecture's sake

No backend, auth, router package, database engine, ad SDK, billing SDK or Markdown parser is introduced until the product needs it. Add a new seam only when real variability or a high-risk provider boundary justifies it.

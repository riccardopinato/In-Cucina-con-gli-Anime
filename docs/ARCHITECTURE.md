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

The UI learns one interface: obtain the currently published recipes. The bootstrap adapter returns an empty list. A later versioned editorial catalog adapter may load validated local packages/DB content behind the same seam.

### User state

Favorites store stable recipe IDs only. Shopping items are user-owned and independent from catalog replacement. Catalog update is never user-data migration.

### Preferences

Theme and locale are small local preferences. They do not need a database or account.

### Entitlements

UI asks ProductLimits/capabilities, not a store SDK. Billing/RevenueCat/Play/StoreKit are future adapters behind the entitlement seam.

## Presentation

- one adaptive app shell;
- NavigationBar on compact width;
- NavigationRail on wide width;
- Explore, Favorites, Shopping primary destinations;
- Settings accessed as a secondary action;
- recipe detail is a pushed route.

## Catalog evolution

```text
editorial source
-> structured package
-> deterministic validator
-> versioned catalog adapter
-> published domain recipes
-> search/filter UI
```

The catalog contract must support stable identity, versions, locale fallback and provenance/rights metadata before recipe batches are added.

## No architecture for architecture's sake

No backend, auth, router package, database engine, ad SDK or billing SDK is introduced until the product needs it. Add a new seam only when real variability or a high-risk provider boundary justifies it.

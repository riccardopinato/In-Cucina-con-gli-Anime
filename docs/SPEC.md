# Product implementation specification

## Problem Statement

The project needs a commercial-grade Flutter foundation and a stable recipe-content contract before production recipes are added. Directly embedding recipes in Dart would couple editorial content, UI, localization and user state.

## Solution

Use a local-first Flutter shell with stable domain seams. Recipe content is consumed through `RecipeCatalogRepository` from a compact JSON runtime package. The package separates canonical culinary metadata from localized editorial text and is rejected if incompatible or malformed.

## User Stories

1. As a user, I want the app to open without requiring an account.
2. As a user, I want Explore, Favorites and Shopping to be obvious destinations.
3. As a user, I want the empty catalog state to remain intentional until real recipes ship.
4. As a user, I want device language by default and a manual language override.
5. As a user, I want system/light/dark appearance.
6. As a user, I want favorite IDs to persist across recipe-content revisions.
7. As a user, I want a shopping list that remains useful offline.
8. As a user, I want responsive navigation on phone and wide screens.
9. As a future paying user, I want purchases to map to a central entitlement state.
10. As a future premium user, I want ads suppressed before any ad request.
11. As a maintainer, I want stable recipe/ingredient/step IDs.
12. As a maintainer, I want schema, catalog and recipe revisions to be explicit.
13. As a maintainer, I want canonical quantities/times separated from translations.
14. As a maintainer, I want deterministic locale fallback.
15. As a maintainer, I want invalid catalog packages to fail closed.
16. As a maintainer, I want CI to validate the production catalog before Flutter analysis/tests.
17. As an editor, I want lightweight origin metadata rather than a heavy provenance database.
18. As an editor, I want future authoring tooling to generate runtime JSON without editing Dart.

## Implementation Decisions

- Flutter 3.47.3 remains the pinned toolchain.
- Riverpod owns presentation/application state.
- SharedPreferences stores small user-owned state.
- `VersionedRecipeCatalogRepository` is the production recipe adapter.
- `RecipeCatalogSource` hides the asset source and gives tests an in-memory seam.
- Runtime catalog format is JSON-only; no Markdown parser dependency.
- `schemaVersion` controls compatibility.
- `catalogVersion` versions the package.
- `contentVersion` versions one stable recipe ID.
- Canonical recipe data contains structured ingredients and ordered steps with optional timers.
- Localized files contain title, ingredient names/notes and step text only.
- Default locale is English; supported app locales are EN/IT/ES/FR/DE/PT.
- Missing recipe translation falls back to the default locale.
- A malformed present translation is rejected rather than partially merged.
- Origin metadata is `contentOrigin = original | inspired | adapted` plus optional internal `sourceNote`.
- Navigator remains sufficient for current route depth.
- Material 3 remains an implementation foundation, not a final visual constraint.
- Monetization stays behind entitlement/ProductLimits seams.
- Platform folders remain generated deterministically.

## Testing Decisions

Tests target stable external behaviour:
- localized catalog loading;
- deterministic fallback to default locale;
- unsupported schema rejection;
- duplicate stable-ID rejection;
- stable recipe identity across content revisions;
- entitlement/ProductLimits logic;
- shopping/favorite persistence behaviour;
- structural validation;
- deterministic production catalog validation.

## Out of Scope

Production recipe population, F2 authoring UI/tooling, decorative-character implementation, cloud sync, auth, notifications, live AdMob, live billing, production signing and store release.

## Further Notes

Planning follows the tracer-bullet/deep-module approach: the catalog parser/validator is hidden behind a small repository interface and F2 can change authoring ergonomics without changing runtime callers.

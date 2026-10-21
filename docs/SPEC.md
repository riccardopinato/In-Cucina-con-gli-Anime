# Foundation specification

## Problem Statement

The project needs a commercial-grade Flutter foundation before recipe content is added. Starting directly from recipe lists would couple content, UI, persistence and monetization too early.

## Solution

Build an empty but functional application shell with stable seams for catalog, user state and entitlements. Reuse App Factory Golden patterns for theme, localization, responsive shell, CI and entitlement contracts. Keep recipe content entirely outside this foundation.

## User Stories

1. As a user, I want the app to open without requiring an account, so that I can immediately understand what it is.
2. As a user, I want Explore, Favorites and Shopping to be obvious destinations, so that navigation is predictable.
3. As a user, I want the empty catalog state to explain that recipes are coming, so that the app never presents fake content.
4. As a user, I want the app to follow my device language, so that first launch feels native.
5. As a user, I want to override the language manually, so that I can choose another supported language.
6. As a user, I want system/light/dark appearance, so that the app fits my device and preferences.
7. As a user, I want favorite IDs to persist locally, so that future catalog updates do not erase my saves.
8. As a user, I want a shopping list that persists locally, so that it remains useful offline.
9. As a user, I want responsive navigation on phone and wide screens, so that Web Preview and tablets are usable.
10. As a future paying user, I want purchases to map to a central entitlement state, so that premium behaviour is consistent.
11. As a future premium user, I want ads to be suppressed before any ad request, so that Remove Ads is truthful.
12. As a maintainer, I want stable catalog IDs and versioning rules, so that editorial updates preserve user state.
13. As a maintainer, I want a deterministic platform scaffold, so that generated Android/iOS/Web files do not drift.
14. As a maintainer, I want explicit validation, so that repository state is reproducible.
15. As a publisher, I want content-rights rules from day one, so that monetization is not built on copied recipes or artwork.

## Implementation Decisions

- Flutter 3.47.3 is the bootstrap toolchain pin, following the current internal donor baseline.
- Riverpod owns presentation/application state.
- SharedPreferences stores small user preferences, favorites and shopping list state.
- Recipe content is accessed through a catalog interface; the bootstrap adapter returns an empty catalog.
- A later versioned editorial catalog adapter can replace the empty adapter without changing UI callers.
- Navigator is sufficient for current route depth; no router dependency is admitted yet.
- Material 3 tokens are reused from the Factory Golden and adapted to the product brand.
- Localization uses Flutter gen_l10n with EN/IT/ES/FR/DE/PT.
- Monetization starts at the provider-agnostic entitlement/ProductLimits seam. No store SDK is integrated yet.
- Platform folders are generated deterministically by a bootstrap script.

## Testing Decisions

Tests target external behaviour at stable seams:
- empty catalog contract;
- entitlement/ProductLimits logic;
- shopping/favorite persistence behaviour;
- core navigation/empty-state widget smoke;
- structural validator for localization parity and bootstrap invariants.

## Out of Scope

Recipe population, copyrighted media ingestion, cloud sync, auth, notifications, live AdMob, live billing, production signing and store release.

## Further Notes

Planning adopts the tracer-bullet/deep-module approach from `mattpocock/skills`: small interfaces, demonstrable roadmap slices and context pointers instead of duplicated agent policy.

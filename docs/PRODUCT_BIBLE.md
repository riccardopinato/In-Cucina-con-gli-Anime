# Product Bible — In Cucina con gli Anime

## Promise

A polished cooking companion that turns food seen in anime into practical recipes users can actually cook, save and shop for.

The product should feel warm, illustrated and playful without presenting itself as an official app of any anime studio, publisher or franchise.

## Target user

- anime/manga fans who also enjoy cooking;
- casual cooks who want approachable themed recipes;
- users looking for a visually distinctive recipe app rather than a generic database.

## MVP product surface

1. **Explore** — search, anime/reference filters, difficulty filters, responsive recipe grid.
2. **Recipe detail** — ingredients, steps, times, difficulty, timer and ingredient checklist.
3. **Favorites** — persistent saved stable recipe IDs.
4. **Shopping** — persistent shopping items and manual additions; later add ingredients from recipes.
5. **Settings** — device language by default, manual language override, system/light/dark theme.
6. **Monetization boundary** — free by default, provider-agnostic Premium/Lifetime state, future safe ads + Remove Ads.

## Current scope

F0 foundation, F1 runtime catalog contract and F2 authoring/import pipeline are complete.

The production catalog intentionally contains zero real recipes. F3 introduces the first approved production batch and the stronger visual identity.

## UX direction

Original watercolor-inspired cooking identity:
- cream/rice-paper background;
- meadow green primary;
- ember orange accent;
- pale sky secondary;
- rounded cards and low elevation;
- handwritten accent typography for display headings;
- clean rounded body typography;
- restrained motion.

F3 may move further beyond stock Material 3 and introduce lightweight animated decorative characters based mainly on Japanese/Chinese folklore and classics.

## Local-first

Core browsing of installed recipe content, favorites and shopping list should remain useful offline. Login is not required to access core value.

## Content model principles

- stable recipe IDs are independent of title/translation;
- schema, package and individual content revisions are versioned separately;
- user-owned state references stable IDs;
- catalog updates never silently erase favorites or shopping data;
- canonical quantities/times/ingredient-step identity are separated from localized editorial wording;
- locale fallback is deterministic;
- invalid/unsupported packages fail closed;
- runtime and authoring content are JSON-only;
- recipe origin tracking stays lightweight through `contentOrigin` and optional internal `sourceNote`;
- generated runtime JSON must match the authoring source deterministically;
- similarity is explainable and domain-configurable, never a destructive authority.

## Editorial workflow

User/reference material is first interpreted as culinary input. Raw copied prose is kept transient rather than committed.

The committed authoring record contains normalized facts and fresh app editorial wording. Recipes may be `original`, `inspired` or `adapted`.

Before publication:
- identity/structure validate;
- all six locales complete;
- assets resolve through the authoring asset manifest;
- duplicate/similarity gate runs;
- blocking comparisons require fingerprint-bound review;
- compiler emits the F1 catalog;
- F1 validator and app preview pass.

Visual/media assets follow a separate rights rule: prefer original, verified reusable/public-domain or intentionally licensed material.

## Monetization direction

Initial preferred model:
- free catalog access;
- non-invasive adaptive banner only on browsing surfaces after consent/provider integration;
- no ad request for entitled users;
- no ads while actively following a recipe/timer;
- one-time Remove Ads/Lifetime before considering a subscription.

Exact pricing/provider/store integration is out of scope until F4.

## Out of scope now

- remaining production recipe expansion before F3B visual review is complete;
- official anime screenshots/posters/logos/modern character artwork without a rights basis;
- account/cloud sync;
- notifications;
- meal planning;
- social/community features;
- live ads;
- live billing/store purchase;
- production signing/certification.

## Current success criteria

- deterministic Android/iOS/Web Flutter scaffold;
- versioned local JSON runtime catalog;
- deterministic authoring -> runtime compiler;
- duplicate/similarity review with stale-decision protection;
- production catalog contains the first five F3A recipes;
- Explore/Favorites/Shopping navigation works;
- localization/theme/settings infrastructure exists;
- stable user-state persistence seams exist;
- entitlement boundary is provider-agnostic;
- CI validates authoring, generated catalog, Flutter tests and production/fixture Web builds;
- new recipes can be added without editing Dart.

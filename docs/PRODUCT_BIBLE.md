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

F0 foundation, F1 runtime catalog contract, F2 authoring/import pipeline and F3A content ingestion are complete.

The production catalog contains all 10 recipes from the supplied reference document, rebuilt editorially and localized in EN/IT/ES/FR/DE/PT. F3 is complete: F3B provides the editorial visual identity and F3C adds the optional recipe-independent decorative-character layer. F4 monetization is next.

## UX direction

Implemented F3B identity:
- Japanese-contemporary editorial cookbook rather than stock Material presentation;
- cream/rice-paper surfaces with meadow green, ember/apricot, matcha, sky and plum accents;
- handwritten Caveat accent only for display/wordmark moments, with clean system body typography;
- large rounded editorial containers, low elevation and strong spacing hierarchy;
- ten deterministic procedural recipe illustrations keyed by stable recipe IDs;
- procedural illustration is the default no-photo treatment and remains replaceable by future original/licensed food photography;
- responsive recipe detail: single-column on phone, two-column editorial composition on wider layouts;
- restrained motion and lightweight rendering; no animated-image dependency.

Implemented F3C character layer:
- six original procedural mascots based on Japanese/Chinese traditional archetypes: Kitsune, Kappa, Tanuki, Oni, Sun Wukong and Chinese Dragon;
- character identity is kept outside recipe/catalog data;
- contextual slots select compatible mascots and prevent immediate repetition;
- native Flutter float/peek/sway motion only, with reduced-motion support;
- Explore uses one rotating primary mascot; empty Favorites and Shopping use contextual mascots;
- no GIF/Lottie/Rive or third-party character-art dependency in the initial implementation.

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
- production catalog contains all 10 recipes from the supplied F3A document;
- Explore/Favorites/Shopping navigation works;
- Explore/cards/detail share the F3B editorial visual system across the full 10-recipe catalog;
- F3C decorative mascots are recipe-independent, contextual, lightweight and reduced-motion aware;
- localization/theme/settings infrastructure exists;
- stable user-state persistence seams exist;
- entitlement boundary is provider-agnostic;
- CI validates authoring, generated catalog, Flutter tests and production/fixture Web builds;
- new recipes can be added without editing Dart.

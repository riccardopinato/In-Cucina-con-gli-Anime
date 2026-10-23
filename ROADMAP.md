# Roadmap

The roadmap uses tracer-bullet slices: each step should end in something demonstrable and leave CI green.

## F0 — Foundation shell — PASS

Blocked by: none.

Delivered the product/architecture baseline, deterministic Flutter shell, localization, responsive navigation, local preferences/favorites/shopping, entitlement seam, CI and Web Preview.

Exit: PASS — PR #1 merged with development checks green.

## F1 — Versioned recipe catalog contract — PASS

Blocked by: F0.

Delivered:
- JSON-only runtime catalog; no Markdown parser dependency;
- stable recipe/ingredient/step IDs;
- schema, catalog and per-recipe content versions;
- canonical culinary metadata separated from localized editorial text;
- structured ingredients and steps with optional step timers;
- EN/IT/ES/FR/DE/PT locale assets with deterministic fallback to English;
- lightweight `contentOrigin`: `original | inspired | adapted`;
- optional internal-only `sourceNote`;
- deterministic Python catalog validator wired into CI;
- runtime defensive validation and fail-closed `RecipeCatalogException`;
- stable-ID regression tests across catalog revisions;
- production catalog still contains zero real recipes.

Exit: PASS — valid package loads deterministically, invalid/unsupported packages are rejected without partial data, and stable IDs survive content revisions.

## F2 — Recipe authoring/import pipeline — PASS

Blocked by: F1.

Delivered:
- per-recipe JSON authoring contract, schema and template outside Flutter source;
- transient-input policy: raw copied source material is not committed;
- deterministic authoring validation for identity, quantities, timings, ingredients, steps and editorial origin;
- published-locale completeness gate for EN/IT/ES/FR/DE/PT;
- minimal rights-aware asset manifest with stable asset IDs;
- compiler from authoring records to the exact F1 runtime package;
- CI drift gate proving committed runtime JSON matches production authoring source;
- Duplicate & Similarity Review Gate using configurable multi-dimensional comparison;
- explicit ingredient aliases and unit conversions;
- explainable comparison reports with per-dimension scores/differences/recommended action;
- blocking `probable_duplicate` / `review_required` classifications until fingerprint-bound human review;
- review-memory invalidation when either recipe changes;
- candidate review CLI before import;
- synthetic six-locale non-production fixture;
- temporary synthetic Flutter Web preview that restores the empty production catalog afterward;
- Python regression coverage for compiler, localization, synonym/unit normalization, false-positive resistance, review invalidation and deterministic reports;
- zero new Flutter/runtime dependencies.

Exit: PASS — a synthetic recipe travels normalized authoring JSON -> validation -> similarity gate -> runtime compilation -> F1 validation -> real Flutter Web build without editing Dart or shipping the fixture.

## F3 — First real editorial batch + visual identity — PASS

Blocked by: F2 — unblocked.

### F3A — First production editorial batch — PASS

Delivered:
- all ten recipes from the supplied reference document authored through the F2 pipeline;
- stable IDs `recipe_000001` through `recipe_000010`;
- fresh editorial copy derived from user-provided culinary reference material rather than copied source prose;
- EN/IT/ES/FR/DE/PT localized content for every published recipe;
- editorially documented serving estimates where the source material omitted yield;
- runtime catalog version `0.4.0`;
- app version `0.5.0+5`;
- production catalog generation with no Dart edits;
- similarity/duplicate gate applied to the real batch;
- F1 runtime validation and CI build gates retained.

First batch:
1. Skillet eggs with crispy bacon — inspired by `Il castello errante di Howl`;
2. Miso ramen with chashu — inspired by `Naruto`;
3. Victory katsudon — inspired by `Yuri!!! on ICE / My Hero Academia`;
4. Dorayaki with anko — inspired by `Doraemon`;
5. Tuna mayo onigiri — inspired by `La città incantata / Pokémon`;
6. Kansai-style okonomiyaki — inspired by `Ranma ½ / Kiss Me Licia`;
7. Takoyaki with octopus — inspired by `One Piece / My Hero Academia`;
8. Ketchup omurice — inspired by `K-On! / Maid Sama!`;
9. Chicken and egg oyakodon — inspired by `Yuri!!! on ICE / Food Wars!`;
10. Pumpkin and fish puff-pastry bake — inspired by `Kiki - Consegne a domicilio`.

Exit: PASS when exact PR head is green for authoring validation, similarity gate, generated-catalog drift, F1 validation, Flutter analyze/test, synthetic preview and production Web build.

### F3B — Visual identity redesign — PASS

Delivered:
- Japanese-contemporary editorial cookbook direction layered over the existing Material 3 infrastructure;
- expanded rice-paper / meadow / ember / matcha / plum design tokens for light and dark themes;
- editorial Explore header, integrated search and horizontally scrollable anime/difficulty filter rails;
- redesigned recipe cards with stronger hierarchy, reference treatment, favorite affordance and compact metadata;
- deterministic procedural artwork keyed by stable recipe IDs, with ten distinct treatments for the current catalog;
- procedural art used only as a no-photo fallback, so future original/licensed photography can replace it without architecture changes;
- redesigned recipe detail hero and summary facts for prep, cook, difficulty and servings;
- responsive two-column tablet/Web detail layout with ingredients/timer separated from preparation steps;
- editorial ingredient checklist, step cards and redesigned cooking timer;
- Favorites inherits the same recipe-card identity;
- EN/IT/ES/FR/DE/PT visual-surface copy parity;
- removed the unused `flutter_staggered_animations` dependency;
- automated smoke coverage proving all ten procedural identities render;
- app version `0.6.0+6`.

Exit: PASS — exact PR head green for structure, authoring/catalog gates, localization, Flutter analyze/test, synthetic Web preview and production Web build.

### F3C — Dynamic Decorative Characters — PASS

Blocked by: F3B — unblocked.

Delivered:
- recipe-independent `DecorativeCharacterRegistry` with explicit culture, motion and compatible-screen slots;
- six original procedural archetypes: Kitsune, Kappa, Tanuki, Oni, Sun Wukong and Chinese Dragon;
- Japanese and Chinese traditional/folklore references only; no copied modern character designs;
- zero bitmap/GIF/Lottie/Rive asset dependency for the initial character set;
- native Flutter `float`, `peek` and `sway` microanimations;
- contextual candidate filtering plus entropy-based rotation;
- immediate anti-repetition per slot and globally within the running session;
- reduced-motion support through `MediaQuery.disableAnimations`;
- Explore hero integration plus contextual empty-state mascots for Favorites and Shopping;
- registry-ready search/wide editorial slots for later use;
- generally one primary animated mascot per screen;
- automated tests for culture/motion coverage, slot coverage, anti-repetition, six-character rendering and reduced-motion behavior;
- no new runtime dependency; stale `flutter_staggered_animations` removed;
- app version `0.7.0+7`.

Exit: PASS — exact PR head green for structure/catalog gates, Flutter analyze/test, synthetic Web preview and production Web build; merged-main verification also green for Pages/Web Preview and Android ARM64 artifact.

## F4 — Monetization v1 — CURRENT

Blocked by: F3 — unblocked.

Goal: introduce monetization without weakening offline-first behaviour, cooking UX, privacy or the existing provider-agnostic entitlement boundary.

### F4A — Consent + privacy foundation — PASS

Delivered:
- provider-agnostic consent state with separate local preference and provider-resolution gates;
- local ad-privacy preference persisted through SharedPreferences;
- provider eligibility starts unresolved on every launch and is never restored as trusted state from local storage;
- privacy/settings surface for allow, block and reset choices;
- fail-closed ProductLimits gate: ad requests require local allow + trusted provider eligibility + non-entitled user;
- no account requirement for core catalog access;
- privacy-policy/store-metadata checklist kept separate from runtime logic;
- deterministic tests with no live ad inventory and no AdMob dependency.

Exit:
- PASS: app remains usable with consent unresolved or blocked;
- PASS: privacy preference survives restart while provider eligibility does not;
- PASS: tests prove local allow alone cannot reach the ad-request path;
- PASS: no ad/billing SDK or production identifier added in F4A.

### F4B — Entitlement + one-time purchase seam — IMPLEMENTED / SANDBOX PROOF PENDING

Delivered in code:
- provider-agnostic entitlement contract remains the UI source of truth;
- one-time Remove Ads / Lifetime capability precedes any subscription plan;
- official Flutter `in_app_purchase` adapter is isolated behind PurchaseGateway;
- Web Preview uses a no-op billing adapter and remains buildable;
- billing is disabled by default and enabled only through explicit build configuration;
- store price/title/description come from ProductDetails rather than hardcoded production values;
- purchase/restore events require a separate verifier before Lifetime can be granted;
- F4B sandbox verifier is opt-in only and must never be enabled for a production build;
- verified Lifetime state is cached locally as `offlineCache`, never reconstructed as `providerVerified`;
- entitled users continue to produce zero ad requests through ProductLimits;
- tests cover verified purchase, verified restore, restart persistence and verification failure;
- no RevenueCat dependency; the official store plugin is currently the smallest sufficient adapter.

Provider decision:
- use `in_app_purchase ^3.3.1` for Android/iOS store transport;
- retain the existing provider-agnostic entitlement seam so RevenueCat or a server verifier can replace verification later without UI changes;
- product ID: `remove_ads_lifetime`;
- default billing flag: OFF.

Exit:
- PENDING: real Google Play/App Store sandbox purchase + restore evidence;
- PASS in automated code coverage: free/entitled states, persisted offline Lifetime, verification failure and zero-ad-request entitlement behaviour;
- PASS: UI has no direct billing SDK dependency;
- PASS: no production billing secret or optimistic entitlement path exists.

See `docs/BILLING_SANDBOX_CHECKLIST.md`.

### F4C — Safe adaptive browsing ads

Delivers:
- adaptive banner placement only on low-interruption browsing surfaces;
- no ads on active recipe-following/timer flows;
- no interstitial/rewarded format in v1;
- no ad request for entitled users;
- loading/failure states do not shift core recipe controls or block navigation;
- Web Preview remains buildable even when native ad capability is unavailable.

Candidate surfaces:
- Explore below/between editorial sections where layout remains stable;
- Favorites only when content exists and the placement does not compete with primary actions;
- never inside ingredient/step/timer interaction zones.

Exit:
- free-user ad path works in test/sandbox mode;
- entitled-user network/request path is absent;
- active cooking remains ad-free by automated/QA evidence.

### F4D — Monetization QA + store sandbox proof

Delivers:
- consent denied / accepted / changed scenarios;
- purchase success / cancel / failure / restore scenarios;
- free vs entitled regression matrix;
- offline launch behaviour;
- app restart persistence;
- Android ARM64 + Web Preview gates remain green;
- app-size delta recorded and reviewed before merge.

Exit: F4 PASS only when consent, entitlement, restore and ad-request suppression have test/sandbox evidence and no cooking-flow regression.

## F5 — Release hardening

Blocked by: F4.

### F5A — Production signing + release artifacts

Delivers:
- persistent Android signing configured outside source control;
- reproducible release AAB;
- APK/AAB hashes and version evidence;
- release notes/versioning discipline.

### F5B — Device + platform QA

Delivers:
- physical Android validation on at least one lower/mid-range and one recent device when available;
- phone/tablet responsive review;
- light/dark/system theme;
- six-locale smoke pass;
- offline launch/catalog/favorites/shopping;
- timer/background/resume behaviour;
- accessibility/reduced-motion checks.

### F5C — Store readiness

Delivers:
- final privacy/data-safety review;
- screenshots/listing assets and localized metadata;
- monetization disclosures;
- rights/content review for recipe references and visual assets;
- certification evidence required by the current App Factory release Golden;
- AppLab FULL only if the AppLab capability is actually available in the execution environment.

Exit: release candidate is signed, reproducible, physically validated and ready for store submission without unresolved blocking checklist items.

## Later candidates

Collections/menu planning, ingredient scaling, pantry mode, timers per step, shareable cards, optional Google Sign-In + backup, remote content packs and seasonal editorial packs.

Visual-system candidates:
- richer character idle states such as blink/bounce/breathing;
- Lottie or Rive only where native Flutter animation is insufficient;
- seasonal character sets;
- contextual character behaviour by section, season or recipe theme;
- thematic decorative collections while keeping runtime and asset weight under control.

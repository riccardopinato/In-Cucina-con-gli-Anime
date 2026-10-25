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

### F3D — Original recipe artwork direction — PASS

Delivered:
- approved premium anime-food visual direction: close food-first composition, warm light, appetizing glossy texture and minimal background;
- card geometry remains unchanged; real artwork is cropped only at render time;
- recipe detail shows the full asset and no longer repeats the recipe title in the collapsing app bar;
- direct anime frames/third-party artwork remain excluded.

### F3E — Recipe asset pipeline hardening — PASS

Delivers:
- one canonical image per recipe; no duplicated card/full asset;
- image IDs owned by authoring data rather than Dart pilot maps;
- explicit dish-semantic review tied to recipe content version;
- deterministic batch artwork queue for multi-recipe processing;
- JPEG dimension/weight gates plus a pinned build-time optimizer;
- orphan/incorrect/stale artwork fails closed;
- wrong Katsudon stand-in removed; recipe_000003 returns to procedural fallback until exact artwork is approved;
- initial approved artwork established with recipe_000002 ramen and recipe_000009 oyakodon; F3F extends the same contract across the catalog.

Exit:
- materialized assets meet <= 140 KiB hard budget with >= 720 px short edge;
- generated catalog is current;
- Python authoring tests, Flutter decode test, analyze/test, Web and Android gates are green on the exact PR head;
- no pilot-only Dart mapping or orphan image remains.

Evidence:
- validated implementation head `c436989761a10d13c4838b37d06ca134bf0a0095`;
- Development checks run `39966691212`: materialization drift, authoring/catalog validation, Flutter analyze/test, synthetic Web preview, production Web release and Android ARM64 artifact all PASS;
- committed artwork sizes: ramen 132092 bytes, oyakodon 111776 bytes;
- recipe_000003 has no image asset until an exact Katsudon artwork is approved.

### F3F — Twenty-recipe editorial + artwork batch — PASS

Delivered:
- second production batch from the user-provided 10-recipe research PDF, assigned stable IDs `recipe_000011` through `recipe_000020`;
- all new recipes localized EN/IT/ES/FR/DE/PT and integrated through the authoring pipeline;
- source contradictions audited instead of copied blindly: Chaliapin Steak Don timing corrected because its method includes a 30-minute onion rest; Nikuman timing corrected because its method includes a 60-minute proof plus steaming;
- all eight previously missing artworks completed, including corrected Katsudon and tuna-mayo onigiri generations after semantic visual review;
- all ten new recipes receive original anime-inspired food artwork;
- catalog now has one canonical artwork for every published recipe (20/20), with the same asset cropped on cards and shown whole in detail;
- committed new artwork is already below the F3E 140 KiB hard limit before CI optimization;
- Okonomiyaki terminology corrected from source label `Aoki` to culinary `aonori` while retaining the stable internal ingredient ID;
- Android ARM64 build/upload restored as a universal PR gate instead of the old F3D-branch-only condition;
- materialized catalog artifact is uploaded before drift validation so future batch updates remain recoverable/automatable;
- app version `0.9.0+9`; runtime catalog version `0.6.0`.

Second batch:
11. Chaliapin Steak Don — `Food Wars! (Shokugeki no Souma)`;
12. Gotcha Pork Roast — `Food Wars! (Shokugeki no Souma)`;
13. Japanese Curry Rice — `Persona 5 / Assassination Classroom`;
14. Spicy Mapo Tofu — `Angel Beats! / Food Wars!`;
15. Nikujaga — `Demon Slayer / Inuyasha`;
16. Karaage — `Haikyuu!! / Food Wars!`;
17. Tamagoyaki — `Demon Slayer / Pokémon`;
18. Nikuman — `Dragon Ball / La città incantata`;
19. Mitarashi Dango — `Naruto / Demon Slayer`;
20. Taiyaki — `My Hero Academia / Kanon`.

Exit:
- authoring + duplicate/similarity gates green for all twenty recipes;
- generated-catalog drift resolved and F1 runtime validation green;
- all twenty artwork assets decode and meet F3E size/dimension gates;
- Flutter analyze/test + Web release + Android ARM64 gates green on exact PR head;
- PR merged without unresolved blocking review.

## F3G — 50-recipe editorial quality upgrade — CURRENT

Blocked by: F3F — unblocked.

Goal: expand the catalog from 20 to 50 recipes while upgrading all existing and incoming recipes to a verified, cookable editorial standard rather than optimizing for recipe count.

Scope:
- F3G-0: culinary + anime-reference audit for all 30 incoming recipes;
- F3G-A: recipe_000021..recipe_000030;
- F3G-B: recipe_000031..recipe_000040;
- F3G-C: recipe_000041..recipe_000050;
- F3G-D: re-audit and editorial expansion of recipe_000001..recipe_000020;
- F3G-E: final 50/50 consistency, duplicate/similarity, artwork, localization and physical-device QA.

Required quality:
- culinary existence and technique verified before publication;
- source errors corrected rather than copied;
- richer recipe descriptions and materially more detailed preparation steps;
- real elapsed time includes proofing/resting/chilling/marinating/cooling;
- structured anime-reference semantics: verified appearance / recurring association / inspired / unverified;
- episode/chapter shown only when verified;
- no copied anime dialogue;
- EN/IT/ES/FR/DE/PT parity;
- one canonical semantically reviewed original artwork per published recipe;
- existing 20 recipes upgraded to the same standard as the new 30.

Evidence:
- initial incoming audit: `docs/F3G_CULINARY_ANIME_REFERENCE_AUDIT.md`.

Exit: 50 published recipes pass authoring/catalog validation, culinary/editorial review, duplicate/similarity review, localization, artwork gates, Flutter tests, Web build, Android build and physical-device smoke QA.

## F4 — Monetization v1 — DEFERRED UNTIL F3G PASS

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

### F4B — Entitlement + one-time purchase seam — NEXT

Delivers:
- keep the existing provider-agnostic entitlement contract as the UI source of truth;
- introduce one-time Remove Ads / Lifetime capability before considering subscription plans;
- purchase/restore adapter behind the entitlement boundary;
- entitled users trigger zero ad requests, not merely hidden ad widgets;
- purchase state survives app restarts and supports restore flow;
- sandbox/test provider configuration only; no production secrets in the repository.

Provider decision:
- select the smallest reliable store/billing integration that preserves the current entitlement seam;
- RevenueCat remains optional, not mandatory, unless its operational value justifies the dependency.

Exit:
- sandbox purchase + restore evidence exists;
- free and entitled states are covered by tests;
- UI does not directly depend on a billing SDK.

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

Early evidence already completed before F5 opens:
- persistent Android signing active in CI with the documented certificate fingerprint;
- first persistent-signed APK physically installed and user-confirmed working on 2026-10-25;
- all twenty current recipe artworks user-confirmed correct on the physical phone;
- update-in-place continuity physically VERIFIED on 2026-10-25: later persistent-signed APK installed over the existing app without uninstalling and existing Favorites were preserved;
- production AAB / exact release artifact evidence remains part of F5A and is not claimed by this early internal validation.

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

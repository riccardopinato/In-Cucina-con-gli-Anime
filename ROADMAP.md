# Roadmap

The roadmap uses tracer-bullet slices: each step should end in something demonstrable and leave CI green.

## F0 — Foundation shell — PASS

Blocked by: none.

Delivered:
- Product Bible + rights policy + architecture;
- App Factory bootstrap manifest and Golden reuse map;
- deterministic Flutter Android/iOS/Web scaffold;
- original launcher-icon source;
- Material 3 light/dark brand theme;
- EN/IT/ES/FR/DE/PT localization infrastructure;
- responsive Explore / Favorites / Shopping shell;
- empty catalog adapter (zero recipes);
- persistent preferences/favorites/shopping;
- provider-agnostic entitlement/ProductLimits;
- dev CI + Web Preview workflow;
- baseline tests.

Exit: PASS — PR #1 merged with development checks green.

## F1 — Versioned recipe catalog contract — CURRENT

Blocked by: F0 — unblocked.

Delivers a validated local catalog package with:
- JSON-only structured recipe content; no Markdown runtime/parser dependency;
- stable recipe IDs independent from title, locale, asset name or content revision;
- explicit schema/catalog/content versioning;
- canonical structured metadata separated from localized editorial text;
- locale fallback with deterministic behaviour;
- lightweight editorial origin metadata:
  - `contentOrigin`: `original`, `inspired` or `adapted`;
  - optional internal-only `sourceNote`;
- deterministic validator for IDs, versions, required fields, localization parity, assets, internal references and publication state;
- fail-closed loading for unsupported or invalid catalog packages;
- compatibility rules so favorites and other user state survive catalog replacement;
- only synthetic/non-production fixtures in tests: still zero real recipes.

Exit: invalid or unsupported packages are rejected deterministically, valid packages load correctly and user state remains stable across catalog revisions.

## F2 — Recipe authoring/import pipeline

Blocked by: F1.

Delivers tooling to add recipes without editing Dart:
- authoring schema/templates aligned with the F1 contract;
- ingestion of user-provided/raw recipe material as editorial input;
- normalization of ingredients, quantities, timings, servings and ordered steps;
- creation of original app editorial wording while preserving the culinary meaning of the source material;
- generation of catalog-compliant JSON;
- asset manifest;
- localization completeness report;
- lightweight editorial-origin checks;
- preview/build command.

Exit: one non-production fixture can travel raw input -> editorial normalization -> JSON generation -> validation -> app preview.

## F3 — First real editorial batch + visual identity

Blocked by: F2.

Delivers:
- the first production recipe batch for the app;
- end-to-end search/filter/detail/timer/favorites/shopping on real content;
- visual refinement beyond stock Material 3 while preserving the underlying design-system architecture;
- Dynamic Decorative Characters system for intentional empty/decorative spaces.

Editorial rules:
- recipes may be original, inspired or adapted from material supplied for editorial processing;
- source wording is not copied verbatim into production content;
- recipe data is normalized into the app schema before publication;
- exact batch size is decided at implementation time.

Dynamic Decorative Characters — target direction:
- cultural scope primarily Japanese and Chinese folklore/classics coherent with the anime theme;
- no dependency on modern copyrighted character artwork unless rights are explicitly cleared;
- prefer original illustrations or verified rights-compatible/public-domain source material;
- transparent, optimized WebP/PNG assets;
- native Flutter microanimations first: `float`, `peek`, `sway`;
- contextual or randomized rotation with anti-repetition;
- generally no more than one primary animated decorative character visible per screen;
- suitable placements: empty states, section headers, editorial gaps and wider tablet/web layouts;
- architecture kept independent from recipe content so assets/behaviours can evolve later.

Exit: the first real content batch and the refined visual system work end-to-end without compromising app weight or core usability.

## F4 — Monetization v1

Blocked by: F3.

Delivers consent/privacy, safe adaptive browsing ads, no ads during active cooking, one-time Remove Ads/Lifetime and entitlement-driven no-ad-request behaviour.

Exit: provider/store sandbox evidence exists.

## F5 — Release hardening

Blocked by: F4.

Delivers persistent Android signing, release AAB/hash evidence, AppLab FULL, physical-device validation and store readiness review.

## Later candidates

Collections/menu planning, ingredient scaling, pantry mode, timers per step, shareable cards, optional Google Sign-In + backup, remote content packs and seasonal editorial packs.

Visual-system candidates:
- richer character idle states such as blink/bounce/breathing;
- Lottie or Rive only where native Flutter animation is insufficient;
- seasonal character sets;
- contextual character behaviour by section, season or recipe theme;
- thematic decorative collections while keeping runtime and asset weight under control.

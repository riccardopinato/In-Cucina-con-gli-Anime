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

## F2 — Recipe authoring/import pipeline — CURRENT

Blocked by: F1 — unblocked.

Delivers tooling to add recipes without editing Dart:
- authoring schema/templates aligned with the F1 contract;
- ingestion of user-provided/raw recipe material as editorial input;
- normalization of ingredients, quantities, timings, servings and ordered steps;
- creation of original app editorial wording while preserving culinary meaning;
- generation of catalog-compliant JSON;
- asset manifest;
- localization completeness report;
- lightweight editorial-origin checks;
- preview/build command.

Exit: one non-production fixture can travel raw input -> editorial normalization -> JSON generation -> validation -> app preview.

## F3 — First real editorial batch + visual identity

Blocked by: F2.

Delivers:
- first production recipe batch;
- end-to-end search/filter/detail/timer/favorites/shopping on real content;
- visual refinement beyond stock Material 3 while preserving design-system architecture;
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
- contextual/randomized rotation with anti-repetition;
- generally no more than one primary animated decorative character visible per screen;
- suitable placements: empty states, section headers, editorial gaps and wider tablet/web layouts;
- architecture independent from recipe content.

Exit: first real content batch and refined visual system work end-to-end without compromising app weight or core usability.

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

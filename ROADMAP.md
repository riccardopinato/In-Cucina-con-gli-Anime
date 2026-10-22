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

## F3 — First real editorial batch + visual identity — CURRENT

Blocked by: F2 — unblocked.

Delivers:
- first production recipe batch authored through the F2 pipeline;
- duplicate/variant review for each incoming batch before publication;
- end-to-end search/filter/detail/timer/favorites/shopping on real content;
- visual refinement beyond stock Material 3 while preserving design-system architecture;
- Dynamic Decorative Characters system for intentional empty/decorative spaces.

Editorial rules:
- recipes may be original, inspired or adapted from material supplied for editorial processing;
- raw source prose remains transient and production wording is written for this app;
- recipe data is normalized into the authoring schema before publication;
- duplicate/similarity reports inform review but never auto-delete/overwrite;
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

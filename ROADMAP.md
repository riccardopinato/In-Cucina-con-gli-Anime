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

### F3C — Dynamic Decorative Characters — CURRENT

Blocked by: F3B — unblocked.

Delivers:
- reusable decorative-character registry independent from recipe content;
- Japanese/Chinese folklore/classic archetypes only unless rights are separately cleared;
- original or verified reusable transparent WebP/PNG assets;
- native Flutter microanimations first: `float`, `peek`, `sway`;
- contextual/randomized rotation with anti-repetition;
- generally no more than one primary animated decorative character visible per screen;
- suitable placements: empty states, section headers, editorial gaps and wider tablet/web layouts.

Exit: decorative motion improves identity without materially increasing app weight, distracting from cooking tasks or creating rights ambiguity.

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

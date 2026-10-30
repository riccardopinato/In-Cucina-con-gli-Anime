# Roadmap

> **Current cross-app baseline resolved 2026-10-29:** App Factory Core **Master v27 ACTIVE** / Golden Index **v23** (`174a05e165076c9e4b2d61a20acd85ca6b215f12`); AppLab **v6.2 SELF_CANARY** (`636490e58d38c3910eb168197cde72adb9cdb3f9`). Resolve `CURRENT.yaml` again only on explicit/core update; old Factory v26.6 pointers are historical.
>
> **Detailed current execution roadmap:** [Factory v27 / AppLab v6.2 — Cooking Anime, 29 October 2026](docs/ROADMAP_FACTORY_V27_APPLAB_V62_2026-10-29.md). **Active P0:** unblock PR #41 F3K 101 short descriptions + F3L two semantic warnings, then exact-head CI and verified merge. Next: qualified culinary/translation review, gated runtime promotion, then new recipe images matching the first 50, then scoped monetization/release.
>
> Existing F0–F5 sections below preserve historical implementation evidence and original stage contracts. Where a legacy `CURRENT` or `NEXT` label conflicts with the detailed current roadmap, reconcile against the latest real commit and CI; never treat a staged draft as publication or an AppLab self-canary as autonomous editing rights for this app.


## R1 Quality Engine v2 — autonomous read-only pilot (separate from culinary certification)

Implementation branch `feat/r1-quality-engine-v2-readonly`: three source-bound, parallel, recurring GitHub Actions analysis lanes for **code, content and workflow security hygiene**. The portable stdlib scanner, configuration, regression tests and workflow are specified in [R1 Quality Engine v2 Pilot](docs/R1_QUALITY_ENGINE_V2_PILOT.md). This is a *technical observation tool*, not human food-safety certification.

**Current deliverable status:** implementation PR / exact-head CI pending. The hourly trigger activates only after merge to `main`; schedules are best-effort, not a 24/7 process. All operation is read-only with no automatic writes, repairs, PR merges, publication or AppLab SELF_CANARY promotion. Existing R1 culinary PR #44 remains draft with 112 recipes and 10 components awaiting qualified review. Factory v27 remains pinned, and future App-Factory-Core reuse needs separate governance.

## R1 Quality Engine v2.1 — longitudinal monitoring (separate from R1 culinary clearance)

v2.0 read-only observer is merged on `main` as PR #46. v2.1 adds source-bound per-lane **NEW / PERSISTING / RESOLVED / REOPENED / UNBASELINED** lifecycle state, with cumulative snapshots read from successful `main` GitHub Actions artifacts and stored for 14 days. This is **NOT permanent central storage** and does not authorize autonomous repair. See [R1 Quality Engine v2.1 History](docs/R1_QUALITY_ENGINE_V21_HISTORY.md). **Execution status:** PR in progress; CI/merge gate pending. Future App-Factory-Core extraction and any repair writer require separate approval. R1 culinary PR #44 remains draft and all 122 reviews PENDING.

## Quality Engine v2.2 — autonomous diagnostic proposals (separate from culinary approval)

Following merged v2.1 on `main` (PR #47), v2.2 introduces a **read-only L1 diagnoser** over source-bound v2 scan + v2.1 delta. It generates specific review proposals by rule and reviewer role in three parallel CI lanes. It does **not** modify code, auto-open PRs, certify content or change release/runtime gates; the roadmap for isolated writer/draft PR L2 and possible bounded L3 automerge remains a **future, separately approved** milestone. See [R1 Quality Engine v2.2 Diagnoser](docs/R1_QUALITY_ENGINE_V22_DIAGNOSER.md). **Execution status:** PR candidate; exact-head CI and review required before merge. R1 culinary PR #44 remains draft, 122 records pending.

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
- F3G implementation evidence — 2026-10-25:
  - F3G-A: recipe_000021..recipe_000030 authored in EN/IT/ES/FR/DE/PT with culinary corrections;
  - F3G-B: recipe_000031..recipe_000040 authored and normalized;
  - F3G-C: recipe_000041..recipe_000050 authored, including corrected Champon/Miso/Kashiwa and verified Food Wars/Gintama references;
  - F3G-D: recipe_000001..recipe_000020 re-audited without changing stable IDs; descriptions, detailed steps and anime-reference semantics upgraded;
  - recipe_000019 rebuilt as true Mitarashi Dango;
  - recipe_000020 now includes the real taiyaki batter rest;
  - existing user-approved artwork semantic reviews advanced to the new content versions;
  - F3G-E automated repository scope completed: runtime catalog 0.7.0 materialized at 50 recipes, duplicate/similarity blockers closed, and 30 new original JPEG artworks installed so all 50 published recipes resolve a semantically reviewed artwork asset;
  - artwork manifest now contains 50 approved recipe assets and the generated runtime has zero missing `imageAsset` values;
  - full F3G PASS remains gated only by final physical-device smoke of the expanded 50-recipe catalog.

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
- the initial twenty recipe artworks user-confirmed correct on the physical phone;
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


### F3H — Recipe editorial hardening — PASS

Delivered:
- P0/P1/P2 recipe audit findings closed;
- legacy preparation order and ingredient coherence hardened;
- anime-reference semantics normalized;
- 13 weak/mismatched recipe artworks regenerated and committed;
- placeholder regression gate added;
- canonical authoring validation PASS;
- similarity unresolved blocking: 0;
- runtime remains 50 recipes / 50 artwork bindings;
- exact-head Development checks green and PR #21 merged to `main`.

### F3I — Motion polish — PASS

Goal: add lightweight, tactile motion before expanding the recipe catalog further, without adding runtime dependencies or weakening reduced-motion accessibility.

Delivered in the implementation branch:
- recipe cards compress slightly on touch and use a subtle artwork zoom on pointer hover;
- favorite feedback keeps its existing heart pop and now respects reduced-motion;
- checked ingredients gain a soft surface transition and one-shot check pop;
- cooking timer progress animates smoothly, the timer icon breathes while active, and completion gets a short pulse before the dialog;
- recipe detail content enters with a small fade + vertical slide while preserving the existing image Hero transition;
- F3C procedural mascots gain a dedicated `recipeCardCorner` slot;
- about one recipe card in six gets a brief deterministic corner peek, with additional short mascot feedback when a recipe is added to Favorites;
- passive mascot motion is sparse, transient and never requires a new bitmap/GIF/Lottie/Rive dependency;
- all new motion paths fail closed to static UI when `MediaQuery.disableAnimations` is enabled;
- app version `0.10.0+10`.

Evidence:
- implementation head `1eb523bd3f829ba4410c87f6729a10f3ff736ea5` passed Development checks run `40219047598`: authoring/catalog gates, Flutter analyze/test, synthetic Web preview, production Web release and persistent-signed Android ARM64 artifact all PASS;
- merge policy remains: the final branch head must be green before merge.


## F3J — Catalog expansion to 162 recipes — PASS

Blocked by: F3H/F3I — unblocked.

Goal: expand the reviewed production catalog from 50 to 162 recipes before the next artwork campaign.

Scope:
- import 112 user-supplied reviewed recipes as stable IDs `recipe_000051` through `recipe_000162`;
- exclude the eight candidates previously classified as duplicates or too similar;
- correct the two editorial issues before import: `Tofu Dengaku` and `Matcha Daifuku con Anko`;
- keep `imageAssetId: null` for recipes 51–162 so the existing deterministic procedural artwork remains the temporary visual fallback;
- preserve complete EN/IT/ES/FR/DE/PT localization and F3G editorial gates;
- materialize runtime catalog version 0.8.0 and keep similarity/validation gates green.

Exit:
- 162 published recipes materialized deterministically;
- zero unresolved blocking similarity comparisons;
- authoring/runtime validation green;
- Flutter analyze/test + Web/Android CI green on exact PR head;
- PR merged to `main`.


## F3K — Italian editorial hardening 51–162 — CURRENT

Blocked by: F3J — unblocked.

Goal: make the 112 recipes added in F3J genuinely complete and cookable in Italian before any translation refresh is allowed.

Non-negotiable sequencing:
1. freeze a 100% Italian source baseline for `recipe_000051` through `recipe_000162`;
2. exact-head CI must pass the dedicated F3K Italian quality gate;
3. only after that PASS may EN/ES/FR/DE/PT translation work begin;
4. any later material Italian edit invalidates the translation baseline and re-locks translation work.

Implemented Italian staging baseline:
- 112/112 recipes covered;
- no fixed four-step quota: procedures use the number of meaningful steps required by the dish;
- minimum 6 meaningful steps, median 8, maximum 13;
- minimum 100 procedure words, median 124, maximum 204;
- dish-specific descriptions, minimum 40 words, with near-duplicate copy blocked;
- ingredient quantities are measured or explicitly `q.b.`;
- reusable subcomponents resolve explicitly instead of relying on unexplained ready-made chashu/kakuni/curry/yakisoba/karaage/etc.;
- real elapsed time includes rests, proofing, chilling, freezing, marinades and long simmering where relevant;
- all 224 anime associations reviewed individually;
- factual anime appearance/recurrence claims require evidence; otherwise the final reviewed relation remains conservatively `inspired`;
- EN/ES/FR/DE/PT are explicitly `BLOCKED_UNTIL_IT_100_PERCENT`.
- generic description boilerplate is explicitly rejected; descriptions must be dish-specific and at least 45 words;
- description pair similarity is blocked at >= 0.70 to prevent formulaic near-duplicates.

Evidence:
- `authoring/f3k_it_hardening_51_162.json`;
- `tool/f3k_it_quality_gate.py`;
- `docs/F3K_IT_HARDENING_AUDIT.md`.

Exit for Phase A:
- dedicated F3K Italian gate PASS on the exact PR head;
- 112/112 IDs present and frozen;
- zero filler/generic-step violations;
- zero unresolved ingredient component references;
- zero incomplete anime review states;
- translation policy remains BLOCKED until that exact-head PASS.

Phase B — EN/ES/FR/DE/PT:
- BLOCKED until the stricter anti-template Italian freeze also passes exact-head CI;
- translations must reproduce the full frozen Italian recipe structure and may not collapse procedures back to generic four-step templates.

### F3L B2-2 — remaining 106 Italian description decisions (105 actual edits)

- **Source candidates applied as Italian prose:** 105 changed descriptions, versioned exactly once; recipe `000055` was already identical to its proposal and is not spuriously versioned. The six previously corrected source recipes remain stable.
- **All five review-only locales synchronized:** 105 newly machine-translated description drafts per EN/ES/FR/DE/PT locale (525 localized description edits); previous six contextually edited records preserved. Source/recipe hash bindings follow the accepted Italian text, not blind rehashing of untranslated wording.
- **Intermediate source SHA after 105 changes:** `ec302126b6578f52fb931cce03a06457660031b058a038360a4e289e684240c3` (historical ledger). **F3K completion repair:** 101 shorter descriptions extended with distinct dish-specific detail to preserve the ≥45-word quality contract; five locales received 101 corresponding translated additions each (**505**) and six witnessed false friends were corrected. **New source SHA:** `deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67`, with separate immutable migration ledger `tool/f3l_b2_2_101_enrichment_baseline.json` and QA test. Details in `docs/f3l_editorial/F3L_B2_2_106_DESCRIPTION_MIGRATION.md`.
- **Status:** AI-assisted staging only. No authenticated Italian culinary or five-language native review; 0/112 human-reviewed per target locale; all five machine drafts remain not publishable. B2/B3 release approval still blocked.
- **Next:** qualified recipe steps/culinary/food-safety review, native full-field translation verification, B3 promotion; only subsequently align illustrations to original first-50 recipe visual style.

### F3L B2-1 — controlled Italian source and five-locale migration, batch 1/19 (six recipes)

- **Implemented in PR:** versioned Italian edits for recipes `000059`, `000073`, `000074`, `000081`, `000088`, `000124`. Both descriptions and five originally defective instruction lines are corrected. 
- **Five-language rebinding with actual prose revision:** for each changed recipe update EN/ES/FR/DE/PT description, and corresponding edited steps, before rehashing. Preserve the remaining 106 recipes and all 10 reusable components byte-semantically via immutable regression snapshots.
- **Exact live source:** `d18d492b0db2148aed213610ffd1ff98bcff925a66cf4444a8a4da9b51576227`; old proposal inventory remains historical against SHA `954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c`.
- **No release:** all five packs still `machine_draft_not_publishable`; 0 qualified/native human approvals; full B2/B3 not complete; no runtime/catalog or image changes. This is a technical, AI-assisted candidate migration, not the qualified editorial gate.
- **Evidence:** `docs/f3l_editorial/F3L_B2_1_PRIORITY6_SOURCE_MIGRATION.md` and `tool/tests/test_f3l_b2_priority6_migration.py`.
- **Next:** remaining Italian source/copy defects, qualified culinary and safety acceptance of 112 + 10 components, further five-locale revisions, native review and only then B3 promotion. Image work follows content stabilization and must use the established first-50 visual style.

### F3L B2-I — complete AI-assisted Italian recipe-description review (112/112 candidate pack)

- **Deliverable:** 112 individual source-grounded Italian copy proposals, ten source component-review dossiers, context-anchored risk/typo leads, numeric timing triage, deterministic negative-path tests and non-production CI reviewer artifact.
- **Scope of completion:** candidate descriptions for 112/112 Italian recipes 51–162 only; changed wording remains segregated under `docs/f3l_editorial/italian_proposals/`. Exact source SHA is enforced; no undocumented recipe/ingredient/step edits.
- **Release and human gates:** no qualified human culinary/editorial acceptance, no source version/hash migration, no localized revisions and **no runtime publication**. Existing source and five draft locales remain unchanged and quarantined; B2 is NOT PASS and B3 remains BLOCKED.
- **Evidence:** `docs/f3l_editorial/F3L_B2_ITALIAN_112_REVIEW_REPORT.md`, `tool/f3l_b2_italian_review.py`, `tool/tests/test_f3l_b2_italian_review.py`, CI artifact `f3l-b2-italian-112-review-candidates`.
- **Next gated step:** qualified Italian editorial/culinary review of all 112 proposed descriptions + the 10 components; remedy step/safety defects; atomic five-locale source-version migration before any release consideration.

### F3L B2-0 — source-first editorial triage + bilingual review dossiers (technical workbench)

- **Scope:** generate a complete 112-recipe Italian review queue; flag six observed dish/copy mismatches and additional template-style copy for contextual examination. These are pending reviews, not corrected or signed-off source records.
- **Language handoff:** produce complete bilingual side-by-side dossiers for 112 recipes and 10 reusable components per EN/ES/FR/DE/PT locale (560 recipe + 50 component review units).
- **Invariants:** exact Italian source fingerprint, immutable quantities/IDs/timers, quarantined machine drafts, 0 human signoffs, runtime content untouched. Invalid/unsafe input must fail closed.
- **Evidence/commands:** `tool/f3l_b2_review_dossiers.py`, tests `tool/tests/test_f3l_b2_review_dossiers.py`, CI artifact `f3l-b2-review-dossiers`, `docs/f3l_editorial/F3L_B2_REVIEW_PROTOCOL.md`.
- **B2 remaining:** perform Italian recipe-by-recipe edits with version/hash migration and all qualified bilingual/culinary reviews. B2-0 technical PASS does **not** close B2 and does not unblock B3/F4.
## F3L — Translation rebuild for recipes 51–162 — CURRENT

Blocked by: F3K Italian editorial freeze — PASS (main `bda4ef4e603741336882cd91cd10b8eff0ab3695`).

Goal: publish all five additional locale packs without losing a single canonical ingredient, quantity, timer, or cooking step.

Phase B1: generate isolated review-required EN/ES/FR/DE/PT candidate packs from the frozen Italian source; mark candidates non-publishable. A dedicated CI workflow produces one artifact per language. The MT authoring tool and model weights are never app/runtime dependencies.

Phase B2: have each candidate reviewed against the Italian source for culinary terminology, full imperative procedures, kitchen-safety wording, accurate temperatures/timing/quantities, and natural native phrasing. Portuguese requires particular care because its candidate passes through English.

Phase B3: promote only audited packs with 112/112 human reviews per language, full 1:1 structural equivalence, zero untranslated or generic boilerplate, and a runtime integration CI green on exact PR head. Keep current runtime translations untouched before this gate.

Evidence: `tool/f3l_translate_drafts.py`, `tool/f3l_translation_gate.py`, `tool/tests/test_f3l_translation_gate.py`, `docs/F3L_TRANSLATION_QA.md`, `.github/workflows/f3l-translation-drafts.yml`.

Do **not** mark F3L PASS because automated machine drafts exist. Gate `--release-ready` explicitly rejects drafts lacking human editorial sign-off.

### F3L staging and versioned-source migration — 2026-10-28

- PR #33 merged on `main` as a non-publishable milestone at `0ce4ff684fca9d83adedcb6b95104c7437e97968`, preserving 560 translated recipe candidates and the 226-field copy-edit ledger.
- `recipe_000089` step-2 Italian rice-cooker erratum is repaired via controlled source version 2 -> 3, five draft pack hash migrations and tests. Details: `docs/f3l_editorial/F3L_SOURCE_MIGRATION_000089.md`.
- **F3L is not release-ready:** every target locale remains at 0/112 human editorial sign-offs. Automated structure/lexical results do not permit publishing. Runtime catalog remains unchanged. F3L B2 and B3 are still gated; F4 is not unblocked by technical staging alone.


### F3L audit remediation — 2026-10-28 (staging / partial, NOT RELEASE READY)

The external audit on main `5146bfd` found confirmed mistranslations in all five draft languages, generic Italian copy and safety-critical instructions. A controlled source revision now corrects six Italian recipes and migrates the five source-bound translation draft packs; witness-level copy-edits and CI regression are recorded in `docs/f3l_editorial/F3L_REMEDIATION_2026-10-28.md`. **Remaining**: full human bilingual culinary review 112/112 per language + 10 components, comprehensive IT copy sweep, native signoff, then runtime validation. Keep F3L B2/B3 and publication blocked.

# Product implementation specification

## Problem Statement

The project needs a commercial-grade Flutter foundation, a stable recipe runtime contract and an editorial pipeline that can add or revise recipes without editing Dart.

Directly embedding recipes in Flutter would couple editorial work, localization, duplicate review and user state to application code.

## Solution

Keep two explicit layers:

```text
authoring/*.json
-> deterministic authoring validation
-> duplicate/similarity review
-> compiler
-> assets/catalog/*.json
-> F1 runtime validation
-> VersionedRecipeCatalogRepository
-> Flutter UI
```

The authoring layer is build-time only. The Flutter app consumes the compact F1 runtime package and remains unaware of editorial tooling.

## User Stories

1. As a user, I want the app to open without requiring an account.
2. As a user, I want Explore, Favorites and Shopping to be obvious destinations.
3. As a user, I want device language by default and a manual language override.
4. As a user, I want favorite IDs to survive recipe-content revisions.
5. As an editor, I want one JSON authoring record per recipe and no Dart edits.
6. As an editor, I want raw source prose to remain transient rather than be committed.
7. As an editor, I want a published recipe to require EN/IT/ES/FR/DE/PT completeness.
8. As an editor, I want recipe images referenced through stable asset IDs.
9. As an editor, I want possible duplicates and variants reported before publication.
10. As an editor, I want the comparison report to explain ingredients, quantities, steps, timing and reference similarity rather than expose only one score.
11. As an editor, I want an exact re-import to be recognized as idempotent.
12. As an editor, I want a changed recipe with the same stable ID to be recognized as an update of the same entity.
13. As an editor, I want human duplicate/variant decisions invalidated when either compared recipe changes.
14. As a maintainer, I want CI to fail when generated runtime JSON drifts from authoring source.
15. As a maintainer, I want one synthetic fixture to prove authoring -> runtime -> Flutter Web without entering production content.
16. As a future paying user, I want purchases to map to a central entitlement state and ads suppressed before requests.

## Implementation Decisions

- Flutter 3.47.3 remains the pinned runtime toolchain.
- Riverpod owns presentation/application state.
- SharedPreferences stores small user-owned state.
- `VersionedRecipeCatalogRepository` remains the production recipe adapter.
- F1 runtime format remains JSON-only; no Markdown parser dependency.
- F2 authoring format is also JSON-only.
- Python standard library tooling is build-time only; no new Flutter/runtime dependency is introduced.
- `authoringVersion` versions editorial tooling independently from F1 `schemaVersion`.
- `catalogVersion` versions the generated runtime package.
- `contentVersion` versions one stable recipe ID.
- Production authoring source is `authoring/recipes/*.json`.
- Synthetic fixtures live separately under `authoring/fixtures/`.
- Raw copied source material is not a committed authoring source.
- Published authoring records require all six configured locales.
- Recipes reference `imageAssetId`; the compiler resolves it through the authoring asset manifest.
- Similarity normalization is deterministic and configured through explicit aliases/unit conversions.
- Current comparison dimensions are reference, ingredients, quantities, default-locale steps and total timing.
- Same ID + same fingerprint is an idempotent duplicate.
- Same ID + changed fingerprint is a same-entity update.
- Different IDs with high semantic similarity enter duplicate/variant review.
- `probable_duplicate` and `review_required` block production compilation unless a current fingerprint-bound review decision resolves them.
- Similarity never authorizes automatic deletion or overwrite.
- Review decisions become stale automatically when either full recipe fingerprint changes.
- `compile_recipe_catalog.py --check` is the generated-file drift gate.
- `build_recipe_preview.py` temporarily compiles the synthetic fixture, validates/builds the real Flutter app and restores production catalog bytes afterward.
- Navigator, entitlement boundaries and Material 3 implementation foundation remain unchanged.

## Testing Decisions

Automated coverage includes:
- F1 localized catalog loading and fallback;
- unsupported schema and duplicate stable-ID rejection;
- stable recipe identity across content revisions;
- authoring validation and F1 compilation;
- published-locale completeness;
- explicit synonym normalization;
- unit conversion equivalence;
- same-ID idempotent re-import;
- same-ID changed-content update classification;
- semantic duplicate detection;
- same-title false-positive resistance;
- review-memory invalidation after content change;
- deterministic similarity report;
- generated runtime catalog drift;
- F1 production catalog validation;
- Flutter analyze/test;
- synthetic fixture Flutter Web build;
- production Flutter Web build.

Android ARM64 remains a merged-main CI gate. AppLab, physical device and store evidence are later release gates.

## Out of Scope

Automatic culinary judgment, automatic rewrite of arbitrary copyrighted source prose, decorative-character implementation before F3C, cloud sync, auth, notifications, live AdMob, live billing, production signing and store release.

## Further Notes

F2 follows the deep-module approach: authoring complexity is hidden behind deterministic CLI tooling while the runtime continues to depend on the small F1 repository contract.

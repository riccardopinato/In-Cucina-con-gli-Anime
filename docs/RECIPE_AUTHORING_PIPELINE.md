# Recipe Authoring / Import Pipeline — F2 + F3E

F2 is the editorial build layer between source material and the F1 runtime catalog. Flutter does not parse authoring files.

## Canonical flow

```text
user/reference material
-> transient editorial analysis
-> normalized authoring JSON
-> deterministic validation
-> duplicate/similarity review
-> localization completeness
-> asset resolution
-> F1 JSON compilation
-> F1 catalog validation
-> synthetic Flutter Web preview
-> production catalog
```

## Rights boundary

Raw copied prose, scans, screenshots, PDFs and book/site text are working inputs only. They are not committed to `authoring/`.

The committed record contains:
- normalized culinary facts;
- stable IDs;
- fresh editorial wording written for this app;
- lightweight `contentOrigin` and optional internal `sourceNote`;
- localized app copy.

The repository does not claim that paraphrasing transfers copyright ownership.

## Authoring source

Production recipes live one JSON file per recipe in:

```text
authoring/recipes/
```

The reference schema is `authoring/schema/recipe_authoring.schema.json` and the copyable starter is `authoring/templates/recipe.template.json`.

F2 keeps production authoring empty. Real records start in F3.

The synthetic fixture under `authoring/fixtures/` is never part of the production compile unless `--include-fixtures` is explicitly supplied.

## Compiler

`tool/compile_recipe_catalog.py` converts authoring records into the exact F1 package:

```text
assets/catalog/manifest.json
assets/catalog/recipes.json
assets/catalog/locales/{en,it,es,fr,de,pt}.json
```

Production CI uses `--check`, which fails if generated runtime JSON differs from the committed authoring source.

No Flutter dependency or Markdown parser is introduced.

## Localization gate

Every recipe requires the default English locale while it is being authored.

A recipe marked `published` must contain all configured locales:
EN / IT / ES / FR / DE / PT.

The authoring report lists available and missing locales per recipe.

## Asset registry and F3E artwork contract

Recipes reference `imageAssetId`, not raw paths. IDs resolve through:

`authoring/assets/manifest.json`

One recipe owns at most one canonical artwork asset. The same JPEG is used twice:
- card: UI crop with `BoxFit.cover` inside the existing 178 px artwork area;
- detail: full image with `BoxFit.contain`.

No separate card/hero files are stored.

The manifest records:
- recipe ownership;
- rights class (`original`, `public_domain`, `licensed`);
- semantic-review state tied to the recipe `contentVersion`;
- a short review note describing the food that was actually checked.

Published recipes may reference artwork only when semantic review is `approved` for the current content version. CI does not pretend to perform culinary judgment: it enforces that the explicit review exists and is current.

F3E image budget:
- JPEG only;
- long edge <= 960 px;
- short edge >= 720 px;
- optimizer target <= 130 KiB;
- hard repository limit <= 140 KiB.

`tool/optimize_recipe_artwork.py` performs deterministic build-time recompression with pinned Pillow. Standard validation checks the committed bytes without requiring Pillow.

`tool/build_recipe_artwork_queue.py --missing-only` produces a deterministic batch queue containing the canonical dish title, inspiration, ingredients, steps, expected asset ID/path and rendering contract. The assistant uses that queue as the source for batch image creation/review instead of rediscovering each recipe ad hoc.

The compiler additionally rejects orphan artwork entries, cross-recipe asset links, stale semantic approvals, oversized files, undersized files and invalid JPEGs.

## Duplicate / Similarity Review Gate

The app implements the App Factory v19 design candidate `GOLDEN_DUPLICATE_SIMILARITY_REVIEW_GATE_v1_DRAFT`.

Comparison is deterministic and configurable in `authoring/config/similarity_policy.json`.

Current dimensions:
- anime/reference similarity;
- normalized ingredient overlap;
- normalized quantity/unit similarity;
- default-locale step-text similarity;
- total timing similarity.

Ingredient aliases and unit conversions are explicit configuration, not inferred AI facts.

Classifications:
- `idempotent_duplicate`: same stable ID + same full fingerprint, safe to skip as the same input;
- `same_entity_update`: same stable ID + changed content, treated as an update path rather than a new duplicate;
- `probable_duplicate`;
- `review_required`;
- `possible_variant`;
- `distinct`.

`probable_duplicate` and `review_required` block compilation until a fingerprint-bound decision is present in `authoring/reviews/decisions.json`.

A similarity score never deletes or overwrites a recipe automatically.

Supported human decisions:
- `accept_new`;
- `skip_new`;
- `replace_existing`;
- `merge`;
- `keep_variant`;
- `defer`.

If either recipe changes, its fingerprint changes and the old decision no longer resolves the comparison.

## Candidate review

To compare an incoming normalized candidate before adding it to production:

```bash
python3 tool/review_recipe_similarity.py path/to/candidate.json
```

The report is written under ignored `build/authoring/`.

## Batch artwork workflow

```bash
python3 tool/build_recipe_artwork_queue.py --missing-only
```

For a selected batch:

1. read the generated queue rather than reopening every source manually;
2. create one original anime-food artwork per recipe from the canonical ingredients/preparation;
3. visually check the dish against the queue before approval;
4. optimize the single JPEG to the F3E budget;
5. register the asset and semantic review in the manifest;
6. set `imageAssetId` in the authoring recipe;
7. compile once for the whole batch;
8. run exact-head CI and merge when green.

## Production compile

```bash
python3 tool/compile_recipe_catalog.py
python3 tool/validate_recipe_catalog.py
```

CI normally uses:

```bash
python3 tool/compile_recipe_catalog.py --check
```

so generated files cannot drift silently.

## Synthetic app preview

```bash
python3 tool/build_recipe_preview.py
```

The preview command:
1. backs up the tracked production catalog;
2. compiles the synthetic fixture into the normal runtime location;
3. runs the F1 catalog validator;
4. builds Flutter Web using the same application code;
5. restores the production catalog even on failure.

Therefore the fixture proves the full authoring -> runtime -> app-build path without shipping synthetic content.

## F2 boundary

The deterministic tools do not perform culinary judgment or automatically rewrite arbitrary copyrighted prose. The human/agent editorial step happens before committed authoring JSON.

This is deliberate: deterministic validation should validate facts/structure, not pretend to replace editorial judgment.


## F3G editorial publication gate

F3G raises the production standard from structural completeness to editorial usefulness.

For every published recipe the pipeline now requires:

- culinary verification with status `verified` or `corrected`;
- structured anime-reference semantics;
- fresh localized dish description;
- localized anime-context copy that matches the evidence level;
- preparation text substantial enough to explain technique, heat, timing and observable doneness cues;
- EN / IT / ES / FR / DE / PT parity.

The deterministic gate is implemented in `tool/f3g_editorial_gate.py` and is invoked by the normal catalog compiler. It complements, rather than replaces, schema validation and the duplicate/similarity gate.

Source material is never promoted to production merely because it contains a plausible recipe. F3G explicitly permits correction of names, ingredient ratios, timings, safety wording and anime associations before publication.

The 0.7.0 migration keeps `recipe_000001..recipe_000020` stable so existing Favorites remain valid while their `contentVersion` and editorial text advance.

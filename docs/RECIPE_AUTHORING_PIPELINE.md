# Recipe Authoring / Import Pipeline — F2

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

## Asset registry

Recipes reference `imageAssetId`, not raw paths. IDs resolve through:

`authoring/assets/manifest.json`

The minimal rights state is:
- `original`;
- `public_domain`;
- `licensed`.

The compiler also requires referenced asset paths to remain inside the repository `assets/` tree and to exist.

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

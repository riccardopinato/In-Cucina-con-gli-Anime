# Cooking Anime — Fast Track Semantic QA: 28 recipes / 83 source-bound ingredient translations

19 November 2026 · zero external paid AI requests

## Exact scope and reason
A read-only, all-catalog scan of the 162 published Italian-source recipes found **40 ingredient rows** explicitly labelled `cipollotto` in the canonical IT ingredient names. Their **200** target-language names across EN/ES/FR/DE/PT included **83 demonstrable false-friend or incomplete translations in 28 distinct recipes**. Representative defects: Spanish `cipollotto` left untranslated; French `ciboulette` (chives, not spring onion); German `Schnittlauch` or generic `Zwiebel`; Portuguese `cebolinho` or generic `cebola`; English generic `onions`. Recipe 138 had absurd `pipetas` / `Unterlegscheiben` / `lavadoras` for sliced onion rings.

## Batch application (two disjoint source edits, one runtime materialization)
Affected canonical recipe IDs:

`000055, 000061, 000063, 000066, 000071, 000073, 000075, 000076, 000078, 000082, 000083, 000090, 000092, 000098, 000100, 000108, 000112, 000114, 000118, 000123, 000130, 000131, 000133, 000134, 000138, 000147, 000151, 000156`.

- **28 / 162 recipes**: each editorial `contentVersion` advances by one; every changed translation name is mapped to the exact Italian ingredient ID and full source description, preserving chopped/sliced/fresh/garnish/green-only distinctions.
- **83** localized ingredient-name repairs: EN 1, ES 20, FR 15, DE 22, PT 25. No source ingredient quantity, unit, canonical key, number of steps, title, work association or artwork changed. All 28 have `imageAssetId: null`, so no existing visual semantic approval is invalidated.
- **Recipe 000083 Tsukemen**: separately corrected five complete descriptions, **35 translated procedural steps** (5 locales × 7 steps) and **17 ingredient names** across the six languages. The original Italian retains its seven steps and timings and receives one spelling correction in `polvere di pesce (katsuobushi in polvere)`. Former misstatements included Spanish `guárdalo ahora` in place of 'eat immediately', French `nouilles écorchées`, German instruction to 'concentrate on a bowl' and Portuguese `traço` in place of dashi.
- The six runtime locale catalogs plus `assets/catalog/recipes.json` were deterministically materialized from these authoring changes. The unaffected `manifest.json` is unchanged.

## Checkable controls
`tool/semantic_qa_food_glossary.py` independently runs an offline source-bound glossary triage over **all 162** published recipes / **40** Italian ingredients / **200** translations. It fails for the known incorrect ingredient classes, writes `build/semantic_qa/food_glossary.json` and explicitly returns `NOT_CERTIFIED`. The regular Semantic QA workflow runs the new regression tests and scans without any model/provider credentials. `tool/tests/test_semantic_qa_food_glossary.py` also confirms strict source/runtime parity, numerical quantities, version alignment and Tsukemen's seven-step translated procedure. Existing Flutter/Android and authoring compilation gate results must pass on the exact PR SHA before merge.

## Limitations
A successful glossary scan proves only that its specific, previously demonstrated terminology losses are corrected. It **does not** certify the context of all 810 source-to-target comparisons, food safety, other potentially mistranslated ingredients, nutrition, anime licensing, or the full recipes. No user data or external paid model endpoints are involved; CI runner usage is a separate infrastructure resource.

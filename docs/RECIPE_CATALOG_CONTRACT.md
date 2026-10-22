# Recipe Catalog Contract — F1

The runtime catalog is JSON-only. It is intentionally compact and split between canonical culinary metadata and localized editorial text.

## Runtime package

```text
assets/catalog/
├── manifest.json
├── recipes.json
└── locales/
    ├── en.json
    ├── it.json
    ├── es.json
    ├── fr.json
    ├── de.json
    └── pt.json
```

F2 may introduce friendlier per-recipe authoring files, but the app runtime continues to consume this compiled package.

## Version axes

- `schemaVersion`: shape/compatibility of the JSON contract. Runtime supports only explicitly known schema versions.
- `catalogVersion`: semantic version of the whole packaged catalog.
- `contentVersion`: positive integer revision of one stable recipe ID.

Changing title, wording, translation, quantities or editorial revision does not change the recipe ID.

## Stable IDs

Recipe, ingredient and step IDs use lowercase snake_case:

```text
fixture_noodles
rice
cook_broth
```

Recipe IDs are permanent identity. Favorites store only these IDs, so catalog replacement does not migrate user state.

## Canonical recipe metadata

Canonical data lives in `recipes.json`. A recipe entry contains:

- `id`
- `contentVersion`
- `status`: `draft | published | archived`
- `inspirationTitle`
- `prepMinutes`
- `cookMinutes`
- `servings`
- `difficulty`: `easy | medium | hard`
- optional `imageAsset`
- `contentOrigin`: `original | inspired | adapted`
- optional internal-only `sourceNote`
- structured `ingredients` with stable item IDs, numeric quantity and optional unit
- structured `steps` with stable step IDs and optional `timerSeconds`

No Markdown is accepted by the runtime contract.

## Localized editorial content

Each locale file maps a recipe ID to:

- localized `title`
- `ingredientTexts`, keyed by canonical ingredient ID
  - `name`
  - optional `note`
- `stepTexts`, keyed by canonical step ID

Quantities, times, servings and timer values remain canonical and are not duplicated across translations.

## Locale fallback

The manifest defines `defaultLocale` and the supported locale assets.

For a supported requested locale:

1. use that recipe translation if present;
2. otherwise use the default-locale recipe translation.

For an unsupported device locale, the repository uses the default locale.

A partially malformed translation is rejected rather than partially merged.

## Editorial origin

F1 deliberately keeps origin metadata lightweight:

- `original`: created for this app;
- `inspired`: developed from a dish/idea/reference with our own recipe/editorial work;
- `adapted`: based more directly on user-supplied reference material, normalized and rewritten for the app.

`sourceNote` is optional and internal. It is not a public attribution system.

## Deterministic validation

`python3 tool/validate_recipe_catalog.py` validates the production package before Flutter analysis/tests.

It rejects, among other things:

- unsupported schema versions;
- malformed catalog versions;
- locale manifest mismatches;
- duplicate or malformed stable IDs;
- invalid status/difficulty/origin values;
- negative timings;
- invalid servings;
- empty ingredient/step collections;
- duplicate ingredient/step IDs;
- broken localized ID parity;
- orphan translations;
- missing default translation for a published recipe;
- missing referenced image assets.

Errors are sorted before output so the same invalid input produces stable diagnostics.

## Runtime fail-closed rule

`VersionedRecipeCatalogRepository` never exposes a partially accepted catalog. Unsupported/malformed input throws `RecipeCatalogException`; the UI can show its normal error state.

The production F1 package contains zero real recipes. Synthetic fixture content exists only inside tests.

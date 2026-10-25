# F3G Editorial Data Contract — design

Status: APPROVED DESIGN TARGET for F3G implementation.

The current F1/F2 contract is intentionally compact but cannot represent the richer editorial experience required for the 50-recipe catalog. F3G extends it without breaking stable recipe IDs or Favorites.

## Public recipe content to add

### Localized description

Each published recipe will eventually require:

```json
"description": "Fresh app-original editorial description..."
```

Purpose:
- explain what the dish is;
- describe taste/texture and culinary context;
- explain why it is useful or distinctive;
- avoid filler text written only to increase recipe count.

Target: normally 2–4 short paragraphs in the UI copy source, but quality and clarity win over fixed length.

### Structured anime references

Canonical authoring metadata will move from the current flat `inspirationTitle` presentation toward:

```json
"animeReferences": [
  {
    "workTitle": "Food Wars! Shokugeki no Soma",
    "relation": "verified_appearance",
    "season": 1,
    "episode": "13–14"
  }
]
```

Allowed relation values:
- `verified_appearance`
- `recurring_association`
- `inspired`
- `unverified`

Rules:
- `unverified` is an authoring state and must not be worded in the public UI as a factual appearance;
- season/episode/chapter are optional and included only when verified;
- one recipe may reference multiple works, but the UI should prefer one strong primary reference over a weak list;
- no copied anime dialogue or long quotes.

### Localized anime-context copy

Each recipe will eventually require localized:

```json
"animeContext": "Short original editorial explanation of how the dish connects to the work."
```

The text must match the canonical reference relation:
- verified appearance -> may state that the dish appears/is prepared/is eaten;
- recurring association -> may describe the recurring food relationship without claiming this exact recipe;
- inspired -> must use inspiration language;
- unverified -> not rendered as a factual anime section.

## Internal editorial verification

The authoring layer will track an internal object such as:

```json
"editorialVerification": {
  "culinaryStatus": "corrected",
  "culinaryNote": "Canonical title normalized to Katsu Curry; roux quantity rewritten.",
  "animeStatus": "verified",
  "animeNote": "Direct episode evidence checked before publication."
}
```

Allowed culinary status:
- `verified`
- `corrected`
- `review_required`

This object is build/editorial evidence and does not need to be shipped to the public runtime package.

## Detailed preparation standard

F3G does not add artificial step-count minimums. Instead each recipe must include enough steps to make the dish realistically cookable.

A useful step should include, when applicable:
- preparation/cut size;
- pan/pot/tool choice;
- heat level;
- elapsed time;
- temperature;
- observable doneness/texture/color cue;
- what to avoid;
- resting/chilling/proofing/marinating state;
- serving timing when texture changes quickly.

“Mix, cook, serve” style instructions are insufficient for a multi-stage recipe.

## Time model

The existing `prepMinutes` and `cookMinutes` remain canonical for now, but F3G editorial review must account for all meaningful elapsed waits in copy and displayed total.

Candidate future canonical fields, only if implementation proves necessary:
- `restMinutes`
- `chillMinutes`
- `proofMinutes`
- `marinateMinutes`

Do not introduce them merely for completeness if a simpler total-time model is clearer.

## UI target

Recipe detail order:

1. artwork;
2. title + verified/inspired anime label;
3. richer recipe description;
4. compact facts (prep/cook/servings/difficulty);
5. **Nell'anime / Anime reference** editorial card;
6. ingredients;
7. detailed preparation steps + timers.

The anime card should show:
- work title;
- relation-aware label;
- localized context;
- season/episode only when verified.

## Migration strategy

F3G implementation remains incremental:

1. add optional parser/model/UI support with safe fallback to the current `inspirationTitle`;
2. migrate incoming recipe_000021..recipe_000050 in three ten-recipe slices;
3. migrate recipe_000001..recipe_000020 to the same richer standard;
4. once all 50 are migrated, tighten authoring validation so published recipes require description + structured anime context;
5. regenerate runtime catalog and run full validation.

Stable recipe IDs do not change, therefore Favorites remain attached to the same recipes.

## Rights boundary

Anime references are factual/editorial metadata. We may name the work and describe a scene/context in fresh wording, but we do not copy dialogue, screenshots, artwork, recipe prose or other protected expression into the catalog.

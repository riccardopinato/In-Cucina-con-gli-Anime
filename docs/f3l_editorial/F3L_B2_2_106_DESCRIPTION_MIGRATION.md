# F3L B2-2 — Remaining Italian editorial description migration (106 decisions)

**Stage: AI-assisted source changes and non-publishable translation drafts. NOT qualified human editorial approval. NOT runtime publication.**

## Actual result

- All 112 Italian editorial proposals from PR #39 were compared to the canonical source after the six earlier PR #40 corrections.
- The 106 remaining cases yield **105 real description changes**. Recipe **000055** already contains the same source description and is deliberately **not version-bumped**.
- The 105 changed Italian recipe descriptions are written into `authoring/f3k_it_hardening_51_162.json`; each of their `targetContentVersion` fields increases exactly once.
- The five persisted translation packs each contain **105 newly machine-translated descriptions** (525 candidate translations) based on the corresponding updated Italian wording. The six earlier contextually edited recipes are preserved and the unchanged recipe 000055 is left alone.
- All remaining canonical non-description fields (112 recipe IDs, ingredient quantities/units/IDs, culinary steps/timers, source anime references, ten reusable components, servings, and time metadata) were retained. No automatic step rewrites are implied.
- The translation model chain remains the original Apache-2.0 authoring-time Helsinki-NLP MarianMT family. The Portuguese draft is produced through an English pivot. The only new work is editorial/authoring, **not an AI runtime dependency**.

## Source provenance

- Original PR #39 candidate inventory SHA: `954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c` (historical, never silently rewritten).
- Immediately preceding PR #40 source SHA: `d18d492b0db2148aed213610ffd1ff98bcff925a66cf4444a8a4da9b51576227`.
- Source after these 105 changes: `ec302126b6578f52fb931cce03a06457660031b058a038360a4e289e684240c3`.
- `tool/f3l_b2_2_106_migration_baseline.json` records the previous SHA for **all 112** source recipes and immutable field hashes for the 105 changed records. Recipe 000055 and the six PR #40 recipes form the seven unchanged items.
- CI-only translator `tool/f3l_b2_translate_remaining_106.py` is reproducible on demand, source-bound, and emits only `machine_draft` candidates; the original translation authoring workflow is retained but no translation packs are published.
- `tool/tests/test_f3l_b2_2_106_italian_migration.py` verifies all 105 version bumps, all five source-linked packs, unchanged fields, draft quarantines, and **zero** human reviewEvidence entries.

## Unresolved gate; do not call this PASS

1. **Italian culinary/food-safety review:** qualified professionals still need to evaluate the steps, ingredients, quantities, temperatures, raw seafood/egg conditions, cooked rice and other risk areas. This description migration alone does not fix every previously flagged method typo or safety instruction.
2. **Five native editorial reviews:** the **525 newly generated descriptions**, all pre-existing steps/ingredient names, and all ten reusable component translations require native-speaker checks. Machine-generated terminology can be unnatural or inaccurate. The result is draft staging, not user-facing copy.
3. **B3 publication:** all five locales remain `reviewStatus=machine_draft_not_publishable`, `noAutomaticPublication=true`, `humanReviewedCount=0`, and `releaseApproved=false`. The production runtime translation/catalog and images are not changed.

## Illustrations (deliberately deferred)

The image pass starts only after text and recipe IDs are stable. Use the already-adopted first 50 images as the **direct style reference** for composition, food styling, material treatment, illustration technique and color, without overwriting existing artwork. Do not treat B2 staging as authorization to invent or publish visual assets.

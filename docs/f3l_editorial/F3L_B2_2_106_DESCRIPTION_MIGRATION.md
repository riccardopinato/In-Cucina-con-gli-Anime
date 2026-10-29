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

## F3K description-completeness repair — 29 October 2026 (AI-assisted staging)

A further deterministic F3K quality preflight showed **101 Italian descriptions had 32–44 words**, below the existing non-negotiable `>=45` word limit; this was a genuine regression of the first 105-description migration, not a test bug. The F3K quality gate has **not been relaxed**.

- Authored 101 distinct, source-grounded Italian completion sentences: `tool/f3l_b2_2_101_description_enrichment.json`. No generic boilerplate, no canonical ingredient/step/timer/identity changes.
- Rechecked exact source-specific candidate coverage: **101/101** descriptions now reach at least 45 words; pairwise token similarity remains below the original 0.70 blocking threshold.
- Incremented `targetContentVersion` once more for the 101 revised records; **11 recipes not revised in this follow-up** preserve their source versions. Historical 105-description and earlier six-recipe migrations remain separately versioned and independently testable.
- New Italian source SHA-256: `deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67`. Previous source SHA: `ec302126b6578f52fb931cce03a06457660031b058a038360a4e289e684240c3`. No content history was overwritten.
- EN/ES/FR/DE/PT each received 101 **actual machine-translated contextual additions** (505 new text candidates); each revised pack has corresponding recipe/content version and source hash. A source-bound CI translation run produced the five 101-item translation ledgers. These are **machine drafts**, not native review.
- Corrected 2 attested French mistranslations (`cuisinier` used incorrectly) and 4 Portuguese mistranslations (`macarrãoes`), plus pasteurized-egg-white terminology in the additional sentence for recipe 162.
- New immutable-field fingerprints and old-version/source identity: `tool/f3l_b2_2_101_enrichment_baseline.json`. New regression: `tool/tests/test_f3l_b2_2_101_enrichment.py`. Other frozen-source tests and previous migration regressions were rebound to the new exact source version **without weakening the culinary, numeric, human review or similarity gates**.
- Translation generation is manual/on-demand after this completed job, to avoid unnecessary retranslation during ordinary CI; no MT models enter the app binary.

**Still NOT approved:** no qualified culinary review of all 112 recipes/ten components; zero authenticated native sign-offs per language; `machine_draft_not_publishable` and `noAutomaticPublication=true` remain in force. The existing runtime catalog is unchanged. No new recipe image was created. `PASS` for F3L B2/B3 or store publication must not be claimed from staging tests.

**Exact-head verification:** check the PR workflow results on the final commit. Documentation of the preflight is not itself evidence that final CI has completed.

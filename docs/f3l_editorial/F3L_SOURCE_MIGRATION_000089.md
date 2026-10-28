# F3L — Source correction and controlled version migration: recipe_000089

Date: 2026-10-28. Predecessor staging PR #33 (merged at `0ce4ff684fca9d83adedcb6b95104c7437e97968`).

## Scope of change

- Canonical Italian authoring source: `authoring/f3k_it_hardening_51_162.json`.
- Recipe: `recipe_000089` (Botamochi / Ohagi), second cooking step.
- Previous instruction: `Cuoci nel lascia cuocereriso o in pentola con 280ml d'acqua per 15 minuti dal bollore.`
- Correct instruction: `Cuoci nel cuociriso o in pentola con 280 ml d'acqua per 15 minuti dal bollore.`
- Versioned edit of the intended rice-cooker operation and spacing only.
- `targetContentVersion` incremented from 2 to 3. `sourceContentVersion` stays 1; stable recipe, ingredient and step IDs remain unchanged.
- Zero changes to source quantities, ingredient units, servings, times, `timerSeconds=900`, component links, anime reference decisions, or the other 111 Italian recipes.

## Cryptographic source binding

| Field | Old F3K source | Updated staging source |
| --- | --- | --- |
| Full Italian source SHA-256 | `4d736cfa431025fdd8c6baa9725adf2525cdf0bcbf2be8508941f5dd68c3710f` | `905e4faa5253bc2968477836657abc6068e2961768008707f83b3b4b6f17431e` |
| Recipe_000089 SHA-256 | `485c7ba4a19db4b71b5455b990a8b73cbc32ac38c226df989a338c704409cd5e` | `56992a2f75b2eb4e0c5935cd9397be9249519bdce10a72323e5af45b655f6f8b` |
| Recipe_000089 target content version | 2 | 3 |

All five EN/ES/FR/DE/PT persisted draft packs have updated the **global source SHA**, **recipe 000089 source SHA**, and **recipe 000089 source content version**. All other 111 per-recipe fingerprints and the full 226-field copy-edit ledger were retained. All 10 reusable components and their five-locale draft copy remain unchanged. Four source-bound correction tools were explicitly rebound to the new exact source SHA. Historical F3K source is recoverable from Git at the previous merge commit.

The rice-cooker translations were already corrected during the second editorial pass. Thus this migration updates their source version bindings rather than replacing those five approved-for-review text candidates or pretending that source changes are invisible.

## Non-publication and review status

- EN/ES/FR/DE/PT are still 112/112 **machine draft** per locale, 0/112 native editorial sign-offs.
- Pack-level `machine_draft_not_publishable`, `noAutomaticPublication=true` and `releaseApproved=false` stay unchanged.
- Structural / lexical zero warnings do not constitute full semantic, culinary or native language review.
- `--strict-release` and `--release-ready` remain intentionally blocked.
- No runtime authoring, app recipe assets, installed user state, store artifact or production content was promoted.

## Verification

`tool/tests/test_f3l_source_migration_000089.py` verifies the new source fingerprint, recreates the original source by undoing the **two allowed mutations** and matches its historical SHA-256, compares the entire 112 recipe dataset, validates all five source-bound packs, and enforces the release block. CI PASS only if exact-head workflow confirms these tests.

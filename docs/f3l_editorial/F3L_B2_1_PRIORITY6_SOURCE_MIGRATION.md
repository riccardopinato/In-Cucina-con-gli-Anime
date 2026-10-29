# F3L B2-1 — First bounded Italian-to-five-locales source migration

**Status:** versioned technical migration in review; **not** qualified/native editorial approval, culinary certification, release approval or runtime publication.

## Scope (exactly six of 112)

Source before: `954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c`

Source after: `d18d492b0db2148aed213610ffd1ff98bcff925a66cf4444a8a4da9b51576227`

| Recipe ID | Italian source content version | Reason |
| --- | --- | --- |
| 000059 — Asari no Sakamushi | 2 → 3 | Remove generic/grammatically broken clam description; describe covered sake steaming |
| 000073 — Pork Kakuni | 2 → 3 | Replace incorrect dough/filling description, repair step-2 syntax and step-3 `l'grasso` |
| 000074 — Oden | 3 → 4 | Replace uninformative/incorrect description; preserve One Piece ep. 966 and its provenance |
| 000081 — Tamago Sando | 2 → 3 | Remove false dough/baking description; describe boiled-egg and shokupan assembly |
| 000088 — Fruit Sando | 2 → 3 | Remove false baking description; repair two broken instruction fragments without changing step count |
| 000124 — Uni Don | 2 → 3 | Remove false whipping/marinating claim and unsafe recommendation to taste raw uni to assess safety |

All six edited Italian descriptions come from the previously segregated AI-assisted, source-specific candidate inventory. Five human-readable translated descriptions per recipe were reauthored against the corrected Italian dish and method (EN/ES/FR/DE/PT), not merely rehashed unchanged. Changed **step instructions** were also translated in each language: 000073 steps 2/3, 000088 steps 3/4, 000124 step 3. Recipe/step/ingredient IDs, quantities, units, timers, equipment, anime references and untouched recipes remain invariant.

**Total in this PR:** six Italian descriptions, five Italian instruction steps and thirty target-language descriptions plus twenty-five target-language step instructions, with per-recipe content versions, per-recipe SHA and five whole-source SHA bindings updated.

## Reproducible technical evidence

- `tool/f3l_b2_priority6_migration_payload.json`: explicit source and five-locale language repair ledger; never a human sign-off.
- `tool/f3l_b2_priority6_migration_baseline.json`: original SHA for all 112 source recipes, immutable field fingerprints for the six changed recipes and old component SHA.
- `tool/tests/test_f3l_b2_priority6_migration.py`: fail-closed checks for exact changed set, source/pack hashes, untouched 106, immutable culinary quantities/timers/IDs, correct contextual translations, non-publication, raw-uni safety language and 0 human sign-offs.
- Other historical tests/source-bound scripts updated for the new live source SHA. The previous `112/112` proposal inventory remains **historical/source-locked to its original baseline**, not silently rewritten or automatically approved.
- The five historic `docs/f3l_editorial/f3l_*_editorial_audit.json` records remain historical evidence tied to the old source SHA; obtain fresh audit reports from current CI before interpreting status.

## Still blocked

- **106** Italian recipe descriptions from the proposal inventory remain unpromoted, and all **112** Italian recipes plus ten reusable components require qualified editorial/culinary review for acceptance.
- Further method, time and safety issues (e.g. raw egg service, raw fish and shellfish handling, cooked-rice storage, plus noted grammar defects) require tracked resolution. The revised recipe 000124 no longer suggests tasting uni to determine safety, but its raw seafood suitability still needs qualified market-specific verification.
- **560** translated recipe candidates and **50** translated component candidates remain `machine_draft_not_publishable` with `editorialStaging.noAutomaticPublication=true`, **0/112** native sign-offs for each target locale, and no production catalog promotion.
- No artwork or visual-style work was performed. After the content phase we can align the new recipe illustrations with the established style used for recipes 1–50.

This PR constitutes a **partial B2 source correction**, not F3L B2 PASS, B3 PASS or an image-production authorization.

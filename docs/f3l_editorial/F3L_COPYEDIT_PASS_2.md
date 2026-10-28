# F3L — Second AI-assisted culinary language pass (non-publishable)

## Exact scope

Frozen Italian F3K source fingerprint: `4d736cfa431025fdd8c6baa9725adf2525cdf0bcbf2be8508941f5dd68c3710f`. Scope: `recipe_000051`–`recipe_000162`, locales EN/ES/FR/DE/PT; 560 distinct translated recipe records with stable ingredient IDs, quantities, units, recipe IDs, times, and step IDs. The previous editorial staging had 185 triage warnings (EN 15 / ES 25 / FR 81 / DE 41 / PT 23), and no native-editor certifications.

This pass modified **226 text fields**: EN 25, ES 42, FR 78, DE 51, PT 30. Individual *before/after* texts and recipe/field identifiers are saved in `f3l_expanded_review_ledger.json`. The changes include complete step-level redrafts where translation distorted the cooking operation or omitted a Japanese preparation name, alongside conservative corrections of names and spelling. It does not claim a complete line-by-line review of every translated step and paragraph.

Specific corrected failures include `jump` instead of `stir-fry` in English; `únete`, `pañuelo`, `mochila` for culinary instructions in Spanish; `myrin`, `cuivre`, `écoutez` (for *égouttez*), and `taureau` (for *tare*) in French; `Mist` for *miso*, `Peitsche` for a whisk, and `streicheln` for a simmer in German; `traço` for *dashi*, `colchão` for a ladle, `pule` for sautéing, and `menme` for *menma* in Portuguese.

The lexical auditor has also been repaired to *recognize* acceptable orthography rather than falsifying a PASS by changing it: French `saké`, Portuguese `saquê`/`saqué`, Spanish `mirín`, German `Misopaste`, `Misoglasur`, `Kochsake`, `Daikonwurzel`, `Ramennudeln` are not evidence of missing Japanese terms. Spanish `con chashu` and `salsa tentsuyu` are grammatical Spanish, not untranslated Italian fragments.

## Verifiable results

| Language | Additional fields corrected | 112 recipe records | Structural errors | Current identified lexical/number flags | Individual editorial sign-offs | Publishable |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| EN | 25 | 112 | 0 | 0 | 0 | **NO** |
| ES | 42 | 112 | 0 | 0 | 0 | **NO** |
| FR | 78 | 112 | 0 | 0 | 0 | **NO** |
| DE | 51 | 112 | 0 | 0 | 0 | **NO** |
| PT | 30 | 112 | 0 | 0 | 0 | **NO** |

**Zero warnings means only that currently implemented checks found no more issues of the covered patterns. It does *not* mean that the translations are error-free, idiomatic throughout, or native-speaker reviewed.** Other weaknesses may remain in descriptions, ingredients, or any step not individually reviewed; particularly the PT translation obtained through an EN pivot. The initial 185 flags should never be equated with all possible errors. There is no auto-approval and each locale still has 0/112 signed-off recipes. The strict release gate must continue to **FAIL** until editorial review evidence exists for every recipe.

### Known Italian source erratum — recipe_000089

F3K `recipe_000089` step 2 currently reads `Cuoci nel lascia cuocereriso o in pentola con 280ml d'acqua per 15 minuti dal bollore.`. This is syntactically damaged and presumably refers to **`Cuoci nel cuociriso o in pentola con 280 ml d'acqua per 15 minuti dal bollore.`** Based on the context and ingredients, the translated method step for this one recipe has been clarified in each locale without changing the immutable IT source, recipe IDs, quantities, or timers. **Before promotion**, amend the Italian source under a documented source-version migration, and recompute all five pack baseline fingerprints and this recipe's source fingerprint. Do not edit the frozen Italian source silently or replace hashes without revalidation.

### Reproducibility and gates

- Apply `tool/f3l_expanded_review.py` to reviewed drafts only; all edits are bound to the exact Italian SHA-256. The script cannot mark a translation human-reviewed.
- `tool/tests/test_f3l_expanded_review.py` checks all five persisted packs, source hash, idempotence, culinary fixes, data invariants, the rice-cooker erratum mitigation, and explicit release blocking.
- `.github/workflows/f3l-editorial-qa.yml` runs regression tests and the draft structural gate against the PR head.
- **Do not merge translated text into app runtime**, generate release assets, or represent all 162 recipes as publication-ready. The PR is an authoring/QA milestone, not a language launch.

Next editorial step: perform a true recipe-by-recipe bilingual semantic pass across *every* remaining field, with culinary/food-safety review and qualified human editorial evidence, then migrate source 000089, recheck the five locales, compile catalog, and run app builds.

### Later controlled migration

The `recipe_000089` malformed Italian source step described in this historical second-pass report has since been fixed through a version/hash migration. See `F3L_SOURCE_MIGRATION_000089.md`. This does not constitute language certification.

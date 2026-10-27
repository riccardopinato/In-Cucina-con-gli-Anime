# F3L — Editorial quality status (not publication-ready)

## Scope and source of truth

- Frozen F3K Italian reference: `authoring/f3k_it_hardening_51_162.json` (112 recipes, IDs 000051–000162; 10 reusable components).
- Five saved revision candidates in `authoring/f3l_review_drafts/` (EN/ES/FR/DE/PT). They are **not** runtime data. The Italian SHA-256 source fingerprint and per-recipe fingerprints prevent stale edits.
- Initial packs retrieved from GitHub Actions F3L run `40598212926` on commit `2b5828a77eb799bfc06c4e4cae2de993a7ca570f`, before the 14-day artifact expiry.
- Recipe `000159` French Kuri Manju had previously been rewritten; its fix is retained in the retrieved FR pack.

## Scope of this revision

1. Complete linguistic rewrite of the Shio Ramen `recipe_000051` description, title, 11 ingredient names and 9 method steps **in all five locales**. Source quantities, timing, IDs, and reference status were unchanged. `reviewStatus` remains `machine_draft`: this is not external/native human certification.
2. Recipe `000053` Ebi Tendon: recast each title/description in all five locales, corrected key ingredient nomenclature (shrimp, vegetables, rice) rather than accepting false friends such as Portuguese *lagartos* for shrimp.
3. Source-specific corrections to recipe `000059` (ES/DE garlic-ginger browning), recipe `000107` (ES/FR/DE exact 2–3 cm shokupan cut; ogura-an preserved), and recipe `000150` (ES duck breast must be **cooked**, not **eaten**, for 2 minutes).
4. Copy-edited all **112 recipe titles in each of the five target languages** (560 titles) using a source-locked glossary table; additionally repaired witnessed mistranslations such as German *Kupfer* for ramen, French *pangratté* for breadcrumb, and Portuguese *macarrãoes* for noodles. These remain AI-assisted revisions, not native-editor sign-offs.
5. A new lexical/number-preservation audit flags Italian leakage in titles, lost Japanese culinary terminology, high-risk mistranslations and numeric changes. It distinguishes heuristics/false positives from proven errors. The numeric tokenizer was corrected to handle units attached directly to numbers (`400ml`, `20g`), avoiding false alerts.
6. Saved all 5 candidate JSON packs and per-language audit reports to the repo. Added a lightweight CI editorial staging audit and negative-path tests. No production recipe authoring or compiled catalog was modified.

## QA outcomes after targeted edits

| Locale | Recipes / 112 | Structural errors | Editorial triage warnings | High-priority warnings | Release-approved |
| --- | ---: | ---: | ---: | ---: | --- |
| EN | 112 | 0 | 15 | 0 | **NO** |
| ES | 112 | 0 | 25 | 0 | **NO** |
| FR | 112 | 0 | 81 | 0 | **NO** |
| DE | 112 | 0 | 41 | 0 | **NO** |
| PT | 112 | 0 | 23 | 0 | **NO** |

The remaining 185 advisory warnings include real observed semantic problems, Italian copy leakage, potential loss of specialized Japanese terms, and some intentionally retained spelled-out numbers. The high-priority lexical signature flags have been addressed, but **this does not establish that severe errors are absent**: the detector knows only specific failure patterns. Counts are **triage flags**, not a comprehensive tally of every translation error. None of the five locales has all 112 entries human-reviewed; 0/112 `human_reviewed` per locale.

## Hard publication lock

Run `python tool/f3l_check_review_drafts.py` for structural/source matching; it passes for quarantined drafts. Run `python tool/f3l_check_review_drafts.py --strict-release` before any runtime promotion: it **must fail** until every locale's recipes are individually reviewed with evidence and all identified risk flags are resolved or documented as accepted, contextually justified exceptions. Do not bypass by marking `human_reviewed` automatically.

A true release requires checking **every ingredient, subrecipe, cooking step, quantity, temperature, time, food safety instruction, and Japanese term** against the frozen Italian source, and reviewing naturalness and consistency of EN/ES/FR/DE/PT with qualified native editors. Retain `recipeRef` links, stable IDs, and timers; validate compiled catalog and Flutter/Web/Android CI only after editorial acceptance. The Portuguese English-pivot translation merits extra attention.

## Additional source-level concern

Some wording in the *Italian* F3K baseline is anomalous (for example, recipe `000089` step 2 includes `Cuoci nel lascia cuocereriso`). Correcting Italian would change its canonical SHA and therefore deliberately invalidate all current draft translations. Plan any such correction as a source-version migration with retranslation of the affected content, not as a silent staging edit.
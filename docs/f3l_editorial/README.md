# F3L — Editorial quality status (not publication-ready)

## Scope and source of truth

- Frozen F3K Italian reference: `authoring/f3k_it_hardening_51_162.json` (112 recipes, IDs 000051–000162; 10 reusable components).
- Five saved revision candidates in `authoring/f3l_review_drafts/` (EN/ES/FR/DE/PT). They are **not** runtime data. All 10 reusable components have now received targeted five-locale copy-edits, including the six with full procedures; the other 112 recipes per locale are not fully reviewed. The Italian SHA-256 source fingerprint and per-recipe fingerprints prevent stale edits.
- Initial packs retrieved from GitHub Actions F3L run `40598212926` on commit `2b5828a77eb799bfc06c4e4cae2de993a7ca570f`, before the 14-day artifact expiry.
- Recipe `000159` French Kuri Manju had previously been rewritten; its fix is retained in the retrieved FR pack.

## Scope of this revision

1. Complete linguistic rewrite of the Shio Ramen `recipe_000051` description, title, 11 ingredient names and 9 method steps **in all five locales**. Source quantities, timing, IDs, and reference status were unchanged. `reviewStatus` remains `machine_draft`: this is not external/native human certification.
2. Recipe `000053` Ebi Tendon: recast each title/description in all five locales, corrected key ingredient nomenclature (shrimp, vegetables, rice) rather than accepting false friends such as Portuguese *lagartos* for shrimp.
3. Source-specific corrections to recipe `000059` (ES/DE garlic-ginger browning), recipe `000107` (ES/FR/DE exact 2–3 cm shokupan cut; ogura-an preserved), and recipe `000150` (ES duck breast must be **cooked**, not **eaten**, for 2 minutes).
4. Copy-edited all **112 recipe titles in each of the five target languages** (560 titles) using a source-locked glossary table; additionally repaired witnessed mistranslations such as German *Kupfer* for ramen, French *pangratté* for breadcrumb, and Portuguese *macarrãoes* for noodles. These remain AI-assisted revisions, not native-editor sign-offs.
5. Rewrote **all six complete reusable preparation components** in each target locale: chashu pork, ajitama eggs, kombu/katsuobushi dashi, tonkatsu cutlets, chocolate pastry cream and brioche dough for Choco Cornet. Each has ingredient-by-ingredient and step-by-step copy-edits, preserving exact quantities, cook/rest durations and component identities. Also corrected the four reference-only component titles without changing their recipeRef links. This is 30 complete subrecipe translations and 20 component title/link labels, not language release approval.
6. A new lexical/number-preservation audit flags Italian leakage in titles, lost Japanese culinary terminology, high-risk mistranslations and numeric changes. It distinguishes heuristics/false positives from proven errors. The numeric tokenizer was corrected to handle units attached directly to numbers (`400ml`, `20g`), avoiding false alerts.
7. Saved all 5 candidate JSON packs and per-language audit reports to the repo. Added a lightweight CI editorial staging audit and negative-path tests. No production recipe authoring or compiled catalog was modified.

## Follow-up copy edit pass (2026-10-28)

See [F3L_COPYEDIT_PASS_2.md](F3L_COPYEDIT_PASS_2.md) for 226 additional source-locked text corrections, exact before/after ledger, expanded regression tests and updated warnings. The earlier figures of 185 issues are historical; the currently implemented lexical/number detectors now report **zero identified flags** across the five saved draft packs. **This is NOT a comprehensive bilingual editorial sign-off:** each locale remains 0/112 human-reviewed and `--strict-release` must fail. No runtime translation has been published.

Italian source `recipe_000089` step 2 requires a separate source-version migration before publication; a source change invalidates all current per-recipe and global SHA fingerprints.


## Later controlled migration

The Italian source erratum for recipe `000089`, described historically above, was corrected on 2026-10-28 through a versioned/hash-bound migration. See `F3L_SOURCE_MIGRATION_000089.md`. The five draft packs remain non-publishable.

# F3L — Translation rebuild from the frozen Italian baseline

**Scope:** recipe_000051–recipe_000162, five target locales (EN/ES/FR/DE/PT).

## Mandatory authoring order

1. F3K Phase A source is the sole translation source. Its canonical file on `main` is `authoring/f3k_it_hardening_51_162.json`.
2. A changed source fingerprint invalidates the entire translation pack. Any substantive Italian edit relocks all five locales.
3. Machine translation is permitted only as a **review-required candidate**. It is not publication sign-off, and cannot be imported into runtime just because structure passes.
4. Every ingredient and step, including all 10 reusable subrecipes (chashu/ajitama/etc.), is translated *individually* while stable IDs, quantities, timerSeconds and elapsed time remain unchanged. Do not reduce 8 steps to four summaries.
5. The ingredient/component glossary requires native review, especially dashi, mirin, shichimi, chashu, menma, anko, kinako, kuromitsu, tare, sake, yuzu, and cooking techniques.
6. Portuguese candidate stage uses an English pivot; this is **extra-risk** and needs stronger bilingual review than direct-language candidates.
7. Publication gate requires 112/112 translated recipes *per locale*, zero structural errors, and explicit human-review evidence for every recipe. Until then, keep existing published runtime locale data unchanged.

## Technical pipeline

`tool/f3l_translate_drafts.py` produces separate, non-publishable JSON draft packs using offline-in-app authoring time MarianMT (open-licensed Apache-2.0 model weights). Models never enter the APK. `tool/f3l_translation_gate.py` enforces 1:1 completeness against a SHA-256 content fingerprint of the F3K baseline; `--release-ready` additionally blocks anything without editorial review.

New CI workflow `.github/workflows/f3l-translation-drafts.yml` uploads review candidate packs by locale. The PR can have successful structural checks while all five languages remain **NOT EDITORIALLY APPROVED**; don't merge translated text or call it 100% until editorial QA is done.

## What CI cannot prove

An automated structural PASS does not prove that a Japanese culinary term is translated correctly, that syntax reads naturally in German/Portuguese, that every thermal/time nuance survived, or that a model did not omit a semantically critical word. Human review must check these independently.

## Italian freeze reference and technical verification

Italian baseline merge: `bda4ef4e603741336882cd91cd10b8eff0ab3695`.
For every generated pack the validator stores an exact source-content SHA-256. The canonical numeric quantities, step timer seconds, step IDs, and recipe IDs must not change. If any field changes on the Italian side, the previous candidate is invalidated automatically.

The model must *not* be bundled into production; workflow artifact downloads are editorial review material, not installable app content. New locale content requires complete linguistic and culinary verification, not merely passing CI.

## Targeted French editorial correction — recipe_000159

The source recipe is **Kuri Manju (chestnut-filled baked cakes)**, with nine
ingredients, nine cooking steps, and an unchanged 20-minute refrigeration,
170 °C fan oven, and 12–15-minute baking time. Initial MarianMT output for
French generated a 3.36x repetitive expansion in the seventh step (zero-based
validator index six: the soy-sauce and egg-yolk glaze). Several other fields in
this same recipe were unnatural, so all French-language fields for this one
recipe (title, description, nine ingredient names, nine instructions) were
rewritten directly from the frozen Italian source instead of merely relaxing
length thresholds.

The repair is stored at `tool/f3l_french_recipe_159.py`, applied only to the
French draft by `tool/f3l_translate_drafts.py`. It is tied to the exact
`sourceRecipeSha256=4de3588c54cb13611568ebba5c65c0e6db3731ad9fe3cef75cb4e24afe14b268`.
Any source revision invalidates the rewrite and fails closed. Ingredient IDs,
amounts/units, step IDs, timer seconds, servings and elapsed times are unchanged.

Replayed the repaired French recipe against the failed production workflow
artifact from run `40591848460`: `f3l_translation_gate.inspect` changed from
one error to **zero errors for all 112 recipes**. Three dedicated regression
tests pass in addition to the existing eight gate tests. This is a targeted
linguistic repair, **not** a claim that all 112 French recipes are fully
human-reviewed. Publication and full-locale release certification remain blocked.

## Italian source correction — 2026-10-28

Controlled version and hash migration for recipe `000089` has updated five source-bound staging drafts and editorial tooling. Historical F3K freeze is recoverable in Git. See `docs/f3l_editorial/F3L_SOURCE_MIGRATION_000089.md`. No human sign-off or runtime publication implied.

# F3L — Editorial remediation against 2026-10-28 audit

**Status:** partial, source-locked and **non-publishable**. This record documents actual edits, NOT a native-language or food-safety certification.
**Italian source before remediation:** `905e4faa5253bc2968477836657abc6068e2961768008707f83b3b4b6f17431e`.
**Italian source after remediation:** `954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c`.
**Source of requirements:** the supplied report `Cooking_Anime_Audit_Editoriale_F3L_2026-10-28.txt` (baseline main `5146bfd73c589388100a54ed4ee0365c6d53e9af`), plus independently checked official food-safety and anime sources.

## Changes to canonical Italian source

The six records `000055`, `000074`, `000134`, `000146`, `000160`, `000162` move from `targetContentVersion=2` to **3**. `000089` stays at version 3 (separate prior erratum). **Stable IDs, quantities, units, all timers, 112-recipe order, reusable components and runtime catalog are unchanged.** All five staging draft packs are bound to the new source SHA, with exact per-recipe SHA and source version updates for these six records; other recipe revisions are untouched.

- `000055` Miso Nikomi Udon: chicken-core-temperature guidance (74 °C; time alone not proof of doneness), pasteurized eggs for soft-yolk preparation, improved Italian description.
- `000074` One Piece / Oden: `verified_appearance` episode corrected from **974** to **966** with primary-source URL and revised note. Official One Piece cast interview explicitly discusses Oden making and sharing the food in episode 966: https://one-piece.com/news/o20210315_12235/index.html.
- `000134` Shirasu Don: pasteurized yolk suitable for use without further cooking; explicit raw-egg warning; dish-specific source description.
- `000146` Maguro Don: tuna must be specifically supplied for raw use, handled chilled per supplier guidance, prepared with clean utensils; marinade adds flavour and does **not** make unsuitable raw fish safe. Avoid asserting a universal parasite-freezing rule for all tuna.
- `000160` Coffee Jelly: replaced generic references to `impasto o crema` with a dish-specific description of coffee jelly, gel setting, cooling and serving.
- `000162` Yuzu Sorbet: changed egg white ingredient to pasteurized product suitable without cooking; explicitly state freezing does not pasteurize and prohibit unpasteurized raw egg white.

Supporting official guidance:
- FDA raw eggs: https://www.fda.gov/food/retail-food-industryregulatory-assistance-training/assuring-safety-eggs-and-menu-and-deli-items-made-raw-shell-eggs
- FDA seafood: https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely
- USDA poultry: https://ask.fsis.usda.gov/article/What-is-a-safe-internal-temperature-for-cooking-meat-and-poultry

## EN/ES/FR/DE/PT draft repair

All 560 recipes remain draft text; the corrected safety fields in four source recipes (`000055`, `000134`, `000146`, `000162`) were rewritten contextually in all five locales, as was the Coffee Jelly description. Known false friends from the audit received additional corrections, including:
- EN: `Door to light boil`, `chicken buns`, `gaskets`, `onipollot`, `semolated sugar`, `it snows the egg white`.
- ES: `Ligera marca`, `bocadillos de pollo`, `huevo golpeado`, `látigo`, `despídelos`, `se represente`, `se tiemble`.
- FR: `blancs d'oie`, `tranches de thon à rayons X`, `hérisson de wasabi`, `striscioli`, `stricholine`, `joints`.
- DE: `Weißweine`, `nähen Sie den frischen Eigelb`, `Dichtungen`, `Seehühnchen`, `Schweineschalen`, `springt die Garnelen`.
- PT: `grampe o gengibre`, `consumo bruto`, `atum de raio`, `chicote`, `ela neva a branca do ovo`; editorial preference for **European Portuguese (pt-PT)** in subsequent manual harmonization, not yet claimed as fully standardized.

The third-pass remediation is intentionally **not** a rewrite of every sentence in 4,500 translated steps / 4,680 translated ingredient labels. Some remaining drafts can still be awkward, imprecise or unsafe. The automated witnessed-error scanner is a **regression floor**, not evidence of semantic completeness.

## Automated gates

- `tool/f3l_translation_gate.py`: canonical quantities/units/ID/version/timer and reusable-component equivalence.
- `tool/f3l_semantic_safety_gate.py`: exact source fingerprint, specifically witnessed false friends, selected safety-critical fields, zero fabricated signoffs, enforced non-publication.
- `tool/tests/test_f3l_editorial_repair.py`: all five 112-recipe candidate packs, 900 steps and 936 ingredient records per locale, source/candidate integrity, fail-closed negative paths.
- `.github/workflows/f3l-editorial-qa.yml` runs regression, strict structural checks and witnessed-error check for each PR head.

All five locale packs retain `reviewStatus=machine_draft_not_publishable`, `editorialStaging.noAutomaticPublication=true`, individual recipe `reviewStatus=machine_draft`, and **0/112 independently attested human approvals per locale**. Strict release is intentionally blocked.

## Work still required (NOT DONE)

1. Qualified professional culinary and food-safety review, especially raw seafood/egg suitability for each distribution market, including product sourcing and temperature/handling guidance.
2. A full contextual bilingual review of **all** 112 recipes **and ten reusable components** per target language, including all instructions, ingredient labels, step durations, wording and anime context. Fix unflagged semantic errors and generic descriptions. Preserve a source-locked edit ledger.
3. Italian-first editorial sweep for generic descriptions beyond the six changed records. Any Italian revision requires a further version/hash migration and renewed comparison of five locales.
4. Locale style guide, terminology glossary, consistent imperative and fully native **pt-PT** spelling/register. No machine-only claim of fluency.
5. Real named reviewer evidence for 112/112 per locale; risk-acceptance and source revision controls. Do not fabricate reviewEvidence or downgrade the release gate.
6. **Only after approval:** versioned runtime catalog promotion and compile, Flutter analyze/test, Web + Android builds, on-device QA, and deployment gate. These have **not** been executed as publication steps by this PR.

**Release decision: NO-GO.** This branch repairs confirmed defects but does not satisfy F3L B2 native review or B3 publication exit criteria.

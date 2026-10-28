# F3L B2 — Italian editorial source pass: 112/112 AI-assisted candidates

**Decision: CANDIDATE PASS (staging only). Canonical migration and qualified sign-off: PENDING. Runtime publication: NO-GO.**

## Scope and reproducibility

- Baseline `main@3af93bfd2d0c87bde23f5184f091105bf83ce1cc`, Italian file `authoring/f3k_it_hardening_51_162.json`.
- Exact source SHA-256: `954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c`.
- Complete AI-assisted, **dish-specific** replacement-description proposals for **112/112** Italian recipes 51–162, distributed in four source-locked candidate files in `docs/f3l_editorial/italian_proposals/`. Existing source titles, ingredient IDs/quantities, steps, timers and anime metadata are not silently changed.
- Source-verbatim contextual review leads for selected recipes, numerical prep/cook/elapsed-time triage on all 112, and 10/10 existing Italian reusable components included verbatim in the generated review dossier for contextual verification.
- Script: `python tool/f3l_b2_italian_review.py`. The machine-readable report is written only under `build/f3l-b2-italian-review/`; CI produces artifact `f3l-b2-italian-112-review-candidates`. An exact source/hash mismatch, incomplete or reordered records, false `human_reviewed` claims or attempt to write into runtime/authoring paths fails closed.

## Confirmed wording problems and qualified-review leads

The source contains at least the following distinct classes of issues:

| Recipes | Evidence and required follow-up |
| --- | --- |
| 052, 054, 060, 061, 104 | Malformed cooking instructions or sentence fragments. Repair the **actual steps** in a separate, versioned canonical migration rather than papering over them with a better description. |
| 073, 074, 081, 088 | Descriptions contradict dish technique or contain generic/ungrammatical copy. 088 also has a step split between the incomplete parenthesis `(es.` and its following sentence. |
| 056, 124, 146 | Seafood served raw. Require supplier/product suitability, storage and qualified market-specific food-safety checks; freshness or tasting is **not** proof of safety. 124 currently instructs tasting raw uni to evaluate quality and needs correction before publication. |
| 059, 096, 156 | Clam handling and service; qualified food-safety review required. |
| 080 | Japanese sanma species and Italian common-name attribution need verification from reliable taxonomic references before correcting the displayed title or ingredient. |
| 110 | Offal cleaning and preparation require qualified review. |
| 117, 133, 150, 153 | Poultry/duck cooking and especially raw egg-yolk service require qualified checks. Recipe 153 uses a fresh raw dipping yolk; specify validated, market-appropriate ingredient handling before publication. |
| 149 | Previously cooked rice used in fried rice: qualified storage/chilling/reheating instructions needed. |

These are **explicit review leads**, not an exhaustive or certified safety/culinary audit. The report records the exact source field and full text supporting each cited observation, not imagined descriptions. Numeric time differences are advisory only; rest, proofing and cooling can make addition-based comparisons misleading.

## Stage versus canonical content

The candidate pass **does not alter**:

- `authoring/f3k_it_hardening_51_162.json` or existing recipe content versions;
- any of the five saved F3L EN/ES/FR/DE/PT packs or their source fingerprints;
- source-dependent curated translation tools, output runtime catalog or Flutter app assets;
- any approval flags, reviewEvidence, or food-safety credentials.

The existing five packs are non-publishable `machine_draft_not_publishable` candidates, and each language still has **0/112** authenticated human editorial reviews. There is **no human source certification** in this step.

## Controlled next phase: accepted Italian source migration

1. Have a qualified Italian culinary/editorial reviewer assess the 112 candidates and all **10** reusable components against the full method, not just the description. Capture real reviewer evidence and rejected/corrected proposals.
2. Remedy the confirmed step/ingredient/time/food-safety anomalies with evidence. Do not use automated find/replace on steps when temperature or operations may be changed.
3. In one controlled branch increment content versions for actually changed Italian recipe IDs, update fingerprint/provenance and **retranslate or contextually edit each impacted candidate field in all five locale packs**. New hashes cannot be pasted onto untranslated old prose. Refresh source-bound repair modules, tests and audit reports.
4. Keep all packs non-publishable until qualified native and culinary reviews plus subsequent B3 runtime promotion gates are fulfilled. A green CI for **this proposal PR** is not certification of the content.

**Concluded within this slice:** complete 112-record, source-locked Italian description proposal inventory and reproducible risk triage. **Not concluded:** qualified acceptance, canonical content migration, validated translations, F3L B2/B3 as a whole.

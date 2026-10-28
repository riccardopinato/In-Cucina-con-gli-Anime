# F3L B2 — Italian source and qualified bilingual review protocol

**Status: REVIEW WORKBENCH ONLY — NO-GO FOR PUBLICATION.**

F3L contains 112 Italian canonical recipes (\`recipe_000051\`–\`recipe_000162\`), five machine-translation candidate packs (EN/ES/FR/DE/PT, **560** recipe candidates), and ten reusable components per target locale (**50** component reviews). The currently published runtime catalog is separate and **must not be touched** by the B2 tooling.

## 1. Generate the review material

From repository root:

\`\`\`bash
python tool/f3l_b2_review_dossiers.py
python tool/f3l_b2_review_dossiers.py --out-dir build/f3l-b2-review
python tool/f3l_b2_review_dossiers.py --locale fr --recipe-id recipe_000073 --out-dir build/f3l-b2-focused
\`\`\`

The CLI uses the current Italian source fingerprint and refuses stale candidates, structural drift, forged review claims and removal of the publication quarantine. It emits a source triage queue and per-locale *paired* source/candidate JSON dossiers to the requested output directory only. CI additionally generates downloadable, **non-production** review dossiers.

Each recipe dossier includes both texts for title, description, anime context, elapsed-time note, equipment, every ingredient and its immutable quantity/unit/ID, and every step with immutable step ID and timer. Every reusable component has its own paired title, ingredient and step review. The dossier is an **aid for human review**, not a translation replacement and not a signed approval.

## 2. Italian editorial pass is first

The source triage lists all 112 records as **PENDING_EDITORIAL_REVIEW**, with conservative heuristic warnings and six independently observed copy conflicts:

| Italian recipe | Reason to check against the complete method |
| --- | --- |
| 000059 — Asari no Sakamushi | Awkward clause about clams/consistency |
| 000073 — Pork Kakuni | Braised pork described as dough/filling work |
| 000074 — Oden | “Nel Oden” grammar; generic final-seasoning language |
| 000081 — Tamago Sando | Egg sandwich described as dough and oven-ready wrapper |
| 000088 — Fruit Sando | Fruit sandwich described as dough development/cooking |
| 000124 — Uni Don | Raw sea-urchin rice bowl described with whipping technique |

These are **review leads**, not automatic edits. Other failures may exist. Review *every* Italian recipe and reusable component for actual cooking steps, quantities, time/rest coherence, food safety, source/anime evidence, grammar and dish-specific copy. Escalate raw seafood, eggs, poultry and perishables for qualified food-safety validation. Do not infer regional legal or culinary certification from a generic temperature rule.

Italian edits must be source-authored in the canonical file, increment per-recipe content versions, update provenance and trigger an atomic revision of all five source-locked candidate packs and related copyedit modules. **Never merely replace hashes on unchanged, semantically stale translations.** If exact translation revision cannot be completed, hold the source revision in a dedicated PR and keep all target locales quarantined.

## 3. Bilingual native review, not AI certification

For each of the five locales, a qualified bilingual/native editor must inspect **112/112** recipes and **10/10** reusable components line-by-line against the latest Italian source. Include the complete operation, culinary terminology (including Japanese words), quantities, timing and temperatures, ingredient notes, regional safety suitability, anime context and idiomatic local language. The PT candidate was generated with an English pivot and needs explicit **pt-PT** normalization.

A real reviewer record should identify:
- actual reviewer and editorial qualification (no fabricated persona or credential);
- locale, recipe/component ID, source fingerprint and entity revision;
- actual timestamp, documented review scope, concrete findings and corrected fields;
- independent food-safety clearance where required, with market-specific scope;
- signed acceptance or rejection and an evidence location the project can audit.

No B2 generator may write \`reviewEvidence\`, \`human_reviewed\`, release approval, runtime JSON or store metadata. Existing packs must retain \`machine_draft_not_publishable\`, recipe \`machine_draft\` and \`editorialStaging.noAutomaticPublication=true\` until qualified reviews and the separate B3 promotion process actually establish otherwise.

## 4. Technical gates and decision

The GitHub F3L editorial staging workflow generates the dossiers only after source/pack structural and semantic checks. The development checks and translation candidate workflow remain distinct. Stage/PR green does **not** mean editorial approval.

B2 is **NOT COMPLETE** until every Italian recipe and component has a documented contextual review, all five target locales have complete and qualified review evidence (112 recipe records + 10 components each), and no unresolved culinary, linguistic, rights or food-safety issues remain. B3 then performs an explicit **versioned** runtime promotion, Flutter/web/Android build and real device/release testing.

**Current approval accounting: 0/112 per locale; 0/10 components per locale; release NO-GO.** This file is a process specification; it is not evidence that manual reviews have occurred.

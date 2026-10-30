# Cooking Anime — R1 culinary & food-safety pre-audit (candidate, not approval)

**Status:** PRE-AUDIT / DRAFT / NO HUMAN SIGN-OFF. 29 October 2026.
**Input:** PR #41 source candidate `7fabb1b36e625b4247a0247cac17351a7c8a13c1`, path `authoring/f3k_it_hardening_51_162.json`, repository content blob `5edfe3e16cccd4e3f93d4be4db4fea2f7c2f4af3`. Italian canonical source digest recorded in F3L: `deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67`.
**R0 state (verified):** PR #41 was squash-merged on 29 October 2026 as `cae9efe1488253d996234f249c0dd8ef3a0b14da`. The post-merge `main` F3K source blob remains `5edfe3e16cccd4e3f93d4be4db4fea2f7c2f4af3` (equal to the candidate above). This draft dossier is **not approved for R1 merge** until genuine qualified review evidence and dispositions exist. Original branch baseline: `4191933639afc7c01b6e459270c7394b297c3fbd`.

## Purpose and boundary

This is a source-grounded **triage and review queue**, not a completed culinary review. It does not change recipes, versions, hashes, translations, runtime catalog, artwork, entitlements or approval state. No chef, food-safety expert or native reviewer has signed off; all rows remain PENDING. An existing field named `it_reviewed_translation_blocked` is NOT a fresh independent R1 human certificate.

For each source recipe and reusable component, qualified reviewers must establish: correct ingredient identity/amount, complete prep sequence, elapsed time including dependencies, foodborne hazards and validated safe handling/cooking, allergens/cross-contamination, sourcing/rights, source-specific action and reviewer identity/evidence/date. Any actual fix must use the canonical authoring/version/fingerprint workflow after R0, then refresh the five source-bound quarantined drafts. **No review evidence -> no R1 PASS.**

## First-pass cases to investigate (risk hypotheses, not confirmed incidents)

| Case | Severity to triage | Source | Finding / required check | Next action |
| --- | --- | --- | --- | --- |
| R1-001 | P0 CANDIDATE | `recipe_000056` — Chirashizushi | Raw salmon/tuna listed and assembled without an explicit supplier/validated raw-consumption control in the preparation. Verify suitability, parasite controls, refrigeration and vulnerable-user advice. Do not treat sashimi wording alone as safety verification. | Ingredient sourcing + safe handling + full step copy; changes only after R0 |
| R1-002 | P0 CANDIDATE | `component_ajitama` — Ajitama | 6 min 30 s soft-boiled eggs; no pasteurized-egg option or fully cooked alternative stated. Verify Salmonella risk, storage, refrigeration and intended audience; downstream ramen cross-reference required. | Component policy + dependent recipes |
| R1-003 | P0 CANDIDATE | `recipe_000110` — Motsunabe | Ingredients allow different beef/pork offal; blanch 1 minute then simmer 10–15 minutes until tender, with no verified preparation-specific doneness/temperature control. Review safe cleaning, full cooking, suitable supplier and timing. | Culinary expert for specific offal varieties; avoid universal cook time |
| R1-004 | P0 CANDIDATE | `recipe_000150` — Kamo Namban Soba | Duck breast cooks 8–10 minutes skin-down, 2 minutes reverse and 2 minutes in broth, but no core-temperature check. A time-only method may vary by breast size. Verify fully cooked poultry endpoint or an explicitly justified validated method. | Internal temperature and technique checked by qualified reviewer |
| R1-005 | P1 CANDIDATE | `recipe_000051` — Shio Ramen | Displayed 45-minute elapsed time uses pre-made chashu and ajitama. Their component elapsed times are 180 and 260 minutes. Clarify advance-preparation assumption and user-facing time definition; include component safety link. | Time dependency plus referenced components |
| R1-006 | P1 CANDIDATE | `recipe_000059` — Asari no Sakamushi | The shell-open/discard rule is present, but prescribed 3–4 min steam should be checked against the intended shellfish/cooking guidance, sanitary origin, handling and timing. Do not automatically assume opening alone certifies safety. | Shellfish sourcing and verified preparation |
| R1-007 | P1 CANDIDATE | `recipe_000080` — Sanma no Shioyaki | Method cooks whole fish including viscera, with time/appearance checks but no core-temperature check. Verify sourcing, handling and whether whole-viscera method is suitable for a consumer-facing recipe. | Seafood specialist review |
| R1-008 | P1 CANDIDATE | `recipe_000124` — Uni Don | Source already requires raw suitability, refrigeration and avoids taste-as-safety checks. Confirm suppliers, shellfish-specific hazards and vulnerable-consumer communication; current precaution is not a safety sign-off. | Raw seafood handling |
| R1-009 | P1 CANDIDATE | `recipe_000146` — Maguro Don | Source already states raw suitability, refrigeration and that marinade does not confer safety. Verify documented supplier controls and raw consumption warnings; avoid turning existing guard into an automatic approval. | Raw fish handling and histamine risk |
| R1-010 | P1 CANDIDATE | `recipe_000134` — Shirasu Don | Pasteurized yolk explicitly required and shirasu listed as cooked. Verify actual ingredient state/handling and consumer-facing wording, without removing existing guard. | Egg and ready-to-eat seafood provenance |
| R1-011 | P1 CANDIDATE | `recipe_000162` — Yuzu Sorbet | Pasteurized egg white required and raw untreated explicitly excluded. Check cross-contamination/cold chain and duration; keep existing safeguards. | Cold dessert with egg whites |
| R1-012 | P1 CANDIDATE | `component_chashu` — Chashu | Review heat penetration, refrigeration after braising, 1-hour chilling assumption and safe rewarming across recipes. | Shared component validation |

| R1-013 | P0 CANDIDATE | `recipe_000153` — Tori Tsukune | Raw fresh egg yolk is served as a dip, with no pasteurization condition. Review a pasteurized yolk or a safe cooked alternative. | Qualified egg safety review; synchronize source plus five draft locales if changed |
| R1-014 | P0 CANDIDATE | `recipe_000133` — Tori Chashu Ramen | Rolled poultry is simmered on a time-only 15–20 minute instruction without measured internal doneness. | Qualified poultry cooking verification |
| R1-015 | P0 CANDIDATE | `recipe_000054` — Hambagu | Mixed ground meat is cooked by time and color, without an internal temperature check. | Ground meat endpoint verification |
| R1-016 | P0 CANDIDATE | `recipe_000064` — Menchi Katsu | Mixed ground meat is fried by prescribed minutes and dark crust; verify interior cooking safely. | Ground meat endpoint verification |
| R1-017 | P1 CANDIDATE | `recipe_000149` — Kani Chahan | Calls for day-old cold cooked rice without rapid-cooling and handling instructions. | Safe rice storage/reheating and supplier review |
| R1-018 | P1 CANDIDATE | `recipe_000117` — Karaage Namban Don | Poultry frying judged by color; cold mayo/egg topping handled separately. | Measured poultry endpoint and hygiene |
| R1-019 | P1 CANDIDATE | `recipe_000096` — Asari Clam Chowder | Opens clams in covered pan; verify shellfish source, broth filtering, safe handling and unopened-clam disposition. | Shellfish expertise |
| R1-020 | P1 CANDIDATE | `recipe_000156` — Asari Ramen | Clams cooked briefly and reused in broth, without explicit discard of unopened clams. | Shellfish expertise |

These are **20 source-witnessed candidate follow-ups**, not a declaration that other records are safe. Priority P0/P1 here denotes triage urgency, not verified severity. The complete review matrix remains pending below.

### Executable review queue

The separate tooling PR [#45](https://github.com/riccardopinato/In-Cucina-con-gli-Anime/pull/45) introduces `python3 tool/r1_culinary_triage.py` (output `build/r1/culinary_triage.json`). It pins the merged Italian source SHA, preserves 112/112 recipes + 10/10 components and their dependencies, emits 20 verbatim-source review leads, and refuses unexpected source changes. **It never creates approvals.** CI/test success of that tool is not acceptance of the 20 leads or of the remaining 102 records without explicit findings.

#### Candidate remediation guidance (NOT applied)

- For #153 and Ajitama: distinguish eggs explicitly pasteurized for lightly cooked/uncooked service from ordinary fresh eggs, or provide a properly cooked alternative.
- For #54, #64, #133, #150 and #117: have a qualified reviewer validate a measurable cooking endpoint appropriate to each meat and process; timing and crust color alone are insufficient.
- For #56, #124 and #146: do not assume marination or freezing removes *all* hazards; retain raw-consumption sourcing, cold-chain and risk-group warnings where appropriate.
- For #149: document cooling of cooked rice promptly and safe refrigerated storage/reheating; do not rely on `day-old` alone.
- For #51: explicitly describe pre-prepared components; component durations are source-grounded: chashu **180 min**, ajitama **260 min**.


## External references used only as review criteria

The following official references were independently checked on 29 October 2026. They provide **screening criteria**, not a professional sign-off nor proof that a recipe is safe.

- FoodSafety.gov — [safe minimum internal temperatures](https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures): poultry including duck **74 °C**; ground beef/pork **71 °C**; finfish **63 °C**, or the listed validated doneness cues. Applicability must be decided for each recipe and market.
- FDA — [selecting and serving seafood safely](https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely): freezing controls some parasites but not all harmful germs; vulnerable groups should avoid raw seafood.
- Istituto Superiore di Sanità — [Anisakidosi / prevenzione](https://www.issalute.it/index.php/la-salute-dalla-a-alla-z-menu/a/anisakidosi-o-anisakiasi): raw fish controls and proper handling of viscera.
- Istituto Superiore di Sanità — [Salmonella](https://www.epicentro.iss.it/salmonella/): raw/undercooked eggs are a risk category.
- UK Food Standards Agency — [home food fact checker](https://www.gov.uk/government/publications/home-food-fact-checker/home-food-fact-checker): cooked rice requires prompt cooling, refrigerated storage and appropriate reheating. UK-specific guidance; verify release-market applicability.

## Candidate corrections for qualified review — NOT committed to source

This is an editorial change proposal queue, **not approved/safe-to-publish recipe copy**. The sentences below are deliberately specific to affected operations and contain no invented certifications. A qualified culinary/food-safety reviewer must validate market requirements, actual ingredient/process constraints, the consumer-facing wording and any alternative, **before** an editor changes canonical source and atomically refreshes five quarantined language packs with version/hash updates.

| Recipe / component | Candidate surgical remediation (Italian source proposal; not applied) | Gate |
| --- | --- | --- |
| `recipe_000153` — Tori Tsukune | Replace the fresh raw dipping yolk with **tuorlo da uovo pastorizzato espressamente idoneo al consumo senza cottura** or a fully cooked alternative. Add a validated poultry core-temperature check for minced chicken before serving. | Egg supply/product suitability + poultry; qualified validation |
| `component_ajitama` | Keep soft yolk only if an appropriate pasteurized/validated egg and storage procedure is specified; otherwise cook until fully set. Explicitly distinguish the 6m30s **quality/timing estimate** from safety evidence. | Shared-component and every dependent ramen |
| `recipe_000133` — Tori Chashu | Rolled chicken: replace time-only `15–20 minuti` as completion criterion with a check that the center reaches **at least 74 °C** using a probe, with cooking time described as indicative; review reheating after cooling. | Poultry guidance + recipe feasibility |
| `recipe_000150` — Kamo Namban | Duck breast: add probe check to a fully cooked **74 °C** center under the consumer-safety standard used here; adjust technique/time as validated, without claiming 2 minutes always suffice. | Duck culinary quality + local-market safety |
| `recipe_000117` — Karaage Namban | Fry chicken until a measured **74 °C at thickest point**; keep cold egg/mayo topping refrigerated and prevent cross-contamination during plating. | Method and cold topping QA |
| `recipe_000054` — Hambagu | Verify a **71 °C** internal endpoint for mixed ground beef/pork, rather than just crust color/steam time. | Recipe technique and temperature measurement |
| `recipe_000064` — Menchi Katsu | Verify mixed ground meat reaches **71 °C** at its thickest point; oil temperature, crust darkness and fixed minutes alone do not certify center doneness. | Frying and measured center |
| `recipe_000056` — Chirashizushi | Specify documented raw-consumption-appropriate salmon and tuna from a suitable supplier, uninterrupted refrigeration and separate clean tools. Explicitly warn that freezing controls some parasite hazards but does **not** eliminate all microorganisms. | Fish species/sourcing + Italy/EU rules + vulnerable groups |
| `recipe_000149` — Kani Chahan | Define prompt cooling of leftover rice (ideally within **1 hour**), refrigeration, use within **24 hours**, thorough reheating until steaming hot and no repeat reheating; adapt to approved release-market policy. | Cold-chain feasibility + UK criteria not automatically Italian certification |
| `recipe_000110` — Motsunabe | Separate tripe from other offal varieties in ingredient/process prerequisites; validate handling and complete-cook endpoint per actual selected organ. A 1-minute blanch + 10–15 minute simmer must not be treated as universally sufficient. | Specialist review per ingredient |
| `recipe_000051` — Shio Ramen | Clarify the indicated **45 min** assumes already prepared chashu (component **180 min**) and ajitama (**260 min**), or explicitly represent total advance-preparation effort and refrigeration. | UI time semantics + component dependencies |

**No text above was applied to a recipe.** This list is intentionally a review prompt, not a direct instruction to bypass F3L localization source locks. Additional cases R1-006, 007, 008, 009, 010, 011, 012, 019 and 020 remain unresolved in the case table.

## 112/112 recipe review checklist — all PENDING

**Definition:** checked means independently reviewed with dated evidence (not simply present/parsed). All unchecked here.
- [ ] `recipe_000051` — Shio Ramen (Ramen al Sale con Chashu e Menma) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000052` — Kare Pan (Panino al Curry Fritto Croccante) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000053` — Ebi Tendon (Tempura di Gamberi con Salsa Tentsuyu) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000054` — Hambagu (Hamburg Steak Giapponese con Salsa Demi-Glace) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000055` — Miso Nikomi Udon (Udon Stufati al Miso) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000056` — Chirashizushi (Riso Sushi Festivo guarnito con Pesce e Verdure) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000057` — Kurogoma Dango (Dango al Sesamo Nero Tostato) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000058` — Hanami Dango (Dango Tricolore della Primavera) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000059` — Asari no Sakamushi (Vongole al Vapore con Sake e Zenzero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000060` — Castella Cake (Pan di Spagna Sofficissimo Giapponese) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000061` — Miso Ramen di Sapporo · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000062` — Kurogoma Nabe (Stufato di Maiale al Sesamo Nero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000063` — Tenshinhan (Omelette di Granchio su Riso con Salsa Agrodolce) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000064` — Menchi Katsu (Cotoletta Croccante di Carne Macinata) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000065` — Shogayaki (Lombata di Maiale allo Zenzero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000066` — Mabo Nasu (Melanzane Saltate al Miso e Carne) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000067` — Monjayaki (Piastra Tradizionale di Tokyo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000068` — Dorayaki alla Crema Custard (Variante alla Crema) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000069` — Yuzu Cheesecake (Cheesecake Cotta allo Yuzu) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000070` — Sakura Mochi (Mochi con Foglia di Ciliegio Salata) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000071` — Tantanmen (Ramen Piccante al Sesamo e Carne Macinata) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000072` — Yakisoba Classica alla Piastra · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000073` — Pork Kakuni (Pancia di Maiale Stufata allo Zenzero e Salsa di Soia) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000074` — Oden Invernale Tradizionale · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000075` — Katsu Curry Udon · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000076` — Agedashi Tofu (Tofu Fritto in Brodo Dashi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000077` — Unadon (Ciotola di Riso con Anguilla Kabayaki Grigliata) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000078` — Ebi Chili (Gamberi Saltati in Salsa Piccante al Pomodoro e Zenzero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000079` — Kani Cream Korokke (Crocchette Cremose al Granchio) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000080` — Sanma no Shioyaki (Luccio di Mare Grigliato al Sale con Daikon) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000081` — Tamago Sando (Sandwich Soffice all'Uovo Giapponese) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000082` — Mizutaki Nabe (Stufato di Pollo e Verdure di Hakata) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000083` — Tsukemen (Ramen con Brodo Concentrato da Intingolo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000084` — Chicken Namban (Pollo Fritto con Salsa Tartara Giapponese) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000085` — Warabi Mochi (Mochi Trasparente con Kinako e Kuromitsu) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000086` — Soufflé Pancake Giapponesi (Pancake Altissimi e Soffici) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000087` — Mont Blanc Chestnut Cake (Torta Mont Blanc alle Castagne) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000088` — Fruit Sando (Sandwich alla Frutta Fresca e Panna) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000089` — Botamochi / Ohagi (Mochi di Riso Glutinoso con Anko) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000090` — Shoyu Ramen Classic · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000091` — Takikomi Gohan · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000092` — Moyashi Itame · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000093` — Katsu Donburi al Formaggio · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000094` — Ishikari Nabe · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000095` — Yuzu Shio Ramen · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000096` — Asari Clam Chowder · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000097` — Kakiage Tempura · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000098` — Chicken Teriyaki Don · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000099` — Anko Dango con Kinako · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000100` — Japanese Curry Udon Classico · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000101` — Yaki Onigiri alla Salsa di Soia e Burro · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000102` — Dashi Maki Tamago · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000103` — Matcha Parfait Stratificato · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000104` — Kabocha Korokke · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000105` — Nerikiri · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000106` — Sweet Potato Yaki-Imo · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000107` — Ogura Toast · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000108` — Tonkotsu Ramen (Ramen in Brodo Denso di Maiale) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000109` — Kurogoma Ice Cream (Gelato al Sesamo Nero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000110` — Motsunabe (Stufato di Frattaglie e Porri di Fukuoka) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000111` — Saba no Misoni (Sgombro Stufato al Miso e Zenzero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000112` — Chashu Don (Ciotola di Riso con Maiale Brasato e Uovo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000113` — Ebi Mayo (Gamberi Croccanti in Salsa Maionese Agrodolce) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000114` — Nagashi Somen (Somen Freddi Estivi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000115` — Anmitsu Classico (Gelatina Kanten con Frutta, Anko e Kuromitsu) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000116` — Kimpira Gobo (Radici di Bardana e Carote Saltate) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000117` — Tori no Karaage Namban Don (Ciotola di Pollo Fritto Namban) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000118` — Kakuni Udon (Udon con Maiale Brasato Morbidissimo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000119` — Kenchinjiru (Zuppa Buddista Vegetariana con Tofu e Radici) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000120` — Yaki Soba Omelette (Omusoba) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000121` — Soufflé Cheesecake Giapponese (Cotton Cheesecake) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000122` — Suika Shiratama (Anguria Estiva con Mochi di Riso e Sciroppo al Limone) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000123` — Tori Zosui (Minestra di Riso, Pollo e Uovo in Brodo Dashi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000124` — Uni Don (Ciotola di Riso con Ricci di Mare Freschi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000125` — Choco Cornet (Panino Soffice a Cono Farcito al Cioccolato) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000126` — Kushikatsu (Spiedini Fritti Croccanti di Osaka) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000127` — Mizumochi / Raindrop Cake (Mochi d'Acqua Trasparente) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000128` — Curry Stufato con Cacao e Mela (Apple & Cocoa Curry) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000129` — Niku Soba (Soba Calda con Maiale e Porri) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000130` — Ebi Tempura Udon (Udon in Brodo con Tempura di Gamberi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000131` — Hiyashi Tanuki Udon (Udon Freddi con Tenkasu Croccanti) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000132` — Katsu Curry Sando (Sandwich con Cotoletta e Salsa Curry) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000133` — Tori Chashu Ramen (Ramen con Pollo Marinato) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000134` — Shirasu Don (Ciotola di Riso con Bianchetti e Uovo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000135` — Agedashi Nasu (Melanzane Fritte Marinate in Brodo Dashi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000136` — Tofu Dengaku (Spiedini di Tofu al Miso) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000137` — Yakiudon al Sesamo e Verdure · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000138` — Tonjiru (Ricca Zuppa di Maiale, Radici e Miso) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000139` — Kabocha no Nimono (Zucca Giapponese Stufata) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000140` — Matcha Mille Crepe Cake (Torta Millefoglie di Crepes al Tè Verde) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000141` — Kurogoma Pudding (Budino al Sesamo Nero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000142` — Matcha Daifuku con Anko · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000143` — Japanese Fruit Tartlet (Tartellette alla Frutta Fresca) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000144` — Soufflé Cheese Tart (Crostatine al Formaggio Soffici) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000145` — Sata Andagi (Frittelle Dolci Tradizionali di Okinawa) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000146` — Maguro Don (Ciotola di Riso con Tonno Rosso Fresco e Wasabi) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000147` — Kurogoma Ramen (Ramen al Brodo Denso di Sesamo Nero) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000148` — Ika no Sugatayaki (Calamaro Intero Grigliato alla Salsa Teriyaki) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000149` — Kani Chahan (Riso Saltato con Polpa di Granchio e Porri) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000150` — Kamo Namban Soba (Soba Calda in Brodo con Anatra e Porri Tostati) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000151` — Chashu Bun (Panino al Vapore Farcito con Maiale Brasato) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000152` — Yaki Curry (Curry al Forno Gratinato con Formaggio e Uovo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000153` — Tori Tsukune (Polpette di Pollo alla Piastra con Salsa Tare e Tuorlo) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000154` — Kenchin Udon (Udon in Zuppa Buddista con Tofu e Radici) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000155` — Buri Daikon (Ricciola Stufata con Radice di Daikon) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000156` — Asari Ramen (Ramen al Brodo di Vongole e Burro) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000157` — Nasu Dengaku (Melanzane Glassate al Miso Dolce Tostato) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000158` — Matcha Chiffon Cake (Torta Soffice e Alta al Tè Verde Matcha) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000159` — Kuri Manju (Dolcetto Cotto al Forno Ripieno di Castagne) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000160` — Coffee Jelly (Gelato e Gelatina al Caffè con Panna) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000161` — Fruit Crepe Harajuku Style (Crepe Arrotolata con Panna e Frutta) · culinary technique / ingredients / time / safety / rights **PENDING**
- [ ] `recipe_000162` — Yuzu Sorbet (Sorbetto Rinfrescante all'Agrume Yuzu) · culinary technique / ingredients / time / safety / rights **PENDING**

## 10/10 component checklist — all PENDING

- [ ] `component_chashu` — Chashu di maiale brasato · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_ajitama` — Ajitama / uova marinate per ramen · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_dashi` — Dashi base kombu e katsuobushi · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_tonkatsu` — Tonkatsu di maiale · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_chocolate_custard` — Crema al cioccolato per Choco Cornet · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_brioche_cornet` — Impasto brioche per Choco Cornet · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_karaage_ref` — Karaage completo · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_japanese_curry_ref` — Curry giapponese completo · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_kakuni_ref` — Kakuni completo · dependencies / prep / cooking / safety / versioning **PENDING**
- [ ] `component_yakisoba_ref` — Yakisoba completa · dependencies / prep / cooking / safety / versioning **PENDING**

## Review/evidence contract

Record a decision per ID: `PENDING | ISSUE_FOUND | FIX_CANDIDATE | VERIFIED_BY_QUALIFIED_REVIEWER`; evidence must identify reviewer, expertise, actual date, source digest/recipe version, validated food handling method and issue disposition. `RELEASE_READY` is not implied by source-only validation, translation CI or a paper checklist.

R1 completion requires **122/122 independently reviewed entries, zero unresolved P0/P1, authentic human evidence, and verified reconcilation with R0 / R2**, not merely this dossier or the CI of its draft PR.

## Scope exclusions

No claim of human food-safety certification; no draft EN/ES/FR/DE/PT promotion; no generated runtime catalog edits; no copyrighted visual asset production; no new ingredient substitutions without recipe-level review.

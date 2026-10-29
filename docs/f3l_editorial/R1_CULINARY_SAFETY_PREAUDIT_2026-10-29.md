# Cooking Anime — R1 culinary & food-safety pre-audit (candidate, not approval)

**Status:** PRE-AUDIT / DRAFT / NO HUMAN SIGN-OFF. 29 October 2026.
**Input:** PR #41 source candidate `7fabb1b36e625b4247a0247cac17351a7c8a13c1`, path `authoring/f3k_it_hardening_51_162.json`, repository content blob `5edfe3e16cccd4e3f93d4be4db4fea2f7c2f4af3`. Italian canonical source digest recorded in F3L: `deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67`.
**Dependency:** R1 is formally downstream of R0; **do not merge or promote this dossier until PR #41 has merged and the source digest has been rechecked against main.** Main baseline of this document branch: `4191933639afc7c01b6e459270c7394b297c3fbd`.

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

These are **12 candidate follow-ups**, not a declaration that other records are safe. Priority P0/P1 here denotes risk-screening urgency, not verified policy severity. The complete review matrix remains pending below.

## External references used only as review criteria

- FoodSafety.gov, minimum cooking temperatures: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures (poultry 74 °C; whole fish 63 °C or verified doneness; shellfish handling).
- FDA, seafood raw-consumption and risk groups: https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely (freezing can control some parasites but **not all microbial hazards**).
- ATS Brescia, correct handling of raw fish: https://www.ats-brescia.it/corretta-gestione-prodotti-ittici-crudi (Italian consumer context; parasite treatment and cold chain).
- UK food fact checker, cooked rice cooling/reheating: https://www.gov.uk/government/publications/home-food-fact-checker/home-food-fact-checker (within 1 h cooling ideal, 24 h chilled use, reheat at most once).
- AUSL Veneto seafood guidance, consult local authoritative source for shellfish cooking and market conditions before updating recipes: https://www.aulss3.veneto.it/myportal/AU12VE/api/content/download?id=63dce51cc2a2200088d4731b

References are **screening material**, not proof that a given recipe passed. Jurisdiction-specific guidance must be validated in the release market.

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

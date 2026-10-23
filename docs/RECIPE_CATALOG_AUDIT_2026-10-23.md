# Recipe Catalog Audit — 2026-10-23

Scope: production recipes `recipe_000001`–`recipe_000020`, F3D/F3E artwork cleanup, and the second ten-recipe batch supplied in `Altre 10 Ricette Complete dagli Anime.pdf`.

## Audit policy

- The user-provided PDF is the editorial source for recipes 11–20.
- Source wording is rebuilt rather than copied verbatim.
- Contradictory timing is corrected and documented in each recipe `sourceNote`.
- Visual approval is dish-semantic, not merely aesthetic: the artwork must depict the ingredients/preparation of the canonical authoring record.
- Artwork is original generated content; direct anime frames and third-party food images are not shipped.
- One JPEG is stored per recipe and reused for card crop + full detail hero.

## Existing catalog audit (1–10)

| ID | Dish | Result |
| --- | --- | --- |
| 000001 | Skillet eggs + crispy bacon | PASS — artwork matches eggs, bacon, butter/pepper and rustic bread |
| 000002 | Miso ramen + chashu | PASS — existing approved artwork retained |
| 000003 | Katsudon | PASS after regeneration — first candidate looked too much like sauce-topped tonkatsu; final artwork includes soft egg + onion |
| 000004 | Dorayaki + anko | PASS |
| 000005 | Tuna-mayo onigiri | PASS after regeneration — final cutaway shows flaky tuna + mayonnaise rather than an ambiguous pink filling |
| 000006 | Kansai okonomiyaki | PASS with editorial correction — source label “Aoki seaweed” normalized to **aonori**; stable ingredient ID retained, contentVersion bumped |
| 000007 | Takoyaki | PASS |
| 000008 | Omurice | PASS |
| 000009 | Oyakodon | PASS — corrected artwork from prior F3D review retained |
| 000010 | Pumpkin + fish puff-pastry bake | PASS |

## Second editorial batch audit (11–20)

| ID | Dish | Editorial result |
| --- | --- | --- |
| 000011 | Chaliapin Steak Don | PASS with timing correction: source table says 25 min while method alone requires 30 min onion tenderizing; catalog uses 35 min prep + 10 min cook |
| 000012 | Gotcha Pork Roast | PASS — potato/onion/mushroom loaf fully wrapped in bacon, not an actual pork roast |
| 000013 | Japanese Curry Rice | PASS — meat, potato, carrot, onion, Japanese curry roux and grated apple |
| 000014 | Spicy Mapo Tofu | PASS — tofu, ground pork, doubanjiang, Sichuan pepper, garlic/ginger and starch-thickened broth |
| 000015 | Nikujaga | PASS — thin beef, potatoes, carrot, onion, dashi, soy, mirin and sugar |
| 000016 | Karaage | PASS — chicken thigh, soy/sake/ginger/garlic marinade, potato-starch coating, two-stage frying |
| 000017 | Tamagoyaki | PASS — layered rolled egg with dashi/sugar/soy seasoning |
| 000018 | Nikuman | PASS with timing correction: source table says 45 min but method includes 60 min proof + 15–18 min steam; catalog uses 75 min prep + 18 min cook |
| 000019 | Mitarashi Dango | PASS — rice dumplings with light char and sweet soy glaze |
| 000020 | Taiyaki | PASS — fish-shaped cake with anko filling |

## Cross-check notes

External culinary references were used only to verify dish identity/composition where useful. They corroborated the core structures of Gotcha Pork Roast, Japanese curry, Nikujaga, Karaage, Tamagoyaki, Nikuman, Mitarashi Dango and Taiyaki. The shipped text remains the app’s own editorial copy derived primarily from the user-provided source.

## Artwork / weight result

- 20 published recipes.
- 20 canonical artwork entries.
- All newly generated JPEGs are already below the F3E 140 KiB hard ceiling before the optimizer runs.
- Current generated range for the 18 new files: roughly 40–84 KiB.
- F3E dimension gate remains 720 px minimum short edge / 960 px maximum long edge.
- Card presentation uses the same file with `BoxFit.cover`; detail uses the same file with `BoxFit.contain`.

## Technical cleanup included in F3F

- Removed dependency on the obsolete F3D pilot branch condition for Android CI.
- Android ARM64 build/upload now runs for every PR.
- Materialized recipe-content artifact is uploaded before the drift check, making catalog batch recovery deterministic.
- Factory baseline references updated to `4cc0b94467b94ab6fabe2c927fcc58afff49e39a`.

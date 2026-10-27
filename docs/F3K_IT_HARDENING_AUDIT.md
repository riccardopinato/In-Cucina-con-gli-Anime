# F3K — Italian editorial hardening 51–162

Date: 2026-10-27

## Scope

F3K hardens only the Italian editorial baseline for `recipe_000051` through `recipe_000162`. EN/ES/FR/DE/PT are intentionally blocked and must not be regenerated until this Italian package is frozen at 112/112 PASS.

## Non-negotiable quality contract

- no fixed four-step quota: each recipe uses as many meaningful steps as the dish requires;
- procedure must be cookable end-to-end, not generic filler;
- rests, proofing, chilling, freezing, marinades and long simmering count toward real elapsed time;
- ingredients are normalized and every quantity is either measured or explicitly `q.b.`;
- reusable subcomponents (dashi, chashu, ajitama, tonkatsu, curry, kakuni, yakisoba, karaage) must resolve to a complete component or recipe reference;
- descriptions must be dish-specific and may not be near-duplicates;
- every anime association is individually reviewed; factual appearance claims require evidence, otherwise the relation remains `inspired`;
- translation state remains blocked until the entire Italian quality gate passes.

## Automated result

**F3K Italian quality gate: PASS (local staging).**

- recipes: **112/112**
- procedure steps: min **6**, median **8**, max **13**
- procedure words: min **100**, median **124**, max **204**
- description words: min **40**, median **56.5**, max **72**
- resolved reusable component references: **61**
- anime relations reviewed: **224/224**
  - evidence-backed verified appearances: **2**
  - evidence-backed recurring associations: **2**
  - deliberately conservative editorial inspiration only: **220**
- unreviewed / `unverified` anime relations: **0**
- translations EN/ES/FR/DE/PT: **BLOCKED**

## Important interpretation of anime review

`inspired` is not a weaker or unfinished state in F3K. It is the correct final classification when there is no direct evidence that the exact dish appears in the named work. The review is complete when every association has been examined and either receives evidence-backed appearance/recurrence semantics or is deliberately kept as inspiration without an episode claim.

## Recipe evidence table

| ID | Italian title | Steps | Procedure words | Total elapsed | Anime review |
| --- | --- | ---: | ---: | ---: | --- |
| `recipe_000051` | Shio Ramen (Ramen al Sale con Chashu e Menma) | 9 | 131 | 45 min | Emiya-san Chi no Kyou no Gohan: inspired, Naruto: inspired |
| `recipe_000052` | Kare Pan (Panino al Curry Fritto Croccante) | 13 | 146 | 110 min | Black Butler (Kuroshitsuji): inspired, My Hero Academia: inspired |
| `recipe_000053` | Ebi Tendon (Tempura di Gamberi con Salsa Tentsuyu) | 9 | 149 | 35 min | Food Wars! (Shokugeki no Soma): inspired, Mob Psycho 100: inspired |
| `recipe_000054` | Hambagu (Hamburg Steak Giapponese con Salsa Demi-Glace) | 13 | 194 | 35 min | Spy x Family: inspired, Food Wars!: inspired |
| `recipe_000055` | Miso Nikomi Udon (Udon Stufati al Miso) | 8 | 140 | 30 min | Yuru Camp△: inspired, Natsume Yuujinchou: inspired |
| `recipe_000056` | Chirashizushi (Riso Sushi Festivo guarnito con Pesce e Verdure) | 7 | 107 | 30 min | Fruits Basket: inspired, Kimi ni Todoke: inspired |
| `recipe_000057` | Kurogoma Dango (Dango al Sesamo Nero Tostato) | 10 | 154 | 25 min | Gintama: inspired, Samurai Champloo: inspired |
| `recipe_000058` | Hanami Dango (Dango Tricolore della Primavera) | 11 | 146 | 25 min | Demon Slayer (Kimetsu no Yaiba): inspired, Clannad: inspired |
| `recipe_000059` | Asari no Sakamushi (Vongole al Vapore con Sake e Zenzero) | 9 | 117 | 15 min | Food Wars! (Shokugeki no Soma): inspired, Midnight Diner (Shinya Shokudo): inspired |
| `recipe_000060` | Castella Cake (Pan di Spagna Sofficissimo Giapponese) | 8 | 147 | 68 min | Si alza il vento (Studio Ghibli): inspired, Gintama: inspired |
| `recipe_000061` | Miso Ramen di Sapporo | 11 | 204 | 45 min | Food Wars! - Shokugeki no Soma: inspired, Ramen Daisuki Koizumi-san: inspired |
| `recipe_000062` | Kurogoma Nabe (Stufato di Maiale al Sesamo Nero) | 9 | 154 | 30 min | Yuru Camp△: inspired, Emiya-san Chi no Kyou no Gohan: inspired |
| `recipe_000063` | Tenshinhan (Omelette di Granchio su Riso con Salsa Agrodolce) | 8 | 154 | 25 min | Dragon Ball: inspired, Food Wars! - Shokugeki no Soma: inspired |
| `recipe_000064` | Menchi Katsu (Cotoletta Croccante di Carne Macinata) | 9 | 160 | 35 min | Isekai Shokudo - Restaurant to Another World: inspired, Persona 5: inspired |
| `recipe_000065` | Shogayaki (Lombata di Maiale allo Zenzero) | 7 | 145 | 20 min | Cooking Papa: inspired, Food Wars! - Shokugeki no Soma: inspired |
| `recipe_000066` | Mabo Nasu (Melanzane Saltate al Miso e Carne) | 9 | 127 | 25 min | Food Wars! - Shokugeki no Soma: inspired, Cooking Master Boy: inspired |
| `recipe_000067` | Monjayaki (Piastra Tradizionale di Tokyo) | 9 | 124 | 20 min | K-On!: inspired, March Comes in Like a Lion: inspired |
| `recipe_000068` | Dorayaki alla Crema Custard (Variante alla Crema) | 12 | 141 | 30 min | Doraemon: inspired, Kimi no Na wa (Your Name): inspired |
| `recipe_000069` | Yuzu Cheesecake (Cheesecake Cotta allo Yuzu) | 8 | 117 | 325 min | Food Wars! - Shokugeki no Soma: inspired, Kaichou wa Maid-sama!: inspired |
| `recipe_000070` | Sakura Mochi (Mochi con Foglia di Ciliegio Salata) | 7 | 123 | 35 min | Demon Slayer (Mitsuri Kanroji): recurring_association, Kimi ni Todoke: inspired |
| `recipe_000071` | Tantanmen (Ramen Piccante al Sesamo e Carne Macinata) | 10 | 165 | 45 min | Food Wars! (Shokugeki no Soma): inspired, Ramen Daisuki Koizumi-san: inspired |
| `recipe_000072` | Yakisoba Classica alla Piastra | 10 | 130 | 30 min | My Hero Academia: inspired, Food Wars!: inspired |
| `recipe_000073` | Pork Kakuni (Pancia di Maiale Stufata allo Zenzero e Salsa di Soia) | 8 | 150 | 120 min | Emiya-san Chi no Kyou no Gohan: inspired, Food Wars!: inspired |
| `recipe_000074` | Oden Invernale Tradizionale | 8 | 129 | 117 min | Gintama: inspired, One Piece: verified_appearance |
| `recipe_000075` | Katsu Curry Udon | 9 | 124 | 50 min | Persona 5: inspired, Jujutsu Kaisen: inspired |
| `recipe_000076` | Agedashi Tofu (Tofu Fritto in Brodo Dashi) | 9 | 136 | 34 min | Demon Slayer (Kimetsu no Yaiba): inspired, Spirited Away: inspired |
| `recipe_000077` | Unadon (Ciotola di Riso con Anguilla Kabayaki Grigliata) | 8 | 120 | 25 min | Food Wars!: inspired, Detective Conan: inspired |
| `recipe_000078` | Ebi Chili (Gamberi Saltati in Salsa Piccante al Pomodoro e Zenzero) | 10 | 129 | 33 min | Food Wars!: inspired, Cooking Master Boy: inspired |
| `recipe_000079` | Kani Cream Korokke (Crocchette Cremose al Granchio) | 10 | 136 | 100 min | Isekai Shokudo (Restaurant to Another World): inspired, Spy x Family: inspired |
| `recipe_000080` | Sanma no Shioyaki (Luccio di Mare Grigliato al Sale con Daikon) | 8 | 109 | 27 min | Emiya-san Chi no Kyou no Gohan: inspired, Yuru Camp△: inspired |
| `recipe_000081` | Tamago Sando (Sandwich Soffice all'Uovo Giapponese) | 11 | 138 | 29 min | Spy x Family: inspired, Detective Conan: inspired |
| `recipe_000082` | Mizutaki Nabe (Stufato di Pollo e Verdure di Hakata) | 7 | 118 | 65 min | Yuru Camp△: inspired, Golden Kamuy: inspired |
| `recipe_000083` | Tsukemen (Ramen con Brodo Concentrato da Intingolo) | 7 | 139 | 70 min | Ramen Daisuki Koizumi-san: inspired, Food Wars!: inspired |
| `recipe_000084` | Chicken Namban (Pollo Fritto con Salsa Tartara Giapponese) | 9 | 124 | 35 min | Food Wars!: inspired, Isekai Izakaya Nobu: inspired |
| `recipe_000085` | Warabi Mochi (Mochi Trasparente con Kinako e Kuromitsu) | 7 | 119 | 20 min | Demon Slayer: inspired, Samurai Champloo: inspired |
| `recipe_000086` | Soufflé Pancake Giapponesi (Pancake Altissimi e Soffici) | 12 | 174 | 35 min | Food Wars!: inspired, Kaguya-sama: Love is War: inspired |
| `recipe_000087` | Mont Blanc Chestnut Cake (Torta Mont Blanc alle Castagne) | 8 | 128 | 60 min | Food Wars!: inspired, K-On!: inspired |
| `recipe_000088` | Fruit Sando (Sandwich alla Frutta Fresca e Panna) | 9 | 124 | 35 min | Cardcaptor Sakura: inspired, Horimiya: inspired |
| `recipe_000089` | Botamochi / Ohagi (Mochi di Riso Glutinoso con Anko) | 8 | 126 | 45 min | Demon Slayer: inspired, Fruits Basket: inspired |
| `recipe_000090` | Shoyu Ramen Classic | 7 | 141 | 45 min | Naruto: inspired, Ramen Daisuki Koizumi-san: inspired |
| `recipe_000091` | Takikomi Gohan | 7 | 152 | 50 min | Emiya-san Chi no Kyou no Gohan: inspired, Demon Slayer: inspired |
| `recipe_000092` | Moyashi Itame | 7 | 130 | 15 min | Gintama: inspired, One-Punch Man: inspired |
| `recipe_000093` | Katsu Donburi al Formaggio | 7 | 137 | 35 min | Food Wars!: inspired, Yuri!!! on ICE: inspired |
| `recipe_000094` | Ishikari Nabe | 7 | 133 | 45 min | Yuru Camp△: inspired, Golden Kamuy: inspired |
| `recipe_000095` | Yuzu Shio Ramen | 7 | 126 | 40 min | Ramen Daisuki Koizumi-san: inspired, Food Wars!: inspired |
| `recipe_000096` | Asari Clam Chowder | 7 | 106 | 35 min | Emiya-san Chi no Kyou no Gohan: inspired, Food Wars!: inspired |
| `recipe_000097` | Kakiage Tempura | 7 | 128 | 30 min | Food Wars!: inspired, Demon Slayer: inspired |
| `recipe_000098` | Chicken Teriyaki Don | 6 | 104 | 25 min | Cooking Papa: inspired, My Hero Academia: inspired |
| `recipe_000099` | Anko Dango con Kinako | 7 | 112 | 25 min | Samurai Champloo: inspired, Naruto: inspired |
| `recipe_000100` | Japanese Curry Udon Classico | 7 | 118 | 30 min | Persona 5: inspired, Mob Psycho 100: inspired |
| `recipe_000101` | Yaki Onigiri alla Salsa di Soia e Burro | 7 | 132 | 20 min | Yuru Camp△: inspired, Log Horizon: inspired |
| `recipe_000102` | Dashi Maki Tamago | 7 | 113 | 20 min | Food Wars!: inspired, Midnight Diner: inspired |
| `recipe_000103` | Matcha Parfait Stratificato | 7 | 117 | 20 min | K-On!: inspired, Gintama: inspired |
| `recipe_000104` | Kabocha Korokke | 8 | 102 | 40 min | Kiki - Consegne a domicilio: inspired, Food Wars!: inspired |
| `recipe_000105` | Nerikiri | 8 | 139 | 45 min | Demon Slayer: inspired, Kimi ni Todoke: inspired |
| `recipe_000106` | Sweet Potato Yaki-Imo | 7 | 121 | 100 min | My Neighbor Totoro: inspired, Yuru Camp△: inspired |
| `recipe_000107` | Ogura Toast | 7 | 129 | 15 min | Food Wars!: inspired, Dagashi Kashi: inspired |
| `recipe_000108` | Tonkotsu Ramen (Ramen in Brodo Denso di Maiale) | 8 | 170 | 442 min | Food Wars! (Shokugeki no Soma): inspired, Ramen Daisuki Koizumi-san: inspired |
| `recipe_000109` | Kurogoma Ice Cream (Gelato al Sesamo Nero) | 7 | 125 | 180 min | Food Wars!: inspired, Gintama: inspired |
| `recipe_000110` | Motsunabe (Stufato di Frattaglie e Porri di Fukuoka) | 7 | 125 | 45 min | Food Wars!: inspired, Golden Kamuy: inspired |
| `recipe_000111` | Saba no Misoni (Sgombro Stufato al Miso e Zenzero) | 7 | 132 | 25 min | Emiya-san Chi no Kyou no Gohan: inspired, Cooking Papa: inspired |
| `recipe_000112` | Chashu Don (Ciotola di Riso con Maiale Brasato e Uovo) | 7 | 113 | 20 min | Naruto: inspired, Food Wars!: inspired |
| `recipe_000113` | Ebi Mayo (Gamberi Croccanti in Salsa Maionese Agrodolce) | 7 | 119 | 25 min | Food Wars!: inspired, Isekai Izakaya Nobu: inspired |
| `recipe_000114` | Nagashi Somen (Somen Freddi Estivi) | 7 | 120 | 15 min | Non Non Biyori: inspired, Karakkai Jozu no Takagi-san: inspired |
| `recipe_000115` | Anmitsu Classico (Gelatina Kanten con Frutta, Anko e Kuromitsu) | 7 | 108 | 30 min | Gintama: inspired, Demon Slayer: inspired |
| `recipe_000116` | Kimpira Gobo (Radici di Bardana e Carote Saltate) | 7 | 113 | 20 min | Emiya-san Chi no Kyou no Gohan: inspired, Fruits Basket: inspired |
| `recipe_000117` | Tori no Karaage Namban Don (Ciotola di Pollo Fritto Namban) | 8 | 153 | 35 min | Food Wars!: inspired, My Hero Academia: inspired |
| `recipe_000118` | Kakuni Udon (Udon con Maiale Brasato Morbidissimo) | 7 | 120 | 50 min | Jujutsu Kaisen: inspired, Food Wars!: inspired |
| `recipe_000119` | Kenchinjiru (Zuppa Buddista Vegetariana con Tofu e Radici) | 7 | 113 | 30 min | Demon Slayer: inspired, Emiya-san Chi no Kyou no Gohan: inspired |
| `recipe_000120` | Yaki Soba Omelette (Omusoba) | 8 | 143 | 25 min | Food Wars!: inspired, Ranma ½: inspired |
| `recipe_000121` | Soufflé Cheesecake Giapponese (Cotton Cheesecake) | 8 | 155 | 120 min | Food Wars!: inspired, K-On!: inspired |
| `recipe_000122` | Suika Shiratama (Anguria Estiva con Mochi di Riso e Sciroppo al Limone) | 7 | 110 | 20 min | Grand Blue: inspired, Free!: inspired |
| `recipe_000123` | Tori Zosui (Minestra di Riso, Pollo e Uovo in Brodo Dashi) | 7 | 115 | 20 min | Barakamon: inspired, Gintama: inspired |
| `recipe_000124` | Uni Don (Ciotola di Riso con Ricci di Mare Freschi) | 7 | 128 | 15 min | Food Wars!: inspired, Golden Kamuy: inspired |
| `recipe_000125` | Choco Cornet (Panino Soffice a Cono Farcito al Cioccolato) | 8 | 129 | 210 min | Lucky Star: verified_appearance, Sound! Euphonium: inspired |
| `recipe_000126` | Kushikatsu (Spiedini Fritti Croccanti di Osaka) | 7 | 115 | 35 min | Food Wars!: inspired, Isekai Izakaya Nobu: inspired |
| `recipe_000127` | Mizumochi / Raindrop Cake (Mochi d'Acqua Trasparente) | 7 | 105 | 270 min | Food Wars!: inspired, Demon Slayer: inspired |
| `recipe_000128` | Curry Stufato con Cacao e Mela (Apple & Cocoa Curry) | 8 | 109 | 50 min | Food Wars! (Shokugeki no Soma): inspired, Persona 5: inspired |
| `recipe_000129` | Niku Soba (Soba Calda con Maiale e Porri) | 6 | 107 | 25 min | Demon Slayer: inspired, Jujutsu Kaisen: inspired |
| `recipe_000130` | Ebi Tempura Udon (Udon in Brodo con Tempura di Gamberi) | 8 | 128 | 35 min | Emiya-san Chi no Kyou no Gohan: inspired, Mob Psycho 100: inspired |
| `recipe_000131` | Hiyashi Tanuki Udon (Udon Freddi con Tenkasu Croccanti) | 7 | 100 | 20 min | March Comes in Like a Lion: inspired, Emiya-san Chi no Kyou no Gohan: inspired |
| `recipe_000132` | Katsu Curry Sando (Sandwich con Cotoletta e Salsa Curry) | 7 | 114 | 25 min | Chainsaw Man: inspired, Spy x Family: inspired |
| `recipe_000133` | Tori Chashu Ramen (Ramen con Pollo Marinato) | 7 | 117 | 45 min | Food Wars!: inspired, Ramen Daisuki Koizumi-san: inspired |
| `recipe_000134` | Shirasu Don (Ciotola di Riso con Bianchetti e Uovo) | 7 | 137 | 15 min | La collina dei papaveri: inspired, Midnight Diner: inspired |
| `recipe_000135` | Agedashi Nasu (Melanzane Fritte Marinate in Brodo Dashi) | 7 | 101 | 26 min | Emiya-san Chi no Kyou no Gohan: inspired, Demon Slayer: inspired |
| `recipe_000136` | Tofu Dengaku (Spiedini di Tofu al Miso) | 7 | 119 | 20 min | Demon Slayer: inspired, Samurai Champloo: inspired |
| `recipe_000137` | Yakiudon al Sesamo e Verdure | 7 | 115 | 20 min | Ranma ½: inspired, My Hero Academia: inspired |
| `recipe_000138` | Tonjiru (Ricca Zuppa di Maiale, Radici e Miso) | 8 | 111 | 30 min | My Hero Academia: inspired, Midnight Diner: inspired |
| `recipe_000139` | Kabocha no Nimono (Zucca Giapponese Stufata) | 6 | 105 | 25 min | Fruits Basket: inspired, Il mio vicino Totoro: inspired |
| `recipe_000140` | Matcha Mille Crepe Cake (Torta Millefoglie di Crepes al Tè Verde) | 8 | 110 | 70 min | K-On!: inspired, Food Wars!: inspired |
| `recipe_000141` | Kurogoma Pudding (Budino al Sesamo Nero) | 7 | 106 | 220 min | Gintama: inspired, Saiki K.: inspired |
| `recipe_000142` | Matcha Daifuku con Anko | 8 | 138 | 35 min | Hyouka: inspired, Fruits Basket: inspired |
| `recipe_000143` | Japanese Fruit Tartlet (Tartellette alla Frutta Fresca) | 8 | 107 | 70 min | Cardcaptor Sakura: inspired, K-On!: inspired |
| `recipe_000144` | Soufflé Cheese Tart (Crostatine al Formaggio Soffici) | 8 | 128 | 45 min | Food Wars!: inspired, Kaguya-sama: Love is War: inspired |
| `recipe_000145` | Sata Andagi (Frittelle Dolci Tradizionali di Okinawa) | 7 | 110 | 30 min | Non Non Biyori: inspired, Azumanga Daioh: inspired |
| `recipe_000146` | Maguro Don (Ciotola di Riso con Tonno Rosso Fresco e Wasabi) | 12 | 160 | 30 min | Food Wars!: inspired, Midnight Diner: Tokyo Stories: inspired |
| `recipe_000147` | Kurogoma Ramen (Ramen al Brodo Denso di Sesamo Nero) | 8 | 141 | 50 min | Ramen Daisuki Koizumi-san: inspired, Food Wars!: inspired |
| `recipe_000148` | Ika no Sugatayaki (Calamaro Intero Grigliato alla Salsa Teriyaki) | 9 | 118 | 20 min | One Piece: inspired, Food Wars!: inspired |
| `recipe_000149` | Kani Chahan (Riso Saltato con Polpa di Granchio e Porri) | 9 | 112 | 20 min | Food Wars!: inspired, Cooking Master Boy: inspired |
| `recipe_000150` | Kamo Namban Soba (Soba Calda in Brodo con Anatra e Porri Tostati) | 10 | 136 | 35 min | Demon Slayer: inspired, Emiya-san Chi no Kyou no Gohan: inspired |
| `recipe_000151` | Chashu Bun (Panino al Vapore Farcito con Maiale Brasato) | 9 | 120 | 127 min | Dragon Ball: inspired, Food Wars!: inspired |
| `recipe_000152` | Yaki Curry (Curry al Forno Gratinato con Formaggio e Uovo) | 7 | 104 | 35 min | Food Wars!: inspired, Persona 5: inspired |
| `recipe_000153` | Tori Tsukune (Polpette di Pollo alla Piastra con Salsa Tare e Tuorlo) | 6 | 106 | 30 min | Food Wars!: inspired, Midnight Diner: inspired |
| `recipe_000154` | Kenchin Udon (Udon in Zuppa Buddista con Tofu e Radici) | 8 | 114 | 30 min | Demon Slayer: inspired, Yuru Camp△: inspired |
| `recipe_000155` | Buri Daikon (Ricciola Stufata con Radice di Daikon) | 7 | 105 | 56 min | Emiya-san Chi no Kyou no Gohan: inspired, Midnight Diner: inspired |
| `recipe_000156` | Asari Ramen (Ramen al Brodo di Vongole e Burro) | 8 | 111 | 35 min | Ramen Daisuki Koizumi-san: inspired, Food Wars!: inspired |
| `recipe_000157` | Nasu Dengaku (Melanzane Glassate al Miso Dolce Tostato) | 9 | 113 | 25 min | Demon Slayer: inspired, Emiya-san Chi no Kyou no Gohan: inspired |
| `recipe_000158` | Matcha Chiffon Cake (Torta Soffice e Alta al Tè Verde Matcha) | 8 | 119 | 55 min | K-On!: inspired, Cardcaptor Sakura: inspired |
| `recipe_000159` | Kuri Manju (Dolcetto Cotto al Forno Ripieno di Castagne) | 9 | 122 | 60 min | Fruits Basket: inspired, Demon Slayer: inspired |
| `recipe_000160` | Coffee Jelly (Gelato e Gelatina al Caffè con Panna) | 7 | 120 | 145 min | The Disastrous Life of Saiki K.: recurring_association, K-On!: inspired |
| `recipe_000161` | Fruit Crepe Harajuku Style (Crepe Arrotolata con Panna e Frutta) | 10 | 116 | 36 min | Nana: inspired, K-On!: inspired |
| `recipe_000162` | Yuzu Sorbet (Sorbetto Rinfrescante all'Agrume Yuzu) | 7 | 110 | 300 min | Food Wars!: inspired, Kaguya-sama: Love is War: inspired |

## Translation release gate

Translation work may start only after:

1. this staging package is merged/accepted as the canonical Italian source for 51–162;
2. the exact-head CI run executes `tool/f3k_it_quality_gate.py` successfully;
3. no subsequent Italian edit invalidates that frozen baseline.

After those conditions, EN/ES/FR/DE/PT must be regenerated from this frozen Italian baseline, preserving the complete step structure rather than falling back to generic four-step templates.
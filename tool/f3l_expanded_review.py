"""F3L source-bound editorial corrections of observed recipe mistranslations.

AI-assisted copy edits, not a human/native certification. Never alter amounts, IDs or timers.
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from f3l_translation_gate import digest, inspect

SOURCE_SHA='954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c'
# Each entry is hand reconstructed from the exact Italian instruction, rather than
# translated with unconstrained substitutions. Ingredient names repaired below.
STEP_EDITS={
 'en':{
 (92,2):'Cut the pancetta, carrot and spring onion into thin pieces. Keep the soy sauce, granulated dashi, pepper and sesame oil beside the wok.',
 (95,6):'Add the chicken, menma bamboo shoots and half an egg, leaving some of the noodles visible.',
 (100,1):'Slice the onion and cut the meat into thin, bite-sized pieces. Bring a separate pot of water to the boil for the udon noodles.',
 (100,3):'Add the dashi, soy sauce and mirin; simmer gently for 3–4 minutes.',
 (100,6):'Cook the udon noodles in the separate pot of water, drain thoroughly and divide among the bowls.',
 (102,1):'In a bowl, gently beat the eggs with the dashi, mirin, soy sauce and salt, without whipping in air.',
 (102,7):'Shape with a bamboo mat, cut into thick slices and serve with grated daikon and soy sauce.',
 (105,6):'Flatten a portion of nerikiri, place the anko filling in the centre and seal the seam firmly underneath.',
 (110,3):'Prepare the broth with dashi, garlic, chilli and miso or soy sauce. Season it well, as the cabbage and tofu will dilute the flavour.',
 (135,7):'Serve warm or at room temperature with grated daikon and fresh ginger.',
 (137,1):'Loosen the udon noodles in boiling water for about 1 minute, drain and separate them gently without breaking them.',
 (137,5):'Add the udon noodles and stir-fry over high heat until thoroughly hot.',
 },
 'es':{
 (74,7):'Añade los saquitos kinchaku durante los últimos 10 minutos para ablandar el mochi del interior sin romperlos.',
 (93,2):'En una sartén pequeña para donburi, lleva a hervor suave el dashi con la salsa de soja, el mirin y el azúcar. Añade la cebolla y cocínala 3-4 minutos, hasta que esté translúcida.',
 (99,6):'Ensarta tres dango en cada brocheta y reparte por encima el anko de textura lisa.',
 (100,1):'Corta la cebolla en rodajas y la carne en trozos finos; pon a hervir aparte una olla de agua para los fideos udon.',
 (100,5):'Cuece otros 5 minutos removiendo: el caldo debe cubrir ligeramente la cuchara, pero seguir lo bastante fluido para envolver los udon.',
 (100,6):'Cuece los fideos udon en el agua aparte, escúrrelos bien y repártelos entre los cuencos.',
 (100,7):'Vierte el curry bien caliente sobre los udon, añade cebolleta y sirve de inmediato.',
 (103,2):'Corta la gelatina en dados regulares y divide el anko en dos porciones para equilibrar las capas de ambos vasos.',
 (105,6):'Aplana una porción de nerikiri, coloca el anko en el centro y sella bien la unión por la parte inferior.',
 (107,2):'Si el anko está muy firme, ablándalo con una cucharadita de agua caliente y remueve hasta que quede cremoso, pero no líquido.',
 (117,2):'Prepara la salsa nanban llevando a hervor suave la salsa de soja, el vinagre de arroz, el mirin y el azúcar. Después deja que se temple.',
 (118,3):'Cuece los udon en una olla aparte siguiendo las indicaciones del envase y escúrrelos muy bien.',
 (118,4):'Enjuaga brevemente los udon solo si lo indica la variedad utilizada; después pásalos a cuencos precalentados.',
 (118,5):'Vierte el caldo hirviendo sobre los udon y separa suavemente los fideos con los palillos.',
 (130,6):'Cuece los udon en agua aparte, escúrrelos bien y repártelos entre los cuencos.',
 (130,7):'Vierte el caldo hirviendo sobre los udon y añade cebolleta.',
 (131,2):'Cuece los udon en abundante agua hirviendo hasta que queden elásticos, pero aún firmes.',
 (137,1):'Suelta los udon en agua hirviendo durante aproximadamente 1 minuto; escúrrelos y sepáralos con cuidado para que no se rompan.',
 (137,5):'Añade los udon y saltéalos a fuego fuerte hasta que estén bien calientes.',
 (137,7):'Sirve de inmediato con katsuobushi, sésamo o cebolleta, sin dejar los udon reposando en la sartén.',
 (142,1):'Divide el anko en seis bolitas iguales y mantenlas tapadas. Espolvorea la superficie de trabajo con almidón de maíz o fécula.',
 (154,6):'Cuece los udon en una olla aparte durante el tiempo indicado, escúrrelos bien y repártelos entre los cuencos.',
 },
 'fr':{
 (53,2):'Porte à léger frémissement pendant 2 minutes pour dissoudre le sucre et permettre à l’alcool du mirin de s’évaporer.',
 (56,6):'Dépose quelques cuillerées d’œufs de saumon ikura au centre, puis parsème de graines de sésame grillées et de fines lanières de nori.',
 (62,3):'Dans un bol, délaye la pâte de sésame noir avec le miso, le mirin et la sauce soja, en versant peu à peu une louche de dashi chaud jusqu’à obtenir un mélange fluide.',
 (76,9):'Garnis chaque cube d’un petit monticule de daikon râpé, d’une pincée de gingembre, de cébette et de flocons de katsuobushi.',
 (80,8):'Sers avec une généreuse portion de daikon frais râpé, légèrement arrosé de sauce soja, et un quartier de citron.',
 (90,1):'Prépare le tare : chauffe doucement la sauce soja, le mirin, le gingembre et l’ail dans une petite casserole pendant 3 minutes, puis filtre.',
 (90,4):'Verse le tare au fond de deux bols à ramen préchauffés, ajoute le bouillon brûlant et mélange pour répartir l’assaisonnement.',
 (93,2):'Dans une petite poêle à donburi, porte le dashi, la sauce soja, le mirin et le sucre à léger frémissement. Ajoute l’oignon et laisse cuire 3 à 4 minutes, jusqu’à ce qu’il soit translucide.',
 (100,1):'Émince l’oignon et coupe la viande en fines bouchées ; porte séparément une casserole d’eau à ébullition pour les nouilles udon.',
 (100,3):'Ajoute le dashi, la sauce soja et le mirin, puis laisse frémir 3 à 4 minutes.',
 (100,5):'Poursuis la cuisson 5 minutes en remuant : la sauce doit napper la cuillère tout en restant assez fluide pour enrober les nouilles udon.',
 (100,6):'Fais cuire les nouilles udon dans l’eau prévue à part, égoutte-les soigneusement et répartis-les dans les bols.',
 (100,7):'Verse le curry brûlant sur les nouilles udon, ajoute de la cébette et sers sans attendre.',
 (108,8):'Ajoute les nouilles, puis complète aussitôt avec le chashu, une demi-portion d’ajitama, des pousses, de la cébette, du nori et quelques gouttes de mayu.',
 (110,3):'Prépare le bouillon avec le dashi, l’ail, le piment et le miso ou la sauce soja. Assaisonne-le suffisamment, car le chou et le tofu en atténueront le goût.',
 (116,4):'Ajoute le sucre et le mirin, puis remue jusqu’à dissolution du sucre, lorsque les légumes commencent à se glacer.',
 (117,1):'Coupe les hauts de cuisse de poulet en morceaux réguliers et assaisonne-les avec la sauce soja, le saké, le gingembre et l’ail. Laisse mariner au moins 20 minutes.',
 (117,2):'Porte doucement à frémissement la sauce soja, le vinaigre de riz, le mirin et le sucre pour préparer la sauce nanban, puis laisse tiédir.',
 (123,2):'Émince le poulet en fines lanières et porte le dashi à léger frémissement avec la sauce soja et le mirin.',
 (130,2):'Porte le dashi, la sauce soja claire et le mirin à léger frémissement. Garde le bouillon chaud sans le laisser réduire excessivement.',
 (130,6):'Fais cuire les nouilles udon dans une casserole d’eau séparée, égoutte-les et répartis-les dans les bols.',
 (130,7):'Verse le bouillon brûlant sur les nouilles udon et ajoute de la cébette.',
 (131,2):'Fais cuire les nouilles udon dans une grande quantité d’eau bouillante jusqu’à ce qu’elles soient souples, mais encore fermes.',
 (131,4):'Égoutte soigneusement les nouilles udon et secoue-les : l’eau résiduelle diluerait le mentsuyu.',
 (131,5):'Répartis-les dans les bols avec le concombre, l’œuf, la cébette et les lanières de nori.',
 (135,5):'Porte le dashi, la sauce soja et le mirin à léger frémissement pendant 1 à 2 minutes.',
 (137,1):'Détache délicatement les nouilles udon dans l’eau bouillante pendant environ 1 minute, égoutte-les et sépare-les sans les casser.',
 (137,5):'Ajoute les nouilles udon et fais-les sauter à feu vif jusqu’à ce qu’elles soient bien chaudes.',
 (137,7):'Sers aussitôt avec du katsuobushi, du sésame ou de la cébette, sans laisser les nouilles udon attendre dans la poêle.',
 (138,1):'Coupe la poitrine de porc, le daikon et la carotte en morceaux fins, puis taille le tofu en cubes.',
 (148,9):'Sers avec la mayonnaise Kewpie à part et une pincée de shichimi togarashi.',
 (154,5):'Assaisonne avec la sauce soja et le mirin ; goûte le bouillon avant d’ajouter davantage de sel.',
 (154,6):'Fais cuire les nouilles udon dans une casserole séparée pendant le temps indiqué, égoutte-les et répartis-les dans les bols.',
 (155,1):'Fais cuire les rondelles de daikon dans l’eau bouillante pendant 10 minutes pour les attendrir et en atténuer l’amertume, puis égoutte.',
 (155,3):'Dans une grande casserole, réunis le dashi, le saké, le sucre, le mirin et le gingembre.',
 },
 'de':{
 (53,2):'Die Mischung 2 Minuten leicht köcheln lassen, bis sich der Zucker gelöst hat und der Alkohol aus dem Mirin verdampfen kann.',
 (55,3):'Eine Kelle heiße Brühe abnehmen und die Misopaste darin mit einem Schneebesen oder Essstäbchen auflösen. Zurück in den Topf geben und gut verrühren.',
 (71,5):'Die Sesampaste, Sojasauce und das scharfe Rayu-Öl gleichmäßig auf zwei vorgewärmte Ramen-Schalen verteilen.',
 (71,9):'Die Ramen-Nudeln 2 Minuten in kochendem Wasser garen, gründlich abgießen und in die Brühe geben.',
 (74,7):'Die Kinchaku-Säckchen in den letzten 10 Minuten zugeben, damit das Mochi darin weich wird, ohne dass die Säckchen aufreißen.',
 (75,7):'Die Udon-Nudeln 2 Minuten in kochendem Wasser garen, abgießen und auf zwei große Schüsseln verteilen.',
 (75,8):'Die heiße, dickflüssige Currybrühe über die Udon-Nudeln gießen.',
 (90,4):'Das Tare auf dem Boden von zwei vorgewärmten Ramen-Schalen verteilen. Die kochend heiße Brühe zugeben und verrühren, damit sich die Würze gleichmäßig verteilt.',
 (100,1):'Die Zwiebel in Scheiben und das Fleisch in dünne, mundgerechte Stücke schneiden. Für die Udon-Nudeln in einem separaten Topf Wasser zum Kochen bringen.',
 (100,5):'Weitere 5 Minuten unter Rühren garen: Die Brühe soll den Löffel leicht überziehen, aber flüssig genug bleiben, um die Udon-Nudeln zu umhüllen.',
 (100,6):'Die Udon-Nudeln im separaten Wasser garen, gründlich abgießen und auf die Schüsseln verteilen.',
 (102,7):'Mit einer Bambusmatte formen, in dicke Scheiben schneiden und mit geriebenem Daikon und Sojasauce servieren.',
 (105,5):'Aus dem Anko vier Kugeln von jeweils etwa 15 g formen und abgedeckt aufbewahren, damit sie nicht austrocknen.',
 (118,3):'Die Udon-Nudeln nach Packungsangabe in einem separaten Topf garen und anschließend gründlich abgießen.',
 (118,4):'Die Udon-Nudeln nur dann kurz abspülen, wenn dies für die verwendete Sorte vorgesehen ist; anschließend in vorgewärmte Schüsseln geben.',
 (118,5):'Die kochend heiße Brühe über die Udon-Nudeln gießen und die Nudelstränge behutsam mit Essstäbchen trennen.',
 (123,2):'Das Hähnchen in feine Streifen schneiden. Das Dashi mit Sojasauce und Mirin leicht zum Köcheln bringen.',
 (130,6):'Die Udon-Nudeln in einem separaten Topf garen, gründlich abgießen und auf die Schüsseln verteilen.',
 (130,7):'Die kochend heiße Brühe über die Udon-Nudeln gießen und Frühlingszwiebel darüberstreuen.',
 (131,2):'Die Udon-Nudeln in reichlich kochendem Wasser garen, bis sie elastisch, aber noch bissfest sind.',
 (135,7):'Lauwarm oder bei Zimmertemperatur mit geriebenem Daikon und frischem Ingwer servieren.',
 (136,6):'Eine zweite Schicht Glasur auftragen und die Auberginen 1 bis 2 Minuten unter den Backofengrill stellen. Dabei ständig kontrollieren, da die zuckerhaltige Misoglasur leicht anbrennt.',
 (137,1):'Die Udon-Nudeln etwa 1 Minute in kochendem Wasser lockern, abgießen und vorsichtig voneinander trennen, ohne sie zu zerreißen.',
 (137,5):'Die Udon-Nudeln zugeben und bei starker Hitze unter Rühren braten, bis sie durchgehend heiß sind.',
 (137,7):'Sofort mit Katsuobushi, Sesam oder Frühlingszwiebel servieren und die Udon-Nudeln nicht in der Pfanne stehen lassen.',
 (154,6):'Die Udon-Nudeln im separaten Topf für die angegebene Zeit garen, gründlich abgießen und auf die Schüsseln verteilen.',
 (157,7):'Das Fruchtfleisch der Auberginen großzügig mit der Misoglasur bestreichen.',
 },
 'pt':{
 (92,2):'Corte o bacon, a cenoura e a cebolinha em pedaços finos. Deixe o molho de soja, o dashi granulado, a pimenta e o óleo de sésamo ao lado do wok.',
 (95,6):'Junte o frango, o menma e meio ovo, deixando uma parte dos noodles à vista.',
 (100,1):'Corte a cebola em rodelas e a carne em pedaços finos. Leve uma panela de água separada à fervura para cozinhar os noodles udon.',
 (100,3):'Adicione o dashi, o molho de soja e o mirin e deixe fervilhar suavemente durante 3 a 4 minutos.',
 (100,6):'Coza os udon na água separada, escorra-os bem e distribua-os pelas tigelas.',
 (102,1):'Numa tigela, bata delicadamente os ovos com o dashi, o mirin, o molho de soja e o sal, sem os bater em castelo.',
 (102,7):'Molde com uma esteira de bambu, corte em fatias grossas e sirva com daikon ralado e molho de soja.',
 (105,6):'Achate uma porção de nerikiri, coloque o anko no centro e feche bem a junção na parte inferior.',
 (110,3):'Prepare o caldo com dashi, alho, malagueta e miso ou molho de soja. Tempere bem, pois a couve e o tofu vão suavizar o sabor.',
 (117,1):'Corte as sobrecoxas de frango em pedaços regulares e tempere com molho de soja, saquê, gengibre e alho. Deixe marinar durante pelo menos 20 minutos.',
 (119,7):'Tempere com saquê e molho de soja, prove e sirva quente. Evite o katsuobushi se quiser manter o prato estritamente vegetariano.',
 (135,7):'Sirva morno ou à temperatura ambiente com daikon ralado e gengibre fresco.',
 (137,1):'Solte delicadamente os udon em água a ferver durante cerca de 1 minuto, escorra e separe os fios sem os partir.',
 (137,5):'Junte os udon e salteie em lume forte até ficarem bem quentes.',
 },
}

# Extra independently witnessed semantic failures outside the original 185
# Japanese-term triage flags (e.g. "jump" for sautée, "listen" for drain).
EXTRA_STEPS={
 'en':{
 (72,9):'Stir-fry vigorously over high heat for 2 minutes, until the sauce caramelizes slightly.',
 (78,9):'Return the shrimp to the pan with the chopped spring onion and toss for 1 minute to coat them completely in the glossy, spicy sauce.',
 (89,2):'Cook in a rice cooker or a saucepan with 280 ml of water; if using a saucepan, simmer for 15 minutes from the boil.',
 (92,5):'Add the sprouts and spring onion and stir-fry vigorously for about 2 minutes. The sprouts should soften slightly but remain crisp.',
 (120,2):'Heat a large frying pan, brown the pork and add the carrot, cabbage and any sprouts. Stir-fry until the vegetables begin to soften.',
 (137,3):'Heat the sesame oil over high heat and stir-fry the onion and carrot for 1–2 minutes.',
 (143,1):'Line the buttered tartlet moulds with shortcrust pastry, trim the edges and prick the bases with a fork.',
 },
 'es':{
 (61,9):'Añade los fideos escurridos y colócalos en el centro.',
 (68,6):'Disuelve la levadura en el agua y añádela a los huevos.',
 (69,4):'Incorpora los huevos de uno en uno y mezcla bien después de cada adición.',
 (72,9):'Saltea y remueve enérgicamente a fuego fuerte durante 2 minutos, hasta que la salsa se caramelice ligeramente.',
 (73,7):'Añade los huevos cocidos y pelados durante los últimos 15 minutos de cocción para que absorban el sabor del caldo oscuro.',
 (89,2):'Cuece el arroz en una arrocera o en una olla con 280 ml de agua durante 15 minutos desde que empiece a hervir.',
 (91,2):'Corta en láminas los shiitake rehidratados, la zanahoria y el aburaage; corta el pollo en dados uniformes de aproximadamente 1,5 cm.',
 (93,6):'Desliza con cuidado el contenido de la sartén pequeña sobre el arroz caliente sin romper la chuleta.',
 (96,7):'Añade las almejas abiertas al final, ajusta la pimienta negra y sirve caliente con picatostes.',
 (120,2):'Calienta una sartén grande, dora el cerdo y añade la zanahoria, la col y los brotes, si los utilizas. Saltea hasta que las verduras empiecen a ablandarse.',
 (129,3):'Añade las lonchas de cerdo y cuécelas durante 3–4 minutos, hasta que estén tiernas.',
 (139,5):'Añade la salsa de soja, vuelve a tapar y cocina a fuego suave otros 8–10 minutos, hasta que la calabaza esté tierna y la salsa se reduzca.',
 },
 'fr':{
 (71,9):'Fais cuire les nouilles ramen 2 minutes dans l’eau bouillante, égoutte-les soigneusement et dépose-les dans le bouillon.',
 (83,4):'Égoutte les nouilles et rince-les immédiatement sous un filet d’eau très froide, avec des glaçons, en les frottant doucement pour éliminer l’amidon de surface.',
 (85,7):'Égoutte les cubes de warabi mochi, répartis-les sur les assiettes et saupoudre généreusement de kinako et de sirop de kuromitsu.',
 (89,2):'Fais cuire le riz au cuiseur à riz ou dans une casserole avec 280 ml d’eau pendant 15 minutes à partir de l’ébullition.',
 (91,3):'Verse le riz dans une casserole ou un cuiseur à riz et ajoute le dashi, la sauce soja, le mirin et le saké, en respectant le niveau de liquide indiqué pour le riz.',
 (99,5):'Plonge-les aussitôt dans de l’eau glacée pour stopper la cuisson, puis égoutte-les et sèche-les délicatement.',
 (108,5):'Filtre le bouillon, remets-le sur le feu et ajuste sa concentration. Prépare séparément le tare, le chashu, les œufs, les pousses, la cébette et le nori.',
 (108,6):'Porte une casserole d’eau séparée à ébullition et fais cuire les nouilles fraîches pendant le temps indiqué, généralement 1 à 2 minutes. Égoutte-les soigneusement.',
 (108,7):'Dépose le tare au fond des bols préchauffés, verse le bouillon tonkotsu brûlant et mélange.',
 },
 'de':{
 (89,2):'Den Reis im Reiskocher oder in einem Topf mit 280 ml Wasser ab dem Aufkochen 15 Minuten garen.',
 },
 'pt':{
 (89,2):'Coza o arroz numa panela elétrica de arroz ou numa panela com 280 ml de água durante 15 minutos a partir do início da fervura.',
 (133,1):'Enrole a sobrecoxa de frango com a pele virada para fora e ate-a firmemente com fio de cozinha.',
 (152,5):'Leve ao forno durante cerca de 10 a 12 minutos, até o queijo derreter e alourar e a clara do ovo ficar firme.',
 (158,8):'Retire do forno e vire imediatamente a forma sobre uma garrafa ou sobre o suporte apropriado. Deixe arrefecer completamente antes de desenformar.',
 (161,4):'Deite uma concha de massa na frigideira, espalhe-a numa camada fina e cozinhe 1 minuto de cada lado.',
 },
}
EXTRA_STEPS['de'].update({
 (55,2):'Die Brühe leicht köcheln lassen.',
 (67,1):'Dashi-Brühe, Mehl und Worcestershiresauce in einem Krug mit einem Schneebesen kräftig verrühren.',
 (71,8):'Die heiße Brühe in die Schüsseln geben und die Sesampaste am Boden mit einem Schneebesen gründlich darin auflösen.',
 (75,6):'Den Herd ausschalten, die zerbröselten Curry-Roux-Würfel zugeben und mit dem Schneebesen rühren, bis sie sich vollständig aufgelöst haben und eine dicke, samtige Brühe entstanden ist.',
 (79,3):'Die warme Milch unter ständigem Rühren mit dem Schneebesen langsam zugießen, bis eine sehr dicke, glatte Béchamelcreme entstanden ist.',
 (87,1):'Kastaniencreme, weiche Butter und Rum in einer Schüssel mit dem Handrührgerät cremig und klümpchenfrei aufschlagen.',
 (90,2):'Die Hühner- oder Dashi-Brühe bis zum leichten Köcheln erhitzen und warm halten, ohne sie zu stark einreduzieren zu lassen.',
 (91,5):'Kurz aufkochen lassen, abdecken, die Hitze auf die niedrigste Stufe reduzieren und etwa 15 Minuten garen, ohne den Deckel anzuheben. Im Reiskocher das normale Programm verwenden.',
 (95,1):'Hähnchen, Menma, wachsweiches Ei und Yuzu-Schale vorbereiten. Einen separaten Topf Wasser für die Nudeln zum Kochen bringen.',
 (109,2):'Die schwarze Sesampaste mit einem Schneebesen gründlich einrühren, bis eine glatte, klümpchenfreie Mischung entsteht.',
 (119,5):'Das Kombu-Dashi zugießen, leicht aufkochen lassen und den entstehenden Schaum abschöpfen.',
 (138,4):'Das Dashi zugießen, leicht aufkochen lassen und gegebenenfalls den Schaum abschöpfen.',
 (138,7):'Den Herd ausschalten, das Miso in einer Kelle Brühe auflösen und in die Suppe rühren, ohne sie erneut aufzukochen.',
 (140,2):'Zucker und Eier verrühren, dann lauwarme Milch und geschmolzene Butter mit dem Schneebesen einarbeiten, bis ein dünnflüssiger, klümpchenfreier Teig entsteht.',
 (141,3):'Bei schwacher Hitze mit dem Schneebesen rühren, bis die Masse gleichmäßig ist und sich der Zucker gelöst hat, ohne sie aufkochen zu lassen.',
 (147,5):'Die restliche Hühnerbrühe erhitzen und die schwarze Sesambasis mit einem Schneebesen kräftig einrühren, bis sich der Sesam gleichmäßig verteilt.',
 (154,4):'Das Kombu-Dashi zugießen, leicht aufkochen lassen und zugedeckt etwa 8–10 Minuten garen, bis das Wurzelgemüse weich ist.',
 (158,3):'Das Mehl zusammen mit dem Matcha-Pulver sieben und mit einem Schneebesen unter die Eigelbmasse rühren.',
 (162,5):'Nach 1 Stunde, sobald der Sorbetansatz am Rand fest wird, ausschließlich pasteurisiertes Eiweiß steif schlagen und vorsichtig unterheben. Kein rohes, unpasteurisiertes Eiweiß verwenden.',
})
EXTRA_STEPS['pt'].update({
 (55,3):'Retire uma concha de caldo quente, dissolva nela a pasta de miso com um batedor de varas ou pauzinhos e volte a juntar tudo à panela, mexendo bem.',
 (61,6):'Numa frigideira à parte, salteie os rebentos de soja com um fio de óleo de sésamo durante 2 minutos, mantendo-os estaladiços.',
 (62,3):'Numa tigela, dilua a pasta de sésamo preto com o miso, o mirin e o molho de soja, juntando aos poucos uma concha de dashi quente até obter uma mistura fluida e homogénea.',
 (78,4):'Aqueça 2 colheres de sopa de óleo no wok e salteie os camarões durante 1 a 2 minutos, até ficarem rosados.',
 (78,9):'Volte a colocar os camarões na frigideira com a cebolinha picada e salteie durante 1 minuto para os envolver completamente no molho brilhante e picante.',
 (111,5):'Retire uma concha do líquido de cozedura, dissolva nela o miso e volte a deitá-lo na frigideira sem deixar ferver intensamente.',
 (137,3):'Aqueça o óleo de sésamo em lume forte e salteie primeiro a cebola e a cenoura durante 1 a 2 minutos.',
})
EXTRA_STEPS['en'].update({
 (67,5):'Using two small spatulas, shape the cabbage on the hot griddle into a wide ring or volcano, leaving a hollow in the centre.',
 (154,3):'Add the daikon, carrot and shiitake and stir-fry for about 3 minutes.',
 (157,8):'Place the aubergines under the oven grill at 220°C for 3–4 minutes, until the glaze bubbles and caramelizes slightly.',
})
EXTRA_STEPS['fr'][(111,1)]='Incise légèrement la peau des filets de maquereau, verse de l’eau bouillante dessus pendant quelques secondes, puis égoutte et sèche-les pour atténuer leur odeur prononcée.'

for _language,_steps in EXTRA_STEPS.items():
    STEP_EDITS[_language].update(_steps)

ING_EDITS={
 'en':{(95,9):'bamboo shoots (menma)',(111,7):'water or dashi',(131,6):'nori cut into thin strips'},
 'es':{(131,6):'nori en tiras finas'},
 'fr':{(110,6):'miso claro o salsa de soja', # corrected to French below
       (124,5):'algue nori en lanières',(130,3):'farine pour tempura (ou farine de blé 00 et eau glacée)',(131,6):'nori en fines lanières',(136,2):'miso rouge ou blanc',(138,6):'miso rouge ou mélange de miso'},
 'de':{(69,8):'abgeriebene Yuzu-Schale',(83,10):'Nori-Algenblätter',(136,2):'rotes oder weißes Miso',(138,6):'rotes oder gemischtes Miso'},
 'pt':{(90,2):'caldo dashi ou caldo de frango leve',(95,9):'rebentos de bambu (menma)',(111,7):'água ou dashi',(131,6):'nori em tiras'},
}
ING_EDITS['fr'][(110,6)]='miso clair ou sauce soja'

# Constrained textual repairs for Japanese culinary names mistranslated as common nouns.
# These apply only when the Italian field uses the corresponding term.
TOKENS={
 'en':{'dashi':[(r'\bdashes\b','dashi'),(r'\bdash\b','dashi')],
       'udon':[(r'\budons\b','udon')], 'daikon':[(r'\bdaikons\b','daikon')],
       'menma':[(r'\bmenme\b','menma'),(r'\bmentha\b','menma')],
       'nori':[(r'\bNordes\b','nori')]},
 'es':{'udon':[(r'\budons?\b','udon'),(r'\budones\b','udon')],
       'anko':[(r'\blonko\b','anko'),(r'\banz(uelo|uelo)\b','anko'),(r'\bL\.A\.nko\b','anko')],
       'mirin':[(r'\bmirín\b','mirin')],
       'nori':[(r'\bNores\b','nori')]},
 'fr':{'udon':[(r'\budons\b','udon')],
       'mirin':[(r'\bmyrin(?:ette|e|s)?\b','mirin')],
       'dashi':[(r'\bdashis?\b','dashi'),(r'\bdashs\b','dashi')],
       'daikon':[(r'\b(?:dakon|dikon|dakons|dikons)\b','daikon')],
       'miso':[(r'\bmyso\b','miso'),(r'\bmyse\b','miso')],
       'nori':[(r'\bNoirs?\b','nori'),(r'\bnor\b','nori')],
       'togarashi':[(r'\bTogarachi\b','togarashi')],
       'sake':[(r'\bsakés\b','saké')]},
 'de':{'udon':[(r'\bUdons\b','Udon')],
       'daikon':[(r'\bDaikons\b','Daikon')],
       'miso':[(r'\bMist\b','Miso')],
       'yuzu':[(r'\bJuzu\b','Yuzu')],
       'nori':[(r'\bNördlich\b','Nori')]},
 'pt':{'dashi':[(r'\btraços?\b','dashi')],
       'udon':[(r'\budons\b','udon')],
       'daikon':[(r'\bdaikons\b','daikon')],
       'menma':[(r'\bmenme\b','menma'),(r'\bmentha\b','menma')],
       'nori':[(r'\bNordes\b','nori')]},
}

def apply(source:dict, pack:dict)->dict:
    if digest(source)!=SOURCE_SHA or pack.get('sourceBaselineSha256')!=SOURCE_SHA:
        raise ValueError('Frozen source fingerprint mismatch; copy edits must be manually rechecked')
    locale=pack['locale']
    changes=[]
    source_by_id={r['id']:r for r in source['recipes']}
    for dst in pack['recipes']:
        src=source_by_id[dst['id']];n=int(dst['id'][-3:])
        for kind,records,key in (('step',dst['steps'],'instruction'),('ingredient',dst['ingredients'],'name')):
            for i,item in enumerate(records,1):
                source_item=(src['steps'] if kind=='step' else src['ingredients'])[i-1]
                source_text=source_item[key]
                old=item[key]
                new=old
                for term,replacements in TOKENS.get(locale,{}).items():
                    if re.search(r'\b'+re.escape(term)+r'\b',source_text,re.I):
                        for pattern,repl in replacements:
                            new=re.sub(pattern,repl,new,flags=re.I)
                replacement=(STEP_EDITS if kind=='step' else ING_EDITS)[locale].get((n,i))
                if replacement is not None:
                    if not replacement.strip():raise ValueError('Empty editorial replacement')
                    new=replacement
                if new!=old:
                    item[key]=new;changes.append({'recipe':dst['id'],'field':f'{kind}_{i}','from':old,'to':new})
    if inspect(source,pack):
        raise ValueError('Structural validation regression: '+str(inspect(source,pack)[:6]))
    return {'locale':locale,'edits':changes,'editCount':len(changes)}

def main():
    import argparse
    ap=argparse.ArgumentParser(description='Apply source-bound F3L editorial corrections to non-publishable candidate packs')
    ap.add_argument('--source',default='authoring/f3k_it_hardening_51_162.json')
    ap.add_argument('--input-dir',default='authoring/f3l_review_drafts')
    ap.add_argument('--output-dir',default='build/f3l/source_bound_review')
    ap.add_argument('--ledger',default='build/f3l/source_bound_review/edit_ledger.json')
    args=ap.parse_args()
    src=json.loads(Path(args.source).read_text(encoding='utf-8'))
    output=Path(args.output_dir);output.mkdir(parents=True,exist_ok=True)
    reports=[]
    for l in ('en','es','fr','de','pt'):
        source_pack=Path(args.input_dir)/f'f3l_{l}_51_162_review_draft.json'
        pack=json.loads(source_pack.read_text(encoding='utf-8'))
        if pack.get('reviewStatus')!='machine_draft_not_publishable':
            raise ValueError('Not an isolated review-draft pack')
        log=apply(src,pack)
        pack.setdefault('editorialStaging',{})['expandedReviewFieldEdits']=log['editCount']
        pack['editorialStaging']['noAutomaticPublication']=True
        (output/source_pack.name).write_text(json.dumps(pack,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        reports.append(log)
    ledger=Path(args.ledger);ledger.parent.mkdir(parents=True,exist_ok=True)
    ledger.write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({x['locale']:x['editCount'] for x in reports}))

if __name__=='__main__':main()
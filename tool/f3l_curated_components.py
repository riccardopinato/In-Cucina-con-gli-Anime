"""AI-assisted culinary copy-edits for 10 reusable components in five locales.

Six components contain full ingredients and cooking instructions; four are
recipeRef-only pointers. These are NOT externally certified or cooking-tested.
"""
from f3l_translation_gate import digest
SOURCE_SHA256='d18d492b0db2148aed213610ffd1ff98bcff925a66cf4444a8a4da9b51576227'
COPY={
'en':{
 'component_chashu':{
  'title':'Chashu — braised pork belly for ramen',
  'ingredients':['pork belly in one piece','water','soy sauce','cooking sake','mirin','sugar','fresh ginger, sliced','spring onions'],
  'steps':[
   'Roll the pork belly and tie it with kitchen twine if you want evenly shaped slices; otherwise leave it flat.',
   'Brown the pork on all sides in a casserole until golden, then pour off the excess rendered fat.',
   'Add the water, soy sauce, sake, mirin, sugar, ginger and spring onions; bring to a gentle simmer.',
   'Cover partially and simmer for 75–90 minutes, turning the pork every 20 minutes. Add a little hot water if the cooking liquid reduces too much.',
   'Turn off the heat when the pork is tender but still firm enough to slice; let it cool slightly in the braising liquid.',
   'Chill for at least 1 hour to firm up the meat, then slice across the grain and briefly glaze the slices with some braising liquid before serving.'
  ]},
 'component_ajitama':{
  'title':'Ajitama — marinated ramen eggs',
  'ingredients':['eggs','soy sauce','mirin','water'],
  'steps':[
   'Bring a small saucepan of water to a boil and lower the eggs in gently.',
   'Cook for 6 minutes and 30 seconds for jammy yolks, then transfer the eggs immediately to ice water.',
   'Peel the eggs once they are completely cool.',
   'Mix the soy sauce, mirin and water. Pour the marinade into a small container and submerge the peeled eggs.',
   'Marinate in the refrigerator for at least 4 hours but no longer than 24 hours, turning the eggs halfway through for even color.'
  ]},
 'component_dashi':{
  'title':'Basic kombu and katsuobushi dashi',
  'ingredients':['water','kombu seaweed','katsuobushi (dried bonito flakes)'],
  'steps':[
   'Gently wipe the kombu with a barely damp cloth, without removing its surface coating.',
   'Put the kombu and water in a pot and let stand for 20–30 minutes.',
   'Heat slowly and remove the kombu just before the water begins to boil.',
   'Turn off the heat, add the katsuobushi and steep for 2 minutes without stirring.',
   'Strain through a fine-mesh sieve without squeezing the flakes. Use the dashi immediately or cool it rapidly.'
  ]},
 'component_tonkatsu':{
  'title':'Tonkatsu — breaded pork cutlets',
  'ingredients':['pork loin slices about 1.5 cm thick','fine salt','pepper','plain flour (Italian type 00)','egg','panko breadcrumbs','neutral oil for deep-frying'],
  'steps':[
   'Score the fatty edge of each pork slice in several places to prevent curling, then pound lightly to an even thickness.',
   'Season with salt and pepper, then coat each slice in flour and shake off the excess.',
   'Dip into the beaten egg and coat with panko, taking care not to press the crumbs too firmly.',
   'Heat the oil to 170–175°C and fry one cutlet at a time until the coating is golden and the pork is cooked through but still juicy.',
   'Drain on a wire rack for 2–3 minutes; slice only when ready to assemble the dish.'
  ]},
 'component_chocolate_custard':{
  'title':'Chocolate pastry cream for Choco Cornet',
  'ingredients':['whole milk','egg yolks','sugar','cornstarch','dark chocolate (55–65% cocoa)'],
  'steps':[
   'Heat the milk until just below boiling point.',
   'In a bowl, whisk the egg yolks with the sugar and cornstarch until smooth.',
   'Pour half the hot milk over the yolk mixture while whisking, then return everything to the saucepan.',
   'Cook over medium-low heat, stirring constantly, until the cream thickens and begins to simmer.',
   'Remove from the heat, add the chopped chocolate and stir until fully melted.',
   'Cover with cling film touching the surface and chill completely in the refrigerator before filling the cornet buns.'
  ]},
 'component_brioche_cornet':{
  'title':'Brioche dough for Choco Cornet',
  'ingredients':['strong bread flour','lukewarm milk','instant dry yeast','sugar','salt','egg','softened butter'],
  'steps':[
   'Mix the flour, sugar and yeast; add the milk and egg, then knead until no dry flour remains.',
   'Add the salt and softened butter a little at a time and continue kneading until the dough is smooth, elastic and pulls away from the work surface.',
   'Cover and let rise for 60–90 minutes, until almost doubled in size.',
   'Gently deflate, divide into 6 pieces and let the dough relax for 10 minutes before rolling each piece into a rope.'
  ]},
 'component_karaage_ref':{'title':'Full karaage recipe'},
 'component_japanese_curry_ref':{'title':'Full Japanese curry recipe'},
 'component_kakuni_ref':{'title':'Full kakuni recipe'},
 'component_yakisoba_ref':{'title':'Full yakisoba recipe'},
},
'es':{
 'component_chashu':{
  'title':'Chashu — panceta de cerdo braseada para ramen',
  'ingredients':['panceta de cerdo en una sola pieza','agua','salsa de soja','sake para cocinar','mirin','azúcar','jengibre fresco en rodajas','cebolletas'],
  'steps':[
   'Enrolla la panceta y átala con hilo de cocina si quieres obtener rodajas uniformes; de lo contrario, déjala extendida.',
   'Dora el cerdo por todos lados en una cazuela hasta que la superficie tome color; retira el exceso de grasa.',
   'Añade el agua, la salsa de soja, el sake, el mirin, el azúcar, el jengibre y las cebolletas. Lleva a un hervor suave.',
   'Tapa parcialmente y deja cocer a fuego lento durante 75–90 minutos, girando la pieza cada 20 minutos. Añade un poco de agua caliente si el líquido se reduce demasiado.',
   'Apaga el fuego cuando la carne esté tierna pero todavía se pueda cortar en lonchas; deja que se temple en su propio líquido de cocción.',
   'Enfría al menos 1 hora para que la carne gane firmeza. Córtala a contrapelo y glasea brevemente las lonchas con un poco del líquido de cocción antes de servir.'
  ]},
 'component_ajitama':{
  'title':'Ajitama — huevos marinados para ramen',
  'ingredients':['huevos','salsa de soja','mirin','agua'],
  'steps':[
   'Pon a hervir agua en un cazo e introduce los huevos con cuidado.',
   'Cuécelos durante 6 minutos y 30 segundos para obtener yemas cremosas y pásalos inmediatamente a un baño de agua con hielo.',
   'Pela los huevos cuando estén completamente fríos.',
   'Mezcla la salsa de soja, el mirin y el agua. Vierte la marinada en un recipiente pequeño y sumerge los huevos pelados.',
   'Déjalos marinar en el frigorífico al menos 4 horas y como máximo 24 horas; dales la vuelta a mitad del tiempo para que se tiñan de forma uniforme.'
  ]},
 'component_dashi':{
  'title':'Dashi básico de kombu y katsuobushi',
  'ingredients':['agua','alga kombu','katsuobushi (copos de bonito seco)'],
  'steps':[
   'Limpia el kombu suavemente con un paño apenas húmedo, sin retirar la capa de su superficie.',
   'Pon el kombu y el agua en una olla y deja reposar durante 20–30 minutos.',
   'Calienta lentamente y retira el kombu justo antes de que el agua comience a hervir.',
   'Apaga el fuego, añade el katsuobushi y deja infusionar 2 minutos sin remover.',
   'Cuela con un colador fino sin exprimir los copos. Utiliza el dashi enseguida o enfríalo rápidamente.'
  ]},
 'component_tonkatsu':{
  'title':'Tonkatsu — filetes de cerdo empanados',
  'ingredients':['lomo de cerdo en filetes de unos 1,5 cm de grosor','sal fina','pimienta','harina de trigo (tipo 00 italiano)','huevo','pan rallado japonés panko','aceite neutro para freír'],
  'steps':[
   'Haz varios cortes en el borde graso de cada filete de cerdo para evitar que se curve; aplánalo ligeramente hasta igualar el grosor.',
   'Sazona con sal y pimienta y pasa cada filete por harina, retirando el exceso.',
   'Pásalo por huevo batido y después por panko, sin presionar demasiado el empanado.',
   'Calienta el aceite a 170–175 °C y fríe un filete cada vez hasta que el empanado esté dorado y el cerdo bien cocinado, pero jugoso.',
   'Deja escurrir sobre una rejilla durante 2–3 minutos y corta los filetes solo cuando vayas a montar el plato.'
  ]},
 'component_chocolate_custard':{
  'title':'Crema pastelera de chocolate para Choco Cornet',
  'ingredients':['leche entera','yemas de huevo','azúcar','maicena','chocolate negro (55–65 % de cacao)'],
  'steps':[
   'Calienta la leche hasta que esté a punto de hervir.',
   'En un cuenco, bate las yemas con el azúcar y la maicena hasta lograr una mezcla lisa.',
   'Vierte la mitad de la leche caliente sobre las yemas sin dejar de remover y devuelve toda la mezcla al cazo.',
   'Cuece a fuego medio-bajo removiendo constantemente hasta que la crema espese y empiece a hervir suavemente.',
   'Retira del fuego, incorpora el chocolate picado y remueve hasta que se funda por completo.',
   'Cubre la superficie de la crema con film transparente en contacto directo y enfría por completo en el frigorífico antes de rellenar los cornet.'
  ]},
 'component_brioche_cornet':{
  'title':'Masa de brioche para Choco Cornet',
  'ingredients':['harina de fuerza','leche tibia','levadura seca de panadería','azúcar','sal','huevo','mantequilla blanda'],
  'steps':[
   'Mezcla la harina, el azúcar y la levadura; añade la leche y el huevo y amasa hasta integrar toda la harina.',
   'Incorpora la sal y la mantequilla blanda poco a poco y sigue amasando hasta obtener una masa lisa, elástica y que se despegue de la superficie.',
   'Tapa y deja fermentar de 60 a 90 minutos, hasta que casi duplique su volumen.',
   'Desgasifica suavemente, divide en 6 porciones y deja reposar 10 minutos antes de estirar cada porción en forma de cordón.'
  ]},
 'component_karaage_ref':{'title':'Receta completa de karaage'},
 'component_japanese_curry_ref':{'title':'Receta completa de curry japonés'},
 'component_kakuni_ref':{'title':'Receta completa de kakuni'},
 'component_yakisoba_ref':{'title':'Receta completa de yakisoba'},
},
'fr':{
 'component_chashu':{
  'title':'Chashu — poitrine de porc braisée pour ramen',
  'ingredients':['poitrine de porc en un seul morceau','eau','sauce soja','saké de cuisine','mirin','sucre','gingembre frais en tranches','oignons nouveaux'],
  'steps':[
   'Roulez la poitrine de porc et ficelez-la si vous souhaitez obtenir des tranches régulières ; sinon, laissez-la à plat.',
   'Faites dorer le porc sur toutes ses faces dans une cocotte, puis retirez l’excédent de graisse.',
   'Ajoutez l’eau, la sauce soja, le saké, le mirin, le sucre, le gingembre et les oignons nouveaux. Portez à léger frémissement.',
   'Couvrez partiellement et laissez mijoter 75 à 90 minutes, en retournant la viande toutes les 20 minutes. Ajoutez un peu d’eau chaude si le jus réduit trop.',
   'Coupez le feu lorsque la viande est tendre mais encore assez ferme pour être tranchée ; laissez-la tiédir dans son jus de cuisson.',
   'Réfrigérez au moins 1 heure pour raffermir la viande. Tranchez ensuite contre les fibres et laquez brièvement les tranches avec un peu de jus avant de servir.'
  ]},
 'component_ajitama':{
  'title':'Ajitama — œufs marinés pour ramen',
  'ingredients':['œufs','sauce soja','mirin','eau'],
  'steps':[
   'Portez une petite casserole d’eau à ébullition et plongez-y délicatement les œufs.',
   'Laissez cuire 6 minutes et 30 secondes pour obtenir des jaunes crémeux, puis transférez immédiatement les œufs dans de l’eau glacée.',
   'Écalez les œufs lorsqu’ils sont complètement froids.',
   'Mélangez la sauce soja, le mirin et l’eau. Versez la marinade dans un petit récipient et immergez les œufs écalés.',
   'Laissez mariner au réfrigérateur pendant 4 heures au minimum et 24 heures au maximum, en retournant les œufs à mi-parcours pour les colorer uniformément.'
  ]},
 'component_dashi':{
  'title':'Dashi de base au kombu et au katsuobushi',
  'ingredients':['eau','algue kombu','katsuobushi (copeaux de bonite séchée)'],
  'steps':[
   'Essuyez délicatement le kombu avec un linge à peine humide, sans retirer le dépôt qui recouvre sa surface.',
   'Mettez le kombu et l’eau dans une casserole et laissez reposer 20 à 30 minutes.',
   'Chauffez lentement et retirez le kombu juste avant l’ébullition.',
   'Éteignez le feu, ajoutez le katsuobushi et laissez infuser 2 minutes sans remuer.',
   'Filtrez à travers une passoire fine, sans presser les copeaux. Utilisez aussitôt le dashi ou refroidissez-le rapidement.'
  ]},
 'component_tonkatsu':{
  'title':'Tonkatsu — escalopes de porc panées',
  'ingredients':['tranches de longe de porc d’environ 1,5 cm d’épaisseur','sel fin','poivre','farine de blé (type italien 00)','œuf','chapelure japonaise panko','huile neutre pour la friture'],
  'steps':[
   'Incisez la bordure grasse des tranches de porc à plusieurs endroits pour éviter qu’elles ne se recroquevillent, puis aplatissez-les légèrement.',
   'Salez et poivrez, puis passez chaque tranche dans la farine en ôtant l’excédent.',
   'Trempez dans l’œuf battu et enrobez de panko sans trop presser la chapelure.',
   'Chauffez l’huile à 170–175 °C et faites frire une escalope à la fois, jusqu’à ce que la panure soit dorée et que le porc soit bien cuit, tout en restant juteux.',
   'Égouttez sur une grille pendant 2 à 3 minutes, puis tranchez seulement au moment du dressage.'
  ]},
 'component_chocolate_custard':{
  'title':'Crème pâtissière au chocolat pour Choco Cornet',
  'ingredients':['lait entier','jaunes d’œufs','sucre','fécule de maïs','chocolat noir à 55–65 % de cacao'],
  'steps':[
   'Faites chauffer le lait presque jusqu’à ébullition.',
   'Dans un saladier, fouettez les jaunes d’œufs avec le sucre et la fécule jusqu’à obtenir un mélange lisse.',
   'Versez la moitié du lait chaud sur les jaunes sans cesser de fouetter, puis reversez le tout dans la casserole.',
   'Faites cuire à feu moyen-doux en remuant constamment, jusqu’à ce que la crème épaississe et commence à frémir.',
   'Hors du feu, ajoutez le chocolat haché et mélangez jusqu’à ce qu’il soit entièrement fondu.',
   'Filmez au contact et laissez refroidir complètement au réfrigérateur avant de garnir les petits pains en cornet.'
  ]},
 'component_brioche_cornet':{
  'title':'Pâte briochée pour Choco Cornet',
  'ingredients':['farine de gruau ou farine riche en gluten','lait tiède','levure boulangère sèche','sucre','sel','œuf','beurre mou'],
  'steps':[
   'Mélangez la farine, le sucre et la levure ; ajoutez le lait et l’œuf, puis pétrissez jusqu’à incorporation complète de la farine.',
   'Ajoutez le sel et le beurre mou petit à petit, puis continuez à pétrir jusqu’à obtenir une pâte lisse, élastique et qui se détache du plan de travail.',
   'Couvrez et laissez lever 60 à 90 minutes, jusqu’à ce que la pâte ait presque doublé de volume.',
   'Dégazez doucement, divisez en 6 morceaux et laissez détendre la pâte pendant 10 minutes avant de façonner les boudins.'
  ]},
 'component_karaage_ref':{'title':'Recette complète du karaage'},
 'component_japanese_curry_ref':{'title':'Recette complète du curry japonais'},
 'component_kakuni_ref':{'title':'Recette complète du kakuni'},
 'component_yakisoba_ref':{'title':'Recette complète du yakisoba'},
},
'de':{
 'component_chashu':{
  'title':'Chashu – geschmorter Schweinebauch für Ramen',
  'ingredients':['Schweinebauch am Stück','Wasser','Sojasauce','Kochsake','Mirin','Zucker','frischer Ingwer in Scheiben','Frühlingszwiebeln'],
  'steps':[
   'Den Schweinebauch aufrollen und mit Küchengarn binden, wenn gleichmäßige Scheiben gewünscht sind; andernfalls flach lassen.',
   'Das Schweinefleisch in einem Schmortopf rundherum goldbraun anbraten, dann überschüssiges ausgelassenes Fett abgießen.',
   'Wasser, Sojasauce, Sake, Mirin, Zucker, Ingwer und Frühlingszwiebeln hinzufügen und alles sanft zum Köcheln bringen.',
   'Teilweise zugedeckt 75–90 Minuten leise köcheln lassen. Das Fleisch alle 20 Minuten wenden und etwas heißes Wasser nachgießen, falls die Flüssigkeit zu stark einkocht.',
   'Die Hitze ausschalten, sobald das Fleisch zart, aber noch schnittfest ist. Im Schmorsud etwas abkühlen lassen.',
   'Mindestens 1 Stunde kalt stellen, damit das Fleisch fester wird. Anschließend quer zur Faser aufschneiden und die Scheiben vor dem Servieren kurz mit etwas Schmorsud glasieren.'
  ]},
 'component_ajitama':{
  'title':'Ajitama – marinierte Ramen-Eier',
  'ingredients':['Eier','Sojasauce','Mirin','Wasser'],
  'steps':[
   'In einem kleinen Topf Wasser zum Kochen bringen und die Eier vorsichtig hineingleiten lassen.',
   'Für einen cremigen Eigelbkern 6 Minuten und 30 Sekunden kochen, dann die Eier sofort in Eiswasser legen.',
   'Die Eier vollständig abkühlen lassen und anschließend pellen.',
   'Sojasauce, Mirin und Wasser verrühren, die Marinade in ein kleines Gefäß füllen und die geschälten Eier vollständig hineingeben.',
   'Im Kühlschrank mindestens 4 Stunden, höchstens jedoch 24 Stunden marinieren. Nach der Hälfte der Zeit wenden, damit sie gleichmäßig Farbe annehmen.'
  ]},
 'component_dashi':{
  'title':'Grundrezept Dashi mit Kombu und Katsuobushi',
  'ingredients':['Wasser','Kombu-Alge','Katsuobushi (getrocknete Bonitoflocken)'],
  'steps':[
   'Den Kombu mit einem nur leicht feuchten Tuch vorsichtig abwischen, ohne den Belag auf der Oberfläche zu entfernen.',
   'Kombu und Wasser in einen Topf geben und 20–30 Minuten ziehen lassen.',
   'Langsam erhitzen und den Kombu kurz bevor das Wasser zu kochen beginnt herausnehmen.',
   'Die Hitze ausschalten, Katsuobushi zugeben und 2 Minuten ohne Umrühren ziehen lassen.',
   'Durch ein feines Sieb abseihen, ohne die Flocken auszudrücken. Das Dashi sofort verwenden oder rasch abkühlen.'
  ]},
 'component_tonkatsu':{
  'title':'Tonkatsu – panierte Schweineschnitzel',
  'ingredients':['Schweinelende in etwa 1,5 cm dicken Scheiben','feines Salz','Pfeffer','Weizenmehl (italienisches Tipo 00)','Ei','Panko-Paniermehl','neutrales Pflanzenöl zum Frittieren'],
  'steps':[
   'Den Fettrand der Schweinescheiben an mehreren Stellen einschneiden, damit sich das Fleisch nicht wölbt, und die Scheiben leicht auf eine gleichmäßige Dicke klopfen.',
   'Mit Salz und Pfeffer würzen, dann die Scheiben im Mehl wenden und überschüssiges Mehl abklopfen.',
   'Durch das verquirlte Ei ziehen und mit Panko umhüllen, ohne die Brösel zu fest anzudrücken.',
   'Das Öl auf 170–175 °C erhitzen und jeweils ein Schnitzel frittieren, bis die Panade goldbraun und das Schweinefleisch vollständig durchgegart, aber noch saftig ist.',
   'Auf einem Gitter 2–3 Minuten abtropfen lassen; erst unmittelbar vor dem Anrichten in Scheiben schneiden.'
  ]},
 'component_chocolate_custard':{
  'title':'Schokoladen-Puddingcreme für Choco Cornet',
  'ingredients':['Vollmilch','Eigelbe','Zucker','Maisstärke','Zartbitterschokolade (55–65 % Kakao)'],
  'steps':[
   'Die Milch erhitzen, bis sie knapp unter dem Siedepunkt ist.',
   'Eigelbe, Zucker und Maisstärke in einer Schüssel glatt verrühren.',
   'Die Hälfte der heißen Milch unter Rühren zu den Eigelben gießen; alles zurück in den Topf geben.',
   'Bei mittlerer bis niedriger Hitze ständig rühren, bis die Creme eindickt und leicht zu köcheln beginnt.',
   'Vom Herd nehmen, die gehackte Schokolade einrühren und vollständig schmelzen lassen.',
   'Frischhaltefolie direkt auf die Creme legen und vor dem Füllen der Choco-Cornet-Brötchen im Kühlschrank vollständig abkühlen lassen.'
  ]},
 'component_brioche_cornet':{
  'title':'Briocheteig für Choco Cornet',
  'ingredients':['backstarkes Weizenmehl','lauwarme Milch','Trockenhefe','Zucker','Salz','Ei','weiche Butter'],
  'steps':[
   'Mehl, Zucker und Hefe vermischen. Milch und Ei zugeben und kneten, bis kein trockenes Mehl mehr übrig ist.',
   'Salz und weiche Butter nach und nach einarbeiten und weiterkneten, bis der Teig glatt und elastisch ist und sich von der Arbeitsfläche löst.',
   'Abdecken und 60–90 Minuten gehen lassen, bis das Volumen nahezu verdoppelt ist.',
   'Den Teig vorsichtig entgasen, in 6 Stücke teilen und 10 Minuten entspannen lassen, bevor die Stücke zu Strängen gerollt werden.'
  ]},
 'component_karaage_ref':{'title':'Vollständiges Karaage-Rezept'},
 'component_japanese_curry_ref':{'title':'Vollständiges Rezept für japanisches Curry'},
 'component_kakuni_ref':{'title':'Vollständiges Kakuni-Rezept'},
 'component_yakisoba_ref':{'title':'Vollständiges Yakisoba-Rezept'},
},
'pt':{
 'component_chashu':{
  'title':'Chashu — entremeada de porco estufada para ramen',
  'ingredients':['entremeada de porco numa só peça','água','molho de soja','saqué para cozinhar','mirin','açúcar','gengibre fresco às rodelas','cebolinhos'],
  'steps':[
   'Enrole a entremeada e ate-a com fio de cozinha se quiser obter fatias regulares; caso contrário, deixe-a estendida.',
   'Aloure o porco de todos os lados num tacho até ficar bem dourado à superfície; retire o excesso de gordura libertada.',
   'Junte a água, o molho de soja, o saqué, o mirin, o açúcar, o gengibre e os cebolinhos. Deixe levantar uma fervura suave.',
   'Tape parcialmente e deixe cozinhar em lume brando durante 75–90 minutos, virando a peça a cada 20 minutos. Acrescente um pouco de água quente se o molho reduzir demasiado.',
   'Desligue o lume quando a carne estiver tenra, mas ainda suficientemente firme para cortar em fatias. Deixe-a arrefecer um pouco no líquido de cozedura.',
   'Leve ao frio durante pelo menos 1 hora para a carne ficar mais firme. Corte em fatias no sentido contrário ao das fibras e glaceie-as brevemente com um pouco do molho antes de servir.'
  ]},
 'component_ajitama':{
  'title':'Ajitama — ovos marinados para ramen',
  'ingredients':['ovos','molho de soja','mirin','água'],
  'steps':[
   'Leve um pequeno tacho com água ao lume até ferver e mergulhe os ovos delicadamente.',
   'Coza durante 6 minutos e 30 segundos para obter gemas cremosas e passe imediatamente os ovos para água com gelo.',
   'Descasque os ovos quando estiverem completamente frios.',
   'Misture o molho de soja, o mirin e a água. Coloque a marinada num recipiente pequeno e mergulhe nela os ovos descascados.',
   'Deixe marinar no frigorífico durante pelo menos 4 horas, mas não mais de 24 horas, virando os ovos a meio do tempo para ganharem cor de maneira uniforme.'
  ]},
 'component_dashi':{
  'title':'Dashi básico de kombu e katsuobushi',
  'ingredients':['água','alga kombu','katsuobushi (flocos de bonito seco)'],
  'steps':[
   'Limpe suavemente o kombu com um pano apenas húmido, sem retirar a camada que reveste a superfície.',
   'Coloque o kombu e a água num tacho e deixe repousar durante 20–30 minutos.',
   'Aqueça lentamente e retire o kombu pouco antes de a água começar a ferver.',
   'Desligue o lume, junte o katsuobushi e deixe em infusão durante 2 minutos sem mexer.',
   'Coe por um passador fino, sem espremer os flocos. Use o dashi de imediato ou arrefeça-o rapidamente.'
  ]},
 'component_tonkatsu':{
  'title':'Tonkatsu — bifes de porco panados',
  'ingredients':['lombo de porco em bifes com cerca de 1,5 cm de espessura','sal fino','pimenta','farinha de trigo (tipo italiano 00)','ovo','pão ralado japonês panko','óleo vegetal neutro para fritar'],
  'steps':[
   'Faça pequenos cortes em vários pontos da borda de gordura dos bifes de porco para evitar que enrolem e bata-os ligeiramente para uniformizar a espessura.',
   'Tempere com sal e pimenta, passe cada bife por farinha e sacuda o excesso.',
   'Passe pelo ovo batido e cubra com panko, sem pressionar demasiado o pão ralado.',
   'Aqueça o óleo a 170–175 °C e frite um bife de cada vez até o panado ficar dourado e a carne de porco estar completamente cozinhada, mas ainda suculenta.',
   'Deixe escorrer sobre uma grelha durante 2–3 minutos e corte em fatias apenas no momento de montar o prato.'
  ]},
 'component_chocolate_custard':{
  'title':'Creme de pasteleiro de chocolate para Choco Cornet',
  'ingredients':['leite gordo','gemas de ovo','açúcar','amido de milho','chocolate negro com 55–65 % de cacau'],
  'steps':[
   'Aqueça o leite até ficar quase a ferver.',
   'Numa tigela, bata as gemas com o açúcar e o amido de milho até obter uma mistura lisa.',
   'Verta metade do leite quente sobre as gemas, mexendo sempre, e volte a colocar toda a mistura no tacho.',
   'Cozinhe em lume médio-baixo, mexendo sem parar, até o creme engrossar e começar a fervilhar suavemente.',
   'Retire do lume, junte o chocolate picado e mexa até derreter completamente.',
   'Cubra com película aderente em contacto com a superfície e leve ao frigorífico até arrefecer completamente antes de rechear os Choco Cornet.'
  ]},
 'component_brioche_cornet':{
  'title':'Massa de brioche para Choco Cornet',
  'ingredients':['farinha de trigo de força','leite morno','fermento de padeiro seco','açúcar','sal','ovo','manteiga amolecida'],
  'steps':[
   'Misture a farinha, o açúcar e o fermento; junte o leite e o ovo e amasse até não restar farinha seca.',
   'Incorpore o sal e a manteiga amolecida aos poucos e continue a amassar até obter uma massa lisa, elástica e que se desprenda da bancada.',
   'Tape e deixe levedar durante 60–90 minutos, até a massa quase duplicar de volume.',
   'Retire o ar suavemente, divida em 6 pedaços e deixe a massa repousar 10 minutos antes de formar os cordões.'
  ]},
 'component_karaage_ref':{'title':'Receita completa de karaage'},
 'component_japanese_curry_ref':{'title':'Receita completa de caril japonês'},
 'component_kakuni_ref':{'title':'Receita completa de kakuni'},
 'component_yakisoba_ref':{'title':'Receita completa de yakisoba'},
},
}

def apply(source,pack):
    if digest(source)!=SOURCE_SHA256 or pack.get('sourceBaselineSha256')!=SOURCE_SHA256:
        raise ValueError('Italian source changed: component review stale')
    local=pack['locale']; source_components=source['reusableComponents'];target_components=pack['reusableComponents']; edits=COPY[local]
    if set(source_components)!=set(edits) or set(source_components)!=set(target_components):
        raise ValueError('Component coverage mismatch')
    for id,src in source_components.items():
        out=target_components[id]; content=edits[id]
        out['title']=content['title']
        if 'recipeRef' in src:
            if out.get('recipeRef')!=src['recipeRef']:raise ValueError('RecipeRef changed')
            if 'ingredients' in content or 'steps' in content:raise ValueError('Reference-only component has recipe content')
            continue
        if len(content['ingredients'])!=len(src['ingredients']) or len(content['steps'])!=len(src['steps']):
            raise ValueError(f'Component {id} cardinality mismatch')
        if len(out['ingredients'])!=len(src['ingredients']) or len(out['steps'])!=len(src['steps']):
            raise ValueError(f'Component {id} target cardinality mismatch')
        for ingredient,text in zip(out['ingredients'],content['ingredients']): ingredient['name']=text
        out['steps']=list(content['steps'])
    return pack
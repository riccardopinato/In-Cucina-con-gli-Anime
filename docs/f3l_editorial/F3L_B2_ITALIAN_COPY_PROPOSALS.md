# F3L B2 — Six Italian source copy proposals (NOT APPLIED)

**Evidence basis:** canonical `authoring/f3k_it_hardening_51_162.json` on baseline `aabf0d02234aabf4d90c85a77ebc006f4853b95b`, source SHA `954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c`. These are AI-assisted **candidate** descriptions reconstructed from the actual saved ingredients/methods; none is a qualified culinary or food-safety approval. **No source JSON, translation pack or runtime artifact is modified by this document.**

## 000059 — Asari no Sakamushi

**Observed:** the existing description has a broken clause about garlic and clam consistency and ends with a generic process sentence.

**Suggested replacement description (IT, pending review):**

> Nell’Asari no Sakamushi le vongole già spurgate vengono cotte brevemente in un tegame coperto con sake, aglio e zenzero. Dopo aver aromatizzato il burro a fuoco dolce, si uniscono le vongole e si alza la fiamma per favorirne l’apertura; quelle rimaste chiuse vengono scartate. A fuoco spento si completa il brodetto con il burro restante e poca salsa di soia, poi si serve con erba cipollina fresca. La preparazione richiede circa 15 minuti, escluso l’eventuale spurgo precedente.

**Checks before acceptance:** confirm clam sourcing and handling instructions; the existing elapsed-time note is a generic template and may require separate correction.

## 000073 — Pork Kakuni

**Observed:** the existing description talks about dough, forming pieces and filling a dish that is actually braised pork; the method also contains the typo `l'grasso` and a punctuation error in step 2.

**Suggested replacement description (IT, pending review):**

> Il Pork Kakuni si prepara con cubi di pancia di maiale prima sobbolliti in acqua con zenzero e parte verde del cipollotto, poi cotti lentamente in un fondo di sake, mirin, salsa di soia e zucchero. La prima cottura aiuta a eliminare il grasso in eccesso; nella seconda, la carne diventa tenera e assorbe gli aromi. Le uova sode entrano nel fondo durante gli ultimi minuti e si servono insieme al maiale, con salsa ristretta e un poco di senape karashi.

**Checks before acceptance:** reconcile the duration of the two simmering stages with total elapsed time; separately repair `l'grasso` and the step-2 punctuation without modifying stable step IDs or timers.

## 000074 — Oden Invernale Tradizionale

**Observed:** `Nel Oden` is ungrammatical and the existing description does not explain daikon, konnyaku, nerimono or kinchaku. One Piece episode provenance corrected in the previous PR must remain untouched.

**Suggested replacement description (IT, pending review):**

> L’oden è una preparazione invernale in cui daikon, konnyaku, uova sode e tortini di pesce cuociono lentamente in un brodo di dashi, salsa di soia chiara e mirin. Il daikon viene prima sbollentato, così come il konnyaku, mentre gli ingredienti principali sobbollono a fiamma bassa per insaporirsi senza disfarsi. I fagottini kinchaku con mochi si aggiungono solo negli ultimi dieci minuti. Si serve ben caldo, con parte del brodo e senape karashi a lato.

**Checks before acceptance:** verify the reported 117-minute total against preparation and simmer phases; preserve verified One Piece episode 966 and source evidence.

## 000081 — Tamago Sando

**Observed:** the source calls a ready-made bread sandwich a dough-based oven-ready wrapper. There is no baked dough in the recorded steps.

**Suggested replacement description (IT, pending review):**

> Il Tamago Sando è un sandwich giapponese di pane shokupan soffice, farcito con uova sode e maionese Kewpie. Parte delle uova viene schiacciata con maionese, latte e condimenti fino a ottenere una crema spalmabile; una mezza porzione di uovo resta intera al centro per creare una sezione decorativa al taglio. Il pane si spalma con poco burro, si farcisce e si lascia riposare avvolto per alcuni minuti prima di essere tagliato. Non richiede cottura del pane.

**Checks before acceptance:** verify ingredient-to-step egg count and food-safety handling/storage for the prepared egg filling.

## 000088 — Fruit Sando

**Observed:** the source talks about making dough and baking despite using ready-made bread and chilled whipped cream. Step 3 ends with `(es.` and step 4 continues as an orphaned sentence.

**Suggested replacement description (IT, pending review):**

> Il Fruit Sando abbina pane shokupan morbido, panna montata con zucchero e vaniglia e frutta fresca. La frutta viene disposta sulle fette ricoperte di panna secondo la diagonale di taglio, poi gli spazi vengono riempiti con altra crema per ottenere una sezione uniforme. Dopo aver chiuso e avvolto i sandwich, si lasciano in frigorifero per circa venti minuti e si tagliano seguendo il segno della diagonale. È un dolce freddo da assemblare, non da cuocere.

**Checks before acceptance:** repair steps 3–4 as a coherent instruction pair with existing stable IDs, and confirm the correct handling of chilled cream.

## 000124 — Uni Don

**Observed:** the description labels the operation as whipping/marinating; the saved method instead assembles chilled uni over warm (not boiling) rice.

**Suggested replacement description (IT, pending review):**

> L’Uni Don mette al centro il sapore delicato dei ricci di mare serviti sopra riso giapponese tiepido. La polpa di uni viene maneggiata il meno possibile e mantenuta refrigerata fino al momento dell’assemblaggio, mentre il riso viene condito e lasciato intiepidire. Nelle ciotole si distribuiscono prima riso e nori, poi si adagiano delicatamente le lingue di uni in un solo strato. Wasabi e salsa di soia si aggiungono con moderazione, preferibilmente a lato.

**Checks before acceptance:** **do not claim raw-seafood safety from freshness, smell or tasting alone**. A qualified reviewer must verify that the supplier/product is suitable for raw consumption and specify handling/market guidance. Revisit the existing instruction to taste raw uni as a purported safety indicator.

## Controlled integration policy

These six candidate descriptions are not a substitute for the **112/112 Italian contextual sweep**. A reviewer must approve each change against the complete source method; a separate source revision must increment the changed recipe versions (`000074` is currently v3; the other five are v2), update source provenance, and regenerate/repair all five target-language candidate packs and their source-locked tools. Do not simply rebind unchanged translated prose to the new source fingerprint. Maintain all 560 translations quarantined and release NO-GO throughout.

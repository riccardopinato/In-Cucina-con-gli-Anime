# Cooking Anime — roadmap operativa post-allineamento Factory v27 / AppLab v6.2

**Data di fotografia:** 29 ottobre 2026 (Europe/Rome). **Stato:** ROADMAP APPROVABILE, non certificazione di funzionalità. Questo documento aggiorna la pianificazione; il codice e gli esiti CI reali prevalgono sulle etichette storiche.

## 0. Source of truth e baseline bloccata

| Authority | Valore verificato | Precedenza |
| --- | --- | --- |
| Product truth | `docs/PRODUCT_BIBLE.md` e `docs/CONTENT_RIGHTS_POLICY.md` | Definiscono ciò che è autorizzato |
| Execution truth | `ROADMAP.md` + questa roadmap di dettaglio, richiamata dalla roadmap root | Dipendenze e gate |
| Factory resolver | `riccardopinato/App-Factory-Core/CURRENT.yaml` | Resolver delle regole cross-app |
| Factory session baseline | `174a05e165076c9e4b2d61a20acd85ca6b215f12` | **Master modulare v27.0 ACTIVE**, manifest `v27/candidate/MODULE_MAP.json`, Golden Index **v23** |
| Golden rilevanti | Agent Governance, Versioned Editorial Catalog (DRAFT), Localization, CI/Android/Web, AppLab QA (CERTIFIED PROCESS), Roadmap Fast, Event-driven Reconciliation, Immutable Artifact | Applicare solo i componenti pertinenti e rispettarne `status` |
| AppLab snapshot | `riccardopinato/AppLab@636490e58d38c3910eb168197cde72adb9cdb3f9` | **v6.2** feature handoff, autoriparazione ancora **SELF_CANARY** |
| Cooking Anime `main` acquisito | `8a7355004d007b40d916790a532f9a549c9da064` | PR #40 fusa; PR #41 non ancora integrata al momento della fotografia |

La v27 ha sostituito il Master v26.8 come authority grazie a `CURRENT.yaml`. I riferimenti v26.6/Golden 19 presenti nei documenti dell'app sono storici; non usarli come policy attuale. Il commit di Factory qui riportato è **snapshot di questa risoluzione**, non un'alternativa permanente a `CURRENT.yaml`: un nuovo refresh esplicito o una modifica centrale verificata invalida il pin. In step consecutivi senza questo trigger **riusare la baseline**, senza ripetere letture del Core/AppLab.

AppLab: `APP_FACTORY_ADOPTION.yaml` dichiara integrazione **CENTRAL** e `enabled: true`; è una dichiarazione di integrazione, **non** certificazione runtime automaticamente eseguita. AppLab v6.2 ha reporter, investigator, fix worker e draft-only PR publisher per il proprio `SELF_CANARY`, con budget 5 file/250 righe/2 tentativi, nessuna autoapprovazione/automerge o release authority del worker. Tre riparazioni indipendenti end-to-end **0/3 verificate** nel documento di handoff. Non abilitare implicitamente mutation su Cooking Anime, né promuovere `PILOT_3`/`PILOT_5`.

## 1. Stato prodotto verificato e vincoli

- **Catalogo runtime esistente:** 162 ricette, ID stabili; le prime 50 conservano artwork approvato, le ricette 51–162 usano il fallback procedurale. L'italiano canonico F3K e le bozze di cinque lingue sono un **percorso authoring separato**, non la pubblicazione automatica.
- **F0–F3J:** baseline funzionale/editoriale già sviluppata; F3B definisce l'identità **ricettario editoriale giapponese contemporaneo**, superfici carta di riso, palette crema/matcha/verde/albicocca/prugna, mascotte originali separate dalle ricette.
- **F3L B2-0/B2-I:** dossier per 112/112 ricette italiane, 10 componenti e 560 recipe-pair / 50 component-pair per EN/ES/FR/DE/PT; materiale AI, **non** approvazione umana.
- **PR #40:** sei ricette italiane prioritarie corrette e cinque pacchetti linguistici ricollegati alla sorgente in staging, merged su `main` come workbench non pubblicabile.
- **PR #41:** 106 casi residui affrontati, **105 descrizioni IT effettivamente modificate**, ricetta 55 già uguale lasciata invariata, **525 descrizioni automatiche** EN/ES/FR/DE/PT e correzioni mirate aggiuntive. La PR è **aperta**, NON fused al momento della fotografia; lo stato deve essere riletto prima di agire su di essa, non inferito da questa roadmap.
- **Problemi concreti nell'ultimo controllo PR #41:** Development checks FAIL in `Validate F3K Italian baseline` (**101 descrizioni sotto la soglia attuale di 45 parole**); F3L editorial staging audit FAIL in `test_f3l_expanded_review` (`warningCount=2`, atteso `0`). Translation draft workflow non ancora completato nel medesimo snapshot. **Non abbassare la soglia, non alterare test per forzare PASS**: migliorare le descrizioni e investigare i warning effettivi.
- **0 review native/culinarie certificate** per gli attuali draft; ogni pack resta `machine_draft_not_publishable`, `noAutomaticPublication=true`; 560 ricette localizzate / 50 componenti localizzati restano candidature, non approvate.
- **Immagini:** **non produrre ancora** i 112 artwork mancanti. Il vincolo richiesto è replicare la direzione stilistica delle prime 50, senza introdurre screenshot, loghi o personaggi protetti di anime.

## 2. Roadmap per priorità, dipendenze e Definition of Done (DoD)

| Maxi-step | Priorità | Dipendenza | Deliverable misurabile | Gate/DoD |
| --- | --- | --- | --- | --- |
| **R0 — Recupero PR #41** | P0 | nessuna | Esatta riconciliazione della PR, 101 descrizioni portate a requisito editoriale **senza boilerplate**, diagnosi dei 2 warning, test nuovi e precedenti coerenti con le versioni | F3K quality 0 errori; F3L audit 0 errori e 0 warning richiesti; source + 5 packs SHA allineati; tutte le required CI GREEN sull'**exact head**, review bloccanti risolte; squash merge verificato su `main` |
| **R1 — QA culinaria della sorgente italiana** | P0/P1 | R0 | Checklist per 112 ricette + 10 componenti, revisione di ingredienti, ordine operazioni, temperature, tempi e sicurezza, traccia di ogni difetto e correzione | Nessun P0/P1 culinario irrisolto; versioni/hash incrementati solo per modifiche reali; ricevute di revisione umana autentiche o **PENDING** esplicito; nessun certificato inventato |
| **R2 — QA linguistica cinque lingue** | P1 | R1 fonte congelata | Dossier bilingue completo 5×112 + 5×10, glossario culinario, fix imperativi/quantità/step/sicurezza; controllo rafforzato portoghese via pivot EN | 112/112 verifiche **umane autentiche** per ogni lingua prima della pubblicazione, incluse 10 subricette per lingua; `release-ready` gate e structural/semantic QA realmente PASS; zero falsi claim di sign-off |
| **R3 — F3L B3: integrazione catalogo runtime** | P1 | R1 + R2 | Migrazione deterministica di 112 ricette localizzate dalla fonte italiana autorizzata all'authoring pubblicabile e agli asset runtime esistenti, senza copie spurie | 162 ricette/6 lingue, ID e favorites/shopping preservati, fallback verificato, drift/schema/similarity/rights fail-closed; Flutter test/Web/Android exact-head GREEN; no sign-off retroattivo |
| **R4 — Artwork originale 51–162** | P1/P2 | contenuti culinari congelati (almeno R1; non anticipare i batch rispetto alle decisioni editoriali) | Reference board dai **50 artwork approvati** + 112 nuovi JPEG originali in batch piccoli (preferibilmente 8–12); un asset per ricetta, riusato in card/hero | Semantica piatto corretta, rights `original|public_domain|licensed` reali, approvazione esplicita e contenuto/versione coerenti, long edge ≤960 px, short edge ≥720 px, target ~130 KiB, hard cap 140 KiB, zero regressioni F3E |
| **R5 — F4 monetizzazione controllata** | P2 | R3, accordo prodotto/prezzi | F4B entitlement + acquisto una tantum, F4C banner adaptive sulle sole pagine browse, F4D Play sandbox/consent/restore | Non attivare provider/SDK o ad requests senza approvazione scope; consent per launch valido, acquisto/restore in sandbox, zero pubblicità in cooking/timer, offline fail-closed |
| **R6 — F5 certificazione e distribuzione** | P1 di release | R3/R4, R5 se monetizzazione inclusa nel prodotto da rilasciare | Signed build identity stabile, AAB + APK e hash, AppLab trusted FULL/CERTIFICATION dove disponibile, QA dispositivo fisico, checklist Play | Same-artifact evidence, no automatic 'CERTIFIED' da CI, test fisici per scenari pertinenti, diritti/immagini verificati, privacy/store metadata e distribuzione provati |

**R4 non riscrive R3:** si può usare il fallback già esistente su ricette senza artwork e aggiungere progressivamente gli asset una volta approvati, ma la pubblicazione delle immagini non anticipa la verifica culinaria della ricetta associata.

## 3. Esecuzione ottimizzata secondo Factory v27

**Procedi = valutazione una volta del router**, non nuova roadmap a ogni messaggio. Usare `ROADMAP_FAST` e i quattro stati manutenzione `BLOCKING_NOW / FIX_CURRENT_STEP / BACKGROUND_MAINTENANCE / FUTURE`.

- **R0: CONTROLLED, seriale sul contenuto.** Il source SHA è condiviso fra cinque pack; un solo writer gestisce mutazione/versionamento. In parallelo solo analisi non mutative indipendenti dei warning, audit e preparazione dei test. Correggere prima il preflight deterministico (`tool/f3k_it_quality_gate.py`, F3L unittest, source/pack check), poi sprecare meno tempo in Flutter/Web/Android CI.
- **R1: 2 workstream realmente separabili quando efficaci.** (A) copy/metodo e anomalie ingredienti/tempi, (B) revisione sicurezza/rights con evidenze, **nessuna doppia scrittura** sulla stessa fonte. Owner unico integra versioni/hash e cinque lingue.
- **R2: parallelismo valido per EN, ES, FR, DE, PT**, una ownership per locale e un glossario autorevole condiviso. L'integrazione arriva **solo dopo** l'ultima modifica italiana, così non si traducono SHA subito invalidati.
- **R4: lavoro per batch visivi indipendenti** dopo il riferimento stilistico e la lista di piatti congelata; QA e approvazione per singolo asset, poi un unico aggiornamento del manifest/CI per batch.
- **AppLab**: riusare l'adapter client Golden certificato per FAST/FULL quando realmente configurato; immutable SHA dell'AppLab verificato, package `com.riccardopinato.animekitchen`, Flutter `3.47.3`, workflow/build contract espliciti. Per l'automazione v6.2 rispettare `SELF_CANARY`; su Cooking Anime usare le normali azioni Chat/GitHub e required checks senza attribuire ad AppLab autoriparazioni non consentite.
- **CI gate e hash:** validare il commit integrato; un commit successivo invalida il vecchio exact-head PASS. Reuse di APK/artifact solo per source SHA + artifact SHA + build contract + toolchain/signing identici. Non fare polling e rilanci costosi o loop `until green` su problemi noti.
- **No nuovo scope implicito**: account, cloud, sync, nuove funzionalità, abbonamenti o uso di materiale anime protetto rimangono fuori dalla roadmap attiva. Le richieste "procedi" possono portare a PR e merge **dopo gate**, ma non superano approvazioni umane, diritti e store.

## 4. Rischi e corsie di manutenzione

| Rischio | Classe | Azione |
| --- | --- | --- |
| PR #41 non mergeabile a causa di descrizioni troppo brevi/avvisi | **BLOCKING_NOW** | Riscrivere i 101 testi in modo specifico; tradurre le modifiche realmente apportate nei cinque pack; risolvere i due warning; eseguire gate senza riduzioni di soglia |
| Pesce/molluschi crudi, tuorlo non pastorizzato, frattaglie, pollo, riso cotto conservato | **BLOCKING_NOW** per la pubblicazione delle ricette impattate | Revisioni culinarie e di sicurezza vere, istruzioni contestuali verificabili e tracciate |
| Errore traduzioni a rischio (es. termini culinari scorretti) | **FIX_CURRENT_STEP** se introdotto dalla PR attiva; altrimenti **BACKGROUND_MAINTENANCE** fino alla promozione, allora blocking | Revisionare frase in contesto, non rebinding cieco hash |
| `APP_BOOTSTRAP.yaml`/AGENTS/Golden manifest con Factory storica v26.6 | **FIX_CURRENT_STEP** allineamento documentale | Aggiornare puntatori alla baseline v27; non duplicare policy |
| Mancanza di immagini 51–162 | **FUTURE** fino a R4 | Conservare fallback funzionale; produrre nuova arte solo dopo fonte stabile |
| Upgrade AppLab v6.2 self-canary oltre il proprio repo | **FUTURE / explicit gate** | Non iscrivere Cooking Anime ai writer autonomi senza prove + decisione policy |
| Debito di codice non correlato o feature desiderabili | **BACKGROUND_MAINTENANCE** | Bounded sweep, nessun ampliamento opportunistico della PR corrente |

## 5. Cosa deve restare verificabile in ogni handoff

1. **Baseline:** Factory SHA + versione Master/Golden, AppLab SHA, app source SHA, PR/head esatto.
2. **Delta:** file cambiati, numero ricette/versioni, source/locale hash, asset manifest e rights state.
3. **Test:** preflight F3K/F3L, authoring catalog, Flutter, Web, Android ed eventuale AppLab reale: `PASS / FAIL / BLOCKED / NOT VERIFIED` distinti.
4. **User state:** ID invariati, Favorites e Shopping preservati, fallback offline invariato.
5. **Pubblicazione:** `machine_draft_not_publishable` resta tale fino a ricevute autentiche, nessuna falsa certificazione da run verde.
6. **Merge e release:** PR/head gate e commit su main verificati; release/store sono gate successivi, non dedotti dal merge.

## 6. Regola di continuità per i prossimi turni

Questa roadmap e i due SHA costituiscono la **baseline dichiarata della pianificazione del 29/10/2026**. I prossimi step possono riusarla direttamente in Chat, senza riscaricare Core/AppLab a ogni risposta. Se una versione centrale viene aggiornata e ne è richiesta l'adozione, risolvere nuovamente `CURRENT.yaml`, il manifest e **solo** i Golden pertinenti, e riconciliare la roadmap con il nuovo stato **reale** dei repository. Una modifica alla PR #41 deve essere letta sul suo nuovo head prima di proporre merge.

**Non dichiarare completati R0–R6 per il solo fatto che questa roadmap sia in repository.**

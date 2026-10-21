# Roadmap

The roadmap uses tracer-bullet slices: each step should end in something demonstrable and leave CI green.

## F0 — Foundation shell — CURRENT

Blocked by: none.

Delivers:
- Product Bible + rights policy + architecture;
- App Factory bootstrap manifest and Golden reuse map;
- deterministic Flutter Android/iOS/Web scaffold;
- original launcher-icon source;
- Material 3 light/dark brand theme;
- EN/IT/ES/FR/DE/PT localization infrastructure;
- responsive Explore / Favorites / Shopping shell;
- empty catalog adapter (zero recipes);
- persistent preferences/favorites/shopping;
- provider-agnostic entitlement/ProductLimits;
- dev CI + Web Preview workflow;
- baseline tests.

Exit: PR merged with development checks green.

## F1 — Versioned recipe catalog contract

Blocked by: F0.

Delivers a validated local catalog package with stable IDs, versioning, canonical metadata vs localized editorial text, provenance/rights, locale fallback and deterministic validation.

Exit: invalid package fails closed; user state survives catalog replacement.

## F2 — Recipe authoring/import pipeline

Blocked by: F1.

Delivers tooling to add our own recipes without editing Dart: authoring schema/templates, asset manifest, localization completeness report, rights/provenance checks and preview/build command.

Exit: one non-production fixture can travel authoring -> validation -> app preview.

## F3 — First real editorial batch

Blocked by: F2.

Delivers the first production recipes written for this app.

Rules:
- do not transcribe recipes from the attached PDF/books/web;
- every entry has rights/provenance review;
- original visuals only unless licensed;
- exact batch size decided at implementation time.

Exit: search/filter/detail/timer/favorites/shopping work end-to-end with real content.

## F4 — Monetization v1

Blocked by: F3.

Delivers consent/privacy, safe adaptive browsing ads, no ads during active cooking, one-time Remove Ads/Lifetime and entitlement-driven no-ad-request behaviour.

Exit: provider/store sandbox evidence exists.

## F5 — Release hardening

Blocked by: F4.

Delivers persistent Android signing, release AAB/hash evidence, AppLab FULL, physical-device validation and store readiness review.

## Later candidates

Collections/menu planning, ingredient scaling, pantry mode, timers per step, shareable cards, optional Google Sign-In + backup, remote content packs and seasonal editorial packs.

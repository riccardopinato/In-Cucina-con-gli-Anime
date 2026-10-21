# Product Bible — In Cucina con gli Anime

## Promise

A polished cooking companion that turns food seen in anime into practical, original recipes users can actually cook, save and shop for.

The product should feel warm, illustrated and playful without presenting itself as an official app of any anime studio, publisher or franchise.

## Target user

- anime/manga fans who also enjoy cooking;
- casual cooks who want approachable themed recipes;
- users looking for a visually distinctive recipe app rather than a generic database.

## MVP product surface

1. **Explore** — search, anime/reference filters, difficulty filters, responsive recipe grid.
2. **Recipe detail** — original recipe text, ingredients, steps, times, difficulty, timer and ingredient checklist.
3. **Favorites** — persistent saved stable recipe IDs.
4. **Shopping** — persistent shopping items and manual additions; later add ingredients from recipes.
5. **Settings** — device language by default, manual language override, system/light/dark theme.
6. **Monetization boundary** — free by default, provider-agnostic Premium/Lifetime state, future safe ads + Remove Ads.

## Current bootstrap scope

This phase builds the application foundation and empty catalog experience only.

**Zero recipes are imported from the attached PDF or from external books/web sources.**
Recipe implementation is a later editorial phase.

## UX direction

Original watercolor-inspired cooking identity:
- cream/rice-paper background;
- meadow green primary;
- ember orange accent;
- pale sky secondary;
- rounded cards and low elevation;
- handwritten accent typography for display headings;
- clean rounded body typography;
- restrained motion.

The design may evoke a cozy illustrated cookbook, but must not copy franchise artwork, logos, characters or official key art.

## Local-first

Core browsing of installed recipe content, favorites and shopping list should remain useful offline. Login is not required to access core value.

## Content model principles

- stable recipe IDs are independent of title/translation;
- catalog content is versioned;
- user-owned state references stable IDs;
- catalog updates never silently erase favorites or shopping data;
- canonical metadata and localized editorial text remain separable;
- shipped image/text assets carry provenance/rights metadata when applicable.

## Monetization direction

Initial preferred model:
- free catalog access;
- non-invasive adaptive banner only on browsing surfaces after consent/provider integration;
- no ad request for entitled users;
- no ads while actively following a recipe/timer;
- one-time Remove Ads/Lifetime before considering a subscription.

Exact pricing/provider/store integration is out of scope for the bootstrap.

## Out of scope now

- recipe population;
- copied cookbook recipes;
- official anime screenshots/posters/logos;
- AI recipe generation;
- account/cloud sync;
- notifications;
- meal planning;
- social/community features;
- live ads;
- live billing/store purchase;
- production signing/certification.

## Foundation success criteria

- deterministic Android/iOS/Web Flutter scaffold;
- intentional empty catalog, no fake recipes;
- Explore/Favorites/Shopping navigation works;
- localization/theme/settings infrastructure exists;
- user-state persistence seams exist;
- entitlement boundary is provider-agnostic;
- CI validates analyze/test/Web and Android internal build;
- the catalog can become versioned without a UI rewrite.

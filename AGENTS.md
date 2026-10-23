# In Cucina con gli Anime — agent contract

Product truth: `docs/PRODUCT_BIBLE.md`.
Execution truth: `ROADMAP.md`.
Architecture truth: `docs/ARCHITECTURE.md`.
Reuse map: `docs/GOLDEN_REUSE_MANIFEST.txt`.
Rights policy: `docs/CONTENT_RIGHTS_POLICY.md`.
Authoring truth: `docs/RECIPE_AUTHORING_PIPELINE.md`.

Factory baseline for the current implementation:
`riccardopinato/App-Factory-Core@4cc0b94467b94ab6fabe2c927fcc58afff49e39a`
(Master 26.6 / Golden Index 19).

Load only the project guidance relevant to the current task:
- cleanup/replacement work -> `governance/agents/code-hygiene.md`
- tests/build/evidence -> `governance/agents/testing-validation.md`
- Git/PR work -> `governance/agents/git-workflow.md`
- donor/OSS/research work -> `governance/agents/research-reuse.md`

Project rules:
- Flutter/Dart, local-first, no mandatory login.
- Keep `main` stable; substantive changes land through PRs.
- Recipes are editorial content, not source code. Stable IDs must preserve user state.
- Runtime recipe JSON is generated from `authoring/recipes/*.json`; do not edit generated catalog files as the primary authoring workflow.
- Raw copied recipe prose/source material is transient input and must not be committed to `authoring/`.
- Similarity scores are review aids, not authority for automatic delete/overwrite.
- Fingerprint-bound duplicate/variant decisions live in `authoring/reviews/decisions.json`.
- Do not copy recipe prose or copyrighted anime artwork into the app.
- The attached historical PDF remains context only; import zero recipes from it unless the user explicitly selects content for editorial processing.
- Web Preview validates shared UI/navigation/content wiring, not native/store capability.
- Prefer deep modules with small interfaces; add a seam only when behaviour actually varies.
- Update Product Bible/Roadmap when product or execution truth changes materially.

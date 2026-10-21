# In Cucina con gli Anime — agent contract

Product truth: `docs/PRODUCT_BIBLE.md`.
Execution truth: `ROADMAP.md`.
Architecture truth: `docs/ARCHITECTURE.md`.
Reuse map: `docs/GOLDEN_REUSE_MANIFEST.txt`.
Rights policy: `docs/CONTENT_RIGHTS_POLICY.md`.

Factory baseline for this bootstrap:
`riccardopinato/App-Factory-Core@47c47f49a7b46812e3bd6f1231c3524f2b52b826`
(Master 26.6 / Golden Index 18).

Load only the project guidance relevant to the current task:
- cleanup/replacement work -> `governance/agents/code-hygiene.md`
- tests/build/evidence -> `governance/agents/testing-validation.md`
- Git/PR work -> `governance/agents/git-workflow.md`
- donor/OSS/research work -> `governance/agents/research-reuse.md`

Project rules:
- Flutter/Dart, local-first, no mandatory login.
- Keep `main` stable; substantive changes land through PRs.
- Recipes are editorial content, not source code. Stable IDs must preserve user state.
- Do not copy recipe prose or copyrighted anime artwork into the app.
- The attached PDF is context only for this bootstrap: import zero recipes from it.
- Web Preview validates shared UI/navigation, not native/store capability.
- Prefer deep modules with small interfaces; add a seam only when behaviour actually varies.
- Update Product Bible/Roadmap when product or execution truth changes materially.

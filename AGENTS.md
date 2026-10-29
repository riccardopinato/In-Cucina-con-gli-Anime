# In Cucina con gli Anime — agent contract

Product truth: `docs/PRODUCT_BIBLE.md`.
Execution truth: `ROADMAP.md`.
Architecture truth: `docs/ARCHITECTURE.md`.
Reuse map: `docs/GOLDEN_REUSE_MANIFEST.txt`.
Rights policy: `docs/CONTENT_RIGHTS_POLICY.md`.
Authoring truth: `docs/RECIPE_AUTHORING_PIPELINE.md`.

Factory resolver (always authoritative): `riccardopinato/App-Factory-Core/CURRENT.yaml`.
Last verified alignment snapshot (2026-10-29): Factory
`174a05e165076c9e4b2d61a20acd85ca6b215f12`
(**Master v27 modular ACTIVE / Golden Index v23**), AppLab
`636490e58d38c3910eb168197cde72adb9cdb3f9` (**v6.2, SELF_CANARY**).
Do not treat historical v26.6 / Golden 19 copies as the current policy.
Resolve the Factory once per bootstrap; reuse pinned SHA between consecutive
steps unless the Core changes or an explicit refresh is requested. AppLab v6.2
does not authorize an autonomous repair writer for this downstream repository.

Detailed active roadmap: `docs/ROADMAP_FACTORY_V27_APPLAB_V62_2026-10-29.md`
under the root `ROADMAP.md`. It distinguishes draft editorial source changes,
real human-review gates, and subsequent artwork in the style of recipes 1–50.

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

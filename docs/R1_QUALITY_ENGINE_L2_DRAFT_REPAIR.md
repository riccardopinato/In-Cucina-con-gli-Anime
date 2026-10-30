# Quality Engine L2 — bounded, autonomous **draft-only** repair pilot

**Scope:** local, minimal formatting on three Quality Engine Markdown docs only.
**Factory baseline:** `174a05e165076c9e4b2d61a20acd85ca6b215f12`, Master v27 ACTIVE, Golden Index v23.
**AppLab:** v6.2 SELF_CANARY has **not** authorized downstream general-purpose self-repair. This pilot is a separately scoped app-local workflow, not a promotion of AppLab privileges.

## Behavior

Two independent GitHub Actions jobs in `.github/workflows/quality-engine-l2-draft.yml`:

1. **Read-only plan** (global `contents:read`) executes on `main` via manual dispatch or best-effort daily schedule at 05:41 UTC. Generates an inspectable 14-day `quality-l2-readonly-plan` artifact. If there are no allowed differences, the writer job does **not** start.
2. **Conditional draft writer** (job-scoped `contents:write` and `pull-requests:write`) runs **only** for the original repository and default-branch event, and only if a plan lists changes. Checks the source SHA still equals current `main`, independently regenerates the plan, runs L2 regression tests, creates a new isolated `quality-l2/blank-lines-{sha}` branch, verifies an exact allowlisted diff, pushes and opens a **draft PR**. No branch overwriting or forced pushes; no merged PRs, no automated review approvals, and no release.
3. GitHub may block `GITHUB_TOKEN` PR creation under repository Actions settings. If so, this is a **real permission blocker**, not something to bypass. GitHub-token-authored PRs may not auto-trigger CI: exact-head tests/reviews remain separate, and an automated draft **must not** merge without those gates.

The schedule is a **recurring GitHub Actions job**, not a persistent 24/7 agent. Observe a real `schedule` event and a valid repair draft on a genuine eligible change before declaring the full autonomous path proven.

## Precisely allowed repair

Rule ID `MD_BLANK_LINE_WHITESPACE`: remove spaces and tabs from lines containing **nothing else** (outside conservatively detected fenced code sections). This does not touch substantive prose, Markdown hard breaks, code snippets, image links, line endings or other file content.

The following are the **only three code-level allowlisted targets**:

- `docs/R1_QUALITY_ENGINE_V2_PILOT.md`
- `docs/R1_QUALITY_ENGINE_V21_HISTORY.md`
- `docs/R1_QUALITY_ENGINE_V22_DIAGNOSER.md`

`.quality-engine-l2.json` further narrows this list; it **cannot** expand beyond the Python immutable allowlist. Each file is verified as an existing UTF-8 regular file, not a symlink; symlink traversal and source differences fail closed. Per-file budget: at most 256 KiB, 40 changed lines, 1024 removed bytes; at most three files total.

`tool/quality_engine_l2_draft.py` provides independent `plan` and `apply` entry points. The plan records original/result SHA-256 hashes, line numbers, counts, repository + baseline commit SHA and policy fingerprint, but no original excerpts or secrets. `apply` regenerates and checks the entire plan from the trusted checkout before writing anything; the caller must open an isolated branch before calling it.

At the time this pilot was built, the three allowed Markdown docs had no eligible whitespace-only lines. Therefore a successful scan naturally produces **zero** repair PRs until such a difference exists. This is desirable: don't inject bugs into `main` to demonstrate auto-fix.

## What is never allowed

- No changes in `lib/`, app Flutter/Dart/Kotlin code, `authoring/`, recipes, culinary approvals, assets, locale packs, translation QA, protected workflows, tests, signing, user data, network security, payments, billing or store configuration.
- No direct commits to main, no `gh pr merge`, no automatic release, no historical rewrite and no overwrite of existing branches.
- No paid AI, no code-evaluation from untrusted PRs or outside repositories, no unattended general-purpose model writer.
- GitHub token privileges apply at job level, not per path. **Our code allowlist is the restricting mechanism**, backed by tests and independent review. Repo branch protection must still remain effective.

## Manual checks

```bash
python3 -m unittest tool.tests.test_quality_engine_l2_draft -v
python3 tool/quality_engine_l2_draft.py plan \
  --root . --config .quality-engine-l2.json \
  --repository riccardopinato/In-Cucina-con-gli-Anime \
  --source-sha "$(git rev-parse HEAD)" \
  --plan build/quality-l2/plan.json
```

To test `apply`, use a disposable checkout/branch and synthetic fixtures; do **not** change production documentation merely to trigger a PR.

## Roadmap to useful self-healing code

- **L2 pilot (this PR):** minimal deterministic doc repairs; code edits disabled. Prove the complete permissioned workflow with a real future candidate and review the generated diff.
- **L2.1 next:** add tightly reviewed individual code-formatting rules backed by deterministic unit tests, with sandbox diff budgets, protected-path policies and canary execution. Use existing v2.2 diagnostic proposals as observations, **not instructions**.
- **L2.2:** in isolated branch create draft PRs for validated low-risk code fixes, independent CI, review, audit and rollback. Introduce separate authorization per repair rule and repository.
- **L3 later:** selectively permit auto-merge of an explicit low-risk allowlist only if exact-head independent checks and branch protection pass. Exclude security, payments, identity, data migrations, culinary/editorial review, asset rights and release/signing without separately authorized qualified verification.
- **Factory Core migration:** do not copy app-local mutable privileges into `App-Factory-Core` until a separately reviewed Golden design, cross-app pilots, governance and rollback procedures are approved.

## Release gate

Merge this **infrastructure PR** only on exact-head Development checks and independent Quality Engine workers green, no unresolved code review, no unexpected changed files. On `main`, verify plan job runs and artifact; the actual writer job remains untested until an eligible low-risk observation occurs. Maintain R1 food-safety PR #44 DRAFT; 112 recipes and 10 components remain PENDING.

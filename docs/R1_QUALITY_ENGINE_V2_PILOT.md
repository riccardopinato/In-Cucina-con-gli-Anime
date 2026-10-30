# R1 Quality Engine v2 — exportable autonomous observation pilot

**Date:** 30 October 2026. **Status:** READ-ONLY PILOT / NOT APP FACTORY CORE CERTIFIED.
Factory baseline pinned: `174a05e165076c9e4b2d61a20acd85ca6b215f12` (Master v27 ACTIVE, Golden Index v23). This branch does **not** edit App-Factory-Core or unlock AppLab's SELF_CANARY limits.

## What is implemented

The versioned Python-standard-library core `tool/quality_engine_v2.py` accepts `--root`, `--config`, `--mode`, `--source-sha` and `--output`, and can be copied to another repository **without importing Cooking Anime modules**. Only the `content` adapter currently understands Cooking Anime's F3K recipe JSON; the `code` and `workflows` adapters operate on generic paths. `.quality-engine-v2.json` defines project-specific path patterns.

- **code:** Python AST for dynamic eval/exec, bare except, shell=True; Dart line heuristics for debugging prints and plaintext HTTP literals. These are risk *candidates*, not proven vulnerabilities.
- **content:** generic consistency checks of structured recipe IDs, ingredients, timing, missing steps/dependencies; dynamic leads for raw fresh egg yolks and longer reusable components, **without hardcoding the 20 R1 v1 cases**.
- **workflows:** GitHub Action immutable-SHA pinning and privileged GitHub Actions event/permission patterns.
- Stable per-finding IDs from rule, relative path, entity and line; explicit severity `info | review | high`, revision/source SHA, deterministic sorting, no raw snippets or alleged human evidence.
- Three independent GitHub Actions matrix workers run **in parallel** on `main` pushes, PR changes, manual dispatch and an **hourly best-effort UTC cron** (`23 * * * *`). Each uploads a 14-day JSON report in GitHub Actions artifacts; GitHub may delay or skip scheduled jobs under high load.
- Default-only read permissions (`contents: read`); no secrets passed, paid AI requests, external service calls, SDK installations, commits, PR creation or changes to app content.
- R1 v1 (`tool/r1_culinary_triage.py` with 20 manually witnessed cases) is **preserved unchanged**. R1 v2 is additive and does not certify its 122 entries.

**Important precision:** scheduled GitHub Actions are *event-driven recurring jobs*, not a resident 24/7 autonomous process. The engine autonomously executes **after its workflow is merged on default `main`**. Before merge it runs for the PR; the hourly `schedule` exists only when default branch contains it.

## What it does NOT do

- No LLM semantic reasoning, full static-analysis compiler, food safety assurance, exploit verification, native human review or guarantees of complete code coverage.
- No edits, auto-fixes, automatic merges, deployments, cross-repository access or privileged GitHub mutation.
- No automatic synchronization with App-Factory-Core; future central adoption requires its own governance and verified adapter.
- No release approval, license or safety certification. `readOnly: true`, `selfRepairEnabled: false`, `certification: NOT_CERTIFIED`, `humanApprovals: 0` in every report.

## How to run

From repository root (Python >=3.11):

```bash
python3 tool/quality_engine_v2.py --mode code --output build/quality-v2/code.json
python3 tool/quality_engine_v2.py --mode content --output build/quality-v2/content.json
python3 tool/quality_engine_v2.py --mode workflows --output build/quality-v2/workflows.json
python3 -m unittest tool.tests.test_quality_engine_v2 -v
```

Every JSON report includes `engine`, `version`, `mode`, `profile`, `sourceSha`, `filesScanned`, `filesSkipped`, severity counts and `findings` with source locations but **no excerpt values**. Open the run `R1 Quality Engine v2 — autonomous read-only scan` under GitHub Actions and inspect `quality-v2-code`, `quality-v2-content`, `quality-v2-workflows`.

## Constraints for safe adoption across App Factory

1. Validate the pilot via exact-head CI, regression tests, real scheduled runs on `main`, signal/noise review and a bounded false-positive register.
2. Extract the core as a versioned **read-only** standalone module: per-language analyzers and per-app schema adapters, well-defined result schema, deterministic fingerprints and an allowlisted scan scope. Never centralize app-specific editorial business facts.
3. Add append-only history/previous-run comparison `NEW | PERSISTING | RESOLVED` without overwriting originals; guard event sources and privacy before enabling cross-repository read access.
4. For optional AI semantic analysis use explicit, scoped model permission and spend budget. LLM findings stay proposals with source evidence and human sign-off; **never use a model judgment as certification**.
5. Add change proposals only through **draft PRs** with bounded writer privileges, protected paths, required reviews and CI. AppLab SELF_CANARY does **not** grant this pilot an auto-fix right.
6. Move to App-Factory-Core only after a separately reviewed Core/Golden proposal and a minimum pilot spanning different app stacks. Keep central `CURRENT.yaml` authoritative; don't update it implicitly.

## Acceptance criteria

- Exact-head existing Development checks and new autonomous workflow PASS.
- The three workers report independent mode-specific findings for the same source SHA and upload artifacts.
- No source/config/user data writes by scanner, including on test failure.
- Negative tests enforce unsafe path rejection, source immutability, no leaking finding excerpts or token-like values, and zero fake approvals.
- No merge if CI fails or blocks; once merged verify default-branch scheduled trigger and observe at least one actual periodic run before saying 'hourly in production'.

**Next after v2 pilot:** add baseline-diff and multi-app adapters in a separate PR; only then an optional autonomous *draft suggestion* agent.

# Quality Engine v2.4-A — first portable static code adapter

Factory pinned baseline: `174a05e165076c9e4b2d61a20acd85ca6b215f12` (Master v27 ACTIVE / Golden Index v23). **Status:** candidate pending CI and review. **No changes to App Factory Core.**

## Goal

Start v2.4 deeper code analysis without confusing lightweight, source-based heuristics with a certified analyzer or Android release validation. The previous v2/v2.1 history scope and schema are **unchanged**. The new source-bound scanner runs independently and has **no inherited historical baseline**, preventing false NEW/RESOLVED entries when new rules appear.

## Added adapters

`tool/quality_engine_v24_static.py` uses Python's standard library only, no network/model calls, and emits deterministic JSON leads:

- **Dart/Flutter:** candidate TLS certificate callback bypass, sensitive-key storage calls with explicit literal keys, release logging, file-level lint suppressions.
- **Kotlin:** candidate permissive TLS hostname verifier and runtime logging.
- **Android manifest XML:** explicit cleartext permission, debuggable manifest, exported app components without local permissions; duplicate component leads get distinct stable IDs.
- **Gradle:** plaintext dependency repositories and dynamically resolved dependency versions.

These are static **review candidates**, not proven exploitability or automatic remediation instructions. Malformed manifests are reported as parse issues; unknown file formats and missing source scopes are visible in the coverage table.

## Important project coverage nuance

Cooking Anime's current Git repository includes Flutter/Dart `lib/`, but **does not version Android/Kotlin/Gradle files** (the CI uses generated platform scaffolding). Therefore the initial `kotlin`, `android_manifest` and `gradle` results are expected to be `NO_MATCHING_FILES`, **not PASS**. Cross-stack implementation must later be validated with real Kotlin Android repositories and generated Android artifacts where appropriate.

## Operation and privacy

- Config `.quality-engine-v24.json` sets mode-specific paths.
- Independent `.github/workflows/quality-engine-v24-static.yml` runs on relevant `main` push and PR events, manual dispatch, and a best-effort daily cron at **06:47 UTC**.
- Only `contents:read` permission. No branch/commit edits, PR writes, remote paid AI, approvals, merges or releases.
- `quality-v24a-static-analysis` artifact retained 14 days, with source SHA, files scanned per technology, skipped-file reasons and candidate review rules, no original input line excerpts.
- `tool/tests/test_quality_engine_v24_static.py` includes **13 regression scenarios**, covering real Dart and synthetic Android/Kotlin/Gradle fixtures, ID uniqueness, input safety, no-source-excerpts, explicit no-coverage status, and workflow permissions.

Run locally:

```bash
python3 -m unittest tool.tests.test_quality_engine_v24_static -v
python3 tool/quality_engine_v24_static.py \
  --config .quality-engine-v24.json --source-sha "$(git rev-parse HEAD)" \
  --output build/quality-v24/static-analysis.json
```

## Next slices

1. v2.4-B: integrate mature, pinned analyzers where available (Flutter `flutter analyze`, Android lint when Android sources exist, Gradle dependency validation) with machine-readable evidence. Do not duplicate compiler claims with regex guesses.
2. v2.4-C: pilot in at least one true Kotlin Android repository, explicit cross-app permissions and false-positive measurements.
3. L2.1: **separately reviewed** isolated draft repair for deterministic code-formatting rules with independent CI. Do not let L2 consume new review leads as unrestricted patch instructions.
4. v3.0: multi-app orchestration with isolated tokens and separately reviewed Factory Core/Golden integration.

Current L2 draft-only repair remains limited to the three allowlisted Quality Engine docs. Culinary review PR #44 remains DRAFT with 112 recipes + 10 components PENDING.

## Merge / release gates

Only merge after exact-head Development checks, Quality Engine v2 code/content/workflows and new `static-review-leads` all green, review threads resolved and no branch protection bypass. Post-merge verify new workflow on `main`; do not claim real daily cron execution before observing an actual `schedule` event.

# Quality Engine v2.4-B — official Dart analyzer evidence

**Status:** engineering PR candidate, exact-head CI and independent review required. Date: 30 October 2026.
**Pinned App Factory baseline:** `174a05e165076c9e4b2d61a20acd85ca6b215f12` (Master v27, Golden Index v23). No App Factory Core or AppLab SELF_CANARY policy changes.

## Objective

The v2.4-A scanner uses bounded heuristics. This iteration adds **actual official Dart analyzer evidence** by running the Dart SDK supplied with **Flutter 3.47.3**, pinned to the same Flutter version and action commit as existing `Development checks`.

This is a supplemental independently readable report, not a substitute for `flutter analyze`, unit tests, Flutter builds or qualified security reviews.

## How it runs

`.github/workflows/quality-engine-v24b-official.yml` runs on relevant changes to `lib/`/tool/analyzer configuration, manual invocation and best-effort daily schedule (07:23 UTC).

1. Checkout with `persist-credentials: false`; job permissions: **`contents: read` only**.
2. Setup `subosito/flutter-action@1a449444c387b1966244ae4d4f8c696479add0b2` (v2.23.0) with `flutter-version: "3.47.3"`, matching the official Development CI.
3. Resolve project dependencies and localization with `flutter pub get` + `flutter gen-l10n`.
4. Capture **`flutter --version --machine`** and **`dart analyze --format=json lib`**. Preserve the Dart analyzer exit code even when diagnostics make the command nonzero. Raw stdout/stderr and tool-version JSON remain local to the workflow; they are **never uploaded**.
5. Run `tool/quality_engine_v24b_official.py` to verify analyzer schema, real Flutter/Dart SDK identity, rule codes, source paths restricted to `lib/**/*.dart`, numeric locations, diagnostic uniqueness and exact source commit.
6. Upload **only** `quality-v24b-dart-evidence` JSON artifact (14 days) with rule IDs, issue severity, relative file/line/column, normalized statuses and tool revision. No diagnostic `problemMessage`, `correctionMessage`, documentation URLs or source excerpts.

A malformed/missing analyzer response or wrong tool version is **fail closed**. An unexpected nonzero analyzer exit without findings is marked `TOOL_FAILURE` and fails the job; a nonzero exit **with valid diagnostics** remains inspectable `ANALYZED_WITH_FINDINGS`, not erased as a job setup failure. The existing Development CI independently enforces its own `flutter analyze` gate.

## Structured report semantics

- `status`: `ANALYZED_CLEAN` / `ANALYZED_WITH_FINDINGS` / `TOOL_FAILURE`
- `qualityGate`: `CLEAN`, `REVIEW_ONLY`, `BLOCKING_FINDINGS`, `INCOMPLETE`.
- `counts`: `ERROR`, `WARNING`, `INFO`, originating from the official Dart analyzer.
- `toolVersions`: pinned Flutter version `3.47.3`, actual Dart SDK version and Flutter framework commit revision.
- `readOnly=true`, `selfRepairEnabled=false`, `certification=NOT_CERTIFIED`, `humanApprovals=0`.

A clean Dart analyzer result covers the declared `lib/` scope. It is not a security certification, proof of feature correctness, runtime tests, or coverage of all native code.

## Coverage caveats and roadmap

Cooking Anime does not track an Android project in Git; the Flutter CI generates the platform scaffold. Therefore **Android lint, Gradle dependency resolution and Kotlin compiler findings are not claimed** by v2.4-B. The v2.4-A output explicitly reports missing Kotlin/Gradle/Android manifest scopes.

- **v2.4-C:** pilot against a real Kotlin/Android repository and add a pinned native Android lint/Gradle capture adapter with independent artifact evidence.
- **L2.1:** separately gated deterministic Dart formatting or similarly mechanical fixes using isolated branch + **draft PR**, no auto-merge.
- **L2.2:** optional model-assisted diagnosis behind cost/security approvals and independent tests.
- **v3.0:** promotion to a multi-app service, with isolated repository permissions, scoped adoption of Core Golden Rules and durable metrics.

No autonomous edits to app code, no billing, recipes, culinary safety approvals, data migrations, signing, release changes, or general auto-merge.

## Acceptance gate

PR exact-head quality-v2 three lanes, v2.4-A static-review-leads, Development `validate` & `materialize-recipe-content`, and new **official-dart-evidence** must all complete with `SUCCESS`. No unresolved review threads; no branch-protection bypass. After merge, verify normalizer and report are on `main` and the new workflow runs on the main commit; do not claim that the best-effort cron has fired until a real `schedule` event is observed.

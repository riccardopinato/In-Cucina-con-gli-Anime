# R1 Quality Engine v2.1 — longitudinal history and lifecycle

**State:** code candidate / exact-head CI required. **Date:** 30 October 2026.
Factory baseline reused: `174a05e165076c9e4b2d61a20acd85ca6b215f12` (Master v27 ACTIVE / Golden Index v23). Do not modify App-Factory-Core or weaken AppLab SELF_CANARY.

## Why this change exists

v2.0 repeats the same source-bound code/content/workflow scan but cannot distinguish a new issue from an old one. v2.1 adds a **portable Python-standard-library history adapter**, without expanding write permissions or promoting any candidate to a verified defect. No model/LLM dependency is introduced.

## Inputs, lifecycle, and invariants

1. Each existing v2 lane scans its own current checkout and exports `build/quality-v2/{mode}.json`.
2. The read-only GitHub Actions adapter inspects **successful runs of the same workflow on `main` only**, selecting the latest unexpired `quality-v21-state-{mode}` artifact. PR artifacts are deliberately excluded. The token only has `actions: read` and `contents: read`.
3. A new `tool/quality_engine_v21_history.py` validates the original report, historical repository/mode/profile, ruleset version, configured path scope, immutable source SHA and bounded JSON schema before comparing finding IDs. Missing baselines are **explicitly `ABSENT`**; corrupt/mismatched baselines **fail** rather than quietly claiming fixes.
4. States: `UNBASELINED` on a first observation, then `NEW`, `PERSISTING`, `RESOLVED` and `REOPENED`. Each finding retains first-seen/last-seen source SHA and observation count. `RESOLVED` means **no longer detected by the complete current scanner under identical rules**, not proof the application is safe.
5. Every lane independently uploads `quality-v21-state-{mode}` and `quality-v21-delta-{mode}` JSON artifacts, plus its unchanged `quality-v2-{mode}` report; retention: **14 days**. A cumulative snapshot is carried forward on each successful run; if no baseline survives, history starts over with `UNBASELINED`.
6. Scans with skipped files, duplicated finding IDs, malformed provenance, changed scanner version or changed path configuration refuse comparison to avoid false "resolved". Files and snippets are not copied into history beyond the sanitized findings already present in v2.

**This is durable history across consecutive successful GitHub runs, not indefinite storage**. After a >14-day inactivity/retention gap, or an invalidating ruleset change, the history needs rebaselining. No database, commits, issues, PR writes or secrets outside the read-only GitHub token are required.

## Commands

```bash
python3 tool/quality_engine_v2.py --mode code --output build/quality-v2/code.json
python3 tool/quality_engine_v21_history.py \
  --report build/quality-v2/code.json \
  --config .quality-engine-v2.json \
  --repository riccardopinato/In-Cucina-con-gli-Anime \
  --run-id local-test \
  --event workflow_dispatch \
  --out-delta build/quality-v21/delta.json \
  --out-state build/quality-v21/state.json
python3 -m unittest tool.tests.test_quality_engine_v21_history -v
```

To compare a second run, add `--previous path/to/previous/state.json`. This is a **report-only** interface. Never pass an unverified report as professional certification.

## Reuse contract for App Factory Core

- This v2.1 file imports **only the Python standard library**. The GitHub adapter is a separate workflow; app-specific source scope remains `.quality-engine-v2.json`. The Core repository is not modified.
- Extract scanner adapters and versioned longitudinal state only after independent multi-app pilots, a reviewed Core Golden proposal and measured false-positive/noise rates.
- Future permanent multi-repository history could live in dedicated central immutable storage with retention and access policies; GitHub Actions artifact history alone is **not** that system.

## Medium/long-term autonomy: proposed gated tiers

| Tier | Privilege | Safe application |
| --- | --- | --- |
| L0 Observer (implemented) | Code/content scans and longitudinal reports | Read-only, scheduled and parallel |
| L1 Diagnoser | Evidence-backed triage with proposed remediation | No code mutations or certification |
| L2 Draft repair | Sandbox changes on isolated branch, **draft PR only** | Strict path allowlists, max diff/attempts, tests, human sign-off |
| L3 Bounded automerge | Optional for specifically approved low-risk repair classes | Independent CI/reviews, branch rules, quality gates, rollback and audit; no bypass |
| L4 Protected actions | Security/identity, data migration, payments, editorial food safety, store release | Do not grant blanket autonomous authority; require domain-specific authorization and evidence |

**Not implemented in v2.1:** L1–L4 remediation, self-repair agents, PR creation, branch writes, automatic merges, automatic product releases, billing/store configuration, food-safety approvals, cross-app modification or paid AI inference.

## Exit gate

Do not merge until exact-head `Development checks` + all `observe-*` jobs on the quality workflow are green, the new regression suite is green, reviewers resolved, no scope expansion/secret exposure. After merge confirm the default-branch three-job run, and **observe a later actual `schedule` run before claiming the hourly history loop empirically verified**.

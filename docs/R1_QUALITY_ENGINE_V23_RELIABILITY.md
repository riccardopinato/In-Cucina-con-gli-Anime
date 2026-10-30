# Quality Engine v2.3 — Autonomy Reliability Gate

**Project:** Cooking Anime, Quality Engine prototype.
**Factory baseline (pinned):** `174a05e165076c9e4b2d61a20acd85ca6b215f12` (Master v27 ACTIVE / Golden Index v23).
**Scope:** operational evidence and duplicate prevention. Not self-approving, not a new generic AI repair agent, not an AppLab SELF_CANARY promotion.

## Why

v2, v2.1 and v2.2 provide parallel scans, history and evidence-linked diagnosis. L2 adds a tightly restricted draft-only repair workflow. A successful CI on the L2 source does **not** prove that a scheduled invocation occurred or that the real GitHub token successfully opened a draft PR. v2.3 closes the operational-observability gap without inventing successful runs and makes the same unchanged defect idempotent across unrelated main commits.

## Deliverables

### A. Scheduled-run proof, not presumed coverage

- `tool/quality_engine_v23_reliability.py`: standard-library verifier consuming **actual GitHub workflow-run metadata**, filtering only `event=schedule` + `head_branch=main`; verifies timezone-aware timestamps, completion status and conclusion.
- Separate new `.github/workflows/quality-engine-v23-reliability.yml`: best-effort daily schedule at **08:17 UTC** and explicit manual dispatch, restricted to trusted `main`. It uses `actions:read` and `contents:read` only, retrieves GitHub API facts for `quality-engine-v2.yml` and `quality-engine-l2-draft.yml`, uploads `quality-v23-scheduler-health` (14-day JSON artifact) and writes human-readable GitHub Action summary.
- States: `NOT_YET_VERIFIED` (no actual scheduled run), `SCHEDULE_OBSERVED`, `SCHEDULE_STALE`, `RUNNING_OR_QUEUED` and `LAST_SCHEDULE_FAILED`. The app's hourly scan gets a 3-hour grace; daily L2 gets a 3-day grace. These are **observability thresholds**, not guarantees of scheduling.
- API failures and malformed metadata **fail**, not fabricated `HEALTHY`. Overall result can be `ATTENTION_REQUIRED` without pretending to certify that an autonomous PR was created.

### B. Repair fingerprint + duplicate prevention

- L2 plans gain a deterministic 24-hex `repairKey` hashed from repository, rule, policy fingerprint and paths with before/after SHA-256. It is **independent of the main source SHA**, while the plan still binds the exact source SHA for stale-work rejection.
- The L2 writer (which still runs **only** on scheduled or manually dispatched trusted `main` when a genuine allowed difference exists) fetches all historical pull-request branch refs via read-only `gh api --paginate` **before** opening a branch. Missing API permission/network returns a failure; unknown state never silently authorizes writes.
- If the identical fingerprint has already been proposed (even in a closed PR), the writer exits without creating a duplicate. If the stable branch already exists, it exits without overwriting or force pushing. Only an unseen, source-locked candidate may create a **draft PR**, never a merge.
- This is de-duplication by **exact before/after bytes and policy**, not an unconditional permanent ban on related future defects. Changing source bytes or policy produces a distinct key. L2 code/file scope and the absence of auto-merge remain unchanged.

### C. Local end-to-end qualification

`tool/tests/test_quality_engine_v23_reliability.py` includes 14 test cases:

1. No scheduled events despite successful push: NOT_YET_VERIFIED.
2. Verified successful hourly/daily scheduled events.
3. Failed scheduled event not masked by a successful push.
4. Stale scheduled evidence.
5. Queued/in-progress schedule not marked successful.
6. Bad/future timestamps and unsupported workflow rejected.
7. RepairKey stable across unrelated main commit.
8. Historical open/closed PR prevents duplicate.
9. Empty plan never authorizes a draft.
10. Tampered/foreign plan rejected.
11. Oversized/untrusted PR history rejected.
12. **Disposable local Git end-to-end:** source -> plan -> de-dup authorize -> branch -> apply -> exact diff -> commit -> return to intact main -> duplicate prevention.
13. Workflow invokes de-dup before `git switch`.
14. Reliability workflow remains read-only and never uses `pull_request_target`.

The full existing Development checks and original v2/v2.1/v2.2 Quality Engine workflow remain independent gates.

## Manual use

```bash
python3 -m unittest tool.tests.test_quality_engine_v23_reliability -v
python3 -m unittest discover -s tool/tests -p 'test_*.py'
```

Run the reliability workflow from GitHub Actions or wait for its configured schedule to produce **real metadata**. The scripts can also be exercised with synthetic, clearly labelled fixture JSON; synthetic test evidence must never be reported as proof of GitHub PR writing.

## Limitations and deferred work

- GitHub schedules are best-effort, subject to provider delay/skip. The daily reliability audit itself can also be delayed; GitHub's Actions page remains the system of record.
- The 14 tests prove the deterministic local Git repair path; **they do not prove the remote GitHub `GITHUB_TOKEN` can push/create PRs**. That requires a naturally occurring eligible L2 change or a separately authorized nonproduction repository canary. Never add an intentional bug to `main` just to trigger an action.
- GitHub Actions may suppress triggers from `GITHUB_TOKEN`-authored draft PRs. An independently triggered exact-head check/review remains necessary.
- This is not durable historical storage beyond the configured artifact retention (14 days). A separate central store and an alert/notification delivery channel can be assessed for a later milestone.
- L2 continues to touch only three fixed Quality Engine documentation files with whitespace-only-line formatting. Application Dart/Kotlin, Python runtime, Food Safety R1, 122 qualified reviews, content rights, billing, authentication, user data, CI configs and publishing remain out of scope.

## Exit criteria

1. PR merge only after exact-head `validate` and `materialize-recipe-content` plus all three independent `observe-*` checks **SUCCESS**, mergeability and zero unresolved code review.
2. CI proves 14 synthetic and local Git fixtures, not an invented remote draft.
3. After merge verify the new files and workflow on `main`, and at least one actual reliability health-report artifact.
4. Do not mark the **remote draft-writer pilot** as fully E2E PASS until GitHub has genuinely opened a reviewable draft for an eligible safe change.
5. Preserve R1 culinary PR #44 as DRAFT and all 122 human culinary reviews as PENDING. Keep Factory Core unchanged.

**Next planned slice:** v2.4 deeper Dart/Kotlin/Python/Android static analyzers using bounded evidence and version-pinned tools; only then L2.1 code-formatting draft repairs with separate approval gates.

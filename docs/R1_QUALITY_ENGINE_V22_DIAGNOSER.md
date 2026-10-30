# Quality Engine v2.2 — autonomously generated, evidence-linked diagnostic proposals

**Date:** 30 October 2026. **Stage:** L1 diagnoser, READ-ONLY, no app-side effects, no certifications.
Factory baseline pinned `174a05e165076c9e4b2d61a20acd85ca6b215f12` (Master v27 ACTIVE, Golden Index v23). AppLab remains SELF_CANARY; this module does **not** modify Factory Core or authorize auto-repair.

## Architecture and purpose

Building on v2 scanner and v2.1 historical lifecycle, a fourth, report-only step `tool/quality_engine_v22_diagnose.py` produces candidate remediation plans for each **currently detected** finding. It uses a strict, versioned, static rulebook (Python/Dart, GitHub Actions, recipe catalog). It is not an LLM and does not claim deep semantic understanding or factual food-safety validation.

Workflow per mode:

```text
code | content | workflows  (3 parallel independent lanes)
    v2 scan -> source-bound v2.1 history/delta
            -> v2.2 rulebook diagnosis and evidence/provenance gate
            -> JSON artifact (suggestions only)
```

One `quality-v22-proposals-{code,content,workflows}` artifact is uploaded per lane, retained for 14 days. This does not change existing v2/v2.1 outputs or the workflow's read-only GitHub permissions. Workflow triggers remain PR, push, best-effort hourly schedule and manual dispatch. No external AI, payment, backend, credentials beyond the existing read-only GitHub token, file edits or network calls from the diagnoser.

## Structured proposal fields

Each actionable `NEW`, `PERSISTING`, `REOPENED` or `UNBASELINED` finding includes:

- stable historical finding ID and current scanner ID, rule, severity, mode, **exact head SHA**, path/line and safe entity reference;
- transition and **candidate** priority P0/P1/P2; these signify triage urgency, **not** confirmed vulnerabilities or food-safety risk;
- static cause hypothesis, investigation plan, expected validation, independent reviewer role;
- `diagnosisStatus=HYPOTHESIS_NOT_VALIDATED`, `reviewDecision=PENDING_HUMAN_REVIEW`, `patch=null`, `autoFixEligible=false`, `approvalEvidence=null`.

`RESOLVED` entries are counted but never receive fix instructions; a resolved scanner finding is not proof of application safety. Unsupported rule IDs are clearly identified as `UNSUPPORTED_RULE` with **no invented code change** and a manual rule-adapter review.

Before producing output, the adapter checks exact `repository`/mode/profile/commit/scope of the report and history delta, verifies every active finding against an original v2 scanner record, verifies counts and duplicate IDs, rejects incomplete scans and unsafe policy. It never copies scanned source excerpts or dynamic source messages into proposals; unclear/free-text entity references are hashed.

## Manual execution

From repository root:

```bash
python3 tool/quality_engine_v2.py --mode content --output build/quality-v2/content.json
python3 tool/quality_engine_v21_history.py \
  --report build/quality-v2/content.json --config .quality-engine-v2.json \
  --repository riccardopinato/In-Cucina-con-gli-Anime \
  --run-id manual-1 --event workflow_dispatch \
  --out-delta build/quality-v21/delta.json \
  --out-state build/quality-v21/state.json
python3 tool/quality_engine_v22_diagnose.py \
  --scan build/quality-v2/content.json \
  --delta build/quality-v21/delta.json \
  --config .quality-engine-v2.json \
  --output build/quality-v22/proposals-content.json
python3 -m unittest tool.tests.test_quality_engine_v22_diagnose -v
```

## Scope and limitations

- Prior 33 content *review leads* from v2 are candidates, not 33 confirmed defects. The new diagnosis may propose specialist checks for dependent preparation times or uncooked egg use, **not** automatically edit recipes or approve the 122 outstanding R1 culinary reviews. PR #44 must remain DRAFT.
- Findings are rule/heuristic-based. `0` for code or workflow means none of **the implemented rules** triggered, not zero defects.
- This is not a production-ready self-healing code agent. It neither executes a patch nor runs a model with repository write access; no automatic branches, draft PRs, merges, or deployment.
- If a scanner adds a new rule, v2.2 reports `UNSUPPORTED_RULE` until a specific reviewed adapter exists. The dynamic source text is not treated as instructions.

## Planned controlled autonomy

- **L0 completed:** recurring parallel read-only audits.
- **L1 (v2.2):** automatic, evidence-linked diagnosis and specific review suggestions.
- **L2 future, not authorized here:** sandbox writer with scoped allowlisted low-risk files/operations and a **draft PR**; no direct main writes. Independent test/CI, protected paths and a review/rollback plan are required.
- **L3 future, separate authorization:** limited classes of fixes can eventually auto-merge **only** when independent security/CI/review and branch protection permit. No self-approval, disabling failing tests or rolling past a failing check.
- **High-risk protected:** auth, security boundaries, billing, data migrations, source/editorial food-safety, translations, releases, signing, rights, and Factory Core governance need domain-specific evidence/approval; no blanket autonomous merger.

Future extraction to App-Factory-Core requires a separately reviewed Golden adoption and pilots across different language stacks. The app repository currently owns these scanners; App Factory Core remains untouched.

## Acceptance gate

Exact head CI green on v2/v2.1/v2.2 three lanes, Development checks pass (including Python test suite, Flutter Web and Android), Codex review threads resolved, PR mergeable, deterministic source-bound proposals, no secrets/excerpts, and correct state migration. Record the squash merge on main and the first main workflow run before calling the v2.2 observer deployed. Never claim the cron actually fired without a `schedule` event.

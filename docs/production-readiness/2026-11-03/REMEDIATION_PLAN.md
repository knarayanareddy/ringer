# ringer remediation plan

Proposed work only; pair with the [review](REVIEW.md). This roadmap is repo-scoped and does not treat the collection as one product.

## Phase gates

| Phase | Entry gate | Exit gate |
| --- | --- | --- |
| P0 Baseline and scope | Review accepted; owner names target workspace(s) | Submission boundary, excluded workspaces, and sampled commands are documented without implying runtime proof |
| P1 Confirmed defects | P0 complete | AccessHold policy defects from RNG-1 and RNG-2 are fixed with negative tests that fail before the fix |
| P2 Risk-based security and evidence | P1 complete | Verification thresholds, fixture/live boundaries, and claim wording are aligned to observed behavior |
| P3 Meaningful automation | P2 complete | Each owner-selected workspace has explicit, reproducible gates tied to that workspace only |
| P4 Release and recovery | P3 complete | Workspace-specific release, rollback, and recovery evidence exists for the chosen candidate only |
| P5 Independent acceptance | P4 complete | An independent reviewer accepts the exact release candidate and records unresolved limits |

## Independent acceptance roles

All five disciplines need named acceptance owners before release sign-off:

| Role | Must inspect | Acceptance output |
| --- | --- | --- |
| Correctness/code review reviewer | RNG-1/RNG-2 fixes, changed policy logic, and linked contract semantics | Confirms behavior matches code and findings are actually addressed |
| Automation/testing reviewer | Negative tests for `exists` and `verification_level`, plus workspace gate matrix | Confirms tests fail on deliberate regressions and cover the chosen workspace |
| OWASP/security reviewer | Evidence-strength policy, fixture/live boundary handling, and any `live_rebook` path | Confirms hard constraints cannot pass on unverified evidence |
| DevOps/operations reviewer | Workspace-specific release, rollback, recovery packet, and exact executed gate evidence | Confirms candidate identity, rollback path, and recovery record are complete |
| UI/UX/accessibility reviewer | Shared UI evidence plus any chosen workspace UX/runtime limitations | Confirms static UI checks are not being misrepresented as runtime accessibility proof |

## Tasks

### RNG-T1 — Fix repo scope and candidate ownership (links: RNG-3)

**Prerequisites:** none.  
**Observed paths:** `README.md:3-16`, `README.md:39-61`, `specs/ui/package.json:5-10`, `evidence/ringer/snapshot.json:449-450`.  
**Owner roles:** product owner, tech lead.

1. Name the exact workspace or workspaces in scope for the next milestone and explicitly list excluded workspaces.
2. Rewrite any repo-level milestone, publication, or QA text so it speaks in workspace-specific terms and does not convert static UI validation into runtime evidence.
3. Record which commands are only planned, which checks are historically claimed, and which results are newly observed for the selected workspace.

**Expected output:** a candidate-scope memo or release checklist that distinguishes portfolio, workspace, static validation, and runtime evidence.  
**Verification:** an independent reviewer can tell which workspace is in scope without inferring from the repo name.  
**Definition of done:**

- [ ] In-scope and out-of-scope workspaces are named.
- [ ] Repo-level claims no longer imply one unified product runtime.
- [ ] Static UI validation is labeled as non-runtime evidence.

### RNG-T2 — Repair AccessHold predicate semantics (links: RNG-1)

**Prerequisites:** RNG-T1; owner confirms AccessHold remains an in-scope slice.  
**Observed paths:** `projects/accesshold/packages/contracts/src/index.ts:22-27`, `projects/accesshold/packages/policy-engine/src/index.ts:73-76`, `projects/accesshold/packages/policy-engine/src/index.ts:124-131`.  
**Proposed implementation/test paths:** `projects/accesshold/packages/policy-engine/src/index.ts`, `projects/accesshold/tests/unit/policy-engine.test.ts`, and, if needed, contract-fixture examples under `projects/accesshold/examples/`.

1. Define the intended truth table for `exists` predicates: present value, null value, missing feature, and explicit "must not exist" behavior.
2. Change the evaluator so existence checks are resolved directly from feature presence semantics instead of returning a status derived only from the expected boolean.
3. Add negative and regression tests that fail when a missing feature is reported as satisfied or when a presence check cannot distinguish absence from type/value mismatch.

**Expected output:** corrected predicate semantics plus tests proving the old behavior was wrong.  
**Verification:** deliberately reintroduce the old `status: expected ? "satisfied" : "violated"` logic and confirm at least one new test fails.  
**Definition of done:**

- [ ] `exists` behavior is specified in code comments or contract docs.
- [ ] Missing, present, and forbidden-presence cases have explicit tests.
- [ ] A broken reversion of the old logic causes failing tests.

### RNG-T3 — Enforce evidence verification thresholds in AccessHold (links: RNG-2)

**Prerequisites:** RNG-T2.  
**Observed paths:** `projects/accesshold/packages/contracts/src/index.ts:9-12`, `projects/accesshold/packages/contracts/src/index.ts:55-65`, `projects/accesshold/packages/policy-engine/src/index.ts:178-196`.  
**Proposed implementation/test/document paths:** `projects/accesshold/packages/policy-engine/src/index.ts`, `projects/accesshold/content/feature-registry/v1.json`, `projects/accesshold/tests/security/policy-boundaries.test.ts`, `projects/accesshold/docs/validation.md`.

1. Decide the minimum acceptable `verification_level` for each policy-sensitive feature or for each constraint priority tier, with owner approval for any live-action path.
2. Extend policy evaluation so `unverified` evidence cannot satisfy a requirement that needs stronger evidence, and ensure failures are surfaced as stable non-sensitive codes.
3. Add tests covering at least three cases: unverified evidence rejected, documented evidence accepted where allowed, and provider-confirmed evidence accepted for the strictest path.

**Expected output:** policy logic and registry/docs tying evidence strength to authorization decisions.  
**Verification:** mutate a fixture so only `unverified` evidence is available for a hard constraint and confirm the evaluation fails closed.  
**Definition of done:**

- [ ] Verification-level policy is written down, not implied.
- [ ] Hard constraints cannot pass solely on unverified evidence where stronger proof is required.
- [ ] Security tests fail when verification checks are removed.

### RNG-T4 — Build meaningful workspace-specific gates (links: RNG-3, preventive)

**Prerequisites:** RNG-T1; preferably RNG-T2 and RNG-T3 for AccessHold if that workspace is selected.  
**Observed paths:** `README.md:19-37`, `projects/accesshold/package.json:10-18`, `projects/curiolab/package.json:10-18`, `projects/roomsmith/package.json:10-18`, `projects/harvestgrid/pyproject.toml:1-48`, `projects/nexttime/pyproject.toml:1-45`, `specs/ui/package.json:6-10`.  
**Proposed paths:** workspace-local CI or validation manifests, workspace release checklist, and per-workspace evidence records.

1. For each selected workspace, define the exact required gates from existing manifests first: lint/type/build/unit/contract/security/content validation as applicable.
2. If a required gate lacks a verified script, add the script to that workspace before adding CI around it; do not invent success criteria in a release note.
3. Separate static spec/UI checks from executable application or package checks so the final evidence bundle shows what was actually validated.

**Expected output:** a workspace gate matrix and reproducible validation path for the chosen candidate.  
**Verification:** intentionally break one selected workspace's contract or type boundary and confirm the mapped gate fails for that workspace without relying on other workspaces' results.  
**Definition of done:**

- [ ] Every selected workspace has an explicit gate list.
- [ ] Static design validation is not the only evidence for user-facing quality.
- [ ] A deliberate defect in one workspace fails that workspace's gate.

### RNG-T5 — Release, rollback, recovery, and independent acceptance per selected workspace (preventive)

**Prerequisites:** RNG-T4; owner selects a release candidate.  
**Observed paths:** `README.md:15-16`, `README.md:27-37`, `projects/accesshold/packages/contracts/src/index.ts:83-93` for live-action sensitivity.  
**Proposed paths:** workspace-specific `docs/release.md`, `docs/recovery.md`, synthetic fixtures under `tests/fixtures/`, and acceptance records under `evidence/`.

1. Define a release packet for the chosen workspace: pinned revision, locked dependency set, exact validation evidence, owner approvals, and explicit unsupported conditions.
2. Rehearse rollback and recovery with synthetic data or fixture content appropriate to that workspace; record what was restored, from where, and by whom.
3. Ask the five named independent reviewers to repeat the acceptance script against the exact candidate and record pass/fail plus unresolved limits instead of summary adjectives.

**Expected output:** workspace-specific release runbook, rollback path, recovery evidence, and independent acceptance record.  
**Verification:** an independent reviewer can identify the exact candidate, repeat the acceptance checklist, and reject it if the evidence does not match observed behavior.  
**Definition of done:**

- [ ] Release evidence names one workspace and one pinned revision.
- [ ] Rollback and recovery steps are documented and observed with synthetic or fixture-safe data.
- [ ] Independent acceptance is signed off with explicit limits, not implied readiness.

## Task dependency map

| Task | Depends on | Why |
| --- | --- | --- |
| RNG-T1 | None | Prevents all later work from treating the collection as one product. |
| RNG-T2 | RNG-T1 | AccessHold repair only matters if that slice is still in scope. |
| RNG-T3 | RNG-T2 | Verification rules should land after predicate semantics are corrected. |
| RNG-T4 | RNG-T1, and preferably RNG-T2/RNG-T3 for AccessHold | Gates should reflect the real candidate and include repaired policy logic where applicable. |
| RNG-T5 | RNG-T4 | Release/recovery/acceptance should run only on the gated candidate. |

## Owner approvals required

- Scope selection: which workspace(s) are actually pursuing release or submission.
- Any use of live-action semantics such as `live_rebook`.
- Minimum acceptable evidence-verification thresholds for policy decisions.
- Recovery objective per workspace: fixture replay, synthetic-content restore, or staged rollback.
- Any public wording summarizing aggregate repo maturity.

## Release, rollback, and recovery policy

Release only from a single named workspace and pinned revision after its own gates pass. Do not publish a collection-wide "ready" statement from README counts or static UI audits. Roll back to the previous independently accepted candidate for that workspace. Recovery evidence must use synthetic or fixture-safe data and record who performed the recovery, what artifact or fixture was used, and what state was restored. If any policy path still accepts unverified evidence, that workspace does not pass security acceptance.

## Independent acceptance checklist

- [ ] The accepted candidate is one named workspace at one pinned revision.
- [ ] RNG-1 and RNG-2 are either fixed and regression-tested or explicitly accepted as open blockers.
- [ ] The evidence bundle separates static design validation, source-level tests, and any runtime observations.
- [ ] Release notes list unsupported environments, integrations, and blocker dependencies.
- [ ] Rollback and recovery were observed for the selected workspace, not inferred.
- [ ] Correctness/code review reviewer signs off on observed behavior and unresolved limits separately.
- [ ] Automation/testing reviewer signs off on observed behavior and unresolved limits separately.
- [ ] OWASP/security reviewer signs off on observed behavior and unresolved limits separately.
- [ ] DevOps/operations reviewer signs off on observed behavior and unresolved limits separately.
- [ ] UI/UX/accessibility reviewer signs off on observed behavior and unresolved limits separately.

# AccessHold validation record

Recorded 2026-10-23 on the local vertical-slice branch. Evidence is limited to deterministic source behavior and synthetic fixtures.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier, including `services/` | Passed |
| TypeScript strict typecheck | Passed |
| Unit tests | 22/22 passed: 12 policy, 5 manual-contract, and 5 ReferenceTravel-monitor tests |
| Canonical schema/contract tests | 6/6 passed; schema copy byte-identical |
| Policy/security tests | 2/2 passed |
| npm audit, moderate and above | No known vulnerabilities |
| TypeScript build | Passed |
| Fixture walking path | Draft import, explicit activation, violation/recovery fixture pages, completed case timeline, JSON repository reopen, four versions; no monitoring worker running |
| **Total tests** | **30/30 passed** |

The manual fixture service validates schema, semantics, registered predicates, traveler scope, and fixture provenance. Tests cover draft correction, optimistic versions, stale approval rejection, known-violation rejection, append-only history, cross-traveler denial, live-document rejection, and reopening through a new file-repository instance. Corrections cannot silently reclassify live input as a fixture.

The explicitly requested ReferenceTravel fixture pages exercise safe change, hard-constraint violation, recovery, immutable asset/evidence versions, and deterministic re-evaluation. Additional tests cover duplicate and conflicting replays, lower-sequence stale events, equivalent-change attachment, degraded recovery remaining open, a new case after completion, malformed/live-looking evidence, and repository-append failure without phantom history. Duplicate event IDs and the recovery-case index are in-memory; their process-restart durability is not implemented or claimed.

The JSON repository uses a mode-0600 temporary file and atomic rename for synthetic local contract data. This proves a normal repository reopen, not crash durability, concurrent-writer safety, or encrypted production storage.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

Or run all five independent projects from the repository root with `scripts/validate-foundations.sh` after each project has been bootstrapped.

## Not evidenced

No TypeScript coverage percentage is claimed. No live Alexa+/MCP, SES, Bedrock, travel provider, calendar, email import, production database, external-action idempotency, scheduled/live monitoring worker, independent replacement-confirmation import, deletion, accessibility participant, performance, deployment, or release behavior was executed. The hotel-room fixture does not satisfy the aircraft/dependent-transfer scenario, and local case completion performs no booking or calendar update. Integration/E2E/infrastructure/deploy targets remain intentionally blocked.

This record supports only the linked local traceability rows. It does not satisfy the specification's build-complete gate or guarantee physical accessibility.

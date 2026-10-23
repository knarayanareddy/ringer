# AccessHold validation record

Recorded 2026-10-23 on the local vertical-slice branch. Evidence is limited to deterministic source behavior and synthetic fixtures.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck | Passed |
| Unit tests | 17/17 passed: 12 policy tests and 5 manual-contract tests |
| Canonical schema/contract tests | 6/6 passed; schema copy byte-identical |
| Policy/security tests | 2/2 passed |
| npm audit, moderate and above | No known vulnerabilities |
| TypeScript build | Passed |
| Fixture walking path | Draft import, explicit activation, JSON repository reopen, two versions; monitoring worker not running |
| **Total tests** | **25/25 passed** |

The manual fixture service validates schema, semantics, registered predicates, traveler scope, and fixture provenance. Tests cover draft correction, optimistic versions, stale approval rejection, known-violation rejection, append-only history, cross-traveler denial, live-document rejection, and reopening through a new file-repository instance. Corrections cannot silently reclassify live input as a fixture.

The JSON repository uses a mode-0600 temporary file and atomic rename for synthetic local data. This proves a normal repository reopen, not crash durability, concurrent-writer safety, encrypted production storage, or a monitoring worker.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

Or run all five independent projects from the repository root with `scripts/validate-foundations.sh` after each project has been bootstrapped.

## Not evidenced

No TypeScript coverage percentage is claimed. No live Alexa+/MCP, SES, Bedrock, provider, calendar, email import, production database, external-action idempotency, monitoring poll, deletion, accessibility participant, performance, deployment, or release behavior was executed. Integration/E2E/infrastructure/deploy targets remain intentionally blocked.

This record supports only the linked local traceability rows. It does not satisfy the specification's build-complete gate or guarantee physical accessibility.

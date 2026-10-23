# AccessHold validation record

Recorded 2026-10-23 on the local foundation branch. Evidence is limited to source-level deterministic behavior and fictional fixtures.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck | Passed |
| Unit tests | 12/12 passed |
| Canonical schema/contract tests | 6/6 passed; schema copy byte-identical |
| Policy/security tests | 2/2 passed |
| npm audit, moderate and above | No known vulnerabilities after dependency updates |
| TypeScript build | Passed |
| Fixture walking path | Passed; fixture provenance remains explicit |
| **Total tests** | **20/20 passed** |

The fixture exercised supported unit normalization, hard-constraint evaluation, stale-evidence handling, and recovery completion rules. It did not contact a provider. The output notice states that workflow evidence is not a physical-accessibility guarantee.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

Or run all five independent foundations from the repository root with `scripts/validate-foundations.sh` after each project has been bootstrapped.

## Not evidenced

No TypeScript coverage percentage is claimed. No live Alexa+/MCP, SES, Bedrock, provider, calendar, persistence, idempotent external action, authorization, deletion, accessibility participant, performance, deployment, or release behavior was executed. Integration/E2E/infrastructure/deploy targets remain intentionally blocked.

This record supports only the linked local traceability rows. It does not satisfy the specification's build-complete gate.

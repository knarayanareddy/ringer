# RoomSmith validation record

Recorded 2026-10-23 on the local foundation branch. Evidence covers pure Kotlin/TypeScript source and synthetic observations only.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck + Kotlin main/test compilation | Passed |
| TypeScript graph/fallback unit tests | 6/6 passed |
| Kotlin puzzle-engine tests | 13/13 passed |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Content-publication security test | 1/1 passed |
| npm audit, moderate and above | No known vulnerabilities after dependency updates |
| TypeScript build + Kotlin runtime JAR build | Passed |
| Draft content CLI | Valid in `draft-development` mode |
| Remote fixture walking path | Three puzzles committed through remote path; state sequence 3; no media in report |
| **Total tests** | **24/24 passed** |

Tests include short/stable holds, wrong relation and unknown object, open-palm thresholds, calibration reset, missing candidates, stale observations, ordered steps, standard timeout, no-timing mode, remote answer/state checks, duplicate solutions, and resume idempotency.

The publication CLI was run with `--publish` and correctly exited nonzero for missing game-design/safety/accessibility reviews, unapproved state, and placeholder graph/asset hashes.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
corepack pnpm validate:content
corepack pnpm validate:content -- --publish   # expected to fail for this draft
```

## Not evidenced

No Kotlin/TypeScript coverage percentage or performance/false-accept campaign is claimed. No Fire TV, companion, camera/perception, WebRTC/TURN, persistence, signed content, full solver, rendered accessibility path, physical playtest, offline app run, deployment, or release gate was exercised. State reconstruction and remote fixture completion are not device or offline-application evidence.

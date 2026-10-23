# RoomSmith validation record

Recorded 2026-10-23 on the local vertical-slice branch. Evidence covers pure Kotlin/TypeScript source and synthetic observations/selections only.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck + Kotlin main/test compilation | Passed |
| TypeScript graph/fallback unit tests | 6/6 passed |
| Kotlin puzzle-engine tests | 18/18 passed |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Content-publication security test | 1/1 passed |
| npm audit, moderate and above | No known vulnerabilities |
| TypeScript build + Kotlin runtime JAR build | Passed |
| Draft content CLI | Valid in `draft-development` mode |
| Remote fixture walking path | Ordered three-puzzle completion, timed remote hold, authored hint, snapshot reconstruction, metadata-only report |
| **Total tests** | **29/29 passed** |

The remote coordinator enforces authored puzzle order and answers, requires the 750 ms shield hold in standard mode, permits single-selection shield completion in no-timing mode, and keeps authored hints separate from puzzle transitions. The case-report type contains episode/version, completion metadata, hint levels, and supplied active time only; it has no room-media fields.

The publication CLI was run with `--publish` and correctly exited nonzero for missing game-design/safety/accessibility reviews, unapproved state, and placeholder graph/asset hashes.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
corepack pnpm validate:content
corepack pnpm validate:content -- --publish   # expected to fail for this draft
```

## Not evidenced

No Kotlin/TypeScript coverage percentage or performance/false-accept campaign is claimed. Snapshot reconstruction is in-memory, elapsed active time is fixture input, and the report is not rendered. No Fire TV, companion, camera/perception, WebRTC/TURN, durable persistence, signed content, full solver, rendered accessibility path, physical playtest, offline application run, deployment, or release gate was exercised.

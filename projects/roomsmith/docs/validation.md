# RoomSmith validation record

Recorded 2026-10-23 on the local vertical-slice branch. Evidence covers pure Kotlin/TypeScript source and synthetic observations/selections only.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck + Kotlin main/test compilation | Passed |
| TypeScript graph/fallback unit tests | 6/6 passed |
| Kotlin puzzle-engine tests | 21/21 passed |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Content-publication security test | 1/1 passed |
| npm audit, moderate and above | No known vulnerabilities |
| TypeScript build + Kotlin runtime JAR build | Passed |
| Draft content CLI | Valid in `draft-development` mode |
| Remote fixture walking path | Ordered three-puzzle completion, timed remote hold, authored hint, two atomic fixture-file saves/reopens, metadata-only report |
| **Total tests** | **32/32 passed** |

The remote coordinator enforces authored puzzle order and answers, requires the 750 ms shield hold in standard mode, permits single-selection shield completion in no-timing mode, and keeps authored hints separate from puzzle transitions. The case-report type contains episode/version, completion metadata, hint levels, and supplied active time only; it has no room-media fields.

The value-only snapshot store uses a versioned bounded binary format, SHA-256 integrity checks, atomic replacement, and semantic remote-state validation. Tests prove reopen through a new store/session with retained hints, completions, and active time; unchanged-state byte determinism; rejection of malformed/checksum/trailing/camera-bearing state; and preservation of the prior file after invalid saves. Transient hold starts are deliberately not persisted, and a reopen test proves the full hold duration cannot be bypassed. Walking/test directories are removed.

The publication CLI was run with `--publish` and correctly exited nonzero for missing game-design/safety/accessibility reviews, unapproved state, and placeholder graph/asset hashes.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
corepack pnpm validate:content
corepack pnpm validate:content -- --publish   # expected to fail for this draft
```

## Not evidenced

No Kotlin/TypeScript coverage percentage or performance/false-accept campaign is claimed. Atomic fixture-file reopen is not an actual process-death/power-loss test; elapsed active time is fixture input, and the report is not rendered. No encrypted production storage, retention/deletion worker, Fire TV, companion, camera/perception, WebRTC/TURN, durable backend persistence, signed content, full solver, rendered accessibility path, physical playtest, offline application run, deployment, or release gate was exercised.

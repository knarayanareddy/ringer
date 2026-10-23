# CurioLab validation record

Recorded 2026-10-23 on the local foundation branch. Evidence covers pure Kotlin/TypeScript source and fictional content only.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck + Kotlin main/test compilation | Passed |
| TypeScript unit tests | 4/4 passed |
| Kotlin episode-engine tests | 10/10 passed |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Content-publication security test | 1/1 passed |
| npm audit, moderate and above | No known vulnerabilities after dependency updates |
| TypeScript build + Kotlin runtime JAR build | Passed |
| Draft content CLI | Valid in `draft-development` mode |
| Fixture walking path | Flat 3, folded 7, greater branch, exact values, sequence 4 |
| **Total tests** | **19/19 passed** |

The publication CLI was also run with `--publish` and correctly exited nonzero. It reported missing science/child-safety reviews, unapproved review state, and placeholder graph/asset hashes. This negative check is expected for the current draft.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
corepack pnpm validate:content
corepack pnpm validate:content -- --publish   # expected to fail for this draft
```

## Not evidenced

No Kotlin/TypeScript coverage percentage, frame-rate/latency measurement, physical count accuracy, process-persistence proof, or signed-bundle verification is claimed. No Fire TV, companion, camera, relay, AWS service, physical experiment, family participant, accessibility study, learning outcome, deployment, or release gate was exercised.

The fixture proves only deterministic state transitions over supplied values; it is not device or learning evidence.

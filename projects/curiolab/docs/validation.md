# CurioLab validation record

Recorded 2026-10-23 on the local vertical-slice branch. Evidence covers pure Kotlin/TypeScript source and fictional content only.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck + Kotlin main/test compilation | Passed |
| TypeScript unit tests | 4/4 passed |
| Kotlin episode-engine tests | 15/15 passed |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Content-publication security test | 1/1 passed |
| npm audit, moderate and above | No known vulnerabilities |
| TypeScript build + Kotlin runtime JAR build | Passed |
| Draft content CLI | Valid in `draft-development` mode |
| Fixture walking path | Manual consent, stop 5/correct to 4, folded 7, greater branch, reflection, snapshot reconstruction |
| **Total tests** | **24/24 passed** |

The manual coordinator requires safety/consent before predictions, an adult-marked stop before confirmation, and a confirmed count before result parameters or comparison. Duplicate stops/confirmations are idempotent, stale sequences and counts outside the episode's 0–30 bounds fail, and the final summary requires reflection and preserves a variable-change prompt rather than asserting a universal law.

The publication CLI was also run with `--publish` and correctly exited nonzero. It reported missing science/child-safety reviews, unapproved review state, and placeholder graph/asset hashes. This negative check is expected for the current draft.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
corepack pnpm validate:content
corepack pnpm validate:content -- --publish   # expected to fail for this draft
```

## Not evidenced

No Kotlin/TypeScript coverage percentage, frame-rate/latency measurement, physical count accuracy, durable process-persistence proof, or signed-bundle verification is claimed. Snapshot reconstruction is in-memory and is not a process-restart test. No Fire TV, companion, camera, relay, AWS service, physical experiment, rendered scene, family participant, accessibility study, learning outcome, deployment, or release gate was exercised.

The fixture proves deterministic state transitions over supplied values only.

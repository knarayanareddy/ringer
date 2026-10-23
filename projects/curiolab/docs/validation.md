# CurioLab validation record

Recorded 2026-10-23 on the local vertical-slice branch. Evidence covers pure Kotlin/TypeScript source and fictional content only.

## Passing checks

| Check | Result |
| --- | --- |
| ESLint + Prettier | Passed |
| TypeScript strict typecheck + Kotlin main/test compilation | Passed |
| TypeScript unit tests | 4/4 passed |
| Kotlin episode-engine tests | 17/17 passed |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Content-publication security test | 1/1 passed |
| npm audit, moderate and above | No known vulnerabilities |
| TypeScript build + Kotlin runtime JAR build | Passed |
| Draft content CLI | Valid in `draft-development` mode |
| Fixture walking path | Manual consent, stop 5/correct to 4, folded 7, greater branch, reflection, two atomic fixture-file saves/reopens through new stores/sessions |
| **Total tests** | **26/26 passed** |

The manual coordinator requires safety/consent before predictions, an adult-marked stop before confirmation, and a confirmed count before result parameters or comparison. Duplicate stops/confirmations are idempotent, stale sequences and counts outside the episode's 0–30 bounds fail, and the final summary requires reflection and preserves a variable-change prompt rather than asserting a universal law.

The versioned value-only snapshot format uses size/count limits, SHA-256 integrity checks, semantic validation, and atomic replacement. Tests prove deterministic bytes for an unchanged snapshot, reopen through a new store and session, continuation to the same measured summary, and fail-closed handling of bad magic/version/checksum, truncation, trailing bytes, and invalid state. Walking/test directories are removed.

The publication CLI was also run with `--publish` and correctly exited nonzero. It reported missing science/child-safety reviews, unapproved review state, and placeholder graph/asset hashes. This negative check is expected for the current draft.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
corepack pnpm validate:content
corepack pnpm validate:content -- --publish   # expected to fail for this draft
```

## Not evidenced

No Kotlin/TypeScript coverage percentage, frame-rate/latency measurement, physical count accuracy, actual process-death/power-loss recovery, encrypted production storage, retention/deletion worker, or signed-bundle verification is claimed. Atomic fixture-file reopen is not a production durability test. No Fire TV, companion, camera, relay, AWS service, physical experiment, rendered scene, family participant, accessibility study, learning outcome, deployment, or release gate was exercised.

The fixture proves deterministic state transitions and ordinary file reopen over supplied synthetic values only.

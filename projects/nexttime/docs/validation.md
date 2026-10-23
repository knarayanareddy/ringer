# NextTime validation record

Recorded 2026-10-23. Project tests, builds, fixture execution, and dependency audit ran under source-built CPython 3.12.12 with zlib, SQLite, and OpenSSL support; Python 3.11 was not substituted.

## Passing checks

| Check | Result |
| --- | --- |
| Ruff lint + format check | Passed |
| Strict mypy | Passed; 8 source files |
| Unit tests | 29/29 passed |
| Branch-aware domain coverage | 96.93%; required gate 90% retained |
| Canonical schema/contract tests | 6/6 passed; schema copy byte-identical |
| Privacy/security tests | 2/2 passed |
| Third-party dependency audit | No known vulnerabilities; editable local package skipped |
| Source distribution + wheel | Both built successfully |
| Fixture walking path | Consent-aware minimization, duplicate-source safety, and unconfirmed rubric outcome passed |
| **Total tests** | **37/37 passed** |

The synthetic transcript path excludes other-speaker and ambiguous turns, excludes other-speaker-like turns from self memos, applies narrow deterministic identifier redaction, and always returns `review_required`. Cached source references remain subject to consent and revocation checks. The source deletion deadline is computed as 24 hours after successful minimization; it is metadata for a future deletion adapter, not proof of deletion.

The rubric fixture still returns `partial`, `confirmation_required: true`, `required_confirmation_unresolved`, and `authentic_skill_update: false`. This is not a real learner outcome.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

Use a Python 3.12 runtime with zlib, SQLite, and SSL/TLS so the normal coverage and audit commands are self-contained. Do not skip the audit or run project tests under 3.11.

## Not evidenced

No Bee/Apple Watch data, CLI/MCP ingestion, diarization model, iOS behavior, authentic transcript, actual transient deletion, revocation worker, durable idempotent ingestion, database scan, rehearsal audio, ASR accent/device evaluation, participant outcome, performance, deployment, or release behavior was executed. The build-complete gate remains open.

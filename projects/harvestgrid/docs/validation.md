# HarvestGrid validation record

Recorded 2026-10-23. Project tests, builds, fixture execution, and dependency audit ran under source-built CPython 3.12.12 with zlib, SQLite, and OpenSSL support; Python 3.11 was not substituted.

## Passing checks

| Check | Result |
| --- | --- |
| Ruff lint + format check | Passed |
| Strict mypy | Passed; 6 source files |
| Unit tests | 26/26 passed |
| Branch-aware domain + matching coverage | 95.32%; required gate 90% retained |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Operational/security boundary test | 1/1 passed |
| Third-party dependency audit | No known vulnerabilities; editable local package skipped |
| Source distribution + wheel | Both built successfully |
| Fixture walking path | Approval, deterministic assignment, bounded location access, revocation, and post-cancellation denial |
| **Total tests** | **31/31 passed** |

The forecast remains `experimental`, `seasonal_baseline`, human-readiness-review-required, and visible-only. Internal-ripeness and food-safety inference remain false.

The in-memory operations slice requires owner and coordinator readiness approvals before deterministic proposals, requires coordinator assignment approval, supports idempotent multi-volunteer confirmation, and permits restricted-location return only to a confirmed assignee inside the explicit reveal window. Owner revocation cancels assignments and denies subsequent access. Tests cover hard filters, stale versions, unauthorized actors, stable ranking, duplicate transitions, invalid intervals, and empty location data. No notification is sent and no real address is used.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

Use a Python 3.12 runtime with zlib, SQLite, and SSL/TLS so the normal coverage and audit commands are self-contained. Do not skip the audit or run project tests under 3.11.

## Not evidenced

No Ring device/API/simulator, real observation, residential media, ROI/masking, weather, CV model, cultivar prior, operational forecast, model-quality result, actual invitation/notification, durable coordinator workflow, production location authorization, weighed glean, verified deletion, participant/pilot, performance, deployment, or release behavior was exercised. No operational forecast or trained model artifact exists.

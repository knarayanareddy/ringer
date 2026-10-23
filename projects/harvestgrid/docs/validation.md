# HarvestGrid validation record

Recorded 2026-10-23. Project tests, builds, fixture execution, and dependency audit ran under source-built CPython 3.12.12 with zlib, SQLite, and OpenSSL support; Python 3.11 was not substituted.

## Passing checks

| Check | Result |
| --- | --- |
| Ruff lint + format check | Passed |
| Strict mypy | Passed; 7 source files |
| Unit tests | 33/33 passed |
| Branch-aware domain + matching coverage | 92.78%; required gate 90% retained |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Operational/security boundary test | 1/1 passed |
| Third-party dependency audit | No known vulnerabilities; editable local package skipped |
| Source distribution + wheel | Both built successfully |
| Fixture walking path | Approval/assignment/revocation plus a separate coordinator-verified outcome, non-sensitive receipt, forecast evaluation, and closure |
| **Total tests** | **38/38 passed** |

The forecast remains `experimental`, `seasonal_baseline`, human-readiness-review-required, and visible-only. Internal-ripeness and food-safety inference remain false.

The in-memory operations slice requires owner and coordinator readiness approvals before deterministic proposals, requires coordinator assignment approval, supports idempotent multi-volunteer confirmation, and permits restricted-location return only to a confirmed assignee inside the explicit reveal window. Owner revocation cancels assignments and denies subsequent access. No notification is sent and no real address is used.

A separate confirmed-workflow branch records 10.0 kg gross, 8.5 kg net, 8.0 kg accepted, and 0.5 kg rejected with a coarse spoilage reason and fixture scale/evidence metadata. Coordinator verification produces one deterministic receipt and a single-outcome evaluation; duplicate entry/verification/closure does not create another version or receipt. The receipt export excludes volunteer, address/access, rejection, scale, and evidence-hash fields. The canonical forecast has no weight estimate, so the evaluation reports `forecast_weight_unavailable` and a visible-count absolute error of 2 rather than inventing a weight error. Automatic model promotion is false. Tests also cover non-null weight errors, undefined zero-weight percentage error, invalid weight arithmetic/evidence, authorization, stale versions, and immutable post-outcome state. They exposed and now regress the forecast validator's estimate/lower/upper unpacking order.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

Use a Python 3.12 runtime with zlib, SQLite, and SSL/TLS so the normal coverage and audit commands are self-contained. Do not skip the audit or run project tests under 3.11.

## Not evidenced

No Ring device/API/simulator, real observation, residential media, ROI/masking, weather, CV model, cultivar prior, operational forecast, model-quality result, actual invitation/notification, durable coordinator workflow, production location authorization, real weighed glean/donation, reviewed evaluation-set manifest, model training/promotion, verified deletion, participant/pilot, performance, deployment, or release behavior was exercised. The verified weights and receipt are synthetic in-memory values, and one outcome is not an evaluation set or model-quality claim. No operational forecast or trained model artifact exists.

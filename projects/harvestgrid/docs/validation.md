# HarvestGrid validation record

Recorded 2026-10-23. Project tests and builds ran under CPython 3.12.12; only the audit client used the separate SSL-capable system interpreter described in `preflight.md`.

## Passing checks

| Check | Result |
| --- | --- |
| Ruff lint + format check | Passed |
| Strict mypy | Passed; 5 source files |
| Unit tests | 18/18 passed |
| Branch-aware domain + matching coverage | 98.17%; required gate 90% retained |
| Canonical schema/contract tests | 4/4 passed; schema copy byte-identical |
| Operational/security boundary test | 1/1 passed |
| Third-party dependency audit | No known vulnerabilities after pytest update; editable local package skipped |
| Source distribution + wheel | Both built successfully |
| Fixture walking path | Passed |
| **Total tests** | **23/23 passed** |

The fixture remains `experimental`, `seasonal_baseline`, human-readiness-review-required, and visible-only. Internal-ripeness and food-safety inference remain false. Matching tests cover hard filters, deterministic scores, and stable seeded ties; they do not create assignments or invitations.

## Reproduce

```bash
make lint typecheck test-unit test-contract test-security build dev
```

An SSL-capable external `PIP_AUDIT` runner may target this project's 3.12 `site-packages` through `PIP_AUDIT_ARGS`; the audit must not be omitted.

## Not evidenced

No Ring device/API/simulator, real observation, residential media, ROI/masking, weather, CV model, cultivar prior, operational forecast, model-quality result, coordinator workflow, address reveal, participant/pilot, performance, deployment, or release behavior was exercised. No operational forecast or trained model artifact exists.

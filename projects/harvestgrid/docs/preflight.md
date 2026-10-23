# HarvestGrid preflight

Recorded 2026-10-23 for the initial local foundation. Project code and tests target Python 3.12; no operational media or model toolchain is implied.

## Available and exercised

| Capability | Recorded version/state |
| --- | --- |
| Project interpreter | Source-built CPython 3.12.12 with zlib and SQLite support |
| Package manager | uv 0.9.5; `uv.lock` is frozen for normal bootstrap |
| Quality tools | Ruff 0.13.2; mypy 1.18.2; pytest 9.0.3; pytest-cov 6.3.0 |
| Runtime dependencies | None for current domain/matching packages |
| Audit-only runner | System CPython 3.11.2 with OpenSSL 3.0.20, auditing the installed 3.12 site-packages |

The source-built 3.12 interpreter lacks SSL and several optional native modules. The recorded dependency audit used the separate SSL-capable runner against `.venv/lib/python3.12/site-packages`; it did not run project code under 3.11. Use complete Python 3.12 for a self-contained `make test-security`.

## Blocked or not implemented

- Documented Ring API/SDK/simulator/device access, OAuth, webhooks, and capability discovery.
- Owner/coordinator consent, residential media, ROI/masking, camera registration, and CV inference.
- Weather adapter, cultivar priors, licensed datasets, trained model artifacts, and forecast evaluation.
- Application/API, persistence, coordinator workflows, notifications, and scoped address reveal.
- Participants, operational pilot, food-safety decisions, deployment, and release evidence.

`datasets/`, `models/`, and `training/` contain boundaries/placeholders, not data or trained models.

## First local checks

```bash
python3.12 --version
uv --version
make bootstrap
make lint typecheck test-unit test-contract test-security build
make dev
```

No fixture may satisfy a Ring, real-observation, model-quality, or operational-release gate. Audit failures must remain visible and be remediated or recorded.

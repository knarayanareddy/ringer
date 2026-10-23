# HarvestGrid data inventory

Inventory date: 2026-10-23. No residential, operational, or training data is present.

| Data | Current location | Classification/provenance | Retention and use |
| --- | --- | --- | --- |
| Fictional harvest window | `examples/harvest-window.example.json` | Synthetic seasonal-baseline contract | Source-controlled schema/semantic tests only |
| Candidate constraints/features | `tests/unit/test_matching.py` | Synthetic volunteer/coordinator inputs | In-memory deterministic tests only |
| Cultivar boundary | `content/cultivars/` | Placeholder documentation; no priors | No operational inference |
| Dataset/model boundaries | `datasets/`, `models/`, `training/` | Documentation/placeholders only | No dataset, artifact, or training run |
| Schema copy | `packages/contracts/` | Non-sensitive forecast contract | Byte-drift tests |
| Configuration examples | `.env.example` | Safe placeholders | Real environment files are Git-ignored |

## Not present or collected

No Ring media/event, exact address/coordinates, access note, owner identity, tree ROI, face/plate/person data, volunteer identity/availability, recipient information, harvest weight, donation receipt, or coordinator decision is present. No database, analytics, prompt log, media store, or model training set exists.

Future raw residential media requires separate revocable consent, ROI/exclusion masking, restricted server-to-server access, seven-day default deletion after extraction, and no analytics/training use without separate consent. Exact location and access notes require assignment-scoped, time-limited reveal.

`datasets/private/`, model artifacts, and common model-binary extensions are Git-ignored. Do not convert real residential media or coordinator records into test fixtures.

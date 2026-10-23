# ringer

Five independent hackathon project workspaces, each with its own specification, design pack, lockfile, deterministic foundation, tests, and evidence boundaries.

## Initial implementation foundations

| Project | Track | Current local foundation | Verified local checks |
| --- | --- | --- | --- |
| [AccessHold](./projects/accesshold/) | Alexa+ | Contract predicates, evidence freshness, recovery transitions | 20 tests; lint/types/build/audit/fixture |
| [CurioLab](./projects/curiolab/) | Fire TV | Kotlin episode state and TypeScript content preflight | 19 tests; lint/types/build/audit/fixture |
| [NextTime](./projects/nexttime/) | Bee | Consent, minimization, authentic rubric, skill state | 29 tests; 98.53% branch-aware coverage; build/audit/fixture |
| [HarvestGrid](./projects/harvestgrid/) | Ring | Forecast semantics and deterministic coordinator matching | 23 tests; 98.17% branch-aware coverage; build/audit/fixture |
| [RoomSmith](./projects/roomsmith/) | Fire TV | Kotlin puzzle engine and TypeScript graph/fallback preflight | 24 tests; lint/types/build/audit/fixture |

**These are initial walking-skeleton/domain foundations, not five completed applications.** No live sponsor integration, real observation, device demo, user study, operational model, deployment, or release approval is claimed. External credentials, devices, datasets, partnerships, human approvals, and unavailable native toolchains remain explicit blockers in each project's `docs/preflight.md`.

### Run locally

Each project is independently bootstrapped and tested:

```bash
cd projects/<project>
make setup
make lint typecheck test-unit test-contract test-security build dev
```

CurioLab and RoomSmith also require Java 17 for their pure Kotlin harnesses. NextTime and HarvestGrid require Python 3.12 and `uv`; their audit command requires SSL/TLS. See each project README for exact prerequisites and content-validation commands.

After bootstrapping, the repository-root runner executes the same independent checks without creating a shared runtime:

```bash
./scripts/validate-foundations.sh
# Optional subset:
./scripts/validate-foundations.sh accesshold nexttime
```

`UV`, `JAVA_HOME`, and the documented `PIP_AUDIT_RUNNER` override can be supplied for workstation-specific tool locations. Project-specific results and limitations are in `projects/<name>/docs/validation.md`.

## Build with five agents

Each implementation project retains an independent workspace and agent entry point:

| Project | Workspace | Start here |
| --- | --- | --- |
| AccessHold | [`projects/accesshold/`](./projects/accesshold/) | [`AGENTS.md`](./projects/accesshold/AGENTS.md) |
| CurioLab | [`projects/curiolab/`](./projects/curiolab/) | [`AGENTS.md`](./projects/curiolab/AGENTS.md) |
| NextTime | [`projects/nexttime/`](./projects/nexttime/) | [`AGENTS.md`](./projects/nexttime/AGENTS.md) |
| HarvestGrid | [`projects/harvestgrid/`](./projects/harvestgrid/) | [`AGENTS.md`](./projects/harvestgrid/AGENTS.md) |
| RoomSmith | [`projects/roomsmith/`](./projects/roomsmith/) | [`AGENTS.md`](./projects/roomsmith/AGENTS.md) |

See [`projects/README.md`](./projects/README.md) for the assignment pattern and parallel-work protocol. Do not consolidate the projects into a shared production runtime or database.

## Shared documentation

- [Hackathon and submission-readiness review](./HACKATHON_REVIEW.md)
- [Research-backed project recommendations](./PROJECT_RECOMMENDATIONS.md)
- [Shared specification and UI index](./specs/README.md)
- [Shared engineering standard](./specs/SHARED_ENGINEERING_STANDARD.md)
- [Shared UI design-system and validation guide](./specs/ui/README.md) — 25 static screen compositions and reproducible checks ([browser index](./specs/ui/index.html))

Specifications, schemas, UI packs, traceability registers, and the new local foundations serve different evidence purposes. Static UI/design validation and source-level fixture tests do not prove platform behavior, live integrations, accessibility outcomes, or release readiness.

# Agent Implementation Workspaces

This directory contains five independent implementation assignments. Each agent receives exactly one workspace and must leave the other four unchanged.

## Assignments

| Agent | Workspace | Start here | Primary track |
| --- | --- | --- | --- |
| AccessHold | [`accesshold/`](./accesshold/) | [`accesshold/AGENTS.md`](./accesshold/AGENTS.md) | Alexa+ |
| CurioLab | [`curiolab/`](./curiolab/) | [`curiolab/AGENTS.md`](./curiolab/AGENTS.md) | Fire TV |
| NextTime | [`nexttime/`](./nexttime/) | [`nexttime/AGENTS.md`](./nexttime/AGENTS.md) | Bee |
| HarvestGrid | [`harvestgrid/`](./harvestgrid/) | [`harvestgrid/AGENTS.md`](./harvestgrid/AGENTS.md) | Ring |
| RoomSmith | [`roomsmith/`](./roomsmith/) | [`roomsmith/AGENTS.md`](./roomsmith/AGENTS.md) | Fire TV |

Every workspace contains:

- `AGENTS.md` — assignment, safeguards, ownership rules, preflight, and completion gate;
- `SPEC.md` — canonical implementation specification and vertical slices;
- `schemas/` and `examples/` — unchanged canonical contract and validated fictional fixture/draft;
- `ui/` — product truth, design system, tokens, theme, and static low-fidelity wireframes;
- `SPEC_TRACEABILITY.md` — all requirement/acceptance IDs, initially `not_started`;
- `SPEC_DEVIATIONS.md` — an empty controlled deviation log.

Shared requirements remain in [`../specs/SHARED_ENGINEERING_STANDARD.md`](../specs/SHARED_ENGINEERING_STANDARD.md). Shared UI review/validation remains in [`../specs/ui/`](../specs/ui/). These are common inputs, not shared production code.

## Copy-paste assignment pattern

Give each agent only its corresponding assignment:

```text
Implement only <PROJECT_PATH>. Read <PROJECT_PATH>/AGENTS.md first and follow it.
Keep the other four projects and shared contracts unchanged. Build the vertical
slices in SPEC.md, maintain SPEC_TRACEABILITY.md and SPEC_DEVIATIONS.md, and do
not claim completion until every required real integration, device, release
gate, and evidence requirement is satisfied. Label unavailable dependencies as
blockers rather than substituting unlabeled mocks.
```

For example, the AccessHold path is `projects/accesshold`; the CurioLab path is `projects/curiolab`.

## Parallel-work protocol

1. Use a separate branch or worktree for each agent when agents run in parallel.
2. Give each agent write ownership of only its `projects/<name>/` directory.
3. Leave `specs/`, root indexes, and other project directories to an integrator unless a cross-project change is explicitly assigned.
4. Review each project independently against its own specification and the shared engineering standard.
5. Do not consolidate the implementations into one runtime or database during integration.

## Current status

All five workspaces now have independently locked, locally validated domain/content and vertical-slice foundations in addition to their specification/design scaffolds. Together they pass 225 local unit/contract/security checks, but applications remain incomplete. No live integration, real observation, device run, user study, operational model, production deployment, or release evidence is claimed. See each project's `README.md` and `docs/validation.md` for exact scope and results.

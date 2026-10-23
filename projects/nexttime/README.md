# NextTime

**Track:** Bee
**Status:** specification and low-fidelity design ready; implementation not started
**Agent entry point:** [`AGENTS.md`](./AGENTS.md)

NextTime is consented real-world language-attempt review and just-in-time Dutch rehearsal.

## Workspace map

| Path | Purpose |
| --- | --- |
| [`AGENTS.md`](./AGENTS.md) | Assignment, ownership boundaries, safeguards, preflight, and completion gate |
| [`SPEC.md`](./SPEC.md) | Canonical implementation specification and vertical slices |
| [`schemas/real-world-attempt.schema.json`](./schemas/real-world-attempt.schema.json) | Canonical machine-readable contract |
| [`examples/real-world-attempt.example.json`](./examples/real-world-attempt.example.json) | Validated fictional fixture/draft instance, not real evidence |
| [`ui/`](./ui/) | Product truth, design system, tokens, theme, and static low-fidelity wireframes |
| [`SPEC_TRACEABILITY.md`](./SPEC_TRACEABILITY.md) | Complete requirement/acceptance register; currently not started |
| [`SPEC_DEVIATIONS.md`](./SPEC_DEVIATIONS.md) | Controlled deviation log; currently empty |
| [`../../specs/SHARED_ENGINEERING_STANDARD.md`](../../specs/SHARED_ENGINEERING_STANDARD.md) | Shared release-blocking engineering requirements |

## Implementation status

No application source, production runtime, credentials, live integration, device run, or user study exists in this workspace. The implementation agent creates the `apps/`, `services/`, `packages/`, `infra/`, `tests/`, `docs/`, and `evidence/` structure required by `SPEC.md` as appropriate to this project.

The static UI is opened through [`ui/wireframe.html`](./ui/wireframe.html). It uses shared review primitives from `specs/ui/`; it is not a production frontend.

## Parallel-agent rule

This folder is the only implementation workspace owned by the NextTime agent. Keep other projects and shared contracts unchanged. External credentials, devices, partnerships, datasets, and human approvals listed in `AGENTS.md` remain explicit blockers until genuinely available.

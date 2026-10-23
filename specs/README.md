# Shared Specification and UI Index

**Version:** 1.0.0
**Date:** October 23, 2026
**Status:** Architecture and acceptance baseline; no implementation is implied

This directory contains the shared engineering standard and UI review/validation for five independent implementation workspaces in [`projects/`](../projects/). Each project owns its specification, schema/example, UI pack, agent instructions, and traceability registers. Each can be built without reading the other four project specifications.

## Project workspaces

| Project | Agent entry point | Build specification | Canonical machine-readable contract | Primary runtime |
| --- | --- | --- | --- | --- |
| AccessHold | [AGENTS.md](../projects/accesshold/AGENTS.md) | [SPEC.md](../projects/accesshold/SPEC.md) | [access-contract.schema.json](../projects/accesshold/schemas/access-contract.schema.json) | Alexa+ MCP, TypeScript, React, AWS |
| CurioLab | [AGENTS.md](../projects/curiolab/AGENTS.md) | [SPEC.md](../projects/curiolab/SPEC.md) | [episode.schema.json](../projects/curiolab/schemas/episode.schema.json) | Fire OS/Android, Kotlin, companion Android, AWS |
| NextTime | [AGENTS.md](../projects/nexttime/AGENTS.md) | [SPEC.md](../projects/nexttime/SPEC.md) | [real-world-attempt.schema.json](../projects/nexttime/schemas/real-world-attempt.schema.json) | Bee, iOS/Swift, Python, AWS |
| HarvestGrid | [AGENTS.md](../projects/harvestgrid/AGENTS.md) | [SPEC.md](../projects/harvestgrid/SPEC.md) | [harvest-window.schema.json](../projects/harvestgrid/schemas/harvest-window.schema.json) | Ring, React, Python/CV, AWS |
| RoomSmith | [AGENTS.md](../projects/roomsmith/AGENTS.md) | [SPEC.md](../projects/roomsmith/SPEC.md) | [puzzle-graph.schema.json](../projects/roomsmith/schemas/puzzle-graph.schema.json) | Fire OS/Android, Kotlin, WebRTC, AWS |

All projects also depend on [SHARED_ENGINEERING_STANDARD.md](./SHARED_ENGINEERING_STANDARD.md).

## UI design layer

The [UI design-system and low-fidelity wireframe pack](./ui/README.md) adds product-truth briefs, visual/component guidance, semantic tokens, and 25 browser-viewable screen compositions across the five projects. Open its [browser index](./ui/index.html) for design review. These artifacts remain static design contracts; they are not five applications, high-fidelity prototypes, device demonstrations, or user-study evidence.

## Validated contract examples

Each schema has a complete example instance. The examples are intentionally marked `fixture` or `draft`: they are serialization targets, not real user evidence, approved content, or production model results.

| Project | Example instance |
| --- | --- |
| AccessHold | [access-contract.example.json](../projects/accesshold/examples/access-contract.example.json) |
| CurioLab | [episode.example.json](../projects/curiolab/examples/episode.example.json) |
| NextTime | [real-world-attempt.example.json](../projects/nexttime/examples/real-world-attempt.example.json) |
| HarvestGrid | [harvest-window.example.json](../projects/harvestgrid/examples/harvest-window.example.json) |
| RoomSmith | [puzzle-graph.example.json](../projects/roomsmith/examples/puzzle-graph.example.json) |

All five schemas pass JSON Schema Draft 2020-12 structural checks, and all five examples validate against their schemas with format checking. Implementations MUST add their own valid and invalid contract tests rather than treating these examples as sufficient coverage.

## How an implementation agent must use this pack

1. Select **one** workspace under `projects/` and read its `AGENTS.md` first. Do not implement all five in one application or share production databases between them.
2. Treat paths in a project specification as relative to that project's own root. No runtime code may import another project's source.
3. Read the shared standard and the selected project specification before creating files.
4. Copy the canonical schema into the implementation unchanged unless a documented schema-version migration is required.
5. Build in the specified vertical-slice order. Complete each slice's tests and evidence before starting the next.
6. Keep a `SPEC_TRACEABILITY.md` in the implementation mapping every `FR`, `NFR`, `INT`, `SEC`, and `AC` identifier to source files, tests, and demo evidence.
7. Record any necessary departure in `SPEC_DEVIATIONS.md`. A departure that changes a MUST requirement is incomplete until explicitly approved; silently substituting a mock, service, data model, or interaction is not allowed.
8. Never mark the project complete from unit tests or simulated sponsor integrations alone. The real-track evidence gate is mandatory.

### Agent instruction

Use the selected workspace's `AGENTS.md`; it contains the project-specific assignment, safeguards, ownership rules, external blockers, and completion gate. A parallel-assignment pattern is available in [`projects/README.md`](../projects/README.md).

## Requirement language and precedence

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative. **MUST** items are release-blocking.

When documents disagree, use this order:

1. current law, platform policy, and the official hackathon rules;
2. the selected project specification;
3. the shared engineering standard;
4. the concept document;
5. implementation convenience.

External APIs and SDKs can change. An implementing agent MUST verify exact request/response mappings against the official versioned documentation during preflight. It MUST NOT invent endpoint paths, SDK methods, device capabilities, or successful responses. The canonical internal contracts in this pack remain stable behind adapters.

## Common definition of “build complete”

A project is build-complete only when all of the following are true:

- every release-blocking requirement in its specification has implementation and test evidence;
- the required Amazon technology runs in the main product path and is demonstrated on the required real device or permitted simulator;
- all P0 acceptance scenarios pass, and no P1 scenario has an undisclosed failure;
- the clean-checkout setup guide has been executed by someone or a clean agent environment that did not write the code;
- security, privacy, accessibility, retention, and deletion requirements are implemented and tested;
- the completion rubric scores at least **90/100**, with no category below 70% of its available points and no critical-gate failure;
- the demo, architecture document, runbook, product feedback, friction log, and evidence manifest are present;
- known limitations are visible in the README and demo rather than hidden behind narration.

## External dependencies not supplied by these documents

The specifications do not include AWS, Amazon developer, Ring, Bee, travel-provider, Apple, Google, or other third-party credentials. They do not include a physical device, consented human dataset, provider partnership, native-language reviewer, accessibility reviewer, insurance arrangement, or educator approval. These are explicit execution dependencies.

An agent may build and test adapter contracts before those dependencies are available, but it MUST label the affected release gate blocked. It MUST NOT fabricate credentials, user research, real-world outcomes, provider confirmations, harvest weights, learning gains, or device demonstrations.

## Evidence layout required in every implementation

```text
<project-root>/
  README.md
  SPEC_TRACEABILITY.md
  SPEC_DEVIATIONS.md
  docs/
    architecture.md
    setup.md
    runbook.md
    demo.md
    security-and-privacy.md
    accessibility.md
    validation.md
    product-feedback.md
    friction-log.md
  evidence/
    requirements.json
    test-results/
    screenshots/
    device-runs/
    evaluation/
    demo-manifest.json
```

`evidence/requirements.json` MUST contain one record per requirement with its ID, implementation paths, automated test paths, manual evidence paths, status, and last-verified timestamp. Generated evidence can be reproduced from clean source; private media and secrets MUST NOT be committed.

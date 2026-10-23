# Implementation Specification Pack

**Version:** 1.0.0  
**Date:** October 23, 2026  
**Status:** Architecture and acceptance baseline; no implementation is implied

This directory contains five independent build specifications for the concepts in [PROJECT_RECOMMENDATIONS.md](../PROJECT_RECOMMENDATIONS.md). They are written for an autonomous coding agent or an engineering team. Each project can be built without reading the other four project specifications.

## Documents

| Project | Build specification | Canonical machine-readable contract | Primary runtime |
| --- | --- | --- | --- |
| AccessHold | [ACCESSHOLD.md](./ACCESSHOLD.md) | [access-contract.schema.json](./schemas/accesshold/access-contract.schema.json) | Alexa+ MCP, TypeScript, React, AWS |
| CurioLab | [CURIOLAB.md](./CURIOLAB.md) | [episode.schema.json](./schemas/curiolab/episode.schema.json) | Fire OS/Android, Kotlin, companion Android, AWS |
| NextTime | [NEXTTIME.md](./NEXTTIME.md) | [real-world-attempt.schema.json](./schemas/nexttime/real-world-attempt.schema.json) | Bee, iOS/Swift, Python, AWS |
| HarvestGrid | [HARVESTGRID.md](./HARVESTGRID.md) | [harvest-window.schema.json](./schemas/harvestgrid/harvest-window.schema.json) | Ring, React, Python/CV, AWS |
| RoomSmith | [ROOMSMITH.md](./ROOMSMITH.md) | [puzzle-graph.schema.json](./schemas/roomsmith/puzzle-graph.schema.json) | Fire OS/Android, Kotlin, WebRTC, AWS |

All projects also depend on [SHARED_ENGINEERING_STANDARD.md](./SHARED_ENGINEERING_STANDARD.md).

## Validated contract examples

Each schema has a complete example instance. The examples are intentionally marked `fixture` or `draft`: they are serialization targets, not real user evidence, approved content, or production model results.

| Project | Example instance |
| --- | --- |
| AccessHold | [access-contract.example.json](./examples/accesshold/access-contract.example.json) |
| CurioLab | [episode.example.json](./examples/curiolab/episode.example.json) |
| NextTime | [real-world-attempt.example.json](./examples/nexttime/real-world-attempt.example.json) |
| HarvestGrid | [harvest-window.example.json](./examples/harvestgrid/harvest-window.example.json) |
| RoomSmith | [puzzle-graph.example.json](./examples/roomsmith/puzzle-graph.example.json) |

All five schemas pass JSON Schema Draft 2020-12 structural checks, and all five examples validate against their schemas with format checking. Implementations MUST add their own valid and invalid contract tests rather than treating these examples as sufficient coverage.

## How an implementation agent must use this pack

1. Select **one** project specification. Do not implement all five in one application or share production databases between them.
2. Treat paths in a project specification as relative to that project's own root. The projects may live in separate repositories or separate top-level directories; no runtime code may import another project's source.
3. Read the shared standard and the selected project specification before creating files.
4. Copy the canonical schema into the implementation unchanged unless a documented schema-version migration is required.
5. Build in the specified vertical-slice order. Complete each slice's tests and evidence before starting the next.
6. Keep a `SPEC_TRACEABILITY.md` in the implementation mapping every `FR`, `NFR`, `INT`, `SEC`, and `AC` identifier to source files, tests, and demo evidence.
7. Record any necessary departure in `SPEC_DEVIATIONS.md`. A departure that changes a MUST requirement is incomplete until explicitly approved; silently substituting a mock, service, data model, or interaction is not allowed.
8. Never mark the project complete from unit tests or simulated sponsor integrations alone. The real-track evidence gate is mandatory.

### Suggested agent instruction

> Implement only `<PROJECT>.md` together with `SHARED_ENGINEERING_STANDARD.md` and its referenced schema. Preserve all requirement IDs. Work through the implementation slices in order, create the traceability and deviation registers, run the specified tests, and do not claim completion until every release-blocking gate has evidence. External credentials or unavailable devices are blockers to disclose, not permission to replace live behavior with an unlabeled mock.

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

# UI/UX Design Pack

**Version:** 1.0.0
**Date:** October 23, 2026
**Scope:** design systems, component behavior, design tokens, and low-fidelity browser wireframes for all five projects

This directory contains shared design foundations, browser review, and validation. Project-owned UI artifacts live in `projects/<name>/ui/`. Nothing here adds production applications or implies that high-fidelity visual design, device testing, or user research has been completed.

## Start here

- [Shared design foundations](./FOUNDATIONS.md)
- [Tool provenance and design decisions](./TOOLING.md)
- [Audit findings and resolution](./audit/README.md)
- [Open the browser wireframe index](./index.html)

Each `projects/<name>/ui/` directory contains:

| File | Purpose |
| --- | --- |
| `PRODUCT.md` | Durable audience, jobs, context, voice, constraints, and product truth |
| `DESIGN.md` | Visual direction, layout, typography, color, components, motion, and accessibility |
| `WIREFRAMES.md` | Screen inventory, flow, layout annotations, and state coverage |
| `tokens.json` | Platform-specific machine-readable design tokens and contrast pairs |
| `wireframe.html` | Browser-viewable low-fidelity screens using realistic fictional fixtures |
| `theme.css` | Project theme values and page-specific composition layered on shared wireframe primitives |

Shared browser and validation files:

- `index.html` / `index.css` — review index for all **25** screen compositions;
- `wireframes.css` / `wireframes.js` — shared responsive primitives and honest static-control feedback;
- `validate.py` / `validate-browser.cjs` — static and rendered validation;
- `package.json` / `package-lock.json` — pinned development-only audit dependencies;
- `audit/` — deterministic reports and findings-to-fix history.

## Project design documents

| Project | Product truth | Visual/component system | Screen flows | Tokens | Browser wireframes |
| --- | --- | --- | --- | --- | --- |
| AccessHold | [PRODUCT](../../projects/accesshold/ui/PRODUCT.md) | [DESIGN](../../projects/accesshold/ui/DESIGN.md) | [WIREFRAMES](../../projects/accesshold/ui/WIREFRAMES.md) | [tokens](../../projects/accesshold/ui/tokens.json) | [open](../../projects/accesshold/ui/wireframe.html) |
| CurioLab | [PRODUCT](../../projects/curiolab/ui/PRODUCT.md) | [DESIGN](../../projects/curiolab/ui/DESIGN.md) | [WIREFRAMES](../../projects/curiolab/ui/WIREFRAMES.md) | [tokens](../../projects/curiolab/ui/tokens.json) | [open](../../projects/curiolab/ui/wireframe.html) |
| NextTime | [PRODUCT](../../projects/nexttime/ui/PRODUCT.md) | [DESIGN](../../projects/nexttime/ui/DESIGN.md) | [WIREFRAMES](../../projects/nexttime/ui/WIREFRAMES.md) | [tokens](../../projects/nexttime/ui/tokens.json) | [open](../../projects/nexttime/ui/wireframe.html) |
| HarvestGrid | [PRODUCT](../../projects/harvestgrid/ui/PRODUCT.md) | [DESIGN](../../projects/harvestgrid/ui/DESIGN.md) | [WIREFRAMES](../../projects/harvestgrid/ui/WIREFRAMES.md) | [tokens](../../projects/harvestgrid/ui/tokens.json) | [open](../../projects/harvestgrid/ui/wireframe.html) |
| RoomSmith | [PRODUCT](../../projects/roomsmith/ui/PRODUCT.md) | [DESIGN](../../projects/roomsmith/ui/DESIGN.md) | [WIREFRAMES](../../projects/roomsmith/ui/WIREFRAMES.md) | [tokens](../../projects/roomsmith/ui/tokens.json) | [open](../../projects/roomsmith/ui/wireframe.html) |

## Design phase exit criteria

This design phase is complete when:

- every project has all six artifacts listed above;
- all primary and recovery screens in the implementation specifications have a wireframe or an explicitly documented state in `WIREFRAMES.md`;
- semantic text/control color pairs meet their declared WCAG contrast targets;
- HTML has no external runtime dependencies, missing local links, or placeholder controls presented as working product behavior;
- Impeccable's deterministic detector has run against the actual HTML/CSS and findings are resolved or explicitly documented;
- remaining high-fidelity, device, accessibility, and usability work is clearly separated from completed design work.

## Validation result

The committed audit reports record 50 passing token contrast pairs, 12 passing Chromium page/viewport combinations with zero axe violations, and a zero-finding Impeccable scan. See [audit findings and limitations](./audit/README.md) before interpreting those results; they do not establish device support, full WCAG conformance, or usability.

## Implementation phase—not completed by these artifacts

Each agent in `projects/<name>/` uses its local UI contracts while implementing its own specification. High-fidelity refinement, real Fire TV/iOS/Android/web/Alexa device checks, accessibility evaluation, and intended-user testing remain separate required evidence activities. Static wireframes must not be presented as a production frontend or device result.

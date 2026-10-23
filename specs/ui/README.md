# UI/UX Design Pack

**Version:** 1.0.0
**Date:** October 23, 2026
**Scope:** design systems, component behavior, design tokens, and low-fidelity browser wireframes for all five projects

This directory completes the design layer that was intentionally absent from the implementation specifications. It does not add production applications or imply that high-fidelity visual design, device testing, or user research has been completed.

## Start here

- [Shared design foundations](./FOUNDATIONS.md)
- [Tool provenance and design decisions](./TOOLING.md)
- [Audit findings and resolution](./audit/README.md)
- [Open the browser wireframe index](./index.html)

Each project contains:

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
| AccessHold | [PRODUCT](./accesshold/PRODUCT.md) | [DESIGN](./accesshold/DESIGN.md) | [WIREFRAMES](./accesshold/WIREFRAMES.md) | [tokens](./accesshold/tokens.json) | [open](./accesshold/wireframe.html) |
| CurioLab | [PRODUCT](./curiolab/PRODUCT.md) | [DESIGN](./curiolab/DESIGN.md) | [WIREFRAMES](./curiolab/WIREFRAMES.md) | [tokens](./curiolab/tokens.json) | [open](./curiolab/wireframe.html) |
| NextTime | [PRODUCT](./nexttime/PRODUCT.md) | [DESIGN](./nexttime/DESIGN.md) | [WIREFRAMES](./nexttime/WIREFRAMES.md) | [tokens](./nexttime/tokens.json) | [open](./nexttime/wireframe.html) |
| HarvestGrid | [PRODUCT](./harvestgrid/PRODUCT.md) | [DESIGN](./harvestgrid/DESIGN.md) | [WIREFRAMES](./harvestgrid/WIREFRAMES.md) | [tokens](./harvestgrid/tokens.json) | [open](./harvestgrid/wireframe.html) |
| RoomSmith | [PRODUCT](./roomsmith/PRODUCT.md) | [DESIGN](./roomsmith/DESIGN.md) | [WIREFRAMES](./roomsmith/WIREFRAMES.md) | [tokens](./roomsmith/tokens.json) | [open](./roomsmith/wireframe.html) |

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

## Next phase—not included here

After selecting one implementation project, create its high-fidelity component library and clickable production-design prototype, run the relevant Fire TV/iOS/Android/web device checks, and test with the intended users. Do not build five high-fidelity applications merely to make the design pack look complete.

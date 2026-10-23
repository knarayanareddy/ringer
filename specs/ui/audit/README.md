# UI Audit Findings and Resolution

**Audit date:** October 23, 2026
**Scope:** five agent workspaces, six HTML pages, shared/project CSS and JavaScript, five schemas/examples and token files, and repository documentation links
**Final automated status:** passed

## Workspace reorganization verification

- Five independent `projects/<name>/` workspaces contain their agent entry point, specification, schema/example, UI pack, and traceability/deviation registers.
- All **284/284** requirement and acceptance IDs match between the canonical specifications and traceability registers.
- All five moved schemas pass Draft 2020-12 structural checks, and all five moved examples validate with format checking.
- Static validation covers **252** repository-local Markdown links after the move.

## Final results

| Check | Result | Evidence |
| --- | --- | --- |
| Agent workspaces and traceability | 5 workspaces, 284/284 IDs matched, canonical JSON files present and duplicate-free | [static.json](./static.json) |
| Token structure and declared WCAG contrast pairs | 5 files, 50/50 pairs passed | [static.json](./static.json) |
| Theme/token agreement | All semantic colors match their project tokens | [static.json](./static.json) |
| HTML/local-link/static-control validation | 6 pages, 25 screens, no missing local targets or external runtime dependencies | [static.json](./static.json) |
| Chromium rendering | 12/12 page/viewport combinations passed | [browser.json](./browser.json) |
| axe-core WCAG-tagged violations | 0 violations across all 12 combinations | [browser.json](./browser.json) |
| Horizontal overflow, small buttons, script errors, external requests | 0 failures | [browser.json](./browser.json) |
| Impeccable 4.7.0 detector | 0 findings; exit code 0 | [impeccable.json](./impeccable.json) |

The browser matrix covers every page at 1440×1000 and 390×844. Mobile-width runs also emulate reduced motion. These are browser viewports, not physical-device tests.

## Findings log

### Impeccable source/HTML/CSS scan

| Pass | Findings | Main categories | Resolution |
| --- | ---: | --- | --- |
| Initial | 109 | Side accents, cramped rows, tracked kickers, theme/contrast resolution, font heuristics | Inspected every category; changed shared primitives and project themes rather than suppressing rules |
| Second | 20 | RoomSmith muted-ink heuristic, one paper-clue button contrast issue, review-canvas palette, index font, copy cadence | Resolved with token/theme refinements, a transparent light-surface button, neutral review chrome, explicit index typography, and plainer copy |
| Final | **0** | — | Full scan passed with no ignore/suppression configuration |

Specific changes included:

- moved per-page theme variables into local external CSS so both browsers and the static detector resolve the same cascade;
- replaced one-sided card accents and increased rule-row inset;
- removed tracked-all-caps kicker styling while retaining useful context labels;
- changed RoomSmith muted ink to the more chromatic `#BDD3D4`, preserving 9.29:1 contrast on the surface;
- fixed the RoomSmith paper-clue action to use dark text on a transparent light-clue background;
- kept warm product canvases inside the app/phone artboards while using neutral review-page chrome;
- rewrote four unnecessarily aphoristic NextTime copy sequences as direct operational language.

### Rendered browser and axe scan

The first complete rendered run passed 8/12 combinations. It found:

- two CurioLab trial graphics with `aria-label` on generic elements;
- CurioLab and HarvestGrid meters without valid progress roles/values;
- CurioLab `− 1`/`+ 1` buttons whose accessible names did not contain their visible labels.

Fixes:

- trial graphics now use `role="img"` and text alternatives;
- meters now use `role="progressbar"` with minimum, maximum, current value, and readable value text;
- coin-button accessible names now include the visible `− 1`/`+ 1` labels, and the visual focus note is outside the control;
- HarvestGrid’s zone group received an explicit group role.

The rerun passed **12/12 combinations with 0 axe violations**.

## Manually reviewed incomplete axe result

The final RoomSmith 390 px run reports two `color-contrast` **incomplete** nodes, not violations: the scene captions in `#room` and `#completion` overlap decorative scene geometry, so axe cannot automatically determine their background.

Manual token/computed-style review confirms both captions use:

- text: `#BDD3D4` (`color.text_muted`);
- background: `#102C3B` (`color.surface`);
- contrast: **9.29:1**, above the 4.5:1 body-text target.

The same elements pass axe’s automated contrast check in the desktop rendering. Full-page desktop and mobile screenshots were generated outside Git and visually inspected for composition. This manual check is limited to the identified captions; it is not a full manual accessibility audit.

## Evidence limits

This audit does **not** claim:

- Fire TV, Fire OS remote/focus behavior, iOS Dynamic Type, Android TalkBack, Alexa-card rendering, camera, AR, or device performance validation;
- manual screen-reader, keyboard-only, switch-control, zoom/reflow, outdoor-light, or cognitive-accessibility evaluation;
- usability testing, child/family observation, worker research, native-language review, or learning/outcome evidence;
- live provider, weather, Bee, Ring, calendar, booking, pairing, inference, or multiplayer behavior;
- high-fidelity visual design or production readiness.

Those remain subsequent-phase activities with explicit evidence requirements. Automated clean scans are necessary regression signals, not proof of product success.

# CurioLab — Specification Traceability

**Status:** implementation not started
**Coverage:** 56 unique requirement and acceptance IDs from [`SPEC.md`](./SPEC.md)
**Evidence warning:** every path/status is currently empty or `not_started`; no implementation or evidence is implied.

This is the working register required by the implementation specification. Requirement summaries aid navigation only; `SPEC.md` remains normative.

## Status rules

- `not_started`: no implementation exists.
- `in_progress`: active implementation exists but is not yet verified.
- `implemented`: code exists; required tests or release evidence remain incomplete.
- `verified`: all required tests and evidence for this row are linked and current.
- `blocked`: an explicit external dependency or decision prevents completion; identify it in `docs/` and evidence.
- `deviation_pending`: a requested change is awaiting explicit approval in [`SPEC_DEVIATIONS.md`](./SPEC_DEVIATIONS.md); a MUST requirement remains incomplete.

Use paths relative to this project root for implementation, tests, and evidence. Do not enter a path until it exists. Do not use fixture/simulated evidence to satisfy a live-integration gate.

## Register

| ID | Requirement or scenario summary | Status | Implementation paths | Test paths | Demo/device evidence |
| --- | --- | --- | --- | --- | --- |
| `FR-CL-001` | Download, verify, cache, and launch a signed/versioned episode bundle on Fire OS. | `not_started` | — | — | — |
| `FR-CL-002` | Present adult consent, safety, privacy, accessibility, and camera choices before the first lab. | `not_started` | — | — | — |
| `FR-CL-003` | Pair one companion to a TV session using a short-lived code and scoped credentials. | `not_started` | — | — | — |
| `FR-CL-004` | Record a prediction before displaying the corresponding experimental result. | `not_started` | — | — | — |
| `FR-CL-005` | Guide the exact paper-bridge protocol and verify calibration before camera-assisted counting. | `not_started` | — | — | — |
| `FR-CL-006` | Produce a stable observed coin count with confidence and occlusion/error states on the companion. | `not_started` | — | — | — |
| `FR-CL-007` | Freeze the count on the adult's collapse action and require family confirmation or correction before use. | `not_started` | — | — | — |
| `FR-CL-008` | Allow complete manual-remote measurement and non-camera completion. | `not_started` | — | — | — |
| `FR-CL-009` | Evaluate graph branches deterministically from confirmed predictions and measurements. | `not_started` | — | — | — |
| `FR-CL-010` | Render scenes with actual measured parameters; do not substitute a canned success value. | `not_started` | — | — | — |
| `FR-CL-011` | Support a second trial and greater/equal/lower comparison with a variable-change prompt. | `not_started` | — | — | — |
| `FR-CL-012` | Provide authored hint fallback and optional schema-bounded Bedrock hints. | `not_started` | — | — | — |
| `FR-CL-013` | Resume an interrupted session at the last committed node without duplicating measurements. | `not_started` | — | — | — |
| `FR-CL-014` | Provide captions, scalable UI, reduced motion, remote-only use, and optional push-to-talk prediction input. | `not_started` | — | — | — |
| `FR-CL-015` | Delete session artifacts on request and automatically under retention policy. | `not_started` | — | — | — |
| `FR-CL-016` | Publish only schema-valid, graph-valid, asset-verified, human-approved content. | `not_started` | — | — | — |
| `INT-CL-001` | The main episode MUST run in an installable Fire OS application and be demonstrated on an actual Fire TV device or the permitted Fire TV simulator. | `not_started` | — | — | — |
| `INT-CL-002` | The companion MUST use CameraX and on-device perception; raw experiment video MUST NOT be uploaded. | `not_started` | — | — | — |
| `INT-CL-003` | Confirmed observations and session messages use the deployed API Gateway WebSocket relay; no direct browser-to-AWS credentials. | `not_started` | — | — | — |
| `INT-CL-004` | Bedrock hints use the shared gateway; authored fallback hints work with Bedrock disabled. | `not_started` | — | — | — |
| `INT-CL-005` | Optional voice uses push-to-talk companion audio and Amazon Transcribe Streaming; no continuous listening. | `not_started` | — | — | — |
| `INT-CL-006` | Polly-generated character/hint audio is cached by content hash; preauthored dialogue ships in the episode bundle. | `not_started` | — | — | — |
| `NFR-CL-001` | At 1080p, scene animation sustains 30 fps on the reference Fire TV device; remote response begins within 100 ms. | `not_started` | — | — | — |
| `NFR-CL-002` | p95 stable-observation-to-scene latency below 700 ms online, measured on reference hardware and a 50 ms RTT network. | `not_started` | — | — | — |
| `NFR-CL-003` | Scene branch computation below 16 ms and never waits on a model call. | `not_started` | — | — | — |
| `NFR-CL-004` | A network/Bedrock outage does not block remote-only episode completion. | `not_started` | — | — | — |
| `NFR-CL-005` | Camera-assisted count is within ±1 coin of confirmed ground truth in at least 95% of valid controlled-protocol test runs; invalid setups must request recalibration. | `not_started` | — | — | — |
| `NFR-CL-006` | No raw frame, raw audio, or child name is written to application logs or cloud analytics. | `not_started` | — | — | — |
| `SEC-CL-001` | No child account, name, precise location, advertising ID, or behavioral advertising profile. | `not_started` | — | — | — |
| `SEC-CL-002` | Raw frames remain in companion memory; cloud message tests reject image/audio fields. | `not_started` | — | — | — |
| `SEC-CL-003` | Voice requires push-to-talk and visible state; no wake-word or background microphone service. | `not_started` | — | — | — |
| `SEC-CL-004` | Pairing tokens are scoped to one session/device and revoked on completion, adult action, or 12-hour expiry. | `not_started` | — | — | — |
| `SEC-CL-005` | Anonymous session snapshots delete after 7 days; deletion request covers snapshots, hints, and transient voice records. | `not_started` | — | — | — |
| `SEC-CL-006` | Content bundles are signed and hash-verified; unapproved content cannot execute. | `not_started` | — | — | — |
| `SEC-CL-007` | Live model text is sanitized, length-bounded, and never rendered as HTML or spoken without schema validation. | `not_started` | — | — | — |
| `SEC-CL-008` | Adult consent is required for analytics separately from episode use; core play works with analytics off. | `not_started` | — | — | — |
| `AC-CL-001` | Given an unsigned/modified bundle, when launching, then content is rejected and prior signed version remains usable. | `not_started` | — | — | — |
| `AC-CL-002` | Given an expired pairing code, when exchanged, then pairing fails without creating credentials. | `not_started` | — | — | — |
| `AC-CL-003` | Given a second companion using an already consumed code, when pairing, then it is denied. | `not_started` | — | — | — |
| `AC-CL-004` | Given no prediction, when the lab result is requested, then the engine remains at prediction. | `not_started` | — | — | — |
| `AC-CL-005` | Given missing/misaligned mat markers, when counting, then calibration blocks stable observations. | `not_started` | — | — | — |
| `AC-CL-006` | Given a stationary valid coin for less than 500 ms, when frames arrive, then it is not added to the stable count. | `not_started` | — | — | — |
| `AC-CL-007` | Given tracker overlap/occlusion, when confidence drops, then `needs_review` appears and no guessed count is committed. | `not_started` | — | — | — |
| `AC-CL-008` | Given observed count 5 and adult correction to 4, when confirmed, then all scenes/branches use 4. | `not_started` | — | — | — |
| `AC-CL-009` | Given manual remote mode, when both trials complete, then the entire episode works without camera/network. | `not_started` | — | — | — |
| `AC-CL-010` | Given flat=3 and folded=7, when comparing, then greater branch and exact values render. | `not_started` | — | — | — |
| `AC-CL-011` | Given flat=4 and folded=4, when comparing, then equal branch renders. | `not_started` | — | — | — |
| `AC-CL-012` | Given flat=6 and folded=2, when comparing, then lower branch renders without assuming a universal outcome. | `not_started` | — | — | — |
| `AC-CL-013` | Given duplicate confirmation messages, when processed, then one state transition occurs. | `not_started` | — | — | — |
| `AC-CL-014` | Given process death after confirmation, when reopened, then the last committed node/value resumes. | `not_started` | — | — | — |
| `AC-CL-015` | Given Bedrock timeout/malformed output, when hint requested, then the authored hint appears within budget. | `not_started` | — | — | — |
| `AC-CL-016` | Given ambiguous voice, when transcribed, then no prediction is selected and remote options remain. | `not_started` | — | — | — |
| `AC-CL-017` | Given reduced-motion/no-timing settings, when playing, then all content remains completable and understandable. | `not_started` | — | — | — |
| `AC-CL-018` | Given a network outage after bundle download, when playing manually, then story/branches/summary still work. | `not_started` | — | — | — |
| `AC-CL-019` | Given deletion request, when jobs finish, then cloud session/hint/voice artifacts are absent and local cache can be cleared. | `not_started` | — | — | — |
| `AC-CL-020` | Given a real Fire TV device/simulator, when running the demo, then the installed app consumes real companion observations and changes the scene accordingly. | `not_started` | — | — | — |

# Amazon Developer Hackathon — End-to-End Review

**Reviewed:** 2026-10-23 at approximately 12:20 UTC  
**Hackathon:** [Build, Ship, Shape: Amazon Developer Hackathon](https://amazonappdev2026.devpost.com/)  
**Repository reviewed:** [knarayanareddy/ringer](https://github.com/knarayanareddy/ringer)  
**Primary sources:** [Overview](https://amazonappdev2026.devpost.com/), [Official Rules](https://amazonappdev2026.devpost.com/rules), [Resources](https://amazonappdev2026.devpost.com/resources), and [Schedule](https://amazonappdev2026.devpost.com/details/dates)

## 1. Executive verdict

**NO-GO if submitted in the state reviewed.**

The GitHub default branch contained only an 8-byte `README.md` with `# ringer`. There was no application, dependency manifest, Ring integration, test suite, setup guide, demo, or submission documentation to evaluate. The repository is public but has no license, so it does not currently satisfy either permitted repository-access route:

1. public **and open source with a license**, or
2. private and shared with Devpost and all specified Amazon reviewers.

No application tests or demo flows could be run. Nothing in this review should be read as confirmation that a Devpost draft, video, Ring account, or other assets exist outside the repository; none were provided.

### Deadline

The submission deadline is **October 23, 2026 at 3:00 PM EDT / 12:00 PM PDT**, which is **19:00 UTC / 21:00 CEST in Delft**. At the review timestamp, approximately **6 hours 40 minutes** remained. The overview and Official Rules express the same deadline in different time zones.

## 2. What the hackathon requires

A submission needs one working primary-track project. Mini challenges are optional additions, not substitutes for a primary track. A project can win at most **one track prize and one mini-challenge prize**.

| Track | Hard requirement | Stronger opportunity areas | Cash prizes |
| --- | --- | --- | --- |
| **Fire TV** | Demo-ready app running on Fire OS or Vega OS; video must show an actual device or Fire TV/Vega simulator | AI-enhanced viewing, sports, fitness, family entertainment, multimodal UX, computer vision | $25k / $15k / $4k |
| **Alexa+** | Agent Skill or self-hosted MCP server using MCP spec 2025-11-25 or later with Streamable HTTP; alternatively, a working simulated Alexa+ web experience | Stateful/agentic workflows, orchestration, purchasing, rich media, MCP Apps | $25k / $15k / $4k |
| **Bee** | Actual data recorded and processed through a Bee device or Apple Watch running Bee software, connected through Bee CLI, MCP, or Agent Skills and used to deliver value | Education, developer experience, personal productivity, cross-device workflows | $12k / $8k |
| **Ring** | Working app or significant extension using a documented Ring API, SDK, simulator, or device; runtime use must exist in code and the video must show a simulator or actual device | Access control, business systems, IoT automation, accessibility, caretaking, non-security workflows | $12k / $8k |

The AWS Builder and Open Source mini challenges each award **$5,000 cash plus $5,000 in AWS credits**. Track prizes also have varying credits and promotional benefits; the published cash pool totals $138,000, while cash plus credits is presented as $190,000 in value.

## 3. How judging actually works

### Stage 1: eligibility and baseline viability

This is pass/fail. The project must reasonably fit the theme and apply the required APIs/SDKs. A polished UI with only a README mention of Ring is not enough.

### Stage 2: four equally weighted criteria

Treat each criterion as **25%** of the qualitative judging framework:

1. **Tech Implementation** — quality of construction and effective use of required technology.
2. **Design** — complete, coherent, intuitive experience appropriate to the platform.
3. **Potential Impact** — credible customer need and a realistic audience beyond the hackathon.
4. **Quality of the Idea** — creativity and understanding of the ecosystem and user needs.

Ties are resolved in that same criterion order. This makes a reliable, genuinely integrated vertical slice more valuable than several disconnected features.

### Friction-log bonus

Specific friction logs can earn **up to a 10% bonus**. Each entry should record:

- task attempted;
- steps taken;
- expected versus actual result;
- severity;
- workaround;
- actionable recommendation.

This is optional, but it is the only published scoring bonus and should be captured while debugging rather than reconstructed afterward.

### Idea-quality warning

The Official Rules explicitly call a **basic motion alert** or **basic doorbell live view** an obvious Ring idea. They cite non-security accessibility/caretaking, package/delivery management, business integration, multi-camera pipelines, and event-based triggers as more creative directions.

## 4. Current repository compliance audit

| Requirement | Evidence found | Status / required action |
| --- | --- | --- |
| New project or significant update during Aug 31–Oct 23 | Repository created Oct 23, 2026; initial commit is inside the window | Timing is compatible with a new project, but there is no project implementation yet |
| Working primary-track application | No source code or dependency manifest | **Blocker:** implement a working Ring application |
| Ring technology called at runtime | No imports, API calls, entry points, SDK use, or simulator flow | **Blocker:** add and exercise a real documented Ring integration |
| Demo through Ring simulator or actual device | No app or demo evidence | **Blocker:** demonstrate the real integration, not a mock-only dashboard |
| Complete source, assets, and run instructions | Only `# ringer` in `README.md` | **Blocker:** add all code/assets and clean setup/run/test instructions |
| Public open-source repository route | Repository is public; `licenseInfo` is `null`; no `LICENSE` file | **Blocker for this route:** add a suitable license and confirm GitHub detects it |
| Private-repository alternative | Not applicable while repository remains public | If made private, share with `testing@devpost.com` and `knmeiss`, `giolaq`, `anishamalde`, `mosesroth`, and `emersonsklar`; invitations must be accepted |
| Public English demo video under 3 minutes | Not provided | **Required:** publish on YouTube or Vimeo and show actual functionality on the intended platform |
| Project text description | Not provided | **Required:** explain features, functionality, and how the implementation works |
| Product feedback for every tool/API/SDK | Not provided | **Required:** cover use, positives, shortcomings, onboarding, and whether the tool would be used again |
| Track and mini-challenge selection | Not provided | **Required:** select Ring; select only mini challenges genuinely completed |
| Judge testing access | No runnable app or testing instructions | **Required:** keep the project available free for judging through the judging period; supply test credentials if private |
| English documentation and submission materials | README heading is English; all other materials absent | Ensure all required materials and testing instructions are English or translated |
| IP and third-party permissions | No assets or dependencies to inspect | Verify ownership, licenses, privacy rights, and permission for video/music/trademarks |
| Existing-project change description | No earlier project history found | If any pre-hackathon project is used, explicitly describe and demo the significant new work |

**Important:** adding an open-source license to this primary repository solves the public-repository access requirement, but does **not by itself qualify for the Open Source mini challenge**. That challenge requires a new, additional open-source project or a contribution to another public repository during the hackathon window, plus its own required fields.

## 5. Ring technical feasibility review

### Relevant official capabilities

The [Ring API documentation](https://developer.amazon.com/docs/ring/api-documentation.html) describes:

- OAuth 2.0 account linking;
- device discovery, capabilities, and status;
- real-time event webhooks;
- WebRTC/WHEP live video;
- historical clips and image snapshots.

The official [ring-api-helloworld](https://github.com/AmazonAppDev/ring-api-helloworld) sample provides a Next.js/TypeScript dashboard and Python API scripts. Its documented Playground path uses a short-lived access token (approximately 30 minutes); its refresh-token mode supports longer-lived sessions.

### Architecture constraints that matter

1. **Use a backend for Ring calls.** Ring states that browser-initiated calls to `api.amazonvision.com` and `oauth.ring.com` are blocked by CORS. The browser should call the application's own backend; only that backend should call Ring.
2. **Show a genuine runtime path.** A Ring client/adapter must be invoked by an application or backend entry point. Mock events can help with unit tests, but cannot be the entire competition demo.
3. **Plan for token expiry.** A Playground token is useful for a fast sandbox demonstration but can expire during recording or judging. Refresh it immediately before recording and provide reproducible setup instructions; use a refresh-token flow if a persistent judge deployment is expected.
4. **Secure webhooks.** Use HTTPS, verify Ring's HMAC signature, validate payloads, make processing idempotent using `request_id`, and acknowledge valid requests within Ring's documented five-second window.
5. **Handle operational failures.** Cover expired tokens, unavailable devices, empty event history, duplicate events, invalid signatures, rate limits/`Retry-After`, and network errors.
6. **Minimize data access.** Request only necessary scopes, keep secrets server-side and out of Git, provide `.env.example`, and define retention/deletion behavior—especially for caretaking or accessibility use cases.

### Simulator versus physical device

The general Ring getting-started guide mentions a device for testing, but the **hackathon overview and Official Rules explicitly permit a simulator and say a physical Ring device is not required**. For this competition, follow the hackathon rules and make the simulator unmistakable in the demo. Full production testing/certification is a separate concern; Ring Appstore publication or certification is not listed as a hackathon submission requirement.

## 6. Recommended product scope for this repository

Given the repository name, remaining time, and published judging guidance, the strongest focused direction is a **Ring caretaking/check-in workflow**, not another generic security dashboard.

### Concept: consent-based routine check-ins

A caregiver or household member defines a simple expected-activity window. Ring events drive a timeline and check-in state; missed expected activity creates a clear, non-diagnostic prompt to check in. The user can acknowledge, snooze, or escalate according to explicit rules.

### Demoable vertical slice

1. Discover a Ring device or load its status through the backend.
2. Trigger a documented simulator event or use an actual testing device.
3. Receive/process the event through the real application path.
4. Verify and deduplicate the event, then update a coherent timeline.
5. Demonstrate one expected-activity rule and one missed-window/check-in outcome.
6. Show empty, loading, success, and failure states with accessible messaging.

Avoid medical claims, fall detection, or inferences that Ring event data cannot support. Avoid adding live video unless it improves the user story; basic live view is explicitly considered an obvious idea and adds significant scope.

### How this maps to judging

| Criterion | Evidence the submission should show |
| --- | --- |
| Tech Implementation | Real Ring API/simulator call, server-side credential handling, webhook verification/idempotency or documented event-history integration, error handling, tests |
| Design | One complete caregiver flow, clear timeline/status hierarchy, accessible controls, useful empty/error states |
| Potential Impact | Specific consent-based caretaking need, realistic users, privacy boundaries, credible path beyond a demo |
| Quality of the Idea | Non-security use of Ring events and event-triggered workflow rather than a basic alert/live-view clone |

This is a recommendation, not evidence that any of these features currently exists.

## 7. Mini-challenge assessment

### AWS Builder

Enter only if AWS was actually used and the integration is documented. The Product Feedback answer must identify the AWS services and explain how they were used. The Official Rules say Kiro Crew can qualify on its own as a development tool; do not claim this without actual usage evidence.

A single Bedrock text-generation call or S3 storage is explicitly described as an obvious implementation. A reliable primary Ring submission should take priority over adding a brittle multi-service pipeline at the last minute. AWS promotional credit codes were reported exhausted on October 7, so do not assume free hackathon credits are available; control spending.

### Open Source

This requires an **additional** project or meaningful public contribution created during the submission window. Required submission fields are:

- contribution URL;
- primary project repository URL;
- GitHub username;
- what was built, how it works, and why it matters.

A typo, formatting tweak, or README-only change is explicitly weak. Do not sacrifice mandatory primary-track requirements to attempt this mini challenge.

## 8. Demo and submission package review

### Recommended video run-of-show

Target **2:30–2:45**, safely below the strict under-three-minute limit:

- **0:00–0:15:** user problem and a preview of the successful outcome.
- **0:15–0:35:** Ring simulator/device and proof of the genuine integration.
- **0:35–1:50:** complete end-to-end user flow, including one failure/edge case if time permits.
- **1:50–2:20:** concise architecture: backend Ring calls, auth, event processing, and optional AWS only if real.
- **2:20–2:40:** design, impact, privacy, and close.

Publish publicly on YouTube or Vimeo in English. Avoid copyrighted music/footage and third-party trademarks unless permission exists. Judges may stop at three minutes and may judge only the submitted text, images, and video, so the video cannot depend on unexplained context.

### Devpost fields and assets to complete

- Clear project description: what it does, who it serves, and how it works.
- Repository URL containing final code, assets, and English setup/run/test instructions.
- Public demo-video URL.
- Primary track: **Ring**, if following this recommendation.
- Only genuinely completed mini challenges.
- Product feedback for **every** tool, API, and SDK used.
- AWS service details in Product Feedback if entering AWS Builder.
- Additional contribution details if entering Open Source.
- Significant-update explanation if using anything pre-existing.
- Testing URL/instructions and credentials where needed.
- Optional feature requests and structured friction logs.

Keep the project available free and without testing restrictions through the judging period. After the deadline, the submission itself generally cannot be changed, so verify links and permissions before final submission.

## 9. Published inconsistencies and interpretation risks

1. **Judging start date:** the schedule page says October 26, while the Official Rules say November 9. Both point to judging ending November 20 and winners around December 3. The Official Rules state that they prevail over conflicting hackathon materials. This does not change the submission deadline.
2. **Ring hardware:** general Ring documentation emphasizes physical-device testing; the hackathon explicitly accepts a simulator and does not require hardware. Use the competition rule for eligibility, but do not claim production-grade hardware validation if only a simulator was used.
3. **Repository wording:** the private-sharing instruction can look like a general requirement when read in isolation. The governing requirement is a choice: public with an open-source license **or** private with the required reviewers.
4. **Open Source confusion:** making the primary repository public/open source is mandatory only for the public access route and is insufficient on its own for the additional Open Source mini challenge.

If any ambiguity affects eligibility, the rules instruct entrants to request clarification before the deadline.

## 10. Priority action plan

### P0 — mandatory for a valid submission

1. Freeze one Ring user story and one real simulator/device path.
2. Implement the thinnest complete backend-to-UI vertical slice; do not begin with a broad dashboard.
3. Add secure configuration, error handling, and focused tests for the integration and core rule.
4. Choose repository access: add a suitable license while public, or switch to private and complete every required invitation.
5. Write clean setup/run/test instructions and verify them from a fresh environment without committed secrets.
6. Record the real flow in under three minutes and complete every Devpost text/feedback field.
7. Verify public video/repo access in a signed-out browser and submit with buffer before 19:00 UTC.

### P1 — improves score after P0 works

1. Capture specific friction logs and actionable feature requests while implementing.
2. Polish the primary flow's accessibility, responsiveness, empty/loading/error states, and privacy explanation.
3. Make the customer need and post-hackathon impact concrete in the description and video.
4. Add a mini challenge only if it is genuine, documented, and does not destabilize the primary submission.

## Final release gate

Do not call the project ready until all answers are **yes**:

- [ ] Does a clean checkout run using only the documented instructions?
- [ ] Does executing the app make a genuine documented Ring integration call?
- [ ] Does the video visibly prove that Ring simulator/device flow end to end?
- [ ] Are secrets absent from Git and browser code?
- [ ] Are core integration, duplicate/error handling, and user-rule tests passing?
- [ ] Is the public repo licensed, or the private repo shared with every required reviewer?
- [ ] Are video, description, testing instructions, track selections, and tool feedback complete in English?
- [ ] Can judges access everything free of charge, with credentials if needed?
- [ ] Is all third-party content licensed/permissioned?
- [ ] Has the complete submission been verified using the same links judges will receive?

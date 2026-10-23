# Five Projects I Would Build for the Amazon Developer Hackathon

**Research date:** October 23, 2026  
**Hackathon:** [Build, Ship, Shape: Amazon Developer Hackathon](https://amazonappdev2026.devpost.com/)  
**Planning assumption:** unlimited implementation time, but not unlimited product sprawl  
**Companion document:** [HACKATHON_REVIEW.md](./HACKATHON_REVIEW.md) contains the verified eligibility, architecture, and submission requirements

> These are research-backed recommendations, not predictions or guarantees of winning. The scores below are a subjective way to prioritize ideas against the hackathon's four equally weighted criteria. A strong execution of a narrower idea is more credible than an ambitious demo held together by mocks.

## Executive answer

If I could fund only one, I would build **AccessHold**: an Alexa+ agent that preserves a traveler's hard accessibility requirements *after* a booking is confirmed, detects when a booking change breaks them, and executes an approved recovery. It has the best combination of durable agent state, meaningful action, human consequence, and a sharp difference from existing accessible-travel discovery products.

If the goal is the most magical living-room demo, I would build **CurioLab**. If the repository must remain Ring-focused, I would build **HarvestGrid**. **NextTime** is the strongest Bee-native concept, while **RoomSmith** is the joyful, technically ambitious wild card.

| Project | Primary track | The legible transformation | Defensible wedge | Heuristic score /100 |
| --- | --- | --- | --- | --- |
| **AccessHold** | Alexa+ | Existing booking → monitored access contract → approved repair after disruption | Post-booking constraint preservation, not another accessible-travel search engine | **93** |
| **CurioLab** | Fire TV | Household experiment → measured result → a different shared TV episode | A real measurement causally changes the story; not merely conversational video | **92** |
| **NextTime** | Bee | Real conversation → timely rehearsal → better outcome in the next real conversation | Learning evaluated in authentic recurring situations, not only inside a tutor app | **91** |
| **HarvestGrid** | Ring | Backyard tree → forecast harvest window → coordinated glean → weighed donation | Longitudinal Ring evidence closes the community-harvest logistics loop | **91** |
| **RoomSmith** | Fire TV | Household objects → verified physical puzzle actions → a responsive cooperative story | A production-quality physical game graph, not a voice-only or point-and-click escape room | **89** |

Do not build all five. Pick one and prove its hardest assumption with real users and real device data.

---

## 1. Research method: what I learned from prior winners

### 1.1 Evidence base

I used four kinds of evidence:

1. **The current hackathon's primary sources.** The [overview](https://amazonappdev2026.devpost.com/), [rules](https://amazonappdev2026.devpost.com/rules), [resources](https://amazonappdev2026.devpost.com/resources), and [schedule](https://amazonappdev2026.devpost.com/details/dates) establish the required runtime integrations and four equally weighted judging criteria: Tech Implementation, Design, Potential Impact, and Quality of Idea.
2. **Official winner announcements and project write-ups.** I examined 13 officially named winners across the [AWS AI Agent Global Hackathon](https://aws-agent-hackathon.devpost.com/updates/38140-congratulations-to-the-winners-of-the-aws-ai-agent-global-hackathon) and [Amazon Nova AI Hackathon](https://amazon-nova.devpost.com/updates/41602-announcing-the-amazon-nova-hackathon-winners), including their product and implementation descriptions. Earlier Alexa projects such as [Loop It](https://devpost.com/software/loop-it) and [FingerString](https://devpost.com/software/fingerstring-appointments) supplied additional interaction lessons, but are not counted as officially verified winners in that sample.
3. **Direct-product and incumbent scans.** I checked the current [Ring Appstore](https://ring.com/appstore), adjacent commercial products, open-source projects, and research prototypes. This eliminated several initially attractive but already crowded pitches.
4. **Explicit analytical lenses.** I evaluated candidates as an agent-systems engineer, device UX/game designer, domain operator, accessibility/privacy reviewer, ML evaluation scientist, and product strategist would. **These are analytical personas, not experts I consulted or quotations from real people.**

### 1.2 What the winners actually did

The important lesson is not “use many agents” or “add multimodal AI.” It is how the strongest projects connect a specific input to a useful, inspectable outcome.

| Verified winner | Product and implementation lesson worth transferring |
| --- | --- |
| [EcoLafaek](https://devpost.com/software/ecolafaek) — AWS Agent 1st | Citizen waste reports become classified evidence, pollution maps, semantic search, and actionable authority dashboards. The Bedrock/AgentCore workflow serves a complete civic reporting loop rather than a generic chatbot. |
| [AegisAgent](https://devpost.com/software/aegisagent-an-insurance-claim-app-fully-developed-by-kiro) — AWS Agent 2nd | Specialized evidence, policy, and compliance agents produce a defensible claim decision. Its useful patterns are cited artifacts, structured decision packets, adversarial review, and pause/resume around consequential actions. |
| [Province](https://aws-agent-hackathon.devpost.com/submissions/828293-province) — AWS Agent 3rd | The official summary describes conversational tax filing, dynamic PDF field mapping, verified tax knowledge, and exact form calculations. The lesson is to make the model navigate a domain artifact while exact computation remains deterministic. I relied on the official summary for this row, not an independently inspected project page. |
| [Drishti AI Navigator](https://devpost.com/software/drishti-ai-navigator) — Best Amazon Nova Act Integration | Accessibility is expressed as a browser task completed through vertical automation, not as a page describing what AI could do. Sponsor technology performs the central action. |
| [AgentShell](https://devpost.com/software/agent-shell) — Best Strands SDK Implementation | Model context is connected to real tools and camera/control workflows through Strands and MCP. The useful lesson is explicit tool state and control at the model/physical-world boundary. |
| [BackstageCommercials](https://devpost.com/software/backstagecommercials) — Nova 1st | A multimodal input becomes a polished creative output. Its demo value comes from a transformation a judge can understand immediately, with model generation embedded in a production pipeline. |
| [Oracus AI](https://devpost.com/software/oracus-ai) — Nova 2nd | Its evaluation-oriented implementation reinforces a recurring winner pattern: generative output becomes more trustworthy when surrounded by explicit rubrics, structured state, and deterministic checks. |
| [Sai](https://devpost.com/software/sai-m2wl0p) — Best Agentic System | Voice and visual context culminate in action on a computer. The assistant is valuable because it completes an operating-system workflow, not because it speaks fluently. |
| [Project Memoria](https://devpost.com/software/project-memoria-the-dementia-assistant) — Best Multimodal Understanding | Memory assistance is grounded in source material and designed around a particular care context. The transferable lesson is source-grounded retrieval plus restrained, audience-specific interaction. |
| [Title AI](https://devpost.com/software/title-ai) — Best UI Automation | Browser automation is applied to a narrow professional workflow. Vertical depth, repeatable state, and a concrete completed artifact beat generic “AI browser agent” breadth. |
| [Flare](https://devpost.com/software/flare-gdyebn) — Best Voice AI | Predictive work and prefetching improve perceived responsiveness. Voice UX depends on latency and timing as much as transcript accuracy. |
| [SpatialMath AI](https://devpost.com/software/spatial-math) — Best Student App | A worksheet becomes a manipulable 3D lesson. Crucially, strict schemas, repair/normalization, gesture smoothing, and deterministic geometry solvers keep generated visuals mathematically exact. |

### 1.3 The cross-winner playbook

Across those projects, eight patterns recur:

1. **Own a complete, costly job.** Input → interpretation → decision → action or artifact → verification. A summary or alert alone is rarely enough.
2. **Make the sponsor technology structurally necessary.** Removing Ring, Bee, Fire TV, or Alexa+ should break the product's main loop, not merely remove an input option.
3. **Separate probabilistic interpretation from exact computation.** Models can extract evidence, classify intent, and draft language. Code should handle arithmetic, geometry, policy evaluation, schedules, state transitions, and financial actions.
4. **Engineer around model fallibility.** Use schemas, validation, repair, retries, model failover, durable state, and idempotency. Do not put a raw model response directly into a renderer, booking system, or physical workflow.
5. **Show provenance and uncertainty.** Winners become credible when a judge can inspect why the system acted. Unknown should remain unknown; a fluent answer is not verification.
6. **Design a demo around a visible transformation.** Scene → commercial, worksheet → interactive lesson, evidence → defensible decision, or voice → completed task is much stronger than a tour of dashboards.
7. **Respect device-native interaction.** A ten-foot Fire TV interface, a short voice exchange, and a wearable interruption budget are different design problems. A responsive web chat is not enough.
8. **Measure the outcome that matters.** Report task success, false action rate, latency, cost, and results on real or known-answer inputs. Do not substitute model confidence or a polished screenshot for evidence.

### 1.4 The expert lenses used to challenge every idea

| Analytical lens | Questions applied to each candidate |
| --- | --- |
| **Agent/systems engineer** | Where is durable state? Which operations are deterministic? What happens on duplicate events, expired credentials, tool failure, or an invalid model response? |
| **Fire TV / game UX designer** | Is the shared screen doing something a phone cannot? Can a remote, voice, and accessibility fallback complete the experience? Is the response immediate enough to feel alive? |
| **Domain operator** | Who already performs this job? Which handoff, exception, and audit trail matter? Does the product reduce work or create another queue to supervise? |
| **Accessibility and privacy reviewer** | Were affected users treated as designers rather than inspiration? Is consent meaningful? Can the system avoid face recognition, covert recording, sensitive inference, and unsupported guarantees? |
| **ML evaluation scientist** | What is ground truth? What simple baseline should this beat? How are uncertainty, subgroup errors, and real-world outcomes measured? |
| **Product strategist / judge** | What incumbent is closest? Why is this wedge different? Is the required Amazon technology essential? Can the value be demonstrated in under three minutes without narration covering missing functionality? |

### 1.5 Ideas rejected or deliberately narrowed

This negative work is important: adding a sponsor API to a familiar SaaS category does not make a strong hackathon idea.

| Earlier candidate | Decision and evidence |
| --- | --- |
| **Whyline** — generic cross-tool decision provenance | **Rejected.** [Align](https://align.tech/) already covers a decision graph, conflict/supersession checks, pre-edit agent checks, and pull-request enforcement. |
| **ClearDock** — generic receiving and dock vision | **Rejected.** Vimaan and PackageX already address computer-vision receiving and package workflows; [PackageProtect](https://ring.com/packageprotect) also covers delivery events in the Ring ecosystem. |
| **Mend** — generic appliance diagnosis and service coordination | **Rejected in that form.** Existing appliance-service and service-agent products already cover the central workflow; camera ingestion alone was not a sufficient wedge. |
| **CommonShelf** — Ring-verified community-fridge inventory | **Rejected.** [FridgeSense](https://github.com/nabour-labs/FridgeSense) already combines Ring fridge clips, S3, Bedrock Nova inventory, a PWA, and Alexa+ MCP; [FridgeFinder](https://www.fridgefinder.app/) covers stock and volunteer coordination. |
| **Threshold** — accessibility mapping | **Held back.** [AccessMap](https://accessmap.world/) and other products already cover access profiles and routing. Only a detect → dispatch → verify remediation lifecycle remained interesting, and AccessHold had the stronger overall execution wedge. |
| **ChargeProof** — camera-verified EV charger uptime | **Held back.** OCPP monitoring, maintenance routing, and camera analytics already exist across products such as Flipturn, Bruviti, and the SpotGenius/Zevtron integration. The remaining fusion idea was useful but less differentiated. |
| **Generic accessible-travel planner** | **Narrowed into AccessHold.** [Wheel the World](https://wheeltheworld.com/) already provides detailed, measured/photographed accessibility inventory, while [Nowah](https://nowah.xyz/blog/ai-travel-booking-accessibility) describes conversational profiles and verification. Search alone is not enough. |
| **Generic AI language tutor** | **Narrowed into NextTime.** [Speak](https://www.speak.com/), [Langua](https://languatalk.com/try-langua), Univerbal, and Praktika already provide adaptive role-play, saved mistakes, and personalized plans. |
| **Generic AI-generated family story** | **Rejected.** Current Fire TV hackathon submissions and products such as Storyloom already make this crowded. CurioLab and RoomSmith require the physical world to change the digital experience. |

---

## 2. Equal-criteria scorecard

Each category is scored out of 25, matching the official equal weighting. These scores assume the proposed production-quality implementation and validation are actually completed; they are not forecasts of a judge's score.

| Project | Tech /25 | Design /25 | Impact /25 | Idea /25 | Total /100 | Main reason it is not higher |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **AccessHold** | 23 | 23 | 24 | 23 | **93** | Provider integrations and reliable evidence are difficult; physical accessibility can never be guaranteed by software alone |
| **CurioLab** | 23 | 24 | 22 | 23 | **92** | Requires excellent educational content and a real learning study, not just a working demo |
| **NextTime** | 22 | 23 | 23 | 23 | **91** | Consent, ASR bias, and attribution of real-world improvement need careful handling |
| **HarvestGrid** | 22 | 22 | 24 | 23 | **91** | Seasonality, occlusion, and volunteer/insurance operations constrain deployment |
| **RoomSmith** | 22 | 24 | 20 | 23 | **89** | Strong entertainment value, but less social/economic impact and substantial CV reliability work |

The following sections are the detailed recommendations.

---

# 1. AccessHold — keep an accessible booking accessible

**Primary track:** Alexa+  
**Best overall balance:** yes  
**One-line pitch:** An agent that watches an existing trip for changes that violate a traveler's hard access needs, proves what changed, and executes an approved recovery.

## User and costly problem

The initial users are disabled travelers, their companions, and specialist travel advocates. The product starts **after any booking**, including bookings made elsewhere.

An “accessible” reservation is not a static fact. An aircraft swap can remove a needed feature or change seat geometry; an accessible hotel room can be reassigned; a changed arrival time can break an arranged transfer. Today, the traveler repeatedly checks reservations, calls providers, re-explains requirements, and advocates during a disruption. Generic travel agents optimize price and arrival time, not a set of non-negotiable physical constraints.

AccessHold's central object is an **Access Contract**, not an itinerary:

- hard constraints and soft preferences, expressed in the traveler's own terms;
- the exact booked asset each constraint applies to;
- evidence type, source, timestamp, and scope;
- status: `provider-confirmed`, `documented`, `unverified`, `violated`, or `not-applicable`;
- approved recovery authority, budget, and escalation contact.

Reviews may provide leads, but never become “verified” evidence.

## Complete workflow

1. **Import an existing trip.** The traveler forwards confirmations or says, “Watch this trip.” The agent extracts bookings and asks only for missing hard constraints.
2. **Build the Access Contract.** A deterministic constraint engine maps needs to flight, seat, transfer, and room assets. The traveler approves the contract before any provider is contacted.
3. **Collect evidence.** Adapters query official data where available. For property-specific details, the agent drafts a concise provider questionnaire; email or voice outreach is sent only with approval. Written responses and source documents are stored with timestamps.
4. **Monitor the whole trip.** Durable workflows watch booking messages, aircraft/seat changes, schedule changes, and provider responses. A change re-evaluates every dependent constraint, including transfers and check-in timing.
5. **Recover without weakening a hard constraint.** The agent proposes alternatives only after running the same evidence checks. It shows cost, refund/change terms, remaining unknowns, and a human-advocate option. No rebooking or purchase occurs without explicit approval.
6. **Close the loop.** After execution, the agent imports the new confirmation and verifies that the Access Contract is attached to the replacement assets. The traveler can ask, “What changed, and what is still only unverified?”

## Architecture and why Alexa+ is essential

- **Alexa+ integration:** self-hosted Streamable HTTP MCP server using the required specification, or an Agent Skill; MCP Apps/rich cards for evidence comparison and approval. Voice is the interruption and negotiation interface; the visual card carries exact details.
- **Durable orchestration:** AWS Step Functions and EventBridge for long-lived monitoring, retries, waits, and human approval; DynamoDB for contract/version state; S3 for encrypted evidence; SES for approved provider correspondence.
- **Document and dialogue AI:** Textract plus Bedrock for itinerary/evidence extraction and concise drafting. A separate critic checks unsupported claims, but cannot mark a requirement verified.
- **Exact policy engine:** versioned code evaluates constraints, time windows, fare rules supplied by providers, and approval authority. A language model never decides whether a measurement meets a hard requirement.
- **Provider adapters:** authenticated booking/calendar/email/status connectors with idempotency keys, secrets management, full audit logs, and a simulated provider adapter for reproducible tests.

Alexa+ is not a veneer: the product needs persistent state, multi-step orchestration, purchasing/rebooking authority, rich media, and natural voice negotiation during a stressful disruption.

## Three-minute demo

1. Import a real test booking through the actual Alexa+ simulator; show four hard constraints and one honestly marked unknown.
2. Approve a provider verification request and show the returned evidence attached to the exact room or aircraft asset.
3. Emit an aircraft-swap event through a labeled test-provider adapter. The agent detects that a required feature is absent and explains the evidence, not just the schedule change.
4. Compare two recovery options on a rich card. Approve one by voice; show the executed test booking, updated calendar, and revalidated Access Contract.

The demo should include one failure: when evidence is missing, AccessHold says “unverified” and offers human escalation. That builds more trust than a perfectly confident scripted run.

## Differentiation

- **[Wheel the World](https://wheeltheworld.com/):** rich accessibility inventory and booking discovery. AccessHold monitors reservations obtained anywhere and owns post-booking integrity and recovery.
- **[Nowah](https://nowah.xyz/blog/ai-travel-booking-accessibility):** conversational profiles and discovery/verification. AccessHold's wedge is the versioned contract, time-based monitoring, and approved execution after change.
- **[Otto](https://www.ottotheagent.com/blog/airline-disruption-management):** general traveler-side disruption monitoring and rebooking. AccessHold evaluates hard accessibility evidence across the whole trip, including provider commitments and dependent reservations.

This is a narrower wedge, not a claim that no adjacent product exists.

## Validation, risks, and release gates

**Measure:** change-detection latency; percentage of hard constraints with current evidence; false-verification rate; approved recovery success; traveler time spent; number of automated actions with unresolved constraints. The last target must be zero.

**Validate with:** compensated disabled-traveler co-design sessions, specialist advocates, and provider operations staff. Build a known-answer suite of aircraft swaps, room changes, missing evidence, stale responses, and partial refunds.

**Do not ship if:** the system treats reviews as proof, hides unknowns, autonomously rebooks outside authority, or claims physical accessibility is guaranteed. Sensitive profiles need minimization, encryption, export/deletion, and no advertising use. Complex rights questions and contested cases go to a human; the product is not a legal or safety guarantee.

**Scope discipline:** do not build another destination search, review scraper, or generic trip planner.

## Mini-challenge route

- **AWS Builder:** the durable event-driven workflow and deterministic evidence gate are substantive, not decorative.
- **Open Source:** publish the Access Contract JSON Schema, reference validator, and anonymized disruption fixtures as a separate project. Merely licensing the main repository would not satisfy the mini challenge.

---

# 2. CurioLab — a science show powered by your real experiment

**Primary track:** Fire TV  
**Best demo magic:** yes  
**One-line pitch:** A shared science episode that pauses while a child performs a household experiment, then changes its story and simulation based on the measured result.

## User and costly problem

The initial audience is families with children roughly 7–11 years old, with a later classroom version. Educational TV is accessible and engaging but usually linear. Conversational video lets a child respond, yet the story rarely depends on something the child actually tested. CurioLab connects narrative, prediction, physical evidence, and explanation on the largest shared screen in the home.

A CHI 2022 study of [conversational science programming](https://par.nsf.gov/servlets/purl/10346104) found that children actively interacted with a media character and performed better on an immediate episode-specific science assessment than peers watching the non-interactive broadcast. That supports the interaction hypothesis; it does **not** prove CurioLab's learning outcomes, which must be tested independently.

## Complete workflow

1. A family launches an original episode on a real Fire OS app and chooses remote, voice, captions, and accessibility preferences.
2. A character presents a problem. Each child makes a prediction before seeing the answer.
3. The episode enters a “lab break” with an allowlisted household activity. A parent and child have distinct roles, so this is shared play rather than solitary tutoring.
4. A paired phone processes the experiment camera stream locally. It emits a structured measurement, confidence, and calibration state—not a continuous video upload. A compatible Fire TV camera can be an optional input, but USB webcam support is model-dependent and is not the baseline assumption.
5. A deterministic measurement service validates the observation. Low confidence triggers a retry or manual remote entry; the model never invents a value.
6. The TV scene, animated simulation, character dialogue, and next challenge use that measurement. A second run lets the child change one variable and see the episode respond differently.

### Flagship episode: “The Bridge to Moon Base”

A character must move supplies across a canyon. The child predicts whether a flat or accordion-folded sheet of paper will support more identical coins. The paired camera observes an allowlisted setup and helps count coins and detect the failure event; the family confirms the final count. The TV then renders the canyon bridge with **their measured maximum load**, branches the dialogue around their original prediction, and asks them to alter one design variable. The point is not that AI knows the answer—it is that the child's evidence changes the show.

## Architecture and why Fire TV is essential

- **Native Fire OS reference app:** Kotlin application with a hardware-accelerated scene renderer, remote-first navigation, local episode cache, captions, and audio description. Vega OS can be a later adapter; the first build should not pretend both runtimes are identical.
- **Episode Experiment Graph:** each episode is a versioned graph of narrative nodes, hypotheses, safety-approved materials, measurement contracts, branches, hints, and learning objectives.
- **On-device perception:** phone-based object detection and temporal smoothing produce only structured observations. Active detectors are restricted to the current experiment; raw frames are discarded by default.
- **Deterministic scene and science engine:** code computes counts, comparisons, units, and simulation parameters. Every branch is checked for reachability and scientific correctness.
- **Constrained generative layer:** Bedrock produces age-appropriate dialogue variations and hints from the graph, never new experiments or measurements. Schema validation, content filters, caching, and human educator approval surround it.
- **AWS services:** S3/CDN episode bundles, DynamoDB session/learner state, AppSync or a low-latency session channel, and a publishing pipeline that runs graph/schema/science tests before release.

Fire TV is essential because the measurement becomes a cinematic, shared event. A phone-only version loses the family roles, ten-foot storytelling, and collective reveal.

## Three-minute demo

Use an actual Fire TV device or the permitted simulator, visibly running the app:

1. Start the episode and make opposite predictions on two runs.
2. Show the real paper-and-coin experiment and the paired phone's structured observation; include the confirmation interaction.
3. Reveal the TV simulation using the measured load and a changed narrative branch.
4. Repeat with the folded design and show a different result, followed by a 15-second view of the Episode Experiment Graph and local-processing architecture.

No prerecorded “fake AI” substitution: the two physical outcomes must genuinely drive two scene states.

## Differentiation

- **Conversational science video:** CurioLab requires physical evidence, not only a spoken answer.
- **[Pivot Interactives](https://www.pivotinteractives.com/):** established video-based investigations, variable manipulation, sensors, and classroom workflows. CurioLab's wedge is an original shared TV narrative driven by a child's own household experiment, not analysis of a prerecorded laboratory event.
- **Generic AI story generators:** CurioLab uses an authored, solvable episode graph; generative dialogue is subordinate to measurement and curriculum.

## Validation, risks, and release gates

**Measure:** measurement error against human ground truth; false branch transitions; p95 observation-to-scene latency; experiment completion; prediction/explanation learning gain immediately and after a delay; parent intervention; equal participation among children.

**Validate with:** families, a science educator, and a child-safety reviewer. Compare three conditions using the same content: linear video, conversational video, and measurement-driven CurioLab. Report learning and engagement separately.

**Do not ship if:** activities are open-ended or unsafe, raw child video is retained by default, the system infers intelligence or emotion, or generated dialogue can introduce unreviewed science. Use push-to-talk, no continuous microphone, no child-targeted purchases, and non-camera completion paths.

**Scope discipline:** one outstanding 10–12 minute episode is better than a generator of unlimited shallow episodes. Do not launch with a full curriculum.

## Mini-challenge route

- **AWS Builder:** the episode compiler, validation pipeline, constrained Bedrock dialogue, and synchronized session architecture form a real AWS workload.
- **Open Source:** publish the Episode Experiment Graph specification, validator, and one safe sample episode as a separate educational-runtime project.

---

# 3. NextTime — practice the conversation you are actually about to have

**Primary track:** Bee  
**Best personal data loop:** yes  
**One-line pitch:** Bee learns from a consented real-world language attempt, delivers a tiny rehearsal just before the next similar encounter, and measures whether the real outcome improves.

## User and costly problem

The initial users are internationally mobile adults who already know basic vocabulary but lose access to it during recurring, consequential conversations: arranging an apartment repair, speaking to a school administrator, or clarifying a shift with a manager.

Existing tutors personalize simulated conversations very well. The unresolved gap is transfer: did the learner succeed the next time a real person responded unpredictably? NextTime optimizes for that moment rather than for lesson streaks or an app-internal fluency score.

## Complete workflow

1. **Capture with consent.** A real conversation is recorded and processed through a Bee device or Apple Watch running Bee software. Recording is user-initiated and limited to contexts where participants have consented. Otherwise, the learner records a post-conversation voice memo through Bee; the authentic-attempt workflow remains available without covert bystander capture.
2. **Extract an attempt, not a personality profile.** Through Bee CLI, MCP, or an Agent Skill, the app obtains the actual transcript/context. Diarization and redaction retain only the learner's consented speech features and the minimum task outcome evidence. Other-speaker content is discarded by default.
3. **Confirm the learning target.** The system proposes one functional breakdown—for example, “did not confirm the proposed appointment time”—with an evidence span and ASR confidence. The learner can correct it before it enters memory.
4. **Predict the next useful rehearsal.** The learner marks a recurrence or explicitly connects a calendar event. A deterministic scheduler triggers a 90-second rehearsal shortly before it; the system does not infer sensitive events from ambient audio.
5. **Rehearse the transfer, not the transcript.** A phone/watch notification opens a new role-play with the same communicative function but altered details. It practices one repair strategy, such as asking for repetition or confirming a time, rather than memorizing a script.
6. **Measure the next authentic attempt.** The next Bee-recorded interaction is evaluated against the same task rubric. Progress is “confirmed the appointment without switching languages,” not “completed five AI lessons.”

## Architecture and why Bee is essential

- **Real Bee data path:** iOS Developer Mode and Bee setup are explicit prerequisites. Bee CLI/MCP/Skill ingestion is exercised in the running product; a text-upload-only clone would not qualify.
- **Consent and redaction boundary:** consent receipts, speaker separation, sensitive-context exclusions, short raw-data retention, and user-visible deletion. Only minimized attempt features enter long-term learner state.
- **Learner model:** DynamoDB stores functional goals, evidence-linked breakdowns, next occurrence, rehearsal history, and real outcomes. A deterministic spaced-practice scheduler controls timing.
- **Speech and scenario pipeline:** speech transcription with confidence gating; Bedrock generates a scenario from an approved template and a critic verifies that it exercises the intended function without adding sensitive content; Polly supplies rehearsal voices.
- **Outcome evaluator:** a rubric distinguishes task completion, requested repair, language switching, and independence. Low ASR confidence or ambiguous outcomes require learner confirmation.

Bee is essential because the learning loop begins and ends in authentic life rather than in a tutor session. Its value is continuity between attempts; it is not merely an expensive microphone for generic role-play.

## Three-minute demo

Use two consenting actors and clearly labeled time compression:

1. Show the actual Bee/Apple Watch recording of a first apartment-repair call. The learner understands the offered time but hangs up without confirming it.
2. Show the minimized attempt card, the learner confirming the target, and the follow-up event linked to the next call.
3. Deliver the timely 90-second rehearsal and demonstrate one interactive exchange.
4. Show the second genuine Bee-recorded call, where the learner asks for repetition and confirms the appointment. End on the real-world outcome comparison, not a grammar score.

The timeline can be edited for length, but the two Bee captures and outcome evaluation must be real.

## Differentiation

- **[Speak](https://www.speak.com/) and [Langua](https://languatalk.com/try-langua):** strong AI conversation, correction, saved vocabulary, and personalized practice. NextTime begins with an authentic attempt, rehearses for an imminent recurrence, and uses the next authentic attempt as the outcome measure.
- **[Praktika](https://openai.com/index/praktika/):** multiple agents personalize lessons from goals, progress, and prior tutor interactions. NextTime's moat is consented real-world transfer evidence, not another multi-agent tutor.
- **Generic wearable coaching:** NextTime does not interrupt or covertly coach during a conversation. The intervention happens before it, with a privacy-preserving review afterward.

## Validation, risks, and release gates

**Measure:** task success on the subsequent authentic attempt; independent communication repair; unwanted language switching; rehearsal lead time and completion; learner-confirmed correction precision; false memory rate; seven-day retention; learner confidence. Do not optimize for accent eradication or “native-like” identity.

**Validate with:** adult language educators and a small cohort of learners using a within-person baseline. Compare NextTime against generic role-play matched for practice time, with blinded human rubric scoring and ASR error analysis by accent.

**Do not ship if:** recording is covert, bystander content is retained without a lawful basis, the app diagnoses ability from low-confidence ASR, or the learner cannot inspect and delete memories. Exclude medical, legal, workplace-discipline, and other sensitive encounters from the initial product.

**Scope discipline:** one language pair, three recurring situations, and one functional outcome rubric. Do not launch with 30 languages and a general CEFR tutor.

## Mini-challenge route

- **AWS Builder:** meaningful if the redaction, learner-state, scenario, and outcome pipelines are genuinely deployed on AWS.
- **Open Source:** publish a consent-aware Real-World Attempt schema and an evaluation harness using synthetic or explicitly consented/de-identified conversations as a separate project.

---

# 4. HarvestGrid — turn backyard trees into a just-in-time harvest network

**Primary track:** Ring  
**Best Ring-specific moonshot:** yes  
**One-line pitch:** Fixed Ring observations forecast a backyard harvest window, then coordinate owner consent, trained gleaners, and recipient capacity—and learn from the weighed result.

## User and costly problem

The users are homeowners with surplus fruit, existing gleaning organizations, trained volunteers, and food-distribution partners. The problem is not simply identifying ripe fruit. It is aligning a short and uncertain readiness window with property access, volunteer labor, equipment, and a recipient that can use the produce.

Organizations such as [Food Forward](https://foodforward.org/faqs/) and [Common Fruit](https://commonfruit.org/) already coordinate gleaning; Food Forward's public workflow includes recent photos, a ready-to-harvest list, volunteer signup, and confirmation. HarvestGrid should integrate with that operational expertise rather than pretend a model can replace it.

## Complete workflow

1. **Opt in a tree, not a household.** An owner confirms species and location, aims a Ring camera at the tree, configures privacy zones, and approves exactly which observations can be used. Exact addresses remain hidden from volunteers until assignment.
2. **Build longitudinal evidence.** The backend uses documented Ring snapshots/live-view/event-clip capabilities to collect a fixed-view series. A custom vision pipeline tracks visible fruit regions, count, size proxies, and color change; weather and owner-confirmed variety add context.
3. **Forecast with humility.** The output is a harvest window and visible-yield range with confidence and occlusion warnings. The owner or trained coordinator confirms readiness. Visual color is not treated as proof of internal ripeness or food safety.
4. **Coordinate the whole glean.** After owner approval, a deterministic matcher considers volunteer training, travel, access instructions, equipment, recipient capacity, and timing. Step Functions handles invitations, reminders, cancellations, and escalation to a human coordinator.
5. **Verify and learn.** A trained event leader confirms completion. Actual harvested and accepted weights are recorded, a donation receipt is generated, and the error between forecast and outcome becomes the next training/evaluation example.
6. **Report real impact.** Owners and organizations see recovered produce, volunteer fill rate, coordinator time saved, and forecast calibration—not a vanity count of camera alerts.

## Architecture and why Ring is essential

- **Documented Ring runtime:** server-to-server OAuth, device discovery, webhooks, snapshots/clips/live view as supported by the selected device; HMAC verification, idempotent event handling, token refresh, and a visible simulator/device demo.
- **Longitudinal vision pipeline:** encrypted short-retention media in S3; fixed-view registration, fruit segmentation/tracking, and a crop-specific forecast model deployed through a controlled inference service. Bedrock may explain evidence and draft coordination messages, but does not invent counts or ripeness.
- **Operations system:** Aurora/PostGIS or an equivalent geospatial store for trees, availability, and recipient capacity; DynamoDB for workflow state; EventBridge schedules; Step Functions for durable glean orchestration; SNS/SES for approved notifications.
- **Human operations console:** confidence, privacy status, owner approval, volunteer credentials, and manual override are first-class. The model cannot autonomously dispatch strangers to a home.
- **Privacy architecture:** crop-only fields of view, privacy masks, no face or license-plate recognition, exact-address reveal only after assignment, and deletion/export controls.

Ring is essential because repeated, fixed-position, real-world observations trigger and later verify the operational loop. A one-off fruit photo would be a different, much weaker product.

## Three-minute demo

1. Show a real Ring device/simulator and a dated fixed-camera series of one tree. Overlay tracked fruit regions and the forecast interval, including one low-confidence/occluded example.
2. The owner approves a harvest request. The system matches a trained volunteer team and a recipient with capacity, then issues the approved invitations.
3. Show the completed glean record, actual accepted weight, donation receipt, and forecast error updating the evaluation dashboard.

Use time-lapse honestly labeled by date. Do not imply that fruit ripened during the presentation. A real small pilot with one species and one gleaning partner is worth more than a map of fabricated trees.

## Differentiation

- **Ring garden/timelapse apps such as Greenlapse:** monitor plant growth or create garden media. HarvestGrid turns longitudinal observations into multi-party logistics and measured donation outcomes.
- **[Thamara](https://github.com/rh7m/Thamara-AI-Fruit-Ripeness-Datector):** an adjacent open-source concept combining fruit detection and farm volunteers. HarvestGrid's narrower wedge is fixed Ring time series, residential privacy, existing gleaning operations, recipient capacity, and outcome-based forecast learning.
- **[FruitCast](https://fruitcast.co.uk/) and commercial orchard systems:** sophisticated agricultural forecasting. HarvestGrid is not a replacement for farm-grade agronomy; it tests whether existing consumer cameras can support a low-cost neighborhood network.
- **Common Fruit / Food Forward:** operational partners and coordination incumbents, not enemies. HarvestGrid supplies evidence and forecast automation around their safety and volunteer processes.

## Validation, risks, and release gates

**Measure:** harvest-window interval error; visible-yield error against weighed outcomes; false-ready dispatch rate; coordinator minutes per event; volunteer fill and cancellation rate; recipient rejection/spoilage; estimated produce recovered relative to each owner's prior baseline.

**Validate with:** one crop, one neighborhood, one experienced gleaning organization, and one full season. Use expert readiness labels and actual scales. Test across camera angles, lighting, occlusion, and tree owners rather than reporting only an in-sample vision score.

**Do not ship if:** the product claims internal ripeness or safety from RGB images, sends volunteers without trained coordination, exposes addresses, or treats an automated dispatch as permission to enter property. Insurance, waivers, food-safety rules, equipment rules, and ladder/climbing restrictions belong with the operating partner.

**Scope discipline:** one visually tractable crop and one partner workflow. Do not begin with all fruit species, a public produce map, or a national volunteer marketplace.

## Mini-challenge route

- **AWS Builder:** a substantial combination of Ring ingestion, longitudinal CV, geospatial state, and durable human-in-the-loop operations.
- **Open Source:** publish a crop-only, consented fixed-camera time-series benchmark and the harvest-window evaluation harness, or a standalone matching engine with synthetic organization fixtures. Do not release raw residential footage or addresses.

---

# 5. RoomSmith — a cooperative escape room that uses your living room

**Primary track:** Fire TV  
**Best playful wild card:** yes  
**One-line pitch:** A responsive TV adventure in which players physically arrange household objects, speak to characters, and cooperate while a deterministic game engine verifies each puzzle.

## User and costly problem

The initial users are two to four co-located family members or friends, roughly ages 8+, who want active shared play without headsets or a commercial escape-room venue. Voice-only escape games lack physical presence; point-and-click adventures keep players seated and looking at individual controls. RoomSmith makes the television the shared world and ordinary objects the controllers.

Its ambition is not “an LLM invents an escape room.” It is a reliable physical-puzzle runtime with an AI director that adapts story and hints without breaking solvability.

## Complete workflow

1. Players choose an authored episode, available object kit, difficulty, and accessibility options on the Fire TV app.
2. A paired phone becomes a local, on-device observation sensor. The app activates only the detectors needed for the current puzzle; it does not continuously identify people or scan the whole home.
3. The TV gives different clues or roles to different players. They arrange allowlisted objects, perform a gesture, or complete a physical sequence.
4. On-device vision emits structured observations such as `red-cup left-of book`. A hold-to-verify interval and temporal hysteresis prevent one noisy frame from solving a puzzle.
5. A deterministic Physical Puzzle Graph compares observations with allowed predicates and changes the scene. The AI director can vary character dialogue and hint timing, but cannot declare success or mutate the solution logic.
6. If perception fails, players get a calibration retry or equivalent remote/non-camera path. The story remains completable.
7. At the end, the app creates a shareable illustrated case report from game state—not from private room footage.

### Flagship micro-episode: “Light the Last Lighthouse”

The TV lighthouse is dark. One player can see a tide chart, another hears a character's clue, and a third controls the object camera. The team places a red cup to the left of a book and holds the arrangement for one second. The deterministic engine accepts the spatial predicate; the lighthouse beam illuminates and reveals the next cooperative puzzle. The director adjusts hints if the team stalls, while the scene and object logic remain exact.

## Architecture and why Fire TV is essential

- **Native Fire OS app:** Kotlin shell plus a hardware-accelerated 2D/3D scene runtime, remote/voice parity, local episode packs, and fast resume.
- **Paired local sensor:** phone-based TFLite/MediaPipe object, color, gesture, and spatial-relation detectors. Only compact observations leave the device during play; raw frames remain local by default.
- **Physical Puzzle Graph:** versioned nodes contain observation predicates, accepted alternatives, timeout/hint policy, accessibility fallback, and scene transitions. A graph solver proves every offered puzzle is solvable with the selected object kit.
- **Constrained AI director:** Bedrock selects approved narrative variations and produces hints from a fixed hint ladder. JSON schema validation, a solvability checker, content filters, and human review surround it.
- **Performance engineering:** detector activation on demand, frame skipping, smoothing, one-second hold verification, local session transport for the interaction loop, and pre-cached scene/voice assets. AWS handles content, session persistence, and publishing rather than putting a cloud model in the frame-rate-critical path.

Fire TV is essential because it supplies the shared cinematic world and group visibility. The physical actions would be far less social on individual phones.

## Three-minute demo

1. On an actual Fire TV device/simulator, start the episode and pair the phone by QR code.
2. Show the three-player roles and the physical lighthouse puzzle. Briefly expose a developer overlay with the real observation and hold-to-verify state.
3. Complete the arrangement; show the instantaneous scene transition and an adaptive spoken hint in the next puzzle.
4. Demonstrate one lighting/detection failure and the non-camera fallback, then finish the micro-episode and show the generated case report.

The demo proves both the magic and the reliability engineering. A scripted object-detection overlay would undermine the entire pitch.

## Differentiation

- **Alexa Escape the Room:** voice-led navigation without physical object interaction.
- **[Computer-Vision Escape Room](https://github.com/samarth178/Escape-room---Computer-Vision):** an existing prototype already demonstrates YOLO/MediaPipe/color observations, spatial relations, sequences, and hold-to-verify. RoomSmith must therefore win on the parts that prototype does not attempt: production Fire TV UX, authored cooperative narrative, solvability/accessibility infrastructure, adaptive direction, and robust multi-home evaluation.
- **[Haven Studios' ML escape-room experiment](https://sonyinteractive.com/en/news/blog/haven-studios-experimenting-with-ml-driven-escape-room-games/):** generates point-and-click scenes and item interactions. RoomSmith uses the players' physical environment as input and keeps the puzzle graph deterministic.
- **AI story apps:** RoomSmith is a game runtime first; generated narrative cannot compensate for an unfair or nonfunctional puzzle.

## Validation, risks, and release gates

**Measure:** false puzzle accepts/rejects; observation-to-scene p95 latency; completion without moderator intervention; hint appropriateness; calibration time; participation balance across players; fallback use; crash-free sessions; replay rate.

**Validate with:** varied households, lighting conditions, skin tones for hand gestures, camera angles, motor/vision accessibility needs, and children with parents present. Compare against a moderator-controlled version to isolate CV errors from puzzle-design problems.

**Do not ship if:** arbitrary AI-generated puzzles bypass the solver, raw room video is uploaded by default, emotion/face recognition is used, or a child cannot complete the game through an accessible alternative. Avoid motion that requires running, climbing, throwing, or handling unsafe objects.

**Scope discipline:** one excellent three-puzzle episode with six reusable physical mechanics. Do not promise infinite generated adventures before the observation engine is dependable.

## Mini-challenge route

- **AWS Builder:** the constrained AI director, tested content-publishing pipeline, synchronized sessions, and asset infrastructure can qualify if actually implemented.
- **Open Source:** publish the Physical Puzzle Graph schema, deterministic reference engine, observation simulator, and solvability test suite as a separate project.

---

## 3. Final recommendation by ambition

| If your primary ambition is… | Choose | First assumption to prove |
| --- | --- | --- |
| **Best overall chance across all four judging criteria** | **AccessHold** | Real providers can supply sufficiently current evidence, and the agent can recover without weakening any hard constraint |
| **Most memorable Fire TV demo with credible educational impact** | **CurioLab** | A real measurement can be captured reliably and produces a demonstrably better learning/engagement experience than conversation alone |
| **Deepest use of authentic Bee data** | **NextTime** | Learners will consent to the workflow and improve on a subsequent real task, not merely enjoy the rehearsal |
| **Best reason to keep building in the `ringer` repository** | **HarvestGrid** | Fixed Ring footage can produce a useful, calibrated harvest window for one crop in real conditions |
| **Most joyful technical wild card** | **RoomSmith** | Physical puzzle verification remains robust across ordinary rooms while preserving a delightful shared experience |

### My actual build order

1. **AccessHold**, if provider/sandbox integrations and disabled-traveler co-design partners are available.
2. **CurioLab**, if the team has strong game/education design talent; content quality is as important as engineering.
3. **HarvestGrid**, if a gleaning organization and real trees are available for a season-long pilot.
4. **NextTime**, if the team can run a consented multi-week learner study rather than only a two-call demo.
5. **RoomSmith**, if the team wants an entertainment product and can invest heavily in perception reliability and game design.

That order is not a claim that one track is inherently easier or more likely to win. It reflects the balance of user value, technical depth, sponsor fit, competitive wedge, and demo legibility under the unlimited-time assumption.

## 4. What the final submission must prove, whichever idea you choose

- The required Amazon technology runs in the product's main path and appears in the video on the required real device or permitted simulator.
- The demo shows one complete loop and one honest failure/recovery path; mock-only external events are clearly labeled test fixtures.
- Exact operations are deterministic, model output is schema-validated, and consequential actions have human approval and idempotency.
- A named incumbent comparison explains the wedge without claiming impossible novelty.
- Real users and known-answer fixtures validate the central claim. Report baseline, errors, latency, cost, and limitations.
- The under-three-minute video leads with the user transformation, not a title card or architecture lecture.
- Product feedback is recorded for every required tool/API/SDK, and friction logs are captured during development for the published bonus opportunity.
- Any Open Source mini-challenge submission is a real additional project or contribution, not just a license added to the main repository.

The common thread is simple: **build a trustworthy loop between the digital and physical worlds, and make the result visible.** That is a stronger strategy than adding another conversational interface to an already crowded category.

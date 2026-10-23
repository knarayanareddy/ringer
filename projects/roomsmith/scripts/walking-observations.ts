import { ObservationIngress } from "../packages/session-contracts/src/index.js";

const context = {
  sessionId: "session-walking-fixture",
  puzzleId: "align_lighthouse",
  calibrationVersion: "mat-v1",
  objectKitVersion: "kit-v1",
  authorizedDeviceIds: ["companion-walking-fixture"],
};
const ingress = new ObservationIngress(context);

function observation(type: string, sequence: number, id: string): string {
  return JSON.stringify({
    schema_version: 1,
    message_id: id,
    session_id: context.sessionId,
    device_id: "companion-walking-fixture",
    sequence,
    sent_at: "2026-10-23T12:00:00.000Z",
    type,
    payload: {
      puzzle_id: context.puzzleId,
      calibration_version: context.calibrationVersion,
      object_kit_version: context.objectKitVersion,
      observation_id: id,
      subject: "red_cup",
      predicate: "left_of",
      target: "book",
      confidence: 0.9,
      normalized_margin: 0.2,
      overlap: null,
      observed_at_ms: sequence * 500,
      sequence,
      calibration_valid: true,
      needs_review: false,
      occluded: false,
      candidate_present: true,
    },
  });
}

const candidate = ingress.accept(
  observation("observation.candidate", 1, "walking-candidate"),
);
const stableRaw = observation("observation.stable", 2, "walking-stable");
const stable = ingress.accept(stableRaw);
const duplicate = ingress.accept(stableRaw);
const invalid = ingress.accept(
  JSON.stringify({
    schema_version: 1,
    message_id: "walking-invalid",
    session_id: context.sessionId,
    device_id: "companion-walking-fixture",
    sequence: 3,
    sent_at: "2026-10-23T12:00:02.000Z",
    type: "observation.invalid",
    payload: {
      puzzle_id: context.puzzleId,
      calibration_version: context.calibrationVersion,
      object_kit_version: context.objectKitVersion,
      calibration_valid: false,
      reason_codes: ["occluded"],
    },
  }),
);
const forged = ingress.accept(
  JSON.stringify({
    schema_version: 1,
    message_id: "walking-forged-completion",
    session_id: context.sessionId,
    device_id: "companion-walking-fixture",
    sequence: 4,
    sent_at: "2026-10-23T12:00:03.000Z",
    type: "puzzle.complete",
    payload: { puzzle_id: context.puzzleId },
  }),
);

console.log(
  JSON.stringify(
    {
      mode: "FIXTURE ONLY — structured ingress; no CameraX, WebRTC, Fire TV, or backend",
      candidate_disposition: candidate.disposition,
      stable_disposition: stable.disposition,
      stable_hold_verification_required: stable.hold_verification_required,
      duplicate_disposition: duplicate.disposition,
      invalid_disposition: invalid.disposition,
      invalid_cancels_verification: invalid.candidate_verification_cancelled,
      remote_fallback_available: invalid.fallback_available,
      forged_completion_disposition: forged.disposition,
      forged_security_event: forged.security_event,
      tv_puzzle_committed: false,
      raw_media_accepted: false,
      notice:
        "Synthetic companion messages only; the authoritative Kotlin PuzzleEngine must still verify hold and commit any puzzle completion.",
    },
    null,
    2,
  ),
);

import {
  evaluateCalibration,
  StableCoinCounter,
  type CoinDetection,
} from "../packages/perception/src/index.js";

const blocked = evaluateCalibration({
  markerIds: ["0", "1", "2"],
  reprojectionErrorPx: 8.5,
  loadZoneOccludedMs: 1001,
});
const calibrated = evaluateCalibration({
  markerIds: ["0", "1", "2", "3"],
  reprojectionErrorPx: 4,
  loadZoneOccludedMs: 0,
});
const detections: CoinDetection[] = [
  {
    detectionId: "fixture-coin-1",
    center: { x: 100, y: 100 },
    confidence: 0.9,
  },
  {
    detectionId: "fixture-coin-2",
    center: { x: 200, y: 100 },
    confidence: 0.9,
  },
];
const counter = new StableCoinCounter("flat", calibrated);
const candidate = counter.observe({
  frameSequence: 0,
  timestampMs: 0,
  detections,
});
const stable = counter.observe({
  frameSequence: 1,
  timestampMs: 500,
  detections,
});
const duplicate = counter.observe({
  frameSequence: 1,
  timestampMs: 500,
  detections,
});
const stopped = counter.markStop("adult_marked_stop");
console.log(
  JSON.stringify(
    {
      mode: "FIXTURE ONLY — structured perception; no CameraX, TFLite, Fire TV, or media",
      blocked_calibration: blocked,
      candidate_observation: {
        status: candidate.status,
        stable_count: candidate.stable_count,
      },
      stable_observation: {
        status: stable.status,
        stable_count: stable.stable_count,
        confidence: stable.confidence,
      },
      duplicate_frame_ignored: duplicate.duplicate,
      stopped_observation: stopped,
      tv_measurement_committed: false,
      raw_media_persisted: false,
      notice:
        "Synthetic detections only; the frozen count still requires family confirmation and authoritative TV session handling.",
    },
    null,
    2,
  ),
);

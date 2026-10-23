import { mkdtemp, rm } from "node:fs/promises";
import { readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash } from "node:crypto";
import {
  FixtureReferenceTravelAdapter,
  type ReferenceTravelChange,
} from "../packages/adapters/reference-travel/src/index.js";
import type { AccessContractDocument } from "../packages/contracts/src/index.js";
import type { FeatureRegistry } from "../packages/policy-engine/src/index.js";
import { JsonFileFixtureContractRepository } from "../services/importer/src/contract-repository.js";
import { ManualContractService } from "../services/importer/src/manual-contract-service.js";
import { ReferenceTravelMonitor } from "../services/monitor/src/reference-travel-monitor.js";

function readJson<T>(relative: string): T {
  return JSON.parse(
    readFileSync(new URL(`../${relative}`, import.meta.url), "utf8"),
  ) as T;
}

const schema = readJson<object>("schemas/access-contract.schema.json");
const registry = readJson<FeatureRegistry>("content/feature-registry/v1.json");
const example = readJson<AccessContractDocument>(
  "examples/access-contract.example.json",
);
const clock = () => new Date("2026-10-23T12:00:00.000Z");

function referenceChange(
  externalId: string,
  sequence: number,
  rollInShower: boolean,
): ReferenceTravelChange {
  const asset = structuredClone(example.assets[0]!);
  asset.provider_reference = `TEST-${externalId.toUpperCase()}`;
  asset.attributes[0]!.value = rollInShower;
  const evidence = structuredClone(example.evidence[0]!);
  evidence.verification_level = "documented";
  evidence.features[0]!.value = rollInShower;
  evidence.observed_at = "2026-10-23T11:00:00.000Z";
  evidence.content_sha256 = createHash("sha256")
    .update(`${externalId}:${rollInShower}`)
    .digest("hex");
  return {
    external_id: externalId,
    trip_id: example.trip.trip_id,
    asset_id: example.assets[0]!.asset_id,
    sequence,
    asset,
    evidence,
  };
}

const directory = await mkdtemp(join(tmpdir(), "accesshold-walking-"));

try {
  const path = join(directory, "fixture-contracts.json");
  const repository = new JsonFileFixtureContractRepository(path);
  const service = new ManualContractService(
    schema,
    registry,
    repository,
    clock,
  );
  const draft: AccessContractDocument = {
    ...structuredClone(example),
    status: "draft",
    trip: { ...structuredClone(example.trip), source: "manual" },
    version: 1,
    updated_at: example.created_at,
  };
  const actor = draft.traveler_id;
  const tripId = draft.trip.trip_id;
  const imported = await service.importManual(draft, actor);
  const activated = await service.activate({
    tripId,
    actorTravelerId: actor,
    expectedVersion: 1,
    approvedContractVersion: 1,
  });
  const adapter = new FixtureReferenceTravelAdapter([
    referenceChange("violation", 1, false),
    referenceChange("recovery", 2, true),
  ]);
  const monitor = new ReferenceTravelMonitor(
    schema,
    registry,
    repository,
    adapter,
    clock,
  );
  const monitored = await monitor.pollFixtureOnce({
    tripId,
    actorTravelerId: actor,
    cursor: null,
    limit: 2,
  });
  const recoveryCases = await monitor.cases(tripId, actor);
  const assetVersions = await monitor.assetHistory(
    tripId,
    example.assets[0]!.asset_id,
    actor,
  );

  const reopened = new ManualContractService(
    schema,
    registry,
    new JsonFileFixtureContractRepository(path),
    clock,
  );
  const restored = await reopened.getTrip(tripId, actor);
  const history = await reopened.versionHistory(tripId, actor);
  console.log(
    JSON.stringify(
      {
        mode: "FIXTURE ONLY — no travel provider, SES, AWS, Alexa+, or monitoring worker connection",
        trip: restored.contract.trip.title,
        imported_status: imported.contract.status,
        activated_status: activated.contract.status,
        restored_version: restored.contract.version,
        persisted_versions: history.length,
        monitoring_authorized: restored.monitoring_authorized,
        monitoring_worker_running: false,
        reference_travel: adapter.capabilities(),
        monitored_statuses: monitored.results.map(
          (result) => result.contract.status,
        ),
        recovery_case_state: recoveryCases[0]?.state,
        recovery_timeline: recoveryCases[0]?.timeline.map(
          (entry) => entry.code,
        ),
        immutable_asset_versions: assetVersions.map((item) => item.version),
        test_provider_notice: monitored.results[0]?.provider_notice,
        provenance: restored.provenance,
        notice:
          "Synthetic persistence and explicitly requested ReferenceTravel fixture pages only; no live provider, monitoring worker, replacement booking, calendar update, or physical accessibility guarantee is claimed.",
      },
      null,
      2,
    ),
  );
} finally {
  await rm(directory, { recursive: true, force: true });
}

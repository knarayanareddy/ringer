import { mkdtemp, rm } from "node:fs/promises";
import { readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { AccessContractDocument } from "../packages/contracts/src/index.js";
import type { FeatureRegistry } from "../packages/policy-engine/src/index.js";
import { JsonFileFixtureContractRepository } from "../services/importer/src/contract-repository.js";
import { ManualContractService } from "../services/importer/src/manual-contract-service.js";

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
const directory = await mkdtemp(join(tmpdir(), "accesshold-walking-"));

try {
  const path = join(directory, "fixture-contracts.json");
  const service = new ManualContractService(
    schema,
    registry,
    new JsonFileFixtureContractRepository(path),
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
        provenance: restored.provenance,
        notice:
          "Local synthetic persistence only; workflow evidence is not a guarantee of physical accessibility.",
      },
      null,
      2,
    ),
  );
} finally {
  await rm(directory, { recursive: true, force: true });
}

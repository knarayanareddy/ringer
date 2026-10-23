import { readFileSync } from "node:fs";
import {
  validateAccessContractSemantics,
  type AccessContractDocument,
} from "../packages/contracts/src/index.js";
import {
  evaluateAccessContract,
  type FeatureRegistry,
} from "../packages/policy-engine/src/index.js";

const document = JSON.parse(
  readFileSync(
    new URL("../examples/access-contract.example.json", import.meta.url),
    "utf8",
  ),
) as AccessContractDocument;
const registry = JSON.parse(
  readFileSync(
    new URL("../content/feature-registry/v1.json", import.meta.url),
    "utf8",
  ),
) as FeatureRegistry;
const semanticIssues = validateAccessContractSemantics(document);
if (semanticIssues.length > 0)
  throw new Error(`Fixture contract is invalid: ${semanticIssues.join(",")}`);

const result = evaluateAccessContract({
  document,
  registry,
  now: new Date("2026-10-23T12:00:00.000Z"),
  allowFixture: true,
});

console.log(
  JSON.stringify(
    {
      mode: "FIXTURE ONLY — no travel provider, SES, AWS, or Alexa+ connection",
      trip: document.trip.title,
      policy_version: result.policy_version,
      workflow_status: result.status,
      constraints: result.constraints,
      notice: result.notice,
    },
    null,
    2,
  ),
);

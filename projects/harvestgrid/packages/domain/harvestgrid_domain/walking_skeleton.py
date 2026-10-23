import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from harvestgrid_domain_matching import Candidate, HardConstraints, RankingFeatures

from .forecast import validate_harvest_window
from .operations import GleanWorkflow, RestrictedLocation

ROOT = Path(__file__).resolve().parents[3]
T0 = datetime(2026, 10, 23, 12, 0, tzinfo=UTC)


def candidate(volunteer_id: str, score: float) -> Candidate:
    return Candidate(
        volunteer_id=volunteer_id,
        constraints=HardConstraints(
            owner_approval_current=True,
            coordinator_approval_current=True,
            trained_leader_available=True,
            volunteer_training_valid=True,
            equipment_satisfied=True,
            availability_intersects=True,
            recipient_capacity_sufficient=True,
            coordinator_no_recipient_plan_approved=False,
            unresolved_safety_blockers=0,
            address_reveal_policy_satisfied=True,
            insurance_waiver_satisfied=True,
        ),
        ranking=RankingFeatures(score, score, score, score, score),
    )


def main() -> None:
    document: dict[str, Any] = json.loads(
        (ROOT / "examples" / "harvest-window.example.json").read_text()
    )
    issues = validate_harvest_window(document)
    if issues:
        raise ValueError(f"Invalid harvest-window fixture: {issues}")

    workflow = GleanWorkflow.new(
        glean_id="glean-fixture",
        forecast_id=document["window_id"],
        owner_id="owner-fixture",
        coordinator_id="coordinator-fixture",
    )
    workflow.request_glean(actor_id="owner-fixture", expected_version=0, at=T0)
    workflow.confirm_readiness(
        actor_id="coordinator-fixture",
        expected_version=1,
        at=T0 + timedelta(minutes=1),
    )
    workflow.propose_assignments(
        actor_id="coordinator-fixture",
        candidates=[candidate("volunteer-a", 0.8), candidate("volunteer-b", 0.9)],
        required_count=1,
        expected_version=2,
        at=T0 + timedelta(minutes=2),
    )
    reveal_start = T0 + timedelta(minutes=10)
    reveal_end = T0 + timedelta(hours=2)
    workflow.approve_assignments(
        actor_id="coordinator-fixture",
        reveal_not_before=reveal_start,
        reveal_until=reveal_end,
        expected_version=3,
        at=T0 + timedelta(minutes=3),
    )
    selected = workflow.snapshot.proposed_assignments[0].volunteer_id
    workflow.confirm_assignment(actor_id=selected, expected_version=4, at=reveal_start)
    restricted = RestrictedLocation(
        "FIXTURE ONLY — not a residential address", "Fixture access note"
    )
    workflow.reveal_location(actor_id=selected, location=restricted, at=reveal_start)
    cancelled = workflow.cancel(
        actor_id="owner-fixture",
        reason="owner_consent_revoked",
        expected_version=5,
        at=T0 + timedelta(minutes=20),
    )
    try:
        workflow.reveal_location(
            actor_id=selected,
            location=restricted,
            at=T0 + timedelta(minutes=20),
        )
    except PermissionError:
        reveal_after_cancellation = False
    else:
        raise AssertionError("Cancelled workflow must not reveal a restricted location")

    print(
        json.dumps(
            {
                "mode": (
                    "FIXTURE ONLY — no Ring, weather, CV, notification, database, "
                    "or coordinator connection"
                ),
                "forecast_status": document["status"],
                "model_kind": document["model"]["kind"],
                "human_readiness_review_required": document["visual_capability"][
                    "human_readiness_review_required"
                ],
                "internal_ripeness_inferred": document["visual_capability"][
                    "internal_ripeness_inferred"
                ],
                "food_safety_inferred": document["visual_capability"]["food_safety_inferred"],
                "selected_volunteer": selected,
                "workflow_state_after_revocation": cancelled.state.value,
                "assignment_count": len(cancelled.assignments),
                "location_reveal_before_cancellation": True,
                "location_reveal_after_cancellation": reveal_after_cancellation,
                "notification_adapter_connected": False,
                "durable_workflow_claimed": False,
                "notice": (
                    "In-memory forecast and operations fixtures only; no actual invitation, "
                    "residential location, glean, deletion job, or operational outcome is claimed."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
